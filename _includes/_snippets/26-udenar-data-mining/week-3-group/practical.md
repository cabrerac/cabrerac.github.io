<!-- NOTEBOOK: -->

## Instrucciones
 
**Propósito.** Cuaderno de grupo de la semana 3 (Lecciones 5 y 6). Es el proyecto. En los laboratorios el equipo del consejo miró las citas entre sus artículos y predijo una etiqueta dada. Aquí su grupo hace lo mismo con **su departamento** en Wikipedia. La decisión sigue igual: **qué artículos debe abrir primero una persona nueva**. Al final, cada artículo tiene hasta cinco apoyos, y la **lista inicial** son los artículos con al menos dos.
 
**Requisito.** Complete primero los cuadernos individuales [L5](https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-data-mining/l5-graphs.ipynb) y [L6](https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-data-mining/l6-prediction.ipynb). Tengan a mano `pregunta.json`, `marcas.csv` y `outputs/en_vista.csv` de su cuaderno de grupo de la semana 2.
 
**Cómo trabajar.** Cada paso empieza con **En este paso**. Los pasos con una celda `# SU CÓDIGO` terminan con una celda `# Comprobar`. La tabla de abajo dice qué celda del cuaderno individual seguir. Algunos pasos vienen resueltos. Si un `assert` falla, corrija su celda antes de seguir. Los nombres del código van en inglés. Los comentarios y las explicaciones van en español.
 
**Entrega Moodle (martes 24 nov 2026, 23:59 Colombia):** ZIP `week-3-<group_id>.zip` con `week-3-group-<group_id>.ipynb` (este cuaderno ejecutado y renombrado), `pregunta.json`, `marcas.csv` de la semana 2, `outputs/grafo.csv`, `outputs/prediccion.csv`, `outputs/lista_inicial.csv`, `project-title-es.txt` y `project-abstract-es.txt`. El mismo cuaderno, con los arreglos después de la devolución, va en el ZIP del proyecto el martes 1 de diciembre.
 
**Mapa del cuaderno**
 
| Parte | Fase CRISP-DM | Qué sale | Qué copiar, dónde está |
|-------|---------------|----------|------------------------|
| 0 | Configuración | Grupo, etiqueta, parámetros y funciones dadas | Dado |
| 1 | Comprensión del negocio | La tarjeta y los tres apoyos de la semana 2 | Dado |
| 2 | Comprensión de los datos | El extracto y lo que cambia con Wikipedia | Dado |
| 3 | Preparación de los datos | La lista de enlaces, los dos grafos, el componente mayor y la tabla de la L6 | L5, Parte 4, y L6, Parte 4 |
| 4 | Modelado | Los seis métodos | L5, Parte 5, y L6, Parte 5 |
| 5 | Evaluación | La alerta de nodo central, un artículo por su lugar, aciertos y errores | L5, Parte 6, y L6, Parte 6 |
| 6 | Despliegue | La lista inicial, la sensibilidad, los archivos, el título y el resumen | L5, Parte 7, y L6, Parte 7 |

---
 
## Parte 0. Configuración
 
Esta parte viene resuelta. Ejecútela y lea lo que imprime.
 
### Paso 1. Su grupo y su etiqueta
En este paso elige su grupo. Cambie solo `GROUP`. `LABEL` es la etiqueta de la L6 para los cinco grupos. La elige el profesor, y hasta que la elija queda `"label"`, la categoría que ya trae el extracto. `LABEL_COLUMNS` dice qué columna del extracto lee cada etiqueta. Si la columna no está en el extracto, el cuaderno se detiene con un error en vez de usar otra etiqueta sin avisar.

```python
GROUP = "G1"        # cambie a G2, G3, G4 o G5
LABEL = "label"     # [POR DECIDIR, pregunta abierta 1] la etiqueta que elija el profesor. "label": la categoría del extracto
# [POR DECIDIR, pregunta abierta 1] la columna del extracto que lee cada etiqueta
LABEL_COLUMNS = {"label": "label", "tiene_imagen": "has_image", "tiene_ficha": "has_infobox", "multilingue": "n_wikipedias"}
if LABEL not in LABEL_COLUMNS:
    raise ValueError(f"LABEL debe ser una de {sorted(LABEL_COLUMNS)}, no {LABEL!r}")

EXTRACTS = {
    "G1": ("Pobreza", "pobreza.csv"),
    "G2": ("Vivienda", "vivienda.csv"),
    "G3": ("Medio ambiente", "medio-ambiente.csv"),
    "G4": ("Agricultura", "agricultura.csv"),
    "G5": ("Salud mental", "salud-mental.csv"),
}
# Las categorías del tema de la L4, las mismas de la semana 2
TARGETS = {
    "G1": ["Hambrunas", "Hambre", "Bancos de alimentos"],
    "G2": ["Hipotecas", "Arrendamiento", "Huelgas de alquileres", "Vivienda asequible", "Vivienda pública"],
    "G3": ["Conservacionismo"],
    "G4": ["Agrarismo", "Organizaciones agrícolas"],
    "G5": ["Trastornos mentales", "Psiquiatría"],
}
DEPARTMENT, FILENAME = EXTRACTS[GROUP]
print(f"Grupo {GROUP}: {DEPARTMENT} ({FILENAME}). Etiqueta de la L6: {LABEL}")
```

### Paso 2. Librerías y parámetros compartidos
En este paso instalamos lo que falte, importamos las librerías y copiamos los parámetros de las lecciones anteriores **sin cambiarlos**. Todos los grupos usan los mismos.

