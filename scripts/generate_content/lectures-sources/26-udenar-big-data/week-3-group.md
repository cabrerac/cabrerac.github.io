---
course_code: 26-udenar-big-data
title: Semana 3 — Ingesta, flujos y analítica (grupo)
description: Group Colab — Part A batch/stream ingestion on week-2 GEIH lake (Prefect, Kafka, audit); Part B analytics, charts, and governance on curated aggregates. Consolidates L5 + L6 homework.
session: 3
start_time: async
end_time: async
hours: 5
author: Christian Cabrera Jojoa
email: chc79@cam.ac.uk
position: Assistant Research Professor
department: Department of Computer Science and Technology
institution: University of Cambridge
layout: lecture
lecture_code: week-3-group
lecture_date: 20/06/2026
visible: false
skip_slides: true
skip_lecture_page: true
notebook_language: es
notebook_title: Semana 3 — ingesta, flujos y analítica (grupo)
notebook_description: Cuaderno canónico del grupo para la semana 3 (L5 + L6). Parte A — capa curated, audit, Prefect, Kafka RSS; Parte B — modelo supervisado, gráficos y gobernanza L6.3. Entrega ZIP martes 23 jun 2026.
---

<!-- NOTEBOOK: -->

## Instrucciones

**Propósito.** Cuaderno grupal para la semana 3 (Lecciones 5 y 6). Aquí está **todo el código evaluable**: ingesta batch/stream sobre el lakehouse de **`week-2-group`** y analítica con gobernanza sobre **agregados GEIH**.

**Requisito.** Ejecute primero **`l5-ingestion`** y **`l6-analytics`** (run-only). Copie patrones de esos cuadernos y de L4 (`audit`, agregados); **escriba** su propia implementación en grupo (bloque del **sábado 20 jun**).

**Datos de entrada.** Parquet particionado **`data/processed/geih-spine/`** (2022–2025) de week 2 en Google Drive. **No** re-harmonice CSV.

**Kafka.** Broker compartido (URL + SASL en Secrets de Colab o `.env`). Tópico sugerido: `udenar.{group_id}.news.raw`. Si Kafka no está disponible, documente fallback JSONL local (A5/A6).

**Recorrido de Vs (A7):** etapas batch = **GEIH**; etapas stream = **sin GEIH** (noticias). Debe quedar explícito en markdown.

**Entrega Moodle (martes 23 jun 2026, 23:59 Colombia):** ZIP `week-3-group-<group_id>.zip` con `week-3-group-<group_id>.ipynb` y `manifest.json` en la **raíz del ZIP**. **Sin** Parquet/CSV en el ZIP.

**Mapa del cuaderno (dos ejercicios)**

| Ejercicio | Tema | Entregable clave |
|-----------|------|------------------|
| **1** | Ingesta L5 (Parte A) | `curated/`, `audit.jsonl`, `schema_contract.json`, Kafka, A7 Vs tour |
| **2** | Analítica L6 (Parte B) | Modelo (lineal **o** MLP), ≥2 gráficos, gobernanza B6 |

Copie de **`l5-ingestion`** y **`l6-analytics`**:

| Qué copiar | Dónde está |
|------------|------------|
| `append_audit`, rutas Drive, Prefect `@flow` | L5 Partes 1–4 |
| `poll_rss_events`, productor/consumidor Kafka | L5 Partes 5–6 |
| `LinearRegression` / `MLPRegressor`, Plotly | L6 Partes 2–4 |
| Plantilla gobernanza L6.3 | L6 Parte 5 |

Use celdas **Comprobar:** de arriba abajo.

---

## Configuración — Drive, Kafka y rutas

Monte **Google Drive** igual que en [`l3-storage`](https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-big-data/l3-storage.ipynb) (Parte 1). Si trabaja en **local**, ponga `USE_GOOGLE_DRIVE = False`.

Defina constantes del grupo:

```python
GROUP_ID = "G1"  # cambie al id de su grupo
USE_GOOGLE_DRIVE = True
MODEL_CHOICE = "linear"  # "linear" o "mlp" — elija UNO para el ejercicio 2
TOPIC_RAW = f"udenar.{GROUP_ID}.news.raw"
RSS_FEEDS = [
    "https://www.portafolio.co/rss/economia.xml",
    "https://www.eltiempo.com/rss/economia.xml",
]
KEYWORDS = ("empleo", "desempleo", "mercado laboral", "trabajo", "geih")
ACTIVIDAD_OCUPADO = 1
```

