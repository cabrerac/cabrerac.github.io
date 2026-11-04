<!-- NOTEBOOK: -->

## Repaso de Python para este cuaderno
 
Este repaso es corto. Muestra la idea que usamos en toda la lección: un modelo aprende con `fit` sobre unas filas y responde con `predict` sobre otras que no vio. Si ya la conoce, ejecute la celda rápido y siga. Es la misma idea de la L4 con el texto, ahora con atributos como el año o el número de autores. Lo que importa es que el modelo nunca vea las filas con las que lo medimos.
 
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

**Lo que vemos.** El árbol aprendió con cuatro filas y acertó las otras cuatro. Con ocho números en orden es fácil. Con artículos reales los aciertos bajan, y por eso hoy siempre comparamos con una línea base.

---
 
## Instrucciones
 
**La historia.** Seguimos con el equipo interno de la secretaría de salud y sus artículos de nutrición. Ya tenemos cuatro resultados: patrones (L2), grupos (L3), texto (L4) y el lugar en la red (L5). Hoy sumamos el último: **predecir una etiqueta dada** a partir de los atributos de cada artículo. La etiqueta del laboratorio es `internacional`: un artículo con autores de al menos dos países. No sale del texto y no es una cuenta de citas. Al final de la lección el equipo tiene una lista de lectura corta, con los resultados que apoyan cada artículo, y sabe qué parte de la lista depende de cada uno.
 
**La idea central.** La etiqueta está dada, no la buscamos. Aprendemos con una parte de los artículos y contamos aciertos y errores en otra parte que ningún modelo vio. Cada modelo se compara con la **clase mayor**: decir siempre la clase más común. Un modelo que no le gana a eso no aporta. Y ponemos al lado una regla de una línea, sin modelo, para ver si los modelos ganan algo sobre lo obvio.
 
**Tres métodos, tres preparaciones.**
 
| Método | Pregunta | Preparación que necesita |
|--------|----------|--------------------------|
| M1. Regresión logística | ¿Qué atributos pesan a favor y en contra? | Números escalados, categorías en columnas de 0 y 1, faltantes llenados |
| M2. Bosque aleatorio | ¿Qué cortes en los atributos separan las clases? | La misma tabla. Escalar no cambia un corte |
| M3. Una capa oculta | ¿Qué combinación de atributos separa las clases? | Todo numérico y escalado, faltantes llenados |
 
**Qué hacer.** Ejecute las celdas de arriba hacia abajo. Cada paso empieza con **En este paso**. Los pasos que crean algo nuevo terminan con una celda `# Comprobar`. Si un `assert` falla, revise la celda anterior antes de seguir. Los nombres del código están en inglés, como en todos los cuadernos del curso. Las explicaciones están en español.
 
**El sábado 21 nov.** Hacia las 09:20 seguimos en vivo con este cuaderno, hasta las 10:00. La meta en clase es ver una predicción con sus errores. Lo que falte se termina en casa.
 
**Del laboratorio al proyecto.** Desde las 10:00 el cuaderno de grupo de la semana 3 repite estos pasos con los atributos de los artículos de su secretaría y arma la lista de inicio.
 
**Mapa del cuaderno**
 
| Parte | Fase CRISP-DM | Qué sale |
|-------|---------------|----------|
| 1 | Configuración | Librerías, parámetros y la función contra la fuga |
| 2 | Comprensión del negocio | `pregunta.json` y los cuatro resultados de las lecciones 2 a 5 |
| 3 | Comprensión de los datos | La etiqueta y los atributos |
| 4 | Preparación de los datos | La tabla, el conjunto apartado y la preparación |
| 5 | Modelado | Clase mayor, regresión logística, bosque y una capa oculta |
| 6 | Evaluación | Aciertos y errores, cinco pliegues y la regla de una línea |
| 7 | Despliegue | El resultado de la predicción y la lista inicial |

---
 
## Parte 1. Configuración
 
### Paso 1. Librerías, carpetas y parámetros
En este paso importamos las librerías y fijamos los parámetros. En Colab todo viene instalado. Los parámetros de la L4 se copian sin cambios. Los de la L6 se definen aquí una sola vez y son los mismos en el cuaderno de grupo. No los cambie aquí.

```python
import json          # leer y escribir pregunta.json
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

# L6 (compartidos con el cuaderno de grupo, no cambiar)
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


print(f"Etiqueta: {LABEL}. Una capa oculta de {HIDDEN_UNITS} unidades, {N_TREES} árboles")
```

