<!-- NOTEBOOK: -->

## Repaso de Python para este cuaderno

Este cuaderno utiliza los siguientes métodos de Python. Si ya los conoce, ejecute estas celdas rápido.
Un modelo aprende con `fit` en unas filas.
Después responde con `predict` en otras filas que no vio.

### Aprender en unas filas, responder en otras

```python
import numpy as np  # numpy arma los arreglos del ejemplo
from sklearn.model_selection import train_test_split  # train_test_split separa las filas en dos partes
from sklearn.tree import DecisionTreeClassifier  # DecisionTreeClassifier es un árbol de decisión

x_toy = np.array([[1], [2], [3], [4], [5], [6], [7], [8]])  # np.array arma un atributo con ocho filas
y_toy = np.array([0, 0, 0, 0, 1, 1, 1, 1])  # np.array arma la etiqueta de cada fila
x_tr, x_te, y_tr, y_te = train_test_split(x_toy, y_toy, test_size=4, stratify=y_toy, random_state=7)  # train_test_split aparta 4 filas con la misma proporción de cada clase
toy_model = DecisionTreeClassifier(random_state=7).fit(x_tr, y_tr)  # fit hace que el árbol aprenda con las otras 4 filas
said = toy_model.predict(x_te)  # predict responde en las filas apartadas
assert len(said) == len(y_te)  # una respuesta por fila apartada
print(f"Dijo {said.tolist()}, era {y_te.tolist()}. Aciertos: {int((said == y_te).sum())} de {len(y_te)}. Repaso de Python: OK")  # print compara lo dicho con la etiqueta
```

**Lo que vemos.** El árbol aprendió con cuatro filas y acertó las otras cuatro.
Con artículos reales los aciertos bajan.
Por eso comparamos con una línea base.

---

## Instrucciones

Seguimos con el equipo interno de la secretaría de salud y sus artículos sobre nutrición.
El equipo debe decidir **qué artículos tiene que leer** un nuevo colega.

Hasta ahora cada resultado salió de los datos mismos.
Ahora alguien nos da una etiqueta.
Por años, los programas que clasificaban seguían reglas escritas a mano.
Después se pasó a aprender la regla desde ejemplos etiquetados (LeCun, Bengio y Hinton, 2015).
Hoy sumamos el último resultado: **predecir una etiqueta dada**.
La etiqueta es `internacional`: autores de al menos dos países (`n_countries >= 2`).

Medimos aciertos y errores en artículos que ningún modelo vio.
Cada modelo se compara con la **clase mayoritaria** y con una regla de una línea, sin modelo.

**Tres métodos, tres preparaciones.**

| Método | Pregunta | Preparación que necesita |
|--------|----------|--------------------------|
| M1. Regresión logística | ¿Qué atributos pesan a favor y en contra? | Números escalados, categorías en columnas de 0 y 1, faltantes llenados |
| M2. Bosque aleatorio | ¿Qué cortes en los atributos separan las clases? | La misma tabla. Escalar no cambia un corte |
| M3. Una capa oculta | ¿Qué combinación de atributos separa las clases? | Todo numérico y escalado, faltantes llenados |

**Qué hacer.** Ejecute las celdas de arriba hacia abajo.
Cada paso empieza con **En este paso**. Si tiene código, termina con una celda **Comprobar**.

**Mapa del cuaderno**

| Parte | Fase CRISP-DM | Qué sale |
|-------|---------------|----------|
| 1 | Comprensión del negocio | La pregunta de hoy, los parámetros y la función contra la fuga |
| 2 | Comprensión de los datos | La etiqueta y los atributos |
| 3 | Preparación de los datos | La tabla, el conjunto apartado y la preparación |
| 4 | Modelado | Clase mayoritaria, regresión logística, bosque y una capa oculta |
| 5 | Evaluación | Aciertos y errores, cinco pliegues, la regla de una línea y una fuga a propósito |
| 6 | Despliegue | La predicción y una lista de hasta 30 artículos |

**Carpetas.** La celda de configuración crea `data/` (datos descargados) y `outputs/` (tablas y gráficos).

---

## Parte 1. Comprensión del negocio

### Paso 1. La pregunta de esta lección
En este paso escribimos qué buscamos hoy.
La decisión no cambia: qué artículos debe leer el colega nuevo.

| Pregunta | Respuesta para el laboratorio |
|----------|-------------------------------|
| ¿Qué buscamos? | Predecir si un artículo es internacional a partir de sus atributos |
| ¿Con qué lo medimos? | Regresión logística, un bosque aleatorio y una red con una capa oculta |
| ¿Contra qué los comparamos? | Contra la clase mayoritaria y contra una regla de una línea |
| ¿Cómo entra la predicción en la lista? | Un artículo entra si al menos 2 de los 3 métodos dicen que sí, con un modelo que no vio su etiqueta, y los tres métodos superan a la clase mayoritaria. La lista guarda como máximo 30 |

Ser internacional no es, por sí solo, una razón para leer.
Esta lista muestra esa predicción.
Cómo se junta con los resultados de otras semanas lo decide el grupo, y lo anota en el cuaderno de grupo.

### Paso 2. Configuración
En este paso importamos las librerías, creamos las carpetas y fijamos los parámetros.
No cambie los parámetros.

