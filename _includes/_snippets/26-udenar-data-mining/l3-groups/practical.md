<!-- NOTEBOOK: -->

## Repaso de Python para este cuaderno

Este cuaderno utiliza los siguientes métodos de Python. Si ya los conoce, ejecute estas celdas rápido.

### Arreglos de `numpy`
Un **arreglo** guarda números en filas y columnas. Aquí cada fila es un artículo y cada columna una palabra. `shape` dice el tamaño.

```python
import numpy as np

counts_toy = np.array([[2, 1, 0], [0, 1, 3]])   # np.array construye la tabla de conteos del ejemplo
print(counts_toy.shape)
print(counts_toy[0])          # el índice 0 toma la primera fila de la tabla
```

### La magnitud de un vector
La magnitud de un vector es la raíz de la suma de sus valores al cuadrado.
En el ejemplo, la primera fila es (2, 1, 0).
Al dividir el vector por su magnitud lo dejamos en magnitud 1.
Así, más adelante, un resumen largo no pesa más que uno corto.

```python
row = counts_toy[0].astype(float)
length = np.linalg.norm(row)
print(f"Largo: {length:.3f}. Después de escalar: {np.linalg.norm(row / length):.3f}")
```

### Coseno de vectores unitarios
Con dos vectores de magnitud 1, el coseno es el producto punto `u @ v`.
Así comparamos la mezcla de palabras y no el largo del artículo.
En el ejemplo comparamos las dos filas de la tabla de juguete.

```python
u = counts_toy[0] / np.linalg.norm(counts_toy[0])
v = counts_toy[1] / np.linalg.norm(counts_toy[1])
assert abs(np.linalg.norm(u) - 1) < 1e-9
print(f"Coseno: {u @ v:.3f}. Repaso de Python: OK")
```

---

## Instrucciones

Seguimos con el equipo interno de la secretaría de salud y sus 320 artículos sobre nutrición.
El equipo debe decidir **qué artículos tiene que leer** un nuevo colega.
En la Lección 2 encontramos pares de palabras que se repiten.
Hoy buscamos **grupos** de artículos con palabras parecidas (Jain, 2010).


**Tres métodos en este cuaderno.** Para cada uno llevaremos a cabo la preparación de los datos y su modelado.
Si un método no da un "buen resultado", lo debemos documentar como un resultado útil.
CRISP-DM sigue con la evaluación para decidir cuáles métodos se deben utilizar.

| Método | Pregunta | Preparación que necesita | Qué aporta |
|--------|----------|--------------------------|------------|
| k-means | ¿Qué $k$ centros resumen mejor los artículos? | Los conteos, cada fila escalada a magnitud 1 | Asigna cada artículo a un grupo |
| Mezcla gaussiana | ¿Qué probabilidad tiene cada artículo de pertenecer a cada nube? | Las primeras 5 direcciones de la SVD | Una probabilidad por artículo y por nube |
| HDBSCAN | ¿Dónde hay zonas densas de artículos? | Distancias coseno sobre las 10 primeras direcciones de la SVD | Un conjunto de grupos |

**Qué hacer.** Ejecute las celdas de arriba hacia abajo.
Cada paso empieza con **En este paso**. Si tiene código, termina con una celda **Comprobar**.

**Mapa del cuaderno**

| Parte | Fase CRISP-DM | Qué sale |
|-------|---------------|----------|
| 1 | Comprensión del negocio | La pregunta de hoy y las palabras del tema |
| 2 | Comprensión de los datos | Parámetros y artículos |
| 3 | k-means | Conteos, cada fila de magnitud 1 |
| 4 | Ajuste de k-means | Centros, silueta y palabras de cada grupo |
| 5 | Mezcla gaussiana | Cinco direcciones, probabilidades y cuántos artículos abriría |
| 6 | HDBSCAN | Diez direcciones, distancias, el ajuste y el ruido |
| 7 | Evaluación | Los tres métodos, las coincidencias y `outputs/grupos_l3.csv` |
| 8 | Despliegue | Hasta 30 artículos para leer, en `outputs/lectura_l3.csv` |

**Carpetas.** La celda de configuración crea `data/` (datos descargados) y `outputs/` (tablas y gráficos).

---

## Parte 1. Comprensión del negocio

### Paso 1. La pregunta de esta lección
Empezamos escribiendo lo que buscamos hoy.
La decisión principal se mantiene: qué artículos debe leer el colega nuevo.

| Pregunta | Respuesta para el laboratorio |
|----------|-------------------------------|
| ¿Qué buscamos? | Grupos de artículos que usan palabras parecidas |
| ¿Con qué los buscamos? | k-means, una mezcla gaussiana y HDBSCAN. |
| ¿Cómo los comparamos? | Con la silueta y viendo dónde coinciden k-means y HDBSCAN. |
| ¿Cómo entra un grupo en la lista? | k-means y HDBSCAN suman la parte de su grupo leído. |

Un artículo sin grupo no se borra. Se debería chequear a mano.

### Paso 2. Las palabras del tema
Antes de ver los grupos escribimos las palabras del tema: obesity, diet, diabetes y las formas cercanas.
No hay un tope para esa lista.
La lista de lectura sí tiene un tope: entre 10 y 30 artículos, `MIN_PAPERS` y `MAX_PAPERS`.
En la evaluación un grupo se lee cuando al menos la mitad de sus artículos tiene una de estas palabras.

```python
MIN_PAPERS = 10
MAX_PAPERS = 30
TOPIC_WORDS = {
    "obesity", "obese", "overweight",   # agregamos las palabras del peso a la lista del tema
    "diet", "dietary",                  # agregamos las palabras de la comida a la lista del tema
    "diabetes", "cardiovascular", "hypertension",   # agregamos las palabras de las enfermedades a la lista del tema
}
print("Palabras del tema:", ", ".join(sorted(TOPIC_WORDS)))
```

