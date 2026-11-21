<!-- NOTEBOOK: -->

## Instrucciones

**Propósito.** Cuaderno de grupo de la semana 2 (Lecciones 3 y 4). Su grupo sigue como equipo interno de una alcaldía, con los artículos de su secretaría. El producto del proyecto es una lista de artículos para los nuevos integrantes del equipo.

**Esta semana.** El grupo repite en sus artículos lo que hicieron las Lecciones 3 y 4, con el método de grupos y el método de texto que mejor se ajustan a estos datos: HDBSCAN y TF-IDF con regresión logística. El resultado de la lista de esta semana es `outputs/lectura_semana_2.csv`. La tabla de cada artículo es `outputs/en_vista.csv`.

**Antes de empezar.** Ejecuten primero los cuadernos individuales de las Lecciones 3 y 4. Este cuaderno lo escribe el grupo. Traigan de los laboratorios los parámetros, las funciones y las figuras. Suban `outputs/patrones.csv` de la semana 1.

**Datos de entrada.** El mismo archivo de la semana 1: G1 Agricultura, G2 Salud mental, G3 Medio ambiente, G4 Inclusión Social y G5 Vivienda. El texto es la columna `lead`, la **descripción** del artículo. La etiqueta de entrenamiento sale de las categorías que pusieron quienes editan Wikipedia.

**Materiales.** [L3 Grupos](https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-data-mining/l3-groups.ipynb) y [L4 Texto](https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-data-mining/l4-text.ipynb).

**Primero etiquetan, después miden el método de texto.** El Paso 3.3 escribe `etiquetas.csv` con 60 a 67 artículos, unos 15 a 21 por persona. Etiqueten leyendo la descripción, sin mirar las categorías, y vuelvan a subir el archivo.

**Las decisiones son del grupo.** El grupo puede cambiar la pregunta, las palabras del tema, un umbral o el alcance. Escriban la razón en el paso donde lo cambia.

**Pregunta del grupo.** ¿Qué artículos de su secretaría debe leer primero una persona nueva en el equipo? Busquen grupos con HDBSCAN y filtren el texto con TF-IDF y regresión logística.

**Mapa del cuaderno**

| Ejercicio | Tema | Entregable clave |
|-----------|------|------------------|
| **0** | Configuración | Grupo, datos, patrones de la semana 1 y parámetros |
| **1** | Comprensión del negocio | La nota de si la pregunta cambió, y las palabras del tema |
| **2** | Comprensión de los datos | Descripciones útiles, su largo y las palabras del tema en ellas |
| **3** | Preparación de los datos | Conteos y SVD, etiquetas y TF-IDF |
| **4** | Modelado | HDBSCAN y TF-IDF con regresión logística |
| **5** | Evaluación | Silueta, grupos leídos, exactitud y matriz de confusión, `outputs/grupos.csv` y `outputs/texto.csv` |
| **6** | Despliegue | `outputs/lectura_semana_2.csv` (hasta 30) y `outputs/en_vista.csv` |

---

## Ejercicio 0. Configuración

### Paso 0.1. Grupo y datos

En este paso eligen el grupo, descargan el archivo de su secretaría y leen los patrones de la semana 1.
Cambien solo `GROUP`. `TARGETS` son las categorías de la etiqueta, elegidas por el profesor.

```python
from pathlib import Path

import pandas as pd
import requests

GROUP = "G1"   # cambie a G2, G3, G4 o G5
EXTRACTS = {"G1": ("Agricultura", "agricultura.csv"), "G2": ("Salud mental", "salud-mental.csv"), "G3": ("Medio ambiente", "medio-ambiente.csv"),
            "G4": ("Inclusión Social", "inclusion-social.csv"), "G5": ("Vivienda", "vivienda.csv")}
TARGETS = {"G1": ["Agrarismo", "Organizaciones agrícolas"], "G2": ["Trastornos mentales", "Psiquiatría"], "G3": ["Conservacionismo"],
           "G4": ["Hambrunas", "Hambre", "Bancos de alimentos"],
           "G5": ["Hipotecas", "Arrendamiento", "Huelgas de alquileres", "Vivienda asequible", "Vivienda pública"]}
SECRETARIAT, FILENAME = EXTRACTS[GROUP]
DATA_DIR = Path("data")  # aquí queda el CSV
OUTPUTS_DIR = Path("outputs")  # aquí quedan las tablas y las figuras
DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
path = DATA_DIR / FILENAME
if not path.is_file():  # usa el archivo si ya está
    path.write_bytes(requests.get(f"https://cabrerac.github.io/assets/data/26-udenar-data-mining/{FILENAME}", timeout=60).content)
articles = pd.read_csv(path, keep_default_na=False)  # una fila por artículo. Una descripción vacía queda como texto vacío
assert (OUTPUTS_DIR / "patrones.csv").is_file(), "Suban outputs/patrones.csv de la semana 1 y vuelvan a ejecutar esta celda"
patterns = pd.read_csv(OUTPUTS_DIR / "patrones.csv")  # los pares de la semana 1
print(f"Grupo {GROUP}: secretaría de {SECRETARIAT}, {len(articles)} artículos, {len(patterns)} pares de la semana 1")
```

