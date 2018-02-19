// State: PROPOSAL
module UrbanService{
  struct position3D{
    float x;
    float y;
    float z;
  };

  sequence<string> CellSequenceID;
  sequence<string> SurfaceSequenceID;
  sequence<string> BoundarySequenceID;

  interface TopologyLayer{
    bool isConnectedCell(string referenceCellID, string cellToCheqID);
    bool isAdjacentCell(string referenceCellID, string cellToCheqID);
    //bool isAccesibleCell(string referenceCellID, string cellToCheqID);

    CellSequenceID getConnectedCells(string referenceCellID);
    CellSequenceID getAdjacentCells(string referenceCellID);
    //CellSequenceID getAccesibleCells(string referenceCellID);

    string getCellofPosition(position3D position);

    string getUsage(string referenceCellID);
    string getName(string referenceCellID);
    float getHeight(string referenceCellID);

    SurfaceSequenceID getExits(string referenceCellID);
    BoundarySequenceID getEntrances();
  };
};