**Comprobar:**

Ahora comprobamos que las palabras del tema están escritas en minúsculas.

```python
assert MIN_PAPERS < MAX_PAPERS
assert len(TOPIC_WORDS) >= 5 and all(w == w.lower() for w in TOPIC_WORDS)
print("Palabras del tema: OK")
```

---

## Parte 2. Comprensión de los datos

### Paso 1. Librerías y carpetas
Como es usual el primer paso es importar las librerías y crear las carpetas donde vamos a guardar los datos.

```python
import math          # math.ceil redondea hacia arriba el umbral de soporte
import re            # re permite definir la expresión regular que filtra las palabras
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
import sklearn
from sklearn.cluster import HDBSCAN, KMeans  # KMeans asigna artículos a centros y HDBSCAN busca zonas densas
from sklearn.mixture import GaussianMixture  # GaussianMixture calcula una probabilidad por nube
from sklearn.decomposition import TruncatedSVD  # TruncatedSVD reduce las columnas a unas pocas direcciones
from sklearn.feature_extraction.text import CountVectorizer  # CountVectorizer cuenta las palabras de cada artículo
from sklearn.metrics import pairwise_distances, silhouette_score  # pairwise_distances arma las distancias y silhouette_score mide la separación
from sklearn.preprocessing import normalize  # normalize escala cada fila a magnitud 1

DATA_DIR = Path("data")         # Path fija la carpeta donde se guardan los datos descargados
OUTPUTS_DIR = Path("outputs")   # Path fija la carpeta donde se guardan las tablas y los gráficos
DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
print(f"scikit-learn {sklearn.__version__}")
```

### Paso 2. Parámetros
Como parte de la configuración fijamos los parámetros que usaremos en el proceso.
Los tres primeros vienen de la Lección 2.
Estos valores son una elección, y optimizarlos queda fuera de este curso.
En este cuaderno usamos estos valores fijos.

```python
SUPPORT_SHARE = 0.03   # fija la proporción de artículos que una palabra debe alcanzar
SUPPORT_MIN = 5        # fija el mínimo de artículos que una palabra debe alcanzar
SEED = 7               # fija el arranque aleatorio para que el ajuste se repita igual

MAX_WORD_SHARE = 0.5          # fija la proporción máxima de artículos en los que una palabra puede aparecer
DENSITY_SVD_DIRECTIONS = 10   # fija cuántas direcciones de la SVD usa HDBSCAN
MIXTURE_DIRECTIONS = 5         # fija cuántas direcciones de la SVD usa la mezcla
K_CANDIDATES = range(3, 9)    # range arma los valores de k que k-means va a probar
MIN_SAMPLES = SUPPORT_MIN     # copia el mínimo de soporte como min_samples de HDBSCAN
READ_SHARE = 0.5              # fija la proporción mínima del tema para que un grupo se lea
TOP_WORDS = 4                 # fija cuántas palabras se muestran de cada grupo


def support_floor(n_texts: int) -> int:
    """Soporte mínimo que necesita una palabra o un par: max(SUPPORT_MIN, ceil(SUPPORT_SHARE * n)).

    Qué hace: la misma función de la L2. En HDBSCAN es también el tamaño mínimo de un grupo.
    Entrada: n_texts, el número de textos.
    Salida: el umbral, un entero.
    """
    return max(SUPPORT_MIN, math.ceil(SUPPORT_SHARE * n_texts))   # max elige el mayor entre el mínimo fijo y el 3% redondeado hacia arriba


print(f"Umbral para 317 artículos: {support_floor(317)}")
```

**Comprobar:**

Comprobamos el umbral de soporte y los valores de k que vamos a probar.

```python
assert support_floor(317) == 10
assert MIN_SAMPLES == SUPPORT_MIN and list(K_CANDIDATES) == [3, 4, 5, 6, 7, 8]
assert MIXTURE_DIRECTIONS == 5
print("Parámetros: OK")
```

### Paso 3. Las palabras útiles
Un resumen trae palabras que no dicen el tema, como "the", "of", la etiqueta "methods" o el resto "http".
Esas palabras aparecen en muchos resúmenes y no separan un grupo de otro.
En este paso las quitamos, como en la Lección 2.
`word_list` conserva cada aparición, porque el conteo de más adelante las suma.
`words` deja cada palabra una sola vez, porque la regla del tema solo pregunta si está.

```python
from spacy.lang.en.stop_words import STOP_WORDS as STOP_WORDS_EN

WORD_RE = re.compile(r"[^\W\d_]+")   # re permite configurar una expresión regular para filtrar secuencias de letras
ABSTRACT_LABELS = {
    "background", "methods", "findings", "interpretation", "funding",
    "conclusions", "results", "objective", "objectives", "aims",
    "bill", "melinda", "gates", "foundation",
}
URL_TOKENS = {"http", "https", "www", "org"}
STOP_WORDS = set(STOP_WORDS_EN) | ABSTRACT_LABELS | URL_TOKENS   # unimos las palabras vacías, las etiquetas del resumen y los restos de direcciones
```

Las dos funciones de abajo hacen esa limpieza.

