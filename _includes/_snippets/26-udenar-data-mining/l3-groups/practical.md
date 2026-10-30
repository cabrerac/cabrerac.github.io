<!-- NOTEBOOK: -->

## Repaso de Python para este cuaderno
 
Este repaso es corto. Muestra las tres piezas de `numpy` que usamos en la lección. Si ya las conoce, ejecute las celdas rápido y siga.
 
### Arreglos de `numpy`
Un **arreglo** guarda números en filas y columnas. En este cuaderno cada fila será un artículo y cada columna una palabra. `shape` dice cuántas filas y columnas tiene.



```python
import numpy as np

counts_toy = np.array([[2, 1, 0], [0, 1, 3]])   # 2 artículos, 3 palabras
print(counts_toy.shape)
print(counts_toy[0])          # la primera fila: el primer artículo
```

### El largo de un vector
El **largo** (la norma) de un vector es la raíz de la suma de sus valores al cuadrado. Dividir un vector por su largo lo deja de largo 1 y conserva su dirección.



```python
row = counts_toy[0].astype(float)
length = np.linalg.norm(row)
print(f"Largo: {length:.3f}. Después de escalar: {np.linalg.norm(row / length):.3f}")
```

### Coseno de vectores de largo 1
Si los dos vectores tienen largo 1, el **coseno** es solo el producto punto `u @ v`. Vale 1 si apuntan igual y 0 si no comparten ninguna palabra. Así comparamos un artículo largo con uno corto: cuenta la mezcla de palabras, no el largo.



```python
u = counts_toy[0] / np.linalg.norm(counts_toy[0])
v = counts_toy[1] / np.linalg.norm(counts_toy[1])
assert abs(np.linalg.norm(u) - 1) < 1e-9
print(f"Coseno: {u @ v:.3f}. Repaso de Python: OK")
```

---
 
## Instrucciones
 
**La historia.** Seguimos con el equipo interno del consejo. Tiene 320 artículos sobre nutrición y debe decidir cuáles leer. En la Lección 1 escribimos la pregunta y el estándar (una lista de 10 a 30 artículos). En la Lección 2 encontramos patrones: pares de palabras que se repiten más que por azar. Hoy buscamos **grupos**: artículos que usan palabras parecidas. Y buscamos los artículos que **no encajan en ningún grupo**.
 
**La idea central.** Un grupo es un conjunto de artículos más parecidos entre sí que con el resto. No sabemos de antemano cuántos grupos hay ni qué significan. Por eso juzgamos los grupos sin etiquetas: contra una línea base al azar, con varias semillas y comparando métodos. Un grupo sirve a la decisión solo si el equipo puede leerlo.
 
**Tres métodos, tres preparaciones.** Los tres parten del mismo conteo de palabras. Cada uno pide su propia forma de los datos.
 
| Método | Pregunta | Preparación que necesita | Qué deja fuera |
|--------|----------|--------------------------|----------------|
| M1. k-means | ¿Qué $k$ centros resumen mejor los artículos? | Los conteos, cada fila escalada a largo 1 | Nada: todo artículo entra en un grupo |
| M2. Mezcla gaussiana | ¿Qué probabilidad tiene cada artículo de venir de cada grupo? | Las 5 primeras componentes de la SVD, estandarizadas | Nada, pero marca a los dudosos |
| M3. HDBSCAN | ¿Dónde hay zonas densas de artículos? | Distancias coseno sobre las 10 primeras componentes | Los artículos sin vecinos claros (ruido) |
 
**Qué hacer.** Ejecute las celdas de arriba hacia abajo. Cada paso empieza con **En este paso**. Los pasos que crean algo nuevo terminan con una celda **Comprobar**. Si un `assert` falla, revise la celda anterior antes de seguir. Los nombres del código están en inglés, como en todos los cuadernos del curso. Las explicaciones están en español.
 
**Mapa del cuaderno**
 
| Parte | Fase CRISP-DM | Qué sale |
|-------|---------------|----------|
| 1 | Configuración | Librerías, parámetros y funciones de la L2 |
| 2 | Comprensión del negocio | `pregunta.json` y `outputs/patrones_l2.csv` de la Lección 2 |
| 3 | Comprensión de los datos | Los artículos con resumen útil |
| 4 | Preparación de los datos | Conteos escalados, SVD y distancias |
| 5 | Modelado | Grupos de k-means, de la mezcla y de HDBSCAN |
| 6 | Evaluación | Línea base, estabilidad, acuerdo y qué significa cada grupo |
| 7 | Despliegue | La tabla de `supports` y `outputs/grupos_l3.csv` |

---
 
## Parte 1. Configuración
 
### Paso 1. Librerías, carpetas y parámetros
En este paso importamos las librerías y fijamos los parámetros. El bloque de la L2 se copia sin cambios. Los parámetros nuevos de la L3 se definen aquí una sola vez y son los mismos en el cuaderno de grupo y en el script de control del curso. No los cambie aquí.
 
