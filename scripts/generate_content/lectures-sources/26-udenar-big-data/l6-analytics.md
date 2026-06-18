---
course_code: 26-udenar-big-data
title: Analytics and visualisation
description: Lecture 6 — supervised models on GEIH aggregates, decision-focused charts, optional stream monitor, and dashboards-as-governance synthesis.
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
visible: false
group_notebook: week-3-group
notebook_language: es
notebook_title: Analítica y visualización
notebook_description: Práctica individual de la Lección 6. Modelamos sobre agregados GEIH (lineal y un MLP pequeño), hacemos gráficos ligados a una pregunta de decisión y discutimos la gobernanza al presentar evidencia.
---

<!-- SLIDES: -->

# Last Time

<!-- end SLIDES: -->

{% include _snippets/26-udenar-big-data/l6-analytics/last-time.md %}

<!-- SLIDES: -->

# ML on aggregates

<!-- end SLIDES: -->

{% include _snippets/26-udenar-big-data/l6-analytics/ml-aggregates.md %}

<!-- SLIDES: -->

# Governance dashboard

<!-- end SLIDES: -->

{% include _snippets/26-udenar-big-data/l6-analytics/governance-dashboard.md %}

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

Un modelo **lineal** busca la recta que mejor relaciona la entrada con la salida. **`fit`** aprende; **`predict`** estima para datos nuevos.

```python
from sklearn.linear_model import LinearRegression

modelo = LinearRegression()
modelo.fit([[1], [2], [3]], [2, 4, 6])  # aprende la relación y = 2x
pred = modelo.predict([[4]])[0]          # estima para x = 4
print("Predicción para x=4:", pred)
assert abs(pred - 8.0) < 0.01
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

---

## Instrucciones

En la Lección 5 trajimos datos: una capa **`curated/`** de agregados GEIH (oficial) y, opcionalmente, un `staging/news_labor.jsonl` de noticias (no oficial). Ya tenemos evidencia; falta **convertirla en una respuesta para quien decide**.

**Qué hacemos en esta lección.** Pasamos de *tener datos* a *informar una decisión*. La pregunta guía es:

> *Como analista del mercado laboral, ¿qué evidencia le mostraría esta semana a quien toma decisiones?*

Para responderla: (1) ajustamos un **modelo** sobre los agregados GEIH, (2) lo comparamos con un **modelo más flexible** (una red neuronal pequeña) y analizamos un dilema real: **precisión vs. poder explicar**, (3) montamos un **monitor en vivo** de titulares RSS (contexto, no estadística), y (4) reunimos la evidencia oficial en un **tablero** rotulado.

**Una regla de gobernanza, desde el inicio.** Modelamos **solo sobre agregados** (departamento × mes), nunca sobre datos de personas individuales ni sobre el texto de las noticias. Las noticias son un **monitor de discurso**, no una estadística.

Antes de esta práctica se debe ejecutar **`l5-ingestion`** y tener (o simular) `data/curated/` y, opcional, `staging/news_labor.jsonl`.

Las tres capas de evidencia que aparecen en esta lección:

| Capa | Fuente | Para qué la usamos |
|------|--------|--------------------|
| **Oficial** | Agregados GEIH en `curated/` | Modelo y gráfico principal |
| **Macro (opcional)** | TRM / COLCAP en `staging/` | Gráfico de contexto |
| **Medios (opcional)** | `news_labor.jsonl` + RSS en vivo | Monitor — **no es dato oficial** |

**Qué hace el cuaderno (en orden).**

| Parte | Tema |
|-------|------|
| **1** | Montar Drive, rutas a `curated/` e instalar librerías |
| **2** | Modelo **lineal** sobre agregados + gráfico (capa oficial) |
| **3** | **Red neuronal pequeña**: comparar y **elegir** modelo (validación → prueba) |
| **4** | **Monitor en vivo** de RSS + consulta a MongoDB (capa no oficial) |
| **5** | **Tablero** que reúne las capas de evidencia |

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

Definimos rutas. Leemos de `curated/` (oficial) y, si existe, de `staging/` (noticias). Guardamos los gráficos en `outputs/`.

```python
CURATED_DIR = WORK_ROOT / "data" / "curated"          # agregados oficiales (entrada)
STAGING_DIR = WORK_ROOT / "data" / "staging"          # noticias (opcional)
SCHEMA_PATH = WORK_ROOT / "data" / "schema_contract.json"
MANIFEST_PATH = WORK_ROOT / "manifest.json"
OUTPUTS_DIR = WORK_ROOT / "outputs"                   # aquí guardamos figuras
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

# Buscamos los agregados que dejó la Lección 5 / Parte A
curated_files = sorted(CURATED_DIR.glob("geih_*.parquet"))
print("Archivos curated encontrados:", len(curated_files))
```

Instalamos analítica, visualización y el monitor en vivo. **scikit-learn** para los modelos, **Plotly** para graficar, **feedparser** + **ipywidgets** para sondear RSS y refrescar el widget.

```python
%pip install -q polars pyarrow scikit-learn plotly feedparser mongomock ipywidgets
```

```python
import json
import threading
import time
import uuid

