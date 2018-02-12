class Cell:
    def __init__(self, _id, name, usage, duality, geometry, bound):
        self.id = _id
        self.name = name
        self.usage = usage
        self.duality = duality
        self.geometry = geometry
        self.bound = bound

    def __str__(self):
        return "Cell id: {}".format(self.id)

    def __repr__(self):
        return str(self)
