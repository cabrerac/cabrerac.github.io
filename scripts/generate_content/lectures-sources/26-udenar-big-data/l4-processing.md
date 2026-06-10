---
course_code: 26-udenar-big-data
title: Data processing and analysis
description: Lecture 4 — compute on stored Parquet; MapReduce mental model; DuckDB and Polars benchmarks; k-anonymity at query time. Individual run-only Colab; assessed code lives in week-2-group Part B.
session: 4
start_time: 07:00 am
end_time: 01:00 pm
hours: 5
author: Christian Cabrera Jojoa
email: chc79@cam.ac.uk
position: Senior Research Associate and Affiliated Lecturer
department: Department of Computer Science and Technology
institution: University of Cambridge
layout: lecture
lecture_code: l4-processing
lecture_date: 13/06/2026
permalink: /teaching/26-udenar-big-data/l4-processing/
visible: false
group_notebook: week-2-group
notebook_language: es
notebook_title: Procesamiento y análisis de datos
notebook_description: Práctica individual de la Lección 4. Misma consulta GEIH 2024 con MapReduce, pandas, DuckDB y Polars; benchmark y supresión k=5 al publicar agregados.
---

<!-- SLIDES: -->

# Last Time

<!-- end SLIDES: -->

*Diapositivas L4 — por redactar (puente desde L3: almacenamiento → consulta).*

<!-- RENDER: -->

### Resources

- [Individual notebook Lecture 4](https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-big-data/l4-processing.ipynb) *(when published)*
- [Individual notebook Lecture 3](https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-big-data/l3-storage.ipynb) — **prerrequisito:** Parquet 2024 en Drive
- [Group notebook week 2](https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-big-data/week-2-group.ipynb) *(when published)*
- [Week 2 hub](/work-space/teaching/big-data/course/week-2/week-2-hub-es.md) · [Session plan PDF](/assets/documents/26-udenar-big-data/week-2-session-plan-es.pdf)
- [GEIH spine specification](/work-space/teaching/big-data/planning/spine-spec.md)
- [Reflection template week 2](/assets/documents/26-udenar-big-data/reflection-week-2-template.docx)

### References

- Dean, J., & Ghemawat, S. (2008). MapReduce: Simplified data processing on large clusters. *Communications of the ACM*, 51(1), 107–113.
- Dwork, C. (2008). Differential privacy: A survey of results. *TAMC* (LNCS 4978).
- Armbrust, M., et al. (2021). *Lakehouse: A new generation of open platforms*. CIDR.

<!-- end RENDER: -->

<!-- NOTEBOOK: -->

## Repaso de Python para este cuaderno

Repasamos lo que usaremos en las Partes 1 a 6. **No** repetimos la solución de semana 1 ni la harmonización de L3 — asumimos que ya ejecutó [`l3-storage`](https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-big-data/l3-storage.ipynb) y tiene Parquet 2024 en Drive.

### `defaultdict` — agrupar en el *shuffle* de MapReduce

En MapReduce, después del **map** reunimos pares `(clave, valor)` por clave. **`defaultdict(list)`** crea listas vacías al acceder a una clave nueva.

```python
from collections import defaultdict

pares = [(52, 1.2), (11, 0.8), (52, 1.5), (11, 0.9)]
buckets: dict[int, list[float]] = defaultdict(list)
for dpto, peso in pares:
    buckets[dpto].append(peso)

assert len(buckets[52]) == 2
assert abs(sum(buckets[52]) - 2.7) < 1e-9
print("defaultdict shuffle: OK")
```

### Filtrar filas con máscara booleana

Para quedarnos solo con **ocupados**, filtramos con **`df.loc[df["is_employed"]]`** (o la columna que corresponda).

```python
import pandas as pd

mini = pd.DataFrame(
    {"dpto": [52, 52, 11], "is_employed": [True, False, True], "expansion_weight": [100.0, 50.0, 80.0]}
)
ocupados = mini.loc[mini["is_employed"]]
assert len(ocupados) == 2
assert ocupados["expansion_weight"].sum() == 180.0
print("filtro booleano: OK")
```

### Agregar con `groupby`

La misma pregunta analítica con pandas: **`groupby("dpto").agg(...)`**.

