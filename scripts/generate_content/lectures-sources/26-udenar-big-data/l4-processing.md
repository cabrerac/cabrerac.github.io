---
course_code: 26-udenar-big-data
title: Data processing and analysis
description: Lecture 4 turns stored Parquet into answers. After the layout benchmark in Lecture 3, we need engines that scale on one machine—MapReduce as the mental model, then pandas, DuckDB, and Polars on the same weighted-employment-by-department query over 2024. The individual run-only notebook contrasts k=5 suppression with Laplace noise on finer aggregates. Assessed processing, engine choice, privacy strategy, and manifest updates for the full 2022–2025 spine are in week-2-group.
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
notebook_description: Práctica individual de la Lección 4. Misma consulta GEIH 2024 con MapReduce, pandas, DuckDB y Polars. Benchmark y gobernanza al publicar agregados finos (supresión k=5 vs privacidad diferencial).
---

<!-- SLIDES: -->

# Last Time

<!-- end SLIDES: -->

{% include _snippets/26-udenar-big-data/l4-processing/last-time.md %}

<!-- SLIDES: -->

# The Need to Process

<!-- end SLIDES: -->

{% include _snippets/26-udenar-big-data/l4-processing/processing-need.md %}

<!-- SLIDES: -->

# Big Data Processing

<!-- end SLIDES: -->

{% include _snippets/26-udenar-big-data/l4-processing/big-data-processing.md %}

<!-- SLIDES: -->

# Governance at Query Time

<!-- end SLIDES: -->

{% include _snippets/26-udenar-big-data/l4-processing/governance.md %}

<!-- SLIDES: -->

# Conclusions

<!-- end SLIDES: -->

{% include _snippets/26-udenar-big-data/l4-processing/conclusions.md %}

{% include _snippets/26-udenar-big-data/l4-processing/practical-slides.md %}

<!-- RENDER: -->

### Resources

- [Individual notebook Lecture 4](https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-big-data/l4-processing.ipynb) *(when published)*
- [Individual notebook Lecture 3](https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-big-data/l3-storage.ipynb), **prerrequisito:** Parquet 2024 en Drive
- [Group notebook week 2](https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-big-data/week-2-group.ipynb) *(when published)*
- [Week 2 hub](/work-space/teaching/big-data/course/week-2/week-2-hub-es.md) · [Session plan PDF](/assets/documents/26-udenar-big-data/week-2-session-plan-es.pdf)
- [Reflection template week 2](/assets/documents/26-udenar-big-data/reflection-week-2-template.docx)

### References

- Dean, J., & Ghemawat, S. (2008). MapReduce: Simplified data processing on large clusters. *Communications of the ACM*, 51(1), 107–113.
- Dwork, C. (2008). Differential privacy: A survey of results. *TAMC* (LNCS 4978).
- Armbrust, M., et al. (2021). *Lakehouse: A new generation of open platforms*. CIDR.

<!-- end RENDER: -->

<!-- NOTEBOOK: -->

## Repaso de Python para este cuaderno

Repasamos lo que usaremos en las Partes 1 a 8. Asumimos que ya ejecutó el cuaderno [`l3-storage`](https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-big-data/l3-storage.ipynb) y tiene Parquet 2024 en Drive o en su directorio local.

### `defaultdict`, agrupar en el *shuffle* de MapReduce

En MapReduce, después del **map** reunimos pares `(clave, valor)` por clave. **`defaultdict(list)`** crea listas vacías al acceder a una clave nueva.

Definimos los pares de ejemplo, `(departamento, peso de expansión)`:

```python
from collections import defaultdict

pares = [(52, 1.2), (11, 0.8), (52, 1.5), (11, 0.9)]
print("Pares (dpto, peso):", pares)
```

Después agrupamos por departamento (fase **shuffle**):

