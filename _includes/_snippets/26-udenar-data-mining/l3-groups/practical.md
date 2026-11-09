<!-- NOTEBOOK: -->

## Repaso de Python para este cuaderno

Este cuaderno utiliza los siguientes métodos de Python. Si ya los conoce, ejecute estas celdas rápido.

### Arreglos de `numpy`
Un **arreglo** guarda números en filas y columnas. Aquí cada fila es un artículo y cada columna una palabra. `shape` dice el tamaño.

```python
import numpy as np

counts_toy = np.array([[2, 1, 0], [0, 1, 3]])   # 2 artículos, 3 palabras
print(counts_toy.shape)
print(counts_toy[0])          # la primera fila: el primer artículo
```

### El largo de un vector
El **largo** de un vector es la raíz de la suma de sus valores al cuadrado. Dividir por el largo deja el vector de largo 1.

```python
row = counts_toy[0].astype(float)
length = np.linalg.norm(row)
print(f"Largo: {length:.3f}. Después de escalar: {np.linalg.norm(row / length):.3f}")
```

### Coseno de vectores de largo 1
Con dos vectores de largo 1, el **coseno** es el producto punto `u @ v`. Así cuenta la mezcla de palabras, no el largo del artículo.

```python
u = counts_toy[0] / np.linalg.norm(counts_toy[0])
v = counts_toy[1] / np.linalg.norm(counts_toy[1])
assert abs(np.linalg.norm(u) - 1) < 1e-9
print(f"Coseno: {u @ v:.3f}. Repaso de Python: OK")
```

---

## Instrucciones

Seguimos con el equipo interno de la secretaría de salud y sus 320 artículos sobre nutrición. El equipo debe decidir **qué artículos tiene que leer** un colega que llega al equipo. En la Lección 2 encontramos pares de palabras que se repiten más que por azar.

Los pares describen palabras, pero el colega lee artículos enteros. Las bibliotecas ordenaban sus libros a mano, por tema. El agrupamiento deja que los textos parecidos se encuentren solos (Jain, 2010). Hoy buscamos **grupos** de artículos con palabras parecidas, y los artículos que **no encajan en ningún grupo**. No hay etiquetas, así que juzgamos los grupos contra el azar, con varias semillas y entre métodos. Un grupo sirve solo si el equipo puede leerlo.

**Tres métodos, tres preparaciones.** Los tres parten del mismo conteo de palabras.

| Método | Pregunta | Preparación que necesita | Qué deja fuera |
|--------|----------|--------------------------|----------------|
| M1. k-means | ¿Qué $k$ centros resumen mejor los artículos? | Los conteos, cada fila escalada a largo 1 | Nada: todo artículo entra en un grupo |
| M2. Mezcla gaussiana | ¿Qué probabilidad tiene cada artículo de venir de cada grupo? | Las 5 primeras componentes de la SVD, estandarizadas | Nada, pero marca a los dudosos |
| M3. HDBSCAN | ¿Dónde hay zonas densas de artículos? | Distancias coseno sobre las 10 primeras componentes | Los artículos sin vecinos claros (ruido) |

**Qué hacer.** Ejecute las celdas de arriba hacia abajo. Cada paso empieza con **En este paso** y termina con una celda **Comprobar**.

**Mapa del cuaderno**

| Parte | Fase CRISP-DM | Qué sale |
|-------|---------------|----------|
| 1 | Comprensión del negocio | La pregunta de hoy, los parámetros, `pregunta.json` y `outputs/patrones_l2.csv` |
| 2 | Comprensión de los datos | Los artículos con resumen útil |
| 3 | Preparación de los datos | Conteos escalados, SVD y distancias |
| 4 | Modelado | Grupos de k-means, de la mezcla y de HDBSCAN |
| 5 | Evaluación | Línea base, estabilidad, acuerdo y qué significa cada grupo |
| 6 | Despliegue | La tabla de `supports` y `outputs/grupos_l3.csv` |

**Carpetas.** La celda de configuración crea `data/` (datos descargados) y `outputs/` (tablas y gráficos).

---

## Parte 1. Comprensión del negocio

### Paso 1. La pregunta de esta lección
En este paso escribimos qué buscamos hoy. La decisión no cambia: qué artículos debe leer el colega nuevo.

| Pregunta | Respuesta para el laboratorio |
|----------|-------------------------------|
| ¿Qué buscamos? | Grupos de artículos que usan palabras parecidas, y los artículos que no encajan en ninguno |
| ¿Con qué los buscamos? | k-means, una mezcla gaussiana y HDBSCAN, sobre los conteos de palabras |
| ¿Contra qué los comparamos? | Contra una tabla barajada sin grupos, entre semillas y entre métodos |
| ¿Cómo entra un grupo en la lista? | Un artículo recibe el resultado del grupo si está en un grupo que el equipo lee |

Un artículo sin grupo no se borra. Se mira a mano.

### Paso 2. Configuración
En este paso importamos las librerías, creamos las carpetas y fijamos los parámetros. No los cambie. La excepción es `MIN_SUPPORTS`, que empieza en 2 y se puede cambiar. Cada grupo fija y justifica este número en su proyecto.

**Un solo umbral.** El grupo más chico de HDBSCAN tiene el tamaño del patrón más chico de la Lección 2: `support_floor(n)`.

**Nada que instalar.** Colab trae spaCy y scikit-learn.

