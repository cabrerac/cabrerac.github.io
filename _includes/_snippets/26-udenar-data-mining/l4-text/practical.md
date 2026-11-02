<!-- NOTEBOOK: -->

## Repaso de Python para este cuaderno
 
Este repaso es corto. Muestra las dos ideas que usamos en toda la lección: separar filas para probar, y contar aciertos y errores. Si ya las conoce, ejecute las celdas rápido y siga.
 
### Separar filas para probar
Para saber si un método funciona, lo probamos con filas que **no vio** al aprender. `train_test_split` separa las filas en dos partes. Con `stratify`, las dos partes tienen la misma proporción de cada clase.



```python
import numpy as np
from sklearn.model_selection import train_test_split

y_toy = np.array([1, 1, 0, 0, 0, 0, 0, 0, 1, 0])
rows_train, rows_test = train_test_split(np.arange(10), test_size=5, stratify=y_toy, random_state=7)
print("Para aprender:", rows_train, "Para probar:", rows_test)
print("Proporción de 1 en cada parte:", y_toy[rows_train].mean(), y_toy[rows_test].mean())
```

### Aciertos y errores a mano
Comparamos lo que dice un método con lo que marcó una persona. Hay cuatro casos: el método dice sí y era sí (**verdadero positivo**, TP), dice sí y era no (**falso positivo**, FP), dice no y era sí (**falso negativo**, FN), dice no y era no (**verdadero negativo**, TN).



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
 
**La historia.** Seguimos con el equipo interno de la secretaría de salud y sus 320 artículos de nutrición. En la Lección 2 encontramos patrones y en la Lección 3 grupos débiles. Con dos resultados, solo 8 artículos quedaron en vista, menos de los 10 que pide el estándar, porque el apoyo del grupo lo reciben solo los 10 artículos del grupo de HDBSCAN que lee el equipo. Hoy sumamos un tercer resultado: **leer el texto** de cada resumen y decir si trata del tema del equipo.
 
**La idea central.** Para enseñarle a un método qué es "un artículo del tema", necesitamos **ejemplos marcados**. Las marcas se escriben **antes** de correr cualquier método, para que los resultados no nos cambien la vara. Separamos un conjunto de artículos marcados que ningún método ve al aprender, y medimos ahí los aciertos y los errores.
 
**Tres métodos, tres preparaciones.**
 
| Método | Pregunta | Preparación que necesita | Cuánto aprende de las marcas |
|--------|----------|--------------------------|------------------------------|
| M1. Lista de palabras clave | ¿El texto tiene alguna palabra de la lista? | Una lista escrita desde la pregunta, antes de ver resultados | Nada: la regla la escribimos nosotros |
| M2. TF-IDF y regresión logística | ¿Qué palabras pesan a favor y en contra? | Conteos con peso TF-IDF, ajustados solo con las filas de entrenamiento | Un peso por palabra |
| M3. Codificador y regresión logística | ¿Qué dice un modelo de lenguaje sobre el texto entero? | El texto con el prefijo `"query: "`, cortado a 512 tokens | Un peso por dimensión del vector |
 
**Qué hacer.** Ejecute las celdas de arriba hacia abajo. Cada paso empieza con **En este paso**. Los pasos que crean algo nuevo terminan con una celda **Comprobar**. Si un `assert` falla, revise la celda anterior antes de seguir. Los nombres del código están en inglés, como en todos los cuadernos del curso. Las explicaciones están en español.
 
**Mapa del cuaderno**
 
| Parte | Fase CRISP-DM | Qué sale |
|-------|---------------|----------|
| 1 | Configuración | Librerías, parámetros, el codificador y la función del intervalo |
| 2 | Comprensión del negocio | `pregunta.json` y `outputs/grupos_l3.csv` de la Lección 3 |
| 3 | Comprensión de los datos | Los artículos, la etiqueta de entrenamiento y el largo de los resúmenes |
| 4 | Preparación de los datos | La lista de palabras, el conjunto marcado, TF-IDF y los textos del codificador |
| 5 | Modelado | Las predicciones de los tres métodos |
| 6 | Evaluación | Aciertos y errores, F1 con intervalo y cinco pliegues |
| 7 | Despliegue | Tres resultados en `supports` y `outputs/texto_l4.csv` |

---
 
## Parte 1. Configuración
 
