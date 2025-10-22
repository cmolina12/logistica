"""
PSEUDOCÓDIGO — Clarke & Wright (FríoExpress)
--------------------------------------------

ENTRADA:
  - Matriz/tabla de costos o distancias (incluye depósito 0 y clientes)
  - Capacidad vehículo (si aplica), demanda por cliente (si aplica)
  - Lista de arcos factibles (eliminar arcos 'INF' o prohibidos)
  - (Opcional) LIMITE_RUTA_KM = 500 (activar si aplica el inciso)

1) Filtrar arcos:
   - Eliminar arcos prohibidos o INF.
   - Si trabajas en Excel, deja celdas vacías o sin fórmula para esos arcos.

2) Calcular ahorros:
   Para cada par (i, j) con i ≠ j y ambos ≠ 0:
      Ahorro(i,j) = C(0,i) + C(0,j) - C(i,j)
   Ordenar pares (i,j) por Ahorro descendente.

3) Inicializar rutas:
   Para cada cliente i: R[i] = [0, i, 0]
   Carga(R[i]) = Demanda(i) (si aplica)

4) Fusionar rutas por ahorros:
   Para (i,j) en orden de mayor ahorro:
      - Si i está al extremo de una ruta R1 y j al extremo de una ruta R2 (R1 ≠ R2)
      - Verificar factibilidad:
          * Capacidad (si aplica): Carga(R1)+Carga(R2) ≤ CapVeh
          * Límite de ruta (si aplica): Distancia(R1⊕R2) ≤ LIMITE_RUTA_KM
      - Si factible: R ← unir R1 y R2 (sin repetir depósitos) y actualizar listas

5) Repetir fusiones hasta que no haya más uniones factibles.

6) Calcular métricas finales:
   - Para cada ruta: sumar distancia/costo total.
   - Reportar: rutas finales, distancia/costo total y # vehículos.
"""