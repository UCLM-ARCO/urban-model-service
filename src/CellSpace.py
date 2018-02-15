class CellSpace:
    def __init__(self, _id, name, usage, duality, geometry, cellSpaceBoundarys):
        self.id = _id
        self.name = name
        self.usage = usage
        self.duality = duality
        self.geometry = geometry
        self.cellSpaceBoundarys = cellSpaceBoundarys

    def __str__(self):
        sb = []
        for key in self.__dict__:
            sb.append("{key}='{value}'".format(
                key=key, value=self.__dict__[key]))

        return ', '.join(sb)

    def __repr__(self):
        return str(self)