### Paso 1. Librerías, carpetas y parámetros
En este paso instalamos lo que falte, importamos las librerías y fijamos los parámetros. En Colab, scikit-learn ya viene instalado. La celda revisa si está `sentence-transformers` y lo instala solo si falta. Los parámetros de la L2 y la L3 se copian sin cambios. Los de la L4 se definen aquí una sola vez y son los mismos en el cuaderno de grupo y en el script de control. No los cambie aquí.



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

# L4 (compartidos con el cuaderno de grupo y el script de control, no cambiar)
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
MIN_SUPPORTS = 2

# Propio de este cuaderno
N_FOLDS = 5                 # pliegues de la validación cruzada


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


print(f"scikit-learn {sklearn.__version__}")
print(f"Con 317 artículos: {n_flagged(317)} marcados, al menos {min_positives(317)} positivos")
```

**Comprobar:**



```python
assert n_flagged(317) == 64 and min_positives(317) == 32
assert tuple(int(v) for v in sklearn.__version__.split(".")[:2]) >= (1, 3)
print("Parámetros: OK")
```

### Paso 2. Funciones de las Lecciones 2 y 3
En este paso traemos, sin cambios, lo que ya conocemos: la descarga, las palabras vacías de la L2, `words` (un conjunto de palabras) y `word_list` (la lista con repeticiones de la L3). Los tres métodos parten de esta misma preparación.



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



```python
assert word_list("The diet, the DIET and the risk", STOP_WORDS) == ["diet", "diet", "risk"]
print("Funciones de la L2 y la L3: OK")
```

### Paso 3. El codificador de texto
En este paso cargamos el **codificador** `intfloat/multilingual-e5-small`. Es un modelo de lenguaje ya entrenado con mucho texto en muchos idiomas. Lo usamos **congelado**: no lo ajustamos, solo le pedimos un vector por texto. El mismo modelo sirve para inglés (este cuaderno) y para español (el cuaderno de grupo).
 
**Tiempo y tamaño.** El modelo se descarga al cargarlo, en esta celda. En un Colab nuevo se descargan unos 470 MB, menos de un minuto. Después queda en la sesión.



```python
from sentence_transformers import SentenceTransformer

start = time.time()
encoder = SentenceTransformer(TEXT_MODEL, device="cpu")
encoder.max_seq_length = MAX_LENGTH
VECTOR_SIZE = len(encoder.encode(PREFIX + "prueba"))
print(f"Codificador cargado en {time.time() - start:.1f} s. Vectores de {VECTOR_SIZE} dimensiones")
```

**Comprobar:**



```python
assert encoder.max_seq_length == MAX_LENGTH
assert VECTOR_SIZE == 384
print("Codificador: OK")
```

### Paso 4. Una función dada: el intervalo del F1
En este paso definimos una función que usaremos en la Parte 6. **Es una celda dada**: no hace falta entender cada línea ahora. La función toma las marcas y las predicciones de un método, sortea 2.000 veces las filas marcadas con reemplazo (un **bootstrap**) y devuelve los percentiles 2,5 y 97,5 del F1. Con dos métodos, devuelve el intervalo de la **diferencia** de F1 sobre las mismas filas.



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

---
 
## Parte 2. Comprensión del negocio
 
### Paso 1. Recuperar la pregunta
En este paso leemos `pregunta.json`. Si abre este cuaderno en un Colab nuevo, la celda escribe la tarjeta para que pueda seguir. La pregunta no cambia. Lo nuevo es **qué cuenta como un artículo del tema**: un artículo sobre dieta, obesidad o las enfermedades que dependen de la dieta.



```python
QUESTION_PATH = Path("pregunta.json")

if QUESTION_PATH.is_file():
    question_card = json.loads(QUESTION_PATH.read_text(encoding="utf-8"))
    print("pregunta.json leído de la Lección 3")
else:
    question_card = {
        "question": "¿Qué artículos de nutrición debe leer el equipo para su tema, y qué filtro los puso en la lista?",
        "standard": {"min_papers": 10, "max_papers": 30, "max_share_citations_only": 0.5},
        "pattern_use": {"rule": "Un artículo entra en la lista cuando lo apoyan al menos dos resultados del curso."},
    }
    QUESTION_PATH.write_text(json.dumps(question_card, ensure_ascii=False, indent=2), encoding="utf-8")
    print("pregunta.json no estaba. Escribimos la tarjeta.")
