---
course_code: 26-udenar-big-data
title: Semana 3 — Ingesta, flujos y analítica (grupo)
description: Group Colab — Exercise 1 builds a governed curated layer for all GEIH years (2022-2025) with audit, schema contract, and a Prefect ETL flow; Exercise 2 trains models (train/val/test) and builds decision charts plus a dashboard. Consolidates L5 + L6 homework.
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
notebook_description: Cuaderno canónico del grupo para la semana 3 (Lecciones 5 y 6). Ejercicio 1 — construir la capa curated para todos los años GEIH (2022-2025) con bitácora, contrato de esquema y un flujo Prefect (ETL). Ejercicio 2 — entrenar modelos (entrenamiento/validación/prueba) y armar gráficos y un tablero. Entrega ZIP martes 23 jun 2026.
---

<!-- NOTEBOOK: -->

## Instrucciones

Este es el cuaderno **grupal** de la semana 3. Tiene dos ejercicios sobre **su** lakehouse GEIH: **Ejercicio 1** construye la capa **curated para todos los años** (2022–2025) de forma gobernada; **Ejercicio 2** entrena modelos y arma los gráficos para responder una pregunta de decisión.

**Antes de empezar.** Ejecuten primero los cuadernos individuales **`l5-ingestion`** y **`l6-analytics`** (solo lectura). Allí cada concepto está explicado paso a paso. Aquí ustedes **escriben** su propia versión sobre **sus** datos. Pueden copiar funciones de esos cuadernos y de la Lección 4, pero **entiéndanlas** antes de pegarlas.

**Datos de entrada.** El lakehouse particionado **`data/processed/geih-spine/`** (2022–2025) que construyeron en `week-2-group`, en Google Drive. **No** vuelvan a harmonizar CSV.

**Sobre el streaming.** La parte de Kafka y noticias de la Lección 5 es **individual** (para entender *velocidad* y *variedad*); **no** va en este cuaderno grupal. Aquí el foco es el **camino batch GEIH**: de las particiones a una capa curada y de ahí a los modelos.

**Entrega Moodle (martes 23 jun 2026, 23:59 Colombia):** un ZIP `week-3-group-<group_id>.zip` con **solo dos archivos** en la raíz: el cuaderno ejecutado `week-3-group-<group_id>.ipynb` y `manifest.json`. **Sin** Parquet, CSV ni copias de `audit.jsonl` / `schema_contract.json` en el ZIP — esos archivos viven en **Drive** junto al lakehouse; el **manifiesto** resume la bitácora y el contrato para que el instructor pueda calificar sin abrir Drive.

**Mapa del cuaderno (dos ejercicios)**

| Ejercicio | Tema | Entregable clave |
|-----------|------|------------------|
| **1** | Curated de todos los años (Lección 5) | En **Drive:** `curated/`, `audit.jsonl`, `schema_contract.json`, flujo Prefect; resumen en `manifest.json` |
| **2** | Modelos y gráficos (Lección 6) | Modelo lineal con train/val/prueba, **2 gráficos** y un **tablero** |

**De dónde copiar cada pieza** (ya las vieron explicadas):

| Qué necesitan | Dónde está explicado |
|---------------|----------------------|
| Montar Drive, rutas, `append_audit`, capa curated | `l5-ingestion`, Partes 1 y 3 |
| Flujo Prefect ETL de **un año** (`batch_flow_year`) | `l5-ingestion`, Parte 4 |
| One-hot de `dpto`, split train/val/prueba, regresión lineal y explicabilidad | `l6-analytics`, Repaso y Parte 3 |
| Referencias (mapa GeoJSON + servicios OSM) y carga de `curated/` | `l6-analytics`, Parte 1 |
| Tablero con varias vistas (mapa, tendencia, modelo) | `l6-analytics`, Partes 2 y 5 |

Ejecuten las celdas **de arriba abajo** y revisen cada **Comprobar:**.

---

## Configuración: Drive y rutas

Monten **Google Drive** igual que en [`l3-storage`](https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-big-data/l3-storage.ipynb) (Parte 1). Si trabajan en **local**, pongan `USE_GOOGLE_DRIVE = False`.

Primero, las constantes del grupo. Cambien `GROUP_ID` por el de su grupo:

```python
GROUP_ID = "G1"          # cambie al id de su grupo
USE_GOOGLE_DRIVE = True

ACTIVIDAD_OCUPADO = 1    # en GEIH, actividad == 1 = ocupado (como en L4)
```

Ahora monten Drive y definan rutas y la función de bitácora. Copien el patrón de `l5-ingestion` (Partes 1 y 3):

```python
# SU CÓDIGO — definan, copiando de l5-ingestion:
#   IN_COLAB, WORK_ROOT, PROCESSED_DIR, CURATED_DIR,
#   AUDIT_PATH, SCHEMA_PATH, MANIFEST_PATH, OUTPUTS_DIR
#   la función append_audit(evento)
#   instalen e importen las librerías que usen (polars, prefect, scikit-learn, plotly)

```

