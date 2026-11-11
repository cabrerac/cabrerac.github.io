<!-- NOTEBOOK: -->

## Repaso de Python para este cuaderno

Este cuaderno utiliza los siguientes métodos de Python. Si ya los conoce, ejecute estas celdas rápido.

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
El **coseno** mide si dos vectores apuntan en la misma dirección. Vale 1 si son paralelos y 0 si no tienen nada en común.

```python
import numpy as np

u = np.array([1.0, 2.0, 0.0])
v = np.array([2.0, 4.0, 0.0])
cosine = u @ v / (np.linalg.norm(u) * np.linalg.norm(v))
assert abs(cosine - 1.0) < 1e-9
print(f"Coseno: {cosine:.2f}")
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

Hoy buscamos **patrones que se repiten** en los resúmenes (`abstract`).
La idea viene de las tiendas: Agrawal, Imielinski y Swami (1993) preguntaron qué productos se repiten juntos en los recibos.
Aquí la canasta es un resumen y los productos son sus palabras.
Un patrón es un par de palabras que aparece junto en muchos artículos.
La evaluación compara el soporte, el lift y la cercanía sobre los mismos artículos.

**Tres métodos, tres preparaciones.**

| Método | Pregunta | Preparación que necesita | Línea base |
|--------|----------|--------------------------|------------|
| M1. Pares frecuentes | ¿En cuántos artículos aparecen juntas dos palabras? | Un conjunto de palabras por artículo | Tablas al azar que conservan el largo de cada artículo y el soporte de cada palabra (swap randomization) |
| M2. Lift | ¿Aparecen juntas más de lo que esperaríamos si fueran independientes? | Conteo de pares y conteo de cada palabra sola | Independencia (lift 1) y las mismas tablas al azar |
| M3. Cercanía en un embedding | ¿Un modelo entrenado con mucho texto las pone cerca? | Palabras que el modelo conoce | Coseno de pares de palabras al azar |

**Qué hacer.** Ejecute las celdas de arriba hacia abajo. Cada paso empieza con **En este paso** y termina con una celda **Comprobar**.

**Mapa del cuaderno**

| Parte | Fase CRISP-DM | Qué sale |
|-------|---------------|----------|
| 1 | Comprensión del negocio | La pregunta de hoy, escrita en el cuaderno |
| 2 | Comprensión de los datos | Parámetros, modelo de vectores y los artículos en memoria |
| 3 | Preparación de los datos | Conjuntos de palabras, conteos y vectores |
| 4 | Modelado | Pares por soporte, lift y coseno |
| 5 | Evaluación | Comparación de los tres métodos y `outputs/patrones_l2.csv` |
| 6 | Despliegue | Cómo usaremos un patrón conservado |

**Carpetas.** La celda de configuración crea `data/` (datos descargados) y `outputs/` (tablas y gráficos).

---

## Parte 1. Comprensión del negocio

### Paso 1. La pregunta de esta lección
En este paso escribimos qué buscamos hoy. La decisión no cambia: qué artículos debe leer el colega nuevo.

| Pregunta | Respuesta para el laboratorio |
|----------|-------------------------------|
| ¿Qué buscamos? | Pares de palabras que se repiten en los resúmenes más de lo que daría el azar |
| ¿Con qué los medimos? | Soporte, lift y cercanía en un embedding |
| ¿Contra qué los comparamos? | Contra tablas al azar y contra la independencia |
| ¿Cómo entra un patrón en la lista? | Como un filtro con nombre, por ejemplo "artículos que contienen *fasting + plasma*" |

Un patrón no elige artículos. Es una pista que el equipo puede revisar.
La lista sigue siendo la de la Lección 1: entre 10 y 30 artículos.

---

## Parte 2. Comprensión de los datos

### Paso 1. Configuración
En este paso importamos las librerías, creamos las carpetas y fijamos los parámetros. No los cambie.

El **umbral de soporte** es una proporción de los artículos con un mínimo. Con 317 artículos da 10.

```python
import math          # techo (ceil) para el umbral de soporte
import random        # tablas al azar con semilla fija
import re            # partir el texto en palabras
import time          # medir cuánto tarda cada paso
from collections import Counter
from collections.abc import Iterable, Sequence
from itertools import combinations
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests

# Carpetas de trabajo
DATA_DIR = Path("data")
OUTPUTS_DIR = Path("outputs")
DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

# Parámetros del curso (no cambiar)
SUPPORT_SHARE = 0.03   # proporción de textos
SUPPORT_MIN = 5        # mínimo de textos
SWAPS_PER_ONE = 5      # intentos de intercambio por cada 1 de la tabla, en cada tabla al azar
N_SAMPLES = 100        # tablas al azar
SEED = 7
PROGRESS_EVERY = 20    # imprime una línea de avance cada 20 tablas (0 = en silencio)
LIFT_MIN = 2.0         # un patrón destaca si aparece al menos el doble de lo esperado


def support_floor(n_texts: int) -> int:
    """Soporte mínimo que necesita una palabra o un par: max(SUPPORT_MIN, ceil(SUPPORT_SHARE * n))."""
    return max(SUPPORT_MIN, math.ceil(SUPPORT_SHARE * n_texts))


