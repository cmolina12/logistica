# ============================================================
# 🧭 SECCIÓN 1: CREACIÓN Y ESTRUCTURA DEL GRAFO
# ============================================================

import networkx as nx

# Crear un grafo dirigido
G = nx.DiGraph()

# Agregar nodos manualmente
G.add_node("Bogotá")

# Agregar aristas con atributos personalizados
G.add_edge("Bogotá", "Medellín", distancia=400, costo=300)

# Listar nodos
print(list(G.nodes()))

# Listar aristas con atributos
print(list(G.edges(data=True)))

# Obtener el grado (número de conexiones) de un nodo
print(G.degree("Bogotá"))

# Obtener los vecinos de un nodo
print(list(G.neighbors("Bogotá")))

# Verificar si el grafo es dirigido
print(nx.is_directed(G))


# ============================================================
# 🧮 SECCIÓN 2: CÁLCULO DE RUTAS Y DISTANCIAS
# ============================================================

# Ruta más corta entre dos nodos (por costo)
ruta = nx.shortest_path(G, source="Bogotá", target="Medellín", weight="costo")
print(ruta)

# Costo total del trayecto
costo_total = nx.shortest_path_length(G, source="Bogotá", target="Medellín", weight="costo")
print(costo_total)

# Dijkstra desde una fuente a todos los nodos
distancias, rutas = nx.single_source_dijkstra(G, source="Bogotá", weight="costo")
print(distancias)
print(rutas)

# Dijkstra entre dos nodos
ruta_dijkstra = nx.dijkstra_path(G, "Bogotá", "Medellín", weight="distancia")
print(ruta_dijkstra)

# Predecesores y distancias
pred, dist = nx.dijkstra_predecessor_and_distance(G, "Bogotá")
print(pred)
print(dist)

# Todas las rutas más cortas entre todos los nodos
todas = nx.all_pairs_dijkstra_path(G, weight="costo")
print(dict(todas))


# ============================================================
# 🧰 SECCIÓN 3: ANÁLISIS DE CONECTIVIDAD
# ============================================================

# Verificar si todo el grafo está conectado (en dirigido)
print(nx.is_strongly_connected(G))

# Número de componentes conectados (no dirigido)
print(nx.number_connected_components(G.to_undirected()))

# Conjuntos de nodos conectados
print(list(nx.connected_components(G.to_undirected())))

# Verificar si hay un camino entre dos nodos
print(nx.has_path(G, "Bogotá", "Medellín"))


# ============================================================
# 📊 SECCIÓN 4: CENTRALIDAD Y MÉTRICAS
# ============================================================

# Nodos más conectados (grado)
print(nx.degree_centrality(G))

# Nodos más transitados en rutas
print(nx.betweenness_centrality(G))

# Nodos más cercanos al resto
print(nx.closeness_centrality(G))

# Influencia o importancia (como PageRank)
print(nx.eigenvector_centrality(G))


# ============================================================
# 🧩 SECCIÓN 5: VISUALIZACIÓN Y ETIQUETAS
# ============================================================

import matplotlib.pyplot as plt

# Layout automático (posición de nodos)
pos = nx.spring_layout(G)

# Dibujar el grafo
nx.draw_networkx(G, pos, with_labels=True, node_color="lightblue", node_size=700)

# Dibujar etiquetas de las aristas (como el costo)
labels = nx.get_edge_attributes(G, "costo")
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_color="green")

plt.title("Grafo de rutas logísticas")
plt.axis("off")
plt.show()


# ============================================================
# 🧠 SECCIÓN 6: TRANSFORMACIONES Y UTILIDADES
# ============================================================

import pandas as pd

# Crear grafo directamente desde un DataFrame (por ejemplo, desde Excel)
df = pd.DataFrame({
    "Origen": ["Bogotá", "Medellín"],
    "Destino": ["Cali", "Cartagena"],
    "Costo": [300, 500],
    "Distancia": [400, 800]
})

G2 = nx.from_pandas_edgelist(
    df,
    source="Origen",
    target="Destino",
    edge_attr=["Costo", "Distancia"],
    create_using=nx.DiGraph()
)

# Convertir grafo a DataFrame (para inspección o exportar)
df_edges = nx.to_pandas_edgelist(G2)
print(df_edges)

# Crear subgrafo con algunos nodos
subG = G2.subgraph(["Bogotá", "Cali"])
print(subG.edges())

# Invertir direcciones de las aristas
G_reverso = G2.reverse()
print(G_reverso.edges())

# Unir dos grafos distintos
G3 = nx.compose(G, G2)

# Cambiar nombres de nodos
mapping = {"Bogotá": "BOG", "Cali": "CLO"}
G_renombrado = nx.relabel_nodes(G2, mapping)
print(list(G_renombrado.nodes()))


# ============================================================
# ⚙️ SECCIÓN 7: TRUCOS AVANZADOS PARA LOGÍSTICA Y OPTIMIZACIÓN
# ============================================================

# 1️⃣ Crear un grafo desde Excel con atributos relevantes

# G = nx.from_pandas_edgelist(df_vuelos, source="origen", target="destino",
#     edge_attr=["distancia(km)", "precio($)"], create_using=nx.DiGraph())

# 2️⃣ Calcular costo total de una ruta ya encontrada

# ruta = nx.shortest_path(G, "ATL", "EWR", weight="precio($)")
# costo = sum(G[ruta[i]][ruta[i+1]]["precio($)"] for i in range(len(ruta)-1))

# 3️⃣ Acceder a los atributos de una arista específica

# print(G["ATL"]["STL"])  # {'distancia(km)': 1500, 'precio($)': 120}

# 4️⃣ Eliminar rutas que no cumplen condiciones

# for u, v, data in list(G.edges(data=True)):
#     if data["distancia(km)"] > 1000:
#         G.remove_edge(u, v)

# 5️⃣ Calcular rutas de múltiples criterios (personalizado)

# for vecino in G.neighbors(nodo):
#     data = G[nodo][vecino]
#     costo = data["costo"]
#     tiempo = data["tiempo"]
#     # ... aplicar tus condiciones y restricciones aquí ...

