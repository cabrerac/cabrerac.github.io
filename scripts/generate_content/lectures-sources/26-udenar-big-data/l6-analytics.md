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
notebook_description: Práctica individual de la Lección 6 (run-only). Modelo lineal vs MLP pequeño sobre agregados GEIH, gráficos con pregunta de decisión y capa opcional de noticias. Código evaluable en week-3-group Parte B.
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

Repasamos lo mínimo para las Partes 1 a 5. Los modelos corren **solo sobre agregados GEIH** — nunca sobre microdatos ni texto de noticias.

### Partición train/test con `sklearn`

Separamos filas para entrenar y evaluar sin mezclar:

```python
from sklearn.model_selection import train_test_split

X = [[1], [2], [3], [4], [5], [6]]
y = [10, 20, 30, 40, 50, 60]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
print("Train:", len(X_train), "| Test:", len(X_test))
assert len(X_test) == 2
print("train_test_split: OK")
```

### Regresión lineal en una línea

```python
from sklearn.linear_model import LinearRegression

model = LinearRegression()
model.fit([[1], [2], [3]], [2, 4, 6])
pred = model.predict([[4]])[0]
print("Predicción x=4:", pred)
assert abs(pred - 8.0) < 0.01
print("LinearRegression: OK")
```

---

## Instrucciones

**Propósito.** L5 terminó en **noticias / Kafka** (velocidad, variedad). L6 pregunta: **¿qué evidencia mostraría al decisor?** — con modelos y gráficos sobre **agregados oficiales**, sin confundir capas.

**Prerrequisito.** Ejecute **`l5-ingestion`** y tenga (o simule con solución instructor) salidas en `data/curated/` y opcionalmente `staging/news_labor.parquet`.

**Capas de evidencia (L6.3).**

| Capa | Fuente | Uso |
|------|--------|-----|
| **Oficial** | `curated/` GEIH | Modelo + gráfico principal |
| **Macro (opcional)** | TRM/COLCAP en `staging/` | Gráfico secundario |
| **Medios (opcional)** | `news_labor.parquet` | Monitor — **no dato oficial** |

**Pregunta de decisión (por defecto):** *Como analista del mercado laboral, ¿qué evidencia mostraría al decisor esta semana?*

**Cuaderno individual:** run-only. **Evaluable:** **`week-3-group` Parte B**.

**Qué hace el cuaderno (en orden).**

| Parte | Tema |
|-------|------|
| **1** | Drive y rutas a `curated/` |
| **2** | Regresión **lineal** + gráfico (capa oficial) |
| **3** | **MLP pequeño** — mismo agregado, contraste de gobernanza |
| **4** | Monitor stream opcional (noticias) |
| **5** | Plantilla markdown de gobernanza (L6.3) |

**Entrega semana 3:** código evaluable en **`week-3-group`**. Ver **Tareas** al final.

---

## Parte 1. Configuración: Drive y rutas

Montamos la misma raíz que en L3–L5.

```python
from pathlib import Path

USE_GOOGLE_DRIVE = True

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

CURATED_DIR = WORK_ROOT / "data" / "curated"
STAGING_DIR = WORK_ROOT / "data" / "staging"
SCHEMA_PATH = WORK_ROOT / "data" / "schema_contract.json"
MANIFEST_PATH = WORK_ROOT / "manifest.json"
OUTPUTS_DIR = WORK_ROOT / "outputs"
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

curated_files = sorted(CURATED_DIR.glob("geih_*.parquet"))
print("Curated:", len(curated_files), "archivos")
```

Instalamos librerías de analítica y visualización:

```python
%pip install -q polars pyarrow scikit-learn plotly matplotlib
```

```python
import json

import matplotlib.pyplot as plt
import polars as pl
import plotly.express as px
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
    "Complete week-3-group Parte A o use la solución instructor."
)
print("Parte 1, configuración: OK")
```

---

