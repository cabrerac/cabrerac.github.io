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

Seguimos con el equipo interno de la secretaría de salud y sus 320 artículos sobre nutrición.
El equipo debe decidir **qué artículos tiene que leer** un colega que llega al equipo.
En la Lección 2 encontramos pares de palabras que se repiten.

Hoy buscamos **grupos** de artículos con palabras parecidas (Jain, 2010).
No hay etiquetas, así que el equipo lee un grupo cuando trata de su tema.

**Tres métodos en este cuaderno.** Cada uno trae la preparación que necesita, el ajuste y su límite.
El límite se calcula en ese paso y queda escrito.
La evaluación los pone en una tabla.
El archivo lo escribe HDBSCAN.

| Método | Pregunta | Preparación que necesita | Papel en el cuaderno |
|--------|----------|--------------------------|----------------------|
| k-means | ¿Qué $k$ centros resumen mejor los artículos? | Los conteos, cada fila escalada a largo 1 | Referencia: todo artículo queda en un grupo |
| Mezcla gaussiana | ¿Qué probabilidad tiene cada artículo de pertenecer a cada nube? | Las primeras 5 direcciones de la SVD | Se corre y se documenta. No escribe el archivo |
| HDBSCAN | ¿Dónde hay zonas densas de artículos? | Distancias coseno sobre las 10 primeras direcciones de la SVD | El método elegido para estos datos |

**Qué hacer.** Ejecute las celdas de arriba hacia abajo.
Cada paso empieza con **En este paso**. Si tiene código, termina con una celda **Comprobar**.

**Mapa del cuaderno**

| Parte | Fase CRISP-DM | Qué sale |
|-------|---------------|----------|
| 1 | Comprensión del negocio | La pregunta de hoy y las palabras del tema |
| 2 | Comprensión de los datos | Parámetros, artículos y patrones de la Lección 2 |
| 3 | k-means | Conteos de largo 1, el ajuste y la silueta |
| 4 | Ajuste de k-means | Centros, silueta y palabras de cada grupo |
| 5 | Mezcla gaussiana | Cinco direcciones, probabilidades y cuántos artículos abriría |
| 6 | HDBSCAN | Diez direcciones, distancias, el ajuste y el ruido |
| 7 | Evaluación | Los tres métodos, las coincidencias y `outputs/grupos_l3.csv` |
| 8 | Despliegue | Hasta 30 artículos para leer, en `outputs/lectura_l3.csv` |

**Carpetas.** La celda de configuración crea `data/` (datos descargados) y `outputs/` (tablas y gráficos).

---

## Parte 1. Comprensión del negocio

### Paso 1. La pregunta de esta lección
En este paso escribimos qué buscamos hoy.
La decisión no cambia: qué artículos debe leer el colega nuevo.

| Pregunta | Respuesta para el laboratorio |
|----------|-------------------------------|
| ¿Qué buscamos? | Grupos de artículos que usan palabras parecidas |
| ¿Con qué los buscamos? | k-means, una mezcla gaussiana y HDBSCAN. El archivo guarda HDBSCAN |
| ¿Cómo los comparamos? | Con la silueta y viendo dónde coinciden k-means y HDBSCAN |
| ¿Cómo entra un grupo en la lista? | Cada método que pone el artículo en un grupo leído suma la parte de ese grupo con palabras del tema |

Un artículo sin grupo no se borra. Se mira a mano.

### Paso 2. Las palabras del tema
En este paso escribimos las palabras del tema antes de ver ningún grupo.
Con ellas decidimos en la evaluación qué grupos se leen.
La lista de la Lección 1 tiene entre 10 y 30 artículos.

```python
MIN_PAPERS = 10
MAX_PAPERS = 30
TOPIC_WORDS = {
    "obesity", "obese", "overweight",   # el peso
    "diet", "dietary",                  # lo que se come
    "diabetes", "cardiovascular", "hypertension",   # enfermedades que dependen de la dieta
}
print("Palabras del tema:", ", ".join(sorted(TOPIC_WORDS)))
```

**Comprobar:**

En este paso comprobamos que las palabras del tema están escritas en minúsculas.

```python
assert MIN_PAPERS < MAX_PAPERS
assert len(TOPIC_WORDS) >= 5 and all(w == w.lower() for w in TOPIC_WORDS)
print("Palabras del tema: OK")
```

---

## Parte 2. Comprensión de los datos

### Paso 1. Librerías y carpetas
En este paso importamos las librerías y creamos las carpetas.
Colab ya trae spaCy y scikit-learn.

