<!-- NOTEBOOK: -->

## Instrucciones
 
**Propósito.** Cuaderno de grupo de la semana 2 (Lecciones 3 y 4). En los laboratorios el equipo del consejo formó grupos de artículos de nutrición y luego leyó el texto con ejemplos marcados. Aquí su grupo hace lo mismo con **su departamento** en Wikipedia. La decisión sigue igual: **qué artículos debe abrir primero una persona nueva**. Al final, cada artículo tiene hasta tres apoyos: un patrón de la semana 1, un grupo de la L3 y el texto de la L4.
 
**Requisito.** Complete primero los cuadernos individuales [L3](https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-data-mining/l3-groups.ipynb) y [L4](https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-data-mining/l4-text.ipynb). Tengan a mano `pregunta.json` y `outputs/patrones.csv` de su cuaderno de grupo de la semana 1. Cada celda `# SU CÓDIGO` dice qué celda del cuaderno individual seguir.
 
**Primero marcan, después corren los modelos.** El sábado, la meta de las 10:00 es la celda que escribe `marcas.csv` (Parte 3, Paso 7). Ese archivo trae los artículos de su conjunto marcado con la columna `marca` vacía. Lo marcan sin mirar las categorías y lo vuelven a subir. Las paradas 7 y 8 que vienen justo después usan el laboratorio de la L4, no sus marcas, así que funcionan antes de marcar.
 
**Cómo trabajar.** Cada paso empieza con **En este paso**. Los pasos con una celda `# SU CÓDIGO` terminan con una celda **Comprobar**. Algunos pasos vienen resueltos. Si un `assert` falla, corrija su celda antes de seguir. Los nombres del código van en inglés, como en los cuadernos individuales. Los comentarios y las explicaciones van en español.
 
**Entrega Moodle (martes 17 nov 2026, 23:59 Colombia):** ZIP `week-2-<group_id>.zip` con `week-2-group-<group_id>.ipynb` (este cuaderno ejecutado y renombrado), `pregunta.json`, `marcas.csv`, `outputs/grupos.csv`, `outputs/texto.csv` y `outputs/en_vista.csv`.
 
**Mapa del cuaderno**
 
| Parte | Fase CRISP-DM | Qué sale | Cuaderno a seguir |
|-------|---------------|----------|-------------------|
| 0 | Configuración | Grupo, parámetros, codificador, datos y funciones dadas | Dado |
| 1 | Comprensión del negocio | Qué significa un grupo para la persona nueva | L3, Parte 2 |
| 2 | Comprensión de los datos | Largo de las entradillas (dado) | L4, Parte 3 |
| 3 | Preparación de los datos | Conteos, SVD, etiqueta, lista de palabras, `marcas.csv` y TF-IDF | L3, Parte 4, y L4, Parte 4 |
| 4 | Modelado | Los seis métodos | L3, Parte 5, y L4, Parte 5 |
| 5 | Evaluación | Línea base, estabilidad, el hallazgo, aciertos y errores con sus marcas | L3, Parte 6, y L4, Parte 6 |
| 6 | Despliegue | Tres apoyos y `outputs/en_vista.csv` | L3 y L4, Parte 7 |
| Cierre | | Registro de contribución y reflexión | |

---
 
## Parte 0. Configuración
 
Esta parte viene resuelta. Ejecútela y lea lo que imprime.
 
### Paso 1. Su grupo
En este paso elige su grupo. Cambie solo `GROUP`. El diccionario dice qué archivo le corresponde.



```python
GROUP = "G1"   # cambie a G2, G3, G4 o G5

EXTRACTS = {
    "G1": ("Pobreza", "pobreza.csv"),
    "G2": ("Vivienda", "vivienda.csv"),
    "G3": ("Medio ambiente", "medio-ambiente.csv"),
    "G4": ("Agricultura", "agricultura.csv"),
    "G5": ("Salud mental", "salud-mental.csv"),
}
DEPARTMENT, FILENAME = EXTRACTS[GROUP]
print(f"Grupo {GROUP}: {DEPARTMENT} ({FILENAME})")
```

### Paso 2. Librerías y parámetros compartidos
En este paso instalamos lo que falte, importamos las librerías y copiamos los parámetros de las Lecciones 2, 3 y 4 **sin cambiarlos**. Todos los grupos y el script de control usan los mismos.



```python
import importlib.util
import subprocess
import sys

if importlib.util.find_spec("sentence_transformers") is None:
    print("Instalando sentence-transformers (una sola vez por sesión)...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "sentence-transformers"], check=True)

import json
from itertools import combinations
import math
import re
import time
from collections.abc import Sequence
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
from sklearn.cluster import HDBSCAN, KMeans
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, adjusted_rand_score, confusion_matrix, f1_score, pairwise_distances, precision_recall_fscore_support, silhouette_score
from sklearn.mixture import GaussianMixture
from sklearn.model_selection import StratifiedKFold, cross_val_predict, train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler, normalize

DATA_DIR = Path("data")
OUTPUTS_DIR = Path("outputs")
DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

# Desde L2, sin cambios
SUPPORT_SHARE = 0.03
SUPPORT_MIN = 5
SEED = 7

# L3, sin cambios
MAX_WORD_SHARE = 0.5
MIXTURE_COMPONENTS = 5
DENSITY_COMPONENTS = 10
K_CANDIDATES = range(3, 9)
MIN_SAMPLES = SUPPORT_MIN
N_SHUFFLES = 30
MIXTURE_K = range(1, 9)
UNSURE_PROB = 0.6
STABILITY_SEEDS = range(5)
TOP_WORDS = 8

# L4, sin cambios
FLAGGED_SHARE = 0.20
FLAGGED_MIN = 40
POSITIVE_SHARE = 0.10
POSITIVES_MIN = 30
C_REG = 10
N_RESAMPLES = 2000
TEXT_MODEL = "intfloat/multilingual-e5-small"
MAX_LENGTH = 512
PREFIX = "query: "
N_FOLDS = 5

# Decisión, L3 en adelante
MIN_SUPPORTS = 2


# support_floor: mismo código que scripts/data-mining-course/swap_randomization.py, salvo docstrings y comentarios en español.
def support_floor(n_texts: int) -> int:
    """Soporte mínimo que necesita una palabra o un par: max(SUPPORT_MIN, ceil(SUPPORT_SHARE * n))."""
    return max(SUPPORT_MIN, math.ceil(SUPPORT_SHARE * n_texts))


def n_flagged(n: int) -> int:
    """Tamaño del conjunto marcado: max(FLAGGED_MIN, ceil(FLAGGED_SHARE * n))."""
    return max(FLAGGED_MIN, math.ceil(FLAGGED_SHARE * n))


def min_positives(n: int) -> int:
    """Positivos que necesita una etiqueta de entrenamiento: max(POSITIVES_MIN, ceil(POSITIVE_SHARE * n))."""
    return max(POSITIVES_MIN, math.ceil(POSITIVE_SHARE * n))


print(f"Con 300 artículos: umbral {support_floor(300)}, {n_flagged(300)} marcados, al menos {min_positives(300)} positivos")
```