```python
# SU CÓDIGO — montar Drive (IN_COLAB), WORK_ROOT, PROCESSED_DIR, CURATED_DIR,
# STAGING_DIR, AUDIT_PATH, SCHEMA_PATH, MANIFEST_PATH, OUTPUTS_DIR,
# append_audit() — copie de l5-ingestion Parte 1 y 3

```

**Comprobar:**

```python
assert WORK_ROOT.is_dir()
assert PROCESSED_DIR.is_dir()
assert MODEL_CHOICE in ("linear", "mlp")
print("Configuración: OK")
```

---

# Ejercicio 1 — Ingesta y flujos (L5, Parte A)

**Tarea.** Capa **curated** batch, **audit**, **Prefect**, productor/consumidor **Kafka** (o fallback), markdown **Vs tour**.

## Paso 1.1 — Puente week-2 (A0)

Documente en markdown las rutas a su spine 2022–2025 y campos clave de `manifest.json` de week 2.

```python
# SU CÓDIGO — listar particiones; mostrar claves del manifest

```

**Comprobar:**

```python
partitions = sorted(PROCESSED_DIR.glob("anio=*/mes=*/part-*.parquet"))
assert len(partitions) >= 12, "¿Falta el lakehouse week-2?"
print("Paso 1.1, puente week-2: OK")
```

---

## Paso 1.2 — Capa curated batch (A1)

Construya agregado mensual (o alineado a su charter) desde particiones → `curated/geih_*.parquet`. Registre cada paso en **`audit.jsonl`**.

```python
# SU CÓDIGO — Polars/DuckDB; append_audit por operación

```

**Comprobar:**

```python
curated_files = list(CURATED_DIR.glob("geih_*.parquet"))
assert len(curated_files) >= 1
assert AUDIT_PATH.is_file() and AUDIT_PATH.stat().st_size > 0
print("Paso 1.2, curated batch: OK")
```

---

## Paso 1.3 — Contrato de esquema (A2)

Escriba **`schema_contract.json`** (columnas, dtypes, fuente, nota de retención).

```python
# SU CÓDIGO

```

**Comprobar:**

```python
contract = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
assert "columns" in contract and len(contract["columns"]) >= 3
print("Paso 1.3, schema_contract: OK")
```

---

## Paso 1.4 — Orquestación Prefect (A3)

Envuelva A1 + validación en un `@flow` Prefect (o script documentado si Prefect falla en Colab).

```python
# SU CÓDIGO — @task / @flow

```

**Comprobar:**

```python
audit_text = AUDIT_PATH.read_text(encoding="utf-8")
assert "prefect" in audit_text.lower() or "batch" in audit_text.lower()
print("Paso 1.4, Prefect: OK — verifique audit.jsonl")
```

---

## Paso 1.5 — Macro Banrep (A4, opcional)

Pull SDMX TRM (+ COLCAP si hay tiempo) → `staging/macro_daily.parquet` + audit.

```python
# SU CÓDIGO — opcional

```

---

## Paso 1.6 — Productor Kafka RSS (A5)

Poll **acotado** (p. ej. ≤2 min) → publique JSON a `{group_id}.news.raw`. Marque `"geih": false` en cada evento.

```python
# SU CÓDIGO — kafka-python o fallback JSONL

```

**Comprobar:**

```python
assert STAGING_DIR.is_dir()
print("Paso 1.6, productor: OK — revise audit")
```

---

## Paso 1.7 — Consumidor y staging stream (A6)

Dedupe por URL; ventana o conteo → `staging/news_labor.parquet` + audit.

```python
# SU CÓDIGO

```

**Comprobar:**

```python
news_path = STAGING_DIR / "news_labor.parquet"
if news_path.is_file():
    import polars as pl
    assert pl.read_parquet(news_path).height >= 0
print("Paso 1.7, consumidor: OK")
```

---

## Paso 1.8 — Markdown: batch vs stream y Vs tour (A7)

Tabla **obligatoria** (etapas 0–5): V ejercitada, ¿GEIH sí/no?, ¿sirve para la pregunta del charter?

```markdown
# SU TABLA Y TEXTO (≥ 120 palabras) — L5.2, Jarrahi source-fit
```

---

## Paso 1.9 — Stretch replay (A8, opcional)

Throughput con `news_events_replay.jsonl` — documente si lo intentó.

---

