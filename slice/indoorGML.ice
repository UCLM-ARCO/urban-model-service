// State: PROPOSAL
module UrbanService{
  struct position3D{
    float x;
    float y;
    float z;
  };

  sequence<position3D> LinearRing;

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

  sequence<string> CellSequence;
  sequence<string> SurfaceSequence;

  interface TopologyLayer{
    bool isAdjacentCell(string referenceCellID, string cellToCheqID);
    bool isConnectedCell(string referenceCellID, string cellToCheqID);
    bool isAccesibleCell(string referenceCellID, string cellToCheqID);

    CellSequence getAdjacentCells(string referenceCellID);
    CellSequence getConnectedCells(string referenceCellID);
    CellSequence getAccesibleCells(string referenceCellID);

    string getCellofPosition(position3D position);

    string getUsage(string referenceCell);
    string getName(string referenceCell);
    float getHeight(string referenceCell);

    SurfaceSequence getExits(string referenceCell);
    string getEntrance();

    string probarProxy(string prueba); //Solo de prueba. Hay que quitarlo
  };
};
