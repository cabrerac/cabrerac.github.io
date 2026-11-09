<!-- NOTEBOOK: -->

## Repaso de Python para este cuaderno

Este cuaderno utiliza los siguientes métodos de Python. Si ya los conoce, ejecute estas celdas rápido.

### Un grafo como diccionario de conjuntos
Cada nodo es una clave y su valor es el conjunto de nodos con los que tiene un enlace. Sin dirección, el enlace va en los dos lados. El **grado** es el tamaño del conjunto.

```python
toy = {"A": set(), "B": set(), "C": set(), "D": set(), "E": set()}
for a, b in [("A", "B"), ("A", "C"), ("B", "C"), ("C", "D")]:
    toy[a].add(b)
    toy[b].add(a)
print({v: sorted(n) for v, n in toy.items()})
print("Grado de cada nodo:", {v: len(n) for v, n in toy.items()})
```

### Búsqueda por niveles a mano
La búsqueda en anchura visita primero a los vecinos, después a los vecinos de los vecinos, y cuenta los pasos. La cola guarda los nodos que faltan, en orden.

```python
from collections import deque

steps = {"A": 0}
queue = deque(["A"])
while queue:
    u = queue.popleft()
    for v in sorted(toy[u]):
        if v not in steps:
            steps[v] = steps[u] + 1
            queue.append(v)
assert steps == {"A": 0, "B": 1, "C": 1, "D": 2}
print(f"Pasos desde A: {steps}. E no se alcanza. Repaso de Python: OK")
```

**Lo que vemos.** D está a dos pasos de A porque hay que pasar por C. La Parte 4 usa esta búsqueda al margen de los tres métodos.

---

## Instrucciones

Seguimos con el equipo interno de la secretaría de salud y sus 320 artículos sobre nutrición. El equipo debe decidir **qué artículos tiene que leer** un colega que llega al equipo. Con los tres resultados de las Lecciones 2 a 4, 52 artículos quedaron en vista.

Los artículos se citan entre ellos. Los índices de citas guardaron esos enlaces para las bibliotecas, y la web los volvió a usar entre páginas. Page et al. (1998) propusieron que un enlace desde una página importante pese más. Hoy describimos un artículo por su **lugar entre los demás**. Un artículo enlazado con muchos es una **alerta**, porque puede ser una revisión que todos citan. Un artículo **citado por artículos importantes** puede ser el que el colega necesita.

**Tres métodos, tres preparaciones.**

| Método | Pregunta | Preparación que necesita |
|--------|----------|--------------------------|
| M1. Grado | ¿Con cuántos se enlaza? | Una lista de enlaces dentro del conjunto, sin dirección |
| M2. PageRank | ¿Lo citan artículos que también son citados? | La misma lista con dirección, un grafo dirigido |
| M3. node2vec | ¿Quiénes están cerca en la red? | El componente mayor y caminatas al azar sobre él |

**Qué hacer.** Ejecute las celdas de arriba hacia abajo. Cada paso empieza con **En este paso** y termina con una celda **Comprobar**.

**Mapa del cuaderno**

| Parte | Fase CRISP-DM | Qué sale |
|-------|---------------|----------|
| 1 | Comprensión del negocio | La pregunta de hoy, los parámetros, los artículos, `pregunta.json` y los tres resultados anteriores |
| 2 | Comprensión de los datos | Los artículos y sus enlaces |
| 3 | Preparación de los datos | La lista de enlaces, los dos grafos y el componente mayor |
| 4 | Modelado | Grado, PageRank y node2vec |
| 5 | Evaluación | Contra las citas, un artículo descrito por su lugar, estabilidad de node2vec |
| 6 | Despliegue | El resultado del grafo en `supports` y `outputs/grafo_l5.csv` |

**Carpetas.** La celda de configuración crea `data/` (datos descargados) y `outputs/` (tablas y gráficos).

---

## Parte 1. Comprensión del negocio

### Paso 1. La pregunta de esta lección
En este paso escribimos qué buscamos hoy. La decisión no cambia: qué artículos debe leer el colega nuevo.

| Pregunta | Respuesta para el laboratorio |
|----------|-------------------------------|
| ¿Qué buscamos? | El lugar de cada artículo en la red de citas dentro de la colección |
| ¿Con qué lo medimos? | Grado, PageRank y node2vec |
| ¿Contra qué lo comparamos? | Contra las citas en el mundo y contra pares de artículos al azar |
| ¿Cómo entra el grafo en la lista? | Un artículo recibe el resultado del grafo si tiene PageRank alto: el cuarto superior entre los artículos con enlaces |

Un nodo central es una alerta. Un artículo aislado no recibe el resultado, pero tampoco sale de la lista.

### Paso 2. Configuración
En este paso importamos las librerías, creamos las carpetas y fijamos los parámetros. La celda instala `gensim` solo si falta. No cambie los parámetros. La excepción es `MIN_SUPPORTS`, que empieza en 2 y se puede cambiar. Cada grupo fija y justifica este número en su proyecto.

