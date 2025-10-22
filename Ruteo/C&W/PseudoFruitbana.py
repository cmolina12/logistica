"""
PSEUDOCÓDIGO — Clarke & Wright con Ventanas de Tiempo (Fruitbana)
------------------------------------------------------------------

ENTRADA:
  - Ventanas [a_i, b_i] por cliente y tiempo de servicio s_i
  - Tiempo máximo de ruta (si aplica)
  - Distancias/tiempos entre nodos, capacidad y demanda

1) Calcular ahorros S(i,j) estándar y ordenar desc.

2) Rutas iniciales:
   R[i] = [0, i, 0], con:
     - Carga = demanda(i)
     - Cronograma: llegada a i = max(a_i, tiempo_desde_0_i), salida_i = llegada_i + s_i
     - Verificar salida_0 final ≤ Tmax (si aplica)

3) Intento de fusión R1 con R2 por (i,j):
   - Unir extremos i (fin de R1) con j (inicio de R2)
   - Recalcular cronograma hacia adelante:
       * Para cada cliente k en la parte añadida:
           llegada_k = max(a_k, llegada_previa + viaje_previo_k)
           Si llegada_k > b_k → NO factible
           salida_k = llegada_k + s_k
   - Verificar:
       * Capacidad: suma demandas ≤ CapVeh
       * Tiempo máximo de ruta (si aplica)
   - Si todo OK → Aceptar fusión

4) Repetir fusiones hasta agotarlas.

5) Reporte final: rutas, costo/tiempo total, esperas (si hubo), utilización de capacidad.
"""