**Una sola regla de umbral para el curso.** El grupo más chico que HDBSCAN puede formar tiene el mismo tamaño que el patrón más chico que la L2 puede conservar: `support_floor(n)`.
 
**Nada que instalar.** Colab ya trae spaCy y scikit-learn. HDBSCAN necesita scikit-learn 1.3 o más nuevo, y la celda de comprobación lo revisa.



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

# L3 (compartidos con el cuaderno de grupo y el script de control, no cambiar)
MAX_WORD_SHARE = 0.5         # palabras en más de la mitad de los textos no separan grupos
MIXTURE_COMPONENTS = 5       # dimensiones para la mezcla gaussiana
DENSITY_COMPONENTS = 10      # dimensiones para HDBSCAN
K_CANDIDATES = range(3, 9)   # valores de k que probamos en k-means
MIN_SAMPLES = SUPPORT_MIN    # min_samples de HDBSCAN
# min_cluster_size de HDBSCAN = support_floor(n), la misma regla que un patrón
N_SHUFFLES = 30              # tablas al azar de la línea base

# Decisión, L3 en adelante
MIN_SUPPORTS = 2             # un artículo queda en vista con al menos dos apoyos

# Propios de este cuaderno
MIXTURE_K = range(1, 9)      # números de grupos que prueba la mezcla
UNSURE_PROB = 0.6            # por debajo de esta probabilidad, el artículo es dudoso
STABILITY_SEEDS = range(5)   # semillas 0 a 4 para la estabilidad
TOP_WORDS = 8                # palabras que mostramos por grupo


# support_floor: mismo código que scripts/data-mining-course/swap_randomization.py, salvo docstrings y comentarios en español.
def support_floor(n_texts: int) -> int:
    """Soporte mínimo que necesita una palabra o un par: max(SUPPORT_MIN, ceil(SUPPORT_SHARE * n))."""
    return max(SUPPORT_MIN, math.ceil(SUPPORT_SHARE * n_texts))


print(f"scikit-learn {sklearn.__version__}")
print(f"Umbral para 317 artículos: {support_floor(317)}")
```

**Comprobar:**



```python
assert support_floor(317) == 10
assert MIN_SAMPLES == SUPPORT_MIN and list(K_CANDIDATES) == [3, 4, 5, 6, 7, 8]
assert tuple(int(v) for v in sklearn.__version__.split(".")[:2]) >= (1, 3)
print("Parámetros: OK")
```

### Paso 2. Funciones de la Lección 2
En este paso traemos lo que volvemos a usar de la L2: la descarga, las palabras vacías, la función `words` y el percentil 95 por rango. La función `words` devuelve un **conjunto** (cada palabra una vez). Para agrupar necesitamos **cuántas veces** aparece cada palabra, así que `word_list` hace la misma limpieza y devuelve una lista con repeticiones. Las dos usan `STOP_WORDS` de la L2, con las etiquetas del resumen y los restos de direcciones web.



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



```python
assert word_list("The diet, the DIET and the risk", STOP_WORDS) == ["diet", "diet", "risk"]
assert set(word_list("diet and risk, https://www.who.int", STOP_WORDS)) == words("diet and risk, https://www.who.int", STOP_WORDS)
assert p95(list(range(30))) == 28
print("Funciones de la L2: OK")
```

---
 
## Parte 2. Comprensión del negocio
 
### Paso 1. Recuperar la pregunta
En este paso leemos `pregunta.json`, la tarjeta de las Lecciones 1 y 2. Si abre este cuaderno en un Colab nuevo, el archivo no está. En ese caso la celda escribe la misma tarjeta para que pueda seguir.
 
Aquí también escribimos `TOPIC_WORDS`, las palabras del tema del equipo: la dieta y las enfermedades que dependen de ella. Las escribimos ahora, desde la pregunta y antes de ver ningún grupo, porque en la Parte 6 decidimos con ellas qué grupos lee el equipo. Si las escribiéramos después de ver los grupos, elegiríamos las palabras que hacen entrar a un grupo.



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
            "may_not": ["citar la lista como evidencia del consejo", "elegir artículos solo por sus citas"],
        },
        "pattern_use": {"rule": "Un artículo entra en la lista cuando lo apoyan al menos dos resultados del curso."},
    }
    QUESTION_PATH.write_text(json.dumps(question_card, ensure_ascii=False, indent=2), encoding="utf-8")
    print("pregunta.json no estaba. Escribimos la tarjeta de la Lección 2.")

TOPIC_WORDS = {"obesity", "obese", "overweight", "diet", "dietary", "diabetes", "cardiovascular", "hypertension"}

print(question_card["question"])
print("Regla:", question_card["pattern_use"]["rule"])
print("Palabras del tema:", ", ".join(sorted(TOPIC_WORDS)))
```

**Comprobar:**



```python
assert {"question", "standard", "pattern_use"} <= set(question_card)
assert len(TOPIC_WORDS) >= 5 and all(w == w.lower() for w in TOPIC_WORDS)
print("Pregunta y palabras del tema: OK")
```

