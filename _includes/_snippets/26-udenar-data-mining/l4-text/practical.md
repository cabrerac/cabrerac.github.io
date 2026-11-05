<!-- NOTEBOOK: -->

## Repaso de Python para este cuaderno

Este cuaderno utiliza los siguientes métodos de Python. Si ya los conoce, ejecute estas celdas rápido.

### Separar filas para probar
Para saber si un método funciona, lo probamos con filas que **no vio**. `train_test_split` separa las filas, y `stratify` mantiene la proporción de cada clase.

```python
import numpy as np
from sklearn.model_selection import train_test_split

y_toy = np.array([1, 1, 0, 0, 0, 0, 0, 0, 1, 0])
rows_train, rows_test = train_test_split(np.arange(10), test_size=5, stratify=y_toy, random_state=7)
print("Para aprender:", rows_train, "Para probar:", rows_test)
print("Proporción de 1 en cada parte:", y_toy[rows_train].mean(), y_toy[rows_test].mean())
```

### Aciertos y errores a mano
Frente a la marca de una persona hay cuatro casos: **verdadero positivo** (TP), **falso positivo** (FP), **falso negativo** (FN) y **verdadero negativo** (TN).

```python
marked = np.array([1, 0, 1, 1, 0, 0])
said = np.array([1, 1, 0, 1, 0, 0])
tp = int(((said == 1) & (marked == 1)).sum())
fp = int(((said == 1) & (marked == 0)).sum())
fn = int(((said == 0) & (marked == 1)).sum())
tn = int(((said == 0) & (marked == 0)).sum())
assert tp + fp + fn + tn == len(marked)
print(f"TP {tp}, FP {fp}, FN {fn}, TN {tn}. Repaso de Python: OK")
```

---

## Instrucciones

Seguimos con el equipo interno de la secretaría de salud y sus 320 artículos sobre nutrición. El equipo debe decidir **qué artículos tiene que leer** un colega que llega al equipo. En la Lección 3 los grupos salieron débiles, y con `MIN_SUPPORTS = 2` solo 8 artículos quedaron en vista.

Los grupos no miran qué pregunta el equipo. Por años, buscar en textos fue buscar palabras clave. Hoy hay modelos que ya leyeron mucho texto antes de ver el nuestro, el preentrenamiento (Devlin et al., 2019). Aun así, una persona marca primero unos ejemplos. Hoy sumamos un tercer resultado: **leer el texto** y decir si trata del tema. Las marcas se escriben **antes** de correr los métodos, y medimos aciertos y errores en artículos que ningún método vio.

**Tres métodos, tres preparaciones.**

| Método | Pregunta | Preparación que necesita | Cuánto aprende de las marcas |
|--------|----------|--------------------------|------------------------------|
| M1. Lista de palabras clave | ¿El texto tiene alguna palabra de la lista? | Una lista escrita desde la pregunta, antes de ver resultados | Nada: la regla la escribimos nosotros |
| M2. TF-IDF y regresión logística | ¿Qué palabras pesan a favor y en contra? | Conteos con peso TF-IDF, ajustados solo con las filas de entrenamiento | Un peso por palabra |
| M3. Codificador y regresión logística | ¿Qué dice un modelo de lenguaje sobre el texto entero? | El texto con el prefijo `"query: "`, cortado a 512 tokens | Un peso por dimensión del vector |

**Qué hacer.** Ejecute las celdas de arriba hacia abajo. Cada paso empieza con **En este paso** y termina con una celda **Comprobar**.

**Mapa del cuaderno**

| Parte | Fase CRISP-DM | Qué sale |
|-------|---------------|----------|
| 1 | Comprensión del negocio | La pregunta de hoy, los parámetros, el codificador, `pregunta.json` y `outputs/grupos_l3.csv` |
| 2 | Comprensión de los datos | Los artículos, la etiqueta de entrenamiento y el largo de los resúmenes |
| 3 | Preparación de los datos | La lista de palabras, el conjunto marcado, TF-IDF y los textos del codificador |
| 4 | Modelado | Las predicciones de los tres métodos |
| 5 | Evaluación | Aciertos y errores, F1 con intervalo y cinco pliegues |
| 6 | Despliegue | Tres resultados en `supports` y `outputs/texto_l4.csv` |

**Carpetas.** La celda de configuración crea `data/` (datos descargados) y `outputs/` (tablas y gráficos).

---

## Parte 1. Comprensión del negocio

### Paso 1. La pregunta de esta lección
En este paso escribimos qué buscamos hoy. La decisión no cambia: qué artículos debe leer el colega nuevo.

| Pregunta | Respuesta para el laboratorio |
|----------|-------------------------------|
| ¿Qué buscamos? | Qué artículos tratan del tema del equipo, según su resumen |
| ¿Con qué lo medimos? | Una lista de palabras clave, TF-IDF con regresión logística y un codificador ya entrenado |
| ¿Contra qué los comparamos? | Contra la clase mayor, en un conjunto marcado que ningún método ve al aprender |
| ¿Cómo entra el texto en la lista? | Un artículo recibe el resultado del texto si un modelo que no lo vio dice leerlo |

Un acierto solo tiene sentido frente a una marca escrita antes de ver resultados.

### Paso 2. Configuración
En este paso importamos las librerías, creamos las carpetas y fijamos los parámetros. La celda instala `sentence-transformers` solo si falta. No cambie los parámetros. La excepción es `MIN_SUPPORTS`, que empieza en 2 y se puede cambiar. Cada grupo fija y justifica este número en su proyecto.