### Paso 3. El codificador de texto
En este paso cargamos `intfloat/multilingual-e5-small`, el mismo codificador de la L4. A diferencia de la L2, aquí el modelo no cambia con el idioma: sirve para inglés y para español. El modelo se descarga al cargarlo, en esta celda. En un Colab nuevo se descargan unos 470 MB, menos de un minuto.



```python
from sentence_transformers import SentenceTransformer

start = time.time()
encoder = SentenceTransformer(TEXT_MODEL, device="cpu")
encoder.max_seq_length = MAX_LENGTH
print(f"Codificador cargado en {time.time() - start:.1f} s")
```

### Paso 4. Descargar el extracto y las funciones de siempre
En este paso descargamos el archivo del grupo y traemos las funciones de la L3: `words` (un conjunto de palabras), `word_list` (la lista con repeticiones) y `p95` (el percentil 95 por rango de la semana 1). Las palabras vacías son las del español, más los restos de direcciones web. Si en la semana 1 quitaron palabras de relleno, cópienlas en `FILLER_WORDS`.



```python
from spacy.lang.es.stop_words import STOP_WORDS as STOP_WORDS_ES

BASE_URL = "https://cabrerac.github.io/assets/data/26-udenar-data-mining"
WORD_RE = re.compile(r"[^\W\d_]+")
URL_TOKENS = {"http", "https", "www", "org"}
FILLER_WORDS = []   # sus palabras de relleno de la semana 1, si las quitaron
STOP_WORDS = set(STOP_WORDS_ES) | URL_TOKENS | set(FILLER_WORDS)


def download_data(name: str, folder: Path = DATA_DIR) -> Path:
    """Descarga un archivo de datos del curso, una sola vez (la función de la L4).

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
    print(f"Descargado: {dest}")
    return dest


def words(text: str, stop_words: set[str]) -> set[str]:
    """Conjunto de palabras útiles de un texto (la función de la L2, sin cambios)."""
    text = (text or "").lower().replace("[cita requerida]", " ")
    return {w for w in WORD_RE.findall(text) if len(w) >= 3 and w not in stop_words}


def word_list(text: str, stop_words: set[str]) -> list[str]:
    """Como words, pero conserva las repeticiones (la función de la L3, sin cambios)."""
    text = (text or "").lower().replace("[cita requerida]", " ")
    return [w for w in WORD_RE.findall(text) if len(w) >= 3 and w not in stop_words]


# p95: mismo código que scripts/data-mining-course/swap_randomization.py, salvo docstrings y comentarios en español.
def p95(values: Sequence[float]) -> float:
    """Percentil 95 por rango, sin interpolar. Es la misma regla de las diapositivas y de los cuadernos."""
    values = sorted(values)
    return values[min(len(values) - 1, int(0.95 * len(values)))]


articles = pd.read_csv(download_data(FILENAME), keep_default_na=False)
print(articles.shape)
articles[["title", "lead"]].head(3)
```

### Paso 5. Dos funciones dadas de la L4
En este paso traemos dos funciones de la L4 sin cambios: `counts_of` cuenta aciertos y errores, y `f1_interval` da el intervalo bootstrap del 95 % del F1. Son celdas dadas: no hace falta reescribirlas.



```python
def counts_of(y, pred):
    """Aciertos y errores de un método en el conjunto marcado (la función de la L4).

    Qué hace: cuenta TP, FP, FN y TN, y calcula precisión, exhaustividad, F1 y exactitud.
    Entrada: y (las marcas) y pred (lo que dice el método).
    Salida: un diccionario con los cuatro conteos y las cuatro medidas.
    Por qué: la misma función para todos los métodos hace la comparación justa.
    """
    tn, fp, fn, tp = confusion_matrix(y, pred, labels=[0, 1]).ravel()
    p, r, f1, _ = precision_recall_fscore_support(y, pred, average="binary", zero_division=0)
    return {"TP": tp, "FP": fp, "FN": fn, "TN": tn, "precision": p, "recall": r, "F1": f1, "accuracy": accuracy_score(y, pred)}


def f1_interval(y, pred_a, pred_b=None, n_resamples=N_RESAMPLES, seed=SEED):
    """Intervalo bootstrap del 95 % del F1 de a, o de F1(a) - F1(b) sobre las mismas filas (la función de la L4).

    Qué hace: sortea n_resamples veces las filas marcadas, con reemplazo, y calcula el F1
    (o la diferencia de F1) en cada sorteo. Devuelve los percentiles 2,5 y 97,5.
    Entrada: y (las marcas), pred_a (las predicciones de un método), pred_b (opcional, otro método).
    Salida: un arreglo [bajo, alto].
    Por qué: con pocas filas marcadas un solo F1 engaña. El intervalo muestra cuánto puede moverse.
    """
    y, a = np.asarray(y), np.asarray(pred_a)
    b = None if pred_b is None else np.asarray(pred_b)
    rng = np.random.default_rng(seed)
    values = []
    for _ in range(n_resamples):
        rows = rng.integers(0, len(y), len(y))
        v = f1_score(y[rows], a[rows], zero_division=0)
        if b is not None:
            v -= f1_score(y[rows], b[rows], zero_division=0)
        values.append(v)
    return np.percentile(values, [2.5, 97.5])
```



