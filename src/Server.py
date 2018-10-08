#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-

import sys
import Ice
import uuid
import xml.etree.ElementTree as ET
import networkx as nx
from shapely.geometry import Point
from shapely.geometry import Polygon
from IndoorGMLreader import IndoorGMLreader

sys.path.insert(0, '../lib')
import openlocationcode as olc

Ice.loadSlice('../slice/UrbanService.ice')
import UrbanService


class IgmlLayerI(UrbanService.IgmlLayer):
    def __init__(self, model):
        self.model = model

    def isConnectedCell(self, referenceCellID, cellToCheqID, current=None):
        spaceLayerID = self.model.getLayerOfaCell(referenceCellID)
        referenceCellSpace = self.model.getCellreference(referenceCellID)
        cellSpaceToCheq = self.model.getCellreference(cellToCheqID)

        referenceCellSpace_duality = referenceCellSpace.duality
        cellSpaceToCheq_duality = cellSpaceToCheq.duality

        return cellSpaceToCheq_duality in self.model.spaceLayers[spaceLayerID].neighbors(referenceCellSpace_duality)

    def isAdjacentCell(self, referenceCellID, cellToCheqID, current=None):
        referenceCellSpace = self.model.getCellreference(referenceCellID)
        cellSpaceToCheq = self.model.getCellreference(cellToCheqID)

        referenceCellSpaceBoundaries = referenceCellSpace.cellSpaceBoundaries
        cellSpaceToCheqBoundaries = cellSpaceToCheq.cellSpaceBoundaries

        return any(cellSpaceToCheqBoundary in referenceCellSpaceBoundaries for cellSpaceToCheqBoundary in cellSpaceToCheqBoundaries)

    def getConnectedCells(self, referenceCellID, current=None):
        connectedCells = []
        spaceLayerID = self.model.getLayerOfaCell(referenceCellID)
        referenceCellSpace = self.model.getCellreference(referenceCellID)
        referenceCellSpace_duality = referenceCellSpace.duality

        for neighbor in self.model.spaceLayers[spaceLayerID].neighbors(referenceCellSpace_duality):
            connectedCells.append(
                self.model.spaceLayers[spaceLayerID].nodes[neighbor]['obj'].duality)

        return connectedCells

    def getAdjacentCells(self, referenceCellID, current=None):
        adjacentCells = []

        for cellToCheqID in self.model.CellSpaces:
            if self.isAdjacentCell(referenceCellID, cellToCheqID) and cellToCheqID != referenceCellID:
                adjacentCells.append(cellToCheqID)

        return adjacentCells

    def getCellSpaceBoundariesBetweenCells(self, referenceCellID1, referenceCellID2, current=None):
        cellSpaceBoundariesID = []
        cellSpace1 = self.model.getCellreference(referenceCellID1)
        cellSpace2 = self.model.getCellreference(referenceCellID2)

        cellSpace1Boundaries = cellSpace1.cellSpaceBoundaries
        cellSpace2Boundaries = cellSpace2.cellSpaceBoundaries

        for cellSpace1Boundary in cellSpace1Boundaries:
            if(cellSpace1Boundary in cellSpace2Boundaries):
                cellSpaceBoundariesID.append(cellSpace1Boundary)

        return cellSpaceBoundariesID

    def getCells(self, spaceLayerID, current=None):
        cells = []

        for cellToCheq in self.model.CellSpaces.values():
            if(self.model.getLayerOfaCell(cellToCheq.id) == spaceLayerID):
                cells.append(cellToCheq)

        return cells

    def getCellSpaceBoundaries(self, spaceLayerID, current=None):
        cellSpaceBoundaries = []

        for cellSpaceBoundary in self.model.cellSpaceBoundaries.values():
            if(self.model.getLayerOfaBoundary(cellSpaceBoundary.id) == spaceLayerID):
                cellSpaceBoundaries.append(cellSpaceBoundary)

        return cellSpaceBoundaries

    def getStates(self, spaceLayerID, current=None):
        return(list(nx.get_node_attributes(self.model.spaceLayers[spaceLayerID], 'obj').values()))

    def getTransitions(self, spaceLayerID, current=None):
        return(list(data['obj'] for node1, node2,
                    data in self.model.spaceLayers[spaceLayerID].edges(data=True)))

    def getUsage(self, referenceCellID, current=None):
        referenceCellSpace = self.model.getCellreference(referenceCellID)
        return referenceCellSpace.usage

    def getName(self, referenceCellID, current=None):
        referenceCellSpace = self.model.getCellreference(referenceCellID)
        return referenceCellSpace.name

    def getHeight(self, referenceCellID, current=None):
        referenceCellSpace = self.model.getCellreference(referenceCellID)
        surfaces = referenceCellSpace.geometry.surfaces

        z_base_coord = surfaces[len(surfaces) - 1].linearRing[0].z
        z_roof_coord = surfaces[0].linearRing[0].z

        return z_roof_coord - z_base_coord

    def getExits(self, referenceCellID, current=None):
        exits = []
        referenceCellSpace = self.model.getCellreference(referenceCellID)
        for cellSpaceBoundary in referenceCellSpace.cellSpaceBoundaries:
            if(self.model.cellSpaceBoundaries[cellSpaceBoundary].usage == 'Door'):
                exits.append(cellSpaceBoundary)

        return exits

    def getEntrances(self, spaceLayerID, current=None):
        entrances = []
        for cellSpace_id, cellSpace in self.model.CellSpaces.items():
            if(cellSpace.usage == 'Entrance' and self.model.getLayerOfaCell(cellSpace_id) == spaceLayerID):
                entrances.append(cellSpace_id)
        return entrances

    def getSpaceLayersID(self, current=None):
        return self.model.get_SpaceLayers_id()

    def getCellofPosition(self, spaceLayerID, position, current=None):
        return self.model.findCellIDofPointInKDTree(spaceLayerID, position)

    def isPositionInCell(self, position, cell, current=None):
        z_coord_of_position_ground = self.model.calculateGroundOfPosition(
            position.z)
        point = [position.x, position.y, z_coord_of_position_ground]
        for value in self.model.shapePoligons.values():
            if(value[0] == cell):
                return(value[1].contains(Point(point)))

    def getPathCellToCell(self, spaceLayerID, CellIDfrom, CellIDto, current=None):
        cellSpaceFrom = self.model.getCellreference(CellIDfrom).duality
        cellSpaceTo = self.model.getCellreference(CellIDto).duality

        nodes = nx.dijkstra_path(
            self.model.spaceLayers[spaceLayerID], cellSpaceFrom, cellSpaceTo)

        result = []
        for n in nodes:
            result.append(
                self.model.spaceLayers[spaceLayerID].nodes[n]['obj'].duality)

        return result

    def getPathPositionToPosition(self, spaceLayerID, positionFrom, positionTo, current=None):
        cellIDfrom = self.getCellofPosition(spaceLayerID, positionFrom)
        cellIDTo = self.getCellofPosition(spaceLayerID, positionTo)
        return self.getPathCellToCell(spaceLayerID, cellIDfrom, cellIDTo)