```python
import importlib.util
import subprocess
import sys

if importlib.util.find_spec("sentence_transformers") is None:
    print("Instalando sentence-transformers (una sola vez por sesión)...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "sentence-transformers"], check=True)

import json          # leer y escribir pregunta.json
import math          # techo (ceil) para los mínimos
import re            # partir el texto en palabras
import time          # medir cuánto tarda cada paso
from collections.abc import Sequence
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import ConfusionMatrixDisplay, accuracy_score, confusion_matrix, f1_score, precision_recall_fscore_support
from sklearn.model_selection import StratifiedKFold, cross_val_predict, train_test_split
from sklearn.pipeline import make_pipeline

# Carpetas de trabajo
DATA_DIR = Path("data")
OUTPUTS_DIR = Path("outputs")
DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

# Desde L2, sin cambios
SUPPORT_SHARE = 0.03
SUPPORT_MIN = 5
SEED = 7

# L4 (no cambiar)
FLAGGED_SHARE = 0.20        # proporción de textos en el conjunto marcado
FLAGGED_MIN = 40            # mínimo de textos marcados
POSITIVE_SHARE = 0.10       # proporción mínima de positivos en la etiqueta
POSITIVES_MIN = 30          # mínimo de positivos
C_REG = 10                  # penalización de la regresión logística (más alto, menos penalización)
N_RESAMPLES = 2000          # bootstrap del F1 en el conjunto marcado
TEXT_MODEL = "intfloat/multilingual-e5-small"
MAX_LENGTH = 512            # tokens que lee el codificador
PREFIX = "query: "          # el prefijo que pide e5

# Desde L3, sin cambios
N_SHUFFLES = 30             # tablas al azar de la línea base de la L3 (aquí no se usa)

# Decisión, L3 en adelante
MIN_SUPPORTS = 2             # el código empieza en 2, cámbielo si lo justifica (0 o 1 también valen)

# Propio de este cuaderno
N_FOLDS = 5                 # pliegues de la validación cruzada


# support_floor: la misma función de la L2.
def support_floor(n_texts: int) -> int:
    """Soporte mínimo que necesita una palabra o un par: max(SUPPORT_MIN, ceil(SUPPORT_SHARE * n))."""
    return max(SUPPORT_MIN, math.ceil(SUPPORT_SHARE * n_texts))


def n_flagged(n: int) -> int:
    """Tamaño del conjunto marcado: max(FLAGGED_MIN, ceil(FLAGGED_SHARE * n))."""
    return max(FLAGGED_MIN, math.ceil(FLAGGED_SHARE * n))


def min_positives(n: int) -> int:
    """Positivos que necesita una etiqueta de entrenamiento: max(POSITIVES_MIN, ceil(POSITIVE_SHARE * n))."""
    return max(POSITIVES_MIN, math.ceil(POSITIVE_SHARE * n))


print(f"scikit-learn {sklearn.__version__}")
print(f"Con 317 artículos: {n_flagged(317)} marcados, al menos {min_positives(317)} positivos")
```

**Comprobar:**

En este paso comprobamos el tamaño del conjunto marcado, el mínimo de positivos y la versión de scikit-learn.

```python
assert n_flagged(317) == 64 and min_positives(317) == 32
assert tuple(int(v) for v in sklearn.__version__.split(".")[:2]) >= (1, 3)
print("Parámetros: OK")
```

### Paso 3. Funciones de las Lecciones 2 y 3
En este paso traemos sin cambios la descarga, las palabras vacías, `words` y `word_list` de las Lecciones 2 y 3.

```python
from spacy.lang.en.stop_words import STOP_WORDS as STOP_WORDS_EN

BASE_URL = "https://cabrerac.github.io/assets/data/26-udenar-data-mining"
WORD_RE = re.compile(r"[^\W\d_]+")
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

    Qué hace: minúsculas, sin "[cita requerida]", solo letras, al menos 3 letras, sin palabras vacías.
    Entrada: text y stop_words.
    Salida: un set con cada palabra una sola vez.
    Por qué: la lista de palabras clave solo pregunta si una palabra está en el texto.
    """
    text = (text or "").lower().replace("[cita requerida]", " ")
    return {w for w in WORD_RE.findall(text) if len(w) >= 3 and w not in stop_words}


def word_list(text: str, stop_words: set[str]) -> list[str]:
    """Como words de la L2, pero conserva las repeticiones (la función de la L3, sin cambios).

    Qué hace: la misma limpieza que words, pero devuelve cada aparición, en orden.
    Entrada: text y stop_words (por defecto STOP_WORDS).
    Salida: una lista de palabras.
    Por qué: TF-IDF cuenta cuántas veces usa un texto cada palabra.
    """
    text = (text or "").lower().replace("[cita requerida]", " ")
    return [w for w in WORD_RE.findall(text) if len(w) >= 3 and w not in stop_words]


print(sorted(words("The diet and the DIET of obese children", STOP_WORDS)))
```

**Comprobar:**

En este paso comprobamos que `word_list` cuenta las repeticiones.

```python
assert word_list("The diet, the DIET and the risk", STOP_WORDS) == ["diet", "diet", "risk"]
print("Funciones de la L2 y la L3: OK")
```

### Paso 4. El codificador de texto
En este paso cargamos el **codificador** `intfloat/multilingual-e5-small`, ya entrenado con texto en muchos idiomas. Lo usamos **congelado**: solo le pedimos un vector por texto.