```python
import math  # math.ceil redondea hacia arriba los mínimos
from pathlib import Path  # Path arma las rutas de las carpetas

import matplotlib.pyplot as plt  # matplotlib dibuja las figuras
import numpy as np  # numpy calcula promedios y cuenta
import pandas as pd  # pandas lee y guarda las tablas
import requests  # requests descarga los datos del curso
from sklearn.base import clone  # clone copia un modelo sin entrenar
from sklearn.compose import ColumnTransformer  # ColumnTransformer prepara cada tipo de columna a su manera
from sklearn.dummy import DummyClassifier  # DummyClassifier dice siempre la clase mayoritaria
from sklearn.ensemble import RandomForestClassifier  # RandomForestClassifier es el bosque aleatorio
from sklearn.impute import SimpleImputer  # SimpleImputer llena los faltantes
from sklearn.linear_model import LogisticRegression  # LogisticRegression es la regresión logística
from sklearn.metrics import ConfusionMatrixDisplay, accuracy_score, confusion_matrix  # medidas de aciertos y errores
from sklearn.model_selection import StratifiedKFold, cross_val_predict, train_test_split  # particiones y pliegues
from sklearn.neural_network import MLPClassifier  # MLPClassifier es la red con una capa oculta
from sklearn.pipeline import make_pipeline  # make_pipeline encadena la preparación y el modelo
from sklearn.preprocessing import OneHotEncoder, StandardScaler  # columnas de 0 y 1, y escalado

# Carpetas de trabajo
DATA_DIR = Path("data")  # aquí quedan los datos descargados
OUTPUTS_DIR = Path("outputs")  # aquí quedan las tablas y las figuras
DATA_DIR.mkdir(parents=True, exist_ok=True)  # mkdir crea la carpeta de datos si no existe
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)  # mkdir crea la carpeta de salidas si no existe
BASE_URL = "https://cabrerac.github.io/assets/data/26-udenar-data-mining"  # la dirección web de los datos del curso

# Desde L2, sin cambios
SEED = 7  # semilla de todos los sorteos

# Desde L4, sin cambios
FLAGGED_SHARE = 0.20  # proporción de filas apartadas
FLAGGED_MIN = 40  # mínimo de filas apartadas
POSITIVE_SHARE = 0.10  # proporción mínima de positivos en la etiqueta
POSITIVES_MIN = 30  # mínimo de positivos
C_REG = 10  # penalización de la regresión logística (más alto, menos penalización)
N_FOLDS = 5  # número de pliegues

# L6 (no cambiar)
LABEL = "internacional"  # laboratorio: autores de al menos dos países
HIDDEN_UNITS = 8  # igual que la diapositiva de mlp-implementation.md
PENALTY = 1.0  # pocas filas, así que una penalización más fuerte que la de la diapositiva (1e-4)
N_TREES = 200  # árboles del bosque
MARGIN = 0.02  # cuánto sobre la clase mayoritaria debe quedar cada método para que la L6 cuente
SPLIT_SEEDS = (7, 8, 9, 10, 11)  # otras particiones, para ver si el resultado se sostiene


def n_flagged(n: int) -> int:
    """Tamaño del conjunto apartado, con la regla de la L4.

    Qué hace: aparta el 20% de las filas (FLAGGED_SHARE), redondeado hacia arriba, y
    nunca menos de FLAGGED_MIN, para que la exactitud no dependa de dos o tres artículos.

    Entrada:
        n: el número de filas con etiqueta.

    Salida:
        El número entero de filas que se apartan.
    """
    return max(FLAGGED_MIN, math.ceil(FLAGGED_SHARE * n))  # max nunca baja de FLAGGED_MIN, y ceil redondea el 20% hacia arriba


def min_positives(n: int) -> int:
    """Cuántas filas necesita la clase minoritaria, con la regla de la L4.

    Qué hace: pide el 10% de las filas (POSITIVE_SHARE), redondeado hacia arriba, y nunca
    menos de POSITIVES_MIN. Con menos, un modelo aprende casi nada de esa clase.

    Entrada:
        n: el número de filas con etiqueta.

    Salida:
        El número entero mínimo de filas de la clase minoritaria.
    """
    return max(POSITIVES_MIN, math.ceil(POSITIVE_SHARE * n))  # max nunca baja de POSITIVES_MIN, y ceil redondea el 10% hacia arriba


print(f"Etiqueta: {LABEL} (n_countries >= 2). Una capa oculta de {HIDDEN_UNITS} unidades con penalización {PENALTY}, {N_TREES} árboles")  # print muestra la etiqueta y los parámetros
```

### Paso 3. La fuga de la respuesta
En este paso escribimos la función que quita de `n_claims` la propiedad que define la etiqueta.
Los artículos de nutrición no tienen `n_claims`, pero las tablas de Wikidata sí.
Si `n_claims` cuenta la etiqueta, el modelo vería la respuesta.
Eso es una **fuga**.
La probamos con una tabla de juguete.

```python
PROPERTY_COLUMN = {"P18": "has_image"}  # propiedad de Wikidata -> columna de la tabla
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
    prop = LABEL_PROPERTY.get(label)  # get devuelve la propiedad de la etiqueta, o None si no es una propiedad
    if prop is None:  # la etiqueta no es una propiedad
        return table["n_claims"].astype(int)  # n_claims queda igual
    column = PROPERTY_COLUMN[prop]  # la columna que guarda esa propiedad
    return (table["n_claims"] - table[column]).astype(int)  # restamos la propiedad de la etiqueta


toy_table = pd.DataFrame({"n_claims": [12, 7, 1, 0], "has_image": [1, 0, 1, 0]})  # DataFrame arma la tabla de juguete
result = n_claims_without(toy_table, "tiene_imagen")  # n_claims_without quita la imagen de n_claims
y = toy_table["has_image"]  # la etiqueta de juguete es tener imagen
print(pd.DataFrame({"n_claims": toy_table["n_claims"], "has_image": y, "sin la imagen": result}))  # print muestra antes y después
```

**Lo que vemos.** Las dos filas con imagen pierden una propiedad.
Las otras quedan igual.

**Comprobar:**

Comprobamos que la función quita la imagen de `n_claims` en las filas con imagen y nada más.

```python
assert (result >= 0).all()  # ningún conteo queda negativo
assert (toy_table.loc[toy_table["has_image"] == 1, "n_claims"] >= 1).all()  # las filas con imagen tenían al menos una propiedad
assert ((toy_table["n_claims"] - result) == y).all()  # la diferencia es justo la imagen
print("Fuga quitada con una etiqueta que es una propiedad: OK")  # print confirma la comprobación
```

**Comprobar:**

Comprobamos que con una etiqueta que no es una propiedad, `n_claims` no cambia.

```python
assert (n_claims_without(toy_table, "categoria") == toy_table["n_claims"]).all()  # con otra etiqueta n_claims queda igual
print("Con otra etiqueta, n_claims queda igual: OK")  # print confirma la comprobación
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
    dest = folder / name  # la ruta local del archivo
    if dest.is_file() and dest.stat().st_size > 0:  # is_file y st_size dicen si ya lo tenemos y no está vacío
        print(f"Ya en caché: {dest}")  # print avisa que usamos la copia local
        return dest  # devolvemos la ruta sin descargar
    response = requests.get(f"{BASE_URL}/{name}", timeout=60)  # requests.get descarga el archivo
    response.raise_for_status()  # raise_for_status detiene la celda si la descarga falló
    dest.write_bytes(response.content)  # write_bytes guarda el archivo en la carpeta
    print(f"Descargado: {dest}")  # print avisa que el archivo quedó guardado
    return dest  # devolvemos la ruta local


raw = pd.read_csv(download_data("nutricion-papers.csv"), keep_default_na=False)  # read_csv lee los artículos y deja los vacíos como texto vacío
papers = raw.drop_duplicates("title").reset_index(drop=True)  # drop_duplicates deja una fila por título
N = len(papers)  # len cuenta los artículos
print(f"{len(raw)} filas, {N} sin títulos repetidos, como en la L5")  # print muestra los dos tamaños
```

### Paso 5. La pregunta
La pregunta es la de la Lección 1.
El equipo decide qué artículos de nutrición leer, y qué filtro los puso en la lista.
La lista tiene entre 10 y 30 artículos.

