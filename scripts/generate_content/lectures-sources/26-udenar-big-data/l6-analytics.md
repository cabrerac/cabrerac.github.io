---
course_code: 26-udenar-big-data
title: Analytics and visualisation
description: Lecture 6 presents analytics and visualisation techniques. Once we have processed, harmonised, and ingested our data, the next step is to use to solve the data problems at hand (i.e., address). Visualisation tools support decision makers by presenting data in formats that are easier to understand and analyse in context (e.g., dashboards). More advanced analytics are possible when probabilistic models support prediction or classification processes.
session: 6
start_time: 07:00 am
end_time: 01:00 pm
hours: 5
author: Christian Cabrera Jojoa
email: chc79@cam.ac.uk
position: Assistant Research Professor
department: Department of Computer Science and Technology
institution: University of Cambridge
layout: lecture
lecture_code: l6-analytics
lecture_date: 20/06/2026
permalink: /teaching/26-udenar-big-data/l6-analytics/
visible: true
group_notebook: week-3-group
notebook_language: es
notebook_title: Analítica y visualización
notebook_description: Práctica individual de la Lección 6. Armamos un tablero con varias vistas del territorio (mapa del indicador laboral por departamento, burbujas sobre OpenStreetMap, tendencia mensual y servicios OSM vs. empleo), luego modelamos los agregados GEIH con regresión lineal explicable y discutimos cómo presentar evidencia a quien decide.
---

<!-- SLIDES: -->

# Last Time

<!-- end SLIDES: -->

{% include _snippets/26-udenar-big-data/l6-analytics/last-time.md %}

<!-- SLIDES: -->

# Analytics

<!-- end SLIDES: -->

{% include _snippets/26-udenar-big-data/l6-analytics/analytics.md %}

<!-- SLIDES: -->

# Visualisation

<!-- end SLIDES: -->

{% include _snippets/26-udenar-big-data/l6-analytics/visualisation.md %}

<!-- SLIDES: -->

# Data Address

<!-- end SLIDES: -->

{% include _snippets/data-address.md %}

<!-- SLIDES: -->

# Supervised Learning

<!-- end SLIDES: -->

{% include _snippets/26-udenar-big-data/l6-analytics/supervised-learning.md %}

<!-- SLIDES: -->

# Conclusions

<!-- end SLIDES: -->

{% include _snippets/26-udenar-big-data/l6-analytics/conclusions.md %}

{% include _snippets/26-udenar-big-data/l6-analytics/practical-slides.md %}

<!-- RENDER: -->

### Week 3 links

- [Week 3 hub](/teaching/26-udenar-big-data/week-3-hub-es/)

### Resources