import feedparser
import ipywidgets as widgets
import mongomock
import plotly.express as px
import plotly.graph_objects as go
import polars as pl
from IPython.display import clear_output, display
from plotly.subplots import make_subplots
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler

print("Dependencias: OK")
```

**Comprobar:**

```python
assert WORK_ROOT.is_dir()
assert len(curated_files) >= 1, (
    "No hay agregados en curated/. Ejecute l5-ingestion (o week-3-group Parte A) primero."
)
print("Parte 1, configuración: OK")
```

---

## Parte 2. Modelar sobre agregados oficiales

Tomamos los agregados GEIH y ajustamos un modelo simple: predecir el empleo ponderado a partir del **mes** y el **año**. Este es un ejemplo **didáctico** y no causal, sirve para ver el flujo entrenar → predecir → medir, y para tener una primera lectura de tendencia.

### Paso 2.1. Cargar y preparar la tabla

```python
# Leemos el primer agregado disponible
df = pl.read_parquet(curated_files[0])

# Aceptamos los dos nombres posibles de la columna objetivo
if "ponderado" not in df.columns and "suma_ponderada" in df.columns:
    df = df.rename({"suma_ponderada": "ponderado"})

# Variables de entrada: las que existan entre mes y anio
feature_cols = [c for c in ("mes", "anio") if c in df.columns]
X = df.select(feature_cols).to_numpy()   # entradas
y = df["ponderado"].to_numpy()           # objetivo: empleo ponderado

print("Variables de entrada:", feature_cols)
print("Filas para modelar:", len(y))
```

### Paso 2.2. Separar en entrenamiento, validación y prueba

Como en el Repaso, hacemos la división en tres. Reservamos la **prueba** para el final (Parte 3) y usamos la **validación** para evaluar cada modelo.

```python
# 1) apartamos la prueba (20 %); 2) del resto, una parte para validación (25 %)
X_tmp, X_test, y_tmp, y_test = train_test_split(X, y, test_size=0.20, random_state=42)
X_train, X_val, y_train, y_val = train_test_split(X_tmp, y_tmp, test_size=0.25, random_state=42)

print("Entrenamiento:", len(y_train), "| Validación:", len(y_val), "| Prueba:", len(y_test))
```

### Paso 2.3. Entrenar la regresión lineal y evaluar en validación

```python
lin = LinearRegression()
lin.fit(X_train, y_train)         # aprende con el entrenamiento
y_val_lin = lin.predict(X_val)    # predice sobre validación

r2_lin = r2_score(y_val, y_val_lin)
mae_lin = mean_absolute_error(y_val, y_val_lin)
print("Lineal (validación) — R²:", round(r2_lin, 3), "| MAE:", round(mae_lin, 2))
```

### Paso 2.4. Graficar observado vs. predicho

Un gráfico observado-contra-predicho muestra de un vistazo qué tan bien predice: cuanto más cerca de la diagonal, mejor. **El título dice de qué capa viene** el dato (oficial GEIH): rotular la fuente es parte de la gobernanza.

```python
fig = px.scatter(
    x=y_val,
    y=y_val_lin,
    labels={"x": "Observado (empleo ponderado)", "y": "Predicho (lineal)"},
    title="Capa oficial GEIH — modelo lineal (validación)",
)
fig.write_html(str(OUTPUTS_DIR / "l6_lineal_obs_pred.html"))  # guardamos la figura
fig.show()
```

**Comprobar:**

```python
assert len(y_val_lin) == len(y_val)
assert (OUTPUTS_DIR / "l6_lineal_obs_pred.html").is_file()
print("Parte 2, modelo lineal: OK")
```

---

## Parte 3. Un modelo más flexible: red neuronal pequeña

Entrenamos una **red neuronal pequeña** (un *MLP*: perceptrón multicapa) sobre **la misma tabla** y la comparamos con la lineal. Un modelo más flexible puede ajustar mejor, pero es **más difícil de explicar** a quien decide. Esa tensión entre **precisión y explicabilidad** es central en la gobernanza de datos y a la **interpretabilidad** de los sistemas de Inteligencia Artificial.

### Paso 3.1. Escalar las entradas

Las redes neuronales aprenden mejor cuando las entradas están en una escala parecida. **`StandardScaler`** las centra y normaliza. Ajustamos el escalador **solo con el entrenamiento** (para no "mirar" la prueba). Esta acción de preprocesamiento prepara los datos para los algoritmos de aprendizaje. Una vez más estamos mejorando la calidad de nuestros datos (i.e., Assess).

```python
scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)  # aprende media/desviación con train
X_test_s = scaler.transform(X_test)        # aplica la misma transformación a test
print("Entradas escaladas.")
```

### Paso 3.2. Entrenar el MLP y evaluar en validación

Usamos **una** capa oculta con pocas neuronas: suficiente para ilustrar, sin sobreajustar una tabla pequeña. Para escalar la validación reutilizamos el `scaler` ajustado con el entrenamiento.

```python
X_val_s = scaler.transform(X_val)