### Paso 0.2. Importaciones, parámetros y funciones de apoyo

En este paso preparan lo que usa el resto del cuaderno, como en la semana 1. Va en tres celdas.
Primero las importaciones de las Lecciones 3 y 4.

```python
# SU CÓDIGO. Paso 0.2a: las importaciones de las Lecciones 3 y 4
```

Después los parámetros de las Lecciones 2, 3 y 4, con los valores de los laboratorios.

```python
# SU CÓDIGO. Paso 0.2b: los parámetros de las Lecciones 2, 3 y 4, MAX_PAPERS, N_FOLDS y folds
```

Al final las dos funciones de tamaño: el soporte mínimo de la Lección 2 y el tamaño del conjunto etiquetado de la Lección 4.

```python
# SU CÓDIGO. Paso 0.2c: support_floor y n_flagged
```

**Listo cuando:**
- Los parámetros tienen los valores de los laboratorios, también `MAX_PAPERS = 30` y `N_FOLDS = 5`.
- `folds` es la validación cruzada en cinco pliegues de la Lección 4, con `SEED`. Un pliegue es una de esas cinco partes.

**Comprobar:**

En este paso comprobamos algunas importaciones, algunos valores de los laboratorios y las dos funciones con unos tamaños conocidos.

```python
assert callable(HDBSCAN) and callable(TfidfVectorizer) and callable(LogisticRegression) and callable(silhouette_score)
assert (READ_SHARE, DENSITY_SVD_DIRECTIONS, N_FOLDS, MAX_PAPERS) == (0.5, 10, 5, 30) and folds.get_n_splits() == N_FOLDS
assert support_floor(100) == 5 and support_floor(300) == 9 and n_flagged(100) == 40 and n_flagged(300) == 60
print("Paso 0.2: OK")
```

---

## Ejercicio 1. Comprensión del negocio

### Paso 1.1. ¿Cambió la pregunta?

La pregunta y el problema ya están en el cuaderno de la semana 1 y en el documento de requerimientos.
En este paso escriben solo si algo cambió.
Si la pregunta o el alcance siguen iguales, escriban "Sin cambio".
Si cambiaron, escriban la línea nueva y por qué.

**Cambio**

**ESCRIBA SU TEXTO AQUÍ**

### Paso 1.2. Las palabras del tema

En este paso escriben las palabras del tema antes de ver ningún grupo, como en la Lección 3.
Van en minúsculas, con y sin tilde, en singular y plural, con un comentario por palabra.

```python
# SU CÓDIGO. Paso 1.2: TOPIC_WORDS
```

**Comprobar:**

En este paso comprobamos el tamaño de la lista y que está en minúsculas.

```python
assert len(TOPIC_WORDS) >= 5 and all(w == w.lower() for w in TOPIC_WORDS)
print("Paso 1.2: OK")
```

---

## Ejercicio 2. Comprensión de los datos

### Paso 2.1. Palabras útiles

En este paso traen `words` y `word_list` de la Lección 3 y las palabras vacías del español de la semana 1.

```python
# SU CÓDIGO. Paso 2.1: STOP_WORDS, word_list y words
```

**Comprobar:**

En este paso comprobamos las palabras vacías y las dos funciones con un texto corto.

```python
assert "también" in STOP_WORDS and word_list("El suelo y el agua del suelo", STOP_WORDS) == ["suelo", "agua", "suelo"]
assert words("El suelo y el agua del suelo", STOP_WORDS) == {"suelo", "agua"}
print("Paso 2.1: OK")
```

### Paso 2.2. Descripciones útiles y su largo

En este paso dejan las descripciones con al menos 5 palabras útiles y cuentan las palabras de cada una.

```python
# SU CÓDIGO. Paso 2.2: articles, texts, N y lead_words
```

**Comprobar:**

En este paso comprobamos que los textos, los artículos y los largos tienen las mismas filas.

```python
assert len(texts) == N == len(articles) == len(lead_words)
print("Paso 2.2: OK")
```

### Paso 2.3. Palabras del tema en las descripciones

