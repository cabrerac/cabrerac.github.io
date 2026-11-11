<!-- NOTEBOOK: -->

## Instrucciones

**Propósito.** Cuaderno de grupo de la semana 1 (Lecciones 1 y 2). Su grupo es un equipo interno de una alcaldía y trabaja para una secretaría. El producto del proyecto es una lista de artículos para los nuevos integrantes del equipo.

**Esta semana.** El grupo escribe la pregunta en este cuaderno y genera `outputs/patrones.csv` (los pares de palabras con soporte, lift y cercanía). La evaluación compara los tres métodos sobre las mismas descripciones de los artículos. El archivo de pares es el resultado de la primera iteración del proyecto.

**Antes de empezar.** Ejecuten primero los cuadernos individuales de las Lecciones 1 y 2. Este cuaderno lo escribe el grupo. Adapten ese trabajo. No peguen sin entender.

**Datos de entrada.** El archivo de su secretaría: G1 Agricultura, G2 Salud mental, G3 Medio ambiente, G4 Inclusión Social y G5 Vivienda. Cada fila es un artículo de Wikipedia en español. El texto para los patrones es la columna `lead`, la **descripción** del artículo.

**Materiales.** [L1 Introducción](https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-data-mining/l1-introduction.ipynb) y [L2 Patrones](https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-data-mining/l2-patterns.ipynb).

**Pregunta del grupo.** ¿Qué artículos de su secretaría debe leer primero una persona nueva en el equipo? Comparen los pares de las descripciones con soporte, lift y cercanía.

**Mapa del cuaderno**

| Ejercicio | Tema | Entregable clave |
|-----------|------|------------------|
| **0** | Configuración | Grupo, datos, parámetros, librerías y modelo de vectores |
| **1** | Comprensión del negocio | La pregunta y el problema, en texto, para el documento de requerimientos |
| **2** | Comprensión de los datos | Perfil de la columna `lead` |
| **3** | Preparación de los datos | Conjuntos de palabras, conteos y vectores |
| **4** | Modelado | Pares por soporte, lift y coseno |
| **5** | Evaluación | Comparación de soporte, lift y cercanía |
| **6** | Despliegue | Uso de un patrón y `outputs/patrones.csv` |

---

## Ejercicio 0. Configuración

### Paso 0.1. Grupo y datos

En este paso eligen el grupo y descargan el archivo de su proyecto desde el sitio web del curso.

Cambien la variable `GROUP` para descargar el archivo asignado.

```python
from pathlib import Path

import pandas as pd
import requests

GROUP = "G1"   # cambie a G2, G3, G4 o G5
EXTRACTS = {"G1": ("Agricultura", "agricultura.csv"), "G2": ("Salud mental", "salud-mental.csv"), "G3": ("Medio ambiente", "medio-ambiente.csv"),
            "G4": ("Inclusión Social", "inclusion-social.csv"), "G5": ("Vivienda", "vivienda.csv")}
SECRETARIAT, FILENAME = EXTRACTS[GROUP]
Path("outputs").mkdir(exist_ok=True)
path = Path("data") / FILENAME
path.parent.mkdir(exist_ok=True)
if not path.is_file():   # descarga una sola vez
    path.write_bytes(requests.get(f"https://cabrerac.github.io/assets/data/26-udenar-data-mining/{FILENAME}", timeout=60).content)
articles = pd.read_csv(path)
print(f"Grupo {GROUP}: secretaría de {SECRETARIAT}, {len(articles)} artículos")
```

### Paso 0.2. Parámetros, librerías y modelo de vectores

En este paso se deben definir los parámetros, las importaciones y el modelo de vectores a utilizar. El modelo de español es `es_core_news_lg`.

```python
# SU CÓDIGO. Paso 0.2: parámetros, rutas de la entrega, importaciones, support_floor, load_vector_model y nlp, MODEL en español

```

**Listo cuando:**
- Los parámetros tienen los valores de la Lección 2.
- `PATTERNS_PATH` es `outputs/patrones.csv`.
- `nlp` y `MODEL` cargan un modelo de español: `MODELS = ["es_core_news_lg", "es_core_news_md"]`. Si Colab falla, reinicie el entorno y repita la celda.

**Comprobar:**

En este paso comprobamos que `support_floor` existe y que cargó un modelo de español.

```python
assert callable(support_floor) and MODEL.startswith("es_core_news")
print("Paso 0.2: OK")
```

---

## Ejercicio 1. Comprensión del negocio

### Paso 1.1. La pregunta y el problema

En este paso escriben la pregunta y el problema de su secretaría. Ese texto alimenta las secciones 2 y 3 del documento de requerimientos del proyecto.

**ESCRIBA SU TEXTO AQUÍ**

---

## Ejercicio 2. Comprensión de los datos