**Tiempo y tamaño.** `multilingual-e5-small` pesa unos 470 MB y se descarga en esta celda, en menos de un minuto.

```python
from sentence_transformers import SentenceTransformer

start = time.time()
encoder = SentenceTransformer(TEXT_MODEL, device="cpu")
encoder.max_seq_length = MAX_LENGTH
VECTOR_SIZE = len(encoder.encode(PREFIX + "prueba"))
print(f"Codificador cargado en {time.time() - start:.1f} s. Vectores de {VECTOR_SIZE} dimensiones")
```

**Comprobar:**

En este paso comprobamos el largo máximo que lee el codificador y el tamaño de sus vectores.

```python
assert encoder.max_seq_length == MAX_LENGTH
assert VECTOR_SIZE == 384
print("Codificador: OK")
```

### Paso 5. Una función dada: el intervalo del F1
En este paso definimos una función para la Parte 5. **Es una celda dada.** Sortea 2.000 veces las filas marcadas (un **bootstrap**) y devuelve el intervalo del 95 % del F1, o de la **diferencia** de F1 entre dos métodos.

```python
def f1_interval(y, pred_a, pred_b=None, n_resamples=N_RESAMPLES, seed=SEED):
    """Intervalo bootstrap del 95 % del F1 de a, o de F1(a) - F1(b) sobre las mismas filas.

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


print(f1_interval([1, 1, 0, 0, 1, 0], [1, 0, 0, 0, 1, 1]).round(2))
```

### Paso 6. La descripción de la pregunta
En este paso leemos `pregunta.json`, la descripción de la pregunta. Si `pregunta.json` no está, este cuaderno escribe la descripción del laboratorio para que pueda seguir. Lo nuevo es **qué cuenta como artículo del tema**: dieta, obesidad o las enfermedades que dependen de la dieta.

```python
QUESTION_PATH = Path("pregunta.json")

if QUESTION_PATH.is_file():
    question_card = json.loads(QUESTION_PATH.read_text(encoding="utf-8"))
    print("pregunta.json leído de la Lección 3")
else:
    question_card = {
        "question": "¿Qué artículos de nutrición debe leer el equipo para su tema, y qué filtro los puso en la lista?",
        "standard": {"min_papers": 10, "max_papers": 30, "max_share_citations_only": 0.5},
        "pattern_use": {"rule": "El equipo explica por qué cada artículo está en la lista y qué resultados lo apoyan. Un artículo puede tener varios, uno o ninguno, si el equipo lo justifica."},
    }
    QUESTION_PATH.write_text(json.dumps(question_card, ensure_ascii=False, indent=2), encoding="utf-8")
    print("pregunta.json no estaba. Escribimos la descripción del laboratorio.")
print(question_card["question"])
```

**Comprobar:**

En este paso comprobamos que la descripción de la pregunta tiene la pregunta y el estándar.

```python
assert {"question", "standard"} <= set(question_card)
print("Pregunta: OK")
```

### Paso 7. Los grupos de la Lección 3
En este paso leemos `outputs/grupos_l3.csv`, con los resultados de las Lecciones 2 y 3. Si el archivo no está, el cuaderno sigue con esos resultados en 0. Para tenerlos, suba a `outputs/` el archivo de la Lección 3.

```python
GROUPS_PATH = OUTPUTS_DIR / "grupos_l3.csv"
if GROUPS_PATH.is_file():
    groups_l3 = pd.read_csv(GROUPS_PATH)
    print(f"grupos_l3.csv: {len(groups_l3)} artículos, {groups_l3['in_view'].sum()} en vista en la L3")
else:
    groups_l3 = pd.DataFrame(columns=["title", "kmeans", "mezcla", "prob_mezcla", "hdbscan", "has_pattern", "read_group", "supports", "in_view"])
    print("No encontramos outputs/grupos_l3.csv. Sin él, los resultados anteriores quedan en 0.")
```

**Comprobar:**

En este paso comprobamos que la tabla de la Lección 3 tiene las columnas de los dos resultados.

```python
assert {"title", "has_pattern", "read_group", "supports", "in_view"} <= set(groups_l3.columns)
print("Grupos de la L3: OK")
```

---

## Parte 2. Comprensión de los datos

### Paso 1. Los artículos con resumen útil
En este paso cargamos los artículos y dejamos fuera los resúmenes con menos de 5 palabras distintas. Quedan 317.

```python
papers = pd.read_csv(download_data("nutricion-papers.csv"), keep_default_na=False)
useful = [len(words(t, STOP_WORDS)) >= 5 for t in papers["abstract"]]
papers = papers[useful].reset_index(drop=True)
texts = papers["abstract"].tolist()
N = len(texts)
print(f"Artículos usados: {N} de {len(useful)}")
```

**Comprobar:**

En este paso comprobamos el número de artículos usados.

```python
assert N == 317
print("Datos: OK")
```

### Paso 2. La etiqueta de entrenamiento
En este paso armamos la **etiqueta de entrenamiento**: 1 si alguno de los temas de OpenAlex (`topics`) menciona obesidad, dieta, nutrición, diabetes, salud cardiovascular, lipoproteínas, presión arterial o hipertensión, y 0 si no.

Es una etiqueta **dada, no encontrada**. Por eso medimos los métodos contra las marcas de la Parte 3, Paso 2.

