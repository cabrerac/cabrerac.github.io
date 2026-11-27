<!-- NOTEBOOK: -->

## Repaso de Python para este cuaderno

Este cuaderno utiliza los siguientes métodos de Python. Si ya los conoce, ejecute estas celdas rápido.
Un modelo aprende con `fit` en unas filas.
Después responde con `predict` en otras filas que no vio.

### Aprender en unas filas, responder en otras

```python
import numpy as np  # numpy arma los arreglos del ejemplo
from sklearn.model_selection import train_test_split  # train_test_split separa las filas en dos partes
from sklearn.linear_model import LogisticRegression  # LogisticRegression es la regresión logística

x_toy = np.array([[1], [2], [3], [4], [5], [6], [7], [8]])  # np.array arma un atributo con ocho filas
y_toy = np.array([0, 0, 0, 0, 1, 1, 1, 1])  # np.array arma la etiqueta de cada fila
x_tr, x_te, y_tr, y_te = train_test_split(x_toy, y_toy, test_size=4, stratify=y_toy, random_state=7)  # train_test_split aparta 4 filas con la misma proporción de cada clase
toy_model = LogisticRegression(random_state=7).fit(x_tr, y_tr)  # fit hace que la regresión aprenda con las otras 4 filas
said = toy_model.predict(x_te)  # predict responde en las filas apartadas
assert len(said) == len(y_te)  # una respuesta por fila apartada
print(f"Dijo {said.tolist()}, era {y_te.tolist()}. Aciertos: {int((said == y_te).sum())} de {len(y_te)}. Repaso de Python: OK")  # print compara lo dicho con la etiqueta
```

**Lo que vemos.** La regresión aprendió con cuatro filas y acertó las otras cuatro.
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

La etiqueta es la de la Lección 4: el artículo trata del tema del colega, según los temas que OpenAlex le asignó.
Suponemos que un artículo del tema **se debe leer**.
Los dos métodos leen solo el resumen.

Medimos aciertos y errores en artículos que ningún modelo vio.
Cada método se compara con la **clase mayoritaria** y con una regla de una línea, sin modelo.

**Dos métodos, la misma preparación.**

| Método | Pregunta | Preparación que necesita |
|--------|----------|--------------------------|
| Regresión logística | ¿Qué palabras del resumen pesan a favor y en contra? | Los pesos TF-IDF de la Lección 4, aprendidos solo con las filas de entrenamiento |
| Una capa oculta | ¿Qué combinación de palabras separa las clases? | Los mismos pesos TF-IDF. La capa de salida es una regresión logística |

**Qué hacer.** Ejecute las celdas de arriba hacia abajo.
Cada paso empieza con **En este paso**. Si tiene código, termina con una celda **Comprobar**.

**Mapa del cuaderno**

| Parte | Fase CRISP-DM | Qué sale |
|-------|---------------|----------|
| 1 | Comprensión del negocio | La pregunta de hoy y los parámetros |
| 2 | Comprensión de los datos | La etiqueta y los resúmenes |
| 3 | Preparación de los datos | El conjunto apartado y los pesos TF-IDF |
| 4 | Modelado | Clase mayoritaria, regresión logística y una capa oculta |
| 5 | Evaluación | Aciertos y errores contra la clase mayoritaria y la regla de una línea, la comparación de los dos métodos, y una fuga de la etiqueta |
| 6 | Despliegue | La predicción en `outputs/prediccion_l6.csv` y hasta 30 artículos en `outputs/lectura_l6.csv` |

**Carpetas.** La celda de configuración crea `data/` (datos descargados) y `outputs/` (tablas y gráficos).

---

## Parte 1. Comprensión del negocio

### Paso 1. La pregunta de esta lección
En este paso escribimos qué buscamos hoy.
La decisión no cambia: qué artículos debe leer el colega nuevo.

| Pregunta | Respuesta para el laboratorio |
|----------|-------------------------------|
| ¿Qué buscamos? | Predecir, desde el resumen, si un artículo se debe leer |
| ¿Qué suponemos? | Que un artículo del tema del colega se debe leer. La etiqueta del tema viene de OpenAlex |
| ¿Con qué lo medimos? | La regresión logística de la Lección 4 y una red con una capa oculta |
| ¿Contra qué los comparamos? | Contra la clase mayoritaria, contra una regla de una línea y entre ellos |
| ¿Cómo entra la predicción en la lista? | Un artículo entra si los dos métodos dicen que se lee, con un modelo que no vio su etiqueta, y los dos métodos superan a la clase mayoritaria. La lista guarda como máximo 30 |

