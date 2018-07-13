// State: PROPOSAL
module UrbanService{
  struct position3D{
    float x;
    float y;
    float z;
  };

  sequence<string> CellSequenceID;
  sequence<string> CellSpaceBoundaryID;
  sequence<string> SurfaceSequenceID;
  sequence<string> BoundarySequenceID;
  sequence<position3D> LinearRing;
  sequence<LinearRing> LinearRingSequence;

  struct geometry3D{
    string id;
    LinearRingSequence surfaces;
  };

  struct cellSpace{
    string id;
    string name;
    string usage;
    string duality;
    geometry3D geometry;
    CellSpaceBoundaryID cellSpaceBoundarys;
  };

  struct cellSpaceBoundary{
    string id;
    string name;
    string usage;
    geometry3D geometry;
  };

  struct state{
    string id;
    string name;
    string duality;
  };

  struct transition{
    string id;
    string name;
    float weight;
    string duality;
    string connectsFrom;
    string connectsTo;
  };

  sequence<cellSpace> CellSequence;
  sequence<cellSpaceBoundary> CellSpaceBoundarySequence;
  sequence<state>StateSequence;
  sequence<transition>TransitionSequence;

  interface TopologyLayer{
    bool isConnectedCell(string referenceCellID, string cellToCheqID);
    bool isAdjacentCell(string referenceCellID, string cellToCheqID);
    //bool isAccesibleCell(string referenceCellID, string cellToCheqID);

    CellSequenceID getConnectedCells(string referenceCellID);
    CellSequenceID getAdjacentCells(string referenceCellID);
    //CellSequenceID getAccesibleCells(string referenceCellID);

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

  // State: PROPOSAL
  struct georef{
    string pluscode;
    string placecode;
  };

  interface GeoHashingService{
    string getPlusCode(position3D position);
    georef getGeoRef(position3D position);
  };
};
