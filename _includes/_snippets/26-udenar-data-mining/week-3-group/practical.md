<!-- NOTEBOOK: -->

## Instrucciones

**Propósito.** Cuaderno de grupo de la semana 3 (Lecciones 5 y 6). Su grupo sigue como equipo interno de una alcaldía, con los artículos de su secretaría. Esta semana se cierra la **lista de inicio**, la lista de artículos para los nuevos integrantes del equipo.

**Esta semana.** Se suman dos resultados: el lugar de cada artículo en la red de enlaces (`outputs/grafo.csv`) y una predicción (`outputs/prediccion.csv`). Después arman la lista en `outputs/lista_inicial.csv`, con los resultados de las tres semanas que apoyan cada artículo y una frase escrita por el grupo: qué hecho lo sacaría de la lista.

**Requisito.** Ejecute primero los cuadernos individuales **L5** y **L6**. Este cuaderno lo escribe el grupo. Cada paso dice qué código de L5 o L6 adaptar. No pegue sin entender. Tengan en la carpeta `pregunta.json` y `outputs/en_vista.csv` de su ZIP de la semana 2. `marcas.csv` no se lee aquí, pero va de nuevo en el ZIP. El sábado 21 nov el grupo lo empieza de 10:00 a 10:45 y lo termina en casa.

**Datos de entrada.** El mismo archivo de su grupo: G1 Agricultura, G2 Salud mental, G3 Medio ambiente, G4 Inclusión Social y G5 Vivienda. La columna `links` trae los enlaces de la entradilla a otros artículos del mismo extracto. Un enlace es una mención en el texto, no una cita. Las categorías las pusieron quienes editan Wikipedia.

**Materiales.** [L5 Grafos](https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-data-mining/l5-graphs.ipynb) y [L6 Predicción](https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-data-mining/l6-prediction.ipynb).

**Pregunta del grupo.** ¿Qué artículos entran en la lista de inicio de su secretaría, qué resultados apoyan a cada uno y qué hecho lo sacaría?

**Entrega Moodle (martes 24 nov 2026, 23:59 Colombia).** ZIP `week-3-<group_id>.zip` con `week-3-group-<group_id>.ipynb` (este cuaderno ejecutado y renombrado), `pregunta.json`, `marcas.csv` de la semana 2, `outputs/grafo.csv`, `outputs/prediccion.csv`, `outputs/lista_inicial.csv`, `project-title-es.txt` y `project-abstract-es.txt`. El mismo cuaderno, con los arreglos después de la devolución, va en el ZIP del proyecto el martes 1 de diciembre.

**Mapa del cuaderno**

| Ejercicio | Tema | Entregable clave |
|-----------|------|------------------|
| **0** | Configuración | Grupo, etiqueta, datos, parámetros y funciones |
| **1** | Comprensión del negocio | La tarjeta y los resultados de la semana 2 |
| **2** | Comprensión de los datos | Títulos únicos y enlaces dentro del extracto |
| **3** | Preparación de los datos | Los grafos y la tabla de la L6 |
| **4** | Modelado | Grado, PageRank, puentes, node2vec y los tres métodos de la L6 |
| **5** | Evaluación | Un artículo por su lugar y si la L6 cuenta |
| **6** | Despliegue | `outputs/grafo.csv`, `outputs/prediccion.csv`, `outputs/lista_inicial.csv`, título y resumen |

**Celdas Comprobar.** Ejecute de arriba abajo. Una Comprobar revisa que exista lo pedido, con su forma. No revisa su respuesta. Si falla, corrija la celda anterior y vuelva a ejecutar desde ahí.

---

## Ejercicio 0. Configuración

### Paso 0.1. Grupo, etiqueta y datos

Cambie solo `GROUP`. La etiqueta de la L6 es `LABEL = "categoria_objetivo"`: 1 si la categoría del artículo (`categoria`) está en `TARGETS[GROUP]`, y 0 si no. `TARGETS` son las mismas categorías del filtro de la semana 2.