**Comprobar:**

```python
assert WORK_ROOT.is_dir()
assert PROCESSED_DIR.is_dir(), "No encuentro el lakehouse de la semana 2."
print("Configuración: OK")
```

---

# Ejercicio 1 — Capa curated de todos los años (Lección 5)

**Meta.** Construir una capa **curated** gobernada que cubra **todos los años** del lakehouse (2022–2025), dejar **bitácora** y **contrato de esquema**, y orquestar el ETL con **Prefect**.

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
print("Particiones encontradas:", len(partitions))
```

---

## Paso 1.2 — Curated de todos los años

En `l5-ingestion`, la Parte 3 hace el ETL **a mano** para **un mes**, la Parte 4 lo **orquesta con Prefect** para **un año** (p. ej. 2022). Aquí **extienden** ese patrón: recorran **todas** las particiones de 2022–2025, calculen el agregado por departamento y mes, y **únanlo** en una sola tabla → `curated/geih_dept_month.parquet`. Con `scan_parquet` y una lista de rutas, Polars lee todo de una vez. **Registren la operación** en `audit.jsonl` con `append_audit`.

```python
# SU CÓDIGO — agregar TODAS las particiones (2022–2025) en un curated + append_audit
#   pista: pl.scan_parquet([...rutas...]) lee varias particiones a la vez

```

**Comprobar:**

```python
curated_files = list(CURATED_DIR.glob("geih_*.parquet"))
assert len(curated_files) >= 1, "No se escribió ningún agregado en curated/."
curated = pl.read_parquet(curated_files[0])
assert curated["anio"].n_unique() >= 2, "El curated debe cubrir varios años (2022–2025)."
assert AUDIT_PATH.is_file() and AUDIT_PATH.stat().st_size > 0, "La bitácora está vacía."
print("Paso 1.2, curated de todos los años: OK — años:", sorted(curated["anio"].unique().to_list()))
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

## Paso 1.4 — Orquestación con Prefect (ETL de todo el lakehouse)

Partan del flujo **`batch_flow_year`** de `l5-ingestion` (Parte 4) y **extiéndanlo** para que reciba **todas** las particiones 2022–2025 (no solo un año). Misma estructura: `@task` extract → `@task` aggregate+write → `@task` validate, unidos en un `@flow`. Si Prefect falla en Colab, documenten en markdown y dejen los pasos como funciones encadenadas.

```python
# SU CÓDIGO — @task extract / @task aggregate+write / @task validate, unidos en un @flow

```

**Comprobar:**

```python
audit_text = AUDIT_PATH.read_text(encoding="utf-8")
assert "prefect" in audit_text.lower() or "flow" in audit_text.lower()
print("Paso 1.4, orquestación ETL: OK — revisen audit.jsonl")
```

---

## Paso 1.5 — Actualizar el manifiesto (Ejercicio 1)

Amplíen `manifest.json` con metadatos de la ingesta. **Mínimo** (nombres sugeridos; pueden anidar bajo `ingesta` o `gobernanza`):

| Campo | Contenido |
|-------|-----------|
| Años cubiertos | p. ej. `[2022, 2023, 2024, 2025]` |
| `bitacora_lineas` | Número de líneas en `audit.jsonl` |
| `bitacora_muestra` | Una línea de ejemplo (JSON) del último evento |
| `contrato_columnas` | Lista de nombres de columna del `schema_contract.json` |
| `curated_filas` | Filas del agregado curated |
| Rutas en Drive | p. ej. `audit_path`, `schema_contract_path`, `curated_path` |

```python
# SU CÓDIGO — leer manifest, actualizar y volver a guardar

```

**Comprobar:**

```python
data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
flat = json.dumps(data, ensure_ascii=False).lower()
assert "bitacora" in flat or "audit" in flat, "Falta resumen de la bitácora en manifest.json"
assert "contrato" in flat or "schema" in flat, "Falta resumen del contrato en manifest.json"
assert "curated" in flat or "curada" in flat or "ingesta" in flat
assert AUDIT_PATH.is_file() and SCHEMA_PATH.is_file()
print("Paso 1.5, manifiesto (Ejercicio 1): OK")
print("Bitácora (líneas):", sum(1 for _ in AUDIT_PATH.open(encoding='utf-8')))
```

---

# Ejercicio 2 — Modelos y gráficos (Lección 6)

**Meta.** Convertir los agregados en **evidencia para una decisión**: un modelo evaluado con **entrenamiento/validación/prueba**, al menos dos gráficos rotulados por fuente y un **tablero** que los reúna. **Modelen solo sobre agregados**, nunca sobre microdatos.

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

## Paso 2.3 — Entrenar el modelo lineal (train/val/prueba)