En este paso cuentan qué parte de las descripciones tiene cada palabra del tema, como en la Lección 3.

```python
# SU CÓDIGO. Paso 2.3: lead_sets y topic_share
```

**Comprobar:**

En este paso comprobamos que hay un conjunto por descripción y una proporción por palabra del tema.

```python
assert len(lead_sets) == N and isinstance(topic_share, pd.Series) and len(topic_share) == len(TOPIC_WORDS)
print("Paso 2.3: OK")
```

Miren las palabras con la proporción más alta. Una palabra que está en casi todas las descripciones, como el nombre de la secretaría, describe toda la colección.
¿Esta palabra distingue un grupo de otro? ¿La dejan en `TOPIC_WORDS`? Escriban por qué.

**ESCRIBA SU TEXTO AQUÍ**

---

## Ejercicio 3. Preparación de los datos

### Paso 3.1. Conteos y largo 1

En este paso preparan la entrada de HDBSCAN, como en la Lección 3, Parte 3.
Una palabra entra si está en al menos `FLOOR` descripciones y en no más de la mitad.
Cada fila queda de largo 1.

```python
# SU CÓDIGO. Paso 3.1: FLOOR, counts, vocabulary y X
```

**Comprobar:**

En este paso comprobamos el umbral, el vocabulario y la forma de los conteos.

```python
assert FLOOR == support_floor(N) and counts.shape == (N, len(vocabulary)) and (counts > 0).sum(axis=0).min() >= FLOOR
assert X.shape == counts.shape
print(f"Paso 3.1: OK. Umbral {FLOOR}, vocabulario {len(vocabulary)}")
```

### Paso 3.2. SVD y distancias

En este paso reducen las filas a 10 direcciones de la SVD y calculan la distancia coseno, la entrada de HDBSCAN.
Traigan también `group_words`, que da las palabras principales de un grupo.

```python
# SU CÓDIGO. Paso 3.2: Z, distances y group_words
```

**Comprobar:**

En este paso comprobamos la forma de las entradas de HDBSCAN.

```python
assert Z.shape == (N, DENSITY_SVD_DIRECTIONS) and distances.shape == (N, N) and callable(group_words)
print("Paso 3.2: OK")
```

### Paso 3.3. La etiqueta y el conjunto etiquetado

En este paso arman la etiqueta de las categorías y apartan el conjunto etiquetado, como en la Lección 4.
La etiqueta vale 1 si el artículo tiene alguna categoría de `TARGETS[GROUP]`. Las categorías van separadas por `|`.
Escriban `etiquetas.csv` con `title`, `lead` y `etiqueta` vacía para los artículos apartados. Si el archivo ya tiene etiquetas, no lo sobrescriban.
Escriban `1` si la persona nueva **debe abrir** la entrada y `0` si no.
Excel en español guarda el CSV con punto y coma. Google Sheets (Archivo, Descargar, CSV) evita ese problema.

```python
# SU CÓDIGO. Paso 3.3: y, train_rows, marked_rows, LABELS_PATH y etiquetas.csv
```

**Comprobar:**

En este paso comprobamos el tamaño del conjunto etiquetado y que las dos partes cubren todos los artículos.

```python
assert len(marked_rows) == n_flagged(N) and len(train_rows) + len(marked_rows) == N and LABELS_PATH.is_file()
print("Paso 3.3: OK. Ya pueden etiquetar.")
```

### Paso 3.4. TF-IDF

En este paso pesan las palabras con TF-IDF, ajustado solo con las filas de entrenamiento, como en la Lección 4.

```python
# SU CÓDIGO. Paso 3.4: X_train y X_marked
```

**Comprobar:**

En este paso comprobamos la forma de las dos tablas.

```python
assert X_train.shape[0] == len(train_rows) and X_marked.shape == (len(marked_rows), X_train.shape[1])
print("Paso 3.4: OK")
```

---

## Ejercicio 4. Modelado

### Paso 4.1. HDBSCAN

En este paso buscan zonas densas con HDBSCAN, como en la Lección 3.
Usen `min_cluster_size=FLOOR`. El ruido queda en $-1$ y no se borra: impriman los 5 artículos de ruido más citados o los primeros 5.

```python
# SU CÓDIGO. Paso 4.1: hdbscan_labels, in_group y n_groups
```

**Comprobar:**

En este paso comprobamos que hay un grupo o $-1$ por artículo.

```python
assert len(hdbscan_labels) == N and hdbscan_labels.min() >= -1 and n_groups == hdbscan_labels.max() + 1
print("Paso 4.1: OK")
```