```python
import math          # techo (ceil) para el umbral de soporte
import re            # partir el texto en palabras
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
import sklearn
from sklearn.cluster import HDBSCAN, KMeans
from sklearn.mixture import GaussianMixture
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import pairwise_distances, silhouette_score
from sklearn.preprocessing import normalize

DATA_DIR = Path("data")         # aquí quedan los datos descargados
OUTPUTS_DIR = Path("outputs")   # aquí quedan las tablas y los gráficos
DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
print(f"scikit-learn {sklearn.__version__}")
```

### Paso 2. Parámetros
En este paso fijamos los parámetros. No los cambie.
Los tres primeros vienen de la Lección 2.

```python
SUPPORT_SHARE = 0.03   # proporción de textos (L2)
SUPPORT_MIN = 5        # mínimo de textos (L2)
SEED = 7               # semilla (L2)

MAX_WORD_SHARE = 0.5          # una palabra en más de la mitad de los textos no separa grupos
DENSITY_SVD_DIRECTIONS = 10   # direcciones de la SVD para HDBSCAN
MIXTURE_DIRECTIONS = 5         # direcciones de la SVD para la mezcla gaussiana
K_CANDIDATES = range(3, 9)    # valores de k que probamos en k-means
MIN_SAMPLES = SUPPORT_MIN     # min_samples de HDBSCAN
READ_SHARE = 0.5              # se lee un grupo si al menos la mitad de sus artículos tiene una palabra del tema
TOP_WORDS = 4                 # palabras que mostramos por grupo


def support_floor(n_texts: int) -> int:
    """Soporte mínimo que necesita una palabra o un par: max(SUPPORT_MIN, ceil(SUPPORT_SHARE * n)).

    Qué hace: la misma función de la L2. En HDBSCAN es también el tamaño mínimo de un grupo.
    Entrada: n_texts, el número de textos.
    Salida: el umbral, un entero.
    """
    return max(SUPPORT_MIN, math.ceil(SUPPORT_SHARE * n_texts))   # el mayor entre 5 y el 3%


print(f"Umbral para 317 artículos: {support_floor(317)}")
```

**Comprobar:**

En este paso comprobamos el umbral de soporte y los valores de k que vamos a probar.

```python
assert support_floor(317) == 10
assert MIN_SAMPLES == SUPPORT_MIN and list(K_CANDIDATES) == [3, 4, 5, 6, 7, 8]
assert MIXTURE_DIRECTIONS == 5
print("Parámetros: OK")
```

### Paso 3. Las palabras útiles
En este paso traemos de la Lección 2 las palabras vacías y `words`.
`word_list` hace la misma limpieza y conserva las repeticiones, porque ahora contamos.

```python
from spacy.lang.en.stop_words import STOP_WORDS as STOP_WORDS_EN

WORD_RE = re.compile(r"[^\W\d_]+")   # secuencias de letras (sin números ni guiones bajos)
ABSTRACT_LABELS = {
    "background", "methods", "findings", "interpretation", "funding",
    "conclusions", "results", "objective", "objectives", "aims",
    "bill", "melinda", "gates", "foundation",
}
URL_TOKENS = {"http", "https", "www", "org"}
STOP_WORDS = set(STOP_WORDS_EN) | ABSTRACT_LABELS | URL_TOKENS   # las de la L2
```

```python
def word_list(text: str, stop_words: set[str]) -> list[str]:
    """Convierte un texto en la lista de sus palabras útiles, con repeticiones.

    Qué hace: pasa a minúsculas, quita el residuo "[cita requerida]" de Wikipedia,
    separa en palabras de letras y descarta las de menos de 3 letras y las palabras vacías.
    Entrada: text (un resumen o una descripción) y stop_words, el conjunto de palabras vacías.
    Salida: una lista de palabras, en orden y con cada aparición.
    Por qué: para agrupar contamos cuántas veces usa un texto cada palabra.
    """
    text = (text or "").lower().replace("[cita requerida]", " ")  # minúsculas, sin la marca de Wikipedia
    useful = []
    for word in WORD_RE.findall(text):  # por cada palabra de solo letras
        long_enough = len(word) >= 3
        is_stop = word in stop_words  # una palabra vacía, como "the" u "of"
        if long_enough and not is_stop:
            useful.append(word)
    return useful


def words(text: str, stop_words: set[str]) -> set[str]:
    """Convierte un texto en el conjunto de sus palabras útiles (la función de la L2).

    Qué hace: la misma limpieza que word_list, pero guarda cada palabra una sola vez.
    Entrada: text y stop_words.
    Salida: un set de palabras.
    Por qué: los patrones de la L2 y la regla de lectura solo preguntan si una palabra está.
    """
    return set(word_list(text, stop_words))  # la lista sin repeticiones


print(word_list("The diet, the DIET and the risk of obesity, see https://www.who.int", STOP_WORDS))
```

**Comprobar:**

En este paso comprobamos que `word_list` cuenta repeticiones y limpia igual que `words`.

