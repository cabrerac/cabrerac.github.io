<!-- NOTEBOOK: -->

## Repaso de Python para este cuaderno

Este cuaderno utiliza los siguientes métodos de Python. Si ya los conoce, ejecute estas celdas rápido. Un modelo aprende con `fit` en unas filas y responde con `predict` en otras que no vio.

### Aprender en unas filas, responder en otras

```python
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

x_toy = np.array([[1], [2], [3], [4], [5], [6], [7], [8]])
y_toy = np.array([0, 0, 0, 0, 1, 1, 1, 1])
x_tr, x_te, y_tr, y_te = train_test_split(x_toy, y_toy, test_size=4, stratify=y_toy, random_state=7)
toy_model = DecisionTreeClassifier(random_state=7).fit(x_tr, y_tr)
said = toy_model.predict(x_te)
assert len(said) == len(y_te)
print(f"Dijo {said.tolist()}, era {y_te.tolist()}. Aciertos: {int((said == y_te).sum())} de {len(y_te)}. Repaso de Python: OK")
```

**Lo que vemos.** El árbol aprendió con cuatro filas y acertó las otras cuatro. Con artículos reales los aciertos bajan, por eso comparamos con una línea base.

---

## Instrucciones

Seguimos con el equipo interno de la secretaría de salud y sus artículos sobre nutrición. El equipo debe decidir **qué artículos tiene que leer** un colega que llega al equipo. Con los cuatro resultados de las Lecciones 2 a 5, 66 artículos quedaron en vista.

Hasta ahora cada resultado salió de los datos mismos. Ahora alguien nos da una etiqueta. Por años, los programas que clasificaban seguían reglas escritas a mano. Después se pasó a aprender la regla desde ejemplos etiquetados (LeCun, Bengio y Hinton, 2015). Hoy sumamos el último resultado: **predecir una etiqueta dada**. La etiqueta es `internacional`: autores de al menos dos países (`n_countries >= 2`).

Medimos aciertos y errores en artículos que ningún modelo vio. Cada modelo se compara con la **clase mayor** y con una regla de una línea, sin modelo.

**Tres métodos, tres preparaciones.**

| Método | Pregunta | Preparación que necesita |
|--------|----------|--------------------------|
| M1. Regresión logística | ¿Qué atributos pesan a favor y en contra? | Números escalados, categorías en columnas de 0 y 1, faltantes llenados |
| M2. Bosque aleatorio | ¿Qué cortes en los atributos separan las clases? | La misma tabla. Escalar no cambia un corte |
| M3. Una capa oculta | ¿Qué combinación de atributos separa las clases? | Todo numérico y escalado, faltantes llenados |

**Qué hacer.** Ejecute las celdas de arriba hacia abajo. Cada paso empieza con **En este paso** y termina con una celda **Comprobar**.

**Mapa del cuaderno**

| Parte | Fase CRISP-DM | Qué sale |
|-------|---------------|----------|
| 1 | Comprensión del negocio | La pregunta de hoy, los parámetros, la función contra la fuga y los cuatro resultados anteriores |
| 2 | Comprensión de los datos | La etiqueta y los atributos |
| 3 | Preparación de los datos | La tabla, el conjunto apartado y la preparación |
| 4 | Modelado | Clase mayor, regresión logística, bosque y una capa oculta |
| 5 | Evaluación | Aciertos y errores, cinco pliegues y la regla de una línea |
| 6 | Despliegue | El resultado de la predicción y la lista inicial |

**Carpetas.** La celda de configuración crea `data/` (datos descargados) y `outputs/` (tablas y gráficos).

---

## Parte 1. Comprensión del negocio

### Paso 1. La pregunta de esta lección
En este paso escribimos qué buscamos hoy. La decisión no cambia: qué artículos debe leer el colega nuevo.

| Pregunta | Respuesta para el laboratorio |
|----------|-------------------------------|
| ¿Qué buscamos? | Predecir si un artículo es internacional a partir de sus atributos |
| ¿Con qué lo medimos? | Regresión logística, un bosque aleatorio y una red con una capa oculta |
| ¿Contra qué los comparamos? | Contra la clase mayor y contra una regla de una línea |
| ¿Cómo entra la predicción en la lista? | Un artículo recibe el resultado si al menos 2 de los 3 métodos dicen que sí, con un modelo que no vio su etiqueta |

Después juntamos los cinco resultados en la lista inicial. La cuenta de 0, 1, 2 y 3 o más resultados ayuda a elegir `MIN_SUPPORTS`.

### Paso 2. Configuración
En este paso importamos las librerías, creamos las carpetas y fijamos los parámetros. No los cambie. La excepción es `MIN_SUPPORTS`, que empieza en 2 y se puede cambiar. Cada grupo fija y justifica este número en su proyecto.

