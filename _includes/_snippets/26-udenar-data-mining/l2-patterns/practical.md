<!-- NOTEBOOK: -->

## Repaso de Python para este cuaderno
 
Este repaso es corto. Solo muestra las cuatro piezas de Python que usamos en la lección. Si ya las conoce, ejecute las celdas rápido y siga.
 
### Conjuntos con `set`
Un **conjunto** guarda elementos sin repetir. Nos sirve para decir qué palabras aparecen en un artículo, sin importar cuántas veces. El operador `&` devuelve lo que dos conjuntos tienen en común.



```python
a = {"obesity", "diet", "risk"}
b = {"diet", "risk", "children"}
print(a & b)          # palabras que están en los dos conjuntos
print(len(a | b))     # palabras distintas entre los dos
```

### Contar con `Counter` y formar pares con `combinations`
`Counter` cuenta cuántas veces aparece cada elemento. Con `most_common(k)` vemos los `k` más frecuentes. `itertools.combinations(lista, 2)` genera todos los pares posibles, una sola vez cada uno. Si la lista está ordenada, el par `("a", "b")` nunca aparece también como `("b", "a")`.



```python
from collections import Counter
from itertools import combinations

counts = Counter(["diet", "risk", "diet", "obesity", "diet"])
print(counts.most_common(2))
print(list(combinations(sorted({"risk", "diet", "obesity"}), 2)))
```

### Coseno con `numpy`
El **coseno** entre dos vectores mide si apuntan en la misma dirección. Vale 1 si son paralelos, 0 si no tienen nada en común. Es el producto punto dividido por el largo de cada vector.



```python
import numpy as np

u = np.array([1.0, 2.0, 0.0])
v = np.array([2.0, 4.0, 0.0])
cosine = u @ v / (np.linalg.norm(u) * np.linalg.norm(v))
assert abs(cosine - 1.0) < 1e-9
print(f"Coseno: {cosine:.2f}. Repaso de Python: OK")
```

---
 
## Instrucciones
 
**La historia.** Seguimos con el mismo equipo interno de la secretaría de salud de la Lección 1. Tiene una colección de 320 artículos sobre nutrición y debe decidir cuáles tiene que leer. En la Lección 1 escribimos la pregunta, los pasos, el estándar y el uso. Hoy damos el primer paso de minería: buscar **patrones que se repiten** en los resúmenes (`abstract`).
 
**La idea central.** Un patrón es un par de palabras que aparece junto en muchos artículos. Un solo artículo famoso no es un patrón. Un patrón vale la pena mirarlo cuando supera a una **línea base** (lo que veríamos por azar). Entre los que la superan, destacan los que aparecen mucho más de lo esperado.
 
**Tres métodos, tres preparaciones.** Cada método pide sus propios datos. Por eso la preparación va método por método.
 
| Método | Pregunta | Preparación que necesita | Línea base |
|--------|----------|--------------------------|------------|
| M1. Pares frecuentes | ¿En cuántos artículos aparecen juntas dos palabras? | Un conjunto de palabras por artículo | Tablas al azar que conservan el largo de cada artículo y el soporte de cada palabra (swap randomization) |
| M2. Lift | ¿Aparecen juntas más de lo que esperaríamos si fueran independientes? | Conteo de pares y conteo de cada palabra sola | Independencia (lift 1) y las mismas tablas al azar |
| M3. Cercanía en un embedding | ¿Un modelo entrenado con mucho texto las pone cerca? | Palabras que el modelo conoce | Coseno de pares de palabras al azar |
 
**Qué hacer.** Ejecute las celdas de arriba hacia abajo. Cada paso empieza con **En este paso** y termina con una celda **Comprobar**. Si un `assert` falla, revise la celda anterior antes de seguir. Los nombres del código están en inglés, como en todos los cuadernos del curso. Las explicaciones están en español.
 
**El sábado 7 nov.** Hacia las 09:20 seguimos en vivo con este cuaderno, hasta las 10:00. La meta en clase es ver el soporte, el lift y por qué un par se conserva. No hace falta terminar la Parte 6 en clase. Lo que falte se termina en casa. Ejecute la Parte 1 antes del sábado para que el modelo de vectores ya esté probado.
 
**Del laboratorio al proyecto.** Desde las 10:00 el cuaderno de grupo repite estos pasos con las entradillas de Wikipedia de su secretaría. Cada paso del cuaderno de grupo dice qué parte de este cuaderno adaptar.
 
**Mapa del cuaderno**
 
| Parte | Fase CRISP-DM | Qué sale |
|-------|---------------|----------|
| 1 | Configuración | Librerías, parámetros y modelo de vectores |
| 2 | Comprensión del negocio | `pregunta.json` de la Lección 1 |
| 3 | Comprensión de los datos | Los 320 artículos en memoria |
| 4 | Preparación de los datos | Conjuntos de palabras, conteos y vectores |
| 5 | Modelado | Pares por soporte, lift y coseno |
| 6 | Evaluación | Líneas base, tabla comparativa y `outputs/patrones_l2.csv` |
| 7 | Despliegue | Cómo usaremos un patrón conservado |
 