```python
import importlib.util
import subprocess
import sys

if importlib.util.find_spec("gensim") is None:
    print("Instalando gensim (una sola vez por sesión)...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "gensim"], check=True)

import json          # leer y escribir pregunta.json
import math          # techo (ceil) para los mínimos
import random        # caminatas de node2vec
import time          # medir cuánto tarda cada paso
from collections import deque   # cola de la búsqueda en anchura
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import requests
from gensim.models import Word2Vec
from scipy.stats import spearmanr

# Carpetas de trabajo
DATA_DIR = Path("data")
OUTPUTS_DIR = Path("outputs")
DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
BASE_URL = "https://cabrerac.github.io/assets/data/26-udenar-data-mining"

# Desde L2, sin cambios
SUPPORT_SHARE = 0.03
SUPPORT_MIN = 5
SEED = 7

# Decisión, L3 en adelante
MIN_SUPPORTS = 2             # el código empieza en 2, cámbielo si lo justifica (0 o 1 también valen)

# L5 (no cambiar)
HUB_SHARE = 0.10          # un nodo enlazado a al menos el 10% de los otros es una alerta
MIN_LINKS = 5             # nunca menos de 5 enlaces para una alerta
DAMPING = 0.85            # PageRank
NODE_DIMENSIONS = 32
WALKS_PER_NODE = 10
WALK_LENGTH = 20
P_RETURN = 1.0
Q_INOUT = 0.5
WINDOW = 5
N2V_SEEDS = (7, 8, 9)     # Word2Vec(workers=1, seed=s), nodos ordenados con sorted(adj)

# Propio de este cuaderno
N_RANDOM_PAIRS = 3000     # pares al azar para comparar con los vecinos de node2vec
EXAMPLE = "Guidelines for the Primary Prevention of Stroke"   # el artículo que describimos por su lugar


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
    return max(min_links, math.ceil(HUB_SHARE * (n - 1)))


print(f"networkx {nx.__version__}. Alerta desde {hub_threshold(318)} enlaces con 318 artículos")
```

### Paso 3. Descargar los artículos
En este paso descargamos los artículos. La columna nueva es `links`, con los títulos que cada artículo cita dentro del conjunto.

```python
def download_data(name: str, folder: Path = DATA_DIR) -> Path:
    """Descarga un archivo de datos del curso, una sola vez.

    Qué hace: si el archivo ya está en la carpeta, lo usa. Si no, lo baja de BASE_URL.

    Entrada:
        name: nombre del archivo. folder: carpeta local, DATA_DIR por defecto.

    Salida:
        La ruta local del archivo.
    """
    dest = folder / name
    if dest.is_file() and dest.stat().st_size > 0:
        print(f"Ya en caché: {dest}")
        return dest
    response = requests.get(f"{BASE_URL}/{name}", timeout=60)
    response.raise_for_status()
    dest.write_bytes(response.content)
    print(f"Descargado: {dest}")
    return dest


raw = pd.read_csv(download_data("nutricion-papers.csv"), keep_default_na=False)
print(f"{len(raw)} filas, columnas: {list(raw.columns)}")
```

### Paso 4. La descripción de la pregunta
En este paso leemos `pregunta.json`, la descripción de la pregunta. Si `pregunta.json` no está, este cuaderno escribe la descripción del laboratorio para que pueda seguir. Lo nuevo es el grafo: un artículo recibe el resultado si **une partes de la red** y no es solo un nodo central.

```python
QUESTION_PATH = Path("pregunta.json")

if QUESTION_PATH.is_file():
    question_card = json.loads(QUESTION_PATH.read_text(encoding="utf-8"))
    print("pregunta.json leído de la Lección 4")
else:
    question_card = {
        "question": "¿Qué artículos de nutrición debe leer el equipo para su tema, y qué filtro los puso en la lista?",
        "standard": {"min_papers": 10, "max_papers": 30, "max_share_citations_only": 0.5},
    }
    QUESTION_PATH.write_text(json.dumps(question_card, ensure_ascii=False, indent=2), encoding="utf-8")
    print("pregunta.json no estaba. Escribimos la descripción del laboratorio.")
print(question_card["question"])
```

### Paso 5. Los tres resultados de las Lecciones 2 a 4
En este paso leemos `outputs/grupos_l3.csv` y `outputs/texto_l4.csv`, con los tres resultados anteriores. Si no están, esos resultados quedan en falso. Para tener la cuenta real, suba a `outputs/` los archivos de las Lecciones 3 y 4.

```python
GROUPS_PATH = OUTPUTS_DIR / "grupos_l3.csv"
TEXT_PATH = OUTPUTS_DIR / "texto_l4.csv"

if GROUPS_PATH.is_file() and TEXT_PATH.is_file():
    groups_l3 = pd.read_csv(GROUPS_PATH, keep_default_na=False)
    text_l4 = pd.read_csv(TEXT_PATH, keep_default_na=False)
    week2 = pd.DataFrame({
        "title": groups_l3["title"],
        "has_pattern": groups_l3["has_pattern"].astype(str) == "True",
        "read_group": groups_l3["read_group"].astype(str) == "True",
        "text_says_read": text_l4["tfidf_lr"].astype(int) == 1,
    })
    print(f"Lecciones 2 a 4: {len(week2)} filas, {week2[['has_pattern', 'read_group', 'text_says_read']].sum().to_dict()}")
else:
    week2 = pd.DataFrame(columns=["title", "has_pattern", "read_group", "text_says_read"])
    print("Faltan grupos_l3.csv o texto_l4.csv. Los tres resultados anteriores quedan en falso.")
```