```python
buckets: dict[int, list[float]] = defaultdict(list)
for dpto, peso in pares:
    buckets[dpto].append(peso)

print("Buckets por dpto:", dict(buckets))
print("Dpto 52, pesos:", buckets[52])
assert len(buckets[52]) == 2
assert abs(sum(buckets[52]) - 2.7) < 1e-9
print("defaultdict shuffle: OK")
```

### Derivar una columna y filtrar con máscara booleana

El Parquet de la lección 3 guarda `actividad` (el código `P6240` del DANE), **sin interpretar**. Aquí **derivamos** la columna que nos interesa: `ocupado` es `True` cuando `actividad == 1`. Esto es **procesamiento**, decidir qué cuenta como ocupado.

```python
import pandas as pd

mini = pd.DataFrame(
    {"dpto": [52, 52, 11], "actividad": [1, 2, 1], "factor_expansion": [100.0, 50.0, 80.0]}
)
# Sí mini["actividad"] is equal to 1, mini["ocupado"] = True
mini["ocupado"] = mini["actividad"] == 1
print("Tabla con la columna derivada:")
print(mini)
```

Con la columna lista, filtramos con la máscara booleana y revisamos el subconjunto:

```python
ocupados = mini.loc[mini["ocupado"]]
print("Solo ocupados:")
print(ocupados)
print("Suma de pesos:", ocupados["factor_expansion"].sum())
assert len(ocupados) == 2
assert ocupados["factor_expansion"].sum() == 180.0
print("filtro booleano: OK")
```

### Agregar con `groupby`

La misma pregunta analítica con pandas: **`groupby("dpto").agg(...)`**.

```python
agg = ocupados.groupby("dpto").agg(
    conteo_ocupados=("ocupado", "count"),
    suma_ponderada=("factor_expansion", "sum"),
)
print("Agregado por departamento:")
print(agg)
assert agg.loc[52, "suma_ponderada"] == 100.0
print("groupby: OK")
```

---

## Instrucciones

**Propósito.** En la **Lección 3** guardamos GEIH 2024 en Parquet particionado. En esta **Lección 4** consultamos ese árbol con distintos motores y medimos su desempeño.

**Prerrequisito.** Ejecute el cuaderno de la **lección 3** (`l3-storage`) hasta la Parte 3 (Parquet `anio=2024/` con 12 meses en Google Drive). Este cuaderno **no** descarga DANE ni harmoniza de nuevo.

**Pregunta analítica (2024 nacional).** Por departamento (`dpto`):

| Métrica | Definición |
|---------|------------|
| **Conteo sin ponderar** | Número de personas ocupadas (filas con `ocupado == True`) |
| **Suma ponderada** | Σ `factor_expansion` sobre ocupados |

**¿Qué es `factor_expansion`?** La GEIH es una **muestra**: no encuesta a todo el país. Cada persona trae un **factor de expansión** (`FEX_C18` en el DANE) que indica **a cuántas personas de la población representa**. Por eso, para estimar un total poblacional no contamos filas, sino que **sumamos el factor de expansión** (la "suma ponderada").

**Regla de ocupado.** La lección 3 guardó `actividad` (código `P6240` del DANE) **sin interpretar**. En esta lección **derivamos** `ocupado = (actividad == 1)` antes de agregar.

**Qué hace el cuaderno (en orden).**

| Parte | Tema |
|-------|------|
| **1** | Montar Drive y rutas al Parquet de la lección 3 |
| **2** | Enunciar la consulta y listar particiones 2024 |
| **3** | **MapReduce** desde cero (map → shuffle → reduce) + tiempo |
| **4** | **pandas**, misma consulta + comparación |
| **5** | **DuckDB**, SQL sobre archivos Parquet |
| **6** | **Polars**, scan lazy + collect |
| **7** | Tabla de tiempos e interpretación |
| **8** | **Gobernanza al consultar** (`dpto × edad`): supresión **k = 5** vs **privacidad diferencial** |

**Entregas semana 2:** el código evaluable está en **`week-2-group`** (Parte B). Ver **Tareas** al final.

---

## Parte 1. Configuración: Drive y rutas del cuaderno de almacenamiento

