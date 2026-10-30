<!-- NOTEBOOK: -->

## Instrucciones
 
**Propósito.** Cuaderno de grupo de la semana 1 (Lecciones 1 y 2). En los laboratorios el equipo del consejo decidió qué artículos de nutrición leer. Aquí su grupo hace lo mismo para **su departamento**, con artículos de Wikipedia en español. La decisión cambia: **qué artículos debe abrir primero una persona nueva** para ponerse al día con el trabajo del departamento. La lista es un punto de partida para leer. No es investigación que el consejo vaya a citar.
 
**Requisito.** Complete primero los cuadernos individuales [L1](https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-data-mining/l1-introduction.ipynb) y [L2](https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-data-mining/l2-patterns.ipynb). Aquí **adaptan** ese código. Cada celda `# SU CÓDIGO` dice qué celda del cuaderno individual seguir. No copie celdas sin entenderlas: el código de los artículos no sirve tal cual para Wikipedia, y esa diferencia es parte de la tarea.
 
**Cómo trabajar.** Cada paso empieza con **En este paso**. Los pasos con una celda `# SU CÓDIGO` terminan con una celda **Comprobar**. Algunos pasos vienen resueltos porque ya los practicaron en los cuadernos individuales. Si un `assert` falla, corrija su celda antes de seguir. Los nombres del código van en inglés, como en los cuadernos individuales. Los comentarios y las explicaciones pueden ir en español.
 
**Entrega Moodle (martes 10 nov 2026, 23:59 Colombia):** ZIP `week-1-<group_id>.zip` con `week-1-group-<group_id>.ipynb` (este cuaderno ejecutado y renombrado), `pregunta.json` y `outputs/patrones.csv`.
 
**Mapa del cuaderno**
 
| Parte | Fase CRISP-DM | Qué sale | Cuaderno a seguir |
|-------|---------------|----------|-------------------|
| 0 | Configuración | Grupo, parámetros, modelo, datos y línea base | Dado |
| 1 | Comprensión del negocio | `pregunta.json` del grupo | L1, Parte 1 |
| 2 | Comprensión de los datos | Perfil de la columna `lead` (dado) | L1, Parte 2 |
| 3 | Preparación de los datos | Conjuntos, conteos y vectores en español | L2, Parte 4 |
| 4 | Modelado | Pares por soporte, lift y coseno | L2, Parte 5 |
| 5 | Evaluación | Su línea base y los patrones conservados | L2, Parte 6 |
| 6 | Despliegue | Uso de un patrón y `outputs/patrones.csv` | L2, Parte 7 |
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
En este paso importamos las librerías y copiamos los parámetros de la Lección 2 **sin cambiarlos**. Todos los grupos usan la misma regla de soporte. Con unos 300 artículos el umbral queda entre 9 y 11.



```python
import json
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

DATA_DIR = Path("data")
OUTPUTS_DIR = Path("outputs")
DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

# Parámetros compartidos con la Lección 2 y el script de control (no cambiar)
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
```

### Paso 3. Modelo de vectores en español
En este paso cargamos `es_core_news_lg`, el modelo grande de spaCy para español. En Colab hay que descargarlo en cada sesión.
 
**Tiempo de instalación.** El archivo pesa 568 MB (603 MB ya instalado). Lo medimos en una máquina de prueba del curso con buena conexión, no en Colab: la descarga e instalación tomó unos 8 segundos y la carga con `spacy.load` 2,5 segundos. En Colab gratuito puede tardar más, según la conexión del momento. Calcule hasta un par de minutos. Si la descarga falla, la celda carga el modelo mediano `es_core_news_md` (unos 42 MB) e imprime cuál cargó. También puede elegir el mediano con `USE_MEDIUM_MODEL = True`.



```python
import importlib
import spacy

USE_MEDIUM_MODEL = False   # ponga True si la descarga del modelo grande falla siempre
MODELS = ["es_core_news_md"] if USE_MEDIUM_MODEL else ["es_core_news_lg", "es_core_news_md"]
UNUSED_PIPES = ["tok2vec", "tagger", "parser", "attribute_ruler", "lemmatizer", "ner", "morphologizer", "senter"]


def load_vector_model(names: list[str]):
    """Carga el primer modelo de la lista que se pueda instalar (igual que en la Lección 2).

    Si un modelo no está instalado, lo descarga. Si la descarga falla, pasa al siguiente.
    Devuelve (nlp, name) e imprime qué modelo cargó y cuánto tardó.
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
```

