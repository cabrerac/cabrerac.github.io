<!-- NOTEBOOK: -->

## Repaso de Python para este cuaderno

Este cuaderno utiliza los siguientes métodos de Python. Si ya los conoce, ejecute estas celdas rápido.

### Separar filas para probar
Para saber si un método funciona, lo probamos con filas que no vio al ajustarse.
`train_test_split` aparta esas filas.
`stratify` conserva en cada parte la proporción de unos.
En el ejemplo hay 10 filas y apartamos 5.
`random_state=7` fija el corte para que se repita igual.

```python
import numpy as np
from sklearn.model_selection import train_test_split

y_toy = np.array([1, 1, 0, 0, 0, 0, 0, 0, 1, 0])  # np.array arma 10 marcas de juguete
rows_train, rows_test = train_test_split(np.arange(10), test_size=5, stratify=y_toy, random_state=7)  # train_test_split aparta 5 filas y stratify conserva la proporción de unos
print("Para aprender:", rows_train, "Para probar:", rows_test)
print("Proporción de 1 en cada parte:", y_toy[rows_train].mean(), y_toy[rows_test].mean())
```

### Aciertos y errores a mano
Una marca es 1 cuando una persona dice que el artículo se lee, y 0 cuando dice que no.
El método también dice 1 o 0.
TP cuenta los dos sí.
FP cuenta un sí del método con un no de la marca.
FN cuenta un no del método con un sí de la marca.
TN cuenta los dos no.
En el ejemplo hay 6 filas.

```python
marked = np.array([1, 0, 1, 1, 0, 0])  # np.array arma las 6 marcas
said = np.array([1, 1, 0, 1, 0, 0])  # np.array arma lo que diría el método
tp = int(((said == 1) & (marked == 1)).sum())  # contamos los casos en que el método y la marca dicen 1
fp = int(((said == 1) & (marked == 0)).sum())  # contamos un sí del método con un no de la marca
fn = int(((said == 0) & (marked == 1)).sum())  # contamos un no del método con un sí de la marca
tn = int(((said == 0) & (marked == 0)).sum())  # contamos los casos en que el método y la marca dicen 0
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

**Tres métodos en este cuaderno.** Para cada uno llevaremos a cabo la preparación de los datos y su modelado.
Si un método no da un buen resultado, lo debemos documentar como un resultado útil.
CRISP-DM sigue con la evaluación para decidir cuáles métodos se deben utilizar.
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
| 2 | Comprensión de los datos | Parámetros, artículos, etiqueta y largo |
| 3 | Lista de palabras | Conteos de la lista y su predicción |
| 4 | Conjunto marcado | Las filas que los dos métodos que aprenden no ven |
| 5 | TF-IDF | Pesos, ajuste y predicción |
| 6 | Codificador | Un vector por resumen, el corte a 512 tokens y la predicción |
| 7 | Evaluación | Exactitud, matrices de confusión y `outputs/texto_l4.csv` |
| 8 | Despliegue | Dos listas de hasta 30 artículos: `outputs/lectura_l4.csv` y `outputs/lectura_encoder_l4.csv` |

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
| ¿Cómo los comparamos? | Con la exactitud y la matriz de confusión sobre las marcas, y la clase mayoritaria como línea de referencia |
| ¿Cómo entra el texto en la lista? | La lista que guardamos suma la lista de palabras y la probabilidad de TF-IDF. El codificador arma una segunda lista, solo con su probabilidad |

Un acierto solo tiene sentido frente a una marca escrita antes de ver resultados.

### Paso 2. La pregunta y las palabras clave
Antes de ver los resultados escribimos las palabras clave desde la pregunta: obesity, diet, diabetes y las formas cercanas.
Van en minúsculas, con singular y plural, porque el resumen puede usar cualquiera de las dos.
No hay un tope para esa lista.
La lista de lectura sí tiene un tope: entre 10 y 30 artículos, `MIN_PAPERS` y `MAX_PAPERS`.

```python
MIN_PAPERS = 10
MAX_PAPERS = 30
KEYWORDS = {"obesity", "obese", "diet", "diets", "dietary",   # agregamos las palabras del peso y de la comida a la lista
            "diabetes", "diabetic", "hypertension", "cholesterol"}   # agregamos las palabras de las enfermedades a la lista
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
import math          # math.ceil redondea hacia arriba los mínimos
import re            # re permite definir la expresión regular que filtra las palabras
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer  # TfidfVectorizer pesa cada palabra por su repetición y por lo rara que es
from sklearn.linear_model import LogisticRegression  # LogisticRegression aprende un peso por columna y devuelve una probabilidad
from sklearn.metrics import ConfusionMatrixDisplay, accuracy_score, confusion_matrix  # estas funciones cuentan aciertos y errores frente a las marcas
from sklearn.model_selection import StratifiedKFold, train_test_split  # train_test_split aparta filas y StratifiedKFold parte las filas de entrenamiento

