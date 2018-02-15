class CellSpaceBoundary:
    def __init__(self, _id, name, usage, geometry):
        self.id = _id
        self.name = name
        self.usage = usage
        self.geometry = geometry

    def __str__(self):
        return self.id

    def __repr__(self):
        return str(self)
