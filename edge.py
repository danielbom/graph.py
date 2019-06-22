class edge(object):
    def __init__(self, source, destiny, destiny_class, weight):
        self.destiny_class = destiny_class
        self.destiny = destiny
        self.source = source
        self.weight = weight
        self.included = True
        self.info = 0

    def __str__(self):
        return f"({self.source}:{self.destiny}:{self.weight})"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return str(self) == str(other)