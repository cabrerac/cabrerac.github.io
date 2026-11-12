<!-- NOTEBOOK: -->

## Instrucciones

**Propósito.** Cuaderno de grupo de la semana 1 (Lecciones 1 y 2). Su grupo es un equipo interno de una alcaldía y trabaja para una secretaría. El producto del proyecto es una lista de artículos para los nuevos integrantes del equipo.

**Esta semana.** El grupo escribe la pregunta y el problema, y repite en sus artículos lo que ya hicieron las Lecciones 1 y 2. El resultado de los pares es `outputs/patrones.csv`. El resultado de la lista de esta semana es `outputs/lectura.csv`.

**Antes de empezar.** Ejecuten primero los cuadernos individuales de las Lecciones 1 y 2. Este cuaderno lo escribe el grupo. Repitan ese trabajo con el archivo de su secretaría.

**Datos de entrada.** El archivo de su secretaría: G1 Agricultura, G2 Salud mental, G3 Medio ambiente, G4 Inclusión Social y G5 Vivienda. Cada fila es un artículo de Wikipedia en español. El texto para los patrones es la columna `lead`, la **descripción** del artículo.

**Materiales.** [L1 Introducción](https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-data-mining/l1-introduction.ipynb) y [L2 Patrones](https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-data-mining/l2-patterns.ipynb).

**Pregunta del grupo.** ¿Qué artículos de su secretaría debe leer primero una persona nueva en el equipo? Comparen los pares de las descripciones con soporte, lift y cercanía.

**Mapa del cuaderno**

| Ejercicio | Tema | Entregable clave |
|-----------|------|------------------|
| **0** | Configuración | Grupo, datos, parámetros y modelo de vectores en español |
| **1** | Comprensión del negocio | La pregunta y el problema, en texto |
| **2** | Comprensión de los datos | Forma, faltantes, largo, duplicados y perfil |
| **3** | Preparación de los datos | Palabras útiles, conjuntos, conteos, pares y vectores |
| **4** | Modelado | Soporte, lift y coseno |
| **5** | Evaluación | Pares conservados, comparación de los tres métodos y `outputs/patrones.csv` |
| **6** | Despliegue | `outputs/lectura.csv`, hasta 30 artículos |

---

## Ejercicio 0. Configuración

### Paso 0.1. Grupo y datos

En este paso eligen el grupo y descargan el archivo de su secretaría, como la descarga de la Lección 1.

Cambien la variable `GROUP` para descargar el archivo asignado.

```python
from pathlib import Path

import pandas as pd
import requests

GROUP = "G1"   # cambie a G2, G3, G4 o G5
EXTRACTS = {"G1": ("Agricultura", "agricultura.csv"), "G2": ("Salud mental", "salud-mental.csv"), "G3": ("Medio ambiente", "medio-ambiente.csv"),
            "G4": ("Inclusión Social", "inclusion-social.csv"), "G5": ("Vivienda", "vivienda.csv")}
SECRETARIAT, FILENAME = EXTRACTS[GROUP]
DATA_DIR = Path("data")  # aquí queda el CSV
OUTPUTS_DIR = Path("outputs")  # aquí quedan las tablas y las figuras
DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
path = DATA_DIR / FILENAME
if not path.is_file():  # usa el archivo si ya está
    path.write_bytes(requests.get(f"https://cabrerac.github.io/assets/data/26-udenar-data-mining/{FILENAME}", timeout=60).content)
articles = pd.read_csv(path)  # una fila por artículo
print(f"Grupo {GROUP}: secretaría de {SECRETARIAT}, {len(articles)} artículos")
```

### Paso 0.2. Parámetros y modelo de vectores

En este paso definen los mismos números de la Lección 2 y cargan el modelo de español `es_core_news_lg`.

```python
# SU CÓDIGO. Paso 0.2: los mismos parámetros de la Lección 2, support_floor, load_vector_model y nlp, MODEL en español

```

**Listo cuando:**
- Los parámetros tienen los valores de la Lección 2.
- `nlp` y `MODEL` cargan un modelo de español: `MODELS = ["es_core_news_lg", "es_core_news_md"]`.

**Comprobar:**

