"""
PSEUDOCÓDIGO — Heurística de Ahorros de Clarke & Wright
========================================================

OBJETIVO:
Determinar la combinación de rutas que minimiza la distancia o el costo total de distribución,
partiendo de un depósito central (o varios, en versión extendida).

DATOS DE ENTRADA:
  - Matriz de distancias o costos entre nodos (incluyendo el depósito)
  - Capacidad máxima de cada vehículo
  - Demanda de cada cliente
  - (Opcional según el problema: tiempo máximo de ruta, ventanas horarias, tipo de vehículo, etc.)

------------------------------------------------------------
1. Calcular los ahorros de cada par de clientes
------------------------------------------------------------
Para cada par de clientes (i, j):
    Si i ≠ j y ambos distintos del depósito:
        Ahorro(i, j) = Costo(depot → i) + Costo(depot → j) - Costo(i → j)

Guardar los ahorros en una tabla y ordenarlos de mayor a menor.

# Si hay dos depósitos (caso Legumbres):
#   Calcular Ahorros1 con respecto al depósito 1
#   Calcular Ahorros2 con respecto al depósito 2
#   Combinar ambas tablas con AhorroFinal(i, j) = MAX(Ahorros1(i, j), Ahorros2(i, j))
#   Registrar a cuál depósito pertenece el máximo (para asignar luego la ruta)

------------------------------------------------------------
2. Inicializar las rutas individuales
------------------------------------------------------------
Para cada cliente i:
    Crear una ruta inicial: [Depósito - i - Depósito]
    Cargar la demanda de i en esa ruta
    Registrar el tiempo o distancia total de esa ruta

------------------------------------------------------------
3. Intentar unir rutas según los mayores ahorros
------------------------------------------------------------
Para cada par (i, j) en orden descendente de ahorro:
    Revisar si el cliente i está al final de alguna ruta existente R1
    y el cliente j está al inicio de otra ruta existente R2

    Si ambas rutas existen y:
        - La suma de sus demandas ≤ capacidad del vehículo
        - (Si aplica) la nueva distancia/tiempo ≤ límite máximo
        - (Si aplica) la unión no viola ventanas horarias ni precedencias
        - (Si aplica) el tipo de vehículo coincide con las condiciones

    Entonces:
        Unir las dos rutas → NuevaRuta = R1 + R2 (sin repetir depósitos)
        Marcar clientes i y j como conectados
        Reemplazar R1 y R2 por NuevaRuta en la lista de rutas

------------------------------------------------------------
4. Continuar hasta que no sea posible más fusiones
------------------------------------------------------------
Repetir el paso 3 hasta que ningún par (i, j) genere una unión factible.

------------------------------------------------------------
5. Calcular el costo o distancia total final
------------------------------------------------------------
Para cada ruta final obtenida:
    Calcular:
        - Distancia total
        - Carga total
        - (Opcional) Tiempo total de la ruta
        - (Opcional) Penalizaciones por exceso, esperas, etc.

Sumar los resultados y reportar:
    - Rutas definitivas
    - Costo total acumulado
    - Número de vehículos usados
    - Utilización promedio de capacidad

------------------------------------------------------------
ADAPTACIONES SEGÚN EL CASO:
------------------------------------------------------------
- FRÍO EXPRESS:
   - Es un C&W estándar con límite de 500 km por ruta.
   - Si una unión excede 500 km, se descarta.

- LEGUMBRES:
   - Hay dos depósitos.
   - Calcular dos matrices de ahorro (una por depósito) y combinar con el máximo.
   - Asignar cada ruta al depósito que ganó el máximo ahorro.

- FRUITBANA:
   - Añadir verificación de ventanas horarias y tiempo máximo.
   - Si llegas antes, puedes esperar; si te pasas, la ruta no es factible.

- MIS PRIMEROS PASOS:
   - Es un C&W de recolección.
   - Se parte de los barrios hacia el jardín.
   - Se debe llegar antes de las 7:00 AM y la capacidad limita el número de niños.

- BAVARIA:
   - Es un C&W con entregas y recogidas simultáneas.
   - Se debe garantizar que la carga total (entregas - recogidas) nunca supere 90 unidades.

------------------------------------------------------------
SALIDA:
------------------------------------------------------------
Mostrar tabla resumen:
    Iteración | Arco | Ahorro | ¿Factible? | Ruta consolidada | Distancia | Carga
Y el costo o distancia total del conjunto de rutas óptimas.
"""