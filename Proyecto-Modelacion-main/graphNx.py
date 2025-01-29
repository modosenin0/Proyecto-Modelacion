import networkx as nx
import matplotlib.pyplot as plt

class GraphNx:
    def __init__(self, edges_list):
        self.edges_list = edges_list

    def create_graph(self):
        G = nx.Graph()

        for edgePar in range(len(self.edges_list)):
            min_edge_list = self.edges_list[edgePar]
            G.add_edge(min_edge_list[0],min_edge_list[1],weight=min_edge_list[2])

        return G