### Paso 2. Recuperar los patrones de la Lección 2
En este paso leemos `outputs/patrones_l2.csv`, la tabla que guardó la L2. Usaremos los patrones que **destacan** (`kept_lift2`) en la Parte 7, como el primer apoyo de cada artículo. Si el archivo no está (un Colab nuevo), súbalo desde su cuaderno de la L2 a la carpeta `outputs/`. Sin él, el cuaderno sigue, pero la columna de patrones queda vacía.



```python
PATTERNS_PATH = OUTPUTS_DIR / "patrones_l2.csv"
PATTERN_COLUMNS = ["pair", "support", "null_p95", "lift", "cosine", "kept", "kept_lift2", "beats_cosine", "shared_vector"]

if PATTERNS_PATH.is_file():
    patterns = pd.read_csv(PATTERNS_PATH)
    print(f"patrones_l2.csv: {len(patterns):,} pares, {patterns['kept_lift2'].sum():,} destacan")
else:
    patterns = pd.DataFrame(columns=PATTERN_COLUMNS)
    print("No encontramos outputs/patrones_l2.csv. Súbalo desde la L2 y vuelva a ejecutar esta celda.")
patterns.head(3)
```

**Comprobar:**



```python
assert list(patterns.columns) == PATTERN_COLUMNS
print("Patrones de la L2: OK")
```

---
 
## Parte 3. Comprensión de los datos
 
### Paso 1. Los artículos con resumen útil
En este paso cargamos los artículos y aplicamos la regla de la L2: dejamos fuera los resúmenes con menos de 5 palabras distintas. Son fragmentos como "Peer Reviewed", no resúmenes. El archivo tiene 320 filas y quedan 317.



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



```python
assert N == 317 and FLOOR == 10
assert len(papers) == N
print("Datos: OK")
```

---
 
## Parte 4. Preparación de los datos
 
Los tres métodos parten de la misma tabla: una fila por artículo, una columna por palabra, y en cada celda cuántas veces aparece la palabra. Después cada método pide algo más. k-means usa esa tabla escalada. La mezcla y HDBSCAN usan una versión con pocas dimensiones.
 
**Una palabra nueva para "ítem".** En la L2 una palabra era un ítem en la canasta de un texto. Desde ahora, el ítem es el texto que agrupamos.
 
### Paso 1. Conteo de palabras con un vocabulario útil
En este paso contamos las palabras con `CountVectorizer` de scikit-learn. Primero hacemos una lista de palabras por artículo con `word_list`, la regla de la L2. Luego `analyzer=lambda tokens: tokens` le dice a `CountVectorizer` que el texto ya viene partido. Le damos dos límites:
 
- `min_df=FLOOR`: una palabra debe aparecer en al menos 10 artículos, el mismo umbral de la L2. Una palabra rara no puede formar un grupo.
- `max_df=MAX_WORD_SHARE`: una palabra que aparece en más de la mitad de los artículos tampoco separa grupos. Está en todos lados.



```python
token_lists = [word_list(t, STOP_WORDS) for t in texts]
vectorizer = CountVectorizer(analyzer=lambda tokens: tokens, min_df=FLOOR, max_df=MAX_WORD_SHARE)
counts = vectorizer.fit_transform(token_lists)
vocabulary = vectorizer.get_feature_names_out()
print(f"Tabla de conteos: {counts.shape[0]} artículos x {counts.shape[1]} palabras")
print(f"Celdas distintas de 0: {counts.nnz:,} ({counts.nnz / (counts.shape[0] * counts.shape[1]):.1%})")
```

La tabla es casi toda ceros. Cada artículo usa unas pocas decenas de las 869 palabras. Por eso scikit-learn la guarda como **matriz dispersa**: solo anota las celdas distintas de 0. Las palabras *http*, *https*, *www* y *org* no están: `STOP_WORDS` las quitó, como en la L2.
 
**Comprobar:**



```python
assert counts.shape == (317, 869)
assert not URL_TOKENS & set(vocabulary)
print("Conteos: OK")
```

### Paso 2. Escalar cada artículo a largo 1
En este paso dividimos cada fila por su largo con `normalize`. Un resumen de 500 palabras tiene conteos mucho más grandes que uno de 50. Sin escalar, el largo pesaría más que el tema. Con filas de largo 1, el coseno entre dos artículos es su producto punto, como en el repaso.



```python
X = normalize(counts)   # cada fila queda de largo 1
row_lengths = np.sqrt(X.multiply(X).sum(axis=1)).A1
print(f"Largo de las filas: mínimo {row_lengths.min():.3f}, máximo {row_lengths.max():.3f}")
```

**Comprobar:**



```python
assert np.allclose(row_lengths, 1)
print("Filas de largo 1: OK")
```