```python
MIN_PAPERS = 10  # la lista tiene al menos 10 artículos
MAX_PAPERS = 30  # la lista tiene como máximo 30 artículos
print(f"Lista: entre {MIN_PAPERS} y {MAX_PAPERS} artículos")  # print muestra el tamaño de la lista
```

### Paso 6. Los títulos de esta lección
En este paso dejamos una fila por título.
La predicción de más adelante se escribe en esa tabla.
No leemos los archivos de las lecciones anteriores.

```python
titles = list(papers["title"])  # list guarda los títulos en orden
table = pd.DataFrame(index=pd.Index(titles, name="title"))  # DataFrame arma una fila por título
print(f"Artículos: {len(table)}")  # print muestra cuántas filas tiene la tabla
```

**Comprobar:**

Comprobamos que hay una fila por título y que no hay títulos repetidos.

```python
assert len(table) == N and table.index.is_unique  # una fila por título, sin repetidos
print("Títulos: OK")  # print confirma la comprobación
```

**Lo que vemos.** Con cuatro resultados hay 66 artículos en vista, los mismos de la Lección 5.

---

## Parte 2. Comprensión de los datos

### Paso 1. La etiqueta `internacional`
En este paso construimos la etiqueta: `n_countries >= 2`.
Un `n_countries = 0` quiere decir que OpenAlex no encontró la afiliación.
Esos artículos quedan fuera como faltantes y no reciben el resultado.

```python
papers["n_countries"] = pd.to_numeric(papers["n_countries"], errors="coerce").fillna(0).astype(int)  # to_numeric lee los países y fillna deja en 0 los que faltan
papers["n_authors"] = pd.to_numeric(papers["n_authors"], errors="coerce")  # to_numeric lee el número de autores
missing = papers["n_countries"] == 0  # sin países quiere decir sin afiliación
print(f"Sin datos de afiliación: {missing.sum()} ({(papers.loc[missing, 'n_authors'] > 0).sum()} de ellos con autores)")  # print muestra cuántos faltan
labelled_count = int((~missing).sum())  # contamos los artículos con etiqueta
positives = int((papers.loc[~missing, "n_countries"] >= 2).sum())  # contamos los internacionales
print(f"Con etiqueta: {labelled_count}. Internacionales: {positives} ({positives / labelled_count:.0%})")  # print muestra los dos conteos
```

**Comprobar:**

Comprobamos que la clase minoritaria tiene suficientes filas.

```python
assert min(positives, labelled_count - positives) >= min_positives(labelled_count)  # la clase minoritaria llega al mínimo
print(f"Clase minoritaria con al menos {min_positives(labelled_count)} filas: OK")  # print confirma la comprobación
```

**Lo que vemos.** Quedan 276 artículos con etiqueta, y 145 (53%) son internacionales.
La clase mayoritaria acierta poco más de la mitad.

### Paso 2. Los atributos
En este paso elegimos las entradas: año, número de autores, tipo de revista, acceso abierto y tipo de trabajo.
No usamos lo que ya fue un resultado (texto, temas, citas, enlaces).
Tampoco usamos `n_countries`, que define la etiqueta.

```python
print("Idioma:", papers["language"].value_counts().to_dict())  # value_counts cuenta los artículos por idioma
print("Tipo de revista:", papers["venue_type"].replace("", "(vacío)").value_counts().to_dict())  # value_counts cuenta los artículos por tipo de revista
print("Tipo de trabajo:", papers["work_type"].value_counts().to_dict())  # value_counts cuenta los artículos por tipo de trabajo
print(papers[["year", "n_authors"]].apply(pd.to_numeric, errors="coerce").describe().round(1))  # describe resume el año y el número de autores
```

**Lo que vemos.** `venue_type` casi no varía.
`n_authors` va de 0 a 100, y 100 es un tope del archivo.
La mediana es 8 autores.

---

## Parte 3. Preparación de los datos

### Paso 1. La tabla con etiqueta
En este paso armamos `labelled`, las filas con etiqueta.
El título es el índice, igual que en `table`.

```python
NUMBER_COLUMNS = ["year", "n_authors", "is_oa"]  # las columnas de números
CATEGORY_COLUMNS = ["venue_type", "work_type"]  # las columnas de categorías

attributes = papers.set_index("title")  # set_index usa el título como índice
attributes["year"] = pd.to_numeric(attributes["year"], errors="coerce")  # to_numeric lee el año
attributes["is_oa"] = pd.to_numeric(attributes["is_oa"], errors="coerce")  # to_numeric lee el acceso abierto
for c in CATEGORY_COLUMNS:  # recorremos las columnas de categorías
    attributes[c] = attributes[c].replace("", np.nan)  # replace marca el texto vacío como faltante
labelled = attributes.loc[attributes["n_countries"] > 0, NUMBER_COLUMNS + CATEGORY_COLUMNS]  # loc deja las filas con afiliación y las columnas de entrada
y = (attributes.loc[labelled.index, "n_countries"] >= 2).astype(int)  # la etiqueta: 1 si hay al menos dos países
print(f"{len(labelled)} filas con etiqueta, {y.sum()} internacionales")  # print muestra los dos conteos
```

### Paso 2. El conjunto apartado
En este paso apartamos `n_flagged(n)` filas, con la misma proporción de cada clase.
Ningún modelo las ve al aprender.

```python
train, test = train_test_split(labelled, test_size=n_flagged(len(labelled)), stratify=y, random_state=SEED)  # train_test_split aparta n_flagged filas con la misma proporción de cada clase
y_train, y_test = y.loc[train.index], y.loc[test.index]  # loc toma la etiqueta de cada parte
print(f"Para aprender: {len(train)}. Apartadas: {len(test)} ({y_test.mean():.0%} internacionales)")  # print muestra los dos tamaños
```

**Comprobar:**

Comprobamos el tamaño del conjunto apartado, que no comparte filas y que las dos partes tienen proporciones parecidas.

```python
assert len(test) == n_flagged(len(labelled)) and not set(train.index) & set(test.index)  # tamaño correcto y sin filas compartidas
assert abs(y_train.mean() - y_test.mean()) < 0.05  # proporciones parecidas en las dos partes
print("Conjunto apartado: OK")  # print confirma la comprobación
```

### Paso 3. Escalar, codificar y llenar faltantes
En este paso preparamos la tabla con el código de las diapositivas.
Los números se llenan con la mediana y se escalan.
Las categorías se llenan con la más común y pasan a columnas de 0 y 1.
Todo se aprende **solo con las filas de entrenamiento**.