```python
import json          # leer y escribir pregunta.json
from itertools import combinations   # los pares de semillas
import math          # techo (ceil) para el umbral de soporte
import re            # partir el texto en palabras
import time          # medir cuánto tarda cada paso
from collections.abc import Sequence
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
import sklearn
from sklearn.cluster import HDBSCAN, KMeans
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import adjusted_rand_score, pairwise_distances, silhouette_score
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler, normalize

# Carpetas de trabajo
DATA_DIR = Path("data")
OUTPUTS_DIR = Path("outputs")
DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

# Desde L2, sin cambios
SUPPORT_SHARE = 0.03   # proporción de textos
SUPPORT_MIN = 5        # mínimo de textos
SEED = 7

# L3 (no cambiar)
MAX_WORD_SHARE = 0.5         # palabras en más de la mitad de los textos no separan grupos
MIXTURE_COMPONENTS = 5       # dimensiones para la mezcla gaussiana
DENSITY_COMPONENTS = 10      # dimensiones para HDBSCAN
K_CANDIDATES = range(3, 9)   # valores de k que probamos en k-means
MIN_SAMPLES = SUPPORT_MIN    # min_samples de HDBSCAN
# min_cluster_size de HDBSCAN = support_floor(n), la misma regla que un patrón
N_SHUFFLES = 30              # tablas al azar de la línea base

# Decisión, L3 en adelante
MIN_SUPPORTS = 2             # el código empieza en 2, cámbielo si lo justifica (0 o 1 también valen)

# Propios de este cuaderno
MIXTURE_K = range(1, 9)      # números de grupos que prueba la mezcla
UNSURE_PROB = 0.6            # por debajo de esta probabilidad, el artículo es dudoso
STABILITY_SEEDS = range(5)   # semillas 0 a 4 para la estabilidad
TOP_WORDS = 8                # palabras que mostramos por grupo


# support_floor: la misma función de la L2.
def support_floor(n_texts: int) -> int:
    """Soporte mínimo que necesita una palabra o un par: max(SUPPORT_MIN, ceil(SUPPORT_SHARE * n))."""
    return max(SUPPORT_MIN, math.ceil(SUPPORT_SHARE * n_texts))


print(f"scikit-learn {sklearn.__version__}")
print(f"Umbral para 317 artículos: {support_floor(317)}")
```

**Comprobar:**

En este paso comprobamos el umbral de soporte, los valores de k que vamos a probar y la versión de scikit-learn.

```python
assert support_floor(317) == 10
assert MIN_SAMPLES == SUPPORT_MIN and list(K_CANDIDATES) == [3, 4, 5, 6, 7, 8]
assert tuple(int(v) for v in sklearn.__version__.split(".")[:2]) >= (1, 3)
print("Parámetros: OK")
```

### Paso 3. Funciones de la Lección 2
En este paso traemos de la Lección 2 la descarga, las palabras vacías, `words` y `p95`. Para agrupar necesitamos cuántas veces aparece cada palabra, así que `word_list` hace la misma limpieza y devuelve una lista con repeticiones.

```python
from spacy.lang.en.stop_words import STOP_WORDS as STOP_WORDS_EN

BASE_URL = "https://cabrerac.github.io/assets/data/26-udenar-data-mining"
WORD_RE = re.compile(r"[^\W\d_]+")   # secuencias de letras (sin números ni guiones bajos)
ABSTRACT_LABELS = {
    "background", "methods", "findings", "interpretation", "funding",
    "conclusions", "results", "objective", "objectives", "aims",
    "bill", "melinda", "gates", "foundation",
}
URL_TOKENS = {"http", "https", "www", "org"}
STOP_WORDS = set(STOP_WORDS_EN) | ABSTRACT_LABELS | URL_TOKENS


def download_data(name: str, folder: Path = DATA_DIR) -> Path:
    """Descarga un archivo de datos del curso, una sola vez.

    Qué hace: si el archivo ya está en la carpeta, lo usa. Si no, lo descarga de BASE_URL.
    Entrada: name, el nombre del archivo, y folder, la carpeta destino.
    Salida: la ruta local del archivo.
    Por qué: no queremos depender de la red en cada ejecución ni descargar dos veces.
    """
    dest = folder / name
    if dest.is_file() and dest.stat().st_size > 0:
        print(f"Ya en caché: {dest}")
        return dest
    response = requests.get(f"{BASE_URL}/{name}", timeout=60)
    response.raise_for_status()
    dest.write_bytes(response.content)
    print(f"Descargado: {dest} ({dest.stat().st_size / 1e6:.1f} MB)")
    return dest


def words(text: str, stop_words: set[str]) -> set[str]:
    """Convierte un texto en el conjunto de sus palabras útiles (la función de la L2, sin cambios).

    Qué hace: pasa a minúsculas, quita el residuo "[cita requerida]" de Wikipedia,
    separa en palabras de letras y descarta las de menos de 3 letras y las palabras vacías.
    Entrada: text (un resumen o una entradilla) y stop_words, el conjunto de palabras vacías.
    Salida: un set con cada palabra una sola vez.
    Por qué: los patrones de la L2 solo preguntan si una palabra está en un texto.
    """
    text = (text or "").lower().replace("[cita requerida]", " ")
    return {w for w in WORD_RE.findall(text) if len(w) >= 3 and w not in stop_words}


def word_list(text: str, stop_words: set[str]) -> list[str]:
    """Como words de la L2, pero conserva las repeticiones.

    Qué hace: la misma limpieza que words (minúsculas, sin "[cita requerida]", solo letras,
    al menos 3 letras, sin palabras vacías), pero devuelve cada aparición, en orden.
    Entrada: text y stop_words (aquí STOP_WORDS, la lista de la L2).
    Salida: una lista de palabras.
    Por qué: para agrupar contamos cuántas veces usa un texto cada palabra.
    Pasamos a CountVectorizer las listas ya hechas, así que la preparación es la de la L2.
    """
    text = (text or "").lower().replace("[cita requerida]", " ")
    return [w for w in WORD_RE.findall(text) if len(w) >= 3 and w not in stop_words]


def p95(values: Sequence[float]) -> float:
    """Percentil 95 por rango, sin interpolar. Es la misma regla de las diapositivas y de los cuadernos."""
    values = sorted(values)
    return values[min(len(values) - 1, int(0.95 * len(values)))]


print(word_list("The diet, the DIET and the risk of obesity, see https://www.who.int", STOP_WORDS))
```

