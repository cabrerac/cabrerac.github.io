<!-- NOTEBOOK: -->

## Instrucciones

**Propósito.** Cuaderno de grupo de la semana 1 (Lecciones 1 y 2). Su grupo es un equipo interno de una alcaldía y trabaja para una secretaría. El producto del proyecto es una lista de artículos para los nuevos integrantes del equipo.

**Esta semana.** El grupo escribe la pregunta en este cuaderno y genera `outputs/patrones.csv` (los pares de palabras con soporte, lift y cercanía).
La evaluación compara los tres métodos sobre las mismas entradillas.
El archivo de pares es el resultado de la primera iteración del proyecto.

**Antes de empezar.** Ejecuten primero los cuadernos individuales de las Lecciones 1 y 2. Este cuaderno lo escribe el grupo. Cada paso dice qué código de la Lección 1 o de la Lección 2 adaptar. No peguen sin entender.

**Datos de entrada.** El archivo de su secretaría: G1 Agricultura, G2 Salud mental, G3 Medio ambiente, G4 Inclusión Social y G5 Vivienda. Cada fila es un artículo de Wikipedia en español. El texto para los patrones es la columna `lead`, la **entradilla** del artículo.

**Materiales.** [L1 Introducción](https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-data-mining/l1-introduction.ipynb) y [L2 Patrones](https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-data-mining/l2-patterns.ipynb).

**Pregunta del grupo.** ¿Qué artículos de su secretaría debe leer primero una persona nueva en el equipo?
Comparen los pares de las entradillas con soporte, lift y cercanía.

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

**Cómo leer cada paso.** Cada paso empieza con **En este paso**, dice qué copiar y dónde está, y termina con una celda **Comprobar**. Ejecuten de arriba abajo. Una Comprobar revisa que exista lo pedido, con su forma. No revisa su respuesta. Si falla, corrijan la celda anterior y vuelvan a ejecutar desde ahí.

---

## Ejercicio 0. Configuración

### Paso 0.1. Grupo y datos

En este paso eligen el grupo y descargan el archivo de su secretaría.

Cambien solo `GROUP`.

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

En este paso copian los parámetros, las importaciones y el modelo de vectores de la Lección 2. El modelo de español `es_core_news_lg` pesa unos 570 MB y se descarga en esta celda.

| Qué copiar | Dónde está en L2 |
|------------|------------------|
| Los parámetros (`SUPPORT_SHARE`, `SUPPORT_MIN`, `LIFT_MIN`, `SWAPS_PER_ONE`, `N_SAMPLES`, `SEED`, `PROGRESS_EVERY`), sin cambiar sus valores | Parte 2, Paso 1 |
| Las importaciones y `support_floor` | Parte 2, Paso 1 |
| `UNUSED_PIPES`, `load_vector_model` y la carga de `nlp, MODEL` | Parte 2, Paso 2 |

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

En este paso escriben la pregunta y el problema de su secretaría.
Ese texto alimenta las secciones 2 y 3 del documento de requerimientos del proyecto.
No se guarda en un archivo.
El ejemplo de laboratorio está en la Lección 1, Parte 1, Paso 1.

| Qué escribir | Sección del documento |
|--------------|------------------------|
| `QUESTION` | 2. Objetivos del negocio |
| `PROBLEM` | 3. Situación |

```python
# SU CÓDIGO. Paso 1.1: QUESTION y PROBLEM

```

**Listo cuando:**
- `QUESTION` (texto) dice la pregunta de una persona nueva, quién necesita la lista, qué puede decidir y qué no.
- `PROBLEM` (texto) nombra la secretaría y el archivo, y dice que la lista es un inicio de lectura.

**Comprobar:**

En este paso comprobamos que escribieron la pregunta y el problema.

```python
assert QUESTION.strip() and PROBLEM.strip()
print("Paso 1.1: OK")
```

---

## Ejercicio 2. Comprensión de los datos

### Paso 2.1. El perfil de la columna `lead`

