<!-- NOTEBOOK: -->

## Instrucciones

**Propósito.** Cuaderno de grupo de la semana 3 (Lecciones 5 y 6). Su grupo sigue como equipo interno de una alcaldía, con los artículos de su secretaría. El producto del proyecto es una lista de artículos para los nuevos integrantes del equipo.

**Esta semana.** El grupo repite en sus artículos lo que hicieron las Lecciones 5 y 6, con el método de grafos y el método de predicción que mejor se ajustan a estos datos: PageRank y un bosque aleatorio.
PageRank, porque los enlaces son menciones con dirección y PageRank da un puntaje a cada artículo, también a los aislados. node2vec deja sin vector entre el 17% y el 31% de los artículos de cada secretaría, y sus vecinos cambian con la semilla.
El bosque aleatorio, porque en las cinco particiones de la Lección 6 no se hunde como la regresión logística (0,328 contra 0,836 de la clase mayoritaria en Medio ambiente) y sus importancias dicen qué atributos usa.
El grado se queda solo para la alerta de nodo central.
Los resultados son `outputs/grafo.csv` y `outputs/prediccion.csv`. El cuaderno del proyecto los lee cuando arma la lista de inicio.

**Antes de empezar.** Ejecuten primero los cuadernos individuales de las Lecciones 5 y 6. Este cuaderno lo escribe el grupo. Traigan de los laboratorios los parámetros y las funciones.

**Datos de entrada.** El archivo de su secretaría: G1 Agricultura, G2 Salud mental, G3 Medio ambiente, G4 Inclusión Social y G5 Vivienda. La columna `links` trae los enlaces de la descripción a otros artículos del mismo archivo. Un enlace es una mención en el texto, no una cita. Las categorías las pusieron quienes editan Wikipedia.

**Materiales.** [L5 Grafos](https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-data-mining/l5-graphs.ipynb) y [L6 Predicción](https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-data-mining/l6-prediction.ipynb).

**Las decisiones son del grupo.** El grupo puede cambiar la pregunta o el alcance. Escriban la razón en el paso donde lo cambia.

**Pregunta del grupo.** ¿Qué lugar ocupa un artículo entre los demás, y la predicción del bosque aleatorio supera a la clase mayoritaria en su secretaría?

**Mapa del cuaderno**

| Ejercicio | Tema | Entregable clave |
|-----------|------|------------------|
| **0** | Configuración | Grupo, etiqueta, datos, parámetros y funciones |
| **1** | Comprensión del negocio | La nota de si la pregunta cambió, y qué esperan del grafo |
| **2** | Comprensión de los datos | Títulos únicos, enlaces y la etiqueta |
| **3** | Preparación de los datos | Los enlaces, el grafo con dirección, el conjunto apartado y la preparación |
| **4** | Modelado | Grado para la alerta, PageRank y el bosque aleatorio |
| **5** | Evaluación | Un artículo por su lugar, aciertos y errores, si la predicción cuenta, `outputs/grafo.csv` y `outputs/prediccion.csv` |
| **6** | Despliegue | Los artículos para leer (hasta 30), si texto y predicción son uno o dos apoyos, las tres semanas, la separación de clases y la fuga |

---

## Ejercicio 0. Configuración

### Paso 0.1. Grupo, etiqueta y datos

En este paso eligen el grupo y descargan el archivo de su secretaría.
Cambien solo `GROUP`.
La etiqueta de la Lección 6 es `LABEL = "categoria_objetivo"`.
Vale 1 si la categoría del artículo (`categoria`) está en `TARGETS[GROUP]`, y 0 si no.