Dividan en **entrenamiento, validación y prueba** (como en `l6-analytics`, Repaso y Parte 3). Entrenen una **regresión lineal**, evalúen en validación y reporten la **prueba** final. Expliquen en markdown si el resultado **apoya o no** la decisión.

**Importante (igual que en `l6-analytics`, Parte 3).** Para que el modelo tenga **señal real**, incluyan el **departamento como entrada one-hot** (`pd.get_dummies(dpto)`), además de `mes` (y `anio` si tienen varios años). Cada departamento tiene su propia escala; sin one-hot, el modelo solo predice el promedio y el R² queda cerca de 0 (o negativo).

Usen `LinearRegression` y lean sus **coeficientes**: son explicables ante quien decide.

```python
# SU CÓDIGO — one-hot de dpto (+mes/anio), split train/val/test, fit, predict, R²/MAE
#   pista: X_cat = pd.get_dummies(df["dpto"].astype(str), prefix="dpto")
#          X = pd.concat([df[["mes"]], X_cat], axis=1).astype(float)

```

Muestren en markdown qué **dicen los coeficientes** de los departamentos con mayor efecto.

**Comprobar:**

```python
assert any(name in dir() for name in ("model", "lin"))
print("Paso 2.3, modelo: OK — completen el markdown")
```

---

## Paso 2.4 — Gráfico 1: capa oficial GEIH

Hagan un gráfico (Plotly) sobre los agregados, con un **título que nombre la fuente** y un pie ligado a la pregunta de decisión. Guárdenlo en `outputs/`.

```python
# SU CÓDIGO — guardar la figura en chart1_path dentro de OUTPUTS_DIR

```

**Comprobar:**

```python
assert chart1_path.is_file()
print("Paso 2.4, gráfico 1: OK")
```

---

## Paso 2.5 — Gráfico 2: diagnóstico del modelo

Un segundo gráfico ligado al modelo: p. ej. **observado vs. predicho** o la tendencia del empleo por año.

```python
# SU CÓDIGO — guardar la figura en chart2_path

```

**Comprobar:**

```python
assert chart2_path.is_file()
print("Paso 2.5, gráfico 2: OK")
```

---

## Paso 2.6 — Tablero

Reúnan sus vistas en un solo **tablero** y guárdenlo en `outputs/` (`dashboard_path`). Tienen dos opciones (como en `l6-analytics`):

- **Sencillo:** `make_subplots` con los dos gráficos en una figura → `write_html`.
- **Enriquecido (opcional):** una rejilla `widgets.GridBox` con varias vistas (p. ej. el **mapa del indicador** y el **observado vs. predicho**). Para el mapa, descarguen las **referencias** (GeoJSON + OSM) como en `l6-analytics`, Parte 1; igual guarden al menos una figura en `dashboard_path`.

```python
# SU CÓDIGO — componer el tablero (make_subplots o GridBox) y guardar en dashboard_path

```

**Comprobar:**

```python
assert dashboard_path.is_file()
print("Paso 2.6, tablero: OK")
```

---

## Paso 2.7 — Manifiesto final

Añadan a `manifest.json`: tipo de modelo elegido, métricas de prueba y rutas de los gráficos y del tablero. **Conserven** los campos de gobernanza del Paso 1.5.

```python
# SU CÓDIGO — actualizar el manifiesto

```

**Comprobar:**

```python
data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
flat = json.dumps(data, ensure_ascii=False).lower()
assert any(k in flat for k in ("modelo", "analitica", "graficos", "tablero", "metric"))
assert "bitacora" in flat or "audit" in flat
assert "contrato" in flat or "schema" in flat
print("Paso 2.7, manifiesto final: OK")
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

Suban el ZIP **`week-3-group-<group_id>.zip`** hasta el **martes 23 de junio de 2026, 23:59 (Colombia)**. **Solo dos archivos** en la raíz del ZIP:

| Archivo | Descripción |
|---------|-------------|
| `week-3-group-<group_id>.ipynb` | Este cuaderno ejecutado (renómbrenlo al exportar) |
| `manifest.json` | Metadatos de ingesta **y** analítica: resumen de bitácora y contrato (Ejercicio 1) + modelo y gráficos (Ejercicio 2). Descarguen la copia actualizada desde Drive. |

`audit.jsonl` y `schema_contract.json` quedan en **Drive** (no en el ZIP). El cuaderno debe mostrar en las celdas **Comprobar** que existen y que el manifiesto los resume.

**Reflexión individual:** `week-3-reflection-<student>.pdf` el **miércoles 24 de junio de 2026** — plantilla en el [hub semana 3](/teaching/26-udenar-big-data/week-3-hub-es/).

**Proyecto:** avancen en la sesión del **sábado 20 jun** (bloque de analítica y gobernanza de capas de evidencia).

<!-- end NOTEBOOK: -->