```python
import json
from pathlib import Path

import pandas as pd
import requests

GROUP = "G1"   # cambie a G2, G3, G4 o G5
LABEL = "categoria_objetivo"   # 1 si categoria está en TARGETS[GROUP], 0 si no
TARGETS = {"G1": ["Agrarismo", "Organizaciones agrícolas"], "G2": ["Trastornos mentales", "Psiquiatría"], "G3": ["Conservacionismo"],
           "G4": ["Hambrunas", "Hambre", "Bancos de alimentos"], "G5": ["Hipotecas", "Arrendamiento", "Huelgas de alquileres",
           "Vivienda asequible", "Vivienda pública"]}
EXTRACTS = {"G1": ("Agricultura", "agricultura.csv"), "G2": ("Salud mental", "salud-mental.csv"), "G3": ("Medio ambiente", "medio-ambiente.csv"),
            "G4": ("Inclusión Social", "inclusion-social.csv"), "G5": ("Vivienda", "vivienda.csv")}
SECRETARIAT, FILENAME = EXTRACTS[GROUP]
Path("outputs").mkdir(exist_ok=True)
path = Path("data") / FILENAME
path.parent.mkdir(exist_ok=True)
if not path.is_file():   # descarga una sola vez
    path.write_bytes(requests.get(f"https://cabrerac.github.io/assets/data/26-udenar-data-mining/{FILENAME}", timeout=60).content)
df = pd.read_csv(path, keep_default_na=False).drop_duplicates("title").reset_index(drop=True)
df = df.rename(columns={"label": "categoria"})   # en el extracto la columna se llama label
print(f"Grupo {GROUP}: secretaría de {SECRETARIAT}, {len(df)} artículos sin títulos repetidos. Etiqueta: {LABEL}")
```

### Paso 0.2. Parámetros, librerías y funciones

| Qué copiar | Dónde está |
|------------|------------|
| Los parámetros de la L5 (`SUPPORT_SHARE`, `SUPPORT_MIN`, `SEED`, `MIN_SUPPORTS`, `HUB_SHARE` a `N_RANDOM_PAIRS`), sin cambiar sus valores. `MIN_SUPPORTS` empieza en 2 y pueden cambiarlo si lo justifican | L5, Parte 1, Paso 1 |
| Los parámetros de la L6 (`FLAGGED_SHARE` a `N_FOLDS` y `HIDDEN_UNITS` a `SPLIT_SEEDS`), sin `LABEL` ni cambiar sus valores | L6, Parte 1, Paso 1 |
| Las importaciones de la L5 (networkx, gensim, random) | L5, Parte 1, Paso 1 |
| Las importaciones de la L6 (sklearn, scipy) | L6, Parte 1, Paso 1 |
| `support_floor` | L2, Parte 1, Paso 1 |
| `hub_threshold` | L5, Parte 1, Paso 1 |
| `n_flagged` y `min_positives` | L6, Parte 1, Paso 1 |
| `PROPERTY_COLUMN`, `LABEL_PROPERTY` y `n_claims_without` | L6, Parte 1, Paso 2 |
| `node2vec_walks` | L5, Parte 5, M3. Las caminatas |

```python
# SU CÓDIGO. Paso 0.2: parámetros, rutas de la entrega, importaciones, support_floor, hub_threshold, n_flagged, min_positives, n_claims_without, node2vec_walks y vote_of

```

**Listo cuando:**
- Los parámetros tienen los valores de L5 y L6.
- Las rutas son `pregunta.json`, `project-title-es.txt`, `project-abstract-es.txt` y, en `outputs/`, `en_vista.csv` (semana 2), `grafo.csv`, `prediccion.csv` y `lista_inicial.csv`.
- `vote_of(predicciones)` recibe las predicciones de los 3 métodos y devuelve, por fila, la clase que dicen al menos 2 como texto, o `None` si los tres dicen algo distinto. La etiqueta puede tener varias clases.

**Comprobar:**

```python
assert callable(node2vec_walks) and vote_of([["a", "b"], ["a", "c"], ["b", "d"]]) == ["a", None]
print("Paso 0.2: OK")
```

---

## Ejercicio 1. Comprensión del negocio

### Paso 1.1. La tarjeta y los resultados de la semana 2

| Qué copiar | Dónde está en L5 |
|------------|------------------|
| Leer la tarjeta en `question_card` | Parte 2, Paso 1 |
| Leer los resultados en `week2`, con las tres columnas en verdadero o falso | Parte 2, Paso 2 (aquí el archivo es `outputs/en_vista.csv`) |

```python
# SU CÓDIGO. Paso 1.1: question_card, week2 y graph_expectation

```

**Listo cuando:**
- `question_card` tiene `group_use` y `text_use`, y `week2` tiene `title`, `has_pattern`, `read_group`, `text_says_read` y `prob_texto`.
- `graph_expectation` (texto, escrito antes de mirar resultados) dice qué artículo creen que será el más enlazado y si una persona nueva debería abrirlo primero.

