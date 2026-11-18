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

Seguimos con el equipo interno de la secretaría de salud y sus 320 artículos sobre nutrición.
El equipo debe decidir **qué artículos tiene que leer** un colega que llega al equipo.
En la Lección 3 buscamos grupos. Los grupos no miran qué pregunta el equipo.

Hoy **leemos el texto** y decidimos si trata del tema.
Hoy hay modelos que ya leyeron mucho texto antes del nuestro, el preentrenamiento (Devlin et al., 2019).
Una persona marca unos ejemplos **antes** de correr los métodos.

**Tres métodos en este cuaderno.** Cada uno trae la preparación que necesita y el ajuste.
Si un método no da un buen resultado, es normal.
Lo dejamos en la tabla.
CRISP-DM sigue con la evaluación: ahí se decide con qué continúa el equipo.
El archivo de texto lo arma TF-IDF con regresión logística.

| Método | Pregunta | Preparación que necesita | Qué aporta |
|--------|----------|--------------------------|------------|
| Lista de palabras clave | ¿El texto tiene alguna palabra de la lista? | Una lista escrita desde la pregunta, antes de ver resultados | Una referencia: no aprende de etiquetas |
| TF-IDF y regresión logística | ¿Qué palabras pesan a favor y en contra? | Conteos con peso TF-IDF, ajustados solo con las filas de entrenamiento | El archivo de texto, con pesos que se pueden leer |
| Codificador de texto | ¿El resumen entero apunta hacia los ejemplos marcados? | Un vector por resumen, con un modelo ya entrenado y fijo | Un vector del resumen entero |

**Qué hacer.** Ejecute las celdas de arriba hacia abajo.
Cada paso empieza con **En este paso**. Si tiene código, termina con una celda **Comprobar**.

**Mapa del cuaderno**

| Parte | Fase CRISP-DM | Qué sale |
|-------|---------------|----------|
| 1 | Comprensión del negocio | La pregunta de hoy y la lista de palabras clave |
| 2 | Comprensión de los datos | Parámetros, artículos, etiqueta, largo y `outputs/grupos_l3.csv` |
| 3 | Lista de palabras | Conteos de la lista y su predicción |
| 4 | Conjunto marcado | Las filas que los dos métodos que aprenden no ven |
| 5 | TF-IDF | Pesos, ajuste y predicción |
| 6 | Codificador | Un vector por resumen, el corte a 512 tokens y la predicción |
| 7 | Evaluación | Aciertos y errores, cinco pliegues y `outputs/texto_l4.csv` |
| 8 | Despliegue | Hasta 30 artículos para leer, en `outputs/lectura_l4.csv` |

**Carpetas.** La celda de configuración crea `data/` (datos descargados) y `outputs/` (tablas y gráficos).

---

## Parte 1. Comprensión del negocio

### Paso 1. La pregunta de esta lección
En este paso escribimos qué buscamos hoy.
La decisión no cambia: qué artículos debe leer el colega nuevo.

| Pregunta | Respuesta para el laboratorio |
|----------|-------------------------------|
| ¿Qué buscamos? | Qué artículos tratan del tema del equipo, según su resumen |
| ¿Con qué lo medimos? | Una lista de palabras, TF-IDF con regresión logística y un codificador fijo. El archivo guarda TF-IDF |
| ¿Cómo los comparamos? | Con aciertos y errores sobre las marcas, la clase mayoritaria como línea de referencia y cinco pliegues |
| ¿Cómo entra el texto en la lista? | La lista de palabras suma 1 si dice leer. TF-IDF suma su probabilidad. El codificador no entra en la suma |

Un acierto solo tiene sentido frente a una marca escrita antes de ver resultados.

### Paso 2. La pregunta y las palabras clave
En este paso escribimos la lista de palabras clave **desde la pregunta**, antes de ver resultados.
Va en minúsculas, con singular, plural y formas cercanas.
La lista de la Lección 1 tiene entre 10 y 30 artículos.

```python
MIN_PAPERS = 10
MAX_PAPERS = 30
KEYWORDS = {"obesity", "obese", "diet", "diets", "dietary",   # el peso y lo que se come
            "diabetes", "diabetic", "hypertension", "cholesterol"}   # enfermedades que dependen de la dieta
print("Palabras clave:", ", ".join(sorted(KEYWORDS)))
```

**Comprobar:**

En este paso comprobamos que la lista está en minúsculas y tiene las formas de *diet*.

```python
assert MIN_PAPERS < MAX_PAPERS
assert all(w == w.lower() for w in KEYWORDS) and {"diet", "diets"} <= KEYWORDS
print("Palabras clave: OK")
```

