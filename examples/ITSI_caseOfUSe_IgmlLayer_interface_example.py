#!/usr/bin/python3
# -*- coding: utf-8; mode: python -*-

import sys
import Ice
import random

Ice.loadSlice('../slice/UrbanService.ice')
import UrbanService


class IgmlLayerExample(Ice.Application):
    def run(self, argv):
        self.spaceLayerID = 'olc-layer'
        broker = Ice.initialize()

        try:
            with open('../src/IgmlLayer1.txt', 'r') as f:
                strproxy = f.readline()
        except IOError:
            print('Please, first start the service and then run again.')
            exit(1)

        proxy = broker.stringToProxy(strproxy)
        self.igmlLayer = UrbanService.IgmlLayerPrx.checkedCast(proxy)

        self.calculatePathBetweenCells()

        broker.destroy()

    def calculatePathBetweenCells(self):
        try:
            # # Entrada ITSI-Rotonda
            # path = self.igmlLayer.getPathCellToCell(self.spaceLayerID,
            #     "CELL_8CCRX3XJ+45P", "CELL_8CCRX3VJ+X3P")

            # Entrada ITSI-Rotonda
            path = self.igmlLayer.getPathCellToCell(self.spaceLayerID,
                "CELL_LABORATORY.11", "CELL_8CCRX3VJ+X3P")
            print("Path between cells:" + str(path))
        except Exception:
            print("No path between cells.")

sys.exit(IgmlLayerExample().main(sys.argv))
