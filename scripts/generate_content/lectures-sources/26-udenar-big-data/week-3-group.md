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
notebook_description: Cuaderno canónico del grupo para la semana 3 (Lecciones 5 y 6). Ejercicio 1 — ingesta batch y stream sobre el lakehouse de la semana 2 (curated, bitácora, Prefect, Kafka). Ejercicio 2 — modelo, gráficos y gobernanza al presentar evidencia. Entrega ZIP martes 23 jun 2026.
---

<!-- NOTEBOOK: -->

## Instrucciones

**Propósito.** Este es el cuaderno **grupal** de la semana 3, donde está **todo el código que se evalúa**. Reúne las dos lecciones: la **ingesta** de la Lección 5 (traer datos batch y stream) y la **analítica** de la Lección 6 (convertir datos en evidencia para una decisión).

**Antes de empezar.** Ejecuten primero los cuadernos individuales **`l5-ingestion`** y **`l6-analytics`** (solo lectura). Allí cada concepto está explicado paso a paso; aquí ustedes **escriben** su propia versión sobre **sus** datos. Pueden copiar funciones de esos cuadernos y de la Lección 4, pero **entiéndanlas** antes de pegarlas.

**Datos de entrada.** El lakehouse particionado **`data/processed/geih-spine/`** (2022–2025) que construyeron en `week-2-group`, en Google Drive. **No** vuelvan a harmonizar CSV.

**Kafka.** Usaremos un servidor compartido (credenciales en *Secrets* de Colab). Si no está disponible, el cuaderno cae a un **modo sin servidor** que guarda los eventos en un archivo local; documenten en markdown si trabajaron así.

**Entrega Moodle (martes 23 jun 2026, 23:59 Colombia):** un ZIP `week-3-group-<group_id>.zip` con el cuaderno ejecutado `week-3-group-<group_id>.ipynb` y `manifest.json` en la **raíz del ZIP**. **Sin** archivos Parquet ni CSV.

**Mapa del cuaderno (dos ejercicios)**

| Ejercicio | Tema | Entregable clave |
|-----------|------|------------------|
| **1** | Ingesta (Lección 5) | `curated/`, `audit.jsonl`, `schema_contract.json`, productor/consumidor de noticias, markdown de *V* |
| **2** | Analítica (Lección 6) | Modelo (lineal **o** red neuronal), **2 gráficos**, reflexión de gobernanza |

**De dónde copiar cada pieza** (ya las vieron explicadas):

| Qué necesitan | Dónde está explicado |
|---------------|----------------------|
| Montar Drive, rutas, `append_audit`, capa curated | `l5-ingestion`, Partes 1 y 3 |
| Flujo Prefect (`@task` / `@flow`) | `l5-ingestion`, Parte 4 |
| Productor y consumidor de noticias | `l5-ingestion`, Partes 5 y 6 |
| `train_test_split`, modelo lineal / MLP, métricas | `l6-analytics`, Partes 2 y 3 |
| Gráficos y reflexión de gobernanza | `l6-analytics`, Partes 4 y 5 |

Ejecuten las celdas **de arriba abajo** y revisen cada **Comprobar:**.

---

## Configuración: Drive, Kafka y rutas

Monten **Google Drive** igual que en [`l3-storage`](https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-big-data/l3-storage.ipynb) (Parte 1). Si trabajan en **local**, pongan `USE_GOOGLE_DRIVE = False`.

Primero, las constantes del grupo. Cambien `GROUP_ID` por el de su grupo y elijan **un** modelo para el Ejercicio 2:

```python
GROUP_ID = "G1"          # cambie al id de su grupo
USE_GOOGLE_DRIVE = True
MODEL_CHOICE = "linear"  # "linear" o "mlp" — elijan UNO para el Ejercicio 2

# Tópico de noticias propio del grupo (evita mezclar mensajes entre grupos)
TOPIC_NEWS = f"udenar.{GROUP_ID}.news.raw"

RSS_FEEDS = [
    "https://www.portafolio.co/rss/economia.xml",
    "https://www.eltiempo.com/rss/economia.xml",
]
KEYWORDS = ("empleo", "desempleo", "mercado laboral", "trabajo", "geih")
ACTIVIDAD_OCUPADO = 1    # en GEIH, actividad == 1 = ocupado (como en L4)
```

Ahora monten Drive y definan rutas y la función de bitácora. Copien el patrón de `l5-ingestion` (Partes 1 y 3):

```python
# SU CÓDIGO — definan, copiando de l5-ingestion:
#   IN_COLAB, WORK_ROOT, PROCESSED_DIR, CURATED_DIR, STAGING_DIR,
#   AUDIT_PATH, SCHEMA_PATH, MANIFEST_PATH, OUTPUTS_DIR
#   la función append_audit(evento)
#   instalen e importen las librerías que usen (polars, prefect, kafka-python, sklearn, plotly)

```

**Comprobar:**

```python
assert WORK_ROOT.is_dir()
assert PROCESSED_DIR.is_dir(), "No encuentro el lakehouse de la semana 2."
assert MODEL_CHOICE in ("linear", "mlp")
print("Configuración: OK")
```

