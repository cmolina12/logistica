import pandas as pd
import networkx as nx 
import matplotlib.pyplot as plt
import heapq

# Importar datos

df_puerto = pd.read_excel("Plantilla - Base de problemas.xlsx", sheet_name="P4-Datos")

#def grafo_completo(df_puerto):
    
#    grafo = nx.DiGraph()
    
#    for _, row in df_puerto.iterrows():
        
#        origen = row["Nodo salida"]
#        destino = row["Nodo llegada"]
#        distancia = row["Distancia (km)"] # en km
#        tiempo = row["Tiempo (h)"] # en horas
        
#        grafo.add_edge(origen,destino,distancia=distancia,tiempo=tiempo)
    
#    return grafo

#grafo = grafo_completo(df_puerto)


grafo = nx.from_pandas_edgelist(df_puerto, source="Nodo salida", target="Nodo llegada", edge_attr=["Distancia (km)", "Tiempo (h)"], create_using=nx.DiGraph())

# Problema A

def dijkstra_marcado(grafo, source):
    
    # [(distancia, tiempo, nodo, ruta)]
    2
    heap = [(0,0,source,[source])]
    
    visitados = dict()
    
    orden_marcado = []
    
    while heap:
        
        distancia, tiempo, nodo, ruta = heapq.heappop(heap)
        
        # Principio de optimalidad
        
        clave = nodo
        
        if clave in visitados and (distancia, tiempo) >= visitados[clave]:
            continue
        
        visitados[clave] = (distancia, tiempo)
        
        orden_marcado.append(clave)
        
        for vecino in grafo.neighbors(nodo):
            
            arco = grafo.get_edge_data(nodo, vecino)
            
            distancia_nuevo = distancia + arco["Distancia (km)"]
            
            tiempo_nuevo = tiempo + arco["Tiempo (h)"]
            
            nodo_nuevo = vecino
            
            ruta_nuevo = ruta + [vecino]
            
            heapq.heappush(heap, (distancia_nuevo, tiempo_nuevo, nodo_nuevo, ruta_nuevo))
            
    return orden_marcado

orden_marcado = dijkstra_marcado(grafo, "A")

print("Problema a)")
print(orden_marcado)

print("-------------------------")

# Problema B

def dijkstra_normal(grafo, source, target):
    
    # [(distancia, tiempo, nodo, ruta)]
    
    heap = [(0,0,source,[source])]
    
    visitados = dict()
    
    while heap:
        
        distancia, tiempo, nodo, ruta = heapq.heappop(heap)
        
        # Principio de optimalidad
        
        clave = nodo
        
        if clave in visitados and (distancia, tiempo) >= visitados[clave]:
            continue
        
        visitados[clave] = (distancia, tiempo)
        
        # Principio de llegada
        
        if nodo == target:
            return ruta, distancia
        
        for vecino in grafo.neighbors(nodo):
            
            arco = grafo.get_edge_data(nodo, vecino)
            
            distancia_nuevo = distancia + arco["Distancia (km)"]
            
            tiempo_nuevo = tiempo + arco["Tiempo (h)"]
            
            nodo_nuevo = vecino
            
            ruta_nuevo = ruta + [vecino]
            
            heapq.heappush(heap, (distancia_nuevo, tiempo_nuevo, nodo_nuevo, ruta_nuevo))
            
    return None, None

ruta, distancia = dijkstra_normal(grafo, "A", "V")
print("Problema b)")
print(" -> ".join(ruta))

print("-------------------------")
print("Problema c)")
print(f"Distancia: {distancia} km")