### Paso 4. Descargar el extracto del grupo
En este paso descargamos el archivo del grupo con la misma función de caché de los cuadernos individuales.



```python
BASE_URL = "https://cabrerac.github.io/assets/data/26-udenar-data-mining"


def download_data(name: str, folder: Path = DATA_DIR) -> Path:
    """Descarga un archivo de datos del curso una sola vez (igual que en L1 y L2)."""
    dest = folder / name
    if dest.is_file() and dest.stat().st_size > 0:
        print(f"Ya en caché: {dest}")
        return dest
    response = requests.get(f"{BASE_URL}/{name}", timeout=60)
    response.raise_for_status()
    dest.write_bytes(response.content)
    print(f"Descargado: {dest}")
    return dest


articles = pd.read_csv(download_data(FILENAME))
print(articles.shape)
articles[["title", "lead"]].head(3)
```

**Comprobar:**



```python
assert GROUP in EXTRACTS and MODEL in ("es_core_news_lg", "es_core_news_md")
assert support_floor(298) == 9 and {"title", "lead", "categories"} <= set(articles.columns)
print(f"Grupo {GROUP}, modelo {MODEL} y datos de {DEPARTMENT}: OK")
```

### Paso 5. La herramienta de la línea base (swap randomization)
En este paso definimos las funciones de la línea base de la L2, Parte 6. No hay que escribirlas. Son las del módulo compartido del curso, con el mismo código y con los docstrings y comentarios en español. Recuerde la idea: una tabla al azar que conserva el **largo de cada artículo** y el **soporte de cada palabra** (Gionis et al., 2007). Un intercambio mueve dos palabras entre dos artículos sin cambiar esos márgenes.



```python
# support_floor, p95, swap_randomize, pair_counts, swap_null_counts y kept_pairs: mismo código que scripts/data-mining-course/swap_randomization.py, salvo docstrings y comentarios en español.
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
    Con los artículos del curso tarda unos 16 s en el PC y unos 20 a 40 s en Colab gratuito.
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


toy = [{"a", "b"}, {"a", "b", "c"}, {"b", "c"}, {"a", "c"}]
toy_random = swap_randomize(toy, 20, random.Random(SEED))
print("Antes:  ", [sorted(t) for t in toy])
print("Después:", [sorted(t) for t in toy_random])
```

**Comprobar:**



```python
assert [len(t) for t in toy_random] == [len(t) for t in toy]
assert Counter(w for t in toy_random for w in t) == Counter(w for t in toy for w in t)
print("Línea base lista: OK")
```

---
 
## Parte 1. Comprensión del negocio
 
### Paso 1. La pregunta y los pasos
En este paso el grupo empieza su tarjeta, como en la **L1, Parte 1, Paso 3**. Use las claves `question` y `steps`. La decisión es otra que en el laboratorio: qué artículos debe abrir primero una persona nueva en **su** departamento.
 
**Pista:** cree un diccionario `question_card`. En `question` escriba la pregunta en una frase. En `steps` ponga los seis pasos de CRISP-DM con palabras del grupo.



```python
# SU CÓDIGO
```

**Comprobar:**



```python
assert {"question", "steps"} <= set(question_card)
assert len(question_card["steps"]) >= 5
print("Pregunta y pasos: OK")
```

### Paso 2. El estándar y el uso
En este paso el grupo escribe **antes de mirar resultados** cómo sabrá que la lista es buena. Piense en la persona nueva. ¿Cuántos artículos alcanza a abrir en su primera semana? ¿Qué no debe pasar? Por ejemplo, un artículo que está en el centro solo porque enlaza con todo es una alerta, no una elección automática.
 
**Pista:** agregue `standard` con números (`min_articles`, `max_articles` y una regla más que el grupo elija) y `use` con `may` y `may_not`, como en la L1.



```python
# SU CÓDIGO
```

**Comprobar:**



```python
assert {"min_articles", "max_articles"} <= set(question_card["standard"])
assert question_card["standard"]["min_articles"] < question_card["standard"]["max_articles"]
assert {"may", "may_not"} <= set(question_card["use"])
```

### Paso 3. Guardar la tarjeta
En este paso guardamos la tarjeta en `pregunta.json`, como en la **L1, Parte 1, Paso 4**. La celda viene resuelta. El nombre del archivo va en español porque es parte de la entrega. Las claves van en inglés.