### Paso 2. La fuga de la respuesta
En este paso escribimos la función que quita de `n_claims` la propiedad que define la etiqueta. Los artículos no tienen `n_claims`, pero los extractos de Wikipedia sí, y el cuaderno de grupo usa esta función. Si la etiqueta es una propiedad de Wikidata que `n_claims` cuenta, cada fila positiva suma 1 a su propio `n_claims`, y el modelo vería la respuesta. Eso se llama **fuga**. La probamos con una tabla de juguete de cuatro filas, donde la etiqueta es tener imagen.

```python
PROPERTY_COLUMN = {"P18": "has_image"}     # propiedad de Wikidata -> columna del extracto
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

**Lo que vemos.** Las dos filas con imagen pierden una propiedad y las otras quedan igual. Sin este paso, un modelo aprendería que más propiedades es más imagen, y acertaría por la razón equivocada.

```python
# Comprobar
assert (result >= 0).all()
assert (toy_table.loc[toy_table["has_image"] == 1, "n_claims"] >= 1).all()
assert ((toy_table["n_claims"] - result) == y).all()
print("Fuga quitada con una etiqueta que es una propiedad: OK")
```

```python
# Comprobar
assert (n_claims_without(toy_table, "categoria") == toy_table["n_claims"]).all()
print("Con otra etiqueta, n_claims queda igual: OK")
```

### Paso 3. Descargar los artículos
En este paso descargamos el archivo de artículos, el mismo de la L5, y quitamos los títulos repetidos. Así cada artículo es una fila y las tablas de las lecciones anteriores se unen por título.

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

---
 
## Parte 2. Comprensión del negocio
 
### Paso 1. Recuperar la pregunta
En este paso leemos `pregunta.json`, la tarjeta que el equipo llena desde la L1. Si la L5 corrió en esta carpeta, la tarjeta ya trae cómo entra el grafo. Si no, escribimos la tarjeta de referencia. El máximo de la lista, `max_papers`, sale de aquí.

```python
QUESTION_PATH = Path("pregunta.json")

if QUESTION_PATH.is_file():
    question_card = json.loads(QUESTION_PATH.read_text(encoding="utf-8"))
    print("pregunta.json leído de la Lección 5")
else:
    question_card = {
        "question": "¿Qué artículos de nutrición debe leer el equipo para su tema, y qué filtro los puso en la lista?",
        "standard": {"min_papers": 10, "max_papers": 30, "max_share_citations_only": 0.5},
    }
    QUESTION_PATH.write_text(json.dumps(question_card, ensure_ascii=False, indent=2), encoding="utf-8")
    print("pregunta.json no estaba. Escribimos la tarjeta.")
print(question_card["question"])
```

### Paso 2. Los cuatro resultados de las lecciones 2 a 5
En este paso armamos la tabla de resultados. Los tres de la semana 2 salen de `outputs/grupos_l3.csv` y `outputs/texto_l4.csv`, unidos por título como en la L5. El del grafo sale de `outputs/grafo_l5.csv` con la misma regla de la L5: un artículo con enlaces, en el cuarto superior por intermediación, que no es un nodo central. Si falta algún archivo, el resultado queda en falso. Recalculamos el resultado del grafo en vez de leerlo, para que la regla quede a la vista en este cuaderno.

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
graph_l5 = read_or_empty(OUTPUTS_DIR / "grafo_l5.csv", ["title", "grado", "intermediacion", "alerta_centro", "supports"])

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
between = graph_l5["intermediacion"].astype(float)
cut = np.sort(between[linked].to_numpy())[int(0.75 * linked.sum())] if linked.any() else np.inf
table["graph_support"] = linked & (between >= cut) & (graph_l5["alerta_centro"].astype(str) != "True")
print(table.sum().to_dict())
```

```python
# Comprobar
SUPPORT_COLUMNS = ["has_pattern", "read_group", "text_says_read", "graph_support"]
assert len(table) == N and set(SUPPORT_COLUMNS) <= set(table.columns)
assert (table[SUPPORT_COLUMNS].astype(int).sum(axis=1) == graph_l5["supports"].fillna(0).astype(int)).all()
print(f"Cuatro resultados, iguales a los de grafo_l5.csv: OK ({(table.astype(int).sum(axis=1) >= MIN_SUPPORTS).sum()} en vista)")
```

**Lo que vemos.** Con cuatro resultados hay 69 artículos en vista con `MIN_SUPPORTS = 2`, los mismos de la L5. El grupo leído de la L3 apoya solo a 10 artículos, y el patrón de la L2 a 87. Hoy agregamos el quinto resultado.

---
 
## Parte 3. Comprensión de los datos
 
