<!-- NOTEBOOK: -->

## Instrucciones

**Propósito.** Cuaderno de grupo de la semana 1 (Lecciones 1 y 2). Su grupo es un equipo interno de una alcaldía y trabaja para una secretaría. El producto del proyecto es una **lista de inicio**: los artículos que una persona nueva en la secretaría debe abrir primero.

**Esta semana.** El cuaderno empieza la lista con dos archivos: la tarjeta de la pregunta en `pregunta.json` y los pares de palabras frente a una línea base en `outputs/patrones.csv`. La lista se cierra en la semana 3.

**Requisito.** Ejecute primero los cuadernos individuales **L1** y **L2**. Este cuaderno lo escribe el grupo. Cada paso dice qué código de L1 o L2 adaptar. No pegue sin entender.

**Datos de entrada.** Un CSV por grupo con artículos de Wikipedia en español. El texto para los patrones es la columna `lead`, la **entradilla** del artículo. Las categorías las pusieron quienes editan Wikipedia. Un par de categorías que se repite no es un patrón del grupo.

**Materiales.** [L1 Introducción](https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-data-mining/l1-introduction.ipynb) y [L2 Patrones](https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-data-mining/l2-patterns.ipynb).

**Pregunta del grupo.** ¿Qué artículos de su secretaría debe abrir primero una persona nueva, y qué pares de palabras de las entradillas superan a la línea base?

**Entrega Moodle (martes 10 nov 2026, 23:59 Colombia).** ZIP `week-1-<group_id>.zip` con `week-1-group-<group_id>.ipynb` (este cuaderno ejecutado y renombrado), `pregunta.json` y `outputs/patrones.csv`.

**Mapa del cuaderno**

| Ejercicio | Tema | Entregable clave |
|-----------|------|------------------|
| **0** | Configuración | Grupo, datos, parámetros, librerías y modelo de vectores |
| **1** | Comprensión del negocio | `pregunta.json` con pregunta, pasos, estándar y uso |
| **2** | Comprensión de los datos | Perfil de la columna `lead` |
| **3** | Preparación de los datos | Conjuntos de palabras, conteos y vectores |
| **4** | Modelado | Pares por soporte, lift y coseno |
| **5** | Evaluación | Su línea base y los pares conservados |
| **6** | Despliegue | Uso de un patrón y `outputs/patrones.csv` |

**Celdas Comprobar.** Ejecute de arriba abajo. Una Comprobar revisa que exista lo pedido, con su forma. No revisa su respuesta. Si falla, corrija la celda anterior y vuelva a ejecutar desde ahí.

---

## Ejercicio 0. Configuración

### Paso 0.1. Grupo y datos

Cambie solo `GROUP`.

```python
import json
from pathlib import Path

import pandas as pd
import requests

GROUP = "G1"   # cambie a G2, G3, G4 o G5
EXTRACTS = {"G1": ("Pobreza", "pobreza.csv"), "G2": ("Vivienda", "vivienda.csv"), "G3": ("Medio ambiente", "medio-ambiente.csv"),
            "G4": ("Agricultura", "agricultura.csv"), "G5": ("Salud mental", "salud-mental.csv")}
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

| Qué copiar | Dónde está en L2 |
|------------|------------------|
| Los parámetros (`SUPPORT_SHARE`, `SUPPORT_MIN`, `LIFT_MIN`, `SWAPS_PER_ONE`, `N_SAMPLES`, `SEED`, `PROGRESS_EVERY`), sin cambiar sus valores | Parte 1, Paso 1 |
| Las importaciones y `support_floor` | Parte 1, Paso 1 |
| `UNUSED_PIPES`, `load_vector_model` y la carga de `nlp, MODEL` | Parte 1, Paso 2 |

```python
# SU CÓDIGO. Paso 0.2: parámetros, rutas de la entrega, importaciones, support_floor, load_vector_model y nlp, MODEL en español