print(f"Umbral para 317 artículos: {support_floor(317)}")
print(f"Umbral para 298 artículos: {support_floor(298)}")
```

**Comprobar:**

En este paso comprobamos que el umbral de soporte da 10 artículos para nuestra colección.

```python
assert support_floor(317) == 10
assert support_floor(100) == SUPPORT_MIN
print("Parámetros: OK")
```

### Paso 2. Modelo de vectores de palabras
En este paso cargamos el modelo de **spaCy** del Método 3, `en_core_web_lg`, de unos 400 MB. Da a cada palabra frecuente su propio vector.

**Tiempo.** Colab lo descarga en cada sesión. Calcule hasta un par de minutos.

**Si la descarga falla**, la celda carga el modelo mediano `en_core_web_md` (unos 33 MB). También puede elegirlo con `USE_MEDIUM_MODEL = True`. En la Parte 3, Paso 7, verá qué cambia.

```python
import importlib
import spacy

USE_MEDIUM_MODEL = False   # ponga True si la descarga del modelo grande falla siempre
MODELS = ["en_core_web_md"] if USE_MEDIUM_MODEL else ["en_core_web_lg", "en_core_web_md"]

# Solo usamos los vectores, así que no cargamos las otras piezas del modelo
UNUSED_PIPES = ["tok2vec", "tagger", "parser", "attribute_ruler", "lemmatizer", "ner", "morphologizer", "senter"]


def load_vector_model(names: list[str]):
    """Carga el primer modelo de spaCy de la lista que se pueda instalar.

    Qué hace: para cada nombre, intenta cargarlo. Si no está instalado, lo descarga
    con spacy.cli.download y vuelve a intentarlo. Si la descarga falla, pasa al siguiente.
    Entrada: names, lista de modelos en orden de preferencia (grande primero).
    Salida: (nlp, name) con el modelo cargado y su nombre.
    Por qué: en Colab el modelo se descarga en cada sesión y una conexión débil puede
    cortar la descarga del modelo grande. El mediano es un plan B que sí funciona.
    """
    for name in names:
        start = time.time()
        try:
            nlp = spacy.load(name, exclude=UNUSED_PIPES)
        except OSError:
            print(f"Descargando {name} (puede tardar unos minutos)...")
            try:
                spacy.cli.download(name)
                importlib.invalidate_caches()
                nlp = spacy.load(name, exclude=UNUSED_PIPES)
            except (Exception, SystemExit) as error:
                print(f"No se pudo instalar {name}: {error}")
                continue
        print(f"Modelo cargado: {name} en {time.time() - start:.1f} s")
        return nlp, name
    raise RuntimeError("No se pudo cargar ningún modelo de vectores. Revise la conexión.")


nlp, MODEL = load_vector_model(MODELS)
print(f"Vectores en el modelo: {nlp.vocab.vectors.shape[0]:,} filas de {nlp.vocab.vectors.shape[1]} dimensiones")
if MODEL == "en_core_web_md":
    print("Cargó el modelo mediano. M1, M2 y la línea base no cambian. M3 sí: muchas palabras comparten vector y sus vecinos y cosenos no coinciden con las diapositivas. Use M3 aquí solo para ver el problema de los vectores compartidos y repita el Paso 2 con el modelo grande cuando pueda.")
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


papers = pd.read_csv(download_data("nutricion-papers.csv"))
print(papers.shape)
papers[["title", "year", "cited_by_count"]].head(3)
```

Para los patrones solo usamos la columna `abstract`. Las citas ya ordenaron la colección en la Lección 1 y no deben volver a decidir.

**Comprobar:**

En este paso comprobamos la forma de los datos y que está la columna `abstract`.

```python
assert papers.shape == (320, 13)
assert "abstract" in papers.columns
print("Datos: OK")
```

---

## Parte 3. Preparación de los datos

Cada método pide algo distinto. M1 pide un conjunto de palabras por artículo, M2 además el conteo de cada palabra y M3 que el modelo conozca las palabras.

Cada artículo es una **transacción** y cada palabra es un **ítem**, como la canasta y sus productos.

### Paso 1. De texto a palabras
En este paso convertimos un resumen en un **conjunto de palabras**. Pasamos a minúsculas, quitamos las palabras de menos de 3 letras y las **palabras vacías** de spaCy ("the", "of", "and"...), que formarían pares sin significado.

```python
from spacy.lang.en.stop_words import STOP_WORDS as STOP_WORDS_EN

WORD_RE = re.compile(r"[^\W\d_]+")   # secuencias de letras (sin números ni guiones bajos)


def words(text: str, stop_words: set[str]) -> set[str]:
    """Convierte un texto en el conjunto de sus palabras útiles.

    Qué hace: pasa a minúsculas, quita el residuo "[cita requerida]" de Wikipedia,
    separa en palabras de letras y descarta las de menos de 3 letras y las palabras vacías.
    Entrada: text (un resumen o una entradilla) y stop_words, el conjunto de palabras vacías.
    Salida: un set con cada palabra una sola vez.
    Por qué: M1 y M2 solo preguntan si una palabra está en un texto, no cuántas veces.
    """
    text = (text or "").lower().replace("[cita requerida]", " ")
    return {w for w in WORD_RE.findall(text) if len(w) >= 3 and w not in stop_words}


example = papers.loc[0, "abstract"]
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

Contamos *background* y *methods* juntas y calculamos su lift (Parte 4).

```python
dirty_sets = [s for s in (words(t, STOP_WORDS_EN) for t in papers["abstract"]) if len(s) >= 5]
n_dirty = len(dirty_sets)
together = sum(1 for s in dirty_sets if {"background", "methods"} <= s)
with_background = sum(1 for s in dirty_sets if "background" in s)
with_methods = sum(1 for s in dirty_sets if "methods" in s)
filler_lift = together * n_dirty / (with_background * with_methods)
print(f"background + methods: {together} artículos, lift {filler_lift:.1f}")
print(f"bill + gates: {sum(1 for s in dirty_sets if {'bill', 'gates'} <= s)} artículos")
```

