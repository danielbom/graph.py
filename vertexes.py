import vertex
from functools import reduce


class vertexes(dict):
    def add_vertex(self, name):
        self[name] = self.get(name, vertex.vertex(name))

    def add_single_edge(self, source, destiny, weight=1):
        self.add_vertex(source)
        self.add_vertex(destiny)

        source_class = self.get(source)
        destiny_class = self.get(destiny)

        source_class.add(source, destiny, destiny_class, weight)

    def add_edge(self, source, destiny, weight=1):
        self.add_vertex(source)
        self.add_vertex(destiny)

        source_class = self.get(source)
        destiny_class = self.get(destiny)

        source_class.add(source, destiny, destiny_class, float(weight))
        destiny_class.add(destiny, source, source_class, float(weight))

    def _remove_vertex(self, name):
        for edge in self[name].edges.list_of_edges():
            edge.included = False
        self[name].included = False

    def _include_all(self):
        for vertex in self.values():
            vertex.included = True
        for edge in self.list_of_all_edges():
            edge.included = True

    def _remove_all_vertex(self):
        for vertex in self.values():
            vertex.included = False

    def list_of_all_targets_edges(self, lazy_mode=False):
        if lazy_mode:
            return [edge.destiny for edge in self.list_of_all_edges() if edge.included]
        else:
            return [edge.destiny for edge in self.list_of_all_edges()]

    def list_of_all_edges(self, lazy_mode=False):
        if lazy_mode:
            return reduce(lambda x, y: x+y,
                          [vertex.edges.list_of_edges() for vertex in self.values() if vertex.included])
        else:
            return reduce(lambda x, y: x+y,
                          [vertex.edges.list_of_edges() for vertex in self.values()])

    def list_of_vertexes(self, lazy_mode=False):
        return [v.name for v in self._list_of_vertexes(lazy_mode)]

    def _list_of_vertexes(self, lazy_mode=False):
        if lazy_mode:
            return [v for v in self.values() if v.included]
        else:
            return list(self.values())

    def matrix_of_adjacence(self):
        def set_m(m, i, j, v):
            m[i, j] = v

        n = len(self._list_of_vertexes())
        self.set_infos(list(range(n)))

        matrix = {(i, j): 0 for j in range(n) for i in range(n)}

        [set_m(matrix, self[edge.source].info, edge.destiny_class.info, edge.weight)
         for edge in self.list_of_all_edges()]

        return matrix

    def set_infos(self, info):
        def set_info(v, info):
            if isinstance(info, dict):
                v.info = info.copy()
            elif isinstance(info, list):
                v.info = info.pop(0)
            else:
                v.info = info
        [set_info(vertex, info) for vertex in sorted(
            list(self._list_of_vertexes()), key=lambda x: x.name)]

    def set_infos_edges(self, info):
        def set_info(v, info):
            if isinstance(info, dict):
                v.info = info.copy()
            elif isinstance(info, list):
                v.info = info.pop(0)
            else:
                v.info = info
        [set_info(vertex, info) for vertex in self.list_of_all_edges()]

    def all_sinks(self):
        return [vertex for vertex in self._list_of_vertexes() if vertex.is_sink()]

    def all_sources(self, lazy_mode=False):
        return list(set(self.list_of_vertexes(lazy_mode)) - set(self.list_of_all_targets_edges(lazy_mode)))

    def reverse(self):
        n = len(self.list_of_vertexes())
        ids = {key: value for value, key in enumerate(self.list_of_vertexes())}

        g = [[] for i in range(n)]
        for edge in self.list_of_all_edges():
            g[ids[edge.source]] += [(ids[edge.destiny], edge.weight)]

        ids = {key: value for value, key in ids.items()}

        self.clear()
        for i in range(n):
            if not len(g[i]):
                self.add_vertex(ids[i])
            else:
                while len(g[i]):
                    id, w = g[i].pop()
                    self.add_single_edge(ids[id], ids[i], w)
