import networkx as nx
import matplotlib.pyplot as plt
import customtkinter as ctk
import tkinter as tk
from tkinter import PhotoImage


def run_graphs(graph, partida, destino, visa):

    #Camino por costo
    camino_por_costo, costo_por_costo, distancia_por_costo = dikjstra_costo(graph, graph.get_node_by_name(partida), graph.get_node_by_name(destino), visa)
    
    #Camino por distancia
    camino_por_distancia, costo_por_distancia, distancia_por_distancia = dikjstra_distancia(graph, graph.get_node_by_name(partida), graph.get_node_by_name(destino), visa)


    return camino_por_costo, costo_por_costo, distancia_por_costo, camino_por_distancia, costo_por_distancia, distancia_por_distancia

#GRAFICAR EL GRAFO CON CAMINOS
def graficar_grafo_paths(graphNx, camino_por_costo, camino_por_distancia):
    
    pos = nx.shell_layout(graphNx)

    rotated_pos = {node: (y, -x) for node, (x, y) in pos.items()}

    plt.figure(3,figsize=(10,8)) 

    #pintar los nodos
    nx.draw_networkx_nodes(graphNx, rotated_pos, node_size=1100, node_color="lightgreen", edgecolors="grey")


    #pintar arcos
    elist = [(u,v) for (u,v,d) in graphNx.edges(data = True)]
    nx.draw_networkx_edges(graphNx,rotated_pos,edgelist=elist,width=3)

    #pintar los arcos de dijkstra
    edges_dijks_costo= get_dijkstra_edges(camino_por_costo)        
    edges_dijks_distancia= get_dijkstra_edges(camino_por_distancia)        
    nx.draw_networkx_edges(graphNx,rotated_pos,edgelist=edges_dijks_distancia,width=5, edge_color="orange", alpha=0.8)
    nx.draw_networkx_edges(graphNx,rotated_pos,edgelist=edges_dijks_costo,width=5, edge_color="blue", alpha=0.8)

    #LABELS
    nx.draw_networkx_labels(graphNx,rotated_pos,font_size=12,font_color="black", font_weight="bold")


    plt.tight_layout()
    plt.xlim(0,2)
    plt.ylim(0,2)
    plt.axis("equal")
    plt.show()

def get_dijkstra_edges(camino):
    edges_list = []
    for node in range(len(camino)-1):
        edges_list.append((camino[node], camino[node+1]))

    return edges_list



#Graficar grafo general
def graficar_grafo(graphNx):
    
    pos = nx.shell_layout(graphNx)

    rotated_pos = {node: (y, -x) for node, (x, y) in pos.items()}

    plt.figure(3,figsize=(10,8)) 

    #pintar los nodos
    nx.draw_networkx_nodes(graphNx, rotated_pos, node_size=900, node_color="powderblue", edgecolors="black")


    #pintar arcos
    elist = [(u,v) for (u,v,d) in graphNx.edges(data = True)]
    nx.draw_networkx_edges(graphNx,rotated_pos,edgelist=elist,width=3)


    #LABELS
    nx.draw_networkx_labels(graphNx,rotated_pos,font_size=12,font_color="black", font_weight="bold")
    
    plt.tight_layout()
    plt.xlim(0,2)
    plt.ylim(0,2)
    plt.axis("equal")
    plt.show()