El par aparece en 77 artículos y casi triplica lo esperado por azar. Es puro formato, así que lo quitamos **antes** de minar.

```python
ABSTRACT_LABELS = {
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
for token in sorted(URL_TOKENS):
    print(f"{token:6s} en {sum(1 for s in dirty_sets if token in s)} resúmenes")

STOP_WORDS = set(STOP_WORDS_EN) | ABSTRACT_LABELS | URL_TOKENS
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

### Paso 4. Un conjunto de palabras por artículo (preparación de M1)
En este paso construimos la entrada de M1: un conjunto de palabras por artículo. Dejamos fuera los resúmenes con menos de 5 palabras útiles.

```python
word_sets = [words(t, STOP_WORDS) for t in papers["abstract"]]
word_sets = [s for s in word_sets if len(s) >= 5]
N = len(word_sets)
FLOOR = support_floor(N)

sizes = pd.Series([len(s) for s in word_sets])
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

### Paso 5. Conteo de cada palabra sola (preparación de M2)
En este paso contamos en **cuántos artículos** aparece cada palabra. El lift necesita este conteo.

Una palabra en menos de 10 artículos no puede formar un par en 10. Es la **propiedad Apriori**, y así descartamos miles de pares sin contarlos.

```python
word_count = Counter(w for s in word_sets for w in s)
vocabulary = sorted(w for w, c in word_count.items() if c >= FLOOR)

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
    Por qué: el soporte es la base de M1 y M2. Filtrar antes por palabra (Apriori)
    evita contar millones de pares que nunca llegarían al umbral.
    """
    pairs = Counter()
    for s in word_sets:
        frequent = sorted(w for w in s if word_count[w] >= floor)
        pairs.update(combinations(frequent, 2))
    return {pair: c for pair, c in pairs.items() if c >= floor}


candidates = count_pairs(word_sets, word_count, FLOOR)
print(f"Pares candidatos (soporte de {FLOOR} o más): {len(candidates):,}")
```

**Comprobar:**

En este paso comprobamos el número de pares candidatos y que todos llegan al umbral.

```python
assert len(candidates) == 16271
assert min(candidates.values()) >= FLOOR
print("Pares: OK")
```

### Paso 7. Palabras que el modelo conoce (preparación de M3)
En este paso cruzamos el vocabulario con el modelo de vectores. M3 no puede decir nada de una palabra sin vector, y lo reportamos.

```python
no_vector = [w for w in vocabulary if not nlp.vocab.has_vector(w)]
print(f"Palabras sin vector en {MODEL}: {len(no_vector)} de {len(vocabulary)} ({len(no_vector) / len(vocabulary):.1%})")
print(no_vector)
```

Faltan siglas (*dalys*, *ylls*) y términos recientes (*covid*). M3 no ve esos pares, M1 y M2 sí.

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
    Por qué: dos palabras con el mismo vector tienen coseno 1.0 por construcción.
    Ese número no mide cercanía y hay que leerlo aparte.
    """
    by_vector = {}
    for w in vocab_words:
        if nlp.vocab.has_vector(w):
            by_vector.setdefault(nlp.vocab.get_vector(w).tobytes(), []).append(w)
    return [group for group in by_vector.values() if len(group) > 1]


shared_groups = shared_vectors(vocabulary, nlp)
group_of = {w: i for i, group in enumerate(shared_groups) for w in group}
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

### M1. Pares frecuentes (soporte)
En este paso ordenamos los candidatos por **soporte**, la proporción de artículos con las dos palabras:

$\displaystyle s(A,B) = \frac{n(A,B)}{N}$

Lo mostramos como conteo $n(A,B)$: 10 de 317 artículos es 3,2 %.

```python
table = pd.DataFrame(
    [(a, b, c) for (a, b), c in candidates.items()],
    columns=["word_a", "word_b", "support"],
)
table["pair"] = table["word_a"] + " + " + table["word_b"]
table.sort_values("support", ascending=False).head(10)
```

Arriba quedan palabras muy generales, como *disease + health*. El soporte solo no distingue un patrón de dos palabras comunes. Eso lo resuelve M2.

```python
top_support = table.nlargest(15, "support").iloc[::-1]
plt.figure(figsize=(7, 5))
plt.barh(top_support["pair"], top_support["support"], color="steelblue")
plt.axvline(FLOOR, color="gray", linestyle="--", label=f"umbral = {FLOOR}")
plt.xlabel("Artículos donde aparecen juntas")
plt.title("M1. Los 15 pares con más soporte")
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
print("M1: OK")
```

### M2. Lift
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
    Por qué: el soporte premia a las palabras comunes. El lift corrige por la frecuencia
    de cada palabra sola.
    """
    return pair_support * n / (n_a * n_b)


table["lift"] = [
    compute_lift(c, word_count[a], word_count[b], N)
    for a, b, c in zip(table["word_a"], table["word_b"], table["support"])
]
table.sort_values("lift", ascending=False).head(10)
```

Ahora suben expresiones del campo: *saharan + sub*, *fasting + plasma*, *cross + sectional*.

**Por qué hace falta el umbral.** El lift crece con palabras raras. Veamos un umbral de 2 artículos.

```python
rare_pair_count = Counter()
for s in word_sets:
    rare_pair_count.update(combinations(sorted(w for w in s if word_count[w] == 2), 2))