```python
assert word_list("The diet, the DIET and the risk", STOP_WORDS) == ["diet", "diet", "risk"]
assert set(word_list("diet and risk, https://www.who.int", STOP_WORDS)) == words("diet and risk, https://www.who.int", STOP_WORDS)
print("Funciones de la L2: OK")
```

### Paso 4. Descargar los artículos
En este paso descargamos los artículos de nutrición, una sola vez, con la función de la Lección 2.

```python
BASE_URL = "https://cabrerac.github.io/assets/data/26-udenar-data-mining"


def download_data(name: str, folder: Path = DATA_DIR) -> Path:
    """Descarga un archivo de datos del curso, una sola vez.

    Qué hace: si el archivo ya está en la carpeta, lo usa. Si no, lo descarga de BASE_URL.
    Entrada: name, el nombre del archivo, y folder, la carpeta destino.
    Salida: la ruta local del archivo.
    Por qué: no queremos depender de la red en cada ejecución ni descargar dos veces.
    """
    dest = folder / name
    if dest.is_file() and dest.stat().st_size > 0:  # ya está y no está vacío
        print(f"Ya en caché: {dest}")
        return dest
    response = requests.get(f"{BASE_URL}/{name}", timeout=60)  # lo pedimos a la página del curso
    response.raise_for_status()  # para si la descarga falló
    dest.write_bytes(response.content)
    print(f"Descargado: {dest} ({dest.stat().st_size / 1e6:.1f} MB)")
    return dest


papers = pd.read_csv(download_data("nutricion-papers.csv"), keep_default_na=False)
print(f"Artículos descargados: {len(papers)}")
```

**Comprobar:**

En este paso comprobamos que están el título y el resumen.

```python
assert {"title", "abstract"} <= set(papers.columns)
print("Descarga: OK")
```

### Paso 5. Los artículos con resumen útil
En este paso dejamos fuera los resúmenes con menos de 5 palabras útiles.

```python
useful = []
for abstract in papers["abstract"]:   # por cada resumen
    useful.append(len(words(abstract, STOP_WORDS)) >= 5)   # al menos 5 palabras útiles
papers = papers[useful].reset_index(drop=True)
texts = papers["abstract"].tolist()
N = len(texts)
FLOOR = support_floor(N)
print(f"Artículos usados: {N} de {len(useful)}. Umbral: {FLOOR} artículos")
```

**Comprobar:**

En este paso comprobamos el número de artículos usados y el umbral.

```python
assert N == 317 and FLOOR == 10
print("Datos: OK")
```

### Paso 6. Las palabras del tema en los resúmenes
En este paso contamos en qué parte de los resúmenes aparece cada palabra del tema.

```python
word_sets = []
for text in texts:
    word_sets.append(words(text, STOP_WORDS))   # las palabras útiles de cada resumen
shares = {}
for word in sorted(TOPIC_WORDS):   # por cada palabra del tema
    with_word = 0
    for word_set in word_sets:
        if word in word_set:
            with_word += 1
    shares[word] = with_word / N   # la parte de los resúmenes con esa palabra
topic_share = pd.Series(shares).round(3)
print(topic_share.to_string())
```

Una palabra que está en casi todos los resúmenes describe toda la colección, no un grupo.
¿Alguna de estas palabras distingue un grupo de otro? Aquí ninguna pasa de 14%.

**Comprobar:**

En este paso comprobamos que hay una proporción por palabra del tema.

```python
assert len(topic_share) == len(TOPIC_WORDS) and topic_share.between(0, 1).all()
print("Palabras del tema en los resúmenes: OK")
```

### Paso 7. Los patrones de la Lección 2
En este paso leemos `outputs/patrones_l2.csv` de la Lección 2.
Si no está, la columna de patrones queda vacía. Suba el archivo a `outputs/`.

```python
PATTERNS_PATH = OUTPUTS_DIR / "patrones_l2.csv"
PATTERN_COLUMNS = ["pair", "support", "lift", "cosine", "kept", "kept_lift2", "beats_cosine", "shared_vector"]

if PATTERNS_PATH.is_file():
    patterns = pd.read_csv(PATTERNS_PATH)
    print(f"patrones_l2.csv: {len(patterns):,} pares, {patterns['kept_lift2'].sum():,} con lift de al menos 2")
else:
    patterns = pd.DataFrame(columns=PATTERN_COLUMNS)
    print("No encontramos outputs/patrones_l2.csv. Sin él, la columna de patrones queda vacía.")
```

**Comprobar:**

En este paso comprobamos que la tabla de patrones tiene sus columnas.

```python
assert set(PATTERN_COLUMNS) <= set(patterns.columns)
print("Patrones de la L2: OK")
```

---

## Parte 3. k-means

