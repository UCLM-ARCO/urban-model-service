import networkx as nx


class Town:
    def __init__(self, name, population):
        self.name = name
        self.population = population

    def __str__(self):
        return "<<name: {} - population: {}>>".format(self.name, self.population)

    def __repr__(self):
        return str(self)


class Road:
    def __init__(self, name, free):
        self.name = name
        self.free = free

    def __str__(self):
        return "<<name: {} - population: {}>>".format(self.name, self.free)

    def __repr__(self):
        return str(self)


city1 = Town("Ciudad Real", 10)
city2 = Town("Toledo", 5)
city3 = Town("Madrid", 100)

road1 = Road("A4", True)
road2 = Road("National road", False)

G = nx.Graph()
G.add_nodes_from([city1, city2, city3])
G.add_edge(city1, city2, object=road2)
G.add_edge(city1, city3, object=road1)

print(list(G.nodes))
print(list(G.edges()))

print(G[city1][city2])