---
 
## Parte 1. Configuración
 
### Paso 1. Librerías, carpetas y parámetros
En este paso importamos las librerías y fijamos los parámetros que usa todo el cuaderno. Los parámetros son **los mismos** en este cuaderno y en el cuaderno de grupo. No los cambie aquí.
 
El **umbral de soporte** es un solo parámetro: una proporción de los artículos con un mínimo absoluto. Con 317 artículos da 10. Con un extracto de 298 artículos da 9. Así ningún grupo trabaja con una regla distinta.



```python
import json          # leer y escribir pregunta.json
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

# Parámetros compartidos con el cuaderno de grupo (no cambiar)
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



```python
assert support_floor(317) == 10
assert support_floor(100) == SUPPORT_MIN
print("Parámetros: OK")
```

### Paso 2. Modelo de vectores de palabras
En este paso cargamos el modelo de **spaCy** que usa el Método 3. Preferimos el modelo grande `en_core_web_lg`, porque da a cada palabra frecuente su propio vector.
 
**Tiempo de instalación.** En un Colab nuevo hay que descargarlo en cada sesión. El archivo pesa 401 MB. En Colab gratuito calcule hasta un par de minutos, según la conexión del momento.
 
**Si la descarga falla.** Con una conexión débil la descarga del modelo grande puede fallar. La celda intenta entonces el modelo mediano `en_core_web_md` (unos 33 MB). También puede elegirlo a propósito con `USE_MEDIUM_MODEL = True`. La celda imprime qué modelo cargó. En la Parte 4, Paso 7, verá qué cambia con el mediano.



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



```python
assert MODEL in ("en_core_web_lg", "en_core_web_md")
assert nlp.vocab.vectors.shape[1] == 300
print(f"Modelo {MODEL}: OK")
```

---
 
## Parte 2. Comprensión del negocio
 
### Paso 1. Recuperar la pregunta de la Lección 1
En este paso leemos `pregunta.json`, la tarjeta que escribimos en la Lección 1. Si abre este cuaderno en un Colab nuevo, el archivo no está. En ese caso la celda escribe la misma tarjeta para que pueda seguir.
 
La tarjeta nos recuerda **para qué** buscamos patrones. Un patrón no decide qué leer. Un patrón es una pista que se suma a otras en las lecciones siguientes.



```python
QUESTION_PATH = Path("pregunta.json")

if QUESTION_PATH.is_file():
    question_card = json.loads(QUESTION_PATH.read_text(encoding="utf-8"))
    print("pregunta.json leído de la Lección 1")
else:
    question_card = {
        "question": "¿Qué artículos de nutrición debe leer el equipo para su tema, y qué filtro los puso en la lista?",
        "steps": ["comprender el negocio", "comprender los datos", "preparar", "modelar", "evaluar", "desplegar"],
        "standard": {"min_papers": 10, "max_papers": 30, "max_share_citations_only": 0.5},
        "use": {
            "may": ["decidir qué artículos abrir primero para el trabajo del equipo"],
            "may_not": ["citar la lista como evidencia de la alcaldía", "elegir artículos solo por sus citas"],
        },
    }
    QUESTION_PATH.write_text(json.dumps(question_card, ensure_ascii=False, indent=2), encoding="utf-8")
    print("pregunta.json no estaba. Escribimos la tarjeta de la Lección 1.")

print(question_card["question"])
print("Estándar:", question_card["standard"])
```

**Comprobar:**



```python
assert {"question", "steps", "standard", "use"} <= set(question_card)
print("Pregunta: OK")
```

---
 
## Parte 3. Comprensión de los datos
 
### Paso 1. Descargar y cargar los artículos
En este paso descargamos `nutricion-papers.csv` del sitio del curso, como en la Lección 1. La función guarda el archivo en `data/` y no lo vuelve a descargar si ya está.



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

Cada fila es un artículo. Para los patrones solo usamos la columna `abstract`. El título, los temas y las citas no entran. Las citas ya ordenaron la colección (Lección 1) y no queremos que vuelvan a decidir por la puerta de atrás.
 
**Comprobar:**



```python
assert papers.shape == (320, 13)
assert "abstract" in papers.columns
print("Datos: OK")
```

---
 
## Parte 4. Preparación de los datos
 
Esta parte prepara los datos **para cada método**. Los tres métodos parten del mismo texto, pero cada uno pide algo distinto. M1 pide un conjunto de palabras por artículo. M2 pide además el conteo de cada palabra sola. M3 pide que el modelo conozca las palabras.
 
En el lenguaje de la minería de patrones, cada artículo es una **transacción** y cada palabra distinta es un **ítem**. Es la misma idea de la canasta del supermercado: la canasta es la transacción y los productos son los ítems.
 
### Paso 1. De texto a palabras
En este paso convertimos un resumen en un **conjunto de palabras**. Pasamos a minúsculas, separamos en palabras de letras, quitamos las palabras cortas (menos de 3 letras) y las **palabras vacías** de spaCy para inglés ("the", "of", "and"...). Las palabras vacías aparecen en casi todos los artículos y formarían pares sin significado.



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
    La misma función sirve para los artículos (inglés) y para Wikipedia (español).
    """
    text = (text or "").lower().replace("[cita requerida]", " ")
    return {w for w in WORD_RE.findall(text) if len(w) >= 3 and w not in stop_words}


example = papers.loc[0, "abstract"]
print(example[:300], "...")
print(sorted(words(example, STOP_WORDS_EN))[:20])
```

