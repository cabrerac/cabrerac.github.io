<!-- NOTEBOOK: -->

## Repaso de Python para este cuaderno

Este cuaderno utiliza los siguientes métodos de Python.

### Leer una tabla con `pandas`
`pd.read_csv` lee un archivo CSV y devuelve un **DataFrame**, una tabla con filas y columnas con nombre. `df.shape` dice cuántas filas y columnas tiene.

```python
import pandas as pd

mini = pd.DataFrame({"title": ["A", "B", "C"], "year": [2010, 2015, 2020]})
print(mini.shape)
mini
```

### Texto con `f"..."`
Una cadena con `f` delante inserta variables dentro del texto, entre llaves. Después de `:` se puede dar formato, por ejemplo `:,` para separar miles.

```python
n_papers = 320
max_citations = 54824
print(f"La colección tiene {n_papers} artículos. El más citado tiene {max_citations:,} citas.")
```

### Filtrar filas
Una condición dentro de `loc` deja solo las filas que la cumplen.
`&` pide que se cumplan dos condiciones.

```python
recent = mini.loc[(mini["year"] >= 2015) & (mini["title"] != "A")]
print(recent)
```

### Una columna de texto
`.str` aplica una operación de texto a toda la columna.

```python
titles = pd.Series(["obesity risk", "diet study", "climate"])
print(titles.str.contains("diet"))
```

### Un histograma
`plt.hist` cuenta cuántos valores caen en cada intervalo. Parte el rango en intervalos del mismo ancho. La cantidad de valores en cada intervalo puede ser distinta. `bins=4` pide cuatro intervalos. En este caso el valor más pequeño es 1 y el más grande es 8. El ancho de cada intervalo es (8 - 1) / 4 = 1.75. Los cortes quedan en 1, 2.75, 4.5, 6.25 y 8. Cada valor entra en el intervalo que lo contiene. El último intervalo incluye el 8. 1, 2 y 2 caen en el primero. El 3 cae en el segundo. El tercero queda vacío. El 8 cae en el cuarto. La altura de la barra es cuántos valores cayeron ahí. Una barra vacía es un hueco entre valores.

```python
import matplotlib.pyplot as plt

plt.hist([1, 2, 2, 3, 8], bins=4, color="steelblue")
plt.xlabel("Valor")
plt.ylabel("Cuántos")
plt.show()
```

### Una función
`def` guarda unos pasos con un nombre.
`return` devuelve el resultado.

```python
def in_range(n: int, low: int, high: int) -> bool:
    """Dice si un número está entre dos límites, incluidos los dos."""
    return low <= n <= high
```

### Comprobar con `assert`
`assert` detiene el cuaderno si una condición es falsa.
Las celdas **Comprobar** usan este patrón, como en todos los cuadernos del curso.

```python
assert in_range(20, 10, 30)
print("Repaso de Python: OK")
```

---

## Instrucciones

Usted es parte de un equipo interno de una alcaldía, en la secretaría de salud. La secretaría tiene una base de artículos científicos sobre nutrición. El equipo debe decidir **qué artículos tiene que leer** un colega que llega al equipo. Durante el curso construiremos esa lista paso a paso, una familia de métodos por lección.

Esta lección trata de lo que pasa **antes** de minar: escribir la pregunta, mirar los datos con calma y decidir qué es una buena respuesta. Seguimos **CRISP-DM**, la metodología del curso. Sus seis fases son las secciones de todos los cuadernos del curso.

**Qué hacer.** Ejecute las celdas de arriba hacia abajo. Cada paso empieza con **En este paso**. Si el paso tiene código, termina con una celda **Comprobar**. El cuaderno de grupo le pedirá escribir la misma pregunta para su secretaría.

**Mapa del cuaderno**

| Parte | Fase CRISP-DM | Qué sale |
|-------|---------------|----------|
| 1 | Comprensión del negocio | La pregunta y el estándar, escritos en el cuaderno |
| 2 | Comprensión de los datos | Tabla de perfil y un histograma de citas |
| 3 | Preparación de los datos | Una revisión, no una limpieza |
| 4 | Modelado | Se explora en las siguiente lecciones |
| 5 | Evaluación | El estándar como función `meets_standard` |
| 6 | Despliegue | El alcance de la lista |