k-means parte de una tabla con una fila por artículo y una columna por palabra.
Cada fila queda de largo 1 para que el largo del resumen no pese más que el tema.

### Paso 1. Conteo de palabras con un vocabulario útil
En este paso contamos las palabras con `CountVectorizer`.
Una palabra entra si está en al menos `FLOOR` artículos y en no más de la mitad.
Con todas las palabras, todas las distancias se parecen y los grupos se pierden.

```python
token_lists = []
for text in texts:
    token_lists.append(word_list(text, STOP_WORDS))   # con repeticiones, porque ahora contamos
vectorizer = CountVectorizer(analyzer=lambda tokens: tokens, min_df=FLOOR, max_df=MAX_WORD_SHARE)
counts = vectorizer.fit_transform(token_lists)   # una matriz dispersa, casi toda ceros
vocabulary = vectorizer.get_feature_names_out()
print(f"Tabla de conteos: {counts.shape[0]} artículos x {counts.shape[1]} palabras")
```

**Comprobar:**

En este paso comprobamos la forma de la tabla y que no quedan restos de direcciones web.

```python
assert counts.shape == (317, 869)
assert not URL_TOKENS & set(vocabulary)
print("Conteos: OK")
```

### Paso 2. Escalar cada artículo a largo 1
En este paso dividimos cada fila por su largo con `normalize`.
Así el largo del resumen no pesa más que el tema.

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

---

## Parte 4. El ajuste de k-means

### Paso 1. Los centros
En este paso agrupamos con **k-means**: $k$ centros, y cada artículo va con el centro más cercano.
Minimiza $J = \sum_{i} \lVert x_i - \mu_{c(i)} \rVert^2$.
Corremos un k-means por cada $k$ de 3 a 8.

```python
kmeans_runs = {}
silhouettes = {}
for k in K_CANDIDATES:
    model = KMeans(n_clusters=k, n_init=10, random_state=SEED)
    model.fit(X)
    labels = model.labels_
    kmeans_runs[k] = labels
    silhouettes[k] = silhouette_score(X, labels, metric="cosine")
    sizes = np.bincount(labels).tolist()
    print(f"k = {k}: tamaños {sizes}, silueta {silhouettes[k]:.3f}")
K_CHOSEN = max(silhouettes, key=silhouettes.get)
kmeans_labels = kmeans_runs[K_CHOSEN]
print(f"k elegido: {K_CHOSEN}")
```

**Comprobar:**

En este paso comprobamos que hay un agrupamiento por cada $k$ y que el $k$ elegido tiene la silueta más alta.

```python
assert list(kmeans_runs) == list(K_CANDIDATES)
for labels in kmeans_runs.values():
    assert len(labels) == N
assert K_CHOSEN in K_CANDIDATES and silhouettes[K_CHOSEN] == max(silhouettes.values())
print("k-means: OK")
```

### Paso 2. La figura de la silueta
En este paso dibujamos la silueta de cada $k$ con las dos líneas de lectura.
Para un artículo, $a$ es la distancia media a su grupo y $b$ al grupo vecino.
Su silueta es $(b - a) / \max(a, b)$.

```python
plt.figure(figsize=(6, 3.5))
plt.plot(list(silhouettes), list(silhouettes.values()), marker="o", color="steelblue")
plt.axhline(0.25, color="darkorange", linestyle="--", label="0,25 o menos: sin estructura sustancial")
plt.axhline(0.5, color="seagreen", linestyle="--", label="0,26 a 0,50: débil, podría ser artificial")
plt.ylim(0, 0.6)
plt.xlabel("k")
plt.ylabel("Silueta media (coseno)")
plt.title("Silueta de k-means para cada k")
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(OUTPUTS_DIR / "silueta_l3.png", dpi=120)
plt.show()
```

Todas las siluetas quedan por debajo de 0,1.
k = 8 tiene la más alta, 0,075.
Ese es el límite de k-means en esta colección: todo artículo entra en un grupo, y la silueta no muestra una estructura sustancial.
El límite queda escrito. No se esconde el método.

### Paso 3. Las palabras de cada grupo
En este paso escribimos una función que da las palabras de más peso de un grupo.
La usan los tres métodos.

```python
def group_words(labels: np.ndarray, group: int, n: int = TOP_WORDS) -> list[str]:
    """Las n palabras de más peso en el promedio de los artículos de un grupo.

    Entrada: labels, el grupo de cada artículo, group, el grupo que leemos, y n.
    Salida: una lista de n palabras.
    Por qué: un grupo sin etiqueta solo se puede leer por sus palabras.
    """
    centre = np.asarray(X[labels == group].mean(axis=0)).ravel()
    order = np.argsort(centre)[::-1]
    top = []
    for j in order[:n]:
        top.append(str(vocabulary[j]))
    return top


print(group_words(kmeans_runs[3], 0))
```