**Comprobar:**

```python
assert "text_use" in question_card and "prob_texto" in week2 and graph_expectation.strip()
print("Paso 1.1: OK")
```

---

## Ejercicio 2. Comprensión de los datos

### Paso 2.1. Títulos y enlaces

| Qué copiar | Dónde está en L5 |
|------------|------------------|
| `titles`, `N` y los títulos repetidos | Parte 3, Paso 1 (aquí `df` ya viene sin repetidos) |
| `listed`, los enlaces escritos | Parte 3, Paso 2 |

```python
# SU CÓDIGO. Paso 2.1: titles, N y listed

```

**Listo cuando:**
- `titles` tiene un título por artículo y `listed` una lista de enlaces por artículo.
- Saben cuántos artículos no enlazan a nadie, cuántos no tienen `inception_year` y cuántos tienen `kind = Other`.

**Comprobar:**

```python
assert len(titles) == N == len(listed) == len(df)
print("Paso 2.1: OK")
```

---

## Ejercicio 3. Preparación de los datos

### Paso 3.1. Los dos grafos y el componente mayor

| Qué copiar | Dónde está en L5 |
|------------|------------------|
| `links_out` y `neighbours` | Parte 4, Paso 1 (use `df` en lugar de `papers`) |
| `directed` y `graph` | Parte 4, Paso 2 |
| `largest`, `adj` y `no_vector` | Parte 4, Paso 3 |

```python
# SU CÓDIGO. Paso 3.1: links_out, neighbours, directed, graph, largest, adj y no_vector

```

**Listo cuando:**
- Los dos grafos tienen un nodo por título.
- Cada artículo está en `adj` o en `no_vector`, nunca en los dos.

**Comprobar:**

```python
assert graph.number_of_nodes() == N and len(adj) + len(no_vector) == N and not set(adj) & set(no_vector)
print("Paso 3.1: OK")
```

### Paso 3.2. La tabla de la L6

| Qué copiar | Dónde está en L6 |
|------------|------------------|
| `attributes` con `kind`, `year`, `has_date`, `has_country`, `has_image` y `n_claims_without` | Parte 4, Paso 1 |
| `train`, `test`, `y_train` y `y_test` con `n_flagged(N)` filas apartadas | Parte 4, Paso 2 |
| `prepare`, el `ColumnTransformer` | Parte 4, Paso 3 |

```python
# SU CÓDIGO. Paso 3.2: label_of, attributes, NUMBER_COLUMNS, CATEGORY_COLUMNS, y, inputs, train, test, y_train, y_test y prepare

```

**Listo cuando:**
- `label_of(attributes)` lee la etiqueta solo de su columna, según `LABEL`, y se detiene con un error si falta. Con `"categoria_objetivo"` da 1 si `categoria` está en `TARGETS[GROUP]` y 0 si no. `y = label_of(attributes)`.
- `kind` deja como `Other` los tipos con menos de `support_floor(N)` artículos. Si `LABEL` es `"tiene_imagen"`, `has_image` no es entrada.
- En los números `add_indicator=False`, porque `has_date` ya marca el año faltante.
- `test` tiene `n_flagged(N)` filas y no comparte títulos con `train`.

**Comprobar:**

```python
assert len(y) == N and len(test) == n_flagged(N) and not set(train.index) & set(test.index)
print("Paso 3.2: OK")
```

---

## Ejercicio 4. Modelado

### Paso 4.1. Grado, PageRank y puentes

| Qué copiar | Dónde está en L5 |
|------------|------------------|
| `degree`, `hubs` con `hub_threshold(N)` y `top_degree` | Parte 5, M1. El grado y la alerta de nodo central |
| `rank` con `nx.pagerank(directed, alpha=DAMPING)` y `top_rank` | Parte 5, M1. PageRank con networkx |
| `between`, redondeado a 9 decimales, y `bridges` | Parte 5, M2. Intermediación y puentes |

```python
# SU CÓDIGO. Paso 4.1: degree, hubs, top_degree, rank, top_rank, between y bridges

```

**Listo cuando:**
- Un puente es un artículo con enlaces, en el cuarto superior por intermediación entre los artículos con enlaces, que **no** es nodo central.
- Un nodo central (`hubs`) es una alerta, no una razón para leerlo.

**Comprobar:**

```python
assert len(bridges) >= 1 and not set(bridges) & set(hubs)
print("Paso 4.1: OK")
```

