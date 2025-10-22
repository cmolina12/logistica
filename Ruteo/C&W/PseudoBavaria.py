"""
PSEUDOCÓDIGO — Clarke & Wright (Simultáneo: entregas + recogidas)
------------------------------------------------------------------

ENTRADA:
  - Cada cliente k tiene demanda de entrega Dk (≥0) y recogida Rk (≥0)
  - Capacidad del vehículo = 90
  - Modelar carga neta como: +Dk al entregar, −Rk al recoger (o la convención que uses)
  - Restricción: en TODO momento, 0 ≤ CargaAcum ≤ 90

1) Calcular ahorros S(i,j) estándar y ordenar desc.

2) Rutas iniciales:
   R[i] = [0, i, 0]
   Simular secuencia (según orden de visita) y calcular CargaAcum a lo largo de la ruta
   Verificar 0 ≤ CargaAcum ≤ 90 en todo punto (prefijos)

3) Fusión por (i,j):
   - Unir extremos i (final R1) con j (inicio R2) → NuevaRuta
   - Re-simular la carga acumulada a lo largo de NuevaRuta:
       * En cada visita k:
           CargaAcum ← CargaAcum + Dk − Rk
           Si CargaAcum < 0 o CargaAcum > 90 → NO factible
   - Si factible → aceptar fusión y actualizar ruta

4) Repetir hasta no poder unir más.

5) Reportar rutas finales y métricas (distancia, perfil de carga, #vehículos).
"""