```python
import importlib.util
import subprocess
import sys

if importlib.util.find_spec("gensim") is None:
    print("Instalando gensim (una sola vez por sesión)...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "gensim"], check=True)

import json
import math
import random
import time
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import requests
from gensim.models import Word2Vec
from scipy.stats import chi2_contingency, spearmanr
from sklearn.base import clone
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import StratifiedKFold, cross_val_predict, train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

DATA_DIR = Path("data")
OUTPUTS_DIR = Path("outputs")
DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
BASE_URL = "https://cabrerac.github.io/assets/data/26-udenar-data-mining"

# Desde L2, sin cambios
SUPPORT_SHARE = 0.03
SUPPORT_MIN = 5
SEED = 7

# L4, sin cambios
FLAGGED_SHARE = 0.20
FLAGGED_MIN = 40
POSITIVE_SHARE = 0.10
POSITIVES_MIN = 30
C_REG = 10
N_FOLDS = 5

# Decisión, L3 en adelante
MIN_SUPPORTS = 2

# L5, sin cambios
HUB_SHARE = 0.10          # un nodo enlazado a al menos el 10% de los otros es una alerta
MIN_LINKS = 5             # nunca menos de 5 enlaces para una alerta
DAMPING = 0.85
NODE_DIMENSIONS = 32
WALKS_PER_NODE = 10
WALK_LENGTH = 20
P_RETURN = 1.0
Q_INOUT = 0.5
WINDOW = 5
N2V_SEEDS = (7, 8, 9)
N_RANDOM_PAIRS = 3000

# L6, sin cambios
HIDDEN_UNITS = 8
PENALTY = 1.0
N_TREES = 200
MARGIN = 0.02
SPLIT_SEEDS = (7, 8, 9, 10, 11)


def support_floor(n_texts: int) -> int:
    """Soporte mínimo: max(SUPPORT_MIN, ceil(SUPPORT_SHARE * n)), como en la L2."""
    return max(SUPPORT_MIN, math.ceil(SUPPORT_SHARE * n_texts))


def n_flagged(n: int) -> int:
    """Tamaño del conjunto apartado: max(FLAGGED_MIN, ceil(FLAGGED_SHARE * n))."""
    return max(FLAGGED_MIN, math.ceil(FLAGGED_SHARE * n))


def min_positives(n: int) -> int:
    """Filas que necesita una clase: max(POSITIVES_MIN, ceil(POSITIVE_SHARE * n))."""
    return max(POSITIVES_MIN, math.ceil(POSITIVE_SHARE * n))


def hub_threshold(n, min_links=MIN_LINKS):
    """Enlaces que necesita un nodo para ser una alerta: al menos el 10% de los otros, nunca menos de min_links."""
    return max(min_links, math.ceil(HUB_SHARE * (n - 1)))


print(f"Con 300 artículos: alerta desde {hub_threshold(300)} enlaces, {n_flagged(300)} apartados, clases de al menos {min_positives(300)}")
```

### Paso 3. Funciones dadas de la L5 y la L6
En este paso traemos tres funciones: las caminatas de node2vec (igual que en la L5), `n_claims_without` (igual que en la L6) y `vote_of`, que dice qué clase eligen al menos 2 de los 3 métodos. Con una etiqueta de dos clases, `vote_of` es lo mismo que `votes >= 2` de la L6. Con la categoría del extracto, que tiene varias clases, hace falta esta versión.

```python
def node2vec_walks(adj, walks_per_node, walk_length, p, q, seed):
    """Caminatas de node2vec de la L5. Nodos y vecinos ordenados: la misma semilla da las mismas caminatas."""
    rng, nodes, walks = random.Random(seed), sorted(adj), []
    for _ in range(walks_per_node):
        rng.shuffle(nodes)
        for start in nodes:
            walk = [start]
            while len(walk) < walk_length:
                options = sorted(adj[walk[-1]])
                if len(walk) == 1:
                    walk.append(rng.choice(options))
                    continue
                before = walk[-2]
                weights = [1 / p if x == before else 1.0 if x in adj[before] else 1 / q for x in options]
                walk.append(rng.choices(options, weights=weights)[0])
            walks.append([str(x) for x in walk])
    return walks


PROPERTY_COLUMN = {"P18": "has_image"}     # propiedad de Wikidata -> columna del extracto
LABEL_PROPERTY = {"tiene_imagen": "P18"}  # etiquetas que son una propiedad contada en n_claims


def n_claims_without(table, label):
    """Devuelve n_claims sin la propiedad de Wikidata que define la etiqueta (la función de la L6)."""
    prop = LABEL_PROPERTY.get(label)
    if prop is None:
        return table["n_claims"].astype(int)
    column = PROPERTY_COLUMN[prop]
    return (table["n_claims"] - table[column]).astype(int)


def vote_of(predictions):
    """Para cada fila, la clase que dicen al menos 2 de los 3 métodos, o None si los tres dicen algo distinto."""
    voted = []
    for row in zip(*predictions):
        values, counts = np.unique(np.array(row, dtype=str), return_counts=True)
        voted.append(str(values[counts.argmax()]) if counts.max() >= 2 else None)
    return voted


def download_data(name: str, folder: Path = DATA_DIR) -> Path:
    """Descarga un archivo de datos del curso una sola vez."""
    dest = folder / name
    if dest.is_file() and dest.stat().st_size > 0:
        print(f"Ya en caché: {dest}")
        return dest
    response = requests.get(f"{BASE_URL}/{name}", timeout=60)
    response.raise_for_status()
    dest.write_bytes(response.content)
    print(f"Descargado: {dest}")
    return dest


print(vote_of([["a", "b", "c"], ["a", "c", "d"], ["b", "c", "e"]]))
```

---
 
## Parte 1. Comprensión del negocio
 
### Paso 1. La tarjeta y los apoyos de la semana 2
En este paso leemos `pregunta.json` y `outputs/en_vista.csv` de la semana 2. Ese archivo trae los tres apoyos de cada artículo: patrón, grupo y texto.

```python
QUESTION_PATH = Path("pregunta.json")
question_card = json.loads(QUESTION_PATH.read_text(encoding="utf-8"))
week2 = pd.read_csv(OUTPUTS_DIR / "en_vista.csv", keep_default_na=False)
for c in ["has_pattern", "read_group", "text_says_read"]:
    week2[c] = week2[c].astype(str) == "True"
print(question_card["question"])
print(f"Semana 2: {len(week2)} artículos, {week2['in_view'].astype(str).eq('True').sum()} en vista con tres resultados")
```

```python
# Comprobar
assert {"question", "pattern_use", "group_use", "text_use"} <= set(question_card)
assert {"title", "has_pattern", "read_group", "text_says_read"} <= set(week2.columns)
print("Tarjeta y apoyos de la semana 2: OK")
```

### Paso 2. Qué significa el grafo para la persona nueva
En este paso escriban, antes de mirar los resultados, qué esperan de la red de su departamento. Un enlace en Wikipedia es una mención en el texto, no una cita. ¿Qué artículo creen que será el más enlazado? ¿Debería abrirlo primero una persona nueva?

```python
graph_expectation = """
Escriban aquí, en dos frases, qué esperan del grafo y qué artículo creen que será el más enlazado.
"""
print(graph_expectation)
```

---
 
## Parte 2. Comprensión de los datos
 
### Paso 1. El extracto sin títulos repetidos
En este paso descargamos el extracto y quitamos los títulos repetidos, porque un nodo es un título.

```python
raw = pd.read_csv(download_data(FILENAME), keep_default_na=False)
df = raw.drop_duplicates("title").reset_index(drop=True)
N = len(df)
titles = list(df["title"])
print(f"{len(raw)} filas, {N} artículos sin repetidos")
```

```python
# Comprobar
assert N == len(set(titles)), "Hay títulos repetidos"
assert {"title", "links", "kind", "label"} <= set(df.columns), "Faltan columnas del extracto"
print(f"Extracto: OK ({N} artículos)")
```

### Paso 2. Los enlaces dentro del extracto
En este paso, dado, contamos los enlaces. El extracto ya guarda solo los enlaces de la entradilla que apuntan a otro artículo del mismo extracto, así que todos cuentan para el grafo. Miramos cuántos artículos no enlazan a nadie.

