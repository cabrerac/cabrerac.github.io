<!-- NOTEBOOK: -->

## Instrucciones

**Propósito.** Cuaderno de grupo de la semana 2 (Lecciones 3 y 4). Su grupo sigue como equipo interno de una alcaldía, con los artículos de su secretaría. Esta semana suma dos resultados a la lista de artículos para los nuevos integrantes del equipo: grupos de artículos parecidos y un filtro de texto con sus aciertos y errores.

**Esta semana.** Cada resultado queda en un archivo con nombre. Los grupos van en `outputs/grupos.csv`. El filtro de texto va en `outputs/texto.csv`, con la marca del grupo al lado para contar aciertos y errores. La tabla `outputs/en_vista.csv` junta los resultados de la semana 1 y de la semana 2 para cada artículo: el par, el grupo y el texto.

**Antes de empezar.** Ejecuten primero los cuadernos individuales de las Lecciones 3 y 4. Este cuaderno lo escribe el grupo. Cada paso dice qué código de la Lección 3 o de la Lección 4 adaptar. No peguen sin entender.

**Datos de entrada.** El mismo archivo de la semana 1: G1 Agricultura, G2 Salud mental, G3 Medio ambiente, G4 Inclusión Social y G5 Vivienda. El texto es la columna `lead`, la **entradilla**. La etiqueta del filtro sale de las categorías que pusieron quienes editan Wikipedia.

**Materiales.** [L3 Grupos](https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-data-mining/l3-groups.ipynb) y [L4 Texto](https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-data-mining/l4-text.ipynb).

**Pregunta del grupo.** ¿Qué grupos de artículos debe leer la persona nueva, y cuántos aciertos y errores tiene un filtro de texto frente a las marcas del grupo?

**Primero marcan, después corren los modelos de texto.** El Paso 3.1 escribe `marcas.csv` con 60 a 67 artículos, unos 15 a 21 por persona. Marquen leyendo la entradilla, sin mirar las categorías, y vuelvan a subir el archivo.

**Mapa del cuaderno**

| Ejercicio | Tema | Entregable clave |
|-----------|------|------------------|
| **0** | Configuración | Grupo, datos, parámetros, librerías, codificador y funciones de L3 y L4 |
| **1** | Comprensión del negocio y de los datos | La descripción de la pregunta, los pares de la semana 1 y las entradillas útiles |
| **2** | Grupos de artículos parecidos (L3) | `outputs/grupos.csv` y el hallazgo sobre la estructura |
| **3** | Filtro de texto (L4) | `marcas.csv` y `outputs/texto.csv` |
| **4** | Despliegue | `outputs/en_vista.csv` y `pregunta.json` con `group_use` y `text_use` |

**Cómo leer cada paso.** Cada paso empieza con **En este paso**, dice qué copiar y dónde está, y termina con una celda **Comprobar**. Ejecuten de arriba abajo. Una Comprobar revisa que exista lo pedido, con su forma. No revisa su respuesta. Si falla, corrijan la celda anterior y vuelvan a ejecutar desde ahí.

---

## Ejercicio 0. Configuración

### Paso 0.1. Grupo y datos

En este paso eligen el grupo y descargan el archivo de su secretaría. Suban el `pregunta.json` y los archivos de salida de su ZIP de la semana anterior (`outputs/patrones.csv`) antes de seguir.

Cambien solo `GROUP`. `TARGETS` son las categorías de la etiqueta del filtro, elegidas por el profesor.

```python
import json
from pathlib import Path

import pandas as pd
import requests

GROUP = "G1"   # cambie a G2, G3, G4 o G5
EXTRACTS = {"G1": ("Agricultura", "agricultura.csv"), "G2": ("Salud mental", "salud-mental.csv"), "G3": ("Medio ambiente", "medio-ambiente.csv"),
            "G4": ("Inclusión Social", "inclusion-social.csv"), "G5": ("Vivienda", "vivienda.csv")}
TARGETS = {"G1": ["Agrarismo", "Organizaciones agrícolas"], "G2": ["Trastornos mentales", "Psiquiatría"], "G3": ["Conservacionismo"],
           "G4": ["Hambrunas", "Hambre", "Bancos de alimentos"], "G5": ["Hipotecas", "Arrendamiento", "Huelgas de alquileres",
           "Vivienda asequible", "Vivienda pública"]}
SECRETARIAT, FILENAME = EXTRACTS[GROUP]
Path("outputs").mkdir(exist_ok=True)
path = Path("data") / FILENAME
path.parent.mkdir(exist_ok=True)
if not path.is_file():   # descarga una sola vez
    path.write_bytes(requests.get(f"https://cabrerac.github.io/assets/data/26-udenar-data-mining/{FILENAME}", timeout=60).content)
articles = pd.read_csv(path, keep_default_na=False)
print(f"Grupo {GROUP}: secretaría de {SECRETARIAT}, {len(articles)} artículos")
```