**Carpetas.** La celda de configuración, en la Parte 2, crea `data/` (datos descargados) y `outputs/` (tablas y gráficos).

---

## Parte 1. Comprensión del negocio

### Paso 1. El equipo y la decisión
En este paso definimos quién decide, qué decide y el alcance de la decisión. Esta definición es clave porque tiene influencia en el resto del proceso.

| Pregunta | Respuesta para el laboratorio |
|----------|-------------------------------|
| ¿Quién usa la lista? | El equipo interno de la secretaría de salud |
| ¿Qué decide la lista? | Qué artículos abrir y leer para su trabajo sobre nutrición |
| Alcance de la lista | Elige qué artículos abrir. No es evidencia oficial de la alcaldía y no reemplaza leer los artículos |
| ¿Cuándo la lista es aceptable? | Tiene entre 10 y 30 artículos, y como máximo la mitad entró solo por las citas |

El estándar se escribe antes de mirar los resultados. Dicho estándar cambia de acuerdo al problema en cuestión y a nuestro conocimiento del mismo. En este caso podríamos incluir artículos dependiendo del número de citaciones. Sin embargo, un artículo muy citado puede ser una revisión de literatura o un artículo de otro tema que cita todo el mundo. La cantidad de citas mide popularidad, no si el artículo sirve para el trabajo del equipo.

---

## Parte 2. Comprensión de los datos

### Paso 1. Configuración
En este paso importamos las librerías y creamos las carpetas donde almacenaremos los datos.
`pandas` es la tabla.
`matplotlib` es la figura.
`requests` descarga el archivo.
`Path` es el nombre de una carpeta.
`data/` guarda el CSV.
`outputs/` guarda el perfil y el histograma.

```python
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import requests

DATA_DIR = Path("data")  # aquí queda el CSV
OUTPUTS_DIR = Path("outputs")  # aquí quedan el perfil y el histograma
DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
print("Carpetas listas:", DATA_DIR, OUTPUTS_DIR)
```

**Comprobar:**

```python
assert DATA_DIR.is_dir() and OUTPUTS_DIR.is_dir()
print("Configuración: OK")
```

### Paso 2. Descargar los artículos
En este paso descargamos `nutricion-papers.csv` del sitio del curso. La función guarda el archivo en `data/` y no lo vuelve a descargar si ya está. Es el mismo patrón de caché de los cuadernos de Big Data pero esta vez asumimos que los datos están disponibles para su análisis.

```python
BASE_URL = "https://cabrerac.github.io/assets/data/26-udenar-data-mining"


def download_data(name: str, folder: Path = DATA_DIR) -> Path:
    """Descarga un archivo de datos del curso, una sola vez.

    Qué hace: si el archivo ya está en la carpeta, lo usa. Si no, lo descarga de BASE_URL.
    Entrada: name, el nombre del archivo (por ejemplo "nutricion-papers.csv"), y folder, la carpeta destino.
    Salida: la ruta local del archivo.
    """
    dest = folder / name
    if dest.is_file() and dest.stat().st_size > 0:  # usa el archivo si ya está
        print(f"Ya en caché: {dest}")
        return dest
    response = requests.get(f"{BASE_URL}/{name}", timeout=60)
    response.raise_for_status()
    dest.write_bytes(response.content)
    print(f"Descargado: {dest} ({dest.stat().st_size / 1e6:.1f} MB)")
    return dest


papers_path = download_data("nutricion-papers.csv")
```

**Comprobar:**

En este paso comprobamos la descarga exitosa.

```python
assert papers_path.is_file() and papers_path.stat().st_size > 500_000
print("Descarga: OK")
```

### Paso 3. Exploración
En este paso cargamos el archivo y miramos su forma y sus columnas.

```python
papers = pd.read_csv(papers_path)  # una fila por artículo
print(f"Filas: {papers.shape[0]}  |  Columnas: {papers.shape[1]}")
papers.head(3)
```

Cada fila es un artículo. Estas son las columnas que usaremos:

| Columna | Qué es | Lección que la usa |
|---------|--------|--------------------|
| `title`, `abstract` | Título y resumen. El resumen es la descripción del artículo que vamos a leer | L2 (patrones), L3 (grupos), L4 (texto) |
| `year`, `cited_by_count` | Año y número de citas | L1 (perfil) |
| `topics`, `links` | Temas de OpenAlex y citas dentro de la colección | L5 (enlaces) |
| `field` y las demás | Campo y atributos del artículo | L6 (predicción) |