Montamos la misma raíz que en la lección 3. Si trabaja **en local** con el mismo layout de carpetas, ponga `USE_GOOGLE_DRIVE = False`.

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
    WORK_ROOT = Path("/content/drive/MyDrive/udenar/cease/2026/big-data/data/")
    print(f"Raíz en Drive: {WORK_ROOT}")
else:
    WORK_ROOT = Path(".")
    print(f"Raíz local: {WORK_ROOT.resolve()}")

PROCESSED_DIR = WORK_ROOT / "data" / "processed" / "geih-spine"  # raíz del Parquet de la lección 3
PARQUET_2024 = PROCESSED_DIR / f"anio={YEAR}"                     # árbol particionado de 2024
OUTPUTS_DIR = WORK_ROOT / "outputs"
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

print("Parquet 2024:", PARQUET_2024)
```

Este cuaderno usa tres librerías que no vienen instaladas en Colab:

- **DuckDB**: una base de datos analítica que corre **dentro del cuaderno** (sin servidor) y consulta archivos Parquet directamente con **SQL**.
- **Polars**: una librería de DataFrames muy rápida, con **evaluación perezosa** (arma el plan de consulta y lo ejecuta al final, en `collect()`).
- **PyArrow**: el motor que pandas usa para leer/escribir Parquet, el mismo que instalamos en la **lección 3**.

```python
# duckdb: SQL sobre Parquet | polars: DataFrames rápidos | pyarrow: motor Parquet (como en lección 3)
%pip install -q duckdb polars pyarrow
```

**Comprobar:**

```python
assert WORK_ROOT.is_dir()
assert PARQUET_2024.is_dir(), (
    f"No encuentro {PARQUET_2024}. Ejecute el cuaderno de la lección 3 (Partes 1–3) primero."
)
_part_check = sorted(PARQUET_2024.rglob("*.parquet"))
print(f"Particiones Parquet 2024: {len(_part_check)}")
assert len(_part_check) >= 12, (
    f"Se esperan ≥12 particiones 2024. Hay {len(_part_check)}. Complete el cuaderno de almacenamiento (lección 3)."
)
print("Parte 1, configuración: OK")
```

---

## Parte 2. Pregunta analítica y particiones

Fijamos constantes compartidas por todos los motores.

```python
import json
import time
from collections import defaultdict

import duckdb
import pandas as pd
import polars as pl

ACTIVIDAD_OCUPADO = 1  # actividad == 1 → ocupado (derivamos ocupado con esta regla)
REGLA_OCUPADO = f"ocupado = (actividad == {ACTIVIDAD_OCUPADO})"
K_MIN = 5  # regla del curso para publicar agregados departamentales

QUERY_DESC = (
    "Por departamento (dpto): conteo sin ponderar de ocupados y "
    "suma de factor_expansion sobre ocupados, GEIH 2024 nacional."
)

part_files = sorted(PARQUET_2024.rglob("*.parquet"))
print(QUERY_DESC)
print(f"Regla ocupado: {REGLA_OCUPADO}")
print(f"Archivos Parquet: {len(part_files)}")
print("Ejemplo:", part_files[0].relative_to(WORK_ROOT))
```

**Comprobar:**

```python
print(f"k mínimo para publicar: {K_MIN}")
assert K_MIN == 5
assert all(p.suffix == ".parquet" for p in part_files)
print("Parte 2, consulta definida: OK")
```

---

## Parte 3. MapReduce

**Idea.** Descomponemos la consulta en tres fases explícitas:

1. **Map:** por cada partición, emitir `(dpto, factor_expansion)` solo para ocupados.
2. **Shuffle:** agrupar todos los pesos por `dpto` (`defaultdict`).
3. **Reduce:** por cada `dpto`, contar filas y sumar pesos.

### Paso 3.1. Definir map, shuffle y reduce

```python
def map_partition(path: Path) -> list[tuple[int, float]]:
    """Lee una partición, deriva ocupado y devuelve pares (dpto, factor_expansion)."""
    # Leer solo las 3 columnas que necesita el map
    df = pd.read_parquet(path, columns=["dpto", "actividad", "factor_expansion"])
    # Derivar ocupado (actividad == 1) y quedarnos con esas filas
    emp = df.loc[df["actividad"] == ACTIVIDAD_OCUPADO, ["dpto", "factor_expansion"]]
    # Emitir un par (dpto, peso) por persona ocupada
    return list(zip(emp["dpto"].astype(int), emp["factor_expansion"].astype(float)))