### Paso 4.2. TF-IDF con regresión logística

En este paso entrenan la regresión logística sobre TF-IDF, como en la Lección 4.
Cada artículo recibe la probabilidad de un modelo que no lo vio.
Las filas de entrenamiento usan validación cruzada en cinco pliegues (`cross_val_predict`).
Un pliegue es una de esas cinco partes.
`prob_texto` es esa probabilidad.
`pred_tfidf` vale 1 si pasa de 0,5.

```python
# SU CÓDIGO. Paso 4.2: prob_texto y pred_tfidf
```

**Comprobar:**

En este paso comprobamos que hay una probabilidad por artículo y que coincide con la predicción.

```python
assert len(prob_texto) == len(pred_tfidf) == N and ((prob_texto > 0.5) == pred_tfidf).all()
print("Paso 4.2: OK")
```

---

## Ejercicio 5. Evaluación

La evaluación usa dos comprobaciones: la silueta para los grupos, y la exactitud con la matriz de confusión para el texto.
La silueta va de −1 a 1. Entre 0,26 y 0,50 la estructura es débil y podría ser artificial (Kaufman y Rousseeuw, 1990).
Con 0,25 o menos no hay estructura sustancial. Entonces los grupos son una ayuda para leer.
Si su silueta queda baja, escríbanlo así. No cambien parámetros solo para subirla.
Un grupo se lee cuando al menos la mitad de sus artículos contiene una palabra del tema.

### Paso 5.1. La silueta de HDBSCAN

En este paso calculan la silueta coseno de HDBSCAN sin el ruido, con su banda de Kaufman y Rousseeuw.
Esa silueta deja fuera la parte de ruido del Paso 4.1, los artículos que no entran en ningún grupo. La de k-means en la Lección 3 usa todos los artículos.
Por eso no se comparan uno a uno. Impriman la parte de ruido junto a la silueta.
Dibujen el tamaño de cada grupo, como la figura de la Lección 3.

```python
# SU CÓDIGO. Paso 5.1: silhouette_hdbscan, noise_share, band y la figura
```

**Comprobar:**

En este paso comprobamos la silueta, la parte de ruido y la banda.

```python
assert -1 <= silhouette_hdbscan <= 1 and 0 <= noise_share <= 1 and isinstance(band, str)
print("Paso 5.1: OK")
```

### Paso 5.2. Qué grupos se leen

En este paso aplican la regla de lectura a los grupos de HDBSCAN, como en la Lección 3.
El ruido nunca se lee. Si no se lee ningún grupo, también es un resultado.
Impriman, por grupo, su tamaño, la parte con palabras del tema y sus 4 palabras principales.
`topic_part` guarda, por artículo, esa parte si su grupo se lee, y 0 si no.

```python
# SU CÓDIGO. Paso 5.2: has_topic, groups_read, topic_part y read_hdbscan
```

**Comprobar:**

En este paso comprobamos que el ruido nunca se lee y que un artículo leído tiene al menos la mitad.

```python
assert len(read_hdbscan) == len(topic_part) == N and not read_hdbscan[hdbscan_labels == -1].any()
assert (topic_part[read_hdbscan == 1] >= READ_SHARE).all()
print("Paso 5.2: OK")
```

### Paso 5.3. Aciertos y errores en las etiquetas

En este paso cuentan aciertos y errores de TF-IDF en el conjunto etiquetado, como en la Lección 4.
Usen sus etiquetas si `etiquetas.csv` está completo.
Si no, usen la etiqueta de las categorías y díganlo: entonces los números son provisionales.
Sumen la fila de la clase mayoritaria: dar a todos la etiqueta más frecuente.
Es la línea de referencia.

```python
# SU CÓDIGO. Paso 5.3: y_labelled, LABELS_SOURCE, counts_of y results
```

**Comprobar:**

En este paso comprobamos las dos filas y que los conteos suman las filas etiquetadas.

```python
assert list(results.index) == ["clase mayoritaria", "TF-IDF"]
assert (results[["TP", "FP", "FN", "TN"]].sum(axis=1) == len(marked_rows)).all()
print("Paso 5.3: OK")
```

### Paso 5.4. Guardar los resultados

En este paso guardan los grupos y el texto de cada artículo, como los patrones de la semana 1.

```python
# SU CÓDIGO. Paso 5.4: outputs/grupos.csv y outputs/texto.csv
```

**Listo cuando:**
- `grupos.csv` tiene `title`, `hdbscan` y `hdbscan_leido`.
- `texto.csv` tiene `title`, `etiqueta` (vacía fuera del conjunto etiquetado), `tfidf` y `prob_texto`.