```python
def word_list(text: str, stop_words: set[str]) -> list[str]:
    """Convierte un texto en la lista de sus palabras útiles, con repeticiones.

    Qué hace: pasa a minúsculas, quita el residuo "[cita requerida]" de Wikipedia,
    separa en palabras de letras y descarta las de menos de 3 letras y las palabras vacías.
    Entrada: text (un resumen o una descripción) y stop_words, el conjunto de palabras vacías.
    Salida: una lista de palabras, en orden y con cada aparición.
    Por qué: para agrupar contamos cuántas veces usa un texto cada palabra.
    """
    text = (text or "").lower().replace("[cita requerida]", " ")  # lower pasa el texto a minúsculas y replace quita la marca de Wikipedia
    useful = []
    for word in WORD_RE.findall(text):  # findall extrae cada secuencia que pasó el filtro de letras
        long_enough = len(word) >= 3
        is_stop = word in stop_words  # in comprueba si la palabra está en el conjunto de palabras vacías
        if long_enough and not is_stop:
            useful.append(word)
    return useful


def words(text: str, stop_words: set[str]) -> set[str]:
    """Convierte un texto en el conjunto de sus palabras útiles (la función de la L2).

    Qué hace: la misma limpieza que word_list, pero guarda cada palabra una sola vez.
    Entrada: text y stop_words.
    Salida: un set de palabras.
    Por qué: los patrones de la L2 y la regla de lectura solo preguntan si una palabra está.
    """
    return set(word_list(text, stop_words))  # set deja cada palabra una sola vez


print(word_list("The diet, the DIET and the risk of obesity, see https://www.who.int", STOP_WORDS))
```

**Comprobar:**

En este paso comprobamos que `word_list` cuenta repeticiones y limpia igual que `words`.

```python
assert word_list("The diet, the DIET and the risk", STOP_WORDS) == ["diet", "diet", "risk"]
assert set(word_list("diet and risk, https://www.who.int", STOP_WORDS)) == words("diet and risk, https://www.who.int", STOP_WORDS)
print("Funciones de la L2: OK")
```

### Paso 4. Descargar los artículos
Los artículos están en `nutricion-papers.csv`, en la página del curso.
La función los descarga una sola vez y, si el archivo ya está, usa esa copia.
Cada fila trae el título y el resumen con los que vamos a agrupar.

```python
BASE_URL = "https://cabrerac.github.io/assets/data/26-udenar-data-mining"


def download_data(name: str, folder: Path = DATA_DIR) -> Path:
    """Descarga un archivo de datos del curso, una sola vez.

    Qué hace: si el archivo ya está en la carpeta, lo usa. Si no, lo descarga de BASE_URL.
    Entrada: name, el nombre del archivo, y folder, la carpeta destino.
    Salida: la ruta local del archivo.
    Por qué: no queremos depender de la red en cada ejecución ni descargar dos veces.
    """
    dest = folder / name
    if dest.is_file() and dest.stat().st_size > 0:  # is_file y stat comprueban que el archivo ya existe y no está vacío
        print(f"Ya en caché: {dest}")
        return dest
    response = requests.get(f"{BASE_URL}/{name}", timeout=60)  # requests.get pide el archivo a la página del curso
    response.raise_for_status()  # raise_for_status detiene la descarga si la página respondió con un error
    dest.write_bytes(response.content)
    print(f"Descargado: {dest} ({dest.stat().st_size / 1e6:.1f} MB)")
    return dest


papers = pd.read_csv(download_data("nutricion-papers.csv"), keep_default_na=False)
print(f"Artículos descargados: {len(papers)}")
```

**Comprobar:**

Comprobamos que el título y el resumen estén presentes en el dataframe `papers`.

```python
assert {"title", "abstract"} <= set(papers.columns)
print("Descarga: OK")
```

### Paso 5. Los artículos con resumen útil
Un resumen con menos de 5 palabras útiles no tiene con qué formar un grupo.
En este paso dejamos fuera esos resúmenes.
De los artículos descargados quedan 317.
Con 317 el piso de soporte, `FLOOR`, sale 10: el mayor entre 5 y el 3% de 317.

```python
useful = []
for abstract in papers["abstract"]:   # recorremos el resumen de cada artículo
    useful.append(len(words(abstract, STOP_WORDS)) >= 5)   # words cuenta las palabras útiles y nos quedamos con los resúmenes que tienen al menos 5
papers = papers[useful].reset_index(drop=True)
texts = papers["abstract"].tolist()
N = len(texts)
FLOOR = support_floor(N)
print(f"Artículos usados: {N} de {len(useful)}. Umbral: {FLOOR} artículos")
```

**Comprobar:**

Comprobamos el número de artículos usados y el umbral.

```python
assert N == 317 and FLOOR == 10
print("Datos: OK")
```

### Paso 6. Las palabras del tema en los resúmenes
Ahora, en los 317 resúmenes, contamos qué proporción contiene cada palabra del tema.
Una palabra que está en casi todos los resúmenes describe toda la colección y no nos permite distinguir un grupo.

```python
word_sets = []
for text in texts:
    word_sets.append(words(text, STOP_WORDS))   # words guarda el conjunto de palabras útiles de este resumen
shares = {}
for word in sorted(TOPIC_WORDS):   # recorremos cada palabra de la lista del tema
    with_word = 0
    for word_set in word_sets:
        if word in word_set:
            with_word += 1
    shares[word] = with_word / N   # dividimos los resúmenes que tienen la palabra entre el total
topic_share = pd.Series(shares).round(3)
print(topic_share.to_string())
```

¿Alguna de estas palabras distingue un grupo de otro? Aquí ninguna pasa de 14%.

**Comprobar:**

Comprobamos que hay una proporción por palabra del tema.

```python
assert len(topic_share) == len(TOPIC_WORDS) and topic_share.between(0, 1).all()
print("Palabras del tema en los resúmenes: OK")
```

---

## Parte 3. k-means

k-means parte de una tabla con una fila por artículo y una columna por palabra.
Cada fila queda de magnitud 1 para que el tamaño del resumen no pese más que el tema.

### Paso 1. Conteo de palabras con un vocabulario útil
Cada resumen ya está limpio y todavía trae las repeticiones de cada palabra.
En este paso armamos una tabla con una fila por artículo y una columna por palabra.
Una celda cuenta cuántas veces aparece esa palabra en ese resumen.
Para estos 317 artículos el piso es `FLOOR`, que vale 10.
Una palabra entra si aparece en al menos 10 artículos y en no más de la mitad, `MAX_WORD_SHARE` = 0,5.
Una palabra en pocos artículos, o en casi todos, no separa un grupo de otro.
`CountVectorizer` hace ese conteo.