```

**Listo cuando:**
- Los parámetros tienen los valores de la L2.
- `QUESTION_PATH` es `pregunta.json` y `PATTERNS_PATH` es `outputs/patrones.csv`.
- `nlp` y `MODEL` cargan un modelo de español: `MODELS = ["es_core_news_lg", "es_core_news_md"]`.

**Comprobar:**

```python
assert callable(support_floor) and MODEL.startswith("es_core_news")
print("Paso 0.2: OK")
```

---

## Ejercicio 1. Comprensión del negocio

### Paso 1.1. La tarjeta de la pregunta

| Qué copiar | Dónde está en L1 |
|------------|------------------|
| La tarjeta `question_card` con `question`, `steps`, `standard` y `use` | Parte 1, Paso 3 |
| Guardar `pregunta.json` | Parte 1, Paso 4 |

```python
# SU CÓDIGO. Paso 1.1: question_card y QUESTION_PATH guardado

```

**Listo cuando:**
- La tarjeta es de su secretaría y el estándar se escribió **antes** de mirar resultados.
- `pregunta.json` tiene `question`, `steps`, `standard` (con `min_articles`, `max_articles` enteros y una regla más del grupo) y `use` (con `may` y `may_not`).

**Comprobar:**

```python
card = json.loads(Path("pregunta.json").read_text(encoding="utf-8"))
assert {"question", "steps", "standard", "use"} <= set(card) and {"min_articles", "max_articles"} <= set(card["standard"])
print("Paso 1.1: OK")
```

---

## Ejercicio 2. Comprensión de los datos

### Paso 2.1. El perfil de la columna `lead`

| Qué copiar | Dónde está en L1 |
|------------|------------------|
| Forma, tipos y valores faltantes | Parte 2, Pasos 2 y 3 |
| Largo del texto en palabras | Parte 2, Paso 4 (use `lead` en lugar de `abstract`) |
| `profile_column` y la tabla `profile` | Parte 2, Paso 8 |

```python
# SU CÓDIGO. Paso 2.1: articles["lead_words"], short_leads y profile

```

**Listo cuando:**
- `profile` tiene una fila por columna de `articles`.
- `short_leads` tiene las entradillas de menos de 20 palabras.

**Comprobar:**

```python
assert "lead_words" in articles and len(profile) == articles.shape[1]
print("Paso 2.1: OK")
```

---

## Ejercicio 3. Preparación de los datos

### Paso 3.1. Palabras útiles en español

| Qué copiar | Dónde está en L2 |
|------------|------------------|
| `WORD_RE` y `words` | Parte 4, Paso 1 |
| `URL_TOKENS` y la suma en `STOP_WORDS` | Parte 4, Paso 3 |

```python
# SU CÓDIGO. Paso 3.1: words, STOP_WORDS, FILLER_WORDS y FILLER_DECISION

```

**Listo cuando:**
- `STOP_WORDS` son las del español (`spacy.lang.es.stop_words`) más `URL_TOKENS`, y `words` quita el residuo "[cita requerida]".
- `FILLER_WORDS` tiene dos palabras de relleno de su extracto y `FILLER_DECISION` (texto) dice en cuántas entradillas aparecen y si las quitan.

**Comprobar:**

```python
assert isinstance(words("Texto de prueba", STOP_WORDS), set) and len(FILLER_WORDS) == 2 and FILLER_DECISION.strip()
print("Paso 3.1: OK")
```

### Paso 3.2. Conjuntos, conteos y pares candidatos

| Qué copiar | Dónde está en L2 |
|------------|------------------|
| `word_sets`, `N` y `FLOOR` (fuera las de menos de 5 palabras útiles) | Parte 4, Paso 4 |
| `word_count` y `vocabulary` | Parte 4, Paso 5 |
| `count_pairs` y `candidates` | Parte 4, Paso 6 |

```python
# SU CÓDIGO. Paso 3.2: word_sets, N, FLOOR, word_count, vocabulary y candidates

