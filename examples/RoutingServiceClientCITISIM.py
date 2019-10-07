#!/usr/bin/python3
# -*- coding: utf-8; mode: python -*-

import sys
import Ice
import random

from libcitisim import SmartServices


class RoutingServiceClientCITISIM(Ice.Application):
    def run(self, argv):
        ic = self.communicator()

        # Local proxy
        # proxy = "RoutingService -t:tcp -h 127.0.0.1 -p 9093"
        proxy = "RoutingService"

        proxy = ic.stringToProxy(proxy)
        self.routingServicePrx = SmartServices.RoutingServicePrx.checkedCast(proxy)
        self.calculatePathBetweenCells()

    def calculatePathBetweenCells(self):
        try:
            # path = self.routingServicePrx.getPath("CELL_8CCRX3XJ+45P", "CELL_8CCRX3VJ+X3P")
            # print("Path ITSI_entrance-roundabout:" + str(path))

            path = self.routingServicePrx.getPath("CELL_LABORATORY.11", "CELL_8CCRX3VJ+X3P")
            print("Path ArcoLab-roundabout:" + str(path))

        except Exception:
            print("No path between cells.")

sys.exit(RoutingServiceClientCITISIM().main(sys.argv))