En este paso describen la columna `lead` con el perfil de la Lección 1.

| Qué copiar | Dónde está en L1 |
|------------|------------------|
| Forma, tipos y valores faltantes | Parte 2, Pasos 3 y 4 |
| Largo del texto en palabras | Parte 2, Paso 5 (use `lead` en lugar de `abstract`) |
| `profile_column` y la tabla `profile` | Parte 2, Paso 9 |

```python
# SU CÓDIGO. Paso 2.1: articles["lead_words"], short_leads y profile

```

**Listo cuando:**
- `profile` tiene una fila por columna de `articles`.
- `short_leads` tiene las entradillas de menos de 20 palabras.

**Comprobar:**

En este paso comprobamos que existe el largo de cada entradilla y una fila de perfil por columna.

```python
assert "lead_words" in articles and len(profile) == articles.shape[1]
print("Paso 2.1: OK")
```

---

## Ejercicio 3. Preparación de los datos

### Paso 3.1. Palabras útiles en español

En este paso preparan las palabras útiles en español y deciden qué hacer con las palabras de relleno.

| Qué copiar | Dónde está en L2 |
|------------|------------------|
| `WORD_RE` y `words` | Parte 3, Paso 1 |
| `URL_TOKENS` y la suma en `STOP_WORDS` | Parte 3, Paso 3 |

```python
# SU CÓDIGO. Paso 3.1: words, STOP_WORDS, FILLER_WORDS y FILLER_DECISION

```

**Listo cuando:**
- `STOP_WORDS` son las del español (`spacy.lang.es.stop_words`) más `URL_TOKENS`, y `words` quita el residuo "[cita requerida]".
- `FILLER_WORDS` tiene dos palabras de relleno de su extracto y `FILLER_DECISION` (texto) dice en cuántas entradillas aparecen y si las quitan.

**Comprobar:**

En este paso comprobamos que `words` devuelve un conjunto y que escribieron las dos palabras de relleno y su decisión.

```python
assert isinstance(words("Texto de prueba", STOP_WORDS), set) and len(FILLER_WORDS) == 2 and FILLER_DECISION.strip()
print("Paso 3.1: OK")
```

### Paso 3.2. Conjuntos, conteos y pares candidatos

En este paso arman un conjunto de palabras por entradilla, los conteos y los pares candidatos.

| Qué copiar | Dónde está en L2 |
|------------|------------------|
| `word_sets`, `N` y `FLOOR` (fuera las de menos de 5 palabras útiles) | Parte 3, Paso 4 |
| `word_count` y `vocabulary` | Parte 3, Paso 5 |
| `count_pairs` y `candidates` | Parte 3, Paso 6 |

```python
# SU CÓDIGO. Paso 3.2: word_sets, N, FLOOR, word_count, vocabulary y candidates

```

**Listo cuando:**
- `N` es el número de conjuntos y `FLOOR` sale de `support_floor(N)`.
- `candidates` va de cada par a su soporte, todos con soporte de `FLOOR` o más.

**Comprobar:**

En este paso comprobamos que hay un conjunto por entradilla y que todos los pares llegan al umbral.

```python
assert len(word_sets) == N and min(candidates.values()) >= FLOOR == support_floor(N)
print(f"Paso 3.2: OK ({len(candidates)} pares)")
```

### Paso 3.3. Palabras que el modelo conoce

En este paso cruzan el vocabulario con el modelo de vectores.

| Qué copiar | Dónde está en L2 |
|------------|------------------|
| `no_vector`, `shared_vectors`, `shared_groups` y `group_of` | Parte 3, Paso 7 |

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

| Qué copiar | Dónde está en L2 |
|------------|------------------|
| `table` con `word_a`, `word_b`, `support` y `pair` | Parte 4, M1 |
| `compute_lift` y la columna `lift` | Parte 4, M2 |

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

| Qué copiar | Dónde está en L2 |
|------------|------------------|
| `unit_vector`, `VECTORS`, `pair_cosine` y las columnas `cosine` y `shared_vector` | Parte 4, M3 |
| `SEED_WORD`, `same_vector` y `neighbours` | Parte 4, M3 |

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

