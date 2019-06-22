from vertex import vertex
from functools import reduce


class vertexes(dict):
    def add_vertex(self, name):
        self[name] = self.get(name, vertex(name))
        return self[name]

    def add_single_edge(self, source, destiny, weight=1):
        source_class = self.add_vertex(source)
        destiny_class = self.add_vertex(destiny)

        source_class.add(destiny_class, weight)

    def add_edge(self, source, destiny, weight=1):
        source_class = self.add_vertex(source)
        destiny_class = self.add_vertex(destiny)

        source_class.add(destiny_class, float(weight))
        destiny_class.add(source_class, float(weight))

    def _remove_vertex(self, name):
        for edge in self[name].edges.list_of_edges():
            edge.included = False
        self[name].included = False

    def _include_all(self):
        for vertex in self.values():
            vertex.included = True
        for edge in self.edges():
            edge.included = True

    def _remove_all_vertex(self):
        for vertex in self.values():
            vertex.included = False

    def edges_destinations(self, lazy_mode=False):
        return (edge.destiny for edge in self.edges(lazy_mode))

    def edges(self, lazy_mode=False):
        if lazy_mode:
            for vertex in self.values():
                if vertex.included:
                    for e in vertex.list_of_edges():
                        yield e
            return
        for vertex in self.values():
            for e in vertex.list_of_edges():
                yield e

    def vertexes_names(self, lazy_mode=False):
        return (v.name for v in self._list_of_vertexes(lazy_mode))

    def _list_of_vertexes(self, lazy_mode=False):
        return (v for v in self.values() if v.included) if lazy_mode else self.values()

    def matrix_of_adjacence(self):
        for i, vertex in enumerate(self.values()):
            vertex.info = i

        n = len(self)
        matrix = [[0] * n for i in range(n)]
        for edge in self.edges():
            matrix[self[edge.source].info][edge.destiny_class.info] = edge.weight

        return matrix

    def set_infos(self, info):
        funct = lambda x: x
        if isinstance(info, dict):
            funct = lambda x: x.copy()
        
        for vertex in self._list_of_vertexes():
            vertex.info = funct(info)

    def set_infos_edges(self, info):
        funct = lambda x: x
        if isinstance(info, dict):
            funct = lambda x: x.copy()

        for vertex in self.edges():
            vertex.info = funct(info)

    def all_sinks(self):
        return [vertex for vertex in self._list_of_vertexes() if vertex.is_sink()]

    def all_sources(self, lazy_mode=False):
        return list(set(self.vertexes_names(lazy_mode)) - set(self.edges_destinations(lazy_mode)))

    def reverse(self):
        vertex_copy = { k: v for k, v in self.items() }

        self.clear()
        for name, vertex in vertex_copy.items():
            self.add_vertex(name)
            for edge in vertex.edges.values():
                self.add_single_edge(edge.destiny, edge.source, edge.weight)

        vertex_copy.clear()


    def __eq__(self, other):
        for kv, v in self.items():
            if not other.get(kv):
                return False
            for ke, e in v.edges.items():
                if not other[kv].edges.get(ke):
                    return False
                if other[kv].edges[ke] != e:
                    return False
        return True