```python
agg = ocupados.groupby("dpto").agg(
    unweighted_count=("is_employed", "count"),
    weighted_sum=("expansion_weight", "sum"),
)
assert agg.loc[52, "weighted_sum"] == 100.0
print("groupby: OK")
```

### Rutas y archivos Parquet

En L3 escribimos particiones bajo `year=2024/mes=MM/`. **`Path.rglob("*.parquet")`** lista todos los archivos del árbol.

```python
from pathlib import Path

ejemplo = Path("data/processed/geih-spine/year=2024")
# En el cuaderno real: list(ejemplo.rglob("*.parquet"))
print("Path + rglob: listo para L4")
```

### Medir tiempo

Usamos **`time.perf_counter()`** para comparar motores en una tabla. También puede usar **`%%time`** al inicio de una celda (como en L3 Parte 4) para ver el tiempo impreso al final.

```python
import time

t0 = time.perf_counter()
_ = sum(range(1_000_000))
elapsed = time.perf_counter() - t0
assert elapsed >= 0
print(f"perf_counter ejemplo: {elapsed:.4f} s")
```

### Comprobar con `assert`

Las celdas **Comprobar** validan resultados. Si fallan, revise celdas anteriores.

```python
assert 2024 == 2024
print("Repaso Python L4: OK")
```

---

## Instrucciones

**Propósito.** En L3 **guardamos** GEIH 2024 en Parquet particionado. En L4 **consultamos** ese árbol con distintos motores y medimos cuál conviene en una sola máquina.

**Prerrequisito.** Ejecute **`l3-storage`** hasta la Parte 3 (Parquet `year=2024/` con 12 meses en Google Drive). Este cuaderno **no** descarga DANE ni harmoniza de nuevo.

**Pregunta analítica (2024 nacional).** Por departamento (`dpto`):

| Métrica | Definición |
|---------|------------|
| **Conteo sin ponderar** | Número de filas con `is_employed == True` |
| **Suma ponderada** | Σ `expansion_weight` sobre ocupados |

**Regla de ocupado (igual que L3):** `is_employed` es `True` cuando **`P6240 == 1`** en la harmonización del curso (ver [`l3-storage`](https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-big-data/l3-storage.ipynb)).

**Qué hace el cuaderno (en orden).**

| Parte | Tema |
|-------|------|
| **1** | Montar Drive y rutas al Parquet L3 |
| **2** | Enunciar la consulta y listar particiones 2024 |
| **3** | **MapReduce** desde cero (map → shuffle → reduce) + tiempo |
| **4** | **pandas** — misma consulta + comparación |
| **5** | **DuckDB** — SQL sobre archivos Parquet |
| **6** | **Polars** — scan lazy + collect |
| **7** | Tabla de tiempos e interpretación |
| **8** | **Gobernanza al consultar** — supresión **k = 5** |

**Entregas semana 2:** el código evaluable está en **`week-2-group`** (Parte B). Ver **Tareas** al final.

---

## Parte 1 — Configuración: Drive y rutas L3

Montamos la misma raíz que en L3. Si trabaja **en local** con el mismo layout de carpetas, ponga `USE_GOOGLE_DRIVE = False`.

```python
from pathlib import Path

USE_GOOGLE_DRIVE = True
YEAR = 2024

try:
    import google.colab  # noqa: F401
    IN_COLAB = True
except ImportError:
    IN_COLAB = False

if USE_GOOGLE_DRIVE and IN_COLAB:
    from google.colab import drive

    drive.mount("/content/drive")
    WORK_ROOT = Path("/content/drive/MyDrive/UDENAR-BigData")
    print(f"Raíz en Drive: {WORK_ROOT}")
else:
    WORK_ROOT = Path(".")
    print(f"Raíz local: {WORK_ROOT.resolve()}")

PROCESSED_DIR = WORK_ROOT / "data" / "processed" / "geih-spine"
PARQUET_2024 = PROCESSED_DIR / f"year={YEAR}"
OUTPUTS_DIR = WORK_ROOT / "outputs"
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

print("Parquet 2024:", PARQUET_2024)
```

Instale motores adicionales (DuckDB y Polars):

```python
%pip install -q duckdb polars pyarrow
```

**Comprobar:**

