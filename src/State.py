class State:
    def __init__(self, _id, name, duality):
        self.id = _id
        self.name = name
        self.duality = duality

    def __str__(self):
        return self.id

    def __repr__(self):
        return str(self)