```

**Listo cuando:**
- `N` es el número de conjuntos y `FLOOR` sale de `support_floor(N)`.
- `candidates` va de cada par a su soporte, todos con soporte de `FLOOR` o más.

**Comprobar:**

```python
assert len(word_sets) == N and min(candidates.values()) >= FLOOR == support_floor(N)
print(f"Paso 3.2: OK ({len(candidates)} pares)")
```

### Paso 3.3. Palabras que el modelo conoce

| Qué copiar | Dónde está en L2 |
|------------|------------------|
| `no_vector`, `shared_vectors`, `shared_groups` y `group_of` | Parte 4, Paso 7 |

```python
# SU CÓDIGO. Paso 3.3: no_vector, shared_groups y group_of

```

**Listo cuando:**
- `no_vector` es una lista y `group_of` un diccionario.

**Comprobar:**

```python
assert isinstance(no_vector, list) and isinstance(group_of, dict)
print("Paso 3.3: OK")
```

---

## Ejercicio 4. Modelado

### Paso 4.1. Soporte y lift (M1 y M2)

| Qué copiar | Dónde está en L2 |
|------------|------------------|
| `table` con `word_a`, `word_b`, `support` y `pair` | Parte 5, M1 |
| `compute_lift` y la columna `lift` | Parte 5, M2 |

```python
# SU CÓDIGO. Paso 4.1: table con support, pair y lift

```

**Listo cuando:**
- `table` tiene una fila por par candidato, con `word_a`, `word_b`, `support`, `pair` y `lift`.

**Comprobar:**

```python
assert {"word_a", "word_b", "support", "pair", "lift"} <= set(table.columns) and len(table) == len(candidates)
print("Paso 4.1: OK")
```

### Paso 4.2. Coseno y vecinos (M3)

| Qué copiar | Dónde está en L2 |
|------------|------------------|
| `unit_vector`, `VECTORS`, `pair_cosine` y las columnas `cosine` y `shared_vector` | Parte 5, M3 |
| `SEED_WORD`, `same_vector` y `neighbours` | Parte 5, M3 |

```python
# SU CÓDIGO. Paso 4.2: columnas cosine y shared_vector, SEED_WORD y neighbours

```

**Listo cuando:**
- `table` tiene `cosine` (entre -1 y 1) y `shared_vector` (verdadero o falso).
- `SEED_WORD` es una palabra central de su secretaría.

**Comprobar:**

```python
assert table["shared_vector"].dtype == bool and table["cosine"].dropna().between(-1.001, 1.001).all()
print("Paso 4.2: OK")
```

---

## Ejercicio 5. Evaluación

### Paso 5.1. La línea base del grupo

| Qué copiar | Dónde está en L2 |
|------------|------------------|
| `frequent_words` y `transactions` | Parte 6, Paso 1 |
| `p95` y `swap_randomize` | Parte 6, Paso 2 |
| `pair_counts`, `swap_null_counts`, `kept_pairs`, `null` y la columna `null_p95` | Parte 6, Paso 4 |

```python
# SU CÓDIGO. Paso 5.1: BASELINE (texto), transactions, null y la columna null_p95

```

**Listo cuando:**
- `BASELINE` (texto) dice qué conserva su azar y por qué es justo para su extracto. La referencia es la de la L2; otra vale si la justifican.
- `null` tiene los conteos al azar de cada par y `table` tiene `null_p95`.

**Comprobar:**

```python
assert BASELINE.strip() and len(null) == len(candidates) and "null_p95" in table
print("Paso 5.1: OK")
```

### Paso 5.2. Pares conservados y su lectura

| Qué copiar | Dónde está en L2 |
|------------|------------------|
| `kept`, la columna `kept` y `kept_table` | Parte 6, Paso 4 |
| Leer un par en sus textos | Parte 6, Paso 5 |
| Cuántos pasan por azar | Parte 6, Paso 6 |

```python
# SU CÓDIGO. Paso 5.2: columna kept, kept_table, PAIR_READING y FORMULA_DECISION

