#!/usr/bin/python3
# -*- coding: utf-8; mode: python -*-

import sys
import Ice
import random

Ice.loadSlice('../slice/UrbanService.ice')
import UrbanService


class IgmlLayerClient(Ice.Application):
    def run(self, argv):
        self.spaceLayerID = 'TOPOLOGY'
        broker = Ice.initialize()

        try:
            with open('IgmlLayer1.txt', 'r') as f:
                strproxy = f.readline()
        except IOError:
            print('Please, first start the service and then run again.')
            exit(1)

        proxy = broker.stringToProxy(strproxy)
        self.igmlLayer = UrbanService.IgmlLayerPrx.checkedCast(proxy)

        random_cells_id = self.getRandomCellsIds()
        self.getInfoAboutCellFromId(random_cells_id[0])
        self.checkRelationBetweenCells(random_cells_id)

        broker.destroy()

    def getRandomCellsIds(self):
        cells = self.igmlLayer.getCells(self.spaceLayerID)
        random_cells = random.sample(cells, 2)
        random_cells_id = [cell.id for cell in random_cells]
        for cell_id in random_cells_id:
            print("Random cell id: " + cell_id)

        return random_cells_id

    def getInfoAboutCellFromId(self, cell_id):
        cell_usage = self.igmlLayer.getUsage(cell_id)
        cell_name = self.igmlLayer.getName(cell_id)
        cell_height = self.igmlLayer.getHeight(cell_id)
        connceted_cells = self.igmlLayer.getConnectedCells(cell_id)
        adjacent_cells = self.igmlLayer.getAdjacentCells(cell_id)

        print("Info about cell with ID {}:\n Usage: {}\n Name: {}\n Height: {}\n Connected cells: {}\n Adjacent cells:{}".format(
            cell_id, cell_usage, cell_name, cell_height, str(connceted_cells), str(adjacent_cells)))

    def checkRelationBetweenCells(self, random_cells_id):
        is_connected = self.igmlLayer.isConnectedCell(
            random_cells_id[0], random_cells_id[1])
        is_adjacent = self.igmlLayer.isAdjacentCell(
            random_cells_id[0], random_cells_id[1])
        print("Check if connected cells: {}\nCheck if adjacents cells: {}".format(
            is_connected, is_adjacent))


sys.exit(IgmlLayerClient().main(sys.argv))
