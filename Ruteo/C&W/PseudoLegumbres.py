"""
PSEUDOCÓDIGO — Clarke & Wright Multi-Depósito (Legumbres)
---------------------------------------------------------

ENTRADA:
  - Dos depósitos: D1 y D2
  - Matriz de costos o distancias
  - Demanda por cliente, capacidad vehículo (si aplica)

1) Calcular ahorros por depósito:
   Para cada par (i,j):
      S1(i,j) = C(D1,i) + C(D1,j) - C(i,j)
      S2(i,j) = C(D2,i) + C(D2,j) - C(i,j)

2) Matriz conjunta y asignación de depósito:
   S(i,j) = max(S1(i,j), S2(i,j))
   DepGanador(i,j) = D1 si S1≥S2, si no D2
   Ordenar pares (i,j) por S descendente.

3) Inicializar rutas por cliente (aún sin fijar depósito final):
   R[i] = [DepTemporal, i, DepTemporal] (solo para empezar)

4) Fusionar respetando depósito:
   Para (i,j) por S:
      - Identificar R1 con extremo i y R2 con extremo j
      - Verificar factibilidad (capacidad, tiempos si aplica)
      - Si factible:
           * Unir R1 y R2
           * Fijar el depósito de esa nueva ruta al DepGanador(i,j)
           * Asegurar que todas las rutas NO mezclen depósitos

5) Al terminar:
   - Separar rutas por depósito (todas de D1 y todas de D2)
   - Calcular costo/distancia por depósito y total.
"""