## Parte 2. Analítica batch: regresión lineal

Cargamos agregados mensuales por departamento y predecimos **ponderado** a partir de **mes** y **año** (ejemplo didáctico — no causal).

```python
df = pl.read_parquet(curated_files[0])
if "ponderado" not in df.columns and "suma_ponderada" in df.columns:
    df = df.rename({"suma_ponderada": "ponderado"})
feature_cols = [c for c in ("mes", "anio") if c in df.columns]
X = df.select(feature_cols).to_numpy()
y = df["ponderado"].to_numpy()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
lin = LinearRegression()
lin.fit(X_train, y_train)
y_pred = lin.predict(X_test)
print("Linear R²:", round(r2_score(y_test, y_pred), 3))
print("Linear MAE:", round(mean_absolute_error(y_test, y_pred), 2))
```

Gráfico con etiqueta de capa oficial:

```python
fig = px.scatter(
    x=y_test,
    y=y_pred,
    labels={"x": "Observado (ponderado)", "y": "Predicho (lineal)"},
    title="Capa oficial GEIH — modelo lineal (demo instructor)",
)
fig.show()
```

**Comprobar:**

```python
assert len(y_pred) == len(y_test)
print("Parte 2, regresión lineal: OK")
```

---

## Parte 3. Contraste: MLP pequeño (misma tabla)

El MLP puede ajustar mejor en muestra pequeña pero **cuesta explicar** al ministerio; el lineal favorece **transparencia** (L6.3).

```python
scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s = scaler.transform(X_test)
mlp = MLPRegressor(hidden_layer_sizes=(8,), max_iter=500, random_state=42)
mlp.fit(X_train_s, y_train)
y_mlp = mlp.predict(X_test_s)
print("MLP R²:", round(r2_score(y_test, y_mlp), 3))
print("MLP MAE:", round(mean_absolute_error(y_test, y_mlp), 2))
```

**Comprobar:**

```python
assert len(y_mlp) == len(y_test)
print("Parte 3, MLP: OK")
```

---

## Parte 4. Monitor de stream (opcional, no GEIH)

Si existe `news_labor.parquet` de L5 / Parte A, mostramos conteo con etiqueta explícita.

```python
news_path = STAGING_DIR / "news_labor.parquet"
if news_path.is_file():
    news = pl.read_parquet(news_path)
    n = news.height
    fig2 = px.bar(
        x=["Noticias filtradas"],
        y=[n],
        title="Discurso mediático — NO dato oficial DANE/GEIH",
        labels={"x": "", "y": "Conteo en ventana"},
    )
    fig2.show()
else:
    print("Sin news_labor.parquet — omita B5 en grupo o complete Parte A6.")
```

**Comprobar:**

```python
print("Parte 4, monitor stream: OK")
```

---

## Parte 5. Plantilla gobernanza (L6.3)

Complete esta plantilla en el cuaderno grupal (**B6**). Demo instructor:

### Capas de evidencia

1. **Oficial:** modelo + gráfico sobre agregados GEIH (`curated/`).
2. **Secundaria (opcional):** macro TRM/COLCAP o conteo de noticias — siempre **etiquetada**.

### Audiencias

- **Ministro:** una cifra oficial + incertidumbre; sin titulares sin contexto.
- **Analista:** series completas + diagnóstico del modelo.
- **Público:** agregados suprimidos (k=5) — callback L4.

### Controles

- Supresión k=5 en publicación; refresh mensual GEIH vs minutos en stream.
- Elección lineal vs MLP documentada en markdown.

---

## Tareas

En **`week-3-group` Parte B** implemente **B0–B7** sobre sus salidas de Parte A: elija **lineal o MLP**, ≥2 gráficos, gobernanza L6.3.

**Entrega grupal:** martes **23 jun 2026** — ZIP con `week-3-group-<group_id>.ipynb` + `manifest.json`.

<!-- end NOTEBOOK: -->