rare = [(a, b) for (a, b), c in rare_pair_count.items() if c == 2]
print(f"Pares de palabras que solo aparecen en 2 artículos, siempre juntas: {len(rare):,}")
print(f"Lift de cada uno: {compute_lift(2, 2, 2, N):.1f}. Ejemplos: {rare[:4]}")
```

Más de 600 pares tendrían lift 158,5 solo por venir de dos resúmenes. Eso no es un patrón. El umbral exige 10 artículos.

**Comprobar:**

En este paso comprobamos que el lift es positivo y el valor de *saharan + sub*.

```python
assert table["lift"].min() > 0
assert abs(table.loc[table["pair"] == "saharan + sub", "lift"].iloc[0] - 18.6) < 0.1
print("M2: OK")
```

### M3. Cercanía en un embedding
En este paso medimos si el modelo pone cerca las dos palabras de cada par. Palabras en contextos parecidos reciben vectores parecidos (**hipótesis distribucional**). Medimos la cercanía con el coseno:

$\displaystyle \cos(u,v) = \frac{u \cdot v}{\|u\|\,\|v\|}$

```python
def unit_vector(word: str, nlp) -> np.ndarray:
    """Devuelve el vector de una palabra dividido por su largo.

    Qué hace: lee el vector del modelo y lo normaliza para que mida 1.
    Entrada: word, la palabra, y el modelo de spaCy.
    Salida: vector numpy de largo 1.
    Por qué: con vectores de largo 1, el coseno es solo el producto punto.
    """
    v = nlp.vocab.get_vector(word)
    return v / np.linalg.norm(v)


VECTORS = {w: unit_vector(w, nlp) for w in vocabulary if w not in no_vector}


def pair_cosine(a: str, b: str) -> float:
    """Coseno entre dos palabras del vocabulario, o NaN si alguna no tiene vector."""
    if a not in VECTORS or b not in VECTORS:
        return float("nan")
    return float(VECTORS[a] @ VECTORS[b])


table["cosine"] = [pair_cosine(a, b) for a, b in zip(table["word_a"], table["word_b"])]
table["shared_vector"] = [a in group_of and group_of.get(a) == group_of.get(b) for a, b in zip(table["word_a"], table["word_b"])]
table.sort_values("cosine", ascending=False).head(10)
```

Los pares más cercanos son variantes de una palabra (*estimate + estimates*) u opuestos del mismo contexto (*females + males*). El embedding mide si dos palabras **se usan igual**, no si forman un tema.

También buscamos los **vecinos** de *obesity*, sin las palabras que comparten su vector.

```python
SEED_WORD = "obesity"
same_vector = {w for w in VECTORS if SEED_WORD in group_of and group_of.get(w) == group_of[SEED_WORD]}
print(f"Palabras con el mismo vector que {SEED_WORD}: {sorted(same_vector - {SEED_WORD}) or 'ninguna'}")
neighbours = sorted(((pair_cosine(SEED_WORD, w), w) for w in VECTORS if w not in same_vector | {SEED_WORD}), reverse=True)[:8]
for c, w in neighbours:
    print(f"{w:15s} {c:.2f}  (en {word_count[w]} artículos)")
```

**Comprobar:**

En este paso comprobamos que casi todos los pares tienen coseno y los vecinos de *obesity*.

```python
assert table["cosine"].notna().mean() > 0.95
assert MODEL == "en_core_web_md" or neighbours[0][1] in {"diabetes", "obese", "overweight"}
print("M3: OK")
```

---

## Parte 5. Evaluación

La evaluación compara el soporte, el lift y la cercanía sobre los mismos artículos.
Un par se conserva cuando el método lo deja por encima de su propio corte.
El corte del soporte es el percentil 95 de las copias al azar.
El corte del coseno es el percentil 95 de pares al azar.

### Paso 1. Qué debe conservar el azar
En este paso decidimos qué es "el azar". Los datos son una tabla de ceros y unos: una fila por artículo y una columna por palabra. La tabla tiene dos **márgenes**:

- el margen de cada fila: cuántas palabras tiene el artículo, su **largo**,
- el margen de cada columna: en cuántos artículos aparece la palabra, su **soporte**.

Un azar justo conserva los dos. Si solo conserva el soporte, olvida que un resumen largo forma cientos de pares, y casi tres de cada cuatro pares pasarían.

La tabla lleva solo las palabras del vocabulario.

```python
frequent_words = set(vocabulary)
transactions = [s & frequent_words for s in word_sets]
lengths = pd.Series([len(t) for t in transactions])
print(f"Tabla: {len(transactions)} artículos x {len(vocabulary)} palabras, {lengths.sum():,} unos")
print(f"Largo de cada artículo (palabras frecuentes): mínimo {lengths.min()}, mediana {lengths.median():.0f}, máximo {lengths.max()}")
```

El artículo más largo tiene más de cien veces las palabras del más corto.

**Comprobar:**

En este paso comprobamos que la tabla conserva el soporte de cada palabra y la diferencia de largos.

```python
assert lengths.sum() == sum(word_count[w] for w in vocabulary)
assert lengths.max() > 50 * lengths.min()
print("Tabla de transacciones: OK")
```

### Paso 2. Un intercambio (swap)
En este paso vemos la **swap randomization** de Gionis, Mannila, Mielikäinen y Tsaparas (2007). Un intercambio:

1. Elige dos unos de la tabla: la palabra $w_1$ en el texto $t_1$ y la palabra $w_2$ en el texto $t_2$.
2. Si $t_1$ no tiene $w_2$ y $t_2$ no tiene $w_1$, cambia las palabras de texto: $t_1$ se queda con $w_2$ y $t_2$ con $w_1$.

Los dos márgenes no cambian. Después de muchos intercambios tenemos una tabla al azar y contamos sus pares.

Lea qué hace cada función en su docstring.

```python
# p95 y swap_randomize. pair_counts, swap_null_counts y kept_pairs van en el Paso 4.
def p95(values: Sequence[float]) -> float:
    """Percentil 95 por rango, sin interpolar. Es la misma regla de las diapositivas y de los cuadernos."""
    values = sorted(values)
    return values[min(len(values) - 1, int(0.95 * len(values)))]