**Comprobar:**



```python
assert words("The diet and the RISK of obesity", STOP_WORDS_EN) == {"diet", "risk", "obesity"}
print("Palabras: OK")
```

### Paso 2. Texto de relleno: las etiquetas del resumen
En este paso buscamos **texto de relleno**. Muchas revistas piden resúmenes estructurados con etiquetas como *Background*, *Methods*, *Findings*, *Interpretation* y *Funding*. Además, decenas de artículos terminan con la misma línea de financiación (*Bill & Melinda Gates Foundation*). Esas palabras se repiten mucho, pero dicen cómo se escribió el resumen, no de qué trata.
 
Veamos qué pasa si no las quitamos. Contamos en cuántos artículos aparecen juntas *background* y *methods*, y calculamos su lift (lo explicamos en la Parte 5).



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

El par *background + methods* aparece en 77 artículos y casi triplica lo esperado por azar. Sería uno de los "patrones" más fuertes de la colección, y es puro formato. Por eso lo quitamos **antes** de minar. Añadimos las etiquetas y la línea de financiación a las palabras vacías.



```python
ABSTRACT_LABELS = {
    "background", "methods", "findings", "interpretation", "funding",
    "conclusions", "results", "objective", "objectives", "aims",
    "bill", "melinda", "gates", "foundation",
}
print(f"Etiquetas de resumen y financiación: {len(ABSTRACT_LABELS)} palabras")
```

**Comprobar:**



```python
assert together == 77
assert len(ABSTRACT_LABELS) == 14
print("Texto de relleno: OK")
```

### Paso 3. Restos de direcciones web
En este paso miramos otro tipo de relleno: pedazos de direcciones web. Algunos resúmenes terminan con un enlace al registro del ensayo o a los datos (`https://www.who.int/...`). Al partir el texto en palabras, el enlace deja *http*, *https*, *www* y *org*. Son palabras de formato, como las etiquetas, y no dicen nada del tema.



```python
URL_TOKENS = {"http", "https", "www", "org"}
for token in sorted(URL_TOKENS):
    print(f"{token:6s} en {sum(1 for s in dirty_sets if token in s)} resúmenes")

STOP_WORDS = set(STOP_WORDS_EN) | ABSTRACT_LABELS | URL_TOKENS
print(f"Palabras vacías: {len(STOP_WORDS_EN)} de spaCy + {len(ABSTRACT_LABELS)} de relleno + {len(URL_TOKENS)} de direcciones web")
```

Varias de estas aparecen en más de 10 resúmenes, así que pasarían el umbral y formarían pares entre ellas. Las quitamos junto con las palabras vacías. Desde aquí, `STOP_WORDS` es la lista que usa todo el cuaderno.
 
**Comprobar:**



```python
assert "background" not in words(example + " Background", STOP_WORDS)
assert not URL_TOKENS & words("see https://www.who.int and www.fao.org", STOP_WORDS)
print("Direcciones web: OK")
```

### Paso 4. Un conjunto de palabras por artículo (preparación de M1)
En este paso construimos la entrada de M1: una lista con un conjunto de palabras por artículo. Dejamos fuera los resúmenes con menos de 5 palabras útiles. Son portadas o notas sueltas, no resúmenes, y no pueden aportar pares.



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

Fíjese en el largo. Hay resúmenes con unas pocas palabras útiles y otros con cientos. Un resumen largo forma muchos pares por sí solo. Esto va a importar en la Parte 6, cuando preguntemos qué daría el azar.
 
**Comprobar:**



```python
assert N == 317
assert FLOOR == 10
print("Conjuntos: OK")
```

### Paso 5. Conteo de cada palabra sola (preparación de M2)
En este paso contamos en **cuántos artículos** aparece cada palabra. Este conteo es el que pide el lift, porque compara un par con sus dos palabras por separado.
 
