from edges import edges


class vertex(object):
    def __init__(self, name):
        self.name = name
        self.info = None
        self.edges = edges()
        self.included = True

    def add(self, destiny_class, weight):
        self.edges.add(self.name, destiny_class.name, destiny_class, weight)

    def list_of_edges(self):
        return self.edges.list_of_edges()

    def list_of_targets_edges(self):
        return [edge.destiny for edge in self.edges.list_of_edges()]

    def __str__(self):
        edges = [(edge.destiny, edge.weight) for edge in self.edges.values()]
        return "From {} -> {}".format(self.name, edges)

    def __repr__(self):
        return self.__str__() 

    def is_sink(self): # Sorvedouro
        return len(self.edges.keys()) == 0