En este paso comprobamos que `support_floor` existe y que cargó un modelo de español.

```python
assert callable(support_floor) and MODEL.startswith("es_core_news")
print("Paso 0.2: OK")
```

---

## Ejercicio 1. Comprensión del negocio

### Paso 1.1. La pregunta y el problema

En este paso escriben la pregunta y el problema de su secretaría, como la tabla de la Lección 1.
La pregunta dice quién usa la lista y qué decide esa lista.
El problema dice el alcance: qué queda dentro y qué queda fuera.
La lista es aceptable cuando tiene entre 10 y 30 artículos.
Ese texto alimenta las secciones 2 y 3 del documento de requerimientos del proyecto.

**La pregunta**

**ESCRIBA SU TEXTO AQUÍ**

**El problema**

**ESCRIBA SU TEXTO AQUÍ**

---

## Ejercicio 2. Comprensión de los datos

### Paso 2.1. Forma y columnas

En este paso miran la forma de la tabla y sus columnas, como la exploración de la Lección 1.
La descripción que van a partir en palabras es la columna `lead`.

```python
# SU CÓDIGO. Paso 2.1: articles.shape, articles.dtypes y articles.head(3)

```

**Comprobar:**

En este paso comprobamos que están el título y la descripción.

```python
assert {"title", "lead"} <= set(articles.columns)
print("Paso 2.1: OK")
```

### Paso 2.2. Valores faltantes

En este paso cuentan las celdas vacías de cada columna, como en la Lección 1.

```python
# SU CÓDIGO. Paso 2.2: missing = articles.isna().sum()

```

**Comprobar:**

En este paso comprobamos que el conteo de vacíos tiene una entrada por columna.

```python
assert len(missing) == articles.shape[1]
print("Paso 2.2: OK")
```

### Paso 2.3. Largo de las descripciones

En este paso cuentan las palabras de cada descripción y dibujan el histograma, como el largo de los resúmenes en la Lección 1.
Guarden la figura en `outputs/histograma_descripcion.png`.

```python
# SU CÓDIGO. Paso 2.3: articles["lead_words"] y el histograma

```

**Comprobar:**

En este paso comprobamos que cada artículo tiene un largo y que la figura quedó guardada.

```python
assert "lead_words" in articles and (OUTPUTS_DIR / "histograma_descripcion.png").is_file()
print("Paso 2.3: OK")
```

### Paso 2.4. Duplicados

En este paso revisan títulos repetidos y descripciones repetidas, como en la Lección 1.
Anótenlos.
No borren filas.

```python
# SU CÓDIGO. Paso 2.4: duplicate_titles y duplicate_leads

```

**Comprobar:**

En este paso comprobamos que los dos conteos son números.

```python
assert duplicate_titles >= 0 and duplicate_leads >= 0
print("Paso 2.4: OK")
```

### Paso 2.5. Tabla de perfil

En este paso arman el perfil, una fila por columna, como en la Lección 1.

```python
# SU CÓDIGO. Paso 2.5: profile

```

**Comprobar:**

En este paso comprobamos que hay una fila de perfil por columna.

```python
assert len(profile) == articles.shape[1]
print("Paso 2.5: OK")
```

---

## Ejercicio 3. Preparación de los datos

### Paso 3.1. Una descripción, tres vistas

En este paso toman una descripción y la ven como lista, como conjunto y como conteo, como en la Lección 1.

```python
# SU CÓDIGO. Paso 3.1: text_words, word_set y word_counts de una descripción

```

**Comprobar:**

En este paso comprobamos que el conjunto no tiene más palabras que la lista.

```python
assert len(word_set) <= len(text_words)
print("Paso 3.1: OK")
```

### Paso 3.2. Palabras útiles

En este paso convierten cada descripción en un conjunto de palabras útiles, como en la Lección 2.
Pasan a minúsculas, quitan el residuo "[cita requerida]", dejan las palabras de solo letras, y descartan las de menos de 3 letras y las palabras vacías del español.
También quitan los pedazos de direcciones web (`http`, `https`, `www`, `org`).

```python
# SU CÓDIGO. Paso 3.2: words, URL_TOKENS y STOP_WORDS

```

