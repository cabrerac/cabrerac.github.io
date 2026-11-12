<!-- NOTEBOOK: -->

## Repaso de Python para este cuaderno

Este cuaderno utiliza los siguientes métodos de Python.

### Conjuntos con `set`
Un **conjunto** guarda elementos sin repetir. El operador `&` devuelve lo que dos conjuntos tienen en común.

```python
a = {"obesity", "diet", "risk"}
b = {"diet", "risk", "children"}
print(a & b)          # palabras que están en los dos conjuntos
print(len(a | b))     # palabras distintas entre los dos
```

### Contar con `Counter` y formar pares con `combinations`
`Counter` cuenta cada elemento y `most_common(k)` muestra los `k` más frecuentes. `itertools.combinations(lista, 2)` genera cada par una sola vez.

```python
from collections import Counter
from itertools import combinations

counts = Counter(["diet", "risk", "diet", "obesity", "diet"])
print(counts.most_common(2))
print(list(combinations(sorted({"risk", "diet", "obesity"}), 2)))
```

### Coseno con `numpy`
El coseno mide si dos flechas apuntan en la misma dirección.
Vale 1 si van por la misma línea y 0 si forman un ángulo recto.
El largo de la flecha no cambia el coseno.
Las listas de palabras de más adelante tienen 300 números.
El dibujo es la misma idea con 2.

```python
import matplotlib.pyplot as plt
import numpy as np


def cosine(a, b):
    """Coseno de dos flechas. Vale 1 si apuntan igual y 0 si forman un ángulo recto."""
    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b)))


same_short = np.array([1.0, 0.0])  # flecha corta sobre el eje horizontal
same_long = np.array([2.0, 0.0])  # la misma línea, el doble de larga
right_angle = np.array([0.0, 1.0])  # ángulo recto con la corta
between = np.array([1.0, 1.0])  # a medio camino entre la corta y el ángulo recto
c_same = cosine(same_short, same_long)
c_right = cosine(same_short, right_angle)
c_between = cosine(same_short, between)
assert abs(c_same - 1.0) < 1e-9
assert abs(c_right) < 1e-9
assert abs(c_between - 0.7071) < 1e-3
print(f"Misma línea: {c_same:.2f}. Ángulo recto: {c_right:.2f}. En medio: {c_between:.2f}.")

arrows = [
    (same_long, "C1", (0.05, -0.18), "larga"),
    (same_short, "C0", (0.05, 0.08), "corta"),
    (right_angle, "C2", (0.08, 0.02), "ángulo recto"),
    (between, "C3", (0.08, 0.02), "en medio"),
]
plt.figure(figsize=(5.2, 5.2))
for vector, color, offset, name in arrows:
    plt.annotate("", xy=vector, xytext=(0, 0), arrowprops=dict(arrowstyle="->", color=color, lw=2))
    plt.text(vector[0] + offset[0], vector[1] + offset[1], name, color=color)
plt.xlim(-0.3, 2.6)
plt.ylim(-0.45, 1.7)
plt.axhline(0, color="gray", linewidth=0.5)
plt.axvline(0, color="gray", linewidth=0.5)
plt.gca().set_aspect("equal")
plt.xlabel("Primer número")
plt.ylabel("Segundo número")
plt.title("Cuatro flechas. El coseno se mide contra la corta.")
plt.show()
```

### Una lista por comprensión
La expresión entre corchetes recorre una lista y arma otra.

```python
sizes = [len(words) for words in [{"diet", "risk"}, {"obesity"}]]
print(sizes)
```

### Una columna de verdadero o falso
Una condición agrega una columna.
Sirve para marcar las filas que se conservan.

```python
import pandas as pd

pairs = pd.DataFrame({"pair": ["diet + risk", "a + b"], "count": [12, 3]})
pairs["kept"] = pairs["count"] >= 10
assert pairs["kept"].tolist() == [True, False]
print(pairs)
print("Repaso de Python: OK")
```

---

## Instrucciones

Seguimos con el equipo interno de la secretaría de salud y sus 320 artículos sobre nutrición. El equipo debe decidir **qué artículos tiene que leer** un colega que llega al equipo. En la Lección 1 escribimos la descripción de la pregunta.

En este cuaderno buscamos **patrones que se repiten** en los resúmenes (`abstract`). El resumen es la descripción del artículo que vamos a leer. La idea viene de las tiendas: Agrawal, Imielinski y Swami (1993) preguntaron qué productos se repiten juntos en los recibos. Aquí la canasta es esa descripción y los productos son sus palabras. Un patrón es un par de palabras que aparece junto en muchos artículos. La evaluación compara tres lecturas del mismo par: cuántas veces aparecen juntas, si aparecen juntas más de lo esperado, y si el modelo las usa en frases parecidas.

**Tres métodos, tres preparaciones.**

| Método | Pregunta | Preparación que necesita |
|--------|----------|--------------------------|
| Pares frecuentes | ¿En cuántos artículos aparecen juntas dos palabras? | Un conjunto de palabras por artículo |
| Lift | ¿Aparecen juntas más de lo que esperaríamos si las dos palabras no tuvieran que ver? | Cuántas veces aparece el par y cuántas veces aparece cada palabra sola |
| Cercanía | ¿El modelo las usa en frases parecidas? | Las palabras que el modelo conoce |

**Qué hacer.** Ejecute las celdas de arriba hacia abajo. Cada paso empieza con **En este paso**. Si el paso tiene código, termina con una celda **Comprobar**.

**Mapa del cuaderno**

| Parte | Fase CRISP-DM | Qué sale |
|-------|---------------|----------|
| 1 | Comprensión del negocio | La pregunta de hoy, escrita en el cuaderno |
| 2 | Comprensión de los datos | Parámetros, modelo de vectores y los artículos en memoria |
| 3 | Preparación de los datos | Conjuntos de palabras, conteos y vectores |
| 4 | Modelado | Pares por soporte, lift y coseno |
| 5 | Evaluación | Los pares conservados, los tres pares de la figura y `outputs/patrones_l2.csv` |
| 6 | Despliegue | Hasta 30 artículos para leer, ordenados por la evidencia de los pares |

**Carpetas.** La celda de configuración crea `data/` (datos descargados) y `outputs/` (tablas y gráficos).

---

## Parte 1. Comprensión del negocio

### Paso 1. La pregunta de esta lección
En este paso escribimos qué buscamos hoy. La decisión no cambia: qué artículos debe leer el colega nuevo.

| Pregunta | Respuesta para el laboratorio |
|----------|-------------------------------|
| ¿Qué buscamos en los resúmenes? | Pares de palabras que aparecen juntas en muchos artículos |
| ¿Cómo medimos un par? | En cuántos artículos aparece. Si ese número supera las tablas reordenadas. Si el modelo usa las dos palabras en frases parecidas |
| ¿Qué hacemos con un par que se conserva? | Lo volvemos un filtro con nombre, por ejemplo los artículos que contienen *fasting* y *plasma* |