```python
QUESTION_PATH = Path("pregunta.json")
QUESTION_PATH.write_text(json.dumps(question_card, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Guardado: {QUESTION_PATH}")
```

**Comprobar:**



```python
saved = json.loads(Path("pregunta.json").read_text(encoding="utf-8"))
assert {"question", "steps", "standard", "use"} <= set(saved)
print("pregunta.json del grupo: OK")
```

---
 
## Parte 2. Comprensión de los datos
 
Cada fila es un artículo de Wikipedia. El texto que usamos es `lead`, la entradilla del artículo: los párrafos antes del primer título.
 
### Paso 1. Forma y valores faltantes
En este paso miramos la forma de la tabla, sus columnas y los valores faltantes, como en la **L1, Parte 2, Pasos 2 y 3**. Los tres pasos de esta parte vienen resueltos, porque el perfil ya lo practicaron en la L1. Ejecútenlos y lean lo que sale.



```python
print(articles.shape)
print(articles.dtypes)
missing = articles.isna().sum()
missing[missing > 0]
```

### Paso 2. El largo de las entradillas
En este paso medimos el largo de `lead` en palabras, como en la **L1, Parte 2, Paso 4**. Lean algunas de las entradillas de menos de 20 palabras. ¿Son artículos cortos de verdad o páginas de desambiguación?



```python
articles["lead_words"] = articles["lead"].fillna("").str.split().str.len()
print(articles["lead_words"].describe().round(0))
short_leads = articles[articles["lead_words"] < 20]
print(f"\nEntradillas de menos de 20 palabras: {len(short_leads)}")
short_leads[["title", "lead"]].head(4)
```

### Paso 3. Tabla de perfil
En este paso armamos la tabla de perfil con `profile_column`, como en la **L1, Parte 2, Paso 8**. Una fila por columna, con tipo, vacíos, distintos y un ejemplo.



```python
def profile_column(series: pd.Series) -> dict:
    """Resume una columna en una fila de la tabla de perfil (igual que en la L1)."""
    non_missing = series.dropna()
    return {
        "dtype": str(series.dtype),
        "missing": int(series.isna().sum()),
        "distinct": int(series.nunique()),
        "example": str(non_missing.iloc[0])[:40] if len(non_missing) else "",
    }


profile = pd.DataFrame({col: profile_column(articles[col]) for col in articles.columns}).T
profile
```

**Las categorías no se usan para patrones.** La columna `categories` trae las etiquetas que pusieron los editores de Wikipedia. Si dos categorías se repiten juntas, eso es la taxonomía de los editores, no un patrón que su grupo encontró. Los patrones salen solo de `lead`.
 
---
 
## Parte 3. Preparación de los datos
 
### Lo que cambia con el idioma
Los cuadernos individuales trabajan con artículos científicos en inglés. Su grupo trabaja con Wikipedia en español. El método es el mismo, pero la preparación cambia. Esta tabla es el punto de partida de la Parte 3.
 
| Qué cambia | Laboratorio (artículos, inglés) | Grupo (Wikipedia, español) |
|------------|--------------------------------|----------------------------|
| Columna de texto | `abstract` | `lead` |
| Palabras vacías | `spacy.lang.en.stop_words` | `spacy.lang.es.stop_words` (ya trae "más", "también", "así") |
| Texto de relleno a quitar | Etiquetas del resumen (*background*, *methods*, *findings*, *interpretation*, *funding*), la línea de financiación y restos de direcciones web | El residuo "[cita requerida]", los espacios invisibles (`\u200b`) donde estaban las notas y restos de direcciones web |
| Modelo de vectores | `en_core_web_lg` (plan B `en_core_web_md`) | `es_core_news_lg` (plan B `es_core_news_md`) |
| Acentos | Casi no hay | Se conservan: "préstamo" y "prestamo" serían dos palabras |
| Umbral de soporte | `support_floor(n)`, 10 artículos | `support_floor(n)`, 9 a 11 artículos según el grupo |
 
Antes de seguir, miren el relleno de su extracto.



```python
with_citation_needed = articles["lead"].fillna("").str.contains("[cita requerida]", regex=False)
invisible = articles["lead"].fillna("").str.count("\u200b").sum()
print(f"Entradillas con [cita requerida]: {with_citation_needed.sum()}")
print(f"Espacios invisibles en total: {invisible}")
```

