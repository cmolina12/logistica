
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import heapq

# Importar datos

df_rutas = pd.read_excel("Plantilla.xlsx", sheet_name="UltraCargo_Rutas_Transporte")
df_centros = pd.read_excel("Plantilla.xlsx", sheet_name="UltraCargo_Centros_Logísticos")

# 1.1 Diseñar grafo completo

def grafo_completo(df_rutas):
    
    grafo = nx.DiGraph()
    
    for _, row in df_rutas.iterrows():
        origen = row["Origen"]
        destino	= row["Destino"]
        distancia = row["Distancia"]
        frontera = row["Frontera"]
        alta_demanda = row["Alta_Demanda"]	      
        
        # Costo
        
        costo = 15 * distancia + 200 * frontera + (150*alta_demanda)
        
        grafo.add_edge(origen, destino, costo=costo)
        
    return grafo

grafo_completo = grafo_completo(df_rutas)

# Dibujar grafo

plt.figure(figsize=(12, 8), facecolor="white")
pos = nx.spring_layout(grafo_completo)
nx.draw_networkx(
    grafo_completo,
    pos,
    with_labels=True,
    node_color="lightblue",
    edge_color="gray",
    node_size=700,
    font_size=10,
)

# Mostrar los costos en las aristas
edge_labels = nx.get_edge_attributes(grafo_completo, "costo")
nx.draw_networkx_edge_labels(grafo_completo, pos, edge_labels=edge_labels, font_color="green")

plt.title("Grafo Dirigido de Rutas de Transporte")
plt.axis("off")
plt.show()

# 1.2 Un cliente ha solicitado el transporte de 20 toneladas de mercancía desde la ciudad de San Diego (EE.UU.) hasta Denver (EE. UU). Encuentre la ruta de menor costo. Reporte el costo total del transporte, la distancia total recorrida y el tiempo total que tomaría realizar la entrega. Para esto tenga en cuenta estas consideraciones:  
        
carga = 20

def grafo_reducido(df_rutas):
    
    grafo = nx.DiGraph()
    
    for _, row in df_rutas.iterrows():
        
        origen = row["Origen"]
        destino	= row["Destino"]
        distancia = row["Distancia"]
        velocidad = row["Velocidad"]
        frontera = row["Frontera"]
        alta_demanda = row["Alta_Demanda"]	 
        capacidad = row["Capacidad"]
        horario = row["Horario"]
        terrestre = row["Terrestre"]
        aereo = row["Aereo"]
        vuelos = row["Vuelos"]
        tiempo = distancia/velocidad
        
        # No se pueden usar rutas aereas despues de las 11 horas
        
        if (aereo == 1) and (horario > 11):
            continue
        
        # Penalizacion
        
        if carga > capacidad:
            penalizacion = 0.15
        else:
            penalizacion = 0
        
        # Costo
        costo = (15 * distancia + 200 * frontera + (150*alta_demanda)     ) *(1+penalizacion)
        
        grafo.add_edge(origen, destino, costo=costo, distancia=distancia, tiempo=tiempo)
     
    return grafo
     
grafo_reducido = grafo_reducido(df_rutas)   
ruta = nx.shortest_path(grafo_reducido, source="San Diego", target="Denver", weight="costo")

costo = sum(grafo_reducido[ruta[i]][ruta[i+1]]["costo"] for i in range(len(ruta)-1))
distancia = sum(grafo_reducido[ruta[i]][ruta[i+1]]["distancia"] for i in range(len(ruta)-1))
tiempo = sum(grafo_reducido[ruta[i]][ruta[i+1]]["tiempo"] for i in range(len(ruta)-1))

print("Punto 1.2)")
print(" -> ".join(ruta))
print(f"Costo total: ${costo}")
print(f"Distancia: {distancia} km")
print(f"Tiempo total: {round(tiempo, 2)} horas")
print("")

tiempo_minimo = 70

ciudades_a_estados = dict()

for _, row in df_centros.iterrows():
    ciudad = row["Ciudad"]
    estado = row["Estado"]
    ciudades_a_estados[ciudad] = estado

#ciudades_a_estados = {row["Ciudad"]: row["Estado"] for _, row in df_centros.iterrows()}

def grafo_aereo(df_r):
    
    grafo = nx.DiGraph()
    
    for _, row in df_rutas.iterrows():
        
        origen = row["Origen"]
        destino	= row["Destino"]
        distancia = row["Distancia"]
        velocidad = row["Velocidad"]
        frontera = row["Frontera"]
        alta_demanda = row["Alta_Demanda"]	 
        capacidad = row["Capacidad"]
        horario = row["Horario"]
        terrestre = row["Terrestre"]
        aereo = row["Aereo"]
        vuelos = row["Vuelos"]
        tiempo = distancia/velocidad
        
        # Para el estado de Texas solo puedes emplear rutas aereas
        
        if ciudades_a_estados[origen] == "Texas" or ciudades_a_estados[destino] == "Texas":
            if aereo == 0:
                continue
        
        # Costo aereo o terrestre
        
        costo = 0
        
        if aereo == 1:
            costo = 500+3*distancia+50*vuelos
        elif terrestre == 1:
            costo = (15*distancia)+(200*frontera)+(150*alta_demanda)
        
        grafo.add_edge(origen, destino, costo=costo, distancia=distancia, tiempo=tiempo)
        
    return grafo

grafo_aereo = grafo_aereo(df_rutas)
        
def dijkstra(grafo, source, target, tiempo_minimo):
    
    # heap = [(costo, tiempo, nodo, ruta)]
    
    heap = [(0,0,source, [source])]
    
    visitados = dict()
    
    while heap:
        
        costo_acumulado, tiempo_acumulado, nodo, ruta = heapq.heappop(heap)
        
        # Principio de optimalidad
        
        clave = (nodo, tiempo_acumulado)
        
        if clave in visitados and costo_acumulado >= visitados[clave]:
            continue
        
        visitados[clave] = costo_acumulado
        
        # Principio de llegada
        
        if nodo == target:
            if tiempo_acumulado < tiempo_minimo:
                continue
            
            distancia = sum(grafo[ruta[i]][ruta[i+1]]["distancia"] for i in range(len(ruta)-1))
            
            return ruta, costo_acumulado, distancia, tiempo_acumulado
        
        for vecino in grafo.neighbors(nodo):
            
            if vecino in ruta:
                continue
            
            arco = grafo.get_edge_data(nodo, vecino)
            
            costo_nuevo = costo_acumulado + arco["costo"]
            
            tiempo_nuevo = tiempo_acumulado + arco["tiempo"]
            
            nodo_nuevo = vecino
            
            ruta_nueva = ruta + [vecino]
            
            heapq.heappush(heap, (costo_nuevo, tiempo_nuevo, nodo_nuevo, ruta_nueva))
            
    return None, None, None, None

ruta, costo, distancia, tiempo = dijkstra(grafo_aereo, "Guadalajara", "Miami", 70)

print("Punto 1.3)")
print(" -> ".join(ruta))
print(f"Costo total: ${costo}")
print(f"Distancia total: {distancia} km")
print(f"Tiempo total: {tiempo} horas")
        
        