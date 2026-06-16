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
notebook_description: Práctica individual de la Lección 6 (run-only). Modelamos sobre agregados GEIH (lineal y un MLP pequeño), hacemos gráficos ligados a una pregunta de decisión y discutimos la gobernanza al presentar evidencia. Código evaluable en week-3-group Parte B.
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

- [Week 3 hub](/teaching/26-udenar-big-data/week-3-hub-es/) *(when published)*

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

### Separar datos en entrenamiento y prueba

Para saber si un modelo **generaliza** (no solo memoriza), entrenamos con una parte de los datos y evaluamos con otra que el modelo **no vio**. **`train_test_split`** hace esa separación al azar.

```python
from sklearn.model_selection import train_test_split

# Datos de juguete: x va de 1 a 6, y es 10 veces x
X = [[1], [2], [3], [4], [5], [6]]
y = [10, 20, 30, 40, 50, 60]

# test_size=0.33 → un tercio para prueba; random_state fija el azar (reproducible)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
print("Entrenamiento:", len(X_train), "| Prueba:", len(X_test))
assert len(X_test) == 2
print("train_test_split: OK")
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

**De dónde venimos.** En la Lección 5 trajimos datos: una capa **`curated/`** de agregados GEIH (oficial) y, opcionalmente, un `staging/news_labor.parquet` de noticias (no oficial). Ya tenemos evidencia; falta **convertirla en una respuesta para quien decide**.

**Qué hacemos en esta lección.** Pasamos de *tener datos* a *informar una decisión*. La pregunta guía es:

> *Como analista del mercado laboral, ¿qué evidencia le mostraría esta semana a quien toma decisiones?*

Para responderla: (1) ajustamos un **modelo** sobre los agregados GEIH, (2) lo comparamos con un **modelo más flexible** (una red neuronal pequeña) para discutir un dilema real —**precisión vs. poder explicar**—, (3) hacemos **gráficos** ligados a la pregunta, y (4) reflexionamos sobre **cómo presentar evidencia con responsabilidad**: qué capa es oficial y cuál no, y a quién le mostramos qué.

**Una regla de gobernanza, desde el inicio.** Modelamos **solo sobre agregados** (departamento × mes), nunca sobre datos de personas individuales ni sobre el texto de las noticias. Las noticias, si aparecen, son un **monitor de discurso**, no una estadística.

**Prerrequisito.** Haber ejecutado **`l5-ingestion`** y tener (o simular) `data/curated/` y, opcional, `staging/news_labor.parquet`.

**Las tres capas de evidencia** que aparecen en esta lección:

| Capa | Fuente | Para qué la usamos |
|------|--------|--------------------|
| **Oficial** | Agregados GEIH en `curated/` | Modelo y gráfico principal |
| **Macro (opcional)** | TRM / COLCAP en `staging/` | Gráfico de contexto |
| **Medios (opcional)** | `news_labor.parquet` | Monitor — **no es dato oficial** |

**Este cuaderno es individual y solo para ejecutar** (run-only). El código evaluable está en **`week-3-group` Parte B**.

**Qué hace el cuaderno (en orden).**

| Parte | Tema |
|-------|------|
| **1** | Montar Drive, rutas a `curated/` e instalar librerías |
| **2** | Modelo **lineal** sobre agregados + gráfico (capa oficial) |
| **3** | **Red neuronal pequeña** sobre la misma tabla — precisión vs. explicabilidad |
| **4** | **Monitor** opcional de noticias (capa no oficial) |
| **5** | Cómo presentar la evidencia: audiencias y controles |

**Entrega de la semana:** el código evaluable va en **`week-3-group`**. Ver **Tareas** al final.

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

Instalamos analítica y visualización. **scikit-learn** para los modelos; **Plotly** y **matplotlib** para graficar.

```python
%pip install -q polars pyarrow scikit-learn plotly matplotlib
```

```python
import json

import matplotlib.pyplot as plt
import plotly.express as px
import polars as pl
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

## Parte 2. Modelar sobre agregados oficiales (regresión lineal)

**Idea.** Tomamos los agregados GEIH y ajustamos un modelo simple: predecir el empleo ponderado a partir del **mes** y el **año**. Es un ejemplo **didáctico** (no causal): sirve para ver el flujo entrenar → predecir → medir, y para tener una primera lectura de tendencia.

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

### Paso 2.2. Entrenar y evaluar

Separamos en entrenamiento/prueba (como en el Repaso), ajustamos la regresión lineal y medimos con R² y MAE.

```python
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)

lin = LinearRegression()
lin.fit(X_train, y_train)        # aprende con el 75 %
y_pred = lin.predict(X_test)     # predice el 25 % reservado

print("Lineal — R²:", round(r2_score(y_test, y_pred), 3))
print("Lineal — MAE:", round(mean_absolute_error(y_test, y_pred), 2))
```

### Paso 2.3. Graficar observado vs. predicho

Un gráfico de dispersión observado-contra-predicho muestra de un vistazo qué tan bien predice: cuanto más cerca de la diagonal, mejor. **El título dice de qué capa viene** el dato (oficial GEIH): rotular la fuente es parte de la gobernanza.

```python
fig = px.scatter(
    x=y_test,
    y=y_pred,
    labels={"x": "Observado (empleo ponderado)", "y": "Predicho (lineal)"},
    title="Capa oficial GEIH — modelo lineal",
)
fig.write_html(str(OUTPUTS_DIR / "l6_lineal_obs_pred.html"))  # guardamos la figura
fig.show()
```

**Comprobar:**

```python
assert len(y_pred) == len(y_test)
assert (OUTPUTS_DIR / "l6_lineal_obs_pred.html").is_file()
print("Parte 2, modelo lineal: OK")
```