def swap_randomize(transactions: Sequence[set], n_swaps: int, rng: random.Random) -> list[set]:
    """Devuelve una lista nueva de conjuntos con el mismo largo de cada texto y el mismo soporte de cada palabra.

    transactions: un conjunto de palabras por texto. No se modifica.
    n_swaps: número de intentos de intercambio. Los intentos que repetirían una palabra en un texto se saltan,
        así que el número real de intercambios es menor.
    rng: un random.Random, para poder repetir la corrida.
    """
    rows = [set(t) for t in transactions]
    # sorted(t): un conjunto de palabras no tiene un orden fijo de un proceso a otro (PYTHONHASHSEED).
    # Por eso ordenamos la lista inicial, para que SEED dé la misma corrida en todas partes.
    cells = [(i, w) for i, t in enumerate(rows) for w in sorted(t)]
    n_cells = len(cells)
    if n_cells < 2:
        return rows
    for _ in range(n_swaps):
        a = rng.randrange(n_cells)
        b = rng.randrange(n_cells)
        t1, w1 = cells[a]
        t2, w2 = cells[b]
        if t1 == t2 or w1 == w2 or w2 in rows[t1] or w1 in rows[t2]:
            continue
        rows[t1].remove(w1)
        rows[t1].add(w2)
        rows[t2].remove(w2)
        rows[t2].add(w1)
        cells[a] = (t1, w2)
        cells[b] = (t2, w1)
    return rows


toy = [{"bread", "milk"}, {"bread", "milk", "eggs"}, {"milk", "eggs"}, {"bread", "eggs"}]
toy_random = swap_randomize(toy, 20, random.Random(SEED))
print("Antes:  ", [sorted(t) for t in toy])
print("Después:", [sorted(t) for t in toy_random])
```

Las canastas cambiaron de contenido, pero los dos márgenes son los mismos.

**Comprobar:**

En este paso comprobamos que el intercambio conserva los dos márgenes de la tabla de ejemplo.

```python
assert [len(t) for t in toy_random] == [len(t) for t in toy]
assert Counter(w for t in toy_random for w in t) == Counter(w for t in toy for w in t)
print("Intercambio: OK")
```

### Paso 3. Una lista corta antes del azar
En este paso miramos los 20 pares con más lift, y después los de soporte 20 o más, también por lift.

La primera lista está cerca del umbral: el lift premia a los pares raros. La segunda tiene pares más generales.

```python
shortlist = table.nlargest(20, "lift")[["pair", "support", "lift"]]
display(shortlist)

common = table[table["support"] >= 20].nlargest(20, "lift")[["pair", "support", "lift"]]
print(f"Pares con soporte de 20 o más: {(table['support'] >= 20).sum():,} de {len(table):,}")
display(common)
```

**Comprobar:**

En este paso comprobamos el tamaño y el soporte de las dos listas cortas.

```python
assert len(shortlist) == 20 and shortlist["support"].min() >= FLOOR
assert common["support"].min() >= 20
print("Listas cortas: OK")
```

### Paso 4. Cien tablas al azar para nuestros artículos
En este paso construimos 100 tablas al azar (`N_SAMPLES`), con 5 intentos de intercambio por cada uno (`SWAPS_PER_ONE`). Cada uno de los 16.271 pares recibe 100 valores del azar.

`pair_counts` cuenta los pares, `swap_null_counts` arma las tablas y `kept_pairs` aplica la regla.

**Tiempo.** Es la celda más lenta, entre 20 y 40 s en Colab. Imprime una línea cada 20 tablas.

```python
def pair_counts(transactions: Sequence[set], pairs: Sequence[tuple], vocab: Sequence[str]) -> np.ndarray:
    """Número de textos que tienen las dos palabras, para cada par, con un solo producto de matrices."""
    index = {w: j for j, w in enumerate(vocab)}
    table = np.zeros((len(transactions), len(vocab)), dtype=np.float32)
    for i, t in enumerate(transactions):
        cols = [index[w] for w in t if w in index]
        table[i, cols] = 1.0
    together = table.T @ table
    left = np.array([index[a] for a, _ in pairs], dtype=np.int64)
    right = np.array([index[b] for _, b in pairs], dtype=np.int64)
    return together[left, right].astype(np.int64)