### Paso 4.2. node2vec

| Qué copiar | Dónde está en L5 |
|------------|------------------|
| Las caminatas y `Word2Vec` con `workers=1` | Parte 5, M3. Los vectores de node2vec |
| `neighbours_by_seed`, un diccionario por semilla con los 5 vecinos de cada artículo de `adj` | Parte 6, Paso 3 |

```python
# SU CÓDIGO. Paso 4.2: neighbours_by_seed y model

```

**Listo cuando:**
- Hay 3 diccionarios de vecinos, uno por semilla de `N2V_SEEDS`.
- `model` es el de la primera semilla, con un vector de `NODE_DIMENSIONS` números por artículo de `adj`.

**Comprobar:**

```python
assert len(neighbours_by_seed) == 3 and model.wv.vectors.shape == (len(adj), NODE_DIMENSIONS)
print("Paso 4.2: OK")
```

### Paso 4.3. Los tres métodos de la L6

| Qué copiar | Dónde está en L6 |
|------------|------------------|
| `lr` | Parte 5, M1. Regresión logística |
| `forest` | Parte 5, M2. Bosque aleatorio |
| `network` | Parte 5, M3. Una capa oculta |
| `models` con `make_pipeline(prepare, ...)` y `test_predictions` | Parte 7, Paso 1 |

```python
# SU CÓDIGO. Paso 4.3: lr, forest, network, models y test_predictions

```

**Listo cuando:**
- Los tres métodos se entrenan con `train`, y `test_predictions` tiene tres listas, una predicción por fila apartada.

**Comprobar:**

```python
assert len(models) == 3 and all(len(p) == len(test) for p in test_predictions)
print("Paso 4.3: OK")
```

---

## Ejercicio 5. Evaluación

### Paso 5.1. Un artículo descrito por su lugar

| Qué copiar | Dónde está en L5 |
|------------|------------------|
| `overlap`, la parte de los 5 vecinos que se repite entre semillas | Parte 6, Paso 3 |
| `near` y `far`, el Jaccard de categorías con vecinos y con pares al azar | Parte 6, Paso 4 (aquí las categorías están en `categories`) |
| `MY_ARTICLE` y su descripción por grado, PageRank, intermediación y vecinos | Parte 6, Paso 2 |

```python
# SU CÓDIGO. Paso 5.1: overlap, near, far, MY_ARTICLE y place_reading

```

**Listo cuando:**
- `MY_ARTICLE` es un título del componente mayor y no es nodo central. Si no tiene vector, lo dicen.
- `place_reading` (texto) dice qué dice su lugar y por qué ser central solo porque enlaza a muchos no es razón para leerlo.

**Comprobar:**

```python
assert MY_ARTICLE in titles and MY_ARTICLE not in hubs and 0 <= overlap <= 1 and place_reading.strip()
print("Paso 5.1: OK")
```

### Paso 5.2. ¿Cuenta la L6?

| Qué copiar | Dónde está en L6 |
|------------|------------------|
| `folds` y `train_predictions`, las predicciones fuera del pliegue | Parte 6, Paso 3 |
| `evaluation`, exactitud y F1 macro de la clase mayor y de los tres métodos | Parte 6, Pasos 1 y 3 |
| `majority` y `l6_counts` | Parte 6, Paso 4 |
| `seeds_holding` con `SPLIT_SEEDS` y `clone(m)` | Parte 6, Paso 6 |

```python
# SU CÓDIGO. Paso 5.2: folds, train_predictions, evaluation, majority, l6_counts, seeds_holding y l6_finding

```

**Listo cuando:**
- La clase mayor es `y_test.value_counts(normalize=True).max()`.
- `l6_counts` dice si la predicción entra en la lista. Es `True` solo si cada uno de los tres métodos acierta en las filas apartadas más que la clase mayor, por un margen de `MARGIN` (0,02, una o dos filas de unas 60, como en la L6). Si es `False`, la predicción no apoya su lista. Es un resultado normal y válido, no un error: lo informan en el proyecto y explican por qué (los métodos no le ganan a la clase mayor por más de `MARGIN`).
- `l6_finding` (texto) da la clase mayor, la exactitud de los tres métodos, `l6_counts` y en cuántas de las 5 particiones se sostiene, y qué significa para la lista.

**Comprobar:**

```python
assert isinstance(l6_counts, bool) and l6_finding.strip()
print("Paso 5.2: OK")
```

---

## Ejercicio 6. Despliegue

