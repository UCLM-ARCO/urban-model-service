// State: PROPOSAL
module indoorGMLservice{
  struct 3Dposition{
    float x;
    float y;
    float z;
  };

  sequence<3Dposition> LinearRing;

  struct Surface{
    string id;
    LinearRing polygon;
  };

  sequence<Surface> Shell;

  struct Geometry3D{
    string id;
    Shell solid;
  };

  sequence<string> PartialBounded;

  struct Cell{
    string id;
    string name;
    string usage;
    string duality;
    Geometry3D geometry;
    PartialBounded bound;
  };

  sequence<cell> CellSequence;
  sequence<Surface> SurfaceSequence;

  interface topologyLayer{
    bool isAdjacentCell(cell referenceCell, cell cellToCheq);
    bool isConnectedCell(cell referenceCell, cell cellToCheq);
    bool isAccesibleCell(cell referenceCell, cell cellToCheq);

    CellSequence getAdjacentCells(Cell referenceCell);
    CellSequence getConnectedCells(Cell referenceCell);
    CellSequence getAccesibleCells(Cell referenceCell);

    Cell getCellofPosition(3Dposition position);

    string getUsage(Cell referenceCell);
    string getHeight(Cell referenceCell);
    string getName(Cell referenceCell);

    SurfaceSequence getExits(Cell referenceCell);
    Surface getEntrance();
  };
};