def swap_null_counts(
    transactions: Sequence[set],
    pairs: Iterable[tuple],
    n_samples: int = N_SAMPLES,
    swaps_per_one: int = SWAPS_PER_ONE,
    seed: int = SEED,
    progress_every: int = PROGRESS_EVERY,
) -> dict[tuple, list[int]]:
    """Conteos del azar para cada par, con tablas al azar por intercambios (swap randomization).

    transactions: un conjunto de palabras por texto, ya limitado a las palabras que llegan
        al umbral de soporte.
    pairs: los pares candidatos (a, b) que se prueban.
    Devuelve {par: [conteo en la tabla al azar 1, ..., conteo en la tabla al azar n_samples]}.
    Cada tabla al azar parte de la tabla observada y recibe
    swaps_per_one * (número de unos) intentos de intercambio.
    progress_every: imprime "random tables: k of n" cada tantas tablas (0 = en silencio).
    Con los artículos del curso tarda unos 20 a 40 s en Colab gratuito.
    """
    pairs = list(pairs)
    vocab = sorted({w for p in pairs for w in p} | {w for t in transactions for w in t})
    n_ones = sum(len(t) for t in transactions)
    rng = random.Random(seed)
    samples = np.empty((n_samples, len(pairs)), dtype=np.int64)
    for s in range(n_samples):
        shuffled = swap_randomize(transactions, swaps_per_one * n_ones, rng)
        samples[s] = pair_counts(shuffled, pairs, vocab)
        if progress_every and (s + 1) % progress_every == 0:
            print(f"random tables: {s + 1} of {n_samples}", flush=True)
    return {p: samples[:, j].tolist() for j, p in enumerate(pairs)}


def kept_pairs(observed: dict[tuple, int], null: dict[tuple, list[int]]) -> dict[tuple, int]:
    """Pares cuyo conteo observado está estrictamente por encima del percentil 95 de sus conteos al azar."""
    return {p: c for p, c in observed.items() if c > p95(null[p])}


start = time.time()
null = swap_null_counts(transactions, candidates)
kept = kept_pairs(candidates, null)
print(f"Cien tablas al azar en {time.time() - start:.1f} s")

table["null_p95"] = [p95(null[(a, b)]) for a, b in zip(table["word_a"], table["word_b"])]
table["kept"] = [(a, b) in kept for a, b in zip(table["word_a"], table["word_b"])]
print(f"Percentil 95 del azar: mediana {table['null_p95'].median():.0f}, de {table['null_p95'].min()} a {table['null_p95'].max()}")
```

```python
kept_table = table[table["kept"]].sort_values("lift", ascending=False)
display(kept_table.head(20)[["pair", "support", "null_p95", "lift"]])
display(kept_table[kept_table["support"] >= 20].head(20)[["pair", "support", "null_p95", "lift"]])

print(f"Pares conservados: {len(kept):,} de {len(candidates):,}")
print("Muchos pares pasan. Con 16 mil pruebas, unos 800 pasan por azar. Lea la lista desde arriba.")
kept_names = set(kept_table["pair"])
print(f"De la lista corta por lift sobreviven {shortlist['pair'].isin(kept_names).sum()} de 20. De la lista con soporte de 20 o más, {common['pair'].isin(kept_names).sum()} de 20.")
```

Con `SEED = 7` todos obtienen 7.311 pares conservados, con un p95 mediano de 14. Con otra semilla cambia en unas decenas.

**Comprobar:**

En este paso comprobamos el número de pares conservados y que cada uno supera su percentil 95.

```python
assert len(kept) == 7311
assert all(table.loc[table["kept"], "support"] > table.loc[table["kept"], "null_p95"])
assert len(kept) > 0.05 * len(candidates)
print("Línea base por swap randomization: OK")
```

### Paso 5. Un par visto de cerca
En este paso miramos el azar de un par común, *disease + health*, y de un par del tema, *children + obesity*.

```python
for pair in [("disease", "health"), ("children", "obesity")]:
    observed = candidates[pair]
    values = null[pair]
    verdict = "se conserva" if pair in kept else "no se conserva"
    print(f"{pair[0]} + {pair[1]}: real {observed}, azar promedio {np.mean(values):.1f}, p95 {p95(values)}. {verdict}")

plt.figure(figsize=(7, 3.5))
plt.hist(null[("disease", "health")], bins=15, color="lightgray", edgecolor="gray")
plt.axvline(p95(null[("disease", "health")]), color="darkorange", linestyle="--", label="percentil 95 del azar")
plt.axvline(candidates[("disease", "health")], color="steelblue", linewidth=2, label="soporte real")
plt.xlabel("Artículos con disease y health")
plt.ylabel("Tablas al azar")
plt.title("100 tablas al azar para disease + health")
plt.legend()
plt.tight_layout()
plt.savefig(OUTPUTS_DIR / "nulo_un_par.png", dpi=120)
plt.show()
```

*disease + health* aparece en 84 artículos y su p95 es 80. Pasa por poco y su lift es 1,3. *children + obesity* tiene soporte 11 y p95 8. Por eso leemos primero los de lift alto.

La línea naranja es el percentil 95. El par se conserva solo si el conteo real queda a la derecha.

### Paso 6. ¿Por qué pasan tantos pares?
En este paso leemos el número con cuidado. Con más de 16.000 pares, cerca del 5 %, unos 800, pasaría por suerte.

Por eso **conservado** quiere decir **vale la pena mirarlo**, no **probado**.

```python
by_luck = round(0.05 * len(candidates))
print(f"Pares que pasarían solo por suerte: unos {by_luck:,}")
print(f"Pares conservados: {len(kept):,}, unas {len(kept) / by_luck:.0f} veces lo que daría la suerte")
table[~table["kept"]].nlargest(5, "support")[["pair", "support", "null_p95", "lift"]]

