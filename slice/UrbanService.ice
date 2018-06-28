// State: PROPOSAL
module UrbanService{
  struct position3D{
    float x;
    float y;
    float z;
  };

  sequence<string> SpaceLayersSequenceID;
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

  interface IgmlLayer{
    bool isConnectedCell(string referenceCellID, string cellToCheqID);
    bool isAdjacentCell(string referenceCellID, string cellToCheqID);
    //bool isAccesibleCell(string referenceCellID, string cellToCheqID);

    CellSequenceID getConnectedCells(string referenceCellID);
    CellSequenceID getAdjacentCells(string referenceCellID);
    //CellSequenceID getAccesibleCells(string referenceCellID);

    CellSequence getCells(string spaceLayerID);
    CellSpaceBoundarySequence getCellSpaceBoundarys(string spaceLayerID);
    StateSequence getStates(string spaceLayerID);
    TransitionSequence getTransitions(string spaceLayerID);

    string getCellofPosition(string spaceLayerID, position3D position);
    CellSequenceID getPathCellToCell(string spaceLayerID, string CellIDfrom, string CellIDto);
    CellSequenceID getPathPositionToPosition(string spaceLayerID, position3D positionFrom, position3D positionTo);

    string getUsage(string referenceCellID);
    string getName(string referenceCellID);
    float getHeight(string referenceCellID);

    SurfaceSequenceID getExits(string referenceCellID);
    BoundarySequenceID getEntrances(string spaceLayerID);

    SpaceLayersSequenceID getSpaceLayersID();
  };
};
