<!-- NOTEBOOK: -->

## Repaso de Python para este cuaderno

Este cuaderno utiliza los siguientes métodos de Python. Si ya los conoce, ejecute estas celdas rápido.

### Un grafo como diccionario de conjuntos
Cada nodo es una clave.
Su valor es el conjunto de nodos con los que tiene un enlace.
Sin dirección, el enlace va en los dos lados.
El **grado** es el tamaño del conjunto.

```python
toy = {"A": set(), "B": set(), "C": set(), "D": set(), "E": set()}  # cada nodo empieza con un conjunto vacío de vecinos
for a, b in [("A", "B"), ("A", "C"), ("B", "C"), ("C", "D")]:  # recorremos los cuatro enlaces del ejemplo
    toy[a].add(b)  # add pone a b entre los vecinos de a
    toy[b].add(a)  # add pone a a entre los vecinos de b, porque el enlace no tiene dirección
toy_neighbours = {}  # aquí guardamos los vecinos de cada nodo, en orden alfabético
toy_degree = {}  # aquí guardamos el grado de cada nodo
for v in toy:  # recorremos cada nodo
    toy_neighbours[v] = sorted(toy[v])  # sorted ordena los vecinos para imprimirlos
    toy_degree[v] = len(toy[v])  # len cuenta los vecinos, que es el grado
print(toy_neighbours)  # print muestra los vecinos de cada nodo
print("Grado de cada nodo:", toy_degree)  # print muestra el grado de cada nodo
```

### Búsqueda por niveles a mano
La búsqueda en anchura visita primero a los vecinos.
Después visita a los vecinos de los vecinos, y cuenta los pasos.
La cola guarda los nodos que faltan, en orden.

```python
from collections import deque  # deque es una cola: sacamos por un lado y agregamos por el otro

steps = {"A": 0}  # A está a 0 pasos de sí mismo
queue = deque(["A"])  # la cola empieza con A
while queue:  # seguimos mientras queden nodos en la cola
    u = queue.popleft()  # popleft saca el primer nodo de la cola
    for v in sorted(toy[u]):  # recorremos sus vecinos en orden alfabético
        if v not in steps:  # solo los vecinos que todavía no visitamos
            steps[v] = steps[u] + 1  # el vecino queda a un paso más que u
            queue.append(v)  # append pone al vecino al final de la cola
assert steps == {"A": 0, "B": 1, "C": 1, "D": 2}  # comprobamos los pasos del ejemplo
print(f"Pasos desde A: {steps}. E no se alcanza. Repaso de Python: OK")  # print muestra los pasos desde A
```

**Lo que vemos.** D está a dos pasos de A porque hay que pasar por C.
La Parte 4 usa esta búsqueda para la intermediación, que se apoya en los caminos más cortos.

---

## Instrucciones

Seguimos con el equipo interno de la secretaría de salud y sus 320 artículos sobre nutrición.
El equipo debe decidir **qué artículos tiene que leer** un nuevo colega.

Los artículos se citan entre ellos.
Los índices de citas guardaron esos enlaces para las bibliotecas, y la web los volvió a usar entre páginas.
Page et al. (1998) propusieron que un enlace desde una página importante pese más.
Hoy describimos un artículo por su **lugar entre los demás**.
Un artículo enlazado con muchos es una **alerta**, porque puede ser una revisión que todos citan.
Un artículo **citado por artículos importantes** puede ser el que el colega necesita.

**Tres métodos, dos grafos.**

| Método | Pregunta | Preparación que necesita |
|--------|----------|--------------------------|
| M1. PageRank | ¿Lo citan artículos que también son citados? | La lista de enlaces con dirección, un grafo dirigido. El grado entra aquí, como idea, no como método aparte |
| M2. Intermediación | ¿Queda en los caminos más cortos entre otros? | La misma lista sin dirección |
| M3. Louvain | ¿Qué grupos tienen más enlaces por dentro que por fuera? | La misma lista sin dirección |

**Qué hacer.** Ejecute las celdas de arriba hacia abajo.
Cada paso empieza con **En este paso**. Si tiene código, termina con una celda **Comprobar**.

**Mapa del cuaderno**

| Parte | Fase CRISP-DM | Qué sale |
|-------|---------------|----------|
| 1 | Comprensión del negocio | La pregunta de hoy, los parámetros y los artículos |
| 2 | Comprensión de los datos | Los artículos y sus enlaces |
| 3 | Preparación de los datos | La lista de enlaces y los dos grafos |
| 4 | Modelado | PageRank (con el grado), intermediación y Louvain |
| 5 | Evaluación | Contra las citas, un artículo descrito por su lugar, modularidad y la intermediación frente al grado |
| 6 | Despliegue | La lista del grafo, hasta 30 artículos, en `outputs/grafo_l5.csv` |

**Carpetas.** La celda de configuración crea `data/` (datos descargados) y `outputs/` (tablas y gráficos).

---

## Parte 1. Comprensión del negocio

### Paso 1. La pregunta de esta lección
En este paso escribimos qué buscamos hoy.
La decisión no cambia: qué artículos debe leer el colega nuevo.

| Pregunta | Respuesta para el laboratorio |
|----------|-------------------------------|
| ¿Qué buscamos? | El lugar de cada artículo en la red de citas dentro de la colección |
| ¿Con qué lo medimos? | PageRank, intermediación y comunidades de Louvain |
| ¿Contra qué lo comparamos? | Contra las citas en el mundo y entre los tres métodos |
| ¿Cómo entra el grafo en la lista? | Un artículo entra si tiene enlaces, su PageRank está en el cuarto superior de esos artículos y no es un nodo central. La lista guarda como máximo 30, los de PageRank más alto |

Un nodo central es una alerta, no un lugar en la lista.
Un artículo aislado no recibe el resultado del grafo.

### Paso 2. Configuración
En este paso importamos las librerías, creamos las carpetas y fijamos los parámetros.
No cambie los parámetros.