La suposición es parte del resultado.
Si el equipo cambia lo que quiere decir "se debe leer", cambia la etiqueta y cambian los aciertos.

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
from sklearn.dummy import DummyClassifier  # DummyClassifier dice siempre la clase mayoritaria
from sklearn.feature_extraction.text import TfidfVectorizer  # TfidfVectorizer convierte cada resumen en pesos de palabras
from sklearn.linear_model import LogisticRegression  # LogisticRegression es la regresión logística
from sklearn.metrics import ConfusionMatrixDisplay, accuracy_score, confusion_matrix  # medidas de aciertos y errores
from sklearn.model_selection import StratifiedKFold, cross_val_predict, train_test_split  # particiones y pliegues
from sklearn.neural_network import MLPClassifier  # MLPClassifier es la red con una capa oculta
from sklearn.pipeline import make_pipeline  # make_pipeline encadena la preparación y el modelo

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
N_FOLDS = 5  # en cuántas partes partimos los artículos para dar una probabilidad a cada uno
TARGET_TOPICS = ["obesity", "diet", "nutrition", "nutritional",  # las palabras del peso, la comida y la nutrición
                 "diabetes", "cardiovascular", "lipoproteins", "blood pressure", "hypertension"]  # las palabras de las enfermedades

# L6
HIDDEN_UNITS = 8  # igual que la diapositiva de la red
PENALTY = 1.0  # pocas filas, así que una penalización más fuerte que la de la diapositiva (1e-4)
MARGIN = 0.02  # cuánto sobre la clase mayoritaria debe quedar cada método para que la L6 cuente
SPLIT_SEEDS = (7, 8, 9, 10, 11)  # otras particiones, para ver si el resultado se sostiene


def n_flagged(n: int) -> int:
    """Devuelve el tamaño del conjunto apartado, con la regla de la L4.

    Aparta el 20% de las filas, redondeado hacia arriba, y nunca menos de FLAGGED_MIN.

    Args:
        n: el número de filas con etiqueta.

    Returns:
        El número entero de filas que se apartan.
    """
    return max(FLAGGED_MIN, math.ceil(FLAGGED_SHARE * n))  # max nunca baja de FLAGGED_MIN, y ceil redondea el 20% hacia arriba


def min_positives(n: int) -> int:
    """Devuelve cuántas filas necesita la clase minoritaria, con la regla de la L4.

    Pide el 10% de las filas, redondeado hacia arriba, y nunca menos de POSITIVES_MIN.
    Con menos, un modelo aprende casi nada de esa clase.

    Args:
        n: el número de filas con etiqueta.

    Returns:
        El número entero mínimo de filas de la clase minoritaria.
    """
    return max(POSITIVES_MIN, math.ceil(POSITIVE_SHARE * n))  # max nunca baja de POSITIVES_MIN, y ceil redondea el 10% hacia arriba


def new_tfidf() -> TfidfVectorizer:
    """Devuelve una preparación TF-IDF sin entrenar.

    Deja fuera las palabras vacías del inglés y las palabras de un solo resumen.
    El peso de una palabra crece con 1 + log(conteo).

    Returns:
        Un TfidfVectorizer que aprende con fit y se aplica con transform.
    """
    return TfidfVectorizer(stop_words="english", sublinear_tf=True, min_df=2)  # TfidfVectorizer con las mismas opciones en todo el cuaderno