Aplicamos ya el umbral. Una palabra que aparece en menos de 10 artículos no puede formar un par que aparezca en 10. Esta es la **propiedad Apriori**: un par nunca es más frecuente que la menos frecuente de sus palabras. Así descartamos miles de pares sin contarlos.



```python
word_count = Counter(w for s in word_sets for w in s)
vocabulary = sorted(w for w, c in word_count.items() if c >= FLOOR)

print(f"Palabras distintas: {len(word_count):,}")
print(f"Palabras en {FLOOR} artículos o más: {len(vocabulary):,}")
print(word_count.most_common(10))
```

**Comprobar:**



```python
assert len(vocabulary) == 870
assert all(word_count[w] >= FLOOR for w in vocabulary)
print("Conteo de palabras: OK")
```

### Paso 6. Conteo de pares
En este paso contamos, para cada par de palabras del vocabulario, en cuántos artículos aparecen juntas. Ese número es el **soporte** del par. Nos quedamos con los pares que llegan al umbral. Son los **candidatos** que evaluaremos.



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



```python
assert len(candidates) == 16271
assert min(candidates.values()) >= FLOOR
print("Pares: OK")
```

### Paso 7. Palabras que el modelo conoce (preparación de M3)
En este paso cruzamos el vocabulario con el modelo de vectores. Una palabra que el modelo no conoce no tiene vector, y M3 no puede decir nada de ella. Reportamos esas pérdidas en vez de esconderlas.



```python
no_vector = [w for w in vocabulary if not nlp.vocab.has_vector(w)]
print(f"Palabras sin vector en {MODEL}: {len(no_vector)} de {len(vocabulary)} ({len(no_vector) / len(vocabulary):.1%})")
print(no_vector)
```

Las palabras que faltan son siglas del campo (*dalys*, *ylls*) o términos muy recientes (*covid*). El modelo se entrenó con texto general anterior a la pandemia. Salen de la vista del embedding, pero no del soporte ni del lift. M3 no ve esos pares, M1 y M2 sí.
 
**Revisión de vectores compartidos.** Un modelo de spaCy guarda una tabla de vectores. Cada palabra apunta a una fila. Para ahorrar espacio, el modelo mediano `en_core_web_md` tiene unas 20.000 filas para unas 685.000 palabras, así que muchas palabras **comparten vector**. Dos palabras con el mismo vector tienen coseno 1.0 aunque signifiquen cosas opuestas. Con el mediano, *obesity* comparte vector con 18 palabras del vocabulario, entre ellas *diabetes*, *disease* y *health*. El modelo grande da a cada una su propio vector.
 
La celda siguiente agrupa las palabras del vocabulario que reciben exactamente el mismo vector. Con el modelo grande no debería encontrar grupos. Si cargó el modelo mediano, verá grupos. Los pares de un mismo grupo saldrán con coseno 1.0. Ese 1.0 no dice que las palabras se parezcan. Dice que el modelo no las distingue. Por eso los marcamos con `shared_vector` y no los contamos como cercanía en la Parte 6.



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



```python
assert len(no_vector) < 0.02 * len(vocabulary)
assert MODEL == "en_core_web_md" or len(shared_groups) == 0
print("Vectores: OK")
```

---
 
## Parte 5. Modelado
 
### M1. Pares frecuentes (soporte)
En este paso ordenamos los candidatos por **soporte**. El soporte de un par $A, B$ es la proporción de artículos donde aparecen las dos palabras:
 
$\displaystyle s(A,B) = \frac{n(A,B)}{N}$
 
Los artículos científicos reportan el soporte como proporción. Aquí lo mostramos como conteo $n(A,B)$, que es más fácil de leer: 10 de 317 artículos es una proporción de 3,2 %.



```python
table = pd.DataFrame(
    [(a, b, c) for (a, b), c in candidates.items()],
    columns=["word_a", "word_b", "support"],
)
table["pair"] = table["word_a"] + " + " + table["word_b"]
table.sort_values("support", ascending=False).head(10)
```

Los pares con más soporte son palabras muy generales: *disease + health*, *health + risk*. Aparecen juntas porque cada una aparece en casi todo. El soporte solo no distingue un patrón de dos palabras comunes. Ese es el problema que resuelve M2.



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



```python
assert len(table) == len(candidates)
assert table["support"].max() == 84
print("M1: OK")
```

### M2. Lift
En este paso comparamos cada par con lo que esperaríamos si sus palabras fueran **independientes**. Si fueran independientes, la probabilidad de verlas juntas sería el producto de sus probabilidades. El **lift** divide lo observado por lo esperado:
 
$\displaystyle \text{lift}(A,B) = \frac{P(A,B)}{P(A)\,P(B)} = \frac{n(A,B)\cdot N}{n(A)\cdot n(B)}$
 
Un lift de 1 es lo que da el azar. Un lift de 2 dice que el par aparece el doble de lo esperado.
 