```python
import math  # math.ceil redondea hacia arriba los mínimos
from collections import deque  # deque es la cola de la búsqueda en anchura
from pathlib import Path  # Path arma las rutas de las carpetas

import matplotlib.pyplot as plt  # matplotlib dibuja las figuras
import networkx as nx  # networkx arma los grafos y calcula PageRank, intermediación y Louvain
import numpy as np  # numpy calcula promedios
import pandas as pd  # pandas lee y guarda las tablas
import requests  # requests descarga los datos del curso
from scipy.stats import spearmanr  # spearmanr compara dos órdenes

# Carpetas de trabajo
DATA_DIR = Path("data")  # aquí quedan los datos descargados
OUTPUTS_DIR = Path("outputs")  # aquí quedan las tablas y las figuras
DATA_DIR.mkdir(parents=True, exist_ok=True)  # mkdir crea la carpeta de datos si no existe
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)  # mkdir crea la carpeta de salidas si no existe
BASE_URL = "https://cabrerac.github.io/assets/data/26-udenar-data-mining"  # la dirección web de los datos del curso

# Desde L2, sin cambios
SUPPORT_SHARE = 0.03  # proporción mínima de artículos de la L2
SUPPORT_MIN = 5  # mínimo de artículos de la L2
SEED = 7  # semilla de Louvain y del dibujo

# L5 (no cambiar)
HUB_SHARE = 0.10  # un nodo enlazado a al menos el 10% de los otros es una alerta
MIN_LINKS = 5  # nunca menos de 5 enlaces para una alerta
DAMPING = 0.85  # probabilidad de seguir un enlace en PageRank

# Propio de este cuaderno
EXAMPLE = "Guidelines for the Primary Prevention of Stroke"  # el artículo que describimos por su lugar


def hub_threshold(n, min_links=MIN_LINKS):
    """Cuántos enlaces necesita un nodo para ser una alerta de nodo central.

    Qué hace: un nodo enlazado con al menos el 10% de los otros (HUB_SHARE) es una alerta.
    En redes pequeñas el 10% puede ser 1 o 2 enlaces, así que nunca pedimos
    menos de min_links. Es la misma regla en todo el curso.

    Entrada:
        n: número de nodos de la red.
        min_links: piso de enlaces, MIN_LINKS = 5 por defecto.

    Salida:
        El número entero de enlaces desde el cual un nodo es una alerta.
    """
    return max(min_links, math.ceil(HUB_SHARE * (n - 1)))  # max nunca baja de min_links, y ceil redondea el 10% hacia arriba


print(f"networkx {nx.__version__}. Alerta desde {hub_threshold(318)} enlaces con 318 artículos")  # print muestra la versión y el umbral de la alerta
```

### Paso 3. Descargar los artículos
En este paso descargamos los artículos.
La columna nueva es `links`, con los títulos que cada artículo cita dentro del conjunto.

```python
def download_data(name: str, folder: Path = DATA_DIR) -> Path:
    """Descarga un archivo de datos del curso, una sola vez.

    Qué hace: si el archivo ya está en la carpeta, lo usa. Si no, lo baja de BASE_URL.

    Entrada:
        name: nombre del archivo. folder: carpeta local, DATA_DIR por defecto.

    Salida:
        La ruta local del archivo.
    """
    dest = folder / name  # la ruta local del archivo
    if dest.is_file() and dest.stat().st_size > 0:  # is_file y st_size dicen si ya lo tenemos y no está vacío
        print(f"Ya en caché: {dest}")  # print avisa que usamos la copia local
        return dest  # devolvemos la ruta sin descargar
    response = requests.get(f"{BASE_URL}/{name}", timeout=60)  # requests.get descarga el archivo
    response.raise_for_status()  # raise_for_status detiene la celda si la descarga falló
    dest.write_bytes(response.content)  # write_bytes guarda el archivo en la carpeta
    print(f"Descargado: {dest}")  # print avisa que el archivo quedó guardado
    return dest  # devolvemos la ruta local


raw = pd.read_csv(download_data("nutricion-papers.csv"), keep_default_na=False)  # read_csv lee los artículos y deja los vacíos como texto vacío
print(f"{len(raw)} filas, columnas: {list(raw.columns)}")  # print muestra el tamaño y las columnas
```

### Paso 4. La pregunta
La pregunta es la de la Lección 1.
El equipo decide qué artículos de nutrición leer, y qué filtro los puso en la lista.
La lista tiene entre 10 y 30 artículos.
Lo nuevo es el grafo.
Un artículo entra en la lista si tiene enlaces, está en el cuarto superior por PageRank entre esos artículos y no es un nodo central.

```python
MIN_PAPERS = 10  # la lista tiene al menos 10 artículos
MAX_PAPERS = 30  # la lista tiene como máximo 30 artículos
print(f"Lista: entre {MIN_PAPERS} y {MAX_PAPERS} artículos")  # print muestra el tamaño de la lista
```

---

## Parte 2. Comprensión de los datos

### Paso 1. Los artículos y los títulos repetidos
En este paso quitamos los títulos repetidos, porque un nodo es un título.
Quedan 318 filas.

```python
repeated = raw.loc[raw["title"].duplicated(), "title"].tolist()  # duplicated marca los títulos que ya aparecieron antes
papers = raw.drop_duplicates("title").reset_index(drop=True)  # drop_duplicates deja una fila por título
N = len(papers)  # len cuenta los artículos, uno por nodo
print(f"Títulos repetidos: {len(repeated)}")  # print muestra cuántos títulos estaban repetidos
for t in repeated:  # recorremos los títulos repetidos
    print("  ", t[:90])  # print muestra los primeros 90 caracteres del título
print(f"Artículos (nodos): {N}")  # print muestra cuántos nodos quedan
```

### Paso 2. Cómo vienen los enlaces
En este paso miramos `links`, con los títulos citados separados por `|`.
Solo cuentan los enlaces a artículos **del conjunto**.

```python
title_set = set(papers["title"])  # set guarda los títulos para buscarlos rápido
listed = []  # aquí guardamos cada enlace escrito
for links in papers["links"]:  # recorremos la columna links de cada artículo
    for t in str(links).split("|"):  # split separa los títulos citados por la barra |
        if t.strip():  # strip quita los espacios, y dejamos fuera los textos vacíos
            listed.append(t.strip())  # append guarda el título citado
inside = []  # aquí guardamos los enlaces a artículos del conjunto
for t in listed:  # recorremos cada enlace escrito
    if t in title_set:  # dejamos solo los títulos que están en el conjunto
        inside.append(t)  # append guarda el enlace de adentro
print(f"Enlaces escritos: {len(listed)}. Dentro del conjunto: {len(inside)}")  # print compara los dos conteos
print("Ejemplo:", papers.loc[papers["links"] != "", "links"].iloc[0][:150])  # iloc toma el primer artículo que tiene enlaces
```

---

## Parte 3. Preparación de los datos

### Paso 1. La lista de enlaces dentro del conjunto
En este paso guardamos cada enlace dos veces.
`links_out` va con dirección, para PageRank.
`neighbours` va sin dirección, para el grado (dentro de PageRank), la intermediación y Louvain.
Un artículo que se cita a sí mismo no cuenta.