```python
papers.dtypes
```

**Comprobar:**

En este paso comprobamos que la forma y las columnas de los datos sean correctas.

```python
assert papers.shape == (320, 13)
assert {"title", "abstract", "year", "cited_by_count"} <= set(papers.columns)
print("Forma de los datos: OK")
```

### Paso 4. Valores faltantes
En este paso contamos las celdas vacías por columna. Un vacío puede ser un error o puede ser normal. Hay que mirarlo antes de decidir.

```python
missing = papers.isna().sum()  # celdas vacías por columna
missing[missing > 0]
```

Dos columnas tienen vacíos. `links` está vacío en 175 artículos. Es normal: muchos artículos no citan a otro artículo de esta misma colección. El `abstract`, que es lo que más usaremos, no tiene vacíos.

**Comprobar:**

En este paso comprobamos los valores esperados.

```python
assert missing["links"] == 175 and missing["venue_type"] == 3
assert missing["abstract"] == 0
print("Faltantes: OK")
```

### Paso 5. Largo de los resúmenes
En este paso contamos las palabras de cada resumen. Un resumen muy corto no es un resumen. Puede ser una portada o una nota de la revista.

```python
papers["abstract_words"] = papers["abstract"].str.split().str.len()  # palabras de la descripción de cada artículo
print(papers["abstract_words"].describe().round(0))
short_abstracts = papers[papers["abstract_words"] < 20]
print(f"\nResúmenes de menos de 20 palabras: {len(short_abstracts)}")
short_abstracts[["title", "abstract"]].head(4)
```

Ocho resúmenes tienen menos de 20 palabras. Por ejemplo, "Peer Reviewed" o la frase de una portada. En la Lección 2 decidimos qué hacer con ellos dependiendo del método.

**Comprobar:**

En este paso comprobamos los valores esperados con respecto a la longitud de los abstracts.

```python
assert len(short_abstracts) == 8
print("Largo de los resúmenes: OK")
```



### Paso 6. Años e idioma
En este paso miramos de cuándo son los artículos y en qué idioma están.

```python
print(f"Años: de {papers['year'].min()} a {papers['year'].max()}")
print(papers["language"].value_counts())
papers.loc[papers["language"] != "en", ["title", "language"]]
```

Casi todo está en inglés. Hay un artículo en polaco. Para algunos métodos el lenguaje es importante.

**Comprobar:**

En este paso comprobamos los valores esperados de nuestros datos.

```python
assert (papers["language"] == "en").sum() == 319
assert papers["year"].between(1980, 2024).all()
print("Años e idioma: OK")
```

### Paso 7. Citas
En este paso miramos el número de citas de cada artículo.

```python
print(papers["cited_by_count"].describe().round(0))
median_citations = papers["cited_by_count"].median()
print(f"\nMediana de citas: {median_citations:,.0f}")
```

El histograma parte el número de citas en 40 intervalos y cuenta cuántos artículos caen en cada uno.
La línea naranja es la mediana.
La mayoría de las barras queda a la izquierda, así que unos pocos artículos muy citados estiran la cola.
El gráfico se guarda en `outputs/histograma_citas.png`.

```python
plt.figure(figsize=(7, 4))
plt.hist(papers["cited_by_count"], bins=40, color="steelblue")  # 40 intervalos
plt.axvline(median_citations, color="darkorange", linestyle="--", label=f"mediana = {median_citations:,.0f}")  # la mediana
plt.xlabel("Citas del artículo")
plt.ylabel("Número de artículos")
plt.title("Citas de los 320 artículos")
plt.legend()
plt.tight_layout()
plt.savefig(OUTPUTS_DIR / "histograma_citas.png", dpi=120)  # la figura guardada
plt.show()
```

La mayoría tiene unos pocos miles de citas y unos pocos tienen decenas de miles. El más citado, *Global cancer statistics*, ni siquiera es de nutrición.

**Comprobar:**

Una vez más, comprobamos los resultados de nuestra exploración.

```python
assert papers["cited_by_count"].max() == 54824
assert (OUTPUTS_DIR / "histograma_citas.png").is_file()
print("Citas: OK")
```