```python
TARGET_TOPICS = ["obesity", "diet", "nutrition", "nutritional", "diabetes", "cardiovascular", "lipoproteins", "blood pressure", "hypertension"]

y = np.array([int(any(t in topics.lower() for t in TARGET_TOPICS)) for topics in papers["topics"]])
print(f"Artículos del tema según OpenAlex: {y.sum()} de {N} ({y.mean():.0%}). Mínimo pedido: {min_positives(N)}")
papers.loc[y == 1, ["title", "topics"]].head(3)
```

**Comprobar:**

En este paso comprobamos el número de artículos del tema y que llega al mínimo de positivos.

```python
assert y.sum() == 96
assert y.sum() >= min_positives(N)
print("Etiqueta: OK")
```

### Paso 3. El largo de los resúmenes
En este paso medimos el largo de cada resumen. El codificador lee hasta 512 tokens.

```python
n_words = pd.Series([len(t.split()) for t in texts])
print(f"Palabras por resumen: mediana {n_words.median():.0f}, máximo {n_words.max():,}")
print(f"Resúmenes con más de 400 palabras: {(n_words > 400).sum()}")
```

La mediana es de unas 245 palabras, pero hay resúmenes de miles.

---

## Parte 3. Preparación de los datos

### Paso 1. La lista de palabras clave (preparación de M1)
En este paso escribimos la lista de palabras clave **desde la pregunta**, antes de ver resultados. Todo en minúsculas, con singular, plural y formas cercanas. Una lista hecha mirando las respuestas parece buena y no lo es.

```python
KEYWORDS = {"obesity", "obese", "diet", "diets", "dietary",
            "diabetes", "diabetic", "hypertension", "cholesterol"}

for word in sorted(KEYWORDS):
    has_word = np.array([word in words(t, STOP_WORDS) for t in texts])
    print(f"{word:13s} en {has_word.sum():2d} resúmenes, {(has_word & (y == 0)).sum():2d} fuera del tema según OpenAlex")
```

Una lista larga encuentra más y se equivoca más. *dietary*, *diabetes* y *obesity* aparecen en una decena de resúmenes fuera del tema.

**Comprobar:**

En este paso comprobamos que la lista de palabras está en minúsculas y tiene las formas de *diet*.

```python
assert all(w == w.lower() for w in KEYWORDS)
assert {"diet", "diets"} <= KEYWORDS
print("Lista de palabras: OK")
```

### Paso 2. El conjunto marcado
En este paso separamos el **conjunto marcado**: `n_flagged(N)` artículos, 64 aquí, que ningún método ve al aprender, con `stratify=y`. Los otros 253 son las **filas de entrenamiento**.

**Las marcas.** El profesor marca esos 64 artículos antes de correr los métodos. Si `marcas-nutricion-l4.csv` está publicado, la celda lo usa. Si no, usa la etiqueta de OpenAlex y lo dice.

```python
rows = np.arange(N)
train_rows, marked_rows = train_test_split(rows, test_size=n_flagged(N), stratify=y, random_state=SEED)
train_texts = [texts[i] for i in train_rows]
test_texts = [texts[i] for i in marked_rows]
y_train = y[train_rows]

MARKS_FILE = "marcas-nutricion-l4.csv"
try:
    marks = pd.read_csv(download_data(MARKS_FILE))
    # La hoja de marcas sigue el orden de marked_rows. Unimos por posición, no por título: hay títulos repetidos.
    if marks["title"].tolist() != papers.loc[marked_rows, "title"].tolist():
        raise ValueError("los títulos no siguen el orden del conjunto marcado")
    y_test = marks["marca"].astype(int).to_numpy()
    MARKS_SOURCE = "marcas del profesor"
except Exception as error:
    y_test = y[marked_rows]
    MARKS_SOURCE = "temas de OpenAlex (todavía no hay marcas del profesor)"
    print(f"No usamos {MARKS_FILE} ({type(error).__name__}: {error}).")
print(f"Entrenamiento: {len(train_rows)} filas, {y_train.sum()} del tema")
print(f"Marcados: {len(marked_rows)} filas, {y_test.sum()} del tema. Fuente de las marcas: {MARKS_SOURCE}")
```

**Comprobar:**

En este paso comprobamos el tamaño de las dos partes, que no comparten filas y que las marcas son 0 o 1.

```python
assert len(train_rows) == 253 and len(marked_rows) == n_flagged(N)
assert not set(train_rows) & set(marked_rows)
assert set(np.unique(y_test)) <= {0, 1}
print("Conjunto marcado: OK")
```

### Paso 3. TF-IDF (preparación de M2)
En este paso pesamos las palabras con **TF-IDF**: pesa más una palabra que se repite en un texto y aparece en pocos textos:

$\displaystyle \text{tf} = 1 + \log(\text{conteo}) \qquad \text{idf} = \log\frac{1 + N}{1 + \text{df}} + 1$

df es el número de textos con la palabra. Después cada fila se escala a largo 1.

**Solo con las filas de entrenamiento.** `fit_transform` aprende de las 253 filas. Las marcadas solo se transforman, para que el método no sepa nada de ellas.

```python
train_tokens = [word_list(t, STOP_WORDS) for t in train_texts]   # una lista de palabras por texto, con repeticiones
test_tokens = [word_list(t, STOP_WORDS) for t in test_texts]
tfidf = TfidfVectorizer(analyzer=lambda tokens: tokens, sublinear_tf=True)   # tf = 1 + log(conteo)
X_train = tfidf.fit_transform(train_tokens)     # ajustado solo con las filas de entrenamiento
X_test = tfidf.transform(test_tokens)           # los textos marcados, apartados
feature_names = tfidf.get_feature_names_out()   # un nombre por columna
print(f"Entrenamiento: {X_train.shape}. Marcados: {X_test.shape}")
idf = pd.Series(tfidf.idf_, index=feature_names)
print("idf más bajos:", idf.nsmallest(5).round(2).to_dict())
```