### Paso 1. La etiqueta `internacional`
En este paso construimos la etiqueta: `n_countries >= 2`. Los artículos con `n_countries = 0` no traen datos de afiliación, aunque la mayoría tiene autores. No sabemos si son internacionales, así que los dejamos fuera de la L6 como faltantes. No reciben el resultado de la predicción. Un cero en `n_countries` no quiere decir un país. Quiere decir que OpenAlex no encontró la afiliación.

```python
papers["n_countries"] = pd.to_numeric(papers["n_countries"], errors="coerce").fillna(0).astype(int)
papers["n_authors"] = pd.to_numeric(papers["n_authors"], errors="coerce")
missing = papers["n_countries"] == 0
print(f"Sin datos de afiliación: {missing.sum()} ({(papers.loc[missing, 'n_authors'] > 0).sum()} de ellos con autores)")
labelled_count = int((~missing).sum())
positives = int((papers.loc[~missing, "n_countries"] >= 2).sum())
print(f"Con etiqueta: {labelled_count}. Internacionales: {positives} ({positives / labelled_count:.0%})")
```

```python
# Comprobar
assert min(positives, labelled_count - positives) >= min_positives(labelled_count)
print(f"Clase menor con al menos {min_positives(labelled_count)} filas: OK")
```

**Lo que vemos.** Quedan 276 artículos con etiqueta, y 145 (53%) son internacionales. Las dos clases son casi del mismo tamaño, así que la clase mayor acierta poco más de la mitad. Un modelo útil tiene que ganarle con claridad.

### Paso 2. Los atributos
En este paso elegimos las entradas: año, número de autores, tipo de revista, acceso abierto y tipo de trabajo. No usamos el resumen ni los temas (eso fue la L4), ni las citas, ni los enlaces (eso fue la L5), ni `n_countries`, porque define la etiqueta. Tampoco el idioma: casi todos están en inglés. La regla es usar solo lo que el equipo sabría de un artículo antes de leerlo y que no repite un resultado anterior. Si una entrada ya fue un resultado, el modelo contaría dos veces la misma señal.

```python
print("Idioma:", papers["language"].value_counts().to_dict())
print("Tipo de revista:", papers["venue_type"].replace("", "(vacío)").value_counts().to_dict())
print("Tipo de trabajo:", papers["work_type"].value_counts().to_dict())
print(papers[["year", "n_authors"]].apply(pd.to_numeric, errors="coerce").describe().round(1))
```

**Lo que vemos.** `venue_type` casi no varía: casi todos los artículos son de revista. Lo dejamos igual, porque cuesta una línea y no hace daño. `n_authors` va de 0 (sin dato, 7 artículos, ninguno con etiqueta) a 100, y 100 es un tope del extracto, no un dato exacto. La mediana es 8 autores. Los estudios de carga global llegan al tope porque tienen cientos de autores.
 
---
 
## Parte 4. Preparación de los datos
 
### Paso 1. La tabla con etiqueta
En este paso armamos `labelled`, las filas con etiqueta, con el título como índice, igual que `table`. Así `train.index` y `test.index` son títulos y se pueden usar en `table` sin traducir. Los textos vacíos de las categorías pasan a faltantes, para que la preparación los llene con la categoría más común.

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
En este paso apartamos `n_flagged(n)` filas, con la misma proporción de cada clase. Ningún modelo las ve al aprender. Son nuestros ejemplos marcados: la etiqueta ya viene dada. La partición es estratificada, así que las apartadas tienen casi la misma proporción de internacionales que las de entrenamiento.

```python
train, test = train_test_split(labelled, test_size=n_flagged(len(labelled)), stratify=y, random_state=SEED)
y_train, y_test = y.loc[train.index], y.loc[test.index]
print(f"Para aprender: {len(train)}. Apartadas: {len(test)} ({y_test.mean():.0%} internacionales)")
```

```python
# Comprobar
assert len(test) == n_flagged(len(labelled)) and not set(train.index) & set(test.index)
assert abs(y_train.mean() - y_test.mean()) < 0.05
print("Conjunto apartado: OK")
```

### Paso 3. Escalar, codificar y llenar faltantes
En este paso preparamos la tabla con el código de las diapositivas. Los números se llenan con la mediana (y una columna que marca el faltante) y se escalan. Las categorías se llenan con la más común y se pasan a columnas de 0 y 1. Todo se aprende **solo con las filas de entrenamiento** y se reutiliza en las apartadas.

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

```python
# Comprobar
assert X_train.shape == (len(train), len(feature_names)) and X_test.shape[1] == len(feature_names)
assert not np.isnan(np.asarray(X_train, dtype=float)).any()
print("Preparación: OK")
```

