#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-

import sys
import Ice
import uuid
import time
import networkx as nx
from IndoorGMLreader import IndoorGMLreader
from libcitisim import SmartServices
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import random


def convertRoute(route, model):
    result = []

    for node in route:
        interLayerConnection = model.InterLayerConnections.get(node)
        if(interLayerConnection != None):
            if interLayerConnection.replace("STATE_", "CELL_") not in result:
                result.append(interLayerConnection.replace("STATE_", "CELL_"))
        else:
            result.append(node.replace("STATE_", "CELL_"))

    return result

def getPath(startPoint, endPoint, model, spaceLayerID):
    cellSpaceFrom = model.getCellreference(startPoint).duality
    cellSpaceTo = model.getCellreference(endPoint).duality

    nodes = nx.dijkstra_path(
        model.spaceLayers[spaceLayerID], cellSpaceFrom, cellSpaceTo)

    route = []
    for n in nodes:
        route.append(
            model.spaceLayers[spaceLayerID].nodes[n]['obj'].id)

    return route
    #return convertRoute(route, model)

def getRandomCellsIds(test_number, model, spaceLayerID):
    origins = []
    ends = []
    states = model.spaceLayers[spaceLayerID].nodes()

    for x in range(test_number):
        random_states = random.sample(states, 2)

        while(checkIfIsBarrier(random_states[0], model) or checkIfIsBarrier(random_states[1], model)):
            random_states = random.sample(states, 2)

        random_cells_id = [state.replace("STATE", "CELL") for state in random_states]

        origins.append(random_cells_id[0])
        ends.append(random_cells_id[1])


    return [origins, ends]


def checkIfIsBarrier(state_id, model):
    interLayerConnection = model.InterLayerConnections.get(state_id)
    cell = model.getCellreference(interLayerConnection.replace("STATE", "CELL"))

    if "barrier" in cell.usage or "building" in cell.usage:
        return True
    else:
        return False


def run_tests(option):
    times = []
    model = IndoorGMLreader(sys.argv[1], fixed_weight = option)

    if 'olc-layer' in  model.spaceLayers:
        spaceLayerID = 'olc-layer'
    else:
        spaceLayerID = 'TOPOLOGY'

    test_number = 10
    repetitions_number = 100
    random_cells_id = getRandomCellsIds(test_number, model, spaceLayerID)
    print(random_cells_id)

    for i in range(test_number):
        print('Calculating route...')
        accumulated_time = 0

        for j in range(repetitions_number):
            start = time.time()
            getPath(random_cells_id[0][i], random_cells_id[1][i], model, spaceLayerID)
            end = time.time()
            accumulated_time += end - start

        average_time = accumulated_time / repetitions_number 
        times.append(average_time)

    return times


times_not_surfaces = run_tests(False)
times_with_surfacers = run_tests(True)

print(times_not_surfaces)
print(times_with_surfacers)

ind = np.arange(len(times_not_surfaces))  # the x locations for the groups
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(ind - width/2, times_not_surfaces, width,
                label='No surfaces')
rects2 = ax.bar(ind + width/2, times_with_surfacers, width,
                label='With Surfaces')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Execution time (ms)')
ax.set_xlabel('Tests')
# ax.set_title('Scores by group and gender')
# ax.set_xticks(ind)
# ax.set_xticklabels(('Test 1', 'Test 2', 'Test 3', 'Test 4', 'Test 5', 'Test 6', 'Test 7', 'Test 8', 'Test 9', 'Test 10'))
ax.legend()

fig.tight_layout()

plt.show()