plt.figure(figsize=(7, 3.5))
plt.bar(["pasarían por suerte", "conservados"], [by_luck, len(kept)], color=["lightgray", "steelblue"])
plt.ylabel("Pares en el umbral")
plt.title(f"{len(candidates):,} pares en el umbral")
plt.tight_layout()
plt.savefig(OUTPUTS_DIR / "suerte_y_conservados.png", dpi=120)
plt.show()
```

### Paso 7. Destacar frente a los otros patrones (M2)
En este paso ordenamos los conservados. Un par **destaca** si además su lift es al menos `LIFT_MIN` (2).

```python
table["kept_lift2"] = table["kept"] & (table["lift"] >= LIFT_MIN)
print(f"Conservados: {table['kept'].sum():,}. Conservados con lift de 2 o más: {table['kept_lift2'].sum():,}")
kept_table[["pair", "support", "null_p95", "lift", "cosine"]].head(10)
```

Deben salir 6.507. Arriba están *intervals + uis* y *saharan + sub*.

**Comprobar:**

En este paso comprobamos cuántos conservados destacan y que no queda texto de relleno entre ellos.

```python
assert table["kept_lift2"].sum() == 6507
assert not kept_table["pair"].str.contains("background|https|www").any()
print("Patrones conservados: OK")
```

### Paso 8. Línea base de pares al azar (M3)
En este paso construimos la línea base de M3: el percentil 95 del coseno de 1.000 pares al azar, sin los de vector compartido.

```python
rng_cosine = random.Random(SEED)
words_with_vector = sorted(VECTORS)
random_cosines = []
for _ in range(1000):
    a, b = rng_cosine.sample(words_with_vector, 2)
    if not (a in group_of and group_of.get(a) == group_of.get(b)):
        random_cosines.append(pair_cosine(a, b))
RANDOM_COSINE_P95 = p95(random_cosines)

table["beats_cosine"] = (table["cosine"] > RANDOM_COSINE_P95) & ~table["shared_vector"]
print(f"Coseno de pares al azar: mediana {np.median(random_cosines):.2f}, percentil 95 {RANDOM_COSINE_P95:.3f}")
print(f"Pares candidatos más cercanos que el azar: {table['beats_cosine'].sum():,}")
print(f"Pares con vector compartido (coseno 1.0 que no cuenta): {table['shared_vector'].sum()}")
```

**Comprobar:**

En este paso comprobamos que el percentil 95 del coseno al azar está en un rango razonable.

```python
assert 0.2 < RANDOM_COSINE_P95 < 0.8
print("Línea base de coseno: OK")
```

### Paso 9. Tabla comparativa de los tres métodos
En este paso ponemos los tres métodos lado a lado. Cada uno responde una pregunta distinta.

```python
TOP = 10
top_m1 = table[table["kept"]].nlargest(TOP, "support")["pair"].tolist()
top_m2 = kept_table.nlargest(TOP, "lift")["pair"].tolist()
top_m3 = table[table["beats_cosine"]].nlargest(TOP, "cosine")["pair"].tolist()

comparison = pd.DataFrame({"M1 soporte": top_m1, "M2 lift": top_m2, "M3 coseno": top_m3}, index=range(1, TOP + 1))
display(comparison)

in_all_three = table[table["kept_lift2"] & table["beats_cosine"]]
print(f"M1 y M2 comparten {len(set(top_m1) & set(top_m2))} de sus 10 primeros pares")
print(f"M2 y M3 comparten {len(set(top_m2) & set(top_m3))} de sus 10 primeros pares")
print(f"Pares que conservan los tres métodos: {len(in_all_three):,}")
in_all_three.nlargest(8, "lift")[["pair", "support", "lift", "cosine"]]
```

Las tres columnas no tienen que coincidir.
Un desacuerdo no elige un ganador.

En este paso dibujamos los tres pares de la diapositiva. *food + nutrition* queda bajo el umbral, así que no entra en `table` y hay que contarlo aparte. Su lift no se lee.

```python
def focus_cosine(a: str, b: str) -> float:
    """Devuelve el coseno de dos palabras.

    Usa el vector guardado cuando la palabra está en la tabla.
    Si no, lee el vector del modelo.
    Devuelve un valor faltante cuando una palabra no tiene vector.
    """
    if a in VECTORS and b in VECTORS:
        return pair_cosine(a, b)
    vector_a = nlp.vocab.get_vector(a)
    vector_b = nlp.vocab.get_vector(b)
    norm_a = float(np.linalg.norm(vector_a))
    norm_b = float(np.linalg.norm(vector_b))
    if norm_a == 0 or norm_b == 0:
        return float("nan")
    return float(vector_a @ vector_b / (norm_a * norm_b))


focus_pairs = [("diabetes", "obesity"), ("health", "years"), ("food", "nutrition")]
focus_labels = [f"{a} + {b}" for a, b in focus_pairs]
focus_papers = []
focus_lifts = []
focus_cosines = []
for a, b in focus_pairs:
    n_ab = sum(1 for s in word_sets if a in s and b in s)
    focus_papers.append(n_ab)
    n_a = word_count.get(a, 0)
    n_b = word_count.get(b, 0)
    if n_ab >= FLOOR and n_a and n_b:
        focus_lifts.append(compute_lift(n_ab, n_a, n_b, N))
    else:
        focus_lifts.append(np.nan)
    focus_cosines.append(focus_cosine(a, b))