def shuffle(pairs: list[tuple[int, float]]) -> dict[int, list[float]]:
    """Reúne valores por clave dpto."""
    buckets: dict[int, list[float]] = defaultdict(list)
    for dpto, weight in pairs:
        buckets[dpto].append(weight)  # agrupar todos los pesos del mismo dpto
    return buckets


def reduce_buckets(buckets: dict[int, list[float]]) -> pd.DataFrame:
    """Agrega conteo sin ponderar y suma ponderada por departamento."""
    rows = [
        # Por cada dpto: número de ocupados y suma de sus pesos
        {"dpto": dpto, "conteo_ocupados": len(weights), "suma_ponderada": sum(weights)}
        for dpto, weights in buckets.items()
    ]
    return pd.DataFrame(rows).sort_values("dpto").reset_index(drop=True)


print("Funciones MapReduce: definidas")
```

**`zip(a, b)`** empareja elemento a elemento: toma las columnas `dpto` y `factor_expansion` y devuelve una lista de tuplas `(dpto, peso)`, que es justo lo que emite la fase *map*.

### Paso 3.2. Map en **una** partición (paso a paso)

Tomamos enero como ejemplo y vemos qué emite la fase **map**:

```python
demo_path = part_files[0]
demo_pairs = map_partition(demo_path)
print(f"Partición demo: {demo_path.name}")
print(f"Pares emitidos (map): {len(demo_pairs):,}")
print("Primeros 5 pares (dpto, peso):", demo_pairs[:5])
```

### Paso 3.3. Shuffle y reduce sobre enero

Agrupamos esos pares y reducimos, solo para entender el patrón:

```python
demo_buckets = shuffle(demo_pairs)
print("Departamentos en enero (shuffle):", len(demo_buckets))
print("Ejemplo bucket dpto 11:", demo_buckets.get(11, [])[:3], "...")

demo_reduce = reduce_buckets(demo_buckets)
print("Reduce en enero (primeras filas):")
print(demo_reduce.head())
```

### Paso 3.4. Consolidación: MapReduce sobre todo 2024

Reunimos map → shuffle → reduce en un solo flujo sobre **las 12 particiones** (bloque de diapositivas):

```python
t0 = time.perf_counter()
all_pairs: list[tuple[int, float]] = []
for path in part_files:
    all_pairs.extend(map_partition(path))
buckets = shuffle(all_pairs)
mr_result = reduce_buckets(buckets)
mr_seconds = round(time.perf_counter() - t0, 3)

