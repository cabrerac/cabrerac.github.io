---
course_code: 26-udenar-big-data
title: Data processing and analysis
description: Lecture 4 introduces data processing. Once data is stored in a harmonised structure we need methods for efficient access and analysis. This lecture presents big data processing approaches and engines that scale like the MapReduce algorithm working on top of pandas, DuckDB, and Polars.
session: 4
start_time: 07:00 am
end_time: 01:00 pm
hours: 5
author: Christian Cabrera Jojoa
email: chc79@cam.ac.uk
position: Assistant Research Professor
department: Department of Computer Science and Technology
institution: University of Cambridge
layout: lecture
lecture_code: l4-processing
lecture_date: 13/06/2026
permalink: /teaching/26-udenar-big-data/l4-processing/
visible: true
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

# Governance

<!-- end SLIDES: -->

{% include _snippets/26-udenar-big-data/l4-processing/governance.md %}

<!-- SLIDES: -->

# Assess and Address

<!-- end SLIDES: -->

{% include _snippets/26-udenar-big-data/l4-processing/assess-address.md %}

<!-- SLIDES: -->

# Data Architecture

<!-- end SLIDES: -->

{% include _snippets/26-udenar-big-data/l4-processing/data-architecture.md %}

<!-- SLIDES: -->

# Conclusions

<!-- end SLIDES: -->

{% include _snippets/26-udenar-big-data/l4-processing/conclusions.md %}

{% include _snippets/26-udenar-big-data/l4-processing/practical-slides.md %}

<!-- RENDER: -->

### Week 2 links

- [Week 2 hub](/teaching/26-udenar-big-data/week-2-hub-es/)

### Resources