**Comprobar:**

En este paso comprobamos que `word_list` cuenta repeticiones y limpia igual que `words`, y la regla del percentil 95.

```python
assert word_list("The diet, the DIET and the risk", STOP_WORDS) == ["diet", "diet", "risk"]
assert set(word_list("diet and risk, https://www.who.int", STOP_WORDS)) == words("diet and risk, https://www.who.int", STOP_WORDS)
assert p95(list(range(30))) == 28
print("Funciones de la L2: OK")
```

### Paso 4. La descripción de la pregunta
En este paso leemos `pregunta.json`, la descripción de la pregunta. Si `pregunta.json` no está, este cuaderno escribe la descripción del laboratorio para que pueda seguir.

Aquí escribimos también `TOPIC_WORDS`, las palabras del tema del equipo. Las escribimos antes de ver ningún grupo, porque en la Parte 5 deciden qué grupos se leen.

```python
QUESTION_PATH = Path("pregunta.json")

if QUESTION_PATH.is_file():
    question_card = json.loads(QUESTION_PATH.read_text(encoding="utf-8"))
    print("pregunta.json leído de la Lección 2")
else:
    question_card = {
        "question": "¿Qué artículos de nutrición debe leer el equipo para su tema, y qué filtro los puso en la lista?",
        "steps": ["comprender el negocio", "comprender los datos", "preparar", "modelar", "evaluar", "desplegar"],
        "standard": {"min_papers": 10, "max_papers": 30, "max_share_citations_only": 0.5},
        "use": {
            "may": ["decidir qué artículos abrir primero para el trabajo del equipo"],
            "may_not": ["citar la lista como evidencia de la alcaldía", "elegir artículos solo por sus citas"],
        },
        "pattern_use": {"rule": "El equipo explica por qué cada artículo está en la lista y qué resultados lo apoyan. Un artículo puede tener varios, uno o ninguno, si el equipo lo justifica."},
    }
    QUESTION_PATH.write_text(json.dumps(question_card, ensure_ascii=False, indent=2), encoding="utf-8")
    print("pregunta.json no estaba. Escribimos la descripción del laboratorio.")

TOPIC_WORDS = {"obesity", "obese", "overweight", "diet", "dietary", "diabetes", "cardiovascular", "hypertension"}

print(question_card["question"])
print("Regla:", question_card["pattern_use"]["rule"])
print("Palabras del tema:", ", ".join(sorted(TOPIC_WORDS)))
```

**Comprobar:**

En este paso comprobamos que la descripción de la pregunta tiene el uso de los patrones y que las palabras del tema están escritas.

```python
assert {"question", "standard", "pattern_use"} <= set(question_card)
assert len(TOPIC_WORDS) >= 5 and all(w == w.lower() for w in TOPIC_WORDS)
print("Pregunta y palabras del tema: OK")
```

### Paso 5. Los patrones de la Lección 2
En este paso leemos `outputs/patrones_l2.csv` de la Lección 2. Si el archivo no está, el cuaderno sigue con la columna de patrones vacía. Para tenerla, suba a `outputs/` el archivo de la Lección 2.

```python
PATTERNS_PATH = OUTPUTS_DIR / "patrones_l2.csv"
PATTERN_COLUMNS = ["pair", "support", "null_p95", "lift", "cosine", "kept", "kept_lift2", "beats_cosine", "shared_vector"]

if PATTERNS_PATH.is_file():
    patterns = pd.read_csv(PATTERNS_PATH)
    print(f"patrones_l2.csv: {len(patterns):,} pares, {patterns['kept_lift2'].sum():,} destacan")
else:
    patterns = pd.DataFrame(columns=PATTERN_COLUMNS)
    print("No encontramos outputs/patrones_l2.csv. Sin él, la columna de patrones queda vacía.")
patterns.head(3)
```

**Comprobar:**

En este paso comprobamos que la tabla de patrones tiene las columnas que vamos a usar.

```python
assert set(PATTERN_COLUMNS) <= set(patterns.columns)
print("Patrones de la L2: OK")
```

---

## Parte 2. Comprensión de los datos

### Paso 1. Los artículos con resumen útil
En este paso cargamos los artículos y dejamos fuera los resúmenes con menos de 5 palabras distintas. De 320 quedan 317.

```python
papers = pd.read_csv(download_data("nutricion-papers.csv"), keep_default_na=False)
useful = [len(words(t, STOP_WORDS)) >= 5 for t in papers["abstract"]]
print(f"Fuera por tener menos de 5 palabras distintas: {papers.loc[[not u for u in useful], 'abstract'].tolist()}")
papers = papers[useful].reset_index(drop=True)
texts = papers["abstract"].tolist()
N = len(texts)
FLOOR = support_floor(N)
print(f"Artículos usados: {N} de {len(useful)}. Umbral: {FLOOR} artículos")
```

**Comprobar:**

En este paso comprobamos el número de artículos usados y el umbral de soporte.

```python
assert N == 317 and FLOOR == 10
assert len(papers) == N
print("Datos: OK")
```

---

## Parte 3. Preparación de los datos

Los tres métodos parten de una tabla con una fila por artículo y una columna por palabra. k-means usa la tabla escalada. La mezcla y HDBSCAN usan pocas dimensiones.

**Una palabra nueva para "ítem".** Desde ahora el ítem es el texto que agrupamos.

### Paso 1. Conteo de palabras con un vocabulario útil
En este paso contamos las palabras con `CountVectorizer`. `word_list` parte el texto y `analyzer=lambda tokens: tokens` lo pasa tal cual. Hay dos límites:

- `min_df=FLOOR`: la palabra aparece en al menos 10 artículos.
- `max_df=MAX_WORD_SHARE`: una palabra en más de la mitad de los artículos no separa grupos.

```python
token_lists = [word_list(t, STOP_WORDS) for t in texts]
vectorizer = CountVectorizer(analyzer=lambda tokens: tokens, min_df=FLOOR, max_df=MAX_WORD_SHARE)
counts = vectorizer.fit_transform(token_lists)
vocabulary = vectorizer.get_feature_names_out()
print(f"Tabla de conteos: {counts.shape[0]} artículos x {counts.shape[1]} palabras")
print(f"Celdas distintas de 0: {counts.nnz:,} ({counts.nnz / (counts.shape[0] * counts.shape[1]):.1%})")
```

La tabla es casi toda ceros, así que se guarda como **matriz dispersa**.

**Comprobar:**

En este paso comprobamos la forma de la tabla de conteos y que no quedan restos de direcciones web.

```python
assert counts.shape == (317, 869)
assert not URL_TOKENS & set(vocabulary)
print("Conteos: OK")
```

### Paso 2. Escalar cada artículo a largo 1
En este paso dividimos cada fila por su largo con `normalize`. Así el largo del resumen no pesa más que el tema.

```python
X = normalize(counts)   # cada fila queda de largo 1
row_lengths = np.sqrt(X.multiply(X).sum(axis=1)).A1
print(f"Largo de las filas: mínimo {row_lengths.min():.3f}, máximo {row_lengths.max():.3f}")
```

**Comprobar:**

En este paso comprobamos que cada fila quedó de largo 1.

```python
assert np.allclose(row_lengths, 1)
print("Filas de largo 1: OK")
```

### Paso 3. Pocas dimensiones con la SVD
En este paso reducimos las 869 columnas con la **descomposición en valores singulares** (SVD), $X = U S V^T$. Cada componente mezcla palabras que suelen ir juntas. En textos se llama **análisis semántico latente** (LSA).

`TruncatedSVD` calcula las primeras 10 componentes (`DENSITY_COMPONENTS`) y devuelve $Z = U S$. `explained_variance_ratio_` dice cuánto explica cada una.

```python
svd = TruncatedSVD(n_components=DENSITY_COMPONENTS, random_state=SEED)
Z = svd.fit_transform(X)
variance_share = svd.explained_variance_ratio_
print(variance_share.cumsum().round(3))
print(f"5 componentes explican {variance_share[:MIXTURE_COMPONENTS].sum():.1%}. Las 10, {variance_share.sum():.1%}")

plt.figure(figsize=(7, 3.5))
plt.plot(range(1, DENSITY_COMPONENTS + 1), variance_share.cumsum(), marker="o", color="steelblue")
plt.axvline(MIXTURE_COMPONENTS, color="darkorange", linestyle="--", label="5 (mezcla)")
plt.xlabel("Número de componentes")
plt.ylabel("Proporción acumulada")
plt.title("Variación explicada por las 10 primeras componentes")
plt.legend()
plt.tight_layout()
plt.savefig(OUTPUTS_DIR / "varianza_l3.png", dpi=120)
plt.show()
```

La curva sube despacio. 10 componentes explican menos de una cuarta parte. Es una primera señal de que no hay pocos temas claros.

**Comprobar:**

En este paso comprobamos la forma de `Z` y qué parte de la variación explican sus componentes.

```python
assert Z.shape == (317, DENSITY_COMPONENTS)
assert 0.15 < variance_share.sum() < 0.35
print("SVD: OK")
```

### Paso 4. La preparación de la mezcla y de HDBSCAN
En este paso armamos la entrada de M2 y de M3.

- **M2.** Las 5 primeras componentes, estandarizadas con `StandardScaler`.
- **M3.** La distancia coseno, $1 - \cos$, sobre las 10 componentes, con `metric="precomputed"`.

```python
Z_mixture = StandardScaler().fit_transform(Z[:, :MIXTURE_COMPONENTS])
distances = pairwise_distances(Z, metric="cosine")
print(f"Entrada de M2: {Z_mixture.shape}. Entrada de M3: {distances.shape}")
print(f"Distancia coseno: mediana {np.median(distances):.2f}, de {distances.min():.2f} a {distances.max():.2f}")
```

**Comprobar:**

En este paso comprobamos la forma de las entradas de M2 y M3.

```python
assert Z_mixture.shape == (317, MIXTURE_COMPONENTS) and abs(Z_mixture.mean()) < 1e-9
assert distances.shape == (317, 317) and np.allclose(np.diag(distances), 0, atol=1e-6)
print("Preparación de M2 y M3: OK")
```

### Paso 5. ¿Por qué no usar todas las palabras?
En este paso vemos HDBSCAN sobre las 869 palabras, sin SVD. Con muchas dimensiones todas las distancias se parecen. Es la **maldición de la dimensión**.

```python
D_all_words = pairwise_distances(X, metric="cosine")
all_words_labels = HDBSCAN(min_cluster_size=FLOOR, min_samples=MIN_SAMPLES, metric="precomputed", copy=True).fit(D_all_words).labels_
print(f"Con todas las palabras: {all_words_labels.max() + 1} grupos, {(all_words_labels == -1).mean():.0%} de ruido")
print(f"Distancia coseno con todas las palabras: mediana {np.median(D_all_words):.2f}. Con 10 componentes: {np.median(distances):.2f}")
```

La distancia mediana queda cerca de 1, HDBSCAN encuentra 2 grupos y deja el 40 % como ruido. Por eso M3 usa 10 componentes.

---

## Parte 4. Modelado

### M1. k-means
En este paso agrupamos con **k-means**: $k$ centros, y cada artículo con el centro más cercano. Minimiza:

$\displaystyle J = \sum_{i=1}^{N} \lVert x_i - \mu_{c(i)} \rVert^2$

Lloyd alterna asignar cada artículo a su centro y mover cada centro al promedio. `KMeans` usa k-means++ y 10 arranques (`n_init=10`).

**Cómo elegir k.** Usamos la silueta, una medida de la evaluación que la Parte 5 compara con el azar. $a$ es la distancia media a su grupo y $b$ al grupo vecino. La silueta es $s = (b - a) / \max(a, b)$. Cerca de 1 está bien en su grupo, cerca de 0 está entre dos.

```python
silhouettes = {}
for k in K_CANDIDATES:
    km = KMeans(n_clusters=k, n_init=10, random_state=SEED).fit(X)
    silhouettes[k] = silhouette_score(X, km.labels_, metric="cosine")
print({k: round(s, 3) for k, s in silhouettes.items()})

K_CHOSEN = max(silhouettes, key=silhouettes.get)
kmeans = KMeans(n_clusters=K_CHOSEN, n_init=10, random_state=SEED).fit(X)
kmeans_labels = kmeans.labels_
print(f"k elegido: {K_CHOSEN}")
```

```python
plt.figure(figsize=(6, 3.5))
plt.plot(list(silhouettes), list(silhouettes.values()), marker="o", color="steelblue")
plt.ylim(0, 0.2)
plt.xlabel("k")
plt.ylabel("Silueta media (coseno)")
plt.title("M1. Silueta de k-means para cada k")
plt.tight_layout()
plt.savefig(OUTPUTS_DIR / "silueta_l3.png", dpi=120)
plt.show()
```

**La silueta es baja y plana**, de 0,06 a 0,08. No hay un $k$ natural. Tomamos el más alto, 8, que da grupos de unos 40 artículos. Elegimos $k$ **para el uso** y lo dejamos escrito.

**Comprobar:**

En este paso comprobamos el k elegido y que la silueta es baja.

```python
assert K_CHOSEN == 8
assert max(silhouettes.values()) < 0.1
print("M1: OK")
```

### M1. Las palabras de cada grupo
En este paso leemos cada grupo por las palabras de más peso en su centro.

```python
def top_words(weights: np.ndarray, vocabulary: Sequence[str], n: int = TOP_WORDS) -> list[str]:
    """Devuelve las n palabras con más peso en un vector de palabras.

    Qué hace: ordena los pesos de mayor a menor y toma las primeras n palabras.
    Entrada: weights, un peso por palabra (por ejemplo el centro de un grupo),
    vocabulary, las palabras en el mismo orden, y n.
    Salida: lista de n palabras.
    Por qué: un grupo sin etiqueta solo se puede leer por sus palabras.
    """
    return [str(vocabulary[j]) for j in np.argsort(weights)[::-1][:n]]


kmeans_words = {g: top_words(centre, vocabulary) for g, centre in enumerate(kmeans.cluster_centers_)}
for g, group_words in kmeans_words.items():
    print(f"Grupo {g} ({(kmeans_labels == g).sum()} artículos): {', '.join(group_words)}")
```

Unos grupos se leen bien (obesidad y alimentos, diabetes, riesgo cardiovascular, carga global). Otros mezclan palabras de método, que dicen cómo se escribió un artículo, no de qué trata.

**Comprobar:**

En este paso comprobamos que hay palabras para cada grupo y que ningún grupo es diminuto.

```python
assert len(kmeans_words) == K_CHOSEN
assert np.bincount(kmeans_labels).min() >= 5
print("Palabras de M1: OK")
```

### M2. Mezcla gaussiana
En este paso ajustamos una **mezcla gaussiana**: cada grupo es una campana con su media y su covarianza.

$\displaystyle p(x) = \sum_{k=1}^{K} \pi_k \, \mathcal{N}(x \mid \mu_k, \Sigma_k)$

EM alterna dos pasos: calcula la probabilidad de cada grupo para cada artículo (**responsabilidades**) y mueve pesos, medias y covarianzas. Los grupos pueden ser alargados.

**Cómo elegir K: el BIC**, $\text{BIC} = -2 \log L + p \log N$. Elegimos el más bajo.

```python
# La mezcla usa n_init=1 (el valor por defecto), como en las diapositivas: se ajusta una vez por K.
# k-means usa n_init=10 en la estabilidad y en la línea base. Diez arranques evitan que un mal arranque
# haga parecer inestables los grupos o más débil el azar. Así comparamos semillas, no arranques.
bic = {}
for K in MIXTURE_K:
    gm = GaussianMixture(n_components=K, covariance_type="full", random_state=SEED).fit(Z_mixture)
    bic[K] = gm.bic(Z_mixture)
print({K: round(b) for K, b in bic.items()})
K_MIXTURE = min(bic, key=bic.get)

mixture = GaussianMixture(n_components=K_MIXTURE, covariance_type="full", random_state=SEED).fit(Z_mixture)
print(f"K elegido por el BIC: {K_MIXTURE}")
```

**Comprobar:**

En este paso comprobamos el número de grupos que elige el BIC.

```python
assert K_MIXTURE == 4
print("M2: OK")
```

### M2. Pertenencia suave
En este paso leemos la **pertenencia suave** con `predict_proba`. Un artículo con probabilidad más alta bajo 0,6 (`UNSURE_PROB`) es **dudoso**.

```python
membership = mixture.predict_proba(Z_mixture)
mixture_labels = mixture.predict(Z_mixture)   # el grupo más probable de cada artículo
top_prob = membership.max(axis=1)
unsure = top_prob < UNSURE_PROB
print(f"Tamaño de cada grupo: {np.bincount(mixture_labels).tolist()}")
print(f"Artículos dudosos (probabilidad más alta bajo {UNSURE_PROB}): {unsure.sum()} ({unsure.mean():.1%})")
papers.loc[unsure, ["title"]].head(5)
```