Un patrón no elige artículos pero es información que el equipo puede utilizar para consolidar la lista.

---

## Parte 2. Comprensión de los datos

### Paso 1. Configuración
En este paso importamos las librerías, creamos las carpetas y fijamos los números con los que vamos a leer los conteos.
`math` tiene funciones numéricas. `random` reordena listas con una semilla fija. `re` encuentra palabras en un texto. `time` mide cuánto tarda un paso. `pandas` es la tabla.
`matplotlib` es la figura. `numpy` guarda listas de números. `requests` descarga el archivo. `Path` es el nombre de una carpeta.

Un par tiene que aparecer en bastantes descripciones. Si no, puede ser una casualidad de un solo artículo. Pedimos al menos 5 artículos, y también al menos el 3% de la colección.
Nos quedamos con el número mayor. La semilla vale 7. Con esa semilla, generamos tablas reordenadas en la sección de evaluación. Estas tablas intercambian palabras entre artículos. De esta forma podemos medir cuando un par aparece junto más que el azar.

```python
import math
import random
import re
import time
from collections import Counter
from collections.abc import Iterable, Sequence
from itertools import combinations
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests

# Carpetas de trabajo
DATA_DIR = Path("data")  # aquí queda el CSV
OUTPUTS_DIR = Path("outputs")  # aquí quedan las tablas y las figuras
DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

# Números con los que leemos los conteos. No los cambie.
SUPPORT_SHARE = 0.03   # al menos el 3% de las descripciones
SUPPORT_MIN = 5        # y nunca menos de 5 artículos
SWAPS_PER_ONE = 5      # intentos de intercambio por cada 1 de la tabla, en cada tabla al azar
N_SAMPLES = 100        # cien tablas al azar
SEED = 7               # la misma semilla para todos, así las tablas al azar coinciden
PROGRESS_EVERY = 20    # imprime una línea de avance cada 20 tablas (0 = en silencio)
LIFT_MIN = 2.0         # el par aparece al menos el doble de lo esperado


def support_floor(n_texts: int) -> int:
    """Soporte mínimo que necesita una palabra o un par: max(SUPPORT_MIN, ceil(SUPPORT_SHARE * n))."""
    return max(SUPPORT_MIN, math.ceil(SUPPORT_SHARE * n_texts))  # el mayor entre 5 y el 3%


print(f"Umbral para 317 artículos: {support_floor(317)}")
print(f"Umbral para 298 artículos: {support_floor(298)}")
```

**Comprobar:**

En este paso comprobamos el valor del umbral de soporte para nuestra colección.

```python
assert support_floor(317) == 10
assert support_floor(100) == SUPPORT_MIN
print("Parámetros: OK")
```

### Paso 2. Modelo de vectores de palabras
En este paso cargamos un modelo de spaCy que ya viene entrenado en inglés.

El tercer método pregunta si las dos palabras se usan en frases parecidas. Para eso el modelo guarda, para cada palabra frecuente, una lista de 300 números. Esa lista es el vector. Dos palabras que aparecen en frases parecidas tienen vectores parecidos. Por ejemplo, diabetes y obesity quedan cerca. Una palabra de nutrición y una palabra de otro tema quedan lejos. Esas listas se aprendieron de una gran cantidad de texto en inglés. El entrenamiento dio números parecidos a las palabras que aparecen en frases parecidas. En este cuaderno solo buscamos una palabra y leemos su lista.

`en_core_web_lg` es un modelo ya entrenado. Pesa unos 400 MB porque guarda esas listas para cientos de miles de palabras. Colab lo descarga en cada sesión. Puede tardar hasta un par de minutos. Si la descarga se corta, la celda carga el modelo mediano `en_core_web_md`, de unos 33 MB. También puede elegirlo con `USE_MEDIUM_MODEL = True`. Ese modelo tiene menos listas distintas, y a veces dos palabras distintas comparten la misma.

```python
import importlib
import spacy

USE_MEDIUM_MODEL = False   # True solo si la descarga del modelo grande falla siempre
MODELS = ["en_core_web_md"] if USE_MEDIUM_MODEL else ["en_core_web_lg", "en_core_web_md"]  # primero el grande, luego el mediano

# Esta lección solo necesita las listas de números. Estas piezas hacen otras tareas (gramática, nombres) y no las cargamos.
UNUSED_PIPES = ["tok2vec", "tagger", "parser", "attribute_ruler", "lemmatizer", "ner", "morphologizer", "senter"]


def load_vector_model(names: list[str]):
    """Carga el primer modelo de spaCy de la lista que se pueda instalar.

    Intenta cargar cada nombre.
    Si no está instalado, lo descarga y vuelve a intentarlo.
    Si la descarga falla, pasa al siguiente.
    Args:
        names: Lista de modelos, el grande primero.
    Returns:
        El modelo cargado y su nombre.
    """
    for name in names:
        start = time.time()
        try:
            nlp = spacy.load(name, exclude=UNUSED_PIPES)  # carga el modelo y deja solo los vectores
        except OSError:
            print(f"Descargando {name} (puede tardar unos minutos)...")
            try:
                spacy.cli.download(name)
                importlib.invalidate_caches()
                nlp = spacy.load(name, exclude=UNUSED_PIPES)  # carga el modelo y deja solo los vectores
            except (Exception, SystemExit) as error:
                print(f"No se pudo instalar {name}: {error}")
                continue
        print(f"Modelo cargado: {name} en {time.time() - start:.1f} s")
        return nlp, name
    raise RuntimeError("No se pudo cargar ningún modelo de vectores. Revise la conexión.")


nlp, MODEL = load_vector_model(MODELS)
print(f"Vectores en el modelo: {nlp.vocab.vectors.shape[0]:,} filas de {nlp.vocab.vectors.shape[1]} dimensiones")
if MODEL == "en_core_web_md":
    print("Cargó el modelo mediano. El conteo y el lift no cambian. La cercanía sí: muchas palabras comparten vector y sus vecinos no coinciden con las diapositivas. Use la cercanía aquí solo para ver ese problema, y repita el Paso 2 con el modelo grande cuando pueda.")
```

**Comprobar:**

En este paso comprobamos que cargó un modelo con vectores de 300 dimensiones.

```python
assert MODEL in ("en_core_web_lg", "en_core_web_md")
assert nlp.vocab.vectors.shape[1] == 300
print(f"Modelo {MODEL}: OK")
```

### Paso 3. Descargar y cargar los artículos
En este paso descargamos `nutricion-papers.csv`, como en la Lección 1.

```python
BASE_URL = "https://cabrerac.github.io/assets/data/26-udenar-data-mining"


def download_data(name: str, folder: Path = DATA_DIR) -> Path:
    """Descarga un archivo de datos del curso, una sola vez.

    Qué hace: si el archivo ya está en la carpeta, lo usa. Si no, lo descarga de BASE_URL.
    Entrada: name, el nombre del archivo (por ejemplo "nutricion-papers.csv"), y folder,
    la carpeta destino.
    Salida: la ruta local del archivo.
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


papers = pd.read_csv(download_data("nutricion-papers.csv"))  # una fila por artículo
print(papers.shape)
papers[["title", "year", "cited_by_count"]].head(3)
```

