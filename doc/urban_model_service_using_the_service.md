+++
date = "2018-05-15T11:31:11+02:00"
title = "Urban Model Service. Using the service"
draft = false

+++


Overview
========
This work puts into operation a service that allows consulting through its interface the data available in a model of a building described according to the standard [IndoorGML](http://www.opengeospatial.org/standards/indoorgml). If the reader is not familiar with this standard, it is strongly recommended that the following [document](https://portal.opengeospatial.org/files/14-005r5) be reviewed before continuing.

More detailed information about the service and its possible uses can be found in the following paper: *Cantarero, R., Rubio, A., Trapero, C., Santofimia, M. J., Felix, J., Villa, D., & Lopez, J. C. (2018). A common-sense based system for Geo-IoT*.


How it works
============

The service `UrbanModelService` is oriented so that it provides basic information about the model of a given building to other services. One of the main advantages of this approach is that it eliminates the need for those who require information about a particular building to know in depth how the IndoorGML standard works or how to read and process an XML file. To this end, an interface has been designed to communicate with this service and make the necessary queries. The resulting interface `TopologyLayer` is shown in the following code. Although only the interface of the topology is shown in this recipe, it is important to mention that this interface can be directly extended to any other type of information layer:Wi-Fi coverage, range of vision of surveillance cameras, or what is the same, to any type of information related to IoT that wants to be represented.

```#!python
interface TopologyLayer{
  bool isConnectedCell(string referenceCellID, string cellToCheqID);
  bool isAdjacentCell(string referenceCellID, string cellToCheqID);

  CellSequenceID getConnectedCells(string referenceCellID);
  CellSequenceID getAdjacentCells(string referenceCellID);

  CellSequence getCells();
  CellSpaceBoundarySequence getCellSpaceBoundarys();
  StateSequence getStates();
  TransitionSequence getTransitions();

  string getCellofPosition(position3D position);
  CellSequenceID getPathCellToCell(string CellIDfrom, string CellIDto);
  CellSequenceID getPathPositionToPosition(position3D positionFrom, position3D positionTo);

  string getUsage(string referenceCellID);
  string getName(string referenceCellID);
  float getHeight(string referenceCellID);

  SurfaceSequenceID getExits(string referenceCellID);
  BoundarySequenceID getEntrances();
};
```

Through this interface, any service can make queries that range from direct consults of the type “What are the cells adjacent to cell X?” whose answers can be directly extracted from the model, to more elaborate questions of the type “To which cell does the position with coordinates `(x, y, z)  belong to?” based on searches in auxiliary structures (graphs, kd-tree, etc).

Below there is a detailed list of each functionality available through the interface:

- **isConnectedCell:** check if two cells are connected.
  - **referenceCellID:** cell reference identifier.
  - **cellToCheqID:** cell identifier to compare.
- **isAdjacentCell:** check if two cells are adjacent.
  - **referenceCellID:** cell reference identifier.
  - **cellToCheqID:** cell identifier to compare.
- **getConnectedCells:** return a cell sequence identifiers of connected cells to one given.
  - **referenceCellID:** cell reference identifier.
- **getAdjacentCells:** return a cell sequence identifiers of adjacent cells to one given.
  - **referenceCellID:** cell reference identifier.
- **getCells:** return all cells defined in the model.
- **getCellSpaceBoundarys:** return all cell space boundarys defined in the model.
- **getStates:** return all states defined in the model.
- **getTransitions:** return all transitions defined in the model.
- **getCellofPosition:** return the cell associated to a position 3D given.
  - **position:** 3D point.
- **getPathCellToCell:**
  - **CellIDfrom:** cell identifier route origin.
  - **CellIDto:** cell identifier route end.
- **getPathPositionToPosition:**
  - **positionFrom:** 3D point route origin.
  - **positionTo:** 3D point route end.
- **getUsage:** return the usages of space associated of a cell. Space features have to be classified by functions and usages of space such as *living room, bathroom, garden, etc*.
  - **referenceCellID:** Cell reference identifier
- **getName:** return the name associated to a cell. This name provides a well-known description of the space such as laboratory, meeting room, etc.
  - **referenceCellID:** Cell reference identifier
- **getHeight:** return the cell height.
  - **referenceCellID:** Cell reference identifier
- **getExits:** return the boundaries defined as exits of a given Cell.
  - **referenceCellID:** Cell reference identifier.
- **getEntrances:** returns the entrances defined in the model if they exists.

**Note:** *the interface and the methods describen here are in PROPOSAL state, which means that it is in constant change and evolution. For this reason some names or methods have been able to undergo changes. It is advisable to consult the latest version available in the repository.*


Starting the service
====================

To install all the dependencies necessary to start the service:
  - At the root of the repository, do 'sh install-dependencies.sh''

To start the service, it is necessary to have a model of a building according to the standard IndoorGML.

To start the service:
  - If you do not have the itsi.indoorgml repository in `~/repos/, you must change the model's path in the Makefile.
  - In ./src/ do `make run-server`.


Checking that everything works
------------------------------

To perform the tests and check that everything works correctly:

Make "make tests" in the root of the repository.



Running the example
===================