### Paso 6.1. La tabla con los cinco resultados

| Columna | De dónde sale | Dónde está |
|---------|---------------|------------|
| `has_pattern`, `read_group`, `text_says_read` | `week2`, unidas por título | L5, Parte 7, Paso 1 |
| `graph_support` | el artículo está en `bridges` | L5, Parte 7, Paso 1 |
| `prediction` | al menos 2 de 3 métodos, con `vote_of`, fuera del pliegue o apartada | L6, Parte 7, Paso 1 |
| `one_support` | si la etiqueta repite el texto de la L4 | L6, Parte 7, Paso 2 |

```python
# SU CÓDIGO. Paso 6.1: table, graph_support, voted, prediction y one_support

```

**Listo cuando:**
- `table` tiene una fila por título (el índice) y las cinco columnas en verdadero o falso. `voted` es la clase votada de cada artículo. `alerta_centro` nunca cuenta como resultado a favor.
- La etiqueta tiene dos clases. `prediction` es verdadero si la clase votada es `"1"`, es decir, si al menos 2 de los 3 métodos dicen que la categoría está en `TARGETS[GROUP]`. `one_support` es `abs(phi) >= 0.30`, con phi entre la etiqueta y `text_says_read`.

**Comprobar:**

```python
assert len(table) == N and table["graph_support"].dtype == table["prediction"].dtype == bool
print("Paso 6.1: OK")
```

### Paso 6.2. La lista de inicio

| Qué copiar | Dónde está en L6 |
|------------|------------------|
| `SUPPORT_COLUMNS`, `table["supports"]` y `table["in_view"]`, con la rama de `one_support` | Parte 7, Paso 3 |
| `drop_one` | Parte 7, Paso 4 |
| `starter_list`, ordenada por número de resultados a favor, `prob_texto` y título, con `recortado` | Parte 7, Paso 5 |

```python
# SU CÓDIGO. Paso 6.2: SUPPORT_COLUMNS, supports, in_view, drop_one y starter_list

```

**Listo cuando:**
- `prob_texto` sale de `week2` y `starter_list` tiene `alerta_centro` (el artículo está en `hubs`). Un artículo con `alerta_centro` solo queda por sus resultados a favor.
- `starter_list` tiene los artículos con al menos `MIN_SUPPORTS` resultados a favor. El código empieza en 2. Cambien el valor si lo justifican, 0 o 1 también valen. Muestran una tabla pequeña con cuántos artículos tienen 0, 1, 2 y 3 o más resultados a favor, y con ella explican su elección. Los no recortados son como mucho `standard["max_articles"]`. Si quedan menos de `standard["min_articles"]`, no rellenan: imprimen que es un resultado débil.

**Comprobar:**

```python
assert starter_list["supports"].between(0, len(SUPPORT_COLUMNS)).all() and starter_list["alerta_centro"].dtype == bool
print("Paso 6.2: OK")
```

### Paso 6.3. Qué hecho sacaría cada artículo

| Qué copiar | Dónde está en L6 |
|------------|------------------|
| `drop_one`, para ver de qué resultado depende más la lista | Parte 7, Paso 4 |

```python
# SU CÓDIGO. Paso 6.3: hecho_que_saca, la columna en starter_list y what_changes

```

**Listo cuando:**
- `hecho_que_saca` es un diccionario de título a un hecho concreto (por ejemplo, "si el grupo de HDBSCAN que lo apoya se rompe con otra semilla") y está en `starter_list["hecho_que_saca"]`. Ningún no recortado queda vacío.
- `what_changes` (texto) dice de qué resultado depende más la lista y qué la cambiaría.

**Comprobar:**

```python
assert "hecho_que_saca" in starter_list and what_changes.strip()
print("Paso 6.3: OK")
```

### Paso 6.4. Guardar los archivos

| Archivo | Columnas | Dónde está |
|---------|----------|------------|
| `outputs/grafo.csv` | `title`, `grado`, `pagerank`, `intermediacion`, `aislado`, `alerta_centro`, `graph_support`, `supports` e `in_view`. Pueden sumar `sin_vector_n2v` y `vecinos_n2v` | L5, Parte 7, Paso 2 |
| `outputs/prediccion.csv` | `title`, `etiqueta`, `apartada`, `clase_votada` y `prediction` | L6, Parte 7, Paso 6 |
| `outputs/lista_inicial.csv` | las de `SUPPORT_COLUMNS` y `title`, `supports`, `prob_texto`, `recortado`, `alerta_centro` y `hecho_que_saca` | L6, Parte 7, Paso 6 |