---

## Parte 2. Comprensión de los datos

### Paso 1. Librerías y carpetas
En este paso importamos las librerías y creamos las carpetas.
Colab ya trae spaCy y scikit-learn.

```python
import math          # techo (ceil) para los mínimos
import re            # partir el texto en palabras
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import ConfusionMatrixDisplay, accuracy_score, confusion_matrix, f1_score
from sklearn.metrics import precision_recall_fscore_support
from sklearn.model_selection import StratifiedKFold, train_test_split

DATA_DIR = Path("data")         # aquí quedan los datos descargados
OUTPUTS_DIR = Path("outputs")   # aquí quedan las tablas y los gráficos
DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
print(f"scikit-learn {sklearn.__version__}")
```

### Paso 2. Parámetros
En este paso fijamos los parámetros y los tamaños mínimos. No los cambie.

```python
SUPPORT_SHARE = 0.03   # proporción de textos (L2)
SUPPORT_MIN = 5        # mínimo de textos (L2)
SEED = 7               # semilla (L2)

FLAGGED_SHARE = 0.20    # proporción de textos en el conjunto marcado
FLAGGED_MIN = 40        # mínimo de textos marcados
POSITIVE_SHARE = 0.10   # proporción mínima de positivos en la etiqueta
POSITIVES_MIN = 30      # mínimo de positivos
C_REG = 10              # penalización de la regresión logística (más alto, menos penalización)
N_FOLDS = 5             # pliegues de la validación cruzada
ENCODER_NAME = "intfloat/multilingual-e5-small"
MAX_TOKENS = 512        # el codificador corta el resumen a partir de este largo


def n_flagged(n: int) -> int:
    """Tamaño del conjunto marcado: max(FLAGGED_MIN, ceil(FLAGGED_SHARE * n)).

    Entrada: n, el número de textos.
    Salida: cuántos textos se apartan para marcar.
    """
    return max(FLAGGED_MIN, math.ceil(FLAGGED_SHARE * n))   # el mayor entre 40 y el 20%


def min_positives(n: int) -> int:
    """Positivos que necesita una etiqueta de entrenamiento: max(POSITIVES_MIN, ceil(POSITIVE_SHARE * n)).

    Entrada: n, el número de textos.
    Salida: el mínimo de textos con etiqueta 1.
    """
    return max(POSITIVES_MIN, math.ceil(POSITIVE_SHARE * n))   # el mayor entre 30 y el 10%


print(f"Con 317 artículos: {n_flagged(317)} marcados, al menos {min_positives(317)} positivos")
```

**Comprobar:**

En este paso comprobamos el tamaño del conjunto marcado, el mínimo de positivos y la versión de scikit-learn.

```python
assert n_flagged(317) == 64 and min_positives(317) == 32
major, minor = sklearn.__version__.split(".")[:2]
assert (int(major), int(minor)) >= (1, 3)
print("Parámetros: OK")
```

### Paso 3. Las palabras útiles
En este paso traemos sin cambios las palabras vacías, `words` y `word_list` de las Lecciones 2 y 3.

```python
from spacy.lang.en.stop_words import STOP_WORDS as STOP_WORDS_EN

WORD_RE = re.compile(r"[^\W\d_]+")   # secuencias de letras
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
    """Convierte un texto en la lista de sus palabras útiles, con repeticiones (la función de la L3).

    Qué hace: pasa a minúsculas, quita "[cita requerida]", separa en palabras de letras
    y descarta las de menos de 3 letras y las palabras vacías.
    Entrada: text y stop_words.
    Salida: una lista de palabras, en orden y con cada aparición.
    Por qué: TF-IDF cuenta cuántas veces usa un texto cada palabra.
    """
    text = (text or "").lower().replace("[cita requerida]", " ")  # minúsculas, sin la marca de Wikipedia
    useful = []
    for word in WORD_RE.findall(text):  # por cada palabra de solo letras
        long_enough = len(word) >= 3
        is_stop = word in stop_words  # una palabra vacía
        if long_enough and not is_stop:
            useful.append(word)
    return useful


def words(text: str, stop_words: set[str]) -> set[str]:
    """Convierte un texto en el conjunto de sus palabras útiles (la función de la L2).

    Qué hace: la misma limpieza que word_list, con cada palabra una sola vez.
    Entrada: text y stop_words.
    Salida: un set de palabras.
    Por qué: la lista de palabras clave solo pregunta si una palabra está en el texto.
    """
    return set(word_list(text, stop_words))  # la lista sin repeticiones


def keep_tokens(tokens: list[str]) -> list[str]:
    """Devuelve la lista tal cual. TfidfVectorizer la usa como analizador: las palabras ya vienen limpias."""
    return tokens  # sin cambios: word_list ya limpió el texto


print(sorted(words("The diet and the DIET of obese children", STOP_WORDS)))
```

