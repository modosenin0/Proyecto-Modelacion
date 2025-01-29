
import json
from graph import Graph
from node import Node
from utils import *
from graphNx import GraphNx

def app():
    with open("data.txt") as json_file:
        data = json.load(json_file)

    grafo = Graph()

    try:   
        for key, info in data["destinos"].items():
            nodo = Node(key, info[0],info[1])
            grafo.add_node(nodo)
    except Exception as e:
        print("Error cargando los nodos.")
        print(e)

    try:
        edges_list = []
        for edge_info in data["conexiones"]:
            grafo.add_edge(edge_info[0],edge_info[1], edge_info[2])
            edges_list.append(edge_info)
    except Exception as e:
        print("Error cargando las aristas.")
        print(e)

    grafoNx = GraphNx(edges_list).create_graph()

    print("GRAFO:")
    for node in grafo.get_nodes():
        print(f"{node.id}: {node.neighbors}")

    interfaz(grafo, grafoNx)


app()