### Paso 3. Pocas dimensiones con la SVD
En este paso reducimos las 869 columnas a unas pocas con la **descomposición en valores singulares** (SVD). La SVD escribe la tabla como $X = U S V^T$. Cada componente es una mezcla de palabras que suelen ir juntas. Aplicada a textos, se llama **análisis semántico latente** (LSA).
 
Usamos `TruncatedSVD`, que trabaja con matrices dispersas y calcula solo las primeras 10 componentes (`DENSITY_COMPONENTS`). `fit_transform` devuelve $Z = U S$: una fila por artículo, una columna por componente. `explained_variance_ratio_` dice qué parte de la variación de la tabla explica cada componente.



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

La curva sube despacio. Con 10 componentes explicamos menos de una cuarta parte de la variación. Es una primera señal: los artículos no se ordenan en pocos temas claros. Aun así, las primeras componentes guardan la parte más grande de la variación y quitan mucho ruido.
 
**Comprobar:**



```python
assert Z.shape == (317, DENSITY_COMPONENTS)
assert 0.15 < variance_share.sum() < 0.35
print("SVD: OK")
```

### Paso 4. La preparación de la mezcla y de HDBSCAN
En este paso armamos la entrada de M2 y de M3.
 
- **M2.** Las 5 primeras componentes, estandarizadas con `StandardScaler` (media 0 y desviación 1 en cada columna). La mezcla gaussiana estima una forma por grupo. Con 5 columnas tiene pocas cosas que estimar.
- **M3.** La distancia coseno entre artículos, $1 - \cos$, sobre las 10 componentes de `Z`. HDBSCAN recibe la matriz de distancias ya hecha (`metric="precomputed"`).



```python
Z_mixture = StandardScaler().fit_transform(Z[:, :MIXTURE_COMPONENTS])
distances = pairwise_distances(Z, metric="cosine")
print(f"Entrada de M2: {Z_mixture.shape}. Entrada de M3: {distances.shape}")
print(f"Distancia coseno: mediana {np.median(distances):.2f}, de {distances.min():.2f} a {distances.max():.2f}")
```

**Comprobar:**



```python
assert Z_mixture.shape == (317, MIXTURE_COMPONENTS) and abs(Z_mixture.mean()) < 1e-9
assert distances.shape == (317, 317) and np.allclose(np.diag(distances), 0, atol=1e-6)
print("Preparación de M2 y M3: OK")
```

### Paso 5. ¿Por qué no usar todas las palabras?
En este paso vemos qué pasa si HDBSCAN trabaja sobre las 869 palabras, sin la SVD. Con muchas dimensiones, casi todos los artículos quedan a distancias parecidas entre sí. Los vecinos dejan de ser claros. Es la **maldición de la dimensión**.



```python
D_all_words = pairwise_distances(X, metric="cosine")
all_words_labels = HDBSCAN(min_cluster_size=FLOOR, min_samples=MIN_SAMPLES, metric="precomputed", copy=True).fit(D_all_words).labels_
print(f"Con todas las palabras: {all_words_labels.max() + 1} grupos, {(all_words_labels == -1).mean():.0%} de ruido")
print(f"Distancia coseno con todas las palabras: mediana {np.median(D_all_words):.2f}. Con 10 componentes: {np.median(distances):.2f}")
```

Con todas las palabras, la distancia mediana entre artículos está cerca de 1: casi ningún par comparte vocabulario. HDBSCAN encuentra solo 2 grupos y deja el 40 % como ruido. En los extractos de Wikipedia es peor: en dos de ellos no encuentra ningún grupo y en los otros deja entre el 50 % y el 75 % como ruido. Por eso M3 trabaja sobre 10 componentes.

---
 
## Parte 5. Modelado
 
### M1. k-means
En este paso agrupamos con **k-means**. El método busca $k$ centros y pone cada artículo con el centro más cercano. Minimiza la suma de distancias al cuadrado de cada artículo a su centro:
 
$\displaystyle J = \sum_{i=1}^{N} \lVert x_i - \mu_{c(i)} \rVert^2$
 
Los pasos de Lloyd alternan dos cosas: asignar cada artículo a su centro más cercano y mover cada centro al promedio de sus artículos. `KMeans` de scikit-learn empieza con k-means++ y prueba 10 arranques (`n_init=10`).
 
**Cómo elegir k: la silueta.** Para cada artículo, $a$ es su distancia media a los de su grupo y $b$ la distancia media al grupo vecino más cercano. Su silueta es $s = (b - a) / \max(a, b)$. Cerca de 1, el artículo está bien en su grupo. Cerca de 0, está entre dos grupos. Promediamos sobre todos los artículos, con distancia coseno.



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

**La silueta es baja y plana.** Va de 0,06 a 0,08 para todos los $k$. No hay un $k$ natural en estos artículos. Tomamos el $k$ con la silueta más alta, 8, porque da grupos de unos 40 artículos, un tamaño que el equipo puede revisar. Elegimos $k$ **para el uso**, no porque los datos lo digan. Lo dejamos escrito. La línea base, la estabilidad y el acuerdo de la Parte 6 usan este $k = 8$.
 