```python
assert WORK_ROOT.is_dir()
assert PARQUET_2024.is_dir(), (
    f"No encuentro {PARQUET_2024}. Ejecute l3-storage Partes 1–3 primero."
)
part_files = sorted(PARQUET_2024.rglob("*.parquet"))
assert len(part_files) >= 12, (
    f"Se esperan ≥12 particiones 2024; hay {len(part_files)}. Complete l3-storage."
)
print(f"Particiones encontradas: {len(part_files)}")
print("Parte 1 — configuración: OK")
```

---

## Parte 2 — Pregunta analítica y particiones

Fijamos constantes compartidas por todos los motores.

```python
import json
import time
from collections import defaultdict

import duckdb
import pandas as pd
import polars as pl

EMPLOYED_RULE = "is_employed == True (P6240 ∈ {1} en harmonización L3)"
K_MIN = 5  # regla del curso para publicar agregados departamentales

QUERY_DESC = (
    "Por departamento (dpto): conteo sin ponderar de ocupados y "
    "suma de expansion_weight sobre ocupados — GEIH 2024 nacional."
)

part_files = sorted(PARQUET_2024.rglob("*.parquet"))
print(QUERY_DESC)
print(f"Regla ocupado: {EMPLOYED_RULE}")
print(f"Archivos Parquet: {len(part_files)}")
print("Ejemplo:", part_files[0].relative_to(WORK_ROOT))
```

**Comprobar:**

```python
assert K_MIN == 5
assert all(p.suffix == ".parquet" for p in part_files)
print("Parte 2 — consulta definida: OK")
```

---

## Parte 3 — MapReduce desde cero

**Idea.** Descomponemos la consulta en tres fases explícitas (como en Hadoop, pero en una sola máquina):

1. **Map:** por cada partición, emitir `(dpto, expansion_weight)` solo para ocupados.
2. **Shuffle:** agrupar todos los pesos por `dpto` (`defaultdict`).
3. **Reduce:** por cada `dpto`, contar filas y sumar pesos.

### Paso 3.1 — Funciones map, shuffle, reduce

```python
def map_partition(path: Path) -> list[tuple[int, float]]:
    """Lee una partición; devuelve pares (dpto, expansion_weight) de ocupados."""
    df = pd.read_parquet(path, columns=["dpto", "is_employed", "expansion_weight"])
    emp = df.loc[df["is_employed"], ["dpto", "expansion_weight"]]
    return list(zip(emp["dpto"].astype(int), emp["expansion_weight"].astype(float)))


def shuffle(pairs: list[tuple[int, float]]) -> dict[int, list[float]]:
    """Reúne valores por clave dpto."""
    buckets: dict[int, list[float]] = defaultdict(list)
    for dpto, weight in pairs:
        buckets[dpto].append(weight)
    return buckets


def reduce_buckets(buckets: dict[int, list[float]]) -> pd.DataFrame:
    """Agrega conteo sin ponderar y suma ponderada por departamento."""
    rows = [
        {"dpto": dpto, "unweighted_count": len(weights), "weighted_sum": sum(weights)}
        for dpto, weights in buckets.items()
    ]
    return pd.DataFrame(rows).sort_values("dpto").reset_index(drop=True)


print("Funciones MapReduce: definidas")
```

### Paso 3.2 — Ejecutar sobre todo 2024 y medir tiempo

```python
t0 = time.perf_counter()
all_pairs: list[tuple[int, float]] = []
for path in part_files:
    all_pairs.extend(map_partition(path))
buckets = shuffle(all_pairs)
mr_result = reduce_buckets(buckets)
mr_seconds = round(time.perf_counter() - t0, 3)

print(f"MapReduce — departamentos: {len(mr_result)}")
print(f"MapReduce — tiempo: {mr_seconds} s")
print(mr_result.head())
```

**Comprobar:**

```python
assert len(mr_result) >= 30, f"Pocos departamentos: {len(mr_result)}"
assert mr_result["weighted_sum"].sum() > 1_000_000
assert mr_result["unweighted_count"].sum() > 10_000
print("Parte 3 — MapReduce: OK")
```

---

## Parte 4 — pandas: misma consulta

Cargamos **todo el árbol 2024** en memoria y usamos **`groupby`** — el “reduce optimizado” que ya conoce.