### Paso 8. Cómo se construyó la colección
En este paso leemos cómo se armó la colección. Esto es parte de comprender los datos, porque explica lo que **no** está.

Los artículos vienen de **OpenAlex**, una base abierta de publicaciones. Se pidieron artículos del tema nutrición **que tuvieran resumen**, y se tomaron los **más citados**. Por eso incluso el menos citado tiene muchas citas.

```python
print(f"El artículo menos citado de la colección tiene {papers['cited_by_count'].min():,} citas.")
```
Consecuencia: la colección **ya es una muestra de popularidad**. Si filtramos otra vez por citas, solo repetimos el criterio con que se construyó. Por eso el estándar dice que un número alto de citas por sí solo no es un filtro. Los filtros del curso tienen que mirar el contenido.

### Paso 9. Tabla de perfil
En este paso juntamos lo visto en una tabla de perfil y la guardamos. El perfil resume una columna en una fila de la tabla.

```python
def profile_column(series: pd.Series) -> dict:
    """Resume una columna en una fila de la tabla de perfil.

    Qué hace: cuenta valores, vacíos y valores distintos, y da un ejemplo.
    Entrada: una columna del DataFrame (pandas Series).
    Salida: un diccionario con tipo, vacíos, distintos y ejemplo.
    """
    non_missing = series.dropna()
    return {
        "dtype": str(series.dtype),
        "missing": int(series.isna().sum()),
        "distinct": int(series.nunique()),
        "example": str(non_missing.iloc[0])[:40] if len(non_missing) else "",
    }

profile = pd.DataFrame({col: profile_column(papers[col]) for col in papers.columns}).T  # una fila por columna
profile.to_csv(OUTPUTS_DIR / "perfil_datos.csv")
profile
```

**Comprobar:**

Comprobamos que el archivo del perfil se almacenó satisfactoriamente.

```python
assert len(profile) == papers.shape[1]
assert (OUTPUTS_DIR / "perfil_datos.csv").is_file()
print("Perfil: OK")
```

---

## Parte 3. Preparación de los datos

Hoy la preparación es una **revisión, no una limpieza**. La razón es que cada método de las próximas lecciones pide su propia preparación. Si limpiamos hoy para un método, podemos dañar la entrada de otro.

### Paso 1. Duplicados y vacíos
En este paso revisamos si hay artículos repetidos.

```python
print(f"Títulos repetidos: {papers['title'].duplicated().sum()}")  # un título que aparece más de una vez
print(f"Resúmenes repetidos: {papers['abstract'].duplicated().sum()}")
papers[papers["title"].duplicated(keep=False)][["title", "year", "cited_by_count"]]
```

Hay dos títulos repetidos. Son declaraciones de consenso que se publicaron en dos revistas a la vez, y OpenAlex guarda un registro por revista. Una de ellas (CONSORT 2010, extensión de 2016) tiene además el mismo resumen en los dos registros. Hoy solo lo anotamos. No borramos nada, porque la decisión depende del método: para contar pares en la Lección 2, un resumen repetido suma dos veces, pero dos artículos no alcanzan el umbral de 10 y no forman un patrón por sí solos.


**Comprobar:**

En este paso comprobamos los datos esperados para los artículos duplicados.

```python
assert papers["title"].duplicated().sum() == 2
assert papers["abstract"].duplicated().sum() == 1
print("Duplicados revisados: OK")
```

### Paso 2. Un resumen, tres preparaciones
En este paso vemos, con un solo resumen, tres diferentes tratamientos. Primero seleccionamos un resumen determinado.

```python
import re
from collections import Counter

text = papers.loc[1, "abstract"]  # la descripción de un artículo
text_words = [w for w in re.findall(r"[^\W\d_]+", text.lower()) if len(w) >= 3]  # palabras de 3 letras o más
print(text[:250], "...")
print(f"\nPalabras: {len(text_words)}")
```

Después lo tratamos como una lista, como un conjunto y como conteo de palabras.

```python
word_set = set(text_words)  # cada palabra una sola vez
word_counts = Counter(text_words)  # cuántas veces aparece cada palabra
print(f"Como lista: {len(text_words)} palabras")
print(f"Como conjunto: {len(word_set)} palabras distintas")
print(f"Como conteo, las más repetidas: {word_counts.most_common(5)}")
```