**Comprobar:**



```python
assert K_CHOSEN == 8
assert max(silhouettes.values()) < 0.1
print("M1: OK")
```

### M1. Las palabras de cada grupo
En este paso leemos cada grupo por sus palabras. El centro de un grupo es el promedio de sus artículos escalados. Las palabras con más peso en el centro dicen de qué habla el grupo.



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

Algunos grupos se leen bien: uno sobre obesidad y alimentos, otro sobre diabetes, otro sobre riesgo cardiovascular, otro sobre la carga global de enfermedad (*burden*). Otros mezclan palabras de método (*data*, *studies*, *research*). Un grupo de método no dice de qué tema trata un artículo, dice cómo se escribió.
 
**Comprobar:**



```python
assert len(kmeans_words) == K_CHOSEN
assert np.bincount(kmeans_labels).min() >= 5
print("Palabras de M1: OK")
```

### M2. Mezcla gaussiana
En este paso ajustamos una **mezcla gaussiana**. Suponemos que cada artículo viene de uno de $K$ grupos, y cada grupo tiene forma de campana (una normal con su media y su covarianza):
 
$\displaystyle p(x) = \sum_{k=1}^{K} \pi_k \, \mathcal{N}(x \mid \mu_k, \Sigma_k)$
 
El algoritmo EM alterna dos pasos. Primero calcula, para cada artículo, la probabilidad de venir de cada grupo (las **responsabilidades**). Después mueve los pesos $\pi_k$, las medias y las covarianzas. A diferencia de k-means, los grupos pueden ser alargados.
 
**Cómo elegir K: el BIC.** El criterio de información bayesiano premia el ajuste y castiga los parámetros: $\text{BIC} = -2 \log L + p \log N$. Elegimos el $K$ con el BIC más bajo.



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



```python
assert K_MIXTURE == 4
print("M2: OK")
```

### M2. Pertenencia suave
En este paso leemos la **pertenencia suave**. `predict_proba` da, para cada artículo, la probabilidad de cada grupo. Un artículo cuya probabilidad más alta queda bajo 0,6 (`UNSURE_PROB`) no encaja bien en ningún grupo. Lo llamamos **dudoso**.



```python
membership = mixture.predict_proba(Z_mixture)
mixture_labels = mixture.predict(Z_mixture)   # el grupo más probable de cada artículo
top_prob = membership.max(axis=1)
unsure = top_prob < UNSURE_PROB
print(f"Tamaño de cada grupo: {np.bincount(mixture_labels).tolist()}")
print(f"Artículos dudosos (probabilidad más alta bajo {UNSURE_PROB}): {unsure.sum()} ({unsure.mean():.1%})")
papers.loc[unsure, ["title"]].head(5)
```

Pocos artículos son dudosos. Eso no quiere decir que los grupos sean claros. La mezcla trabaja sobre 5 componentes que explican solo una parte chica de la variación, y en tan pocas dimensiones casi todo artículo queda cerca de una campana. La seguridad de la mezcla es la seguridad del modelo, no de los datos.
 
**Comprobar:**



```python
assert np.allclose(membership.sum(axis=1), 1)
assert unsure.mean() < 0.2
print("Pertenencia suave: OK")
```

### M3. HDBSCAN
En este paso buscamos **zonas densas** con HDBSCAN. La idea, en cuatro pasos:
 
1. La **distancia de núcleo** de un artículo es la distancia a su vecino número `min_samples`. Es chica en zonas densas.
2. La **distancia de alcance mutuo** entre dos artículos es la mayor entre su distancia y las dos distancias de núcleo. Aleja a los artículos de zonas poco densas.
3. Con esa distancia arma un árbol que une a todos los artículos y lo corta a distintas alturas.
4. Se queda con los grupos más **estables** a lo largo de los cortes, con al menos `min_cluster_size` artículos. Los que no entran en ninguno reciben la etiqueta $-1$: **ruido**.
 
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

Cuatro de los cinco grupos densos se leen con claridad: cáncer (16), diabetes (10), guías clínicas (38) y la carga global de enfermedad (58). El quinto, con 87 artículos, es más grande que cualquier grupo de k-means y mezcla palabras de método (*studies*, *data*, *research*). Ninguno es solo de obesidad. Los artículos de obesidad quedan repartidos o como ruido.
 
**Comprobar:**



```python
assert n_groups == 5
assert 0.3 < noise < 0.4
print("M3: OK")
```

### M3. La lista de ruido
En este paso miramos los artículos que HDBSCAN deja como ruido. **No los borramos.** Un artículo sin vecinos claros puede ser el único sobre un tema, o un artículo que mezcla varios. Para el equipo es una lista para mirar a mano.



```python
noise_list = papers.loc[~in_group, ["title", "year", "cited_by_count"]]
print(f"Artículos sin grupo: {len(noise_list)}")
noise_list.sort_values("cited_by_count", ascending=False).head(10)
```