print(f"Una capa oculta de {HIDDEN_UNITS} unidades con penalización {PENALTY}. Margen {MARGIN}")  # print muestra los parámetros de hoy
```

### Paso 3. Descargar los artículos
En este paso descargamos los artículos y quitamos los títulos repetidos, como en la Lección 5.

```python
def download_data(name: str, folder: Path = DATA_DIR) -> Path:
    """Descarga un archivo de datos del curso, una sola vez.

    Si el archivo ya está en la carpeta, lo usa.
    Si no, lo baja de BASE_URL.

    Args:
        name: nombre del archivo.
        folder: carpeta local, DATA_DIR por defecto.

    Returns:
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
titles = list(papers["title"])  # list guarda los títulos en orden
print(f"{len(raw)} filas, {N} sin títulos repetidos, como en la L5")  # print muestra los dos tamaños
```

**Comprobar:**

Comprobamos que hay un título por artículo y que están el resumen y los temas.

```python
assert papers["title"].is_unique and {"abstract", "topics"} <= set(papers.columns)  # títulos sin repetir y las dos columnas que usamos
print("Artículos: OK")  # print confirma la comprobación
```

### Paso 4. La pregunta
La pregunta es la de la Lección 1.
El equipo decide qué artículos de nutrición leer, y qué filtro los puso en la lista.
La lista tiene entre 10 y 30 artículos.

```python
MIN_PAPERS = 10  # la lista tiene al menos 10 artículos
MAX_PAPERS = 30  # la lista tiene como máximo 30 artículos
print(f"Lista: entre {MIN_PAPERS} y {MAX_PAPERS} artículos")  # print muestra el tamaño de la lista
```

---

## Parte 2. Comprensión de los datos

### Paso 1. La etiqueta: se debe leer
En este paso construimos la etiqueta, como en la Lección 4.
Escribimos 1 cuando uno de los temas de OpenAlex menciona una palabra de `TARGET_TOPICS`.
Los editores de OpenAlex asignaron esos temas antes de este cuaderno.
Por eso la etiqueta viene dada, y no la encontró un método nuestro.

```python
y = []  # aquí guardamos la etiqueta de cada artículo
for topics in papers["topics"]:  # recorremos los temas de OpenAlex de cada artículo
    found = 0  # empezamos suponiendo que no es del tema
    for topic in TARGET_TOPICS:  # recorremos cada palabra de la etiqueta
        if topic in topics.lower():  # in busca esa palabra dentro del texto de los temas
            found = 1  # el tema de OpenAlex trae la palabra
    y.append(found)  # append guarda la etiqueta de este artículo
y = pd.Series(y, index=titles, name="leer")  # Series pone la etiqueta junto a cada título
print(f"Se deben leer: {y.sum()} de {N} ({y.mean():.0%})")  # print muestra cuántos son del tema
```

**Comprobar:**

Comprobamos que hay una etiqueta por artículo y que la clase minoritaria tiene suficientes filas.

```python
assert len(y) == N and set(y.unique()) <= {0, 1}  # una etiqueta por artículo, con 0 o 1
assert min(y.sum(), N - y.sum()) >= min_positives(N)  # la clase minoritaria llega al mínimo
print(f"Clase minoritaria con al menos {min_positives(N)} filas: OK")  # print confirma la comprobación
```

**Lo que vemos.** De los 318 artículos, 98 (31%) son del tema.
La clase mayoritaria dice que ninguno se lee, y acierta cerca de 0,69.

### Paso 2. Los resúmenes
En este paso miramos la única entrada de los dos métodos: el resumen.
Los temas de OpenAlex no entran, porque de ellos sale la etiqueta.

```python
texts = pd.Series(papers["abstract"].to_numpy(), index=titles, name="abstract")  # Series pone el resumen junto a cada título
n_words = texts.str.split().str.len()  # split separa por espacios y len cuenta los trozos
print(f"Palabras por resumen. Mediana: {n_words.median():.0f}. Mínimo: {n_words.min()}. Máximo: {n_words.max()}")  # print resume el largo
print(texts.iloc[0][:300])  # mostramos el comienzo del primer resumen
```

**Lo que vemos.** La mediana es de 244 palabras.
Algunos resúmenes son muy cortos, y de esos el método tiene poco que leer.

---

## Parte 3. Preparación de los datos

### Paso 1. El conjunto apartado
En este paso apartamos `n_flagged(N)` filas, con la misma proporción de cada clase.
Ningún modelo las ve al aprender.

```python
train, test = train_test_split(texts, test_size=n_flagged(N), stratify=y, random_state=SEED)  # train_test_split aparta n_flagged filas con la misma proporción de cada clase
y_train, y_test = y.loc[train.index], y.loc[test.index]  # loc toma la etiqueta de cada parte
print(f"Para aprender: {len(train)}. Apartadas: {len(test)}, {y_test.sum()} del tema")  # print muestra los dos tamaños
```

**Comprobar:**

Comprobamos el tamaño del conjunto apartado, que no comparte filas y que las dos partes tienen proporciones parecidas.

```python
assert len(test) == n_flagged(N) and not set(train.index) & set(test.index)  # tamaño correcto y sin filas compartidas
assert abs(y_train.mean() - y_test.mean()) < 0.05  # proporciones parecidas en las dos partes
print("Conjunto apartado: OK")  # print confirma la comprobación
```

### Paso 2. Los pesos TF-IDF
En este paso convertimos cada resumen en una fila de pesos, como en la Lección 4.
El peso sube cuando la palabra se repite en el resumen y baja cuando aparece en muchos resúmenes.
Los pesos se aprenden **solo con las filas de entrenamiento**.
Cada fila queda de largo 1, así que la red no necesita otro escalado.

```python
tfidf = new_tfidf()  # new_tfidf prepara TF-IDF sin entrenar
X_train = tfidf.fit_transform(train)  # fit_transform aprende el vocabulario y los pesos con las filas de entrenamiento
X_test = tfidf.transform(test)  # transform los aplica a las filas apartadas y nunca vuelve a aprender
feature_names = tfidf.get_feature_names_out()  # get_feature_names_out da la palabra de cada columna
print(f"Entrenamiento: {X_train.shape}. Apartadas: {X_test.shape}")  # print muestra las dos formas
```

**Comprobar:**

Comprobamos que las dos tablas tienen las mismas columnas y que cada fila de entrenamiento quedó de largo 1.

```python
assert X_train.shape == (len(train), len(feature_names)) and X_test.shape[1] == len(feature_names)  # las dos tablas tienen las mismas columnas
assert np.allclose(np.sqrt(X_train.multiply(X_train).sum(axis=1)), 1)  # cada fila tiene largo 1
print("TF-IDF: OK")  # print confirma la comprobación
```

**Lo que vemos.** Cada resumen se vuelve una fila de 3624 pesos, una por palabra.

---

## Parte 4. Modelado

### La clase mayoritaria
En este paso construimos la línea base.
Decimos siempre la clase más común, aquí no leer.

```python
baseline = DummyClassifier(strategy="most_frequent").fit(X_train, y_train)  # DummyClassifier aprende cuál es la clase más común
pred_majority = baseline.predict(X_test)  # predict dice esa clase en todas las filas apartadas
majority = max(np.mean(y_test), 1 - np.mean(y_test))  # la parte de la clase mayoritaria en las filas apartadas
print(f"La clase mayoritaria acierta {accuracy_score(y_test, pred_majority):.2f} de las apartadas")  # accuracy_score cuenta la parte de aciertos
```

### Regresión logística
En este paso usamos la regresión logística de la Lección 4.
Un peso positivo empuja hacia leer.
`class_weight="balanced"` da el mismo peso a las dos clases.

```python
lr = LogisticRegression(class_weight="balanced", C=C_REG, max_iter=1000)  # LogisticRegression prepara la regresión con clases balanceadas
lr.fit(X_train, y_train)  # fit aprende un peso por palabra
pred_lr = lr.predict(X_test)  # predict responde en las filas apartadas

weights = pd.Series(lr.coef_[0], index=feature_names).sort_values()  # coef_ guarda el peso de cada palabra y sort_values los ordena
print("Hacia leer:", weights.tail(8).round(2).to_dict())  # tail muestra los ocho pesos más altos
print("Hacia no leer:", weights.head(8).round(2).to_dict())  # head muestra los ocho pesos más bajos
```

**Lo que vemos.** Diabetes (3,81), cardiovascular (2,96) y obesity (2,68) empujan hacia leer.
Cancer (-1,93) empuja hacia no leer.
Los pesos se pueden leer palabra por palabra.

### Una capa oculta
En este paso entrenamos una red con una capa oculta de `HIDDEN_UNITS` unidades, sobre los mismos pesos TF-IDF.
`PENALTY` es la penalización L2 (`alpha`).
Es más fuerte que la de la diapositiva porque hay pocas filas.
La capa de salida es una regresión logística: combina lo que produce la capa oculta y da una probabilidad para cada clase.

```python
network = MLPClassifier(hidden_layer_sizes=(HIDDEN_UNITS,), alpha=PENALTY, max_iter=3000, random_state=SEED)  # MLPClassifier prepara la red con una capa oculta
network.fit(X_train, y_train)  # fit aprende los pesos de las dos capas
pred_nn = network.predict(X_test)  # predict responde en las filas apartadas
print(f"La red terminó en {network.n_iter_} pasos")  # n_iter_ dice cuántos pasos dio la red
```

**Lo que vemos.** La red paró en 576 pasos, lejos del máximo de 3000.
Sus pesos no se leen palabra por palabra, porque pasan por la capa oculta.

**Comprobar:**

Comprobamos que hay una predicción por fila apartada para cada método.

```python
predictions = {"clase mayoritaria": pred_majority, "regresión logística": pred_lr, "una capa oculta": pred_nn}  # las tres predicciones, con su nombre
for name in predictions:  # recorremos cada método
    assert len(predictions[name]) == len(y_test), name  # una predicción por fila apartada
print("Predicciones: OK")  # print confirma la comprobación
```

---

## Parte 5. Evaluación

### Paso 1. Aciertos y errores en las filas apartadas
En este paso contamos TP, FP, FN y TN de cada método, y su exactitud.
Al lado ponemos una regla de una línea: **se lee si el resumen menciona una palabra de `TARGET_TOPICS`**.
Es la lista de palabras clave de la Lección 4, sin modelo.

```python
def counts_of(y_true, pred):
    """Cuenta los aciertos y errores de un método sobre las filas apartadas.

    La clase positiva es leer (1).
    La exactitud es la parte de filas bien dichas.

    Args:
        y_true: las etiquetas verdaderas.
        pred: lo que dijo el método, en el mismo orden.

    Returns:
        Un diccionario con TP, FP, FN, TN y la exactitud a 3 decimales.
    """
    tn, fp, fn, tp = confusion_matrix(y_true, pred, labels=[0, 1]).ravel()  # confusion_matrix cuenta los cuatro casos y ravel los deja en fila
    return {"TP": int(tp), "FP": int(fp), "FN": int(fn), "TN": int(tn), "exactitud": round(accuracy_score(y_true, pred), 3)}  # devolvemos los conteos y la exactitud


def mentions_topic(text):
    """Devuelve 1 si el texto menciona una palabra de TARGET_TOPICS, y 0 si no."""
    for topic in TARGET_TOPICS:  # recorremos cada palabra de la lista
        if topic in text.lower():  # in busca la palabra en el texto
            return 1  # el texto la menciona
    return 0  # ninguna palabra aparece


pred_rule = test.apply(mentions_topic).to_numpy()  # apply aplica la regla a cada resumen apartado
predictions["regla de una línea"] = pred_rule  # sumamos la regla a las predicciones
rows = {}  # aquí guardamos los conteos de cada método
for name, pred in predictions.items():  # recorremos cada método
    rows[name] = counts_of(y_test, pred)  # counts_of cuenta sus aciertos y errores
results = pd.DataFrame(rows).T  # DataFrame arma la tabla y T deja un método por fila
results = results.astype({"TP": int, "FP": int, "FN": int, "TN": int})  # astype deja los conteos como enteros
results  # mostramos la tabla
```

**Comprobar:**

Comprobamos que los cuatro casos suman las filas apartadas y que los dos métodos igualan o superan a la clase mayoritaria.
Esta comprobación no decide si la predicción cuenta.
Eso se decide en el Paso 3.

```python
assert (results[["TP", "FP", "FN", "TN"]].sum(axis=1) == len(y_test)).all()  # los cuatro casos suman las filas apartadas
for name in ["regresión logística", "una capa oculta"]:  # recorremos los dos métodos
    assert results.loc[name, "exactitud"] >= majority, name  # el método iguala o supera a la clase mayoritaria
print("Los dos métodos igualan o superan a la clase mayoritaria: OK")  # print confirma la comprobación
```

**Lo que vemos.** La clase mayoritaria acierta 0,688.
La regresión logística acierta 0,922 y la red 0,844.
La regla de una línea acierta 0,828.
La regla encuentra 17 de los 20 artículos del tema, pero marca 8 que no lo son.
La red no marca ninguno de más, pero deja fuera 10 de los 20.

### Paso 2. Las matrices de confusión
En este paso dibujamos las matrices de confusión y las guardamos en `outputs/`.

```python
for name, pred, file in [("regresión logística", pred_lr, "confusion_regresion.png"), ("una capa oculta", pred_nn, "confusion_red.png")]:  # recorremos los dos métodos con su archivo
    fig, ax = plt.subplots(figsize=(3.5, 3.2))  # subplots abre la figura
    ConfusionMatrixDisplay.from_predictions(y_test, pred, labels=[0, 1], display_labels=["no leer", "leer"], cmap="Blues", colorbar=False, ax=ax)  # from_predictions dibuja la matriz de confusión
    ax.set_title(name)  # set_title pone el nombre del método
    fig.tight_layout()  # tight_layout acomoda los márgenes
    fig.savefig(OUTPUTS_DIR / file, dpi=120)  # savefig guarda la figura
    plt.show()  # show muestra la figura
```

**Lo que vemos.** Las dos matrices casi no tienen falsos positivos.
La diferencia está en los falsos negativos: la red deja fuera más artículos del tema.

### Paso 3. ¿Cuenta la predicción?
En este paso decidimos si la predicción suma un resultado.
Cuenta (`l6_counts`) solo si los dos métodos quedan más de `MARGIN` (0,02) por encima de la clase mayoritaria en las filas apartadas.
Después repetimos la comparación con las cinco particiones de `SPLIT_SEEDS`, con copias sin entrenar (`clone`).

```python
models = {"regresión logística": make_pipeline(new_tfidf(), clone(lr)), "una capa oculta": make_pipeline(new_tfidf(), clone(network))}  # cada método con su propia preparación TF-IDF
l6_counts = True  # empezamos suponiendo que cuenta
for name in ["regresión logística", "una capa oculta"]:  # recorremos los dos métodos
    if results.loc[name, "exactitud"] <= majority + MARGIN:  # no supera a la clase mayoritaria por más de MARGIN
        l6_counts = False  # con un método que no la supera, la predicción no cuenta

by_seed = []  # aquí guardamos una fila por semilla
for s in SPLIT_SEEDS:  # recorremos las cinco semillas de partición
    tr, te = train_test_split(texts, test_size=n_flagged(N), stratify=y, random_state=s)  # train_test_split arma otra partición
    row = {"semilla": s, "clase mayoritaria": y.loc[te.index].value_counts(normalize=True).max(), "regla": (te.apply(mentions_topic) == y.loc[te.index]).mean()}  # la semilla, la línea base y la regla
    for name, m in models.items():  # recorremos los dos métodos
        row[name] = accuracy_score(y.loc[te.index], clone(m).fit(tr, y.loc[tr.index]).predict(te))  # clone copia el método sin entrenar, fit lo entrena y predict responde
    row["se sostiene"] = min(row["regresión logística"], row["una capa oculta"]) > row["clase mayoritaria"] + MARGIN  # los dos superan la línea base por más de MARGIN
    by_seed.append(row)  # append guarda la fila de esta semilla
by_seed = pd.DataFrame(by_seed).set_index("semilla")  # DataFrame arma la tabla, una fila por semilla
print(f"l6_counts = {l6_counts}. Se sostiene en {by_seed['se sostiene'].sum()} de {len(SPLIT_SEEDS)} particiones")  # print muestra el resultado
if not by_seed["se sostiene"].all():  # no se sostiene en todas
    print("Con otra partición de los datos este resultado cambia: léalo como débil.")  # print avisa que el resultado es débil
by_seed.round(3)  # mostramos la tabla
```

**Lo que vemos.** La predicción cuenta en las cinco particiones.
En promedio, la regresión logística acierta 0,878, la red 0,822 y la regla 0,806.
La regresión le gana a la red en las cinco.
La regla le gana a la red en las semillas 10 y 11, y a la regresión en la 11.
Con estos 318 artículos, el método más grande no es el que más acierta.

### Paso 4. Los mismos artículos
En este paso miramos los artículos apartados donde los dos métodos coinciden y donde no.

```python
said = pd.DataFrame({"regresión": pred_lr, "red": pred_nn, "etiqueta": y_test.to_numpy()}, index=test.index)  # DataFrame pone lo que dijo cada método junto a la etiqueta
rows = []  # aquí guardamos una fila por combinación de respuestas
for lr_said in (0, 1):  # recorremos lo que puede decir la regresión
    for nn_said in (0, 1):  # recorremos lo que puede decir la red
        group = said[(said["regresión"] == lr_said) & (said["red"] == nn_said)]  # los artículos con esta combinación
        rows.append({"regresión": "leer" if lr_said else "no leer", "red": "leer" if nn_said else "no leer", "artículos": len(group), "del tema": int(group["etiqueta"].sum())})  # append guarda el conteo y cuántos son del tema
agreement = pd.DataFrame(rows)  # DataFrame arma las cuatro combinaciones, incluida la que está en cero
print(agreement.to_string(index=False))  # print muestra la tabla sin el índice
only_lr = said[(said["regresión"] == 1) & (said["red"] == 0)]  # los artículos que solo la regresión manda a leer
print(f"Solo la regresión dice leer: {len(only_lr)}, y {only_lr['etiqueta'].sum()} son del tema")  # print cuenta los aciertos de ese grupo
for t in only_lr.index[:3]:  # recorremos hasta tres de esos artículos
    print("  ", t[:90])  # print muestra el comienzo del título
```

**Lo que vemos.** Los dos dicen no leer en 47 artículos, y 4 de ellos sí son del tema.
Los dos dicen leer en 10, y los 10 son del tema.
La red nunca dice leer cuando la regresión dice que no, así que esa fila queda en 0.
La regresión suma 7 artículos más, y 6 de ellos son del tema.
Por eso la regresión encuentra más artículos del tema.

### Paso 5. Una fuga de la etiqueta
Una fuga es una entrada que ya contiene la etiqueta.
En este cuaderno la etiqueta se arma buscando palabras en los temas de OpenAlex.
Si un método lee esos temas, lee la respuesta y no el resumen.
Esta vez la entrada son solo los temas, en las mismas filas.
La exactitud con el resumen queda al lado, para ver el salto.

```python
topics_text = pd.Series(papers["topics"].to_numpy(), index=titles)  # Series pone los temas junto a cada título
example = y_test[y_test == 1].index[0]  # el primer artículo apartado que sí es del tema
found = [topic for topic in TARGET_TOPICS if topic in topics_text[example].lower()]  # las palabras de la etiqueta que ya están en los temas
print(example[:90])  # print muestra el título
print(f"Los temas ya traen: {found}")  # print muestra la palabra que decide la etiqueta
print(topics_text[example][:180])  # print muestra el comienzo de los temas
for name, m in models.items():  # recorremos los dos métodos
    leaked = clone(m).fit(topics_text.loc[train.index], y_train)  # fit aprende con los temas de las filas de entrenamiento
    got = accuracy_score(y_test, leaked.predict(topics_text.loc[test.index]))  # accuracy_score mide la exactitud en las filas apartadas
    print(f"{name}: {results.loc[name, 'exactitud']:.3f} con el resumen, {got:.3f} con los temas")  # print pone las dos exactitudes juntas
```

**Comprobar:**

Comprobamos que la etiqueta es exactamente lo que dicen los temas.
Si una palabra de `TARGET_TOPICS` está en los temas, la etiqueta es 1.
Si no está, la etiqueta es 0.

```python
built = topics_text.apply(mentions_topic)  # mentions_topic busca las mismas palabras en el texto de los temas
assert (built.to_numpy() == y.to_numpy()).all()  # la etiqueta no dice nada que los temas no digan ya
print("La etiqueta está dentro de los temas: OK")  # print confirma la comprobación
```

**Lo que vemos.** El primer artículo apartado del tema es el consenso sobre el término probiotic.
Sus temas dicen "Infant Nutrition and Health", así que la etiqueta es 1 por la palabra nutrition.
Con los temas, los dos métodos aciertan 0,969.
La regresión sube de 0,922 y la red de 0,844.
Ese salto no es un mejor modelo.
La entrada ya trae la respuesta.
Por eso los temas no entran en la Parte 3.
Un salto así se revisa antes de creerlo.

**Tres errores para leer.** La celda muestra tres artículos donde la regresión logística se equivoca.
Un error puede ser del modelo o de la etiqueta.

```python
said_lr = pd.Series(pred_lr, index=test.index)  # Series pone lo que dijo la regresión junto a cada título
wrong = test.index[said_lr != y_test][:3]  # tomamos los tres primeros errores
for t in wrong:  # recorremos cada error
    print(f"{t[:80]}  etiqueta {y_test[t]}, la regresión dijo {said_lr[t]}")  # print muestra la etiqueta y lo que dijo la regresión
```

---

## Parte 6. Despliegue

### Paso 1. Una predicción para cada artículo
En este paso cada artículo recibe una probabilidad de un modelo que no vio su etiqueta.
Partimos los 318 artículos en `N_FOLDS` partes, como en la Lección 4.
Cada parte la responde un modelo entrenado con las otras cuatro.
La predicción es positiva si **los dos métodos** dicen que se lee.

```python
folds = StratifiedKFold(n_splits=N_FOLDS, shuffle=True, random_state=SEED)  # StratifiedKFold arma cinco partes con la misma proporción de cada clase
table = pd.DataFrame(index=pd.Index(titles, name="title"))  # DataFrame arma una fila por título
for name, column in [("regresión logística", "prob_regresion"), ("una capa oculta", "prob_red")]:  # recorremos los dos métodos con su columna
    table[column] = cross_val_predict(clone(models[name]), texts, y, cv=folds, method="predict_proba")[:, 1]  # cross_val_predict da a cada artículo la probabilidad de un modelo que no lo vio
table["prediction"] = (table["prob_regresion"] > 0.5) & (table["prob_red"] > 0.5)  # los dos métodos dicen leer
table["prob_media"] = (table["prob_regresion"] + table["prob_red"]) / 2  # el promedio ordena la lista
print(f"Regresión dice leer: {(table['prob_regresion'] > 0.5).sum()}. Red: {(table['prob_red'] > 0.5).sum()}. Los dos: {table['prediction'].sum()}")  # print muestra los tres conteos
```

**Comprobar:**

Comprobamos que hay una probabilidad por artículo y que está entre 0 y 1.

```python
assert len(table) == N and table[["prob_regresion", "prob_red"]].stack().between(0, 1).all()  # una probabilidad por artículo, entre 0 y 1
print("Predicción para cada artículo: OK")  # print confirma la comprobación
```

**Lo que vemos.** La regresión manda a leer 78 artículos y la red 55.
Los dos coinciden en 55, y 53 de ellos son del tema.

### Paso 2. Guardar la predicción
En este paso guardamos `outputs/prediccion_l6.csv`.

```python
prediction_table = table.reset_index()  # reset_index deja el título como columna
prediction_table["etiqueta"] = y.to_numpy()  # la etiqueta de OpenAlex
prediction_table["apartada"] = prediction_table["title"].isin(test.index)  # si la fila estaba apartada en la Parte 3
prediction_table[["prob_regresion", "prob_red", "prob_media"]] = prediction_table[["prob_regresion", "prob_red", "prob_media"]].round(3)  # round deja 3 decimales
prediction_path = OUTPUTS_DIR / "prediccion_l6.csv"  # Path fija la ruta de la predicción
prediction_table.to_csv(prediction_path, index=False)  # to_csv escribe la tabla y deja fuera el índice
print(f"Guardado: {prediction_path} ({len(prediction_table)} filas)")  # print confirma dónde quedó
```

### Paso 3. Qué cambiaría la decisión
En este paso escribimos cómo entra la predicción y qué la cambiaría.

| Qué | Respuesta |
|-----|-----------|
| Cómo entra | Entra en la lista si los dos métodos dicen leer, con un modelo que no vio la etiqueta, y solo si los dos superan a la clase mayoritaria |
| Cómo se lee | La etiqueta supone que un artículo del tema se debe leer. La regresión acierta más que la red. La red marca menos artículos, y casi todos los que marca son del tema |
| Qué lo cambia | Otra definición de "se debe leer". Otras palabras en `TARGET_TOPICS`. Otra partición de los datos. Otro margen que 0,02 |

### Paso 4. Artículos para leer
Si la predicción cuenta, la lista guarda como máximo 30 artículos que los dos métodos mandan a leer.
Ordenamos por la probabilidad media, de mayor a menor, y si empatan, por título.
Si no cuenta, la lista queda vacía y lo decimos.

```python
if l6_counts:  # la predicción cuenta
    reading = table[table["prediction"]].reset_index()  # reset_index deja el título como columna
else:  # la predicción no cuenta
    reading = table.iloc[0:0].reset_index()  # la lista queda vacía
    print("Los dos métodos no superan a la clase mayoritaria. La predicción no arma lista.")  # print lo dice
reading = reading.sort_values(["prob_media", "title"], ascending=[False, True])  # sort_values ordena por la probabilidad media y después por título
reading_list = reading[["title", "prob_media"]].head(MAX_PAPERS).round(3).reset_index(drop=True)  # head se queda con los MAX_PAPERS primeros
reading_path = OUTPUTS_DIR / "lectura_l6.csv"  # Path fija la ruta de la lista
reading_list.to_csv(reading_path, index=False)  # to_csv escribe la lista y deja fuera el índice
print(f"Los dos dicen leer: {len(reading)}. En la lista: {len(reading_list)}.")  # print muestra los dos conteos
reading_list.head(10)  # head muestra los 10 primeros títulos
```

Arriba quedan los artículos que los dos métodos mandan a leer con más seguridad.
Si hay varias ediciones de la misma guía, el equipo abre la más reciente.

**Comprobar:**

Comprobamos que la lista no pasa de 30, que va ordenada y que cada artículo lo mandan a leer los dos métodos.

```python
assert len(reading_list) == min(MAX_PAPERS, len(reading))  # la lista no pasa de 30
assert reading_list["prob_media"].is_monotonic_decreasing  # la probabilidad no sube al bajar en la lista
assert table.loc[reading_list["title"], "prediction"].all()  # cada artículo lo mandan a leer los dos métodos
print("Lista de lectura: OK")  # print confirma la comprobación
```

En esta iteración predijimos, desde el resumen, si cada uno de los 318 artículos se debe leer.
La etiqueta supone que un artículo del tema del colega se debe leer.
La regresión logística acierta 0,878 en promedio, la red 0,822 y la clase mayoritaria 0,688.
La lista guarda 30 de los 55 artículos que los dos métodos mandan a leer.

La principal razón detrás de estos resultados es que el tema se nota en las palabras del resumen.
Con 318 artículos, una red con una capa oculta no le gana a la regresión logística.
Estos hallazgos deben reportarse como parte del proceso de minería y al mismo tiempo informar futuras iteraciones.

<!-- end NOTEBOOK: -->