---

# Ejercicio 1 — Ingesta y flujos (Lección 5)

**Meta.** Construir una capa **curated** gobernada sobre su lakehouse, dejar **bitácora** y **contrato de esquema**, orquestar con **Prefect**, y traer una fuente **stream** (noticias) con productor y consumidor.

## Paso 1.1 — Puente con el lakehouse de la semana 2

Confirmen que el lakehouse está en Drive y describan en markdown sus rutas y los campos de `manifest.json` de la semana 2.

```python
# SU CÓDIGO — listar particiones del lakehouse y mostrar claves del manifest

```

**Comprobar:**

```python
partitions = sorted(PROCESSED_DIR.glob("anio=*/mes=*/part-*.parquet"))
assert len(partitions) >= 12, "Falta el lakehouse de la semana 2 (esperamos ≥12 meses)."
print("Paso 1.1, puente con el lakehouse: OK")
```

---

## Paso 1.2 — Capa curated gobernada

Construyan un agregado (por departamento y mes, o el que pida su pregunta de decisión) desde las particiones → `curated/geih_*.parquet`. **Registren cada operación** en `audit.jsonl` con `append_audit`.

```python
# SU CÓDIGO — agregado con Polars o DuckDB + append_audit por operación

```

**Comprobar:**

```python
curated_files = list(CURATED_DIR.glob("geih_*.parquet"))
assert len(curated_files) >= 1, "No se escribió ningún agregado en curated/."
assert AUDIT_PATH.is_file() and AUDIT_PATH.stat().st_size > 0, "La bitácora está vacía."
print("Paso 1.2, capa curated: OK")
```

---

## Paso 1.3 — Contrato de esquema

Escriban **`schema_contract.json`** con las columnas del curated, sus tipos, la fuente y una nota de retención (recuerden: agregados, no microdatos).

```python
# SU CÓDIGO — construir el dict del contrato y guardarlo como JSON

```

**Comprobar:**

```python
contract = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
assert "columns" in contract and len(contract["columns"]) >= 3
print("Paso 1.3, contrato de esquema: OK")
```

---

## Paso 1.4 — Orquestación con Prefect

Envuelvan el agregado + su validación en un **flujo Prefect** (`@task` / `@flow`). Si Prefect falla en Colab, documenten en markdown y dejen los pasos como funciones encadenadas.

```python
# SU CÓDIGO — @task para construir/validar, @flow que los encadene

```

**Comprobar:**

```python
audit_text = AUDIT_PATH.read_text(encoding="utf-8")
assert "prefect" in audit_text.lower() or "batch" in audit_text.lower()
print("Paso 1.4, orquestación: OK — revisen audit.jsonl")
```

---

## Paso 1.5 — Contexto macro (opcional)

Si tienen tiempo, traigan una serie macro del Banco de la República (la TRM, vía su servicio SDMX) → `staging/macro_daily.parquet` + bitácora. Es contexto, no GEIH.

```python
# SU CÓDIGO — opcional

```

---

## Paso 1.6 — Productor de noticias

Sondeen los feeds RSS, filtren por palabras clave de empleo y **publiquen** los eventos al tópico `TOPIC_NEWS` (o al archivo local si no hay servidor). Marquen `geih=False` en cada evento.

```python
# SU CÓDIGO — poll_rss_events + envío al tópico (o fallback local)

```

**Comprobar:**

```python
assert STAGING_DIR.is_dir()
print("Paso 1.6, productor de noticias: OK — revisen audit.jsonl")
```

---

## Paso 1.7 — Consumidor y staging

Lean el tópico (o el archivo local), **deduplican por URL** y guarden el resultado en `staging/news_labor.parquet` + bitácora.

```python
# SU CÓDIGO — consumidor + deduplicado + escritura de staging

```

**Comprobar:**

```python
news_path = STAGING_DIR / "news_labor.parquet"
if news_path.is_file():
    assert pl.read_parquet(news_path).height >= 0
print("Paso 1.7, consumidor y staging: OK")
```

---

## Paso 1.8 — Markdown: ¿qué *V* ejercita cada fuente?

Escriban una tabla y un texto (≈120 palabras) que comparen **GEIH** (volumen, veracidad; lenta, estructurada) con las **noticias** (velocidad, variedad; no oficial). Expliquen **qué fuente encaja con su pregunta de decisión** y por qué.

```markdown
# SU TABLA Y TEXTO — compare GEIH vs noticias por cada V; relacione con su pregunta
```

---

## Paso 1.9 — Reproducción a alta tasa (opcional)

Si quieren explorar **velocidad**, reproduzcan muchos eventos desde `news_events_replay.jsonl` y midan el tiempo. Documenten lo que observaron.

```python
# SU CÓDIGO — opcional

```

---

## Paso 1.10 — Actualizar el manifiesto (Ejercicio 1)

Amplíen `manifest.json` con metadatos de la ingesta: número de líneas en la bitácora, tópico usado, filas en batch vs. stream.

