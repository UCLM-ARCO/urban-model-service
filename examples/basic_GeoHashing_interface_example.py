#!/usr/bin/python3
# -*- coding: utf-8; mode: python -*-

import sys
import Ice
import random

Ice.loadSlice('../slice/UrbanService.ice')
import UrbanService

class GeoHashingExample(Ice.Application):
    def run(self, argv):
        broker = Ice.initialize()

        try:
            with open('../src/GeoHashing1.txt', 'r') as f:
                strproxy = f.readline()
        except IOError:
            print('Please, first start the service and then run again.')
            exit(1)

        proxy = broker.stringToProxy(strproxy)
        self.GeoHashing = UrbanService.GeoHashingPrx.checkedCast(proxy)

        self.retrievesInformationAboutBuilfing("Instituto de Tecnologías y Sistemas de Información")

        broker.destroy()

    def retrievesInformationAboutBuilfing(self, building_name):
        building_info = self.GeoHashing.getBuilding(building_name)
        openLocationCodes = building_info.openLocationCodes
        name = building_info.name
        uuid = building_info.uuid

        print(name)
        print(uuid)
        print(openLocationCodes)
    

sys.exit(GeoHashingExample().main(sys.argv))