```python
numbers = make_pipeline(SimpleImputer(strategy="median", add_indicator=True), StandardScaler())  # los números se llenan con la mediana y se escalan
categories = make_pipeline(SimpleImputer(strategy="most_frequent"), OneHotEncoder(handle_unknown="ignore"))  # las categorías se llenan con la más común y pasan a columnas de 0 y 1
prepare = ColumnTransformer([("num", numbers, NUMBER_COLUMNS), ("cat", categories, CATEGORY_COLUMNS)])  # ColumnTransformer aplica cada preparación a sus columnas

X_train = prepare.fit_transform(train)  # fit_transform aprende medianas, escalas y categorías
X_test = prepare.transform(test)  # transform las reutiliza y nunca vuelve a aprender
feature_names = prepare.get_feature_names_out()  # get_feature_names_out da el nombre de cada columna preparada
print(f"{X_train.shape[1]} columnas preparadas: {list(feature_names)}")  # print muestra las columnas preparadas
```

**Comprobar:**

Comprobamos la forma de las tablas preparadas y que no quedan faltantes.

```python
assert X_train.shape == (len(train), len(feature_names)) and X_test.shape[1] == len(feature_names)  # las dos tablas tienen las mismas columnas
assert not np.isnan(np.asarray(X_train, dtype=float)).any()  # isnan confirma que no quedan faltantes
print("Preparación: OK")  # print confirma la comprobación
```

**Lo que vemos.** Las 5 columnas de entrada se vuelven 12.

---

## Parte 4. Modelado

### La clase mayoritaria
En este paso construimos la línea base.
Decimos siempre la clase más común, aquí internacional.

```python
baseline = DummyClassifier(strategy="most_frequent").fit(X_train, y_train)  # DummyClassifier aprende cuál es la clase más común
pred_majority = baseline.predict(X_test)  # predict dice esa clase en todas las filas apartadas
majority = max(np.mean(y_test), 1 - np.mean(y_test))  # la parte de la clase mayoritaria en las filas apartadas
print(f"La clase mayoritaria acierta {accuracy_score(y_test, pred_majority):.2f} de las apartadas")  # accuracy_score cuenta la parte de aciertos
```

### M1. Regresión logística
En este paso usamos la regresión logística de la Lección 4.
Un peso positivo empuja hacia internacional.
`class_weight="balanced"` da el mismo peso a las dos clases.

```python
lr = LogisticRegression(class_weight="balanced", C=C_REG, max_iter=1000)  # LogisticRegression prepara la regresión con clases balanceadas
lr.fit(X_train, y_train)  # fit aprende un peso por columna
pred_lr = lr.predict(X_test)  # predict responde en las filas apartadas

weights = pd.Series(lr.coef_[0], index=feature_names)  # coef_ guarda el peso de cada columna
print(weights.sort_values().round(2))  # sort_values ordena los pesos de menor a mayor
```

**Lo que vemos.** Pesan más los tipos de trabajo.
Revisión (1,32) y artículo (0,98) empujan hacia internacional, y preprint (-1,13) hacia nacional.
`n_authors` pesa 0,44.

### Un corte a mano
En este paso hacemos a mano lo que hace un árbol en cada nodo, con los números de la diapositiva.
El árbol prueba cada umbral y se queda con el que deja los lados más puros.
Al final `y` vuelve a ser la etiqueta `internacional`.

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
    n = len(labels)  # len cuenta las etiquetas
    squares = 0.0  # aquí sumamos las proporciones al cuadrado
    for c in set(labels):  # recorremos cada clase distinta
        squares += (labels.count(c) / n) ** 2  # count cuenta las filas de esa clase
    return 1 - squares  # 1 menos la suma


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
    left = []  # aquí guardamos las etiquetas del lado izquierdo
    right = []  # aquí guardamos las etiquetas del lado derecho
    for xi, yi in zip(x, y):  # zip recorre cada valor junto con su etiqueta
        if xi <= threshold:  # el valor no pasa del umbral
            left.append(yi)  # la fila va a la izquierda
        else:  # el valor pasa del umbral
            right.append(yi)  # la fila va a la derecha
    n = len(y)  # len cuenta todas las filas
    return len(left) / n * gini(left) + len(right) / n * gini(right)  # cada lado pesa según su parte de las filas


x = [1, 2, 3, 4, 5, 6]  # un atributo
y = [0, 0, 0, 1, 1, 1]  # las etiquetas
candidates = sorted(set(x))[:-1]  # los umbrales que se prueban, sin el último valor
best = candidates[0]  # empezamos con el primer umbral
toy_scores = {}  # aquí guardamos la impureza de cada umbral
for t in candidates:  # recorremos cada umbral
    toy_scores[t] = round(split_score(x, y, t), 3)  # split_score mide la impureza de ese corte
    if split_score(x, y, t) < split_score(x, y, best):  # este corte deja los lados más puros
        best = t  # nos quedamos con este umbral
print(best)  # print muestra el mejor umbral, 3
y = (attributes.loc[labelled.index, "n_countries"] >= 2).astype(int)  # y vuelve a ser la etiqueta de la L6
```

**Comprobar:**

Comprobamos el mejor corte de la tabla de ejemplo y su impureza.

```python
assert best == 3 and toy_scores[best] == 0.0 and gini([0, 0, 1, 1]) == 0.5, "El mejor umbral de la diapositiva es 3"  # el umbral 3 deja los dos lados puros
for t in toy_scores:  # recorremos los otros umbrales
    assert t == best or toy_scores[t] > 0  # los otros cortes dejan algo de mezcla
assert y.index.equals(labelled.index)  # y volvió a ser la etiqueta de la L6
print("Corte a mano: OK", toy_scores)  # print confirma la comprobación
```

Con datos reales ningún corte deja los lados puros.
Por eso el bosque junta muchos árboles y los deja votar.

### M2. Bosque aleatorio
En este paso entrenamos 200 árboles.
Cada uno usa una muestra al azar de filas y atributos.
`min_samples_leaf=3` evita hojas de una fila.
La importancia es cuánto baja la impureza de Gini.

```python
forest = RandomForestClassifier(n_estimators=N_TREES, min_samples_leaf=3, random_state=SEED)  # RandomForestClassifier prepara 200 árboles con hojas de al menos 3 filas
forest.fit(X_train, y_train)  # escalar no cambia un corte, así que sirve el mismo X_train
pred_rf = forest.predict(X_test)  # predict deja votar a los árboles en las filas apartadas

importance = pd.Series(forest.feature_importances_, index=feature_names)  # feature_importances_ dice cuánto baja la impureza cada columna
print(importance.nlargest(5).round(3))  # nlargest muestra las 5 columnas más importantes
```

**Lo que vemos.** El bosque usa sobre todo `n_authors` (0,51) y el año (0,37).

### M3. Una capa oculta
En este paso entrenamos una red con una capa oculta de `HIDDEN_UNITS` unidades.
`PENALTY` es la penalización L2 (`alpha`).
Es más fuerte que la de la diapositiva porque hay pocas filas.

```python
network = MLPClassifier(hidden_layer_sizes=(HIDDEN_UNITS,), alpha=PENALTY, max_iter=3000, random_state=SEED)  # MLPClassifier prepara la red con una capa oculta
network.fit(X_train, y_train)  # X_train ya viene escalado por prepare
pred_nn = network.predict(X_test)  # predict responde en las filas apartadas
print(f"La red terminó en {network.n_iter_} pasos")  # n_iter_ dice cuántos pasos dio la red
```

**Lo que vemos.** La red paró en 188 pasos, lejos del máximo de 3000.

**Comprobar:**

Comprobamos que hay una predicción por fila apartada para cada método.

```python
predictions = {"clase mayoritaria": pred_majority, "regresión logística": pred_lr, "bosque": pred_rf, "una capa oculta": pred_nn}  # las cuatro predicciones, con su nombre
for name in predictions:  # recorremos cada método
    assert len(predictions[name]) == len(y_test), name  # una predicción por fila apartada