**Comprobar:**

En este paso comprobamos el número de filas de TF-IDF y que cada fila quedó de largo 1.

```python
assert X_train.shape[0] == 253 and X_test.shape[1] == X_train.shape[1]
assert np.allclose(np.sqrt(X_train.multiply(X_train).sum(axis=1)), 1)
print("TF-IDF: OK")
```

### Paso 4. El texto para el codificador (preparación de M3)
En este paso preparamos la entrada de M3: el resumen con el prefijo `"query: "` que pide e5. El codificador parte el texto en **tokens** y lee como máximo 512.

```python
lengths = [len(encoder.tokenizer(PREFIX + t)["input_ids"]) for t in texts]
n_cut = sum(l > MAX_LENGTH for l in lengths)
print(f"Tokens por resumen: mediana {np.median(lengths):.0f}, máximo {max(lengths):,}")
print(f"{n_cut} de {N} resúmenes se cortan a {MAX_LENGTH} tokens")
```

93 de los 317 resúmenes se cortan. El codificador lee su comienzo.

**Comprobar:**

En este paso comprobamos cuántos resúmenes corta el codificador.

```python
assert n_cut == 93
print("Textos del codificador: OK")
```

---

## Parte 4. Modelado

### M1. La lista de palabras clave
En este paso aplicamos la lista: 1 si el texto tiene alguna palabra de la lista, 0 si no.

```python
def keyword_match(text):
    """1 si el texto tiene alguna palabra de la lista, 0 si no."""
    return int(bool(words(text, STOP_WORDS) & KEYWORDS))


pred_keywords = [keyword_match(t) for t in test_texts]
cv_keywords = [keyword_match(t) for t in train_texts]   # sin entrenamiento: la misma regla en las filas de entrenamiento
print(f"La lista dice sí en {sum(pred_keywords)} de {len(test_texts)} marcados")
```

**Comprobar:**

En este paso comprobamos que la lista de palabras da una predicción por artículo marcado.

```python
assert len(pred_keywords) == n_flagged(N)
print("M1: OK")
```

### M2. Regresión logística sobre TF-IDF
En este paso entrenamos una **regresión logística**, que da un peso a cada palabra:

$\displaystyle P(y = 1 \mid x) = \sigma(w \cdot x + b) = \frac{1}{1 + e^{-(w \cdot x + b)}}$

Minimiza la **pérdida logarítmica** con una penalización $L_2$ (`C_REG`). `class_weight="balanced"` pesa más la clase menor. Dice 1 si la probabilidad pasa de 0,5.

```python
lr = LogisticRegression(class_weight="balanced", C=C_REG, max_iter=1000)
lr.fit(X_train, y_train)
pred_lr = lr.predict(X_test)
print(f"TF-IDF dice sí en {pred_lr.sum()} de {len(test_texts)} marcados")
```

**Comprobar:**

En este paso comprobamos que TF-IDF da una predicción de 0 o 1 por artículo marcado.

```python
assert len(pred_lr) == n_flagged(N) and set(np.unique(pred_lr)) <= {0, 1}
print("M2: OK")
```

### M2. Leer los pesos
En este paso leemos las palabras de más peso, a favor y en contra.

```python
weights = pd.Series(lr.coef_[0], index=feature_names)
display(weights.nlargest(15).round(2).to_frame("a favor"))
display(weights.nsmallest(15).round(2).to_frame("en contra"))
```

A favor salen *obesity*, *diet*, *diabetes*, *cardiovascular*. En contra, otros temas: *cancer*, *mental*, *liver*. El modelo aprendió la etiqueta de OpenAlex.

### M3. Los vectores del codificador
En este paso pedimos al codificador un vector de 384 números por resumen (**mean pooling**), de largo 1. Se guardan en `outputs/vectores_l4.npy`.

**Tiempo.** Unos 30 a 60 s en Colab.

```python
VECTORS_PATH = OUTPUTS_DIR / "vectores_l4.npy"
start = time.time()
if VECTORS_PATH.is_file() and np.load(VECTORS_PATH).shape == (N, 384):
    vectors = np.load(VECTORS_PATH)
    print("Vectores leídos de outputs/vectores_l4.npy")
else:
    vectors = encoder.encode([PREFIX + t for t in texts], normalize_embeddings=True, batch_size=16, show_progress_bar=True)
    np.save(VECTORS_PATH, vectors)
print(f"Vectores: {vectors.shape} en {time.time() - start:.1f} s")
V_train = vectors[train_rows]
V_test = vectors[marked_rows]
```

**Comprobar:**

En este paso comprobamos la forma de los vectores y que cada uno tiene largo 1.

```python
assert vectors.shape == (N, 384)
assert np.allclose(np.linalg.norm(vectors, axis=1), 1, atol=1e-4)
print("Vectores: OK")
```

### M3. Regresión logística sobre los vectores
En este paso usamos la misma regresión logística sobre los vectores.

```python
lr_enc = LogisticRegression(class_weight="balanced", C=C_REG, max_iter=1000).fit(V_train, y_train)
pred_encoder = lr_enc.predict(V_test)
print(f"El codificador dice sí en {pred_encoder.sum()} de {len(test_texts)} marcados")
```

**Comprobar:**

En este paso comprobamos que el codificador da una predicción por artículo marcado.