**Comprobar:**

En este paso comprobamos que `word_list` cuenta las repeticiones.

```python
assert word_list("The diet, the DIET and the risk", STOP_WORDS) == ["diet", "diet", "risk"]
print("Funciones de la L2 y la L3: OK")
```

### Paso 4. Los artículos con resumen útil
En este paso cargamos los artículos, con la descarga de la Lección 2, y dejamos fuera los resúmenes con menos de 5 palabras útiles.

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
useful = []
for abstract in papers["abstract"]:   # por cada resumen
    useful.append(len(words(abstract, STOP_WORDS)) >= 5)   # al menos 5 palabras útiles
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

### Paso 5. La etiqueta de entrenamiento
En este paso armamos la **etiqueta de entrenamiento** desde los temas de OpenAlex (`topics`).
Vale 1 si un tema menciona obesidad, dieta, nutrición, diabetes, salud cardiovascular, lipoproteínas, presión arterial o hipertensión.
Es una etiqueta **dada, no encontrada**. Por eso medimos contra las marcas.

```python
TARGET_TOPICS = ["obesity", "diet", "nutrition", "nutritional",   # el peso y lo que se come
                 "diabetes", "cardiovascular", "lipoproteins", "blood pressure", "hypertension"]   # enfermedades ligadas a la dieta

y = np.zeros(N, dtype=int)
for i, topics in enumerate(papers["topics"]):   # por cada artículo
    for topic in TARGET_TOPICS:
        if topic in topics.lower():   # menciona un tema del equipo
            y[i] = 1
print(f"Artículos del tema según OpenAlex: {y.sum()} de {N} ({y.mean():.0%}). Mínimo pedido: {min_positives(N)}")
```

**Comprobar:**

En este paso comprobamos el número de artículos del tema y que llega al mínimo de positivos.

```python
assert y.sum() == 96 and y.sum() >= min_positives(N)
print("Etiqueta: OK")
```

### Paso 6. El largo de los resúmenes
En este paso contamos las palabras de cada resumen.
Con textos cortos y pocos ejemplos, un modelo simple sobre palabras suele bastar.

```python
word_counts = []
for text in texts:
    word_counts.append(len(text.split()))   # palabras por resumen
lengths = pd.Series(word_counts)
print(f"Palabras por resumen: mediana {lengths.median():.0f}, máximo {lengths.max():,}")
```

**Comprobar:**

En este paso comprobamos que hay un largo por resumen.

```python
assert len(lengths) == N and lengths.min() > 0
print("Largo: OK")
```

### Paso 7. Los grupos de la Lección 3
En este paso leemos `outputs/grupos_l3.csv`, con los grupos leídos de la Lección 3.
Si no está, la parte de los grupos queda en 0. Suba el archivo a `outputs/`.

```python
GROUPS_PATH = OUTPUTS_DIR / "grupos_l3.csv"
GROUP_COLUMNS = ["title", "kmeans_parte", "hdbscan_parte"]
if GROUPS_PATH.is_file():
    groups_l3 = pd.read_csv(GROUPS_PATH, keep_default_na=False)
    print(f"grupos_l3.csv: {len(groups_l3)} artículos")
else:
    groups_l3 = pd.DataFrame({"title": papers["title"], "kmeans_parte": 0.0, "hdbscan_parte": 0.0})
    print("No encontramos outputs/grupos_l3.csv. Sin él, la parte de los grupos queda en 0.")
```

**Comprobar:**

En este paso comprobamos que la tabla de la Lección 3 tiene la parte de los dos métodos.

```python
assert set(GROUP_COLUMNS) <= set(groups_l3.columns)
print("Grupos de la L3: OK")
```

---

## Parte 3. Lista de palabras

### Paso 1. Las palabras clave en los resúmenes
En este paso contamos en cuántos resúmenes aparece cada palabra clave.
También contamos cuántos de ellos están fuera del tema según OpenAlex.

```python
word_sets = []
for text in texts:
    word_sets.append(words(text, STOP_WORDS))   # las palabras útiles de cada resumen
for word in sorted(KEYWORDS):   # por cada palabra clave
    with_word, off_topic = 0, 0
    for i, word_set in enumerate(word_sets):
        if word in word_set:
            with_word += 1
            off_topic += int(y[i] == 0)   # un resumen fuera del tema que la tiene
    print(f"{word:13s} en {with_word:2d} resúmenes, {off_topic:2d} fuera del tema")
```