```python
# Comprobar
assert GROUP in EXTRACTS and {"title", "lead", "categories"} <= set(articles.columns)
assert words("La pobreza [cita requerida] en https://www.cepal.org", STOP_WORDS) == {"pobreza", "cepal"}
print(f"Grupo {GROUP}, codificador y datos de {DEPARTMENT}: OK")
```

---
 
## Parte 1. Comprensión del negocio
 
### Paso 1. La tarjeta de la semana 1
En este paso leemos el `pregunta.json` de su grupo. Súbalo a la carpeta de trabajo antes de ejecutar la celda. Trae su pregunta, su estándar y el uso de un patrón (`pattern_use`).



```python
QUESTION_PATH = Path("pregunta.json")
question_card = json.loads(QUESTION_PATH.read_text(encoding="utf-8"))
print(question_card["question"])
print("Uso de un patrón:", question_card.get("pattern_use", {}).get("how_it_enters", "(falta)"))
```



```python
# Comprobar
assert {"question", "standard", "pattern_use"} <= set(question_card)
print("Tarjeta de la semana 1: OK")
```

### Paso 2. Qué significa un grupo para la persona nueva
En este paso escriban, en dos o tres frases, qué le serviría a una persona nueva saber que un artículo está en un grupo. Por ejemplo: un grupo de artículos sobre un mismo tema le dice qué leer junto. Escriban también qué grupo **no** le serviría.



```python
group_meaning = """
Escriba aquí qué significa un grupo para la persona nueva, y qué grupo no le serviría.
"""
print(group_meaning)
```



```python
# Comprobar
assert "Escriba aquí" not in group_meaning
print("Significado de un grupo: OK")
```

---
 
## Parte 2. Comprensión de los datos
 
### Paso 1. Las entradillas útiles y su largo
En este paso dejamos fuera las entradillas con menos de 5 palabras útiles, como en la semana 1, y miramos su largo. Esta celda viene resuelta.



```python
useful = [len(words(t, STOP_WORDS)) >= 5 for t in articles["lead"]]
articles = articles[useful].reset_index(drop=True)
texts = articles["lead"].tolist()
N = len(texts)
FLOOR = support_floor(N)
n_words = pd.Series([len(t.split()) for t in texts])
print(f"Entradillas usadas: {N} de {len(useful)}. Umbral: {FLOOR}")
print(f"Palabras por entradilla: mediana {n_words.median():.0f}, máximo {n_words.max():,}")
```



```python
# Comprobar
assert N >= 290 and FLOOR == support_floor(N)
print("Datos: OK")
```

---
 
## Parte 3. Preparación de los datos
 
### Lo que cambia con el idioma
El método es el de los laboratorios. La preparación cambia en estos puntos.
 
| Qué cambia | Laboratorio (artículos, inglés) | Grupo (Wikipedia, español) |
| --- | --- | --- |
| Columna de texto | `abstract` | `lead` |
| Palabras vacías y relleno | como en L2 | como en la semana 1 del grupo |
| Lista de palabras clave | en inglés, singular y plural | en español, con y sin tilde (hambruna, hambrunas) |
| Etiqueta de entrenamiento | temas de OpenAlex | categorías de los editores, dadas y no encontradas |
| Conjunto marcado | marcado por el profesor | marcado por el grupo antes de correr los modelos |
| Codificador | `multilingual-e5-small` | el mismo modelo. Aquí no cambia, a diferencia de L2 |
| Longitud | resúmenes largos, algunos se cortan a 512 tokens | entradas más cortas, pero entre 6 y 41 por archivo se cortan a 512 tokens (2% a 12%) |
 
### Paso 1. Conteo de palabras y escala (L3)
En este paso cuenten las palabras de cada entradilla, como en la **L3, Parte 4, Pasos 1 y 2**. Hagan `token_lists = [word_list(t, STOP_WORDS) for t in texts]` y cuenten con `CountVectorizer(analyzer=lambda tokens: tokens, min_df=FLOOR, max_df=MAX_WORD_SHARE)`. Guarden `token_lists`, `vectorizer`, `counts`, `vocabulary` y `X` (cada fila escalada a largo 1 con `normalize`). Una entradilla sin ninguna palabra del vocabulario queda como una fila de ceros: cuenten cuántas hay.



```python
# SU CÓDIGO
```



```python
# Comprobar
assert counts.shape[0] == N and len(vocabulary) == counts.shape[1]
assert np.allclose(np.sqrt(X.multiply(X).sum(axis=1)).A1[counts.getnnz(axis=1) > 0], 1)
print(f"Conteos: OK ({counts.shape[0]} x {counts.shape[1]})")
```

### Paso 2. La SVD y las entradas de la mezcla y de HDBSCAN (L3)
En este paso sigan la **L3, Parte 4, Pasos 3 y 4**. Guarden `svd` (con `n_components=DENSITY_COMPONENTS` y `random_state=SEED`), `Z`, `Z_mixture` (las 5 primeras componentes estandarizadas) y `distances` (la distancia coseno sobre las 10 componentes). Impriman cuánto explican 5 y 10 componentes.



```python
# SU CÓDIGO
```



```python
# Comprobar
assert Z.shape == (N, DENSITY_COMPONENTS) and Z_mixture.shape == (N, MIXTURE_COMPONENTS)
assert distances.shape == (N, N)
print("SVD: OK")
```

### Paso 3. La etiqueta de entrenamiento (L4)
En este paso elegimos la **etiqueta de entrenamiento**: un 1 para cada artículo que tiene alguna de las categorías de `TARGET_CATEGORIES`. Es una etiqueta **dada, no encontrada**: la escribieron los editores de Wikipedia. Pueden elegir otro conjunto de sus categorías si tiene al menos `min_positives(N)` positivos. Si lo cambian, digan por qué en un comentario.



