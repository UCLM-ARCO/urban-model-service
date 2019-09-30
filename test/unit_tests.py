# -*- mode:python; coding:utf-8; tab-width:4 -*-
# !/usr/bin/python3

import Ice
from unittest import TestCase

Ice.loadSlice('../slice/UrbanService.ice')
import UrbanService

from libcitisim import SmartServices


class IgmlTests(TestCase):
    def setUp(self):
        broker = Ice.initialize()
        self.addCleanup(broker.destroy)
        self.spaceLayerID = 'TOPOLOGY'

        # FIXME: use a known proxy for testing
        # do not include testing related code on server!!
        try:
            with open('IgmlLayer1.txt', 'r') as f:
                strproxy = f.readline()
        except IOError as error:
            print('Please, first start the service and then run again.')

        proxy = broker.stringToProxy(strproxy)
        self.igmlLayer = UrbanService.IgmlLayerPrx.checkedCast(proxy)

    def test_if_two_cells_are_adjacent(self):
        referenceCellID = "CELL_LABORATORY.11"
        cellToCheqID = "CELL_LABORATORY.12"
        response = self.igmlLayer.isAdjacentCell(
            referenceCellID, cellToCheqID)
        self.assertTrue(response)

    def test_if_two_cells_are_not_adjacent(self):
        referenceCellID = "CELL_LABORATORY.11"
        cellToCheqID = "CELL_LABORATORY.15"
        response = self.igmlLayer.isAdjacentCell(
            referenceCellID, cellToCheqID)
        self.assertFalse(response)

    def test_if_two_cells_are_connected(self):
        referenceCellID = "CELL_LABORATORY.11"
        cellToCheqID = "CELL_CORRIDOR.1"
        response = self.igmlLayer.isConnectedCell(
            referenceCellID, cellToCheqID)
        self.assertTrue(response)

    def test_if_two_cells_are_not_connected(self):
        referenceCellID = "CELL_LABORATORY.11"
        cellToCheqID = "CELL_LABORATORY.15"
        response = self.igmlLayer.isConnectedCell(
            referenceCellID, cellToCheqID)
        self.assertFalse(response)

    def test_if_cell_not_exist(self):
        referenceCellID = "INVENTED_CELL"
        cellToCheqID = "CELL_CORRIDOR.1"

        with self.assertRaises(Exception):
            self.igmlLayer.isConnectedCell(referenceCellID, cellToCheqID)

    # # No sabemos si esta funcionalidad hará falta
    # def test_if_two_cells_are_accesible(self):
    #     referenceCellID = ""  # To-do
    #     cellToCheqID = ""  # To-do
    #     response = self.igmlLayer.isAccesibleCell(
    #         referenceCellID, cellToCheqID)
    #     self.assertTrue(response)
    #
    # def test_if_two_cells_are_not_accesible(self):
    #     referenceCellID = ""  # To-do
    #     cellToCheqID = ""  # To-do
    #     response = self.igmlLayer.isAccesibleCell(
    #         referenceCellID, cellToCheqID)
    #     self.assertFalse(response)

    def test_if_the_adjacent_ones_are_correct(self):
        referenceCellID = "CELL_LABORATORY.11"
        expected_response = ["CELL_LABORATORY.12",
                             "CELL_MEETINGROOM.2", "CELL_CORRIDOR.1"]
        response = self.igmlLayer.getAdjacentCells(referenceCellID)
        self.assertCountEqual(expected_response, response)

    def test_if_the_connected_ones_are_correct(self):
        referenceCellID = "CELL_HALL.8"
        expected_response = ["CELL_WAREHOUSE.7", "CELL_OFFICE.4",
                             "CELL_OFFICE.5", "CELL_LABORATORY.15", "CELL_CORRIDOR.1"]
        response = self.igmlLayer.getConnectedCells(referenceCellID)
        self.assertCountEqual(expected_response, response)

    # # No sabemos si esta funcionalidad hará falta
    # def test_if_the_accesible_ones_are_correct(self):
    #     referenceCellID = ""
    #     expected_response = ["", "", ""]
    #     response = self.igmlLayer.getAccesibleCells(referenceCellID)
    #     self.assertEqual(expected_response, response)

    def test_the_case_when_it_not_have_adjacents(self):
        referenceCellID = "CELL_FIRESTAIRS.0"
        expected_response = [""]
        response = self.igmlLayer.getAdjacentCells(referenceCellID)
        self.assertNotEqual(expected_response, response)

    def test_the_case_when_it_not_have_connected(self):
        referenceCellID = "CELL_FIRESTAIRS.0"
        expected_response = [""]
        response = self.igmlLayer.getConnectedCells(referenceCellID)
        self.assertNotEqual(expected_response, response)

    # # No sabemos si esta funcionalidad hará falta
    # def test_the_case_when_it_not_have_accesibles(self):
    #     referenceCellID = ""
    #     expected_response = ["", "", ""]
    #     response = self.igmlLayer.getAccesibleCells(referenceCellID)
    #     self.assertNotEqual(expected_response, response)

    def test_the_cell_of_a_position_fisrt_floor(self):
        position3D = UrbanService.position3D(37, 5, 2.9)
        expected_response = "CELL_MEETINGROOM.1"
        response = self.igmlLayer.getCellofPosition(
            self.spaceLayerID, position3D)
        self.assertEqual(expected_response, response)

    def test_the_cell_of_a_position_second_floor(self):
        position3D = UrbanService.position3D(37, 5, 3.1)
        expected_response = "CELL_LABORATORY.17"
        response = self.igmlLayer.getCellofPosition(
            self.spaceLayerID, position3D)
        self.assertEqual(expected_response, response)

    def test_the_cell_of_a_position_inside_a_complex_cell(self):
        # position3D = UrbanService.position3D(30, 9, 1)
        position3D = UrbanService.position3D(
            41, 11, 2)  # Al final del pasillo derecha
        expected_response = "CELL_CORRIDOR.0"
        response = self.igmlLayer.getCellofPosition(
            self.spaceLayerID, position3D)
        self.assertEqual(expected_response, response)

    def test_the_cell_of_a_position_outside_model(self):
        position3D = UrbanService.position3D(37, 5, 8.9)
        expected_response = ""
        response = self.igmlLayer.getCellofPosition(
            self.spaceLayerID, position3D)
        self.assertEqual(expected_response, response)

    def test_the_usage_of_a_cell(self):
        referenceCellID = "CELL_LABORATORY.11"
        expected_response = "Usage=Room"
        response = self.igmlLayer.getUsage(referenceCellID)
        self.assertEqual(expected_response, response)

    def test_the_height_of_a_cell(self):
        referenceCellID = "CELL_LABORATORY.11"
        expected_response = 3.0
        response = self.igmlLayer.getHeight(referenceCellID)
        self.assertEqual(expected_response, response)

    def test_the_name_of_a_cell(self):
        referenceCellID = "CELL_LABORATORY.11"
        expected_response = "CELL_LABORATORY.11"
        response = self.igmlLayer.getName(referenceCellID)
        self.assertEqual(expected_response, response)

    def test_if_the_exit_are_correct(self):
        referenceCellID = "CELL_HALL.8"
        expected_response = ["CB9192", "CB9195",
                             "CB9198", "CB9201", "CB9189"]
        response = self.igmlLayer.getExits(referenceCellID)
        self.assertCountEqual(expected_response, response)

    def test_the_entrances(self):
        expected_response = ["CELL_HALL.13"]
        response = self.igmlLayer.getEntrances(self.spaceLayerID)
        self.assertEqual(expected_response, response)

    # To-Do
    # def test_SpaceLayersListCorrect(self):


class RoutingServiceTests(TestCase):
    def setUp(self):
        broker = Ice.initialize()
        self.addCleanup(broker.destroy)

        # FIXME: use a known proxy for testing
        # do not include testing related code on server!!
        try:
            with open('RoutingService1.txt', 'r') as f:
                strproxy = f.readline()
        except IOError as error:
            print('Please, first start the service and then run again.')

        proxy = broker.stringToProxy(strproxy)
        self.routingServicePrx = SmartServices.RoutingServicePrx.checkedCast(proxy)

    def test_PathCellToCell_route(self):
        expected_response = ['CELL_LABORATORY.11',
                             'CELL_CORRIDOR.1', 'CELL_HALL.10', 'CELL_OFFICE.8']
        response = self.routingServicePrx.getPath("CELL_LABORATORY.11", "CELL_OFFICE.8")
        self.assertEqual(expected_response, response)