Mire cuántos resúmenes fuera del tema trae cada palabra.
Una lista más larga encuentra más y también se equivoca más.
Si se equivoca, es normal.
Esa cuenta se queda en la pantalla.
La lista igual sirve de referencia porque no aprende.

**Comprobar:**

En este paso comprobamos que hay un conjunto de palabras por resumen.

```python
assert len(word_sets) == N
print("Palabras clave en los resúmenes: OK")
```

### Paso 2. La predicción de la lista
En este paso aplicamos la lista: 1 si el resumen tiene alguna palabra clave, 0 si no.
No aprende nada, así que vale para todos los artículos.

```python
pred_keywords = np.zeros(N, dtype=int)
for i, word_set in enumerate(word_sets):
    pred_keywords[i] = int(bool(word_set & KEYWORDS))
print(f"La lista dice sí en {pred_keywords.sum()} de {N} artículos")
```

**Comprobar:**

En este paso comprobamos que la lista da un 0 o un 1 por artículo.

```python
assert len(pred_keywords) == N and set(np.unique(pred_keywords)) <= {0, 1}
print("Lista de palabras clave: OK")
```

---

## Parte 4. El conjunto marcado

La lista no aprende.
Los dos métodos que siguen sí aprenden.
Por eso apartamos unas filas que no pueden ver.

En este paso separamos el **conjunto marcado**: `n_flagged(N)` artículos, 64 aquí.
Los métodos que aprenden no ven estas filas.
Los otros 253 son las filas de entrenamiento.
Si `marcas-nutricion-l4.csv` está publicado, usamos las marcas del profesor. Si no, la etiqueta.

```python
rows = np.arange(N)
train_rows, marked_rows = train_test_split(rows, test_size=n_flagged(N), stratify=y, random_state=SEED)
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
    print(f"No usamos {MARKS_FILE} ({type(error).__name__}).")
print(f"Entrenamiento: {len(train_rows)} filas, {y_train.sum()} del tema")
print(f"Marcados: {len(marked_rows)} filas, {y_test.sum()} del tema. Marcas: {MARKS_SOURCE}")
```

**Comprobar:**

En este paso comprobamos el tamaño de las dos partes, que no comparten filas y que las marcas son 0 o 1.

```python
assert len(train_rows) == 253 and len(marked_rows) == n_flagged(N)
assert not set(train_rows) & set(marked_rows)
assert set(np.unique(y_test)) <= {0, 1}
print("Conjunto marcado: OK")
```

---

## Parte 5. TF-IDF

### Paso 1. Los pesos TF-IDF
En este paso pesamos las palabras con **TF-IDF**.
Pesa más una palabra que se repite en un texto y aparece en pocos textos.

$\displaystyle \text{tf} = 1 + \log(\text{conteo}) \qquad \text{idf} = \log\frac{1 + N}{1 + \text{df}} + 1$

`fit_transform` aprende solo de las 253 filas de entrenamiento. Las marcadas solo se transforman.

```python
token_lists = []
for text in texts:
    token_lists.append(word_list(text, STOP_WORDS))   # una lista de palabras por texto, con repeticiones
train_tokens, marked_tokens = [], []
for i in train_rows:
    train_tokens.append(token_lists[i])
for i in marked_rows:
    marked_tokens.append(token_lists[i])   # los textos marcados, apartados
tfidf = TfidfVectorizer(analyzer=keep_tokens, sublinear_tf=True)   # tf = 1 + log(conteo)
X_train = tfidf.fit_transform(train_tokens)     # ajustado solo con las filas de entrenamiento
X_marked = tfidf.transform(marked_tokens)
feature_names = tfidf.get_feature_names_out()
print(f"Entrenamiento: {X_train.shape}. Marcados: {X_marked.shape}")
```

**Comprobar:**

En este paso comprobamos el número de filas de TF-IDF y que cada fila quedó de largo 1.

```python
assert X_train.shape[0] == 253 and X_marked.shape[1] == X_train.shape[1]
assert np.allclose(np.sqrt(X_train.multiply(X_train).sum(axis=1)), 1)
print("TF-IDF: OK")
```

---

Ya tenemos un peso por palabra.
Ahora un modelo aprende qué pesos empujan hacia sí.

### Paso 2. El ajuste
En este paso entrenamos una **regresión logística**, que da un peso a cada palabra.

$\displaystyle P(y = 1 \mid x) = \frac{1}{1 + e^{-(w \cdot x + b)}}$

`class_weight="balanced"` pesa más la clase menor. Dice 1 si la probabilidad pasa de 0,5.

