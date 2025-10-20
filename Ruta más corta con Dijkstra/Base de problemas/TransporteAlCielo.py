
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import heapq

df_aeropuertos = pd.read_excel("Plantilla - Base de problemas.xlsx", sheet_name="P3-Datos_nombres")
df_vuelos = pd.read_excel("Plantilla - Base de problemas.xlsx", sheet_name="P3-Vuelos")

#print(df_aeropuertos.head())
#print(df_vuelos.head())

# a. Construya un grafo dirigido que modele las rutas de transporte entre las ciudades, asegurándose 
# de que los nodos representen las ciudades y los arcos incluyan tanto el costo del envío como la 
# distancia de cada trayecto.  Este grafo deberá programarse y será evaluado en el código enviado.

def grafo_completo(df_vuelos):
    
    grafo = nx.DiGraph()
    
    for _, row in df_vuelos.iterrows():
        
        origen = row["origen"]
        destino = row["destino"]
        distancia = row["distancia(km)"]
        precio = row["precio($)"]
        
        grafo.add_edge(origen,destino,costo=precio,distancia=distancia)
        
    return grafo


G = grafo_completo(df_vuelos)

plt.figure(figsize=(12, 8), facecolor="white")
pos = nx.spring_layout(G)
nx.draw_networkx(
    G,
    pos,
    with_labels=True,
    node_color="lightblue",
    edge_color="gray",
    node_size=700,
    font_size=10,
)

# Mostrar los costos en las aristas
edge_labels = nx.get_edge_attributes(G, "costo")
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color="green")

plt.title("Grafo Dirigido de Rutas de Transporte")
plt.axis("off")
plt.show()

# Utilizando el Algoritmo de Dijkstra, determine la ruta con el menor costo de transporte entre la 
# ciudad de Atlanta, Georgia, y la ciudad de Newark, Nueva Jersey. Indique el camino encontrado 
# junto con el costo total y la distancia recorrida.

def dijkstra(grafo, source, target):
    
    # heap =[(costo, route, nodo, ruta)]
    
    ruta = [source]
    
    heap = [(0,tuple(ruta),source,ruta)]
    
    visitados = dict()

    
    while heap:
        
        costo_acumulado, ruta_tupla, nodo, ruta = heapq.heappop(heap)
        
        # Principio de optimalidad
        
        clave = nodo
        
        if clave in visitados and costo_acumulado < visitados[clave]:
            continue
        visitados[clave] = costo_acumulado
        
        
        # Principio de llegada
        
        if nodo == target:
            distancia = sum(grafo[ruta[i]][ruta[i+1]]["distancia"] for i in range(len(ruta)-1))
            
            return costo_acumulado, distancia, ruta
        
        for vecino in grafo.neighbors(nodo):
            
            arco = grafo.get_edge_data(nodo, vecino)
            
            costo_nuevo = costo_acumulado+arco["costo"]
            
            ruta_nuevo = ruta + [vecino]
            
            ruta_tupla_nuevo = tuple(ruta_nuevo)
            
            nodo_nuevo = vecino
            
            heapq.heappush(heap, (costo_nuevo, ruta_tupla_nuevo, nodo_nuevo, ruta_nuevo))
        
    return None, None, None, None

costo, distancia, ruta = dijkstra(G, "ATL", "EWR")

dict_aeropuertos=dict()

for _, row in df_aeropuertos.iterrows():
    codigo = row["Código"]
    aeropuerto = row["Ciudad"]
    
    dict_aeropuertos[codigo]=aeropuerto
    
ruta_nombres = [dict_aeropuertos.get(code) for code in ruta]
    

print("Problema b)")
print(" -> ".join(ruta_nombres))
print(f"Costo de la ruta: ${costo}")
print(f"Distancia: {distancia} km")


print("-------------------------")

# Determine  la  ruta  con  la  menor  cantidad  de  escalas  entre  la  ciudad  de  Atlanta,  Georgia,  y  la 
# ciudad  de  Newark,  Nueva  Jersey.    Especifique  la  ruta  obtenida,  el  costo  total  y  la  distancia 
# recorrida. Se pueden hacer escalas. 