El residuo "[cita requerida]" aparece en pocas entradillas, menos que el umbral de soporte de cualquier grupo. Aun así lo quitamos: es formato de Wikipedia, no contenido. Con la limpieza, ningún par de esas palabras de formato llega a la tabla.
 
### Paso 1. La función `words` y las palabras vacías
En este paso preparen la función que convierte una entradilla en un conjunto de palabras, como en la **L2, Parte 4, Pasos 1 a 3**. La función `words` de la L2 ya quita "[cita requerida]". El patrón de letras `[^\W\d_]+` ya parte en los espacios invisibles y conserva los acentos. Lo que cambia es la lista de palabras vacías.
 
**Pista:** `from spacy.lang.es.stop_words import STOP_WORDS as STOP_WORDS_ES`. Arme `STOP_WORDS` con esa lista más `URL_TOKENS = {"http", "https", "www", "org"}`. Si encuentran otro relleno propio de su extracto, añádanlo y expliquen por qué en un comentario.



```python
# SU CÓDIGO
```

**Comprobar:**



```python
assert words("La pobreza [cita requerida] en https://www.cepal.org", STOP_WORDS) == {"pobreza", "cepal"}
assert "también" in STOP_WORDS
print("Palabras: OK")
```

**Relleno de su extracto (se califica la evidencia, no la elección).** Busquen dos palabras de relleno propias de su extracto, muestren en cuántas entradillas aparecen y decidan si las quitan. Si las quitan, añádanlas a `STOP_WORDS` y vuelvan a ejecutar la celda de `words`.



```python
# SU CÓDIGO: cuenten en cuántas entradillas aparece cada palabra
FILLER_WORDS = []   # sus dos palabras
FILLER_DECISION = """
Escriba aquí si las quitan y por qué, con los números que encontraron.
"""
print(FILLER_DECISION)
```

**Comprobar:**



```python
assert len(FILLER_WORDS) == 2
assert "Escriba aquí" not in FILLER_DECISION
print("Relleno del extracto: OK")
```

### Paso 2. Un conjunto de palabras por artículo
En este paso construyan `word_sets`, un conjunto por entradilla, y dejen fuera las que tienen menos de 5 palabras útiles. Calculen `N = len(word_sets)` y `FLOOR = support_floor(N)`. Miren también el largo: ¿cuántas palabras útiles tiene la entradilla más corta y la más larga?



```python
# SU CÓDIGO
```

**Comprobar:**



```python
assert N >= 290 and FLOOR == support_floor(N)
assert not any("requerida" in s for s in word_sets)
print(f"Conjuntos: OK ({N} artículos, umbral {FLOOR})")
```

### Paso 3. Conteo de palabras y de pares
En este paso cuenten en cuántos artículos aparece cada palabra y cada par, como en la **L2, Parte 4, Pasos 5 y 6**. Guarden `word_count`, `vocabulary` (la lista ordenada de palabras con soporte de `FLOOR` o más) y `candidates` (los pares con soporte de `FLOOR` o más, con `count_pairs`). Miren las 15 palabras más frecuentes. ¿Son del tema o son palabras generales de enciclopedia?



```python
# SU CÓDIGO
```

**Comprobar:**



```python
assert vocabulary == sorted(vocabulary) and all(word_count[w] >= FLOOR for w in vocabulary)
assert len(candidates) > 0 and min(candidates.values()) >= FLOOR
print(f"Conteos: OK ({len(vocabulary)} palabras, {len(candidates)} pares candidatos)")
```

### Paso 4. Palabras que el modelo conoce y vectores compartidos
En este paso crucen el vocabulario con el modelo, como en la **L2, Parte 4, Paso 7**. Reporten las palabras sin vector (`no_vector`) y ejecuten la revisión de vectores compartidos con `shared_vectors`. Guarden `shared_groups` y `group_of`.
 
Con `es_core_news_lg` no debería haber grupos. Con el mediano, unas pocas palabras comparten vector (por ejemplo *hambruna* y *hambre* en Pobreza, o *bipolar*, *psicosis* y *trastorno* en Salud mental). Sus pares salen con coseno 1.0, y ese 1.0 solo dice que el modelo no las distingue.



```python
# SU CÓDIGO
```

**Comprobar:**



```python
assert len(no_vector) < 0.05 * len(vocabulary)
assert MODEL == "es_core_news_md" or len(shared_groups) == 0
print(f"Vectores: OK ({len(no_vector)} palabras sin vector)")
```