```python
token_lists = []
for text in texts:
    token_lists.append(word_list(text, STOP_WORDS))   # word_list conserva cada aparición de la palabra
vectorizer = CountVectorizer(analyzer=lambda tokens: tokens, min_df=FLOOR, max_df=MAX_WORD_SHARE)  # CountVectorizer cuenta las palabras ya limpias y deja fuera las muy raras y las demasiado comunes
counts = vectorizer.fit_transform(token_lists)   # fit_transform arma la tabla de conteos, una fila por artículo
vocabulary = vectorizer.get_feature_names_out()  # get_feature_names_out devuelve la palabra que corresponde a cada columna
print(f"Tabla de conteos: {counts.shape[0]} artículos x {counts.shape[1]} palabras")
```

**Comprobar:**

Comprobamos la forma de la tabla y que no quedan restos de direcciones web.

```python
assert counts.shape == (317, 869)
assert not URL_TOKENS & set(vocabulary)
print("Conteos: OK")
```

### Paso 2. Escalar cada artículo a su vector unitario
La tabla de conteos tiene 317 filas y 869 columnas.
Un resumen largo suma más conteos que uno corto, aunque hablen del mismo tema.
En este paso `normalize` divide cada fila por su magnitud y la deja en 1.
Así la comparación mira la mezcla de palabras y no el largo del resumen.
La celda imprime el mínimo y el máximo de esas magnitudes. Los dos deben quedar en 1.

```python
X = normalize(counts)   # normalize divide cada fila por su magnitud para dejarla en 1
row_lengths = np.sqrt(X.multiply(X).sum(axis=1)).A1  # recalculamos la magnitud de cada fila para comprobar el escalado
print(f"Largo de las filas: mínimo {row_lengths.min():.3f}, máximo {row_lengths.max():.3f}")
```

**Comprobar:**

En este paso comprobamos que cada fila tenga magnitud 1.

```python
assert np.allclose(row_lengths, 1)
print("Filas de largo 1: OK")
```

---

## Parte 4. El ajuste de k-means

La tabla de conteos ya está lista. Cada fila tiene magnitud 1. Ahora buscamos los centros.

### Paso 1. Los centros
La tabla `X` tiene los 317 artículos y las 869 palabras, y cada fila ya tiene magnitud 1.
Un centro es el promedio de los artículos que cayeron en un grupo.
Probamos $k$ de 3 a 8 porque no sabemos de antemano cuántos grupos hay.
En cada prueba cada artículo va al centro más cercano, y el centro se mueve a ese promedio.
$J$ suma, para cada artículo, el cuadrado de su distancia al centro que le tocó.
La silueta, con distancia coseno, mide qué tan separado quedó ese $k$.
Nos quedamos con el $k$ de silueta más alta.
Buscamos minimizar $J = \sum_{i} \lVert x_i - \mu_{c(i)} \rVert^2$.

```python
kmeans_runs = {}
silhouettes = {}
for k in K_CANDIDATES:
    model = KMeans(n_clusters=k, n_init=10, random_state=SEED)  # KMeans prepara k centros y repite el arranque 10 veces
    model.fit(X)  # fit asigna cada artículo al centro más cercano y mueve los centros
    labels = model.labels_  # labels_ guarda el grupo de cada artículo
    kmeans_runs[k] = labels  # guardamos este agrupamiento para leer sus palabras después
    silhouettes[k] = silhouette_score(X, labels, metric="cosine")  # silhouette_score mide con distancia coseno qué tan separado quedó este k
    sizes = np.bincount(labels).tolist()  # bincount cuenta cuántos artículos cayeron en cada grupo
    print(f"k = {k}: tamaños {sizes}, silueta {silhouettes[k]:.3f}")
K_CHOSEN = max(silhouettes, key=silhouettes.get)  # nos quedamos con el k de silueta más alta
kmeans_labels = kmeans_runs[K_CHOSEN]  # estas son las etiquetas del k elegido
print(f"k elegido: {K_CHOSEN}")
```

**Comprobar:**

Ahora comprobamos que hay un agrupamiento por cada $k$ y que el $k$ elegido tiene la silueta más alta.

```python
assert list(kmeans_runs) == list(K_CANDIDATES)
for labels in kmeans_runs.values():
    assert len(labels) == N
assert K_CHOSEN in K_CANDIDATES and silhouettes[K_CHOSEN] == max(silhouettes.values())
print("k-means: OK")
```

### Paso 2. La figura de la silueta
En este paso dibujamos la silueta media de cada $k$, de 3 a 8.
Para un artículo, $a$ es la distancia coseno media a su grupo y $b$ al grupo vecino.
Su silueta es $(b - a) / \max(a, b)$, un número entre −1 y 1.
La silueta del $k$ es el promedio de esas siluetas sobre los 317 artículos.
Las líneas de 0,25 y 0,50 marcan las bandas de Kaufman y Rousseeuw.

```python
plt.figure(figsize=(6, 3.5))
plt.plot(list(silhouettes), list(silhouettes.values()), marker="o", color="steelblue")
plt.axhline(0.25, color="darkorange", linestyle="--", label="0,25 o menos: sin estructura sustancial")
plt.axhline(0.5, color="seagreen", linestyle="--", label="0,26 a 0,50: débil, podría ser artificial")
plt.ylim(0, 0.6)
plt.xlabel("k")
plt.ylabel("Silueta media (coseno)")
plt.title("Silueta de k-means para cada k")
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(OUTPUTS_DIR / "silueta_l3.png", dpi=120)
plt.show()
```

Debemos analizar la figura y el $k$ que se utilizó para generarla.
Si las siluetas quedan bajo la línea de 0,25, k-means no separó los artículos.
Es un resultado pobre pero normal en el proceso de minería.