```python
import math          # techo (ceil) para los mínimos
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
from sklearn.base import clone
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import ConfusionMatrixDisplay, accuracy_score, confusion_matrix
from sklearn.model_selection import StratifiedKFold, cross_val_predict, train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# Carpetas de trabajo
DATA_DIR = Path("data")
OUTPUTS_DIR = Path("outputs")
DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
BASE_URL = "https://cabrerac.github.io/assets/data/26-udenar-data-mining"

# Desde L2, sin cambios
SEED = 7

# Desde L4, sin cambios
FLAGGED_SHARE = 0.20        # proporción de filas apartadas
FLAGGED_MIN = 40            # mínimo de filas apartadas
POSITIVE_SHARE = 0.10       # proporción mínima de positivos en la etiqueta
POSITIVES_MIN = 30          # mínimo de positivos
C_REG = 10                  # penalización de la regresión logística (más alto, menos penalización)
N_FOLDS = 5

# Decisión, L3 en adelante
MIN_SUPPORTS = 2             # el código empieza en 2, cámbielo si lo justifica (0 o 1 también valen)

# L6 (no cambiar)
LABEL = "internacional"     # laboratorio: autores de al menos dos países
HIDDEN_UNITS = 8            # igual que la diapositiva de mlp-implementation.md
PENALTY = 1.0               # pocas filas, así que una penalización más fuerte que la de la diapositiva (1e-4)
N_TREES = 200
MARGIN = 0.02               # cuánto sobre la clase mayor debe quedar cada método para que la L6 cuente
SPLIT_SEEDS = (7, 8, 9, 10, 11)   # otras particiones, para ver si el resultado se sostiene


def n_flagged(n: int) -> int:
    """Tamaño del conjunto apartado, con la regla de la L4.

    Qué hace: aparta el 20% de las filas (FLAGGED_SHARE), redondeado hacia arriba, y
    nunca menos de FLAGGED_MIN, para que la exactitud no dependa de dos o tres artículos.

    Entrada:
        n: el número de filas con etiqueta.

    Salida:
        El número entero de filas que se apartan.
    """
    return max(FLAGGED_MIN, math.ceil(FLAGGED_SHARE * n))


def min_positives(n: int) -> int:
    """Cuántas filas necesita la clase menor, con la regla de la L4.

    Qué hace: pide el 10% de las filas (POSITIVE_SHARE), redondeado hacia arriba, y nunca
    menos de POSITIVES_MIN. Con menos, un modelo aprende casi nada de esa clase.

    Entrada:
        n: el número de filas con etiqueta.

    Salida:
        El número entero mínimo de filas de la clase menor.
    """
    return max(POSITIVES_MIN, math.ceil(POSITIVE_SHARE * n))


print(f"Etiqueta: {LABEL} (n_countries >= 2). Una capa oculta de {HIDDEN_UNITS} unidades con penalización {PENALTY}, {N_TREES} árboles")
```

### Paso 3. La fuga de la respuesta
En este paso escribimos la función que quita de `n_claims` la propiedad que define la etiqueta. Los artículos de nutrición no tienen `n_claims`, pero las tablas de Wikidata sí. Si `n_claims` cuenta la etiqueta, el modelo vería la respuesta. Eso es una **fuga**. La probamos con una tabla de juguete.

```python
PROPERTY_COLUMN = {"P18": "has_image"}     # propiedad de Wikidata -> columna de la tabla
LABEL_PROPERTY = {"tiene_imagen": "P18"}  # etiquetas que son una propiedad contada en n_claims


def n_claims_without(table, label):
    """Devuelve n_claims sin la propiedad de Wikidata que define la etiqueta.

    Qué hace: n_claims cuenta las propiedades distintas de cada artículo. Si la etiqueta es
    una de esas propiedades (por ejemplo P18, la imagen), cada fila positiva suma 1 a su
    propio n_claims, y el modelo vería la respuesta. En ese caso restamos la columna de la
    propiedad. Para cualquier otra etiqueta, n_claims queda igual.

    Entrada:
        table: una tabla con n_claims y las columnas de PROPERTY_COLUMN.
        label: el nombre de la etiqueta.

    Salida:
        Una serie de enteros con n_claims sin la propiedad de la etiqueta.
    """
    prop = LABEL_PROPERTY.get(label)
    if prop is None:
        return table["n_claims"].astype(int)
    column = PROPERTY_COLUMN[prop]
    return (table["n_claims"] - table[column]).astype(int)


toy_table = pd.DataFrame({"n_claims": [12, 7, 1, 0], "has_image": [1, 0, 1, 0]})
result = n_claims_without(toy_table, "tiene_imagen")
y = toy_table["has_image"]
print(pd.DataFrame({"n_claims": toy_table["n_claims"], "has_image": y, "sin la imagen": result}))
```

**Lo que vemos.** Las dos filas con imagen pierden una propiedad y las otras quedan igual.

**Comprobar:**

En este paso comprobamos que la función quita la imagen de `n_claims` en las filas con imagen y nada más.

```python
assert (result >= 0).all()
assert (toy_table.loc[toy_table["has_image"] == 1, "n_claims"] >= 1).all()
assert ((toy_table["n_claims"] - result) == y).all()
print("Fuga quitada con una etiqueta que es una propiedad: OK")
```

**Comprobar:**

En este paso comprobamos que con una etiqueta que no es una propiedad, `n_claims` no cambia.

```python
assert (n_claims_without(toy_table, "categoria") == toy_table["n_claims"]).all()
print("Con otra etiqueta, n_claims queda igual: OK")
```

### Paso 4. Descargar los artículos
En este paso descargamos los artículos y quitamos los títulos repetidos, como en la Lección 5.

```python
def download_data(name: str, folder: Path = DATA_DIR) -> Path:
    """Descarga un archivo de datos del curso, una sola vez.

    Qué hace: si el archivo ya está en la carpeta, lo usa. Si no, lo baja de BASE_URL.

    Entrada:
        name: nombre del archivo. folder: carpeta local, DATA_DIR por defecto.

    Salida:
        La ruta local del archivo.
    """
    dest = folder / name
    if dest.is_file() and dest.stat().st_size > 0:
        print(f"Ya en caché: {dest}")
        return dest
    response = requests.get(f"{BASE_URL}/{name}", timeout=60)
    response.raise_for_status()
    dest.write_bytes(response.content)
    print(f"Descargado: {dest}")
    return dest


raw = pd.read_csv(download_data("nutricion-papers.csv"), keep_default_na=False)
papers = raw.drop_duplicates("title").reset_index(drop=True)
N = len(papers)
print(f"{len(raw)} filas, {N} sin títulos repetidos, como en la L5")
```