```python
listed = [[t.strip() for t in str(links).split("|") if t.strip()] for links in df["links"]]
print(f"Enlaces escritos: {sum(map(len, listed))}. Artículos sin ningún enlace propio: {sum(len(l) == 0 for l in listed)} de {len(listed)}")
```

```python
# Comprobar
assert len(listed) == N
assert all(t in set(titles) for links in listed for t in links), "Hay enlaces a artículos fuera del extracto"
print("Enlaces dentro del extracto: OK")
```

### Paso 3. Los atributos de la L6
En este paso, dado, miramos las cinco entradas fijas y la etiqueta. Fíjense en cuántos artículos no tienen fecha y en cuántos tienen `kind = Other`.

```python
print("kind:", df["kind"].value_counts().head(6).to_dict())
print(f"Con fecha: {pd.to_numeric(df['inception_year'], errors='coerce').notna().mean():.0%}. Con país: {df['has_country'].astype(str).eq('1').mean():.0%}. Con imagen: {df['has_image'].astype(str).eq('1').mean():.0%}")
print("n_claims:", pd.to_numeric(df["n_claims"], errors="coerce").describe().round(1).to_dict())
```

**Lo que aprendemos aquí.** Las cinco entradas de la L6 son pobres. La fecha casi siempre falta, así que el año llenado con la mediana dice poco, y `kind` casi siempre es `Other`. La marca `has_date` dice si Wikidata conoce la fecha, y en algunos departamentos eso distingue tipos de artículo (una hambruna tiene fecha, un concepto no). Si la L6 no supera a la clase mayor, una parte de la razón está aquí.

### Lo que cambia con Wikipedia
 
| Qué cambia | Laboratorio (artículos) | Grupo (Wikipedia) |
| --- | --- | --- |
| Enlaces | citas dentro del conjunto, 38% aislados | enlaces entre artículos, 14% a 27% aislados |
| Nodo central | ninguno pasa del 8% | el artículo más enlazado (14% a 30%), y de 1 a 9 nodos centrales por extracto, es una alerta |
| Sin vector en node2vec | 170 de 318 (fuera del componente mayor) | 17% a 31% |
| Etiqueta L6 | `internacional` (n_countries >= 2), sin los 42 sin afiliación | `LABEL`, la que elija el profesor |
| Entradas L6 | year, n_authors, venue_type, is_oa, work_type | las cinco fijas: kind, has_country, has_date con el año imputado, has_image, `n_claims_without(...)` |
| Fecha | year completo | inception_year falta en 85% a 96%. La marca `has_date` dice si hay fecha, el año imputado es casi constante. Sin la marca de faltante del imputador, que repetiría `has_date` |
| `kind` | no aplica | "Other" en 78% a 100% de las filas, aporta poco |
 
---
 
## Parte 3. Preparación de los datos
 
### Paso 1. La lista de enlaces (L5, Parte 4, Paso 1)
En este paso construya `links_out` (con dirección, solo enlaces a títulos del extracto) y `neighbours` (sin dirección), con el código de la L5. Use `df` en lugar de `papers`.

```python
# SU CÓDIGO
# Cree links_out y neighbours, dos dict de sets con una clave por título.
```

```python
# Comprobar
assert set(links_out) == set(neighbours) == set(titles)
assert all(a in neighbours[b] for a in neighbours for b in neighbours[a])
print(f"Enlaces: OK ({sum(len(v) for v in links_out.values())} con dirección, {sum(len(v) for v in neighbours.values()) // 2} sin dirección)")
```

### Paso 2. Los dos grafos y el componente mayor (L5, Parte 4, Pasos 2 y 3)
En este paso construya `directed` y `graph` con networkx, y después `largest` (el componente mayor), `adj` (los vecinos dentro de él) y `no_vector` (los artículos fuera de él).

```python
# SU CÓDIGO
# Cree directed (nx.DiGraph), graph (nx.Graph), largest, adj y no_vector.
```

```python
# Comprobar
assert graph.number_of_nodes() == N and len(adj) + len(no_vector) == N
assert len(largest) >= 0.5 * N, "En Wikipedia el componente mayor tiene al menos la mitad de los artículos"
print(f"Grafos: OK. {graph.number_of_edges()} enlaces, {sum(1 for v in graph if graph.degree(v) == 0)} aislados, componente mayor {len(largest)} ({len(largest) / N:.0%}), sin vector {len(no_vector)}")
```

### Paso 3. La tabla de la L6 (L6, Parte 4, Paso 1)
En este paso viene dada la tabla de atributos. Las entradas son las cinco fijas. `kind` deja como "Other" los tipos con menos de `support_floor(n)` artículos. `has_date` marca si hay año, y el año faltante se llena después con la mediana. Por eso la preparación del grupo no agrega la marca de faltante del imputador (`add_indicator=False`): sería una copia de `has_date`. `n_claims_without` quita de `n_claims` la propiedad de la etiqueta, si la etiqueta es una propiedad.

```python
attributes = df.set_index("title")
kinds = attributes["kind"].value_counts()
attributes["kind"] = attributes["kind"].where(attributes["kind"].isin(kinds[kinds >= support_floor(N)].index), "Other")
attributes["year"] = pd.to_numeric(attributes["inception_year"], errors="coerce")
attributes["has_date"] = attributes["year"].notna().astype(int)
for c in ["has_country", "has_image", "n_claims"]:
    attributes[c] = pd.to_numeric(attributes[c], errors="coerce").fillna(0).astype(int)
result = n_claims_without(attributes, LABEL)
attributes["n_claims_without"] = result

NUMBER_COLUMNS = ["year", "has_date", "has_country", "has_image", "n_claims_without"]
if LABEL == "tiene_imagen":   # [POR DECIDIR, pregunta abierta 1]
    NUMBER_COLUMNS.remove("has_image")   # la etiqueta no puede ser una entrada
CATEGORY_COLUMNS = ["kind"]
# [POR DECIDIR, pregunta abierta 1] la etiqueta sale de su columna en LABEL_COLUMNS, nunca de otra
label_column = LABEL_COLUMNS[LABEL]
if label_column not in attributes.columns:
    raise ValueError(f"La etiqueta {LABEL!r} necesita la columna {label_column!r}, que el extracto todavía no trae.")
if LABEL == "label":
    y = attributes["label"].astype(str)
elif LABEL == "multilingue":
    y = (pd.to_numeric(attributes[label_column], errors="coerce").fillna(0) >= 10).astype(int)
else:
    y = pd.to_numeric(attributes[label_column], errors="coerce").fillna(0).astype(int)
print(f"Con fecha: {attributes['has_date'].mean():.0%}. kind = Other: {(attributes['kind'] == 'Other').mean():.0%}")
print("Clases de la etiqueta:", y.value_counts().to_dict())
```

```python
# Comprobar
assert (result >= 0).all() and (attributes.loc[attributes["has_image"] == 1, "n_claims"] >= 1).all()
if LABEL in LABEL_PROPERTY:
    assert ((attributes["n_claims"] - result) == y).all()
else:
    assert (result == attributes["n_claims"]).all()
print("n_claims sin la propiedad de la etiqueta: OK")
```