## Paso 1.10 — Actualizar manifest Parte A (A9)

Amplíe `manifest.json`: conteos audit, tópicos Kafka, filas batch vs stream.

```python
# SU CÓDIGO

```

**Comprobar:**

```python
data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
assert any(k in data for k in ("audit", "kafka", "ingesta", "lakehouse"))
print("Paso 1.10, manifest Parte A: OK")
```

---

# Ejercicio 2 — Analítica y gobernanza (L6, Parte B)

**Tarea.** Modelo supervisado sobre **agregados GEIH**, ≥2 gráficos, gobernanza L6.3 con **dos capas de evidencia**.

## Paso 2.1 — Pregunta de decisión (B0)

```markdown
# SU PREGUNTA (default del curso o del PDF de proyecto §3)
```

---

## Paso 2.2 — Cargar curated y validar esquema (B1)

```python
# SU CÓDIGO — pl.read_parquet; compare dtypes con schema_contract.json

```

**Comprobar:**

```python
assert len(curated_files) >= 1
print("Paso 2.2, carga curated: OK")
```

---

## Paso 2.3 — Modelo supervisado (B2)

| Elección | Clase sklearn |
|----------|----------------|
| `MODEL_CHOICE == "linear"` | `LinearRegression` o `LogisticRegression` |
| `MODEL_CHOICE == "mlp"` | `MLPRegressor` o `MLPClassifier` (1 capa oculta, pocas unidades) |

**Solo agregados GEIH** — no microdatos ni texto de noticias. Markdown: ¿**apoya / no apoya** la decisión? Justifique lineal vs MLP si aplica.

```python
# SU CÓDIGO

```

**Comprobar:**

```python
assert "model" in dir() or "lin" in dir() or "mlp" in dir()
print("Paso 2.3, modelo: OK — complete markdown")
```

---

## Paso 2.4 — Gráfico 1: capa oficial GEIH (B3)

Plotly o matplotlib con **pie de figura** ligado a la pregunta de decisión. Guarde en `outputs/`.

```python
# SU CÓDIGO

```

**Comprobar:**

```python
assert chart1_path.is_file()
print("Paso 2.4, gráfico 1: OK")
```

---

## Paso 2.5 — Gráfico 2: macro o diagnóstico (B4)

Segundo gráfico: TRM/COLCAP **o** diagnóstico del modelo.

```python
# SU CÓDIGO

```

**Comprobar:**

```python
assert chart2_path.is_file()
print("Paso 2.5, gráfico 2: OK")
```

---

## Paso 2.6 — Gráfico stream (B5, opcional)

Tasa de palabras clave en `news_labor.parquet`. Título: **“discurso mediático, no dato oficial”**.

```python
# SU CÓDIGO — opcional

```

---

## Paso 2.7 — Gobernanza L6.3 (B6)

Markdown **obligatorio**: dos capas (oficial GEIH + opcional macro/stream); audiencias; controles; nota lineal vs MLP. Enlace §6–§7 del PDF de requerimientos si aplica.

```markdown
# SU TEXTO
```

---

## Paso 2.8 — Manifest final (B7)

Añada: tipo de modelo, rutas de gráficos, resumen gobernanza (una línea).

```python
# SU CÓDIGO

```

**Comprobar:**

```python
data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
assert any(k in data for k in ("modelo", "analitica", "governance", "graficos"))
print("Paso 2.8, manifest final: OK")
```

---

## Registro de contribución (grupo)

Cada integrante añade **una línea** con tarea concreta. Indique el **escriba de semana 3** (consolidación del ZIP).

```python
contribution_log = """
- ...
Escriba semana 3: ...
"""
print(contribution_log)
```

---

## Tarea grupal (Moodle)

ZIP **`week-3-group-<group_id>.zip`** hasta el **martes 23 de junio de 2026, 23:59 (Colombia)**:

| Archivo | Descripción |
|---------|-------------|
| `week-3-group-<group_id>.ipynb` | Este cuaderno ejecutado (plantilla Colab: `week-3-group`) |
| `manifest.json` | Metadatos Partes A + B (raíz del ZIP) |

**Reflexión individual:** `week-3-reflection-<student>.pdf` el **miércoles 24 de junio de 2026** — plantilla *(cuando se publique)*.

**Requerimientos del proyecto:** avance en la sesión del **sábado 20 jun** (bloque analítica + gobernanza de capas).

<!-- end NOTEBOOK: -->