```python
from pathlib import Path  # Path arma las rutas de las carpetas

import pandas as pd  # pandas lee y guarda las tablas
import requests  # requests descarga el archivo de la secretaría

GROUP = "G1"  # cambie a G2, G3, G4 o G5
LABEL = "categoria_objetivo"  # 1 si categoria está en TARGETS[GROUP], 0 si no
TARGETS = {  # las categorías de la etiqueta de cada secretaría
    "G1": ["Agrarismo", "Organizaciones agrícolas"],  # Agricultura
    "G2": ["Trastornos mentales", "Psiquiatría"],  # Salud mental
    "G3": ["Conservacionismo"],  # Medio ambiente
    "G4": ["Hambrunas", "Hambre", "Bancos de alimentos"],  # Inclusión Social
    "G5": ["Hipotecas", "Arrendamiento", "Huelgas de alquileres", "Vivienda asequible", "Vivienda pública"],  # Vivienda
}
EXTRACTS = {  # el nombre y el archivo de cada secretaría
    "G1": ("Agricultura", "agricultura.csv"),  # G1
    "G2": ("Salud mental", "salud-mental.csv"),  # G2
    "G3": ("Medio ambiente", "medio-ambiente.csv"),  # G3
    "G4": ("Inclusión Social", "inclusion-social.csv"),  # G4
    "G5": ("Vivienda", "vivienda.csv"),  # G5
}
SECRETARIAT, FILENAME = EXTRACTS[GROUP]  # tomamos la secretaría y el archivo del grupo
DATA_DIR = Path("data")  # aquí queda el CSV
OUTPUTS_DIR = Path("outputs")  # aquí quedan grafo.csv y prediccion.csv
DATA_DIR.mkdir(parents=True, exist_ok=True)  # mkdir crea la carpeta de datos si no existe
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)  # mkdir crea la carpeta de salidas si no existe
path = DATA_DIR / FILENAME  # la ruta local del archivo
if not path.is_file():  # usa el archivo si ya está
    path.write_bytes(requests.get(f"https://cabrerac.github.io/assets/data/26-udenar-data-mining/{FILENAME}", timeout=60).content)  # requests.get descarga el archivo y write_bytes lo guarda
df = pd.read_csv(path, keep_default_na=False).drop_duplicates("title").reset_index(drop=True)  # read_csv lee los artículos y drop_duplicates deja una fila por título
df = df.rename(columns={"label": "categoria"})  # en el extracto la columna se llama label
print(f"Grupo {GROUP}: secretaría de {SECRETARIAT}, {len(df)} artículos sin títulos repetidos. Etiqueta: {LABEL}")  # print muestra el grupo y el tamaño
```

### Paso 0.2. Importaciones, parámetros y funciones de apoyo

En este paso preparan lo que usa el resto del cuaderno. Va en tres celdas.
Primero las importaciones de las Lecciones 5 y 6 que usa este cuaderno: `math`, `networkx`, `numpy` y las de scikit-learn.

```python
# SU CÓDIGO. Paso 0.2a: las importaciones de las Lecciones 5 y 6
```

Después los parámetros de las Lecciones 5 y 6, con los valores de los laboratorios.
Este cuaderno no usa los parámetros de node2vec, de la regresión ni de la red.

```python
# SU CÓDIGO. Paso 0.2b: los parámetros de las Lecciones 5 y 6, MAX_PAPERS y folds
```

Al final las funciones de tamaño: `support_floor`, `hub_threshold` y `n_flagged`.

```python
# SU CÓDIGO. Paso 0.2c: support_floor, hub_threshold y n_flagged
```

**Listo cuando:**
- Los parámetros tienen los valores de los laboratorios: `SEED`, `HUB_SHARE`, `MIN_LINKS`, `DAMPING`, `N_TREES`, `MARGIN`, `SPLIT_SEEDS`, `N_FOLDS` y los de las filas apartadas. También `MAX_PAPERS = 30`.
- `folds` es la validación cruzada en cinco pliegues de la Lección 6, con `SEED`.

**Comprobar:**

Comprobamos algunos valores de los laboratorios y las tres funciones con unos tamaños conocidos.

```python
assert callable(RandomForestClassifier) and callable(nx.pagerank) and folds.get_n_splits() == N_FOLDS  # las importaciones y los pliegues están
assert (DAMPING, N_TREES, MARGIN, SPLIT_SEEDS, MAX_PAPERS) == (0.85, 200, 0.02, (7, 8, 9, 10, 11), 30)  # algunos valores de los laboratorios
assert support_floor(300) == 9 and hub_threshold(318) == 32 and n_flagged(300) == 60  # las funciones dan los tamaños de las lecciones
print("Paso 0.2: OK")  # print confirma la comprobación
```

---

## Ejercicio 1. Comprensión del negocio

### Paso 1.1. ¿Cambió la pregunta?

La pregunta y el problema están en el documento de requerimientos.
En este paso escriben solo si algo cambió.
Si la pregunta o el alcance siguen iguales, escriban "Sin cambio".
Si cambiaron, escriban la línea nueva y por qué.