Cada fila es un artículo. La descripción que vamos a partir en palabras es el resumen, la columna `abstract`. El título, el año y las citas se quedan en la tabla.

**Comprobar:**

En este paso comprobamos la forma de los datos y que está la columna `abstract`.

```python
assert papers.shape == (320, 13)
assert "abstract" in papers.columns
print("Datos: OK")
```

---

## Parte 3. Preparación de los datos

Cada método de análisis pide algo distinto. El primero pide un conjunto de palabras por artículo. El segundo pide además cuántos artículos tienen cada palabra. El tercer método pide que el modelo conozca la palabra.

### Paso 1. De texto a palabras
En este paso convertimos un resumen en un **conjunto de palabras**. Pasamos a minúsculas, quitamos las palabras de menos de 3 letras y las **palabras vacías** de spaCy ("the", "of", "and"...), que formarían pares sin significado.

```python
from spacy.lang.en.stop_words import STOP_WORDS as STOP_WORDS_EN

WORD_RE = re.compile(r"[^\W\d_]+")   # secuencias de letras (sin números ni guiones bajos)


def words(text: str, stop_words: set[str]) -> set[str]:
    """Convierte un texto en el conjunto de sus palabras útiles.

    Qué hace: pasa a minúsculas, quita el residuo "[cita requerida]" de Wikipedia,
    separa en palabras de letras y descarta las de menos de 3 letras y las palabras vacías.
    Entrada: text, la descripción de un artículo, y stop_words, el conjunto de palabras vacías.
    Salida: un set con cada palabra una sola vez.
    """
    text = (text or "").lower().replace("[cita requerida]", " ")  # el resumen en minúsculas, sin la marca de Wikipedia
    useful = set()
    for word in WORD_RE.findall(text):  # por cada palabra de solo letras en el resumen
        long_enough = len(word) >= 3  # tiene al menos 3 letras
        is_stop = word in stop_words  # es una palabra vacía, como "the", "of" o "and"
        if long_enough and not is_stop:  # la palabra habla del tema
            useful.add(word)  # entra una sola vez, aunque el resumen la repita
    return useful


example = papers.loc[0, "abstract"]  # la descripción del primer artículo
print(example[:300], "...")
print(sorted(words(example, STOP_WORDS_EN))[:20])
```

**Comprobar:**

En este paso comprobamos que `words` deja solo las palabras útiles de una frase de prueba.

```python
assert words("The diet and the RISK of obesity", STOP_WORDS_EN) == {"diet", "risk", "obesity"}
print("Palabras: OK")
```

### Paso 2. Texto de relleno: las etiquetas del resumen
En este paso buscamos **texto de relleno**: etiquetas como *Background*, *Methods* y *Funding*, y la misma línea de financiación en decenas de artículos. Dicen cómo se escribió el resumen, no de qué trata.

Contamos *background* y *methods* juntas.
El lift dice cuántas veces aparecen juntas respecto de lo que esperaríamos si no tuvieran que ver.
La fórmula está en la Parte 4.

```python
dirty_sets = []
for text in papers["abstract"]:  # por cada resumen de la colección
    words_here = words(text, STOP_WORDS_EN)  # sus palabras, todavía con las etiquetas del resumen
    if len(words_here) >= 5:  # el resumen tiene al menos 5 palabras
        dirty_sets.append(words_here)  # este artículo entra a la cuenta del relleno
n_dirty = len(dirty_sets)
together = 0
with_background = 0
with_methods = 0
bill_gates = 0
for words_here in dirty_sets:  # por cada resumen de esa cuenta
    has_background = "background" in words_here  # el resumen trae la etiqueta Background
    has_methods = "methods" in words_here  # el resumen trae la etiqueta Methods
    if has_background and has_methods:
        together = together + 1  # las dos etiquetas están en el mismo resumen
    if has_background:
        with_background = with_background + 1  # un resumen más con Background
    if has_methods:
        with_methods = with_methods + 1  # un resumen más con Methods
    has_bill_gates = "bill" in words_here and "gates" in words_here  # el resumen nombra la fundación
    if has_bill_gates:
        bill_gates = bill_gates + 1  # un resumen más con esa financiación
filler_lift = together * n_dirty / (with_background * with_methods)  # veces lo esperado si las dos palabras no tuvieran que ver
print(f"background + methods: {together} artículos, lift {filler_lift:.1f}")
print(f"bill + gates: {bill_gates} artículos")
```

El par aparece en 77 artículos y casi triplica lo esperado por azar. Es puro formato, así que lo quitamos **antes** de minar.

```python
ABSTRACT_LABELS = {  # etiquetas del resumen y de la financiación, no del tema
    "background", "methods", "findings", "interpretation", "funding",
    "conclusions", "results", "objective", "objectives", "aims",
    "bill", "melinda", "gates", "foundation",
}
print(f"Etiquetas de resumen y financiación: {len(ABSTRACT_LABELS)} palabras")
```

**Comprobar:**

En este paso comprobamos cuántos artículos tienen *background* y *methods* y el tamaño de la lista de relleno.

```python
assert together == 77
assert len(ABSTRACT_LABELS) == 14
print("Texto de relleno: OK")
```

### Paso 3. Restos de direcciones web
En este paso quitamos los pedazos de direcciones web (*http*, *https*, *www*, *org*). Son formato y no dicen nada del tema.

```python
URL_TOKENS = {"http", "https", "www", "org"}
for token in sorted(URL_TOKENS):  # por cada pedazo de dirección web
    articles_with_token = 0
    for words_here in dirty_sets:  # por cada resumen
        if token in words_here:  # el resumen contiene ese pedazo
            articles_with_token = articles_with_token + 1  # un resumen más con ese pedazo
    print(f"{token:6s} en {articles_with_token} resúmenes")

STOP_WORDS = set(STOP_WORDS_EN) | ABSTRACT_LABELS | URL_TOKENS  # la lista que usa el resto del cuaderno
print(f"Palabras vacías: {len(STOP_WORDS_EN)} de spaCy + {len(ABSTRACT_LABELS)} de relleno + {len(URL_TOKENS)} de direcciones web")
```

Desde aquí, `STOP_WORDS` es la lista que usa todo el cuaderno.

**Comprobar:**

En este paso comprobamos que las etiquetas del resumen y los restos de direcciones web ya no pasan como palabras.

```python
assert "background" not in words(example + " Background", STOP_WORDS)
assert not URL_TOKENS & words("see https://www.who.int and www.fao.org", STOP_WORDS)
print("Direcciones web: OK")
```

