---
course_code: 26-udenar-big-data
title: Semana 2 — Lakehouse GEIH y procesamiento (grupo)
description: Group Colab — harmonize and partition GEIH 2022–2025, MapReduce plus one engine benchmark, publish aggregates with k=5 suppression or Laplace noise (student choice with justification). Consolidates L3 + L4 homework.
session: 2
start_time: async
end_time: async
hours: 4
author: Christian Cabrera Jojoa
email: chc79@cam.ac.uk
position: Assistant Research Professor
department: Department of Computer Science and Technology
institution: University of Cambridge
layout: lecture
lecture_code: week-2-group
lecture_date: 13/06/2026
visible: false
skip_slides: true
skip_lecture_page: true
notebook_language: es
notebook_title: Semana 2 — lakehouse GEIH y procesamiento (grupo)
notebook_description: Cuaderno canónico del grupo para la semana 2 (L3 + L4). Harmoniza 2022–2025 en Parquet, consulta con MapReduce y un motor moderno, publica agregados con k=5 o privacidad diferencial (justificado). Entrega en **Tarea grupal**.
---

<!-- NOTEBOOK: -->

## Instrucciones

**Propósito.** Cuaderno grupal para la semana 2 (Lecciones 3 y 4). Aquí está **todo el código evaluable** de la semana: construir el **lakehouse GEIH completo (2022–2025)**, consultarlo con **MapReduce** y **un motor moderno**, y **publicar agregados** con gobernanza.

**Requisito.** Ejecute primero los cuadernos individuales **`l3-storage`** y **`l4-processing`** (run-only). Aquí **adaptan** y **escriben** código — no copie sin entender. Desarrolle el cuaderno en grupo (bloque de 2 h el **sábado 13 jun**).

**Datos de entrada.** CSV crudos **2022–2025** de **`week-1-group`** (o la misma copia en Google Drive). Catálogos DANE: 2022 → `771`, 2023 → `782`, 2024 → `819`, 2025 → `853`.