DATA_DIR = Path("data")         # Path fija la carpeta donde se guardan los datos descargados
OUTPUTS_DIR = Path("outputs")   # Path fija la carpeta donde se guardan las tablas y los gráficos
DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
print(f"scikit-learn {sklearn.__version__}")
```

### Paso 2. Parámetros
Fijamos los valores que el resto del cuaderno va a usar.
Elegirlos es una optimización, y esa optimización queda fuera de este curso.
En este cuaderno usamos estos valores fijos.
Con 317 artículos apartamos 64 para marcar, el mayor entre 40 y el 20%.
La etiqueta del tema debe cubrir al menos 32, el mayor entre 30 y el 10%.

```python
SUPPORT_SHARE = 0.03   # fija la proporción de artículos que una palabra debe alcanzar
SUPPORT_MIN = 5        # fija el mínimo de artículos que una palabra debe alcanzar
SEED = 7               # fija el arranque aleatorio para que los cortes se repitan igual

FLAGGED_SHARE = 0.20    # fija la proporción de artículos que apartamos para marcar
FLAGGED_MIN = 40        # fija el mínimo de artículos marcados
POSITIVE_SHARE = 0.10   # fija la proporción mínima de artículos del tema
POSITIVES_MIN = 30      # fija el mínimo de artículos del tema
C_REG = 10              # fija la penalización de la regresión logística
N_FOLDS = 5             # fija en cuántas partes partimos las filas de entrenamiento para escribir una probabilidad por fila
ENCODER_NAME = "intfloat/multilingual-e5-small"  # fija el modelo ya entrenado que convierte cada resumen en un vector
MAX_TOKENS = 512        # fija el largo a partir del cual el codificador corta el resumen


def n_flagged(n: int) -> int:
    """Tamaño del conjunto marcado: max(FLAGGED_MIN, ceil(FLAGGED_SHARE * n)).

    Entrada: n, el número de textos.
    Salida: cuántos textos se apartan para marcar.
    """
    return max(FLAGGED_MIN, math.ceil(FLAGGED_SHARE * n))   # max elige el mayor entre 40 y el 20% redondeado hacia arriba


def min_positives(n: int) -> int:
    """Positivos que necesita una etiqueta de entrenamiento: max(POSITIVES_MIN, ceil(POSITIVE_SHARE * n)).

    Entrada: n, el número de textos.
    Salida: el mínimo de textos con etiqueta 1.
    """
    return max(POSITIVES_MIN, math.ceil(POSITIVE_SHARE * n))   # max elige el mayor entre 30 y el 10% redondeado hacia arriba


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
Un resumen trae palabras que no dicen el tema, como "the", "of", la etiqueta "methods" o el resto "http".
Esas palabras aparecen en muchos resúmenes y no separan el tema.
En este paso las quitamos, con las mismas funciones de las Lecciones 2 y 3.
`word_list` conserva cada aparición, porque TF-IDF cuenta cuántas veces aparece la palabra.
`words` deja cada palabra una sola vez, porque la lista de palabras clave solo pregunta si está.

```python
from spacy.lang.en.stop_words import STOP_WORDS as STOP_WORDS_EN

WORD_RE = re.compile(r"[^\W\d_]+")   # re permite configurar una expresión regular para filtrar secuencias de letras
ABSTRACT_LABELS = {
    "background", "methods", "findings", "interpretation", "funding",
    "conclusions", "results", "objective", "objectives", "aims",
    "bill", "melinda", "gates", "foundation",
}
URL_TOKENS = {"http", "https", "www", "org"}
STOP_WORDS = set(STOP_WORDS_EN) | ABSTRACT_LABELS | URL_TOKENS   # unimos las palabras vacías, las etiquetas del resumen y los restos de direcciones
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
    text = (text or "").lower().replace("[cita requerida]", " ")  # lower pasa el texto a minúsculas y replace quita la marca de Wikipedia
    useful = []
    for word in WORD_RE.findall(text):  # findall extrae cada secuencia que pasó el filtro de letras
        long_enough = len(word) >= 3
        is_stop = word in stop_words  # in comprueba si la palabra está en el conjunto de palabras vacías
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
    return set(word_list(text, stop_words))  # set deja cada palabra una sola vez


def keep_tokens(tokens: list[str]) -> list[str]:
    """Devuelve la lista tal cual. TfidfVectorizer la usa como analizador: las palabras ya vienen limpias."""
    return tokens  # devolvemos la lista que ya armó word_list


print(sorted(words("The diet and the DIET of obese children", STOP_WORDS)))
```