---

## Parte 3. Un modelo más flexible: red neuronal pequeña

**Idea.** ¿Por qué no usar siempre el modelo más potente? Entrenamos una **red neuronal pequeña** (un *MLP*: perceptrón multicapa) sobre **la misma tabla** y la comparamos con la lineal. El objetivo no es ganar precisión, sino **vivir el dilema**: un modelo más flexible puede ajustar mejor, pero es **más difícil de explicar** a quien decide. Esa tensión —**precisión vs. explicabilidad**— es central en la gobernanza de datos.

### Paso 3.1. Escalar las entradas

Las redes neuronales aprenden mejor cuando las entradas están en una escala parecida. **`StandardScaler`** las centra y normaliza. Ajustamos el escalador **solo con el entrenamiento** (para no "mirar" la prueba).

```python
scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)  # aprende media/desviación con train
X_test_s = scaler.transform(X_test)        # aplica la misma transformación a test
print("Entradas escaladas.")
```

### Paso 3.2. Entrenar el MLP y comparar

Usamos **una** capa oculta con pocas neuronas: suficiente para ilustrar, sin sobreajustar una tabla pequeña.

```python
mlp = MLPRegressor(hidden_layer_sizes=(8,), max_iter=500, random_state=42)
mlp.fit(X_train_s, y_train)
y_mlp = mlp.predict(X_test_s)

print("MLP — R²:", round(r2_score(y_test, y_mlp), 3))
print("MLP — MAE:", round(mean_absolute_error(y_test, y_mlp), 2))
print()
print("Lineal  → R²:", round(r2_score(y_test, y_pred), 3),
      "| MAE:", round(mean_absolute_error(y_test, y_pred), 2))
print("MLP     → R²:", round(r2_score(y_test, y_mlp), 3),
      "| MAE:", round(mean_absolute_error(y_test, y_mlp), 2))
```

**Lectura.** Comparen las métricas. Aunque el MLP iguale o supere a la lineal, con la lineal podemos decir *"el empleo sube/baja tanto por mes"*; con el MLP no hay un coeficiente así de claro. Para hablarle a un ministerio, **la explicabilidad suele pesar más** que un decimal de R². Eso lo discutiremos en la Parte 5.

**Comprobar:**

```python
assert len(y_mlp) == len(y_test)
print("Parte 3, red neuronal pequeña: OK")
```

---

## Parte 4. Monitor de noticias (capa opcional, no oficial)

**Idea.** Si la Lección 5 dejó `news_labor.parquet`, podemos **monitorear el discurso** sobre empleo: cuántos titulares capturamos. Es una señal de **velocidad y variedad**, útil como contexto, pero **no es una medición de empleo**. Por eso el gráfico lo dice explícitamente en el título.

```python
news_path = STAGING_DIR / "news_labor.parquet"

if news_path.is_file():
    news = pl.read_parquet(news_path)
    n = news.height
    fig2 = px.bar(
        x=["Titulares de empleo capturados"],
        y=[n],
        labels={"x": "", "y": "Conteo"},
        title="Discurso mediático — NO es dato oficial DANE/GEIH",
    )
    fig2.write_html(str(OUTPUTS_DIR / "l6_monitor_noticias.html"))
    fig2.show()
    print("Titulares en el monitor:", n)
else:
    print("Sin news_labor.parquet — esta capa es opcional; continúe con la Parte 5.")
```

**Comprobar:**

```python
print("Parte 4, monitor de noticias: OK")
```

---

## Parte 5. Cómo presentar la evidencia: audiencias y controles

**Idea.** Tener un buen modelo no basta: hay que **decidir qué mostrar, a quién y con qué advertencias**. Un mismo resultado se comunica distinto a un ministro, a un analista o al público. Esta es la síntesis ética de la semana: el **tablero como acto de gobernanza**.

La siguiente plantilla es la que ustedes **completan y razonan** en el cuaderno grupal (Parte B). Aquí queda como guía:

### Capas de evidencia

1. **Oficial:** el modelo y el gráfico sobre agregados GEIH (`curated/`) — la base de cualquier afirmación.
2. **Secundaria (opcional):** macro (TRM/COLCAP) o el conteo de noticias — siempre **rotulada** como contexto, nunca mezclada con lo oficial sin avisar.

### Audiencias

- **Quien decide (ministro):** una cifra oficial con su incertidumbre; sin titulares fuera de contexto.
- **Analista:** las series completas y el diagnóstico del modelo (incluida la comparación lineal vs. MLP).
- **Público:** agregados con **supresión k=5** (como en la Lección 4), para no exponer celdas pequeñas.

### Controles

- Distinta **frecuencia de actualización**: GEIH es mensual; el stream, casi en vivo. No los presentemos como si tuvieran el mismo respaldo.
- La **elección de modelo** (lineal vs. MLP) se justifica en texto: por qué priorizamos explicabilidad o precisión.

---

## Tareas

Lo que practicaron aquí lo **implementan ustedes** en el cuaderno grupal **`week-3-group` (Parte B)**, sobre **sus** agregados de la Parte A:

1. **Elijan un modelo** (lineal o MLP) y justifiquen la elección pensando en quién decide.
2. Hagan al menos **dos gráficos** ligados a la pregunta de decisión, con la fuente rotulada.
3. (Opcional) Añadan el **monitor de noticias** como capa no oficial.
4. Escriban la **reflexión de gobernanza**: capas, audiencias y controles.

**Entrega grupal:** martes **23 jun 2026** — ZIP con `week-3-group-<group_id>.ipynb` + `manifest.json`.

<!-- end NOTEBOOK: -->