```python
assert len(pred_encoder) == n_flagged(N)
print("M3: OK")
```

---

## Parte 5. Evaluación

### Paso 1. Aciertos y errores en el conjunto marcado
En este paso contamos TP, FP, FN y TN sobre los 64 marcados. De ahí salen tres medidas:

- **Precisión** $= \text{TP} / (\text{TP} + \text{FP})$: de lo que el método dice sí, cuánto era sí.
- **Exhaustividad** (*recall*) $= \text{TP} / (\text{TP} + \text{FN})$: de lo que era sí, cuánto encontró.
- **F1**, la media armónica de las dos: $2 \cdot P \cdot R / (P + R)$.

La **línea base** es la clase mayor: decir "no" a todo. Acierta 7 de cada 10 y no encuentra ninguno del tema.

```python
def counts_of(y, pred):
    """Aciertos y errores de un método en el conjunto marcado.

    Qué hace: cuenta TP, FP, FN y TN, y calcula precisión, exhaustividad, F1 y exactitud.
    Entrada: y (las marcas) y pred (lo que dice el método).
    Salida: un diccionario con los cuatro conteos y las cuatro medidas.
    Por qué: la misma función para todos los métodos hace la comparación justa.
    """
    tn, fp, fn, tp = confusion_matrix(y, pred, labels=[0, 1]).ravel()
    p, r, f1, _ = precision_recall_fscore_support(y, pred, average="binary", zero_division=0)
    return {"TP": tp, "FP": fp, "FN": fn, "TN": tn, "precision": p, "recall": r, "F1": f1, "accuracy": accuracy_score(y, pred)}


pred_majority = [0] * len(y_test)   # la línea base: todo "no leer"
predictions = {"clase mayor": pred_majority, "palabras clave": pred_keywords, "TF-IDF": pred_lr, "codificador": pred_encoder}
results = pd.DataFrame({name: counts_of(y_test, pred) for name, pred in predictions.items()}).T
results[["TP", "FP", "FN", "TN"]] = results[["TP", "FP", "FN", "TN"]].astype(int)   # los conteos, como números enteros
print(f"Marcas: {MARKS_SOURCE}")
results.round(2)
```

TF-IDF y el codificador encuentran casi todos y se equivocan poco. La lista de palabras se equivoca en 7 y no encuentra otros 7.

**Comprobar:**

En este paso comprobamos que los cuatro casos suman los marcados y que TF-IDF supera a la clase mayor.

```python
assert (results[["TP", "FP", "FN", "TN"]].sum(axis=1) == n_flagged(N)).all()
assert results.loc["TF-IDF", "accuracy"] > results.loc["clase mayor", "accuracy"]
print("Aciertos y errores: OK")
```

### Paso 2. Las matrices de confusión
En este paso dibujamos la **matriz de confusión** de cada método.

```python
for name, file_name in [("palabras clave", "confusion_palabras_clave.png"), ("TF-IDF", "confusion_tfidf.png"), ("codificador", "confusion_codificador.png")]:
    display_ = ConfusionMatrixDisplay.from_predictions(y_test, predictions[name], labels=[0, 1], display_labels=["no leer", "leer"], cmap="Blues", colorbar=False)
    display_.ax_.set_title(f"{name}: {len(y_test)} marcados")
    display_.ax_.set_xlabel("Dice el método")
    display_.ax_.set_ylabel("Marca")
    plt.tight_layout()
    plt.savefig(OUTPUTS_DIR / file_name, dpi=120)
    plt.show()
```

### Paso 3. El F1 con su intervalo
En este paso ponemos a cada F1 su intervalo del 95 %. Solo 19 de los 64 marcados son del tema, así que un error mueve mucho el F1.

```python
for name in ["palabras clave", "TF-IDF", "codificador"]:
    low, high = f1_interval(y_test, predictions[name])
    print(f"{name:15s} F1 {results.loc[name, 'F1']:.2f} [{low:.2f}, {high:.2f}]")
```

Los intervalos de TF-IDF y del codificador se tocan casi por completo. El de la lista queda más abajo.

**Comprobar:**

En este paso comprobamos que el F1 de TF-IDF cae dentro de su intervalo.

```python
assert f1_interval(y_test, pred_lr)[0] <= results.loc["TF-IDF", "F1"] <= f1_interval(y_test, pred_lr)[1]
print("Intervalos: OK")
```

### Paso 4. Cinco pliegues en las filas de entrenamiento
En este paso usamos **validación cruzada** con 5 pliegues en las 253 filas de entrenamiento. Con `make_pipeline`, TF-IDF aprende dentro de cada pliegue, así que cada fila se predice sin haberla visto.

```python
folds = StratifiedKFold(n_splits=N_FOLDS, shuffle=True, random_state=SEED)
model_tfidf = make_pipeline(
    TfidfVectorizer(analyzer=lambda tokens: tokens, sublinear_tf=True),
    LogisticRegression(class_weight="balanced", C=C_REG, max_iter=1000))
model_encoder = LogisticRegression(class_weight="balanced", C=C_REG,
                                   max_iter=1000)

cv_tfidf = cross_val_predict(model_tfidf, train_tokens, y_train, cv=folds)
cv_encoder = cross_val_predict(model_encoder, V_train, y_train, cv=folds)

cv_results = pd.DataFrame({
    "clase mayor": counts_of(y_train, [0] * len(y_train)),
    "palabras clave": counts_of(y_train, cv_keywords),
    "TF-IDF": counts_of(y_train, cv_tfidf),
    "codificador": counts_of(y_train, cv_encoder),
}).T
cv_results[["F1", "accuracy"]].round(2)
```