Las herramientas de reglas de asociación (mlxtend, arules) muestran primero la **confianza**, la proporción de textos con A que también tienen B. La confianza ignora cuán común es B, así que aquí usamos soporte y lift.



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

Ahora suben pares con significado propio: *saharan + sub*, *fasting + plasma*, *cross + sectional*. Son expresiones del campo ("sub-Saharan Africa", "fasting plasma glucose", "cross-sectional study").
 
**Por qué hace falta el umbral.** El lift crece sin límite con palabras raras. Si dos palabras aparecen en un solo artículo, juntas, su lift es $N$, el máximo posible. Veamos qué pasaría con un umbral de 2 artículos.



```python
rare_pair_count = Counter()
for s in word_sets:
    rare_pair_count.update(combinations(sorted(w for w in s if word_count[w] == 2), 2))
rare = [(a, b) for (a, b), c in rare_pair_count.items() if c == 2]
print(f"Pares de palabras que solo aparecen en 2 artículos, siempre juntas: {len(rare):,}")
print(f"Lift de cada uno: {compute_lift(2, 2, 2, N):.1f}. Ejemplos: {rare[:4]}")
```

Más de 600 pares tendrían un lift de 158,5, ocho veces el más alto que vemos con el umbral, solo por venir de dos resúmenes. Eso es un artículo que destaca, no un patrón. El umbral de soporte exige que el par se repita en al menos 10 artículos distintos.
 
**Comprobar:**



```python
assert table["lift"].min() > 0
assert abs(table.loc[table["pair"] == "saharan + sub", "lift"].iloc[0] - 18.6) < 0.1
print("M2: OK")
```

### M3. Cercanía en un embedding
En este paso medimos si el modelo pone cerca las dos palabras de cada par. El modelo aprendió sus vectores de mucho texto general. La idea es la **hipótesis distribucional**: palabras que aparecen en contextos parecidos reciben vectores parecidos. Medimos la cercanía con el coseno:
 
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

Los pares más cercanos son variantes de una palabra (*estimate + estimates*) u opuestos que se usan en el mismo contexto (*increased + decreased*, *females + males*). El embedding mide si dos palabras **se usan igual**, no si forman un tema en estos artículos. Si cargó el modelo mediano, arriba de esta tabla verá pares con coseno 1.0 y `shared_vector` en `True`. Léalos como "el modelo no distingue estas palabras", no como "son sinónimos".
 
Otra forma de leer un embedding es buscar los **vecinos** de una palabra semilla. Tomamos *obesity*, el tema del equipo. Dejamos fuera las palabras que comparten vector con la semilla, porque su coseno 1.0 no es cercanía.



```python
SEED_WORD = "obesity"
same_vector = {w for w in VECTORS if SEED_WORD in group_of and group_of.get(w) == group_of[SEED_WORD]}
print(f"Palabras con el mismo vector que {SEED_WORD}: {sorted(same_vector - {SEED_WORD}) or 'ninguna'}")
neighbours = sorted(((pair_cosine(SEED_WORD, w), w) for w in VECTORS if w not in same_vector | {SEED_WORD}), reverse=True)[:8]
for c, w in neighbours:
    print(f"{w:15s} {c:.2f}  (en {word_count[w]} artículos)")
```

**Comprobar:**



```python
assert table["cosine"].notna().mean() > 0.95
assert MODEL == "en_core_web_md" or neighbours[0][1] in {"diabetes", "obese", "overweight"}
print("M3: OK")
```

---
 
## Parte 6. Evaluación
 
Un número alto no basta. Para conservar un patrón pedimos que **supere a su línea base**: que no sea lo que veríamos por azar. Entre los conservados, miramos primero los que **destacan**, los que aparecen al menos el doble de lo esperado.
 
### Paso 1. Qué debe conservar el azar
En este paso decidimos qué es "el azar" para nuestros artículos. Pensemos en los datos como una tabla de ceros y unos: una fila por artículo (transacción), una columna por palabra (ítem), un 1 si la palabra está en el artículo. La tabla tiene dos **márgenes**:
 
- el margen de cada fila: cuántas palabras tiene el artículo, su **largo**,
- el margen de cada columna: en cuántos artículos aparece la palabra, su **soporte**.
 
Un azar justo tiene que conservar los dos. Si solo conserva el soporte de cada palabra y la reparte en artículos al azar, olvida que un resumen largo forma cientos de pares por sí solo. Ese azar da muy pocas coincidencias, y casi cualquier par parece un patrón. Con ese azar, casi tres de cada cuatro pares candidatos pasaban la prueba.
 
Como solo las palabras del vocabulario pueden formar un par candidato, la tabla lleva solo esas palabras. El largo de un artículo es entonces su número de palabras frecuentes.



