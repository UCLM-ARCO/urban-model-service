# -*- mode:python; coding:utf-8; tab-width:4 -*-
# !/usr/bin/python3

import Ice
from unittest import TestCase

Ice.loadSlice('../slice/UrbanService.ice')
import UrbanService


class IgmlTests(TestCase):
    def setUp(self):
        broker = Ice.initialize()
        self.addCleanup(broker.destroy)
        self.spaceLayerID = 'TOPOLOGY'

        try:
            with open('../src/IgmlLayer1.txt', 'r') as f:
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
        expected_response = "Room"
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

    def test_PathCellToCell_route(self):
        expected_response = ['CELL_LABORATORY.11',
                             'CELL_CORRIDOR.1', 'CELL_HALL.10', 'CELL_OFFICE.8']
        response = self.igmlLayer.getPathCellToCell(self.spaceLayerID,
                                                    "CELL_LABORATORY.11", "CELL_OFFICE.8")
        self.assertEqual(expected_response, response)

    def test_PathPositionToPosition(self):
        position3DFrom = UrbanService.position3D(
            2, 20, 3.1)  # CELL_LABORATORY.11
        position3DTo = UrbanService.position3D(
            42, 5, 3.1)  # CELL_OFFICE.8
        expected_response = ['CELL_LABORATORY.11',
                             'CELL_CORRIDOR.1', 'CELL_HALL.10', 'CELL_OFFICE.8']
        response = self.igmlLayer.getPathPositionToPosition(self.spaceLayerID,
                                                            position3DFrom, position3DTo)
        self.assertEqual(expected_response, response)

    # To-Do
    # def test_SpaceLayersListCorrect(self):