**Comprobar:**

En este paso comprobamos que `word_list` cuenta las repeticiones.

```python
assert word_list("The diet, the DIET and the risk", STOP_WORDS) == ["diet", "diet", "risk"]
print("Funciones de la L2 y la L3: OK")
```

### Paso 4. Los artículos con resumen útil
Los artículos están en `nutricion-papers.csv`, en la página del curso.
La función los descarga una sola vez y, si el archivo ya está, usa esa copia.
Un resumen con menos de 5 palabras útiles no tiene con qué decidir el tema.
En este paso dejamos fuera esos resúmenes.
De los artículos descargados quedan 317.

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
    if dest.is_file() and dest.stat().st_size > 0:  # is_file y stat comprueban que el archivo ya existe y no está vacío
        print(f"Ya en caché: {dest}")
        return dest
    response = requests.get(f"{BASE_URL}/{name}", timeout=60)  # requests.get pide el archivo a la página del curso
    response.raise_for_status()  # raise_for_status detiene la descarga si la página respondió con un error
    dest.write_bytes(response.content)
    print(f"Descargado: {dest} ({dest.stat().st_size / 1e6:.1f} MB)")
    return dest


papers = pd.read_csv(download_data("nutricion-papers.csv"), keep_default_na=False)
useful = []
for abstract in papers["abstract"]:   # recorremos el resumen de cada artículo
    useful.append(len(words(abstract, STOP_WORDS)) >= 5)   # words cuenta las palabras útiles y nos quedamos con los resúmenes que tienen al menos 5
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
OpenAlex ya trae, en `topics`, los temas que sus editores asignaron a cada artículo.
En este paso marcamos 1 cuando uno de esos temas menciona obesidad, dieta, nutrición, diabetes, salud cardiovascular, lipoproteínas, presión arterial o hipertensión.
Esa etiqueta viene dada. No la encontró un método de este cuaderno.
Por eso, más adelante, medimos los métodos contra marcas escritas antes de ver los resultados.
Con estos 317 artículos la etiqueta queda en 1 para 96.

```python
TARGET_TOPICS = ["obesity", "diet", "nutrition", "nutritional",   # agregamos las palabras del peso, la comida y la nutrición
                 "diabetes", "cardiovascular", "lipoproteins", "blood pressure", "hypertension"]   # agregamos las palabras de las enfermedades

y = np.zeros(N, dtype=int)  # empezamos con 0 en los 317 artículos
for i, topics in enumerate(papers["topics"]):   # recorremos los temas de OpenAlex de cada artículo
    for topic in TARGET_TOPICS:  # recorremos cada palabra de la etiqueta
        if topic in topics.lower():   # in busca esa palabra dentro del texto de los temas
            y[i] = 1  # escribimos 1 cuando el tema de OpenAlex trae la palabra
print(f"Artículos del tema según OpenAlex: {y.sum()} de {N} ({y.mean():.0%}). Mínimo pedido: {min_positives(N)}")
```

**Comprobar:**

En este paso comprobamos el número de artículos del tema y que llega al mínimo de positivos.

```python
assert y.sum() == 96 and y.sum() >= min_positives(N)
print("Etiqueta: OK")
```

### Paso 6. El largo de los resúmenes
El codificador de más adelante corta un resumen cuando pasa de 512 tokens.
En este paso contamos las palabras de cada uno de los 317 resúmenes, para ver qué tan largos son antes de ese corte.
`split` separa el resumen por espacios y `len` cuenta esos trozos.
La celda imprime la mediana y el máximo.

```python
word_counts = []
for text in texts:  # recorremos cada resumen
    word_counts.append(len(text.split()))   # split separa el resumen por espacios y len cuenta esos trozos
lengths = pd.Series(word_counts)  # Series guarda el largo de cada resumen
print(f"Palabras por resumen: mediana {lengths.median():.0f}, máximo {lengths.max():,}")
```

**Comprobar:**

En este paso comprobamos que hay un largo por resumen.

```python
assert len(lengths) == N and lengths.min() > 0
print("Largo: OK")
```

---

## Parte 3. Lista de palabras

### Paso 1. Las palabras clave en los resúmenes
La lista no aprende. Solo pregunta si una palabra está.
En este paso, en los 317 resúmenes, contamos en cuántos aparece cada palabra clave.
También contamos cuántos de esos resúmenes tienen etiqueta 0 según OpenAlex.
Una palabra que aparece en muchos resúmenes de etiqueta 0 va a marcar artículos fuera del tema.
Esa cuenta se queda en la pantalla y la lista sigue como referencia.

