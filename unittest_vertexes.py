
# python3 -m unittest unittest_vertexes.py -v

from vertexes import vertexes
import unittest

glen = lambda gen: sum(1 for _ in gen)

class UnittestVertexes(unittest.TestCase):
    def setUp(self):
        self.vertexes = vertexes()

    def test_add_single_egde(self):
        length = len(self.vertexes)
        self.vertexes.add_single_edge("a", "b", 10)
        self.assertEqual(glen(self.vertexes.edges()), length+1)

    def test_add_edges(self):
        length = len(self.vertexes)
        self.vertexes.add_edge("c", "d", 10)
        self.assertEqual(glen(self.vertexes.edges()), length+2)


if __name__ == "__main__":
    unittest.main()