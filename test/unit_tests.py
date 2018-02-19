# -*- mode:python; coding:utf-8; tab-width:4 -*-
# !/usr/bin/python3

import Ice
from unittest import TestCase

Ice.loadSlice('./slice/indoorGML.ice')
import UrbanService


class ToplogyTests(TestCase):
    def setUp(self):
        broker = Ice.initialize()
        self.addCleanup(broker.destroy)

        with open('./src/proxy.out', 'r') as f:
            strproxy = f.readline()

        proxy = broker.stringToProxy(strproxy)
        self.topologyLayer = UrbanService.TopologyLayerPrx.checkedCast(proxy)

    def test_if_two_cells_are_adjacent(self):
        referenceCellID = "CELL_LABORATORY.11"
        cellToCheqID = "CELL_LABORATORY.12"
        response = self.topologyLayer.isAdjacentCell(
            referenceCellID, cellToCheqID)
        self.assertTrue(response)

    def test_if_two_cells_are_not_adjacent(self):
        referenceCellID = "CELL_LABORATORY.11"
        cellToCheqID = "CELL_LABORATORY.15"
        response = self.topologyLayer.isAdjacentCell(
            referenceCellID, cellToCheqID)
        self.assertFalse(response)

    def test_if_two_cells_are_connected(self):
        referenceCellID = "CELL_LABORATORY.11"
        cellToCheqID = "CELL_CORRIDOR.1"
        response = self.topologyLayer.isConnectedCell(
            referenceCellID, cellToCheqID)
        self.assertTrue(response)

    def test_if_two_cells_are_not_connected(self):
        referenceCellID = "CELL_LABORATORY.11"
        cellToCheqID = "CELL_LABORATORY.15"
        response = self.topologyLayer.isConnectedCell(
            referenceCellID, cellToCheqID)
        self.assertFalse(response)

    def test_if_cell_not_exist(self):
        referenceCellID = "INVENTED_CELL"
        cellToCheqID = "CELL_CORRIDOR.1"

        with self.assertRaises(Exception):
            self.topologyLayer.isConnectedCell(referenceCellID, cellToCheqID)

    # # No sabemos si esta funcionalidad hará falta
    # def test_if_two_cells_are_accesible(self):
    #     referenceCellID = ""  # To-do
    #     cellToCheqID = ""  # To-do
    #     response = self.topologyLayer.isAccesibleCell(
    #         referenceCellID, cellToCheqID)
    #     self.assertTrue(response)
    #
    # def test_if_two_cells_are_not_accesible(self):
    #     referenceCellID = ""  # To-do
    #     cellToCheqID = ""  # To-do
    #     response = self.topologyLayer.isAccesibleCell(
    #         referenceCellID, cellToCheqID)
    #     self.assertFalse(response)

    def test_if_the_adjacent_ones_are_correct(self):
        referenceCellID = "CELL_LABORATORY.11"
        expected_response = ["CELL_LABORATORY.12",
                             "CELL_MEETINGROOM.2", "CELL_CORRIDOR.1"]
        response = self.topologyLayer.getAdjacentCells(referenceCellID)
        self.assertCountEqual(expected_response, response)

    def test_if_the_connected_ones_are_correct(self):
        referenceCellID = "CELL_HALL.8"
        expected_response = ["CELL_WAREHOUSE.7", "CELL_OFFICE.4",
                             "CELL_OFFICE.5", "CELL_LABORATORY.15", "CELL_CORRIDOR.1"]
        response = self.topologyLayer.getConnectedCells(referenceCellID)
        self.assertCountEqual(expected_response, response)

    # # No sabemos si esta funcionalidad hará falta
    # def test_if_the_accesible_ones_are_correct(self):
    #     referenceCellID = ""
    #     expected_response = ["", "", ""]
    #     response = self.topologyLayer.getAccesibleCells(referenceCellID)
    #     self.assertEqual(expected_response, response)

    def test_the_case_when_it_not_have_adjacents(self):
        referenceCellID = "CELL_FIRE STAIRS.0"
        expected_response = [""]
        response = self.topologyLayer.getAdjacentCells(referenceCellID)
        self.assertNotEqual(expected_response, response)

    def test_the_case_when_it_not_have_connected(self):
        referenceCellID = "CELL_FIRE STAIRS.0"
        expected_response = [""]
        response = self.topologyLayer.getConnectedCells(referenceCellID)
        self.assertNotEqual(expected_response, response)

    # # No sabemos si esta funcionalidad hará falta
    # def test_the_case_when_it_not_have_accesibles(self):
    #     referenceCellID = ""
    #     expected_response = ["", "", ""]
    #     response = self.topologyLayer.getAccesibleCells(referenceCellID)
    #     self.assertNotEqual(expected_response, response)

    def test_the_cell_of_a_position(self):
        position3D = UrbanService.position3D(
            99999.9, 99999.9, 999999.9)  # To-DO: 3D coordinate (x,y,z)
        expected_response = ""  # To-Do: Cell ID
        response = self.topologyLayer.getCellofPosition(position3D)
        self.assertEqual(expected_response, response)

    def test_the_usage_of_a_cell(self):
        referenceCellID = "CELL_LABORATORY.11"
        expected_response = "Room"
        response = self.topologyLayer.getUsage(referenceCellID)
        self.assertEqual(expected_response, response)

    def test_the_height_of_a_cell(self):
        referenceCellID = "CELL_LABORATORY.11"
        expected_response = 3.0
        response = self.topologyLayer.getHeight(referenceCellID)
        self.assertEqual(expected_response, response)

    def test_the_name_of_a_cell(self):
        referenceCellID = "CELL_LABORATORY.11"
        expected_response = "CELL_LABORATORY.11"
        response = self.topologyLayer.getName(referenceCellID)
        self.assertEqual(expected_response, response)

    def test_if_the_exit_are_correct(self):
        referenceCellID = "CELL_HALL.8"
        expected_response = ["CB19713", "CB19716",
                             "CB34475", "CB19707", "CB19710"]
        response = self.topologyLayer.getExits(referenceCellID)
        self.assertCountEqual(expected_response, response)

    def test_the_entrances(self):
        expected_response = ["CELL_HALL.7"]
        response = self.topologyLayer.getEntrances()
        self.assertEqual(expected_response, response)