Fíjese en que las palabras más repetidas son "the", "and", "of". No dicen nada del tema.

**Comprobar:**

Una vez más comprobamos los datos explorados.

```python
assert len(word_set) <= len(text_words)
print("Vista previa de preparación: OK")
```

---

## Parte 4. Modelado

Esta etapa de la metodología se explorará en detalle en las siguientes lecciones.

---

## Parte 5. Evaluación

### Paso 1. El estándar como función
En este paso convertimos el estándar definido anteriormente en una función. Así cualquier lista se puede comprobar bajo las mismas condiciones. Una lista es una tabla con al menos las columnas `title` y `filter` (el nombre del filtro que puso cada artículo).

```python
MIN_PAPERS = 10  # la lista tiene al menos 10 artículos
MAX_PAPERS = 30  # y como mucho 30
MAX_SHARE_CITATIONS_ONLY = 0.5  # como máximo la mitad entró solo por las citas


def meets_standard(reading_list: pd.DataFrame, collection: pd.DataFrame = papers) -> tuple[bool, list[str]]:
    """Comprueba si una lista de artículos cumple el estándar.

    Args:
        reading_list: Tabla con las columnas title y filter.
        collection: Colección completa, con title y cited_by_count.
    Returns:
        Si la lista cumple, y las reglas que no cumple.
    """
    reasons = []
    n = len(reading_list)
    if n < MIN_PAPERS:
        reasons.append(f"tiene {n} artículos, el mínimo es {MIN_PAPERS}")
    if n > MAX_PAPERS:
        reasons.append(f"tiene {n} artículos, el máximo es {MAX_PAPERS}")
    if reading_list["filter"].isna().any() or (reading_list["filter"].astype(str).str.strip() == "").any():
        reasons.append("algún artículo no dice qué filtro lo puso")
    most_cited = set(collection.nlargest(MAX_PAPERS, "cited_by_count")["title"])  # los 30 más citados de la colección
    citations_only = reading_list["title"].isin(most_cited) & (reading_list["filter"] == "citas")  # entraron solo por las citas
    if n and citations_only.mean() > MAX_SHARE_CITATIONS_ONLY:
        reasons.append(f"{citations_only.mean():.0%} de la lista viene solo de las citas")
    return len(reasons) == 0, reasons
```

### Paso 2. Probar el estándar con dos listas ejemplo
En este paso probamos la función con dos listas de ejemplo. a primera lista toma los 20 artículos más citados. La segunda toma artículos cuyo resumen menciona *obesity* y *children*.

```python
citation_list = papers.nlargest(20, "cited_by_count")[["title"]].assign(filter="citas")  # los 20 artículos más citados
citations_ok, citation_reasons = meets_standard(citation_list)
print("Lista por citas:", "cumple" if citations_ok else "no cumple", citation_reasons)

mentions = papers["abstract"].str.contains("obesity", case=False) & papers["abstract"].str.contains("children", case=False)  # la descripción menciona las dos palabras
topic_list = papers.loc[mentions, ["title"]].head(30).assign(filter="resumen menciona obesity y children")  # como máximo 30 de esos artículos
topic_ok, topic_reasons = meets_standard(topic_list)
print(f"Lista por tema ({len(topic_list)} artículos):", "cumple" if topic_ok else "no cumple", topic_reasons)
```

La lista por citas toma los 20 artículos más citados. Tiene buen tamaño, pero repite cuáles artículos ya eran famosos. No cumple, porque más de la mitad entró solo por las citas. La lista por tema toma artículos cuya descripción menciona obesity y children. Cumple el tamaño.

**Comprobar:**

Comprobamos el resultado esperado.

```python
assert citations_ok is False
assert topic_ok is True
print("Estándar: OK")
```

---

## Parte 6. Despliegue

### Paso 1. El alcance de la lista
En este paso el despliegue es entregar la lista al equipo y decir hasta dónde llega.

| Dentro del alcance | Fuera del alcance |
|--------------------|-------------------|
| Decidir qué artículos abre primero el equipo de nutrición | Citar la lista como evidencia de la alcaldía |
| Usarla para este tema, en esta secretaría | Usarla en otra secretaría, o con otro tema, sin rehacerla |
| Cambiarla cuando cambia el tema | Tratarla como si la lectura ya estuviera hecha |

<!-- end NOTEBOOK: -->