El F1 baja a cerca de 0,77. 64 filas son pocas. Los dos números juntos son más honestos.

**Comprobar:**

En este paso comprobamos que hay una predicción por fila de entrenamiento y que TF-IDF supera a la clase mayor.

```python
assert len(cv_tfidf) == 253
assert cv_results.loc["TF-IDF", "accuracy"] > cv_results.loc["clase mayor", "accuracy"]
print("Cinco pliegues: OK")
```

### Paso 5. ¿Gana el codificador?
En este paso calculamos el intervalo de la **diferencia** de F1 entre el codificador y TF-IDF. Si incluye el 0, no podemos decir que uno gana.

```python
low, high = f1_interval(y_test, pred_encoder, pred_lr)
print(f"F1 del codificador menos F1 de TF-IDF: {results.loc['codificador', 'F1'] - results.loc['TF-IDF', 'F1']:+.2f} [{low:.2f}, {high:.2f}]")
print("El intervalo incluye el 0." if low <= 0 <= high else "El intervalo no incluye el 0.")
```

El intervalo incluye el 0. Con 19 artículos del tema no podemos decir que el codificador gane ni que pierda.

### Paso 6. Leer tres errores por método
En este paso leemos tres errores de cada método. Un error puede ser del método o de la marca.

```python
for name in ["palabras clave", "TF-IDF", "codificador"]:
    wrong = [i for i, (m, p) in enumerate(zip(y_test, predictions[name])) if m != p][:3]
    print(f"\n{name}:")
    for i in wrong:
        kind = "FP (dice leer)" if predictions[name][i] == 1 else "FN (dice no leer)"
        print(f"  {kind}: {papers.loc[marked_rows[i], 'title'][:90]}")
```

---

## Parte 6. Despliegue

### Paso 1. Tres resultados en la tabla
En este paso sumamos el texto como tercer resultado. Cada artículo recibe la predicción de TF-IDF de un modelo que no lo vio: `pred_lr` para los 64 marcados y `cv_tfidf` para los 253. Usamos TF-IDF porque es el más simple que funciona.

Ahora hay tres columnas en `SUPPORT_COLUMNS`. Un artículo queda **en vista** según `MIN_SUPPORTS`, el número de resultados a favor que pide el código. `MIN_SUPPORTS` empieza en 2 y se puede cambiar. Cada grupo fija y justifica este número en su proyecto. 0 o 1 valen si se explica. La celda cuenta cuántos artículos tienen 0, 1, 2 y 3 o más resultados a favor.

```python
SUPPORT_COLUMNS = ["has_pattern", "read_group", "text_says_read"]   # una columna por resultado

text_says_read = np.zeros(N, dtype=int)
text_says_read[marked_rows] = pred_lr
text_says_read[train_rows] = cv_tfidf
encoder_says_read = np.zeros(N, dtype=int)
encoder_says_read[marked_rows] = pred_encoder
encoder_says_read[train_rows] = cv_encoder

# La L3 guarda los artículos en el mismo orden. Unimos por posición, no por título: hay títulos repetidos.
same_rows = len(groups_l3) == N and groups_l3["title"].tolist() == papers["title"].tolist()
supports = pd.DataFrame({"title": papers["title"]})
supports["has_pattern"] = groups_l3["has_pattern"].astype(bool).to_numpy() if same_rows else False
supports["read_group"] = groups_l3["read_group"].astype(bool).to_numpy() if same_rows else False
supports["text_says_read"] = text_says_read.astype(bool)
supports["supports"] = supports[SUPPORT_COLUMNS].astype(int).sum(axis=1)
supports["in_view"] = supports["supports"] >= MIN_SUPPORTS
l3_in_view = (supports[["has_pattern", "read_group"]].astype(int).sum(axis=1) >= MIN_SUPPORTS).sum()
print(f"Solo L2 y L3, con MIN_SUPPORTS = {MIN_SUPPORTS}: {l3_in_view} en vista")
print(f"El texto dice leer: {supports['text_says_read'].sum()}. Con tres resultados: {supports['in_view'].sum()} en vista")
counts = supports["supports"].clip(upper=3).value_counts().reindex(range(4), fill_value=0).rename(index={3: "3 o más"})
print(counts.rename_axis("resultados a favor").to_frame("artículos").T.to_string())
```

Con el texto la lista crece, porque un artículo puede entrar con patrón y texto, o con grupo y texto.

**Comprobar:**

En este paso comprobamos que el número de resultados a favor está en su rango y que la lista no se achica con el texto.

```python
assert supports["supports"].between(0, len(SUPPORT_COLUMNS)).all()
assert supports["in_view"].sum() >= l3_in_view and list(supports.columns[1:4]) == SUPPORT_COLUMNS
print("Resultados: OK")
```

### Paso 2. El largo de la lista
En este paso aplicamos el máximo del estándar, `standard["max_papers"]` (30). Ordenamos por resultados a favor, después por `prob_texto` y al final por título.

Los que no entran siguen en la tabla con `recortado` en verdadero.