### Paso 0.2. Parámetros, librerías, codificador y funciones

En este paso copian los parámetros, las librerías, el codificador y las funciones de las Lecciones 3 y 4. El codificador `multilingual-e5-small` pesa unos 470 MB y se descarga en esta celda.

| Qué copiar | Dónde está |
|------------|------------|
| Los parámetros de L3 (`SUPPORT_SHARE`, `SUPPORT_MIN`, `SEED`, `MIN_SUPPORTS`, `MAX_WORD_SHARE` a `TOP_WORDS`), sin cambiar sus valores. `MIN_SUPPORTS` empieza en 2 y se puede cambiar. Cada grupo fija y justifica este número en su proyecto. 0 o 1 valen si se explica | L3, Parte 1, Paso 2 |
| Los parámetros de L4 (`FLAGGED_SHARE` a `PREFIX` y `N_FOLDS`), sin cambiar sus valores | L4, Parte 1, Paso 2 |
| Las importaciones y la instalación de `sentence-transformers` | L3, Parte 1, Paso 2, y L4, Parte 1, Paso 2 |
| `support_floor`, `n_flagged` y `min_positives` | L4, Parte 1, Paso 2 |
| `WORD_RE`, `words`, `word_list` y `p95` | L3, Parte 1, Paso 3 |
| `encoder` | L4, Parte 1, Paso 4 |
| `f1_interval` | L4, Parte 1, Paso 5 |
| `counts_of` | L4, Parte 5, Paso 1 |

```python
# SU CÓDIGO. Paso 0.2: parámetros, rutas de la entrega, importaciones, encoder, STOP_WORDS y las funciones de la tabla

```

**Listo cuando:**
- Los parámetros tienen los valores de las Lecciones 3 y 4.
- Las rutas son `pregunta.json`, `marcas.csv` y, en `outputs/`, `patrones.csv`, `grupos.csv`, `texto.csv` y `en_vista.csv`.
- `STOP_WORDS` son las del español más `URL_TOKENS` (y sus `FILLER_WORDS` si las quitaron), y `words` y `word_list` quitan "[cita requerida]".
- `encoder` lee hasta `MAX_LENGTH` tokens.

**Comprobar:**

En este paso comprobamos que existe `counts_of`, que el codificador lee hasta `MAX_LENGTH` tokens y que las palabras vacías son del español.

```python
assert callable(counts_of) and encoder.max_seq_length == MAX_LENGTH and "también" in STOP_WORDS
print("Paso 0.2: OK")
```

---

## Ejercicio 1. Comprensión del negocio y de los datos

### Paso 1.1. La descripción de la pregunta, los pares y las entradillas útiles

En este paso leen la descripción de la pregunta y los pares de la semana 1, y dejan las entradillas útiles.

| Qué copiar | Dónde está |
|------------|------------|
| Leer `pregunta.json` en `question_card` | L3, Parte 1, Paso 4 |
| Leer los pares en `patterns` | L3, Parte 1, Paso 5 (aquí el archivo es `outputs/patrones.csv`) |
| `texts`, `N` y `FLOOR` | L3, Parte 2, Paso 1 (use `lead` en lugar de `abstract`) |
| `n_cut`, las entradillas que el codificador corta | L4, Parte 3, Paso 4 |

```python
# SU CÓDIGO. Paso 1.1: question_card, patterns, articles sin las entradillas cortas, texts, N, FLOOR, n_cut y group_meaning

```

**Listo cuando:**
- `articles` y `texts` dejan fuera las entradillas con menos de 5 palabras útiles y tienen las mismas `N` filas.
- `group_meaning` (texto) dice qué le sirve a la persona nueva saber que un artículo está en un grupo, y qué grupo no le serviría.

**Comprobar:**

