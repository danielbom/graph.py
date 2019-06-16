from collections import Counter
from vertexes import vertexes
import disjoint_set as dset
import random
import math
import re

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
    delim = r"[ ]*\-\>[ ]*"
    regex = re.compile(r"(?P<from>[^\-\>]*)" + delim +
                        r"(?P<to>[^\-\>]*)" + delim +
                        r"(?P<weight>[\d]+(\.[\d]+))?")
    with open(filename) as file:
        for line in file.readlines():
            match = regex.match(line.strip())
            weight = match["weight"]
            if weight == None:
                weight = 1
            graph.add_edge(match["from"], match["to"], weight)

def random_graph(graph, limite=20):
    for _ in range(limite):
        graph.add_edge(random.randint(0, limite), random.randint(0, limite))

def random_graph_weight(graph, limite=20):
    for _ in range(limite):
        graph.add_edge(random.randint(0, limite), random.randint(
            0, limite), random.randint(0, limite*10))

def random_density_graph(graph, limite=20):
    for _ in range(limite*100):
        graph.add_edge(random.randint(0, limite), random.randint(0, limite))

def print_graph(graph):
    print(*sorted(list(graph.values()), key=lambda x: x.name), sep='\n')
    print()

class graph(vertexes):
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

        self.set_infos(None)
        return returned

    def depth_first_search(self, begin):
        raise NotImplementedError

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

            for _ in range(len(self.keys())):
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
                ... TODO: Usar o 2º link para completar esta parte.
            
            Passos realizados para encontrar a MST usando o algoritmo de Kruskal
                1 - Ordene todas as arestas na order crescente de pesos.
                2 - Pege a aresta de menor peso. Verifique se ele forma ciclos
                com a árvore geradora. Se ele não formar, inclua a aresta. Se
                não, descarte-a.
                3 - Repita o passo 2 até existirem (V - 1) vértices na MST.
            
            Links:
            https://www.geeksforgeeks.org/?p=26604/
            https://www.geeksforgeeks.org/applications-of-minimum-spanning-tree/
        '''
        # n = len(self.keys())
        # TODO: Usar fila de prioridades
        all_egdes = sorted(self.list_of_all_edges(), key=lambda x: x.weight)

        ds = dset.disjoint_set()
        mst = []
        for e in all_egdes:
            if ds.union(e.source, e.destiny):
                mst.append({
                    "p": e.source,
                    "s": e.destiny,
                    "wt": e.weight
                })

        return mst

    def prim(self, begin=None):
        ''' Constrói a árvore geradora mínima do presente grafo.

            Parâmetros
            ----------
            self : graph
                Estrutura de dados grafo.
            begin : string | int, opcional
                Valor inicial para a construção da árvore. Caso não seja
                especificado, uma valor aleatório é utilizada.
            
            Retornos:
            ---------
            list
                Retorna os resultados da árvore geradora mínina em uma lista.
            
            Informações adicionais
            ----------------------
            A ideia por trás do algoritmo de Prim é simple, em uma árvore
            geradora mínima, todos os vértices devem se conectar. Então dois,
            conjuntos disjuntos de vértices são conectados para contruir a
            a árvore. E elas devem ser conectadas com as arestas de menor peso
            para construir a ávore geradora minima.

            Passos realizados para encontrar a MST usando o algoritmo de Prim.
                1 - Crie um conjunto para controlar os vértices já incluídos.
                2 - Marque um valor chame en todos os vértices do grafo com o 
                valor infinito. Marque 0 para o primeiro vértice e guarde-o.
                3 - Enquanto todos os vértices não forem incluídos na árvore
                    a - Pegue um vértice 'u' que não está incluído na MST e
                    possui a menor chave.
                    b - Inclua 'u' na MST.
                    b - Atualize as chaves dos vértices adjacentes de 'u', se
                    o novo valor é menor do que o que os vértices adjacentes
                    possuem.
            
            A ideia de usar um valor chave é pegar o menor peso da aresta de
            corte. O valor chave é usado somente para o vértice que não está
            incluído na MST. e este valor indica o peso das arestas conectadas
            até ele na MST.

            Links:
            https://www.geeksforgeeks.org/prims-minimum-spanning-tree-mst-greedy-algo-5/
        '''
        # TODO: Change the all_vertex by a priority queue
        # TODO: Use diisjoint set to now if has generate cicle
        self.set_infos({"key": math.inf, "p": None})
        
        if begin is None:
            begin = random.choice(list(self.keys()))
        vertex = self.get(begin)
        vertex.info["key"] = 0
        
        all_vertex, mst = self._list_of_vertexes(), []
        mst.append({"p": None, "s": vertex.name, "wt": vertex.info["key"]})
        while True:
            all_vertex.remove(vertex)

            for edge in vertex.list_of_edges():
                destiny = edge.destiny_class
                if destiny not in all_vertex:
                    continue
                new_weight = edge.weight + vertex.info["key"]
                if new_weight < destiny.info["key"]:
                    destiny.info["key"] = new_weight
                    destiny.info["p"] = vertex.name
            
            if not all_vertex:
                break

            vertex = min(all_vertex, key=lambda v: v.info["key"])
            mst.append({
                "p": vertex.info["p"],
                "s": vertex.name,
                "wt": vertex.info["key"]
            })

        self.set_infos(None)
        return mst

    # Fluxo maximo
    def ford_fulkerson(self, begin, end):
        raise NotImplementedError

    def dinic(self, begin, end):
        raise NotImplementedError

    def edmonds_karp(self, begin, end):
        raise NotImplementedError

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
        raise NotImplementedError

    # Auxiliares
    def has_circle(self):
        ds = dset.disjoint_set()
        for e in self.list_of_all_edges():
            if not ds.union(e.source, e.destiny):
                return True
        return False

    def print(self):
        print(*sorted(self.values(), key=lambda x: x.name), sep='\n', end='\n\n')