### Paso 4. Un conjunto de palabras por artículo
En este paso armamos la entrada del primer método: un conjunto de palabras por artículo. Dejamos fuera las descripciones con menos de 5 palabras útiles.

```python
word_sets = []
for text in papers["abstract"]:  # por cada resumen de la colección
    words_here = words(text, STOP_WORDS)  # sus palabras útiles, ya sin relleno ni direcciones
    if len(words_here) >= 5:  # el resumen tiene al menos 5 palabras útiles
        word_sets.append(words_here)  # este artículo entra al análisis
N = len(word_sets)  # artículos que siguen
FLOOR = support_floor(N)  # piso de esta colección: 10 artículos

lengths = []
for words_here in word_sets:  # por cada artículo que entra al análisis
    lengths.append(len(words_here))  # cuántas palabras útiles tiene su resumen
sizes = pd.Series(lengths)
print(f"Artículos usados: {N} de {len(papers)}")
print(f"Palabras distintas por artículo: mediana {sizes.median():.0f}, mínimo {sizes.min()}, máximo {sizes.max()}")
print(f"Umbral de soporte: {FLOOR} artículos")
```

Hay resúmenes cortos y otros con cientos de palabras. Un resumen largo forma muchos pares por sí solo, y eso importa en la Parte 5.

**Comprobar:**

En este paso comprobamos el número de artículos usados y el umbral de soporte.

```python
assert N == 317
assert FLOOR == 10
print("Conjuntos: OK")
```

### Paso 5. Conteo de cada palabra sola
En este paso contamos en **cuántos artículos** aparece cada palabra. El lift necesita este conteo.

Una palabra en menos de 10 artículos no puede formar un par en 10. Es la **propiedad Apriori**, y así descartamos miles de pares sin contarlos.

```python
word_count = Counter()
for words_here in word_sets:  # por cada artículo que entra al análisis
    for word in words_here:  # por cada palabra útil de su resumen
        word_count[word] = word_count[word] + 1  # un artículo más donde aparece esa palabra
vocabulary = []
for word, count in word_count.items():  # por cada palabra distinta
    if count >= FLOOR:  # aparece en al menos 10 artículos
        vocabulary.append(word)  # puede formar un par
vocabulary = sorted(vocabulary)

print(f"Palabras distintas: {len(word_count):,}")
print(f"Palabras en {FLOOR} artículos o más: {len(vocabulary):,}")
print(word_count.most_common(10))
```

**Comprobar:**

En este paso comprobamos el tamaño del vocabulario y que cada palabra llega al umbral.

```python
assert len(vocabulary) == 870
assert all(word_count[w] >= FLOOR for w in vocabulary)
print("Conteo de palabras: OK")
```

### Paso 6. Conteo de pares
En este paso contamos en cuántos artículos aparece cada par. Ese número es el **soporte**. Los pares que llegan al umbral son los **candidatos**.

```python
def count_pairs(word_sets: list[set[str]], word_count: Counter, floor: int) -> dict:
    """Cuenta en cuántos textos aparece cada par de palabras frecuentes.

    Qué hace: en cada texto toma solo las palabras que llegan al umbral, genera sus pares
    ordenados con combinations y los cuenta. Devuelve los pares que llegan al umbral.
    Entrada: word_sets (un conjunto de palabras por texto), word_count (en cuántos textos
    aparece cada palabra) y floor (el umbral de soporte).
    Salida: diccionario {(word_a, word_b): soporte}.
    """
    pairs = Counter()
    for words_here in word_sets:  # por cada artículo
        frequent = []
        for word in words_here:  # por cada palabra de su resumen
            if word_count[word] >= floor:  # esta palabra aparece en al menos 10 artículos
                frequent.append(word)  # puede formar un par en este resumen
        frequent = sorted(frequent)  # orden fijo, para que diet + risk no se cuente dos veces
        pairs.update(combinations(frequent, 2))  # cada par de palabras de este resumen, una sola vez
    kept_pairs = {}
    for pair, count in pairs.items():  # por cada par que apareció
        if count >= floor:  # las dos palabras están juntas en al menos 10 artículos
            kept_pairs[pair] = count  # este par es candidato
    return kept_pairs


candidates = count_pairs(word_sets, word_count, FLOOR)  # pares que aparecen en al menos 10 artículos
print(f"Pares candidatos (soporte de {FLOOR} o más): {len(candidates):,}")
```

**Comprobar:**

En este paso comprobamos el número de pares candidatos y que todos llegan al umbral.

```python
assert len(candidates) == 16271
assert min(candidates.values()) >= FLOOR
print("Pares: OK")
```

### Paso 7. Palabras que el modelo conoce
En este paso cruzamos el vocabulario con el modelo de vectores. La cercanía no puede decir nada de una palabra sin vector, y lo reportamos.

```python
no_vector = []
for word in vocabulary:  # por cada palabra que llega al piso
    if not nlp.vocab.has_vector(word):  # el modelo no guarda una lista de números para ella
        no_vector.append(word)  # la cercanía no puede leer esta palabra
print(f"Palabras sin vector en {MODEL}: {len(no_vector)} de {len(vocabulary)} ({len(no_vector) / len(vocabulary):.1%})")
print(no_vector)
```

Faltan siglas (*dalys*, *ylls*) y términos recientes (*covid*). La cercanía no ve esos pares. El conteo y el lift sí.

**Vectores compartidos.** El modelo mediano tiene unas 20.000 filas para 685.000 palabras, así que muchas palabras **comparten vector** y salen con coseno 1.0. El modelo grande da a cada una su propio vector.

La celda siguiente busca palabras con el mismo vector. Con el modelo grande no debería encontrar grupos. Esos pares van marcados con `shared_vector` y no cuentan como cercanía.

```python
def shared_vectors(vocab_words: list[str], nlp) -> list[list[str]]:
    """Agrupa las palabras que reciben exactamente el mismo vector del modelo.

    Qué hace: lee el vector de cada palabra y junta las palabras cuyo vector es idéntico.
    Eso pasa cuando apuntan a la misma fila de la tabla (key2row) y también cuando el
    modelo copió una fila en otra al recortar su vocabulario.
    Entrada: vocab_words, lista de palabras, y el modelo de spaCy cargado.
    Salida: lista de grupos (listas de 2 o más palabras con el mismo vector).
    """
    by_vector = {}
    for w in vocab_words:  # por cada palabra del vocabulario
        if nlp.vocab.has_vector(w):  # el modelo guarda una lista de números para ella
            by_vector.setdefault(nlp.vocab.get_vector(w).tobytes(), []).append(w)  # las de la misma lista quedan juntas
    groups = []
    for group in by_vector.values():  # por cada lista de números distinta
        if len(group) > 1:  # dos o más palabras recibieron esa misma lista
            groups.append(group)  # esas palabras comparten vector
    return groups


shared_groups = shared_vectors(vocabulary, nlp)
group_of = {}
for i, group in enumerate(shared_groups):  # por cada grupo que comparte vector
    for word in group:  # por cada palabra de ese grupo
        group_of[word] = i  # el número del grupo de esta palabra
print(f"Modelo {MODEL}: {len(shared_groups)} grupos de palabras con el mismo vector")
print(shared_groups[:5])
```