### Paso 2.1. El perfil de la columna `lead`

En este paso describen la columna `lead` en cuanto a su forma, tipos de datos, valores faltantes, la longitud del texto en palabras y el `profile`.

```python
# SU CÓDIGO. Paso 2.1: articles["lead_words"], short_leads y profile

```

**Listo cuando:**
- `profile` tiene una fila por columna de `articles`.
- `short_leads` tiene las descripciones de menos de 20 palabras.

**Comprobar:**

En este paso comprobamos que existe el largo de cada descripción y una fila de perfil por columna.

```python
assert "lead_words" in articles and len(profile) == articles.shape[1]
print("Paso 2.1: OK")
```

---

## Ejercicio 3. Preparación de los datos

### Paso 3.1. Palabras útiles en español

En este paso preparan las palabras útiles en español y deciden qué hacer con las palabras de relleno.
El texto dice en cuántas descripciones aparecen dos palabras de relleno y si las quitan.

**ESCRIBA SU TEXTO AQUÍ**

```python
# SU CÓDIGO. Paso 3.1: words, STOP_WORDS y FILLER_WORDS

```

**Listo cuando:**
- `STOP_WORDS` son las del español (`spacy.lang.es.stop_words`) más `URL_TOKENS`, y `words` quita el residuo "[cita requerida]".
- `FILLER_WORDS` tiene dos palabras de relleno de su extracto.
- El texto dice en cuántas descripciones aparecen esas dos palabras y si las quitan.

**Comprobar:**

En este paso comprobamos que `words` devuelve un conjunto y que hay dos palabras de relleno.

```python
assert isinstance(words("Texto de prueba", STOP_WORDS), set) and len(FILLER_WORDS) == 2
print("Paso 3.1: OK")
```

### Paso 3.2. Conjuntos, conteos y pares candidatos

En este paso arman un conjunto de palabras por descripción, los conteos y los pares candidatos.

```python
# SU CÓDIGO. Paso 3.2: word_sets, N, FLOOR, word_count, vocabulary y candidates

```

**Listo cuando:**
- `N` es el número de conjuntos y `FLOOR` sale de `support_floor(N)`.
- `candidates` va de cada par a su soporte, todos con soporte de `FLOOR` o más.

**Comprobar:**

En este paso comprobamos que hay un conjunto por descripción y que todos los pares llegan al umbral.

```python
assert len(word_sets) == N and min(candidates.values()) >= FLOOR == support_floor(N)
print(f"Paso 3.2: OK ({len(candidates)} pares)")
```

### Paso 3.3. Palabras que el modelo conoce

En este paso cruzan el vocabulario con el modelo de vectores.

```python
# SU CÓDIGO. Paso 3.3: no_vector, shared_groups y group_of

```

**Listo cuando:**
- `no_vector` es una lista y `group_of` un diccionario.

**Comprobar:**

En este paso comprobamos que existen `no_vector` y `group_of`.

```python
assert isinstance(no_vector, list) and isinstance(group_of, dict)
print("Paso 3.3: OK")
```

---

## Ejercicio 4. Modelado

### Paso 4.1. Soporte y lift (M1 y M2)

En este paso calculan el soporte y el lift de cada par candidato.

```python
# SU CÓDIGO. Paso 4.1: table con support, pair y lift

```

**Listo cuando:**
- `table` tiene una fila por par candidato, con `word_a`, `word_b`, `support`, `pair` y `lift`.

**Comprobar:**

En este paso comprobamos que la tabla tiene sus columnas y una fila por par candidato.

```python
assert {"word_a", "word_b", "support", "pair", "lift"} <= set(table.columns) and len(table) == len(candidates)
print("Paso 4.1: OK")
```

### Paso 4.2. Coseno y vecinos (M3)

En este paso calculan el coseno de cada par y los vecinos de una palabra de su secretaría.

```python
# SU CÓDIGO. Paso 4.2: columnas cosine y shared_vector, SEED_WORD y neighbours

```

**Listo cuando:**
- `table` tiene `cosine` (entre -1 y 1) y `shared_vector` (verdadero o falso).
- `SEED_WORD` es una palabra central de su secretaría.

**Comprobar:**

En este paso comprobamos las columnas `shared_vector` y `cosine`.

```python
assert table["shared_vector"].dtype == bool and table["cosine"].dropna().between(-1.001, 1.001).all()
print("Paso 4.2: OK")
```

---

## Ejercicio 5. Evaluación

### Paso 5.1. La línea base del grupo

En este paso escriben su línea base y cuentan cada par en tablas al azar.
El texto dice qué conserva el azar y por qué es justo para su extracto.

**ESCRIBA SU TEXTO AQUÍ**

```python
# SU CÓDIGO. Paso 5.1: transactions, null y la columna null_p95

```