```python
TARGETS = {
    "G1": ["Hambrunas", "Hambre", "Bancos de alimentos"],
    "G2": ["Hipotecas", "Arrendamiento", "Huelgas de alquileres", "Vivienda asequible", "Vivienda pública"],
    "G3": ["Conservacionismo"],
    "G4": ["Agrarismo", "Organizaciones agrícolas"],
    "G5": ["Trastornos mentales", "Psiquiatría"],
}
TARGET_CATEGORIES = set(TARGETS[GROUP])
categories = [{c.strip() for c in str(t).split("|") if c.strip()} for t in articles["categories"]]
y = np.array([int(bool(c & TARGET_CATEGORIES)) for c in categories])
print(f"Etiqueta: {sorted(TARGET_CATEGORIES)}")
print(f"Positivos: {y.sum()} de {N} ({y.mean():.0%}). Mínimo: {min_positives(N)}")
```



```python
# Comprobar
assert y.sum() >= min_positives(N)
print("Etiqueta: OK")
```

### Paso 4. La lista de palabras clave (L4)
En este paso escriban su lista **desde la pregunta**, antes de correr ningún método, como en la **L4, Parte 4, Paso 1**. En español, en minúsculas, con y sin tilde y con singular y plural (*hambruna*, *hambrunas*). No la armen con los nombres de las categorías de la etiqueta: una lista hecha mirando las respuestas parece buena y no lo es. Expliquen en un comentario por qué está cada palabra.
 
Escriban aquí también `TOPIC_WORDS`, las palabras de su tema, como en la **L3, Parte 2, Paso 1**. En la Parte 5 decidirán qué grupos de HDBSCAN se leen. Por eso se escriben ahora, antes de ver ningún grupo: si las escriben mirando los grupos, eligen las palabras que hacen entrar a un grupo. Pueden ser las mismas de `KEYWORDS`.



```python
# SU CÓDIGO
KEYWORDS = set()
TOPIC_WORDS = set()
```



```python
# Comprobar
assert len(KEYWORDS) >= 5 and all(w == w.lower() for w in KEYWORDS)
assert len(TOPIC_WORDS) >= 1 and all(w == w.lower() for w in TOPIC_WORDS)
print(f"Listas: OK ({len(KEYWORDS)} palabras clave, {len(TOPIC_WORDS)} palabras del tema)")
```

### Paso 5. El conjunto marcado
En este paso separamos `n_flagged(N)` artículos que ningún método ve al aprender, con `stratify=y`, como en la L4. Esta celda viene resuelta.



```python
rows = np.arange(N)
train_rows, marked_rows = train_test_split(rows, test_size=n_flagged(N), stratify=y, random_state=SEED)
train_texts = [texts[i] for i in train_rows]
test_texts = [texts[i] for i in marked_rows]
y_train = y[train_rows]
print(f"Entrenamiento: {len(train_rows)} filas. Marcados: {len(marked_rows)} filas")
```

### Paso 6. Cómo marcar
En este paso leen las reglas antes de marcar. La columna `marca` se escribe así:
 
| Escriba | Cuando |
|---------|--------|
| `1` | La persona nueva **debe abrir** esta entrada para su pregunta |
| `0` | **No** hace falta que la abra |
 
Solo `1` o `0`: sin "sí", sin "no", sin celdas vacías. Marquen leyendo el `lead`, **sin mirar las categorías** ni ningún resultado. Repártanse las filas: unas 16 o 17 por persona (en G1, unas 20). Si dudan con una entrada, decidan entre todos y anoten por qué en el registro de contribución.

### Paso 7. Escribir `marcas.csv` (la meta de las 10:00)
En este paso el cuaderno escribe `marcas.csv` con `title`, `lead` y `marca` vacía. Descárguenlo, márquenlo (en una hoja de cálculo, guardando como CSV) y vuelvan a subirlo con el mismo nombre. Si ya hay un `marcas.csv` con marcas, la celda no lo sobrescribe.
 
**Hojas de cálculo.** Lo más simple es Google Sheets: Archivo, Descargar, CSV. Excel en español suele guardar el CSV con punto y coma y con otra codificación de las tildes. La función `read_marks` de esta celda lee los dos casos.



```python
MARKS_PATH = Path("marcas.csv")


def read_marks(path: Path) -> pd.DataFrame:
    """Lee marcas.csv aunque venga de una hoja de cálculo en español.

    Qué hace: adivina el separador (coma o punto y coma) y prueba UTF-8 y después cp1252.
    Entrada: path, la ruta de marcas.csv.
    Salida: la tabla con title, lead y marca.
    Por qué: Excel en español no guarda el CSV igual que Google Sheets o pandas.
    """
    try:
        return pd.read_csv(path, sep=None, engine="python", encoding="utf-8-sig")
    except UnicodeDecodeError:
        return pd.read_csv(path, sep=None, engine="python", encoding="cp1252")


to_mark = pd.DataFrame({"title": articles.loc[marked_rows, "title"].to_numpy(), "lead": test_texts, "marca": ""})
if MARKS_PATH.is_file() and read_marks(MARKS_PATH)["marca"].notna().any():
    print("marcas.csv ya tiene marcas. No lo sobrescribimos.")
else:
    to_mark.to_csv(MARKS_PATH, index=False)
    print(f"Escrito: {MARKS_PATH} ({len(to_mark)} filas). Márquenlo con 1 o 0 y súbanlo de nuevo.")
```

### Paradas 7 y 8: el laboratorio de la L4
Estas dos celdas usan los artículos de nutrición de la L4 y el extracto sin marcas. **No dependen de `marcas.csv`**: pueden correrlas antes de marcar.
 
**Parada 7. El corte del codificador.** El codificador lee hasta 512 tokens. Contamos cuántas entradillas de su extracto pasan de 512 y se cortan, y lo mismo en el laboratorio.