---
 
## Parte 4. Modelado
 
Copien de la L2 y adapten:
 
| Qué copiar | Dónde está en L2 |
|------------|------------------|
| Tabla de pares con `support` y columna `pair` | Parte 5, M1 |
| `compute_lift` y la columna `lift` | Parte 5, M2 |
| `unit_vector`, `VECTORS`, `pair_cosine`, columnas `cosine` y `shared_vector` | Parte 5, M3 |
| Vecinos de una palabra semilla | Parte 5, M3 (elijan una palabra central de su departamento) |
 
### Paso 1. M1 y M2, soporte y lift
En este paso construyan `table`, con una fila por par candidato y las columnas `word_a`, `word_b`, `support`, `pair` y `lift`. Muestren los 10 pares con más soporte y los 10 con más lift. ¿Los de más soporte dicen algo del departamento o son palabras generales? Entre los de más lift, busquen expresiones de su campo (en la L2 salían *saharan + sub* y *fasting + plasma*).



```python
# SU CÓDIGO
```

**Comprobar:**



```python
assert {"word_a", "word_b", "support", "pair", "lift"} <= set(table.columns)
assert len(table) == len(candidates) and table["lift"].min() > 0
print(f"M1 y M2: OK (lift máximo {table['lift'].max():.1f})")
```

### Paso 2. M3, coseno y vecinos
En este paso agreguen las columnas `cosine` y `shared_vector`, y muestren los 10 pares más cercanos. Después elijan una palabra semilla central de su departamento y muestren sus 8 vecinos, sin contar las palabras que comparten vector con ella.



```python
# SU CÓDIGO
```

**Comprobar:**



```python
assert {"cosine", "shared_vector"} <= set(table.columns)
assert table["cosine"].notna().mean() > 0.9
print("M3: OK")
```

---
 
## Parte 5. Evaluación
 
### Paso 1. La línea base del grupo
En este paso el grupo **define su línea base**, como pide el proyecto. La referencia es la de la L2: swap randomization para soporte y lift, y pares de palabras al azar para el coseno. Pueden usarla, cambiarla o proponer otra si la justifican. Lo que no pueden hacer es conservar un patrón sin compararlo con algo.
 
Escriban en `BASELINE` qué conserva su azar (¿el largo de cada entradilla? ¿el soporte de cada palabra?) y por qué es justo para su extracto.



```python
BASELINE = """
Escriba aquí qué representa su línea base y por qué es justa para su extracto.
"""
print(BASELINE)
```

**Comprobar:**



```python
assert "Escriba aquí" not in BASELINE
print("Línea base descrita: OK")
```

### Paso 2. Calcular la línea base
En este paso calculen la línea base, como en la **L2, Parte 6, Pasos 1 y 4**. Con la referencia del curso: armen `transactions` (cada conjunto limitado al vocabulario), llamen `swap_null_counts(transactions, candidates)` y guarden el resultado en `null`. Agreguen a `table` la columna `null_p95`.
 
**Tiempo.** Con unas 300 entradillas tarda pocos segundos. En Colab gratuito calcule entre 5 y 15 s. La función imprime una línea cada 20 tablas (`random tables: 20 of 100`).
 
**Antes del azar, una lista corta.** Como en la **L2, Parte 6, Paso 3**, la celda siguiente (ya resuelta) muestra los 20 pares con más lift y los 20 con más lift entre los que tienen soporte de 20 o más. Después de calcular `kept`, vuelvan a mirarlas: ¿cuáles sobrevivieron al azar?



```python
shortlist = table.nlargest(20, "lift")[["pair", "support", "lift"]]
display(shortlist)
common = table[table["support"] >= 20].nlargest(20, "lift")[["pair", "support", "lift"]]
print(f"Pares con soporte de 20 o más: {(table['support'] >= 20).sum()} de {len(table)}")
display(common)
```



```python
# SU CÓDIGO
```

**Comprobar:**



```python
assert "null_p95" in table.columns
assert len(null) == len(candidates)
print(f"Línea base: OK (p95 mediano {table['null_p95'].median():.0f})")
```

### Paso 3. Patrones conservados
En este paso decidan qué se conserva, como en la **L2, Parte 6, Paso 4**. Un par se conserva cuando llega al umbral y su soporte real está **estrictamente por encima** del p95 de su azar. Agreguen la columna `kept` (`True` o `False`).
 