**Cambio**

**ESCRIBA SU TEXTO AQUÍ**

### Paso 1.2. Qué esperan del grafo

En este paso escriben qué esperan del grafo, antes de mirar resultados.
¿Qué artículo creen que será el más enlazado?
¿Una persona nueva debería abrirlo primero? ¿Por qué?

**Lo que esperamos**

**ESCRIBA SU TEXTO AQUÍ**

---

## Ejercicio 2. Comprensión de los datos

### Paso 2.1. Títulos y enlaces

En este paso revisan los títulos y cómo vienen los enlaces, como en la Lección 5, Parte 2.
Aquí `df` ya viene sin títulos repetidos.
`listed` guarda, por artículo, la lista de títulos que nombra en `links`.

```python
# SU CÓDIGO. Paso 2.1: titles, N y listed
```

**Comprobar:**

Comprobamos que hay un título y una lista de enlaces por artículo.

```python
assert len(titles) == N == len(listed) == len(df)  # un título y una lista por artículo
print("Paso 2.1: OK")  # print confirma la comprobación
```

### Paso 2.2. La etiqueta y los atributos

En este paso arman la tabla de atributos y la etiqueta, como en la Lección 6, Parte 3.
`attributes` usa el título como índice.
Lleva `kind`, `year`, `has_date`, `has_country`, `has_image` y `n_claims_without`.
`kind` deja como `Other` los tipos con menos de `support_floor(N)` artículos.
`y` vale 1 si `categoria` está en `TARGETS[GROUP]`, y 0 si no.
Impriman cuántos artículos tienen 1 y cuántos tienen 0.

```python
# SU CÓDIGO. Paso 2.2: attributes y y
```

**Comprobar:**

Comprobamos que hay una etiqueta por artículo y que solo vale 0 o 1.

```python
assert len(y) == N and set(y.unique()) <= {0, 1}  # una etiqueta por artículo, con 0 o 1
assert list(y.index) == list(attributes.index)  # la etiqueta va en el mismo orden que los atributos
print(f"Paso 2.2: OK. Etiqueta en 1: {int(y.sum())} de {N}")  # print confirma la comprobación
```

---

## Ejercicio 3. Preparación de los datos

### Paso 3.1. Los enlaces y el grafo con dirección

En este paso arman los enlaces dentro del extracto, como en la Lección 5, Parte 3.
`links_out` va con dirección y `neighbours` sin dirección.
`directed` es el grafo con dirección que usa PageRank.

```python
# SU CÓDIGO. Paso 3.1: links_out, neighbours y directed
```

**Comprobar:**

Comprobamos que el grafo tiene un nodo por artículo y que ningún artículo se enlaza a sí mismo.

```python
assert directed.number_of_nodes() == N == len(neighbours)  # un nodo por artículo
assert nx.number_of_selfloops(directed) == 0  # nadie se enlaza a sí mismo
print(f"Paso 3.1: OK. Enlaces con dirección: {directed.number_of_edges()}")  # print confirma la comprobación
```

### Paso 3.2. El conjunto apartado

En este paso apartan `n_flagged(N)` filas con `SEED`, con la misma proporción de cada clase, como en la Lección 6.
Ningún modelo las ve al aprender.

```python
# SU CÓDIGO. Paso 3.2: train, test, y_train y y_test
```

**Comprobar:**

Comprobamos el tamaño del conjunto apartado y que no comparte filas con el entrenamiento.

```python
assert len(test) == n_flagged(N) and len(train) + len(test) == N  # tamaño correcto
assert not set(train.index) & set(test.index)  # sin filas compartidas
print("Paso 3.2: OK")  # print confirma la comprobación
```

### Paso 3.3. La preparación

En este paso arman `prepare`, el `ColumnTransformer` de la Lección 6.
En los números usen `add_indicator=False`, porque `has_date` ya marca el año faltante.

```python
# SU CÓDIGO. Paso 3.3: NUMBER_COLUMNS, CATEGORY_COLUMNS y prepare
```

**Comprobar:**

Comprobamos que la preparación usa las columnas de la tabla.

```python
assert set(NUMBER_COLUMNS + CATEGORY_COLUMNS) <= set(attributes.columns) and "kind" in CATEGORY_COLUMNS  # las columnas existen
print("Paso 3.3: OK")  # print confirma la comprobación
```

---

## Ejercicio 4. Modelado