**Comprobar:**

En este paso comprobamos que la función da `TOP_WORDS` palabras.

```python
assert len(group_words(kmeans_runs[3], 0)) == TOP_WORDS
print("Palabras de un grupo: OK")
```

---

## Parte 5. Mezcla gaussiana

La mezcla describe los artículos como nubes con forma de campana.
Cada artículo recibe una probabilidad por nube.
La preparación son las primeras 5 direcciones de la SVD, no las 10 de HDBSCAN.
El número de nubes es el $k$ que eligió la silueta.

### Paso 1. Cinco direcciones
En este paso reducimos los conteos a 5 direcciones.
Cada dirección mezcla palabras que suelen ir juntas.

```python
svd_mixture = TruncatedSVD(n_components=MIXTURE_DIRECTIONS, random_state=SEED)
svd_mixture.fit(X)
Z_mixture = svd_mixture.transform(X)
variance_mixture = svd_mixture.explained_variance_ratio_.sum()
print(f"Las 5 direcciones explican {variance_mixture:.1%}")
print(f"Forma: {Z_mixture.shape}")
```

**Comprobar:**

En este paso comprobamos la forma de las cinco direcciones.

```python
assert Z_mixture.shape == (N, MIXTURE_DIRECTIONS)
print("Direcciones de la mezcla: OK")
```

### Paso 2. El ajuste
En este paso ajustamos la mezcla y leemos la probabilidad de cada nube.

```python
mixture = GaussianMixture(n_components=K_CHOSEN, covariance_type="full", random_state=SEED)
mixture.fit(Z_mixture)
mixture_proba = mixture.predict_proba(Z_mixture)
mixture_labels = mixture_proba.argmax(axis=1)
print("Probabilidad del primer artículo:", mixture_proba[0].round(2))
print(f"Tamaños: {np.bincount(mixture_labels).tolist()}")
```

**Comprobar:**

En este paso comprobamos que hay una etiqueta por artículo y que las probabilidades suman 1.

```python
assert len(mixture_labels) == N
assert np.allclose(mixture_proba.sum(axis=1), 1)
print("Mezcla gaussiana: OK")
```

### Paso 3. Cuántos artículos abriría
En este paso aplicamos la misma regla del tema que usará la evaluación.
Un grupo se lee cuando al menos la mitad de sus artículos tiene una palabra del tema.
El número que sale es el límite de la forma de campana en esta colección.

```python
has_topic = np.zeros(N, dtype=bool)
for i, word_set in enumerate(word_sets):
    has_topic[i] = bool(word_set & TOPIC_WORDS)


def topic_parts(labels: np.ndarray) -> np.ndarray:
    """La parte con palabras del tema del grupo de cada artículo, si ese grupo se lee.

    Qué hace: por cada grupo calcula qué parte de sus artículos tiene una palabra del tema.
    Si llega a READ_SHARE, el grupo se lee y sus artículos reciben esa parte.
    Si no, reciben 0.
    El ruido (-1) nunca se lee.
    Entrada: labels, el grupo de cada artículo.
    Salida: un arreglo con un número entre 0 y 1 por artículo.
    Por qué: un grupo con más artículos del tema da más evidencia que uno que apenas llega.
    """
    part = np.zeros(len(labels))
    for g in sorted(set(labels) - {-1}):
        in_g = labels == g
        share = has_topic[in_g].mean()
        if share >= READ_SHARE:
            part[in_g] = round(share, 2)
    return part


mixture_part = topic_parts(mixture_labels)
mixture_read = (mixture_part > 0).astype(int)
print(f"La mezcla abriría {mixture_read.sum()} artículos")
```

La mezcla supone nubes con forma de campana.
El número de arriba es cuántos artículos abriría esa suposición con la regla del tema.
Queda escrito en la tabla de la evaluación.
No suma un punto en la lista y no escribe el archivo.

**Comprobar:**

En este paso comprobamos que la cuenta de artículos abiertos no pasa del total.

```python
assert mixture_read.sum() <= N
print("Límite de la mezcla: OK")
```

---

## Parte 6. HDBSCAN

HDBSCAN busca zonas densas.
Lo que no cae en una zona densa es ruido y se conserva.
La preparación es la distancia coseno sobre 10 direcciones.

### Paso 1. Diez direcciones
En este paso reducimos las columnas con la SVD, $X = U S V^T$.
`TruncatedSVD` calcula las primeras 10 y devuelve $Z = U S$.

```python
svd = TruncatedSVD(n_components=DENSITY_SVD_DIRECTIONS, random_state=SEED)
svd.fit(X)
Z = svd.transform(X)
variance_share = svd.explained_variance_ratio_
print(f"Las 10 direcciones explican {variance_share.sum():.1%}")
```

