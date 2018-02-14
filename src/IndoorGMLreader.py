#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-

import sys
import re
import networkx as nx
import matplotlib.pyplot as plt

from lxml import etree
from CellSpaceBoundary import CellSpaceBoundary
from Geometry3D import Geometry3D
from CellSpace import CellSpace
from State import State
from Transition import Transition

import Ice
Ice.loadSlice('../slice/indoorGML.ice')
from UrbanService import position3D


ns = {'indoorgml': 'http://www.opengis.net/indoorgml/1.0/core',
      'gml': 'http://www.opengis.net/gml/3.2'}
tags = {'CellSpaceBoundary':
        '{http://www.opengis.net/indoorgml/1.0/core}CellSpaceBoundary',
        'CellSpaceBoundary_id': '{http://www.opengis.net/gml/3.2}id',
        'Polygon_id': '{http://www.opengis.net/gml/3.2}id',
        'CellSpace': '{http://www.opengis.net/indoorgml/1.0/core}CellSpace',
        'CellSpace_id': '{http://www.opengis.net/gml/3.2}id',
        'CellSpace_duality': '{http://www.w3.org/1999/xlink}href',
        'Solid_id': '{http://www.opengis.net/gml/3.2}id',
        'partialboundedBy_duality': '{http://www.w3.org/1999/xlink}href',
        'SpaceLayer': '{http://www.opengis.net/indoorgml/1.0/core}SpaceLayer',
        'SpaceLayer_id': '{http://www.opengis.net/gml/3.2}id',
        'State_id': '{http://www.opengis.net/gml/3.2}id',
        'State_duality': '{http://www.w3.org/1999/xlink}href',
        'Transition_id': '{http://www.opengis.net/gml/3.2}id',
        'Transition_duality': '{http://www.w3.org/1999/xlink}href',
        'Transition_connects': '{http://www.w3.org/1999/xlink}href'}