### Paso 4. El conjunto apartado y la preparación (L6, Parte 4, Pasos 2 y 3)
En este paso aparte `n_flagged(N)` filas con `train_test_split` (estratificado, `random_state=SEED`), sobre `attributes[NUMBER_COLUMNS + CATEGORY_COLUMNS]`. Llame `train` y `test` a las dos partes y `y_train`, `y_test` a sus etiquetas. Después cree `prepare`, el `ColumnTransformer` de la L6, con un cambio: `add_indicator=False` en los números, porque `has_date` ya es la marca del año faltante.

```python
# SU CÓDIGO
# Cree train, test, y_train, y_test y prepare.
```

```python
# Comprobar
assert len(test) == n_flagged(N) and not set(train.index) & set(test.index)
assert set(prepare.fit(train).get_feature_names_out()) >= {"num__has_date", "num__n_claims_without"} - {f"num__{LABEL}"}
print(f"Apartadas {len(test)}, para aprender {len(train)}: OK")
```

---
 
## Parte 4. Modelado
 
### M1. Grado, alerta y PageRank (L5, Parte 5)
En este paso cree `degree`, `hubs` (con `hub_threshold`), `top_degree` (los 10 de más grado), `rank` (con `nx.pagerank(directed, alpha=DAMPING)`) y `top_rank` (los 10 primeros por PageRank).

```python
# SU CÓDIGO
# Cree degree, hubs, top_degree, rank y top_rank.
```

```python
# Comprobar
assert all(degree[v] >= hub_threshold(N) for v in hubs)
assert abs(sum(rank.values()) - 1) < 1e-6
print(f"Grado y PageRank: OK. Nodos centrales ({len(hubs)}): {', '.join(sorted(hubs))}")
```

### Grado contra PageRank (parada en vivo)
En este paso, dado, ponemos los 10 primeros por PageRank junto a su grado. Mostramos valores de grado, no puestos, porque el puesto depende de cómo se ordenan los empates.

```python
for v in top_rank:
    mark = "" if v in top_degree else "  <- no está entre los 10 de más grado"
    print(f"  PageRank {rank[v]:.3f}, grado {degree[v]:3d}{' (nodo central)' if v in hubs else ''}  {v}{mark}")
print(f"El grado más bajo entre los 10 de más grado: {min(degree[v] for v in top_degree)}")
```

```python
fig, ax = plt.subplots(figsize=(6, 3.5))
ax.hist(list(degree.values()), bins=range(0, max(degree.values()) + 2), color="#4C72B0")
ax.axvline(hub_threshold(N), color="#C44E52", linestyle="--", label=f"alerta ({hub_threshold(N)} enlaces)")
ax.set_xlabel("Grado")
ax.set_ylabel("Artículos")
ax.set_title(f"Grado en {DEPARTMENT}")
ax.legend()
fig.tight_layout()
fig.savefig(OUTPUTS_DIR / "grado.png", dpi=120)
plt.show()
```

**Lo que aprendemos aquí.** PageRank sigue casi siempre al grado de entrada: un artículo sube si lo enlazan muchos, y sube más si lo enlazan artículos que a su vez reciben muchos enlaces. Los artículos que PageRank pone arriba sin tener mucho grado son los interesantes para la persona nueva: los enlazan pocos, pero importantes.

### Un ejemplo pequeño de intermediación
En este paso, dado, calculamos la intermediación en un grafo de juguete antes de usarla en el extracto. Dos triángulos (A, B, C y E, F, G) unidos por un camino C, D, E. D tiene solo dos enlaces, pero todo camino más corto de un triángulo al otro pasa por D.

```python
toy_graph = nx.Graph([("A", "B"), ("B", "C"), ("A", "C"), ("C", "D"), ("D", "E"), ("E", "F"), ("F", "G"), ("E", "G")])
toy_between = nx.betweenness_centrality(toy_graph, normalized=True)
for v in sorted(toy_graph):
    print(f"  {v}: grado {toy_graph.degree[v]}, intermediación {toy_between[v]:.2f}")
```

```python
# Comprobar
assert max(toy_between, key=toy_between.get) == "D", "D debería tener la intermediación más alta"
assert toy_graph.degree["D"] == 2 and toy_between["A"] == 0
print("Grado bajo, intermediación alta: OK")
```

Un puente es eso en su extracto: un artículo con pocos enlaces que une dos partes de la red. Por eso el apoyo del grafo excluye a los nodos centrales. Un nodo central también tiene intermediación alta, pero ya lo encuentra cualquiera.

### M2. Intermediación y puentes (L5, Parte 5)
En este paso cree `between`, **redondeado a 9 decimales** como en la L5, y `bridges`: artículos con enlaces, en el cuarto superior por intermediación, que no son nodos centrales.

```python
# SU CÓDIGO
# Cree between (redondeado) y bridges.
```

```python
# Comprobar
assert all(between[v] == round(between[v], 9) for v in between)
assert len(bridges) >= 1 and not set(bridges) & set(hubs)
print(f"Puentes: OK ({len(bridges)}, ninguno es nodo central)")
```

**Lo que aprendemos aquí.** Miren cuántos de sus puentes están en el cuarto superior por intermediación y no son nodos centrales. Esos artículos son los que el grafo agrega a la lista. Si un puente les parece raro, ábranlo: muchas veces es un artículo general que une dos temas del departamento.

### M3. node2vec (L5, Parte 5)
En este paso entrene node2vec con las tres semillas de `N2V_SEEDS`. Guarde en `neighbours_by_seed` una lista con un diccionario por semilla: para cada artículo del componente mayor, sus 5 vecinos más cercanos. Use `workers=1`.

```python
# SU CÓDIGO
# Cree neighbours_by_seed (lista de 3 dict) y model (el de la primera semilla).
```

```python
# Comprobar
assert len(neighbours_by_seed) == 3 and set(neighbours_by_seed[0]) == set(adj)
assert not set(no_vector) & set(model.wv.index_to_key)
print("node2vec: OK (ningún artículo sin vector tiene coseno)")
```

### Una caminata de node2vec
En este paso, dado, miramos una caminata. node2vec aprende los vectores a partir de miles de caminatas como esta, igual que Word2Vec aprende palabras a partir de frases. Con `Q_INOUT = 0.5` la caminata prefiere alejarse del nodo anterior, así que explora la red más allá de los vecinos directos.

```python
start = top_rank[0] if top_rank[0] in adj else sorted(adj)[0]
demo_walk = next(w for w in node2vec_walks(adj, 1, WALK_LENGTH, P_RETURN, Q_INOUT, SEED) if w[0] == start)
print(" -> ".join(demo_walk[:8]), "...")
print(f"Pasos que salen de los vecinos directos de {start}: {sum(v not in adj[start] and v != start for v in demo_walk)} de {len(demo_walk)}")
```