**Comprobar:**

En este paso comprobamos que la descripción de la pregunta y los tres resultados anteriores tienen sus columnas.

```python
assert {"question", "standard"} <= set(question_card)
assert {"title", "has_pattern", "read_group", "text_says_read"} <= set(week2.columns)
print("Pregunta y resultados anteriores: OK")
```

---

## Parte 2. Comprensión de los datos

### Paso 1. Los artículos y los títulos repetidos
En este paso quitamos los títulos repetidos, porque un nodo es un título. Quedan 318 filas. Al juntar resultados, un título repetido toma el resultado a favor de cualquiera de sus dos filas.

```python
repeated = raw.loc[raw["title"].duplicated(), "title"].tolist()
papers = raw.drop_duplicates("title").reset_index(drop=True)
N = len(papers)
print(f"Títulos repetidos: {len(repeated)}")
for t in repeated:
    print("  ", t[:90])
print(f"Artículos (nodos): {N}")
```

### Paso 2. Cómo vienen los enlaces
En este paso miramos `links`, con los títulos citados separados por `|`. Solo cuentan los enlaces a artículos **del conjunto**.

```python
title_set = set(papers["title"])
listed = [t.strip() for links in papers["links"] for t in str(links).split("|") if t.strip()]
inside = [t for t in listed if t in title_set]
print(f"Enlaces escritos: {len(listed)}. Dentro del conjunto: {len(inside)}")
print("Ejemplo:", papers.loc[papers["links"] != "", "links"].iloc[0][:150])
```

---

## Parte 3. Preparación de los datos

### Paso 1. La lista de enlaces dentro del conjunto (preparación de M1 y M2)
En este paso guardamos cada enlace dos veces: `links_out` con dirección, para PageRank, y `neighbours` sin dirección, para el grado y node2vec. Un artículo que se cita a sí mismo no cuenta.

```python
df = papers
df = df.drop_duplicates("title")        # cada fila: un artículo y los artículos que cita
titles = list(df["title"])
title_set = set(titles)
links_out = {t: set() for t in titles}          # con dirección, para PageRank
for title, links in zip(df["title"], df["links"]):
    for target in str(links).split("|"):
        target = target.strip()
        if target in title_set and target != title:
            links_out[title].add(target)        # solo enlaces dentro del conjunto

neighbours = {t: set() for t in titles}         # sin dirección, para lo demás
for a, targets in links_out.items():
    for b in targets:
        neighbours[a].add(b)
        neighbours[b].add(a)
print(f"Enlaces con dirección: {sum(len(v) for v in links_out.values())}. Sin dirección: {sum(len(v) for v in neighbours.values()) // 2}")
```

### Paso 2. Los dos grafos (preparación de M1 y M2)
En este paso pasamos los diccionarios a networkx: `directed` con dirección y `graph` sin dirección. Contamos los aislados y los componentes.

```python
directed = nx.DiGraph()
directed.add_nodes_from(links_out)
directed.add_edges_from((u, v) for u, vs in links_out.items() for v in vs)

graph = nx.Graph()
graph.add_nodes_from(neighbours)
graph.add_edges_from((u, v) for u, vs in neighbours.items() for v in vs)

components = sorted(nx.connected_components(graph), key=len, reverse=True)
isolated_count = sum(1 for v in graph if graph.degree(v) == 0)
n_components = sum(1 for c in components if len(c) > 1)
print(f"Nodos {graph.number_of_nodes()}, enlaces {graph.number_of_edges()}, aislados {isolated_count} ({isolated_count / N:.0%})")
print(f"Componentes con más de un artículo: {n_components}. El mayor tiene {len(components[0])} ({len(components[0]) / N:.0%})")
```

**Comprobar:**

En este paso comprobamos que hay un nodo por artículo en los dos grafos.

```python
assert graph.number_of_nodes() == N == len(titles)
assert directed.number_of_edges() >= graph.number_of_edges()
print("Grafos: OK")
```

**Lo que vemos.** El 38% de los artículos está aislado. El conjunto viene de una búsqueda por tema, así que no es un error. El grafo no dice nada de ellos.

### Paso 3. El componente mayor (preparación de M3)
En este paso nos quedamos con el componente mayor para node2vec. Los artículos de fuera quedan **sin vector** y nunca entran en un coseno.

```python
largest = max(nx.connected_components(graph), key=len)
adj = {v: neighbours[v] & largest for v in largest}
no_vector = [v for v in graph if v not in largest]   # se reportan, nunca entran en un coseno
print(f"Componente mayor: {len(adj)} artículos. Sin vector: {len(no_vector)} ({len(no_vector) / N:.0%})")
```

