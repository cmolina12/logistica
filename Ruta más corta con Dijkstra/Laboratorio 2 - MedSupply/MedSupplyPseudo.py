"""
PSEUDOCÓDIGO — Mejor ruta de menor costo (MedSupply LATAM)
===========================================================

PROCEDIMIENTO MejorRuta_MedSupply(Rutas, Estaciones, Origen, Destino, CiudadObligatoria, CargaKG)

1. Crear diccionario de autonomía de estaciones
   ---------------------------------
   Para cada fila en Estaciones:
       Autonomia[Nombre] = valor de la columna "Autonomía"

2. Construir grafo con rutas válidas
   ---------------------------------
   Crear grafo dirigido vacío G

   Para cada fila en Rutas:
       origen = "Origen"
       destino = "Destino"
       distancia = "Distancia_km"
       tiempo = "Tiempo_estimado_h"
       transporte = "Transporte"
       clima = "Clima"
       ventana = "Ventana_Horaria"
       capacidad = "Capacidad_Maxima_kg"
       refrigeracion = "Refrigeración"

       # Restricción 1: no usar rutas con clima = “Tormenta”
       Si clima == "Tormenta":
           continuar

       # Restricción 2: descartar si ventana < 8 horas
       Dividir ventana en inicio y fin
       Si (fin - inicio) < 8:
           continuar

       # Restricción 3: debe tener refrigeración disponible
       Si refrigeracion == "No":
           continuar

       # Penalización por exceso de carga
       Si CargaKG > capacidad:
           penalizacion = 0.15
       Si no:
           penalizacion = 0

       # Cálculo del costo según tipo de transporte
       Si transporte == "Camión": constante = 1
       Si transporte == "Barco":  constante = 1.5
       Si transporte == "Avión":  constante = 2

       costo = (10 * distancia + 100 * constante) * (1 + penalizacion)

       Añadir al grafo arco (origen → destino) con:
           costo = costo
           distancia = distancia
           tiempo = tiempo

3. Dijkstra modificado con restricciones
   ---------------------------------
   La cola prioriza (menor costo, menor tiempo en caso de empate)

   Si origen == CiudadObligatoria: flag_medellin = Verdadero, sino Falso
   contador_baja = 1 si Autonomía[origen] == "Baja", sino 0

   Insertar en PQ: (costo=0, tiempo=0, nodo=Origen, flag_medellin, contador_baja, ruta=[Origen])
   Crear diccionario visitados vacío

   Mientras PQ no esté vacía:
       sacar el elemento con menor (costo, tiempo)
       Si nodo == Destino y flag_medellin == Verdadero y contador_baja <= 1:
           Calcular distancia_total sumando las distancias de la ruta
           Retornar ruta, costo, tiempo, distancia_total

       clave = (nodo, flag_medellin, contador_baja)
       Si clave ya existe en visitados y el par (costo, tiempo) no mejora:
           continuar
       guardar visitados[clave] = (costo, tiempo)

       Para cada vecino del nodo:
           Si vecino ya está en la ruta:
               continuar

           costo_nuevo = costo + costo(nodo, vecino)
           tiempo_nuevo = tiempo + tiempo(nodo, vecino)
           flag_medellin_nuevo = flag_medellin o (vecino == CiudadObligatoria)
           contador_baja_nuevo = contador_baja + 1 si Autonomía[vecino] == "Baja"

           Si contador_baja_nuevo > 1:
               continuar

           nueva_ruta = ruta + [vecino]
           Insertar en PQ:
               (costo_nuevo, tiempo_nuevo, vecino, flag_medellin_nuevo, contador_baja_nuevo, nueva_ruta)

4. Si no se encuentra ruta válida:
   ---------------------------------
   retornar sin_ruta, +∞, +∞, +∞

----------------------------------------------------------
Resumen de lógica:
  - El grafo elimina rutas con tormenta, poca ventana o sin refrigeración.
  - Aplica penalización del 15% si la carga excede la capacidad.
  - Dijkstra prioriza menor costo; en empate, menor tiempo.
  - La ruta debe pasar por Medellín y tener máximo una estación de autonomía baja.
"""