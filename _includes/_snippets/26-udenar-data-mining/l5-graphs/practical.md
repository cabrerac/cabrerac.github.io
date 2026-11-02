<!-- NOTEBOOK: -->

## Repaso de Python para este cuaderno
 
Este repaso es corto. Muestra las dos ideas que usamos en toda la lección: guardar un grafo como un diccionario de conjuntos, y recorrerlo por niveles. Las dos vuelven más adelante con los artículos de nutrición. El diccionario es la forma en que guardamos quién cita a quién, y el recorrido por niveles es la base de la intermediación. Si ya las conoce, ejecute las celdas rápido y siga.
 
### Un grafo como diccionario de conjuntos
Cada nodo es una clave. Su valor es el conjunto de nodos con los que tiene un enlace. Si el enlace no tiene dirección, lo guardamos en los dos lados: A está en el conjunto de B y B en el de A. Un conjunto no repite elementos, así que un enlace escrito dos veces cuenta una sola vez. El **grado** de un nodo es el tamaño de su conjunto.

```python
toy = {"A": set(), "B": set(), "C": set(), "D": set(), "E": set()}
for a, b in [("A", "B"), ("A", "C"), ("B", "C"), ("C", "D")]:
    toy[a].add(b)
    toy[b].add(a)
print({v: sorted(n) for v, n in toy.items()})
print("Grado de cada nodo:", {v: len(n) for v, n in toy.items()})
```

### Búsqueda por niveles a mano
La búsqueda en anchura sale de un nodo, visita primero a sus vecinos, después a los vecinos de los vecinos, y así. Cuenta cuántos pasos hay hasta cada nodo. E no tiene enlaces, así que nunca se alcanza. La cola guarda los nodos que faltan por visitar, en el orden en que los encontramos. Por eso los vecinos directos salen antes que los vecinos de los vecinos.

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

**Lo que vemos.** D está a dos pasos de A porque hay que pasar por C. Si quitáramos C, la red se partiría en dos. Esa idea, un nodo por el que pasan los caminos de los demás, es la intermediación que calculamos en la Parte 5.

---
 
## Instrucciones
 
**La historia.** Seguimos con el equipo interno de la secretaría de salud y sus 320 artículos de nutrición. Ya tenemos tres resultados: patrones (L2), grupos (L3) y texto (L4). Con ellos, 52 de los 317 artículos quedaron en vista. Hoy miramos algo que ninguno de los tres usa: **las citas entre los artículos**. Un artículo citado por otros del conjunto, o que une dos partes del conjunto, tiene un lugar que no se ve en su texto ni en su número de citas en el mundo.
 
**La idea central.** Describimos un artículo por su **lugar entre los demás**, no por cuántas veces se lo cita. Un artículo enlazado con muchos otros es una **alerta**, no una elección automática: puede ser una revisión general que todos citan. Un artículo que **une dos grupos** puede ser justo el que una persona nueva necesita leer.
 
**Tres métodos, tres preparaciones.**
 
| Método | Pregunta | Preparación que necesita |
|--------|----------|--------------------------|
| M1. Grado y PageRank | ¿Con cuántos se enlaza, y quién lo cita? | Una lista de enlaces dentro del conjunto. Un grafo dirigido para PageRank |
| M2. Intermediación | ¿Está en el camino entre otros? | El grafo sin dirección |
| M3. node2vec | ¿Quiénes están cerca en la red? | El componente mayor y caminatas al azar sobre él |
 
**Qué hacer.** Ejecute las celdas de arriba hacia abajo. Cada paso empieza con **En este paso**. Los pasos que crean algo nuevo terminan con una celda `# Comprobar`. Si un `assert` falla, revise la celda anterior antes de seguir. Los nombres del código están en inglés, como en todos los cuadernos del curso. Las explicaciones están en español.
 
**Mapa del cuaderno**
 