```python
word_sets = []
for text in texts:  # recorremos cada resumen
    word_sets.append(words(text, STOP_WORDS))   # words guarda el conjunto de palabras útiles de este resumen
for word in sorted(KEYWORDS):   # recorremos cada palabra de la lista clave
    with_word, off_topic = 0, 0  # empezamos en cero la cuenta de la palabra y la cuenta fuera del tema
    for i, word_set in enumerate(word_sets):  # recorremos el conjunto de palabras de cada resumen
        if word in word_set:  # in comprueba si el resumen trae la palabra
            with_word += 1  # sumamos uno cuando el resumen la trae
            off_topic += int(y[i] == 0)   # sumamos 1 cuando el resumen tiene la palabra y su etiqueta es 0
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
La lista no tiene pesos ni filas de entrenamiento.
En este paso recorremos los 317 resúmenes.
Marcamos 1 cuando el resumen comparte alguna palabra con `KEYWORDS`, y 0 cuando no.
La celda imprime en cuántos artículos la lista dice sí.

```python
pred_keywords = np.zeros(N, dtype=int)
for i, word_set in enumerate(word_sets):
    pred_keywords[i] = int(bool(word_set & KEYWORDS))  # marcamos 1 si el resumen comparte alguna palabra con la lista
print(f"La lista dice sí en {pred_keywords.sum()} de {N} artículos")
```

**Comprobar:**

En este paso comprobamos que la lista da un 0 o un 1 por artículo.

```python
assert len(pred_keywords) == N and set(np.unique(pred_keywords)) <= {0, 1}
print("Lista de palabras clave: OK")
```

---

## Parte 4. El conjunto y sus etiquetas

La lista no aprende, así que puede ver las 317 filas.
TF-IDF y el codificador sí aprenden.
En este paso partimos la etiqueta de OpenAlex, ya armada para los 317 artículos, en entrenamiento y prueba.
Apartamos 64 filas, el 20% de 317, con `train_test_split`.
`stratify` conserva en cada parte la proporción de la etiqueta.
Las otras 253 filas son el entrenamiento.
Las dos partes usan esa misma etiqueta.
Los temas los escribieron los editores de OpenAlex, antes de correr los métodos de este cuaderno.

```python
rows = np.arange(N)
train_rows, marked_rows = train_test_split(rows, test_size=n_flagged(N), stratify=y, random_state=SEED)  # train_test_split aparta 64 filas y stratify conserva la proporción del tema
y_train = y[train_rows]  # copiamos la etiqueta de los 317 artículos en las 253 filas de entrenamiento
y_test = y[marked_rows]  # copiamos la misma etiqueta en las 64 filas de prueba
print(f"Entrenamiento: {len(train_rows)} filas, {y_train.sum()} del tema")
print(f"Marcados: {len(marked_rows)} filas, {y_test.sum()} del tema. Marcas: temas de OpenAlex")
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
Cada resumen ya es una lista de palabras, con repeticiones.
TF-IDF convierte esa lista en una fila de pesos.
El peso sube cuando la palabra se repite en el resumen y baja cuando aparece en muchos resúmenes.

$\displaystyle \text{tf} = 1 + \log(\text{conteo}) \qquad \text{idf} = \log\frac{1 + N}{1 + \text{df}} + 1$

`N` aquí es el número de resúmenes con los que se ajusta el peso, las 253 filas de entrenamiento.
`df` es en cuántos de esos resúmenes aparece la palabra.
`fit_transform` aprende esos pesos solo con el entrenamiento.
Las 64 filas etiquetadas solo se transforman, para que no enseñen el vocabulario.