### Paso 3. Las palabras de cada grupo
Hasta aquí un grupo es un número. Para leerlo miramos las palabras más frecuentes en los resúmenes de ese grupo.
La función promedia sus conteos escalados a 1 y se queda con las cuatro más altas.
La prueba de abajo ejecuta este paso con $k=3$. Esas cuatro palabras son las más frecuentes en los resúmenes de ese grupo.

```python
def group_words(labels: np.ndarray, group: int, n: int = TOP_WORDS) -> list[str]:
    """Las n palabras de más peso en el promedio de los artículos de un grupo.

    Entrada: labels, el grupo de cada artículo, group, el grupo que leemos, y n.
    Salida: una lista de n palabras.
    Por qué: un grupo sin etiqueta solo se puede leer por sus palabras.
    """
    centre = np.asarray(X[labels == group].mean(axis=0)).ravel()  # promediamos los conteos escalados de los artículos de este grupo
    order = np.argsort(centre)[::-1]  # argsort ordena las palabras de mayor a menor promedio
    top = []
    for j in order[:n]:
        top.append(str(vocabulary[j]))
    return top


print(group_words(kmeans_runs[3], 0))
```

**Comprobar:**

En este paso comprobamos que la función da `TOP_WORDS` palabras.

```python
assert len(group_words(kmeans_runs[3], 0)) == TOP_WORDS
print("Palabras de un grupo: OK")
```

---

## Parte 5. Mezcla gaussiana

La mezcla describe los artículos como nubes con forma de campana de Gauss.
Cada artículo recibe una probabilidad de pertenencia a una nube.
El número de nubes es el $k$ con mejor calificación de silueta obtenido en el método de k-means.
Aquí vemos cómo la selección de un hiperparámetro puede estar informada por otro método.

### Paso 1. Cinco direcciones
Nuestros datos tienen una fila por resumen y una columna por palabra, 317 filas por 869 columnas.
Una celda nos dice cuántas veces aparece una palabra en un resumen.
Pueden existir columnas que no sean independientes entre sí.
Una columna dependiente repite información que otra columna ya trae.
Esa repetición hace el modelo más complejo.
En este paso reducimos el número de columnas a 5.
Cada columna nueva, una dirección, mezcla columnas que dependen entre sí.
Para ello utilizamos la SVD.

```python
svd_mixture = TruncatedSVD(n_components=MIXTURE_DIRECTIONS, random_state=SEED)  # TruncatedSVD prepara las 5 direcciones
svd_mixture.fit(X)  # fit encuentra las direcciones que mezclan las columnas dependientes
Z_mixture = svd_mixture.transform(X)  # transform reemplaza las 869 columnas de cada artículo por 5 puntajes
variance_mixture = svd_mixture.explained_variance_ratio_.sum()  # explained_variance_ratio_ suma qué parte de la variación cubren esas direcciones
print(f"Las 5 direcciones explican {variance_mixture:.1%}")
print(f"Forma: {Z_mixture.shape}")
```

**Comprobar:**

Comprobamos la forma de las cinco direcciones.

```python
assert Z_mixture.shape == (N, MIXTURE_DIRECTIONS)
print("Direcciones de la mezcla: OK")
```

### Paso 2. El ajuste
Cada artículo ya es un punto con 5 puntajes, uno por dirección.
El número de nubes es el $k$ que eligió la silueta.
`covariance_type="full"` deja que cada nube tenga su propia forma.
`fit` calcula la probabilidad de cada artículo en cada nube y mueve los pesos, los centros y las formas.
La primera fila impresa es la probabilidad del primer artículo.
Las probabilidades de un artículo suman 1.

```python
mixture = GaussianMixture(n_components=K_CHOSEN, covariance_type="full", random_state=SEED)  # GaussianMixture prepara las nubes y deja que cada una tenga su propia forma
mixture.fit(Z_mixture)  # fit calcula las probabilidades y mueve los pesos, los centros y las formas
mixture_proba = mixture.predict_proba(Z_mixture)  # predict_proba escribe la probabilidad de cada artículo en cada nube
mixture_labels = mixture_proba.argmax(axis=1)  # argmax asigna cada artículo a la nube de probabilidad más alta
print("Probabilidad del primer artículo:", mixture_proba[0].round(2))
print(f"Tamaños: {np.bincount(mixture_labels).tolist()}")
```

**Comprobar:**

Ahora comprobamos que hay una etiqueta por artículo y que las probabilidades suman 1.

```python
assert len(mixture_labels) == N
assert np.allclose(mixture_proba.sum(axis=1), 1)
print("Mezcla gaussiana: OK")
```

### Paso 3. Cuántos artículos abriría
Cada artículo ya quedó en la nube de probabilidad más alta.
Un grupo se lee cuando al menos la mitad de sus artículos, `READ_SHARE` = 0,5, tiene una palabra del tema.
Esas palabras son las del inicio: obesity, obese, diet y las demás.
El número que imprime la celda es cuántos de los 317 artículos abriría la mezcla.

```python
has_topic = np.zeros(N, dtype=bool)
for i, word_set in enumerate(word_sets):
    has_topic[i] = bool(word_set & TOPIC_WORDS)


def topic_parts(labels: np.ndarray) -> np.ndarray:
    """La parte con palabras del tema del grupo de cada artículo, si ese grupo se lee.

    Qué hace: por cada grupo calcula qué parte de sus artículos tiene una palabra del tema.
    Si llega a READ_SHARE, el grupo se lee y sus artículos reciben esa parte.
    Si no, reciben 0.
    El ruido (-1) nunca se lee.
    Entrada: labels, el grupo de cada artículo.
    Salida: un arreglo con un número entre 0 y 1 por artículo.
    Por qué: un grupo con más artículos del tema da más evidencia que uno que apenas llega.
    """
    part = np.zeros(len(labels))
    for g in sorted(set(labels) - {-1}):
        in_g = labels == g
        share = has_topic[in_g].mean()
        if share >= READ_SHARE:
            part[in_g] = round(share, 2)
    return part


mixture_part = topic_parts(mixture_labels)
mixture_read = (mixture_part > 0).astype(int)
print(f"La mezcla abriría {mixture_read.sum()} artículos")
```