class IndoorGMLreader:
    def __init__(self, _file):
        self.file = _file
        self.loadCellSpaceBoundarys()
        self.loadCellSpaces()
        self.layers = {}

    def loadCellSpaceBoundarys(self):
        self.CellSpaceBoundarys = {}
        for (event, node) in etree.iterparse(self.file, events=['end'],
                                             tag=tags['CellSpaceBoundary'], huge_tree=True):

            cellSpaceBoundary_id = node.attrib[tags['CellSpaceBoundary_id']]
            cellSpaceBoundary_name = node.find('gml:name', ns).text

            cellSpaceBoundary_usage = ''
            if(node.find('gml:description', ns) is not None):
                dirty_cellSpaceBoundary_usage = node.find(
                    'gml:description', ns).text
                cellSpaceBoundary_usage = dirty_cellSpaceBoundary_usage[6:]

            geometry_id = node.find('indoorgml:geometry3D', ns).find(
                'gml:Polygon', ns).attrib[tags['Polygon_id']]

            cellSpaceBoundary_linearRing_node = node.find('indoorgml:geometry3D', ns).find(
                'gml:Polygon', ns).find('gml:exterior', ns).find('gml:LinearRing', ns)

            linearRing = []
            for pos in cellSpaceBoundary_linearRing_node.findall('gml:pos', ns):
                position = pos.text.split()
                linearRing.append(position3D(
                    float(position[0]), float(position[1]), float(position[2])))

            geometry = Geometry3D(geometry_id, [linearRing])
            self.CellSpaceBoundarys[cellSpaceBoundary_id] = CellSpaceBoundary(
                cellSpaceBoundary_id, cellSpaceBoundary_name,
                cellSpaceBoundary_usage, geometry)

            node.clear()

    def loadCellSpaces(self):
        self.CellSpaces = {}
        for (event, node) in etree.iterparse(self.file,
                                             tag=tags['CellSpace'],
                                             huge_tree=True):

            cellSpace_id = node.attrib[tags['CellSpace_id']]
            cellSpace_name = node.find('gml:name', ns).text
            cellSpace_usage = ''
            if(node.find('gml:description', ns) is not None):
                dirty_cellSpace_usage = node.find(
                    'gml:description', ns).text
                cellSpace_usage = re.split(':|=', dirty_cellSpace_usage)[1]

            cellSpace_duality_node = node.find('indoorgml:duality', ns)
            cellSpace_duality = ''
            if(cellSpace_duality_node is not None):
                cellSpace_duality = cellSpace_duality_node.attrib[tags['CellSpace_duality']][1:]

            geometry_id = node.find('indoorgml:Geometry3D', ns).find(
                'gml:Solid', ns).attrib[tags['Solid_id']]

            surfaceMember_id = node.find('indoorgml:Geometry3D', ns).find(
                'gml:Solid', ns).attrib[tags['Solid_id']]

            shell_node = node.find('indoorgml:Geometry3D', ns).find(
                'gml:Solid', ns).find('gml:exterior', ns).find('gml:Shell', ns)

            surfaces = []
            for surfaceMember in shell_node.findall('gml:surfaceMember', ns):
                linearRing_node = surfaceMember.find('gml:Polygon', ns).find(
                    'gml:exterior', ns).find('gml:LinearRing', ns)

                linearRing = []

                for pos in linearRing_node.findall('gml:pos', ns):
                    position = pos.text.split()
                    linearRing.append(position3D(
                        float(position[0]), float(position[1]), float(position[2])))

                surfaces.append(linearRing)

            cellSpaceBoundarys = []
            for partialboundedByNode in node.findall('indoorgml:partialboundedBy', ns):
                cellSpaceBoundarys.append(
                    partialboundedByNode.attrib[tags['partialboundedBy_duality']][1:])

            geometry = Geometry3D(geometry_id, surfaces)
            self.CellSpaces[cellSpace_id] = CellSpace(cellSpace_id, cellSpace_name,
                                                      cellSpace_usage, cellSpace_duality, geometry, cellSpaceBoundarys)

            node.clear()

    def loadLayer(self, spaceLayer_id):
        self.layers[spaceLayer_id] = nx.Graph()
        root = None
        for (event, node) in etree.iterparse(self.file,
                                             tag=tags['SpaceLayer'],
                                             huge_tree=True):

            if(node.attrib[tags['SpaceLayer_id']] == spaceLayer_id):
                root = node
                break

        nodes_node = root.find('indoorgml:nodes', ns)
        edges_node = root.find('indoorgml:edges', ns)

        self.loadNodes(nodes_node, self.layers[spaceLayer_id])
        self.loadEdges(edges_node, self.layers[spaceLayer_id])

    def loadNodes(self, root, graph):
        for stateMember in root.findall('indoorgml:stateMember', ns):
            state_node = stateMember.find('indoorgml:State', ns)
            state_id = state_node.attrib[tags['State_id']]
            state_name = state_node.find('gml:name', ns).text

            state_duality_node = state_node.find('indoorgml:duality', ns)
            state_duality = ''
            if(state_duality_node is not None):
                state_duality = state_duality_node.attrib[tags['State_duality']][1:]

            state = State(state_id, state_name, state_duality)
            graph.add_node(state_id, obj=state)

    def loadEdges(self, root, graph):
        for transitionMember in root.findall('indoorgml:transitionMember', ns):
            transition_node = transitionMember.find('indoorgml:Transition', ns)
            transition_id = transition_node.attrib[tags['Transition_id']]
            transition_name = transition_node.find('gml:name', ns).text
            transition_weight = float(
                transition_node.find('indoorgml:weight', ns).text)

            transition_duality_node = transition_node.find(
                'indoorgml:duality', ns)
            transition_duality = ''
            if(transition_duality_node is not None):
                transition_duality = transition_duality_node.attrib[tags['Transition_duality']][1:]

            connects = transition_node.findall('indoorgml:connects', ns)
            state_ref_1 = connects[0].attrib[tags['Transition_connects']][1:]
            state_ref_2 = connects[1].attrib[tags['Transition_connects']][1:]

            transition = Transition(
                transition_id, transition_name, transition_weight, transition_duality)
            graph.add_edge(state_ref_1, state_ref_2, object=transition)

    def drawLayer(self, spaceLayer_id):
        nx.draw(self.layers[spaceLayer_id], with_labels=True)
        plt.show()


filepath = sys.argv[1]
model = IndoorGMLreader(filepath)
# print(model.CellSpaceBoundarys)
# print(model.CellSpaces)
# print(len(model.CellSpaces))

model.loadLayer('TOPOLOGY')
model.drawLayer('TOPOLOGY')
# model.loadLayer('topo')
# model.loadLayer('cober')