def interfaz(graph, graphNx):

    #Variables y funciones auxiliares
    def combobox_callback(choice):
        print(choice)
    
    options = []
    for node in graph.nodos.values():
        options.append(node.name)
    

    camino_por_costo = ""
    costo_por_costo = 0
    distancia_por_costo = 0

    camino_por_distancia = ""
    costo_por_distancia = 0
    distancia_por_distancia = 0

    error = ""
    

    #setup interfaz
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")
    root = ctk.CTk()
    root.geometry("600x750")
    root.title("MetroTravel")

    bg = PhotoImage(file = "bg.png")
    bg_label = ctk.CTkLabel(root, image=bg)
    bg_label.place(x=0, y=0)

    #Frames y labels
    frame = ctk.CTkFrame(master=root)
    frame.pack(pady=20, padx=20, fill="both", expand=True)
    titulo = ctk.CTkLabel(master=frame, text="MetroTravel", font=("Arial Black", 20))
    titulo.pack(pady=10)
    grafo_info = ctk.CTkFrame(master=frame)
    grafo_info.pack(padx=10, pady=10, fill="both")


    visa = ctk.CTkLabel(master=grafo_info,  text="Elija si posee visa o no:", font=("Arial Black", 14))
    visa.pack(pady=10, padx=10)
    
    #opciones para generar el camino
    visa = tk.StringVar()
    visa.set("Visa")
    combobox = ctk.CTkComboBox(grafo_info, values=["Visa", "No Visa"], variable=visa, command=combobox_callback, state="readonly")
    combobox.pack(pady=10, padx=10)

    label1 = ctk.CTkLabel(master=grafo_info,  text="Elija el aeropuerto de partida:", font=("Arial Black", 14))
    label1.pack(pady=10, padx=10)

    #opciones para generar el camino
    selected_option1 = tk.StringVar()
    selected_option1.set(options[0])
    combobox = ctk.CTkComboBox(grafo_info, values=options, variable=selected_option1, command=combobox_callback, state="readonly")
    combobox.pack(pady=10, padx=10)

    label2 = ctk.CTkLabel(master=grafo_info,  text="Elija el aeropuerto de destino:", font=("Arial Black", 14))
    label2.pack(pady=10, padx=10)

    #opciones para generar el camino
    selected_option2 = tk.StringVar()
    selected_option2.set(options[1])
    combobox = ctk.CTkComboBox(grafo_info, values=options, variable=selected_option2, command=combobox_callback, state="readonly")
    combobox.pack(pady=10, padx=10)

    labelError = ctk.CTkLabel(master=grafo_info,  text=error, font=("Arial Black", 14), text_color="red")
    labelError.pack(pady=1, padx=1)

    #buton para calcular dijkstra por costo
    ir_button=ctk.CTkButton(grafo_info, text="CALCULAR CAMINO", command=lambda: calcular_todo(selected_option1.get(), selected_option2.get(), visa.get(), resultados_camino_costo, resultados_costo_por_costo, resultados_distancia_por_costo, resultados_camino_distancia, resultados_costo_por_distancia, resultados_distancia_por_distancia, labelError))
    ir_button.pack(padx=150, pady=30)

    def calcular_todo(partida, destino, visa, resultados_camino_costo, resultados_costo_por_costo, resultados_distancia_por_costo, resultados_camino_distancia, resultados_costo_por_distancia, resultados_distancia_por_distancia, labelError):
        
        labelError.configure(text="")

        resultados_camino_costo.configure(text="")
        resultados_costo_por_costo.configure(text="")
        resultados_distancia_por_costo.configure(text="")

        resultados_camino_distancia.configure(text="")
        resultados_costo_por_distancia.configure(text="")
        resultados_distancia_por_distancia.configure(text="")
        
        if visa == "Visa":
            has_visa = True
        else:
            has_visa = False
        if partida == "" and destino == "":
            graficar_grafo(graphNx)  
        elif partida == destino:
            labelError.configure(text=str("Por favor elige aeropuertos diferentes."))
        elif not has_visa and graph.get_node_by_name(partida).visa_required:
            labelError.configure(text=str("Se requiere visa para estar en el aeropuerto de " + partida))
        elif not has_visa and graph.get_node_by_name(destino).visa_required:
            labelError.configure(text=str("Se requiere visa para estar en el aeropuerto de " + destino))
        else:
            camino_por_costo, costo_por_costo, distancia_por_costo, camino_por_distancia, costo_por_distancia, distancia_por_distancia = run_graphs(graph, partida, destino, has_visa)

            if camino_por_costo == False or camino_por_distancia == False:
                labelError.configure(text=str("No existe camino entre esos aeropuertos!"))
                graficar_grafo(graphNx)
                return

            camino_costo = ""
            if(len(camino_por_costo) > 0):
                camino_costo = camino_por_costo[0]
                for node in range(len(camino_por_costo)-1):
                    camino_costo += " => "
                    camino_costo += camino_por_costo[node+1]

            resultados_camino_costo.configure(text=str(camino_costo))
            resultados_costo_por_costo.configure(text="Costo: $ "+str(costo_por_costo))
            resultados_distancia_por_costo.configure(text="Distancia:  "+str(distancia_por_costo))

            if (int(distancia_por_costo) == int(distancia_por_distancia)):
                camino_por_distancia = camino_por_costo
                costo_por_distancia = costo_por_costo
                distancia_por_distancia = distancia_por_costo

            camino_distancia = ""
            if(len(camino_por_distancia) > 0):
                camino_distancia = camino_por_distancia[0]
                for node in range(len(camino_por_distancia)-1):
                    camino_distancia += " => "
                    camino_distancia += camino_por_distancia[node+1]
            
            resultados_camino_distancia.configure(text=str(camino_distancia))
            resultados_costo_por_distancia.configure(text="Costo: $ "+str(costo_por_distancia))
            resultados_distancia_por_distancia.configure(text="Distancia:  "+str(distancia_por_distancia))

        
            
            graficar_grafo_paths(graphNx, list(camino_por_costo),list(camino_por_distancia))


    #Resultados del recorrido
    resultados_info = ctk.CTkFrame(master=frame)
    resultados_info.pack(padx=10, pady=10, fill="both")
    
    resultados_info.columnconfigure(0, weight=1)
    resultados_info.columnconfigure(1, weight=1)

    camino_costo = ctk.CTkLabel(master=resultados_info, text="Camino por costo", font=("Arial Black", 14))
    resultados_camino_costo = ctk.CTkLabel(master=resultados_info, width=80, text=str(camino_por_costo))
    resultados_costo_por_costo = ctk.CTkLabel(master=resultados_info, width=80, text="Costo: $ "+str(costo_por_costo))
    resultados_distancia_por_costo = ctk.CTkLabel(master=resultados_info,text="Distancia:  "+str(distancia_por_costo))


    camino_distancia = ctk.CTkLabel(master=resultados_info, text="Camino por distancia", font=("Arial Black", 14))
    resultados_camino_distancia = ctk.CTkLabel(master=resultados_info, width=80, text=str(camino_por_distancia))
    resultados_costo_por_distancia = ctk.CTkLabel(master=resultados_info, width=80, text="Costo: $ "+str(costo_por_distancia))
    resultados_distancia_por_distancia = ctk.CTkLabel(master=resultados_info,text="Distancia:  "+str(distancia_por_distancia))


    camino_costo.grid(row=0,column=0, padx=10, pady=10, sticky="we")
    resultados_camino_costo.grid(row=1,column=0, padx=10, pady=10, sticky="we")
    resultados_costo_por_costo.grid(row=2,column=0, padx=10, pady=10, sticky="we" )
    resultados_distancia_por_costo.grid(row=3,column=0, padx=10, pady=10, sticky="we" )

    camino_distancia.grid(row=0,column=1, padx=10, pady=10, sticky="we")
    resultados_camino_distancia.grid(row=1,column=1, padx=10, pady=10, sticky="we")
    resultados_costo_por_distancia.grid(row=2,column=1, padx=10, pady=10, sticky="we" )
    resultados_distancia_por_distancia.grid(row=3,column=1, padx=10, pady=10, sticky="we" )
    
    root.mainloop()

    