```python
token_lists = []
for text in texts:  # recorremos cada resumen
    token_lists.append(word_list(text, STOP_WORDS))   # word_list conserva cada aparición de la palabra
train_tokens, marked_tokens = [], []
for i in train_rows:  # recorremos las 253 filas de entrenamiento
    train_tokens.append(token_lists[i])  # guardamos la lista de palabras de esta fila
for i in marked_rows:
    marked_tokens.append(token_lists[i])   # apartamos las listas de las 64 filas etiquetadas
tfidf = TfidfVectorizer(analyzer=keep_tokens, sublinear_tf=True)   # TfidfVectorizer pesa cada palabra con tf = 1 + log(conteo)
X_train = tfidf.fit_transform(train_tokens)     # fit_transform aprende los pesos y arma la tabla solo con las 253 filas
X_marked = tfidf.transform(marked_tokens)  # transform aplica esos pesos a las 64 filas, sin volver a aprenderlos
feature_names = tfidf.get_feature_names_out()  # get_feature_names_out devuelve el nombre de cada columna de pesos
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

Ya tenemos un peso por palabra en las 253 filas.
Ahora un modelo aprende qué pesos empujan hacia el sí.

### Paso 2. El ajuste
La regresión logística pone un peso `w` a cada palabra y un número `b`.
La probabilidad de decir sí es

$\displaystyle P(y = 1 \mid x) = \frac{1}{1 + e^{-(w \cdot x + b)}}$

`class_weight="balanced"` da más peso a la clase del tema, que es la menor: 96 de 317.
`C_REG` vale 10 y fija la penalización de esos pesos.
`fit` aprende los pesos con las 253 filas.
`predict` dice 1 cuando la probabilidad pasa de 0,5.
La celda imprime en cuántos de los 64 marcados el modelo dice sí.

```python
tfidf_model = LogisticRegression(class_weight="balanced", C=C_REG, max_iter=1000)  # LogisticRegression prepara un peso por palabra. balanced da más peso a la clase menor
tfidf_model.fit(X_train, y_train)  # fit aprende esos pesos con las 253 filas de entrenamiento
pred_tfidf = tfidf_model.predict(X_marked)  # predict dice 1 en las 64 filas cuando la probabilidad pasa de 0,5
print(f"TF-IDF dice sí en {pred_tfidf.sum()} de {len(marked_rows)} marcados")
```

**Comprobar:**

En este paso comprobamos que TF-IDF da un 0 o un 1 por artículo marcado.

```python
assert len(pred_tfidf) == n_flagged(N) and set(np.unique(pred_tfidf)) <= {0, 1}
print("TF-IDF con regresión logística: OK")
```

### Leer los pesos
`coef_` guarda el peso que el modelo dio a cada palabra.
Un peso positivo empuja hacia el sí. Un peso negativo empuja hacia el no.
En este paso mostramos las 10 palabras de peso más alto y las 10 de peso más bajo.

```python
weights = pd.Series(tfidf_model.coef_[0], index=feature_names)  # coef_ guarda el peso de cada palabra y lo unimos con su nombre
pd.DataFrame({"a favor": weights.nlargest(10).index, "en contra": weights.nsmallest(10).index})  # nlargest toma las 10 de peso más alto y nsmallest las 10 de peso más bajo
```

Mire las diez palabras a favor y las diez en contra.
Esas palabras son lo que el modelo aprendió de la etiqueta.
Si el tema no aparece entre las de más peso, el resultado es pobre.
Lo documentamos y lo dejamos en la tabla.
El archivo guarda esta predicción porque esos pesos se pueden leer.

---

## Parte 6. Codificador de texto

El codificador ya fue entrenado con mucho texto y en este cuaderno no se vuelve a ajustar.
Lee el resumen entero, así que cada token depende de los que lo rodean.
El modelo entrega un vector por resumen.
Ese vector no se puede leer palabra por palabra, a diferencia de los pesos de TF-IDF.

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
El nombre del modelo es `intfloat/multilingual-e5-small`.
En este paso lo descargamos.
Pesa unos 470 MB y puede tardar un par de minutos.
Aquí no se vuelve a entrenar. `SentenceTransformer` solo lo carga.

```python
encoder = SentenceTransformer(ENCODER_NAME)  # SentenceTransformer descarga el modelo fijo y lo deja listo para convertir resúmenes en vectores
```

**Comprobar:**

En este paso comprobamos que el modelo cargó.

```python
assert encoder is not None
print("Modelo: OK")
```

### Paso 3. Un vector por resumen
Este modelo lee como máximo 512 tokens. Lo que pasa de ahí lo corta.
En este paso contamos cuántos de los 317 resúmenes pasan de 512, y dejamos que el modelo haga el corte.
Cada resumen empieza con `passage:` porque así pide usarse este modelo.
`encode` convierte cada resumen en un vector y `normalize_embeddings=True` lo deja en magnitud 1.
Así, como en la Lección 3, comparamos la mezcla y no el largo.

```python
n_cut = 0
passages = []
for text in texts:
    n_tokens = len(encoder.tokenizer.encode(text, add_special_tokens=False))  # el tokenizador cuenta los tokens del resumen, sin los tokens especiales
    if n_tokens > MAX_TOKENS:
        n_cut += 1  # contamos los resúmenes que el modelo va a cortar
    passages.append("passage: " + text)  # anteponemos passage: al resumen
print(f"Resúmenes de más de {MAX_TOKENS} tokens: {n_cut} de {N}")
vectors = encoder.encode(passages, normalize_embeddings=True, show_progress_bar=False)  # encode convierte cada resumen en un vector y lo deja en magnitud 1
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
Cada artículo ya es un vector de magnitud 1.
En este paso la regresión logística aprende con los vectores de las mismas 253 filas.
El codificador no se vuelve a ajustar. Solo cambian los pesos de la regresión.
`predict` dice sí o no en las 64 filas etiquetadas.
La celda imprime los aciertos de TF-IDF y los del codificador, lado a lado.

