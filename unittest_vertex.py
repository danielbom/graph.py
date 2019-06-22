
# python3 -m unittest unittest_vertex.py -v

from vertex import vertex
import unittest

class UnittestVertex(unittest.TestCase):
    def setUp(self):
        self.vertex = vertex("test")

    def test_add_egde(self):
        self.assertEqual(len(self.vertex.edges), 0)
        self.vertex.add(vertex("b"), 10)
        self.assertEqual(len(self.vertex.edges), 1)


if __name__ == "__main__":
    unittest.main()