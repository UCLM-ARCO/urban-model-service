# -*- mode:python; coding:utf-8; tab-width:4 -*-
import Ice
from unittest import TestCase

class ToplogyTests(TestCase):
    def setUp(self):
        # Cliente normalmente
        # proxy = self.communicator().stringToProxy(argv[1])
        # router = Streetlayout.RouterPrx.checkedCast(proxy)
        #
        # if not router:
        #     raise RuntimeError('Invalid proxy')

        # ------------------------------------

        # Hecho con david https://bitbucket.org/arco_group/street.info.service/src/8a2c1e29a9ec034bdc2501c4bee0e535fa8efc2b/test/unit_tests.py?at=default&fileviewer=file-view-default
        # broker = Ice.initialize()
        # self.addCleanup(broker.destroy)
        #
        # strproxy = 'scone -t -e 1.1:tcp -h localhost -p 5001'
        # proxy = broker.stringToProxy(strproxy)
        # self.sut = StreetInfo(proxy)

    def test_if_two_cells_are_adjacent(self):

    def test_if_two_cells_are_not_adjacent(self):

    def test_if_two_cells_are_connected(self):

    def test_if_two_cells_are_not_connected(self):

    def test_if_two_cells_are_accesible(self):

    def test_if_two_cells_are_not_accesible(self):

    def test_if_the_adjacent_ones_are_correct(self):

    def test_if_the_connected_ones_are_correct(self):

    def test_if_the_accesible_ones_are_correct(self):

    def test_the_case_when_it_not_have_adjacents(self):

    def test_the_case_when_it_not_have_connected(self):

    def test_the_case_when_it_not_have_accesibles(self):

    def test_the_cell_of_a_position(self):

    def test_the_usage_of_a_cell(self):

    def test_the_height_of_a_cell(self):

    def test_the_name_of_a_cell(self):

    def test_if_the_exit_are_correct(self):

    def test_the_entrance(self):