| Qué copiar | Dónde está en L2 |
|------------|------------------|
| `frequent_words` y `transactions` | Parte 5, Paso 1 |
| `p95` y `swap_randomize` | Parte 5, Paso 2 |
| `pair_counts`, `swap_null_counts`, `kept_pairs`, `null` y la columna `null_p95` | Parte 5, Paso 4 |

```python
# SU CÓDIGO. Paso 5.1: BASELINE (texto), transactions, null y la columna null_p95

```

**Listo cuando:**
- `BASELINE` (texto) dice qué conserva su azar y por qué es justo para su extracto. La referencia es la de la Lección 2. Otra vale si la justifican.
- `null` tiene los conteos al azar de cada par y `table` tiene `null_p95`.

**Comprobar:**

En este paso comprobamos que escribieron su línea base y que cada par tiene sus conteos al azar.

```python
assert BASELINE.strip() and len(null) == len(candidates) and "null_p95" in table
print("Paso 5.1: OK")
```

### Paso 5.2. Pares conservados y su lectura

En este paso marcan los pares que superan la línea base y leen uno en sus textos.

| Qué copiar | Dónde está en L2 |
|------------|------------------|
| `kept`, la columna `kept` y `kept_table` | Parte 5, Paso 4 |
| Leer un par en sus textos | Parte 5, Paso 5 |
| Cuántos pasan por azar | Parte 5, Paso 6 |

```python
# SU CÓDIGO. Paso 5.2: columna kept, kept_table, PAIR_READING y FORMULA_DECISION

```

**Listo cuando:**
- `table["kept"]` es verdadero solo si el soporte está estrictamente por encima de `null_p95`.
- `PAIR_READING` (texto) lee tres pares conservados. `FORMULA_DECISION` (texto) dice qué hicieron con los pares de fórmula, como "el término X se refiere a".

**Comprobar:**

En este paso comprobamos la columna `kept` y que escribieron su lectura y su decisión.

```python
assert table["kept"].dtype == bool and PAIR_READING.strip() and FORMULA_DECISION.strip()
print("Paso 5.2: OK")
```

### Paso 5.3. Comparar los tres métodos

En este paso comparan el soporte, el lift y la cercanía sobre las mismas entradillas.
Un par que los tres métodos conservan es un candidato más fuerte.
Un par que solo un método conserva no es el ganador.
El par de solo cercanía puede quedar bajo el umbral, así que no tiene que ser una fila de `table`.

| Qué copiar | Dónde está en L2 |
|------------|------------------|
| La columna `kept_lift2` | Parte 5, Paso 7 |
| `random_cosines`, `RANDOM_COSINE_P95` y la columna `beats_cosine` | Parte 5, Paso 8 |
| La tabla `comparison` | Parte 5, Paso 9 |

```python
# SU CÓDIGO. Paso 5.3: columnas kept_lift2 y beats_cosine, RANDOM_COSINE_P95, comparison y COMPARISON_READING

```

**Listo cuando:**
- `kept_lift2` solo es verdadero en pares conservados.
- `beats_cosine` es verdadero o falso para cada par.
- `COMPARISON_READING` (texto) nombra un par de cada tipo en sus entradillas: los tres métodos, solo los conteos y solo la cercanía.

**Comprobar:**

En este paso comprobamos que solo destacan pares conservados, la columna `beats_cosine` y que escribieron la comparación.

```python
assert not (table["kept_lift2"] & ~table["kept"]).any() and table["beats_cosine"].dtype == bool and COMPARISON_READING.strip()
print("Paso 5.3: OK")
```

### Paso 5.4. Dos pares y los artículos que seleccionan

En este paso toman dos pares conservados y listan artículos cuya entradilla contiene las dos palabras.

```python
# SU CÓDIGO. Paso 5.4: PAIR_ARTICLES

```