**Lo que vemos.** Las 5 columnas de entrada se vuelven 12: tres números escalados y nueve columnas de 0 y 1 para las categorías. No hay columna de faltante para los números porque en el entrenamiento no falta ninguno.

---
 
## Parte 5. Modelado
 
### La clase mayor
En este paso construimos la línea base: decir siempre la clase más común en el entrenamiento. Todo modelo se mide contra ella. Aquí la clase mayor es internacional, y acierta un poco más de la mitad de las apartadas.

```python
baseline = DummyClassifier(strategy="most_frequent").fit(X_train, y_train)
pred_majority = baseline.predict(X_test)
majority = max(np.mean(y_test), 1 - np.mean(y_test))
print(f"La clase mayor acierta {accuracy_score(y_test, pred_majority):.2f} de las apartadas")
```

### M1. Regresión logística
En este paso usamos la regresión logística de la L4, con el mismo código. Cada atributo preparado recibe un peso. Un peso positivo empuja hacia internacional y uno negativo hacia nacional. `class_weight="balanced"` da el mismo peso total a las dos clases, como en la diapositiva.

```python
lr = LogisticRegression(class_weight="balanced", C=C_REG,
                        max_iter=1000)
lr.fit(X_train, y_train)
pred_lr = lr.predict(X_test)

weights = pd.Series(lr.coef_[0], index=feature_names)
print(weights.sort_values().round(2))
```

**Lo que vemos.** Los pesos más grandes son de `work_type`: una revisión (1,32) o un artículo (0,98) empujan hacia internacional, y un preprint (-1,13) hacia nacional. `n_authors` tiene un peso positivo de 0,44 por cada desviación estándar. Los tipos raros, con una o dos filas, tienen pesos grandes que no hay que creer.

### Un corte a mano
En este paso hacemos a mano lo que hace un árbol de decisión en cada nodo, con los números de juguete de la diapositiva. Al final de la celda `y` vuelve a ser la etiqueta `internacional`, y la comprobación lo verifica. El árbol prueba cada umbral de un atributo, mide qué tan mezcladas quedan las etiquetas a cada lado y se queda con el umbral que deja los lados más puros.

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

```python
# Comprobar
assert best == 3, "El mejor umbral de la diapositiva es 3"
assert toy_scores[best] == 0.0 and gini([0, 0, 1, 1]) == 0.5
assert all(score > 0 for t, score in toy_scores.items() if t != best) and y.index.equals(labelled.index)
print("Corte a mano: OK", toy_scores)
```

Con estos números un solo corte separa todo. Con datos reales ningún corte deja los lados puros, y un árbol profundo termina con una hoja por fila de entrenamiento. Por eso el bosque junta muchos árboles, cada uno un poco distinto, y los deja votar.

### M2. Bosque aleatorio
En este paso entrenamos 200 árboles. Cada uno aprende con una muestra al azar de las filas y prueba un subconjunto de atributos en cada corte. El bosque vota. `min_samples_leaf=3` no deja hojas de una sola fila. La importancia de un atributo es cuánto baja la impureza de Gini en los cortes que lo usan, sumada sobre todos los árboles.

```python
forest = RandomForestClassifier(n_estimators=N_TREES, min_samples_leaf=3,
                                random_state=SEED)
forest.fit(X_train, y_train)   # escalar no cambia un corte, así que sirve el mismo X_train
pred_rf = forest.predict(X_test)

importance = pd.Series(forest.feature_importances_, index=feature_names)
print(importance.nlargest(5).round(3))
```

**Lo que vemos.** El bosque usa sobre todo `n_authors` (0,51) y el año (0,37). Los tipos de trabajo casi no cuentan. La regresión ponía arriba el tipo de trabajo y el bosque pone el número de autores: dos modelos, dos lecturas de la misma tabla.

### M3. Una capa oculta
En este paso entrenamos una red con una capa oculta de `HIDDEN_UNITS` unidades. `PENALTY` es el peso de la penalización L2 (`alpha` en scikit-learn). Con pocas filas usamos una penalización más fuerte que la de la diapositiva. Ocho unidades y 220 filas ya son muchos pesos para tan pocos datos. La red necesita números escalados, y `prepare` ya los escaló.

```python
network = MLPClassifier(hidden_layer_sizes=(HIDDEN_UNITS,), alpha=PENALTY,
                        max_iter=3000, random_state=SEED)
network.fit(X_train, y_train)          # X_train ya viene escalado por prepare
pred_nn = network.predict(X_test)
print(f"La red terminó en {network.n_iter_} pasos")
```