**Comprobar:**

En este paso comprobamos que faltan pocos vectores y que el modelo grande no comparte vectores.

```python
assert len(no_vector) < 0.02 * len(vocabulary)
assert MODEL == "en_core_web_md" or len(shared_groups) == 0
print("Vectores: OK")
```

---

## Parte 4. Modelado

### Pares frecuentes (soporte)
En este paso ordenamos los candidatos por **soporte**, la proporción de artículos con las dos palabras:

$\displaystyle s(A,B) = \frac{n(A,B)}{N}$

Lo mostramos como conteo $n(A,B)$: 10 de 317 artículos es 3,2 %.

```python
rows = []
for (word_a, word_b), count in candidates.items():  # por cada par que llega al piso
    rows.append((word_a, word_b, count))  # las dos palabras y en cuántos artículos aparecen juntas
table = pd.DataFrame(rows, columns=["word_a", "word_b", "support"])
table["pair"] = table["word_a"] + " + " + table["word_b"]  # el nombre del par, para leerlo en las tablas
table.sort_values("support", ascending=False).head(10)
```

Arriba quedan palabras muy generales, como *disease + health*. El soporte solo no distingue un patrón de dos palabras comunes. El lift hace esa corrección.

```python
top_support = table.nlargest(15, "support").iloc[::-1]
plt.figure(figsize=(7, 5))
plt.barh(top_support["pair"], top_support["support"], color="steelblue")
plt.axvline(FLOOR, color="gray", linestyle="--", label=f"umbral = {FLOOR}")  # el piso de 10 artículos
plt.xlabel("Artículos donde aparecen juntas")
plt.title("Los 15 pares con más soporte")
plt.legend()
plt.tight_layout()
plt.savefig(OUTPUTS_DIR / "m1_soporte.png", dpi=120)
plt.show()
```

**Comprobar:**

En este paso comprobamos que la tabla tiene un par por candidato y el soporte más alto.

```python
assert len(table) == len(candidates)
assert table["support"].max() == 84
print("Pares frecuentes: OK")
```

### Lift
En este paso comparamos cada par con lo esperado si sus palabras fueran **independientes**. El **lift** divide lo observado por lo esperado:

$\displaystyle \text{lift}(A,B) = \frac{P(A,B)}{P(A)\,P(B)} = \frac{n(A,B)\cdot N}{n(A)\cdot n(B)}$

Un lift de 1 es lo que da el azar. Un lift de 2 es el doble de lo esperado.

```python
def compute_lift(pair_support: int, n_a: int, n_b: int, n: int) -> float:
    """Calcula el lift de un par de palabras.

    Qué hace: divide el soporte observado del par por el soporte esperado si las dos
    palabras fueran independientes.
    Entrada: pair_support (soporte del par), n_a y n_b (textos con cada palabra) y n
    (total de textos).
    Salida: el lift (1 = independencia, más de 1 = aparecen juntas más de lo esperado).
    """
    return pair_support * n / (n_a * n_b)  # observado dividido por lo esperado si no tuvieran que ver


lifts = []
for word_a, word_b, count in zip(table["word_a"], table["word_b"], table["support"]):  # por cada par candidato
    lifts.append(compute_lift(count, word_count[word_a], word_count[word_b], N))  # cuántas veces lo esperado si las dos palabras no tuvieran que ver
table["lift"] = lifts
table.sort_values("lift", ascending=False).head(10)
```

Ahora suben expresiones del campo: *saharan + sub*, *fasting + plasma*, *cross + sectional*.
El lift crece cuando las dos palabras son raras.
El piso de 10 artículos es lo que impide que un par de dos resúmenes parezca enorme.

**Comprobar:**

En este paso comprobamos que el lift es positivo y el valor de *saharan + sub*.

```python
assert table["lift"].min() > 0
assert abs(table.loc[table["pair"] == "saharan + sub", "lift"].iloc[0] - 18.6) < 0.1
print("Lift: OK")
```

### Cercanía de las palabras
En este paso medimos si el modelo pone cerca las dos palabras de cada par. Palabras en contextos parecidos reciben vectores parecidos (**hipótesis distribucional**). Medimos la cercanía con el coseno:

$\displaystyle \cos(u,v) = \frac{u \cdot v}{\|u\|\,\|v\|}$

```python
def unit_vector(word: str, nlp) -> np.ndarray:
    """Devuelve el vector de una palabra dividido por su largo.

    Qué hace: lee el vector del modelo y lo normaliza para que mida 1.
    Entrada: word, la palabra, y el modelo de spaCy.
    Salida: vector numpy de largo 1.
    """
    v = nlp.vocab.get_vector(word)  # la lista de 300 números de esa palabra
    return v / np.linalg.norm(v)  # largo 1, para que el coseno sea el producto punto


VECTORS = {}
for word in vocabulary:  # por cada palabra que llega al piso
    if word not in no_vector:  # el modelo conoce la palabra
        VECTORS[word] = unit_vector(word, nlp)  # su lista de 300 números, con largo 1


def pair_cosine(a: str, b: str) -> float:
    """Coseno entre dos palabras del vocabulario, o NaN si alguna no tiene vector."""
    if a not in VECTORS or b not in VECTORS:
        return float("nan")
    return float(VECTORS[a] @ VECTORS[b])  # 1 si apuntan igual, 0 si no tienen nada en común


cosines = []
shared_flags = []
for word_a, word_b in zip(table["word_a"], table["word_b"]):  # por cada par candidato
    cosines.append(pair_cosine(word_a, word_b))  # qué tan parecidas son las dos listas de números
    same_group = word_a in group_of and group_of.get(word_a) == group_of.get(word_b)  # las dos palabras usan la misma lista
    shared_flags.append(same_group)  # esa cercanía no cuenta, porque es el mismo vector
table["cosine"] = cosines
table["shared_vector"] = shared_flags
table.sort_values("cosine", ascending=False).head(10)
```

Los pares más cercanos son variantes de una palabra (*estimate + estimates*) u opuestos del mismo contexto (*females + males*). La cercanía mide si dos palabras **se usan igual**, no si forman un tema.

También buscamos los **vecinos** de *obesity*, sin las palabras que comparten su vector.