### Paso 4.1. Grado y alerta de nodo central

En este paso cuentan el grado de cada artículo, como en la Lección 5, M1.
El grado solo sirve aquí para la alerta.
Un nodo central (`hubs`) es una alerta, no una razón para leerlo.
Impriman los 5 artículos de más grado.

```python
# SU CÓDIGO. Paso 4.1: degree y hubs
```

**Comprobar:**

Comprobamos que hay un grado por artículo y que la alerta sigue su regla.

```python
assert len(degree) == N  # un grado por artículo
for v in hubs:  # recorremos cada nodo central
    assert degree[v] >= hub_threshold(N), v  # cada uno llega al umbral de la alerta
print(f"Paso 4.1: OK. Nodos centrales: {len(hubs)}")  # print confirma la comprobación
```

### Paso 4.2. PageRank

En este paso calculan PageRank con `nx.pagerank(directed, alpha=DAMPING)` y marcan los artículos con PageRank alto, como en la Lección 5, M2.
Usamos PageRank porque un enlace aquí es una mención con dirección: un artículo sube si lo mencionan artículos que también son mencionados (Page et al., 1998).
PageRank da un puntaje a todos los artículos.
node2vec solo da un vector a los del componente mayor, y sus vecinos cambian con la semilla.
Un artículo con PageRank alto tiene enlaces, está en el cuarto superior por PageRank entre los artículos con enlaces y **no** es nodo central.
Redondeen PageRank a 6 decimales antes del corte.

```python
# SU CÓDIGO. Paso 4.2: rank y high_rank
```

**Comprobar:**

Comprobamos que PageRank suma 1, que hay artículos con PageRank alto y que ninguno es nodo central.

```python
assert abs(sum(rank.values()) - 1) < 1e-6 and len(rank) == N  # un puntaje por artículo, que suman 1
assert len(high_rank) >= 1 and not set(high_rank) & set(hubs)  # hay PageRank alto y ningún nodo central
print(f"Paso 4.2: OK. Con PageRank alto: {len(high_rank)}")  # print confirma la comprobación
```

### Paso 4.3. El bosque aleatorio

En este paso entrenan el bosque aleatorio de la Lección 6, M2, con la preparación adelante: `make_pipeline(prepare, RandomForestClassifier(...))`.
Usamos el bosque porque, con estas etiquetas, no se hunde bajo la clase mayoritaria como la regresión logística, y dice qué atributos usa.
`test_prediction` es lo que dice el bosque en las filas apartadas.
`train_prediction` es lo que dice en las filas de entrenamiento, con cinco pliegues (`cross_val_predict` y `folds`), así un modelo que no vio la fila la predice.

```python
# SU CÓDIGO. Paso 4.3: forest, test_prediction y train_prediction
```

**Comprobar:**

Comprobamos que hay una predicción por fila apartada y por fila de entrenamiento.

```python
assert len(test_prediction) == len(test) and len(train_prediction) == len(train)  # una predicción por fila
print("Paso 4.3: OK")  # print confirma la comprobación
```

### Paso 4.4. Qué atributos usa el bosque

En este paso leen las importancias del bosque, como en la Lección 6.
`importance` es una serie con la importancia de cada columna preparada.
Impriman las 5 más altas.

```python
# SU CÓDIGO. Paso 4.4: importance
```

**Comprobar:**

Comprobamos que las importancias suman 1.

```python
assert abs(importance.sum() - 1) < 1e-6  # las importancias del bosque suman 1
print("Paso 4.4: OK")  # print confirma la comprobación
```

¿El atributo más importante tiene sentido para su secretaría?
¿Se parece demasiado a la etiqueta? Escriban por qué.

**ESCRIBA SU TEXTO AQUÍ**

---

## Ejercicio 5. Evaluación

### Paso 5.1. Un artículo descrito por su lugar

En este paso eligen un artículo y lo describen por su lugar en la red, como en la Lección 5, Parte 5.
`MY_ARTICLE` es un título del extracto que no es nodo central.
Impriman su grado, su puesto por PageRank y si tiene PageRank alto.

```python
# SU CÓDIGO. Paso 5.1: MY_ARTICLE
```

**Comprobar:**

Comprobamos que el artículo está en el extracto y no es nodo central.

