class Surface:
    def __init__(self, _id, linearRing):
        self.id = _id
        self.linearRing = linearRing

    def __str__(self):
        return "Surface id: {}".format(self.id)

    def __repr__(self):
        return str(self)