Uno de cada tres artículos queda fuera de todo grupo denso. k-means los mete igual en alguno de sus 8 grupos, porque no tiene otra opción. HDBSCAN dice lo que k-means esconde.

---
 
## Parte 6. Evaluación
 
No tenemos etiquetas, así que no hay "respuesta correcta" con la que comparar. Juzgamos los grupos de cuatro maneras: contra el azar, entre semillas, entre métodos y por lo que dicen sus palabras.
 
### Paso 1. Silueta contra una línea base al azar
En este paso preguntamos qué silueta daría una tabla **sin grupos**. El azar debe conservar algo de los datos: aquí, cada palabra aparece en el mismo número de artículos y con los mismos conteos. Barajamos cada columna por separado, 30 veces (`N_SHUFFLES`), y corremos k-means con el $k$ elegido en cada tabla barajada. El percentil 95 de esas siluetas, con la regla `p95()` de la L2, es la línea base.
 
**Una diferencia con la L2.** El intercambio (swap) de la L2 conservaba también el largo de cada texto. Este azar no lo conserva. No hace falta: las filas se escalan a largo 1, así que lo que se compara es la mezcla de palabras, no el largo.
 
**Tiempo.** La celda corre k-means 30 veces con 10 arranques. En la máquina de prueba del curso tardó unos 10 s. En Colab gratuito calcule entre 20 s y un minuto.



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

`np.apply_along_axis(rng.permutation, 0, dense)` baraja cada columna por separado: cada palabra conserva sus conteos, pero en otros artículos. Desaparece cualquier relación entre palabras.
 
La silueta real supera al azar, pero por poco: 0,075 contra 0,054. Hasta una tabla sin ningún grupo da una silueta de 0,05. Los grupos de k-means existen, pero son débiles.
 
**Comprobar:**



```python
assert len(shuffled_silhouettes) == N_SHUFFLES
assert silhouettes[K_CHOSEN] > BASELINE_P95
print("Línea base: OK")
```

### Paso 2. Estabilidad entre semillas
En este paso repetimos k-means con 5 semillas fijas, de 0 a 4, con los mismos 10 arranques del modelo que usamos. Comparamos los 10 pares de resultados con el **índice de Rand ajustado** (ARI). El ARI vale 1 si dos agrupaciones son iguales y cerca de 0 si coinciden como por azar. No importa el número que cada grupo recibe, solo quién queda con quién.



```python
# n_init=10 en cada semilla: vea el comentario de la mezcla (M2)
seed_labels = [KMeans(n_clusters=K_CHOSEN, n_init=10, random_state=s).fit(X).labels_ for s in STABILITY_SEEDS]
seed_ari = [adjusted_rand_score(a, b) for a, b in combinations(seed_labels, 2)]   # los 10 pares de semillas
print(f"ARI entre semillas (10 pares): media {np.mean(seed_ari):.2f}, de {min(seed_ari):.2f} a {max(seed_ari):.2f}")
```

Con otra semilla, k-means arma grupos bastante distintos. El ARI medio está cerca de 0,45, mucho más cerca del azar (0) que de dos agrupaciones iguales (1). Con un solo arranque por semilla sería aún más bajo.
 
**Comprobar:**



```python
assert len(seed_ari) == 10
assert 0.2 < np.mean(seed_ari) < 0.7
print("Estabilidad: OK")
```

### Paso 3. Tamaños y acuerdo entre los tres métodos
En este paso ponemos los tres métodos lado a lado. Primero los tamaños de sus grupos. Después el acuerdo, con el mismo ARI. Para HDBSCAN usamos solo los artículos que no son ruido, porque el ruido no es un grupo.



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

La columna `left_out` dice qué deja fuera cada método: k-means nada, la mezcla marca a los dudosos y HDBSCAN deja el ruido. Los métodos coinciden más en los artículos que HDBSCAN pone en un grupo. Son los artículos de zonas densas, y ahí cualquier método los junta. En el resto cada método decide distinto. No es una competencia: cada método responde una pregunta distinta.
 
**Comprobar:**



```python
assert sizes["groups"].tolist() == [K_CHOSEN, K_MIXTURE, n_groups]
assert agreement.loc[1, "ari"] > agreement.loc[0, "ari"]
print("Acuerdo: OK")
```

### Paso 4. Qué significa un grupo para el equipo
En este paso decidimos qué grupos **lee el equipo**. Los grupos de la decisión son los de **HDBSCAN**, porque HDBSCAN no obliga a ningún artículo a entrar en un grupo: un artículo de ruido no recibe apoyo, y se mira a mano. k-means, con k = 8, nos sirvió para la estabilidad y el acuerdo entre métodos, no para decidir.
 
El tema del equipo es la dieta y las enfermedades que dependen de ella. Sus palabras, `TOPIC_WORDS`, las escribimos en la Parte 2, antes de mirar ningún grupo. Aquí no las tocamos. El equipo lee un grupo de HDBSCAN si alguna de esas palabras está entre sus 8 palabras de más peso. La celda muestra todos los grupos con sus palabras, para que se vea qué se lee y qué no.