```python
frequent_words = set(vocabulary)
transactions = [s & frequent_words for s in word_sets]
lengths = pd.Series([len(t) for t in transactions])
print(f"Tabla: {len(transactions)} artículos x {len(vocabulary)} palabras, {lengths.sum():,} unos")
print(f"Largo de cada artículo (palabras frecuentes): mínimo {lengths.min()}, mediana {lengths.median():.0f}, máximo {lengths.max()}")
```

El artículo más largo tiene más de cien veces las palabras del más corto. El azar que usamos debe respetar esa diferencia.
 
**Comprobar:**



```python
assert lengths.sum() == sum(word_count[w] for w in vocabulary)
assert lengths.max() > 50 * lengths.min()
print("Tabla de transacciones: OK")
```

### Paso 2. Un intercambio (swap)
En este paso vemos la herramienta que conserva los dos márgenes: la **swap randomization** de Gionis, Mannila, Mielikäinen y Tsaparas (2007). Un intercambio hace esto:
 
1. Elige dos unos de la tabla: la palabra $w_1$ en el texto $t_1$ y la palabra $w_2$ en el texto $t_2$.
2. Si $t_1$ no tiene $w_2$ y $t_2$ no tiene $w_1$, cambia las palabras de texto: $t_1$ se queda con $w_2$ y $t_2$ con $w_1$.
 
Cada texto sigue con el mismo número de palabras y cada palabra sigue en el mismo número de textos. Después de muchos intercambios, la tabla es una tabla al azar con los mismos márgenes. Contamos los pares en esa tabla y obtenemos un valor de lo que daría el azar.
 
Esta celda define las funciones de la línea base. Lea qué hace cada una en su docstring. No hace falta memorizar el código.



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

Mire las dos tablas. Las canastas cambiaron de contenido, pero cada una tiene el mismo número de productos que antes, y cada producto está en el mismo número de canastas.
 
**Comprobar:**



```python
assert [len(t) for t in toy_random] == [len(t) for t in toy]
assert Counter(w for t in toy_random for w in t) == Counter(w for t in toy for w in t)
print("Intercambio: OK")
```

### Paso 3. Una lista corta antes del azar
En este paso miramos lo que ya tenemos, antes de preguntarle nada al azar. La primera lista son los 20 pares con más lift. La segunda toma solo los pares con soporte de 20 o más, que se apoyan en más artículos, y los ordena también por lift.
 
Fíjese en el soporte de la primera lista. Casi todos están cerca del umbral: el lift premia a los pares que aparecen poco. La segunda lista tiene pares más generales, pero cada uno se repite en muchos resúmenes. En el paso siguiente veremos cuáles de estos pares sobreviven al azar.



```python
shortlist = table.nlargest(20, "lift")[["pair", "support", "lift"]]
display(shortlist)

common = table[table["support"] >= 20].nlargest(20, "lift")[["pair", "support", "lift"]]
print(f"Pares con soporte de 20 o más: {(table['support'] >= 20).sum():,} de {len(table):,}")
display(common)
```

**Comprobar:**



```python
assert len(shortlist) == 20 and shortlist["support"].min() >= FLOOR
assert common["support"].min() >= 20
print("Listas cortas: OK")
```

### Paso 4. Cien tablas al azar para nuestros artículos
En este paso construimos 100 tablas al azar (`N_SAMPLES`). Cada una parte de la tabla real y recibe 5 intentos de intercambio por cada uno de la tabla (`SWAPS_PER_ONE`). En cada tabla contamos el soporte de los 16.271 pares candidatos. Así cada par tiene 100 valores de lo que daría el azar.
 
La celda define tres funciones más: `pair_counts` cuenta todos los pares de una vez con un producto de matrices, `swap_null_counts` arma las 100 tablas y `kept_pairs` aplica la regla.
 
**Tiempo.** Esta es la celda más lenta del cuaderno. En Colab gratuito calcule entre 20 y 40 s, menos de un minuto. Mientras trabaja, la celda imprime una línea cada 20 tablas (`random tables: 20 of 100`) para que vea que avanza.



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

**Una nota sobre el número exacto.** Con `SEED = 7` todos deben obtener el mismo número: 7.311 pares conservados, con un p95 mediano de 14. Para eso `swap_randomize` ordena las palabras de cada texto antes de empezar (`sorted(t)`): Python no guarda los conjuntos en un orden fijo, y sin ese orden la misma semilla daría tablas distintas en cada sesión. Con otra semilla el número cambia en unas decenas y los pares de arriba son los mismos. Lo que importa es el orden de magnitud y qué pares quedan arriba, no el último dígito.
 
**Comprobar:**



```python
assert len(kept) == 7311
assert all(table.loc[table["kept"], "support"] > table.loc[table["kept"], "null_p95"])
assert len(kept) > 0.05 * len(candidates)
print("Línea base por swap randomization: OK")
```

