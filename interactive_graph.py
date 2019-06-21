from collections import Counter
from graph import graph, print_graph, random_graph, random_graph_weight, random_density_graph
import json
import re

def print_mat(mat, n):
    for i in range(n):
        for j in range(n):
            print("%3.0f" % mat[i, j], end=" ")
        print()
    print()


def print_res(res):
    keys = sorted(res.keys())
    c = Counter([value["d"] for key, value in res.items()])
    print()
    for key in keys:
        value = res[key]
        print(f"    From {key}: Distance( {value['d']:3.0f} ) and Predecessor( {value['p']} )")
    print()
    print("    Number of distances")
    for key, val in sorted(c.items()):
        print(f"    {key}: {val}")
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


class interactive_graph(object):
    def __init__(self):
        self.running = True
        self.command = ""
        self.g = graph()
        with open("metadata.settings.json", "r", encoding="UTF-8") as file:
            jsn = json.load(file)
            self.commands = jsn["commands"]
            self.redirect = jsn["redirect"]
        
    def _get_match(self, command):
        return re.match(self.commands[command]["match"], self.command)
    
    def _print_command(self, cmd):
        print(f"        {cmd['name']}: {cmd['help']}", end='\n\n')
    
    def add_graph(self):
        match = self._get_match("add")
        if match:
            frm = match["from"]
            to = match["to"]
            weight = match["weight"]
            if weight == None:
                weight = 1
            if to:
                self.g.add_single_edge(frm, to, weight)
            else:
                self.g.add_vertex(frm)

    def example_kruskal(self):
        self.command = "file ./examples/kruskal.txt"
        self.load_file_graph()
        self.print_graph()
        self.kruskal_graph()

    def examples(self):
        match = self._get_match("example")
        algorithm = match["algorithm"]
        function = self.commands["example"]["algorithm"][algorithm]
        if algorithm:
            eval(function)
        else:
            self._print_command(self.commands["example"])
    
    def docs(self):
        match = self._get_match("docs")
        algorithm = self.commands[match["algorithm"]] if match else None
        if algorithm:
            eval(algorithm["docs"])
        else:
            self._print_command(self.commands["docs"])

    def floydwarshall_graph(self):
        print("Floyd Warshall")
        res = self.g.floyd_warshall()
        n = len(self.g.list_of_vertexes())
        print("ID's")
        print(*res["ids"].items())

        print("Distancias")
        print_mat(res["d"], n)

        print("Predecessores")
        print_mat(res["p"], n)

    def bellman_ford_graph(self):
        print("Bellman Ford")

        match = self._get_match("bellmanford")
        first = match["first"]
        if first == None:
            first = list(self.g.keys())[0]
            print(f"From random {first}")
            res = self.g.bellman_ford(first)
        else:
            print(f"From {first}")
            res = self.g.bellman_ford(first)
        
        print_res(res)

    def kruskal_graph(self):
        print("Kruskal")
        res = self.g.kruskal()
        print(res)
    
    def bfs_graph(self):
        print("Breadth First Search")

        match = self._get_match("bfs")
        first = match["first"]
        if first == None:
            first = list(self.g.keys())[0]
            print(f"From random {first}")
            res = self.g.breadth_first_search(first)
        else:
            print(f"From {first}")
            res = self.g.breadth_first_search(first)

        print_res(res)

    def dijkstra_graph(self):
        print("Dijkstra")
        
        match = self._get_match("dijkstra")
        first = match["first"]
        if first == None:
            first = list(self.g.keys())[0]
            print(f"From random {first}")
            res = self.g.breadth_first_search(first)
        else:
            print(f"From {first}")
            res = self.g.breadth_first_search(first)
        
        print_res(res)

    def load_file_graph(self):
        match = self._get_match("file")
        filename = match["filename"]
        if filename != None:
            try:
                file_graph(self.g, filename)
            except IOError:
                print(f"Error when load a file '{filename}'.")
            except:
                print("Error!!!")
        else:
            self._print_command(self.commands["file"])

    def clear_graph(self):
        self.g.clear()

    def random_graph(self):
        match = self._get_match("random")
        n = match["num"]
        if n != None:
            self.clear_graph()
            n = int(n)
            mtype = match["type"]
            if mtype == None:
                random_graph(self.g, n)
            elif mtype == "weight":
                random_graph_weight(self.g, n)
            elif mtype == "density":
                random_density_graph(self.g, n)
            else:
                self._print_command(self.commands["random"])
        else:
            self._print_command(self.commands["random"])

    def print_graph(self):
        self.g.print()

    def exit(self):
        self.running = False
    
    def input_command(self):
        self.command = input("> ").strip()

    def help(self):
        for cmd in sorted(self.commands.values(), key=lambda c: c["name"]):
            self._print_command(cmd)
    
    def execute_command(self, cmds):
        for cmd in cmds.split("|"):
            cmd = cmd.strip()
            self.command = cmd
            name = cmd.split(" ", 1)[0]
            if name in self.redirect:
                name = self.redirect[name]

            cmd = self.commands.get(name, None)
            if cmd:
                eval(cmd["fnct"])
            else:
                print(f"Erro in '{self.command}'")
                print("Command not found.")
                print("Use 'help' for list all commands.")
                print()

    def run(self):
        print("Interactive graph.")
        print("Use 'help' to list all commands.")
        print()
        while self.running:
            self.input_command()
            self.execute_command(self.command)

if __name__ == "__main__":
    # example_prim()
    interactive = interactive_graph()
    # interactive.execute_command("random 5 | print | bellmanford ")
    # interactive.execute_command("file ./examples/kruskal.txt | print")
    # interactive.execute_command("example 1")
    interactive.run()
    