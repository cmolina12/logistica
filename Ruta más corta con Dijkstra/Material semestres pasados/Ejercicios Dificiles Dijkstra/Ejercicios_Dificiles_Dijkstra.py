import pandas as pd
import networkx as nx
import heapq

# Ejercicio 1

df_ejercicio1 = pd.read_excel("Ejercicios_Dijkstra_Datos.xlsx", sheet_name="Ejercicio 1")

def grafo_ejercicio1(df_r):
    
    grafo = nx.DiGraph()
    
    inestables = ["B","F","J"]
    
    for _, row in df_r.iterrows():
        
        origen = row["Origen"]
        destino = row["Destino"]
        peso = row["Peso"]
        
        if origen in inestables or destino in inestables:
            continue
        
        grafo.add_edge(origen, destino, peso=peso)
    
    return grafo
        
grafo = grafo_ejercicio1(df_ejercicio1)   
ruta = nx.shortest_path(grafo, source="A", target="O", weight="peso")