print(f"Pares totales (map): {len(all_pairs):,}")
print(f"MapReduce, departamentos: {len(mr_result)}")
print(f"MapReduce, tiempo: {mr_seconds} s")
print(mr_result.head())
```

**Comprobar:**

```python
print(f"Departamentos: {len(mr_result)} | Suma ponderada total: {mr_result['suma_ponderada'].sum():,.0f}")
assert len(mr_result) >= 30, f"Pocos departamentos: {len(mr_result)}"
assert mr_result["suma_ponderada"].sum() > 1_000_000
assert mr_result["conteo_ocupados"].sum() > 10_000
print("Parte 3, MapReduce: OK")
```

---

## Parte 4. pandas: misma consulta

Cargamos **todo el árbol 2024** en memoria y usamos la instrucción **`groupby`**.

### Paso 4.1. Paso a paso: leer, filtrar, agrupar

```python
df_2024 = pd.read_parquet(PARQUET_2024)
print(f"Filas cargadas (2024 completo): {len(df_2024):,}")
print("Columnas:", list(df_2024.columns[:8]), "...")
```

Derivamos `ocupado` desde `actividad`, filtramos ocupados y mostramos el subconjunto:

```python
# Derivar ocupado (regla del curso) y filtrar
df_2024["ocupado"] = df_2024["actividad"] == ACTIVIDAD_OCUPADO
employed = df_2024.loc[df_2024["ocupado"]]
print(f"Filas ocupadas: {len(employed):,}")
print(employed[["dpto", "factor_expansion"]].head(5))
```

Agrupamos por departamento:

```python
pandas_result = (
    employed.groupby("dpto", as_index=False)
    .agg(conteo_ocupados=("ocupado", "count"), suma_ponderada=("factor_expansion", "sum"))
    .sort_values("dpto")
    .reset_index(drop=True)
)
print("Agregado pandas (primeras filas):")
print(pandas_result.head())
```

### Paso 4.2. Consolidación: medir tiempo del flujo completo

```python
t0 = time.perf_counter()
_df = pd.read_parquet(PARQUET_2024)
_emp = _df.loc[_df["actividad"] == ACTIVIDAD_OCUPADO]
_pandas = (
    _emp.groupby("dpto", as_index=False)
    .agg(conteo_ocupados=("factor_expansion", "count"), suma_ponderada=("factor_expansion", "sum"))
)
pandas_seconds = round(time.perf_counter() - t0, 3)
del _df, _emp, _pandas

print(f"pandas, departamentos: {len(pandas_result)}")
print(f"pandas, tiempo: {pandas_seconds} s")
```

Opcional: ver el tiempo con **`%%time`** (como en la lección 3):

```python
%%time
_ = pd.read_parquet(PARQUET_2024, columns=["dpto", "actividad", "factor_expansion"])
```

**Comprobar:**

```python
merged = mr_result.merge(pandas_result, on="dpto", suffixes=("_mr", "_pd"))
max_diff = (merged["suma_ponderada_mr"] - merged["suma_ponderada_pd"]).abs().max()
print(f"Diferencia máxima MR vs pandas: {max_diff:.4f}")
assert max_diff < 1.0
print("Parte 4, pandas coincide con MapReduce: OK")
```

---

## Parte 5. DuckDB: SQL sobre Parquet

DuckDB lee el árbol **sin** cargar todo en un DataFrame de pandas primero. Se consulta con **SQL**, el lenguaje estándar de bases de datos. Las piezas que usamos:

- **`SELECT ... FROM`**: qué columnas devolver y de dónde (aquí, los Parquet vía `read_parquet`).
- **`WHERE`**: filtra filas (nuestra regla de ocupado, `actividad = 1`).
- **`COUNT(*)`** y **`SUM(col)`**: agregaciones (contar filas, sumar una columna).
- **`GROUP BY dpto`**: aplica esas agregaciones **por departamento** (el "reduce" de SQL).
- **`ORDER BY`**: ordena el resultado.

```python
# Patrón de rutas para que DuckDB lea todos los Parquet del árbol
parquet_glob = str(PARQUET_2024 / "**" / "*.parquet").replace("\\", "/")
sql_query = f"""
SELECT
    dpto,
    COUNT(*)::BIGINT AS conteo_ocupados,      -- contar ocupados por dpto
    SUM(factor_expansion) AS suma_ponderada   -- sumar sus pesos
FROM read_parquet('{parquet_glob}', hive_partitioning=false)
WHERE actividad = {ACTIVIDAD_OCUPADO}         -- solo ocupados
GROUP BY dpto
ORDER BY dpto
"""
print("Consulta SQL (extracto):")
print(sql_query[:200], "...")
```

**Consolidación**, ejecutamos y medimos tiempo:

```python
t0 = time.perf_counter()
con = duckdb.connect()
duckdb_result = con.execute(sql_query).df()
duckdb_seconds = round(time.perf_counter() - t0, 3)
con.close()

