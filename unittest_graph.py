
# python3 -m unittest unittest_vertexes.py -v

from graph import *
import copy
import unittest

def simple_graph(graph):
    graph.add_single_edge("a", "b")
    graph.add_single_edge("b", "c")
    graph.add_single_edge("d", "e")
    graph.add_single_edge("e", "f")

class Unittestgraph(unittest.TestCase):
    def setUp(self):
        self.graph = graph()

    def test_add_single_egde(self):
        length = len(self.graph)
        self.graph.add_single_edge("a", "b", 10)
        self.assertEqual(len(list(self.graph.edges())), length+1)

    def test_add_edges(self):
        length = len(self.graph)
        self.graph.add_edge("c", "d", 10)
        self.assertEqual(len(list(self.graph.edges())), length+2)

    def test_not_has_circle(self):
        self.assertEqual(self.graph.has_circle(), False, "Empty")
        self.graph.add_single_edge("a", "b")
        self.assertEqual(self.graph.has_circle(), False, "One [a -> b, b -> c, c -> d]")
        self.graph.add_single_edge("b", "c")
        self.graph.add_single_edge("c", "d")
        self.assertEqual(self.graph.has_circle(), False, "Three")
    
    def test_has_circle(self):
        self.assertEqual(self.graph.has_circle(), False, "Empty")
        self.graph.add_single_edge("a", "b")
        self.graph.add_single_edge("b", "c")
        self.graph.add_single_edge("c", "d")
        self.graph.add_single_edge("d", "a")
        self.assertEqual(self.graph.has_circle(), True, "Four [a -> b, b -> c, c -> d, d -> a]")

    def test_kosajaru(self):
        self.assertRaises(NotImplementedError,self.graph.kosajaru)

    def test_reverse_simple(self):
        simple_graph(self.graph)
        gcopy = copy.deepcopy(self.graph)
        self.assertEqual(gcopy == self.graph, True)
        self.graph.reverse()
        self.assertEqual(gcopy == self.graph, False)

    def test_reverse_oriented(self):
        random_graph(self.graph, oriented=True)
        gcopy = copy.deepcopy(self.graph)
        self.assertEqual(gcopy == self.graph, True)
        self.graph.reverse()
        self.assertEqual(gcopy == self.graph, False)

    def test_reverse_bidirectional(self):
        random_graph(self.graph, oriented=False)
        gcopy = copy.deepcopy(self.graph)
        self.assertEqual(gcopy == self.graph, True)
        self.graph.reverse()
        self.assertEqual(gcopy == self.graph, True)

    def test_vertexes_names(self):
        simple_graph(self.graph)
        self.assertEqual(set(self.graph.vertexes_names()), set("abcdef"))
    
    def test_vertexes_names_lazy(self):
        simple_graph(self.graph)
        self.graph._remove_vertex("b")
        self.graph._remove_vertex("e")
        self.assertEqual(set(self.graph.vertexes_names(True)), set("acdf"))

    def test_edges_destination(self):
        simple_graph(self.graph)
        destinations = set(self.graph.edges_destinations())
        self.assertEqual(destinations, set("bcef"))

    def test_edges_destination_lazy(self):
        simple_graph(self.graph)
        self.graph._remove_vertex("b")
        self.graph._remove_vertex("e")
        destinations = set(self.graph.edges_destinations(True))
        self.assertEqual(destinations, set("be"))

    
    
    def test_edmonds_karp(self):
        pass
    
    def test_dinic(self):
        pass

    def test_depth_first_search(self):
        pass



    def test_topological_sort(self):
        simple_graph(self.graph)
        self.graph.topological_sort()
    
    def test_khan(self):
        simple_graph(self.graph)
        self.graph.khan()

    def test_ford_fulkerson(self):
        self.graph.floyd_warshall()
        simple_graph(self.graph)
        res = self.graph.floyd_warshall()

    def test_prim(self):
        simple_graph(self.graph)
        self.graph.prim()
    
    def test_kruskal(self):
        simple_graph(self.graph)
        self.graph.kruskal()
    
    def test_floyd_warshall(self):
        simple_graph(self.graph)
        self.graph.floyd_warshall()        
    
    def test_bellman_ford(self):
        simple_graph(self.graph)
        self.graph.bellman_ford("a")
    
    def test_dijkstra(self):
        simple_graph(self.graph)
        self.graph.dijkstra("a")

    def test_breadth_first_search(self):
        simple_graph(self.graph)
        self.graph.breadth_first_search("a")



if __name__ == "__main__":
    unittest.main()