En este paso comprobamos que leyeron los pares, que los textos y los artículos tienen las mismas filas y que escribieron `group_meaning`.

```python
assert "kept_lift2" in patterns and len(texts) == N == len(articles) and group_meaning.strip()
print("Paso 1.1: OK")
```

---

## Ejercicio 2. Grupos de artículos parecidos (Lección 3)

### Paso 2.1. Las palabras del tema y la lista de palabras clave

En este paso escriben las palabras del tema y la lista de palabras clave antes de ver resultados.

| Qué copiar | Dónde está |
|------------|------------|
| `TOPIC_WORDS` | L3, Parte 1, Paso 4 |
| `KEYWORDS` | L4, Parte 3, Paso 1 |

```python
# SU CÓDIGO. Paso 2.1: TOPIC_WORDS y KEYWORDS, con un comentario por palabra

```

**Listo cuando:**
- Las dos listas se escriben **antes** de ver ningún grupo ni resultado, en minúsculas, con y sin tilde, en singular y plural, sin los nombres de `TARGETS`. Pueden ser la misma lista.
- `KEYWORDS` tiene al menos 5 palabras.

**Comprobar:**

En este paso comprobamos el tamaño de la lista de palabras clave y que todo está en minúsculas.

```python
assert len(KEYWORDS) >= 5 and all(w == w.lower() for w in KEYWORDS | TOPIC_WORDS)
print("Paso 2.1: OK")
```

### Paso 2.2. Conteos, escala y pocas dimensiones

En este paso cuentan las palabras, llevan cada entradilla a largo 1 y reducen las dimensiones.

| Qué copiar | Dónde está en L3 |
|------------|------------------|
| `token_lists`, `vectorizer`, `counts` y `vocabulary` | Parte 3, Paso 1 |
| `X` con cada fila de largo 1 | Parte 3, Paso 2 |
| `svd` y `Z` | Parte 3, Paso 3 |
| `Z_mixture` y `distances` | Parte 3, Paso 4 |

```python
# SU CÓDIGO. Paso 2.2: token_lists, counts, vocabulary, X, svd, Z, Z_mixture y distances

```

**Listo cuando:**
- `counts` y `X` tienen `N` filas y una columna por palabra de `vocabulary`.
- `Z` tiene `DENSITY_COMPONENTS` columnas y `distances` es de `N` por `N`.

**Comprobar:**

En este paso comprobamos la forma de `X`, de `Z` y de las distancias.

```python
assert X.shape == (N, len(vocabulary)) and Z.shape[1] == DENSITY_COMPONENTS and distances.shape == (N, N)
print("Paso 2.2: OK")
```

### Paso 2.3. Los tres métodos de grupos

En este paso corren k-means, la mezcla gaussiana y HDBSCAN.

| Qué copiar | Dónde está en L3 |
|------------|------------------|
| `silhouettes`, `K_CHOSEN`, `kmeans`, `kmeans_labels`, `top_words` y `kmeans_words` | Parte 4, M1 |
| `bic`, `K_MIXTURE`, `mixture`, `membership`, `mixture_labels`, `top_prob` y `unsure` | Parte 4, M2 |
| `hdbscan_labels`, `n_groups`, `in_group`, `noise` y `hdbscan_words` | Parte 4, M3 |

```python
# SU CÓDIGO. Paso 2.3: k-means, mezcla gaussiana y HDBSCAN

```

**Listo cuando:**
- Cada método da un grupo por entradilla. HDBSCAN usa `min_cluster_size=FLOOR` y su ruido es -1.
- `membership` tiene una fila por entradilla que suma 1.

**Comprobar:**

En este paso comprobamos que cada método da un grupo por entradilla.

```python
assert len(kmeans_labels) == len(hdbscan_labels) == N and membership.shape == (N, K_MIXTURE)
print("Paso 2.3: OK")
```

### Paso 2.4. Línea base, estabilidad y acuerdo

En este paso comparan los grupos con el azar, entre semillas y entre métodos.

| Qué copiar | Dónde está en L3 |
|------------|------------------|
| `shuffled_silhouettes` y `BASELINE_P95` | Parte 5, Paso 1 |
| `seed_ari` | Parte 5, Paso 2 |
| `agreement` | Parte 5, Paso 3 |

```python
# SU CÓDIGO. Paso 2.4: shuffled_silhouettes, BASELINE_P95, seed_ari y agreement

```