### Paso 5. La pregunta
La pregunta es la de la Lección 1.
El equipo decide qué artículos de nutrición leer, y qué filtro los puso en la lista.
La lista tiene entre 10 y 30 artículos.

```python
MIN_PAPERS = 10
MAX_PAPERS = 30
print(f"Lista: entre {MIN_PAPERS} y {MAX_PAPERS} artículos")
```

### Paso 6. Los cuatro resultados de las Lecciones 2 a 5
En este paso armamos la tabla de resultados con `outputs/grupos_l3.csv`, `outputs/texto_l4.csv` y `outputs/grafo_l5.csv`, unidos por título. El resultado del grafo se recalcula con la regla de la Lección 5. Si falta algún archivo, el resultado queda en falso. Para tener la cuenta real, suba a `outputs/` los archivos de las Lecciones 3, 4 y 5.

```python
def read_or_empty(path, columns):
    """Lee un CSV de una lección anterior, o una tabla vacía si el archivo no está.

    Qué hace: si falta el archivo, avisa y devuelve una tabla vacía con las columnas
    pedidas, así el resto del cuaderno corre y esos resultados quedan en falso.

    Entrada:
        path: la ruta del CSV. columns: las columnas que esperamos.

    Salida:
        Una tabla de pandas.
    """
    if path.is_file():
        return pd.read_csv(path, keep_default_na=False)
    print(f"Falta {path}. Sus resultados quedan en falso.")
    return pd.DataFrame(columns=columns)


groups_l3 = read_or_empty(OUTPUTS_DIR / "grupos_l3.csv", ["title", "has_pattern", "read_group"])
text_l4 = read_or_empty(OUTPUTS_DIR / "texto_l4.csv", ["title", "tfidf_lr"])
graph_l5 = read_or_empty(OUTPUTS_DIR / "grafo_l5.csv", ["title", "grado", "pagerank", "alerta_centro", "supports"])

week2 = pd.DataFrame({
    "title": groups_l3["title"],
    "has_pattern": groups_l3["has_pattern"].astype(str) == "True",
    "read_group": groups_l3["read_group"].astype(str) == "True",
    "text_says_read": text_l4["tfidf_lr"].astype(str) == "1",
})
titles = list(papers["title"])
table = week2.groupby("title")[["has_pattern", "read_group", "text_says_read"]].any().reindex(titles).fillna(False).astype(bool)
table.index.name = "title"   # table: una fila por artículo, el título es el índice

graph_l5 = graph_l5.set_index("title").reindex(titles)
linked = graph_l5["grado"].fillna(0).astype(int) > 0
rank_l5 = graph_l5["pagerank"].astype(float)
cut = np.sort(rank_l5[linked].to_numpy())[int(0.75 * linked.sum())] if linked.any() else np.inf
table["graph_support"] = linked & (rank_l5 >= cut) & (graph_l5["alerta_centro"].astype(str) != "True")
print(table.sum().to_dict())
```

**Comprobar:**

En este paso comprobamos que la tabla tiene los cuatro resultados y que suman lo mismo que en `grafo_l5.csv`.

```python
SUPPORT_COLUMNS = ["has_pattern", "read_group", "text_says_read", "graph_support"]
assert len(table) == N and set(SUPPORT_COLUMNS) <= set(table.columns)
assert (table[SUPPORT_COLUMNS].astype(int).sum(axis=1) == graph_l5["supports"].fillna(0).astype(int)).all()
print(f"Cuatro resultados, iguales a los de grafo_l5.csv: OK ({(table.astype(int).sum(axis=1) >= MIN_SUPPORTS).sum()} en vista)")
```

**Lo que vemos.** Con cuatro resultados hay 66 artículos en vista, los mismos de la Lección 5.

---

## Parte 2. Comprensión de los datos

### Paso 1. La etiqueta `internacional`
En este paso construimos la etiqueta: `n_countries >= 2`. Un `n_countries = 0` quiere decir que OpenAlex no encontró la afiliación. Esos artículos quedan fuera como faltantes y no reciben el resultado.

```python
papers["n_countries"] = pd.to_numeric(papers["n_countries"], errors="coerce").fillna(0).astype(int)
papers["n_authors"] = pd.to_numeric(papers["n_authors"], errors="coerce")
missing = papers["n_countries"] == 0
print(f"Sin datos de afiliación: {missing.sum()} ({(papers.loc[missing, 'n_authors'] > 0).sum()} de ellos con autores)")
labelled_count = int((~missing).sum())
positives = int((papers.loc[~missing, "n_countries"] >= 2).sum())
print(f"Con etiqueta: {labelled_count}. Internacionales: {positives} ({positives / labelled_count:.0%})")
```

**Comprobar:**

En este paso comprobamos que la clase menor tiene suficientes filas.

```python
assert min(positives, labelled_count - positives) >= min_positives(labelled_count)
print(f"Clase menor con al menos {min_positives(labelled_count)} filas: OK")
```

**Lo que vemos.** Quedan 276 artículos con etiqueta, y 145 (53%) son internacionales. La clase mayor acierta poco más de la mitad.

### Paso 2. Los atributos
En este paso elegimos las entradas: año, número de autores, tipo de revista, acceso abierto y tipo de trabajo. No usamos lo que ya fue un resultado (texto, temas, citas, enlaces) ni `n_countries`, que define la etiqueta.

```python
print("Idioma:", papers["language"].value_counts().to_dict())
print("Tipo de revista:", papers["venue_type"].replace("", "(vacío)").value_counts().to_dict())
print("Tipo de trabajo:", papers["work_type"].value_counts().to_dict())
print(papers[["year", "n_authors"]].apply(pd.to_numeric, errors="coerce").describe().round(1))
```

**Lo que vemos.** `venue_type` casi no varía. `n_authors` va de 0 a 100, y 100 es un tope del archivo. La mediana es 8 autores.

---

