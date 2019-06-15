

graph(vertexes)
{
// Buscas
#define breadth_first_search(begin; string) ; // OK
#define depth_first_search(begin; string) ;
// Determinar caminho
#define dijkstra(begin; string) ;     // OK
#define bellman_ford(begin; string) ; // OK
#define floyd_warshall() ;
// Arvore geradora de curso minimo
#define kruskal() ; // OK
#define prim() ;
// Fluxo maximo
#define ford_fulkerson(begin; string, end; string) ;
#define dinic(begin; string, end; string) ;
#define edmonds_karp(begin; string, end; string) ;
// Ordenacao topologica
#define khan() ;
#define topological_sort() ;
// Componentes fortemente conexas
#define kosajaru() ;
// Aux
#define has_circle() ;
}

vertexes(dict)
{
#define add_vertex(name; string) ;                                              // OK
#define add_edge(source; string, destiny; string, weigth; int / float) ;        // OK
#define add_single_edge(source; string, destiny; string, weigth; int / float) ; // OK
#define list_of_all_edges() ;                                                   // OK
#define list_of_vertexes() ;                                                    // OK
#define matrix_of_adjacence() ;
#define set_infos(info; object) ; // OK
#define all_sinks() ;
#define all_sources() ;
}

// Cada vertice possui
vertex(object)
{
    typedef(name; string);
    typedef(info; object);
    typedef(edges; edges);
#define add(source; string, destiny; string, weigth; int / float) ;
#define is_sink() ;
#define is_source() ;
}

// Apartir das arestas de um vertice e possivel
edges(dict)
{
#define add(source; string, destiny; string, destiny_class; vertex, weigth; int / float) ; // OK
#define list_of_edges() ;                                                                  // OK
#define list_of_vertexes() ;                                                               // OK
}

edge(object)
{
    typedef(destiny_class; vertex);
    typedef(destiny; string);
    typedef(source; string);
    typedef(weigth; int / float);
    typedef(info; object);
}

disjoint_set(dict)
{
#define find(x; string) ;               // OK
#define union(x; string, y; string);    // OK
#define makeset(x; string, y; string) ; // OK
}

dict(object)
{
#define clear() ;
#define copy() ;
#define fromkeys() ;
#define get() ;
#define items() ;
#define keys() ;
#define pop() ;
#define popitem() ;
#define setdefault() ;
#define update() ;
#define values() ;
}