**Listo cuando:**
- `PAIR_ARTICLES` (texto) nombra dos pares conservados y, para cada uno, artículos de su secretaría.

**Comprobar:**

En este paso comprobamos que escribieron los dos pares y sus artículos.

```python
assert PAIR_ARTICLES.strip()
print("Paso 5.4: OK")
```

---

## Ejercicio 6. Despliegue

### Paso 6.1. El uso de un patrón y `outputs/patrones.csv`

En este paso escriben cómo entra un patrón en la decisión y guardan `outputs/patrones.csv`.

| Qué escribir o copiar | Dónde está en L2 |
|--------------------|------------------|
| Cómo entra un patrón, en `PATTERN_USE` y `WHAT_CHANGES_IT` | Parte 6, Paso 1 |
| Guardar la tabla de pares | Parte 5, Paso 10 (aquí el archivo es `PATTERNS_PATH`) |

```python
# SU CÓDIGO. Paso 6.1: PATTERN_USE, WHAT_CHANGES_IT y PATTERNS_PATH

```

**Listo cuando:**
- `PATTERN_USE` (texto) dice cómo un patrón conservado entra en la lista.
- `WHAT_CHANGES_IT` (texto) dice qué hecho sacaría un par de la lista.
- `outputs/patrones.csv` tiene una fila por par candidato con `pair`, `support`, `null_p95`, `lift`, `cosine`, `kept`, `kept_lift2`, `beats_cosine` y `shared_vector`.

**Comprobar:**

En este paso comprobamos que escribieron el uso del patrón y que `outputs/patrones.csv` tiene sus columnas.

```python
assert PATTERN_USE.strip() and WHAT_CHANGES_IT.strip()
assert {"pair", "support", "null_p95", "kept", "kept_lift2"} <= set(pd.read_csv("outputs/patrones.csv").columns)
print("Paso 6.1: OK. Armen el ZIP.")
```

---

## Registro de contribución

En este paso cada integrante anota su tarea concreta y el grupo dice quién consolida el ZIP.

```python
# SU CÓDIGO. Registro: contribution_log, una línea por integrante y quién consolida el ZIP

```

**Listo cuando:**
- `contribution_log` (texto) tiene una línea con una tarea concreta por integrante y dice quién consolidó el ZIP.

## Para la reflexión individual

Use la [plantilla de la reflexión de la semana 1](https://cabrerac.github.io/assets/documents/26-udenar-data-mining/reflection-week-1-template.docx) y mantenga sus títulos. Extensión: entre 700 y 1000 palabras. Por debajo de 500 palabras el texto queda corto.

| Título | Qué escribir |
|--------|--------------|
| **Metadatos** | Nombre, grupo, semana 1 (L1 + L2), conteo aproximado de palabras y la lectura que cita. |
| **Proceso** | Qué hizo el grupo en el cuaderno de la semana 1. Diga cuál fue su contribución. |
| **Decisión** | Describa las reglas de asociación que exploró en esta semana. |
| **Métodos** | Explique cuáles fueron los métodos utilizados en esta semana y cómo se comparan entre ellos. |
| **Ética** | Nombre una elección técnica de esta semana. Diga a quién ayuda o perjudica, o cómo se podría usar mal un resultado de esta semana. Relacione el punto con Wirth y Hipp (2000) o con Agrawal, Imielinski y Swami (1993). |

## Entrega

El ZIP se entrega el martes 17 nov 2026, 23:59 (hora de Colombia), con el cuaderno ejecutado y renombrado.

| Archivo del ZIP `week-1-<group_id>.zip` | Descripción |
|-----------------------------------------|-------------|
| `week-1-group-<group_id>.ipynb` | Este cuaderno ejecutado, con la pregunta escrita en el Paso 1.1 |
| `outputs/patrones.csv` | Una fila por par candidato, con sus columnas de evaluación |

La pregunta queda en el cuaderno.
`outputs/patrones.csv` es el resultado de esta semana.
En la semana 2 el grupo lo compara con lo que encuentre.

<!-- end NOTEBOOK: -->