```python
# SU CÓDIGO — leer manifest, actualizar y volver a guardar

```

**Comprobar:**

```python
data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
assert any(k in data for k in ("audit", "kafka", "ingesta", "lakehouse"))
print("Paso 1.10, manifiesto (Ejercicio 1): OK")
```

---

# Ejercicio 2 — Analítica y gobernanza (Lección 6)

**Meta.** Convertir los agregados en **evidencia para una decisión**: un modelo, al menos dos gráficos rotulados por fuente, y una reflexión sobre cómo presentar todo con responsabilidad. **Modelen solo sobre agregados**, nunca sobre microdatos ni texto.

## Paso 2.1 — La pregunta de decisión

Escriban en markdown la pregunta que van a responder (la del curso por defecto, o una de su proyecto).

```markdown
# SU PREGUNTA DE DECISIÓN
```

---

## Paso 2.2 — Cargar curated y validar contra el contrato

Lean los agregados del Ejercicio 1 y verifiquen que sus columnas y tipos coinciden con `schema_contract.json`.

```python
# SU CÓDIGO — leer curated y comparar con el contrato

```

**Comprobar:**

```python
assert len(curated_files) >= 1
print("Paso 2.2, carga de agregados: OK")
```

---

## Paso 2.3 — Entrenar el modelo elegido

Según `MODEL_CHOICE`, entrenen y evalúen. Expliquen en markdown si el resultado **apoya o no** la decisión, y por qué eligieron ese modelo.

| Si `MODEL_CHOICE` es… | Usen |
|------------------------|------|
| `"linear"` | `LinearRegression` o `LogisticRegression` |
| `"mlp"` | `MLPRegressor` o `MLPClassifier` (1 capa oculta, pocas neuronas) |

```python
# SU CÓDIGO — train_test_split, fit, predict, R²/MAE (o accuracy)

```

**Comprobar:**

```python
assert any(name in dir() for name in ("model", "lin", "mlp"))
print("Paso 2.3, modelo: OK — completen el markdown")
```

---

## Paso 2.4 — Gráfico 1: capa oficial GEIH

Hagan un gráfico (Plotly o matplotlib) sobre los agregados, con un **título que nombre la fuente** y un pie ligado a la pregunta de decisión. Guárdenlo en `outputs/`.

```python
# SU CÓDIGO — guardar la figura en chart1_path dentro de OUTPUTS_DIR

```

**Comprobar:**

```python
assert chart1_path.is_file()
print("Paso 2.4, gráfico 1: OK")
```

---

## Paso 2.5 — Gráfico 2: contexto o diagnóstico

Un segundo gráfico: contexto macro (TRM) **o** un diagnóstico del modelo (p. ej. observado vs. predicho).

```python
# SU CÓDIGO — guardar la figura en chart2_path

```

**Comprobar:**

```python
assert chart2_path.is_file()
print("Paso 2.5, gráfico 2: OK")
```

---

## Paso 2.6 — Gráfico de noticias (opcional)

Si trajeron noticias, grafiquen su conteo. El título **debe** decir que es discurso mediático, **no** dato oficial.

```python
# SU CÓDIGO — opcional

```

---

## Paso 2.7 — Reflexión de gobernanza

Escriban un markdown que cubra: las **capas de evidencia** (oficial GEIH + opcional macro/noticias, siempre rotuladas), las **audiencias** (quien decide / analista / público) y los **controles** (supresión k=5, frecuencia de actualización, elección de modelo).

```markdown
# SU TEXTO — capas, audiencias y controles
```

---

## Paso 2.8 — Manifiesto final

Añadan a `manifest.json`: tipo de modelo elegido, rutas de los gráficos y un resumen de una línea de la reflexión de gobernanza.

```python
# SU CÓDIGO — actualizar el manifiesto

```

**Comprobar:**

```python
data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
assert any(k in data for k in ("modelo", "analitica", "governance", "graficos"))
print("Paso 2.8, manifiesto final: OK")
```

---

## Registro de contribución (grupo)

Cada integrante añade **una línea** con la tarea concreta que hizo. Indiquen quién fue el **escriba de la semana** (quien consolida y sube el ZIP).

```python
contribution_log = """
- ...
Escriba de la semana 3: ...
"""
print(contribution_log)
```

---

## Tarea grupal (Moodle)

Suban el ZIP **`week-3-group-<group_id>.zip`** hasta el **martes 23 de junio de 2026, 23:59 (Colombia)**:

| Archivo | Descripción |
|---------|-------------|
| `week-3-group-<group_id>.ipynb` | Este cuaderno ejecutado (renómbrenlo al exportar) |
| `manifest.json` | Metadatos de los Ejercicios 1 y 2 (en la raíz del ZIP) |

**Reflexión individual:** `week-3-reflection-<student>.pdf` el **miércoles 24 de junio de 2026** *(plantilla cuando se publique)*.

**Proyecto:** avancen en la sesión del **sábado 20 jun** (bloque de analítica y gobernanza de capas de evidencia).

<!-- end NOTEBOOK: -->
