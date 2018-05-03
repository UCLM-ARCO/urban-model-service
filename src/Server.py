#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-

import sys
import Ice
import networkx as nx

from IndoorGMLreader import IndoorGMLreader

Ice.loadSlice('../slice/UrbanService.ice')
import UrbanService


class TopologyLayerI(UrbanService.TopologyLayer):
    def __init__(self, model):
        self.model = model
        self.topologyLayer_graph = self.model.spaceLayers['TOPOLOGY']

    def getCellreference(self, cellID):
        if cellID in self.model.CellSpaces:
            return self.model.CellSpaces[cellID]
        else:
            raise Exception('Invalid cellID')

    def isConnectedCell(self, referenceCellID, cellToCheqID, current=None):
        referenceCellSpace = self.getCellreference(referenceCellID)
        cellSpaceToCheq = self.getCellreference(cellToCheqID)

        referenceCellSpace_duality = referenceCellSpace.duality
        cellSpaceToCheq_duality = cellSpaceToCheq.duality

        return cellSpaceToCheq_duality in self.topologyLayer_graph.neighbors(referenceCellSpace_duality)

    def isAdjacentCell(self, referenceCellID, cellToCheqID, current=None):
        referenceCellSpace = self.getCellreference(referenceCellID)
        cellSpaceToCheq = self.getCellreference(cellToCheqID)

        referenceCellSpaceBoundarys = referenceCellSpace.cellSpaceBoundarys
        cellSpaceToCheqBoundarys = cellSpaceToCheq.cellSpaceBoundarys

        return any(cellSpaceToCheqBoundary in referenceCellSpaceBoundarys for cellSpaceToCheqBoundary in cellSpaceToCheqBoundarys)

    def getConnectedCells(self, referenceCellID, current=None):
        connectedCells = []
        referenceCellSpace = self.getCellreference(referenceCellID)
        referenceCellSpace_duality = referenceCellSpace.duality

        for neighbor in self.topologyLayer_graph.neighbors(referenceCellSpace_duality):
            connectedCells.append(
                self.topologyLayer_graph.nodes[neighbor]['obj'].duality)

        return connectedCells

    def getAdjacentCells(self, referenceCellID, current=None):
        adjacentCells = []

        for cellToCheqID in self.model.CellSpaces:
            if self.isAdjacentCell(referenceCellID, cellToCheqID) and cellToCheqID != referenceCellID:
                adjacentCells.append(cellToCheqID)

        return adjacentCells

    def getCells(self, current=None):
        return list(self.model.CellSpaces.values())

    def getCellSpaceBoundarys(self, current=None):
        return list(self.model.CellSpaceBoundarys.values())

    def getStates(self, current=None):
        return(list(nx.get_node_attributes(self.topologyLayer_graph, 'obj').values()))

    def getTransitions(self, current=None):
        return(list(data['obj'] for node1, node2,
                    data in self.topologyLayer_graph.edges(data=True)))

    def getUsage(self, referenceCellID, current=None):
        referenceCellSpace = self.getCellreference(referenceCellID)
        return referenceCellSpace.usage

    def getName(self, referenceCellID, current=None):
        referenceCellSpace = self.getCellreference(referenceCellID)
        return referenceCellSpace.name

    def getHeight(self, referenceCellID, current=None):
        referenceCellSpace = self.getCellreference(referenceCellID)
        surfaces = referenceCellSpace.geometry.surfaces
        return surfaces[0][0].z - surfaces[len(surfaces) - 1][0].z

    def getExits(self, referenceCellID, current=None):
        exits = []
        referenceCellSpace = self.getCellreference(referenceCellID)
        for cellSpaceBoundary in referenceCellSpace.cellSpaceBoundarys:
            if(self.model.CellSpaceBoundarys[cellSpaceBoundary].usage == 'Door'):
                exits.append(cellSpaceBoundary)

        return exits

    def getEntrances(self, current=None):
        entrances = []
        for cellSpace_id, cellSpace in self.model.CellSpaces.items():
            if(cellSpace.usage == 'Entrance'):
                entrances.append(cellSpace_id)
        return entrances

    def getCellofPosition(self, position, current=None):
        return self.model.findCellIDofPointInKDTree(position)

    def getPathCellToCell(self, CellIDfrom, CellIDto, current=None):
        cellSpaceFrom = self.getCellreference(CellIDfrom).duality
        cellSpaceTo = self.getCellreference(CellIDto).duality

        nodes = nx.dijkstra_path(
            self.topologyLayer_graph, cellSpaceFrom, cellSpaceTo)

        result = []
        for n in nodes:
            result.append(self.topologyLayer_graph.nodes[n]['obj'].duality)

        return result

    def getPathPositionToPosition(self, positionFrom, positionTo, current=None):
        cellIDfrom = self.getCellofPosition(positionFrom)
        cellIDTo = self.getCellofPosition(positionTo)
        return self.getPathCellToCell(cellIDfrom, cellIDTo)


class Server(Ice.Application):
    def __init__(self):
        self.model = IndoorGMLreader(sys.argv[1])

    def run(self, argv):
        broker = self.communicator()
        servant = TopologyLayerI(self.model)

        adapter = broker.createObjectAdapter("TopologyLayerAdapter")
        proxy = adapter.add(servant, broker.stringToIdentity("topologyLayer1"))

        print(proxy)
        sys.stdout.flush()

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0


server = Server()
sys.exit(server.main(sys.argv))