print(question_card["question"])
```

**Comprobar:**



```python
assert {"question", "standard"} <= set(question_card)
print("Pregunta: OK")
```

### Paso 2. Recuperar los grupos de la Lección 3
En este paso leemos `outputs/grupos_l3.csv`. Trae, para cada artículo, los dos apoyos de la L2 y la L3. En la Parte 7 sumaremos el tercero. Si el archivo no está (un Colab nuevo), súbalo desde su cuaderno de la L3 a la carpeta `outputs/`. Sin él, el cuaderno sigue, pero los apoyos anteriores quedan en 0.



```python
GROUPS_PATH = OUTPUTS_DIR / "grupos_l3.csv"
if GROUPS_PATH.is_file():
    groups_l3 = pd.read_csv(GROUPS_PATH)
    print(f"grupos_l3.csv: {len(groups_l3)} artículos, {groups_l3['in_view'].sum()} en vista con dos resultados")
else:
    groups_l3 = pd.DataFrame(columns=["title", "kmeans", "mezcla", "prob_mezcla", "hdbscan", "has_pattern", "read_group", "supports", "in_view"])
    print("No encontramos outputs/grupos_l3.csv. Súbalo desde la L3 y vuelva a ejecutar esta celda.")
```

**Comprobar:**



```python
assert {"title", "has_pattern", "read_group", "supports", "in_view"} <= set(groups_l3.columns)
print("Grupos de la L3: OK")
```

---
 
## Parte 3. Comprensión de los datos
 
### Paso 1. Los artículos con resumen útil
En este paso cargamos los artículos con la regla de la L2 y la L3: fuera los resúmenes con menos de 5 palabras distintas. El archivo tiene 320 filas. Tres son fragmentos como "Peer Reviewed", así que quedan 317.



```python
papers = pd.read_csv(download_data("nutricion-papers.csv"), keep_default_na=False)
useful = [len(words(t, STOP_WORDS)) >= 5 for t in papers["abstract"]]
papers = papers[useful].reset_index(drop=True)
texts = papers["abstract"].tolist()
N = len(texts)
print(f"Artículos usados: {N} de {len(useful)}")
```

**Comprobar:**



```python
assert N == 317
print("Datos: OK")
```

### Paso 2. La etiqueta de entrenamiento
En este paso armamos la **etiqueta de entrenamiento**: un 1 para cada artículo del tema y un 0 para el resto. No marcamos a mano 317 artículos. Usamos los temas que OpenAlex asigna a cada artículo (`topics`): un artículo es del tema si alguno de sus temas menciona obesidad, dieta, nutrición, diabetes, salud cardiovascular, lipoproteínas, presión arterial o hipertensión.
 
Es una etiqueta **dada, no encontrada**: la escribió otro, con su propio criterio. Por eso no medimos los métodos contra ella sino contra las marcas del Paso 2 de la Parte 4.



```python
TARGET_TOPICS = ["obesity", "diet", "nutrition", "nutritional", "diabetes", "cardiovascular", "lipoproteins", "blood pressure", "hypertension"]

y = np.array([int(any(t in topics.lower() for t in TARGET_TOPICS)) for topics in papers["topics"]])
print(f"Artículos del tema según OpenAlex: {y.sum()} de {N} ({y.mean():.0%}). Mínimo pedido: {min_positives(N)}")
papers.loc[y == 1, ["title", "topics"]].head(3)
```

**Comprobar:**



```python
assert y.sum() == 96
assert y.sum() >= min_positives(N)
print("Etiqueta: OK")
```

### Paso 3. El largo de los resúmenes
En este paso medimos el largo de cada resumen en palabras. El codificador de la Parte 4 lee hasta 512 tokens, así que los resúmenes muy largos se cortan.



```python
n_words = pd.Series([len(t.split()) for t in texts])
print(f"Palabras por resumen: mediana {n_words.median():.0f}, máximo {n_words.max():,}")
print(f"Resúmenes con más de 400 palabras: {(n_words > 400).sum()}")
```

La mediana es de unas 245 palabras, pero hay resúmenes de miles de palabras. Son textos que OpenAlex guardó con parte del artículo. Contaremos cuántos corta el codificador.

---
 
## Parte 4. Preparación de los datos
 
### Paso 1. La lista de palabras clave (preparación de M1)
En este paso escribimos la lista **desde la pregunta**, antes de ver ningún resultado. Pensamos qué palabras usaría un artículo del tema. Normalizamos: todo en minúsculas, singular y plural, y formas cercanas (*diabetes*, *diabetic*). No miramos la etiqueta ni los resultados para armarla: una lista hecha mirando las respuestas parece buena y no lo es.



```python
KEYWORDS = {"obesity", "obese", "diet", "diets", "dietary",
            "diabetes", "diabetic", "hypertension", "cholesterol"}