**Listo cuando:**
- Hay `N_SHUFFLES` siluetas al azar y un índice de Rand por cada par de semillas.

**Comprobar:**

En este paso comprobamos el número de siluetas al azar y de pares de semillas.

```python
assert len(shuffled_silhouettes) == N_SHUFFLES and len(seed_ari) == 10
print("Paso 2.4: OK")
```

### Paso 2.5. Qué grupos lee la persona nueva y `outputs/grupos.csv`

En este paso deciden qué grupos lee la persona nueva, escriben lo que encontraron y guardan `outputs/grupos.csv`.

| Qué copiar | Dónde está en L3 |
|------------|------------------|
| `team_groups` y `read_group` con sus `TOPIC_WORDS` sin cambiarlas | Parte 5, Paso 4 |
| El hallazgo `structure_finding` | Parte 5, Paso 6 |
| Guardar los grupos | Parte 6, Paso 2 (aquí en `outputs/grupos.csv`) |

```python
# SU CÓDIGO. Paso 2.5: team_groups, read_group, structure_finding y outputs/grupos.csv

```

**Listo cuando:**
- `read_group` es verdadero o falso por entradilla y nunca verdadero en el ruido. Si ningún grupo toca su tema, también es un resultado.
- `structure_finding` (texto) da la silueta y el p95 de la línea base, la estabilidad, el % de ruido y qué significa para la lista.
- `outputs/grupos.csv` tiene `title`, `kmeans`, `mezcla`, `prob_mezcla` y `hdbscan`.

**Comprobar:**

En este paso comprobamos que el ruido nunca se lee y que `outputs/grupos.csv` tiene la columna `hdbscan`.

```python
assert not read_group[hdbscan_labels == -1].any() and "hdbscan" in pd.read_csv("outputs/grupos.csv")
print("Paso 2.5: OK")
```

---

## Ejercicio 3. Filtro de texto (Lección 4)

### Paso 3.1. La etiqueta, el conjunto marcado y `marcas.csv`

En este paso arman la etiqueta, apartan el conjunto marcado y escriben `marcas.csv` para marcar.

| Qué copiar | Dónde está en L4 |
|------------|------------------|
| La etiqueta `y` (aquí: 1 si el artículo tiene alguna categoría de `TARGETS[GROUP]`) | Parte 2, Paso 2 |
| `train_rows`, `marked_rows`, `train_texts`, `test_texts` y `y_train` | Parte 3, Paso 2 |

```python
# SU CÓDIGO. Paso 3.1: y, train_rows, marked_rows, train_texts, test_texts, y_train y marcas.csv

```

**Listo cuando:**
- `y` sale de la columna `categories` (separadas por `|`) y tiene al menos `min_positives(N)` positivos.
- `marcas.csv` tiene `n_flagged(N)` filas con `title`, `lead` y `marca` vacía. Si ya tiene marcas, no se sobrescribe.
- El grupo marca leyendo la entradilla, sin mirar categorías ni resultados: `1` si la persona nueva **debe abrir** la entrada, `0` si no. Excel en español guarda el CSV con punto y coma. Google Sheets (Archivo, Descargar, CSV) evita ese problema.

**Comprobar:**

En este paso comprobamos el tamaño del conjunto marcado y que `marcas.csv` tiene la columna `marca`.

```python
assert len(marked_rows) == n_flagged(N) and "marca" in pd.read_csv("marcas.csv", sep=None, engine="python")
print("Paso 3.1: OK. Ya pueden marcar.")
```

### Paso 3.2. Los tres métodos de texto

En este paso corren los tres métodos de texto sobre el conjunto marcado.

| Qué copiar | Dónde está en L4 |
|------------|------------------|
| `train_tokens`, `test_tokens`, `tfidf`, `X_train`, `X_test` y `feature_names` | Parte 3, Paso 3 |
| `keyword_match`, `pred_keywords` y `cv_keywords` | Parte 4, M1 |
| `lr`, `pred_lr` y `weights` | Parte 4, M2 |
| `vectors`, `V_train`, `V_test`, `lr_enc` y `pred_encoder` | Parte 4, M3 (guarde los vectores en `outputs/vectores.npy`) |

```python
# SU CÓDIGO. Paso 3.2: TF-IDF, las tres predicciones y los vectores

```