**Comprobar:**

En este paso comprobamos que cada artículo está en el componente mayor o sin vector, y que nadie queda solo en el componente.

```python
assert len(adj) + len(no_vector) == N
assert all(adj[v] for v in adj)
print("Componente mayor y artículos sin vector: OK")
```

---

## Parte 4. Modelado

### M1. El grado y la alerta de nodo central
En este paso contamos el **grado** de cada artículo y su parte del total posible. Un artículo enlazado con al menos el 10% de los otros es una **alerta**. Con 318 artículos, `hub_threshold` pide 32 enlaces.

```python
n = len(neighbours)
degree = {v: len(nbrs) for v, nbrs in neighbours.items()}
degree_share = {v: d / (n - 1) for v, d in degree.items()}
isolated = [v for v, d in degree.items() if d == 0]
hubs = [v for v, d in degree.items() if d >= hub_threshold(n)]

top_degree = sorted(degree, key=degree.get, reverse=True)[:10]
print(f"Alerta desde {hub_threshold(n)} enlaces. Nodos centrales: {len(hubs)}")
for v in top_degree:
    print(f"  grado {degree[v]:3d} ({degree_share[v]:.0%})  {v[:80]}")
```

```python
fig, ax = plt.subplots(figsize=(6, 3.5))
ax.hist(list(degree.values()), bins=range(0, max(degree.values()) + 2), color="#4C72B0")
ax.axvline(hub_threshold(n), color="#C44E52", linestyle="--", label=f"alerta ({hub_threshold(n)} enlaces)")
ax.set_xlabel("Grado")
ax.set_ylabel("Artículos")
ax.set_title("Grado de los artículos de nutrición")
ax.legend()
fig.tight_layout()
fig.savefig(OUTPUTS_DIR / "grado_l5.png", dpi=120)
plt.show()
```

**Comprobar:**

En este paso comprobamos el número de aislados y que la alerta de nodo central sigue su regla.

```python
assert len(isolated) == isolated_count
assert (max(degree_share.values()) < HUB_SHARE) == (len(hubs) == 0)
print(f"Grado: OK ({len(hubs)} nodos centrales, el más enlazado tiene {max(degree_share.values()):.0%})")
```

**Lo que vemos.** El más enlazado tiene 25 enlaces y no llega a la alerta. Arriba están los estudios de carga global, que todos usan de referencia.