**Comprobar:**

En este paso comprobamos la forma de `Z`.

```python
assert Z.shape == (N, DENSITY_SVD_DIRECTIONS)
print("SVD: OK")
```

### Paso 2. Distancias
En este paso armamos la distancia coseno sobre las 10 direcciones.

```python
distances = pairwise_distances(Z, metric="cosine")
print(f"Distancias: {distances.shape}")
```

**Comprobar:**

En este paso comprobamos la forma de las distancias y que cada artículo está a 0 de sí mismo.

```python
assert distances.shape == (N, N) and np.allclose(np.diag(distances), 0, atol=1e-6)
print("Distancias: OK")
```

### Paso 3. El ajuste
En este paso buscamos las zonas densas.
Un grupo necesita al menos `FLOOR` artículos.
Lo que no queda en una zona densa es ruido ($-1$).

```python
hdbscan_model = HDBSCAN(
    min_cluster_size=FLOOR,
    min_samples=MIN_SAMPLES,
    metric="precomputed",
    copy=True,
)
hdbscan_model.fit(distances)
hdbscan_labels = hdbscan_model.labels_
n_groups = int(hdbscan_labels.max()) + 1
in_group = hdbscan_labels != -1
n_noise = int((~in_group).sum())
print(f"Grupos: {n_groups}. Tamaños: {np.bincount(hdbscan_labels[in_group]).tolist()}")
print(f"Ruido: {n_noise} artículos ({n_noise / N:.0%})")
```

El ruido es el límite de HDBSCAN.
No se borra.
El número queda escrito y entra en la tabla de la evaluación.

**Comprobar:**

En este paso comprobamos que hay grupos y que el ruido lleva $-1$.

```python
assert n_groups >= 1
assert set(np.unique(hdbscan_labels)) <= set(range(-1, n_groups))
print("HDBSCAN: OK")
```

### Paso 4. La lista de ruido
En este paso miramos el ruido. **No lo borramos.**
Un artículo sin vecinos claros puede ser el único de su tema.

```python
noise_list = papers.loc[~in_group, ["title", "year", "cited_by_count"]]
noise_list.sort_values("cited_by_count", ascending=False).head(5)
```

---

## Parte 7. Evaluación

La evaluación pone los tres métodos en una tabla.
No hay marcas para los grupos, así que la silueta dice qué tan separado queda cada artículo, entre −1 y 1.
Entre 0,26 y 0,50 la estructura es débil y podría ser artificial (Kaufman y Rousseeuw, 1990).
Con 0,25 o menos no hay estructura sustancial.
Un grupo se lee cuando al menos la mitad de sus artículos contiene una palabra del tema.
Un artículo que k-means y HDBSCAN ponen en un grupo leído es un candidato más fuerte.
La mezcla está en la tabla para documentar cuántos artículos abriría.
No suma un punto.

### Paso 1. La tabla de los tres métodos
En este paso reunimos grupos, ruido, silueta y artículos que la regla del tema abriría.
La silueta de HDBSCAN se mide sin el ruido.
La de la mezcla se mide en sus cinco direcciones.

```python
def reading_of(score: float) -> str:
    """La lectura de una silueta con los cortes de Kaufman y Rousseeuw (1990).

    Qué hace: compara la silueta media con los tres cortes y devuelve su banda.
    Entrada: score, una silueta media entre -1 y 1.
    Salida: el nombre de la banda.
    """
    if score > 0.70:
        return "estructura fuerte"
    if score > 0.50:
        return "estructura razonable"
    if score > 0.25:
        return "débil, podría ser artificial"
    return "sin estructura sustancial"


hdbscan_silhouette = np.nan
if n_groups > 1:
    hdbscan_silhouette = silhouette_score(X[in_group], hdbscan_labels[in_group], metric="cosine")
mixture_silhouette = silhouette_score(Z_mixture, mixture_labels, metric="cosine")
structure = pd.DataFrame({
    "method": ["k-means", "mezcla", "HDBSCAN"],
    "groups": [K_CHOSEN, K_CHOSEN, n_groups],
    "noise": [0, 0, n_noise],
    "silhouette": [silhouettes[K_CHOSEN], mixture_silhouette, hdbscan_silhouette],
    "leidos": [0, int(mixture_read.sum()), 0],
}).round(3)
structure["reading"] = structure["silhouette"].map(reading_of)
structure
```

k-means mete a todos en un grupo y su silueta queda por debajo de 0,1.
HDBSCAN deja el ruido fuera de la silueta: 108 de 317 resúmenes.
La columna `leidos` de la mezcla es el límite de la forma de campana.
Las tres filas quedan escritas. Los grupos son una ayuda para leer.

**Comprobar:**

En este paso comprobamos que la tabla tiene los tres métodos.