print("Cuatro predicciones sobre las filas apartadas: OK")  # print confirma la comprobación
```

---

## Parte 5. Evaluación

### Paso 1. Aciertos y errores en las filas apartadas
En este paso contamos TP, FP, FN y TN de cada método, y su exactitud.
Al lado ponemos una regla de una línea: **internacional si tiene al menos 4 autores**.
4 es el umbral que más acierta en las filas de entrenamiento (Paso 6).

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
    tn, fp, fn, tp = confusion_matrix(y, pred, labels=[0, 1]).ravel()  # confusion_matrix cuenta los cuatro casos y ravel los deja en fila
    return {"TP": tp, "FP": fp, "FN": fn, "TN": tn, "exactitud": round(accuracy_score(y, pred), 3)}  # devolvemos los conteos y la exactitud


pred_rule = (attributes.loc[test.index, "n_authors"] >= 4).astype(int).to_numpy()  # la regla dice internacional desde 4 autores
predictions["regla n_authors >= 4"] = pred_rule  # sumamos la regla a las predicciones
rows = {}  # aquí guardamos los conteos de cada método
for name, pred in predictions.items():  # recorremos cada método
    rows[name] = counts_of(y_test, pred)  # counts_of cuenta sus aciertos y errores
results = pd.DataFrame(rows).T  # DataFrame arma la tabla y T deja un método por fila
results = results.astype({"TP": int, "FP": int, "FN": int, "TN": int})  # astype deja los conteos como enteros
results  # mostramos la tabla
```

**Comprobar:**

Comprobamos que los cuatro casos suman las filas apartadas y que los tres métodos igualan o superan a la clase mayoritaria.

```python
assert (results[["TP", "FP", "FN", "TN"]].sum(axis=1) == len(y_test)).all()  # los cuatro casos suman las filas apartadas
for name in ["regresión logística", "bosque", "una capa oculta"]:  # recorremos los tres métodos
    assert results.loc[name, "exactitud"] >= majority, name  # el método iguala o supera a la clase mayoritaria
print("Los tres métodos igualan o superan a la clase mayoritaria: OK")  # print confirma la comprobación
```

**Lo que vemos.** Los tres métodos le ganan a la clase mayoritaria (0,52): regresión 0,61, bosque 0,71 y red 0,63.
La regla acierta 0,73, una fila más que el bosque.
Eso es menos que `MARGIN`, así que no le gana con claridad.

### Paso 2. Las matrices de confusión
En este paso dibujamos las matrices de confusión y las guardamos en `outputs/`.

```python
for name, pred, file in [("regresión logística", pred_lr, "confusion_regresion.png"), ("bosque", pred_rf, "confusion_bosque.png"), ("una capa oculta", pred_nn, "confusion_red.png")]:  # recorremos los tres métodos con su archivo
    fig, ax = plt.subplots(figsize=(3.5, 3.2))  # subplots abre la figura
    ConfusionMatrixDisplay.from_predictions(y_test, pred, labels=[0, 1], display_labels=["nacional", "internacional"], cmap="Blues", colorbar=False, ax=ax)  # from_predictions dibuja la matriz de confusión
    ax.set_title(name)  # set_title pone el nombre del método
    fig.tight_layout()  # tight_layout acomoda los márgenes
    fig.savefig(OUTPUTS_DIR / file, dpi=120)  # savefig guarda la figura
    plt.show()  # show muestra la figura
```

**Lo que vemos.** El bosque equilibra mejor los dos errores, con 8 FP y 8 FN.

### Paso 3. Cinco pliegues en las filas de entrenamiento
En este paso repetimos la cuenta con cinco pliegues sobre las 220 filas de entrenamiento.
La preparación va dentro de cada modelo.

```python
folds = StratifiedKFold(n_splits=N_FOLDS, shuffle=True, random_state=SEED)  # StratifiedKFold arma cinco pliegues con la misma proporción de cada clase
models = []  # aquí guardamos los tres métodos con su preparación
for m in (lr, forest, network):  # recorremos los tres métodos
    models.append(make_pipeline(prepare, m))  # make_pipeline pone la preparación antes del método
names = ["regresión logística", "bosque", "una capa oculta"]  # el nombre de cada método
cv_predictions = []  # aquí guardamos las predicciones fuera del pliegue
for m in models:  # recorremos los tres métodos
    cv_predictions.append(cross_val_predict(m, train, y_train, cv=folds))  # cross_val_predict predice cada fila con un modelo que no la vio
majority_cv = max(y_train.mean(), 1 - y_train.mean())  # la parte de la clase mayoritaria en las filas de entrenamiento
for name, p in zip(names, cv_predictions):  # recorremos cada método con sus predicciones
    print(f"{name:20s} exactitud en cinco pliegues {accuracy_score(y_train, p):.2f} (clase mayoritaria {majority_cv:.2f})")  # print compara con la clase mayoritaria
rule_train = ((attributes.loc[train.index, "n_authors"] >= 4).astype(int) == y_train).mean()  # mean da la parte de aciertos de la regla
print(f"{'regla n_authors >= 4':20s} exactitud en las {len(train)} filas de entrenamiento {rule_train:.2f}")  # print muestra la regla
```

**Lo que vemos.** Los tres quedan entre 0,61 y 0,65, contra 0,53 de la clase mayoritaria.
La regla acierta 0,69.
El bosque baja de 0,71 a 0,62, así que no leemos un solo número.

### Paso 4. ¿Cuenta la predicción?
En este paso decidimos si la predicción suma un resultado.
Cuenta (`l6_counts`) solo si los tres métodos quedan más de `MARGIN` (0,02) por encima de la clase mayoritaria en las filas apartadas.
Después repetimos con otras cuatro particiones, con copias sin entrenar (`clone`).