```python
df = papers  # df es la tabla de artículos
df = df.drop_duplicates("title")  # drop_duplicates asegura una fila por artículo
titles = list(df["title"])  # list guarda los títulos en orden
title_set = set(titles)  # set guarda los títulos para buscarlos rápido
links_out = {}  # con dirección, para PageRank
for t in titles:  # recorremos cada título
    links_out[t] = set()  # cada artículo empieza sin enlaces
for title, links in zip(df["title"], df["links"]):  # zip recorre cada título junto con los títulos que cita
    for target in str(links).split("|"):  # split separa los títulos citados
        target = target.strip()  # strip quita los espacios
        if target in title_set and target != title:  # solo enlaces dentro del conjunto y nunca a sí mismo
            links_out[title].add(target)  # add guarda el enlace con dirección

neighbours = {}  # sin dirección, para lo demás
for t in titles:  # recorremos cada título
    neighbours[t] = set()  # cada artículo empieza sin vecinos
for a, targets in links_out.items():  # items recorre cada artículo y los que cita
    for b in targets:  # recorremos cada artículo citado
        neighbours[a].add(b)  # add pone a b entre los vecinos de a
        neighbours[b].add(a)  # add pone a a entre los vecinos de b
n_directed = 0  # aquí contamos los enlaces con dirección
for targets in links_out.values():  # recorremos lo que cita cada artículo
    n_directed += len(targets)  # len suma sus enlaces
n_undirected = 0  # aquí contamos los vecinos de todos los artículos
for nbrs in neighbours.values():  # recorremos los vecinos de cada artículo
    n_undirected += len(nbrs)  # len suma sus vecinos
print(f"Enlaces con dirección: {n_directed}. Sin dirección: {n_undirected // 2}")  # cada enlace sin dirección se contó dos veces
```

### Paso 2. Los dos grafos
En este paso pasamos los diccionarios a networkx.
`directed` va con dirección y `graph` sin dirección.
Contamos los aislados y los componentes.

```python
directed = nx.DiGraph()  # DiGraph arma un grafo con dirección
directed.add_nodes_from(titles)  # add_nodes_from pone un nodo por título, en el orden de titles
for u in titles:  # recorremos cada artículo en orden
    for v in sorted(links_out[u]):  # sorted deja los citados en orden, para que el grafo no cambie de una sesión a otra
        directed.add_edge(u, v)  # add_edge pone el enlace de u a v

graph = nx.Graph()  # Graph arma un grafo sin dirección
graph.add_nodes_from(titles)  # add_nodes_from pone un nodo por título, en el orden de titles
for u in titles:  # recorremos cada artículo en orden
    for v in sorted(neighbours[u]):  # sorted deja los vecinos en orden, para que Louvain se repita igual
        graph.add_edge(u, v)  # add_edge pone el enlace una sola vez, aunque lo veamos dos veces

components = sorted(nx.connected_components(graph), key=len, reverse=True)  # connected_components da los componentes y sorted los ordena del mayor al menor
isolated_count = 0  # aquí contamos los aislados
for v in graph:  # recorremos cada nodo
    if graph.degree(v) == 0:  # degree en 0 quiere decir que no tiene enlaces
        isolated_count += 1  # sumamos un aislado
n_components = 0  # aquí contamos los componentes con más de un artículo
for c in components:  # recorremos cada componente
    if len(c) > 1:  # dejamos fuera los aislados
        n_components += 1  # sumamos un componente
print(f"Nodos {graph.number_of_nodes()}, enlaces {graph.number_of_edges()}, aislados {isolated_count} ({isolated_count / N:.0%})")  # print muestra el tamaño del grafo
print(f"Componentes con más de un artículo: {n_components}. El mayor tiene {len(components[0])} ({len(components[0]) / N:.0%})")  # print muestra los componentes
```

**Comprobar:**

Comprobamos que hay un nodo por artículo en los dos grafos.

```python
assert graph.number_of_nodes() == N == len(titles)  # un nodo por artículo
assert directed.number_of_edges() >= graph.number_of_edges()  # el grafo con dirección tiene al menos los mismos enlaces
print("Grafos: OK")  # print confirma la comprobación
```

**Lo que vemos.** El 38% de los artículos está aislado.
El conjunto viene de una búsqueda por tema, así que no es un error.
El grafo no dice nada de ellos.

## Parte 4. Modelado

### M1. El grado, dentro de PageRank
En este paso contamos el **grado** de cada artículo y su parte del total posible.
El grado no es un método aparte en esta lección.
Sirve para leer PageRank: un enlace no pesa lo mismo si viene de un nodo muy enlazado o de uno poco enlazado.
Un artículo enlazado con al menos el 10% de los otros es una **alerta**.
Con 318 artículos, `hub_threshold` pide 32 enlaces.

```python
n = len(neighbours)  # len cuenta los nodos
degree = {}  # aquí guardamos el grado de cada artículo
degree_share = {}  # aquí guardamos la parte de los otros con la que se enlaza
isolated = []  # aquí guardamos los artículos sin enlaces
hubs = []  # aquí guardamos los nodos centrales, las alertas
for v in neighbours:  # recorremos cada artículo
    degree[v] = len(neighbours[v])  # len cuenta sus vecinos, que es el grado
    degree_share[v] = degree[v] / (n - 1)  # dividimos por los n - 1 otros artículos
    if degree[v] == 0:  # sin vecinos quiere decir aislado
        isolated.append(v)  # append guarda el aislado
    if degree[v] >= hub_threshold(n):  # hub_threshold da el umbral de la alerta
        hubs.append(v)  # append guarda el nodo central

top_degree = sorted(degree, key=degree.get, reverse=True)[:10]  # sorted ordena por grado de mayor a menor y nos quedamos con 10
print(f"Alerta desde {hub_threshold(n)} enlaces. Nodos centrales: {len(hubs)}")  # print muestra el umbral y las alertas
for v in top_degree:  # recorremos los 10 de más grado
    print(f"  grado {degree[v]:3d} ({degree_share[v]:.0%})  {v[:80]}")  # print muestra el grado, la parte y el título
```

```python
fig, ax = plt.subplots(figsize=(6, 3.5))  # subplots abre la figura
ax.hist(list(degree.values()), bins=range(0, max(degree.values()) + 2), color="#4C72B0")  # hist dibuja cuántos artículos tienen cada grado
ax.axvline(hub_threshold(n), color="#C44E52", linestyle="--", label=f"alerta ({hub_threshold(n)} enlaces)")  # axvline marca el umbral de la alerta
ax.set_xlabel("Grado")  # set_xlabel nombra el eje del grado
ax.set_ylabel("Artículos")  # set_ylabel nombra el eje de los artículos
ax.set_title("Grado de los artículos de nutrición")  # set_title pone el título
ax.legend()  # legend muestra la línea de la alerta
fig.tight_layout()  # tight_layout acomoda los márgenes
fig.savefig(OUTPUTS_DIR / "grado_l5.png", dpi=120)  # savefig guarda la figura
plt.show()  # show muestra la figura
```

**Comprobar:**

Comprobamos el número de aislados y que la alerta de nodo central sigue su regla.