def dikjstra_costo(grafo, partida, destino, visa):
    camino = []
    tabla = {}

    for node in grafo.get_nodes():
        tabla[node.id] = ["-", 9999, False]
    tabla[partida.id][1] = 0

    actual = partida

    while tabla[destino.id][2] != True:
        tabla[actual.id][2] = True

        for neighbor, cost in actual.neighbors.items():

            if(tabla[neighbor][1] > tabla[actual.id][1]+cost and (visa or (not visa and grafo.get_node(neighbor).visa_required == False))):
                tabla[neighbor][1]=tabla[actual.id][1]+cost
                tabla[neighbor][0]=actual.id
        
        temp_tabla = {}
        for key, value in tabla.items():
            if value[2] == False and value[1] != 9999:
                temp_tabla[key] = value
        
        if not temp_tabla:
            break
        
        actual = grafo.get_node(min(temp_tabla.items(), key=lambda x: x[1][1])[0])

    if(tabla[destino.id][1] == 9999):
        return False, False, False
            
    print(tabla)

    costo = tabla[destino.id][1]
    temp = tabla[destino.id]
    
    camino.insert(0,destino.id)
    while temp[0] != "-":
        camino.insert(0, temp[0])
        temp = tabla[temp[0]]
        
    distancia = len(camino)-1

    return camino, costo, distancia

def dikjstra_distancia(grafo, partida, destino, visa):
    camino = []
    tabla = {}

    for node in grafo.get_nodes():
        tabla[node.id] = ["-", 9999, False]
    tabla[partida.id][1] = 0


    actual = partida

    while tabla[destino.id][2] != True:
        tabla[actual.id][2] = True

        for neighbor, cost in actual.neighbors.items():
            
            if(tabla[neighbor][1] > tabla[actual.id][1]+1 and (visa or (not visa and grafo.get_node(neighbor).visa_required == False))):
                tabla[neighbor][1]=tabla[actual.id][1]+1
                tabla[neighbor][0]=actual.id
        
        temp_tabla = {}
        for key, value in tabla.items():
            if value[2] == False and value[1] != 9999:
                temp_tabla[key] = value

        if not temp_tabla:
            break

        actual = grafo.get_node(min(temp_tabla.items(), key=lambda x: x[1][1])[0])

        
        
    if(tabla[destino.id][1] == 9999):
        return False, False, False


    distancia = tabla[destino.id][1]
    temp = tabla[destino.id]
    
    camino.insert(0,destino.id)
    actual = destino.id
    while temp[0] != "-":
        camino.insert(0, temp[0])
        temp = tabla[temp[0]]

    costo = calcular_costo(grafo, camino)

    return camino, costo, distancia

def calcular_costo(grafo, camino):
    costo = 0
    for node in range(len(camino)-1):
        costo += grafo.get_node(camino[node]).neighbors[camino[node+1]]

    return costo