for word in sorted(KEYWORDS):
    has_word = np.array([word in words(t, STOP_WORDS) for t in texts])
    print(f"{word:13s} en {has_word.sum():2d} resúmenes, {(has_word & (y == 0)).sum():2d} fuera del tema según OpenAlex")
```

Una lista más larga encuentra más artículos del tema, y también más artículos que no lo son. Una lista más corta se equivoca menos pero se pierde más. Mire *dietary*, *diabetes* y *obesity*: cada una aparece en una decena de resúmenes fuera del tema. *diet*, en cambio, casi siempre cae en el tema.
 
**Comprobar:**



```python
assert all(w == w.lower() for w in KEYWORDS)
assert {"diet", "diets"} <= KEYWORDS
print("Lista de palabras: OK")
```

### Paso 2. El conjunto marcado
En este paso separamos el **conjunto marcado**: `n_flagged(N)` artículos, 64 aquí, que ningún método ve al aprender. Usamos `stratify=y` para que tengan la misma proporción de artículos del tema que el resto. Los otros 253 son las **filas de entrenamiento**.
 
**Las marcas.** El profesor marca a mano esos 64 artículos: 1 si el equipo debe leerlo para su tema, 0 si no. Marca antes de correr los métodos. Si sus marcas están publicadas (`marcas-nutricion-l4.csv`), la celda las usa. Si no, usa la etiqueta de OpenAlex en esas filas, y lo dice.



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



```python
assert len(train_rows) == 253 and len(marked_rows) == n_flagged(N)
assert not set(train_rows) & set(marked_rows)
assert set(np.unique(y_test)) <= {0, 1}
print("Conjunto marcado: OK")
```

### Paso 3. TF-IDF (preparación de M2)
En este paso pesamos las palabras con **TF-IDF**. Una palabra pesa más si se repite en un texto (TF) y si aparece en pocos textos de la colección (IDF):
 
$\displaystyle \text{tf} = 1 + \log(\text{conteo}) \qquad \text{idf} = \log\frac{1 + N}{1 + \text{df}} + 1$
 
donde df es el número de textos con la palabra. Una palabra que está en casi todos los resúmenes, como *health*, recibe un idf bajo. Después cada fila se escala a largo 1, como en la L3.
 
**Solo con las filas de entrenamiento.** `fit_transform` aprende el vocabulario y los idf de las 253 filas de entrenamiento. Las filas marcadas solo se transforman. Si el idf viera las filas marcadas, el método sabría algo de ellas antes de la prueba.



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



```python
assert X_train.shape[0] == 253 and X_test.shape[1] == X_train.shape[1]
assert np.allclose(np.sqrt(X_train.multiply(X_train).sum(axis=1)), 1)
print("TF-IDF: OK")
```

### Paso 4. El texto para el codificador (preparación de M3)
En este paso preparamos la entrada de M3: el resumen tal como está, con el prefijo `"query: "` que pide e5. El codificador no usa nuestras palabras vacías. Parte el texto en **tokens**, pedazos de palabras de su propio vocabulario, y lee como máximo 512. Contamos cuántos resúmenes pasan de 512 tokens y se cortan.



```python
lengths = [len(encoder.tokenizer(PREFIX + t)["input_ids"]) for t in texts]
n_cut = sum(l > MAX_LENGTH for l in lengths)
print(f"Tokens por resumen: mediana {np.median(lengths):.0f}, máximo {max(lengths):,}")
print(f"{n_cut} de {N} resúmenes se cortan a {MAX_LENGTH} tokens")
```

93 de los 317 resúmenes se cortan. El codificador lee su comienzo, que en un resumen suele decir el tema. En las entradillas de Wikipedia del cuaderno de grupo, más cortas, se cortan pocas: entre 6 y 41 por extracto.
 
**Comprobar:**



```python
assert n_cut == 93
print("Textos del codificador: OK")
```

---
 
## Parte 5. Modelado
 
### M1. La lista de palabras clave
En este paso aplicamos la lista. La regla es simple: 1 si el texto tiene alguna palabra de la lista, 0 si no. No aprende nada de las marcas.



```python
def keyword_match(text):
    """1 si el texto tiene alguna palabra de la lista, 0 si no."""
    return int(bool(words(text, STOP_WORDS) & KEYWORDS))