```python
t0 = time.perf_counter()
df_2024 = pd.read_parquet(PARQUET_2024)
employed = df_2024.loc[df_2024["is_employed"]]
pandas_result = (
    employed.groupby("dpto", as_index=False)
    .agg(unweighted_count=("is_employed", "count"), weighted_sum=("expansion_weight", "sum"))
    .sort_values("dpto")
    .reset_index(drop=True)
)
pandas_seconds = round(time.perf_counter() - t0, 3)
del df_2024, employed

print(f"pandas — departamentos: {len(pandas_result)}")
print(f"pandas — tiempo: {pandas_seconds} s")
```

Opcional: ver el tiempo con **`%%time`** (como en L3):

```python
%%time
_ = pd.read_parquet(PARQUET_2024, columns=["dpto", "is_employed", "expansion_weight"])
```

**Comprobar:**

```python
merged = mr_result.merge(pandas_result, on="dpto", suffixes=("_mr", "_pd"))
assert (merged["weighted_sum_mr"] - merged["weighted_sum_pd"]).abs().max() < 1.0
print("Parte 4 — pandas coincide con MapReduce: OK")
```

---

## Parte 5 — DuckDB: SQL sobre Parquet

DuckDB lee el árbol **sin** cargar todo en un DataFrame de pandas primero.

```python
parquet_glob = str(PARQUET_2024 / "**" / "*.parquet")

t0 = time.perf_counter()
con = duckdb.connect()
duckdb_result = con.execute(
    f"""
    SELECT
        dpto,
        COUNT(*)::BIGINT AS unweighted_count,
        SUM(expansion_weight) AS weighted_sum
    FROM read_parquet('{parquet_glob.replace(chr(92), "/")}', hive_partitioning=false)
    WHERE is_employed = true
    GROUP BY dpto
    ORDER BY dpto
    """
).df()
duckdb_seconds = round(time.perf_counter() - t0, 3)
con.close()

print(f"DuckDB — departamentos: {len(duckdb_result)}")
print(f"DuckDB — tiempo: {duckdb_seconds} s")
```

**Comprobar:**

```python
cmp = mr_result.merge(duckdb_result, on="dpto", suffixes=("_mr", "_dk"))
assert (cmp["weighted_sum_mr"] - cmp["weighted_sum_dk"]).abs().max() < 1.0
print("Parte 5 — DuckDB: OK")
```

---

## Parte 6 — Polars: scan lazy

**Polars** aplaza el trabajo hasta **`collect()`** — útil cuando el dataset crece (como en **`week-2-group`** 2022–2025).

```python
t0 = time.perf_counter()
polars_result = (
    pl.scan_parquet(str(PARQUET_2024 / "**" / "*.parquet"))
    .filter(pl.col("is_employed"))
    .group_by("dpto")
    .agg(
        pl.len().alias("unweighted_count"),
        pl.col("expansion_weight").sum().alias("weighted_sum"),
    )
    .sort("dpto")
    .collect()
    .to_pandas()
)
polars_seconds = round(time.perf_counter() - t0, 3)

print(f"Polars — departamentos: {len(polars_result)}")
print(f"Polars — tiempo: {polars_seconds} s")
```

**Comprobar:**

```python
cmp = mr_result.merge(polars_result, on="dpto", suffixes=("_mr", "_pl"))
assert (cmp["weighted_sum_mr"] - cmp["weighted_sum_pl"]).abs().max() < 1.0
print("Parte 6 — Polars: OK")
```

---

## Parte 7 — Tabla de tiempos e interpretación

```python
timing_df = pd.DataFrame(
    [
        {"motor": "MapReduce (desde cero)", "segundos": mr_seconds},
        {"motor": "pandas (groupby)", "segundos": pandas_seconds},
        {"motor": "DuckDB (SQL)", "segundos": duckdb_seconds},
        {"motor": "Polars (lazy)", "segundos": polars_seconds},
    ]
).sort_values("segundos")

print("Comparación de motores — GEIH 2024 completo:")
print(timing_df.to_string(index=False))
print(
    "\nInterpretación: MapReduce enseña el patrón; pandas/DuckDB/Polars implementan "
    "el mismo reduce de forma optimizada. En L3 vimos poda por partición; aquí "
    "leemos todo 2024 para comparar motores en igualdad de condiciones."
)
```

