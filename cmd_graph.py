from cmd import Cmd
from collections import Counter
from graph import graph, file_graph, print_graph, random_graph, random_weight_graph, random_density_graph
import math
import re

g = graph()

algorithm_docs = {}
try:
    with open("algorithms.docs.json", "r", encoding="UTF-8") as file:
        algorithm_docs = json.load(file)
except:
    pass


def get_first(g, inp):
    first = inp.strip()

    if first:
        if first in g:
            print(f"From {first}")
        elif first.isdigit() and int(first) in g:
            first = int(first)
            print(f"From {first}")
    else:
        first = list(g.keys())[0]
        print(f"From random {first}")

    return first


def print_mat(mat, n):
    for i in range(n):
        for j in range(n):
            print("%3.0f" % mat[i, j], end=" ")
        print()
    print()


def print_res(res):
    keys = sorted(res.keys(), key=lambda k: res[k]['d'])
    c = Counter([value["d"] for key, value in res.items()])
    print()
    for key in keys:
        value = res[key]
        if math.isinf(value['d']):
            continue
        print(f"  From '{value['p']}' with distance '{value['d']}' to '{key}'")
    print()
    print("Number of distances")
    for i, pair in enumerate(sorted(c.items())):
        key, val = pair
        print(f"  {key}: {val}", end='')
        if i > 0 and i % 5 == 0:
            print()
        else:
            print(' |', end='')
    print()


def example_kruskal():
    g = graph()
    g.add_edge(0, 1, 4)
    g.add_edge(0, 7, 8)
    g.add_edge(1, 7, 11)
    g.add_edge(1, 2, 8)
    g.add_edge(2, 8, 2)
    g.add_edge(2, 5, 4)
    g.add_edge(2, 3, 7)
    g.add_edge(6, 5, 2)
    g.add_edge(7, 8, 7)
    g.add_edge(7, 6, 1)
    g.add_edge(8, 6, 6)
    g.add_edge(3, 4, 9)
    g.add_edge(3, 5, 14)
    g.add_edge(4, 5, 10)

    print("Kruskal exemple")
    res = g.kruskal()

    for r in res:
        print(r)
    print()


def example_dijkstra_and_bellman_ford():
    g = graph()
    g.add_edge("A", "B", 4)
    g.add_edge("A", "C", 2)
    g.add_edge("B", "C", 1)
    g.add_edge("B", "D", 5)
    g.add_edge("C", "D", 8)
    g.add_edge("C", "E", 10)
    g.add_edge("D", "E", 2)
    g.add_edge("D", "F", 6)
    g.add_edge("E", "F", 2)

    print("Grafo")
    print_graph(g)
    print()

    initial = "A"
    print("Inicial:", initial)

    print("Dijkstra exemple")
    res = g.dijkstra(initial)
    for r in sorted(list(res.items()), key=lambda x: x[0]):
        print(r)
    print()

    print("Bellman Ford exemple")
    res = g.bellman_ford(initial)
    for r in sorted(list(res.items()), key=lambda x: x[0]):
        print(r)
    print()


def example_floyd_warshall():
    g = graph()
    g.add_single_edge(1, 2, 3)
    g.add_single_edge(1, 3, 8)
    g.add_single_edge(1, 5, -4)
    g.add_single_edge(2, 4, 1)
    g.add_single_edge(2, 5, 7)
    g.add_single_edge(3, 2, 4)
    g.add_single_edge(4, 1, 2)
    g.add_single_edge(4, 3, -5)
    g.add_single_edge(5, 4, 6)

    print("Grafo")
    print_graph(g)
    print()

    res = g.floyd_warshall()

    n = len(g.list_of_vertexes())

    print("ID's")
    print(*res["ids"].items())

    print("Distancias")
    print_mat(res["d"], n)

    print("Predecessores")
    print_mat(res["p"], n)


def example_topological_sort():
    g = graph()
    g.add_single_edge("Camisa", "Cinto")
    g.add_single_edge("Camisa", "Gravata")
    g.add_single_edge("Gravata", "Paleto")
    g.add_single_edge("Cinto", "Paleto")
    g.add_single_edge("Calca", "Cinto")
    g.add_single_edge("Cueca", "Calca")
    g.add_single_edge("Cueca", "Sapato")
    g.add_single_edge("Meia", "Sapato")
    g.add_vertex("Relogio")

    print("Khan example")
    res = g.khan()
    print(*res)

    print("Topological sort DFS exemple")
    res = g.topological_sort()
    print(*res)


def example_prim():
    g = graph()
    g.add_edge(0, 1, 4)
    g.add_edge(0, 7, 8)
    g.add_edge(1, 7, 11)
    g.add_edge(1, 2, 8)
    g.add_edge(2, 8, 2)
    g.add_edge(2, 5, 4)
    g.add_edge(2, 3, 7)
    g.add_edge(6, 5, 2)
    g.add_edge(7, 8, 7)
    g.add_edge(7, 6, 1)
    g.add_edge(8, 6, 6)
    g.add_edge(3, 4, 9)
    g.add_edge(3, 5, 14)
    g.add_edge(4, 5, 10)

    res = g.prim(0)

    for i in res:
        print(i)


