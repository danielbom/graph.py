from edges import edges


class vertex(object):
    def __init__(self, name):
        self.name = name
        self.info = None
        self.edges = edges()
        self.included = True

    def add(self, source, destiny, destiny_class, weight):
        self.edges.add(source, destiny, destiny_class, weight)

    def list_of_edges(self):
        return self.edges.list_of_edges()

    def list_of_targets_edges(self):
        return [edge.destiny for edge in self.edges.list_of_edges()]

    def __str__(self):
        return "From %s -> %s" % (str(self.name), str(list(self.edges.keys())))

    def __repr__(self):
        return "From %s -> %s" % (str(self.name), str(list(self.edges.keys())))

    def is_sink(self):
        # Sorvedouro
        return len(self.edges.keys()) == 0
