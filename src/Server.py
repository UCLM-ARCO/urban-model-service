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

from libcitisim import SmartServices


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
            if(cellSpace.usage == 'Usage=Entrance' and self.model.getLayerOfaCell(cellSpace_id) == spaceLayerID):
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


class RoutingServiceI(SmartServices.RoutingService):
    def __init__(self, model):
        self.model = model

        if 'olc-layer' in  self.model.spaceLayers:
            self.spaceLayerID = 'olc-layer'
        else:
            self.spaceLayerID = 'TOPOLOGY'

    def dijkstra(self, graph, start, end):
        distances = {} 
        predecessors = {} 
        to_assess = graph.nodes 

        for node in graph.nodes:
            distances[node] = float('inf')
            predecessors[node] = None
        
        sp_set = []
        distances[start] = 0
        
        while len(sp_set) < len(to_assess):
            still_in = {node: distances[node]\
                        for node in [node for node in\
                        to_assess if node not in sp_set]}

            closest = min(still_in, key = distances.get)

            sp_set.append(closest)
            
            for node in graph[closest]:
                if distances[node] > distances[closest] +\
                        graph[closest][node]['weight']:

                    distances[node] = distances[closest] +\
                        graph[closest][node]['weight']

                    predecessors[node] = closest
                    
        path = [end]
        while start not in path:
            path.append(predecessors[path[-1]])
        
        return path[::-1], distances[end]

    def convertRoute(self, route):
        result = []

        for node in route:
            interLayerConnection = self.model.InterLayerConnections.get(node)
            if(interLayerConnection != None):
                if interLayerConnection.replace("STATE_", "CELL_") not in result:
                    result.append(interLayerConnection.replace("STATE_", "CELL_"))
            else:
                result.append(node.replace("STATE_", "CELL_"))

        return result

    def getPath(self, startPoint, endPoint, current=None):
        cellSpaceFrom = self.model.getCellreference(startPoint).duality
        cellSpaceTo = self.model.getCellreference(endPoint).duality

        nodes = nx.dijkstra_path(
            self.model.spaceLayers[self.spaceLayerID], cellSpaceFrom, cellSpaceTo)
        
        # nodes, distances= self.dijkstra(self.model.spaceLayers[self.spaceLayerID ], cellSpaceFrom, cellSpaceTo)

        route = []
        for n in nodes:
            route.append(
                self.model.spaceLayers[self.spaceLayerID].nodes[n]['obj'].id)
        #         self.model.spaceLayers[self.spaceLayerID ].nodes[n]['obj'].duality)
        # return route

        return self.convertRoute(route)

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

        servant = RoutingServiceI(self.model)
        adapter = broker.createObjectAdapter("RoutingServiceAdapter")
        proxy = adapter.add(servant, broker.stringToIdentity("RoutingService1"))
        adapter.activate()
        self.create_proxy_file("RoutingService1", proxy)
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
