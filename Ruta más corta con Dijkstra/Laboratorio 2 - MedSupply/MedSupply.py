import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Importar datos

df_r = pd.read_excel("Plantilla - Laboratorio 2.xlsx", sheet_name = "Punto1_Rutas")

df_c = pd.read_excel("Plantilla - Laboratorio 2.xlsx", sheet_name = "Punto1_Ciudades")


# 1.1. Diseñar  un  grafo  dirigido  que  represente  la  red  completa  de  todas  rutas  disponibles,  donde  las  ciudades  serán  los  nodos  y  las  rutas  los  arcos.  Asegúrese  de  que  en  cada  arco  se  calcule  y  muestre explícitamente  el  costo  logístico  total  del  trayecto.  Insertar  la  imagen  del  grafo  generado  en  el  inciso correspondiente. 

def grafo_completo(df_r):
    
    G = nx.DiGraph()
    
    for _, row in df_r.iterrows():
        
        origen = row["Origen"]
        destino = row["Destino"]
        distancia = row["Distancia_km"]
        tipo_transporte = row["Transporte"]
        
        constante = (1 if tipo_transporte =="Camion" else 1.5 if tipo_transporte=="Barco" else 2)
        
        costo = 10 * distancia + 100 * constante
        
        G.add_edge(origen, destino, costo=costo)
        
    return G

G = grafo_completo(df_r)

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

# 1.2 El Centro de Distribución de Bogotá debe enviar urgentemente cinco cajas de vacunas al Hospital Regional de Quito, debido a un brote epidémico en dicha ciudad. Por requerimientos sanitarios, el envío debe pasar obligatoriamente por la estación de Medellín para validación de cadena de frío y documentación.

# cinco cajas de 20 kg cada una

carga = 20 * 5

# 1. Las rutas no pueden ser utilizadas si el clima es “Tormenta”, sin importar el tipo de transporte.
# 2. Rutas cuya ventana horaria sea menor a 8 horas disponibles se consideran no operativas y deben
# ser descartadas.
# 3. El transporte de vacunas debe realizarse exclusivamente en rutas con refrigeración disponible.
# 4. El trayecto completo no puede incluir más de una estación con autonomía baja, ya que estas no
# garantizan condiciones de transferencia seguras
# 5. Si el envío excede la capacidad máxima de la ruta, se aplica una penalización del 15% adicional al
# costo de esa ruta.

dict_autonomia = {}

for _, row in df_c.iterrows():
    
    ciudad = row["Nombre"]
    autonomia = row["Autonomia"]
    dict_autonomia[ciudad] = autonomia
    

def grafo_reducido(df_r):
    
    grafo = nx.DiGraph()
    
    for _, row in df_r.iterrows():
        
        origen = row["Origen"]
        destino = row["Destino"]
        tipo_transporte = row["Transporte"]
        clima = row["Clima"]
        ventana_horaria = row["Ventana_Horaria"]
        capacidad = row["Capacidad_Maxima_kg"]
        distancia = row["Distancia_km"]
        refrigeracion = row["Refrigeracion"]
        tiempo_estimado = row["Tiempo_estimado_h"]
        
        # Restriccion 1 - No se puede "Tormenta"
        
        if clima == "Tormenta":
            continue
        
        # Restriccion 2 - Ventanas horarios menor a 8 horas
        
        inicio, fin = map(int, ventana_horaria.split("-"))
        
        if (fin-inicio) < 8:
            continue
        
        # Restriccion 3 - Refrigeracion
        
        if refrigeracion == "No":
            continue
        
        # Penalizacion
        
        if carga > capacidad:
            penalizacion = 0.15
        else:
            penalizacion = 0
        
        # Costo
        
        constante = (1 if tipo_transporte =="Camión" else 1.5 if tipo_transporte=="Barco" else 2)
        
        costo = (10 * distancia + 100 * constante) * (1+penalizacion)

        
        # Añadir arcos
        
        grafo.add_edge(origen, 
                   destino, 
                   costo=costo,
                   distancia=distancia,
                   tiempo=tiempo_estimado,
                   transporte=tipo_transporte,
                   clima=clima,
                   ventana=ventana_horaria,
                   capacidad=capacidad,
                   refrigeracion=refrigeracion)
        
        for node in G.nodes():
            
            G.nodes[node]["autonomia"]= dict_autonomia.get(node)
            
    return grafo

import heapq

def dijkstra(grafo, source, target, ciudad_obligatoria):
    
    # (costo, tiempo, nodo, flag_medellin, contador_baja, ruta)
    
    flag_medellin = True if source == ciudad_obligatoria else False
    contador_baja = 1 if dict_autonomia.get(source) == "Baja" else 0
    
    
    heap = [(0,0,source, flag_medellin, contador_baja, [source])]
    
    visitados = dict()
    
    while heap:
        
        costo_acumulado, tiempo_acumulado, nodo, flag_medellin, contador_baja, ruta = heapq.heappop(heap)
        
        # Principio de llegada
        
        if nodo == target and flag_medellin == True and contador_baja <= 1:
            
            distancia = sum(grafo[ruta[i]][ruta[i+1]]['distancia'] for i in range(len(ruta)-1))
            
            return ruta, costo_acumulado, tiempo_acumulado, distancia
        
        # Principio de optimalidad

        clave = (nodo, flag_medellin, contador_baja)
        
        if clave in visitados:
            costo_prev, tiempo_prev = visitados[clave]
            if (costo_acumulado, tiempo_acumulado) >= (costo_prev, tiempo_prev):
                continue

        visitados[clave] = (costo_acumulado, tiempo_acumulado)
        
        # Iterar sobre los vecinos
        
        for vecino in grafo.neighbors(nodo):
            
            # Evitar ciclos
            
            if vecino in ruta:
                continue
            
            arco = grafo.get_edge_data(nodo, vecino)
            
            
            costo_nuevo = costo_acumulado + arco["costo"]
            
            tiempo_nuevo = tiempo_acumulado + arco["tiempo"]
            
            nodo_nuevo = vecino
            
            flag_medellin_nuevo = flag_medellin or (vecino==ciudad_obligatoria)
            
            contador_baja_nuevo = contador_baja + (1 if dict_autonomia.get(vecino) == "Baja" else 0)
            
            if contador_baja_nuevo > 1:
                continue
            
            heapq.heappush(heap, (costo_nuevo, tiempo_nuevo, nodo_nuevo, flag_medellin_nuevo, contador_baja_nuevo, ruta + [nodo_nuevo]))
        
    return None, float("inf"), float("inf"), float("inf")
    

grafo = grafo_reducido(df_r)
print(list(grafo.nodes()))
    
ruta, costo, tiempo, distancia = dijkstra(grafo, "Bogotá", "Quito", "Medellín")

print(ruta)
print(costo)
print(tiempo)
print(distancia)
            
    
            
        

  
    
    
  