```python
assert structure["method"].tolist() == ["k-means", "mezcla", "HDBSCAN"]
print("Tabla de los tres métodos: OK")
```

### Paso 2. Qué grupos se leen
En este paso aplicamos la regla de lectura a k-means y a HDBSCAN.
La mezcla ya tiene su cuenta.
El ruido de HDBSCAN nunca se lee.

```python
part_of = {
    "kmeans": topic_parts(kmeans_labels),
    "mezcla": mixture_part,
    "hdbscan": topic_parts(hdbscan_labels),
}
read = {}
for method in ("kmeans", "hdbscan"):
    labels = kmeans_labels if method == "kmeans" else hdbscan_labels
    read[method] = (part_of[method] > 0).astype(int)
    print(f"\n{method}: {read[method].sum()} artículos en grupos leídos")
    for g in sorted(set(labels) - {-1}):
        share = has_topic[labels == g].mean()
        mark = "lee" if share >= READ_SHARE else "no lee"
        top = ", ".join(group_words(labels, g))
        print(f"  grupo {g} ({(labels == g).sum()} artículos, {share:.0%} con el tema, {mark}): {top}")
read_kmeans, read_hdbscan = read["kmeans"], read["hdbscan"]
structure.loc[structure["method"] == "k-means", "leidos"] = int(read_kmeans.sum())
structure.loc[structure["method"] == "HDBSCAN", "leidos"] = int(read_hdbscan.sum())
structure
```

k-means lee 2 grupos (56 artículos) y HDBSCAN 1 (10).
El grupo leído de HDBSCAN es el de las guías de diabetes.
El grupo de *obesity, food* no se lee: solo 32% de sus artículos tiene una palabra del tema.
Aceptamos el límite de HDBSCAN: el ruido queda contado y no se lee.
Documentamos el límite de la mezcla en `leidos` y no lo usamos para la lista.

¿Están de acuerdo con guardar HDBSCAN? Usen el ruido, la silueta y la columna `leidos`.

**ESCRIBA SU TEXTO AQUÍ**

**Comprobar:**

En este paso comprobamos que el ruido nunca se lee.

```python
assert not read_hdbscan[~in_group].any()
assert set(np.unique(read_kmeans)) <= {0, 1}
print("Grupos leídos: OK")
```

### Paso 3. Dónde coinciden k-means y HDBSCAN
En este paso contamos en cuántos métodos cae cada artículo dentro de un grupo leído.

```python
group_points = read_kmeans + read_hdbscan   # de 0 a 2
group_agreement = pd.Series(group_points).value_counts().reindex(range(3), fill_value=0)
print(group_agreement.rename_axis("métodos que lo leen").to_frame("artículos").T.to_string())
```

Solo 9 artículos caen en un grupo leído de los dos métodos.
Otros 48 caen en un grupo leído de uno solo.

**Comprobar:**

En este paso comprobamos que cada artículo cae en una sola cuenta.

```python
assert group_agreement.sum() == N
print("Coincidencias: OK")
```

### Paso 4. La figura de los tres métodos
En este paso dibujamos los artículos de cada grupo, método por método.
Las barras oscuras son los grupos leídos.

```python
method_labels = {
    "kmeans": kmeans_labels,
    "mezcla": mixture_labels,
    "hdbscan": hdbscan_labels,
}
fig, axes = plt.subplots(1, 3, figsize=(12, 3.2))
for ax, (method, labels) in zip(axes, method_labels.items()):
    names, sizes, colors = [], [], []
    for g in sorted(set(labels) - {-1}):
        names.append(str(g))
        sizes.append(int((labels == g).sum()))
        in_g = labels == g
        colors.append("steelblue" if part_of[method][in_g].max() > 0 else "lightgray")
    ax.bar(names, sizes, color=colors)
    opened = int((part_of[method] > 0).sum())
    ax.set_title(f"{method}: {opened} artículos")
    ax.set_xlabel("grupo")
axes[0].set_ylabel("artículos")
fig.tight_layout()
fig.savefig(OUTPUTS_DIR / "metodos_l3.png", dpi=120)
plt.show()
```

### Paso 7. Guardar los grupos
En este paso guardamos `outputs/grupos_l3.csv`, una fila por artículo.
Lleva el grupo de cada método y si ese grupo se lee.
`has_pattern` y `read_group` siguen para las Lecciones 5 y 6.