Pocos son dudosos, pero eso es seguridad del modelo, no de los datos. 5 componentes explican poco.

**Comprobar:**

En este paso comprobamos que las probabilidades suman 1 y que hay pocos dudosos.

```python
assert np.allclose(membership.sum(axis=1), 1)
assert unsure.mean() < 0.2
print("Pertenencia suave: OK")
```

### M3. HDBSCAN
En este paso buscamos **zonas densas** con HDBSCAN:

1. La **distancia de núcleo** es la distancia al vecino número `min_samples`.
2. La **distancia de alcance mutuo** aleja a los artículos de zonas poco densas.
3. Con ella arma un árbol y lo corta a distintas alturas.
4. Se queda con los grupos más **estables**, de al menos `min_cluster_size`. El resto es **ruido** ($-1$).

Usamos `min_cluster_size = FLOOR` (10) y `min_samples = MIN_SAMPLES` (5).

```python
hdb = HDBSCAN(min_cluster_size=FLOOR, min_samples=MIN_SAMPLES, metric="precomputed", copy=True).fit(distances)
hdbscan_labels = hdb.labels_            # -1 es ruido
n_groups = hdbscan_labels.max() + 1
in_group = hdbscan_labels != -1
noise = (hdbscan_labels == -1).mean()
print(f"Grupos: {n_groups}. Tamaños: {np.bincount(hdbscan_labels[in_group]).tolist()}")
print(f"Ruido: {(~in_group).sum()} artículos ({noise:.0%})")

hdbscan_words = {g: top_words(np.asarray(X[hdbscan_labels == g].mean(axis=0)).ravel(), vocabulary) for g in range(n_groups)}
for g, group_words in hdbscan_words.items():
    print(f"Grupo {g} ({(hdbscan_labels == g).sum()} artículos): {', '.join(group_words)}")
```

Cuatro de los cinco grupos se leen: cáncer (16), diabetes (10), guías clínicas (38) y carga global (58). El quinto, de 87, mezcla palabras de método. Ninguno es solo de obesidad.

**Comprobar:**

En este paso comprobamos el número de grupos densos y la parte de ruido.

```python
assert n_groups == 5
assert 0.3 < noise < 0.4
print("M3: OK")
```

### M3. La lista de ruido
En este paso miramos el ruido. **No lo borramos.** Un artículo sin vecinos claros puede ser el único de su tema.

```python
noise_list = papers.loc[~in_group, ["title", "year", "cited_by_count"]]
print(f"Artículos sin grupo: {len(noise_list)}")
noise_list.sort_values("cited_by_count", ascending=False).head(10)
```

Uno de cada tres artículos queda fuera. k-means los mete igual en un grupo.

---

## Parte 5. Evaluación

Sin etiquetas, juzgamos los grupos contra el azar, entre semillas, entre métodos y por sus palabras.

### Paso 1. Silueta contra una línea base al azar
En este paso preguntamos qué silueta da una tabla **sin grupos**. Barajamos cada columna 30 veces (`N_SHUFFLES`) y corremos k-means con el $k$ elegido. El percentil 95, con `p95()`, es la línea base.

Este azar no conserva el largo de cada texto, como sí hacía el de la Lección 2. No hace falta, porque las filas tienen largo 1.

**Tiempo.** Entre 20 s y un minuto en Colab.

```python
start = time.time()
rng = np.random.default_rng(SEED)
dense = counts.toarray()
shuffled_silhouettes = []
for _ in range(N_SHUFFLES):
    # cada palabra queda en el mismo número de artículos, al azar
    X_shuffled = normalize(np.apply_along_axis(rng.permutation, 0, dense))
    km_shuffled = KMeans(n_clusters=K_CHOSEN, n_init=10, random_state=SEED).fit(X_shuffled)
    shuffled_silhouettes.append(silhouette_score(X_shuffled, km_shuffled.labels_, metric="cosine"))
BASELINE_P95 = p95(shuffled_silhouettes)
print(f"{N_SHUFFLES} tablas al azar en {time.time() - start:.1f} s")
print(f"Silueta real con k = {K_CHOSEN}: {silhouettes[K_CHOSEN]:.3f}. Percentil 95 del azar: {BASELINE_P95:.3f}")
```

La silueta real supera al azar por poco: 0,075 contra 0,054. Los grupos existen, pero son débiles.

**Comprobar:**

En este paso comprobamos que hay una silueta por tabla barajada y que la silueta real supera al azar.

```python
assert len(shuffled_silhouettes) == N_SHUFFLES
assert silhouettes[K_CHOSEN] > BASELINE_P95
print("Línea base: OK")
```

### Paso 2. Estabilidad entre semillas
En este paso repetimos k-means con 5 semillas (0 a 4) y comparamos los 10 pares con el **índice de Rand ajustado** (ARI). Vale 1 si dos agrupaciones son iguales y cerca de 0 si coinciden por azar.

```python
# n_init=10 en cada semilla: vea el comentario de la mezcla (M2)
seed_labels = [KMeans(n_clusters=K_CHOSEN, n_init=10, random_state=s).fit(X).labels_ for s in STABILITY_SEEDS]
seed_ari = [adjusted_rand_score(a, b) for a, b in combinations(seed_labels, 2)]   # los 10 pares de semillas
print(f"ARI entre semillas (10 pares): media {np.mean(seed_ari):.2f}, de {min(seed_ari):.2f} a {max(seed_ari):.2f}")
```

El ARI medio está cerca de 0,45. Con otra semilla los grupos cambian bastante.

**Comprobar:**

En este paso comprobamos que hay un ARI por cada par de semillas y su valor medio.

```python
assert len(seed_ari) == 10
assert 0.2 < np.mean(seed_ari) < 0.7
print("Estabilidad: OK")
```

