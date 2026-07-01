<!-- NOTEBOOK: -->

## Instrucciones

**Propósito.** Cuaderno grupal para la semana 2 (Lecciones 3 y 4). Aquí está **todo el código evaluable** de la semana: construir el **lakehouse GEIH completo (2022–2025)**, consultarlo con **MapReduce** y **un motor moderno**, y **publicar agregados** con gobernanza.

**Requisito.** Ejecute primero los cuadernos individuales **`l3-storage`** y **`l4-processing`** (run-only). Aquí **adaptan** y **escriben** código — copie funciones de L3/L4 y extiéndalas; no pegue sin entender. Desarrolle el cuaderno en grupo (bloque de 2 h el **sábado 13 jun**).

**Datos de entrada.** CSV crudos **2022–2025** de **`week-1-group`** (o la misma copia en Google Drive). Catálogos DANE: 2022 → `771`, 2023 → `782`, 2024 → `819`, 2025 → `853`.

**Colab:** `/content` se borra al reiniciar. Monte **Google Drive** (`USE_GOOGLE_DRIVE = True`) o vuelva a copiar CSV desde week-1. Use `spine_has_full_raw` / `resolve_raw_dir` de L3 para separar sesión y Drive.

**Materiales:** [L3 Almacenamiento](https://cabrerac.github.io/teaching/26-udenar-big-data/l3-storage/) · [L4 Procesamiento](https://cabrerac.github.io/teaching/26-udenar-big-data/l4-processing/).

**Pregunta analítica (igual que L4).** Por departamento (`dpto`): **conteo sin ponderar** de ocupados y **suma ponderada** (Σ `factor_expansion`). Regla de ocupado: `actividad == 1`. **Importante:** cada Parquet es **un mes**; promedie estimaciones mensuales por `dpto` (L4 Parte 3.4–3.5). **No** sume 48 meses crudos (~48× inflado).

**Entrega Moodle (martes 16 jun 2026, 23:59 Colombia):** ZIP `week-2-group-<group_id>.zip` con `week-2-group-<group_id>.ipynb` (renombre este cuaderno al exportar) y `manifest.json` en la **raíz del ZIP**. **Sin** archivos Parquet ni CSV en el ZIP.

**Mapa del cuaderno (tres ejercicios)**

| Ejercicio | Tema | Entregable clave |
|-----------|------|------------------|
| **1** | Lakehouse 2022–2025 | Parquet particionado en Drive + benchmark layout + retención/linaje |
| **2** | MapReduce + **un** motor (DuckDB **o** Polars) | Tabla de tiempos + markdown de elección de motor |
| **3** | Publicar con gobernanza | Agregado por `dpto` + **k = 5** **o** Laplace (justificado) + `manifest.json` |

Use `SKIP_IF_PARQUET_EXISTS` si ya tiene los datos en Drive. El ejercicio 2 sobre el árbol completo es pesado; empiece con un subconjunto si Colab se queda sin memoria y documente la limitación en markdown.

**Celdas Comprobar:** ejecute **de arriba abajo**. Si una celda de código falla, las Comprobar siguientes pueden marcar error hasta que corrija y re-ejecute desde ahí.

---

## Configuración — Drive y rutas

Monte **Google Drive** igual que en [`l3-storage`](https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-big-data/l3-storage.ipynb) (Parte 1). Si trabaja en **local** con el mismo layout, ponga `USE_GOOGLE_DRIVE = False`.

Copie constantes y ayudantes de harmonización del cuaderno individual **L3**:

| Qué copiar | Dónde está en L3 |
|------------|------------------|
| `CSV_SEP`, `CSV_ENCODING`, `PERSON_KEYS`, `PRIMARY_TABLE_KEYWORD`, `DEMOG_TABLE_KEYWORDS` | Parte 0 / Parte 2 |
| `_csv_files`, `_labour_csv`, `_demog_csv`, `month_dirs_for_year` | Parte 2, Paso 2.1 |
| `a_entero`, `harmonize_month`, `read_geih_csv` | Parte 0 / Parte 2 |
| `count_month_folders`, `spine_has_full_raw`, `resolve_raw_dir` | Parte 0 / Parte 1 |

Copie de **L4** (Parte 3) para el ejercicio 2:

| Qué copiar | Dónde está en L4 |
|------------|------------------|
| `map_partition`, `shuffle`, `reduce_buckets` | Parte 3, Paso 3.1 |
| `anio_mes_from_path`, `annual_avg_from_monthly` | Parte 3, Paso 3.1 |

Defina también:

```python
SPINE_YEARS = [2022, 2023, 2024, 2025]
# Motor moderno para el ejercicio 2: "duckdb" o "polars" (elija UNO)
ENGINE = "duckdb"  # cambie a "polars" si su grupo prefiere Polars
# Estrategia de privacidad para el ejercicio 3: "k_suppression" o "laplace"
PRIVACY_STRATEGY = "k_suppression"  # o "laplace"
ACTIVIDAD_OCUPADO = 1
K_MIN = 5
EPSILON = 1.0
SENSIBILIDAD = 1.0
```

```python
# SU CÓDIGO — montar Drive, WORK_ROOT, SESSION_RAW, DRIVE_RAW, resolve_raw_dir → RAW_DIR,
# PROCESSED_DIR, MANIFEST_PATH, OUTPUTS_DIR
# + constantes y funciones copiadas de l3-storage y l4-processing

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

Verifique que cada año tiene **12 carpetas mensuales** con CSV bajo `data/raw/<año>/`. Si todos los conteos son 0, revise las líneas sesión vs Drive del Paso 1.2/1.3 en L3 o re-ejecute week-1.

```python
# SU CÓDIGO — meses_por_anio con count_month_folders

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

Recorra **cada año** con `month_dirs_for_year` (solo meses con labour + demog), aplique `harmonize_month` y escriba Parquet. Use `SKIP_IF_PARQUET_EXISTS = True` para no reescribir particiones ya cargadas.

**Pista:** extienda el bucle de L3 Parte 3 (un año) a cuatro años y acumule `partition_stats`.

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

1. Leer **todo** el spine bajo `PROCESSED_DIR` (p. ej. `read_parquet_tree` de L4)
2. `pd.read_parquet(PROCESSED_DIR / "anio=2024" / "mes=01")` — **una partición**

Guarde números en `bench_full_seconds`, `bench_one_seconds`.

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

1. **MapReduce desde cero** — **mensual** (map → shuffle → reduce por partición) → **`annual_avg_from_monthly`** (o equivalente sobre ~48 meses).
2. **Un motor moderno:** DuckDB **o** Polars, misma lógica de **dos pasos** (`GROUP BY dpto, anio, mes` → promedio por `dpto`).

No hace falta repetir pandas si ya lo vieron en L4; puede citar tiempos del cuaderno individual en el markdown.

## Paso 2.1 — MapReduce desde cero

Copie de L4 Parte 3 (`map_partition`, `shuffle`, `reduce_buckets`, `anio_mes_from_path`, `annual_avg_from_monthly`):

- Liste **todos** los `.parquet` bajo `PROCESSED_DIR`.
- Por partición: map → shuffle → reduce; guarde `anio` y `mes` con `anio_mes_from_path`.
- Concatene en `mr_monthly`; promedie en `mr_result`; tiempo en `mr_seconds`.
- Imprima `promedio_nacional = mr_result["suma_ponderada"].sum()` (debe estar ~15–30 millones, no ~200M).

```python
# SU CÓDIGO

```

**Comprobar:**

```python
assert len(mr_result) >= 30
promedio_nacional = mr_result["suma_ponderada"].sum()
assert 15_000_000 < promedio_nacional < 30_000_000, (
    f"¿Sumó meses crudos? Promedio nacional: {promedio_nacional:,.0f}"
)
assert mr_seconds > 0
print(f"MapReduce: {len(mr_result)} dptos | {mr_seconds:.3f}s | nacional: {promedio_nacional:,.0f}")
print("Paso 2.1, MapReduce: OK")
```

---

## Paso 2.2 — Motor elegido (DuckDB o Polars)

Implemente la **misma consulta** con el motor indicado en `ENGINE` (L4 Parte 5 o 6: subconsulta mensual + promedio exterior; incluya **`anio`** en el `GROUP BY` mensual).

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

Arme `timing_df` con al menos MapReduce y su motor. En markdown (**≥ 80 palabras**): por qué eligió DuckDB **o** Polars; trade-offs vs MapReduce; cite **sus** tiempos.

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

**Tarea.** Construya el agregado departamental (`dpto`, `conteo_ocupados`, `suma_ponderada`) desde `mr_result`. **Elija UNA estrategia** (`PRIVACY_STRATEGY`):

| Estrategia | Qué implementar | Referencia |
|------------|-----------------|------------|
| `k_suppression` | Suprimir celdas con conteo &lt; 5; publicar suma ponderada solo si no suprimida | L4 Parte 8.2 |
| `laplace` | Ruido de Laplace en conteos (defina `epsilon` y sensibilidad) | L3 Parte 5.2 / L4 Parte 8.3 |

En markdown (**≥ 100 palabras**): **justifique** por qué su grupo eligió k-anonimato/supresión **o** privacidad diferencial para **este** agregado y su proyecto (Dwork, Zuboff cap. 3, §6–§7 del PDF de requerimientos).

## Paso 3.1 — Agregado departamental

Guarde la tabla en Drive, p. ej. `outputs/agg_ocupados_dpto_spine.csv`.

```python
# SU CÓDIGO — dept_agg desde mr_result; guardar CSV

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
# SU CÓDIGO — leer manifest existente, actualizar, json.dump

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