print(f"DuckDB, departamentos: {len(duckdb_result)}")
print(f"DuckDB, tiempo: {duckdb_seconds} s")
print(duckdb_result.head())
```

**Comprobar:**

```python
cmp = mr_result.merge(duckdb_result, on="dpto", suffixes=("_mr", "_dk"))
max_diff = (cmp["suma_ponderada_mr"] - cmp["suma_ponderada_dk"]).abs().max()
print(f"Diferencia máxima MR vs DuckDB: {max_diff:.4f}")
assert max_diff < 1.0
print("Parte 5, DuckDB: OK")
```

---

## Parte 6. Polars: scan lazy

**Polars** aplaza el trabajo hasta **`collect()`**, útil cuando el dataset crece. La consulta se arma con expresiones encadenadas, equivalentes al SQL de arriba:

- **`scan_parquet(...)`**: abre el árbol en modo **perezoso** (aún no lee nada).
- **`.filter(pl.col("actividad") == 1)`**: el `WHERE` (solo ocupados).
- **`.group_by("dpto").agg(...)`**: el `GROUP BY` + agregaciones (`pl.len()` cuenta, `.sum()` suma).
- **`.collect()`**: ejecuta el plan completo (recién aquí se leen los datos).

```python
# scan_parquet NO lee aún: solo describe la consulta (lazy)
lazy_scan = pl.scan_parquet(str(PARQUET_2024 / "**" / "*.parquet"))
lazy_employed = lazy_scan.filter(pl.col("actividad") == ACTIVIDAD_OCUPADO)   # WHERE ocupado
lazy_agg = lazy_employed.group_by("dpto").agg(
    pl.len().alias("conteo_ocupados"),                       # contar
    pl.col("factor_expansion").sum().alias("suma_ponderada"),  # sumar pesos
)
print("Plan lazy Polars definido (sin ejecutar aún)")
```

**Consolidación**, `collect()` ejecuta el plan y medimos tiempo:

```python
t0 = time.perf_counter()
polars_result = lazy_agg.sort("dpto").collect().to_pandas()
polars_seconds = round(time.perf_counter() - t0, 3)

print(f"Polars, departamentos: {len(polars_result)}")
print(f"Polars, tiempo: {polars_seconds} s")
print(polars_result.head())
```

**Comprobar:**

```python
cmp = mr_result.merge(polars_result, on="dpto", suffixes=("_mr", "_pl"))
max_diff = (cmp["suma_ponderada_mr"] - cmp["suma_ponderada_pl"]).abs().max()
print(f"Diferencia máxima MR vs Polars: {max_diff:.4f}")
assert max_diff < 1.0
print("Parte 6, Polars: OK")
```

---

## Parte 7. Tabla de tiempos e interpretación

```python
timing_df = pd.DataFrame(
    [
        {"motor": "MapReduce (desde cero)", "segundos": mr_seconds},
        {"motor": "pandas (groupby)", "segundos": pandas_seconds},
        {"motor": "DuckDB (SQL)", "segundos": duckdb_seconds},
        {"motor": "Polars (lazy)", "segundos": polars_seconds},
    ]
).sort_values("segundos")

print("Comparación de motores, GEIH 2024 completo:")
print(timing_df.to_string(index=False))
print(
    "\nInterpretación: MapReduce enseña el patrón. Pandas/DuckDB/Polars implementan "
    "el mismo reduce de forma optimizada. En la lección 3 vimos que Parquet se lee más "
    "rápido que el CSV crudo. Aquí leemos todo 2024 para comparar motores en igualdad de condiciones."
)
```

Un gráfico de barras hace la comparación más fácil de leer (menos es mejor):

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(7, 3.5))
ax.barh(timing_df["motor"], timing_df["segundos"], color="#4472C4")  # barras horizontales
ax.set_xlabel("Tiempo (segundos, menos es mejor)")
ax.set_title("Tiempo por motor — GEIH 2024 completo")
for y, s in enumerate(timing_df["segundos"]):
    ax.text(s, y, f" {s:.2f}s", va="center")  # etiqueta al final de cada barra
fig.tight_layout()
fig.savefig(OUTPUTS_DIR / "benchmark_motores_2024.png", dpi=120)
plt.show()
print("Gráfico guardado:", OUTPUTS_DIR / "benchmark_motores_2024.png")
```

