#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-

import sys
import Ice
import networkx as nx
import xml.etree.ElementTree as ET


Ice.loadSlice('../slice/indoorGML.ice')
import UrbanService


class TopologyLayerI(UrbanService.TopologyLayer):
    def probarProxy(self, prueba, current=None):
        print(prueba)
        return prueba


class Server(Ice.Application):
    def __init__(self):
        # To-do
        topologyLayer = nx.Graph()

    def loadModel(self):
        # To-do

    def run(self, argv):
        broker = self.communicator()
        servant = TopologyLayerI()

        adapter = broker.createObjectAdapter("TopologyLayerAdapter")
        proxy = adapter.add(servant, broker.stringToIdentity("topologyLayer1"))

        print(proxy)
        sys.stdout.flush()
        print("--------------------------------------")

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0


server = Server()
sys.exit(server.main(sys.argv))