**Listo cuando:**
- `STOP_WORDS` son las del español (`spacy.lang.es.stop_words`) más `URL_TOKENS`.
- `words` quita el residuo "[cita requerida]".

**Comprobar:**

En este paso comprobamos que `words` devuelve un conjunto y que un pedazo de dirección no pasa.

```python
assert isinstance(words("Texto de prueba", STOP_WORDS), set)
assert "http" not in words("vea https://www.example.org", STOP_WORDS)
print("Paso 3.2: OK")
```

### Paso 3.3. Conjuntos, conteos y pares

En este paso arman un conjunto de palabras por descripción, el conteo de cada palabra y los pares candidatos, como en la Lección 2.
Dejan fuera las descripciones con menos de 5 palabras útiles.
Una palabra y un par entran si llegan al piso de `support_floor(N)`.

```python
# SU CÓDIGO. Paso 3.3: word_sets, N, FLOOR, word_count, vocabulary y candidates

```

**Comprobar:**

En este paso comprobamos que hay un conjunto por descripción usada y que todos los pares llegan al piso.

```python
assert len(word_sets) == N and min(candidates.values()) >= FLOOR == support_floor(N)
print(f"Paso 3.3: OK ({len(candidates)} pares)")
```

### Paso 3.4. Palabras que el modelo conoce

En este paso cruzan el vocabulario con el modelo, como en la Lección 2.
La cercanía no lee una palabra sin vector.
Las palabras que comparten el mismo vector quedan en `group_of`.

```python
# SU CÓDIGO. Paso 3.4: no_vector, shared_groups y group_of

```

**Comprobar:**

En este paso comprobamos que existen `no_vector` y `group_of`.

```python
assert isinstance(no_vector, list) and isinstance(group_of, dict)
print("Paso 3.4: OK")
```

---

## Ejercicio 4. Modelado

### Paso 4.1. Soporte y lift

En este paso arman la tabla de pares con el soporte y el lift, como en la Lección 2.
El soporte es el número de descripciones donde aparecen las dos palabras.
El lift es cuántas veces ese número supera lo esperado si las dos palabras no tuvieran que ver.

```python
# SU CÓDIGO. Paso 4.1: table con word_a, word_b, support, pair y lift

```

**Comprobar:**

En este paso comprobamos que la tabla tiene sus columnas y una fila por par candidato.

```python
assert {"word_a", "word_b", "support", "pair", "lift"} <= set(table.columns) and len(table) == len(candidates)
print("Paso 4.1: OK")
```

### Paso 4.2. Coseno y vecinos

En este paso miden el coseno de cada par y los vecinos de una palabra de su secretaría, como en la Lección 2.
Un par que comparte el mismo vector queda marcado y no cuenta como cercanía.

```python
# SU CÓDIGO. Paso 4.2: columnas cosine y shared_vector, SEED_WORD y neighbours

```

**Listo cuando:**
- `SEED_WORD` es una palabra de su secretaría que el modelo conoce.

**Comprobar:**

En este paso comprobamos las columnas `shared_vector` y `cosine`.

```python
assert table["shared_vector"].dtype == bool and table["cosine"].dropna().between(-1.001, 1.001).all()
print("Paso 4.2: OK")
```

---

## Ejercicio 5. Evaluación

### Paso 5.1. Los pares que se conservan

En este paso repiten la evaluación de la Lección 2.
En las descripciones reales, un par aparece en `n` de ellas.
Armen 100 copias de la colección.
En cada copia intercambien palabras entre artículos.
Cada artículo conserva su largo y cada palabra conserva su conteo.
En la copia 1 el par aparece en `m1` descripciones, en la copia 2 en `m2`, y así hasta `m100`.
El percentil 95 es el conteo que deja a 95 de esas 100 copias en ese valor o por debajo.
El par se conserva solo si `n` es mayor que ese conteo.
`kept_lift2` marca los conservados que además aparecen al menos el doble de lo esperado.
Muestren los conservados de mayor lift y los conservados con soporte de 20 o más.
Impriman cuántos pares pasarían ese corte por suerte.

```python
# SU CÓDIGO. Paso 5.1: transactions, null, null_p95, kept y kept_lift2

```

**Comprobar:**

