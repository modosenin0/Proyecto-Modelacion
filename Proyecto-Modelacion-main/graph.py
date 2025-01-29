from node import Node

class Graph():
    def __init__(self):
        self.nodos = {}
    
    def add_node(self, node):
        if isinstance(node, Node) and node.id not in self.nodos:
            self.nodos[node.id] = node
            return True
        else:
            return False

    def add_edge(self, nodo1, nodo2, cost):
        if nodo1 in self.nodos and nodo2 in self.nodos:
            self.nodos[nodo1].add_neighbor(nodo2, cost)
            self.nodos[nodo2].add_neighbor(nodo1, cost)
            return True
        else:
            return False
        
    def get_node(self, id):
        try:
            return self.nodos[id]
        except:
            return False
        
    def get_nodes(self):
        return self.nodos.values()
    
    def get_node_by_name(self, name):
        try:
            for node in self.nodos.values():
                if node.name == name:
                    return node
        except:
            return False
        
    