Analizamos cuántos artículos se recomiendan abrir de acuerdo a la mezcla. Esa cuenta supone nubes con forma de campana.
Si el número es alto, la suposición no ayudó a distinguir grupos. Nuevamente, este resultado es normal en el proceso de minería.

**Comprobar:**

Comprobamos que la cuenta de artículos abiertos no pasa del total.

```python
assert mixture_read.sum() <= N
print("Cuenta de la mezcla: OK")
```

---

## Parte 6. HDBSCAN

HDBSCAN busca zonas densas en nuestra colección de datos.
Lo que no cae en una zona densa es ruido y se conserva.
La preparación es la distancia coseno sobre 10 columnas o direcciones.

### Paso 1. Diez direcciones
Seguimos con la misma tabla, 317 filas por 869 columnas, ya escalada a magnitud 1.
Las columnas dependientes siguen repitiendo información.
La mezcla usó 5 direcciones porque una nube se describe con un centro y una forma.
HDBSCAN arma distancias entre artículos, y esas distancias necesitan más de la variación.
En este paso nos quedamos con 10 direcciones.
Cada dirección mezcla columnas que dependen entre sí.
`TruncatedSVD` hace esa reducción, y la celda imprime qué parte de la variación cubren las 10.

```python
svd = TruncatedSVD(n_components=DENSITY_SVD_DIRECTIONS, random_state=SEED)  # TruncatedSVD prepara las 10 direcciones de HDBSCAN
svd.fit(X)  # fit encuentra esas direcciones en la misma tabla de conteos escalados
Z = svd.transform(X)  # transform reemplaza las 869 columnas de cada artículo por 10 puntajes
variance_share = svd.explained_variance_ratio_  # explained_variance_ratio_ da la parte de la variación de cada dirección
print(f"Las 10 direcciones explican {variance_share.sum():.1%}")
```

**Comprobar:**

En este paso comprobamos la forma de `Z`.

```python
assert Z.shape == (N, DENSITY_SVD_DIRECTIONS)
print("SVD: OK")
```

### Paso 2. Distancias
`Z` tiene 317 artículos y 10 puntajes.
El coseno entre dos filas compara la mezcla de esos puntajes y deja fuera su magnitud.
Una distancia chica quiere decir que los dos artículos usan una mezcla parecida.
Una distancia grande los deja en una zona delgada.
En este paso `pairwise_distances` arma esa distancia entre cada par.
La tabla queda de 317 por 317, y cada artículo está a distancia 0 de sí mismo.

```python
distances = pairwise_distances(Z, metric="cosine")  # pairwise_distances calcula la distancia coseno entre cada par de artículos
print(f"Distancias: {distances.shape}")
```

**Comprobar:**

Comprobamos la forma de las distancias y que cada artículo está a 0 de sí mismo.

```python
assert distances.shape == (N, N) and np.allclose(np.diag(distances), 0, atol=1e-6)
print("Distancias: OK")
```

### Paso 3. El ajuste
HDBSCAN une primero los artículos con distancia chica y corta después los enlaces largos.
`FLOOR` vale 10 para estos 317 artículos.
Un lado del corte con menos de 10 artículos no forma grupo.
`min_samples` vale 5. La distancia núcleo de un artículo llega hasta su quinto vecino.
Lo que queda fuera de una zona densa se marca con −1 y se conserva.
Esos artículos pueden ser el único de su tema.
La celda imprime cuántos grupos hay y cuántos artículos quedaron como ruido.

```python
hdbscan_model = HDBSCAN(
    min_cluster_size=FLOOR,  # un grupo necesita al menos FLOOR artículos
    min_samples=MIN_SAMPLES,  # min_samples fija a qué vecino llega la distancia núcleo
    metric="precomputed",  # precomputed indica que la tabla ya trae las distancias
    copy=True,  # copy deja esa tabla sin cambios
)
hdbscan_model.fit(distances)  # fit arma el árbol, corta los enlaces largos y etiqueta los grupos
hdbscan_labels = hdbscan_model.labels_  # labels_ guarda el grupo de cada artículo y usa -1 para el ruido
n_groups = int(hdbscan_labels.max()) + 1  # el máximo más uno da el número de grupos, sin contar el ruido
in_group = hdbscan_labels != -1  # separamos los artículos que sí quedaron en un grupo
n_noise = int((~in_group).sum())  # contamos los artículos que quedaron como ruido
print(f"Grupos: {n_groups}. Tamaños: {np.bincount(hdbscan_labels[in_group]).tolist()}")
print(f"Ruido: {n_noise} artículos ({n_noise / N:.0%})")
```

Una vez más analizamos cuántos artículos se incluyen y cuántos quedaron como ruido.
Necesitamos conservar estos resúmenes porque nos informan sobre posibles artículos sin grupo.

**Comprobar:**

En este paso comprobamos que hay grupos y que el ruido se marca con un $-1$.

```python
assert n_groups >= 1
assert set(np.unique(hdbscan_labels)) <= set(range(-1, n_groups))
print("HDBSCAN: OK")
```

### Paso 4. La lista de ruido
Ahora examinamos el ruido. Un artículo sin vecinos claros puede ser el único de su tema.

```python
noise_list = papers.loc[~in_group, ["title", "year", "cited_by_count"]]
noise_list.sort_values("cited_by_count", ascending=False).head(5)
```

---

## Parte 7. Evaluación