**Listo cuando:**
- `pred_keywords`, `pred_lr` y `pred_encoder` tienen una predicción de 0 o 1 por fila marcada.

**Comprobar:**

En este paso comprobamos que los tres métodos dan una predicción por fila marcada.

```python
assert len(pred_keywords) == len(pred_lr) == len(pred_encoder) == len(marked_rows)
print("Paso 3.2: OK")
```

### Paso 3.3. Aciertos y errores con sus marcas

En este paso cuentan aciertos y errores frente a sus marcas.

| Qué copiar | Dónde está en L4 |
|------------|------------------|
| Leer las marcas en `y_test`, en el orden de `marked_rows` | Parte 3, Paso 2 |
| `predictions` y `results` con `counts_of` | Parte 5, Paso 1 |
| `intervals` con `f1_interval` | Parte 5, Paso 3 |
| `folds`, `model_tfidf`, `model_encoder`, `cv_tfidf` y `cv_encoder` | Parte 5, Paso 4 |
| El intervalo de la diferencia de F1 | Parte 5, Paso 5 |

```python
# SU CÓDIGO. Paso 3.3: y_test, predictions, results, intervals, cv_tfidf, cv_encoder y error_reading

```

**Listo cuando:**
- `y_test` solo tiene 0 y 1, una marca por fila marcada.
- `results` tiene TP, FP, FN y TN para `clase mayor`, `palabras clave`, `TF-IDF` y `codificador`, y compara sus marcas con la etiqueta de los editores.
- `error_reading` (texto) da tres títulos mal clasificados y si cada error es del método o de la marca.

**Comprobar:**

En este paso comprobamos que hay una marca por fila marcada, los cuatro métodos en `results` y su lectura de errores.

```python
assert len(y_test) == len(marked_rows) and len(results) == 4 and error_reading.strip()
print("Paso 3.3: OK")
```

### Paso 3.4. Guardar el filtro de texto

En este paso guardan el filtro de texto de cada artículo en `outputs/texto.csv`.

| Qué copiar | Dónde está en L4 |
|------------|------------------|
| `text_says_read`, `encoder_says_read` y `marca` por artículo | Parte 6, Paso 1, y Parte 6, Paso 3 |
| La tabla de texto | Parte 6, Paso 3 (aquí en `outputs/texto.csv`) |

```python
# SU CÓDIGO. Paso 3.4: text_says_read, encoder_says_read, marca y outputs/texto.csv

```

**Listo cuando:**
- Cada artículo lleva la predicción de un modelo que no lo vio: los marcados con `pred_lr`, los de entrenamiento con `cv_tfidf`.
- `outputs/texto.csv` tiene una fila por artículo con `title`, `keyword`, `tfidf_lr`, `codificador` y `marca` (0 o 1 en las filas marcadas, vacía en las demás).

**Comprobar:**

En este paso comprobamos que las marcas guardadas son 0 o 1.

```python
assert pd.read_csv("outputs/texto.csv")["marca"].dropna().isin([0, 1]).all()
print("Paso 3.4: OK")
```

---

## Ejercicio 4. Despliegue

### Paso 4.1. Los resultados de cada artículo y `outputs/en_vista.csv`

En este paso juntan los resultados de cada artículo y guardan `outputs/en_vista.csv`.

| Qué copiar | Dónde está en L4 |
|------------|------------------|
| `supports` con las tres columnas, `supports` e `in_view` | Parte 6, Paso 1 |
| `prob_texto`, el orden y `recortado` con `MAX_ARTICLES` y `MIN_ARTICLES` de su descripción de la pregunta | Parte 6, Paso 2 |

```python
# SU CÓDIGO. Paso 4.1: supports, prob_texto, recortado y outputs/en_vista.csv

```

**Listo cuando:**
- Las columnas de resultados son `has_pattern` (un par con `kept_lift2` y una palabra de `TOPIC_WORDS`), `read_group` (un grupo de HDBSCAN que se lee) y `text_says_read` (TF-IDF dice abrir). `in_view` usa `MIN_SUPPORTS`, el número de resultados a favor que pide el código. `MIN_SUPPORTS` empieza en 2 y se puede cambiar. Cada grupo fija y justifica este número en su proyecto. 0 o 1 valen si se explica. Muestran una tabla pequeña con cuántos artículos tienen 0, 1, 2 y 3 o más resultados a favor, y con ella explican su elección.
- `outputs/en_vista.csv` tiene una fila por artículo con `title`, `has_pattern`, `read_group`, `text_says_read`, `prob_texto`, `supports`, `in_view` y `recortado`.
- `recortado` solo es verdadero en artículos en vista. Si quedan menos de `standard["min_articles"]`, no rellenan: imprimen que es un resultado débil.