pred_keywords = [keyword_match(t) for t in test_texts]
cv_keywords = [keyword_match(t) for t in train_texts]   # sin entrenamiento: la misma regla en las filas de entrenamiento
print(f"La lista dice sí en {sum(pred_keywords)} de {len(test_texts)} marcados")
```

**Comprobar:**



```python
assert len(pred_keywords) == n_flagged(N)
print("M1: OK")
```

### M2. Regresión logística sobre TF-IDF
En este paso entrenamos una **regresión logística**. El modelo da un peso a cada palabra y calcula la probabilidad de que un texto sea del tema:
 
$\displaystyle P(y = 1 \mid x) = \sigma(w \cdot x + b) = \frac{1}{1 + e^{-(w \cdot x + b)}}$
 
Aprende los pesos minimizando la **pérdida logarítmica** más una penalización $L_2$ que evita pesos enormes. `C_REG` controla esa penalización: más alto, menos penalización. `class_weight="balanced"` da más peso a los artículos del tema, que son menos. El modelo dice 1 cuando la probabilidad pasa de 0,5.



```python
lr = LogisticRegression(class_weight="balanced", C=C_REG, max_iter=1000)
lr.fit(X_train, y_train)
pred_lr = lr.predict(X_test)
print(f"TF-IDF dice sí en {pred_lr.sum()} de {len(test_texts)} marcados")
```

**Comprobar:**



```python
assert len(pred_lr) == n_flagged(N) and set(np.unique(pred_lr)) <= {0, 1}
print("M2: OK")
```

### M2. Leer los pesos
En este paso leemos las palabras de más peso, a favor y en contra. Un modelo que acierta por una palabra rara merece una mirada.



```python
weights = pd.Series(lr.coef_[0], index=feature_names)
display(weights.nlargest(15).round(2).to_frame("a favor"))
display(weights.nsmallest(15).round(2).to_frame("en contra"))
```

A favor salen las palabras del tema: *obesity*, *diet*, *diabetes*, *cardiovascular*. En contra salen palabras de otros temas de la colección: *cancer*, *mental*, *liver*, *infections*, *dementia*, *agricultural*. El modelo aprendió lo que dice la etiqueta de OpenAlex, con sus aciertos y sus límites.

### M3. Los vectores del codificador
En este paso pedimos al codificador un vector por resumen. El codificador lee los tokens, los pasa por sus capas y promedia los vectores de los tokens (**mean pooling**) en un solo vector de 384 números. `normalize_embeddings=True` lo deja de largo 1. Guardamos los vectores en `outputs/vectores_l4.npy` para no volver a calcularlos si repite la celda.
 
**Tiempo.** En Colab gratuito, unos 30 a 60 s para los 317 resúmenes. La descarga ya ocurrió al cargar el modelo, en la Parte 1.



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



```python
assert vectors.shape == (N, 384)
assert np.allclose(np.linalg.norm(vectors, axis=1), 1, atol=1e-4)
print("Vectores: OK")
```

### M3. Regresión logística sobre los vectores
En este paso usamos la misma regresión logística, ahora sobre los vectores. El codificador no cambia: solo aprendemos un peso por dimensión.



```python
lr_enc = LogisticRegression(class_weight="balanced", C=C_REG, max_iter=1000).fit(V_train, y_train)
pred_encoder = lr_enc.predict(V_test)
print(f"El codificador dice sí en {pred_encoder.sum()} de {len(test_texts)} marcados")
```

**Comprobar:**



```python
assert len(pred_encoder) == n_flagged(N)
print("M3: OK")
```

---
 
## Parte 6. Evaluación
 
### Paso 1. Aciertos y errores en el conjunto marcado
En este paso contamos, para cada método, TP, FP, FN y TN sobre los 64 marcados. De ahí salen tres medidas:
 
- **Precisión** $= \text{TP} / (\text{TP} + \text{FP})$: de lo que el método dice sí, cuánto era sí.
- **Exhaustividad** (*recall*) $= \text{TP} / (\text{TP} + \text{FN})$: de lo que era sí, cuánto encontró.
- **F1**, la media armónica de las dos: $2 \cdot P \cdot R / (P + R)$.
 
La **línea base** es la clase mayor: decir "no" a todo. Acierta en 7 de cada 10 artículos y no encuentra ninguno del tema.



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

TF-IDF y el codificador encuentran casi todos los artículos del tema y se equivocan poco. La lista de palabras encuentra menos y se equivoca más: dice sí en 7 artículos que no son del tema, por *dietary*, *diabetes* u *obesity*, y no encuentra 7 artículos del tema que no usan ninguna palabra de la lista.
 
**Comprobar:**



```python
assert (results[["TP", "FP", "FN", "TN"]].sum(axis=1) == n_flagged(N)).all()
assert results.loc["TF-IDF", "accuracy"] > results.loc["clase mayor", "accuracy"]
print("Aciertos y errores: OK")
```

### Paso 2. Las matrices de confusión
En este paso dibujamos los cuatro conteos de cada método como una **matriz de confusión**: filas para la marca, columnas para lo que dice el método.



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
En este paso ponemos a cada F1 su intervalo del 95 %, con la función dada de la Parte 1. Solo 19 de los 64 marcados son del tema. Con tan pocos, un artículo mal clasificado mueve mucho el F1.



```python
for name in ["palabras clave", "TF-IDF", "codificador"]:
    low, high = f1_interval(y_test, predictions[name])
    print(f"{name:15s} F1 {results.loc[name, 'F1']:.2f} [{low:.2f}, {high:.2f}]")