examples = [
    example_kruskal,
    example_floyd_warshall,
    example_topological_sort,
    example_dijkstra_and_bellman_ford,
    example_prim,
]
examples_names = [e.__name__ for e in examples]
examples_dict = dict(zip(examples_names, examples))


class Prompt(Cmd):
    intro = "Interactive graph. Use 'help' to list all commands."
    prompt = "> "

    # docs
    def do_docs(self, inp):
        print("docs")

    def help_docs(self):
        print("? Show the docs string of a command.")

    # print
    def do_print(self, inp):
        if not g:
            return print("Graph is empty")

        print_graph(g)

    def help_print(self):
        print("? Print the graph.")

    # random
    def do_random(self, inp):
        values = re.split(r"\s+", inp)
        len_values = len(values)
        if len_values >= 1 and values[0].isdigit():
            g.clear()
            n = int(values[0])
            m = values[1] if len_values > 1 else None
            if m is None:
                print("Create a basic random graph")
                return random_graph(g, n)
            if "weight".startswith(m):
                print("Weight random graph created")
                return random_weight_graph(g, n)
            if "density".startswith(m):
                print("Density random graph created")
                return random_density_graph(g, n)
        self.help_random()

    def help_random(self):
        print("? Create a new graph of a given length.")
        print("\n\trandom N [weight|density]")

    # file
    def do_file(self, inp):
        try:
            file_graph(g, inp)
        except IOError:
            print(f"Error when load a file '{inp}'.")
        except Exception as e:
            print("Error!!!")
            print(e)

    def help_file(self):
        print("? Load a graph from a file.")

    # clear
    def do_clear(self, inp):
        g.clear()

    def help_clear(self):
        print("? help_clear")

    # add
    def do_add(self, inp):
        values = re.split(r"\s+", inp)[:3]
        n = len(values)

        if n == 1:
            g.add_vertex(values[0])
            return print("Add vertex '{}'", *values)
        if n == 2:
            values.append(1)
            g.add_single_edge(*values)
            return print("Add edge '{} -> {} -> 1'", *values)
        if values[-1].isdigit():
            values[-1] = int(values[-1])
            g.add_single_edge(*values)
            return print("Add edge '{} -> {} -> 1'", *values)

        print("The last element (weight) must be a integer")

    def help_add(self):
        print("? Add vertexs and egdes to the graph.")

    # example
    def do_example(self, inp):
        inp = inp.strip()
        for name in examples_names:
            if inp == name:
                return examples_dict[name]()

        for name in examples_names:
            if name.startswith(inp):
                return examples_dict[name]()

        for name in examples_names:
            if inp in name:
                return examples_dict[name]()

    def help_example(self):
        print("? Show examples from number or name.\n\t\t1 kruskal\n\t\t2 floyd warshall\n\t\t3 topologiical sort\n\t\t4 dijkstra bellmanford")

        print("Remove all elements of a graph.")

        print("Run the Kruskal's algorithm for generate a Minimal Spanning Tree")

    # bellmanford
    def do_bellmanford(self, inp):
        if not g:
            return print("Graph is empty")

        print("Bellman Ford")

        first = get_first(g, inp)

        res = g.bellman_ford(first)
        print_res(res)

    def help_bellmanford(self):
        print("? Run the Bellman Ford's algorithm for...")

    # bfs
    def do_bfs(self, inp):
        if not g:
            return print("Graph is empty")

        print("Breadth First Search")

        first = get_first(g, inp)

        res = g.breadth_first_search(first)
        print_res(res)

    def help_bfs(self):
        print("? Run a breadth first search in the current graph.")

    # dfs
    def do_dfs(self, inp):
        if not g:
            return print("Graph is empty")

        print("Breadth First Search")

        first = get_first(g, inp)

        res = g.depth_first_search(first)
        print_res(res)

    def help_dfs(self):
        print("? Run a depth first search in the current graph.")

    # dijkstra
    def do_dijkstra(self, inp):
        if not g:
            return print("Graph is empty")

        print("Dijkstra")
        first = get_first(g, inp)
        res = g.dijkstra(first)
        print_res(res)

    def help_dijkstra(self):
        print("? Run the Dijkstra's algorithm for minimum distances.")

    # floydwarshall
    def do_floydwarshall(self, inp):
        if not g:
            return print("Graph is empty")

        print("Floyd Warshall")
        res = g.floyd_warshall()
        n = len(g.list_of_vertexes())
        print("ID's")
        print(*res["ids"].items())

        print("Distancias")
        print_mat(res["d"], n)

        print("Predecessores")
        print_mat(res["p"], n)

    def help_floydwarshall(self):
        print("? help_floydwarshall")

    # kruskal
    def do_kruskal(self, inp):
        if not g:
            return print("Graph is empty")

        print("Kruskal")
        res = g.kruskal()
        print(res)

    def help_kruskal(self):
        print("? help_kruskal")

    # redirects
    def do_p(self, inp):
        return self.do_print(inp)
    
    def do_r(self, inp):
        return self.do_random(inp)

    def do_bf(self, inp):
        return self.do_bellmanford(inp)

    def do_d(self, inp):
        return self.do_dijkstra(inp)

    def do_fw(self, inp):
        return self.do_floydwarshall(inp)

    def do_k(self, inp):
        return self.do_kruskal(inp)


if __name__ == "__main__":
    Prompt().cmdloop()