class GeoHashingTests(TestCase):
    def setUp(self):
        broker = Ice.initialize()
        self.addCleanup(broker.destroy)

        try:
            with open('../src/GeoHashing1.txt', 'r') as f:
                strproxy = f.readline()
        except IOError:
            print('Please, first start the service and then run again.')

        proxy = broker.stringToProxy(strproxy)
        self.GeoHashing = UrbanService.GeoHashingPrx.checkedCast(proxy)

    def test_is_valid_when_valid(self):
        self.assertTrue(self.GeoHashing.isValid("8CCRX3XJ+526"))

    def test_is_valid_when_not_valid(self):
        self.assertFalse(self.GeoHashing.isValid("8CCRX3XJ52rgwt4hthrh56"))

    def test_encode(self):
        expected_response = "8CCRX3XJ+526"
        response = (self.GeoHashing.encode(
                                        38.9979133605957,
                                        -3.9199843406677246, 
                                        11))
        self.assertEqual(expected_response, response)

    def test_decode(self):
        expected_response = UrbanService.CodeArea(
                                        latitudeLo = 38.99789810180664,
                                        longitudeLo = -3.9200000762939453,
                                        latitudeHi = 38.9979248046875,
                                        longitudeHi = -3.919968843460083,
                                        codeLength = 11,
                                        latitudeCenter = 38.9979133605957,
                                        longitudeCenter = -3.9199843406677246
                                    )
        response = (self.GeoHashing.decode("8CCRX3XJ+526"))
        self.assertEqual(expected_response, response)

    def test_getBulding(self):
        expected_response_UUID = "6b6b1b71-9d28-3a52-bfa8-126387ee612f"
        expected_response_openLocationCodes = (
            ['8CCRX3XJ+763','8CCRX3XJ+764','8CCRX3XJ+66R','8CCRX3XJ+66V','8CCRX3XJ+66W','8CCRX3XJ+65J','8CCRX3XJ+65M','8CCRX3XJ+65P','8CCRX3XJ+65Q','8CCRX3XJ+66J','8CCRX3XJ+66M','8CCRX3XJ+66P','8CCRX3XJ+66Q','8CCRX3XJ+64G','8CCRX3XJ+64H','8CCRX3XJ+65C','8CCRX3XJ+65F','8CCRX3XJ+65G','8CCRX3XJ+65H','8CCRX3XJ+66C','8CCRX3XJ+66F','8CCRX3XJ+66G','8CCRX3XJ+66H','8CCRX3XJ+639','8CCRX3XJ+646','8CCRX3XJ+647','8CCRX3XJ+648','8CCRX3XJ+649','8CCRX3XJ+656','8CCRX3XJ+657','8CCRX3XJ+658','8CCRX3XJ+659','8CCRX3XJ+666','8CCRX3XJ+667','8CCRX3XJ+668','8CCRX3XJ+669','8CCRX3XJ+676','8CCRX3XJ+633','8CCRX3XJ+634','8CCRX3XJ+635','8CCRX3XJ+642','8CCRX3XJ+643','8CCRX3XJ+644','8CCRX3XJ+645','8CCRX3XJ+652','8CCRX3XJ+653','8CCRX3XJ+654','8CCRX3XJ+655','8CCRX3XJ+662','8CCRX3XJ+663','8CCRX3XJ+664','8CCRX3XJ+665','8CCRX3XJ+672','8CCRX3XJ+52W','8CCRX3XJ+52X','8CCRX3XJ+53R','8CCRX3XJ+53V','8CCRX3XJ+53W','8CCRX3XJ+53X','8CCRX3XJ+54R','8CCRX3XJ+54V','8CCRX3XJ+54W','8CCRX3XJ+54X','8CCRX3XJ+55R','8CCRX3XJ+55V','8CCRX3XJ+55W','8CCRX3XJ+55X','8CCRX3XJ+56R','8CCRX3XJ+56V','8CCRX3XJ+56W','8CCRX3XJ+56X','8CCRX3XJ+57R','8CCRX3XJ+57V','8CCRX3XJ+52J','8CCRX3XJ+52M','8CCRX3XJ+52P','8CCRX3XJ+52Q','8CCRX3XJ+53J','8CCRX3XJ+53M','8CCRX3XJ+53P','8CCRX3XJ+53Q','8CCRX3XJ+54J','8CCRX3XJ+54M','8CCRX3XJ+54P','8CCRX3XJ+54Q','8CCRX3XJ+55J','8CCRX3XJ+55M','8CCRX3XJ+55P','8CCRX3XJ+55Q','8CCRX3XJ+56J','8CCRX3XJ+56M','8CCRX3XJ+56P','8CCRX3XJ+56Q','8CCRX3XJ+57J','8CCRX3XJ+57M','8CCRX3XH+5XH','8CCRX3XJ+52C','8CCRX3XJ+52F','8CCRX3XJ+52G','8CCRX3XJ+52H','8CCRX3XJ+53C','8CCRX3XJ+53F','8CCRX3XJ+53G','8CCRX3XJ+53H','8CCRX3XJ+54C','8CCRX3XJ+54F','8CCRX3XJ+54G','8CCRX3XJ+54H','8CCRX3XJ+55C','8CCRX3XJ+55F','8CCRX3XJ+55G','8CCRX3XJ+55H','8CCRX3XJ+56C','8CCRX3XH+5X9','8CCRX3XJ+526','8CCRX3XJ+527','8CCRX3XJ+528','8CCRX3XJ+529','8CCRX3XJ+536','8CCRX3XJ+537','8CCRX3XJ+538','8CCRX3XJ+539','8CCRX3XJ+546','8CCRX3XJ+547','8CCRX3XJ+548','8CCRX3XJ+549','8CCRX3XJ+556','8CCRX3XJ+557','8CCRX3XJ+558','8CCRX3XJ+559','8CCRX3XJ+566','8CCRX3XJ+522','8CCRX3XJ+523','8CCRX3XJ+524','8CCRX3XJ+525','8CCRX3XJ+532','8CCRX3XJ+533','8CCRX3XJ+534','8CCRX3XJ+535','8CCRX3XJ+542','8CCRX3XJ+543','8CCRX3XJ+544','8CCRX3XJ+545','8CCRX3XJ+552','8CCRX3XJ+553','8CCRX3XJ+554','8CCRX3XJ+42R','8CCRX3XJ+42V','8CCRX3XJ+42W','8CCRX3XJ+42X','8CCRX3XJ+43R','8CCRX3XJ+43V','8CCRX3XJ+43W','8CCRX3XJ+43X','8CCRX3XJ+44R','8CCRX3XJ+44V','8CCRX3XJ+44W','8CCRX3XJ+44X','8CCRX3XJ+42M','8CCRX3XJ+42P','8CCRX3XJ+42Q','8CCRX3XJ+43J','8CCRX3XJ+43M','8CCRX3XJ+43P','8CCRX3XJ+43Q','8CCRX3XJ+44J','8CCRX3XJ+44M','8CCRX3XJ+42F','8CCRX3XJ+42G','8CCRX3XJ+42H','8CCRX3XJ+43C','8CCRX3XJ+43F','8CCRX3XJ+43G','8CCRX3XJ+427','8CCRX3XJ+428','8CCRX3XJ+429','8CCRX3XJ+436','8CCRX3XJ+56F','8CCRX3XJ+56G', '8CCRX3XJ+65W', '8CCRX3XJ+65X', '8CCRX3XJ+42J'])

        response = self.GeoHashing.getBuilding("Instituto de Tecnologías y Sistemas de Información")
        response_openLocationCodes = response.openLocationCodes
        response_UUID = response.uuid

        self.assertCountEqual(expected_response_openLocationCodes, response_openLocationCodes)
        self.assertCountEqual(expected_response_UUID, response_UUID)