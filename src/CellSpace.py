class CellSpace:
    def __init__(self, _id, name, usage, duality, geometry, cellSpaceBoundarys):
        self.id = _id
        self.name = name
        self.usage = usage
        self.duality = duality
        self.geometry = geometry
        self.cellSpaceBoundarys = cellSpaceBoundarys

    def __str__(self):
        return self.id

    def __repr__(self):
        return str(self)
