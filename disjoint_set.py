import random


class disjoint_set(dict):
    ''' Conjuntos disjuntos é uma estrutura de dados que controla um conjunto de
        elementos particionados em vários subconjuntos disjuntos. O algoritmo
        union-find é um algorimo que realiza duas operações nesta estrutura:
        
        Find: Determina qual subconjunto um elemento particular está. Ele pode
        ser usado para determinar se dois elementos estão no mesmo subconjunto.

        Union: Une dois conjuntos em um único subconjunto.

        * O algoritmo union-find pode ser usado para verificar se um grafo
        unidirecional possui ciclos ou não.
    '''
    # ranked
    def _find_ranked(self, x, rank=0):
        ''' Encontra o ancestral e o ranking deste ancestral a partir de um 
            elemento.
        
            Parâmetros
            ----------
            self : disjoint_set<T>
                Conjunto disjunto que armazena as informações dos conjuntos.
            x : T
                Parâmetro de busca para o subconjunto que ele se encontra.
            rank : int
                Rank do elemento buscado. Quanto menor, maior sua prioridade.
            
            Retornos
            --------
            tuple
                Retorna o último ancestral do elemento x e seu rank.
        '''
        father = self.get(x, x)
        return (x, rank) if father == x else self._find_ranked(father, rank+1)

    def _compress(self, x, ancestral):
        ''' Faz a compressão dos conjuntos a partir de um elemento.

            Parâmetros
            ----------
            self : disjoint_set<T>
                Conjunto disjunto que armazena as informações dos conjuntos.
            x : T
                Parâmetro de busca para o subconjunto que ele se encontra.
            ancestral : T
                Elemento usado para mudar o ancestral dos elementos para o
                mais importante.
        '''
        if self[x] != x:
            self._compress(self[x], ancestral)
            self[x] = ancestral

    def add(self, x):
        ''' Adiciona um elemento a estrutura conjuntos disjuntos.

        Parâmetro
        ---------
        self : disjoint_set<T>
            Conjunto disjunto que armazena as informações dos conjuntos.
        x : T
            Elemento a ser adionado.
        '''
        self[x] = self.get(x, x)

    def find(self, x):
        ''' Determina qual subconjunto um elemento particular está. Ele pode
            ser usado para determinar se dois elementos estão no mesmo
            subconjunto.

            Parâmetros
            ----------
            self : disjoint_set<T>
                Conjunto disjunto que armazena as informações dos conjuntos.
            x : T
                Parâmetro de busca para o subconjunto que ele se encontra.
            
            Retornos
            --------
            tuple
                Retonar o ancestral do seu subconjunto e seu rank. Se o
                ancestral for igual ao elemento, ele não foi encontrado
                em nenhum subconjunto existe, e foi adiciona a um novo
                conjunto com apenas um elemento, ele próprio.
        '''
        ancestral, rank = self._find_ranked(x)
        self.add(x)
        self._compress(x, ancestral)
        return (ancestral, rank)

    def union(self, x, y):
        ''' Une dois conjuntos em um único subconjunto, a partir dos elementos 
            dos subconjuntos. Estes elementos são usados para definir seus 
            subconjuntos e então fazer a união.
        
        Parâmetros
        ----------
        self : disjoint_set<T>
            Conjunto disjunto que armazena as informações dos conjuntos.
        x : T
            Elemento 1 de um subconjunto qualquer.
        y : T
            Elemento 2 de um subconjunto qualquer.
        
        Retornos
        --------
        bool
            Retorna True se foi possível fazer a união dos dois conjuntos.
        '''
        ancestral_x, rank_1 = self.find(x)
        ancestral_y, rank_2 = self.find(y)

        # Union by rank
        if rank_1 > rank_2:
            self[ancestral_x] = ancestral_y
        else:
            self[ancestral_y] = ancestral_x
        
        return not ancestral_x == ancestral_y

    def makeset(self, x, y):
        ''' Verifica se dois elementos estão no mesmo subconjunto.

        Parâmetros
        ----------
        self : disjoint_set<T>
            Conjunto disjunto que armazena as informações dos conjuntos.
        x : T
            Elemento 1 de um subconjunto qualquer.
        y : T
            Elemento 2 de um subconjunto qualquer.
        
        Retornos
        --------
        bool
            Retorna se o subconjunto de 'x' é o mesmo que o subconjunto de 'y'.
        '''
        anct_x, _ = self.find(x)
        anct_y, _ = self.find(y)

        return not anct_x == anct_y
    '''
        # not ranked
        def _find(self, x):
            father = self.get(x, x)
            return x if x == father else self._find(father)

        def find(self, x):
            # Determina o ultimo ancestral
            anct = self._find(x)
            self[x] = anct
            return self[x]

        def union(self, x, y):
            anct_x = self.find(x)
            anct_y = self.find(y)

            self[anct_x] = anct_y
            return not anct_x == anct_y
    '''

def test_1():
    cj = disjoint_set()

    lim = 1000
    div = 5
    for i in range(lim):
        x = random.randint(0, lim//div)
        y = random.randint(0, lim//div)
        cj.union(x, y)
        #print("% 3d % 3d %s" % (x, y, str(cj.union_find(x, y))))

    to_print = sorted(
        sorted(list(cj.items()), key=lambda x: x[0]), key=lambda x: x[1])
    j = to_print[0][1]
    for i in to_print:
        if i[1] != j:
            print()
            j = i[1]
        print(i, end=" ")

def test_2():
    ds = disjoint_set()
    print(ds.union(0, 1))
    print(ds.union(1, 2))
    print(ds.union(2, 0))

    print(ds)

if __name__ == "__main__":
    pass