La evaluación junta los tres métodos.
No hay marcas para los grupos, así que miramos la silueta, entre −1 y 1.
Entre 0,26 y 0,50 la estructura es débil y podría ser artificial (Kaufman y Rousseeuw, 1990).
Con 0,25 o menos no hay una estructura clara.
Un grupo se lee cuando al menos la mitad de sus artículos contiene una palabra clave del tema.
Un artículo que k-means y HDBSCAN ponen en un grupo leído es un candidato más fuerte.
Si el resultado de un método fue pobre, su fila sigue en la tabla.
En esta fase miramos las tres filas y decidimos cuáles resultados entran en la lista.

### Paso 1. Qué grupos se leen
En este paso aplicamos la regla de lectura a k-means y a HDBSCAN y utilizamos la cuenta que ya habíamos
calculado en la mezcla.

```python
part_of = {
    "kmeans": topic_parts(kmeans_labels),
    "mezcla": mixture_part,
    "hdbscan": topic_parts(hdbscan_labels),
}
read = {}
pairs = (("kmeans", kmeans_labels), ("hdbscan", hdbscan_labels))
for method, labels in pairs:
    read[method] = (part_of[method] > 0).astype(int)
    print(f"\n{method}: {read[method].sum()} artículos en grupos leídos")
    for g in sorted(set(labels) - {-1}):
        share = has_topic[labels == g].mean()
        mark = "lee" if share >= READ_SHARE else "no lee"
        top = ", ".join(group_words(labels, g))
        print(f"  grupo {g} ({(labels == g).sum()} artículos, {share:.0%} con el tema, {mark}): {top}")
read_kmeans = read["kmeans"]
read_hdbscan = read["hdbscan"]
```

Mire cuántos artículos caen en un grupo leído y qué palabras tiene cada grupo.
El ruido no se lee, pero nos informa cuáles artículos no tienen cosas en común con los demás.

**Comprobar:**

Comprobamos que el ruido no hace parte de nuestra lectura.

```python
assert not read_hdbscan[~in_group].any()
assert set(np.unique(read_kmeans)) <= {0, 1}
print("Grupos leídos: OK")
```

### Paso 2. La tabla de los tres métodos
En este paso reunimos grupos, ruido, silueta y artículos leídos.
La silueta de HDBSCAN se mide sin el ruido.
La de la mezcla se mide en sus cinco direcciones.

```python
def reading_of(score: float) -> str:
    """La lectura de una silueta con los cortes de Kaufman y Rousseeuw (1990).

    Qué hace: compara la silueta media con los tres cortes y devuelve su banda.
    Entrada: score, una silueta media entre -1 y 1.
    Salida: el nombre de la banda.
    Por qué: la silueta sola no dice si el grupo se puede usar.
    """
    if score > 0.70:
        return "estructura fuerte"
    if score > 0.50:
        return "estructura razonable"
    if score > 0.25:
        return "débil, podría ser artificial"
    return "sin estructura sustancial"


hdbscan_silhouette = np.nan
if n_groups > 1:
    hdbscan_silhouette = silhouette_score(X[in_group], hdbscan_labels[in_group], metric="cosine")  # silhouette_score mide la separación de HDBSCAN sin los artículos de ruido
mixture_silhouette = silhouette_score(Z_mixture, mixture_labels, metric="cosine")  # silhouette_score mide la separación de la mezcla en sus cinco direcciones
structure = pd.DataFrame({
    "method": ["k-means", "mezcla", "HDBSCAN"],
    "groups": [K_CHOSEN, K_CHOSEN, n_groups],
    "noise": [0, 0, n_noise],
    "silhouette": [silhouettes[K_CHOSEN], mixture_silhouette, hdbscan_silhouette],
    "leidos": [int(read_kmeans.sum()), int(mixture_read.sum()), int(read_hdbscan.sum())],
}).round(3)
structure["reading"] = structure["silhouette"].map(reading_of)
structure
```

Analizamos la silueta y la columna de leídos. k-means mete a todos en un grupo. HDBSCAN deja el ruido fuera de su silueta.
La fila de la mezcla es la cuenta que ya imprimimos. Si un resultado es pobre también es útil porque nos informa direcciones que debemos evitar en nuestra exploración.

**Comprobar:**

En este paso comprobamos que la tabla tiene los tres métodos.

```python
assert structure["method"].tolist() == ["k-means", "mezcla", "HDBSCAN"]
print("Tabla de los tres métodos: OK")
```

### Paso 3. Dónde coinciden k-means y HDBSCAN
En el paso anterior la mezcla no logró un subconjunto pequeño de artículos.
k-means tampoco separó bien los artículos: su silueta quedó por debajo de 0,25.
En este paso votan k-means y HDBSCAN.
Un artículo que los dos ponen en un grupo leído es un mejor candidato.
Esta regla no es general.
La decidimos nosotros, y esa decisión hace parte del proceso.

```python
group_points = read_kmeans + read_hdbscan  # sumamos cuántos de los dos métodos leen cada artículo
counts = pd.Series(group_points).value_counts()
group_agreement = counts.reindex(range(3), fill_value=0)
print(group_agreement.rename_axis("métodos que lo leen").to_frame("artículos").T.to_string())
```

Analizamos cuántos artículos leen los dos métodos y cuántos lee uno solo.

**Comprobar:**

Comprobamos que cada artículo cae en una sola cuenta.

```python
assert group_agreement.sum() == N
print("Coincidencias: OK")
```

### Paso 4. La figura de los tres métodos
Cada panel es un método y cada barra es un grupo.
La altura de la barra es el número de artículos de ese grupo.
La barra azul pasó la regla del tema. La gris no.
El título del panel dice cuántos artículos abriría ese método.