### M2. PageRank a mano
En este paso calculamos PageRank a mano, con el código de las diapositivas (Page et al., 1998, en la [copia archivada del informe](https://web.archive.org/web/20241231011600/http://ilpubs.stanford.edu:8090/422/)). Un artículo sube si lo citan artículos que a su vez tienen puntaje alto. Con probabilidad `DAMPING` el navegante sigue un enlace, y si no, salta a cualquier artículo.

```python
DAMPING = 0.85

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
    nodes = list(links_out)
    n = len(nodes)
    rank = {v: 1 / n for v in nodes}
    for _ in range(steps):
        new = {v: (1 - d) / n for v in nodes}
        for u in nodes:
            targets = links_out[u] or nodes   # sin enlaces: salta a cualquiera
            for v in targets:
                new[v] += d * rank[u] / len(targets)
        rank = new
    return rank

rank = pagerank(links_out)
hand_rank = rank
print(f"Suma de los puntajes: {sum(rank.values()):.6f}")
```

### M2. El sumidero de puntaje
En este paso vemos por qué hace falta el salto al azar. Un **sumidero** es un grupo de nodos que se enlazan entre ellos y no enlazan a nadie más: el puntaje entra y no sale. En el grafo de juguete A cita a B, y B y C se citan entre ellos.

```python
sink = {"A": {"B"}, "B": {"C"}, "C": {"B"}}
for d in (1.0, DAMPING):
    toy_rank = pagerank(sink, d=d)
    print(f"d = {d}: A {toy_rank['A']:.3f}, B y C juntos {toy_rank['B'] + toy_rank['C']:.3f}")
```

**Lo que vemos.** Sin salto (d = 1) B y C se quedan con todo y A queda en 0. Con el salto A conserva su parte del azar, 0,15 / 3 = 0,05.

### M2. PageRank con networkx
En este paso usamos `networkx.pagerank`, lo comparamos con el cálculo a mano y ponemos los 10 primeros por PageRank junto a los 10 primeros por grado.

```python
rank = nx.pagerank(directed, alpha=DAMPING)
top_rank = sorted(rank, key=rank.get, reverse=True)[:10]
not_by_degree = [v for v in top_rank if v not in top_degree]

diff = max(abs(rank[v] - hand_rank[v]) for v in rank)
print(f"Diferencia más grande con el cálculo a mano: {diff:.1e}")
print(f"El primero tiene {rank[top_rank[0]]:.3f}, {rank[top_rank[0]] * N:.1f} veces el puntaje uniforme 1/{N}")
for v in top_rank:
    mark = "" if v in top_degree else "  <- no está entre los 10 de más grado"
    print(f"  PageRank {rank[v]:.3f}, grado {degree[v]:3d}  {v[:70]}{mark}")
```

**Comprobar:**

En este paso comprobamos que PageRank suma 1 y que el cálculo a mano coincide con networkx.

```python
assert abs(sum(rank.values()) - 1) < 1e-6
assert diff < 1e-3
print(f"PageRank: OK ({len(top_rank) - len(not_by_degree)} de los 10 primeros también están entre los 10 de más grado)")
```

**Lo que vemos.** PageRank premia que te cite alguien importante. "Obesity in children and young people" tiene grado 6 y está entre los 3 primeros.

### M2. Los artículos con PageRank alto
En este paso marcamos los artículos con **PageRank alto**: tienen enlaces, están en el cuarto superior por PageRank entre los artículos con enlaces y no son un nodo central. Usamos PageRank redondeado a 6 decimales, el mismo valor que guarda `grafo_l5.csv`, para que la Lección 6 obtenga la misma lista.

```python
score = {v: round(rank[v], 6) for v in rank}   # el valor que se guarda en grafo_l5.csv
connected = [v for v in graph if degree[v] > 0]
cut = sorted(score[v] for v in connected)[int(0.75 * len(connected))]
high_rank = [v for v in connected if score[v] >= cut and v not in hubs]
print(f"Artículos con enlaces: {len(connected)}. Corte del cuarto superior: {cut:.6f}. Con PageRank alto: {len(high_rank)}")
```

**Comprobar:**

En este paso comprobamos que hay artículos con PageRank alto, que son pocos y que ninguno es un nodo central.

```python
assert 0 < len(high_rank) <= len(connected) - int(0.75 * len(connected))
assert not set(high_rank) & set(hubs)
print(f"PageRank alto: OK ({len(high_rank)})")
```

### M3. Las caminatas de node2vec
En este paso escribimos las caminatas de las diapositivas. Volver atrás pesa 1/p, quedarse cerca 1 y alejarse 1/q. Con `Q_INOUT = 0.5`, alejarse pesa el doble.

```python
def node2vec_walks(adj, walks_per_node, walk_length, p, q, seed):
    """Caminatas al azar de node2vec sobre el componente mayor (Grover y Leskovec, 2016).

    Qué hace: cada nodo es el inicio de walks_per_node caminatas de walk_length pasos. El primer
    paso va a un vecino al azar. Desde el segundo, el peso de cada vecino depende de
    dónde estaba la caminata antes: volver al nodo anterior pesa 1/p, ir a un vecino
    del nodo anterior pesa 1 y alejarse pesa 1/q. Los nodos y los vecinos van
    ordenados y hay un solo random.Random por semilla, así que la misma semilla da
    las mismas caminatas en cualquier sesión.

    Entrada:
        adj: diccionario de cada nodo del componente mayor a sus vecinos dentro de él.
        walks_per_node: caminatas por nodo, WALKS_PER_NODE.
        walk_length: pasos por caminata, WALK_LENGTH.
        p: peso de volver atrás, P_RETURN.
        q: peso de alejarse, Q_INOUT.
        seed: semilla del sorteo.

    Salida:
        Una lista de caminatas. Cada caminata es una lista de títulos, como una frase de palabras.
    """
    rng, nodes, walks = random.Random(seed), sorted(adj), []
    for _ in range(walks_per_node):
        rng.shuffle(nodes)
        for start in nodes:
            walk = [start]
            while len(walk) < walk_length:
                here = walk[-1]
                options = sorted(adj[here])   # nunca vacío en el componente mayor
                if len(walk) == 1:
                    walk.append(rng.choice(options))
                    continue
                before = walk[-2]
                weights = [1 / p if x == before            # volver atrás
                           else 1.0 if x in adj[before]     # quedarse cerca
                           else 1 / q                       # alejarse
                           for x in options]
                walk.append(rng.choices(options, weights=weights)[0])
            walks.append([str(x) for x in walk])
    return walks

walks = node2vec_walks(adj, WALKS_PER_NODE, WALK_LENGTH, P_RETURN, Q_INOUT, N2V_SEEDS[0])
print(f"{len(walks)} caminatas de {WALK_LENGTH} pasos. La primera empieza en: {walks[0][0][:70]}")
```

### M3. Los vectores de node2vec
En este paso entrenamos word2vec sobre las caminatas: una caminata es una frase y un artículo es una palabra. `workers=1` y una semilla fija dan los mismos vectores.

```python
start = time.time()
model = Word2Vec(walks, vector_size=NODE_DIMENSIONS, window=WINDOW,
                 min_count=1, sg=1, workers=1, seed=N2V_SEEDS[0])
some_item = top_rank[0]
print(f"Entrenado en {time.time() - start:.1f} s")
print(model.wv.most_similar(str(some_item), topn=5))
```

**Comprobar:**

En este paso comprobamos que hay un vector por artículo del componente mayor y ninguno para los artículos sin vector.

```python
assert len(model.wv) == len(adj)
assert not set(no_vector) & set(model.wv.index_to_key)
print("Vectores de node2vec: OK (ningún artículo sin vector tiene coseno)")
```

**Lo que vemos.** Los vecinos comparten lugar en la red, no siempre un tema. En la Parte 5 lo medimos.

### Al margen. Distancias por niveles
En este paso, fuera de los tres métodos, escribimos la búsqueda en anchura como función y la usamos desde el primer artículo por PageRank.

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
    dist = {source: 0}
    queue = deque([source])
    while queue:
        u = queue.popleft()
        for v in neighbours[u]:
            if v not in dist:
                dist[v] = dist[u] + 1
                queue.append(v)
    return dist

first = top_rank[0]
reach = distances_from(first, neighbours)
print(f"Desde el primero por PageRank se alcanzan {len(reach) - 1} artículos. El más lejano está a {max(reach.values())} pasos")
```

**Lo que vemos.** Se llega a los otros 147 del componente mayor, en 5 pasos como máximo. Los otros 170 no se alcanzan.

---

## Parte 5. Evaluación

Aquí no hay marcas ni ganador. Miramos qué dicen el grado, PageRank y node2vec que los otros no dicen, y si node2vec es estable.

### Paso 1. Grado y PageRank contra las citas
En este paso comparamos el orden por PageRank y por grado con el grado de entrada y las citas en el mundo (`cited_by_count`), con la correlación de rangos de Spearman. node2vec no da un puntaje, así que lo evaluamos por sus vecinos en los pasos 3 y 4.

```python
cites = dict(zip(titles, pd.to_numeric(papers["cited_by_count"], errors="coerce").fillna(0)))
in_degree = dict(directed.in_degree())
pr = [rank[t] for t in titles]
rho_degree = spearmanr(pr, [degree[t] for t in titles])[0]
rho_in = spearmanr(pr, [in_degree[t] for t in titles])[0]
rho_cites = spearmanr(pr, [cites[t] for t in titles])[0]
print(f"Spearman de PageRank con el grado {rho_degree:.2f}, con el grado de entrada {rho_in:.2f}, con las citas {rho_cites:.2f}")
deg = [degree[t] for t in titles]
rho_degree_in = spearmanr(deg, [in_degree[t] for t in titles])[0]
rho_degree_cites = spearmanr(deg, [cites[t] for t in titles])[0]
print(f"Spearman del grado con el grado de entrada {rho_degree_in:.2f}, con las citas {rho_degree_cites:.2f}")
```

**Lo que vemos.** PageRank sigue al grado de entrada (0,97), menos al grado (0,75) y poco a las citas (0,30). El grafo mide el lugar dentro de lo que el equipo va a leer.

### Paso 2. Un artículo descrito por su lugar
En este paso describimos un artículo por su lugar: puestos por grado, PageRank y citas, y sus vecinos de node2vec. Es una guía clínica elegida antes de ver la lista final.

```python
def place_of(score):
    """Puesto de cada artículo según un puntaje, de mayor a menor.

    Qué hace: el artículo con el puntaje más alto tiene el puesto 1. Sirve para comparar
    medidas con escalas distintas (grado, PageRank, citas) en una misma
    línea. Los empates quedan en el orden de titles.

    Entrada:
        score: diccionario de cada título a su puntaje.

    Salida:
        Un diccionario de cada título a su puesto, de 1 a N.
    """
    return {t: i + 1 for i, t in enumerate(sorted(titles, key=lambda t: -score[t]))}

by_degree, by_rank, by_cites = place_of(degree), place_of(rank), place_of(cites)
print(EXAMPLE)
print(f"  grado {degree[EXAMPLE]}, puesto {by_degree[EXAMPLE]} por grado, puesto {by_rank[EXAMPLE]} por PageRank, puesto {by_cites[EXAMPLE]} de {N} por citas ({int(cites[EXAMPLE]):,})")
print(f"  PageRank alto: {'sí' if EXAMPLE in high_rank else 'no'}")
```

```python
example_neighbours = [t for t, _ in model.wv.most_similar(EXAMPLE, topn=5)]
for t in example_neighbours:
    linked = "enlazado" if t in neighbours[EXAMPLE] else "sin enlace directo"
    print(f"  vecino node2vec: {t[:75]} ({linked})")
```

**Comprobar:**

En este paso comprobamos que el artículo de ejemplo está en el componente mayor, que tiene PageRank alto y que sube por PageRank frente a las citas.

```python
assert EXAMPLE in adj and EXAMPLE in high_rank
assert by_rank[EXAMPLE] < by_cites[EXAMPLE]
print("Artículo descrito por su lugar: OK")
```

**Lo que vemos.** La guía tiene grado 10. Está en el puesto 48 por PageRank y en el 187 por citas: dentro del conjunto pesa más que en el mundo. Recibe el resultado del grafo.

### Paso 3. ¿Son estables los vecinos de node2vec?
En este paso repetimos node2vec con tres semillas y contamos cuántos de los 5 vecinos se repiten.

```python
start = time.time()
neighbours_by_seed = []
for seed in N2V_SEEDS:
    seed_walks = node2vec_walks(adj, WALKS_PER_NODE, WALK_LENGTH, P_RETURN, Q_INOUT, seed)
    seed_model = Word2Vec(seed_walks, vector_size=NODE_DIMENSIONS, window=WINDOW, min_count=1, sg=1, workers=1, seed=seed)
    neighbours_by_seed.append({v: [x for x, _ in seed_model.wv.most_similar(str(v), topn=5)] for v in adj})
lcc = sorted(adj)
overlap = np.mean([len(set(neighbours_by_seed[0][v]) & set(neighbours_by_seed[k][v])) / 5 for v in lcc for k in (1, 2)])
stable = set.intersection(*(set(nb[EXAMPLE]) for nb in neighbours_by_seed))
print(f"Tres semillas en {time.time() - start:.1f} s. Vecinos que se repiten: {overlap:.2f}")
print(f"Del artículo de ejemplo, {len(stable)} de 5 vecinos están en las tres semillas")
```

### Paso 4. Vecinos contra pares al azar
En este paso medimos si los vecinos comparten temas de OpenAlex más que dos artículos al azar, con el índice de Jaccard. Los temas no entran en node2vec, así que es una prueba independiente.

```python
def topic_set(text):
    """Conjunto de temas de OpenAlex de un artículo.

    Entrada:
        text: la columna topics, con los temas separados por |.

    Salida:
        Un conjunto de temas, sin espacios ni temas vacíos.
    """
    return {x.strip() for x in str(text).split("|") if x.strip()}

topics = dict(zip(titles, map(topic_set, papers["topics"])))

def jaccard(a, b):
    """Índice de Jaccard: elementos en común sobre elementos en total.

    Entrada:
        a, b: dos conjuntos de temas.

    Salida:
        Un número entre 0 y 1. Dos conjuntos vacíos dan 0.
    """
    return len(a & b) / len(a | b) if a | b else 0.0

near = np.mean([np.mean([jaccard(topics[v], topics[u]) for u in neighbours_by_seed[0][v]]) for v in lcc])
pairs = random.Random(SEED)
far = np.mean([jaccard(topics[a], topics[b]) for a, b in (pairs.sample(lcc, 2) for _ in range(N_RANDOM_PAIRS))])
print(f"Jaccard de temas, vecinos {near:.3f}, pares al azar {far:.3f}, {near / far:.1f} veces más")
```

**Comprobar:**

En este paso comprobamos que los vecinos se repiten entre semillas y comparten más temas que el azar.

```python
assert overlap >= 0.5
assert near > far
print("node2vec estable y con sentido: OK")
```

**Lo que vemos.** Tres de cada cuatro vecinos se repiten, y comparten 4,6 veces más temas que al azar.

### Paso 5. Un dibujo del componente mayor
En este paso dibujamos el componente mayor. El tamaño es el grado, el color es PageRank y los artículos con PageRank alto llevan borde negro. La posición cambia con la semilla del dibujo.

```python
# Nodos y aristas en orden: vienen de sets, y sin orden el dibujo cambia de una ejecución a otra
sub = nx.Graph()
sub.add_nodes_from(sorted(largest))
sub.add_edges_from(sorted(tuple(sorted(e)) for e in graph.subgraph(largest).edges()))
pos = nx.spring_layout(sub, seed=SEED)
fig, ax = plt.subplots(figsize=(7, 6))
nx.draw_networkx_edges(sub, pos, ax=ax, alpha=0.3)
nodes_drawn = nx.draw_networkx_nodes(sub, pos, ax=ax, node_size=[20 + 8 * degree[v] for v in sub],
                                     node_color=[rank[v] for v in sub], cmap="viridis",
                                     edgecolors=["black" if v in high_rank else "none" for v in sub])
fig.colorbar(nodes_drawn, ax=ax, label="PageRank")
ax.set_title(f"Componente mayor ({len(largest)} artículos). Borde negro: PageRank alto")
ax.axis("off")
fig.tight_layout()
fig.savefig(OUTPUTS_DIR / "componente_l5.png", dpi=120)
plt.show()
```

**Lo que leemos.** El grafo habla solo de una parte de la colección. Por eso es un resultado más, no la decisión.

---

## Parte 6. Despliegue

### Paso 1. El resultado del grafo en la tabla
En este paso armamos `table`, una fila por título, con los tres resultados anteriores y `graph_support`, tener **PageRank alto** (Parte 4, M2). Los 3 resúmenes cortos van como "sin texto". Un artículo queda **en vista** según `MIN_SUPPORTS`, el número de resultados a favor que pide el código. `MIN_SUPPORTS` empieza en 2 y se puede cambiar. Cada grupo fija y justifica este número en su proyecto. 0 o 1 valen si se explica. La celda cuenta cuántos artículos tienen 0, 1, 2 y 3 o más resultados a favor.

```python
supports_w2 = week2.groupby("title")[["has_pattern", "read_group", "text_says_read"]].any()
table = supports_w2.reindex(titles).fillna(False).astype(bool)   # table: una fila por artículo, el título es el índice
table.index.name = "title"
no_text = [t for t in titles if t not in supports_w2.index]
print(f"Sin texto en las Lecciones 3 y 4: {len(no_text)}")
for t in no_text:
    print("  ", t[:70])

table["graph_support"] = table.index.isin(high_rank)   # cuarto superior por PageRank, sin nodos centrales
SUPPORT_COLUMNS = ["has_pattern", "read_group", "text_says_read", "graph_support"]
table["supports"] = table[SUPPORT_COLUMNS].astype(int).sum(axis=1)
table["in_view"] = table["supports"] >= MIN_SUPPORTS
before = (table[SUPPORT_COLUMNS[:3]].astype(int).sum(axis=1) >= MIN_SUPPORTS).sum()
print(f"En vista con tres resultados: {before}. Con el grafo: {table['in_view'].sum()} de {N}")
counts = table["supports"].clip(upper=3).value_counts().reindex(range(4), fill_value=0).rename(index={3: "3 o más"})
print(counts.rename_axis("resultados a favor").to_frame("artículos").T.to_string())
```

**Comprobar:**

En este paso comprobamos que la tabla tiene un artículo por fila y que el grafo suma un resultado a cada artículo con PageRank alto.

```python
assert len(table) == N and table.index.is_unique
assert table["in_view"].sum() >= before and table["graph_support"].sum() == len(high_rank)
print("Tabla de resultados con el grafo: OK")
```

**Lo que aprendemos aquí.** El grafo apoya a los 49 artículos con PageRank alto. Los aislados y los sin vector no reciben el resultado, pero no salen de la lista. Con el grafo, la lista pasa de 52 a 66 artículos en vista.

### Paso 2. Guardar el grafo
En este paso guardamos `outputs/grafo_l5.csv`. `vecinos_n2v` lleva los 5 vecinos separados por `|`.

```python
graph_table = pd.DataFrame({
    "title": titles,
    "grado": [degree[t] for t in titles],
    "pagerank": [round(rank[t], 6) for t in titles],
    "aislado": [degree[t] == 0 for t in titles],
    "alerta_centro": [t in hubs for t in titles],
    "sin_vector_n2v": [t not in adj for t in titles],
    "vecinos_n2v": ["|".join(neighbours_by_seed[0][t]) if t in adj else "" for t in titles],
    "supports": table.loc[titles, "supports"].to_numpy(),
    "in_view": table.loc[titles, "in_view"].to_numpy(),
})
graph_path = OUTPUTS_DIR / "grafo_l5.csv"
graph_table.to_csv(graph_path, index=False)
print(f"Guardado: {graph_path} ({len(graph_table)} filas)")
```

**Comprobar:**

En este paso comprobamos que el archivo guardado tiene sus columnas y una fila por artículo.

```python
saved = pd.read_csv(graph_path, keep_default_na=False)
assert {"title", "grado", "pagerank", "aislado", "alerta_centro", "sin_vector_n2v", "vecinos_n2v", "supports", "in_view"} <= set(saved.columns)
assert len(saved) == N
print("grafo_l5.csv: OK")
```

### Paso 3. Qué cambiaría la decisión
En este paso anotamos en `pregunta.json` cómo entra el grafo y qué lo cambiaría.

```python
question_card["graph_use"] = {
    "how_it_enters": "El resultado del grafo cuenta a favor de un artículo si tiene PageRank alto: está en el cuarto superior por PageRank entre los artículos con enlaces, y no es un nodo central.",
    "reading": "El grafo solo ve las citas dentro del conjunto. Un artículo aislado no tiene lugar, no es malo.",
    "high_rank": len(high_rank),
    "what_changes_it": ["otro corte que el cuarto superior", "otra regla para los nodos centrales", "más artículos o más enlaces en el conjunto"],
}
QUESTION_PATH.write_text(json.dumps(question_card, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(question_card["graph_use"], ensure_ascii=False, indent=1))
```

### Paso 4. Comprobación final
En este paso revisamos que el cuaderno dejó lo que la Lección 6 necesita.

```python
def _check_ok(name, predicate):
    """Ejecuta una comprobación sin detener el cuaderno: un error cuenta como incompleto.

    Salida:
        True si la comprobación pasó, False si no.
    """
    try:
        ok = bool(predicate())
    except Exception:
        ok = False
    print(f"{name}: {'OK' if ok else 'incompleto'}")
    return ok


checks = [
    ("pregunta.json con uso del grafo", lambda: "graph_use" in json.loads(QUESTION_PATH.read_text(encoding="utf-8"))),
    ("outputs/grafo_l5.csv", lambda: graph_path.is_file()),
    ("Histograma de grado y dibujo del componente", lambda: all((OUTPUTS_DIR / f).is_file() for f in ["grado_l5.png", "componente_l5.png"])),
    ("Resultados de las Lecciones 2 a 4", lambda: len(week2) > 0),
]
passed = sum(_check_ok(n, f) for n, f in checks)
print(f"\nL5_CHECKS={passed}/{len(checks)}")
if passed == len(checks):
    print("L5_OK. Siga con la Lección 6.")
```

<!-- end NOTEBOOK: -->