```python
assert len(isolated) == isolated_count  # los aislados coinciden con los de la Parte 3
assert (max(degree_share.values()) < HUB_SHARE) == (len(hubs) == 0)  # no hay alerta solo si nadie llega al 10%
print(f"Grado: OK ({len(hubs)} nodos centrales, el más enlazado tiene {max(degree_share.values()):.0%})")  # print confirma la comprobación
```

**Lo que vemos.** El más enlazado tiene 25 enlaces y no llega a la alerta.
Arriba están los estudios de carga global, que todos usan de referencia.

### M1. PageRank a mano
En este paso calculamos PageRank a mano, con el código de las diapositivas (Page et al., 1998, en la [copia archivada del informe](https://web.archive.org/web/20241231011600/http://ilpubs.stanford.edu:8090/422/)).
Un artículo sube si lo citan artículos que a su vez tienen puntaje alto.
Con probabilidad `DAMPING` el navegante sigue un enlace.
Si no, salta a cualquier artículo.

```python
DAMPING = 0.85  # probabilidad de seguir un enlace


def pagerank(links_out, d=DAMPING, steps=100):
    """PageRank a mano, por iteración de potencias, como en la diapositiva.

    Qué hace: todos empiezan con el mismo puntaje 1/n. En cada vuelta, cada artículo reparte
    su puntaje en partes iguales entre los artículos que cita, con peso d, y todos
    reciben además (1 - d)/n por el salto al azar. Un artículo que no cita a nadie
    reparte entre todos. Después de suficientes vueltas los puntajes dejan de cambiar.

    Entrada:
        links_out: diccionario de cada título al conjunto de títulos que cita.
        d: probabilidad de seguir un enlace, DAMPING = 0.85.
        steps: número de vueltas.

    Salida:
        Un diccionario de cada título a su PageRank. Los puntajes suman 1.
    """
    nodes = list(links_out)  # list guarda los títulos en orden
    n = len(nodes)  # len cuenta los artículos
    rank = {}  # aquí guardamos el puntaje de cada artículo
    for v in nodes:  # recorremos cada artículo
        rank[v] = 1 / n  # todos empiezan con el mismo puntaje
    for _ in range(steps):  # repetimos steps vueltas
        new = {}  # aquí armamos los puntajes de esta vuelta
        for v in nodes:  # recorremos cada artículo
            new[v] = (1 - d) / n  # cada uno recibe su parte del salto al azar
        for u in nodes:  # recorremos cada artículo que reparte
            targets = links_out[u] or nodes  # sin enlaces, salta a cualquiera
            for v in targets:  # recorremos cada artículo que recibe
                new[v] += d * rank[u] / len(targets)  # u reparte su puntaje en partes iguales
        rank = new  # los puntajes nuevos reemplazan a los viejos
    return rank  # devolvemos el puntaje final


rank = pagerank(links_out)  # pagerank calcula el puntaje a mano
hand_rank = rank  # guardamos el cálculo a mano para compararlo con networkx
print(f"Suma de los puntajes: {sum(rank.values()):.6f}")  # sum suma los puntajes, que deben dar 1
```

### M1. El sumidero de puntaje
En este paso vemos por qué hace falta el salto al azar.
Un **sumidero** es un grupo de nodos que se enlazan entre ellos y no enlazan a nadie más.
El puntaje entra y no sale.
En el grafo de juguete A cita a B, y B y C se citan entre ellos.

```python
sink = {"A": {"B"}, "B": {"C"}, "C": {"B"}}  # A cita a B, y B y C se citan entre ellos
for d in (1.0, DAMPING):  # probamos sin salto y con el salto de la lección
    toy_rank = pagerank(sink, d=d)  # pagerank calcula el puntaje del grafo de juguete
    print(f"d = {d}: A {toy_rank['A']:.3f}, B y C juntos {toy_rank['B'] + toy_rank['C']:.3f}")  # print muestra el puntaje de A y del sumidero
```

**Lo que vemos.** Sin salto (d = 1) B y C se quedan con todo y A queda en 0.
Con el salto A conserva su parte del azar, 0,15 / 3 = 0,05.

### M1. PageRank con networkx
En este paso usamos `networkx.pagerank` y lo comparamos con el cálculo a mano.
Ponemos los 10 primeros por PageRank junto a los 10 primeros por grado.

```python
rank = nx.pagerank(directed, alpha=DAMPING)  # nx.pagerank calcula PageRank sobre el grafo con dirección
top_rank = sorted(rank, key=rank.get, reverse=True)[:10]  # sorted ordena por PageRank y nos quedamos con 10
not_by_degree = []  # aquí guardamos los de PageRank alto que no están entre los 10 de más grado
for v in top_rank:  # recorremos los 10 primeros por PageRank
    if v not in top_degree:  # no está entre los 10 de más grado
        not_by_degree.append(v)  # append lo guarda

diff = 0.0  # aquí guardamos la diferencia más grande
for v in rank:  # recorremos cada artículo
    diff = max(diff, abs(rank[v] - hand_rank[v]))  # max se queda con la diferencia más grande
print(f"Diferencia más grande con el cálculo a mano: {diff:.1e}")  # print muestra la diferencia
print(f"El primero tiene {rank[top_rank[0]]:.3f}, {rank[top_rank[0]] * N:.1f} veces el puntaje uniforme 1/{N}")  # print compara el primero con el puntaje uniforme
for v in top_rank:  # recorremos los 10 primeros por PageRank
    mark = "" if v in top_degree else "  <- no está entre los 10 de más grado"  # marcamos los que el grado no pone arriba
    print(f"  PageRank {rank[v]:.3f}, grado {degree[v]:3d}  {v[:70]}{mark}")  # print muestra PageRank, grado y título
```

**Comprobar:**

Comprobamos que PageRank suma 1 y que el cálculo a mano coincide con networkx.

```python
assert abs(sum(rank.values()) - 1) < 1e-6  # los puntajes suman 1
assert diff < 1e-3  # el cálculo a mano coincide con networkx
print(f"PageRank: OK ({len(top_rank) - len(not_by_degree)} de los 10 primeros también están entre los 10 de más grado)")  # print confirma la comprobación
```

**Lo que vemos.** PageRank premia que te cite alguien importante.
"Obesity in children and young people" tiene grado 6 y está entre los 3 primeros.

### M1. Los artículos con PageRank alto
En este paso marcamos los artículos con **PageRank alto**.
Tienen enlaces, están en el cuarto superior por PageRank entre los artículos con enlaces y no son un nodo central.
Redondeamos PageRank a 6 decimales, el mismo valor que guarda `grafo_l5.csv`.

```python
score = {}  # aquí guardamos PageRank redondeado, el valor que se guarda en grafo_l5.csv
for v in rank:  # recorremos cada artículo
    score[v] = round(rank[v], 6)  # round deja 6 decimales
connected = []  # aquí guardamos los artículos con enlaces
for v in graph:  # recorremos cada nodo
    if degree[v] > 0:  # tiene al menos un enlace
        connected.append(v)  # append lo guarda
connected_scores = []  # aquí guardamos el PageRank de los artículos con enlaces
for v in connected:  # recorremos los artículos con enlaces
    connected_scores.append(score[v])  # append guarda su PageRank redondeado
cut = sorted(connected_scores)[int(0.75 * len(connected))]  # sorted ordena los puntajes y tomamos el corte del cuarto superior
high_rank = []  # aquí guardamos los artículos con PageRank alto
for v in connected:  # recorremos los artículos con enlaces
    if score[v] >= cut and v not in hubs:  # en el cuarto superior y sin ser nodo central
        high_rank.append(v)  # append lo guarda
print(f"Artículos con enlaces: {len(connected)}. Corte del cuarto superior: {cut:.6f}. Con PageRank alto: {len(high_rank)}")  # print muestra el corte y cuántos pasan
```

**Comprobar:**

Comprobamos que hay artículos con PageRank alto, que son pocos y que ninguno es un nodo central.

```python
assert 0 < len(high_rank) <= len(connected) - int(0.75 * len(connected))  # hay algunos, y no más que el cuarto superior
assert not set(high_rank) & set(hubs)  # ninguno es nodo central
print(f"PageRank alto: OK ({len(high_rank)})")  # print confirma la comprobación
```

### M2. Caminos más cortos e intermediación
En este paso medimos la **intermediación** (Freeman, 1977).
Un artículo tiene intermediación alta si queda en muchos caminos más cortos entre otros.
No es lo mismo que el grado: puede unir dos grupos sin tener muchos enlaces.
Usamos el grafo sin dirección.
Primero repetimos la búsqueda por niveles desde el primero por PageRank.

```python
def distances_from(source, neighbours):
    """Búsqueda en anchura: cuántos pasos hay desde source hasta cada nodo alcanzable.

    Qué hace: visita primero a los vecinos de source, después a los vecinos de esos vecinos,
    y así, con una cola. Cada nodo se visita una sola vez, la primera vez que se
    encuentra, y esa es su distancia más corta. Los nodos que no se alcanzan no
    aparecen en el resultado.

    Entrada:
        source: el nodo de partida.
        neighbours: diccionario de cada nodo a su conjunto de vecinos, sin dirección.

    Salida:
        Un diccionario de cada nodo alcanzable a su número de pasos desde source.
    """
    dist = {source: 0}  # source está a 0 pasos de sí mismo
    queue = deque([source])  # la cola empieza con source
    while queue:  # seguimos mientras queden nodos en la cola
        u = queue.popleft()  # popleft saca el primer nodo de la cola
        for v in neighbours[u]:  # recorremos sus vecinos
            if v not in dist:  # solo los que todavía no visitamos
                dist[v] = dist[u] + 1  # el vecino queda a un paso más que u
                queue.append(v)  # append pone al vecino al final de la cola
    return dist  # devolvemos los pasos hasta cada nodo alcanzable


first = top_rank[0]  # el primero por PageRank
reach = distances_from(first, neighbours)  # distances_from cuenta los pasos desde ese artículo
print(f"Desde el primero por PageRank se alcanzan {len(reach) - 1} artículos. El más lejano está a {max(reach.values())} pasos")  # print muestra cuántos se alcanzan y el más lejano
```

**Lo que vemos.** Se llega a los otros 147 del componente mayor, en 5 pasos como máximo.
Los otros 170 no se alcanzan.

### M2. Intermediación con networkx
En este paso calculamos la intermediación de cada artículo con `nx.betweenness_centrality`.
Listamos los 10 primeros y los comparamos con los 10 de más grado.
Un artículo de intermediación alta que no está entre los 10 de más grado une grupos que el grado no pone arriba.

```python
betweenness = nx.betweenness_centrality(graph)  # betweenness_centrality mide en cuántos caminos más cortos queda cada artículo
top_betweenness = sorted(betweenness, key=betweenness.get, reverse=True)[:10]  # sorted ordena por intermediación y nos quedamos con 10
not_by_degree_b = []  # aquí guardamos los de intermediación alta que no están entre los 10 de más grado
for v in top_betweenness:  # recorremos los 10 primeros por intermediación
    if v not in top_degree:  # no está entre los 10 de más grado
        not_by_degree_b.append(v)  # append lo guarda
print(f"El primero tiene intermediación {betweenness[top_betweenness[0]]:.4f}")  # print muestra el valor más alto
for v in top_betweenness:  # recorremos los 10 primeros
    mark = "" if v in top_degree else "  <- no está entre los 10 de más grado"  # marcamos los que el grado no pone arriba
    print(f"  intermediación {betweenness[v]:.4f}, grado {degree[v]:3d}  {v[:70]}{mark}")  # print muestra intermediación, grado y título
print(f"De los 10 primeros por intermediación, {len(not_by_degree_b)} no están entre los 10 de más grado")  # print cuenta los que el grado no destaca
```

**Comprobar:**

Comprobamos que hay un valor por artículo y que la intermediación queda entre 0 y 1.

```python
assert len(betweenness) == N  # un valor por artículo
for v in betweenness:  # recorremos cada artículo
    assert 0 <= betweenness[v] <= 1, v  # la intermediación es una proporción de caminos
print("Intermediación: OK")  # print confirma la comprobación
```

**Lo que vemos.** El primero coincide con el de más grado (0,0361, grado 25).
Otros no: "Defining and Setting National Goals for Cardiovascular Health Promotion and Disease Reduction" tiene intermediación 0,0221 y grado 11, y no está entre los 10 de más grado.
La guía de ejemplo también queda entre los 10 de más intermediación, con grado 10.

### M3. Comunidades de Louvain
En este paso agrupamos los artículos con Louvain (Blondel et al., 2008).
Una comunidad tiene más enlaces por dentro que los que habría al azar.
La **modularidad** resume esa diferencia: más cerca de 1, más nítidos los grupos.
Usamos el grafo sin dirección y `nx.community.louvain_communities` con `seed=SEED`, para que el resultado se repita.
Los aislados quedan cada uno en su propia comunidad de tamaño 1.

```python
def community_key(comm):
    """Clave para ordenar comunidades: primero las más grandes, luego por título.

    Entrada:
        comm: un conjunto de títulos que forman una comunidad.

    Salida:
        Una tupla con el tamaño, en negativo, y el primer título en orden alfabético.
    """
    return (-len(comm), min(comm))  # min da el primer título, para que el orden no cambie


communities = list(nx.community.louvain_communities(graph, seed=SEED))  # louvain_communities arma las comunidades
communities = sorted(communities, key=community_key)  # sorted deja primero las más grandes
modularity = nx.community.modularity(graph, communities)  # modularity puntúa la partición
community_of = {}  # aquí guardamos el identificador de la comunidad de cada artículo
community_size = {}  # aquí guardamos el tamaño de la comunidad de cada artículo
for i, comm in enumerate(communities):  # enumerate numera las comunidades, de 0 en adelante
    for v in comm:  # recorremos cada artículo de la comunidad
        community_of[v] = i  # el identificador de su comunidad
        community_size[v] = len(comm)  # el tamaño de su comunidad
sizes = []  # aquí guardamos el tamaño de cada comunidad, en el mismo orden
for comm in communities:  # recorremos cada comunidad
    sizes.append(len(comm))  # append guarda su tamaño
n_singletons = 0  # aquí contamos las comunidades de un solo artículo
for s in sizes:  # recorremos cada tamaño
    if s == 1:  # un solo artículo
        n_singletons += 1  # sumamos una comunidad de aislado
print(f"Comunidades: {len(communities)}. Modularidad: {modularity:.3f}")  # print muestra el conteo y la modularidad
print(f"Las más grandes: {sizes[:8]}. Comunidades de un solo artículo: {n_singletons}")  # print muestra los tamaños
```

**Comprobar:**

Comprobamos que cada artículo queda en una comunidad y que la modularidad está en su rango.

```python
assert len(community_of) == N  # un identificador por artículo
assert 0 <= modularity <= 1  # la modularidad de una partición queda entre 0 y 1
print("Louvain: OK")  # print confirma la comprobación
```

**Lo que vemos.** Hay 152 comunidades y la modularidad es 0,590.
Las más grandes tienen 40, 33, 22 y 16 artículos.
122 comunidades son un artículo aislado, los mismos 122 aislados de la Parte 3.
La partición tiene sentido sobre los que sí tienen enlaces.

### M3. Una lectura de dos comunidades
En este paso leemos la comunidad más grande y la segunda.
Imprimimos unos títulos de cada una, los de más grado.

```python
for i in (0, 1):  # recorremos las dos comunidades más grandes
    members = list(communities[i])  # list guarda los títulos de la comunidad
    members = sorted(members, key=degree.get, reverse=True)  # sorted deja primero los de más grado
    print(f"Comunidad {i}: {len(communities[i])} artículos")  # print muestra el tamaño
    for t in members[:6]:  # recorremos los 6 de más grado
        print(f"  grado {degree[t]:3d}  {t[:80]}")  # print muestra el grado y el título
```

**Lo que vemos.** La comunidad 0 (40 artículos) junta los estudios de carga global de la enfermedad.
La comunidad 1 (33 artículos) junta guías clínicas de corazón y de accidente cerebrovascular.
El artículo de ejemplo está en la comunidad 1.

---

## Parte 5. Evaluación

Aquí no hay marcas ni ganador.
Miramos qué dicen PageRank, la intermediación y Louvain que los otros no dicen.

### Paso 1. PageRank e intermediación contra las citas
En este paso comparamos el orden por PageRank, por grado y por intermediación con el grado de entrada y con las citas en el mundo (`cited_by_count`).
Usamos la correlación de rangos de Spearman.

```python
cites = dict(zip(titles, pd.to_numeric(papers["cited_by_count"], errors="coerce").fillna(0)))  # to_numeric lee las citas y fillna deja en 0 las que faltan
in_degree = dict(directed.in_degree())  # in_degree cuenta cuántos artículos del conjunto citan a cada uno
pr = []  # aquí guardamos PageRank en el orden de titles
deg = []  # aquí guardamos el grado en el mismo orden
in_deg = []  # aquí guardamos el grado de entrada en el mismo orden
cites_list = []  # aquí guardamos las citas en el mismo orden
bet_list = []  # aquí guardamos la intermediación en el mismo orden
for t in titles:  # recorremos cada título
    pr.append(rank[t])  # append guarda su PageRank
    deg.append(degree[t])  # append guarda su grado
    in_deg.append(in_degree[t])  # append guarda su grado de entrada
    cites_list.append(cites[t])  # append guarda sus citas
    bet_list.append(betweenness[t])  # append guarda su intermediación
rho_degree = spearmanr(pr, deg)[0]  # spearmanr compara el orden por PageRank con el orden por grado
rho_in = spearmanr(pr, in_deg)[0]  # spearmanr compara PageRank con el grado de entrada
rho_cites = spearmanr(pr, cites_list)[0]  # spearmanr compara PageRank con las citas
rho_bet_degree = spearmanr(bet_list, deg)[0]  # spearmanr compara la intermediación con el grado
rho_bet_pr = spearmanr(bet_list, pr)[0]  # spearmanr compara la intermediación con PageRank
rho_bet_cites = spearmanr(bet_list, cites_list)[0]  # spearmanr compara la intermediación con las citas
print(f"Spearman de PageRank con el grado {rho_degree:.2f}, con el grado de entrada {rho_in:.2f}, con las citas {rho_cites:.2f}")  # print muestra las tres correlaciones
print(f"Spearman de la intermediación con el grado {rho_bet_degree:.2f}, con PageRank {rho_bet_pr:.2f}, con las citas {rho_bet_cites:.2f}")  # print muestra las tres correlaciones de la intermediación
```

**Lo que vemos.** PageRank sigue al grado de entrada (0,97), menos al grado (0,75) y poco a las citas (0,30).
La intermediación sigue más al grado (0,86) que a PageRank (0,66) y también poco a las citas (0,30).
El grafo mide el lugar dentro de lo que el equipo va a leer.

### Paso 2. Un artículo descrito por su lugar
En este paso describimos un artículo por su lugar.
Damos sus puestos por grado, PageRank, intermediación y citas, y su comunidad.
Es una guía clínica elegida antes de ver la lista final.

```python
def place_of(score):
    """Puesto de cada artículo según un puntaje, de mayor a menor.

    Qué hace: el artículo con el puntaje más alto tiene el puesto 1. Sirve para comparar
    medidas con escalas distintas (grado, PageRank, intermediación, citas) en una misma
    línea. Los empates quedan en el orden de titles.

    Entrada:
        score: diccionario de cada título a su puntaje.

    Salida:
        Un diccionario de cada título a su puesto, de 1 a N.
    """
    order = sorted(titles, key=score.get, reverse=True)  # sorted ordena los títulos de mayor a menor puntaje
    places = {}  # aquí guardamos el puesto de cada título
    for i, t in enumerate(order):  # enumerate da la posición de cada título, desde 0
        places[t] = i + 1  # el puesto empieza en 1
    return places  # devolvemos los puestos


by_degree = place_of(degree)  # place_of da el puesto por grado
by_rank = place_of(rank)  # place_of da el puesto por PageRank
by_betweenness = place_of(betweenness)  # place_of da el puesto por intermediación
by_cites = place_of(cites)  # place_of da el puesto por citas
print(EXAMPLE)  # print muestra el título del ejemplo
print(f"  grado {degree[EXAMPLE]}, puesto {by_degree[EXAMPLE]} por grado, puesto {by_rank[EXAMPLE]} por PageRank, puesto {by_betweenness[EXAMPLE]} por intermediación, puesto {by_cites[EXAMPLE]} de {N} por citas ({int(cites[EXAMPLE]):,})")  # print muestra sus puestos
print(f"  PageRank alto: {'sí' if EXAMPLE in high_rank else 'no'}. Comunidad {community_of[EXAMPLE]} ({community_size[EXAMPLE]} artículos)")  # print dice si tiene PageRank alto y su comunidad
```

**Comprobar:**

Comprobamos que el artículo de ejemplo tiene PageRank alto y que sube por PageRank frente a las citas.

```python
assert EXAMPLE in high_rank  # el ejemplo tiene PageRank alto
assert by_rank[EXAMPLE] < by_cites[EXAMPLE]  # sube por PageRank frente a las citas
print("Artículo descrito por su lugar: OK")  # print confirma la comprobación
```

**Lo que vemos.** La guía tiene grado 10.
Está en el puesto 48 por PageRank, en el 10 por intermediación y en el 187 por citas: dentro del conjunto pesa más que en el mundo, y queda en más caminos más cortos que lo que sugiere su grado.
Pertenece a la comunidad 1, la de las guías clínicas.
Recibe el resultado del grafo.

### Paso 3. Intermediación frente al grado
En este paso dibujamos la intermediación contra el grado.
Los 10 de más intermediación que no están entre los 10 de más grado van en otro color.
Así se ven los artículos que unen grupos sin ser los más enlazados.

```python
fig, ax = plt.subplots(figsize=(6, 4))  # subplots abre la figura
x_vals = []  # aquí guardamos el grado de cada artículo
y_vals = []  # aquí guardamos la intermediación de cada artículo
x_mark = []  # el grado de los que unen grupos y no están entre los 10 de más grado
y_mark = []  # su intermediación
for v in titles:  # recorremos cada artículo
    if v in not_by_degree_b:  # es de intermediación alta y no está entre los 10 de más grado
        x_mark.append(degree[v])  # append guarda su grado
        y_mark.append(betweenness[v])  # append guarda su intermediación
    else:  # el resto
        x_vals.append(degree[v])  # append guarda su grado
        y_vals.append(betweenness[v])  # append guarda su intermediación
ax.scatter(x_vals, y_vals, s=18, color="#4C72B0", alpha=0.7, label="los demás")  # scatter dibuja el resto
ax.scatter(x_mark, y_mark, s=36, color="#C44E52", label="alta intermediación, no entre los 10 de más grado")  # scatter marca los que unen grupos
ax.set_xlabel("Grado")  # set_xlabel nombra el eje del grado
ax.set_ylabel("Intermediación")  # set_ylabel nombra el eje de la intermediación
ax.set_title("Intermediación frente al grado")  # set_title pone el título
ax.legend()  # legend muestra las dos series
fig.tight_layout()  # tight_layout acomoda los márgenes
fig.savefig(OUTPUTS_DIR / "intermediacion_grado_l5.png", dpi=120)  # savefig guarda la figura
plt.show()  # show muestra la figura
```

**Lo que leemos.** Varios artículos de intermediación alta no están entre los de más grado.
PageRank y el grado no alcanzan para verlos.

### Paso 4. Un dibujo del componente mayor, por comunidad
En este paso dibujamos el componente mayor.
El tamaño es el grado y el color es la comunidad de Louvain.
La posición cambia con la semilla del dibujo.

```python
largest = max(nx.connected_components(graph), key=len)  # max se queda con el componente de más artículos
# Nodos y aristas en orden: vienen de sets, y sin orden el dibujo cambia de una ejecución a otra
sub = nx.Graph()  # Graph arma el grafo del dibujo
sub.add_nodes_from(sorted(largest))  # add_nodes_from pone los nodos del componente mayor en orden
edges = []  # aquí guardamos los enlaces en orden
for e in graph.subgraph(largest).edges():  # subgraph deja solo los enlaces del componente mayor
    edges.append(tuple(sorted(e)))  # sorted ordena los dos extremos de cada enlace
sub.add_edges_from(sorted(edges))  # add_edges_from pone los enlaces en orden
pos = nx.spring_layout(sub, seed=SEED)  # spring_layout calcula la posición de cada nodo
sizes = []  # aquí guardamos el tamaño de cada nodo
colours = []  # aquí guardamos el color de cada nodo
for v in sub:  # recorremos cada nodo del dibujo
    sizes.append(20 + 8 * degree[v])  # el tamaño crece con el grado
    colours.append(community_of[v])  # el color es la comunidad
fig, ax = plt.subplots(figsize=(7, 6))  # subplots abre la figura
nx.draw_networkx_edges(sub, pos, ax=ax, alpha=0.3)  # draw_networkx_edges dibuja los enlaces
nodes_drawn = nx.draw_networkx_nodes(sub, pos, ax=ax, node_size=sizes, node_color=colours, cmap="tab20")  # draw_networkx_nodes dibuja los nodos
fig.colorbar(nodes_drawn, ax=ax, label="Comunidad")  # colorbar muestra la escala de las comunidades
ax.set_title(f"Componente mayor ({len(largest)} artículos). Color: comunidad de Louvain")  # set_title pone el título
ax.axis("off")  # axis("off") quita los ejes
fig.tight_layout()  # tight_layout acomoda los márgenes
fig.savefig(OUTPUTS_DIR / "comunidades_l5.png", dpi=120)  # savefig guarda la figura
plt.show()  # show muestra la figura
```

**Lo que leemos.** El dibujo es el componente mayor.
Los colores agrupan artículos que se citan más entre ellos que con el resto.

---

## Parte 6. Despliegue

### Paso 1. La lista del grafo
En este paso armamos una fila por título.
`graph_support` es el PageRank alto de la Parte 4: enlaces, cuarto superior entre esos artículos, y no es un nodo central.
La lista guarda como máximo 30 de esos artículos, los de PageRank más alto.
La intermediación y la comunidad se guardan en el archivo, para leerlas, y no deciden quién entra en esta lista.

```python
table = pd.DataFrame(index=pd.Index(titles, name="title"))  # DataFrame arma una fila por título
table["graph_support"] = table.index.isin(high_rank)  # isin marca los artículos con PageRank alto
by_rank_series = pd.Series(rank).loc[high_rank].sort_values(ascending=False)  # sort_values ordena los de PageRank alto de mayor a menor
kept = by_rank_series.head(MAX_PAPERS).index  # head se queda con los MAX_PAPERS primeros
table["en_lista"] = table.index.isin(kept)  # isin marca los que entran en la lista
print(f"PageRank alto: {int(table['graph_support'].sum())}. En la lista: {int(table['en_lista'].sum())}.")  # print muestra los dos conteos
```

**Comprobar:**

Comprobamos que hay una fila por artículo y que la lista no pasa de 30.

```python
assert len(table) == N and table.index.is_unique  # una fila por artículo, sin repetidos
assert table["graph_support"].sum() == len(high_rank) and table["en_lista"].sum() == min(MAX_PAPERS, len(high_rank))  # los conteos coinciden con la Parte 4
assert set(table.index[table["en_lista"]]) <= set(high_rank)  # la lista sale solo del PageRank alto
print("Lista del grafo: OK")  # print confirma la comprobación
```

Los artículos con PageRank alto son el resultado que usa la lista de esta lección.
Un aislado no entra.
Un nodo central tampoco entra: es una alerta, no un lugar en la lista.

### Paso 2. Guardar el grafo
En este paso guardamos `outputs/grafo_l5.csv`.
El archivo deja el grado, PageRank, la intermediación, la comunidad y la modularidad de la partición.

```python
grado = []  # aquí guardamos el grado de cada título
pagerank_values = []  # aquí guardamos PageRank redondeado
intermediacion = []  # aquí guardamos la intermediación redondeada
comunidad = []  # aquí guardamos el identificador de la comunidad
tamano = []  # aquí guardamos el tamaño de la comunidad
modularidad = []  # aquí guardamos la modularidad, la misma en todas las filas
aislado = []  # aquí guardamos si el artículo está aislado
alerta_centro = []  # aquí guardamos si es nodo central
for t in titles:  # recorremos cada título en orden
    grado.append(degree[t])  # append guarda su grado
    pagerank_values.append(round(rank[t], 6))  # round deja PageRank con 6 decimales
    intermediacion.append(round(betweenness[t], 6))  # round deja la intermediación con 6 decimales
    comunidad.append(community_of[t])  # append guarda su comunidad
    tamano.append(community_size[t])  # append guarda el tamaño de su comunidad
    modularidad.append(round(modularity, 4))  # round deja la modularidad con 4 decimales
    aislado.append(degree[t] == 0)  # grado 0 quiere decir aislado
    alerta_centro.append(t in hubs)  # está entre los nodos centrales
graph_table = pd.DataFrame({  # DataFrame arma la tabla del grafo, una fila por título
    "title": titles,  # el título
    "grado": grado,  # el grado
    "pagerank": pagerank_values,  # PageRank redondeado
    "intermediacion": intermediacion,  # la intermediación
    "comunidad": comunidad,  # el identificador de la comunidad
    "tamano_comunidad": tamano,  # el tamaño de la comunidad
    "modularidad": modularidad,  # la modularidad de la partición
    "aislado": aislado,  # sin enlaces
    "alerta_centro": alerta_centro,  # nodo central, una alerta
    "graph_support": table.loc[titles, "graph_support"].to_numpy(),  # PageRank alto
    "en_lista": table.loc[titles, "en_lista"].to_numpy(),  # en la lista de esta lección
})
graph_path = OUTPUTS_DIR / "grafo_l5.csv"  # Path fija la ruta del archivo del grafo
graph_table.to_csv(graph_path, index=False)  # to_csv escribe la tabla y deja fuera el índice
print(f"Guardado: {graph_path} ({len(graph_table)} filas)")  # print confirma dónde quedó
```

**Comprobar:**

Comprobamos que el archivo guardado tiene sus columnas y una fila por artículo.

```python
saved = pd.read_csv(graph_path, keep_default_na=False)  # read_csv vuelve a leer el archivo guardado
assert {"title", "grado", "pagerank", "intermediacion", "comunidad", "tamano_comunidad", "modularidad", "aislado", "alerta_centro", "graph_support", "en_lista"} <= set(saved.columns)  # están todas las columnas
assert len(saved) == N  # una fila por artículo
print("grafo_l5.csv: OK")  # print confirma la comprobación
```

### Paso 3. Qué cambiaría la decisión
En este paso escribimos cómo entra el grafo y qué lo cambiaría.

| Qué | Respuesta |
|-----|-----------|
| Cómo entra | El resultado cuenta a favor si el artículo está en el cuarto superior por PageRank entre los que tienen enlaces, y no es un nodo central |
| Cómo se lee | El grafo solo ve las citas dentro del conjunto. Un artículo aislado no tiene lugar. No es un artículo malo. La intermediación y la comunidad se leen en el archivo, y no deciden esta lista |
| Qué lo cambia | Otro corte que el cuarto superior. Otra regla para los nodos centrales. Más artículos o más enlaces. Usar la intermediación o la comunidad para decidir la lista |

### Paso 4. Comprobación final
En este paso revisamos que el cuaderno guardó el grafo y las figuras.

```python
def _check_ok(name, check):
    """Ejecuta una comprobación sin detener el cuaderno: un error cuenta como incompleto.

    Salida:
        True si la comprobación pasó, False si no.
    """
    try:  # intentamos la comprobación
        ok = bool(check())  # check devuelve True si pasó
    except Exception:  # cualquier error cuenta como incompleto
        ok = False  # la comprobación no pasó
    print(f"{name}: {'OK' if ok else 'incompleto'}")  # print muestra el resultado
    return ok  # devolvemos si pasó


def graph_saved():
    """Dice si el archivo del grafo quedó guardado."""
    return graph_path.is_file()  # is_file dice si el archivo existe


def figures_saved():
    """Dice si las tres figuras de la lección quedaron guardadas."""
    for name in ["grado_l5.png", "intermediacion_grado_l5.png", "comunidades_l5.png"]:  # recorremos las tres figuras
        if not (OUTPUTS_DIR / name).is_file():  # is_file dice si la figura existe
            return False  # falta una figura
    return True  # están las tres


checks = [  # cada comprobación tiene un nombre y una función
    ("outputs/grafo_l5.csv", graph_saved),  # el archivo del grafo
    ("Histograma de grado, intermediación y comunidades", figures_saved),  # las tres figuras
]
passed = 0  # aquí contamos las comprobaciones que pasan
for name, check in checks:  # recorremos cada comprobación
    passed += _check_ok(name, check)  # _check_ok suma 1 si pasó
print(f"\nL5_CHECKS={passed}/{len(checks)}")  # print muestra cuántas pasaron
if passed == len(checks):  # pasaron todas
    print("L5_OK")  # print confirma el cuaderno
```

<!-- end NOTEBOOK: -->