**Lo que vemos.** La red paró en 188 pasos, lejos del máximo de 3000. Eso quiere decir que encontró un mínimo y no la cortamos a la mitad. Si apareciera un aviso de convergencia, habría que subir `max_iter`.

```python
# Comprobar
predictions = {"clase mayor": pred_majority, "regresión logística": pred_lr, "bosque": pred_rf, "una capa oculta": pred_nn}
assert all(len(p) == len(y_test) for p in predictions.values())
print("Cuatro predicciones sobre las filas apartadas: OK")
```

---
 
## Parte 6. Evaluación
 
### Paso 1. Aciertos y errores en las filas apartadas
En este paso contamos TP, FP, FN y TN de cada método, y su exactitud. Ponemos al lado una regla de una línea, sin modelo: **internacional si tiene al menos 4 autores**. 4 es el umbral que más acierta en las filas de entrenamiento, en las cinco particiones: lo imprimimos en el Paso 6. TP es un internacional que el método llamó internacional, FP un nacional que llamó internacional, FN un internacional que se le pasó y TN un nacional bien dicho.

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

```python
# Comprobar
assert (results[["TP", "FP", "FN", "TN"]].sum(axis=1) == len(y_test)).all()
assert all(results.loc[m, "exactitud"] >= majority for m in ["regresión logística", "bosque", "una capa oculta"])
print("Los tres métodos igualan o superan a la clase mayor: OK")
```

**Lo que vemos.** Los tres métodos le ganan a la clase mayor (0,52): la regresión acierta 0,61, el bosque 0,71 y la red 0,63. En esta partición la regla acierta 0,73, una fila más que el bosque (41 contra 40 de 56). Una fila es menos que `MARGIN`, así que la regla no le gana al bosque con claridad. Con otras semillas la ventaja cambia, por eso miramos varias en el Paso 6. Casi no se le pasan internacionales (3 FN), a cambio de llamar internacionales a 12 nacionales.

### Paso 2. Las matrices de confusión
En este paso dibujamos las matrices de confusión de los tres métodos y las guardamos en `outputs/`. Son los mismos números de la tabla, en la forma que se usa en un informe.

```python
for name, pred, file in [("regresión logística", pred_lr, "confusion_regresion.png"), ("bosque", pred_rf, "confusion_bosque.png"), ("una capa oculta", pred_nn, "confusion_red.png")]:
    fig, ax = plt.subplots(figsize=(3.5, 3.2))
    ConfusionMatrixDisplay.from_predictions(y_test, pred, labels=[0, 1], display_labels=["nacional", "internacional"], cmap="Blues", colorbar=False, ax=ax)
    ax.set_title(name)
    fig.tight_layout()
    fig.savefig(OUTPUTS_DIR / file, dpi=120)
    plt.show()
```

**Lo que vemos.** La regresión y la red se equivocan parecido: dejan pasar unos 15 internacionales. El bosque equilibra mejor los dos errores, con 8 FP y 8 FN. Ningún método se equivoca solo de un lado.

### Paso 3. Cinco pliegues en las filas de entrenamiento
En este paso repetimos la cuenta con cinco pliegues sobre las filas de entrenamiento. Cada modelo va con su preparación adentro, así que en cada pliegue la preparación se aprende sin ver la parte que se prueba. Las 56 filas apartadas son pocas, y cinco pliegues sobre 220 filas dan una segunda opinión.

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

**Lo que vemos.** En cinco pliegues los tres quedan entre 0,61 y 0,65, contra 0,53 de la clase mayor. La regla acierta 0,69 en las mismas 220 filas. La regla solo fija un número, 4, y es el mejor en estas filas en las cinco particiones, así que este 0,69 es un poco optimista. El bosque baja de 0,71 a 0,62. La diferencia es la suerte de las 56 filas apartadas, y por eso no leemos un solo número.

### Paso 4. ¿Cuenta la L6?
En este paso decidimos si la predicción suma un resultado. Cuenta (`l6_counts`) solo si los tres métodos quedan más de `MARGIN` por encima de la clase mayor en las filas apartadas. 0,02 es una o dos filas de unas 60: sirve para desempatar, no es una prueba. La línea de `l6_counts` es la de la diapositiva y escribe 0,02 a mano. Ese 0,02 es `MARGIN`. Los modelos ya están entrenados con `train`, así que la línea solo predice. En el bucle de particiones usamos `clone`, una copia sin entrenar de cada modelo, para no tocar los modelos ya entrenados. Después repetimos con otras cuatro particiones para ver si el resultado se sostiene.

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