```python
MAX_PAPERS = question_card["standard"]["max_papers"]   # el máximo de la descripción de la pregunta (Lección 1)

prob_texto = np.zeros(N)
prob_texto[marked_rows] = lr.predict_proba(X_test)[:, 1]   # marcados: el modelo entrenado sin ellos
prob_texto[train_rows] = cross_val_predict(model_tfidf, train_tokens, y_train, cv=folds, method="predict_proba")[:, 1]   # entrenamiento: los mismos cinco pliegues de cv_tfidf
supports.insert(4, "prob_texto", prob_texto)

order = supports[supports["in_view"]].sort_values(["supports", "prob_texto", "title"], ascending=[False, False, True], kind="mergesort")
kept = order.index[:MAX_PAPERS]
supports["recortado"] = supports["in_view"] & ~supports.index.isin(kept)
print(f"En vista: {supports['in_view'].sum()}. Máximo de la descripción: {MAX_PAPERS}. Quedan {len(kept)}, recortados: {supports['recortado'].sum()}")
print(f"De los que quedan: {(supports.loc[kept, 'supports'] == 3).sum()} con tres resultados y {(supports.loc[kept, 'supports'] == 2).sum()} con dos")
if len(kept) < 5:
    print("Quedan menos de 5 artículos en vista. Es un resultado débil: no rellenamos la lista.")
supports.loc[kept, ["title", "supports", "prob_texto"]].head(10).round(3)
```

Quedan en vista 52 y se leen 30: los 8 con tres resultados y 22 de los 44 con dos. En la lista hay varias ediciones de la misma guía de la ADA. El equipo abre la más reciente.

**Comprobar:**

En este paso comprobamos el corte de la lista, que solo se recortan artículos en vista y que `prob_texto` coincide con el resultado del texto.

```python
assert (supports["in_view"] & ~supports["recortado"]).sum() == min(supports["in_view"].sum(), MAX_PAPERS)
assert not (supports["recortado"] & ~supports["in_view"]).any()
assert ((supports["prob_texto"] > 0.5) == supports["text_says_read"]).all()
print("Lista recortada: OK")
```

### Paso 3. Guardar el texto
En este paso guardamos `outputs/texto_l4.csv`. `marca` lleva las 64 marcas, y `prob_texto` y `recortado` guardan el orden y el corte.

```python
marca = pd.Series(pd.NA, index=range(N), dtype="Int64")
marca[marked_rows] = y_test
text_table = pd.DataFrame({
    "title": papers["title"],
    "keyword": [keyword_match(t) for t in texts],
    "tfidf_lr": text_says_read,
    "prob_texto": prob_texto,
    "codificador": encoder_says_read,
    "marca": marca,
    "supports": supports["supports"],
    "in_view": supports["in_view"],
    "recortado": supports["recortado"],
})
text_path = OUTPUTS_DIR / "texto_l4.csv"
text_table.to_csv(text_path, index=False)
print(f"Guardado: {text_path} ({len(text_table)} filas, {text_table['marca'].notna().sum()} marcadas)")
```

**Comprobar:**

En este paso comprobamos que el archivo guardado tiene sus columnas y las marcas de los artículos marcados.

```python
saved = pd.read_csv(text_path)
assert {"title", "keyword", "tfidf_lr", "prob_texto", "codificador", "marca", "supports", "in_view", "recortado"} <= set(saved.columns)
assert saved["marca"].notna().sum() == n_flagged(N)
print("texto_l4.csv: OK")
```

### Paso 4. Qué cambiaría la decisión
En este paso escribimos en la descripción de la pregunta cómo entra el texto y qué lo cambiaría: otra lista de palabras, otras marcas, otra etiqueta, otro umbral que 0,5 u otro máximo de la lista.

```python
question_card["text_use"] = {
    "how_it_enters": "El resultado del texto cuenta a favor de un artículo si TF-IDF con regresión logística dice leer, con un modelo que no lo vio.",
    "marks": MARKS_SOURCE,
    "reading": "TF-IDF y el codificador no se distinguen con este conjunto marcado: el intervalo de la diferencia incluye el 0.",
    "rule": "MIN_SUPPORTS empieza en 2, de tres resultados: patrón (L2), grupo (L3) y texto (L4). Se puede cambiar. Cada grupo fija y justifica este número en su proyecto. 0 o 1 valen si se explica.",
    "reading_list": "Si hay más en vista que el máximo de la descripción, se ordena por número de resultados a favor, luego por prob_texto y luego por título. El resto queda con recortado = True.",
    "what_changes_it": ["otra lista de palabras", "otro conjunto marcado", "otra etiqueta de entrenamiento", "otro umbral que 0,5", "otro máximo de la lista", "otro orden del recorte"],
}
QUESTION_PATH.write_text(json.dumps(question_card, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(question_card["text_use"], ensure_ascii=False, indent=1))
```

### Paso 5. Comprobación final
En este paso revisamos que el cuaderno dejó lo que la Lección 5 necesita.

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
    ("pregunta.json con uso del texto", lambda: "text_use" in json.loads(QUESTION_PATH.read_text(encoding="utf-8"))),
    ("outputs/texto_l4.csv", lambda: text_path.is_file()),
    ("outputs/vectores_l4.npy", lambda: VECTORS_PATH.is_file()),
    ("Matrices de confusión", lambda: all((OUTPUTS_DIR / f).is_file() for f in ["confusion_palabras_clave.png", "confusion_tfidf.png", "confusion_codificador.png"])),
    ("Resultados de la L3", lambda: len(groups_l3) == N),
]
passed = sum(_check_ok(n, f) for n, f in checks)
print(f"\nL4_CHECKS={passed}/{len(checks)}")
if passed == len(checks):
    print("L4_OK. Siga con la Lección 5.")
```

<!-- end NOTEBOOK: -->