fig, axes = plt.subplots(1, 3, figsize=(10.5, 3.4), sharey=True)
y = np.arange(len(focus_labels))
axes[0].barh(y, focus_papers, color="steelblue")
axes[0].axvline(FLOOR, color="gray", linestyle="--", label=f"umbral = {FLOOR}")
axes[0].set_xlabel("Artículos")
axes[0].legend(loc="lower right")
lift_ok = ~np.isnan(focus_lifts)
axes[1].barh(y[lift_ok], np.array(focus_lifts)[lift_ok], color="darkorange")
axes[1].axvline(1, color="gray", linestyle="--", label="lift = 1")
axes[1].set_xlabel("Lift")
axes[1].legend(loc="lower right")
axes[2].barh(y, focus_cosines, color="seagreen")
axes[2].axvline(RANDOM_COSINE_P95, color="gray", linestyle="--", label="percentil 95")
axes[2].set_xlabel("Coseno")
axes[2].legend(loc="lower right")
axes[0].set_yticks(y, focus_labels)
fig.tight_layout()
fig.savefig(OUTPUTS_DIR / "comparacion_metodos.png", dpi=120)
plt.show()
```

Cómo leer la figura:

- **Los tres:** *diabetes + obesity* es un candidato más fuerte.
- **Solo los conteos:** *health + years* se repite en estos resúmenes.
- **Solo la cercanía:** *food + nutrition* se usan de forma parecida en otros textos. El conteo queda bajo el umbral, así que el lift no se lee.
- Un par que solo un método conserva no es el ganador.

```python
top_lift = kept_table.nlargest(15, "lift").iloc[::-1]
plt.figure(figsize=(7, 5))
plt.barh(top_lift["pair"], top_lift["lift"], color="darkorange")
plt.axvline(LIFT_MIN, color="gray", linestyle="--", label=f"lift mínimo = {LIFT_MIN:.0f}")
plt.xlabel("Lift (veces lo esperado por independencia)")
plt.title("M2. Los 15 patrones conservados con más lift")
plt.legend()
plt.tight_layout()
plt.savefig(OUTPUTS_DIR / "m2_lift.png", dpi=120)
plt.show()
```

**Comprobar:**

En este paso comprobamos la forma de la tabla comparativa y que algún par destaca con dos métodos.

```python
assert comparison.shape == (TOP, 3)
assert len(in_all_three) > 0
assert focus_papers == [19, 81, 9]
assert np.isnan(focus_lifts[2])
print("Comparación: OK")
```

### Paso 10. Guardar los patrones
En este paso guardamos `outputs/patrones_l2.csv`, una fila por par. `kept` dice si superó al azar y `kept_lift2` si además destaca.

```python
columns = ["pair", "support", "null_p95", "lift", "cosine", "kept", "kept_lift2", "beats_cosine", "shared_vector"]
patterns_path = OUTPUTS_DIR / "patrones_l2.csv"
table.sort_values("lift", ascending=False)[columns].to_csv(patterns_path, index=False)
print(f"Guardado: {patterns_path} ({len(table):,} filas)")
```

**Comprobar:**

En este paso comprobamos que el archivo guardado tiene los mismos pares conservados.

```python
saved = pd.read_csv(patterns_path)
assert saved["kept"].sum() == len(kept)
print("patrones_l2.csv: OK")
```

### Paso 11. Para ir más lejos: Benjamini y Hochberg (1995)
En este paso, opcional, miramos los conservados con Benjamini y Hochberg, que controla la **proporción de falsos descubrimientos**. No cambia `kept`. Con 100 tablas el valor p más chico es 1/101, así que léalo como una segunda opinión.

```python
# Para ir más lejos: no cambia kept ni los números del curso
p_values = sorted((1 + sum(v >= candidates[p] for v in null[p])) / (N_SAMPLES + 1) for p in candidates)
m = len(p_values)
bh_passed = max((rank for rank, p in enumerate(p_values, start=1) if p <= 0.05 * rank / m), default=0)
print(f"Pares que pasan Benjamini-Hochberg al 5 %: {bh_passed:,} de {m:,} (conservados por la regla del curso: {len(kept):,})")
```

---

## Parte 6. Despliegue

### Paso 1. Cómo usaremos un patrón conservado
En este paso escribimos cómo entra un patrón.
Un patrón se vuelve un filtro con nombre, por ejemplo "artículos con *fasting + plasma*", que se suma a otros resultados.

| Qué | Respuesta |
|-----|-----------|
| Cómo entra | Un patrón conservado nombra un filtro: los artículos que contienen las dos palabras |
| Cómo se lee | Conservado quiere decir que vale la pena mirarlo, no que esté probado |
| Qué lo cambia | El patrón es formato o financiación. Deja de superar al azar con datos nuevos. El equipo cambia de tema |

El equipo explica por qué cada artículo está en la lista y qué resultados lo apoyan.
Un artículo puede tener varios, uno o ninguno, si el equipo lo justifica.

```python
first = kept_table.iloc[0]
covered = sum(1 for s in word_sets if {first["word_a"], first["word_b"]} <= s)
print(f"Ejemplo de filtro: {first['pair']} selecciona {covered} artículos")
```

Un filtro de 10 o 15 artículos cabe en el estándar de la Lección 1 (entre 10 y 30).

**Comprobar:**

En este paso comprobamos que el filtro de ejemplo llega al umbral.

```python
assert covered >= FLOOR
print("Despliegue: OK")
```

### Paso 2. Comprobación final
En este paso revisamos que el cuaderno dejó lo que la Lección 3 necesita.

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
    ("outputs/patrones_l2.csv", lambda: patterns_path.is_file()),
    ("Gráficos de la evaluación", lambda: all((OUTPUTS_DIR / f).is_file() for f in ["m1_soporte.png", "m2_lift.png", "nulo_un_par.png", "suerte_y_conservados.png", "comparacion_metodos.png"])),
    ("Patrones conservados", lambda: len(kept) > 0),
]
passed = sum(_check_ok(n, f) for n, f in checks)
print(f"\nL2_CHECKS={passed}/{len(checks)}")
if passed == len(checks):
    print("L2_OK. Siga con la Lección 3.")
```

<!-- end NOTEBOOK: -->