**Comprobar:**

En este paso comprobamos las columnas de los dos archivos.

```python
saved_groups, saved_text = pd.read_csv(OUTPUTS_DIR / "grupos.csv"), pd.read_csv(OUTPUTS_DIR / "texto.csv")
assert {"title", "hdbscan", "hdbscan_leido"} <= set(saved_groups.columns)
assert {"title", "etiqueta", "tfidf", "prob_texto"} <= set(saved_text.columns)
assert saved_text["etiqueta"].notna().sum() == len(marked_rows)
print("Paso 5.4: OK")
```

---

## Ejercicio 6. Despliegue

### Paso 6.1. Artículos para leer

En este paso arman la lista de lectura de esta semana con los dos métodos.
HDBSCAN filtra: solo entran los artículos de los grupos que se leen. TF-IDF ordena: dentro de esos grupos, de mayor a menor `prob_texto`, y después por título.
La lista es el orden de TF-IDF dentro de los grupos leídos. No suma las dos partes.
Guarden como máximo 30 artículos en `outputs/lectura_semana_2.csv`, con `title`, `hdbscan` (el grupo), `prob_texto` y `tfidf`.
¿Es este método estadísticamente válido? ¿Pueden mejorar su rigurosidad o reemplazarlo de alguna forma, de acuerdo con su conocimiento estadístico?

```python
# SU CÓDIGO. Paso 6.1: reading y outputs/lectura_semana_2.csv
```

### Paso 6.2. La tabla para el proyecto

En este paso guardan todos los artículos en `outputs/en_vista.csv` para el cuaderno del proyecto.
`has_pattern` dice si la descripción tiene un par de la semana 1 con una palabra del tema. `read_group` dice si HDBSCAN lo pone en un grupo leído. `text_says_read` dice si TF-IDF dice que se abra.

```python
# SU CÓDIGO. Paso 6.2: week2 y outputs/en_vista.csv
```

### Paso 6.3. Interpretación de resultados

¿Por qué se seleccionaron los artículos de la lista resultante esta semana?
Explique la selección de acuerdo con HDBSCAN, TF-IDF y la pregunta.
¿TF-IDF supera a la clase mayoritaria?
Con la silueta y la parte de ruido, diga si los grupos sirven para leer.
Si la silueta queda baja, escríbalo así.

**Interpretación**

**ESCRIBA SU TEXTO AQUÍ**

**Comprobar:**

En este paso comprobamos el largo de la lista, que todo viene de grupos leídos, el orden de TF-IDF y las columnas de `outputs/en_vista.csv`.

```python
reading_list = pd.read_csv(OUTPUTS_DIR / "lectura_semana_2.csv")
week2 = pd.read_csv(OUTPUTS_DIR / "en_vista.csv")
assert len(reading_list) == min(MAX_PAPERS, read_hdbscan.sum()) and reading_list["prob_texto"].is_monotonic_decreasing
assert reading_list["hdbscan"].isin(groups_read).all()
assert len(week2) == N and {"title", "has_pattern", "read_group", "text_says_read", "prob_texto"} <= set(week2.columns)
print(f"Paso 6.3: OK. prob_texto de {reading_list['prob_texto'].max()} a {reading_list['prob_texto'].min()}. Armen el ZIP.")
```

---

## Registro de contribución

En este paso cada integrante anota su tarea concreta, quién repartió las etiquetas y quién consolida el ZIP.

**ESCRIBA SU TEXTO AQUÍ**

## Entrega

El ZIP se entrega el martes 24 nov 2026, 23:59 (hora de Colombia), con el cuaderno ejecutado y renombrado.

| Archivo del ZIP `week-2-<group_id>.zip` | Descripción |
|-----------------------------------------|-------------|
| `week-2-group-<group_id>.ipynb` | Este cuaderno ejecutado, con la nota de la pregunta y la interpretación escritos |
| `etiquetas.csv` | Su conjunto etiquetado, con `etiqueta` en 1 o 0 |
| `outputs/grupos.csv` | Los grupos de HDBSCAN y si cada grupo se lee |
| `outputs/texto.csv` | Las predicciones de TF-IDF, `prob_texto` y la etiqueta |
| `outputs/lectura_semana_2.csv` | Hasta 30 artículos de los grupos leídos, en el orden de TF-IDF |
| `outputs/en_vista.csv` | Una fila por artículo, con las columnas que lee el proyecto |

`outputs/lectura_semana_2.csv` es la lista de esta semana.
No es la lista de inicio.
El cuaderno del proyecto lee `outputs/en_vista.csv`.

<!-- end NOTEBOOK: -->