### Paso 5. Un par visto de cerca
En este paso miramos los 100 valores al azar de un par muy común, *disease + health*, y los comparamos con su soporte real. Hacemos lo mismo con un par del tema del equipo, *children + obesity*.



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

*disease + health* aparece en 84 artículos, el soporte más alto de la colección. Las dos palabras son tan comunes, y los resúmenes largos las juntan tan a menudo, que el azar ya da unos 72 en promedio. El par pasa, pero por poco: 84 contra un p95 de 80. Su lift es 1,3. Superar al azar no lo hace interesante. Por eso, entre los conservados, leemos primero los de lift alto. El par del tema, *children + obesity*, tiene un soporte chico (11), pero su azar es aún más chico (p95 8).

### Paso 6. ¿Por qué pasan tantos pares?
En este paso leemos el número con cuidado. Probamos más de 16.000 pares, cada uno contra su percentil 95. Aunque ningún par tuviera nada especial, cerca del 5 % pasaría por pura suerte. Eso son unos 800 pares.
 
Por eso leemos **conservado** como **vale la pena mirarlo**, no como **probado**. Un par conservado entra en la lista de cosas para revisar. No es una prueba de que las dos palabras formen un tema.



```python
by_luck = round(0.05 * len(candidates))
print(f"Pares que pasarían solo por suerte: unos {by_luck:,}")
print(f"Pares conservados: {len(kept):,}, unas {len(kept) / by_luck:.0f} veces lo que daría la suerte")
table[~table["kept"]].nlargest(5, "support")[["pair", "support", "null_p95", "lift"]]
```

Los descartados con más soporte son pares de palabras comunes, como *factors + health* o *health + including*: el azar ya explica lo que vemos.

### Paso 7. Destacar frente a los otros patrones (M2)
En este paso ordenamos los conservados. Un par **destaca** cuando, además de superar al azar, su lift es al menos `LIFT_MIN` (2): aparece al menos el doble de lo que daría la independencia. Son los primeros que el equipo debería mirar.



```python
table["kept_lift2"] = table["kept"] & (table["lift"] >= LIFT_MIN)
print(f"Conservados: {table['kept'].sum():,}. Conservados con lift de 2 o más: {table['kept_lift2'].sum():,}")
kept_table[["pair", "support", "null_p95", "lift", "cosine"]].head(10)
```

Deben salir 6.507 conservados con lift de 2 o más. Arriba están *intervals + uis* (intervalos de incertidumbre, del Global Burden of Disease) y *saharan + sub*.
 
**Comprobar:**



```python
assert table["kept_lift2"].sum() == 6507
assert not kept_table["pair"].str.contains("background|https|www").any()
print("Patrones conservados: OK")
```

### Paso 8. Línea base de pares al azar (M3)
En este paso construimos la línea base de M3. Tomamos 1.000 pares de palabras del vocabulario al azar y calculamos su coseno. El percentil 95 de esos cosenos es el valor que un par debe superar para contar como cercano. Dejamos fuera los pares con vector compartido, porque su coseno no mide cercanía.



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



```python
assert 0.2 < RANDOM_COSINE_P95 < 0.8
print("Línea base de coseno: OK")
```