```python
encoder_model = LogisticRegression(class_weight="balanced", C=C_REG, max_iter=1000)  # LogisticRegression prepara un peso por cada número del vector
encoder_model.fit(vectors[train_rows], y_train)  # fit aprende esos pesos con los vectores de las 253 filas
pred_encoder = encoder_model.predict(vectors[marked_rows])  # predict dice 1 o 0 en las 64 filas etiquetadas
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
La exactitud es los aciertos sobre las 64 filas.
La clase mayoritaria da a todos la marca más frecuente.
Es la línea de referencia: un método útil debería superarla.
Si un método acierta poco, es normal.
Su fila sigue en la tabla.

### Paso 1. Aciertos y errores en el conjunto marcado
Los tres métodos y la clase mayoritaria se miden en las mismas 64 filas etiquetadas.
En este paso contamos TP, FP, FN y TN de cada uno, y su exactitud.
La exactitud es (TP + TN) / 64.
La clase mayoritaria da a las 64 filas la marca más frecuente. Es la línea de referencia.

```python
def counts_of(marks: np.ndarray, pred: np.ndarray) -> dict:
    """Cuenta los cuatro casos y la exactitud de un método frente a las marcas.

    Args:
        marks: Las marcas, 0 o 1.
        pred: Lo que dice el método, 0 o 1.

    Returns:
        Un diccionario con TP, FP, FN, TN y la exactitud.
    """
    tn, fp, fn, tp = confusion_matrix(marks, pred, labels=[0, 1]).ravel()  # confusion_matrix cuenta TN, FP, FN y TP en ese orden
    accuracy = accuracy_score(marks, pred)  # accuracy_score divide los aciertos entre todas las marcas
    return {"TP": tp, "FP": fp, "FN": fn, "TN": tn, "accuracy": accuracy}


majority_mark = int(y_test.mean() > 0.5)   # nos quedamos con 1 cuando más de la mitad de las marcas son 1
predictions = {
    "clase mayoritaria": np.full(len(marked_rows), majority_mark),  # full repite la marca más frecuente en las 64 filas
    "palabras clave": pred_keywords[marked_rows],
    "TF-IDF": pred_tfidf,
    "codificador": pred_encoder,
}
rows_by_method = {}
for name, pred in predictions.items():   # counts_of arma la fila de aciertos y errores de cada método
    rows_by_method[name] = counts_of(y_test, pred)
results = pd.DataFrame(rows_by_method).T  # DataFrame arma una fila por método
results[["TP", "FP", "FN", "TN"]] = results[["TP", "FP", "FN", "TN"]].astype(int)
print("Marcas: temas de OpenAlex")
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
Cada matriz tiene dos filas, la marca, y dos columnas, lo que dijo el método.
Las 64 filas etiquetadas caen en una de las cuatro casillas: TN, FP, FN o TP.
En este paso dibujamos esa matriz para la lista, para TF-IDF y para el codificador.
La clase mayoritaria no entra en la figura. Ya está en la tabla del paso anterior.

```python
fig, axes = plt.subplots(1, 3, figsize=(11, 3.4))  # subplots abre un panel por método
for ax, name in zip(axes, ["palabras clave", "TF-IDF", "codificador"]):  # recorremos la lista, TF-IDF y el codificador
    ConfusionMatrixDisplay.from_predictions(y_test, predictions[name], labels=[0, 1], display_labels=["no leer", "leer"],  # from_predictions dibuja la matriz de esta predicción contra las marcas
                                            cmap="Blues", colorbar=False, ax=ax)
    ax.set_title(name)  # set_title pone el nombre del método
    ax.set_xlabel("Dice el método")  # set_xlabel nombra lo que dice el método
    ax.set_ylabel("Marca")  # set_ylabel nombra la marca
fig.tight_layout()  # tight_layout acomoda los márgenes
fig.savefig(OUTPUTS_DIR / "confusion_l4.png", dpi=120)  # savefig guarda la figura
plt.show()  # show muestra la figura
```

### Paso 3. El texto para toda la colección
Hasta aquí TF-IDF y el codificador dicen sí o no solo en las 64 filas etiquetadas.
Las dos listas necesitan un número para los 317 artículos.
En este paso guardamos la probabilidad de TF-IDF y la del codificador.
Las 64 filas etiquetadas usan el modelo ya ajustado con las 253.
Cada fila de entrenamiento usa el pliegue que no la vio, para que ninguna fila reciba la probabilidad de un modelo que la usó para aprender.
Pasamos a 1 cuando la probabilidad de TF-IDF supera 0,5.