```python
from spacy.lang.en.stop_words import STOP_WORDS as STOP_WORDS_EN

lab = pd.read_csv(download_data("nutricion-papers.csv"), keep_default_na=False)
LAB_STOP_WORDS = set(STOP_WORDS_EN) | URL_TOKENS | {
    "background", "methods", "findings", "interpretation", "funding",
    "conclusions", "results", "objective", "objectives", "aims",
    "bill", "melinda", "gates", "foundation",
}
lab = lab[[len(words(t, LAB_STOP_WORDS)) >= 5 for t in lab["abstract"]]].reset_index(drop=True)
lab_texts = lab["abstract"].tolist()

n_tokens = [len(encoder.tokenizer(PREFIX + t)["input_ids"]) for t in texts]
n_cut = sum(n > MAX_LENGTH for n in n_tokens)
lab_n_cut = sum(len(encoder.tokenizer(PREFIX + t)["input_ids"]) > MAX_LENGTH for t in lab_texts)
print(f"Su extracto: {n_cut} de {N} entradillas se cortan a {MAX_LENGTH} tokens ({n_cut / N:.0%})")
print(f"Laboratorio: {lab_n_cut} de {len(lab_texts)} resúmenes se cortan")
```

**Parada 8. El F1 con su intervalo.** En el laboratorio, con la etiqueta de OpenAlex en las filas marcadas, el F1 de TF-IDF lleva su intervalo bootstrap del 95 %. Con pocos positivos el intervalo es ancho y puede llegar a 1,00.



```python
LAB_TOPICS = ["obesity", "diet", "nutrition", "nutritional", "diabetes", "cardiovascular", "lipoproteins", "blood pressure", "hypertension"]
lab_y = np.array([int(any(t in topics.lower() for t in LAB_TOPICS)) for topics in lab["topics"]])
lab_train, lab_marked = train_test_split(np.arange(len(lab_y)), test_size=n_flagged(len(lab_y)), stratify=lab_y, random_state=SEED)
lab_model = make_pipeline(
    TfidfVectorizer(analyzer=lambda t: word_list(t, LAB_STOP_WORDS), sublinear_tf=True),
    LogisticRegression(class_weight="balanced", C=C_REG, max_iter=1000))
lab_model.fit([lab_texts[i] for i in lab_train], lab_y[lab_train])
lab_pred = lab_model.predict([lab_texts[i] for i in lab_marked])
lab_f1 = f1_score(lab_y[lab_marked], lab_pred)
lab_low, lab_high = f1_interval(lab_y[lab_marked], lab_pred)
print(f"Laboratorio, TF-IDF: F1 {lab_f1:.2f} [{lab_low:.2f}, {lab_high:.2f}] con {lab_y[lab_marked].sum()} positivos de {len(lab_marked)}")
```

**Comprobar** (paradas 7 y 8 sin `marcas.csv`):



```python
assert lab_n_cut == 93 and 0 <= n_cut < N
assert lab_low <= lab_f1 <= lab_high
print("Paradas 7 y 8: OK. Usan el laboratorio y el extracto sin marcas, no marcas.csv")
```

### Paso 8. TF-IDF (L4)
En este paso preparen TF-IDF como en la **L4, Parte 4, Paso 3**: `train_tokens` y `test_tokens` con `word_list`, y `TfidfVectorizer(analyzer=lambda tokens: tokens, sublinear_tf=True)` ajustado **solo** con `train_tokens`. Guarden `tfidf`, `X_train`, `X_test` y `feature_names = tfidf.get_feature_names_out()`.



```python
# SU CÓDIGO
```



```python
# Comprobar
assert X_train.shape[0] == len(train_rows) and X_test.shape == (len(marked_rows), X_train.shape[1])
print("TF-IDF: OK")
```

---
 
## Parte 4. Modelado
 
Copien de la L3 y la L4 y adapten:
 
| Método | Qué copiar | Dónde está |
|--------|------------|------------|
| M1. k-means | Silueta para cada k, `K_CHOSEN`, `kmeans`, `kmeans_labels` y `kmeans_words` con `top_words` | L3, Parte 5, M1 |
| M2. Mezcla gaussiana | `bic`, `K_MIXTURE`, `mixture`, `membership`, `mixture_labels`, `top_prob`, `unsure` | L3, Parte 5, M2 |
| M3. HDBSCAN | `hdbscan_labels`, `n_groups`, `in_group`, `noise`, `hdbscan_words` y la lista de ruido | L3, Parte 5, M3 |
| M4. Lista de palabras | `keyword_match`, `pred_keywords`, `cv_keywords` | L4, Parte 5, M1 |
| M5. TF-IDF y regresión logística | `lr`, `pred_lr` y `weights` con `feature_names` | L4, Parte 5, M2 |
| M6. Codificador y regresión logística | `lr_enc`, `pred_encoder` | L4, Parte 5, M3 |
 
### M1. k-means
En este paso corran k-means para cada k de `K_CANDIDATES` sobre `X`, con `n_init=10` y `random_state=SEED`. Guarden `silhouettes`, `K_CHOSEN` (el k de silueta más alta), `kmeans`, `kmeans_labels` y `kmeans_words` con la función `top_words` de la L3.



```python
# SU CÓDIGO
```



```python
# Comprobar
assert set(silhouettes) == set(K_CANDIDATES) and K_CHOSEN in K_CANDIDATES
assert len(kmeans_words) == K_CHOSEN
print(f"k-means: OK (k = {K_CHOSEN}, silueta {silhouettes[K_CHOSEN]:.3f})")
```

### M2. Mezcla gaussiana
En este paso ajusten la mezcla sobre `Z_mixture` para cada K de `MIXTURE_K`, elijan `K_MIXTURE` por el BIC más bajo y calculen la pertenencia suave (`membership`). El grupo de cada entrada es `mixture_labels = mixture.predict(Z_mixture)`, como en la diapositiva. Usen el `n_init` por defecto (1), como en la L3. k-means sí usa `n_init=10` en la estabilidad y la línea base.



```python
# SU CÓDIGO
```



```python
# Comprobar
assert K_MIXTURE in MIXTURE_K and membership.shape == (N, K_MIXTURE)
assert np.allclose(membership.sum(axis=1), 1)
print(f"Mezcla: OK (K = {K_MIXTURE}, {unsure.sum()} dudosos)")
```

### M3. HDBSCAN
En este paso corran HDBSCAN sobre `distances` con `min_cluster_size=FLOOR`, `min_samples=MIN_SAMPLES`, `metric="precomputed"` y `copy=True`. Muestren cuántos grupos salen y cuánto ruido queda. Guarden `hdbscan_words`, las 8 palabras de más peso de cada grupo, con `top_words`: con ellas elegirán qué grupos leer.



