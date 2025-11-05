import networkx as nx
import pandas as pd
import heapq
import matplotlib.pyplot as plt

df_1 = pd.read_excel("c.molinap.xlsx", sheet_name="Datos_punto1")

# 1.1 grafo completo grafica


def grafo_completo(df_1):

    grafo = nx.DiGraph()

    for _, row in df_1.iterrows():

        origen = row["origen"]
        destino = row["destino"]
        tiempo = row["tiempo_horas"]  # en horas
        velocidad = row["velocidad_kmh"]  # en km/h
        costo = row["costo_usd"]
        capacidad = row["capacidad_max_ton"]
        tipo_ruta = row["tipo_ruta"]
        distancia = velocidad * tiempo

        grafo.add_edge(
            origen,
            destino,
            distancia=distancia,
            tipo_ruta=tipo_ruta,
            costo=costo,
            tiempo=tiempo,
        )

    return grafo


grafo_completo = grafo_completo(df_1)

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
edge_labels = nx.get_edge_attributes(grafo_completo, "distancia")
nx.draw_networkx_edge_labels(
    grafo_completo, pos, edge_labels=edge_labels, font_color="green"
)

plt.title("Grafo Dirigido de Rutas de Transporte")
plt.axis("off")
plt.show()

# 1.2 20 toneladas de bogotá a quito

# 1. no se puede transitar por un trayecto donde la capcaida sea menor a la carga del camio
# 2. Si el trayecto es un peaje se aplica un recargo adicional de 20%. si es un puente, el recargo es del 10%.

carga = 20  # toneladas


def grafo_reducido(df_1):

    grafo = nx.DiGraph()

    for _, row in df_1.iterrows():

        origen = row["origen"]
        destino = row["destino"]
        tiempo = row["tiempo_horas"]  # en horas
        velocidad = row["velocidad_kmh"]  # en km/h
        costo = row["costo_usd"]
        capacidad = row["capacidad_max_ton"]
        tipo_ruta = row["tipo_ruta"]
        distancia = velocidad * tiempo

        # No se puede transitar por un trayecto donde capacidad sea menor a la carga

        if capacidad < carga:
            continue

        # Si el trayecto es peaje, se aplica recargo de 20%

        costo_nuevo = 0

        if tipo_ruta == "peaje":
            costo_nuevo = costo * (1.2)
        elif tipo_ruta == "puente":
            costo_nuevo = costo * (1.1)
        else:
            costo_nuevo = costo

        grafo.add_edge(
            origen, destino, costo=costo_nuevo, distancia=distancia, tiempo=tiempo
        )

    return grafo


grafo_reducido = grafo_reducido(df_1)

ruta = nx.shortest_path(
    grafo_reducido, source="Bogotá", target="Quito", weight="distancia"
)

costo = sum(grafo_reducido[ruta[i]][ruta[i + 1]]["costo"] for i in range(len(ruta) - 1))
distancia = sum(
    grafo_reducido[ruta[i]][ruta[i + 1]]["distancia"] for i in range(len(ruta) - 1)
)
tiempo = sum(
    grafo_reducido[ruta[i]][ruta[i + 1]]["tiempo"] for i in range(len(ruta) - 1)
)

print("1.2")
print(" -> ".join(ruta))
print(f"Costo: ${costo}")
print(f"Distancia: {distancia} km")
print(f"Tiempo total: {tiempo} horas")

# 1.3


def dijkstra(grafo_completo, source, target, ciudad_obligatoria):

    # [(distancia, nodo, ciudad_obligatoria, flag_peaje, ruta)]

    flag_cali = False
    contador_peaje = 0

    heap = [(0, flag_cali, contador_peaje, source, [source])]

    visitados = dict()

    while heap:

        distancia_acumulada, flag_cali, contador_peaje, nodo, ruta = heapq.heappop(heap)

        # optimalidad
        clave = (nodo, flag_cali, contador_peaje)

        if clave in visitados and distancia_acumulada >= visitados[clave]:
            continue

        visitados[clave] = distancia_acumulada

        # principio de llegada

        if nodo == target and flag_cali == True:  # Si llegue al destino y pase por cali
            if contador_peaje == 0:
                continue

            costo = sum(
                grafo_completo[ruta[i]][ruta[i + 1]]["costo"]
                for i in range(len(ruta) - 1)
            )
            tiempo = sum(
                grafo_completo[ruta[i]][ruta[i + 1]]["tiempo"]
                for i in range(len(ruta) - 1)
            )

            return costo, distancia_acumulada, tiempo, ruta

        for vecino in grafo_completo.neighbors(nodo):

            if vecino in ruta:
                continue

            contador_peaje_nuevo = contador_peaje

            if flag_cali == True:

                if grafo_completo[nodo][vecino]["tipo_ruta"] == "peaje":
                    contador_peaje_nuevo = contador_peaje + 1

            arco = grafo_completo.get_edge_data(nodo, vecino)

            distancia_nueva = distancia_acumulada + arco["distancia"]

            flag_cali_nuevo = flag_cali or (vecino == ciudad_obligatoria)

            nuevo_nodo = vecino

            nueva_ruta = ruta + [nuevo_nodo]

            heapq.heappush(
                heap,
                (
                    distancia_nueva,
                    flag_cali_nuevo,
                    contador_peaje_nuevo,
                    nuevo_nodo,
                    nueva_ruta,
                ),
            )

    return None, None


costo, distancia, tiempo, ruta = dijkstra(
    grafo_completo, "Medellín", "Guayaquil", "Cali"
)

print("1.3")
print(f"Costo:  + {costo}")
print(f"Distancia:  + {distancia}")
print(f"Tiempo:  + {tiempo}")
print(ruta)
