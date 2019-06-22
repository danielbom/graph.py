import edge


class edges(dict):
    def add(self, source, destiny, destiny_class, weight):
        self[destiny] = edge.edge(source, destiny, destiny_class, weight)

    def list_of_edges(self):
        return self.values()

    def destiniations(self):
        return [edge.destiny_class for edge in self.values()]