**Comprobar:**

```python
print("Tiempos (s):", timing_df.set_index("motor")["segundos"].to_dict())
assert len(timing_df) == 4
assert timing_df["segundos"].min() > 0
print("Parte 7, benchmark: OK")
```

---

## Parte 8. Gobernanza al consultar: supresión k=5 vs privacidad diferencial

Las Partes 3 a 7 agregaron por `dpto`: celdas **grandes** (cada departamento tiene miles de personas), con bajo riesgo. Pero publicar tablas **más finas** sube el riesgo de reidentificación: si cruzamos `dpto × edad`, algunas celdas quedan con **muy pocas personas** (departamentos pequeños en edades extremas). Sobre ese agregado fino comparamos **dos protecciones** del curso:

- **Supresión k = 5** (lección 2): ocultar celdas con menos de 5 personas.
- **Privacidad diferencial** (lección 3): publicar todas las celdas, pero con **ruido de Laplace** que oculta el aporte de cualquier individuo.

### Paso 8.1. Agregado fino con celdas pequeñas (`dpto × edad`)

Reusamos `df_2024` (cargado en la Parte 4, ya con la columna `ocupado`):

```python
# Agregado FINO: ocupados por dpto y edad → aparecen celdas pequeñas
fino = (
    df_2024.loc[df_2024["ocupado"]]
    .groupby(["dpto", "edad"], as_index=False)
    .agg(conteo_ocupados=("ocupado", "count"), suma_ponderada=("factor_expansion", "sum"))
)
n_pequenas = int((fino["conteo_ocupados"] < K_MIN).sum())  # celdas riesgosas
print(f"Celdas (dpto × edad): {len(fino):,}")
print(f"Celdas con conteo < {K_MIN}: {n_pequenas:,}")
print(fino.head())
```

### Paso 8.2. Protección A: supresión k = 5

```python
def apply_k_suppression(agg: pd.DataFrame, k: int = K_MIN) -> pd.DataFrame:
    """Marca celdas suprimidas. Publica suma_ponderada solo si conteo_ocupados >= k."""
    out = agg.copy()
    out["suprimido"] = out["conteo_ocupados"] < k                       # celda pequeña → ocultar
    out["suma_publica"] = out["suma_ponderada"].where(~out["suprimido"])  # NaN si se suprime
    return out


pub_k = apply_k_suppression(fino)
n_suprimido = int(pub_k["suprimido"].sum())
print(f"k = {K_MIN} → celdas suprimidas: {n_suprimido:,} de {len(pub_k):,}")
print(pub_k.head(8).to_string(index=False))
```

### Paso 8.3. Protección B: privacidad diferencial (ruido de Laplace)

En lugar de ocultar celdas pequeñas, **sumamos ruido aleatorio** a cada conteo. El ruido se calibra con dos números:

- **Sensibilidad** = 1: un conteo cambia como máximo en 1 si una persona entra o sale.
- **Épsilon (ε)**: el presupuesto de privacidad. **Menor ε = más ruido = más privacidad** (y menos exactitud).

```python
import numpy as np

EPSILON = 1.0        # presupuesto de privacidad (menor = más privacidad)
SENSIBILIDAD = 1.0   # un conteo cambia como máximo 1 con una persona

def laplace_count(valor: float, epsilon: float, sensibilidad: float, rng) -> int:
    ruido = rng.laplace(0.0, sensibilidad / epsilon)  # escala = sensibilidad/epsilon
    return max(0, round(valor + ruido))               # conteos no negativos

rng = np.random.default_rng(42)  # semilla fija para reproducir
pub_dp = fino.copy()
pub_dp["conteo_dp"] = [laplace_count(c, EPSILON, SENSIBILIDAD, rng) for c in pub_dp["conteo_ocupados"]]

print(f"Privacidad diferencial (ε = {EPSILON}): ruido agregado a cada conteo")
print(pub_dp[["dpto", "edad", "conteo_ocupados", "conteo_dp"]].head(8).to_string(index=False))
```

