"""
PSEUDOCÓDIGO — Mejor ruta de menor costo (UltraCargo Inc.)
===========================================================

PROCEDIMIENTO MejorRuta_UltraCargo(Rutas, Ciudades, Origen, Destino,
                                   CargaTN, HoraLimiteAereo, UsarTexasSoloAereo,
                                   UsarCostoAereo22, TiempoMinimoHoras)

1. Preparar mapa ciudad → estado
   ---------------------------------
   Para cada fila en Ciudades:
       guardar Estado[Ciudad] = valor de la columna "Estado"

2. Construir el grafo con rutas válidas
   ---------------------------------
   Crear un grafo dirigido vacío llamado G

   Para cada fila en Rutas:
       origen     = "Origen"
       destino    = "Destino"
       distancia  = "Distancia"
       velocidad  = "Velocidad"
       frontera   = "Frontera"
       alta_dem   = "Alta_Demanda"
       capacidad  = "Capacidad"
       horario    = "Horario"
       terrestre  = "Terrestre"
       aereo      = "Aereo"
       vuelos     = "Vuelos"

       # Regla 1: Si es ruta aérea y el horario >= HoraLimiteAereo → eliminar
       Si aereo = 1 y horario >= HoraLimiteAereo:
           continuar

       # Regla 2: Si toca Texas, solo se permiten rutas aéreas (cuando aplica)
       toca_texas = (Estado[origen] == "Texas") o (Estado[destino] == "Texas")
       Si UsarTexasSoloAereo y toca_texas y aereo = 0:
           continuar

       # Penalización si la carga supera la capacidad
       Si CargaTN > capacidad:
           penalizacion = 0.15
       Si no:
           penalizacion = 0

       # Cálculo del costo logístico
       Si aereo = 1 y UsarCostoAereo22:
           costo_base = 500 + 3*distancia + 50*vuelos       # Fórmula 2.2
       Si no:
           flag_frontera = 1 si frontera = 1, sino 0
           flag_alta     = 1 si alta_dem = 1, sino 0
           costo_base = 15*distancia + 200*flag_frontera + 150*flag_alta

       costo_arco = costo_base * (1 + penalizacion)
       tiempo_arco = distancia / velocidad

       Añadir al grafo conexión (origen → destino) con:
           costo = costo_arco
           distancia = distancia
           tiempo = tiempo_arco

3. Dijkstra por costo con desempate por tiempo
   ---------------------------------
   Crear una cola de prioridad PQ que priorice (menor costo, menor tiempo)
   Insertar en PQ: (costo=0, tiempo=0, nodo=Origen, ruta=[Origen])

   Crear diccionario visitados vacío
   Mientras PQ no esté vacía:
       sacar el elemento con menor (costo, tiempo)
       Si nodo == Destino:
           Si TiempoMinimoHoras > 0 y tiempo_acum < TiempoMinimoHoras:
               continuar
           Calcular distancia_total sumando los arcos de la ruta
           Retornar ruta, costo_acum, distancia_total, tiempo_acum

       Si nodo ya está en visitados con valores mejores o iguales:
           continuar
       guardar visitados[nodo] = (costo_acum, tiempo_acum)

       Para cada vecino del nodo:
           Si vecino ya está en la ruta:
               continuar
           costo_nuevo  = costo_acum + costo(nodo, vecino)
           tiempo_nuevo = tiempo_acum + tiempo(nodo, vecino)
           ruta_nueva = ruta + [vecino]
           Insertar en PQ: (costo_nuevo, tiempo_nuevo, vecino, ruta_nueva)

4. Si no hay ruta válida:
   ---------------------------------
   retornar sin_ruta, +∞, +∞, +∞

----------------------------------------------------------
Parámetros típicos de uso:
  • Caso 1.2 (San Diego → Denver)
        HoraLimiteAereo = 11
        UsarTexasSoloAereo = Falso
        UsarCostoAereo22 = Falso
        TiempoMinimoHoras = 0
        CargaTN = 20
  • Caso 1.3 (Guadalajara → Miami)
        HoraLimiteAereo = 0
        UsarTexasSoloAereo = Verdadero
        UsarCostoAereo22 = Verdadero
        TiempoMinimoHoras = 70
        CargaTN = valor según el enunciado
"""