```python
method_labels = {
    "kmeans": kmeans_labels,
    "mezcla": mixture_labels,
    "hdbscan": hdbscan_labels,
}
fig, axes = plt.subplots(1, 3, figsize=(12, 3.2))
for ax, (method, labels) in zip(axes, method_labels.items()):
    names, sizes, colors = [], [], []
    for g in sorted(set(labels) - {-1}):
        names.append(str(g))
        sizes.append(int((labels == g).sum()))
        in_g = labels == g
        colors.append("steelblue" if part_of[method][in_g].max() > 0 else "lightgray")
    ax.bar(names, sizes, color=colors)
    opened = int((part_of[method] > 0).sum())
    ax.set_title(f"{method}: {opened} artículos")
    ax.set_xlabel("grupo")
axes[0].set_ylabel("artículos")
fig.tight_layout()
fig.savefig(OUTPUTS_DIR / "metodos_l3.png", dpi=120)
plt.show()
```

Mire las barras azules. Son los grupos que la regla del tema lee.

### Paso 5. Guardar los grupos
Guardamos una fila por cada uno de los 317 artículos en `outputs/grupos_l3.csv`.
Las columnas traen el grupo de k-means, el grupo de HDBSCAN y si ese grupo se lee.
`read_group` queda en verdadero cuando al menos uno de esos dos lo lee.
Este archivo es el resultado de esta lección.

```python
groups_table = pd.DataFrame({
    "title": papers["title"],
    "kmeans": kmeans_labels,
    "hdbscan": hdbscan_labels,
    "kmeans_leido": read_kmeans,
    "hdbscan_leido": read_hdbscan,
    "kmeans_parte": part_of["kmeans"],
    "hdbscan_parte": part_of["hdbscan"],
    "read_group": group_points >= 1,   # marcamos el artículo si k-means o HDBSCAN lo ponen en un grupo leído
})
groups_path = OUTPUTS_DIR / "grupos_l3.csv"
groups_table.to_csv(groups_path, index=False)
print(f"Guardado: {groups_path} ({len(groups_table)} filas)")
```

**Comprobar:**

En este paso comprobamos que el archivo tiene una fila por artículo y sus columnas.

```python
saved = pd.read_csv(groups_path)
assert {"title", "kmeans", "hdbscan", "kmeans_leido", "hdbscan_leido"} <= set(saved.columns)
assert {"kmeans_parte", "hdbscan_parte", "read_group"} <= set(saved.columns)
assert len(saved) == N
print("grupos_l3.csv: OK")
```

---

## Parte 8. Despliegue

### Paso 1. Qué hace un grupo con la lista
Un grupo leído es un filtro: los artículos que un método junta y que tratan del tema.
El archivo guarda los grupos de HDBSCAN.
Los artículos sin grupo siguen contados y no entran en la lista.
La cuenta de la mezcla queda en la tabla de la evaluación.
La lista suma solo k-means y HDBSCAN, los dos votos de esta lección.

### Paso 2. Artículos para leer
Cada método que pone un artículo en un grupo leído suma la parte de ese grupo con palabras del tema, entre 0,5 y 1.
La evidencia es la suma, de 0 a 2.
Un grupo en el que casi todos los artículos tienen el tema pesa más que uno que apenas llega a la mitad.
Ordenamos de mayor a menor evidencia y, si empatan, por título.
De los 317 mostramos como máximo 30, el tope de la Lección 1.
Esta lista usa solo los grupos de hoy.

```python
reading_rows = []
for i in range(N):   # recorremos cada artículo
    evidencia = part_of["kmeans"][i] + part_of["hdbscan"][i]   # sumamos la parte de k-means y la parte de HDBSCAN
    if evidencia == 0:
        continue   # saltamos el artículo cuando los dos métodos le dan evidencia 0
    reading_rows.append({
        "title": papers.loc[i, "title"],
        "kmeans": part_of["kmeans"][i],
        "hdbscan": part_of["hdbscan"][i],
        "evidencia": round(evidencia, 2),
    })

reading = pd.DataFrame(reading_rows)
reading = reading.sort_values(["evidencia", "title"], ascending=[False, True])   # sort_values ordena de mayor a menor evidencia y, si empatan, por título
reading_list = reading.head(MAX_PAPERS)   # head corta la lista en 30 artículos
reading_path = OUTPUTS_DIR / "lectura_l3.csv"
reading_list.to_csv(reading_path, index=False)
print(f"Artículos con alguna evidencia: {len(reading)}. En la lista: {len(reading_list)}.")
reading_list.head(10)
```

Examinamos cuántos artículos tienen alguna evidencia y cuántos entran en la lista. Arriba quedan los que leen los dos métodos.
Si hay varias ediciones de la misma guía, el equipo abre la más reciente.

**Comprobar:**

En este paso comprobamos el largo de la lista, su orden y que la evidencia es la suma de los dos métodos.

```python
assert len(reading_list) == min(MAX_PAPERS, len(reading)) and reading_list["evidencia"].min() > 0
assert reading_list["evidencia"].is_monotonic_decreasing
assert ((reading_list["evidencia"] - reading_list["kmeans"] - reading_list["hdbscan"]).abs() < 0.011).all()
print("Lista de lectura: OK")
```

En esta iteración intentamos agrupar los 317 resúmenes.
Los métodos explorados no funcionaron adecuadamente para separar los artículos.
En el caso de k-means las siluetas quedaron bajo 0,25 para todo k de 3 a 8.
La mezcla Gaussiana no refinó el conjunto.
HDBSCAN formó grupos y dejó fuera los resúmenes sin vecinos.
La lista resultante es una respuesta débil a la pregunta que el laboratorio nos plantea.

La principal razón detrás de estos resultados es que los datos ya pertenecen a un grupo (i.e., nutrición) y los subgrupos existentes no marcan una diferencia entre sí.
A pesar de esto, la iteración nos informa el tipo de métodos que presentaría limitaciones en los datos que estamos analizando.
Estos hallazgos deben reportarse como parte del proceso de minería y al mismo tiempo informar futuras iteraciones.

<!-- end NOTEBOOK: -->