### Paso 8.4. Consolidación: comparar las dos estrategias

```python
# Unimos ambas vistas para comparar en las celdas pequeñas (las riesgosas)
comparacion = pub_k.merge(pub_dp[["dpto", "edad", "conteo_dp"]], on=["dpto", "edad"])
muestra = (
    comparacion.loc[comparacion["suprimido"], ["dpto", "edad", "conteo_ocupados", "suma_publica", "conteo_dp"]]
    .head(8)
)
print("Celdas pequeñas (conteo < 5): qué hace cada estrategia")
print(muestra.to_string(index=False))
print(
    f"\nk={K_MIN}: oculta {n_suprimido:,} celdas (suma_publica = NaN), pierde detalle fino.\n"
    "DP: publica todas las celdas, pero cada conteo trae ruido (compare conteo_ocupados vs conteo_dp)."
)

pub_path = OUTPUTS_DIR / "agg_ocupados_dpto_edad_2024.csv"
comparacion.to_csv(pub_path, index=False)  # uso interno del curso, no Moodle
print(f"\nGuardado: {pub_path}")
```

**Comprobar:**

```python
print(f"Suprimidas (k={K_MIN}): {n_suprimido} | Celdas con ruido DP: {len(pub_dp)}")
assert pub_k.loc[pub_k["suprimido"], "suma_publica"].isna().all()   # k-supresión oculta lo pequeño
assert (pub_dp["conteo_dp"] >= 0).all()                              # DP no produce conteos negativos
assert pub_path.is_file()
print("Parte 8, gobernanza (k=5 y privacidad diferencial): OK")
```

---

## Puente al cuaderno grupal

En **`week-2-group` Parte B** su grupo:

1. Reimplementa **MapReduce desde cero** sobre el spine **2022–2025** (misma consulta).
2. **Selecciona UN motor** (DuckDB **o** Polars) y lo aplica sobre **2022–2025**, justificando la elección.
3. **Decide la estrategia de privacidad**: continuar con **supresión k = 5** (lección 4) o aplicar **privacidad diferencial** (ruido de Laplace, lección 3). Justifica la decisión.
4. Actualiza **`manifest.json`** (conteos y metadatos, no Parquet en el ZIP).

Entrega Moodle **martes 16 jun 2026**: ZIP con cuaderno ejecutado + `manifest.json` (sin archivos de datos).

---

## Tareas

Plantillas y plazos en el [hub semana 2](/work-space/teaching/big-data/course/week-2/week-2-hub-es.md) y en la [Lección 4 (Procesamiento)](/teaching/26-udenar-big-data/l4-processing/).

### Trabajo en grupo (semana 2)

Colab **`week-2-group`**. ZIP **`week-2-<group_id>.zip`** hasta el **martes 16 de junio de 2026, 23:59 (Colombia)**:

| Archivo en el ZIP | Descripción |
|-------------------|-------------|
| `week-2-group-<group_id>.ipynb` | Cuaderno grupal ejecutado |
| `manifest.json` | Conteos y metadatos |

### Reflexión individual

PDF **`week-2-reflection-<student>.pdf`** hasta el **miércoles 17 de junio de 2026**. Plantilla: [reflection-week-2-template.docx](/assets/documents/26-udenar-big-data/reflection-week-2-template.docx).

### Requerimientos del proyecto

Discusión de los requerimientos durante la sesión del **sábado 13 jun**. Esta semana se deben tener definidos, harmonizados y particionados los datos que va a utilizar durante el proyecto. La arquitectura de datos y procesamiento se discute en la sesión del **sábado 20 jun**.

<!-- end NOTEBOOK: -->