### Paso 3. Tamaños y acuerdo entre los tres métodos
En este paso comparamos los tamaños y el acuerdo de los tres métodos. Para HDBSCAN usamos solo los artículos que no son ruido.

```python
sizes = pd.DataFrame({
    "method": ["k-means", "mezcla", "HDBSCAN"],
    "groups": [K_CHOSEN, K_MIXTURE, n_groups],
    "sizes": [sorted(np.bincount(kmeans_labels), reverse=True), sorted(np.bincount(mixture_labels), reverse=True), sorted(np.bincount(hdbscan_labels[in_group]), reverse=True)],
    "left_out": [0, int(unsure.sum()), int((~in_group).sum())],
})
display(sizes)

agreement = pd.DataFrame({
    "pair": ["k-means y mezcla", "k-means y HDBSCAN", "mezcla y HDBSCAN"],
    "ari": [
        adjusted_rand_score(kmeans_labels, mixture_labels),
        adjusted_rand_score(kmeans_labels[in_group], hdbscan_labels[in_group]),
        adjusted_rand_score(mixture_labels[in_group], hdbscan_labels[in_group]),
    ],
}).round(2)
agreement
```

`left_out` dice qué deja fuera cada método. Los métodos coinciden en las zonas densas y difieren en el resto.

**Comprobar:**

En este paso comprobamos los tamaños de los tres métodos y que coinciden más fuera del ruido.

```python
assert sizes["groups"].tolist() == [K_CHOSEN, K_MIXTURE, n_groups]
assert agreement.loc[1, "ari"] > agreement.loc[0, "ari"]
print("Acuerdo: OK")
```

### Paso 4. Qué significa un grupo para el equipo
En este paso decidimos qué grupos **lee el equipo**. Usamos los de **HDBSCAN**, porque no obliga a ningún artículo a entrar en un grupo.

El equipo lee un grupo si alguna de sus `TOPIC_WORDS`, escritas en la Parte 1, está entre sus 8 palabras de más peso.

```python
team_groups = sorted(g for g, group_words in hdbscan_words.items() if TOPIC_WORDS & set(group_words))
read_group = np.isin(hdbscan_labels, team_groups)   # el ruido (-1) nunca está en team_groups
for g, group_words in hdbscan_words.items():
    mark = "lee" if g in team_groups else "no lee"
    print(f"Grupo {g} ({(hdbscan_labels == g).sum()} artículos, {mark}): {', '.join(group_words)}")
print(f"Grupos que lee el equipo: {team_groups}. Artículos en ellos: {read_group.sum()}")
print(f"Ruido, sin resultado del grupo y para mirar a mano: {(~in_group).sum()} artículos")
```

Solo el grupo de diabetes, con 10 artículos, toca el tema. Los 108 artículos de ruido no reciben este resultado y se miran a mano.

**Comprobar:**

En este paso comprobamos que el equipo lee algún grupo, no todos, y que el ruido no recibe el resultado.

```python
assert 1 <= len(team_groups) < n_groups and not read_group[~in_group].any()
print("Grupos del tema: OK")
```

### Paso 5. Una vista de los grupos
En este paso dibujamos los artículos sobre las dos primeras componentes, con el color de su grupo de HDBSCAN. El ruido va en gris. Es una sombra de 869 dimensiones en 2.

```python
plt.figure(figsize=(7, 5))
plt.scatter(Z[~in_group, 0], Z[~in_group, 1], color="lightgray", s=14, label="ruido")
plt.scatter(Z[in_group, 0], Z[in_group, 1], c=hdbscan_labels[in_group], cmap="tab10", s=18, alpha=0.8)
plt.scatter(Z[read_group, 0], Z[read_group, 1], facecolors="none", edgecolors="black", s=30, linewidths=0.6, label="grupo que lee el equipo")
plt.xlabel("Componente 1")
plt.ylabel("Componente 2")
plt.title(f"Artículos en las dos primeras componentes, {n_groups} grupos de HDBSCAN")
plt.legend()
plt.tight_layout()
plt.savefig(OUTPUTS_DIR / "dispersion_l3.png", dpi=120)
plt.show()
```

### Paso 6. Lo que encontramos: una estructura débil
En este paso juntamos lo que dicen los números. La silueta queda entre 0,06 y 0,08, cerca de 0.

No es un error del código. Los subtemas comparten vocabulario y se mezclan.

1. **Línea base.** La silueta real apenas supera el percentil 95 del azar.
2. **Estabilidad.** El ARI entre semillas queda cerca de 0,45.
3. **Ruido.** Uno de cada tres artículos no tiene vecinos claros.

```python
print(f"Silueta con k = {K_CHOSEN}: {silhouettes[K_CHOSEN]:.3f}. Percentil 95 de la línea base: {BASELINE_P95:.3f}")
print(f"Estabilidad entre semillas (ARI medio): {np.mean(seed_ari):.2f}")
print(f"Ruido de HDBSCAN: {noise:.0%} de los artículos")
```

**Lo que leemos.** Los grupos son débiles. No decidimos con un grupo solo. La lista muestra qué otros resultados apoyan cada artículo.

**Qué cambiaría esta lectura.** Otro $k$, otro umbral, otra preparación del texto o una pregunta que pida grupos más amplios.

---

## Parte 6. Despliegue

### Paso 1. La tabla de resultados
En este paso juntamos los dos resultados que tenemos. Cada uno es una columna de `SUPPORT_COLUMNS`:

- **`has_pattern` (Lección 2).** El resumen tiene un patrón que destaca y toca el tema.
- **`read_group` (Lección 3).** El artículo está en un grupo de HDBSCAN que el equipo lee.