**Materiales:** [L3 Almacenamiento](https://cabrerac.github.io/teaching/26-udenar-big-data/l3-storage/) · [L4 Procesamiento](https://cabrerac.github.io/teaching/26-udenar-big-data/l4-processing/).

**Pregunta analítica (igual que L4).** Por departamento (`dpto`): **conteo sin ponderar** de ocupados y **suma ponderada** (Σ `factor_expansion`). Regla de ocupado: `actividad == 1` (derivar `ocupado` antes de agregar).

**Entrega Moodle (martes 16 jun 2026, 23:59 Colombia):** ZIP `week-2-group-<group_id>.zip` con `week-2-group-<group_id>.ipynb` (renombre este cuaderno al exportar) y `manifest.json` en la **raíz del ZIP**. **Sin** archivos Parquet ni CSV en el ZIP.

**Mapa del cuaderno (tres ejercicios)**

| Ejercicio | Tema | Entregable clave |
|-----------|------|------------------|
| **1** | Lakehouse 2022–2025 | Parquet particionado en Drive + benchmark layout + retención/linaje |
| **2** | MapReduce + **un** motor (DuckDB **o** Polars) | Tabla de tiempos + markdown de elección de motor |
| **3** | Publicar con gobernanza | Agregado por `dpto` + **k = 5** **o** Laplace (justificado) + `manifest.json` |

Use `SKIP_IF_PARQUET_EXISTS` si ya tiene los datos en Drive. El ejercicio 2 sobre el árbol completo es pesado, explore y empiece con un subconjunto si el Colab se queda sin memoria y documente la limitación en markdown.

---

## Configuración — Drive y rutas

Monte **Google Drive** igual que en [`l3-storage`](https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-big-data/l3-storage.ipynb) (Parte 1). Si trabaja en **local** con el mismo layout, ponga `USE_GOOGLE_DRIVE = False`.

Copie constantes y ayudantes de harmonización del cuaderno individual L3 (Parte 2):

| Qué copiar | Dónde está en L3 |
|------------|------------------|
| `CSV_SEP`, `CSV_ENCODING`, `PERSON_KEYS`, `PRIMARY_TABLE_KEYWORD`, `DEMOG_TABLE_KEYWORDS` | Parte 0 / Parte 2 |
| `_labour_csv`, `_demog_csv`, `a_entero`, `harmonize_month` | Parte 2 |
| `read_geih_csv` (delimitador `;` o `,`) | Parte 0 / Parte 2 |
| `count_month_folders` | Parte 0 / Parte 1 |

Defina también:

```python
SPINE_YEARS = [2022, 2023, 2024, 2025]
# Motor moderno para el ejercicio 2: "duckdb" o "polars" (elija UNO)
ENGINE = "duckdb"  # cambie a "polars" si su grupo prefiere Polars
# Estrategia de privacidad para el ejercicio 3: "k_suppression" o "laplace"
PRIVACY_STRATEGY = "k_suppression"  # o "laplace"
```

```python
# SU CÓDIGO — montar Drive, WORK_ROOT, RAW_DIR, PROCESSED_DIR, MANIFEST_PATH, OUTPUTS_DIR
# + constantes y funciones copiadas de l3-storage

```

**Comprobar:**

```python
assert WORK_ROOT.is_dir()
assert RAW_DIR.is_dir()
assert PROCESSED_DIR.is_dir()
assert ENGINE in ("duckdb", "polars")
assert PRIVACY_STRATEGY in ("k_suppression", "laplace")
print("Configuración: OK")
```

---

# Ejercicio 1 — Construir el lakehouse (2022–2025)

**Tarea.** Harmonizar **todos los meses** de **2022, 2023, 2024 y 2025** y cargar el lakehouse `data/processed/geih-spine/` como Parquet particionado (`anio=…/mes=…/part-000.parquet`). Repita el benchmark de L3: leer **árbol completo** vs **una partición**.

## Paso 1.1 — Confirmar datos crudos

Verifique que cada año tiene **12 carpetas mensuales** con CSV bajo `data/raw/<año>/`. Si falta algo, verifique la descarga del dataset en cuadernos previos.

```python
# SU CÓDIGO — contar meses por año e imprimir resumen

```

**Comprobar:**

```python
meses_por_anio = {y: count_month_folders(RAW_DIR / str(y)) for y in SPINE_YEARS}
print("Meses por año:", meses_por_anio)
assert all(meses_por_anio[y] >= 12 for y in SPINE_YEARS), meses_por_anio
print("Paso 1.1, datos crudos: OK")
```

---

## Paso 1.2 — Harmonizar y escribir particiones

Recorra **cada año** y **cada carpeta mensual**, aplique `harmonize_month` y escriba Parquet. Use `SKIP_IF_PARQUET_EXISTS = True` para no reescribir particiones ya cargadas.

**Pista:** el bucle de L3 Parte 3 escribe un año. En este caso extiéndalo a cuatro años y acumule `partition_stats`.

```python
# SU CÓDIGO

```

**Comprobar:**

```python
assert len(partition_stats) >= 48, f"Se esperan ~48 particiones (12×4). Hay {len(partition_stats)}"
total_filas = sum(s["filas"] for s in partition_stats)
assert total_filas > 500_000
assert (PROCESSED_DIR / "anio=2024" / "mes=01" / "part-000.parquet").is_file()
print(f"Particiones: {len(partition_stats)} | Filas totales: {total_filas:,}")
print("Paso 1.2, lakehouse escrito: OK")
```

---

## Paso 1.3 — Benchmark: árbol completo vs una partición

Compare tiempo (y memoria si es posible) de:

1. `pd.read_parquet(PROCESSED_DIR)` — **todo el spine**
2. `pd.read_parquet(PROCESSED_DIR / "anio=2024" / "mes=01")` — **una partición**

Guarde números en variables `bench_full_seconds`, `bench_one_seconds` (y memoria si las calcula).

```python
# SU CÓDIGO

```

**Comprobar:**

```python
assert bench_full_seconds > 0 and bench_one_seconds > 0
assert bench_one_seconds < bench_full_seconds, "Una partición debería leer más rápido que el árbol completo"
print(f"Completo: {bench_full_seconds:.2f}s | Una partición: {bench_one_seconds:.2f}s")
print("Paso 1.3, benchmark layout: OK")
```

---

## Paso 1.4 — Markdown: partición, retención y linaje

En una celda markdown (mínimo **120 palabras**, español):

1. **Por qué** particionamos por `anio` y `mes` (y qué consultas benefician).
2. **Retención:** cuánto tiempo conservarán microdatos en Drive y quién accede.
3. **Linaje:** de CSV DANE → lakehouse (cite rutas y `manifest.json`).

Vincule con su **`project_requirements.pdf`** §6–§7 cuando aplique.

```markdown
# SU TEXTO (markdown)
```

---

# Ejercicio 2 — MapReduce + un motor sobre el spine completo

**Tarea.** Sobre el lakehouse **2022–2025**, implemente la consulta de ocupados por `dpto` con:

1. **MapReduce desde cero** (map → shuffle → reduce), con **benchmark**.
2. **Un motor moderno:** DuckDB **o** Polars (el que eligió en `ENGINE`), misma consulta, **benchmark**.

No hace falta repetir pandas si ya lo vieron en L4; puede citar tiempos del cuaderno individual en el markdown.

## Paso 2.1 — MapReduce desde cero

Copie la **idea** de L4 Parte 3 (`map_partition`, `shuffle`, `reduce_buckets`) pero:

- Liste **todos** los `.parquet` bajo `PROCESSED_DIR` (48+ archivos).
- Emita `(dpto, factor_expansion)` solo para `actividad == 1`.
- Guarde resultado en `mr_result` y tiempo en `mr_seconds`.

```python
# SU CÓDIGO

```

**Comprobar:**

```python
assert len(mr_result) >= 30
assert mr_result["suma_ponderada"].sum() > 1_000_000
assert mr_seconds > 0
print(f"MapReduce: {len(mr_result)} dptos | {mr_seconds:.3f}s")
print("Paso 2.1, MapReduce: OK")
```

---

## Paso 2.2 — Motor elegido (DuckDB o Polars)

Implemente la **misma consulta** con el motor indicado en `ENGINE`.

| Motor | Referencia en L4 |
|-------|------------------|
| `duckdb` | Parte 5 — `read_parquet` + SQL `GROUP BY dpto` |
| `polars` | Parte 6 — `scan_parquet` lazy + `group_by` |

Guarde resultado en `engine_result` y tiempo en `engine_seconds`.

```python
# SU CÓDIGO — ramifique según ENGINE == "duckdb" o "polars"

```

**Comprobar:**

```python
cmp = mr_result.merge(engine_result, on="dpto", suffixes=("_mr", "_eng"))
max_diff = (cmp["suma_ponderada_mr"] - cmp["suma_ponderada_eng"]).abs().max()
assert max_diff < 1.0, f"MR y {ENGINE} difieren demasiado: {max_diff}"
assert engine_seconds > 0
print(f"{ENGINE}: {engine_seconds:.3f}s | diff max vs MR: {max_diff:.4f}")
print("Paso 2.2, motor moderno: OK")
```

---

## Paso 2.3 — Tabla de tiempos y elección de motor

Arme `timing_df` con al menos MapReduce y su motor. En markdown (**≥ 80 palabras**): por qué eligió DuckDB **o** Polars; trade-offs vs MapReduce y vs el otro motor; cite **sus** tiempos.

```python
# SU CÓDIGO — timing_df + opcional gráfico en outputs/

```

```markdown
# SU TEXTO — justificación del motor (markdown)
```

**Comprobar:**

```python
assert len(timing_df) >= 2
assert timing_df["segundos"].min() > 0
print("Paso 2.3, benchmark motores: OK")
```

---

# Ejercicio 3 — Publicar con gobernanza (k = 5 o Laplace)

**Tarea.** Construya el agregado departamental (`dpto`, `conteo_ocupados`, `suma_ponderada`) sobre el spine completo. **Elija UNA estrategia** (`PRIVACY_STRATEGY`):

| Estrategia | Qué implementar | Referencia |
|------------|-----------------|------------|
| `k_suppression` | Suprimir celdas con conteo &lt; 5; publicar suma ponderada solo si no suprimida | L4 Parte 8.2 |
| `laplace` | Ruido de Laplace en conteos (defina `epsilon` y sensibilidad) | L3 Parte 5.2 / L4 Parte 8.3 |

En markdown (**≥ 100 palabras**): **justifique** por qué su grupo eligió k-anonimato/supresión **o** privacidad diferencial para **este** agregado y su proyecto (Dwork, Zuboff cap. 3, §6–§7 del PDF de requerimientos).

## Paso 3.1 — Agregado departamental

Guarde la tabla en Drive, p. ej. `outputs/agg_ocupados_dpto_spine.csv` (ruta documentada en el cuaderno).

```python
# SU CÓDIGO — dept_agg desde mr_result o recomputando; guardar CSV

```

**Comprobar:**

```python
assert len(dept_agg) >= 30
assert {"dpto", "conteo_ocupados", "suma_ponderada"}.issubset(dept_agg.columns)
assert agg_path.is_file()
print("Paso 3.1, agregado departamental: OK")
```

---

## Paso 3.2 — Aplicar la estrategia elegida

```python
# SU CÓDIGO — k_suppression O laplace según PRIVACY_STRATEGY
# Guarde pub_table (tabla publicable) y métricas (n_suprimidas, epsilon, etc.)

```

**Comprobar:**

```python
if PRIVACY_STRATEGY == "k_suppression":
    assert "suprimido" in pub_table.columns or "suma_publica" in pub_table.columns
    n_priv = int(pub_table.get("suprimido", pub_table["conteo_ocupados"] < 5).sum())
    print(f"k=5: celdas suprimidas o pequeñas: {n_priv}")
elif PRIVACY_STRATEGY == "laplace":
    assert "conteo_publica" in pub_table.columns or "conteo_dp" in pub_table.columns
    assert EPSILON > 0
    print(f"Laplace ε={EPSILON}")
assert pub_path.is_file()
print("Paso 3.2, privacidad: OK")
```

---

## Paso 3.3 — Justificación (markdown)

```markdown
# SU TEXTO — por qué k=5 o Laplace para su grupo y proyecto
```

---

## Paso 3.4 — Actualizar `manifest.json`

Amplíe el manifiesto de week 1 con metadatos del lakehouse y la publicación (sin subir Parquet en el ZIP). Mínimo:

- `filas_por_anio` (dict año → filas)
- `benchmark_layout` (tiempos ejercicio 1)
- `benchmark_motores` (MR + motor elegido)
- `privacidad` (estrategia, k o epsilon, conteos suprimidos / ruido)
- `lakehouse_path` (ruta en Drive)

```python
# SU CÓDIGO — leer manifest existente, actualizar, write_manifest o json.dump

```

**Comprobar:**

```python
assert MANIFEST_PATH.is_file()
data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
assert "filas_por_anio" in data or "lakehouse" in data
assert "privacidad" in data
print("Paso 3.4, manifest.json: OK")
```

---

## Registro de contribución (grupo)

Cada integrante añade **una línea** con tarea concreta. Indique el **escriba de semana 2** (consolidación del ZIP).

```python
contribution_log = """
- ...
Escriba semana 2: ...
"""
print(contribution_log)
```

---

## Tarea grupal (Moodle)

ZIP **`week-2-group-<group_id>.zip`** hasta el **martes 16 de junio de 2026, 23:59 (Colombia)**:

| Archivo | Descripción |
|---------|-------------|
| `week-2-group-<group_id>.ipynb` | Este cuaderno ejecutado (plantilla Colab: `week-2-group`) |
| `manifest.json` | Metadatos actualizados (raíz del ZIP) |

**Reflexión individual:** `week-2-reflection-<student>.pdf` el **miércoles 17 de junio de 2026** — plantilla [`reflection-week-2-template.docx`](/assets/documents/26-udenar-big-data/reflection-week-2-template.docx).

**Requerimientos del proyecto:** avance en la sesión del **sábado 13 jun** (bloque 11:30–12:45 — **arquitectura de datos**: años, departamentos, variables + vínculo con ética en Word). PDF con el **proyecto summativo (27 jun)**.

<!-- end NOTEBOOK: -->