```python
tfidf_model = LogisticRegression(class_weight="balanced", C=C_REG, max_iter=1000)
tfidf_model.fit(X_train, y_train)
pred_tfidf = tfidf_model.predict(X_marked)
print(f"TF-IDF dice sí en {pred_tfidf.sum()} de {len(marked_rows)} marcados")
```

**Comprobar:**

En este paso comprobamos que TF-IDF da un 0 o un 1 por artículo marcado.

```python
assert len(pred_tfidf) == n_flagged(N) and set(np.unique(pred_tfidf)) <= {0, 1}
print("TF-IDF con regresión logística: OK")
```

### Leer los pesos
En este paso leemos las palabras de más peso, a favor y en contra.

```python
weights = pd.Series(tfidf_model.coef_[0], index=feature_names)
pd.DataFrame({"a favor": weights.nlargest(10).index, "en contra": weights.nsmallest(10).index})
```

Mire las diez palabras a favor y las diez en contra.
Esas palabras son lo que el modelo aprendió de la etiqueta.
Si el tema no aparece entre las de más peso, el resultado es pobre y es normal.
Lo dejamos en la tabla.
El archivo guarda esta predicción porque esos pesos se pueden leer.

---

## Parte 6. Codificador de texto

El codificador ya fue entrenado en otro lado y aquí no se mueve.
Lee el resumen entero.
Cada token depende de los demás.
El modelo entrega un vector por resumen.

### Paso 1. La librería
En este paso importamos la librería.
Si falta, la instalamos.

```python
try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "sentence-transformers"])
    from sentence_transformers import SentenceTransformer
```

**Comprobar:**

En este paso comprobamos que la clase quedó importada.

```python
assert SentenceTransformer is not None
print("Librería del codificador: OK")
```

### Paso 2. El modelo
En este paso descargamos el modelo.
Pesa unos 470 MB y puede tardar un par de minutos.
Aquí no se vuelve a entrenar.

```python
encoder = SentenceTransformer(ENCODER_NAME)
```

**Comprobar:**

En este paso comprobamos que el modelo cargó.

```python
assert encoder is not None
print("Modelo: OK")
```

### Paso 3. Un vector por resumen
En este paso contamos los resúmenes de más de 512 tokens y dejamos que el modelo los corte.
Cada resumen empieza con `passage:` porque así pide usarse este modelo.

```python
n_cut = 0
passages = []
for text in texts:
    n_tokens = len(encoder.tokenizer.encode(text, add_special_tokens=False))
    if n_tokens > MAX_TOKENS:
        n_cut += 1
    passages.append("passage: " + text)
print(f"Resúmenes de más de {MAX_TOKENS} tokens: {n_cut} de {N}")
vectors = encoder.encode(passages, normalize_embeddings=True, show_progress_bar=False)
print(f"Vectores: {vectors.shape}")
```

Mire cuántos resúmenes superan los 512 tokens.
Eso es lo que este modelo no alcanza a leer.
Si el corte es grande, es normal.
Lo dejamos en la pantalla.

**Comprobar:**

En este paso comprobamos que hay un vector por resumen y que el corte no pasa del total.

```python
assert vectors.shape[0] == N
assert n_cut <= N
print("Codificador: OK")
```

### Paso 4. La regresión sobre los vectores
En este paso aprendemos con las mismas filas de entrenamiento.
El codificador no se vuelve a ajustar.

```python
encoder_model = LogisticRegression(class_weight="balanced", C=C_REG, max_iter=1000)
encoder_model.fit(vectors[train_rows], y_train)
pred_encoder = encoder_model.predict(vectors[marked_rows])
tfidf_hits = int((pred_tfidf == y_test).sum())
encoder_hits = int((pred_encoder == y_test).sum())
print(f"Aciertos en los marcados. TF-IDF: {tfidf_hits}. Codificador: {encoder_hits}")
```

Mire los aciertos del codificador al lado de los de TF-IDF.
Si acierta menos, es normal.
Lo dejamos en la tabla.
La probabilidad que guardamos es la de TF-IDF, porque sus pesos se pueden leer.

**Comprobar:**

En este paso comprobamos que hay una predicción por artículo marcado.

```python
assert len(pred_encoder) == n_flagged(N)
assert set(np.unique(pred_encoder)) <= {0, 1}
print("Codificador con regresión logística: OK")
```

---

## Parte 7. Evaluación