**Comprobar:**

En este paso comprobamos que `outputs/en_vista.csv` tiene una fila por artículo y que solo se recortan artículos en vista.

```python
saved = pd.read_csv("outputs/en_vista.csv")
assert len(saved) == N and not (saved["recortado"] & ~saved["in_view"]).any()
print("Paso 4.1: OK")
```

### Paso 4.2. Qué cambiaría la decisión

En este paso escriben en `pregunta.json` cómo entran los grupos y el texto, y qué los cambiaría.

| Qué copiar | Dónde está |
|------------|------------|
| `group_use` con `how_it_enters`, `reading` y `what_changes_it` | L3, Parte 6, Paso 3 |
| `text_use` con las mismas claves | L4, Parte 6, Paso 4 |

```python
# SU CÓDIGO. Paso 4.2: group_use, text_use y pregunta.json guardado

```

**Listo cuando:**
- `pregunta.json` tiene `group_use` y `text_use`, cada uno con `how_it_enters`, `reading` y `what_changes_it`.

**Comprobar:**

En este paso comprobamos que `pregunta.json` tiene `group_use` y `text_use`.

```python
assert {"group_use", "text_use"} <= set(json.loads(Path("pregunta.json").read_text(encoding="utf-8")))
print("Paso 4.2: OK. Armen el ZIP.")
```

---

## Registro de contribución

En este paso cada integrante anota su tarea concreta, quién repartió las marcas y quién consolida el ZIP.

```python
# SU CÓDIGO. Registro: contribution_log, una línea por integrante, quién reparte las marcas y quién consolida el ZIP

```

**Listo cuando:**
- `contribution_log` (texto) tiene una línea con una tarea concreta por integrante y dice quién repartió las marcas y quién consolidó el ZIP.

## Para la reflexión individual

Use la [plantilla de la reflexión de la semana 2](https://cabrerac.github.io/assets/documents/26-udenar-data-mining/reflection-week-2-template.docx) y mantenga sus títulos. Extensión: entre 700 y 1000 palabras. Por debajo de 500 palabras el texto queda corto.

| Título | Qué escribir |
|--------|--------------|
| **Metadatos** | Nombre, grupo, semana 2 (L3 + L4), conteo aproximado de palabras y la lectura que cita. |
| **Proceso** | Qué hizo el grupo en el cuaderno de la semana 2. Diga cuál fue su contribución. |
| **Decisión** | Describa los grupos que encontró el grupo y los resultados del filtro de texto. Diga qué artículo le parece más útil para la persona nueva y por qué. |
| **Métodos** | Explique cuáles fueron los métodos utilizados en esta semana (k-means, mezcla gaussiana, HDBSCAN, TF-IDF y el codificador de texto) y cómo se comparan entre ellos. |
| **Ética** | Nombre una elección técnica de esta semana. Diga a quién ayuda o perjudica, o cómo se podría usar mal un resultado de esta semana. Relacione el punto con Jain (2010) o con Devlin, Chang, Lee y Toutanova (2019). |

## Entrega

El ZIP se entrega el martes 17 nov 2026, 23:59 (hora de Colombia), con el cuaderno ejecutado y renombrado.

| Archivo del ZIP `week-2-<group_id>.zip` | Descripción |
|-----------------------------------------|-------------|
| `week-2-group-<group_id>.ipynb` | Este cuaderno ejecutado |
| `pregunta.json` | La descripción de la pregunta con `group_use` y `text_use` |
| `marcas.csv` | Su conjunto marcado, con `marca` en 1 o 0 |
| `outputs/grupos.csv` | Los grupos de los tres métodos |
| `outputs/texto.csv` | Las predicciones de texto de cada artículo y sus marcas |
| `outputs/en_vista.csv` | Los resultados de las semanas 1 y 2, `prob_texto`, si el artículo queda en vista y si quedó `recortado` |

Estos archivos son la segunda iteración. En la semana 3 el grupo añade el lugar en el grafo y la predicción, y los compara con lo que ya tiene.

<!-- end NOTEBOOK: -->