- [Introductory Python course](https://www.youtube.com/watch?v=nKPbfIU442g) (optional video)
- [Introduction to data management](https://www.youtube.com/watch?v=9P2oNqRbdyI) (optional video)

### References

- Zuboff, S. (2019). *The age of surveillance capitalism* (Chapter 3). PublicAffairs. *(Course PDF — same as week 1.)*
- Dwork, C. (2006). [Differential privacy](https://doi.org/10.1007/11787006_1). *ICALP 2006* (LNCS 4052).
- Dean, J., & Ghemawat, S. (2008). [MapReduce: Simplified data processing on large clusters](https://doi.org/10.1145/1327452.1327492). *Communications of the ACM*, 51(1), 107–113.
- Armbrust, M., et al. (2021). [Lakehouse: A new generation of open platforms](https://people.eecs.berkeley.edu/~matei/papers/2021/cidr_lakehouse.pdf). *CIDR ’21*.

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
| **Conteo sin ponderar (mensual)** | Filas ocupadas en **un mes** |
| **Suma ponderada (mensual)** | Σ `factor_expansion` sobre ocupados **en ese mes** → estimación DANE del empleo ese mes |
| **Promedio anual por dpto** | **Media** de las 12 sumas mensuales por departamento (no sumar los 12 meses) |

**¿Qué es `factor_expansion`?** La GEIH es una **muestra**: no encuesta a todo el país. Cada persona trae un **factor de expansión** (`FEX_C18` en el DANE) que indica **a cuántas personas de la población representa**. Por eso, para estimar un total poblacional no contamos filas, sino que **sumamos el factor de expansión** (la "suma ponderada") **en un mes dado**.

**Promedio anual (método del curso).** Cada mes es una **foto distinta** de la población ocupada. **No** sumamos enero+diciembre (eso infla ~12×). Primero calculamos la suma ponderada **por `(dpto, mes)`**, luego **`promedio_anual = media de esos 12 valores`**. Es un **promedio anual simple**, alineado con la idea DANE de *promedio del año* (no es panel longitudinal de las mismas personas).

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
    """Fase Map: emite (dpto, factor_expansion) por cada ocupado en una partición.

    Parámetros:
        path: ruta a un part-000.parquet (un mes del lakehouse).

    Retorna:
        Lista de tuplas (código departamento, peso de expansión).
    """
    df = pd.read_parquet(path, columns=["dpto", "actividad", "factor_expansion"])
    # Derivar ocupado (actividad == 1) y quedarnos con esas filas
    emp = df.loc[df["actividad"] == ACTIVIDAD_OCUPADO, ["dpto", "factor_expansion"]]
    # Emitir un par (dpto, peso) por persona ocupada
    return list(zip(emp["dpto"].astype(int), emp["factor_expansion"].astype(float)))


def shuffle(pairs: list[tuple[int, float]]) -> dict[int, list[float]]:
    """Fase Shuffle: agrupa pesos por clave dpto.

    Parámetros:
        pairs: salida de map_partition (lista de tuplas).

    Retorna:
        Dict {dpto: [lista de factor_expansion]}.
    """
    buckets: dict[int, list[float]] = defaultdict(list)
    for dpto, weight in pairs:
        buckets[dpto].append(weight)  # agrupar todos los pesos del mismo dpto
    return buckets


def reduce_buckets(buckets: dict[int, list[float]]) -> pd.DataFrame:
    """Fase Reduce: conteo y suma ponderada por departamento.

    Parámetros:
        buckets: salida de shuffle ({dpto: [pesos]}).

    Retorna:
        DataFrame con columnas dpto, conteo_ocupados, suma_ponderada.
    """
    rows = [
        # Por cada dpto: número de ocupados y suma de sus pesos
        {"dpto": dpto, "conteo_ocupados": len(weights), "suma_ponderada": sum(weights)}
        for dpto, weights in buckets.items()
    ]
    return pd.DataFrame(rows).sort_values("dpto").reset_index(drop=True)


def anio_mes_from_path(path: Path) -> tuple[int, int]:
    """Extrae año y mes de una ruta con partición Hive.

    Parámetros:
        path: ruta con segmentos anio=AAAA y mes=MM (p. ej. …/anio=2024/mes=01/…).

    Retorna:
        Tupla (anio, mes) como enteros.

    Lanza:
        ValueError si falta anio= o mes= en la ruta.
    """
    anio = mes = None
    for part in path.parts:
        if part.startswith("anio="):
            anio = int(part.split("=", 1)[1])
        if part.startswith("mes="):
            mes = int(part.split("=", 1)[1])
    if anio is None or mes is None:
        raise ValueError(f"No encontré anio=/mes= en {path}")
    return anio, mes


def mes_from_path(path: Path) -> int:
    """Atajo: devuelve solo el mes desde una ruta Hive.

    Parámetros:
        path: ruta con mes=MM (y anio=AAAA).

    Retorna:
        Entero mes (1–12). Reutiliza anio_mes_from_path.
    """
    return anio_mes_from_path(path)[1]


def annual_avg_from_monthly(monthly: pd.DataFrame) -> pd.DataFrame:
    """Promedio anual por departamento a partir de estimaciones mensuales.

    Parámetros:
        monthly: tabla con dpto, mes y columnas conteo_ocupados, suma_ponderada
                 (una fila por dpto × mes).

    Retorna:
        DataFrame por dpto con medias de conteo y suma_ponderada (columna meses).
    """
    return (
        monthly.groupby("dpto", as_index=False)
        .agg(
            meses=("mes", "count"),
            conteo_ocupados=("conteo_ocupados", "mean"),
            suma_ponderada=("suma_ponderada", "mean"),
        )
        .sort_values("dpto")
        .reset_index(drop=True)
    )


print("Funciones MapReduce: definidas")
```

**`zip(a, b)`** empareja elemento a elemento: toma las columnas `dpto` y `factor_expansion` y devuelve una lista de tuplas `(dpto, peso)`, que es justo lo que emite la fase *map*.

### Paso 3.2. Map en **una** partición (paso a paso)

Tomamos enero como ejemplo y vemos qué emite la fase **map**:

```python
demo_path = part_files[0]
# Reutiliza map_partition (definida arriba)
demo_pairs = map_partition(demo_path)
print(f"Partición demo: {demo_path.name}")
print(f"Pares emitidos (map): {len(demo_pairs):,}")
print("Primeros 5 pares (dpto, peso):", demo_pairs[:5])
```

### Paso 3.3. Shuffle y reduce sobre enero

Agrupamos esos pares y reducimos, solo para entender el patrón:

```python
# Reutiliza shuffle y reduce_buckets
demo_buckets = shuffle(demo_pairs)
print("Departamentos en enero (shuffle):", len(demo_buckets))
print("Ejemplo bucket dpto 11:", demo_buckets.get(11, [])[:3], "...")

demo_reduce = reduce_buckets(demo_buckets)
print("Reduce en enero (primeras filas):")
print(demo_reduce.head())
```

### Paso 3.4. MapReduce **mensual** (12 particiones)

Cada archivo Parquet es **un mes**. Ejecutamos map → shuffle → reduce **por partición** y guardamos el mes:

```python
t0 = time.perf_counter()
monthly_rows: list[pd.DataFrame] = []
for path in part_files:
    anio, mes = anio_mes_from_path(path)  # Reutiliza anio_mes_from_path
    # Reutiliza map → shuffle → reduce
    dept = reduce_buckets(shuffle(map_partition(path)))
    dept["anio"] = anio
    dept["mes"] = mes
    monthly_rows.append(dept)

mr_monthly = pd.concat(monthly_rows, ignore_index=True).sort_values(["dpto", "anio", "mes"])
mr_seconds = round(time.perf_counter() - t0, 3)
print(f"Filas mensuales (dpto × mes): {len(mr_monthly):,}")
print(f"MapReduce mensual, tiempo: {mr_seconds} s")
print(mr_monthly.head(8))
```

### Paso 3.5. **Promedio anual** por departamento

**Método:** para cada `dpto`, promediamos las 12 `suma_ponderada` mensuales. Eso estima el **empleo ocupado promedio del año** (nivel nacional ≈ suma de promedios departamentales).

```python
# Reutiliza annual_avg_from_monthly (no sumar meses crudos)
mr_result = annual_avg_from_monthly(mr_monthly)

promedio_nacional = mr_result["suma_ponderada"].sum()
suma_doce_meses = mr_monthly.groupby("dpto")["suma_ponderada"].sum().sum()  # trampa: ~12× inflado

print(f"MapReduce, departamentos: {len(mr_result)}")
print(f"Promedio nacional anual (ocupados ponderados): {promedio_nacional:,.0f}")
print(f"(Contraste — NO usar) suma cruda 12 meses: {suma_doce_meses:,.0f}")
print(mr_result.head())
```

**Comprobar:**

```python
assert mr_monthly["mes"].nunique() >= 12, "Faltan meses en mr_monthly"
assert (mr_monthly.groupby("dpto")["mes"].count() >= 10).all(), "Algún dpto con pocos meses"
assert 15_000_000 < promedio_nacional < 30_000_000, (
    f"Promedio nacional fuera de rango plausible: {promedio_nacional:,.0f}"
)
assert promedio_nacional * 10 < suma_doce_meses, "La suma 12-meses debería ser mucho mayor que el promedio anual"
print("Parte 3, MapReduce mensual + promedio anual: OK")
```

---

## Parte 4. pandas: misma consulta

Cargamos **todo el árbol 2024** en memoria y usamos la instrucción **`groupby`**.

```python
def read_parquet_tree(root: Path, columns=None) -> pd.DataFrame:
    """Lee y concatena particiones Parquet bajo root (misma función que L3 Parte 4).

    Parámetros:
        root: carpeta del lakehouse o subárbol (p. ej. PARQUET_2024).
        columns: columnas opcionales a cargar.

    Retorna:
        DataFrame con todas las filas concatenadas.

    Lanza:
        FileNotFoundError si no hay .parquet bajo root.
    """
    files = sorted(root.rglob("*.parquet"))
    if not files:
        raise FileNotFoundError(f"Sin Parquet bajo {root}")
    parts = [pd.read_parquet(f, columns=columns) for f in files]
    return pd.concat(parts, ignore_index=True)
```

### Paso 4.1. Paso a paso: leer, filtrar, agrupar

```python
# Reutiliza read_parquet_tree
df_2024 = read_parquet_tree(PARQUET_2024)
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

Agrupamos por **departamento y mes**, luego **promedio anual** (mismo método que MapReduce):

```python
monthly_pd = (
    employed.groupby(["dpto", "anio", "mes"], as_index=False)
    .agg(conteo_ocupados=("ocupado", "count"), suma_ponderada=("factor_expansion", "sum"))
)
# Reutiliza annual_avg_from_monthly (misma semántica que MapReduce)
pandas_result = annual_avg_from_monthly(monthly_pd)
print("Promedio anual pandas (primeras filas):")
print(pandas_result.head())
```

### Paso 4.2. Consolidación: medir tiempo del flujo completo

```python
t0 = time.perf_counter()
# Reutiliza read_parquet_tree y annual_avg_from_monthly
_df = read_parquet_tree(PARQUET_2024)
_emp = _df.loc[_df["actividad"] == ACTIVIDAD_OCUPADO]
_monthly = _emp.groupby(["dpto", "anio", "mes"], as_index=False).agg(
    conteo_ocupados=("factor_expansion", "count"),
    suma_ponderada=("factor_expansion", "sum"),
)
_pandas = annual_avg_from_monthly(_monthly)
pandas_seconds = round(time.perf_counter() - t0, 3)
del _df, _emp, _pandas

print(f"pandas, departamentos: {len(pandas_result)}")
print(f"pandas, tiempo: {pandas_seconds} s")
```

Opcional: ver el tiempo con **`%%time`** (como en la lección 3):

```python
%%time
_ = read_parquet_tree(PARQUET_2024, columns=["dpto", "actividad", "factor_expansion"])
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
- **`GROUP BY dpto, anio, mes`**: agrega **por mes** (incluya `anio` si hay varios años en el árbol); la consulta exterior promedia → **promedio anual** (o promedio sobre todas las particiones mensuales en `week-2-group`).

```python
# Patrón de rutas para que DuckDB lea todos los Parquet del árbol
parquet_glob = str(PARQUET_2024 / "**" / "*.parquet").replace("\\", "/")
sql_query = f"""
SELECT
    dpto,
    AVG(conteo_ocupados) AS conteo_ocupados,
    AVG(suma_ponderada) AS suma_ponderada
FROM (
    SELECT
        dpto,
        anio,
        mes,
        COUNT(*)::BIGINT AS conteo_ocupados,
        SUM(factor_expansion) AS suma_ponderada
    FROM read_parquet('{parquet_glob}', hive_partitioning=false)
    WHERE actividad = {ACTIVIDAD_OCUPADO}
    GROUP BY dpto, anio, mes
) monthly
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
cmp = mr_result.merge(duckdb_result, on="dpto", suffixes=("_mr", "_dk"))  # comparar con MapReduce
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
- **`.group_by("dpto", "anio", "mes").agg(...)`** luego **`.group_by("dpto").agg(pl.mean(...))`**: promedio sobre estimaciones mensuales.

```python
# scan_parquet NO lee aún: solo describe la consulta (lazy)
lazy_scan = pl.scan_parquet(str(PARQUET_2024 / "**" / "*.parquet"))
lazy_employed = lazy_scan.filter(pl.col("actividad") == ACTIVIDAD_OCUPADO)
lazy_monthly = lazy_employed.group_by("dpto", "anio", "mes").agg(
    pl.len().alias("conteo_ocupados"),
    pl.col("factor_expansion").sum().alias("suma_ponderada"),
)
lazy_agg = lazy_monthly.group_by("dpto").agg(
    pl.col("conteo_ocupados").mean().alias("conteo_ocupados"),
    pl.col("suma_ponderada").mean().alias("suma_ponderada"),
)
print("Plan lazy Polars definido (promedio anual, sin ejecutar aún)")
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
    """Suprime celdas con conteo menor que k antes de publicar agregados.

    Parámetros:
        agg: tabla agregada con conteo_ocupados y suma_ponderada.
        k: umbral mínimo de personas en celda (curso: 5).

    Retorna:
        Copia de agg con columnas suprimido (bool) y suma_publica (NaN si suprimido).
    """
    out = agg.copy()
    out["suprimido"] = out["conteo_ocupados"] < k                       # celda pequeña → ocultar
    out["suma_publica"] = out["suma_ponderada"].where(~out["suprimido"])  # NaN si se suprime
    return out


pub_k = apply_k_suppression(fino)  # Reutiliza apply_k_suppression
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
    """Añade ruido Laplace a un conteo (privacidad diferencial).

    Parámetros:
        valor: conteo real.
        epsilon: presupuesto de privacidad (menor → más ruido).
        sensibilidad: cambio máximo si entra/sale una persona (1 para conteos).
        rng: generador numpy (p. ej. np.random.default_rng(42)).

    Retorna:
        Entero ≥ 0 con ruido aplicado (redondeado).
    """
    ruido = rng.laplace(0.0, sensibilidad / epsilon)
    return max(0, round(valor + ruido))               # conteos no negativos

rng = np.random.default_rng(42)  # semilla fija para reproducir
pub_dp = fino.copy()
pub_dp["conteo_dp"] = [
    laplace_count(c, EPSILON, SENSIBILIDAD, rng)  # Reutiliza laplace_count (L3 Parte 5.2)
    for c in pub_dp["conteo_ocupados"]
]

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

En **`week-2-group`** su grupo **reutiliza** las funciones de este cuaderno (`map_partition`, `shuffle`, `reduce_buckets`, `anio_mes_from_path`, `annual_avg_from_monthly`) sobre el spine **2022–2025** (~48 particiones):

1. **MapReduce mensual → promedio** por `dpto` (no sume 48 meses crudos: inflaría ~48× el empleo nacional).
2. **Selecciona UN motor** (DuckDB **o** Polars) con la misma lógica de dos pasos (`GROUP BY dpto, anio, mes` → promedio).
3. **Decide la estrategia de privacidad**: **supresión k = 5** o **privacidad diferencial** (Laplace). Justifica.
4. Actualiza **`manifest.json`** (conteos y metadatos, no Parquet en el ZIP).

Copie también de **L3** los helpers de harmonización (`spine_has_full_raw`, `resolve_raw_dir`, `_labour_csv`, `month_dirs_for_year`, `harmonize_month`).

Entrega Moodle **martes 16 jun 2026**: ZIP con cuaderno ejecutado + `manifest.json` (sin archivos de datos).

---

## Tareas

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