```python
SEED_WORD = "obesity"  # buscamos las palabras que el modelo usa cerca de esta
same_vector = set()
for word in VECTORS:  # por cada palabra que el modelo conoce
    shares = SEED_WORD in group_of and group_of.get(word) == group_of.get(SEED_WORD)  # usa la misma lista que obesity
    if shares:
        same_vector.add(word)  # no entra como vecina, porque es el mismo vector
others = []
for word in sorted(same_vector):  # por cada palabra con esa misma lista
    if word != SEED_WORD:
        others.append(word)  # las otras palabras que comparten el vector de obesity
print(f"Palabras con el mismo vector que {SEED_WORD}: {others or 'ninguna'}")
neighbour_rows = []
for word in VECTORS:  # por cada palabra que el modelo conoce
    if word == SEED_WORD or word in same_vector:  # es obesity o usa su misma lista
        continue  # no es una vecina distinta
    neighbour_rows.append((pair_cosine(SEED_WORD, word), word))  # qué tan cerca está de obesity
neighbour_rows = sorted(neighbour_rows, reverse=True)
neighbours = neighbour_rows[:8]
for c, w in neighbours:
    print(f"{w:15s} {c:.2f}  (en {word_count[w]} artículos)")
```

**Comprobar:**

En este paso comprobamos que casi todos los pares tienen coseno y los vecinos de *obesity*.

```python
assert table["cosine"].notna().mean() > 0.95
assert MODEL == "en_core_web_md" or neighbours[0][1] in {"diabetes", "obese", "overweight"}
print("Cercanía: OK")
```

---

## Parte 5. Evaluación

La evaluación compara el soporte, el lift y la cercanía sobre los mismos artículos.

En los artículos reales, un par aparece en n de ellos. Luego armamos 100 copias de la colección completa. En cada copia intercambiamos palabras entre artículos. Cada artículo conserva su largo y cada palabra conserva su conteo. Lo que cambia es qué palabras quedan juntas. En la copia 1 el par aparece en m1 artículos, en la copia 2 en m2, y así hasta m100. Esos 100 conteos son lo que ese par haría por azar. Los ordenamos de menor a mayor. El percentil 95 es el conteo que deja a 95 de esas 100 copias en ese valor o por debajo. El par se conserva solo si n es mayor que ese conteo. Un conteo alto puede salir de dos palabras comunes que se encuentran por casualidad. Con más de 16.000 pares, unos 800 superarían ese corte por suerte. Por eso leemos desde los de mayor lift.

### Paso 1. Los pares que se conservan
En este paso armamos esas 100 copias y marcamos los pares cuyo n supera ese corte. Cada artículo es una canasta de palabras. Una copia intercambia palabras entre canastas.

```python
frequent_words = set(vocabulary)  # las palabras que aparecen en al menos 10 artículos
transactions = []
for words_here in word_sets:  # por cada artículo que entra al análisis
    basket = words_here & frequent_words  # su resumen, ya sin las palabras raras
    transactions.append(basket)  # la canasta de ese artículo


def p95(values: Sequence[float]) -> float:
    """Devuelve el percentil 95 de una lista, sin interpolar.

    Args:
        values: Conteos o cosenos de los que se quiere el corte.
    Returns:
        El valor que deja por debajo al 95% de la lista.
    """
    ordered = sorted(values)  # la lista de conteos, de menor a mayor
    rank = int(0.95 * len(ordered))  # el lugar que deja al 95% de los conteos en ese valor o por debajo
    if rank >= len(ordered):
        rank = len(ordered) - 1  # el último conteo, si la lista es corta
    return ordered[rank]  # ese conteo es el percentil 95


def swap_randomize(transactions: Sequence[set], n_swaps: int, rng: random.Random) -> list[set]:
    """Devuelve canastas nuevas con el mismo largo y los mismos conteos de palabras.

    Args:
        transactions: Un conjunto de palabras por artículo. No se modifica.
        n_swaps: Intentos de intercambio.
        rng: Generador con semilla, para repetir la corrida.
    Returns:
        Las canastas después de los intercambios.
    """
    rows = []
    for basket in transactions:  # por cada artículo
        rows.append(set(basket))  # una copia de las palabras de su resumen
    cells = []
    for i, basket in enumerate(rows):  # por cada copia
        for word in sorted(basket):  # por cada palabra de esa copia
            cells.append((i, word))  # un lugar donde esa palabra se puede intercambiar
    n_cells = len(cells)
    if n_cells < 2:
        return rows
    for _ in range(n_swaps):  # por cada intento de intercambio
        a = rng.randrange(n_cells)  # un lugar al azar
        b = rng.randrange(n_cells)  # otro lugar al azar
        t1, w1 = cells[a]  # el primer artículo y su palabra
        t2, w2 = cells[b]  # el segundo artículo y su palabra
        same_article = t1 == t2  # las dos palabras están en el mismo artículo
        same_word = w1 == w2  # es la misma palabra
        already_there = w2 in rows[t1] or w1 in rows[t2]  # el otro artículo ya tiene esa palabra
        if same_article or same_word or already_there:
            continue  # este intento no cambia qué palabras quedan juntas
        rows[t1].remove(w1)  # el primer artículo deja su palabra
        rows[t1].add(w2)  # y recibe la del segundo
        rows[t2].remove(w2)  # el segundo artículo deja su palabra
        rows[t2].add(w1)  # y recibe la del primero
        cells[a] = (t1, w2)  # el primer lugar ahora tiene la palabra recibida
        cells[b] = (t2, w1)  # el segundo lugar ahora tiene la palabra recibida
    return rows


def pair_counts(transactions: Sequence[set], pairs: Sequence[tuple], vocab: Sequence[str]) -> np.ndarray:
    """Cuenta en cuántos artículos aparece cada par.

    Args:
        transactions: Una canasta por artículo.
        pairs: Los pares que se quieren contar.
        vocab: Las palabras de esas canastas.
    Returns:
        Un conteo por par, en el mismo orden.
    """
    index = {}
    for j, word in enumerate(vocab):  # por cada palabra que vamos a contar
        index[word] = j  # la columna de esta palabra
    presence = np.zeros((len(transactions), len(vocab)), dtype=np.float32)
    for i, basket in enumerate(transactions):  # por cada artículo
        for word in basket:  # por cada palabra de su canasta
            if word in index:  # es una palabra que estamos contando
                presence[i, index[word]] = 1.0  # este artículo contiene esta palabra
    together = presence.T @ presence  # en cuántos artículos aparece cada par de palabras
    left = []
    right = []
    for word_a, word_b in pairs:  # por cada par candidato
        left.append(index[word_a])  # la columna de la primera palabra
        right.append(index[word_b])  # la columna de la segunda
    left = np.array(left, dtype=np.int64)
    right = np.array(right, dtype=np.int64)
    return together[left, right].astype(np.int64)  # el conteo de cada par, en el mismo orden


def swap_null_counts(
    transactions: Sequence[set],
    pairs: Iterable[tuple],
    n_samples: int = N_SAMPLES,
    swaps_per_one: int = SWAPS_PER_ONE,
    seed: int = SEED,
    progress_every: int = PROGRESS_EVERY,
) -> dict[tuple, list[int]]:
    """Arma las tablas al azar y anota el conteo de cada par.

    Args:
        transactions: Una canasta por artículo.
        pairs: Los pares candidatos.
        n_samples: Cuántas tablas al azar.
        swaps_per_one: Intentos de intercambio por cada palabra presente.
        seed: Semilla de la reordenación.
        progress_every: Cada cuántas tablas se imprime el avance. 0 calla el aviso.
    Returns:
        Para cada par, la lista de sus conteos en las tablas al azar.
    """
    pairs = list(pairs)
    vocab_words = set()
    for pair in pairs:  # por cada par candidato
        for word in pair:  # por cada una de sus dos palabras
            vocab_words.add(word)  # entra al vocabulario que vamos a reordenar
    for basket in transactions:  # por cada artículo
        for word in basket:  # por cada palabra de su canasta
            vocab_words.add(word)  # también entra, aunque no forme un par candidato
    vocab = sorted(vocab_words)
    n_ones = 0
    for basket in transactions:  # por cada artículo
        n_ones = n_ones + len(basket)  # cuántas palabras hay en total, para fijar los intentos de intercambio
    rng = random.Random(seed)
    samples = np.empty((n_samples, len(pairs)), dtype=np.int64)
    for s in range(n_samples):  # por cada una de las 100 copias
        shuffled = swap_randomize(transactions, swaps_per_one * n_ones, rng)  # una copia con las palabras intercambiadas
        samples[s] = pair_counts(shuffled, pairs, vocab)  # en cuántos artículos aparece cada par en esta copia
        if progress_every and (s + 1) % progress_every == 0:
            print(f"Tablas al azar: {s + 1} de {n_samples}", flush=True)
    counts = {}
    for j, pair in enumerate(pairs):  # por cada par candidato
        counts[pair] = samples[:, j].tolist()  # sus 100 conteos, uno por copia
    return counts


def kept_pairs(observed: dict[tuple, int], null: dict[tuple, list[int]]) -> dict[tuple, int]:
    """Devuelve los pares cuyo conteo real supera su percentil 95.

    Args:
        observed: Conteo real de cada par.
        null: Conteos del mismo par en las tablas al azar.
    Returns:
        Los pares conservados y su conteo real.
    """
    kept = {}
    for pair, count in observed.items():  # por cada par candidato
        cut = p95(null[pair])  # el percentil 95 de sus 100 conteos
        if count > cut:  # en los artículos reales aparece más veces que ese corte
            kept[pair] = count  # el par se conserva
    return kept


start = time.time()
null = swap_null_counts(transactions, candidates)
kept = kept_pairs(candidates, null)
print(f"Cien tablas al azar en {time.time() - start:.1f} s")

null_p95 = []
kept_flags = []
for word_a, word_b in zip(table["word_a"], table["word_b"]):  # por cada par candidato
    pair = (word_a, word_b)
    null_p95.append(p95(null[pair]))  # el percentil 95 de sus 100 copias
    kept_flags.append(pair in kept)  # verdadero si el conteo real supera ese corte
table["null_p95"] = null_p95
table["kept"] = kept_flags
table["kept_lift2"] = table["kept"] & (table["lift"] >= LIFT_MIN)  # se conserva y además aparece al menos el doble de lo esperado

kept_table = table[table["kept"]].sort_values("lift", ascending=False)
display(kept_table.head(20)[["pair", "support", "null_p95", "lift"]])
display(kept_table[kept_table["support"] >= 20].head(20)[["pair", "support", "null_p95", "lift"]])

by_luck = round(0.05 * len(candidates))  # con el corte del 95%, cerca del 5% pasaría por suerte
print(f"Pares conservados: {len(kept):,} de {len(candidates):,}.")
print(f"Unos {by_luck:,} pasarían por suerte. Leemos desde los de mayor lift.")
```