Lean el número con cuidado. Con varios cientos de pares, cerca del 5 % pasaría por pura suerte. Un par conservado **vale la pena mirarlo**. No está **probado**. La celda resuelta que sigue a la comprobación muestra la lista y el número.



```python
# SU CÓDIGO
```

**Comprobar:**



```python
assert table["kept"].dtype == bool and table["kept"].sum() > 0
assert (table.loc[table["kept"], "support"] > table.loc[table["kept"], "null_p95"]).all()
print(f"Conservados: OK ({table['kept'].sum()})")
```

La celda siguiente viene resuelta. Muestra los 20 conservados con más lift, con su p95, y los 20 primeros entre los que tienen soporte de 20 o más.



```python
kept_table = table[table["kept"]].sort_values("lift", ascending=False)
display(kept_table.head(20)[["pair", "support", "null_p95", "lift"]])
display(kept_table[kept_table["support"] >= 20].head(20)[["pair", "support", "null_p95", "lift"]])

print(f"Pares conservados: {len(kept_table)} de {len(table)}")
print(f"Muchos pares pasan. Con {len(table)} pruebas, unos {round(0.05 * len(table))} pasan por azar. Lea la lista desde arriba.")
kept_names = set(kept_table["pair"])
print(f"De la lista corta por lift sobreviven {shortlist['pair'].isin(kept_names).sum()} de {len(shortlist)}. De la lista con soporte de 20 o más, {common['pair'].isin(kept_names).sum()} de {len(common)}.")
```

**Lean tres pares (se califica la lectura).** Elijan tres pares de la lista, lean dos entradillas de cada uno y escriban si nombran un tema, una frase hecha o una fórmula.



```python
# SU CÓDIGO: muestren dos entradillas que contengan las dos palabras de cada par
PAIR_READING = """
Escriba aquí, para cada par, si nombra un tema, una frase hecha o una fórmula, y qué leyeron en las entradillas.
"""
print(PAIR_READING)
```

**Comprobar:**



```python
assert "Escriba aquí" not in PAIR_READING
print("Lectura de tres pares: OK")
```

### Paso 4. Un par que pasa todo y no dice nada
En este paso buscamos pares conservados que son fórmula y no contenido. En la L2 fue *background + methods*, las etiquetas del resumen. En Wikipedia, el formato de la página no llega a la tabla: "[cita requerida]" se limpió en la Parte 3, y aun sin limpiar aparece en menos entradillas que el umbral. "Referencias" o "enlaces externos" no están en las entradillas. Pero las entradillas tienen su propia fórmula: "El **término** X se **refiere** a...".
 
En el extracto de Pobreza (G1), *refiere + término* aparece en 15 entradillas, con un p95 del azar de unos 11 y un lift de 3,1. Pasa el umbral, supera al azar y destaca. Y solo dice que la entradilla es una definición. La celda siguiente busca pares así en su extracto.



```python
FORMULA_WORDS = {"término", "refiere", "denomina", "define", "conoce", "llama", "generalmente", "ejemplo", "forma", "tipo"}
formula = table[table["kept"] & (table["word_a"].isin(FORMULA_WORDS) | table["word_b"].isin(FORMULA_WORDS))]
print(f"Pares conservados con palabras de fórmula: {len(formula)}")
formula.nlargest(8, "lift")[["pair", "support", "null_p95", "lift"]]
```

Decidan qué hacer con ellos. Pueden añadir esas palabras a `STOP_WORDS` y volver a ejecutar desde la Parte 3, o dejarlas y marcarlas en la reflexión. Lo que no deben hacer es presentarlas como un tema del departamento. Escriban su decisión.



```python
FORMULA_DECISION = """
Escriba aquí qué hizo el grupo con los pares de fórmula y por qué.
"""
print(FORMULA_DECISION)
```

**Comprobar:**



```python
assert "Escriba aquí" not in FORMULA_DECISION
print("Pares de fórmula revisados: OK")
```

### Paso 5. Destacar y comparar los tres métodos
En este paso, como en la **L2, Parte 6, Pasos 7 a 9**: agreguen `kept_lift2` (conservado y con lift de al menos `LIFT_MIN`), calculen la línea base del coseno con 1.000 pares al azar (`RANDOM_COSINE_P95 = p95(random_cosines)`) y la columna `beats_cosine`, y armen la tabla comparativa con los 10 primeros pares de cada método.



```python
# SU CÓDIGO
```