```python
prob_texto = np.zeros(N)  # empezamos la probabilidad de TF-IDF en cero para los 317 artículos
prob_encoder = np.zeros(N)  # empezamos la probabilidad del codificador en cero para los 317 artículos
prob_texto[marked_rows] = tfidf_model.predict_proba(X_marked)[:, 1]  # predict_proba escribe la probabilidad de TF-IDF en las 64 filas etiquetadas
prob_encoder[marked_rows] = encoder_model.predict_proba(vectors[marked_rows])[:, 1]  # predict_proba escribe la probabilidad del codificador en las 64 filas etiquetadas
folds = StratifiedKFold(n_splits=N_FOLDS, shuffle=True, random_state=SEED)  # StratifiedKFold parte las 253 filas en 5 pliegues y conserva la proporción del tema
for fit_rows, test_rows in folds.split(train_rows, y_train):  # split entrega en cada vuelta las filas de ajuste y la parte que no vio
    learn, check = train_rows[fit_rows], train_rows[test_rows]  # learn son las filas que el pliegue ajusta y check la parte que no vio
    learn_tokens, check_tokens = [], []
    for i in learn:  # recorremos las filas de ajuste
        learn_tokens.append(token_lists[i])  # guardamos la lista de palabras de esta fila
    for i in check:  # recorremos la parte que el pliegue no vio
        check_tokens.append(token_lists[i])  # guardamos la lista de palabras de esta fila
    fold_vectorizer = TfidfVectorizer(analyzer=keep_tokens, sublinear_tf=True)  # TfidfVectorizer prepara los pesos de este pliegue
    fold_vectorizer.fit(learn_tokens)  # fit aprende los pesos solo con las filas que este pliegue sí ve
    fold_model = LogisticRegression(class_weight="balanced", C=C_REG, max_iter=1000)  # LogisticRegression prepara la regresión de TF-IDF para este pliegue
    fold_model.fit(fold_vectorizer.transform(learn_tokens), y[learn])  # fit aprende los pesos sin ver la parte de prueba
    fold_prob = fold_model.predict_proba(fold_vectorizer.transform(check_tokens))[:, 1]  # predict_proba escribe la probabilidad de TF-IDF en la parte que no vio
    prob_texto[check] = fold_prob  # cada fila de entrenamiento recibe la probabilidad de TF-IDF del pliegue que no la vio
    fold_encoder = LogisticRegression(class_weight="balanced", C=C_REG, max_iter=1000)  # LogisticRegression prepara la regresión del codificador para este pliegue
    fold_encoder.fit(vectors[learn], y[learn])  # fit aprende con los vectores de las filas que este pliegue sí ve
    prob_encoder[check] = fold_encoder.predict_proba(vectors[check])[:, 1]  # predict_proba escribe la probabilidad del codificador en la parte que no vio
text_tfidf = (prob_texto > 0.5).astype(int)  # pasamos a 1 cuando la probabilidad de TF-IDF supera 0,5
print(f"Dicen leer: palabras clave {pred_keywords.sum()}, TF-IDF {text_tfidf.sum()}")
```

**Comprobar:**

En este paso comprobamos que `prob_texto` coincide con la predicción de TF-IDF y que las dos probabilidades cubren los 317 artículos.

```python
assert ((prob_texto > 0.5) == text_tfidf).all()
assert len(prob_texto) == N and len(prob_encoder) == N
assert ((prob_texto >= 0) & (prob_texto <= 1)).all() and ((prob_encoder >= 0) & (prob_encoder <= 1)).all()
print("Texto para toda la colección: OK")
```

### Paso 4. Guardar el texto
Guardamos una fila por cada uno de los 317 artículos en `outputs/texto_l4.csv`.
`keyword` es el sí o no de la lista. `tfidf_lr` es el sí o no de TF-IDF. `prob_texto` es su probabilidad.
`marca` lleva las 64 marcas. Las otras filas quedan vacías, porque esas filas sirvieron para aprender y no tienen marca de prueba.
Este archivo es el resultado de esta lección.