**Listo cuando:**
- El texto dice qué conserva el azar y por qué es justo para su extracto.
- `null` tiene los conteos al azar de cada par y `table` tiene `null_p95`.

**Comprobar:**

En este paso comprobamos que cada par tiene sus conteos al azar.

```python
assert len(null) == len(candidates) and "null_p95" in table
print("Paso 5.1: OK")
```

### Paso 5.2. Pares conservados y su lectura

En este paso marcan los pares que superan la línea base y leen tres pares conservados en sus textos. El texto también dice qué hicieron con los pares de fórmula, como "el término X se refiere a".

**ESCRIBA SU TEXTO AQUÍ**

```python
# SU CÓDIGO. Paso 5.2: columna kept y kept_table

```

**Listo cuando:**
- `table["kept"]` es verdadero solo si el soporte está estrictamente por encima de `null_p95`.
- El texto lee tres pares conservados y dice qué hicieron con los pares de fórmula.

**Comprobar:**

En este paso comprobamos la columna `kept`.

```python
assert table["kept"].dtype == bool
print("Paso 5.2: OK")
```

### Paso 5.3. Comparar los tres métodos

En este paso comparan el soporte, el lift y la cercanía sobre las mismas descripciones.
Un par que los tres métodos conservan es un candidato más fuerte. Un par que solo un método conserva no es el ganador. El par de solo cercanía puede quedar bajo el umbral, así que no tiene que ser una fila de `table`.

El texto nombra un par de cada tipo en sus descripciones: los tres métodos, solo los conteos y solo la cercanía.

**ESCRIBA SU TEXTO AQUÍ**

```python
# SU CÓDIGO. Paso 5.3: columnas kept_lift2 y beats_cosine, RANDOM_COSINE_P95 y comparison

```

**Listo cuando:**
- `kept_lift2` solo es verdadero en pares conservados.
- `beats_cosine` es verdadero o falso para cada par.
- El texto nombra un par de cada tipo: los tres métodos, solo los conteos y solo la cercanía.

**Comprobar:**

En este paso comprobamos que solo destacan pares conservados y la columna `beats_cosine`.

```python
assert not (table["kept_lift2"] & ~table["kept"]).any() and table["beats_cosine"].dtype == bool
print("Paso 5.3: OK")
```

### Paso 5.4. Dos pares y los artículos que seleccionan

En este paso toman dos pares conservados y listan artículos cuya descripción contiene las dos palabras. Nombren dos pares conservados y, para cada uno, artículos de su secretaría.

**ESCRIBA SU TEXTO AQUÍ**

**Listo cuando:**
- El texto nombra dos pares conservados y, para cada uno, artículos de su secretaría.

---

## Ejercicio 6. Despliegue

### Paso 6.1. El uso de un patrón y `outputs/patrones.csv`

En este paso escriben cómo entra un patrón en la decisión y guardan `outputs/patrones.csv`. El texto dice cómo un patrón conservado entra en la lista y qué hecho sacaría un par de la lista.

**ESCRIBA SU TEXTO AQUÍ**

```python
# SU CÓDIGO. Paso 6.1: PATTERNS_PATH

```

**Listo cuando:**
- El texto dice cómo un patrón conservado entra en la lista y qué hecho sacaría un par.
- `outputs/patrones.csv` tiene una fila por par candidato con `pair`, `support`, `null_p95`, `lift`, `cosine`, `kept`, `kept_lift2`, `beats_cosine` y `shared_vector`.

**Comprobar:**

En este paso comprobamos que `outputs/patrones.csv` tiene sus columnas.

```python
assert {"pair", "support", "null_p95", "kept", "kept_lift2"} <= set(pd.read_csv("outputs/patrones.csv").columns)
print("Paso 6.1: OK. Armen el ZIP.")
```

---

## Registro de contribución

En este paso cada integrante anota su tarea concreta y el grupo dice quién consolida el ZIP.

**ESCRIBA SU TEXTO AQUÍ**

## Entrega

El ZIP se entrega el martes 17 nov 2026, 23:59 (hora de Colombia), con el cuaderno ejecutado y renombrado.

| Archivo del ZIP `week-1-<group_id>.zip` | Descripción |
|-----------------------------------------|-------------|
| `week-1-group-<group_id>.ipynb` | Este cuaderno ejecutado, con la pregunta escrita en el Paso 1.1 |
| `outputs/patrones.csv` | Una fila por par candidato, con sus columnas de evaluación |

La pregunta queda en el cuaderno.
`outputs/patrones.csv` es el resultado de esta semana.
En la semana 2 el grupo lo compara con lo que encuentre.
El cuaderno del proyecto lee este archivo cuando arma la lista de inicio. No vuelve a calcular los pares.

<!-- end NOTEBOOK: -->