```python
assert MY_ARTICLE in titles and MY_ARTICLE not in hubs  # un título del extracto que no es alerta
print("Paso 5.1: OK")  # print confirma la comprobación
```

¿Qué dice su lugar en la red?
¿Por qué ser central solo porque enlaza con muchos no es una razón para leerlo?

**ESCRIBA SU TEXTO AQUÍ**

### Paso 5.2. Aciertos y errores en las filas apartadas

En este paso cuentan aciertos y errores del bosque en las filas apartadas, como en la Lección 6, Parte 5.
Sumen la fila de la clase mayoritaria: dar a todos la etiqueta más frecuente.
Es la línea de referencia.
`results` tiene una fila por método, con `TP`, `FP`, `FN`, `TN` y `exactitud`.

```python
# SU CÓDIGO. Paso 5.2: majority y results
```

**Comprobar:**

Comprobamos las dos filas y que los conteos suman las filas apartadas.

```python
assert list(results.index) == ["clase mayoritaria", "bosque aleatorio"]  # las dos filas, en este orden
assert (results[["TP", "FP", "FN", "TN"]].sum(axis=1) == len(test)).all()  # los conteos suman las filas apartadas
print("Paso 5.2: OK")  # print confirma la comprobación
```

### Paso 5.3. ¿Cuenta la predicción?

En este paso deciden si la predicción cuenta, como en la Lección 6, Parte 5, Paso 4.
`l6_counts` es `True` solo si el bosque acierta en las filas apartadas más que la clase mayoritaria, por un margen de `MARGIN` (0,02).
Ese margen es una o dos filas de unas 60.
`seeds_holding` cuenta en cuántas de las 5 particiones de `SPLIT_SEEDS` se sostiene, con `clone`.
Si `l6_counts` es `False`, la predicción no apoya su lista. Es un resultado normal y válido, no un error.

```python
# SU CÓDIGO. Paso 5.3: l6_counts y seeds_holding
```

**Comprobar:**

Comprobamos que `l6_counts` es verdadero o falso y que `seeds_holding` va de 0 a 5.

```python
assert isinstance(l6_counts, bool) and 0 <= seeds_holding <= len(SPLIT_SEEDS)  # tipos y rango correctos
print(f"Paso 5.3: OK. l6_counts = {l6_counts}, se sostiene en {seeds_holding} de {len(SPLIT_SEEDS)}")  # print confirma la comprobación
```

### Paso 5.4. Guardar el grafo y la predicción

En este paso guardan los dos resultados de esta semana.

```python
# SU CÓDIGO. Paso 5.4: outputs/grafo.csv y outputs/prediccion.csv
```

**Listo cuando:**
- `grafo.csv` tiene `title`, `grado`, `pagerank`, `aislado`, `alerta_centro` y `graph_support`. `graph_support` es verdadero si el artículo está en `high_rank`. `alerta_centro` no es un resultado a favor.
- `prediccion.csv` tiene `title`, `etiqueta`, `apartada`, `clase_votada` y `prediction`. `clase_votada` es la clase que votan los árboles del bosque. `prediction` es verdadero si esa clase es 1.

**Comprobar:**

Comprobamos las columnas de los dos archivos y que un nodo central nunca tiene `graph_support`.

```python
grafo, prediccion = pd.read_csv(OUTPUTS_DIR / "grafo.csv"), pd.read_csv(OUTPUTS_DIR / "prediccion.csv")  # read_csv vuelve a leer los dos archivos
assert {"title", "graph_support", "alerta_centro"} <= set(grafo.columns) and {"title", "clase_votada", "prediction"} <= set(prediccion.columns)  # están las columnas
assert not (grafo["graph_support"] & grafo["alerta_centro"]).any()  # un nodo central nunca tiene graph_support
print("Paso 5.4: OK")  # print confirma la comprobación
```

---

## Ejercicio 6. Despliegue

### Paso 6.1. Artículos para leer

En este paso arman la lista de lectura de esta semana con los dos métodos.
PageRank filtra: solo entran los artículos con `graph_support`.
Si la predicción cuenta (`l6_counts`), primero van los que el bosque marca con `prediction`.
Después ordenan por PageRank, de mayor a menor.
Si la predicción no cuenta, ordenan solo por PageRank.
Guarden como máximo 30 artículos en `reading`, con `title`, `pagerank` y `prediction`.
Esta lista es la lectura de los resultados de esta semana. La lista de inicio se escribe en el cuaderno del proyecto.

