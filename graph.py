import vertexes
import random
import math
import disjoint_set as dset
from collections import Counter
from functools import reduce

'''
    Caminhos mínimos de fonte única:
    Determina o menor caminho de um vértice até todos os outros vértices.
    Caminhos mínimos de todas as fontes:
    Determina o menor caminho de todos os vértices para todos os outros vértices.

    Árvore geradora mínima:


    Ordenação topológica:
    * Para grafos direcionados acíclicos.
    Os vértices representam alguma tarefa ou recurso, que depende das ligações das arestas.
    As direções das arestas representam restrições e/ou pré-requisitos.
    Ordena os vértices de acordo com as 'direçoes das arestas'.
'''

# p : predecessor
# s : sucessor
# wt : weight
# d : distancia


def file_graph(graph, filename):
    with open(filename) as file:
        content = [line.strip() for line in file.readlines()]
        friends = list(map(lambda friend: tuple(
            friend.split(' -> ')), content))
        for frm, to in friends:
            graph.add_edge(frm, to)


def random_graph(graph, limite=20):
    for i in range(limite):
        graph.add_edge(random.randint(0, limite), random.randint(0, limite))


def random_graph_weight(graph, limite=20):
    for i in range(limite):
        graph.add_edge(random.randint(0, limite), random.randint(
            0, limite), random.randint(0, limite*10))


def random_density_graph(graph, limite=20):
    for i in range(limite*100):
        graph.add_edge(random.randint(0, limite), random.randint(0, limite))


def print_graph(graph):
    print(*sorted(list(graph.values()), key=lambda x: x.name), sep='\n')
    print()