```python
# SU CÓDIGO. Paso 6.4: los tres archivos y pregunta.json

```

**Listo cuando:**
- Los tres archivos existen con sus columnas.
- `pregunta.json` tiene `graph_use` y `prediction_use`, cada uno con `how_it_enters` y `what_changes_it`, como en la L6, Parte 7, Paso 7.

**Comprobar:**

```python
assert "prediction_use" in json.loads(Path("pregunta.json").read_text(encoding="utf-8"))
assert Path("outputs/lista_inicial.csv").is_file() and Path("outputs/grafo.csv").is_file()
print("Paso 6.4: OK")
```

### Paso 6.5. El título y el resumen de la charla

| Qué ver | Dónde está |
|---------|------------|
| El formato del título y del resumen | [project-title-es.example.txt](https://cabrerac.github.io/assets/documents/26-udenar-data-mining/project-title-es.example.txt) y [project-abstract-es.example.txt](https://cabrerac.github.io/assets/documents/26-udenar-data-mining/project-abstract-es.example.txt) (sobre el laboratorio de artículos, no sirven para copiar) |

```python
# SU CÓDIGO. Paso 6.5: project_title y project_abstract, guardados con write_text(..., encoding="utf-8")

```

**Listo cuando:**
- `project-title-es.txt` tiene el título de la charla del sábado 28 de noviembre, con menos de 15 palabras.
- `project-abstract-es.txt` es un solo párrafo de unas 120 palabras: la secretaría, la pregunta de la persona nueva, los resultados que apoyan la lista y qué hecho sacaría un artículo.

**Comprobar:**

```python
assert 0 < len(Path("project-title-es.txt").read_text(encoding="utf-8").split()) < 15
print("Paso 6.5: OK")
```

## Registro de contribución

```python
# SU CÓDIGO. Registro: contribution_log, una línea por integrante y quién consolida el ZIP

```

**Listo cuando:**
- `contribution_log` (texto) tiene una línea con una tarea concreta por integrante y dice quién consolidó el ZIP.

## Para la reflexión individual

Use la [plantilla de la reflexión de la semana 3](https://cabrerac.github.io/assets/documents/26-udenar-data-mining/reflection-week-3-template.docx) y mantenga sus títulos. Extensión: entre 700 y 1000 palabras. Por debajo de 500 palabras el texto queda corto.

| Título | Qué escribir |
|--------|--------------|
| **Metadatos** | Nombre, grupo, semana 3 (L5 + L6), conteo aproximado de palabras y la lectura que cita. |
| **Proceso** | Qué hizo el grupo en el cuaderno de la semana 3. Diga cuál fue su contribución. |
| **Decisión** | Describa la lista de inicio de su grupo. Elija un artículo de `outputs/lista_inicial.csv` y diga por qué está en la lista y qué hecho lo sacaría. |
| **Métodos** | Explique cuáles fueron los métodos utilizados en esta semana (grado, PageRank, puentes y los modelos de predicción) y cómo se comparan entre ellos. |
| **Ética** | Nombre una elección técnica de esta semana. Diga a quién ayuda o perjudica, o cómo se podría usar mal un resultado de esta semana. Relacione el punto con Page, Brin, Motwani y Winograd (1998) o con LeCun, Bengio y Hinton (2015). |

## Entrega

| Archivo del ZIP `week-3-<group_id>.zip` | Descripción |
|-----------------------------------------|-------------|
| `week-3-group-<group_id>.ipynb` | Este cuaderno ejecutado |
| `pregunta.json` | La tarjeta con `graph_use` y `prediction_use` |
| `marcas.csv` | Su conjunto marcado de la semana 2 |
| `outputs/grafo.csv` | El lugar de cada artículo en la red, con `graph_support` y `alerta_centro` |
| `outputs/prediccion.csv` | La clase votada y el resultado de la predicción |
| `outputs/lista_inicial.csv` | Los artículos en vista, con los resultados que los apoyan, `recortado`, `alerta_centro` y `hecho_que_saca` |
| `project-title-es.txt` | El título de la charla, con menos de 15 palabras |
| `project-abstract-es.txt` | El resumen de la charla, un párrafo de unas 120 palabras |

La lista de inicio es el producto del proyecto. Cada artículo muestra los resultados que lo apoyan y un hecho que lo sacaría. Estos archivos son la tercera iteración.

<!-- end NOTEBOOK: -->