```

Los intervalos de TF-IDF y del codificador se tocan casi por completo. Varios llegan a 1,00. El de la lista de palabras queda claramente más abajo.
 
**Comprobar:**



```python
assert f1_interval(y_test, pred_lr)[0] <= results.loc["TF-IDF", "F1"] <= f1_interval(y_test, pred_lr)[1]
print("Intervalos: OK")
```

### Paso 4. Cinco pliegues en las filas de entrenamiento
En este paso miramos los métodos de otra forma: con **validación cruzada** en las 253 filas de entrenamiento. Partimos esas filas en 5 pliegues. Cada pliegue se predice con un modelo que aprendió de los otros cuatro. Para TF-IDF usamos una tubería (`make_pipeline`): los pesos de las palabras se aprenden dentro de cada pliegue. Así cada fila de entrenamiento se predice una vez, sin que el modelo la haya visto.



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

En los cinco pliegues el F1 baja (alrededor de 0,77 para los dos modelos) respecto del conjunto marcado. Es lo esperado: 64 filas son pocas, y el conjunto marcado tuvo suerte. Los dos números juntos dan una idea más honesta que cualquiera solo.
 
**Comprobar:**



```python
assert len(cv_tfidf) == 253
assert cv_results.loc["TF-IDF", "accuracy"] > cv_results.loc["clase mayor", "accuracy"]
print("Cinco pliegues: OK")
```

### Paso 5. ¿Gana el codificador?
En este paso preguntamos si el conjunto marcado puede distinguir al codificador de TF-IDF. Usamos la misma función con los dos métodos: el intervalo de la **diferencia** de F1 sobre las mismas filas. Si el intervalo incluye el 0, los datos no alcanzan para decir que uno gana.



```python
low, high = f1_interval(y_test, pred_encoder, pred_lr)
print(f"F1 del codificador menos F1 de TF-IDF: {results.loc['codificador', 'F1'] - results.loc['TF-IDF', 'F1']:+.2f} [{low:.2f}, {high:.2f}]")
print("El intervalo incluye el 0." if low <= 0 <= high else "El intervalo no incluye el 0.")
```

El intervalo incluye el 0. Con 19 artículos del tema en el conjunto marcado, no podemos decir que el codificador gane, ni que pierda. En los cinco extractos de los grupos pasa lo mismo: todos los intervalos incluyen el 0. El codificador puede ayudar cuando las palabras del tema varían mucho, y no agrega nada cuando unas pocas palabras deciden, como aquí *obesity* o *diabetes*. No es una competencia.

### Paso 6. Leer tres errores por método
En este paso leemos a mano tres artículos mal clasificados por cada método. Un error puede ser del método, o puede ser de la marca. Leerlos es la única forma de saberlo.



```python
for name in ["palabras clave", "TF-IDF", "codificador"]:
    wrong = [i for i, (m, p) in enumerate(zip(y_test, predictions[name])) if m != p][:3]
    print(f"\n{name}:")
    for i in wrong:
        kind = "FP (dice leer)" if predictions[name][i] == 1 else "FN (dice no leer)"
        print(f"  {kind}: {papers.loc[marked_rows[i], 'title'][:90]}")