Con la semilla 7 salen 7.311 pares conservados, y 6.507 de ellos tienen lift de al menos 2.

**Comprobar:**

En este paso comprobamos cuántos pares se conservan y que cada uno supera su corte.

```python
assert len(kept) == 7311
assert all(table.loc[table["kept"], "support"] > table.loc[table["kept"], "null_p95"])
assert table["kept_lift2"].sum() == 6507
print("Pares conservados: OK")
```

### Paso 2. Dónde coinciden los tres métodos
En este paso comparamos los tres métodos en los mismos tres pares de la diapositiva.
El corte del coseno es el percentil 95 de 1.000 pares de palabras elegidos al azar.
*diabetes + obesity* queda en los tres.
*health + years* se repite en estos resúmenes y su cercanía no destaca.
*food + nutrition* se usan de forma parecida en otros textos.
Su conteo queda bajo el piso, así que el lift no se lee.
Un par que solo un método conserva no es el ganador.

```python
rng_cosine = random.Random(SEED)
words_with_vector = sorted(VECTORS)
random_cosines = []
for _ in range(1000):  # por cada par de palabras elegido al azar
    word_a, word_b = rng_cosine.sample(words_with_vector, 2)  # dos palabras que el modelo conoce
    share_vector = word_a in group_of and group_of.get(word_a) == group_of.get(word_b)  # usan la misma lista de números
    if not share_vector:  # son dos palabras distintas para el modelo
        random_cosines.append(pair_cosine(word_a, word_b))  # qué tan parecidas son sus listas
RANDOM_COSINE_P95 = p95(random_cosines)  # el percentil 95 de esas cercanías al azar
table["beats_cosine"] = (table["cosine"] > RANDOM_COSINE_P95) & ~table["shared_vector"]  # la cercanía supera ese corte y no es el mismo vector

TOP = 10
top_support = table[table["kept"]].nlargest(TOP, "support")["pair"].tolist()
top_lift = kept_table.nlargest(TOP, "lift")["pair"].tolist()
top_cosine = table[table["beats_cosine"]].nlargest(TOP, "cosine")["pair"].tolist()
comparison = pd.DataFrame({"Soporte": top_support, "Lift": top_lift, "Coseno": top_cosine}, index=range(1, TOP + 1))
display(comparison)


def focus_cosine(word_a: str, word_b: str) -> float:
    """Devuelve el coseno de dos palabras.

    Args:
        word_a: Primera palabra.
        word_b: Segunda palabra.
    Returns:
        El coseno, o un valor faltante si alguna palabra no tiene vector.
    """
    if word_a in VECTORS and word_b in VECTORS:
        return pair_cosine(word_a, word_b)
    vector_a = nlp.vocab.get_vector(word_a)  # la lista de números, aunque la palabra no esté en la tabla
    vector_b = nlp.vocab.get_vector(word_b)
    norm_a = float(np.linalg.norm(vector_a))
    norm_b = float(np.linalg.norm(vector_b))
    if norm_a == 0 or norm_b == 0:
        return float("nan")
    return float(vector_a @ vector_b / (norm_a * norm_b))


focus_pairs = [("diabetes", "obesity"), ("health", "years"), ("food", "nutrition")]
focus_labels = []
focus_papers = []
focus_lifts = []
focus_cosines = []
for word_a, word_b in focus_pairs:  # por cada par de la figura
    focus_labels.append(f"{word_a} + {word_b}")
    papers_with_both = 0
    for words_here in word_sets:  # por cada artículo
        has_both = word_a in words_here and word_b in words_here  # su resumen contiene las dos palabras
        if has_both:
            papers_with_both = papers_with_both + 1  # un artículo más con ese par
    focus_papers.append(papers_with_both)
    count_a = word_count.get(word_a, 0)  # artículos cuyo resumen contiene la primera palabra
    count_b = word_count.get(word_b, 0)  # artículos cuyo resumen contiene la segunda
    above_floor = papers_with_both >= FLOOR and count_a > 0 and count_b > 0  # el par llega al piso de 10
    if above_floor:
        focus_lifts.append(compute_lift(papers_with_both, count_a, count_b, N))  # cuántas veces lo esperado
    else:
        focus_lifts.append(np.nan)  # bajo el piso el lift no se lee
    focus_cosines.append(focus_cosine(word_a, word_b))  # qué tan parecidas son sus listas de números

fig, axes = plt.subplots(1, 3, figsize=(10.5, 3.4), sharey=True)
y = np.arange(len(focus_labels))
axes[0].barh(y, focus_papers, color="steelblue")
axes[0].axvline(FLOOR, color="gray", linestyle="--", label=f"umbral = {FLOOR}")  # el piso de 10 artículos
axes[0].set_xlabel("Artículos")
axes[0].legend(loc="lower right")
lift_ok = ~np.isnan(focus_lifts)
axes[1].barh(y[lift_ok], np.array(focus_lifts)[lift_ok], color="darkorange")
axes[1].axvline(1, color="gray", linestyle="--", label="lift = 1")  # lo esperado si las palabras no tuvieran que ver
axes[1].set_xlabel("Lift")
axes[1].legend(loc="lower right")
axes[2].barh(y, focus_cosines, color="seagreen")
axes[2].axvline(RANDOM_COSINE_P95, color="gray", linestyle="--", label="percentil 95")  # el corte de la cercanía
axes[2].set_xlabel("Coseno")
axes[2].legend(loc="lower right")
axes[0].set_yticks(y, focus_labels)
fig.tight_layout()
fig.savefig(OUTPUTS_DIR / "comparacion_metodos.png", dpi=120)
plt.show()
```