```python
majority = max(np.mean(y_test), 1 - np.mean(y_test))  # la parte de la clase mayoritaria en las filas apartadas
l6_counts = True  # empezamos suponiendo que cuenta
for m in models:  # recorremos los tres métodos
    accuracy = np.mean(m.predict(test) == y_test)  # mean da la parte de aciertos en las filas apartadas
    if accuracy <= majority + MARGIN:  # no supera a la clase mayoritaria por más de MARGIN
        l6_counts = False  # con un método que no la supera, la predicción no cuenta

seeds_holding = 0  # aquí contamos las particiones donde se sostiene
for s in SPLIT_SEEDS:  # recorremos las cinco semillas de partición
    tr, te = train_test_split(labelled, test_size=n_flagged(len(labelled)), stratify=y, random_state=s)  # train_test_split arma otra partición
    share = y.loc[te.index].value_counts(normalize=True).max()  # la parte de la clase mayoritaria en esas filas apartadas
    holds = True  # empezamos suponiendo que se sostiene
    for m in models:  # recorremos los tres métodos
        fitted = clone(m).fit(tr, y.loc[tr.index])  # clone copia el método sin entrenar y fit lo entrena en esta partición
        if np.mean(fitted.predict(te) == y.loc[te.index]) <= share + MARGIN:  # no supera a la clase mayoritaria por más de MARGIN
            holds = False  # en esta partición no se sostiene
    seeds_holding += holds  # sumamos 1 si se sostuvo
print(f"l6_counts = {l6_counts}. Se sostiene en {seeds_holding} de {len(SPLIT_SEEDS)} particiones")  # print muestra el resultado
if seeds_holding < len(SPLIT_SEEDS):  # no se sostiene en todas
    print("Con otra partición de los datos este resultado cambia: léalo como débil.")  # print avisa que el resultado es débil
```

**Lo que vemos.** La predicción cuenta en las cinco particiones.
En otros datos puede salir `l6_counts = False`.
Es un resultado normal y se informa con su razón.

### Paso 5. ¿De dónde sale la señal?
En este paso probamos dos variantes: solo `n_authors`, y todo menos `n_authors`.
Así vemos qué atributo lleva la señal.

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
    numbers_only = []  # aquí guardamos las columnas de números pedidas
    for c in NUMBER_COLUMNS:  # recorremos las columnas de números
        if c in columns:  # la columna está entre las pedidas
            numbers_only.append(c)  # append la guarda
    categories_only = []  # aquí guardamos las columnas de categorías pedidas
    for c in CATEGORY_COLUMNS:  # recorremos las columnas de categorías
        if c in columns:  # la columna está entre las pedidas
            categories_only.append(c)  # append la guarda
    steps = [("num", make_pipeline(SimpleImputer(strategy="median", add_indicator=True), StandardScaler()), numbers_only)]  # la preparación de los números
    if categories_only:  # hay columnas de categorías
        steps.append(("cat", make_pipeline(SimpleImputer(strategy="most_frequent"), OneHotEncoder(handle_unknown="ignore")), categories_only))  # append suma la preparación de las categorías
    accuracies = []  # aquí guardamos la exactitud de cada método
    for m in (lr, forest, network):  # recorremos los tres métodos
        pipeline = make_pipeline(ColumnTransformer(steps), clone(m))  # make_pipeline une esta preparación con una copia sin entrenar
        pipeline.fit(train, y_train)  # fit entrena la copia con las filas de entrenamiento
        accuracies.append(round(accuracy_score(y_test, pipeline.predict(test)), 2))  # accuracy_score mide la exactitud en las filas apartadas
    return accuracies  # devolvemos las tres exactitudes


without_authors = []  # aquí guardamos todas las columnas menos n_authors
for c in NUMBER_COLUMNS + CATEGORY_COLUMNS:  # recorremos todas las columnas de entrada
    if c != "n_authors":  # dejamos fuera n_authors
        without_authors.append(c)  # append guarda la columna
print(f"Clase mayoritaria {majority:.2f}")  # print muestra la línea base
print("Solo n_authors:     ", heldout_accuracy(["n_authors"]))  # heldout_accuracy mide los tres métodos solo con n_authors
print("Todo menos n_authors:", heldout_accuracy(without_authors))  # heldout_accuracy mide los tres métodos sin n_authors
print(f"Regla n_authors >= 4 en las {len(labelled)} filas con etiqueta: {((attributes.loc[labelled.index, 'n_authors'] >= 4).astype(int) == y).mean():.2f}")  # print muestra la regla en todas las filas con etiqueta
```

### Paso 6. La regla y los modelos en las cinco particiones
En este paso repetimos la comparación en las cinco particiones de `SPLIT_SEEDS`.
La última columna es el umbral que más acierta en las filas de entrenamiento.

```python
without = ColumnTransformer([("num", make_pipeline(SimpleImputer(strategy="median", add_indicator=True), StandardScaler()), ["year", "is_oa"]), ("cat", make_pipeline(SimpleImputer(strategy="most_frequent"), OneHotEncoder(handle_unknown="ignore")), CATEGORY_COLUMNS)])  # la preparación sin n_authors
by_seed = []  # aquí guardamos una fila por semilla
for s in SPLIT_SEEDS:  # recorremos las cinco semillas de partición
    tr, te = train_test_split(labelled, test_size=n_flagged(len(labelled)), stratify=y, random_state=s)  # train_test_split arma la partición
    y_tr, y_te = y.loc[tr.index], y.loc[te.index]  # loc toma la etiqueta de cada parte
    authors_tr, authors_te = attributes.loc[tr.index, "n_authors"], attributes.loc[te.index, "n_authors"]  # loc toma el número de autores de cada parte
    row = {"semilla": s, "clase mayoritaria": y_te.value_counts(normalize=True).max(), "regla": ((authors_te >= 4).astype(int) == y_te).mean()}  # la semilla, la línea base y la regla
    for name, m in zip(["regresión", "bosque", "red"], (lr, forest, network)):  # recorremos los tres métodos
        row[name] = accuracy_score(y_te, make_pipeline(clone(prepare), clone(m)).fit(tr, y_tr).predict(te))  # exactitud con todas las columnas
        row[f"{name} sin n_authors"] = accuracy_score(y_te, make_pipeline(clone(without), clone(m)).fit(tr, y_tr).predict(te))  # exactitud sin n_authors
    best_threshold = 1  # empezamos con el umbral de 1 autor
    best_accuracy = -1.0  # todavía no medimos ningún umbral
    for t in range(1, 21):  # probamos de 1 a 20 autores
        accuracy = ((authors_tr >= t).astype(int) == y_tr).mean()  # mean da la parte de aciertos de ese umbral
        if accuracy > best_accuracy:  # este umbral acierta más
            best_threshold, best_accuracy = t, accuracy  # nos quedamos con este umbral
    row["mejor umbral"] = best_threshold  # guardamos el umbral que más acierta
    by_seed.append(row)  # append guarda la fila de esta semilla