Un artículo queda **en vista** según `MIN_SUPPORTS`, el número de resultados a favor que pide el código. `MIN_SUPPORTS` empieza en 2 y se puede cambiar. Cada grupo fija y justifica este número en su proyecto. 0 o 1 valen si se explica. La celda cuenta cuántos artículos tienen 0, 1, 2 y 3 o más resultados a favor.

```python
SUPPORT_COLUMNS = ["has_pattern", "read_group"]   # una columna por resultado

topic_pairs = [tuple(p.split(" + ")) for p in patterns.loc[patterns["kept_lift2"].astype(bool), "pair"] if TOPIC_WORDS & set(p.split(" + "))]
word_sets = [words(t, STOP_WORDS) for t in texts]

supports = pd.DataFrame({"title": papers["title"]})
supports["has_pattern"] = [any(a in s and b in s for a, b in topic_pairs) for s in word_sets]
supports["read_group"] = read_group
supports["supports"] = supports[SUPPORT_COLUMNS].astype(int).sum(axis=1)
supports["in_view"] = supports["supports"] >= MIN_SUPPORTS
print(f"Patrones del tema que destacan: {len(topic_pairs)}")
print(f"Con patrón: {supports['has_pattern'].sum()}. En grupo del tema: {supports['read_group'].sum()}. En vista: {supports['in_view'].sum()}")
counts = supports["supports"].clip(upper=3).value_counts().reindex(range(4), fill_value=0).rename(index={3: "3 o más"})
print(counts.rename_axis("resultados a favor").to_frame("artículos").T.to_string())
supports[supports["in_view"]].head(10)
```

**Lo que aprendemos aquí.** Con `MIN_SUPPORTS = 2` quedan 8 artículos, menos de los 10 del estándar. Es un resultado honesto. Con k-means serían 56, pero un grupo solo cuenta si el equipo lo puede leer. El grupo 4, de 87 artículos, tiene *food* entre sus palabras, pero *food* no está en `TOPIC_WORDS`. Esas palabras se escribieron antes y no se cambian para que un grupo entre. Por eso van en la descripción de la pregunta como algo que cambia la decisión.

**Comprobar:**

En este paso comprobamos que el número de resultados a favor está en su rango y que el ruido no recibe el resultado del grupo.

```python
assert supports["supports"].between(0, len(SUPPORT_COLUMNS)).all()
assert supports["in_view"].dtype == bool and not supports.loc[~in_group, "read_group"].any()
print("Resultados: OK")
```

### Paso 2. Guardar los grupos
En este paso guardamos `outputs/grupos_l3.csv`, una fila por artículo. El ruido lleva `-1` en `hdbscan` y sigue en la tabla.

```python
groups_table = pd.DataFrame({
    "title": papers["title"],
    "kmeans": kmeans_labels,
    "mezcla": mixture_labels,
    "prob_mezcla": top_prob.round(3),
    "hdbscan": hdbscan_labels,
    "has_pattern": supports["has_pattern"],
    "read_group": supports["read_group"],
    "supports": supports["supports"],
    "in_view": supports["in_view"],
})
groups_path = OUTPUTS_DIR / "grupos_l3.csv"
groups_table.to_csv(groups_path, index=False)
print(f"Guardado: {groups_path} ({len(groups_table)} filas)")
```

**Comprobar:**

En este paso comprobamos que el archivo guardado tiene una fila por artículo y sus columnas.

```python
saved = pd.read_csv(groups_path)
assert {"title", "kmeans", "mezcla", "prob_mezcla", "hdbscan", "has_pattern", "read_group", "supports", "in_view"} <= set(saved.columns)
assert len(saved) == N
print("grupos_l3.csv: OK")
```

### Paso 3. Qué cambiaría la decisión
En este paso escribimos en la descripción de la pregunta cómo entra un grupo y qué lo cambiaría: otro umbral, más componentes de la SVD u otra lectura de las palabras.

```python
question_card["group_use"] = {
    "how_it_enters": "El resultado del grupo cuenta a favor de un artículo si está en un grupo de HDBSCAN que el equipo lee (sus palabras tocan el tema). El ruido no lo recibe.",
    "reading": "Los grupos son débiles: la silueta apenas supera al azar y cambia con la semilla. Un grupo solo no decide.",
    "k_chosen": int(K_CHOSEN),
    "team_groups": [int(g) for g in team_groups],
    "noise": "Los artículos que HDBSCAN deja como ruido no tienen el resultado del grupo. Se miran a mano, no se borran.",
    "what_changes_it": ["otro umbral de soporte", "más direcciones de la SVD", "otra lectura de las palabras de un grupo"],
}
QUESTION_PATH.write_text(json.dumps(question_card, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(question_card["group_use"], ensure_ascii=False, indent=1))
```

### Paso 4. Comprobación final
En este paso revisamos que el cuaderno dejó lo que la Lección 4 necesita.

```python
def _check_ok(name, predicate):
    """Ejecuta una comprobación y dice OK o incompleto, sin detener el cuaderno."""
    try:
        ok = bool(predicate())
    except Exception:
        ok = False
    print(f"{name}: {'OK' if ok else 'incompleto'}")
    return ok


checks = [
    ("pregunta.json con uso de grupos", lambda: "group_use" in json.loads(QUESTION_PATH.read_text(encoding="utf-8"))),
    ("outputs/grupos_l3.csv", lambda: groups_path.is_file()),
    ("Gráficos de varianza, silueta y dispersión", lambda: all((OUTPUTS_DIR / f).is_file() for f in ["varianza_l3.png", "silueta_l3.png", "dispersion_l3.png"])),
    ("Patrones de la L2 en los resultados", lambda: len(topic_pairs) > 0),
]
passed = sum(_check_ok(n, f) for n, f in checks)
print(f"\nL3_CHECKS={passed}/{len(checks)}")
if passed == len(checks):
    print("L3_OK. Siga con la Lección 4.")
```

<!-- end NOTEBOOK: -->