## Parte 3. Preparación de los datos

### Paso 1. La tabla con etiqueta
En este paso armamos `labelled`, las filas con etiqueta, con el título como índice, igual que `table`.

```python
NUMBER_COLUMNS = ["year", "n_authors", "is_oa"]
CATEGORY_COLUMNS = ["venue_type", "work_type"]

attributes = papers.set_index("title")
attributes["year"] = pd.to_numeric(attributes["year"], errors="coerce")
attributes["is_oa"] = pd.to_numeric(attributes["is_oa"], errors="coerce")
for c in CATEGORY_COLUMNS:
    attributes[c] = attributes[c].replace("", np.nan)
labelled = attributes.loc[attributes["n_countries"] > 0, NUMBER_COLUMNS + CATEGORY_COLUMNS]
y = (attributes.loc[labelled.index, "n_countries"] >= 2).astype(int)
print(f"{len(labelled)} filas con etiqueta, {y.sum()} internacionales")
```

### Paso 2. El conjunto apartado
En este paso apartamos `n_flagged(n)` filas, con la misma proporción de cada clase. Ningún modelo las ve al aprender.

```python
train, test = train_test_split(labelled, test_size=n_flagged(len(labelled)), stratify=y, random_state=SEED)
y_train, y_test = y.loc[train.index], y.loc[test.index]
print(f"Para aprender: {len(train)}. Apartadas: {len(test)} ({y_test.mean():.0%} internacionales)")
```

**Comprobar:**

En este paso comprobamos el tamaño del conjunto apartado, que no comparte filas y que las dos partes tienen proporciones parecidas.

```python
assert len(test) == n_flagged(len(labelled)) and not set(train.index) & set(test.index)
assert abs(y_train.mean() - y_test.mean()) < 0.05
print("Conjunto apartado: OK")
```

### Paso 3. Escalar, codificar y llenar faltantes
En este paso preparamos la tabla con el código de las diapositivas. Los números se llenan con la mediana y se escalan. Las categorías se llenan con la más común y pasan a columnas de 0 y 1. Todo se aprende **solo con las filas de entrenamiento**.

```python
numbers = make_pipeline(SimpleImputer(strategy="median", add_indicator=True),
                        StandardScaler())
categories = make_pipeline(SimpleImputer(strategy="most_frequent"),
                           OneHotEncoder(handle_unknown="ignore"))
prepare = ColumnTransformer([("num", numbers, NUMBER_COLUMNS),
                             ("cat", categories, CATEGORY_COLUMNS)])

X_train = prepare.fit_transform(train)   # aprende medianas, escalas y categorías
X_test = prepare.transform(test)         # las reutiliza, nunca vuelve a aprender
feature_names = prepare.get_feature_names_out()
print(f"{X_train.shape[1]} columnas preparadas: {list(feature_names)}")
```

**Comprobar:**

En este paso comprobamos la forma de las tablas preparadas y que no quedan faltantes.

```python
assert X_train.shape == (len(train), len(feature_names)) and X_test.shape[1] == len(feature_names)
assert not np.isnan(np.asarray(X_train, dtype=float)).any()
print("Preparación: OK")
```

**Lo que vemos.** Las 5 columnas de entrada se vuelven 12.

---

## Parte 4. Modelado

### La clase mayor
En este paso construimos la línea base: decir siempre la clase más común, aquí internacional.

```python
baseline = DummyClassifier(strategy="most_frequent").fit(X_train, y_train)
pred_majority = baseline.predict(X_test)
majority = max(np.mean(y_test), 1 - np.mean(y_test))
print(f"La clase mayor acierta {accuracy_score(y_test, pred_majority):.2f} de las apartadas")
```

### M1. Regresión logística
En este paso usamos la regresión logística de la Lección 4. Un peso positivo empuja hacia internacional. `class_weight="balanced"` da el mismo peso a las dos clases.

```python
lr = LogisticRegression(class_weight="balanced", C=C_REG,
                        max_iter=1000)
lr.fit(X_train, y_train)
pred_lr = lr.predict(X_test)

weights = pd.Series(lr.coef_[0], index=feature_names)
print(weights.sort_values().round(2))
```

**Lo que vemos.** Pesan más los tipos de trabajo: revisión (1,32) y artículo (0,98) hacia internacional, preprint (-1,13) hacia nacional. `n_authors` pesa 0,44.

### Un corte a mano
En este paso hacemos a mano lo que hace un árbol en cada nodo, con los números de la diapositiva. El árbol prueba cada umbral y se queda con el que deja los lados más puros. Al final `y` vuelve a ser la etiqueta `internacional`.

```python
def gini(labels):
    """Impureza de Gini de una lista de etiquetas.

    Qué hace: da la probabilidad de equivocarse si tomamos una fila al azar y le damos una
    etiqueta sorteada con las proporciones de la lista: 1 menos la suma de las proporciones
    al cuadrado. Vale 0 cuando todas las etiquetas son iguales y 0.5 con dos clases mitad y mitad.

    Entrada:
        labels: una lista de etiquetas.

    Salida:
        Un número entre 0 y 1. Ejemplo: gini([0, 0, 1, 1]) da 0.5 y gini([1, 1, 1]) da 0.0.
    """
    n = len(labels)
    return 1 - sum((labels.count(c) / n) ** 2 for c in set(labels))

def split_score(x, y, threshold):
    """Impureza ponderada de cortar el atributo x en threshold.

    Qué hace: las filas con x <= threshold van a la izquierda y el resto a la derecha. Cada
    lado pesa según su parte de las filas: |L|/|S| G(L) + |R|/|S| G(R). Un valor más bajo es
    un corte mejor. El árbol elige el umbral con el valor más bajo y repite en cada lado.

    Entrada:
        x: los valores de un atributo.
        y: las etiquetas, en el mismo orden.
        threshold: el umbral que se prueba.

    Salida:
        La impureza ponderada de los dos lados, un número entre 0 y 1.
    """
    left = [yi for xi, yi in zip(x, y) if xi <= threshold]
    right = [yi for xi, yi in zip(x, y) if xi > threshold]
    n = len(y)
    return len(left) / n * gini(left) + len(right) / n * gini(right)

x = [1, 2, 3, 4, 5, 6]          # un atributo
y = [0, 0, 0, 1, 1, 1]          # las etiquetas
best = min(sorted(set(x))[:-1], key=lambda t: split_score(x, y, t))   # 3
print(best)
toy_scores = {t: round(split_score(x, y, t), 3) for t in sorted(set(x))[:-1]}
y = (attributes.loc[labelled.index, "n_countries"] >= 2).astype(int)   # y vuelve a ser la etiqueta de la L6
```