mlp = MLPRegressor(hidden_layer_sizes=(8,), max_iter=500, random_state=42)
mlp.fit(X_train_s, y_train)
y_val_mlp = mlp.predict(X_val_s)

r2_mlp = r2_score(y_val, y_val_mlp)
mae_mlp = mean_absolute_error(y_val, y_val_mlp)
print("MLP (validación) — R²:", round(r2_mlp, 3), "| MAE:", round(mae_mlp, 2))
```

### Paso 3.3. Elegir el modelo (en validación) y evaluar en prueba

Usamos la **validación** para decidir y la **prueba** solo para la evaluación final del modelo elegido.

```python
# Elegimos por menor MAE en validación
if mae_lin <= mae_mlp:
    modelo_elegido, nombre = lin, "lineal"
    y_test_pred = modelo_elegido.predict(X_test)
else:
    modelo_elegido, nombre = mlp, "mlp"
    y_test_pred = modelo_elegido.predict(scaler.transform(X_test))

print(f"Modelo elegido (mejor en validación): {nombre}")
print("Prueba final — R²:", round(r2_score(y_test, y_test_pred), 3),
      "| MAE:", round(mean_absolute_error(y_test, y_test_pred), 2))
```

Aunque el MLP iguale o supere a la lineal, con la lineal podemos decir *"el empleo sube/baja tanto por mes"*; con el MLP no hay un coeficiente así de claro. Para hablarle a un ministerio, **la explicabilidad suele pesar más** que un decimal de R². Por eso elegir el modelo no es solo una cuestión de métricas.

**Comprobar:**

```python
assert len(y_test_pred) == len(y_test)
assert nombre in ("lineal", "mlp")
print("Parte 3, comparación y elección de modelo: OK")
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

El monitor se **actualiza solo** cada `POLL_SECONDS` segundos (hilo en segundo plano). No hace falta pulsar un botón; interrumpan el runtime (■) cuando quieran detenerlo.

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
POLL_SECONDS = 30      # actualización automática cada 30 s
MAX_TICKS = 12         # tope ≈ 6 min; evita un bucle infinito en Colab


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

**Comprobar:**

```python
print("Parte 4, monitor en vivo: OK")
```

---

## Parte 5. Un tablero que reúne las capas de evidencia

Tener un buen modelo no basta: hay que **presentar la evidencia junta y bien rotulada**. Un **tablero** (*dashboard*) combina la **capa oficial** (modelo GEIH) con un **resumen del contexto** (titulares almacenados). Cada panel dice de dónde viene su dato.

```python
titulos = ["Oficial GEIH: observado vs. predicho (validación)"]
if news_stored > 0:
    titulos.append("Contexto: titulares almacenados (no oficial)")

dash = make_subplots(rows=len(titulos), cols=1, subplot_titles=titulos)

dash.add_trace(
    go.Scatter(x=y_val, y=y_val_lin, mode="markers", name="lineal"),
    row=1,
    col=1,
)

if news_stored > 0:
    dash.add_trace(
        go.Bar(x=["Titulares en almacén (L5)"], y=[news_stored], name="noticias"),
        row=2,
        col=1,
    )

dash.update_layout(
    height=350 * len(titulos),
    showlegend=False,
    title_text="Tablero de evidencia — capa oficial (GEIH) y contexto mediático",
)
dash.write_html(str(OUTPUTS_DIR / "l6_dashboard.html"))
dash.show()
print("Tablero guardado en:", OUTPUTS_DIR / "l6_dashboard.html")
```

**Cómo leerlo.** El panel oficial sostiene cualquier afirmación de empleo; el de contexto solo acompaña, y su título avisa que **no** es estadística oficial. A distintas audiencias mostraríamos distintos paneles (a quien decide, solo el oficial con su incertidumbre; a un analista, ambos).

**Comprobar:**

```python
assert (OUTPUTS_DIR / "l6_dashboard.html").is_file()
print("Parte 5, tablero de evidencia: OK")
```

---

## Tareas

Lo que practicaron aquí lo **implementan ustedes** en el cuaderno grupal **`week-3-group` (Ejercicio 2)**, sobre los agregados que construyan en el Ejercicio 1:

1. Dividan en **entrenamiento/validación/prueba** y entrenen el modelo elegido (lineal o MLP).
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
| **Presentación en vivo** (diapositivas; no van en el ZIP) | **Sábado 27 jun 2026** — tras charla L7 (~1 h) |
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

**Diapositivas (sábado 27):** siga la plantilla [project-presentation-template.pptx](/assets/documents/26-udenar-big-data/project-presentation-template.pptx) — **6 diapositivas:** título → canvas (requerimientos + ética) → pipeline → arquitectura → analítica → conclusiones. La ética se integra en canvas, pipeline, arquitectura y analítica (sin diapositiva final solo de ética).

**Sábado 27:** charla del instructor (L7) → presentaciones (L8). La charla puede ser versión en curso; el **informe en el ZIP** es la entrega escrita final.

<!-- end NOTEBOOK: -->