| Parte | Fase CRISP-DM | Qué sale |
|-------|---------------|----------|
| 1 | Configuración | Librerías, parámetros y funciones |
| 2 | Comprensión del negocio | `pregunta.json` y los tres apoyos de la semana 2 |
| 3 | Comprensión de los datos | Los artículos y sus enlaces |
| 4 | Preparación de los datos | La lista de enlaces, los dos grafos y el componente mayor |
| 5 | Modelado | Grado, PageRank, intermediación y node2vec |
| 6 | Evaluación | Contra las citas, un artículo descrito por su lugar, estabilidad de node2vec |
| 7 | Despliegue | El apoyo del grafo en `supports` y `outputs/grafo_l5.csv` |

---
 
## Parte 1. Configuración
 
### Paso 1. Librerías, carpetas y parámetros
En este paso instalamos lo que falte, importamos las librerías y fijamos los parámetros. En Colab, networkx ya viene instalado. La celda instala `gensim` solo si falta. Los parámetros de la L5 se definen aquí una sola vez y son los mismos en el cuaderno de grupo. No los cambie aquí.

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
MIN_SUPPORTS = 2

# L5 (compartidos con el cuaderno de grupo, no cambiar)
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
    menos de min_links. Es la misma regla en la L5 y en el cuaderno de grupo.

    Entrada:
        n: número de nodos de la red.
        min_links: piso de enlaces, MIN_LINKS = 5 por defecto.

    Salida:
        El número entero de enlaces desde el cual un nodo es una alerta.
    """
    return max(min_links, math.ceil(HUB_SHARE * (n - 1)))


print(f"networkx {nx.__version__}. Alerta desde {hub_threshold(318)} enlaces con 318 artículos")
```

### Paso 2. Descargar los artículos
En este paso descargamos el archivo de la semana 1, una sola vez. Es el mismo archivo de las lecciones anteriores. La columna nueva para hoy es `links`, con los títulos que cada artículo cita dentro del conjunto.

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

---
 
## Parte 2. Comprensión del negocio
 
### Paso 1. Recuperar la pregunta
En este paso leemos `pregunta.json`. La pregunta no cambia. Lo nuevo es cómo entra el grafo: un artículo recibe el apoyo del grafo si **une partes de la red** y no es solo un nodo central. Si trabaja en la misma carpeta de la L4, la tarjeta ya está. Si no, la celda escribe la tarjeta de referencia del laboratorio.

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
    print("pregunta.json no estaba. Escribimos la tarjeta.")
print(question_card["question"])
```

### Paso 2. Recuperar los tres apoyos de la semana 2
En este paso leemos `outputs/grupos_l3.csv` (patrón y grupo) y `outputs/texto_l4.csv` (texto). Si no están, siga igual: los tres apoyos quedan en falso y la cuenta final será más baja. Copie `grupos_l3.csv` de la L3 y `texto_l4.csv` de la L4 a la carpeta `outputs/` para tener la cuenta real. Estos tres apoyos son los resultados de la semana 2: el patrón de la L2, el grupo leído de la L3 y el texto de la L4. Hoy les sumamos un cuarto.

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
    print(f"Semana 2: {len(week2)} filas, {week2[['has_pattern', 'read_group', 'text_says_read']].sum().to_dict()}")
else:
    week2 = pd.DataFrame(columns=["title", "has_pattern", "read_group", "text_says_read"])
    print("Faltan grupos_l3.csv o texto_l4.csv. Los tres apoyos de la semana 2 quedan en falso.")
```

```python
# Comprobar
assert {"question", "standard"} <= set(question_card)
assert list(week2.columns) == ["title", "has_pattern", "read_group", "text_says_read"]
print("Pregunta y apoyos de la semana 2: OK")
```

---
 
## Parte 3. Comprensión de los datos
 
### Paso 1. Los artículos y los títulos repetidos
En este paso quitamos los títulos repetidos. Un nodo del grafo es un título, así que dos filas con el mismo título serían el mismo nodo. Nos quedamos con la primera. En la semana 2 se usaron 317 filas: se quitaron 3 resúmenes demasiado cortos y se dejaron las dos copias de cada título repetido. Aquí se usan las 318 filas sin repetidos. Más adelante, al juntar con la semana 2, un título repetido toma un apoyo si cualquiera de sus dos filas lo tenía.

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
En este paso miramos la columna `links`. Cada fila trae los títulos que el artículo cita, separados por `|`. Solo cuentan los enlaces a artículos **del conjunto**. Un artículo citado de fuera no es un nodo. El extracto ya trae solo los enlaces a títulos del conjunto, así que las dos cuentas salen iguales. Si usted arma su propio conjunto, la segunda cuenta es la que importa.

```python
title_set = set(papers["title"])
listed = [t.strip() for links in papers["links"] for t in str(links).split("|") if t.strip()]
inside = [t for t in listed if t in title_set]
print(f"Enlaces escritos: {len(listed)}. Dentro del conjunto: {len(inside)}")
print("Ejemplo:", papers.loc[papers["links"] != "", "links"].iloc[0][:150])
```

---
 
## Parte 4. Preparación de los datos
 
### Paso 1. La lista de enlaces dentro del conjunto (preparación de M1)
En este paso guardamos cada enlace dos veces. `links_out` tiene la dirección (quién cita a quién), para PageRank. `neighbours` no tiene dirección, para el grado, la intermediación y node2vec. Es el código de las diapositivas. Un artículo que se cita a sí mismo no cuenta, porque un enlace a uno mismo no conecta con nadie. La diferencia entre las dos cuentas de enlaces son los pares que se citan en las dos direcciones: con dirección son dos enlaces, sin dirección es uno.

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
En este paso pasamos los diccionarios a networkx. `directed` es el grafo con dirección. `graph` es el grafo sin dirección. Contamos los artículos aislados (sin ningún enlace) y los componentes, es decir, las partes de la red que no se tocan entre sí. Usamos networkx porque ya trae PageRank, la intermediación y los componentes, y porque es la librería que encontrará fuera del curso.

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

```python
# Comprobar
assert graph.number_of_nodes() == N == len(titles)
assert directed.number_of_edges() >= graph.number_of_edges()
print("Grafos: OK")
```

**Lo que vemos.** El 38% de los artículos no cita ni es citado por otro del conjunto. Eso no es un error: el conjunto viene de una búsqueda por tema, no de seguir citas. Un artículo aislado no tiene lugar en la red, así que el grafo no dice nada de él, ni bueno ni malo.
 
### Paso 3. El componente mayor (preparación de M3)
En este paso nos quedamos con el componente mayor para node2vec. Las caminatas en un componente de 2 o 3 artículos dan ruido: se repiten los mismos nodos y los vecinos cambian con la semilla. Los artículos fuera del componente mayor quedan **sin vector**. Los dibujamos en el origen y nunca los usamos en un coseno, porque un vector de ceros no tiene coseno.

```python
largest = max(nx.connected_components(graph), key=len)
adj = {v: neighbours[v] & largest for v in largest}
no_vector = [v for v in graph if v not in largest]   # se reportan, nunca entran en un coseno
print(f"Componente mayor: {len(adj)} artículos. Sin vector: {len(no_vector)} ({len(no_vector) / N:.0%})")
```

```python
# Comprobar
assert len(adj) + len(no_vector) == N
assert all(adj[v] for v in adj)
print("Componente mayor y artículos sin vector: OK")
```

---
 
## Parte 5. Modelado
 
### M1. El grado y la alerta de nodo central
En este paso contamos los enlaces de cada artículo (su **grado**) y su parte del total posible, grado / (n - 1). Un artículo enlazado con al menos el 10% de los otros es una **alerta**: puede ser una revisión que todos citan, y no sirve para separar unos artículos de otros. Mostramos valores de grado, no puestos, porque el puesto depende de cómo se ordenan los empates. El umbral sale de `hub_threshold`: con 318 artículos, una alerta necesita 32 enlaces.

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

```python
# Comprobar
assert len(isolated) == isolated_count
assert (max(degree_share.values()) < HUB_SHARE) == (len(hubs) == 0)
print(f"Grado: OK ({len(hubs)} nodos centrales, el más enlazado tiene {max(degree_share.values()):.0%})")
```

**Lo que vemos.** El artículo más enlazado tiene 25 enlaces, el 8% de los otros, y no llega a la alerta. Los más enlazados son los estudios de carga global de enfermedad: los cita casi cualquier artículo de salud pública. Muchos enlaces no dicen que un artículo sea el tema del equipo. Dicen que es un artículo que todos usan de referencia.

### M1. PageRank a mano
En este paso calculamos PageRank con el código de las diapositivas. Un artículo tiene un PageRank alto si lo citan muchos, o si lo citan pocos que a su vez tienen PageRank alto (Page et al., 1998, p. 3, en la [copia archivada del informe](https://web.archive.org/web/20241231011600/http://ilpubs.stanford.edu:8090/422/)). Con probabilidad `DAMPING` el navegante sigue un enlace, y si no, salta a cualquier artículo. Un artículo sin enlaces de salida reparte su puntaje entre todos. Escribirlo a mano una vez muestra que PageRank es solo una cuenta repetida, sin nada escondido.

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

### M1. PageRank con networkx
En este paso usamos `networkx.pagerank` sobre el grafo con dirección y comparamos con el cálculo a mano. Después ponemos los 10 primeros por PageRank junto a los 10 primeros por grado. Las dos cuentas deben coincidir hasta varios decimales. networkx para cuando los puntajes cambian menos que una tolerancia, y nuestro cálculo da 100 vueltas fijas.

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

```python
# Comprobar
assert abs(sum(rank.values()) - 1) < 1e-6
assert diff < 1e-3
print(f"PageRank: OK ({len(top_rank) - len(not_by_degree)} de los 10 primeros también están entre los 10 de más grado)")
```

**Lo que vemos.** PageRank premia que te cite alguien importante, no solo que te citen muchos. "Obesity in children and young people" tiene grado 6 y está entre los 3 primeros por PageRank, mientras que el grado más bajo entre los 10 de más grado es 14. En los extractos de Wikipedia pasa lo mismo: *Medicina psicosomática* tiene grado 3 y la enlaza Psiquiatría, el artículo con más PageRank de salud mental, y *Abono verde* tiene grado 6 y la enlazan Fertilizante y Agricultura ecológica. Lo verá en el cuaderno de grupo con su secretaría.
 
### M2. Distancias por niveles
En este paso escribimos la búsqueda en anchura del repaso como una función. La intermediación cuenta caminos más cortos, y esta función es la base. La usamos una vez desde el primer artículo por PageRank, para ver hasta dónde llega la red desde él.

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

**Lo que vemos.** Desde el primer artículo por PageRank se llega a los otros 147 del componente mayor, y el más lejano está a 5 pasos. Los otros 170 artículos no se alcanzan: están aislados o en componentes pequeños.

### M2. Intermediación y puentes
En este paso calculamos la **intermediación**: qué parte de los caminos más cortos entre otros dos artículos pasa por cada artículo. Redondeamos a 9 decimales antes de ordenar. Dos puntajes iguales en la cuenta exacta pueden salir distintos en el último decimal según el orden de los enlaces, y sin redondear la cuenta de puentes cambiaría de una sesión a otra. Un **puente** es un artículo con enlaces, en el cuarto superior por intermediación, que no es un nodo central.

```python
between = nx.betweenness_centrality(graph, normalized=True)
between = {v: round(b, 9) for v, b in between.items()}   # puntajes iguales siguen iguales

connected = [v for v in graph if degree[v] > 0]
cut = sorted(between[v] for v in connected)[int(0.75 * len(connected))]
bridges = [v for v in connected if between[v] >= cut and v not in hubs]
top_between = sorted(between, key=lambda v: -between[v])[:5]
print(f"Artículos con enlaces: {len(connected)}. Corte del cuarto superior: {cut:.4f}. Puentes: {len(bridges)}")
for v in top_between:
    print(f"  intermediación {between[v]:.3f}, grado {degree[v]:3d}  {v[:70]}")
```

```python
# Comprobar
assert 0 < len(bridges) <= len(connected) - int(0.75 * len(connected))
assert not set(bridges) & set(hubs)
print(f"Puentes: OK ({len(bridges)})")
```

**Lo que vemos.** Los más altos por intermediación son otra vez estudios de carga global, pero también aparecen artículos con grado 11 o 12, como las metas de salud cardiovascular y un ensayo sobre presión arterial. Un puente no necesita muchos enlaces. Necesita estar entre dos partes de la red que sin él quedarían más lejos.

### M3. Las caminatas de node2vec
En este paso escribimos la función de caminatas de las diapositivas. Cada caminata sale de un nodo y da `WALK_LENGTH` pasos. En cada paso, volver atrás pesa 1/p, quedarse cerca pesa 1 y alejarse pesa 1/q. Con `Q_INOUT = 0.5`, alejarse pesa el doble. Los nodos y los vecinos van ordenados, así que una semilla da las mismas caminatas en cualquier sesión.

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
En este paso entrenamos word2vec sobre las caminatas, como en la L2 lo hicimos sobre frases. Una caminata es una frase y un artículo es una palabra. Dos artículos que aparecen en las mismas caminatas quedan cerca, aunque no se citen entre sí. `workers=1` y una semilla fija dan los mismos vectores cada vez. Con más de un hilo, word2vec reparte el trabajo en otro orden en cada corrida y los vecinos cambian un poco.

```python
start = time.time()
model = Word2Vec(walks, vector_size=NODE_DIMENSIONS, window=WINDOW,
                 min_count=1, sg=1, workers=1, seed=N2V_SEEDS[0])
some_item = top_rank[0]
print(f"Entrenado en {time.time() - start:.1f} s")
print(model.wv.most_similar(str(some_item), topn=5))
```

```python
# Comprobar
assert len(model.wv) == len(adj)
assert not set(no_vector) & set(model.wv.index_to_key)
print("Vectores de node2vec: OK (ningún artículo sin vector tiene coseno)")
```

**Lo que vemos.** Los vecinos del primer artículo por PageRank mezclan carne, alimentos ultraprocesados y otros estudios de carga global. Comparten lugar en la red, no necesariamente un tema. En la Parte 6 medimos si esos vecinos comparten temas de OpenAlex más que dos artículos al azar.

---
 
## Parte 6. Evaluación
 
Aquí no hay marcas. No buscamos un ganador entre los métodos: no es una competencia. Miramos qué dice cada uno que los otros no dicen, y si node2vec es estable. Las preguntas son las del equipo de la secretaría de salud. ¿El grafo repite lo que ya dicen las citas? ¿Hay artículos que el grafo pone arriba y una cuenta de citas no? ¿Podemos confiar en los vecinos de node2vec si cambiamos la semilla?
 
### Paso 1. Grado y PageRank contra las citas
En este paso comparamos el orden por PageRank con el orden por grado, por grado de entrada (cuántos lo citan dentro del conjunto) y por citas en el mundo (`cited_by_count`). Usamos la correlación de rangos de Spearman. Compara órdenes y no valores: vale 1 si los dos órdenes son iguales y 0 si no tienen relación. Sirve aquí porque los puntajes tienen escalas muy distintas.

```python
cites = dict(zip(titles, pd.to_numeric(papers["cited_by_count"], errors="coerce").fillna(0)))
in_degree = dict(directed.in_degree())
pr = [rank[t] for t in titles]
rho_degree = spearmanr(pr, [degree[t] for t in titles])[0]
rho_in = spearmanr(pr, [in_degree[t] for t in titles])[0]
rho_cites = spearmanr(pr, [cites[t] for t in titles])[0]
print(f"Spearman de PageRank con el grado {rho_degree:.2f}, con el grado de entrada {rho_in:.2f}, con las citas {rho_cites:.2f}")
```

**Lo que vemos.** PageRank sigue de cerca al grado de entrada (0,97), mucho menos al grado total (0,75) y poco a las citas en el mundo (0,30). Un artículo muy citado en el mundo puede no tener ningún enlace dentro de este conjunto. Por eso el grafo es un cuarto resultado y no una copia de las citas: mide el lugar dentro de lo que el equipo va a leer.
 
### Paso 2. Un artículo descrito por su lugar
En este paso describimos un artículo por su lugar en la red: su grado, su puesto por PageRank, su puesto por intermediación y su puesto por citas. Es un artículo que una cuenta de citas no pondría arriba. Lo elegimos antes de mirar la lista final: una guía clínica con grado medio, que está entre los artículos con más intermediación.

```python
def place_of(score):
    """Puesto de cada artículo según un puntaje, de mayor a menor.

    Qué hace: el artículo con el puntaje más alto tiene el puesto 1. Sirve para comparar
    medidas con escalas distintas (PageRank, intermediación, citas) en una misma
    línea. Los empates quedan en el orden de titles.

    Entrada:
        score: diccionario de cada título a su puntaje.

    Salida:
        Un diccionario de cada título a su puesto, de 1 a N.
    """
    return {t: i + 1 for i, t in enumerate(sorted(titles, key=lambda t: -score[t]))}

by_rank, by_between, by_cites = place_of(rank), place_of(between), place_of(cites)
print(EXAMPLE)
print(f"  grado {degree[EXAMPLE]}, puesto {by_rank[EXAMPLE]} por PageRank, puesto {by_between[EXAMPLE]} de {N} por intermediación")
print(f"  puesto {by_cites[EXAMPLE]} de {N} por citas ({int(cites[EXAMPLE]):,}). Puente: {'sí' if EXAMPLE in bridges else 'no'}")
```

```python
example_neighbours = [t for t, _ in model.wv.most_similar(EXAMPLE, topn=5)]
for t in example_neighbours:
    linked = "enlazado" if t in neighbours[EXAMPLE] else "sin enlace directo"
    print(f"  vecino node2vec: {t[:75]} ({linked})")
```

```python
# Comprobar
assert EXAMPLE in adj and EXAMPLE in bridges
assert by_between[EXAMPLE] < by_cites[EXAMPLE]
print("Artículo descrito por su lugar: OK")
```

**Lo que vemos.** La guía de prevención del accidente cerebrovascular tiene grado 10, está en el puesto 10 de 318 por intermediación y en el 187 por citas. Una cuenta de citas la dejaría en la mitad de abajo. Su lugar en la red dice que une partes del conjunto, y cuatro de sus cinco vecinos de node2vec son artículos que cita o que la citan.

### Paso 3. ¿Son estables los vecinos de node2vec?
En este paso repetimos node2vec con las tres semillas y medimos cuántos de los 5 vecinos más cercanos se repiten entre la primera semilla y las otras dos. Las caminatas son al azar, así que los vectores cambian con la semilla. Si los vecinos cambiaran casi todos, no podríamos leerlos.

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
En este paso medimos si los vecinos de node2vec comparten temas de OpenAlex más que dos artículos al azar del componente mayor. Usamos el índice de Jaccard: temas en común sobre temas en total. Los temas no entran en node2vec, así que son una prueba independiente: si los vecinos comparten temas, la red está diciendo algo sobre el contenido.

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

```python
# Comprobar
assert overlap >= 0.5
assert near > far
print("node2vec estable y con sentido: OK")
```

**Lo que vemos.** Tres de cada cuatro vecinos se repiten entre semillas, y los vecinos comparten 4,6 veces más temas que dos artículos al azar. Los vecinos de node2vec son estables y tienen sentido, aunque no son una lista exacta: una semilla puede cambiar uno de los cinco.

### Paso 5. Un dibujo del componente mayor
En este paso dibujamos el componente mayor. El color es la intermediación. Los puentes van con borde negro. El tamaño de cada punto crece con su grado. El dibujo no es una medida: la posición de cada punto cambia con la semilla del dibujo. Sirve para ver que los puentes están entre zonas de la red y no solo en el centro.

```python
# Nodos y aristas en orden: vienen de sets, y sin orden el dibujo cambia de una ejecución a otra
sub = nx.Graph()
sub.add_nodes_from(sorted(largest))
sub.add_edges_from(sorted(tuple(sorted(e)) for e in graph.subgraph(largest).edges()))
pos = nx.spring_layout(sub, seed=SEED)
fig, ax = plt.subplots(figsize=(7, 6))
nx.draw_networkx_edges(sub, pos, ax=ax, alpha=0.3)
nodes_drawn = nx.draw_networkx_nodes(sub, pos, ax=ax, node_size=[20 + 8 * degree[v] for v in sub],
                                     node_color=[between[v] for v in sub], cmap="viridis",
                                     edgecolors=["black" if v in bridges else "none" for v in sub])
fig.colorbar(nodes_drawn, ax=ax, label="Intermediación")
ax.set_title(f"Componente mayor ({len(largest)} artículos). Borde negro: puente")
ax.axis("off")
fig.tight_layout()
fig.savefig(OUTPUTS_DIR / "componente_l5.png", dpi=120)
plt.show()
```

**Hallazgo sobre el lugar (completen con sus números).** Copie los números de las celdas anteriores y escriba qué significan para la lista del equipo.

```python
place_finding = """
- Artículos aislados: ___ %. Sin vector en node2vec: ___ %.
- El artículo de ejemplo: puesto ___ por intermediación y ___ por citas.
- Vecinos de node2vec que se repiten entre semillas: ___.
- Qué significa para nuestra lista: ___.
"""
print(place_finding)
```

---
 
## Parte 7. Despliegue
 
### Paso 1. El apoyo del grafo en la tabla de apoyos
En este paso armamos `table`, una fila por artículo con el título como índice. Juntamos los tres apoyos de la semana 2 por título. Si un título repetido aparecía dos veces en la semana 2, toma el apoyo si cualquiera de sus dos filas lo tenía. Los 3 resúmenes cortos que la semana 2 dejó fuera no tienen apoyo de L3 ni de L4, y los mostramos como "sin texto". El apoyo del grafo es ser un **puente**. Las columnas de apoyo tienen los nombres de las diapositivas: `has_pattern`, `read_group`, `text_says_read` y ahora `graph_support`.

```python
supports_w2 = week2.groupby("title")[["has_pattern", "read_group", "text_says_read"]].any()
table = supports_w2.reindex(titles).fillna(False).astype(bool)   # table: una fila por artículo, el título es el índice
table.index.name = "title"
no_text = [t for t in titles if t not in supports_w2.index]
print(f"Sin texto en la semana 2: {len(no_text)}")
for t in no_text:
    print("  ", t[:70])

table["graph_support"] = table.index.isin(bridges)   # cuarto superior, sin nodos centrales
SUPPORT_COLUMNS = ["has_pattern", "read_group", "text_says_read", "graph_support"]
table["supports"] = table[SUPPORT_COLUMNS].astype(int).sum(axis=1)
table["in_view"] = table["supports"] >= MIN_SUPPORTS
before = (table[SUPPORT_COLUMNS[:3]].astype(int).sum(axis=1) >= MIN_SUPPORTS).sum()
print(f"En vista con tres resultados: {before}. Con el grafo: {table['in_view'].sum()} de {N}")
print(table["supports"].value_counts().sort_index().to_dict())
```

```python
# Comprobar
assert len(table) == N and table.index.is_unique
assert table["in_view"].sum() >= before and table["graph_support"].sum() == len(bridges)
print("Tabla de apoyos con el grafo: OK")
```

**Lo que aprendemos aquí.** El grafo suma un apoyo a los puentes, que son unos pocos artículos con enlaces. Más de la mitad de los artículos no tiene vector y el 38% está aislado, así que el grafo no puede apoyarlos: eso no los saca de la lista, solo dice que su lugar en la red no cuenta para ellos. Ningún artículo de nutrición pasa la alerta de nodo central. En los extractos de Wikipedia sí hay nodos centrales, y los puentes los dejan fuera. Con el grafo, la lista pasa de 52 a 69 artículos en vista. Solo uno tiene los cuatro apoyos.
 
### Paso 2. Guardar el grafo
En este paso guardamos `outputs/grafo_l5.csv`, con una fila por artículo. Los nombres de las columnas van en español, como en las semanas anteriores. `vecinos_n2v` lleva los 5 vecinos separados por `|`, y queda vacía para los artículos sin vector. La L6 lee este archivo para traer el apoyo del grafo sin repetir los cálculos.

```python
graph_table = pd.DataFrame({
    "title": titles,
    "grado": [degree[t] for t in titles],
    "pagerank": [round(rank[t], 6) for t in titles],
    "intermediacion": [between[t] for t in titles],
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

```python
# Comprobar
saved = pd.read_csv(graph_path, keep_default_na=False)
assert list(saved.columns) == ["title", "grado", "pagerank", "intermediacion", "aislado", "alerta_centro", "sin_vector_n2v", "vecinos_n2v", "supports", "in_view"]
assert len(saved) == N
print("grafo_l5.csv: OK")
```

### Paso 3. Qué cambiaría la decisión
En este paso anotamos en `pregunta.json` cómo entra el grafo y qué lo cambiaría. La tarjeta viaja con el equipo de lección en lección. Así, quien lea la lista sabe por qué un artículo tiene el apoyo del grafo y qué regla lo decidió.

```python
question_card["graph_use"] = {
    "how_it_enters": "Un artículo recibe un apoyo si es un puente: está en el cuarto superior por intermediación entre los artículos con enlaces, y no es un nodo central.",
    "reading": "El grafo solo ve las citas dentro del conjunto. Un artículo aislado no tiene lugar, no es malo.",
    "bridges": len(bridges),
    "what_changes_it": ["otro corte que el cuarto superior", "otra regla para los nodos centrales", "más artículos o más enlaces en el conjunto"],
}
QUESTION_PATH.write_text(json.dumps(question_card, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(question_card["graph_use"], ensure_ascii=False, indent=1))
```

**Su turno.** Elija un artículo de la tabla con dos apoyos o más. Escriba en dos frases qué dice su lugar en la red y qué cambiaría si quitáramos el apoyo del grafo.

```python
my_paper = """
Escriba aquí el título, su lugar en la red y qué cambiaría sin el grafo.
"""
print(my_paper)
```

### Paso 4. Comprobación final
En este paso revisamos que el cuaderno dejó todo lo que el cuaderno de grupo y la L6 necesitan. Las dos líneas de texto que usted escribe cuentan como comprobaciones. Si alguna dice incompleto, vuelva a esa celda.

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
    ("Apoyos de la semana 2", lambda: len(week2) > 0),
    ("Hallazgo sobre el lugar escrito", lambda: "___" not in place_finding),
    ("Un artículo leído por su lugar", lambda: "Escriba aquí" not in my_paper),
]
passed = sum(_check_ok(n, f) for n, f in checks)
print(f"\nL5_CHECKS={passed}/{len(checks)}")
if passed == len(checks):
    print("L5_OK. Siga con la L6. En el cuaderno de grupo hará lo mismo con los enlaces de Wikipedia.")
```

<!-- end NOTEBOOK: -->