**Comprobar:**

En este paso comprobamos el mejor corte de la tabla de ejemplo y su impureza.

```python
assert best == 3, "El mejor umbral de la diapositiva es 3"
assert toy_scores[best] == 0.0 and gini([0, 0, 1, 1]) == 0.5
assert all(score > 0 for t, score in toy_scores.items() if t != best) and y.index.equals(labelled.index)
print("Corte a mano: OK", toy_scores)
```

Con datos reales ningún corte deja los lados puros. Por eso el bosque junta muchos árboles y los deja votar.

### M2. Bosque aleatorio
En este paso entrenamos 200 árboles, cada uno con una muestra al azar de filas y atributos. `min_samples_leaf=3` evita hojas de una fila. La importancia es cuánto baja la impureza de Gini.

```python
forest = RandomForestClassifier(n_estimators=N_TREES, min_samples_leaf=3,
                                random_state=SEED)
forest.fit(X_train, y_train)   # escalar no cambia un corte, así que sirve el mismo X_train
pred_rf = forest.predict(X_test)

importance = pd.Series(forest.feature_importances_, index=feature_names)
print(importance.nlargest(5).round(3))
```

**Lo que vemos.** El bosque usa sobre todo `n_authors` (0,51) y el año (0,37).

### M3. Una capa oculta
En este paso entrenamos una red con una capa oculta de `HIDDEN_UNITS` unidades. `PENALTY` es la penalización L2 (`alpha`), más fuerte que la de la diapositiva porque hay pocas filas.

```python
network = MLPClassifier(hidden_layer_sizes=(HIDDEN_UNITS,), alpha=PENALTY,
                        max_iter=3000, random_state=SEED)
network.fit(X_train, y_train)          # X_train ya viene escalado por prepare
pred_nn = network.predict(X_test)
print(f"La red terminó en {network.n_iter_} pasos")
```

**Lo que vemos.** La red paró en 188 pasos, lejos del máximo de 3000.

**Comprobar:**

En este paso comprobamos que hay una predicción por fila apartada para cada método.

```python
predictions = {"clase mayor": pred_majority, "regresión logística": pred_lr, "bosque": pred_rf, "una capa oculta": pred_nn}
assert all(len(p) == len(y_test) for p in predictions.values())
print("Cuatro predicciones sobre las filas apartadas: OK")
```

---

## Parte 5. Evaluación

### Paso 1. Aciertos y errores en las filas apartadas
En este paso contamos TP, FP, FN y TN de cada método, y su exactitud. Al lado ponemos una regla de una línea: **internacional si tiene al menos 4 autores**. 4 es el umbral que más acierta en las filas de entrenamiento (Paso 6).

```python
def counts_of(y, pred):
    """Aciertos y errores de un método sobre las filas apartadas.

    Qué hace: cuenta la matriz de confusión con internacional (1) como clase positiva y
    calcula la exactitud, la parte de filas bien dichas.

    Entrada:
        y: las etiquetas verdaderas. pred: lo que dijo el método, en el mismo orden.

    Salida:
        Un diccionario con TP, FP, FN, TN y la exactitud a 3 decimales.
    """
    tn, fp, fn, tp = confusion_matrix(y, pred, labels=[0, 1]).ravel()
    return {"TP": tp, "FP": fp, "FN": fn, "TN": tn, "exactitud": round(accuracy_score(y, pred), 3)}

pred_rule = (attributes.loc[test.index, "n_authors"] >= 4).astype(int).to_numpy()
predictions["regla n_authors >= 4"] = pred_rule
results = pd.DataFrame({name: counts_of(y_test, p) for name, p in predictions.items()}).T
results = results.astype({"TP": int, "FP": int, "FN": int, "TN": int})
results
```

**Comprobar:**

En este paso comprobamos que los cuatro casos suman las filas apartadas y que los tres métodos igualan o superan a la clase mayor.

```python
assert (results[["TP", "FP", "FN", "TN"]].sum(axis=1) == len(y_test)).all()
assert all(results.loc[m, "exactitud"] >= majority for m in ["regresión logística", "bosque", "una capa oculta"])
print("Los tres métodos igualan o superan a la clase mayor: OK")
```

**Lo que vemos.** Los tres métodos le ganan a la clase mayor (0,52): regresión 0,61, bosque 0,71 y red 0,63. La regla acierta 0,73, una fila más que el bosque. Eso es menos que `MARGIN`, así que no le gana con claridad.

### Paso 2. Las matrices de confusión
En este paso dibujamos las matrices de confusión y las guardamos en `outputs/`.

```python
for name, pred, file in [("regresión logística", pred_lr, "confusion_regresion.png"), ("bosque", pred_rf, "confusion_bosque.png"), ("una capa oculta", pred_nn, "confusion_red.png")]:
    fig, ax = plt.subplots(figsize=(3.5, 3.2))
    ConfusionMatrixDisplay.from_predictions(y_test, pred, labels=[0, 1], display_labels=["nacional", "internacional"], cmap="Blues", colorbar=False, ax=ax)
    ax.set_title(name)
    fig.tight_layout()
    fig.savefig(OUTPUTS_DIR / file, dpi=120)
    plt.show()
```

