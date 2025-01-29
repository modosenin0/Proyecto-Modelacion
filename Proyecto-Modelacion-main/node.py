class Node():
    def __init__(self, id, name, visa):
        self.id = id
        self.name = name
        self.visa_required = visa
        self.neighbors = {}
    
    def add_neighbor(self, id, cost):
        if id not in self.neighbors:
            self.neighbors[id] = cost
    
    def is_visa_required(self):
        return self.visa_required
    