La evaluación compara los tres métodos sobre los mismos textos marcados.
Contamos aciertos y errores en el conjunto marcado, que los métodos que aprenden no vieron.
La clase mayoritaria da a todos la marca más frecuente.
Es la línea de referencia: un método útil debería superarla.
Los cinco pliegues muestran el F1 más bajo y el más alto.
Si están lejos, un solo número no basta para confiar en el método.
Si un método acierta poco, es normal.
Su fila sigue en la tabla.

### Paso 1. Aciertos y errores en el conjunto marcado
En este paso contamos TP, FP, FN y TN de cada método sobre los 64 marcados.
**Precisión** es TP / (TP + FP). **Exhaustividad** es TP / (TP + FN).
**F1** es la media armónica de las dos.

```python
def counts_of(marks: np.ndarray, pred: np.ndarray) -> dict:
    """Los cuatro conteos y las cuatro medidas de un método frente a las marcas.

    Qué hace: cruza cada marca con lo que dice el método y cuenta los cuatro casos.
    Con esos conteos calcula precisión, exhaustividad, F1 y exactitud.
    Entrada: marks, las marcas (0 o 1), y pred, lo que dice el método (0 o 1).
    Salida: un diccionario con TP, FP, FN, TN y las cuatro medidas.
    """
    tn, fp, fn, tp = confusion_matrix(marks, pred, labels=[0, 1]).ravel()  # los cuatro casos
    p, r, f1, _ = precision_recall_fscore_support(marks, pred, average="binary", zero_division=0)
    accuracy = accuracy_score(marks, pred)
    return {"TP": tp, "FP": fp, "FN": fn, "TN": tn, "precision": p, "recall": r, "F1": f1, "accuracy": accuracy}


majority_mark = int(y_test.mean() > 0.5)   # la marca más frecuente
predictions = {
    "clase mayoritaria": np.full(len(marked_rows), majority_mark),
    "palabras clave": pred_keywords[marked_rows],
    "TF-IDF": pred_tfidf,
    "codificador": pred_encoder,
}
rows_by_method = {}
for name, pred in predictions.items():   # una fila por método
    rows_by_method[name] = counts_of(y_test, pred)
results = pd.DataFrame(rows_by_method).T
results[["TP", "FP", "FN", "TN"]] = results[["TP", "FP", "FN", "TN"]].astype(int)
print(f"Marcas: {MARKS_SOURCE}")
results.round(2)
```

La clase mayoritaria da a todos la respuesta más común.
Mire los aciertos de esta corrida.
Si un método acierta poco, es normal.
Su fila sigue en la tabla.

**Comprobar:**

En este paso comprobamos que los cuatro casos suman los marcados.

```python
assert (results[["TP", "FP", "FN", "TN"]].sum(axis=1) == n_flagged(N)).all()
assert len(results) == 4
print("Aciertos y errores: OK")
```

### Paso 2. Las matrices de confusión
En este paso dibujamos la **matriz de confusión** de cada método.

```python
fig, axes = plt.subplots(1, 3, figsize=(11, 3.4))
for ax, name in zip(axes, ["palabras clave", "TF-IDF", "codificador"]):
    ConfusionMatrixDisplay.from_predictions(y_test, predictions[name], labels=[0, 1], display_labels=["no leer", "leer"],
                                            cmap="Blues", colorbar=False, ax=ax)
    ax.set_title(name)
    ax.set_xlabel("Dice el método")
    ax.set_ylabel("Marca")
fig.tight_layout()
fig.savefig(OUTPUTS_DIR / "confusion_l4.png", dpi=120)
plt.show()
```

### Paso 3. Cinco pliegues en las filas de entrenamiento
En este paso partimos las 253 filas de entrenamiento en 5 pliegues.
En cada pliegue ajustamos TF-IDF, ajustamos el codificador y anotamos el F1 de los tres métodos.
Guardamos el F1 más bajo y el más alto.