```

**Su turno.** Elija uno de esos errores. Lea el resumen (`papers.loc[marked_rows[i], "abstract"]`) y escriba en dos frases si el error es del método o de la marca, y por qué.



```python
my_error = """
Escriba aquí el título, si el error es del método o de la marca, y por qué.
"""
print(my_error)
```

---
 
## Parte 7. Despliegue
 
### Paso 1. Tres resultados en la tabla de apoyos
En este paso sumamos el texto como tercer resultado. Cada artículo recibe una predicción de TF-IDF de un modelo que no lo vio: los 64 marcados, del modelo entrenado con las 253 filas (`pred_lr`), y las 253 filas de entrenamiento, de los cinco pliegues (`cv_tfidf`). Usamos TF-IDF porque es el método más simple que funciona, y el codificador no lo supera con claridad.
 
Ahora hay tres columnas en `SUPPORT_COLUMNS`. Un artículo queda **en vista** con al menos `MIN_SUPPORTS` (2) de los tres.



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
print(f"Con dos resultados (L2 y L3): {l3_in_view} en vista")
print(f"El texto dice leer: {supports['text_says_read'].sum()}. Con tres resultados: {supports['in_view'].sum()} en vista")
print(supports["supports"].value_counts().sort_index().to_dict())
```

`grupos_l3.csv` guarda los dos apoyos de la L2 y la L3 en `has_pattern` y `read_group`. Aquí les sumamos `text_says_read`, una columna por resultado, como en la L3. La regla es la misma: dos apoyos de tres. Con el texto, la lista crece, porque ahora un artículo puede entrar con patrón y texto, o con grupo y texto. Los artículos con los tres apoyos son los primeros para abrir.
 
**Comprobar:**



```python
assert supports["supports"].between(0, len(SUPPORT_COLUMNS)).all()
assert supports["in_view"].sum() >= l3_in_view and list(supports.columns[1:4]) == SUPPORT_COLUMNS
print("Apoyos: OK")
```

### Paso 2. El largo de la lista
En este paso comparamos la lista con el estándar de la tarjeta. La L1 fijó un máximo, `standard["max_papers"]` (30): una lista más larga no se alcanza a leer. Si hay más artículos en vista, los ordenamos y nos quedamos con los primeros. Primero van los de más apoyos. Entre los que tienen los mismos apoyos, primero va el de `prob_texto` más alta. `prob_texto` dice qué tan seguro está TF-IDF de que conviene abrir el artículo. Como `text_says_read`, sale de un modelo que no vio ese artículo. Al final desempata el título, para que el corte sea el mismo en cada corrida.
 
Los que no entran no se borran. Quedan en la tabla con `recortado` en verdadero.



```python
MAX_PAPERS = question_card["standard"]["max_papers"]   # el máximo de la tarjeta de la L1

prob_texto = np.zeros(N)
prob_texto[marked_rows] = lr.predict_proba(X_test)[:, 1]   # marcados: el modelo entrenado sin ellos
prob_texto[train_rows] = cross_val_predict(model_tfidf, train_tokens, y_train, cv=folds, method="predict_proba")[:, 1]   # entrenamiento: los mismos cinco pliegues de cv_tfidf
supports.insert(4, "prob_texto", prob_texto)

order = supports[supports["in_view"]].sort_values(["supports", "prob_texto", "title"], ascending=[False, False, True], kind="mergesort")
kept = order.index[:MAX_PAPERS]
supports["recortado"] = supports["in_view"] & ~supports.index.isin(kept)
print(f"En vista: {supports['in_view'].sum()}. Máximo de la tarjeta: {MAX_PAPERS}. Quedan {len(kept)}, recortados: {supports['recortado'].sum()}")
print(f"De los que quedan: {(supports.loc[kept, 'supports'] == 3).sum()} con tres apoyos y {(supports.loc[kept, 'supports'] == 2).sum()} con dos")
if len(kept) < 5:
    print("Quedan menos de 5 artículos en vista. Es un resultado débil: no rellenamos la lista.")
supports.loc[kept, ["title", "supports", "prob_texto"]].head(10).round(3)
```