```python
team_groups = sorted(g for g, group_words in hdbscan_words.items() if TOPIC_WORDS & set(group_words))
read_group = np.isin(hdbscan_labels, team_groups)   # el ruido (-1) nunca está en team_groups
for g, group_words in hdbscan_words.items():
    mark = "lee" if g in team_groups else "no lee"
    print(f"Grupo {g} ({(hdbscan_labels == g).sum()} artículos, {mark}): {', '.join(group_words)}")
print(f"Grupos que lee el equipo: {team_groups}. Artículos en ellos: {read_group.sum()}")
print(f"Ruido, sin apoyo y para mirar a mano: {(~in_group).sum()} artículos")
```

Solo uno de los 5 grupos de HDBSCAN toca el tema por sus palabras: el de diabetes, con 10 artículos. Los otros cuatro (cáncer, guías clínicas, carga global de enfermedad y un grupo amplio de datos e investigación) no lo tocan, aunque traten de salud. Muchos artículos del tema, como los de obesidad, quedan en el ruido: 108 artículos no tienen grupo, no reciben este apoyo y se miran a mano.
 
**Comprobar:**



```python
assert 1 <= len(team_groups) < n_groups and not read_group[~in_group].any()
print("Grupos del tema: OK")
```

### Paso 5. Una vista de los grupos
En este paso dibujamos los artículos sobre las dos primeras componentes de la SVD, con el color de su grupo de HDBSCAN. El ruido va en gris. Los artículos de un grupo que lee el equipo llevan borde negro. Es una sombra de 869 dimensiones en 2, así que grupos que se tocan aquí pueden estar separados en otras componentes.



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
En este paso leemos los números con calma. En los artículos, la silueta de k-means queda entre 0,06 y 0,08 según el valor de k. En los extractos de Wikipedia de los grupos queda entre 0,03 y 0,12. Una silueta de 1 diría que cada artículo está mucho más cerca de su grupo que de cualquier otro. Una silueta cerca de 0 dice que muchos artículos quedan a medio camino entre dos grupos. Nuestros valores están cerca de 0.
 
Esto no es un error del código. Es un hallazgo sobre los datos. Los textos de un mismo tema comparten mucho vocabulario, y los subtemas se mezclan. Un artículo sobre obesidad también habla de dieta y de diabetes.
 
Tres comprobaciones nos dicen cuánto confiar en los grupos:
 
1. **Línea base.** Repartimos al azar las palabras entre los artículos, 30 veces, y medimos la silueta cada vez. Cada palabra conserva el número de artículos en que aparece. Si la silueta real apenas supera el percentil 95 del azar, los grupos son débiles.
2. **Estabilidad.** Repetimos k-means con 5 semillas fijas (de 0 a 4) y comparamos los resultados con el índice de Rand ajustado. Un valor bajo dice que los grupos cambian con la semilla. En nuestros extractos la media queda entre 0,37 y 0,57.
3. **Ruido.** HDBSCAN no obliga a ningún artículo a entrar en un grupo. Entre el 29 % y el 52 % de los textos queda como ruido, según el extracto. Ese número dice cuántos textos no tienen vecinos claros.
 
Un grupo débil no es un resultado inútil. Nos dice que no debemos decidir con un grupo solo. Por eso la regla de la decisión pide al menos dos apoyos para dejar un artículo en vista.



```python
print(f"Silueta con k = {K_CHOSEN}: {silhouettes[K_CHOSEN]:.3f}. Percentil 95 de la línea base: {BASELINE_P95:.3f}")
print(f"Estabilidad entre semillas (ARI medio): {np.mean(seed_ari):.2f}")
print(f"Ruido de HDBSCAN: {noise:.0%} de los artículos")
```

**Hallazgo sobre la estructura (completen con sus números).** Copie los números de la celda anterior y escriba qué significan para la lista del equipo.



```python
structure_finding = """
- Silueta con k = ___: ___. Percentil 95 de la línea base: ___.
- Estabilidad entre semillas (índice de Rand ajustado medio): ___.
- Ruido de HDBSCAN: ___ % de los artículos.
- Qué significa para nuestra lista: ___.
"""
print(structure_finding)
```

Ejemplo de una frase final: "En nuestro extracto los grupos son débiles. La silueta supera al azar por poco y cambia con la semilla. No usamos un grupo solo para decidir qué leer. Un artículo queda en vista solo si lo apoyan al menos dos resultados."
 
**Qué cambiaría esta lectura.** Otro valor de k, otro umbral de soporte, otra preparación del texto (por ejemplo TF-IDF, que veremos en L4), o una pregunta que pida grupos más amplios.

---
 
## Parte 7. Despliegue
 
### Paso 1. La tabla de apoyos
En este paso juntamos los dos resultados que tenemos hasta ahora. Cada uno da un **apoyo** a un artículo, en su propia columna de `SUPPORT_COLUMNS`:
 