**Lo que vemos.** El bosque equilibra mejor los dos errores, con 8 FP y 8 FN.

### Paso 3. Cinco pliegues en las filas de entrenamiento
En este paso repetimos la cuenta con cinco pliegues sobre las 220 filas de entrenamiento, con la preparación dentro de cada modelo.

```python
folds = StratifiedKFold(n_splits=N_FOLDS, shuffle=True, random_state=SEED)
models = [make_pipeline(prepare, m) for m in (lr, forest, network)]
names = ["regresión logística", "bosque", "una capa oculta"]
cv_predictions = [cross_val_predict(m, train, y_train, cv=folds) for m in models]
majority_cv = max(y_train.mean(), 1 - y_train.mean())
for name, p in zip(names, cv_predictions):
    print(f"{name:20s} exactitud en cinco pliegues {accuracy_score(y_train, p):.2f} (clase mayor {majority_cv:.2f})")
rule_train = ((attributes.loc[train.index, "n_authors"] >= 4).astype(int) == y_train).mean()
print(f"{'regla n_authors >= 4':20s} exactitud en las {len(train)} filas de entrenamiento {rule_train:.2f}")
```

**Lo que vemos.** Los tres quedan entre 0,61 y 0,65, contra 0,53 de la clase mayor. La regla acierta 0,69. El bosque baja de 0,71 a 0,62, así que no leemos un solo número.

### Paso 4. ¿Cuenta la predicción?
En este paso decidimos si la predicción suma un resultado. Cuenta (`l6_counts`) solo si los tres métodos quedan más de `MARGIN` (0,02) por encima de la clase mayor en las filas apartadas. Después repetimos con otras cuatro particiones, con copias sin entrenar (`clone`).

```python
majority = max(np.mean(y_test), 1 - np.mean(y_test))
l6_counts = all(np.mean(m.predict(test) == y_test) > majority + 0.02
                for m in models)

seeds_holding = 0
for s in SPLIT_SEEDS:
    tr, te = train_test_split(labelled, test_size=n_flagged(len(labelled)), stratify=y, random_state=s)
    share = y.loc[te.index].value_counts(normalize=True).max()
    seeds_holding += all(np.mean(clone(m).fit(tr, y.loc[tr.index]).predict(te) == y.loc[te.index]) > share + MARGIN for m in models)
print(f"l6_counts = {l6_counts}. Se sostiene en {seeds_holding} de {len(SPLIT_SEEDS)} particiones")
if seeds_holding < len(SPLIT_SEEDS):
    print("Con otra partición de los datos este resultado cambia: tómalo como débil.")
```

**Lo que vemos.** La predicción cuenta en las cinco particiones. En otros datos puede salir `l6_counts = False`. Es un resultado normal y se informa con su razón.

### Paso 5. ¿De dónde sale la señal?
En este paso probamos dos variantes: solo `n_authors`, y todo menos `n_authors`. Así vemos qué atributo lleva la señal.

```python
def heldout_accuracy(columns):
    """Exactitud de los tres métodos en las filas apartadas, usando solo estas columnas.

    Qué hace: arma una preparación con las columnas pedidas, entrena una copia nueva de
    cada modelo con train y mide la exactitud en test. Los modelos ya entrenados no cambian.

    Entrada:
        columns: la lista de columnas de entrada.

    Salida:
        Una lista con la exactitud de la regresión, el bosque y la red, a 2 decimales.
    """
    numbers_only = [c for c in NUMBER_COLUMNS if c in columns]
    categories_only = [c for c in CATEGORY_COLUMNS if c in columns]
    steps = [("num", make_pipeline(SimpleImputer(strategy="median", add_indicator=True), StandardScaler()), numbers_only)]
    if categories_only:
        steps.append(("cat", make_pipeline(SimpleImputer(strategy="most_frequent"), OneHotEncoder(handle_unknown="ignore")), categories_only))
    return [round(accuracy_score(y_test, make_pipeline(ColumnTransformer(steps), clone(m)).fit(train, y_train).predict(test)), 2) for m in (lr, forest, network)]

print(f"Clase mayor {majority:.2f}")
print("Solo n_authors:     ", heldout_accuracy(["n_authors"]))
print("Todo menos n_authors:", heldout_accuracy([c for c in NUMBER_COLUMNS + CATEGORY_COLUMNS if c != "n_authors"]))
print(f"Regla n_authors >= 4 en las {len(labelled)} filas con etiqueta: {((attributes.loc[labelled.index, 'n_authors'] >= 4).astype(int) == y).mean():.2f}")
```

### Paso 6. La regla y los modelos en las cinco particiones
En este paso repetimos la comparación en las cinco particiones de `SPLIT_SEEDS`. La última columna es el umbral que más acierta en las filas de entrenamiento.