by_seed = pd.DataFrame(by_seed).set_index("semilla")  # DataFrame arma la tabla, una fila por semilla
print(by_seed.round(3).to_string())  # print muestra la tabla
```

**Lo que vemos.** La regla gana en las semillas 7 y 8.
En la 9 y la 10 gana la red, y en la 11 el bosque empata.
Sin `n_authors` los modelos siguen sobre la clase mayoritaria.
El mejor umbral es 4 en las cinco.

**Lo que encontramos.** La señal es el número de autores.
Más autores quiere decir más instituciones, y más países.
Tres modelos no le ganan con claridad a una regla de una línea.
El resultado es real pero modesto, y se dice así.

**Tres errores para leer.** La celda muestra tres artículos donde el bosque se equivoca.
Un error puede ser del modelo o de la etiqueta.

```python
said_rf = pd.Series(pred_rf, index=test.index)  # Series pone lo que dijo el bosque junto a cada título
wrong = test.index[said_rf != y_test][:3]  # tomamos los tres primeros errores
for t in wrong:  # recorremos cada error
    print(f"{t[:80]}  autores {attributes.loc[t, 'n_authors']:.0f}, países {attributes.loc[t, 'n_countries']}, el bosque dijo {said_rf[t]}")  # print muestra autores, países y lo que dijo el bosque
```

### Paso 7. Qué pasa si se cuela la etiqueta
En este paso vemos una fuga con los artículos de nutrición, no con una tabla de juguete.

La etiqueta `internacional` sale de `n_countries`: vale 1 si hay dos o más países.
En el Paso 2 de la Parte 2 no usamos `n_countries` como atributo, precisamente por eso.
Ahora la añadimos a propósito.
Entrenamos otro bosque (el de la Parte 4 no cambia) y comparamos la exactitud en las mismas filas apartadas.

```python
train_leaked = train.copy()  # copy deja el entrenamiento original sin cambios
test_leaked = test.copy()  # copy deja las filas apartadas originales sin cambios
train_leaked["n_countries"] = attributes.loc[train.index, "n_countries"]  # loc trae el número de países, del que sale la etiqueta
test_leaked["n_countries"] = attributes.loc[test.index, "n_countries"]  # loc trae el mismo dato en las filas apartadas
NUMBER_COLUMNS_LEAKED = ["year", "n_authors", "is_oa", "n_countries"]  # las columnas de números, ahora con la fuga
numbers_leaked = make_pipeline(SimpleImputer(strategy="median", add_indicator=True), StandardScaler())  # la misma preparación de números que en la Parte 3
categories_leaked = make_pipeline(SimpleImputer(strategy="most_frequent"), OneHotEncoder(handle_unknown="ignore"))  # la misma preparación de categorías
prepare_leaked = ColumnTransformer([("num", numbers_leaked, NUMBER_COLUMNS_LEAKED), ("cat", categories_leaked, CATEGORY_COLUMNS)])  # ColumnTransformer aplica cada preparación a sus columnas
forest_leaked = make_pipeline(prepare_leaked, RandomForestClassifier(n_estimators=N_TREES, min_samples_leaf=3, random_state=SEED))  # make_pipeline pone la preparación antes de un bosque nuevo
forest_leaked.fit(train_leaked, y_train)  # fit entrena ese bosque con la columna que se cuela
pred_rf_leaked = forest_leaked.predict(test_leaked)  # predict responde en las mismas filas apartadas
leak_rows = {}  # aquí guardamos la exactitud de cada fila
leak_rows["clase mayoritaria"] = {"exactitud": round(accuracy_score(y_test, pred_majority), 3)}  # accuracy_score mide la clase mayoritaria
leak_rows["bosque"] = {"exactitud": round(accuracy_score(y_test, pred_rf), 3)}  # el bosque de la Parte 4, sin n_countries
leak_rows["bosque con n_countries"] = {"exactitud": round(accuracy_score(y_test, pred_rf_leaked), 3)}  # el bosque nuevo, con la fuga
leak_compare = pd.DataFrame(leak_rows).T  # DataFrame arma la tabla y T deja un método por fila
print(leak_compare)  # print muestra las tres exactitudes
importance_leaked = pd.Series(forest_leaked[-1].feature_importances_, index=forest_leaked[0].get_feature_names_out())  # el último paso es el bosque y el primero la preparación
print(importance_leaked.nlargest(5).round(3))  # nlargest muestra las 5 columnas más importantes
```

**Lo que vemos.** Los números salen de la celda de arriba.
La clase mayoritaria acierta 0,518 de las filas apartadas.
El bosque de la Parte 4 acierta 0,714.
Si añadimos `n_countries`, el bosque acierta 1,000: todas las filas apartadas.
La columna que más usa es `num__n_countries` (0,745), por encima de `n_authors` (0,144).
Eso no es un atributo independiente: es el dato del que sale la etiqueta.
En otros datos una fuga puede ser más disimulada, por ejemplo una categoría casi igual a la etiqueta.

**Comprobar:**

Comprobamos que las tablas originales no tienen `n_countries` y que, con esa columna, el bosque acierta más y deja las apartadas perfectas.

```python
assert "n_countries" not in train.columns and "n_countries" not in test.columns  # las tablas originales no tienen la fuga
assert accuracy_score(y_test, pred_rf_leaked) > accuracy_score(y_test, pred_rf)  # con la fuga el bosque acierta más
assert accuracy_score(y_test, pred_rf_leaked) == 1  # con n_countries el bosque acierta todas las apartadas
print("Fuga con n_countries: OK")  # print confirma la comprobación
```

---

## Parte 6. Despliegue

### Paso 1. El resultado de la predicción
En este paso definimos el resultado de la predicción.
Es positivo si **al menos 2 de los 3 métodos** dicen que sí.
Cada artículo lo puntúa un modelo que no vio su etiqueta.
Los artículos sin etiqueta no reciben este resultado.

```python
folds = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)  # StratifiedKFold arma los cinco pliegues
models = []  # aquí guardamos los tres métodos con su preparación
for m in (lr, forest, network):  # recorremos los tres métodos
    models.append(make_pipeline(prepare, m))  # make_pipeline pone la preparación antes del método

train_votes = 0  # aquí sumamos los votos en las filas de entrenamiento
for m in models:  # recorremos los tres métodos
    train_votes = train_votes + cross_val_predict(m, train, y_train, cv=folds)  # fuera del pliegue, cada fila la predice un modelo que no la vio
test_votes = 0  # aquí sumamos los votos en las filas apartadas
for m in models:  # recorremos los tres métodos
    test_votes = test_votes + m.fit(train, y_train).predict(test)  # en las apartadas responde el modelo entrenado sin ellas
voted = pd.concat([train.assign(votes=train_votes), test.assign(votes=test_votes)])["votes"]  # concat junta los votos, con el título como índice, como table
table["prediction"] = (voted >= 2).reindex(table.index, fill_value=False)  # 2 de 3 de acuerdo. Las filas sin etiqueta quedan en False

