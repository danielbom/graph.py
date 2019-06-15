import edge


class edges(dict):
    def add(self, source, destiny, destiny_class, weight):
        self[destiny] = edge.edge(source, destiny, destiny_class, weight)

    def list_of_edges(self):
        return list(self.values())

    def list_of_vertexes(self):
        return [edge.destiny_class for edge in self.values()]