Quedan en vista 52 artículos y la tarjeta pide como máximo 30. Arriba quedan los 8 con los tres apoyos, y después 22 de los 44 con dos, los de `prob_texto` más alta. Los otros 22 no se borran: siguen en la tabla con `recortado` en verdadero. La lista para leer es la de `in_view` sin `recortado`. En ella quedan varias ediciones de la misma guía: los *Standards of Medical Care in Diabetes* de la ADA de 2011, 2013, 2020, 2022 y 2023, y el consenso ADA y EASD de 2018 y 2022. El equipo abre la más reciente de cada una. Si quedaran menos de 5 en vista, no rellenaríamos la lista: la celda lo diría, y sería un resultado débil.
 
**Comprobar:**



```python
assert (supports["in_view"] & ~supports["recortado"]).sum() == min(supports["in_view"].sum(), MAX_PAPERS)
assert not (supports["recortado"] & ~supports["in_view"]).any()
assert ((supports["prob_texto"] > 0.5) == supports["text_says_read"]).all()
print("Lista recortada: OK")
```

### Paso 3. Guardar el texto
En este paso guardamos `outputs/texto_l4.csv`. La columna `marca` lleva las marcas en los 64 artículos marcados y queda vacía en el resto. `prob_texto` y `recortado` guardan el orden y el corte de la lista.



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



```python
saved = pd.read_csv(text_path)
assert list(saved.columns) == ["title", "keyword", "tfidf_lr", "prob_texto", "codificador", "marca", "supports", "in_view", "recortado"]
assert saved["marca"].notna().sum() == n_flagged(N)
print("texto_l4.csv: OK")
```

### Paso 4. Qué cambiaría la decisión
En este paso escribimos en la tarjeta cómo entra el texto y qué lo cambiaría: otra lista de palabras, otro conjunto marcado (o las marcas del profesor en lugar de los temas de OpenAlex), otra etiqueta de entrenamiento, otro umbral que 0,5 para decir "leer", otro máximo de la lista u otro orden del recorte.



```python
question_card["text_use"] = {
    "how_it_enters": "Un artículo recibe un apoyo si TF-IDF con regresión logística dice leer, con un modelo que no lo vio.",
    "marks": MARKS_SOURCE,
    "reading": "TF-IDF y el codificador no se distinguen con este conjunto marcado: el intervalo de la diferencia incluye el 0.",
    "rule": "Un artículo queda en vista con al menos dos de tres apoyos: patrón (L2), grupo (L3), texto (L4).",
    "reading_list": "Si hay más en vista que el máximo de la tarjeta, se ordena por apoyos, luego por prob_texto y luego por título. El resto queda con recortado = True.",
    "what_changes_it": ["otra lista de palabras", "otro conjunto marcado", "otra etiqueta de entrenamiento", "otro umbral que 0,5", "otro máximo de la lista", "otro orden del recorte"],
}
QUESTION_PATH.write_text(json.dumps(question_card, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(question_card["text_use"], ensure_ascii=False, indent=1))
```

### Paso 5. Comprobación final
En este paso revisamos que el cuaderno dejó todo lo que el cuaderno de grupo y las lecciones siguientes necesitan.



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
    ("Apoyos de la L3", lambda: len(groups_l3) == N),
    ("Un error leído a mano", lambda: "Escriba aquí" not in my_error),
]
passed = sum(_check_ok(n, f) for n, f in checks)
print(f"\nL4_CHECKS={passed}/{len(checks)}")
if passed == len(checks):
    print("L4_OK. Lleve sus tres resultados al sábado. En el cuaderno de grupo hará lo mismo con Wikipedia, en español.")
```



<!-- end NOTEBOOK: -->