```python
# Comprobar
assert len(demo_walk) == WALK_LENGTH
assert all(b in adj[a] for a, b in zip(demo_walk, demo_walk[1:])), "Cada paso debe seguir un enlace"
print("Caminata: OK")
```

**Pregunta de lectura.** Grover y Leskovec (2016), *node2vec: Scalable Feature Learning for Networks*, sección 3.2.2 ([arXiv](https://arxiv.org/abs/1607.00653)). ¿Qué pasa con las caminatas cuando `q` es menor que 1, y qué tipo de vecinos produce eso? Respondan con un artículo de su extracto.

```python
n2v_answer = """
Escriban aquí su respuesta, en dos frases, con un artículo de su extracto.
"""
print(n2v_answer)
```

### M4, M5 y M6. Los tres métodos de la L6 (L6, Parte 5)
En este paso cree `lr`, `forest` y `network` con los mismos argumentos de la L6, y `models`, la lista de los tres dentro de `make_pipeline(prepare, ...)`. Entrénelos con `train` y guarde sus predicciones en las filas apartadas en `test_predictions` (una lista de tres).

```python
# SU CÓDIGO
# Cree lr, forest, network, models y test_predictions.
```

```python
# Comprobar
assert len(models) == 3 and all(len(p) == len(test) for p in test_predictions)
print("Tres métodos de la L6 entrenados: OK")
```

---
 
## Parte 5. Evaluación
 
### Paso 1. La alerta de nodo central
En este paso, dado, miramos los nodos centrales. En Wikipedia el artículo del departamento, o el más general, se enlaza con muchos otros. No es una mala señal, pero no ayuda a elegir: casi todo pasa por él. Por eso los puentes no incluyen nodos centrales.

```python
for v in sorted(hubs, key=lambda v: -degree[v]):
    print(f"  grado {degree[v]:3d} ({degree[v] / (N - 1):.0%}), PageRank {rank[v]:.3f}  {v}")
print(f"El primero por PageRank: {top_rank[0]}. ¿Es nodo central? {'sí' if top_rank[0] in hubs else 'no'}")
```

### Paso 2. PageRank sigue al grado de entrada
En este paso, dado, comparamos PageRank con el grado total y con el grado de entrada (cuántos artículos del extracto lo enlazan). Pregunta de lectura de Page et al. (1998), p. 3, en la [copia archivada](https://web.archive.org/web/20241231011600/http://ilpubs.stanford.edu:8090/422/): ¿cuándo están en desacuerdo el grado y PageRank?

```python
in_degree = dict(directed.in_degree())
pr = [rank[t] for t in titles]
print(f"Spearman de PageRank con el grado {spearmanr(pr, [degree[t] for t in titles])[0]:.2f}, con el grado de entrada {spearmanr(pr, [in_degree[t] for t in titles])[0]:.2f}")
reading_answer = """
Escriban aquí su respuesta a la pregunta de lectura, con un artículo de su extracto.
"""
print(reading_answer)
```

### Paso 3. Un artículo descrito por su lugar
En este paso elija un artículo del componente mayor que no sea nodo central y descríbalo por su lugar: grado, PageRank, intermediación y vecinos de node2vec. Si no sabe cuál elegir, use un artículo con mucho PageRank y poco grado, como *Medicina psicosomática* en salud mental o *Abono verde* en agricultura. Si su artículo no tiene vector, la celda lo dice.

```python
candidates = [v for v in top_rank if v not in hubs and v not in top_degree] or [v for v in top_rank if v not in hubs]
MY_ARTICLE = candidates[0]   # cambie por el título que quiera describir

by_rank = {t: i + 1 for i, t in enumerate(sorted(titles, key=lambda t: -rank[t]))}
by_between = {t: i + 1 for i, t in enumerate(sorted(titles, key=lambda t: -between[t]))}
print(f"{MY_ARTICLE}: grado {degree[MY_ARTICLE]}, puesto {by_rank[MY_ARTICLE]} por PageRank, puesto {by_between[MY_ARTICLE]} por intermediación, puente: {'sí' if MY_ARTICLE in bridges else 'no'}")
if MY_ARTICLE in adj:
    for t in neighbours_by_seed[0][MY_ARTICLE]:
        print(f"  vecino node2vec: {t} ({'enlazado' if t in neighbours[MY_ARTICLE] else 'sin enlace directo'})")
else:
    print("  sin vector: está fuera del componente mayor")
```

### Paso 4. ¿Son estables y tienen sentido los vecinos? (L5, Parte 6, Pasos 3 y 4)
En este paso calcule `overlap` (la parte de los 5 vecinos de la primera semilla que se repite en las otras dos, promedio sobre el componente mayor), `near` (el Jaccard de categorías entre cada artículo y sus vecinos) y `far` (el Jaccard de `N_RANDOM_PAIRS` pares al azar con `random.Random(SEED)`), como en la L5. Las categorías están en la columna `categories`.

```python
# SU CÓDIGO
# Cree overlap, near y far.
```

```python
# Comprobar
assert overlap >= 0.5, "Los vecinos de node2vec cambian demasiado con la semilla"
assert near > far
print(f"Vecinos estables ({overlap:.2f}) y con más categorías en común que al azar ({near:.3f} contra {far:.3f}): OK")
```

### Paso 5. Los artículos sin vector (parada en vivo)
En este paso, dado, dibujamos el componente mayor y contamos los artículos sin vector. Un artículo sin vector no es malo: está fuera de la parte conectada de la red, así que node2vec no lo puede ubicar.

```python
# Nodos y aristas en orden: vienen de sets, y sin orden el dibujo cambia de una ejecución a otra
sub = nx.Graph()
sub.add_nodes_from(sorted(largest))
sub.add_edges_from(sorted(tuple(sorted(e)) for e in graph.subgraph(largest).edges()))
pos = nx.spring_layout(sub, seed=SEED)
fig, ax = plt.subplots(figsize=(7, 6))
nx.draw_networkx_edges(sub, pos, ax=ax, alpha=0.3)
drawn = nx.draw_networkx_nodes(sub, pos, ax=ax, node_size=[15 + 4 * degree[v] for v in sub], node_color=[between[v] for v in sub],
                               cmap="viridis", edgecolors=["black" if v in bridges else "none" for v in sub])
fig.colorbar(drawn, ax=ax, label="Intermediación")
ax.set_title(f"Componente mayor de {DEPARTMENT} ({len(largest)} artículos). Borde negro: puente")
ax.axis("off")
fig.tight_layout()
fig.savefig(OUTPUTS_DIR / "componente.png", dpi=120)
plt.show()
print(f"Sin vector: {len(no_vector)} de {N} ({len(no_vector) / N:.0%}). Aislados: {sum(degree[v] == 0 for v in titles)}")
```

```python
# Comprobar
assert len(no_vector) == N - len(largest)
assert not set(no_vector) & set(adj), "Un artículo sin vector no puede estar en el componente mayor"
print("Sin vector fuera del componente mayor: OK")
```

### Paso 6. Aciertos y errores de la L6 (L6, Parte 6)
En este paso, dado, contamos los aciertos de cada método y de la clase mayor en las filas apartadas, y en cinco pliegues sobre las filas de entrenamiento. [POR DECIDIR, pregunta abierta 1] Con una etiqueta de varias clases miramos la exactitud y el F1 macro (el promedio del F1 de cada clase), en las apartadas y en los cinco pliegues. Las clases con menos de `min_positives(N)` artículos se marcan, no se juntan.

```python
folds = StratifiedKFold(n_splits=N_FOLDS, shuffle=True, random_state=SEED)
train_predictions = [cross_val_predict(m, train, y_train, cv=folds) for m in models]
baseline = DummyClassifier(strategy="most_frequent").fit(train, y_train)
names = ["clase mayor", "regresión logística", "bosque", "una capa oculta"]
rows = []
for name, p_test, p_cv in zip(names, [baseline.predict(test)] + test_predictions, [baseline.predict(train)] + train_predictions):
    rows.append({"método": name, "exactitud apartadas": round(accuracy_score(y_test, p_test), 3),
                 "F1 macro apartadas": round(f1_score(y_test, p_test, average="macro"), 3),
                 "exactitud cinco pliegues": round(accuracy_score(y_train, p_cv), 3),
                 "F1 macro cinco pliegues": round(f1_score(y_train, p_cv, average="macro"), 3)})
evaluation = pd.DataFrame(rows).set_index("método")
small = {c: n for c, n in y.value_counts().items() if n < min_positives(N)}
print(f"Clases con menos de {min_positives(N)} artículos: {small}")
evaluation
```

**Lo que aprendemos aquí.** Con muchas clases pequeñas, la exactitud y el F1 macro cuentan cosas distintas. La exactitud premia acertar la clase grande. El F1 macro da el mismo peso a cada clase, así que cae cuando el modelo nunca dice las clases pequeñas. Si una clase tiene menos de `min_positives(N)` artículos, sus aciertos en el conjunto apartado son pocos y cambian mucho con la partición.

### Paso 7. La fecha que falta (parada en vivo)
En este paso, dado, miramos qué pesa más en el bosque, y comparamos la marca `has_date` con el año. La mayoría de los artículos no tiene fecha. En algunos departamentos la marca pesa más que el año, y en otros no: miren su caso.

```python
models[1].fit(train, y_train)   # la tubería entrena el mismo objeto forest, con las mismas filas de antes
importance = pd.Series(forest.feature_importances_, index=models[1][0].get_feature_names_out())
print(importance.nlargest(6).round(3))
print(f"has_date {importance.get('num__has_date', 0):.3f} contra year {importance.get('num__year', 0):.3f}")
```

```python
# Comprobar
assert abs(importance.sum() - 1) < 1e-6
assert (importance >= 0).all()
print(f"Importancias: OK. La más alta es {importance.idxmax()}")
```

### Paso 8. ¿Cuenta la L6? (L6, Parte 6, Paso 4)
En este paso calcule `l6_counts`: verdadero solo si los tres métodos quedan más de `MARGIN` por encima de la clase mayor de las filas apartadas. Después cuente en `seeds_holding` en cuántas de las particiones de `SPLIT_SEEDS` se cumple lo mismo.

```python
# SU CÓDIGO
# Cree majority, l6_counts y seeds_holding.
# La clase mayor con varias clases: y_test.value_counts(normalize=True).max(), como en el bucle de semillas de la L6.
# En el bucle use clone(m), una copia sin entrenar, para no tocar los modelos ya entrenados.
```

```python
# Comprobar
assert isinstance(l6_counts, bool) and 0 <= seeds_holding <= len(SPLIT_SEEDS)
print(f"l6_counts = {l6_counts}. Se sostiene en {seeds_holding} de {len(SPLIT_SEEDS)} particiones")
if seeds_holding < len(SPLIT_SEEDS):
    print("Con otra partición de los datos este resultado cambia: tómalo como débil.")
```

**Su turno.** Lea tres artículos apartados donde el bosque se equivoca. Escriban en dos frases si el error es del modelo o de la etiqueta.

```python
said = pd.Series(test_predictions[1], index=test.index)
for t in test.index[said != y_test][:3]:
    print(f"{t}: etiqueta {y_test[t]}, el bosque dijo {said[t]}")
my_errors = """
Escriban aquí qué pasa con esos tres artículos.
"""
print(my_errors)
```

**Hallazgo de la L6 (completen).** Copie los números y escriba qué significan. Si `l6_counts` es falso, la L6 no suma apoyos: es un resultado, no un error.

```python
l6_finding = """
- Clase mayor en las apartadas: ___. Exactitud de los tres métodos: ___, ___, ___.
- l6_counts: ___, en ___ de 5 particiones.
- Qué significa para nuestra lista: ___.
"""
print(l6_finding)
```

---
 
## Parte 6. Despliegue
 
### Paso 1. La tabla con los cinco apoyos (L5, Parte 7, y L6, Parte 7)
En este paso, dado, armamos `table`, una fila por artículo con el título como índice. Los tres apoyos de la semana 2 se unen por título. El grafo da un apoyo a los puentes. La predicción es positiva cuando al menos 2 de los 3 métodos lo dicen: en las filas de entrenamiento con las predicciones fuera del pliegue, y en las apartadas con las de los modelos que no las vieron. Es el código de la L6 (`pd.concat` y `reindex`), con `vote_of` en lugar de `votes >= 2`. [POR DECIDIR, pregunta abierta 1] Con la categoría del extracto, "positiva" quiere decir que la clase votada es una de las categorías del tema de la L4.

```python
table = week2.groupby("title")[["has_pattern", "read_group", "text_says_read"]].any().reindex(titles).fillna(False).astype(bool)
table.index.name = "title"   # table: una fila por artículo, el título es el índice
print(f"Sin texto en la semana 2: {int((~table.index.isin(week2['title'])).sum())}")
table["graph_support"] = table.index.isin(bridges)

if LABEL == "label":   # [POR DECIDIR, pregunta abierta 1]
    is_positive = lambda c: c in TARGETS[GROUP]
else:
    is_positive = lambda c: c == "1"
train_votes = vote_of(train_predictions)   # fuera del pliegue
test_votes = vote_of(test_predictions)     # apartadas
voted = pd.concat([train.assign(votes=train_votes),       # con el título como índice, como table
                   test.assign(votes=test_votes)])["votes"]
# 2 de 3 de acuerdo. reindex pone los votos en el orden de table
table["prediction"] = voted.map(lambda c: c is not None and is_positive(c)).reindex(table.index, fill_value=False).astype(bool)
print(f"Predichos positivos: {table['prediction'].sum()}")
```

### Paso 2. ¿Se repite con el texto?
En este paso, dado, decidimos si el texto (L4) y la predicción (L6) son uno o dos apoyos. Para eso medimos si la etiqueta repite el texto de la L4 (el parecido entre la etiqueta y `text_says_read`). Medimos la etiqueta, no la predicción. [POR DECIDIR, pregunta abierta 1] Con la categoría del extracto, la etiqueta repite la L4: la L4 aprendió de esas mismas categorías. Entonces cuentan siempre como **un** apoyo, `text_or_prediction`. Con una etiqueta de dos clases, son un apoyo si phi es al menos 0,30 en valor absoluto.

```python
if LABEL == "label":   # [POR DECIDIR, pregunta abierta 1]
    crosstab = pd.crosstab(y, table.loc[y.index, "text_says_read"]).to_numpy()
    overlap_l4 = np.sqrt(chi2_contingency(crosstab, correction=False)[0] / (crosstab.sum() * (min(crosstab.shape) - 1)))
    one_support = True
else:
    overlap_l4 = np.corrcoef(y.astype(int), table.loc[y.index, "text_says_read"].astype(int))[0, 1]
    one_support = abs(overlap_l4) >= 0.30
added = table["prediction"] & l6_counts & ~table["text_says_read"]
print(f"Parecido con la L4: {overlap_l4:.2f}. {'Un solo apoyo' if one_support else 'Dos apoyos'}. La L6 agrega {added.sum()} artículos que la L4 no tenía")
```

**Lo que aprendemos aquí.** [POR DECIDIR, pregunta abierta 1] Si la etiqueta repite el texto de la L4 (phi, o la V de Cramér con varias clases, entre la etiqueta y `text_says_read`), contar la predicción y el texto como dos apoyos sería contar dos veces la misma señal. Por eso, con la categoría del extracto, la L4 y la L6 forman un solo apoyo, `text_or_prediction`. La L6 solo suma artículos nuevos cuando cuenta (`l6_counts`).

### Paso 3. La lista inicial y la sensibilidad
En este paso sume los apoyos con el código de la L6 (la rama `one_support`), cree `table["supports"]` y `table["in_view"]`, y guarde en `drop_one` cuántos artículos salen de la lista si quitamos cada resultado una vez.

```python
# SU CÓDIGO
# Cree SUPPORT_COLUMNS, table['supports'], table['in_view'] y drop_one.
```

```python
# Comprobar
assert (table["supports"] == table[SUPPORT_COLUMNS].astype(int).sum(axis=1)).all()
assert set(drop_one) == set(SUPPORT_COLUMNS)
print(f"Lista inicial: {table['in_view'].sum()} con dos apoyos, {(table['supports'] >= 3).sum()} con tres. Salen si quitamos: {drop_one}")
```

### Paso 4. Una lista que se pueda leer en voz alta
En este paso, dado, recortamos la lista con la regla de la semana 2. El máximo es `standard["max_articles"]` de `pregunta.json`. Ordenamos por apoyos, después por `prob_texto` (la probabilidad de TF-IDF y regresión logística que guardó la semana 2 en `outputs/en_vista.csv`) y después por título. Nos quedamos con los primeros y marcamos el resto con `recortado = True`, sin borrarlo. Si quedan menos de 5 en vista, no rellenamos: la lista corta es el resultado.
 
**Lo que la lista puede y no puede decidir.** La lista dice qué abrir primero, no qué es importante para el departamento. Si un resultado saca a muchos de la lista cuando lo quitamos, la lista depende de él: díganlo en la charla.

```python
MAX_LIST = question_card["standard"]["max_articles"]
text_w2 = pd.read_csv(OUTPUTS_DIR / "en_vista.csv", keep_default_na=False)
if "prob_texto" in text_w2.columns:
    prob_text = text_w2.assign(prob_texto=pd.to_numeric(text_w2["prob_texto"], errors="coerce")).groupby("title")["prob_texto"].max()
else:
    prob_text = pd.Series(dtype=float)
    print("en_vista.csv no trae prob_texto. Dentro de cada número de apoyos se ordena por título.")
table["prob_texto"] = prob_text.reindex(table.index)
starter_list = (table.loc[table["in_view"], SUPPORT_COLUMNS + ["supports", "prob_texto"]].reset_index()
                .sort_values(["supports", "prob_texto", "title"], ascending=[False, False, True], na_position="last"))
starter_list["recortado"] = np.arange(len(starter_list)) >= MAX_LIST
kept = int((~starter_list["recortado"]).sum())
print(f"En vista {len(starter_list)}. Se leen {kept}, recortados {int(starter_list['recortado'].sum())} (máximo {MAX_LIST})")
if kept < 5:
    print("La lista tiene menos de 5 artículos, se lee completa y se reporta como resultado débil.")
print(starter_list.loc[~starter_list["recortado"], ["title", "supports", "prob_texto"]].head(10).to_string(index=False))
```

```python
# Comprobar
assert kept <= MAX_LIST and kept == min(len(starter_list), MAX_LIST)
assert starter_list["supports"].is_monotonic_decreasing
print("Lista recortada: OK")
```

### Paso 5. Qué cambiaría la lista (parada en vivo)
En este paso escriban qué resultado saca a más artículos de la lista cuando lo quitamos, y qué cambiaría si el profesor eligiera otra etiqueta para la L6.

```python
print("Salen de la lista si quitamos:", drop_one)
what_changes = """
Escriban aquí, en dos frases, de qué resultado depende más su lista y qué la cambiaría.
"""
print(what_changes)
```

### Paso 6. Guardar los archivos
En este paso, dado, guardamos `outputs/grafo.csv`, `outputs/prediccion.csv` y `outputs/lista_inicial.csv`, y anotamos en `pregunta.json` cómo entran el grafo y la predicción.

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
graph_table.to_csv(OUTPUTS_DIR / "grafo.csv", index=False)
pd.DataFrame({"title": titles, "etiqueta": y.reindex(titles).astype(str).to_numpy(), "apartada": table.index.isin(test.index),
              "clase_votada": voted.reindex(titles).astype(str).to_numpy(), "prediction": table.loc[titles, "prediction"].to_numpy()}).to_csv(OUTPUTS_DIR / "prediccion.csv", index=False)
starter_list.to_csv(OUTPUTS_DIR / "lista_inicial.csv", index=False)
question_card["graph_use"] = {"how_it_enters": "Un artículo recibe un apoyo si es un puente que no es nodo central.", "bridges": len(bridges), "hubs": sorted(hubs),
                              "what_changes_it": ["otro corte que el cuarto superior", "otra regla para los nodos centrales"]}
question_card["prediction_use"] = {"label": LABEL, "l6_counts": bool(l6_counts), "seeds_holding": f"{seeds_holding} de {len(SPLIT_SEEDS)}", "one_support": bool(one_support),
                                   "starter_list": {"in_view": int(len(starter_list)), "read": kept, "cut": int(starter_list["recortado"].sum())},
                                   "what_changes_it": ["otra etiqueta", "otra partición", "otro margen que 0,02"]}
QUESTION_PATH.write_text(json.dumps(question_card, ensure_ascii=False, indent=2), encoding="utf-8")
print("Guardados grafo.csv, prediccion.csv, lista_inicial.csv y pregunta.json")
```

```python
# Comprobar
saved_list = pd.read_csv(OUTPUTS_DIR / "lista_inicial.csv", keep_default_na=False)
assert {"title", "supports", "prob_texto", "recortado"} <= set(saved_list.columns)
assert (saved_list["recortado"].astype(str) == "False").sum() == kept
print(f"lista_inicial.csv: OK ({kept} se leen, {len(saved_list) - kept} recortados)")
```

### Paso 7. El título y el resumen de la charla
En este paso escriben el título y el resumen de su charla del sábado 28 de noviembre y los guardan en dos archivos de texto. Los dos van solo en el ZIP de esta semana.
 
- `project-title-es.txt`: el título, con menos de 15 palabras.
- `project-abstract-es.txt`: un solo párrafo de unas 120 palabras con el departamento, la pregunta, dos resultados que apoyan la lista y qué la cambiaría.
 
Vean el formato en los ejemplos [project-title-es.example.txt](https://cabrerac.github.io/assets/documents/26-udenar-data-mining/project-title-es.example.txt) y [project-abstract-es.example.txt](https://cabrerac.github.io/assets/documents/26-udenar-data-mining/project-abstract-es.example.txt). Están escritos sobre el laboratorio de artículos, así que no sirven para copiar: el suyo habla de su departamento y de su lista.

```python
# SU CÓDIGO
# Escriban project_title y project_abstract con su propio texto, no el del ejemplo.
# Guárdenlos con Path("project-title-es.txt").write_text(project_title, encoding="utf-8")
# y Path("project-abstract-es.txt").write_text(project_abstract, encoding="utf-8").
```

```python
# Comprobar
# El largo solo avisa y no falla. "Unas 120 palabras" no es un número exacto, así que aceptamos
# un margen del 20% (de 96 a 144). El título debe tener menos de 15 palabras.
TITLE_FILE, ABSTRACT_FILE = Path("project-title-es.txt"), Path("project-abstract-es.txt")
assert TITLE_FILE.is_file() and ABSTRACT_FILE.is_file(), "Falta project-title-es.txt o project-abstract-es.txt"
title_text, abstract_text = TITLE_FILE.read_text(encoding="utf-8").strip(), ABSTRACT_FILE.read_text(encoding="utf-8").strip()
assert title_text and abstract_text, "El título o el resumen está vacío"
n_title, n_abstract = len(title_text.split()), len(abstract_text.split())
n_paragraphs = len([part for part in abstract_text.split("\n\n") if part.strip()])
notes = [text for text, off in [(f"el título tiene {n_title} palabras y debe tener menos de 15", n_title >= 15),
                                (f"el resumen tiene {n_paragraphs} párrafos y debe tener uno", n_paragraphs != 1),
                                (f"el resumen tiene {n_abstract} palabras y debe tener unas 120", not 96 <= n_abstract <= 144)] if off]
print(f"Título y resumen: OK ({n_title} y {n_abstract} palabras)" if not notes else "Título y resumen guardados. Aviso: " + ", ".join(notes) + ".")
```

### Paso 8. Comprobación final
En este paso revisamos que el cuaderno dejó los archivos del ZIP y que las lecturas están escritas. Las líneas que dicen incompleto les dicen qué celda falta.

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


saved_graph = pd.read_csv(OUTPUTS_DIR / "grafo.csv", keep_default_na=False)
checks = [
    ("outputs/grafo.csv con sus columnas", lambda: list(saved_graph.columns) == ["title", "grado", "pagerank", "intermediacion", "aislado", "alerta_centro", "sin_vector_n2v", "vecinos_n2v", "supports", "in_view"]),
    ("outputs/prediccion.csv y outputs/lista_inicial.csv", lambda: (OUTPUTS_DIR / "prediccion.csv").is_file() and (OUTPUTS_DIR / "lista_inicial.csv").is_file()),
    ("pregunta.json con grafo y predicción", lambda: {"graph_use", "prediction_use"} <= set(json.loads(QUESTION_PATH.read_text(encoding="utf-8")))),
    ("marcas.csv de la semana 2", lambda: Path("marcas.csv").is_file()),
    ("project-title-es.txt y project-abstract-es.txt con texto", lambda: all(Path(f).is_file() and Path(f).read_text(encoding="utf-8").strip() for f in ["project-title-es.txt", "project-abstract-es.txt"])),
    ("Hallazgo de la L6 escrito", lambda: "___" not in l6_finding),
    ("Lecturas escritas (grafo, Page et al., node2vec, errores, qué cambiaría)", lambda: all("Escriban aquí" not in t for t in [graph_expectation, reading_answer, n2v_answer, my_errors, what_changes])),
]
passed = sum(_check_ok(n, f) for n, f in checks)
print(f"\nW3_CHECKS={passed}/{len(checks)}")
if passed == len(checks):
    print("W3_OK. Armen el ZIP de la entrega.")
```

## Registro de contribución
 
Cada integrante añade **una línea** con una tarea concreta. Indiquen quién consolidó el ZIP.

```python
contribution_log = """
- Nombre Apellido: grafo y puentes (L5)
- Nombre Apellido: node2vec y el artículo descrito por su lugar
- Nombre Apellido: los tres métodos de la L6 y su evaluación
- Nombre Apellido: lista inicial, sensibilidad y revisión final
Consolida el ZIP: Nombre Apellido
"""
print(contribution_log)
```

## Para la reflexión individual
 
La reflexión de la semana 3 va con la plantilla Word de la semana. Una pregunta para empezar: **¿qué artículo de su lista inicial depende de un solo resultado, y qué pasaría si ese resultado cambiara?** Salud mental (G5): su lista es la más recortada de los cinco grupos. Digan por qué (la etiqueta de la L4 es la mitad de las entradillas, y "mental" está en las palabras del tema) y qué artículos quedaron fuera por el recorte.
 
| Archivo del ZIP `week-3-<group_id>.zip` | Descripción |
|-----------------------------------------|-------------|
| `week-3-group-<group_id>.ipynb` | Este cuaderno ejecutado |
| `pregunta.json` | La tarjeta con `graph_use` y `prediction_use` |
| `marcas.csv` | Su conjunto marcado de la semana 2 |
| `outputs/grafo.csv` | El lugar de cada artículo en la red |
| `outputs/prediccion.csv` | La clase votada y el apoyo de la predicción |
| `outputs/lista_inicial.csv` | Los artículos con al menos dos apoyos, con `prob_texto` y `recortado` |
| `project-title-es.txt` | El título de la charla, con menos de 15 palabras |
| `project-abstract-es.txt` | El resumen de la charla, un párrafo de unas 120 palabras: departamento, pregunta, dos resultados que apoyan la lista y qué la cambiaría |

<!-- end NOTEBOOK: -->