- [Introductory Python course](https://www.youtube.com/watch?v=nKPbfIU442g) (optional video)
- [scikit-learn user guide](https://scikit-learn.org/stable/user_guide.html) (reference)

### References

- Zaharia, M., et al. (2016). [Apache Spark: a unified engine for big data processing](https://doi.org/10.1145/2934664). *CACM*, 59(11), 56–65.
- Jarrahi, M. H., et al. (2023). *The Principles of Data-Centric AI*. *(Course PDF.)*

<!-- end RENDER: -->

<!-- NOTEBOOK: -->

## Repaso de Python para este cuaderno

En esta lección **modelamos y visualizamos** para responder una pregunta de decisión. Lo nuevo frente a las lecciones anteriores son tres ideas de aprendizaje automático con **`scikit-learn`**: separar datos, entrenar un modelo y medir qué tan bien predice. Trabajamos **siempre sobre agregados** (departamento × mes), **nunca** sobre microdatos de personas ni texto de noticias.

### Separar datos en entrenamiento, validación y prueba

Para saber si un modelo **generaliza** (no solo memoriza) usamos **tres** subconjuntos:

- **Entrenamiento** (*train*): el modelo **aprende** con estos datos.
- **Validación** (*validation*): comparamos modelos y **elegimos** el mejor (sin tocar la prueba).
- **Prueba** (*test*): la evaluación **final e imparcial**, con datos que nunca se usaron para decidir.

`train_test_split` separa en dos; para obtener tres, lo aplicamos **dos veces**: primero apartamos la prueba, luego dividimos el resto en entrenamiento y validación.

```python
from sklearn.model_selection import train_test_split

# Datos de juguete: x va de 1 a 8, y es 10 veces x
X = [[1], [2], [3], [4], [5], [6], [7], [8]]
y = [10, 20, 30, 40, 50, 60, 70, 80]

# 1) Apartamos el 25 % para la prueba final
X_tmp, X_test, y_tmp, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
# 2) Del resto, apartamos un tercio para validación
X_train, X_val, y_train, y_val = train_test_split(X_tmp, y_tmp, test_size=0.33, random_state=42)

print("Entrenamiento:", len(X_train), "| Validación:", len(X_val), "| Prueba:", len(X_test))
assert len(X_test) == 2 and len(X_val) >= 1
print("train/val/test: OK")
```

### Entrenar una regresión lineal

Un modelo **lineal** busca la recta que mejor relaciona la entrada con la salida. **`fit`** aprende; **`predict`** estima para datos nuevos. En un gráfico vemos **puntos** (datos) y la **recta** (ajuste): cuanto más cerca queden los puntos de la recta, mejor predice.

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Datos de juguete con un poco de ruido (no caen exactamente en y = 2x)
X_demo = np.array([[1.0], [2.0], [3.0], [4.0]])
y_demo = np.array([2.0, 4.1, 5.9, 8.2])

modelo = LinearRegression()
modelo.fit(X_demo, y_demo)
x_line = np.linspace(0.5, 4.5, 100).reshape(-1, 1)

plt.figure(figsize=(5, 3))
plt.scatter(X_demo, y_demo, color="steelblue", label="datos")
plt.plot(x_line, modelo.predict(x_line), "r--", label="ajuste lineal")
plt.xlabel("x")
plt.ylabel("y")
plt.title("Repaso: la recta que mejor ajusta los puntos")
plt.legend()
plt.tight_layout()
plt.show()

pred = modelo.predict([[4.0]])[0]
print("Predicción para x=4:", round(pred, 2))
assert abs(pred - 8.0) < 0.5
print("LinearRegression: OK")
```

### Medir el error: R² y MAE

Necesitamos números para comparar modelos:

- **R²** (entre 0 y 1): qué fracción de la variación explica el modelo. Más alto, mejor.
- **MAE** (error absoluto medio): en promedio, cuánto se equivoca, en las unidades de `y`. Más bajo, mejor.

```python
from sklearn.metrics import mean_absolute_error, r2_score

real = [10, 20, 30]
estimado = [11, 19, 32]
print("R²:", round(r2_score(real, estimado), 3))
print("MAE:", round(mean_absolute_error(real, estimado), 3))
print("Métricas: OK")
```

### Convertir una categoría en columnas (one-hot)

El **departamento** (`dpto`) es una **categoría**, no un número con el que se pueda hacer aritmética. Si lo dejáramos como código (5, 8, 11…), el modelo creería que "Atlántico (8)" es *más* que "Antioquia (5)", lo cual no tiene sentido. La técnica estándar es **one-hot**: crear **una columna 0/1 por categoría**. Así el modelo aprende un nivel propio para **cada** departamento, que es justo lo que necesitamos para que prediga bien el empleo (cada departamento tiene su escala).

```python
import pandas as pd

ejemplo = pd.DataFrame({"dpto": [5, 8, 5]})
onehot = pd.get_dummies(ejemplo["dpto"].astype(str), prefix="dpto")
print(onehot)
assert onehot.shape == (3, 2)  # dos departamentos distintos → dos columnas
print("one-hot: OK")
```

---

## Instrucciones

En la Lección 5 trajimos datos: una capa **`curated/`** de agregados GEIH (oficial) y, opcionalmente, un `staging/news_labor.jsonl` de noticias (no oficial). Ya tenemos evidencia; falta **convertirla en una respuesta para quien decide**.

**Qué hacemos en esta lección.** Pasamos de *tener datos* a *informar una decisión*. La pregunta guía es:

> *Como analista del mercado laboral, ¿qué evidencia le mostraría esta semana a quien toma decisiones?*

Seguimos el mismo orden de las diapositivas: **primero visualizamos** (montamos un **tablero** con varias vistas del territorio), **después modelamos** (un modelo simple y uno más flexible, y discutimos **precisión vs. poder explicar**), y al final volvemos al tablero para añadirle el resultado del modelo. Un **monitor en vivo** de titulares aporta contexto (no estadística).

**Una regla de gobernanza, desde el inicio.** Trabajamos **solo sobre agregados** (departamento × mes), nunca sobre datos de personas individuales ni sobre el texto de las noticias. Cada vista del tablero **dice de qué fuente viene**.

Antes de esta práctica se debe ejecutar **`l5-ingestion`** y tener `data/curated/` (y, opcional, `staging/news_labor.jsonl`).

Las capas de evidencia que aparecen en esta lección:

| Capa | Fuente | Para qué la usamos |
|------|--------|--------------------|
| **Oficial** | Agregados GEIH en `curated/` | Indicador laboral, tendencia y modelo |
| **Mapa** | `colombia_departments.geojson` (límites DANE) | Pintar el indicador por departamento |
| **Servicios (OSM)** | `osm_services_by_dpto.csv` (OpenStreetMap) | Comparar servicios (salud / educación / comercio) con el empleo — **comunitario, no oficial** |
| **Medios (opcional)** | `news_labor.jsonl` + RSS en vivo | Monitor de discurso — **no es dato oficial** |

Los dos archivos de **referencia** (mapa y servicios) los **descargamos una vez** del sitio del curso y quedan **en caché** en su Drive (`data/reference/`); en corridas siguientes se leen de ahí, sin volver a descargar.

**Qué hace el cuaderno (en orden).**

| Parte | Tema |
|-------|------|
| **1** | Montar Drive, rutas, **descargar referencias** (mapa + OSM), instalar librerías y cargar `curated/` |
| **2** | **Tablero**: indicador por departamento (mapa), burbujas sobre OSM, tendencia mensual y servicios vs. empleo |
| **3** | **Modelar** el empleo con **regresión lineal** y discutir **explicabilidad** |
| **4** | **Monitor en vivo** de RSS (contexto, no oficial) |
| **5** | **Tablero final**: mapa + modelo lineal + contexto RSS |

Ver **Tareas** al final.

---

## Parte 1. Configuración: Drive, rutas y librerías

Montamos la **misma raíz** que en las lecciones 3 a 5, para leer la capa `curated/` que dejó la ingesta.

```python
from pathlib import Path

USE_GOOGLE_DRIVE = True

# Detectamos Colab para montar Drive solo allí
try:
    import google.colab  # noqa: F401
    IN_COLAB = True
except ImportError:
    IN_COLAB = False

if USE_GOOGLE_DRIVE and IN_COLAB:
    from google.colab import drive

    drive.mount("/content/drive")
    WORK_ROOT = Path("/content/drive/MyDrive/udenar/cease/2026/big-data/")
    print(f"Raíz en Drive: {WORK_ROOT}")
else:
    WORK_ROOT = Path(".")
    print(f"Raíz local: {WORK_ROOT.resolve()}")
```

Definimos rutas. Leemos de `curated/` (oficial) y, si existe, de `staging/` (noticias). En `reference/` guardamos los archivos de mapa y servicios; en `outputs/` los gráficos.

```python
CURATED_DIR = WORK_ROOT / "data" / "curated"          # agregados oficiales (entrada)
STAGING_DIR = WORK_ROOT / "data" / "staging"          # noticias (opcional)
REFERENCE_DIR = WORK_ROOT / "data" / "reference"      # mapa + servicios OSM (caché)
SCHEMA_PATH = WORK_ROOT / "data" / "schema_contract.json"
MANIFEST_PATH = WORK_ROOT / "manifest.json"
OUTPUTS_DIR = WORK_ROOT / "outputs"                   # aquí guardamos figuras
for d in (REFERENCE_DIR, OUTPUTS_DIR):
    d.mkdir(parents=True, exist_ok=True)

# Buscamos los agregados que dejó la Lección 5 / Parte A
curated_files = sorted(CURATED_DIR.glob("geih_*.parquet"))
print("Archivos curated encontrados:", len(curated_files))
```

Instalamos analítica, visualización y el monitor en vivo. **scikit-learn** para los modelos, **pandas** para preparar las tablas, **Plotly** para los mapas y gráficos, **feedparser** + **ipywidgets** para el monitor RSS en vivo.

```python
%pip install -q polars pyarrow pandas scikit-learn plotly feedparser mongomock ipywidgets
```

**Nota (Colab).** Si pip imprime `ERROR: pip's dependency resolver…` con conflictos de `websockets`, `click` o `typer` contra paquetes como `google-adk`, `wandb` o `huggingface-hub`, **ignore** esos avisos: son librerías que Colab trae de fábrica y **este cuaderno no usa**. Siga si las importaciones de abajo funcionan (véase la explicación completa en `l5-ingestion`, Parte 1).

```python
import json          # leer/escribir JSON (contrato, manifiesto, GeoJSON)
import threading     # hilo en segundo plano para el monitor RSS
import time          # pausas y marcas de tiempo en el monitor
import urllib.request  # descargar referencias (mapa, OSM) al Drive
import uuid          # ids únicos en eventos RSS

import feedparser    # leer feeds RSS de noticias
import ipywidgets as widgets  # monitor en vivo (Parte 4)
import mongomock     # consultar titulares exportados desde L5
import numpy as np   # arreglos numéricos para modelos
import pandas as pd  # tablas, one-hot y coeficientes legibles
import plotly.express as px   # mapas y gráficos rápidos
import plotly.graph_objects as go  # figuras compuestas (tablero, tablas)
import polars as pl  # leer Parquet curated
from IPython.display import clear_output, display  # monitor RSS
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

print("Dependencias: OK")


def guardar_fig(fig, nombre: str) -> None:
    """Guarda la figura en outputs/ y la muestra inline en Colab."""
    ruta = OUTPUTS_DIR / nombre
    fig.write_html(str(ruta))
    fig.show()
```

**Descargar las referencias (una sola vez).** El **mapa** de departamentos (límites oficiales DANE) y el conteo de **servicios OSM** por departamento son archivos que el curso ya preparó. Los **descargamos del sitio** y los **guardamos en caché** en su Drive (`data/reference/`). Si ya están, no se vuelven a descargar: así el cuaderno no depende de la red en cada corrida ni satura Colab.

```python
BASE_URL = "https://cabrerac.github.io/assets/data/26-udenar-big-data"
REFERENCE_FILES = {
    "colombia_departments.geojson": f"{BASE_URL}/colombia_departments.geojson",
    "osm_services_by_dpto.csv": f"{BASE_URL}/osm_services_by_dpto.csv",
}

for nombre, url in REFERENCE_FILES.items():
    destino = REFERENCE_DIR / nombre
    if destino.is_file() and destino.stat().st_size > 0:
        print("Ya en caché:", nombre)
    else:
        urllib.request.urlretrieve(url, destino)  # descarga y guarda en Drive
        print("Descargado:", nombre)

GEOJSON_PATH = REFERENCE_DIR / "colombia_departments.geojson"
OSM_PATH = REFERENCE_DIR / "osm_services_by_dpto.csv"
```

**Cargar los agregados.** Leemos **todos** los archivos `geih_*.parquet` y los unimos en una sola tabla (una fila por **departamento × año × mes**). Aceptamos los dos nombres posibles de la columna objetivo (`ponderado` o `suma_ponderada`).

```python
frames = []
for f in curated_files:
    t = pl.read_parquet(f)
    if "ponderado" not in t.columns and "suma_ponderada" in t.columns:
        t = t.rename({"suma_ponderada": "ponderado"})
    frames.append(t)

# Unimos y quitamos duplicados (un mismo dpto/año/mes podría venir en dos archivos)
cur = pl.concat(frames, how="diagonal").unique(subset=["dpto", "anio", "mes"])
cur_pd = cur.to_pandas()                 # versión pandas para graficar y modelar
cur_pd["dpto"] = cur_pd["dpto"].astype(int)

anios = sorted(cur_pd["anio"].unique().tolist())
print("Filas en curated:", len(cur_pd), "| años:", anios, "| departamentos:", cur_pd["dpto"].nunique())
```

**Comprobar:**

```python
assert WORK_ROOT.is_dir()
assert len(curated_files) >= 1, (
    "No hay agregados en curated/. Ejecute l5-ingestion (o week-3-group Parte A) primero."
)
assert GEOJSON_PATH.is_file() and OSM_PATH.is_file(), "Faltan los archivos de referencia."
assert {"dpto", "anio", "mes", "ponderado"}.issubset(cur_pd.columns)
print("Parte 1, configuración: OK")
```

---

## Parte 2. Tablero: ver el territorio antes de modelar

Antes de cualquier modelo, **miramos los datos**. Un **tablero** (*dashboard*) reúne **varias vistas** de la misma pregunta para que quien decide entienda el panorama de un vistazo. Aquí armamos cuatro vistas **complementarias**, cada una con su **fuente rotulada**:

1. **Mapa del indicador** — pinta cada departamento según su indicador laboral (más oscuro = más alto).
2. **Burbujas sobre OpenStreetMap** — el tamaño muestra el empleo de cada departamento, ubicado en el mapa real.
3. **Tendencia mensual** — cómo evoluciona el empleo total mes a mes.
4. **Servicios vs. empleo** — ¿qué servicios mapeados en OSM (salud, educación, comercio) acompañan mejor al indicador laboral?

### Paso 2.1. Un indicador laboral por departamento

Necesitamos **un número por departamento** para pintar el mapa. Si el `curated/` tiene **varios años**, usamos el **crecimiento del empleo** (cuánto cambió entre el primer y el último año): un "mejor/peor" con sentido. Si solo hay **un año**, usamos el **nivel promedio** de empleo y lo rotulamos como tal (es tamaño, no calidad).

```python
# Empleo promedio por departamento y año (base para el indicador)
por_dpto_anio = cur_pd.groupby(["dpto", "anio"])["ponderado"].mean().reset_index()

if len(anios) >= 2:
    primero, ultimo = anios[0], anios[-1]
    piv = (
        por_dpto_anio.pivot(index="dpto", columns="anio", values="ponderado")
        .dropna(subset=[primero, ultimo])
    )
    ind_df = pd.DataFrame(
        {"dpto": piv.index, "indicador": (piv[ultimo] - piv[primero]) / piv[primero] * 100.0}
    ).reset_index(drop=True)
    indicador_label = f"Crecimiento del empleo {primero}->{ultimo} (%)"
    indicador_tipo = "crecimiento"
else:
    ind_df = cur_pd.groupby("dpto")["ponderado"].mean().reset_index()
    ind_df.columns = ["dpto", "indicador"]
    indicador_label = "Empleo ponderado promedio (nivel)"
    indicador_tipo = "nivel"

ind_df["dpto"] = ind_df["dpto"].astype(int)
print(indicador_label, "—", len(ind_df), "departamentos")
```

### Paso 2.2. Cargar el mapa (GeoJSON) y los servicios (OSM)

El **GeoJSON** trae los límites de cada departamento (con su código DANE en `dpto`). De cada polígono sacamos un **centro aproximado** (promedio de sus puntos) para colocar las burbujas. Del CSV de **OSM** calculamos la **proporción** de cada servicio (salud / educación / comercio) sobre el total mapeado: comparar **proporciones** es más justo que comparar conteos, porque un departamento grande tiene más de todo.

```python
with open(GEOJSON_PATH, encoding="utf-8") as f:
    geojson = json.load(f)


def _coords(geom):
    """Recorre todos los pares (lon, lat) de un polígono o multipolígono."""
    if geom["type"] == "Polygon":
        for ring in geom["coordinates"]:
            yield from ring
    elif geom["type"] == "MultiPolygon":
        for poly in geom["coordinates"]:
            for ring in poly:
                yield from ring


centroides, nombres = {}, {}
for feat in geojson["features"]:
    code = int(feat["properties"]["dpto"])
    nombres[code] = feat["properties"].get("dpto_nombre", str(code))
    pts = list(_coords(feat["geometry"]))
    centroides[code] = (sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts))

osm = pd.read_csv(OSM_PATH)
for c in ("health", "education", "commerce"):
    osm[c + "_share"] = osm[c] / osm["total"]   # proporción, no conteo crudo

print("Departamentos en el mapa:", len(centroides), "| filas OSM:", len(osm))
```

### Paso 2.3. Construir las cuatro vistas

Cada figura usa **Plotly**. Los dos mapas se dibujan **sobre teselas reales de OpenStreetMap** (`mapbox_style="open-street-map"`, sin token). Fijamos títulos que **nombran la fuente**.

```python
# (1) Mapa del indicador por departamento (capa oficial GEIH sobre límites DANE)
fig_mapa = px.choropleth_mapbox(
    ind_df, geojson=geojson, locations="dpto", featureidkey="properties.dpto",
    color="indicador", color_continuous_scale="YlGnBu",
    mapbox_style="open-street-map", zoom=3.7, center={"lat": 4.6, "lon": -73.5},
    opacity=0.75, labels={"indicador": indicador_label},
)
fig_mapa.update_layout(title=f"GEIH (oficial) — {indicador_label}",
                       margin=dict(l=0, r=0, t=40, b=0), height=420)

# (2) Burbujas: empleo promedio por departamento, ubicado por su centro
emp_dpto = cur_pd.groupby("dpto")["ponderado"].mean().reset_index()
emp_dpto["dpto"] = emp_dpto["dpto"].astype(int)
emp_dpto["lon"] = emp_dpto["dpto"].map(lambda d: centroides.get(d, (None, None))[0])
emp_dpto["lat"] = emp_dpto["dpto"].map(lambda d: centroides.get(d, (None, None))[1])
emp_dpto["nombre"] = emp_dpto["dpto"].map(nombres)
emp_dpto = emp_dpto.dropna(subset=["lon", "lat"])
fig_burbujas = px.scatter_mapbox(
    emp_dpto, lat="lat", lon="lon", size="ponderado", color="ponderado",
    color_continuous_scale="YlOrRd", size_max=38, zoom=3.7,
    center={"lat": 4.6, "lon": -73.5}, mapbox_style="open-street-map",
    hover_name="nombre", labels={"ponderado": "Empleo ponderado"},
)
fig_burbujas.update_layout(title="GEIH (oficial) — empleo por departamento (sobre OSM)",
                           margin=dict(l=0, r=0, t=40, b=0), height=420)

# (3) Tendencia mensual del empleo total
serie = cur_pd.groupby(["anio", "mes"])["ponderado"].sum().reset_index().sort_values(["anio", "mes"])
serie["periodo"] = serie["anio"].astype(str) + "-" + serie["mes"].astype(str).str.zfill(2)
fig_tendencia = px.line(serie, x="periodo", y="ponderado", markers=True,
                        title="GEIH (oficial) — empleo ponderado total por mes",
                        labels={"periodo": "Periodo (año-mes)", "ponderado": "Empleo ponderado"})
fig_tendencia.update_layout(margin=dict(l=10, r=10, t=40, b=10), height=420)

# (4) Servicios OSM vs. indicador laboral: correlación de cada proporción
comp = ind_df.merge(osm, on="dpto", how="inner")
correls = {c: comp["indicador"].corr(comp[c + "_share"]) for c in ("health", "education", "commerce")}
srv_es = {"health": "salud", "education": "educación", "commerce": "comercio"}
fig_osm = px.bar(x=[srv_es[c] for c in correls], y=[round(v, 2) for v in correls.values()],
                 labels={"x": "servicio (OSM)", "y": f"correlación con {indicador_tipo}"},
                 title="Servicios OSM vs. indicador laboral (por departamento)")
fig_osm.update_layout(margin=dict(l=10, r=10, t=40, b=10), height=420)
print("Correlaciones:", {srv_es[c]: round(v, 2) for c, v in correls.items()})
```

### Paso 2.4. Componer el tablero

En Colab, **`fig.show()`** de Plotly renderiza **inline** de forma fiable. Los `GridBox` de widgets a veces **no** muestran mapas (solo guardan HTML en Drive). Mostramos las cuatro vistas **una tras otra** aquí; al final del cuaderno las reuniremos con el modelo y el contexto RSS.

```python
guardar_fig(fig_mapa, "l6_mapa_indicador.html")
guardar_fig(fig_burbujas, "l6_mapa_burbujas.html")
guardar_fig(fig_tendencia, "l6_tendencia.html")
guardar_fig(fig_osm, "l6_osm_correlacion.html")
print("Tablero descriptivo: cuatro vistas mostradas arriba y guardadas en", OUTPUTS_DIR)
```

**Cómo leer la vista de servicios.** La correlación va de -1 a 1: cerca de **+1**, el servicio sube donde el indicador laboral es alto; cerca de **0**, no hay relación. Es **exploratorio**, no causal: OSM es un mapa **comunitario** con **cobertura desigual** (mejor en ciudades grandes) y son solo ~33 departamentos. Sirve para **plantear preguntas**, no para concluir.

**Comprobar:**

```python
assert len(ind_df) >= 1
assert (OUTPUTS_DIR / "l6_mapa_indicador.html").is_file()
assert set(correls.keys()) == {"health", "education", "commerce"}
print("Parte 2, tablero descriptivo: OK")
```

---

## Parte 3. Modelar el empleo: regresión lineal

El tablero **describe**; un **modelo** intenta **predecir**. Aquí predecimos el **empleo ponderado** (la variable objetivo) de un departamento en un mes a partir de tres entradas que ya están en los agregados: el **departamento**, el **mes** y, si hay varios años, el **año**.

El departamento es una variable **categórica** (un código, no una cantidad), así que no se puede usar tal cual: lo convertimos en columnas **one-hot** (una columna 0/1 por departamento). Esto le da al modelo el contexto de que cada departamento tiene su propia escala —Bogotá no se parece a Vaupés—; sin ese contexto, el modelo solo podría predecir el promedio nacional. El **mes** y el **año** entran como números porque capturan estacionalidad y tendencia.

Con tablas **pequeñas y agregadas** (pocas filas dpto×mes), usamos una **regresión lineal**: es sencilla, **explicable** y adecuada para mostrar evidencia a quien decide. La **explicabilidad** — poder decir *por qué* el modelo predice más empleo en un departamento — es central en la gobernanza de la IA.

### Paso 3.1. Preparar las variables (one-hot del departamento)

Seleccionamos las entradas (`mes`, `anio` si aplica, y el one-hot de `dpto`) y separamos la variable objetivo (`ponderado`). El año solo entra cuando el `curated/` cubre más de un año.

```python
feat = cur_pd.copy()
feat["dpto"] = feat["dpto"].astype(int)

# Entrada: one-hot del departamento + mes (+ año si hay varios). Objetivo: empleo ponderado.
base_cols = ["mes"] + (["anio"] if feat["anio"].nunique() > 1 else [])
X_cat = pd.get_dummies(feat["dpto"].astype(str), prefix="dpto")
X = pd.concat([feat[base_cols].reset_index(drop=True), X_cat.reset_index(drop=True)], axis=1).astype(float)
y = feat["ponderado"].to_numpy()
feature_names = list(X.columns)

print("Variables de entrada:", len(feature_names), "(mes/año +", X_cat.shape[1], "departamentos)")
print("Filas para modelar:", len(y))
```

### Paso 3.2. Separar en entrenamiento, validación y prueba

Apartamos la **prueba** antes de entrenar y no la tocamos hasta el final: así medimos el modelo sobre datos que **nunca** vio. La **validación** sirve para ajustar decisiones durante el desarrollo; el **entrenamiento** es lo que el modelo usa para aprender.

```python
# 1) apartamos la prueba (20 %); 2) del resto, una parte para validación (25 %)
X_tmp, X_test, y_tmp, y_test = train_test_split(X.to_numpy(), y, test_size=0.20, random_state=42)
X_train, X_val, y_train, y_val = train_test_split(X_tmp, y_tmp, test_size=0.25, random_state=42)
print("Entrenamiento:", len(y_train), "| Validación:", len(y_val), "| Prueba:", len(y_test))
```

### Paso 3.3. Regresión lineal

Entrenamos la regresión lineal con `fit` (aprende los coeficientes) y la evaluamos en **validación** con dos medidas: **R²** (qué parte de la variación explica, más cerca de 1 es mejor) y **MAE** (error promedio en las mismas unidades del empleo ponderado).

```python
lin = LinearRegression()
lin.fit(X_train, y_train)
y_val_lin = lin.predict(X_val)
r2_lin = r2_score(y_val, y_val_lin)
mae_lin = mean_absolute_error(y_val, y_val_lin)
print("Lineal (validación) — R²:", round(r2_lin, 3), "| MAE:", round(mae_lin, 2))
```

### Paso 3.4. Evaluar en validación y prueba

Ahora sí usamos la **prueba** (reservada en el Paso 3.2) una sola vez, para reportar cómo se comporta el modelo con datos nuevos. Comparar validación y prueba nos dice si el resultado se sostiene o si solo funcionaba en los datos de ajuste.

```python
nombre = "lineal"
y_val_pred = y_val_lin
y_test_pred = lin.predict(X_test)

print(f"Modelo: {nombre}")
print("Validación — R²:", round(r2_lin, 3), "| MAE:", round(mae_lin, 2))
print("Prueba final — R²:", round(r2_score(y_test, y_test_pred), 3),
      "| MAE:", round(mean_absolute_error(y_test, y_test_pred), 2))
```

### Paso 3.5. Explicabilidad: leer el modelo lineal

Evaluar un modelo **no es solo** mirar R². También importa **explicar** a quien decide qué entradas empujan la predicción.

```python
def fig_obs_pred(y_true, y_pred, titulo: str) -> go.Figure:
    """Gráfico observado vs. predicho con diagonal ideal y = x."""
    lo = float(min(y_true.min(), y_pred.min()))
    hi = float(max(y_true.max(), y_pred.max()))
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=y_true, y=y_pred, mode="markers", name="validación"))
    fig.add_trace(go.Scatter(x=[lo, hi], y=[lo, hi], mode="lines",
                             name="ideal (y = x)", line=dict(dash="dash")))
    fig.update_layout(title=titulo, xaxis_title="Observado (empleo ponderado)",
                      yaxis_title="Predicho", height=380, margin=dict(l=10, r=10, t=40, b=10))
    return fig


fig_model_lin = fig_obs_pred(y_val, y_val_lin, "GEIH — lineal (validación)")

# Coeficientes lineales de los 8 departamentos con mayor efecto (explicabilidad)
coef = pd.Series(lin.coef_, index=feature_names)
coef_dpto = coef[coef.index.str.startswith("dpto_")].sort_values(ascending=False).head(8)
fig_coef = px.bar(
    x=coef_dpto.index.str.replace("dpto_", "dpto "),
    y=coef_dpto.values,
    labels={"x": "departamento (one-hot)", "y": "coeficiente lineal"},
    title="Explicabilidad — efecto por departamento (modelo lineal)",
)
fig_coef.update_layout(height=380)

guardar_fig(fig_model_lin, "l6_modelo_lineal_obs_pred.html")
guardar_fig(fig_coef, "l6_modelo_coeficientes.html")

print("\n--- Métricas (validación) ---")
print(f"{'Modelo':<10} {'R² val':>8} {'MAE val':>12}")
print(f"{'lineal':<10} {r2_lin:>8.3f} {mae_lin:>12.0f}")
print("\nEl lineal permite decir *por qué* predice más empleo en un dpto (coeficientes arriba).")
```

El modelo **lineal** se puede **leer**: cada **`dpto_*`** es el nivel base de empleo de ese departamento; **`mes`** / **`anio`** capturan estacionalidad y tendencia. Eso ayuda a sostener afirmaciones ante quien decide — no solo a reportar un número de error.

**Comprobar:**

```python
assert len(y_test_pred) == len(y_test)
assert nombre == "lineal"
assert (OUTPUTS_DIR / "l6_modelo_lineal_obs_pred.html").is_file()
assert (OUTPUTS_DIR / "l6_modelo_coeficientes.html").is_file()
print("Parte 3, modelo y explicabilidad: OK")
```

---

## Parte 4. Monitor en vivo: RSS y MongoDB

Un monitor de stream **en tiempo real** muestra titulares **a medida que llegan**. En producción leeríamos de Kafka o MongoDB; aquí combinamos dos ideas:

1. **Widget en vivo:** sondeamos feeds RSS de **economía**, el monitor se **actualiza solo** cada pocos segundos.
2. **MongoDB:** cargamos `news_labor.jsonl` (lo que dejó la Lección 5) y consultamos cuántos documentos hay almacenados.

Los feeds ya son de economía; ampliamos las **palabras clave** respecto a la Lección 5 (solo empleo) para que el monitor suela mostrar titulares: inflación, TRM, tasas, etc. Sigue siendo **contexto mediático**, no estadística oficial — pero encaja con la pregunta de decisión sobre el mercado laboral.

### Paso 4.1. Cargar los documentos de la Lección 5

```python
news_path = STAGING_DIR / "news_labor.jsonl"
mongo = mongomock.MongoClient()
news_col = mongo["udenar"]["news_raw"]

if news_path.is_file():
    with news_path.open(encoding="utf-8") as f:
        docs = [json.loads(ln) for ln in f if ln.strip()]
    if docs:
        news_col.insert_many(docs)

news_stored = news_col.count_documents({})
print("Documentos cargados desde L5:", news_stored)
```

### Paso 4.2. Monitor RSS con actualización automática

Usamos dos grupos de palabras clave: **empleo** (como en L5) y **macro/economía** (más titulares en los feeds de economía). Revisamos más entradas por feed para no quedarnos en cero.

El monitor se **actualiza solo** unas pocas veces (hilo en segundo plano) y **se detiene solo**. Lo mantenemos **corto a propósito** para no recargar Colab; si quieren más, vuelvan a ejecutar la celda o suban `MAX_TICKS`.

```python
RSS_FEEDS = [
    "https://www.portafolio.co/rss/economia.xml",
    "https://www.eltiempo.com/rss/economia.xml",
]
# Empleo directo + contexto macro (feeds de economía)
KEYWORDS_LABOR = ("empleo", "desempleo", "mercado laboral", "trabajo", "geih", "salario", "nómina", "nomina")
KEYWORDS_MACRO = (
    "inflación", "inflacion", "trm", "dólar", "dolar", "tasas", "banrep", "banco de la república",
    "crecimiento", "pib", "colcap", "finanzas", "economía", "economia", "ipc", "remesas",
)
KEYWORDS = KEYWORDS_LABOR + KEYWORDS_MACRO
ENTRIES_PER_FEED = 20  # más entradas por feed que en L5
POLL_SECONDS = 20      # actualización automática cada 20 s
MAX_TICKS = 3          # corto a propósito (≈ 40 s): no recarga Colab


def keyword_hit(text: str) -> bool:
    t = (text or "").lower()
    return any(k in t for k in KEYWORDS)


def poll_rss_events(max_items: int = 15) -> list[dict]:
    events: list[dict] = []
    for url in RSS_FEEDS:
        feed = feedparser.parse(url)
        for entry in feed.entries[:ENTRIES_PER_FEED]:
            title = entry.get("title", "")
            summary = entry.get("summary", "")
            if keyword_hit(title + " " + summary):
                events.append(
                    {
                        "id": str(uuid.uuid4()),
                        "url": entry.get("link", ""),
                        "title": title,
                        "feed": url,
                        "geih": False,
                    }
                )
            if len(events) >= max_items:
                return events
    return events


monitor_out = widgets.Output()
header = widgets.HTML(value="Monitor de discurso mediático — NO es dato oficial DANE/GEIH")


def refresh_monitor(tick: int | None = None) -> None:
    with monitor_out:
        clear_output(wait=True)
        live = poll_rss_events(max_items=15)
        stamp = time.strftime("%H:%M:%S")
        label = f"actualización {tick}" if tick is not None else "inicio"
        print(f"[{stamp}] Titulares recientes ({label}) — {len(live)} coincidencias:")
        if live:
            for e in live:
                print(" -", e["title"], f"({e.get('feed', '')})")
        else:
            print(" (ninguno en esta consulta — pruebe de nuevo en unos segundos)")
        print(f"En almacén (L5): {news_stored} documentos")


def auto_poll_loop() -> None:
    for tick in range(1, MAX_TICKS + 1):
        refresh_monitor(tick=tick)
        if tick < MAX_TICKS:
            time.sleep(POLL_SECONDS)


threading.Thread(target=auto_poll_loop, daemon=True).start()
refresh_monitor()

display(widgets.VBox([header, monitor_out]))
print(f"Monitor en marcha: actualiza cada {POLL_SECONDS} s (máx. {MAX_TICKS} veces). Detenga con ■ si hace falta.")
```

### Paso 4.3. Snapshot RSS para el tablero final

El widget en vivo es útil en clase, pero el **tablero final** necesita una vista **estática** que se pueda mostrar junto al mapa y al modelo. Hacemos **un sondeo** (sin bucle) y armamos una **tabla** de titulares + el conteo del almacén L5.

```python
rss_snapshot = poll_rss_events(max_items=5)
titulos_rss = [e.get("title", "(sin título)") for e in rss_snapshot]
if not titulos_rss:
    titulos_rss = ["(ningún titular en esta consulta — reintente la celda)"]

fig_rss = go.Figure(
    data=[
        go.Table(
            header=dict(
                values=[
                    "Titulares recientes (NO oficial DANE)",
                    f"Documentos en almacén L5: {news_stored}",
                ]
            ),
            cells=dict(values=[titulos_rss]),
        )
    ]
)
fig_rss.update_layout(
    title="Medios — contexto de discurso (no es estadística GEIH)",
    height=280,
    margin=dict(l=10, r=10, t=40, b=10),
)
fig_rss.write_html(str(OUTPUTS_DIR / "l6_rss_contexto.html"))
print("Snapshot RSS listo para el tablero final.")
```

**Comprobar:**

```python
print("Parte 4, monitor en vivo: OK")
```

---

## Parte 5. Tablero final: mapa + modelo lineal + contexto RSS

Cerramos reuniendo **toda** la evidencia para la pregunta de decisión: **mapa** (oficial), **modelo lineal** (oficial + explicable) y **RSS** (contexto, no oficial). Cada panel se muestra **inline** en Colab con `fig.show()`.

```python
print("=== Tablero final — evidencia para la decisión ===\n")
print("1/3 — Mapa del indicador laboral (GEIH, oficial)")
fig_mapa.show()
print("\n2/3 — Modelo lineal: observado vs. predicho (GEIH, oficial)")
fig_model_lin.show()
print("\n3/3 — Contexto mediático (NO oficial)")
fig_rss.show()

# Resumen HTML por panel (por si abren outputs/ en Drive)
for nombre in (
    "l6_mapa_indicador.html",
    "l6_modelo_lineal_obs_pred.html",
    "l6_rss_contexto.html",
):
    assert (OUTPUTS_DIR / nombre).is_file()
print("\nPaneles guardados en:", OUTPUTS_DIR)
```

**Cómo leerlo.** El **mapa** y el **modelo lineal** sostienen afirmaciones sobre empleo con fuente DANE. El panel **RSS** acompaña el discurso público, pero **no** reemplaza a GEIH. A quien decide: mapa + tendencia (Parte 2) + lineal con coeficientes legibles.

**Comprobar:**

```python
assert (OUTPUTS_DIR / "l6_mapa_indicador.html").is_file()
assert (OUTPUTS_DIR / "l6_modelo_lineal_obs_pred.html").is_file()
assert (OUTPUTS_DIR / "l6_rss_contexto.html").is_file()
print("Parte 5, tablero final: OK")
```

---

## Tareas

Lo que practicaron aquí lo **implementan ustedes** en el cuaderno grupal **`week-3-group` (Ejercicio 2)**, sobre los agregados que construyan en el Ejercicio 1:

1. Dividan en **entrenamiento/validación/prueba** y entrenen una **regresión lineal** explicable.
2. Hagan al menos **dos gráficos** ligados a la pregunta de decisión, con la fuente rotulada.
3. Armen un **tablero** que reúna las vistas.

**Entrega grupal (semana 3):** martes **23 jun 2026** — ZIP con `week-3-group-<group_id>.ipynb` + `manifest.json` (detalle en `week-3-group`).

---

## Entregables del proyecto (resumen)

**Sábado 20 jun** — el instructor explica esto en el bloque de proyecto (11:30–12:45).

| Recurso | Enlace |
|---------|--------|
| Informe (Word) | [project-report-template.docx](/assets/documents/26-udenar-big-data/project-report-template.docx) |
| Diapositivas (plantilla) | [project-presentation-template.pptx](/assets/documents/26-udenar-big-data/project-presentation-template.pptx) |
| Reflexión final (Word) | [project-reflection-template.docx](/assets/documents/26-udenar-big-data/project-reflection-template.docx) |
| Catálogo público (L8) | [l8-final-project](/teaching/26-udenar-big-data/l8-final-project/) |

| Qué | Cuándo (Colombia) |
|-----|-------------------|
| **Presentación en vivo** (~20 min slides + live demo + ~10 min Q&A; slides not in ZIP) | **Sábado 27 jun 2026** — tras charla L7 (~1 h) |
| **Un solo ZIP** `project-<group_id>.zip` | **Martes 30 jun 2026, 23:59** |
| **Reflexión individual** `project-reflection-<student>.pdf` | **Miércoles 1 jul 2026, 23:59** |

**Contenido obligatorio del ZIP** (raíz; sin Parquet ni CSV):

| Archivo | Descripción |
|---------|-------------|
| `project-report-<group_id>.pdf` | Informe consolidado (secciones 1–7 en la plantilla) |
| Cuaderno(s) ejecutado(s) | Código reproducible del pipeline y la analítica |
| `manifest.json` | Manifiesto final (`publish_on_web: true` si publican en L8) |
| `audit.jsonl` + `schema_contract.json` | Linaje y contrato |

**Publicación opcional en el sitio (L8)** — solo si `publish_on_web: true` en `manifest.json`:

| Archivo | Descripción |
|---------|-------------|
| `project-title-en.txt` | Un título en **inglés** (una línea) |
| `project-abstract-en.txt` | **~200 palabras en inglés**: problema, proceso seguido y resultados |

Sin microdatos ni material re-identificable. El instructor publica título + abstract en [L8](/teaching/26-udenar-big-data/l8-final-project/) tras revisar la entrega.

**Diapositivas (sábado 27):** siga la plantilla [project-presentation-template.pptx](/assets/documents/26-udenar-big-data/project-presentation-template.pptx) — **6 diapositivas:** título → canvas (requerimientos + ética) → pipeline → arquitectura → analítica → conclusiones. **~20 min** en total (incluya **demo en vivo** del pipeline, tablero o salidas clave) + **~10 min** de preguntas. La ética se integra en canvas, pipeline, arquitectura y analítica (sin diapositiva final solo de ética).

<!-- end NOTEBOOK: -->