**Comprobar:**



```python
assert not (table["kept_lift2"] & ~table["kept"]).any()
assert table["beats_cosine"].dtype == bool
print(f"Comparación: OK ({table['kept_lift2'].sum()} destacan)")
```

¿Qué método ve el departamento mejor? ¿Algún par destaca en M2 y es cercano en M3? Esos son los candidatos más fuertes para la persona nueva, y siguen siendo candidatos para mirar.

### Para ir más lejos: Benjamini y Hochberg (1995)
En este paso, que es opcional, miramos los conservados con otra regla. Esta celda no es parte de la regla del curso y no cambia `kept`. El procedimiento ordena los pares por su valor p (la parte de sus 100 tablas al azar que llegó a su soporte real) y controla la proporción de falsos descubrimientos. Con 100 tablas el valor p más chico es 1/101, así que la corrección es gruesa. Ejecútela solo si tiene `null` y `kept`.



```python
# Para ir más lejos: no cambia kept
p_values = sorted((1 + sum(v >= candidates[p] for v in null[p])) / (N_SAMPLES + 1) for p in candidates)
m = len(p_values)
bh_passed = max((rank for rank, p in enumerate(p_values, start=1) if p <= 0.05 * rank / m), default=0)
print(f"Pares que pasan Benjamini-Hochberg al 5 %: {bh_passed} de {m} (kept: {int(table['kept'].sum())})")
```
 
---
 
## Parte 6. Despliegue
 
### Paso 1. Cómo usará la persona nueva un patrón conservado
En este paso añadan a la tarjeta la clave `pattern_use`, como en la **L2, Parte 7, Paso 1**. Expliquen cómo un patrón conservado ayuda a elegir qué abrir primero (`how_it_enters`), qué cambiaría ese uso (`what_changes_it`) y tres ejemplos (`examples`). Guarden de nuevo `pregunta.json`.



```python
# SU CÓDIGO
```

**Comprobar:**



```python
saved = json.loads(Path("pregunta.json").read_text(encoding="utf-8"))
assert {"how_it_enters", "what_changes_it", "examples"} <= set(saved["pattern_use"])
print("Uso de patrones: OK")
```

### Paso 2. Guardar los patrones
En este paso guardamos `outputs/patrones.csv`, una fila por par candidato, con las columnas `pair`, `support`, `null_p95`, `lift`, `cosine`, `kept`, `kept_lift2`, `beats_cosine` y `shared_vector`. La celda viene resuelta.



```python
columns = ["pair", "support", "null_p95", "lift", "cosine", "kept", "kept_lift2", "beats_cosine", "shared_vector"]
patterns_path = OUTPUTS_DIR / "patrones.csv"
table.sort_values("lift", ascending=False)[columns].to_csv(patterns_path, index=False)
print(f"Guardado: {patterns_path} ({len(table)} filas)")
```

**Comprobar:**



```python
patterns = pd.read_csv(OUTPUTS_DIR / "patrones.csv")
assert {"pair", "support", "null_p95", "lift", "cosine", "kept", "kept_lift2"} <= set(patterns.columns)
print(f"patrones.csv: OK ({len(patterns)} filas)")
```

---
 
## Registro de contribución
 
Cada integrante añade **una línea** con una tarea concreta. Indiquen quién consolidó el ZIP.



```python
contribution_log = """
- Nombre Apellido: tarjeta de la pregunta y estándar
- Nombre Apellido: preparación en español y relleno
- Nombre Apellido: línea base y evaluación
- Nombre Apellido: despliegue y revisión final
Consolida el ZIP: Nombre Apellido
"""
print(contribution_log)
```

## Para la reflexión individual
 
La reflexión de la semana 1 va en `week-1-reflection-<apellido>-<inicial>.pdf` (miércoles 11 nov 2026, 23:59 Colombia), con la plantilla Word de la semana. Una pregunta para empezar: **¿qué parte del código de los artículos no sirvió tal cual para Wikipedia, y qué decidió el grupo en su lugar?**
 
| Archivo del ZIP `week-1-<group_id>.zip` | Descripción |
|-----------------------------------------|-------------|
| `week-1-group-<group_id>.ipynb` | Este cuaderno ejecutado |
| `pregunta.json` | La tarjeta del grupo con `pattern_use` |
| `outputs/patrones.csv` | Una fila por par candidato, con sus columnas de evaluación |



<!-- end NOTEBOOK: -->