```python
folds = StratifiedKFold(n_splits=N_FOLDS, shuffle=True, random_state=SEED)
fold_f1 = {"palabras clave": [], "TF-IDF": [], "codificador": []}
for fit_rows, test_rows in folds.split(train_rows, y_train):
    learn, check = train_rows[fit_rows], train_rows[test_rows]
    learn_tokens, check_tokens = [], []
    for i in learn:
        learn_tokens.append(token_lists[i])
    for i in check:
        check_tokens.append(token_lists[i])
    fold_vectorizer = TfidfVectorizer(analyzer=keep_tokens, sublinear_tf=True)
    fold_vectorizer.fit(learn_tokens)
    learn_matrix = fold_vectorizer.transform(learn_tokens)
    check_matrix = fold_vectorizer.transform(check_tokens)
    fold_tfidf = LogisticRegression(class_weight="balanced", C=C_REG, max_iter=1000)
    fold_tfidf.fit(learn_matrix, y[learn])
    fold_pred = fold_tfidf.predict(check_matrix)
    fold_encoder = LogisticRegression(class_weight="balanced", C=C_REG, max_iter=1000)
    fold_encoder.fit(vectors[learn], y[learn])
    encoder_pred = fold_encoder.predict(vectors[check])
    fold_f1["palabras clave"].append(f1_score(y[check], pred_keywords[check], zero_division=0))
    fold_f1["TF-IDF"].append(f1_score(y[check], fold_pred, zero_division=0))
    fold_f1["codificador"].append(f1_score(y[check], encoder_pred, zero_division=0))
cv_rows = {}
for name, values in fold_f1.items():
    cv_rows[name] = {"F1 más bajo": min(values), "F1 más alto": max(values)}
cv_table = pd.DataFrame(cv_rows).T.round(2)
cv_table
```

Mire el F1 más bajo y el más alto de cada método.
Si están lejos, con pocas marcas un solo F1 no basta.

**Comprobar:**

En este paso comprobamos que hay cinco F1 por método.

```python
for values in fold_f1.values():
    assert len(values) == N_FOLDS
assert (cv_table["F1 más bajo"] <= cv_table["F1 más alto"]).all()
print("Cinco pliegues: OK")
```

### Paso 4. La clase mayoritaria como referencia
En este paso comparamos cada método con la fila de la clase mayoritaria de la tabla del Paso 1.
Mire también el F1 más bajo y el más alto.
Si un método queda por debajo, es normal.
Su fila sigue en la tabla.
El archivo guarda TF-IDF porque sus pesos se pueden leer.

¿Qué métodos superan a la clase mayoritaria?
¿Están de acuerdo con guardar TF-IDF?
Usen la tabla de aciertos y los cinco pliegues.

**ESCRIBA SU TEXTO AQUÍ**

### Paso 5. Leer tres errores por método
En este paso leemos tres errores de cada método. Un error puede ser del método o de la marca.

```python
for name in ["palabras clave", "TF-IDF", "codificador"]:
    wrong = []
    for i in range(len(y_test)):
        if y_test[i] != predictions[name][i] and len(wrong) < 3:   # los tres primeros errores
            wrong.append(i)
    print(f"\n{name}:")
    for i in wrong:
        kind = "FP (dice leer)" if predictions[name][i] == 1 else "FN (dice no leer)"
        print(f"  {kind}: {papers.loc[marked_rows[i], 'title'][:90]}")
```

### Paso 6. El texto para toda la colección
En este paso repetimos el mismo corte.
Esta vez guardamos la probabilidad, no solo el sí o el no.
Los marcados usan el modelo ya ajustado.
Cada fila de entrenamiento usa el pliegue que no la vio.

```python
prob_texto = np.zeros(N)
prob_texto[marked_rows] = tfidf_model.predict_proba(X_marked)[:, 1]
for fit_rows, test_rows in folds.split(train_rows, y_train):
    learn, check = train_rows[fit_rows], train_rows[test_rows]
    learn_tokens, check_tokens = [], []
    for i in learn:
        learn_tokens.append(token_lists[i])
    for i in check:
        check_tokens.append(token_lists[i])
    fold_vectorizer = TfidfVectorizer(analyzer=keep_tokens, sublinear_tf=True)
    fold_vectorizer.fit(learn_tokens)
    fold_model = LogisticRegression(class_weight="balanced", C=C_REG, max_iter=1000)
    fold_model.fit(fold_vectorizer.transform(learn_tokens), y[learn])
    fold_prob = fold_model.predict_proba(fold_vectorizer.transform(check_tokens))[:, 1]
    prob_texto[check] = fold_prob
text_tfidf = (prob_texto > 0.5).astype(int)
print(f"Dicen leer: palabras clave {pred_keywords.sum()}, TF-IDF {text_tfidf.sum()}")
```

**Comprobar:**

En este paso comprobamos que `prob_texto` coincide con la predicción de TF-IDF.

```python
assert ((prob_texto > 0.5) == text_tfidf).all()
print("Texto para toda la colección: OK")
```

### Paso 7. Guardar el texto
En este paso guardamos `outputs/texto_l4.csv`, una fila por artículo.
`marca` lleva las 64 marcas. Las demás filas quedan vacías.