**Lo que vemos.** La L6 cuenta, y se sostiene en las cinco particiones. La predicción suma un resultado. Falta saber de dónde sale la señal. En otros datos puede salir `l6_counts = False`. Eso es un resultado normal y válido: la predicción no apoya la lista, y en el proyecto se informa así, con la razón (los métodos no le ganan a la clase mayor por más de `MARGIN`).

### Paso 5. ¿De dónde sale la señal?
En este paso probamos dos variantes con los mismos modelos: solo `n_authors`, y todo menos `n_authors`. Así vemos qué atributo lleva la señal. Cada variante arma su propia preparación con las columnas que usa, y entrena copias nuevas de los modelos con `clone`.

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
En este paso repetimos la comparación en las cinco particiones de `SPLIT_SEEDS`. Para cada una, la regla de 4 autores, los tres modelos y los tres modelos sin `n_authors`, siempre con copias nuevas (`clone`). La última columna es el umbral que más acierta en las filas de entrenamiento de esa partición. Así vemos si el resultado de la partición del cuaderno se repite.

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

**Lo que vemos.** La regla le gana a los tres modelos en las semillas 7 y 8. En la 9 y la 10 la red le gana (0,732 contra 0,679 y 0,768 contra 0,696), y en la 11 el bosque empata (0,714). Sin `n_authors` los tres modelos siguen sobre la clase mayor (0,518) en las cinco, entre 0,554 y 0,714. El mejor umbral en las filas de entrenamiento es 4 en las cinco particiones, así que la regla no se eligió mirando las filas apartadas.

**Lo que encontramos.** La señal es el número de autores. Tres modelos no le ganan con claridad a contar autores. En esta partición la regla acierta 0,73, una fila más que el bosque, y en las 220 filas de entrenamiento acierta 0,69, contra 0,61 a 0,65 de los modelos en cinco pliegues. Con otras semillas la ventaja cambia, por eso miramos varias: en el Paso 6 la red le gana a la regla en dos de las cinco particiones. Solo con `n_authors`, el bosque acierta 0,70, cerca de su 0,71 con todos los atributos. Sin `n_authors` los modelos siguen por encima de la clase mayor en las cinco particiones, y en la del cuaderno quedan unos 5 a 9 puntos por encima. Tiene sentido: más autores quiere decir más instituciones, y más instituciones, más países. El resultado es real pero modesto, y se dice así. Que tres modelos no superen con claridad a una regla de una línea no es un fracaso del cuaderno: es lo que un equipo tiene que saber antes de confiar en un modelo.
 
**Su turno.** Lea tres artículos apartados donde los modelos se equivocan. Escriba en dos frases si el error es del modelo o de la etiqueta (por ejemplo, un país que falta en la afiliación). Un artículo con 100 autores de un solo país es raro, y vale la pena mirar su afiliación en OpenAlex.

```python
said_rf = pd.Series(pred_rf, index=test.index)
wrong = test.index[said_rf != y_test][:3]
for t in wrong:
    print(f"{t[:80]}  autores {attributes.loc[t, 'n_authors']:.0f}, países {attributes.loc[t, 'n_countries']}, el bosque dijo {said_rf[t]}")
my_errors = """
Escriba aquí qué pasa con esos tres artículos.
"""
print(my_errors)
```

---
 
## Parte 7. Despliegue
 
### Paso 1. El resultado de la predicción
En este paso definimos el resultado de la predicción. Un artículo se predice positivo cuando **al menos 2 de los 3 métodos** dicen que sí. Las filas de entrenamiento usan las predicciones fuera del pliegue y las apartadas usan las predicciones de los modelos entrenados sin ellas. Así ningún artículo lo puntúa un modelo que vio su etiqueta. Los artículos sin etiqueta no reciben este resultado. El código es el de la diapositiva: `pd.concat` junta los votos de las dos partes, con el título como índice, y `reindex` los pone en el orden de `table`, con falso para las filas sin etiqueta.

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

```python
# Comprobar
assert not table.loc[~table.index.isin(labelled.index), "prediction"].any()
assert table.loc[labelled.index, "prediction"].sum() == (train_votes >= 2).sum() + (test_votes >= 2).sum()
print("Resultado de la predicción sin filas vistas: OK")
```

### Paso 2. ¿Se repite con el texto?
En este paso medimos si la etiqueta repite el texto de la L4 (phi entre la etiqueta y `text_says_read`), en las filas con etiqueta. Medimos la etiqueta y no la predicción: si la etiqueta misma sigue al texto, predecirla no es un resultado nuevo. Si phi es al menos 0,30 en valor absoluto, las dos cuentan como **un** resultado (`text_or_prediction`). Si no, son dos. phi es la correlación de dos columnas de 0 y 1: vale 0 si no tienen relación.