def dijkstra_escalas(grafo, source, target):
    
    heap = [(0, source, [source])]
    
    visitados = dict()
    
    while heap:
        
        escala, nodo, ruta = heapq.heappop(heap)
        
        # Principio de llegada
        
        if nodo == target:
            
            distancia = sum(grafo[ruta[i]][ruta[i+1]]["distancia"] for i in range(len(ruta)-1))
            
            costo = sum(grafo[ruta[i]][ruta[i+1]]["costo"] for i in range(len(ruta)-1))
            
            return ruta, costo, distancia
        
        # Prinicipio de optimalidad
        
        clave = nodo
        
        if clave in visitados and escala >= visitados[clave]:
            continue
        
        visitados[clave] = escala
        
        for vecino in grafo.neighbors(nodo):
            
            if vecino in ruta:
                continue
            
            escala_nueva = escala + 1
            
            nodo_nuevo = vecino
            
            ruta_nueva = ruta + [vecino]
            
            heapq.heappush(heap, (escala_nueva, nodo_nuevo, ruta_nueva))
            
    return None, None, None

ruta, costo, distancia = dijkstra_escalas(G, "ATL", "EWR")

ruta_nombres = [dict_aeropuertos.get(code) for code in ruta]

print("Problema c)")
print(" -> ".join(ruta_nombres))
print(f"Costo de la ruta: ${costo}")
print(f"Distancia: {distancia} km")

print("-------------------------")

# d. Un cliente importante ha solicitado un envío urgente desde Tampa, Florida hasta 
# Cleveland,Ohio.  Sin  embargo,  tenga  en  cuenta  que  en  las  ciudades  de Detroit,  Michigan  y  Duluth, 
# Minnesota se  aplica  un costo  adicional  de  $130 por  servicio  express  en  cada  ciudad.  Con  esta 
# información, determine la ruta más económica.



def grafo_penalizacion (df_r):
    
    grafo = nx.DiGraph()
    
    penalizadas = ["DTW", "DUL"]
    
    for _, row in df_r.iterrows():
        
        origen = row["origen"]
        destino = row["destino"]
        distancia = row["distancia(km)"]
        costo = float(row["precio($)"])
        
        if destino in penalizadas:
            costo += 130
            
        grafo.add_edge(origen, destino, costo=costo,distancia=distancia)
    
    return grafo
        
grafo_penalizado = grafo_penalizacion(df_vuelos)

def dijkstra_penalizacion(grafo, source, target):
    
    heap = [(0, source, [source])]
    
    visitados = dict()
    
    while heap:
        
        costo, nodo, ruta = heapq.heappop(heap)
        
        # Principio de llegada
        
        if nodo == target:
            
            distancia = sum(grafo[ruta[i]][ruta[i+1]]["distancia"] for i in range(len(ruta)-1))
            escalas = len(ruta) - 1
            
            return ruta, escalas, costo, distancia
        
        # Prinicipio de optimalidad
        
        clave = nodo
        
        if clave in visitados and costo > visitados[clave]:
            continue
        
        visitados[clave] = costo
        
        for vecino in grafo.neighbors(nodo):
            
            if vecino in ruta:
                continue
            
            arco = grafo.get_edge_data(nodo, vecino)

            costo_nuevo = costo + arco["costo"]
            
            nodo_nuevo = vecino
            
            ruta_nueva = ruta + [vecino]
            
            heapq.heappush(heap, (costo_nuevo, nodo_nuevo, ruta_nueva))
            
    return None, None, None, None

grafo_p = grafo_penalizacion(df_vuelos)

ruta, escalas, costo, distancia = dijkstra_penalizacion(grafo_p, "TPA", "CLE")

ruta_nombres = [dict_aeropuertos.get(code) for code in ruta]

print("Problema d)")
print(" -> ".join(ruta_nombres))
print(f"Numero de escalas: {escalas}")
print(f"Costo de la ruta: ${costo}")
print(f"Distancia: {distancia} km")
            
        
        
        