```python
# SU CÓDIGO
```



```python
# Comprobar
assert len(hdbscan_labels) == N and n_groups == hdbscan_labels.max() + 1
assert 0 <= noise <= 1 and len(hdbscan_words) == n_groups
print(f"HDBSCAN: OK ({n_groups} grupos, {noise:.0%} de ruido)")
```

### M4. La lista de palabras
En este paso apliquen su lista, como en la **L4, Parte 5, M1**, a las filas marcadas (`pred_keywords`) y a las de entrenamiento (`cv_keywords`).



```python
# SU CÓDIGO
```



```python
# Comprobar
assert len(pred_keywords) == len(marked_rows) and len(cv_keywords) == len(train_rows)
print("Lista de palabras: OK")
```

### M5. TF-IDF y regresión logística
En este paso entrenen la regresión logística con `class_weight="balanced"`, `C=C_REG` y `max_iter=1000`, y guarden `pred_lr`. Muestren las 15 palabras de más peso a favor y en contra con `weights = pd.Series(lr.coef_[0], index=feature_names)`. ¿Son del tema, o son palabras de las categorías de la etiqueta?



```python
# SU CÓDIGO
```



```python
# Comprobar
assert len(pred_lr) == len(marked_rows) and set(np.unique(pred_lr)) <= {0, 1}
print("TF-IDF: OK")
```

### M6. Los vectores del codificador
En este paso calculamos un vector por entradilla con el prefijo `"query: "`. Esta celda viene resuelta y guarda `outputs/vectores.npy` para no volver a calcularlos. En Colab gratuito, unos 15 a 30 s para sus entradillas. La descarga del modelo ya ocurrió en la Parte 0.



```python
VECTORS_PATH = OUTPUTS_DIR / "vectores.npy"
start = time.time()
if VECTORS_PATH.is_file() and np.load(VECTORS_PATH).shape[0] == N:
    vectors = np.load(VECTORS_PATH)
else:
    vectors = encoder.encode([PREFIX + t for t in texts], normalize_embeddings=True, batch_size=16)
    np.save(VECTORS_PATH, vectors)
V_train, V_test = vectors[train_rows], vectors[marked_rows]
print(f"Vectores: {vectors.shape} en {time.time() - start:.1f} s")
```

En este paso entrenen la misma regresión logística sobre `V_train` y guarden `lr_enc` y `pred_encoder`, como en la **L4, Parte 5, M3**.



```python
# SU CÓDIGO
```



```python
# Comprobar
assert len(pred_encoder) == len(marked_rows)
print("Codificador: OK")
```

---
 
## Parte 5. Evaluación
 
### Paso 1. Silueta contra la línea base al azar (L3)
En este paso comparen la silueta de `K_CHOSEN` con `N_SHUFFLES` tablas al azar, como en la **L3, Parte 6, Paso 1**: cada palabra queda en el mismo número de artículos. Guarden `shuffled_silhouettes` y `BASELINE_P95 = p95(shuffled_silhouettes)`. Calcule unos 10 a 30 s.



```python
# SU CÓDIGO
```



```python
# Comprobar
assert len(shuffled_silhouettes) == N_SHUFFLES and BASELINE_P95 == p95(shuffled_silhouettes)
print(f"Línea base: OK (silueta {silhouettes[K_CHOSEN]:.3f}, percentil 95 del azar {BASELINE_P95:.3f})")
```

### Paso 2. Estabilidad entre semillas (L3)
En este paso corran k-means con `K_CHOSEN` y cada semilla de `STABILITY_SEEDS`, y comparen los 10 pares con el índice de Rand ajustado. Guarden `seed_ari`.



```python
# SU CÓDIGO
```



```python
# Comprobar
assert len(seed_ari) == 10 and all(-1 <= a <= 1 for a in seed_ari)
print(f"Estabilidad: OK (ARI medio {np.mean(seed_ari):.2f})")
```

### Paso 3. Acuerdo entre los tres métodos de grupos
En este paso comparamos los grupos de los tres métodos. Esta celda viene resuelta.



