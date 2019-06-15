from graph import *


def print_mat(mat, n):
    for i in range(n):
        for j in range(n):
            print("%3.0f" % mat[i, j], end=" ")
        print()
    print()


def exemple_kruskal():
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


def exemple_dijkstra_and_bellman_ford():
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


def exemple_floyd_warshall():
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


def exemple_topological_sort():
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


if __name__ == "__main__":
    EXEMPLES = True

    FLOYD_WARSHALL = False
    BELLMAN_FORD = False
    DIJKSTRA = False
    KRUSKAL = False
    BFS = True

    PRINT_GRAPH = FLOYD_WARSHALL or BELLMAN_FORD or DIJKSTRA or KRUSKAL or BFS

    g = graph()
    n = 15
    # file_graph(g, "teste.txt")
    # file_graph(g, "amigos.txt")
    random_graph_weight(g, n)

    if PRINT_GRAPH:
        print("Grafo")
        if n <= 20:
            g.print()
        print()

        initial = list(g.keys())[0]
        print("Inicial:", initial)

    if BFS:
        print("Breadth First Search")
        res = g.breadth_first_search(initial)
        if n <= 20:
            for i in res.items():
                print(i)

        c = Counter([value["d"] for key, value in res.items()])
        print()
        print(sorted(list(c.items()), key=lambda x: x[0]))
        print()

    if DIJKSTRA:
        print("Dijkstra")
        res = g.dijkstra(initial)
        if n <= 20:
            for r in res.items():
                print(r)
        print()

    if KRUSKAL:
        print("Kruskal")
        res = g.kruskal()

        if n <= 20:
            for r in sorted(res.items(), key=lambda x: x[0]):
                print(r)
        print()

    if BELLMAN_FORD:
        print("Bellman Ford")
        res = g.bellman_ford(initial)
        if n <= 20:
            for i in res.items():
                print(i)
        print()

    if FLOYD_WARSHALL:
        print("Floyd Warshall")
        res = g.floyd_warshall()
        n = len(g.list_of_vertexes())
        print("ID's")
        print(*res["ids"].items())

        print("Distancias")
        print_mat(res["d"], n)

        print("Predecessores")
        print_mat(res["p"], n)

    if EXEMPLES:
        # exemple_kruskal()
        # exemple_dijkstra_and_bellman_ford()
        # exemple_floyd_warshall()
        exemple_topological_sort()