```python
marca = pd.Series(pd.NA, index=range(N), dtype="Int64")
marca[marked_rows] = y_test
text_table = pd.DataFrame({
    "title": papers["title"],
    "keyword": pred_keywords,
    "tfidf_lr": text_tfidf,
    "prob_texto": prob_texto,
    "marca": marca,
})
text_path = OUTPUTS_DIR / "texto_l4.csv"
text_table.to_csv(text_path, index=False)
print(f"Guardado: {text_path} ({len(text_table)} filas, {text_table['marca'].notna().sum()} marcadas)")
```

**Comprobar:**

En este paso comprobamos las columnas del archivo y las marcas guardadas.

```python
saved = pd.read_csv(text_path)
assert {"title", "keyword", "tfidf_lr", "prob_texto", "marca"} <= set(saved.columns)
assert saved["marca"].notna().sum() == n_flagged(N)
print("texto_l4.csv: OK")
```

---

## Parte 8. Despliegue

### Paso 1. Qué hace el texto con la lista
En este paso decimos para qué sirve el texto.
La lista de palabras suma 1 si dice leer.
TF-IDF suma su probabilidad, de 0 a 1.
Los grupos de la Lección 3 suman la parte con palabras del tema de su grupo leído, de 0 a 2.
El codificador no entra en la suma.

### Paso 2. Artículos para leer
En este paso juntamos los grupos de la Lección 3 y el texto de hoy.
La evidencia va de 0 a 4.
Hasta 2 vienen de los grupos de la Lección 3.
1 viene de la lista de palabras.
Hasta 1 viene de TF-IDF.
Ordenamos por evidencia, después por `prob_texto` y al final por título.
Mostramos como máximo 30 artículos.

```python
assert groups_l3["title"].tolist() == papers["title"].tolist()   # la L3 guarda los artículos en el mismo orden
reading_rows = []
for i in range(N):   # por cada artículo
    row = {"title": papers.loc[i, "title"],
           "kmeans": float(groups_l3.loc[i, "kmeans_parte"]),     # la parte de su grupo leído de k-means
           "hdbscan": float(groups_l3.loc[i, "hdbscan_parte"]),   # la parte de su grupo leído de HDBSCAN
           "palabras_clave": int(pred_keywords[i]),               # 1 si tiene una palabra clave
           "tfidf": round(prob_texto[i], 2)}                      # la probabilidad de TF-IDF
    row["grupos"] = round(row["kmeans"] + row["hdbscan"], 2)
    row["texto"] = round(row["palabras_clave"] + row["tfidf"], 2)
    row["evidencia"] = round(row["grupos"] + row["texto"], 2)
    row["prob_texto"] = round(prob_texto[i], 3)
    reading_rows.append(row)

reading = pd.DataFrame(reading_rows).sort_values(["evidencia", "prob_texto", "title"], ascending=[False, False, True])
reading_list = reading.head(MAX_PAPERS)   # como máximo 30 artículos
reading_path = OUTPUTS_DIR / "lectura_l4.csv"
reading_list.to_csv(reading_path, index=False)
print(f"Artículos: {len(reading)}. En la lista: {len(reading_list)}.")
top, bottom = reading_list["evidencia"].max(), reading_list["evidencia"].min()
print(f"Evidencia en la lista: de {top} a {bottom}, {reading_list['evidencia'].nunique()} valores distintos")
reading_list.head(10)
```

Mire cuántos artículos tienen evidencia y cuántos entran en la lista.
Mire también el máximo y el mínimo de evidencia que imprimió la celda.
Si hay varias ediciones de la misma guía, el equipo abre la más reciente.

**Comprobar:**

En este paso comprobamos el largo de la lista, su orden y que la evidencia es la suma de grupos y texto.

```python
assert len(reading_list) == min(MAX_PAPERS, len(reading)) and reading_list["evidencia"].is_monotonic_decreasing
assert ((reading_list["evidencia"] - reading_list["grupos"] - reading_list["texto"]).abs() < 0.011).all()
assert reading_list["evidencia"].between(0, 4).all()
print("Lista de lectura: OK")
```

### Paso 3. Comprobación final
En este paso revisamos que el cuaderno dejó lo que la Lección 5 necesita.

```python
checks = {
    "outputs/texto_l4.csv": text_path.is_file(),
    "outputs/lectura_l4.csv": reading_path.is_file(),
    "Matrices de confusión": (OUTPUTS_DIR / "confusion_l4.png").is_file(),
    "Grupos de la L3": GROUPS_PATH.is_file(),
}
for name, ok in checks.items():
    print(f"{name}: {'OK' if ok else 'incompleto'}")
passed = sum(checks.values())
print(f"\nL4_CHECKS={passed}/{len(checks)}")
if passed == len(checks):
    print("L4_OK. Siga con la Lección 5.")
```

<!-- end NOTEBOOK: -->