```python
topic_pairs = []
for pair in patterns.loc[patterns["kept_lift2"].astype(bool), "pair"]:   # pares de la L2 con lift de al menos 2
    a, b = pair.split(" + ")
    if TOPIC_WORDS & {a, b}:   # con una palabra del tema
        topic_pairs.append((a, b))
has_pattern = []
for word_set in word_sets:   # por cada resumen
    found = False
    for a, b in topic_pairs:
        if a in word_set and b in word_set:   # tiene un par del tema
            found = True
    has_pattern.append(found)
groups_table = pd.DataFrame({
    "title": papers["title"],
    "kmeans": kmeans_labels,
    "hdbscan": hdbscan_labels,
    "kmeans_leido": read_kmeans,
    "hdbscan_leido": read_hdbscan,
    "kmeans_parte": part_of["kmeans"],
    "hdbscan_parte": part_of["hdbscan"],
    "has_pattern": has_pattern,
    "read_group": group_points >= 1,   # al menos un método lo pone en un grupo leído
})
groups_path = OUTPUTS_DIR / "grupos_l3.csv"
groups_table.to_csv(groups_path, index=False)
print(f"Guardado: {groups_path} ({len(groups_table)} filas)")
```

**Comprobar:**

En este paso comprobamos que el archivo tiene una fila por artículo y sus columnas.

```python
saved = pd.read_csv(groups_path)
assert {"title", "kmeans", "hdbscan", "kmeans_leido", "hdbscan_leido"} <= set(saved.columns)
assert {"kmeans_parte", "hdbscan_parte", "has_pattern", "read_group"} <= set(saved.columns)
assert len(saved) == N
print("grupos_l3.csv: OK")
```

---

## Parte 8. Despliegue

### Paso 1. Qué hace un grupo con la lista
En este paso decimos para qué sirve un grupo leído.
El grupo nombra un filtro: los artículos que un método junta y que tratan del tema.
El archivo guarda HDBSCAN.
Aceptamos su límite: los artículos sin grupo quedan contados y no entran en la lista.
La mezcla queda documentada en la tabla y no suma evidencia.

### Paso 2. Artículos para leer
En este paso armamos la lista de lectura de esta lección.
Cada método que pone un artículo en un grupo leído suma la parte de ese grupo con palabras del tema, entre 0,5 y 1.
La evidencia es la suma, de 0 a 2. Así un grupo con más artículos del tema pesa más que uno que apenas llega a la mitad.
Ordenamos de mayor a menor evidencia, y después por título.
Mostramos como máximo 30 artículos, el máximo de la Lección 1.
Esta lista usa solo los grupos de hoy.

```python
reading_rows = []
for i in range(N):   # por cada artículo
    evidencia = part_of["kmeans"][i] + part_of["hdbscan"][i]   # la parte de cada método que lo lee
    if evidencia == 0:
        continue   # ningún método lo pone en un grupo leído
    reading_rows.append({
        "title": papers.loc[i, "title"],
        "kmeans": part_of["kmeans"][i],
        "hdbscan": part_of["hdbscan"][i],
        "evidencia": round(evidencia, 2),
    })

reading = pd.DataFrame(reading_rows)
reading = reading.sort_values(["evidencia", "title"], ascending=[False, True])   # más evidencia primero
reading_list = reading.head(MAX_PAPERS)   # como máximo 30 artículos
reading_path = OUTPUTS_DIR / "lectura_l3.csv"
reading_list.to_csv(reading_path, index=False)
print(f"Artículos con alguna evidencia: {len(reading)}. En la lista: {len(reading_list)}.")
reading_list.head(10)
```

57 artículos tienen evidencia. La lista guarda 30: arriba los 9 que leen los dos métodos, con 1,90, y después los que lee un solo método.
Hay varias ediciones de la misma guía de diabetes. El equipo abre la más reciente.

**Comprobar:**

En este paso comprobamos el largo de la lista, su orden y que la evidencia es la suma de los dos métodos.

```python
assert len(reading_list) == min(MAX_PAPERS, len(reading)) and reading_list["evidencia"].min() > 0
assert reading_list["evidencia"].is_monotonic_decreasing
assert ((reading_list["evidencia"] - reading_list["kmeans"] - reading_list["hdbscan"]).abs() < 0.011).all()
print("Lista de lectura: OK")
```

### Paso 3. Comprobación final
En este paso revisamos que el cuaderno dejó lo que la Lección 4 necesita.

```python
figures_ok = (OUTPUTS_DIR / "silueta_l3.png").is_file() and (OUTPUTS_DIR / "metodos_l3.png").is_file()
checks = {
    "outputs/grupos_l3.csv": groups_path.is_file(),
    "outputs/lectura_l3.csv": reading_path.is_file(),
    "Figuras de la silueta y de los tres métodos": figures_ok,
}
for name, ok in checks.items():
    print(f"{name}: {'OK' if ok else 'incompleto'}")
passed = sum(checks.values())
print(f"\nL3_CHECKS={passed}/{len(checks)}")
if passed == len(checks):
    print("L3_OK. Siga con la Lección 4.")
```

<!-- end NOTEBOOK: -->