```python
without = ColumnTransformer([("num", make_pipeline(SimpleImputer(strategy="median", add_indicator=True), StandardScaler()), ["year", "is_oa"]),
                             ("cat", make_pipeline(SimpleImputer(strategy="most_frequent"), OneHotEncoder(handle_unknown="ignore")), CATEGORY_COLUMNS)])
by_seed = []
for s in SPLIT_SEEDS:
    tr, te = train_test_split(labelled, test_size=n_flagged(len(labelled)), stratify=y, random_state=s)
    y_tr, y_te = y.loc[tr.index], y.loc[te.index]
    authors_tr, authors_te = attributes.loc[tr.index, "n_authors"], attributes.loc[te.index, "n_authors"]
    row = {"semilla": s, "clase mayor": y_te.value_counts(normalize=True).max(), "regla": ((authors_te >= 4).astype(int) == y_te).mean()}
    for name, m in zip(["regresión", "bosque", "red"], (lr, forest, network)):
        row[name] = accuracy_score(y_te, make_pipeline(clone(prepare), clone(m)).fit(tr, y_tr).predict(te))
        row[f"{name} sin n_authors"] = accuracy_score(y_te, make_pipeline(clone(without), clone(m)).fit(tr, y_tr).predict(te))
    row["mejor umbral"] = max(range(1, 21), key=lambda t: ((authors_tr >= t).astype(int) == y_tr).mean())
    by_seed.append(row)
by_seed = pd.DataFrame(by_seed).set_index("semilla")
print(by_seed.round(3).to_string())
```

**Lo que vemos.** La regla gana en las semillas 7 y 8. En la 9 y la 10 gana la red, y en la 11 el bosque empata. Sin `n_authors` los modelos siguen sobre la clase mayor. El mejor umbral es 4 en las cinco.

**Lo que encontramos.** La señal es el número de autores. Más autores quiere decir más instituciones, y más países. Tres modelos no le ganan con claridad a una regla de una línea. El resultado es real pero modesto, y se dice así.

**Tres errores para leer.** La celda muestra tres artículos donde el bosque se equivoca. Un error puede ser del modelo o de la etiqueta.

```python
said_rf = pd.Series(pred_rf, index=test.index)
wrong = test.index[said_rf != y_test][:3]
for t in wrong:
    print(f"{t[:80]}  autores {attributes.loc[t, 'n_authors']:.0f}, países {attributes.loc[t, 'n_countries']}, el bosque dijo {said_rf[t]}")
```

---

## Parte 6. Despliegue

### Paso 1. El resultado de la predicción
En este paso definimos el resultado de la predicción: positivo si **al menos 2 de los 3 métodos** dicen que sí. Cada artículo lo puntúa un modelo que no vio su etiqueta. Los artículos sin etiqueta no reciben este resultado.

```python
folds = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)
models = [make_pipeline(prepare, m) for m in (lr, forest, network)]

train_votes = sum(cross_val_predict(m, train, y_train, cv=folds)   # fuera del pliegue
                  for m in models)
test_votes = sum(m.fit(train, y_train).predict(test)                # apartadas
                 for m in models)
voted = pd.concat([train.assign(votes=train_votes),       # con el título como índice, como table
                   test.assign(votes=test_votes)])["votes"]
# 2 de 3 de acuerdo. Las filas sin etiqueta quedan en False
table["prediction"] = (voted >= 2).reindex(table.index, fill_value=False)

majority = max(np.mean(y_test), 1 - np.mean(y_test))
l6_counts = all(np.mean(m.predict(test) == y_test) > majority + 0.02
                for m in models)
print(f"Predichos positivos: {table['prediction'].sum()} de {len(labelled)} con etiqueta. l6_counts = {l6_counts}")
```

**Comprobar:**

En este paso comprobamos que solo los artículos con etiqueta reciben el resultado y que los votos cuadran.

```python
assert not table.loc[~table.index.isin(labelled.index), "prediction"].any()
assert table.loc[labelled.index, "prediction"].sum() == (train_votes >= 2).sum() + (test_votes >= 2).sum()
print("Resultado de la predicción sin filas vistas: OK")
```

### Paso 2. ¿Se repite con el texto?
En este paso medimos si la etiqueta repite el texto de la Lección 4, con phi entre la etiqueta y `text_says_read`. Si phi es al menos 0,30 en valor absoluto, cuentan como **un** resultado (`text_or_prediction`).

```python
phi = np.corrcoef(y, table.loc[labelled.index, "text_says_read"].astype(int))[0, 1]
one_support = abs(phi) >= 0.30
print(f"phi entre la etiqueta y el texto de la L4: {phi:.2f} (límite 0.30). {'Un solo resultado' if one_support else 'Dos resultados separados'}")
```

**Lo que vemos.** phi es casi 0, así que el texto y la predicción cuentan por separado.

### Paso 3. La lista inicial
En este paso sumamos los cinco resultados. Un artículo entra en la lista inicial según `MIN_SUPPORTS`, el número de resultados a favor que pide el código. `MIN_SUPPORTS` empieza en 2 y se puede cambiar. Cada grupo fija y justifica este número en su proyecto. 0 o 1 valen si se explica. La celda cuenta cuántos artículos tienen 0, 1, 2 y 3 o más resultados a favor.

```python
added = table["prediction"] & l6_counts & ~table["text_says_read"]
if one_support:                    # |phi| >= 0.30: la etiqueta repite la L4
    table["text_or_prediction"] = table["text_says_read"] | (table["prediction"] & l6_counts)
    SUPPORT_COLUMNS = ["has_pattern", "read_group", "text_or_prediction", "graph_support"]
else:
    table["prediction"] = table["prediction"] & l6_counts
    SUPPORT_COLUMNS = ["has_pattern", "read_group", "text_says_read", "graph_support", "prediction"]

table["supports"] = table[SUPPORT_COLUMNS].astype(int).sum(axis=1)
table["in_view"] = table["supports"] >= MIN_SUPPORTS
print(f"En vista: {table['in_view'].sum()}. Con tres resultados a favor: {(table['supports'] >= 3).sum()}. La predicción agrega {added.sum()} que el texto no tenía")
counts = table["supports"].clip(upper=3).value_counts().reindex(range(4), fill_value=0).rename(index={3: "3 o más"})
print(counts.rename_axis("resultados a favor").to_frame("artículos").T.to_string())
```

### Paso 4. Quitar cada resultado una vez
En este paso quitamos cada resultado y contamos quién sale de la lista con `MIN_SUPPORTS = 2`. La lista depende mucho de un resultado que saca a muchos.

