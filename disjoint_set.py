import random


class disjoint_set(dict):
    # ranked
    def _find_ranked(self, x, i):
        father = self.get(x, x)
        return (x, i) if father == x else self._find_ranked(father, i+i)

    def _compress(self, x, ancestral):
        if self[x] != x:
            self._compress(self[x], ancestral)
            self[x] = ancestral

    def add(self, x):
        self[x] = self.get(x, x)

    def find(self, x):
        ancestral, rank = self._find_ranked(x, 0)
        self.add(x)
        self._compress(x, ancestral)
        return (ancestral, rank)

    def union(self, x, y):
        anct_x, rank_1 = self.find(x)
        anct_y, rank_2 = self.find(y)

        # Union by rank
        if rank_1 > rank_2:
            self[anct_x] = anct_y
        else:
            self[anct_y] = anct_x
        return not anct_x == anct_y

    def makeset(self, x, y):
        anct_x, _ = self.find(x)
        anct_y, _ = self.find(y)

        return not anct_x == anct_y
    # not ranked
    '''
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


if __name__ == "__main__":
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