### Paso 9. Tabla comparativa de los tres métodos
En este paso ponemos los tres métodos lado a lado sobre los mismos artículos. No es una competencia. Cada método responde una pregunta distinta y la tabla muestra qué ve cada uno.



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
print(f"Pares que destacan y además son cercanos en el embedding: {len(in_all_three):,}")
in_all_three.nlargest(8, "lift")[["pair", "support", "lift", "cosine"]]
```

Cómo leer la tabla:
 
- **M1** encuentra el vocabulario general de la colección. Útil para describirla, poco útil para filtrar.
- **M2** encuentra expresiones del campo. Es el método que más sirve al equipo, siempre con el umbral y la línea base.
- **M3** encuentra palabras que se usan igual en cualquier texto. Confirma un par de M2, pero sola no encuentra temas.
- Un par que destaca en M2 **y** es cercano en M3 destaca con dos métodos distintos. Es el candidato más fuerte para la decisión, y aun así es un candidato para mirar.



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



```python
assert comparison.shape == (TOP, 3)
assert len(in_all_three) > 0
print("Comparación: OK")
```

### Paso 10. Guardar los patrones
En este paso guardamos `outputs/patrones_l2.csv`. Una fila por par candidato, con las columnas que usaremos en las próximas lecciones. `kept` dice si el par superó al azar y `kept_lift2` si además destaca.



```python
columns = ["pair", "support", "null_p95", "lift", "cosine", "kept", "kept_lift2", "beats_cosine", "shared_vector"]
patterns_path = OUTPUTS_DIR / "patrones_l2.csv"
table.sort_values("lift", ascending=False)[columns].to_csv(patterns_path, index=False)
print(f"Guardado: {patterns_path} ({len(table):,} filas)")
```

**Comprobar:**



```python
saved = pd.read_csv(patterns_path)
assert saved["kept"].sum() == len(kept)
print("patrones_l2.csv: OK")
```

---
 
## Parte 7. Despliegue
 
### Paso 1. Cómo usaremos un patrón conservado
En este paso escribimos, en la tarjeta de la pregunta, cómo entra un patrón en la decisión. Un patrón no elige artículos. Un patrón se convierte en un **filtro con nombre**: "artículos que contienen *fasting + plasma*". Ese filtro se suma a los resultados de las lecciones siguientes (grupos, texto, enlaces). El equipo explica por qué cada artículo está en la lista y qué resultados lo apoyan. Un artículo puede tener varios resultados a favor, uno o ninguno, si el equipo lo justifica.
 
Y escribimos qué cambiaría ese uso. Si un patrón solo aparece por un formato de revista, como pasó con *background + methods*, se descarta. Si deja de superar al azar con datos nuevos, también. Si el equipo cambia de tema, cambian los patrones que importan.



```python
question_card["pattern_use"] = {
    "how_it_enters": "Cada patrón conservado define un filtro con nombre (artículos que contienen las dos palabras).",
    "reading": "Conservado quiere decir que vale la pena mirarlo, no que esté probado.",
    "rule": "El equipo explica por qué cada artículo está en la lista y qué resultados lo apoyan. Un artículo puede tener varios, uno o ninguno, si el equipo lo justifica.",
    "what_changes_it": [
        "el patrón resulta ser formato o financiación y no contenido",
        "el patrón ya no supera la línea base con datos nuevos",
        "el equipo cambia de tema",
    ],
    "examples": top_m2[:3],
}
QUESTION_PATH.write_text(json.dumps(question_card, ensure_ascii=False, indent=2), encoding="utf-8")

first = kept_table.iloc[0]
covered = sum(1 for s in word_sets if {first["word_a"], first["word_b"]} <= s)
print(f"Ejemplo de filtro: {first['pair']} selecciona {covered} artículos")
```

Un filtro de 10 o 15 artículos tiene el tamaño que pide el estándar de la Lección 1 (entre 10 y 30). Por eso un patrón puede ser una pieza útil de la lista final.
 
**Comprobar:**



```python
assert "pattern_use" in json.loads(QUESTION_PATH.read_text(encoding="utf-8"))
assert covered >= FLOOR
print("Despliegue: OK")
```

### Paso 2. Su turno
En este paso escribe en dos o tres frases qué par conservado le parece más útil para el equipo y qué revisaría antes de usarlo como filtro. Piense en el azar: ¿podría ser uno de los 800 que pasan por suerte?



```python
my_pair = """
Escriba aquí el par, por qué le sirve al equipo y qué revisaría.
"""
print(my_pair)
```

### Paso 3. Comprobación final
En este paso revisamos que el cuaderno completo dejó lo que la Lección 3 necesita.



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
    ("pregunta.json con uso de patrones", lambda: "pattern_use" in json.loads(QUESTION_PATH.read_text(encoding="utf-8"))),
    ("outputs/patrones_l2.csv", lambda: patterns_path.is_file()),
    ("Gráficos de M1, M2 y el par de cerca", lambda: all((OUTPUTS_DIR / f).is_file() for f in ["m1_soporte.png", "m2_lift.png", "nulo_un_par.png"])),
    ("Patrones conservados", lambda: len(kept) > 0),
]
passed = sum(_check_ok(n, f) for n, f in checks)
print(f"\nL2_CHECKS={passed}/{len(checks)}")
if passed == len(checks):
    print("L2_OK. Lleve sus patrones al sábado. En el cuaderno de grupo hará lo mismo con Wikipedia, en español.")
```

### Para ir más lejos: Benjamini y Hochberg (1995)
En este paso, que es opcional, miramos los conservados con otra regla. Esta celda no es parte de la regla del curso y no cambia `kept`. Si quiere ir más allá de "unos 800 por suerte", el procedimiento de Benjamini y Hochberg ordena los pares por su valor p y controla la **proporción de falsos descubrimientos** entre los que pasan. El valor p de un par es la parte de sus 100 tablas al azar que llegó a su soporte real. Con 100 tablas el valor p más chico posible es 1/101, así que la corrección es gruesa. Léala como una segunda opinión.



```python
# Para ir más lejos: no cambia kept ni los números del curso
p_values = sorted((1 + sum(v >= candidates[p] for v in null[p])) / (N_SAMPLES + 1) for p in candidates)
m = len(p_values)
bh_passed = max((rank for rank, p in enumerate(p_values, start=1) if p <= 0.05 * rank / m), default=0)
print(f"Pares que pasan Benjamini-Hochberg al 5 %: {bh_passed:,} de {m:,} (conservados por la regla del curso: {len(kept):,})")
```



<!-- end NOTEBOOK: -->