```python
phi = np.corrcoef(y, table.loc[labelled.index, "text_says_read"].astype(int))[0, 1]
one_support = abs(phi) >= 0.30
print(f"phi entre la etiqueta y el texto de la L4: {phi:.2f}. {'Un solo resultado' if one_support else 'Dos resultados separados'}")
```

**Lo que vemos.** phi es casi 0. Ser internacional no tiene nada que ver con que el texto diga leer, así que el texto y la predicción cuentan como dos resultados separados.

### Paso 3. La lista inicial
En este paso sumamos los cinco resultados. Un artículo entra en la lista inicial con al menos `MIN_SUPPORTS` resultados a favor. El código empieza en 2. Cambie el valor si lo justifica, 0 o 1 también valen. La tabla de la celda cuenta cuántos artículos tienen 0, 1, 2 y 3 o más resultados a favor. Mostramos cuántos artículos agrega la predicción que el texto no tenía, y el tamaño con tres resultados a favor. Si la L6 no cuenta, la predicción no suma a nadie, y eso también se informa como resultado.

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
En este paso quitamos cada resultado y contamos quién sale de la lista. Es lo que cambiaría la decisión. Un artículo sale si sin ese resultado le quedan menos de `MIN_SUPPORTS` resultados a favor. Aquí usamos `MIN_SUPPORTS = 2`, el valor con que empieza el código. Si el equipo cambia el valor, esta cuenta cambia. Un resultado que saca a muchos artículos es uno del que la lista depende mucho. Si ese resultado fuera débil, la lista también lo sería.

```python
drop_one = {}
for column in SUPPORT_COLUMNS:
    rest = [c for c in SUPPORT_COLUMNS if c != column]
    drop_one[column] = int((table["in_view"] & (table[rest].astype(int).sum(axis=1) < MIN_SUPPORTS)).sum())
print("Salen de la lista si quitamos:", drop_one)
```

```python
# Comprobar
assert table["supports"].between(0, len(SUPPORT_COLUMNS)).all()
assert set(drop_one) == set(SUPPORT_COLUMNS)
print("Lista inicial y sensibilidad: OK")
```

**Lo que vemos.** Con cinco resultados y `MIN_SUPPORTS = 2` hay 98 artículos en vista, 29 más que con cuatro. Si quitamos la predicción salen 29, y si quitamos el patrón de la L2 salen 35. El grupo leído casi no mueve la lista (2).

### Paso 5. Una lista que se pueda leer
En este paso recortamos la lista con la regla de la semana 2. El máximo es `standard["max_papers"]` de `pregunta.json`. Ordenamos por número de resultados a favor, después por `prob_texto` (la probabilidad de TF-IDF y regresión logística en `outputs/texto_l4.csv`) y después por título. Nos quedamos con los primeros y marcamos el resto con `recortado = True`, sin borrarlo. Los 3 artículos sin texto van al final dentro de su número de resultados a favor. El orden no es un puntaje nuevo: solo decide qué se lee primero cuando hay demasiados.