class GeoHashingI(UrbanService.GeoHashing):
    def __init__(self, dataFile):
        self.dataFile = dataFile
        self.buildingsPolygon = {}
        self.readOSM()

    def readOSM(self, current=None):
        tree = ET.parse(self.dataFile)

        for way in tree.iterfind('way'):
            if way.find('tag[@k="building"]') is not None and way.find('tag[@k="name"]') is not None:
                points = []
                name = (way.find('tag[@k="name"]').attrib['v'])

                for nd in way.iterfind('nd'):
                    ref = nd.attrib['ref']
                    node = tree.find("node" + "[@id='" + ref +"']")
                    
                    lat = node.attrib['lat']
                    lon = node.attrib['lon']
                    points.append([float(lat), float(lon)])

                self.buildingsPolygon[name] = Polygon(points)

    def encode(self, position, codeLength, current=None):
        return olc.encode(position.x, position.y, codeLength)

    def decode(self, code, current=None):
        result = olc.decode(code)
        return UrbanService.CodeArea(
            result.latitudeLo, result.longitudeLo,                            result.latitudeHi, result.longitudeHi,                           result.codeLength, result.latitudeCenter,                        result.longitudeCenter)

    def isValid(self, code, current=None):
        return olc.isValid(code)

    def getNeighbourCodeAreas(self, code, current=None):
        codeArea = self.decode(code)
        centerOfArea = [codeArea.latitudeCenter, codeArea.longitudeCenter]

        longitudeOffset = (1.0/32000)
        latitudeOffset = (1.0/40000)

        rightCenter = self.encode(
            UrbanService.position3D(
                centerOfArea[0], 
                centerOfArea[1] + longitudeOffset), 
            11)

        leftCenter = self.encode(
            UrbanService.position3D(
                centerOfArea[0], 
                centerOfArea[1] - longitudeOffset), 
            11)


        upCenter = self.encode(
            UrbanService.position3D(
                centerOfArea[0] + latitudeOffset, 
                centerOfArea[1]), 
            11)

        downCenter = self.encode(
            UrbanService.position3D(
                centerOfArea[0] - latitudeOffset, 
                centerOfArea[1]), 
            11)


        return [rightCenter, leftCenter, upCenter, downCenter]

    def getPolygonOpenLocationCode(self, code, current=None):
        codeArea = self.decode(code)
        return Polygon([ [codeArea.latitudeLo,codeArea.longitudeLo],      
                            [codeArea.latitudeHi, codeArea.longitudeLo], [codeArea.latitudeHi,codeArea.longitudeHi], [codeArea.latitudeLo, codeArea.longitudeHi],
                            [codeArea.latitudeLo,codeArea.longitudeLo] ])

    def getCellsOfBuilding(self, buildingPolygon, current=None):
        proccesedOpenLocationCode = []
        result = []

        initialOpenLocationCode = self.encode(
            UrbanService.position3D(buildingPolygon.centroid.x,       
                                    buildingPolygon.centroid.y), 
            11)

        queue = [initialOpenLocationCode] + self.getNeighbourCodeAreas(initialOpenLocationCode)

        while queue:
            openLocationCode = queue.pop(0)
            proccesedOpenLocationCode.append(openLocationCode)

            if buildingPolygon.intersects(self.getPolygonOpenLocationCode(openLocationCode)):
                result.append(openLocationCode)
            else:
                continue

            neighbours = self.getNeighbourCodeAreas(openLocationCode)

            for neighbour in neighbours:
                if neighbour not in proccesedOpenLocationCode and neighbour not in queue:
                    queue.append(neighbour)

        return result

    def getBuilding(self, name, current=None):
        openLocationCodes = self.getCellsOfBuilding(self.buildingsPolygon[name])
        buildingUUID = uuid.uuid3(
            uuid.NAMESPACE_DNS, 
            "".join(openLocationCodes))

        return UrbanService.building(name, str(buildingUUID), openLocationCodes)

class Server(Ice.Application):
    def __init__(self):
        self.model = IndoorGMLreader(sys.argv[1])

    def run(self, argv):
        broker = self.communicator()

        servant = IgmlLayerI(self.model)
        adapter = broker.createObjectAdapter("IgmlLayerAdapter")
        proxy = adapter.add(servant, broker.stringToIdentity("IgmlLayer1"))
        adapter.activate()
        self.create_proxy_file("IgmlLayer1", proxy)
        print(proxy)

        servant = GeoHashingI(sys.argv[2])
        adapter = broker.createObjectAdapter("GeoHashingAdapter")
        proxy = adapter.add(servant, broker.stringToIdentity("GeoHashing1"))
        adapter.activate()
        self.create_proxy_file("GeoHashing1", proxy)
        print(proxy)

        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0

    def create_proxy_file(self, name, proxy):
        file = open(name + ".txt","w") 
        file.write(str(proxy))
        file.close()

server = Server()
sys.exit(server.main(sys.argv))
