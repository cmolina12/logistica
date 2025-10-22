"""
PSEUDOCÓDIGO — Clarke & Wright (Escolar: recolección con deadline)
-------------------------------------------------------------------

ENTRADA:
  - Todos los nodos son puntos de recogida que terminan en el jardín (depósito)
  - Tiempo de servicio por niño = 10 min
  - Hora límite de llegada al jardín: 7:00
  - Capacidad del bus (número máximo de niños)
  - Tiempos/distancias entre barrios y jardín

1) Calcular ahorros S(i,j) con respecto al jardín (depósito 0).

2) Rutas iniciales:
   R[i] = [i, 0]  (recolección → depósito)
   Niños(R[i]) = 1
   Cronograma: simular desde el último pickup hacia el jardín
       (o desde el primero acumulando hasta llegar al jardín)
   Verificar llegada_al_jardín ≤ 7:00

3) Fusión por (i,j):
   - Unir rutas donde i sea extremo de R1 y j extremo de R2 (secuencia de pickups)
   - Verificar:
       * Niños(R1)+Niños(R2) ≤ CapBus
       * Recalcular cronograma (sumar tiempos de servicio + viaje)
       * Llegada final al jardín ≤ 7:00
   - Si factible → aceptar unión

4) Repetir hasta no poder unir más.

5) Reportar rutas finales, llegada al jardín, #niños por ruta y distancia total.
"""