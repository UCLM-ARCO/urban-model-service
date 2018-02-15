class Geometry3D:
    def __init__(self, _id, shell):
        self.id = _id
        self.shell = shell

    def __str__(self):
        return self.id

    def __repr__(self):
        return str(self)
