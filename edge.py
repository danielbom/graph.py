class edge(object):
    def __init__(self, source, destiny, destiny_class, weight):
        self.destiny_class = destiny_class
        self.destiny = destiny
        self.source = source
        self.weight = weight
        self.included = True
        self.info = 0

    def __str__(self):
        return str(self.destiny)

    def __repr__(self):
        return str(self.destiny)