En este paso comprobamos que cada par tiene sus 100 conteos y que un par conservado supera su percentil 95.

```python
assert len(null) == len(candidates) and "null_p95" in table and table["kept"].dtype == bool
assert table.loc[table["kept"], "support"].gt(table.loc[table["kept"], "null_p95"]).all()
assert not (table["kept_lift2"] & ~table["kept"]).any()
print("Paso 5.1: OK")
```

### Paso 5.2. Dónde coinciden los tres métodos

En este paso comparan el soporte, el lift y la cercanía sobre las mismas descripciones, como en la Lección 2.
El corte del coseno es el percentil 95 de 1.000 pares de palabras elegidos al azar.
Armen la tabla de los 10 pares con más soporte, los 10 con más lift y los 10 con más coseno.
Elijan tres pares de su tabla y dibujen la misma figura de tres paneles: artículos, lift y coseno.
Un par que los tres métodos conservan es un candidato más fuerte.
Un par que solo un método conserva no es el ganador.

```python
# SU CÓDIGO. Paso 5.2: beats_cosine, RANDOM_COSINE_P95, comparison y la figura

```

**Comprobar:**

En este paso comprobamos la columna `beats_cosine` y que la comparación tiene tres columnas.

```python
assert table["beats_cosine"].dtype == bool and comparison.shape == (10, 3)
assert -1 <= RANDOM_COSINE_P95 <= 1
print("Paso 5.2: OK")
```

### Paso 5.3. Guardar los patrones

En este paso guardan `outputs/patrones.csv`, una fila por par candidato, como en la Lección 2.

```python
# SU CÓDIGO. Paso 5.3: outputs/patrones.csv

```

**Listo cuando:**
- El archivo tiene `pair`, `support`, `null_p95`, `lift`, `cosine`, `kept`, `kept_lift2`, `beats_cosine` y `shared_vector`.

**Comprobar:**

En este paso comprobamos las columnas del archivo.

```python
saved = pd.read_csv(OUTPUTS_DIR / "patrones.csv")
assert {"pair", "support", "null_p95", "lift", "cosine", "kept", "kept_lift2", "beats_cosine", "shared_vector"} <= set(saved.columns)
print("Paso 5.3: OK")
```

---

## Ejercicio 6. Despliegue

### Paso 6.1. Artículos para leer

En este paso arman la lista de lectura de esta semana, como en la Lección 2.
Un par suma un punto si el soporte lo conserva, un punto si el lift también lo conserva, y un punto si la cercanía lo conserva.
La evidencia del artículo es la suma de esos puntos.
Ordenen de mayor a menor evidencia.
Guarden como máximo 30 artículos en `outputs/lectura.csv`, con las columnas `title`, `soporte`, `lift`, `cercania` y `evidencia`.
Esta lista usa solo los pares de hoy.
Las semanas siguientes agregan otras evidencias.
No es la lista de inicio del proyecto.

```python
# SU CÓDIGO. Paso 6.1: reading y outputs/lectura.csv

```

**Comprobar:**

En este paso comprobamos que la lista tiene como máximo 30 artículos y que la evidencia es la suma de los tres métodos.

```python
reading_list = pd.read_csv(OUTPUTS_DIR / "lectura.csv")
assert len(reading_list) == min(30, len(reading))
assert reading_list["evidencia"].min() > 0
three = reading_list["soporte"] + reading_list["lift"] + reading_list["cercania"]
assert (reading_list["evidencia"] == three).all()
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
| `week-1-group-<group_id>.ipynb` | Este cuaderno ejecutado, con la pregunta y el problema escritos en el Paso 1.1 |
| `outputs/patrones.csv` | Una fila por par candidato, con las columnas de la Lección 2 |
| `outputs/lectura.csv` | Hasta 30 artículos, ordenados por la evidencia de los tres métodos |

La pregunta y el problema quedan en el cuaderno.
`outputs/patrones.csv` es el resultado de los pares de esta semana.
`outputs/lectura.csv` es la lista de esta semana.
No es la lista de inicio.
El cuaderno del proyecto lee `outputs/patrones.csv` cuando arma la lista de inicio.
No vuelve a calcular los pares.

<!-- end NOTEBOOK: -->