**Comprobar:**

```python
assert len(timing_df) == 4
assert timing_df["segundos"].min() > 0
print("Parte 7 — benchmark: OK")
```

---

## Parte 8 — Gobernanza al consultar (k = 5)

En L3 documentamos qué **guardamos**. Al **publicar** agregados, suprimimos celdas con **menos de k = 5 ocupados sin ponderar**; si no se suprime, reportamos la **suma ponderada**.

```python
def apply_k_suppression(agg: pd.DataFrame, k: int = K_MIN) -> pd.DataFrame:
    """Marca celdas suprimidas; weighted_sum solo si unweighted_count >= k."""
    out = agg.copy()
    out["suppressed"] = out["unweighted_count"] < k
    out["weighted_sum_public"] = out["weighted_sum"].where(~out["suppressed"])
    return out


pub_mr = apply_k_suppression(mr_result)
n_suppressed = int(pub_mr["suppressed"].sum())
n_published = int((~pub_mr["suppressed"]).sum())

print(f"Departamentos totales: {len(pub_mr)}")
print(f"Suprimidos (conteo < {K_MIN}): {n_suppressed}")
print(f"Publicables (conteo ≥ {K_MIN}): {n_published}")
print("\nVista publicable (primeras filas):")
print(
    pub_mr[["dpto", "unweighted_count", "weighted_sum_public", "suppressed"]]
    .head(10)
    .to_string(index=False)
)

pub_path = OUTPUTS_DIR / "agg_employed_by_dpto_2024_k5.csv"
pub_mr.to_csv(pub_path, index=False)
print(f"\nGuardado (uso interno del curso, no Moodle): {pub_path}")
```

**No publicar** este CSV en Moodle ni en redes — es demo de gobernanza; el ZIP grupal lleva solo conteos en `manifest.json`.

**Comprobar:**

```python
assert pub_mr.loc[pub_mr["suppressed"], "weighted_sum_public"].isna().all()
assert pub_mr.loc[~pub_mr["suppressed"], "weighted_sum_public"].notna().all()
assert pub_path.is_file()
print("Parte 8 — gobernanza k=5: OK")
```

---

## Puente al cuaderno grupal

En **`week-2-group` Parte B** su grupo:

1. Reimplementa **MapReduce desde cero** sobre el spine **2022–2025** (misma consulta).
2. Repite la consulta con **DuckDB o Polars** y documenta la **elección de motor**.
3. Aplica **k = 5** al agregado multi-año y actualiza **`manifest.json`** (conteos, no Parquet en el ZIP).

Entrega Moodle **martes 16 jun 2026**: ZIP con cuaderno ejecutado + `manifest.json` (sin archivos de datos).

---

## Tareas

Plantillas y plazos en el [hub semana 2](/work-space/teaching/big-data/course/week-2/week-2-hub-es.md).

### Cuaderno individual (este archivo)

Ejecute **Partes 1–8** antes del sábado 13 jun. **Prerrequisito:** Parquet 2024 de **`l3-storage`**. No hay entrega separada de este cuaderno.

### Trabajo en grupo (semana 2)

Colab **`week-2-group`** Parte B. ZIP **`week-2-group-<group_id>.zip`** hasta el **martes 16 de junio de 2026, 23:59 (Colombia)**:

| Archivo en el ZIP | Descripción |
|-------------------|-------------|
| `week-2-group-<group_id>.ipynb` | Cuaderno grupal ejecutado |
| `manifest.json` | Conteos y metadatos (sin CSV ni Parquet) |

### Reflexión individual

PDF **`week-2-reflection-<student>.pdf`** hasta el **miércoles 17 de junio de 2026**. Plantilla: [reflection-week-2-template.docx](/assets/documents/26-udenar-big-data/reflection-week-2-template.docx).

### Requerimientos del proyecto

Avance en Word durante el **sábado 13 jun** (checkpoint: **§5 subconjunto GEIH definido**). El PDF **`project_requirements.pdf`** se entrega con el **proyecto summativo (27 jun 2026)**.

<!-- end NOTEBOOK: -->