```

**Listo cuando:**
- `table["kept"]` es verdadero solo si el soporte está estrictamente por encima de `null_p95`.
- `PAIR_READING` (texto) lee tres pares conservados. `FORMULA_DECISION` (texto) dice qué hicieron con los pares de fórmula, como "el término X se refiere a".

**Comprobar:**

```python
assert table["kept"].dtype == bool and PAIR_READING.strip() and FORMULA_DECISION.strip()
print("Paso 5.2: OK")
```

### Paso 5.3. Destacar y comparar los tres métodos

| Qué copiar | Dónde está en L2 |
|------------|------------------|
| La columna `kept_lift2` | Parte 6, Paso 7 |
| `random_cosines`, `RANDOM_COSINE_P95` y la columna `beats_cosine` | Parte 6, Paso 8 |
| La tabla `comparison` | Parte 6, Paso 9 |

```python
# SU CÓDIGO. Paso 5.3: columnas kept_lift2 y beats_cosine, RANDOM_COSINE_P95 y comparison

```

**Listo cuando:**
- `kept_lift2` solo es verdadero en pares conservados.
- `beats_cosine` es verdadero o falso para cada par.

**Comprobar:**

```python
assert not (table["kept_lift2"] & ~table["kept"]).any() and table["beats_cosine"].dtype == bool
print("Paso 5.3: OK")
```

---

## Ejercicio 6. Despliegue

### Paso 6.1. El uso de un patrón y `outputs/patrones.csv`

| Qué copiar | Dónde está en L2 |
|------------|------------------|
| `pattern_use` con `how_it_enters`, `what_changes_it` y `examples` | Parte 7, Paso 1 |
| Guardar la tabla de pares | Parte 6, Paso 10 (aquí el archivo es `PATTERNS_PATH`) |

```python
# SU CÓDIGO. Paso 6.1: question_card["pattern_use"], pregunta.json y PATTERNS_PATH

```

**Listo cuando:**
- `pregunta.json` tiene `pattern_use`, y `what_changes_it` dice qué hecho sacaría un par de la lista.
- `outputs/patrones.csv` tiene una fila por par candidato con `pair`, `support`, `null_p95`, `lift`, `cosine`, `kept`, `kept_lift2`, `beats_cosine` y `shared_vector`.

**Comprobar:**

```python
assert "pattern_use" in json.loads(Path("pregunta.json").read_text(encoding="utf-8"))
assert {"pair", "support", "null_p95", "kept", "kept_lift2"} <= set(pd.read_csv("outputs/patrones.csv").columns)
print("Paso 6.1: OK. Armen el ZIP.")
```

---

## Registro de contribución

```python
# SU CÓDIGO. Registro: contribution_log, una línea por integrante y quién consolida el ZIP

```

**Listo cuando:**
- `contribution_log` (texto) tiene una línea con una tarea concreta por integrante y dice quién consolidó el ZIP.

## Para la reflexión individual

La reflexión de la semana 1 va con la plantilla Word de la semana. Estas son sus preguntas:

| Parte | Pregunta |
|-------|----------|
| **Proceso** | Qué hizo el grupo en el cuaderno de la semana 1, en orden. Diga cuál fue su línea en el registro de contribución. |
| **Elección** | Una elección del grupo, por qué esa elección y un límite de esa elección. |
| **Decisión** | Un par que el grupo conservó en `outputs/patrones.csv`. Cómo cambia ese par quién queda en la lista de inicio. |
| **Ética** | Nombre una elección técnica de esta semana. Diga a quién ayuda o perjudica, o cómo se podría usar mal la lista. Relacione el punto con Wirth y Hipp (2000) o con Agrawal, Imielinski y Swami (1993). |

## Entrega

| Archivo del ZIP `week-1-<group_id>.zip` | Descripción |
|-----------------------------------------|-------------|
| `week-1-group-<group_id>.ipynb` | Este cuaderno ejecutado |
| `pregunta.json` | La tarjeta del grupo con `pattern_use` |
| `outputs/patrones.csv` | Una fila por par candidato, con sus columnas de evaluación |

Estos dos archivos empiezan la lista de inicio. Los pares con `kept_lift2` cuentan como el primer apoyo de un artículo en la semana 2.

<!-- end NOTEBOOK: -->