```python
# SU CÓDIGO. Paso 6.1: reading
```

### Paso 6.2. Interpretación de resultados

¿Por qué se seleccionaron los artículos de la lista resultante esta semana?
Explique la selección de acuerdo con PageRank, la predicción y la pregunta.
¿La predicción supera a la clase mayoritaria?
Si no la supera, escríbalo así y diga qué hecho lo cambiaría.

**Interpretación**

**ESCRIBA SU TEXTO AQUÍ**

**Comprobar:**

Comprobamos el largo de la lista y que todo viene del PageRank alto.

```python
assert len(reading) == min(MAX_PAPERS, len(high_rank))  # la lista no pasa de 30
assert set(reading["title"]) <= set(high_rank)  # todo viene del PageRank alto
print("Paso 6.2: OK. Armen el ZIP.")  # print confirma la comprobación
```

### Paso 6.3. Uno o dos apoyos

El filtro de texto de la semana 2 y la predicción de esta semana salen, en este curso, de categorías de Wikipedia.
Los materiales no dicen si cuentan como un apoyo o como dos.
Decidan y anoten por qué.

**Uno o dos apoyos**

**ESCRIBA SU TEXTO AQUÍ**

### Paso 6.4. Las tres semanas

Comparen los resultados de las semanas 1, 2 y 3.
¿Un método que funcionó en una semana falla en esta? ¿Por qué puede pasar?

**Las tres semanas**

**ESCRIBA SU TEXTO AQUÍ**

### Paso 6.5. Cuando el modelo no separa las clases

Si el bosque no supera a la clase mayoritaria, expliquen por qué no logra separar las clases en su secretaría.
Si sí la supera, expliquen de todos modos qué lo impediría.

**Cuando no separa**

**ESCRIBA SU TEXTO AQUÍ**

### Paso 6.6. Fuga de la etiqueta

¿Cómo comprobaron si algún atributo se cuela la respuesta (una fuga)?
¿Qué hicieron con lo que encontraron?

**Fuga**

**ESCRIBA SU TEXTO AQUÍ**

---

## Registro de contribución

En este paso cada integrante anota su tarea concreta y el grupo dice quién consolida el ZIP.

**ESCRIBA SU TEXTO AQUÍ**

## Para la reflexión individual

Use la [plantilla de la reflexión de la semana 3](https://cabrerac.github.io/assets/documents/26-udenar-data-mining/reflection-week-3-template.docx) y mantenga sus títulos. Extensión: entre 700 y 1000 palabras. Por debajo de 500 palabras el texto queda corto.

| Título | Qué escribir |
|--------|--------------|
| **Metadatos** | Nombre, grupo, semana 3 (L5 + L6) y conteo aproximado de palabras. |
| **Proceso** | Qué hizo el grupo en el cuaderno de la semana 3. Diga y evidencie cuál fue su contribución con un pantallazo de un bloque de código que usted implementó o ayudó a implementar, y explíquelo en detalle. |
| **Decisión** | Describa el lugar de los artículos en la red de enlaces y la predicción de la etiqueta que exploró en esta semana. |
| **Métodos** | Explique cuáles fueron los métodos utilizados en esta semana y cómo se comparan entre ellos. ¿En qué consiste el método node2vec discutido en clase? |
| **Interpretabilidad** | En sus palabras, explique las razones detrás de los artículos de Wikipedia que esta semana quedaron seleccionados por su lugar en la red y por la predicción. |

## Entrega

El ZIP se entrega el martes 1 dic 2026, 23:59 (hora de Colombia), con el cuaderno ejecutado y renombrado.
La reflexión individual se entrega el miércoles 2 dic 2026, 23:59 (hora de Colombia).

| Archivo del ZIP `week-3-<group_id>.zip` | Descripción |
|-----------------------------------------|-------------|
| `week-3-group-<group_id>.ipynb` | Este cuaderno ejecutado, con la nota de la pregunta y la interpretación escritas |
| `outputs/grafo.csv` | El lugar de cada artículo en la red, con `graph_support` y `alerta_centro` |
| `outputs/prediccion.csv` | La clase que vota el bosque y el resultado de la predicción |

Estos archivos son el resultado de esta semana.
El cuaderno del proyecto los lee cuando arma la lista de inicio.

<!-- end NOTEBOOK: -->