```python
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

### Paso 4. Qué grupos lee la persona nueva
En este paso eligen qué grupos de **HDBSCAN** lee la persona nueva, como en la **L3, Parte 6, Paso 4**. Los grupos de la decisión son los de HDBSCAN. k-means solo sirvió para la estabilidad y el acuerdo. Usen las `TOPIC_WORDS` que escribieron en la Parte 3, sin cambiarlas, y lean las palabras de cada grupo en `hdbscan_words`. Guarden `team_groups` (los grupos que se leen) y `read_group = np.isin(hdbscan_labels, team_groups)`. Las entradas de ruido no reciben apoyo: listen sus títulos para mirarlos a mano. Si ningún grupo toca su tema, también es un resultado: sigan con dos apoyos posibles.



```python
# SU CÓDIGO
```



```python
# Comprobar
assert len(read_group) == N and read_group.sum() < N
assert not read_group[hdbscan_labels == -1].any()
print("Grupos del tema: OK. Ningún grupo toca su tema. Es un resultado: sigan con dos apoyos posibles." if read_group.sum() == 0 else f"Grupos del tema: OK ({team_groups}, {read_group.sum()} artículos)")
```

### Paso 5. Lo que encontramos sobre la estructura
En este paso escriban el hallazgo con sus números, como en la **L3, Parte 6, Paso 6**. Una estructura débil también es un resultado: dice que un grupo solo no basta para decidir.



```python
print(f"Silueta con k = {K_CHOSEN}: {silhouettes[K_CHOSEN]:.3f}. Percentil 95 de la línea base: {BASELINE_P95:.3f}")
print(f"Estabilidad entre semillas (ARI medio): {np.mean(seed_ari):.2f}")
print(f"Ruido de HDBSCAN: {noise:.0%} de las entradillas")
```



```python
structure_finding = """
- Silueta con k = ___: ___. Percentil 95 de la línea base: ___.
- Estabilidad entre semillas (índice de Rand ajustado medio): ___.
- Ruido de HDBSCAN: ___ % de las entradillas.
- Qué significa para nuestra lista: ___.
"""
print(structure_finding)
```



```python
# Comprobar
assert "___" not in structure_finding
print("Hallazgo: OK")
```

### Paso 6. Leer sus marcas
En este paso leemos `marcas.csv` ya marcado. La celda revisa que tenga `n_flagged(N)` filas, los mismos títulos que el conjunto marcado y ninguna marca vacía. Solo cuenta `1` o `0`.



```python
marks = read_marks(MARKS_PATH)
marks["marca"] = pd.to_numeric(marks["marca"], errors="coerce")
marca_values = marks.set_index("title")["marca"].reindex(articles.loc[marked_rows, "title"]).to_numpy()
y_test = np.nan_to_num(marca_values, nan=-1).astype(int)   # -1 marca una fila vacía o inválida
print(f"Marcas: {len(marks)} filas, {(y_test == 1).sum()} con 1, {(y_test == -1).sum()} vacías o inválidas")
```



```python
# Comprobar
assert len(marks) == n_flagged(N) and set(marks["title"]) == set(articles.loc[marked_rows, "title"])
assert marks["marca"].notna().all() and set(marks["marca"]) <= {0, 1}
print("marcas.csv: OK")
```

### Paso 7. Sus marcas contra la etiqueta de los editores
En este paso comparamos sus marcas con la etiqueta de los editores en las mismas filas. La diferencia dice cuánto se aleja una etiqueta dada de lo que su grupo lee como "para abrir". Esta celda viene resuelta.



```python
editors = y[marked_rows]
both = pd.crosstab(pd.Series(y_test, name="marca del grupo"), pd.Series(editors, name="etiqueta de los editores"))
print(f"Coinciden en {(y_test == editors).sum()} de {len(editors)} filas")
both
```

### Paso 8. Aciertos y errores con sus marcas
En este paso cuenten TP, FP, FN y TN de la clase mayor y de los tres métodos contra `y_test`, con `counts_of`, como en la **L4, Parte 6, Paso 1**. Guarden `predictions` (un diccionario que va de cada nombre de método a su predicción) y `results`.



```python
# SU CÓDIGO
```



```python
# Comprobar
assert set(results.index) == {"clase mayor", "palabras clave", "TF-IDF", "codificador"}
assert (results[["TP", "FP", "FN", "TN"]].sum(axis=1) == len(marked_rows)).all()
print("Aciertos y errores: OK")
```

### Paso 9. El F1 con su intervalo y los cinco pliegues
En este paso pongan a cada F1 su intervalo con `f1_interval`, como en la **L4, Parte 6, Paso 3**. Luego calculen los cinco pliegues en las filas de entrenamiento, como en la **L4, Parte 6, Paso 4**. Guarden `intervals` (de cada nombre de método a su [bajo, alto]), `folds`, `model_tfidf`, `model_encoder`, `cv_tfidf` y `cv_encoder`.



```python
# SU CÓDIGO
```



```python
# Comprobar
assert all(lo <= results.loc[m, "F1"] <= hi for m, (lo, hi) in intervals.items())
assert len(cv_tfidf) == len(train_rows) and len(cv_encoder) == len(train_rows)
print("Intervalos y pliegues: OK")
```

### Paso 10. ¿Gana el codificador?
En este paso calculamos el intervalo de la diferencia de F1 entre el codificador y TF-IDF sobre las mismas filas. Esta celda viene resuelta.



```python
low, high = f1_interval(y_test, pred_encoder, pred_lr)
print(f"F1 del codificador menos F1 de TF-IDF: [{low:.2f}, {high:.2f}]")
print("El intervalo incluye el 0: el conjunto marcado no alcanza para decir que uno gana." if low <= 0 <= high else "El intervalo no incluye el 0.")
```

**Su turno.** Lean tres entradas mal clasificadas por el método que van a usar y escriban si el error es del método o de la marca.



```python
error_reading = """
Escriba aquí tres títulos, si cada error es del método o de la marca, y por qué.
"""
print(error_reading)
```

---
 
## Parte 6. Despliegue
 
### Paso 1. Tres apoyos por artículo
En este paso armen la tabla de apoyos con tres columnas, como en la **L4, Parte 7, Paso 1**:
 
- `has_pattern`: la entradilla contiene un par de `outputs/patrones.csv` de la semana 1 con `kept_lift2` y una palabra de `TOPIC_WORDS`.
- `read_group`: está en un grupo de HDBSCAN que la persona nueva lee. El ruido no recibe este apoyo.
- `text_says_read`: TF-IDF dice abrir, con un modelo que no la vio (los marcados con `pred_lr`, los de entrenamiento con `cv_tfidf`).
 
Guarden `supports` con `title`, las tres columnas, `supports` y `in_view` (al menos `MIN_SUPPORTS`).
 
Si quedan pocos artículos en vista, no agreguen grupos para inflar la cuenta. En el laboratorio de la L3, HDBSCAN dejó 8 artículos en vista donde k-means habría dejado 56. Los grupos por densidad son estrictos, y un apoyo solo cuenta cuando pueden leer el grupo.



```python
SUPPORT_COLUMNS = ["has_pattern", "read_group", "text_says_read"]
patterns = pd.read_csv(OUTPUTS_DIR / "patrones.csv")
# SU CÓDIGO
```



```python
# Comprobar
assert list(supports.columns[:4]) == ["title"] + SUPPORT_COLUMNS
assert (supports["supports"] == supports[SUPPORT_COLUMNS].astype(int).sum(axis=1)).all()
print(f"Apoyos: OK ({supports['in_view'].sum()} en vista, {(supports['supports'] == 3).sum()} con los tres)")
```

### Paso 2. El largo de la lista
En este paso comparamos la lista con el estándar de su tarjeta, como en la **L4, Parte 7, Paso 2**. El máximo es `standard["max_articles"]` de su `pregunta.json`. Si hay más entradas en vista, las ordenamos por número de apoyos, después por `prob_texto` (la probabilidad de TF-IDF con regresión logística, de un modelo que no vio la entrada) y después por título, y nos quedamos con las primeras. Las demás no se borran: quedan en `en_vista.csv` con `recortado` en verdadero. Si quedan menos de 5 en vista, no rellenen la lista: es un resultado débil. Esta celda viene resuelta.



```python
MAX_ARTICLES = question_card["standard"]["max_articles"]   # el máximo de su tarjeta de la semana 1