```python
drop_one = {}
for column in SUPPORT_COLUMNS:
    rest = [c for c in SUPPORT_COLUMNS if c != column]
    drop_one[column] = int((table["in_view"] & (table[rest].astype(int).sum(axis=1) < MIN_SUPPORTS)).sum())
print("Salen de la lista si quitamos:", drop_one)
```

**Comprobar:**

En este paso comprobamos que el número de resultados a favor está en su rango y que quitamos cada resultado una vez.

```python
assert table["supports"].between(0, len(SUPPORT_COLUMNS)).all()
assert set(drop_one) == set(SUPPORT_COLUMNS)
print("Lista inicial y sensibilidad: OK")
```

**Lo que vemos.** Hay 97 artículos en vista, 31 más que con cuatro. Sin la predicción salen 31 y sin el patrón salen 32.

### Paso 5. Una lista que se pueda leer
En este paso recortamos la lista con la regla de la Lección 4: el máximo de 30 artículos, ordenando por resultados a favor, `prob_texto` y título. El resto queda con `recortado = True`.

```python
MAX_LIST = MAX_PAPERS
if "prob_texto" in text_l4.columns:
    prob_text = text_l4.assign(prob_texto=pd.to_numeric(text_l4["prob_texto"], errors="coerce")).groupby("title")["prob_texto"].max()
else:
    prob_text = pd.Series(dtype=float)
    print("texto_l4.csv no trae prob_texto. Dentro de cada número de resultados a favor se ordena por título.")
table["prob_texto"] = prob_text.reindex(table.index)
starter_list = (table.loc[table["in_view"], SUPPORT_COLUMNS + ["supports", "prob_texto"]].reset_index()
                .sort_values(["supports", "prob_texto", "title"], ascending=[False, False, True], na_position="last"))
starter_list["recortado"] = np.arange(len(starter_list)) >= MAX_LIST
kept = int((~starter_list["recortado"]).sum())
print(f"En vista {len(starter_list)}. Se leen {kept}, recortados {int(starter_list['recortado'].sum())} (máximo {MAX_LIST})")
if kept < 5:
    print("La lista tiene menos de 5 artículos, se lee completa y se reporta como resultado débil.")
```

**Comprobar:**

En este paso comprobamos el tamaño de la lista que se lee y que va ordenada por resultados a favor.

```python
assert kept <= MAX_LIST and kept == min(len(starter_list), MAX_LIST)
assert starter_list["supports"].is_monotonic_decreasing
print("Lista recortada: OK")
```

**Lo que vemos.** De 97 en vista se leen 30 y quedan 67 recortados, que siguen en el archivo.

**Lo que aprendemos aquí.** La lista crece mucho con la predicción, porque el 53% se predice internacional. Ser internacional no es una razón para leer. La lista inicial es un punto de partida.

### Paso 6. Guardar la predicción y la lista
En este paso guardamos `outputs/prediccion_l6.csv` y `outputs/lista_inicial.csv`. `votos` es cuántos métodos dijeron internacional.

```python
prediction_table = pd.DataFrame({
    "title": titles,
    "etiqueta": y.reindex(titles).astype("Int64").to_numpy(),
    "apartada": table.index.isin(test.index),
    "votos": voted.reindex(titles).astype("Int64").to_numpy(),
    "prediction": table.loc[titles, "prediction"].to_numpy(),
})
prediction_path = OUTPUTS_DIR / "prediccion_l6.csv"
prediction_table.to_csv(prediction_path, index=False)
starter_path = OUTPUTS_DIR / "lista_inicial.csv"
starter_list.to_csv(starter_path, index=False)
print(f"Guardado: {prediction_path} ({len(prediction_table)} filas) y {starter_path} ({len(starter_list)} filas)")
```

### Paso 7. Qué cambiaría la decisión
En este paso escribimos cómo entra la predicción y qué la cambiaría.

| Qué | Respuesta |
|-----|-----------|
| Cómo entra | La predicción cuenta a favor si al menos 2 de los 3 métodos dicen que sí, con un modelo que no vio la etiqueta, y solo si esta lección cuenta |
| Cómo se lee | La señal es el número de autores. Tres modelos no le ganan con claridad a contar autores. Con otras semillas la ventaja cambia |
| Qué lo cambia | Otra etiqueta. Otra partición de los datos. Los artículos sin afiliación. Otro margen que 0,02 |

**Lo que vemos.** Quien lea la lista sabe por qué la predicción apoya a un artículo sin abrir este cuaderno.

### Paso 8. Comprobación final
En este paso revisamos que el cuaderno dejó la predicción y la lista inicial.

```python
def _check_ok(name, predicate):
    """Ejecuta una comprobación sin detener el cuaderno: un error cuenta como incompleto.

    Salida:
        True si la comprobación pasó, False si no.
    """
    try:
        ok = bool(predicate())
    except Exception:
        ok = False
    print(f"{name}: {'OK' if ok else 'incompleto'}")
    return ok


checks = [
    ("outputs/prediccion_l6.csv", lambda: prediction_path.is_file()),
    ("outputs/lista_inicial.csv", lambda: starter_path.is_file()),
    ("Matrices de confusión", lambda: all((OUTPUTS_DIR / f).is_file() for f in ["confusion_regresion.png", "confusion_bosque.png", "confusion_red.png"])),
    ("Resultados de las lecciones 2 a 5", lambda: len(groups_l3) > 0 and len(graph_l5.dropna(how="all")) > 0),
]
passed = sum(_check_ok(n, f) for n, f in checks)
print(f"\nL6_CHECKS={passed}/{len(checks)}")
if passed == len(checks):
    print("L6_OK. Siga con la Lección 7.")
```

<!-- end NOTEBOOK: -->
