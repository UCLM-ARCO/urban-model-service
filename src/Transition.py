class Transition:
    def __init__(self, _id, name, weight, duality):
        self.id = _id
        self.name = name
        self.weight = weight
        self.duality = duality

    def __str__(self):
        return "Transition id: {}".format(self.id)

    def __repr__(self):
        return str(self)