prob_texto = np.zeros(N)
prob_texto[marked_rows] = lr.predict_proba(X_test)[:, 1]   # marcados: el modelo entrenado sin ellos
prob_texto[train_rows] = cross_val_predict(model_tfidf, train_tokens, y_train, cv=folds, method="predict_proba")[:, 1]   # entrenamiento: los mismos cinco pliegues de cv_tfidf
supports.insert(4, "prob_texto", prob_texto)

order = supports[supports["in_view"]].sort_values(["supports", "prob_texto", "title"], ascending=[False, False, True], kind="mergesort")
kept = order.index[:MAX_ARTICLES]
supports["recortado"] = supports["in_view"] & ~supports.index.isin(kept)
print(f"En vista: {supports['in_view'].sum()}. Máximo de la tarjeta: {MAX_ARTICLES}. Quedan {len(kept)}, recortados: {supports['recortado'].sum()}")
if len(kept) < 5:
    print("Quedan menos de 5 entradas en vista. Es un resultado débil: no rellenamos la lista.")
supports.loc[kept, ["title", "supports", "prob_texto"]].head(10).round(3)
```



```python
# Comprobar
assert (supports["in_view"] & ~supports["recortado"]).sum() == min(supports["in_view"].sum(), MAX_ARTICLES)
assert not (supports["recortado"] & ~supports["in_view"]).any()
assert ((supports["prob_texto"] > 0.5) == supports["text_says_read"]).all()
print("Lista recortada: OK")
```

### Paso 3. Guardar los resultados
En este paso guardamos los tres archivos de la entrega. La celda viene resuelta.



```python
marca = pd.Series(pd.NA, index=range(N), dtype="Int64")
marca[marked_rows] = y_test
encoder_says_read = np.zeros(N, dtype=int)
encoder_says_read[marked_rows] = pred_encoder
encoder_says_read[train_rows] = cv_encoder

pd.DataFrame({"title": articles["title"], "kmeans": kmeans_labels, "mezcla": mixture_labels,
              "prob_mezcla": top_prob.round(3), "hdbscan": hdbscan_labels}).to_csv(OUTPUTS_DIR / "grupos.csv", index=False)
pd.DataFrame({"title": articles["title"], "keyword": [keyword_match(t) for t in texts], "tfidf_lr": supports["text_says_read"].astype(int),
              "codificador": encoder_says_read, "marca": marca}).to_csv(OUTPUTS_DIR / "texto.csv", index=False)
supports.to_csv(OUTPUTS_DIR / "en_vista.csv", index=False)
print("Guardados: outputs/grupos.csv, outputs/texto.csv y outputs/en_vista.csv")
```

### Paso 4. Qué cambiaría la decisión
En este paso añadan a la tarjeta `group_use` y `text_use`, como en la L3 y la L4: cómo entra cada resultado (`how_it_enters`), qué dice la evaluación (`reading`) y qué cambiaría la lista (`what_changes_it`), incluido el máximo de la lista y el orden del recorte. Guarden de nuevo `pregunta.json`.



```python
# SU CÓDIGO
```



```python
# Comprobar
saved = json.loads(QUESTION_PATH.read_text(encoding="utf-8"))
assert {"how_it_enters", "reading", "what_changes_it"} <= set(saved["group_use"]) & set(saved["text_use"])
print("Tarjeta: OK")
```

### Paso 5. Comprobación final
En este paso revisamos que el cuaderno dejó todo lo que pide la entrega.



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
    ("pregunta.json con group_use y text_use", lambda: {"group_use", "text_use"} <= set(json.loads(QUESTION_PATH.read_text(encoding="utf-8")))),
    ("marcas.csv marcado", lambda: read_marks(MARKS_PATH)["marca"].notna().all()),
    ("outputs/grupos.csv, texto.csv y en_vista.csv", lambda: all((OUTPUTS_DIR / f).is_file() for f in ["grupos.csv", "texto.csv", "en_vista.csv"])),
    ("Hallazgo sobre la estructura", lambda: "___" not in structure_finding),
    ("Errores leídos a mano", lambda: "Escriba aquí" not in error_reading),
]
passed = sum(_check_ok(n, f) for n, f in checks)
print(f"\nW2_CHECKS={passed}/{len(checks)}")
if passed == len(checks):
    print("W2_OK. Armen el ZIP de la entrega.")
```

---
 
## Registro de contribución
 
Cada integrante añade **una línea** con una tarea concreta. Indiquen quién repartió las marcas y quién consolidó el ZIP.



```python
contribution_log = """
- Nombre Apellido: preparación y grupos (L3)
- Nombre Apellido: lista de palabras y marcas
- Nombre Apellido: métodos de texto y evaluación (L4)
- Nombre Apellido: apoyos, tarjeta y revisión final
Reparte las marcas: Nombre Apellido
Consolida el ZIP: Nombre Apellido
"""
print(contribution_log)
```

## Para la reflexión individual
 
La reflexión de la semana 2 va con la plantilla Word de la semana. Una pregunta para empezar: **¿en qué filas sus marcas no coincidieron con la etiqueta de los editores, y quién tenía razón?**
 
| Archivo del ZIP `week-2-<group_id>.zip` | Descripción |
|-----------------------------------------|-------------|
| `week-2-group-<group_id>.ipynb` | Este cuaderno ejecutado |
| `pregunta.json` | La tarjeta con `group_use` y `text_use` |
| `marcas.csv` | Su conjunto marcado, con `marca` en 1 o 0 |
| `outputs/grupos.csv` | Los grupos de los tres métodos |
| `outputs/texto.csv` | Las predicciones de los tres métodos de texto y sus marcas |
| `outputs/en_vista.csv` | Los tres apoyos, `prob_texto`, si el artículo queda en vista y si quedó `recortado` |



<!-- end NOTEBOOK: -->