- **`has_pattern` (L2).** El resumen tiene las dos palabras de un patrón que destaca (`kept_lift2`) y que toca el tema (al menos una palabra de `TOPIC_WORDS`).
- **`read_group` (L3).** El artículo está en un grupo de HDBSCAN que el equipo lee. El ruido no recibe este apoyo.
 
Un artículo queda **en vista** cuando tiene al menos `MIN_SUPPORTS` (2) apoyos. Con dos resultados, eso pide los dos. En la L4 sumaremos un tercero.



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
supports[supports["in_view"]].head(10)
```

**Lo que aprendemos aquí.** Quedan en vista 8 artículos, menos de los 10 que pide el estándar. Es un resultado honesto, no un error. Los grupos por densidad son estrictos: HDBSCAN deja 108 artículos como ruido, y solo uno de sus cinco grupos, el de diabetes con 10 artículos, toca el tema del equipo. Con los grupos de k-means habrían quedado 56 artículos en vista, porque k-means obliga a cada artículo a entrar en un grupo. Pero un apoyo solo cuenta cuando el equipo puede leer el grupo y decir de qué trata. No agregamos grupos para inflar la cuenta. Hay un caso que muestra qué cambiaría el resultado. El grupo 4, el más grande con 87 artículos, tiene *food* entre sus 8 palabras de más peso, pero no se lee: *food* no está en `TOPIC_WORDS`. Escribimos esas palabras en la Parte 2, antes de mirar los grupos, y no las cambiamos después para que un grupo entre. Si el equipo hubiera puesto *food* en su lista desde el principio, ese grupo daría apoyo y la cuenta cambiaría. Por eso la lista de palabras se anota en la tarjeta como algo que cambia la decisión. La L4 suma el texto como tercer resultado: con él quedan 52 de los 317 en vista, y un artículo puede entrar con un patrón y el texto aunque HDBSCAN lo deje como ruido.
 
**Comprobar:**



```python
assert supports["supports"].between(0, len(SUPPORT_COLUMNS)).all()
assert 1 <= supports["in_view"].sum() < N and not supports.loc[~in_group, "read_group"].any()
print("Apoyos: OK")
```

### Paso 2. Guardar los grupos
En este paso guardamos `outputs/grupos_l3.csv`, con una fila por artículo. Los artículos que HDBSCAN deja como ruido llevan `-1` en la columna `hdbscan`. No se borran: siguen en la tabla para que alguien los mire. La L4 lee este archivo para sumar el tercer apoyo.



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



```python
saved = pd.read_csv(groups_path)
assert list(saved.columns) == ["title", "kmeans", "mezcla", "prob_mezcla", "hdbscan", "has_pattern", "read_group", "supports", "in_view"]
assert len(saved) == N
print("grupos_l3.csv: OK")
```

### Paso 3. Qué cambiaría la decisión
En este paso escribimos en la tarjeta cómo entra un grupo en la decisión y qué la cambiaría. Otro umbral cambia el vocabulario y el tamaño mínimo de un grupo de HDBSCAN. Más direcciones de la SVD cambian las distancias. Otra lectura de las palabras de un grupo cambia qué artículos reciben el apoyo.



```python
question_card["group_use"] = {
    "how_it_enters": "Un artículo recibe un apoyo si está en un grupo de HDBSCAN que el equipo lee (sus palabras tocan el tema). El ruido no recibe apoyo.",
    "reading": "Los grupos son débiles: la silueta apenas supera al azar y cambia con la semilla. Un grupo solo no decide.",
    "k_chosen": int(K_CHOSEN),
    "team_groups": [int(g) for g in team_groups],
    "noise": "Los artículos que HDBSCAN deja como ruido no tienen apoyo. Se miran a mano, no se borran.",
    "what_changes_it": ["otro umbral de soporte", "más direcciones de la SVD", "otra lectura de las palabras de un grupo"],
}
QUESTION_PATH.write_text(json.dumps(question_card, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(question_card["group_use"], ensure_ascii=False, indent=1))
```

**Su turno.** En dos o tres frases: ¿qué grupo de HDBSCAN le parece más útil para el equipo, y qué artículo de la lista de ruido miraría primero? ¿Por qué?



```python
my_group = """
Escriba aquí el grupo, por qué le sirve al equipo y qué artículo del ruido miraría.
"""
print(my_group)
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
    ("Patrones de la L2 en los apoyos", lambda: len(topic_pairs) > 0),
    ("Hallazgo sobre la estructura escrito", lambda: "___" not in structure_finding),
]
passed = sum(_check_ok(n, f) for n, f in checks)
print(f"\nL3_CHECKS={passed}/{len(checks)}")
if passed == len(checks):
    print("L3_OK. Lleve sus grupos a la Lección 4. Allí sumaremos el texto como tercer resultado.")
```



<!-- end NOTEBOOK: -->