majority = max(np.mean(y_test), 1 - np.mean(y_test))  # la parte de la clase mayoritaria en las filas apartadas
l6_counts = True  # empezamos suponiendo que cuenta
for m in models:  # recorremos los tres métodos
    if np.mean(m.predict(test) == y_test) <= majority + MARGIN:  # no supera a la clase mayoritaria por más de MARGIN
        l6_counts = False  # con un método que no la supera, la predicción no cuenta
print(f"Predichos positivos: {table['prediction'].sum()} de {len(labelled)} con etiqueta. l6_counts = {l6_counts}")  # print muestra el resultado
```

**Comprobar:**

Comprobamos que solo los artículos con etiqueta reciben el resultado y que los votos cuadran.

```python
assert not table.loc[~table.index.isin(labelled.index), "prediction"].any()  # los artículos sin etiqueta quedan en False
assert table.loc[labelled.index, "prediction"].sum() == (train_votes >= 2).sum() + (test_votes >= 2).sum()  # los positivos son los de al menos 2 votos
print("Resultado de la predicción sin filas vistas: OK")  # print confirma la comprobación
```

### Paso 2. La lista de esta lección
La predicción dice si el artículo es internacional.
Eso no es, por sí solo, una razón para leer.
Si los tres métodos superan a la clase mayoritaria, la lista guarda como máximo 30 artículos con predicción positiva, los que recibieron más votos.
Si no la superan, la lista queda vacía y lo decimos.

```python
if l6_counts:  # la predicción cuenta
    chosen = table.index[table["prediction"]]  # los artículos con predicción positiva
else:  # la predicción no cuenta
    chosen = []  # la lista queda vacía
    print("Los tres métodos no superan a la clase mayoritaria. La predicción no arma lista.")  # print lo dice
reading = table.loc[chosen, ["prediction"]].copy()  # copy toma las filas elegidas
reading["votos"] = voted.reindex(reading.index)  # reindex trae los votos de cada artículo
reading = reading.reset_index().sort_values(["votos", "title"], ascending=[False, True])  # sort_values ordena por votos y después por título
reading_list = reading.head(MAX_PAPERS)  # head se queda con los MAX_PAPERS primeros
print(f"Predichos positivos: {len(reading)}. En la lista: {len(reading_list)}.")  # print muestra los dos conteos
```

**Comprobar:**

Comprobamos que la lista no pasa de 30 y que cada fila tiene predicción positiva.

```python
assert len(reading_list) == min(MAX_PAPERS, len(reading))  # la lista no pasa de 30
assert reading_list.empty or reading_list["prediction"].all()  # cada fila tiene predicción positiva
print("Lista de la predicción: OK")  # print confirma la comprobación
```

### Paso 3. Guardar la predicción y la lista
En este paso guardamos `outputs/prediccion_l6.csv` y `outputs/lectura_l6.csv`.
`votos` es cuántos métodos dijeron internacional.

```python
prediction_table = pd.DataFrame({  # DataFrame arma la tabla de la predicción, una fila por título
    "title": titles,  # el título
    "etiqueta": y.reindex(titles).astype("Int64").to_numpy(),  # la etiqueta, vacía sin afiliación
    "apartada": table.index.isin(test.index),  # si la fila estaba apartada
    "votos": voted.reindex(titles).astype("Int64").to_numpy(),  # cuántos métodos dijeron internacional
    "prediction": table.loc[titles, "prediction"].to_numpy(),  # el resultado de la predicción
})
prediction_path = OUTPUTS_DIR / "prediccion_l6.csv"  # Path fija la ruta de la predicción
prediction_table.to_csv(prediction_path, index=False)  # to_csv escribe la tabla y deja fuera el índice
reading_path = OUTPUTS_DIR / "lectura_l6.csv"  # Path fija la ruta de la lista
reading_list.to_csv(reading_path, index=False)  # to_csv escribe la lista y deja fuera el índice
print(f"Guardado: {prediction_path} ({len(prediction_table)} filas) y {reading_path} ({len(reading_list)} filas)")  # print confirma dónde quedaron
```

### Paso 4. Qué cambiaría la decisión
En este paso escribimos cómo entra la predicción y qué la cambiaría.

| Qué | Respuesta |
|-----|-----------|
| Cómo entra | Entra en la lista si al menos 2 de los 3 métodos dicen que sí, con un modelo que no vio la etiqueta, y solo si los tres superan a la clase mayoritaria |
| Cómo se lee | La señal es el número de autores. Tres modelos no le ganan con claridad a contar autores. Con otras semillas la ventaja cambia |
| Qué lo cambia | Otra etiqueta. Otra partición de los datos. Los artículos sin afiliación. Otro margen que 0,02 |

**Lo que vemos.** La lista nombra artículos que los modelos marcan como internacionales.
Ser internacional no es, por sí solo, una razón para leer.

### Paso 5. Comprobación final
En este paso revisamos que el cuaderno guardó la predicción, la lista y las figuras.

```python
def _check_ok(name, check):
    """Ejecuta una comprobación sin detener el cuaderno: un error cuenta como incompleto.

    Salida:
        True si la comprobación pasó, False si no.
    """
    try:  # intentamos la comprobación
        ok = bool(check())  # check devuelve True si pasó
    except Exception:  # cualquier error cuenta como incompleto
        ok = False  # la comprobación no pasó
    print(f"{name}: {'OK' if ok else 'incompleto'}")  # print muestra el resultado
    return ok  # devolvemos si pasó


def prediction_saved():
    """Dice si el archivo de la predicción quedó guardado."""
    return prediction_path.is_file()  # is_file dice si el archivo existe


def reading_saved():
    """Dice si el archivo de la lista quedó guardado."""
    return reading_path.is_file()  # is_file dice si el archivo existe


def confusion_saved():
    """Dice si las tres matrices de confusión quedaron guardadas."""
    for name in ["confusion_regresion.png", "confusion_bosque.png", "confusion_red.png"]:  # recorremos las tres figuras
        if not (OUTPUTS_DIR / name).is_file():  # is_file dice si la figura existe
            return False  # falta una figura
    return True  # están las tres


checks = [  # cada comprobación tiene un nombre y una función
    ("outputs/prediccion_l6.csv", prediction_saved),  # el archivo de la predicción
    ("outputs/lectura_l6.csv", reading_saved),  # el archivo de la lista
    ("Matrices de confusión", confusion_saved),  # las tres figuras
]
passed = 0  # aquí contamos las comprobaciones que pasan
for name, check in checks:  # recorremos cada comprobación
    passed += _check_ok(name, check)  # _check_ok suma 1 si pasó
print(f"\nL6_CHECKS={passed}/{len(checks)}")  # print muestra cuántas pasaron
if passed == len(checks):  # pasaron todas
    print("L6_OK. Siga con la Lección 7.")  # print confirma el cuaderno
```

<!-- end NOTEBOOK: -->