**Comprobar:**

En este paso comprobamos los tres pares de la figura y el corte del coseno.

```python
assert comparison.shape == (TOP, 3)
assert focus_papers == [19, 81, 9]
assert np.isnan(focus_lifts[2])
assert 0.2 < RANDOM_COSINE_P95 < 0.8
print("Comparación: OK")
```

### Paso 3. Guardar los patrones
En este paso guardamos `outputs/patrones_l2.csv`, una fila por par candidato.

```python
columns = ["pair", "support", "null_p95", "lift", "cosine", "kept", "kept_lift2", "beats_cosine", "shared_vector"]
patterns_path = OUTPUTS_DIR / "patrones_l2.csv"
table.sort_values("lift", ascending=False)[columns].to_csv(patterns_path, index=False)  # una fila por par, con las tres lecturas
print(f"Guardado: {patterns_path} ({len(table):,} filas)")
```

**Comprobar:**

En este paso comprobamos que el archivo tiene los mismos pares conservados.

```python
saved = pd.read_csv(patterns_path)
assert saved["kept"].sum() == len(kept)
print("patrones_l2.csv: OK")
```

---

## Parte 6. Despliegue

### Paso 1. Qué hace un patrón con la lista
En este paso decimos para qué sirve un par conservado. El par nombra un filtro: los artículos cuya descripción contiene las dos palabras. Conservado quiere decir que vale la pena mirarlo.

### Paso 2. Artículos para leer
En este paso armamos la lista de lectura resultante de esta lección. Un par de palabras suma un punto por cada método que lo conserva. El soporte cuenta si el par superó sus tablas reordenadas. El lift cuenta si además aparece al menos el doble de lo esperado. La cercanía cuenta si el coseno supera el corte de los pares al azar. La evidencia del artículo es la suma de esos puntos. Un par que conservan los tres métodos pesa más que un par que conserva uno solo. Ordenamos de mayor a menor evidencia. Una descripción larga puede contener más pares, así que el conteo también refleja el largo. La Lección 1 pide entre 10 y 30 artículos, así que mostramos como máximo 30. Esta lista usa solo los pares de hoy. Las lecciones siguientes agregan otras evidencias.

```python
scored_pairs = []
for row in table.itertuples(index=False):  # por cada par candidato
    if row.kept or row.kept_lift2 or row.beats_cosine:  # al menos un método lo conserva
        scored_pairs.append((row.word_a, row.word_b, row.kept, row.kept_lift2, row.beats_cosine))  # entra a la cuenta de la lista

reading_rows = []
for _, paper in papers.iterrows():  # por cada artículo
    words_here = words(paper["abstract"], STOP_WORDS)  # las palabras útiles de su resumen
    if len(words_here) < 5:
        continue  # el resumen tiene menos de 5 palabras útiles
    n_support = 0
    n_lift = 0
    n_cosine = 0
    for word_a, word_b, kept, kept_lift2, beats_cosine in scored_pairs:  # por cada par que algún método conserva
        has_both = word_a in words_here and word_b in words_here  # el resumen contiene las dos palabras
        if not has_both:
            continue  # este par no está en el resumen
        if kept:
            n_support = n_support + 1  # el soporte lo conserva
        if kept_lift2:
            n_lift = n_lift + 1  # el lift también lo conserva
        if beats_cosine:
            n_cosine = n_cosine + 1  # la cercanía también lo conserva
    evidencia = n_support + n_lift + n_cosine  # un punto por cada método que conserva un par del resumen
    if evidencia == 0:
        continue  # ningún método conserva un par de este resumen
    reading_rows.append({
        "title": paper["title"],
        "soporte": n_support,
        "lift": n_lift,
        "cercania": n_cosine,
        "evidencia": evidencia,
    })

reading = pd.DataFrame(reading_rows)
reading = reading.sort_values(["evidencia", "title"], ascending=[False, True])  # más evidencia primero
reading_list = reading.head(30)  # como máximo 30 artículos
reading_path = OUTPUTS_DIR / "lectura_l2.csv"
reading_list.to_csv(reading_path, index=False)
print(f"Artículos con alguna evidencia: {len(reading)}. En la lista: {len(reading_list)}.")
reading_list
```

**Comprobar:**

En este paso comprobamos que la lista tiene hasta 30 artículos, que está ordenada por la evidencia y que la evidencia es la suma de los tres métodos.

```python
assert len(reading) >= 10
assert len(reading_list) == min(30, len(reading))
assert reading_list["evidencia"].is_monotonic_decreasing
assert reading_list["evidencia"].min() > 0
three = reading_list["soporte"] + reading_list["lift"] + reading_list["cercania"]
assert (reading_list["evidencia"] == three).all()
print("Lista de lectura: OK")
```

<!-- end NOTEBOOK: -->