```python
marca = pd.Series(pd.NA, index=range(N), dtype="Int64")  # Series deja la marca vacía en las 317 filas
marca[marked_rows] = y_test  # escribimos la marca solo en las 64 filas apartadas
text_table = pd.DataFrame({
    "title": papers["title"],
    "keyword": pred_keywords,
    "tfidf_lr": text_tfidf,
    "prob_texto": prob_texto,
    "marca": marca,
})  # DataFrame arma una fila por artículo
text_path = OUTPUTS_DIR / "texto_l4.csv"  # Path fija la ruta de texto_l4.csv
text_table.to_csv(text_path, index=False)  # to_csv escribe la tabla y deja fuera el índice
print(f"Guardado: {text_path} ({len(text_table)} filas, {text_table['marca'].notna().sum()} etiquetadas)")
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

### Paso 1. Qué hace el texto con las listas
El texto de esta lección es un filtro.
La lista que guardamos deja pasar los artículos que la lista de palabras o TF-IDF marcan para leer.
Cada punto de esa lista se puede mirar: una palabra de la lista, o un peso de TF-IDF.
El codificador arma una segunda lista, ordenada solo por su probabilidad.
Un artículo que aparece solo en esa segunda lista no tiene una palabra que citar.
Por eso no entra en la lista que el equipo usa para leer.
`texto_l4.csv` guarda el sí o no de la lista y de TF-IDF, y la probabilidad de TF-IDF.
Un método que quedó bajo la clase mayoritaria se queda en la tabla de la evaluación.
Esta lista usa solo el texto de hoy.

### Paso 2. Artículos para leer
La lista de palabras suma 1 cuando dice leer.
TF-IDF suma su probabilidad, de 0 a 1.
La evidencia es esa suma, de 0 a 2.
El codificador no entra en esa suma.
Ordenamos de mayor a menor evidencia, después por `prob_texto` y, si empatan, por título.
De los 317 mostramos como máximo 30, el tope de la Lección 1.

```python
reading_rows = []
for i in range(N):   # recorremos cada artículo
    row = {"title": papers.loc[i, "title"],
           "palabras_clave": int(pred_keywords[i]),   # escribimos 1 cuando la lista dice leer
           "tfidf": round(prob_texto[i], 2)}          # escribimos la probabilidad de TF-IDF
    row["evidencia"] = round(row["palabras_clave"] + row["tfidf"], 2)  # sumamos la lista y la probabilidad de TF-IDF
    row["prob_texto"] = round(prob_texto[i], 3)
    reading_rows.append(row)

reading = pd.DataFrame(reading_rows).sort_values(["evidencia", "prob_texto", "title"], ascending=[False, False, True])  # sort_values ordena por evidencia, luego por probabilidad y luego por título
reading_list = reading.head(MAX_PAPERS)   # head corta la lista en 30 artículos
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

En este paso comprobamos el largo de la lista, su orden y que la evidencia es la suma de la lista de palabras y TF-IDF.

```python
assert len(reading_list) == min(MAX_PAPERS, len(reading)) and reading_list["evidencia"].is_monotonic_decreasing
assert ((reading_list["evidencia"] - reading_list["palabras_clave"] - reading_list["tfidf"]).abs() < 0.011).all()
assert reading_list["evidencia"].between(0, 2).all()
print("Lista de lectura: OK")
```

### Paso 3. La lista del codificador
Esta lista ordena los 317 artículos solo por la probabilidad del codificador.
Mostramos como máximo 30, igual que la lista que guardamos.
En este paso contamos cuántos de esos 30 ya están en la primera lista y cuántos están solo aquí.
Los que están solo aquí no tienen una palabra de la lista ni un peso de TF-IDF que los explique.
Por eso no entran en `lectura_l4.csv`.

```python
encoder_rows = []
for i in range(N):  # recorremos cada artículo
    encoder_rows.append({"title": papers.loc[i, "title"], "prob_encoder": round(float(prob_encoder[i]), 3)})  # guardamos el título y la probabilidad del codificador
encoder_reading = pd.DataFrame(encoder_rows).sort_values(["prob_encoder", "title"], ascending=[False, True])  # sort_values ordena por la probabilidad del codificador y luego por título
encoder_list = encoder_reading.head(MAX_PAPERS)  # head corta la lista en 30 artículos
encoder_path = OUTPUTS_DIR / "lectura_encoder_l4.csv"  # Path fija la ruta de la lista del codificador
encoder_list.to_csv(encoder_path, index=False)  # to_csv escribe la lista y deja fuera el índice
kept_titles = set(reading_list["title"])  # set guarda los títulos de la lista que sí explicamos
both = int(encoder_list["title"].isin(kept_titles).sum())  # sum cuenta cuántos de los 30 ya están en esa lista
only_encoder = len(encoder_list) - both  # restamos para contar los que están solo en el codificador
print(f"En las dos listas: {both}. Solo en el codificador: {only_encoder}.")
encoder_list.loc[~encoder_list["title"].isin(kept_titles), "title"].head(5)  # head muestra hasta cinco títulos que no tienen una palabra que citar
```

Mire el conteo y los títulos que salen solo en el codificador. Esos artículos se leerían sin una palabra que mostrar lo cual dificulta la explicación e interpretación de resultados.

**Comprobar:**

En este paso comprobamos el largo de la segunda lista, su orden y que el conteo cubre sus 30 títulos.

```python
assert len(encoder_list) == min(MAX_PAPERS, N) and encoder_list["prob_encoder"].is_monotonic_decreasing
assert both + only_encoder == len(encoder_list)
print("Lista del codificador: OK")
```

<!-- end NOTEBOOK: -->