```python
MAX_LIST = question_card["standard"]["max_papers"]
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

```python
# Comprobar
assert kept <= MAX_LIST and kept == min(len(starter_list), MAX_LIST)
assert starter_list["supports"].is_monotonic_decreasing
print("Lista recortada: OK")
```

**Lo que vemos.** De 98 artículos en vista se leen 30 y quedan 68 recortados. Los recortados siguen en el archivo con `recortado = True`, así que el equipo puede volver a ellos si la lista corta no alcanza. Primero van los artículos con más resultados a favor, y dentro de cada número de resultados los que el texto de la L4 puntuó más alto.

**Lo que aprendemos aquí.** La lista crece mucho con la predicción, porque más de la mitad de los artículos con etiqueta (146 de 276, el 53%) se predice internacional y eso no tiene que ver con el tema del equipo. Ser internacional es un atributo del artículo, no una razón para leerlo. Por eso la lista inicial es un punto de partida para leer, y la tabla de "quitar cada resultado" dice qué parte de la lista depende de cada método.
 
### Paso 6. Guardar la predicción y la lista
En este paso guardamos `outputs/prediccion_l6.csv` (una fila por artículo) y `outputs/lista_inicial.csv` (los artículos en vista, primero los de más resultados a favor). `votos` es cuántos de los tres métodos dijeron internacional, y queda vacío en las filas sin etiqueta.

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
En este paso anotamos en `pregunta.json` cómo entra la predicción, si la L6 cuenta y qué lo cambiaría. Es la última entrada de la tarjeta antes del sábado.

```python
question_card["prediction_use"] = {
    "label": LABEL,
    "how_it_enters": "La predicción cuenta a favor de un artículo si al menos 2 de los 3 métodos lo predicen positivo, con un modelo que no vio su etiqueta, y solo si la L6 cuenta.",
    "l6_counts": bool(l6_counts),
    "starter_list": {"in_view": int(len(starter_list)), "read": kept, "cut": int(starter_list["recortado"].sum())},
    "seeds_holding": f"{seeds_holding} de {len(SPLIT_SEEDS)}",
    "reading": "La señal es el número de autores. Tres modelos no le ganan con claridad a contar autores (la regla de al menos 4 autores). Con otras semillas la ventaja cambia, por eso miramos varias.",
    "what_changes_it": ["otra etiqueta", "otra partición de los datos", "los artículos sin afiliación", "otro margen que 0,02"],
}
QUESTION_PATH.write_text(json.dumps(question_card, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(question_card["prediction_use"], ensure_ascii=False, indent=1))
```

**Lo que vemos.** La tarjeta dice con qué etiqueta trabajamos, que la L6 cuenta en las cinco particiones y que la señal es el número de autores. También dice qué cambiaría la decisión. Quien lea la lista el sábado puede saber por qué la predicción apoya a un artículo sin abrir este cuaderno.

### Paso 8. Comprobación final
En este paso revisamos que el cuaderno dejó todo lo que el sábado necesita. La línea de los tres errores la escribe usted, así que cuenta como comprobación.

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
    ("pregunta.json con uso de la predicción", lambda: "prediction_use" in json.loads(QUESTION_PATH.read_text(encoding="utf-8"))),
    ("outputs/prediccion_l6.csv", lambda: prediction_path.is_file()),
    ("outputs/lista_inicial.csv", lambda: starter_path.is_file()),
    ("Matrices de confusión", lambda: all((OUTPUTS_DIR / f).is_file() for f in ["confusion_regresion.png", "confusion_bosque.png", "confusion_red.png"])),
    ("Resultados de las lecciones 2 a 5", lambda: len(groups_l3) > 0 and len(graph_l5.dropna(how="all")) > 0),
    ("Tres errores leídos a mano", lambda: "Escriba aquí" not in my_errors),
]
passed = sum(_check_ok(n, f) for n, f in checks)
print(f"\nL6_CHECKS={passed}/{len(checks)}")
if passed == len(checks):
    print("L6_OK. Lleve su lista inicial al sábado. En el cuaderno de grupo hará lo mismo con Wikipedia.")
```

---

## Conclusiones

El equipo de la secretaría de salud empezó la semana 2 con 318 artículos y una pregunta: ¿qué leer para su tema, y qué filtro puso cada artículo en la lista? Ahora tiene una lista de 30 para leer, recortada de 98 en vista. La lista muestra qué resultados apoyan cada artículo: el patrón de la L2, el grupo leído de la L3, el texto de la L4, el lugar en la red de la L5 y la predicción de la L6.

Cada resultado agregó algo distinto. El patrón de la L2 es el que más pesa: si lo quitamos salen 35 artículos. Sin el texto salen 22 y sin el grafo 14. El grafo agrega puentes que una cuenta de citas no vería. Si quitamos la predicción salen 29, pero su señal es el número de autores. Tres modelos no le ganan con claridad a contar autores. Con otras semillas la ventaja cambia, por eso miramos varias. Ser internacional no es una razón para leer un artículo, y el equipo lo sabe porque la tabla de "quitar cada resultado" lo muestra.

Lo que cambiaría la lista: otra etiqueta para la L6, otra partición de los datos, los 42 artículos sin afiliación, u otro margen que 0,02. Esta es la lista que el equipo lleva al sábado.

```python
reading_list = starter_list.loc[~starter_list["recortado"], ["title", "supports"]].reset_index(drop=True)
reading_list.index += 1
print(f"Lista de lectura del equipo: {len(reading_list)} artículos")
for i, row in reading_list.iterrows():
    print(f"{i:2d}. ({row['supports']} resultados) {row['title'][:90]}")
```

Esta lista no es la respuesta final. Es un punto de partida para leer, con el porqué de cada artículo escrito al lado. En el cuaderno de grupo cada grupo hace lo mismo con los artículos de Wikipedia de su secretaría.

<!-- end NOTEBOOK: -->