class graph(vertexes.vertexes):
    # Buscas
    def breadth_first_search(self, begin):
        '''
            Busca em largura
        '''
        begin_class = self.get(begin)
        if begin_class != None:
            self.set_infos({"cor": 'b', "d": math.inf, "p": None})

            begin_class.info["cor"] = 'c'
            begin_class.info["d"] = 0

            fila = [begin_class]

            while len(fila):
                vertex_1 = fila.pop(0)
                for vertex_2 in vertex_1.edges.list_of_vertexes():
                    if vertex_2.info["cor"] == 'b':
                        vertex_2.info["cor"] = 'c'
                        vertex_2.info["d"] = vertex_1.info["d"]+1
                        vertex_2.info["p"] = vertex_1.name
                        fila.append(vertex_2)
                vertex_2.info["cor"] = 'p'

        returned = {vertex.name: vertex.info.copy()
                    for vertex in self._list_of_vertexes()}

        self.set_infos(0)
        return returned

    def depth_first_search(self, begin):
        '''
            Busca em profundidade
        '''
        pass

    # Determinar caminho
    def dijkstra(self, begin):
        '''
            O caminho mais curto de um nó até todos os outros nós.

            Não permite pesos negativos.
        '''
        def all_get(name):
            return _all.get(name, {"d": 0})["d"]

        returned = {}
        if self.get(begin) != None:
            # Para cada vertice, vou associar seu nome com um peso e um predecessor
            _all = {vertex.name: {"d": math.inf, "p": None}
                    for vertex in self._list_of_vertexes()}

            # Altero o peso do nó inicial para 0
            _all[begin]["d"] = 0

            while len(_all):
                # Encontro e removo o nó com a menor peso
                _min = min(_all, key=lambda x: _all[x]["d"])
                returned[_min] = _all.pop(_min)

                # Para cada vertice alcançável pelo meu menor elemento
                # faço o relaxamento dos pesos
                for edge in self[_min].edges.list_of_edges():
                    _sum = returned[_min]["d"] + edge.weight
                    if all_get(edge.destiny) > _sum:
                        _all[edge.destiny]["d"] = _sum
                        _all[edge.destiny]["p"] = _min

        return returned

    def bellman_ford(self, begin):
        '''
            O caminho mais curto de um nó até todos os outros nós.

            Permite pesos negativos.
        '''
        # Modelo parecido com a busca em profundidade
        begin_class = self.get(begin)
        if begin_class != None:
            self.set_infos({"d": math.inf, "p": None})

            begin_class.info["d"] = 0

            for i in range(len(self.keys())):
                for vertex in self._list_of_vertexes():
                    for edge in vertex.edges.list_of_edges():
                        # soma das distancias
                        _sum = edge.destiny_class.info["d"] + edge.weight
                        if vertex.info["d"] > _sum:
                            vertex.info["d"] = _sum
                            vertex.info["p"] = edge.destiny
                            relax = True
                if not relax:
                    break

        returned = {vertex.name: vertex.info.copy()
                    for vertex in self._list_of_vertexes()}
        self.set_infos(None)
        return returned
        # Modelo com vetores auxiliares
        '''
        n = len(self.keys())
        d = [math.inf for v in range(n)]
        p = [None for v in range(n)]
        self.set_infos(list(range(n)))

        d[self[begin].info] = 0

        for i in range(n):
            relax = False
            for vertex in self._list_of_vertexes():
                for edge in vertex.edges.list_of_edges():
                    _sum = d[edge.destiny_class.info] + edge.weight
                    if d[vertex.info] > _sum:
                        d[vertex.info] = _sum
                        p[vertex.info] = edge.destiny
                        relax = True
            if not relax:
                break

        return {vertex.name: {"id": vertex.info, "d": d[vertex.info], "p": p[vertex.info]} for vertex in self._list_of_vertexes()}
        '''

    def floyd_warshall(self):
        '''
            O caminho mais curto de todos os nó até todos os outros nós.
        '''
        d = {key: math.inf if value == 0 and key[0] != key[1] else value
             for key, value in self.matrix_of_adjacence().items()}
        p = {key: key[0] if value != math.inf and key[0] != key[1] else -1
             for key, value in d.items()}
        n = len(self.keys())

        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if d[i, j] > d[i, k] + d[k, j]:
                        d[i, j] = d[i, k] + d[k, j]
                        p[i, j] = p[k, j]

        ids = {vertex.name: vertex.info for vertex in self._list_of_vertexes()}

        return {"ids": ids, "d": d, "p": p}

    # Arvore geradora de custo minimo
    def kruskal(self):
        ''' Cálculo da árvore geradora mínima deste grafo a partir do algoritmo
            de Kruskal.

            Parâmetros
            ----------
            self : graph
                Grafo.

            Retornos
            --------
            list
                Retorna a arvore geradora mínima deste grafo.
            
            Informações adicionais
            ----------------------
            Dado um grafo conectado e unidirecional, uma árvore geradora
            deste grafo é um subgrafo na forma de árvore e que conecta todos
            os vértices juntos. Um único grafo por ter diferentes árvores
            geradoras mínimas. Uma árvore geradora mínima (MST) ou árvore
            geradora de peso mínimo de um grafo ponderado unidirecional e
            conectado é uma árvore geradora com o peso menor ou igual todas
            as outras árvores geradoras possíveis. A o peso da árvore geradora 
            é a soma dos pesos de cada uma de suas arestas.

            Quantas arestas formam uma árvore geradora?
                Uma árvore geradora mínima tem (V - 1) arestas, onde V é o
            número de vértices do grafo.

            Onde aplicar as árvores geradoras mínimas?
                ...
            
            Passos realizados para encontrar a MST usando o algoritmo de Kruskal
                1 - Ordene todas as arestas na order crescente de pesos.
                2 - Pege a aresta de menor peso. Verifique se ele forma ciclos
                com a árvore geradora. Se ele não formar, inclua a aresta. Se
                não, descarte-a.
                3 - Repita o passo 2 até existirem (V - 1) vértices na MST.
        '''
        # n = len(self.keys())
        # TODO: Usar fila de prioridades
        all_egdes = sorted(self.list_of_all_edges(), key=lambda x: x.weight)

        ds = dset.disjoint_set()
        mst = []
        for e in all_egdes:
            if ds.union(e.source, e.destiny):
                mst.append(
                    {"p": e.source, "s": e.destiny, "wt": e.weight})

        return mst

    def prim(self):
        pass

    # Fluxo maximo
    def ford_fulkerson(self, begin, end):
        pass

    def dinic(self, begin, end):
        pass

    def edmonds_karp(self, begin, end):
        pass

    # Ordenacao topologica
    def khan(self):
        LAZY_MODE = True
        sorted_list = []

        sources = set(self.all_sources(LAZY_MODE))
        while len(sources):
            while len(sources):
                poped = sources.pop()
                sorted_list.append(poped)
                self._remove_vertex(poped)
            sources = set(self.all_sources(LAZY_MODE))

        self._include_all()
        return sorted_list + list(sources)

    def _topological_sort(self, vertex, sorted_list):
        if not self[vertex].included:
            self[vertex].included = True
            for destiny in self[vertex].list_of_targets_edges():
                self._topological_sort(destiny, sorted_list)
            sorted_list.append(vertex)

    def topological_sort(self):
        # I'm not secure with this algorithm
        self.reverse()
        self._remove_all_vertex()  # Not visited
        sources = self.all_sources()
        sorted_list = []

        while len(sources):
            self._topological_sort(sources.pop(), sorted_list)

        # self._include_all() # In fact, all vertexes must be visited
        self.reverse()
        return sorted_list

    # Componentes fortemente conexas
    def kosajaru(self):
        pass

    # Auxiliares
    def has_circle(self):
        pass

    def print(self):
        print(*sorted(self.values(), key=lambda x: x.name), sep='\n', end='\n\n')
