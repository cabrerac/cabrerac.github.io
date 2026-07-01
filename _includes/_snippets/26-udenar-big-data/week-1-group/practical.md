<!-- NOTEBOOK: -->

## Instrucciones

**Propósito.** Cuaderno grupal para la semana 1 (Lecciones 1 y 2). Parte A: descargar GEIH **2022–2025** (mismo patrón que el [cuaderno individual L1](https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-big-data/l1-introduction.ipynb)). Parte B: auditoría ética y enlace GEIH + OSM (adaptando el [cuaderno individual L2](https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-big-data/l2-ethics-governance.ipynb)).

**Requisito.** Complete primero los cuadernos individuales **L1** y **L2**. Aquí **adaptan** ese código. No copie celdas sin entenderlas. Este cuaderno se debe desarrollar en grupo en la sesión del Sábado.

Lea la [definición del proyecto (PDF)](/assets/documents/26-udenar-big-data/project-definition-big-data.pdf) con su grupo (también en la [página L1](/teaching/26-udenar-big-data/l1-introduction/)). Plantilla Word de requerimientos: [`project-requirements-template.docx`](/assets/documents/26-udenar-big-data/project-requirements-template.docx) (PDF en **semana 2**).

**Materiales:** páginas de [L1](https://cabrerac.github.io/teaching/26-udenar-big-data/l1-introduction/) y [L2](https://cabrerac.github.io/teaching/26-udenar-big-data/l2-ethics-governance/) (sección *Resources*).

**Entrega Moodle (lunes 8 jun 2026, 23:59 Colombia):** ZIP `week-1-<group_id>.zip` con `notebook-week-1-group-<group_id>.ipynb` (renombre este cuaderno al exportar), `manifest.json` (raíz del ZIP) y `outputs/osm_poi_by_dpto.csv`.

**Catálogos DANE por año:** 2022 → `771`, 2023 → `782`, 2024 → `819`, 2025 → `853`.

**Mapa del cuaderno**

| Bloque | Pasos | Entregable clave |
|--------|-------|------------------|
| **Parte A** (L1) | Config → descarga → exploración (3 pasos) | `manifest.json` + exploración en el cuaderno |
| **Parte B** (L2) | Preparar `df` → 3 pasos (código) | `outputs/osm_poi_by_dpto.csv` + `enlace_df` + gráfico |
| **Cierre** | Registro de contribución | Líneas por integrante + escriba de la semana (cuaderno; §10 del PDF = S1–S4) |

**Tiempo orientativo:** La descarga puede tardar un tiempo en Parte A. Parte B: bucle OSM con **mínimo 5 departamentos** (más si alcanza el tiempo).

---

# Parte A — Access GEIH 2022–2025 (L1)

**Tarea.** Replicar el pipeline de acceso de L1 para **cuatro años** y dejar un manifiesto auditable.

## Configuración

Copie del [cuaderno individual L1](https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-big-data/l1-introduction.ipynb) y adapte (referencias L1):

| Qué copiar | Dónde está en L1 |
|------------|------------------|
| `download_zip` | Parte 1, Paso 2 |
| `extract_csvs` | Parte 1, Paso 3 |
| `write_manifest` | Parte 1, Paso 5 |
| `list_catalog_downloads` + bucle `access_file` | Parte 2, Paso 2 y Paso 3 |
| Constantes `CSV_SEP`, `CSV_ENCODING`, `PRIMARY_TABLE_KEYWORD` | Parte 1, Paso 1 |

**Pista:** En esta celda se deben añadir las variables y constantes que usted considere necesarias. Por ejemplo, la lista de catalogos por año y la lista de años.

```python
# SU CÓDIGO

```

---

## Descargar 2022–2025

**En este paso:** por cada año en `DATASET_YEARS`, obtenga la lista de archivos del catálogo DANE, descargue cada mes, extraiga CSV y añada una fila a `manifest_entries`.

Cada fila del manifiesto debe incluir **`survey_year`** (como en L1 `access_file`), además de `catalog_id`, `file_id`, `filename`, `bytes_downloaded`, etc.

**Pista:** Una petición get-microdata por año. Bucle sobre los archivos mensuales. La tarea puede tomar un tiempo y ocupar **varios GB**.

Al terminar debe existir:

- `manifest_entries`: lista de diccionarios (una fila por ZIP descargado)
- `manifest_path`: `Path("manifest.json")` escrito con su función `write_manifest`

```python
# SU CÓDIGO

```

**Comprobar:**

```python
assert manifest_path.is_file(), "Falta manifest.json"
assert len(manifest_entries) >= 40, "Se esperan ~48 archivos (12 meses × 4 años)"
assert manifest_entries[0].get("bytes_downloaded", 0) > 0
assert "survey_year" in manifest_entries[0], "Cada fila del manifiesto debe tener survey_year"
print("Descarga 2022–2025: OK")
```

---

## Exploración inicial (L1)

Replique las ideas de la **Parte 3** del cuaderno individual L1 (Pasos 1–3 bastan para este ZIP, Pasos 4–5 del L1 individual son opcionales). Resuma con el manifiesto y mire **un** CSV de muestra (recomendado: **enero 2024** en `data/raw/2024/`).

### Paso 1 — Resumen desde `manifest.json`

```python
# SU CÓDIGO

```

**Comprobar:**

```python
assert len(manifest_df) >= 40
assert manifest_df["bytes_downloaded"].sum() > 0
print("Exploración L1, Paso 1 — manifiesto: OK")
```

---

### Paso 2 — Vista de un CSV de muestra

Elija **un** mes ya extraído. Cargue `Fuerza de trabajo.CSV` en un DataFrame y explorelo.

```python
# SU CÓDIGO

```

**Comprobar:**

```python
assert n_rows > 10_000, "Se espera un mes nacional"
assert "DPTO" in df.columns
print("Exploración L1, Paso 2 — CSV muestra: OK")
```

---

### Paso 3 — Gráfico del proceso de descarga

Cree un gráfico que nos permita analizar alguna dimension del proceso de descarga.

```python
# SU CÓDIGO

```

**Comprobar:**

```python
assert "survey_year" in manifest_df.columns
print("Exploración L1, Paso 3 — gráfico: OK")
```

---

# Parte B — Ética y OSM (L2)

**Tarea.** **Replicar en código** lo que ya hizo en el cuaderno individual L2, pero **a mayor escala** gracias a la Parte A: más años en disco y más departamentos en OSM.

| Parte individual L2 | Qué amplía el grupo (Parte A) |
|---------------------|-------------------------------|
| Parte 2 — cuasi-identificadores | Mismo análisis en **enero 2024** y repetición en **enero de otro año** (p. ej. 2023) descargado en Parte A |
| Parte 4 — OSM + enlace GEIH | Mismo código, pero **≥ 5 departamentos** en el CSV (L2 solo Nariño) |

Copie del [cuaderno individual L2](https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-big-data/l2-ethics-governance.ipynb):

| Qué copiar | Dónde está en L2 |
|------------|------------------|
| `CANDIDATOS_QI` + bloque `presentes` / `tabla_qi` | Parte 2 |
| `overpass_post`, `contar_nodos_amenity`, `PAUSA_SEG` | Repaso HTTP + Parte 4 |
| Merge edad `P6040` con `PERSON_KEYS` | Parte 1, Paso 5 |
| Agregado GEIH por `DPTO` + gráfico | Parte 4, Pasos 3–4 |

---

## Preparar `df` — enero 2024 con edad

**En este paso:** tenga un DataFrame `df` del mes **enero 2024** (`Fuerza de trabajo` + edad `P6040` unida con `merge` sobre `DIRECTORIO`, `HOGAR`, `ORDEN`).

Al terminar debe existir:

- `df` con columnas `DPTO` y `P6040`

```python
# SU CÓDIGO — cargar enero 2024 y merge con Características generales si hace falta

```

**Comprobar:**

```python
assert "DPTO" in df.columns and "P6040" in df.columns
print("Parte B — df listo: OK")
```

---

## Paso 1 — Cuasi-identificadores (replicar L2 Parte 2)

**En este paso:**

1. Copie de L2 Parte 2 la lista **`CANDIDATOS_QI`** y el código que arma **`tabla_qi`** (`columna`, `tipo`, `valores_unicos`) sobre su `df` de **enero 2024**.
2. **Ampliación (dataset más grande):** repita el mismo bloque con **enero de otro año** ya descargado en la Parte A (p. ej. `data/raw/2023/…`). Guarde `tabla_qi_2023` (o el año que elija) e imprima una comparación breve (p. ej. columnas en `presentes` que cambian o `valores_unicos` de `DPTO` / `MPIO`).

Al terminar debe existir:

- `tabla_qi` con al menos **cinco filas** y columnas `columna`, `tipo`, `valores_unicos`
- segunda tabla o impresión comparando **dos eneros** (2024 + otro año)

```python
# SU CÓDIGO

```

**Comprobar:**

```python
assert {"columna", "tipo", "valores_unicos"}.issubset(tabla_qi.columns)
assert len(tabla_qi) >= 5
assert "DPTO" in tabla_qi["columna"].values
try:
    _segunda = tabla_qi_2023
except NameError:
    try:
        _segunda = tabla_qi_otro_anio
    except NameError:
        _segunda = None
assert _segunda is not None and len(_segunda) >= 1, "Repita L2 Parte 2 para enero de otro año (p. ej. tabla_qi_2023)"
print("Parte B, Paso 1 — cuasi-identificadores (2 años): OK")
```

---

## Paso 2 — OSM por departamento (replicar L2 Parte 4, más departamentos)

**En este paso:**

1. Cree la carpeta `outputs/` si no existe.
2. Arme un diccionario **`DPTO_TO_OSM_RELATION`**: código DANE → id de **relación** OSM del departamento (`admin_level=4`). Ejemplo: Nariño `52` → relación **`1380130`** (área Overpass = `3600000000 + 1380130`). **No** use `120027` (es Colombia entera).
3. Para **cada** departamento del diccionario (mínimo **5**), consulte Overpass y guarde una fila en **`outputs/osm_poi_by_dpto.csv`** con:
   - `poi_school_count` — nodos `amenity=school`
   - `poi_health_count` — nodos con `amenity` en `hospital`, `clinic`, `doctors`, `pharmacy`, `health_centre`
   - `poi_servicios_basicos_count` — suma de las dos anteriores

**Pista:** Copie `contar_nodos_amenity` de L2 y llámela dos veces por departamento (escuela y cada tag de salud, o una consulta que usted defina). Pausa **`PAUSA_SEG`** entre departamentos. Empiece con 3 departamentos si el tiempo apremia.

Al terminar debe existir:

- `osm_path = Path("outputs/osm_poi_by_dpto.csv")` con ≥ 5 filas y las cuatro columnas de la tabla

```python
# SU CÓDIGO

```

**Comprobar:**

```python
assert osm_path.is_file()
assert len(osm_df) >= 5
assert {"dpto", "poi_school_count", "poi_health_count", "poi_servicios_basicos_count"}.issubset(osm_df.columns)
print("Parte B, Paso 2 — osm_poi_by_dpto.csv: OK")
```

---

## Paso 3 — Enlace GEIH + OSM (replicar L2 Parte 4, todos los DPTO del CSV)

**En este paso:**

1. Copie la lógica de L2 Parte 4 Pasos 3–4: cuente **personas en la muestra** por `DPTO` en `df` (enero 2024) → `personas_muestra`.
2. **`merge`** con `outputs/osm_poi_by_dpto.csv` por código de departamento → `enlace_df`.
3. Grafique (barras o scatter): `personas_muestra` vs `poi_servicios_basicos_count`.

**Pista:** Igual que en L2: enlace **ilustrativo**, no causal.

Al terminar debe existir:

- `enlace_df` con al menos 5 departamentos y columna `personas_muestra`
- un gráfico guardado o mostrado en el cuaderno

```python
# SU CÓDIGO

```

**Comprobar:**

```python
assert len(enlace_df) >= 5
assert "personas_muestra" in enlace_df.columns
print("Parte B, Paso 3 — enlace GEIH + OSM: OK")
```

---

## Registro de contribución (grupo)

Cada integrante añade **una línea** con tarea concreta (descarga, OSM, redacción, gráfico). Indique el **escriba de semana 1** en este cuaderno (consolidación del ZIP). La **rotación S1–S4** del liderazgo semanal va en el PDF (**§10**), no aquí.

```python
contribution_log = """
- Ana Pérez — bucle descarga 2023 y manifiesto
- Luis Gómez — Parte B Paso 2 OSM (5 departamentos)
- ...
Escriba semana 1: Ana Pérez
"""
print(contribution_log)
```

---

## Tarea grupal (Moodle)

ZIP **`week-1-<group_id>.zip`** hasta el **lunes 8 de junio de 2026, 23:59 (Colombia)**:

| Archivo | Descripción |
|---------|-------------|
| `notebook-week-1-group-<group_id>.ipynb` | Este cuaderno ejecutado (plantilla Colab: `week-1-group`) |
| `manifest.json` | Registro DANE (L1), en la raíz del ZIP |
| `outputs/osm_poi_by_dpto.csv` | POI OSM por departamento (L2; conservar carpeta `outputs/`) |

**Reflexión individual:** `week-1-reflection-<student>.pdf` el **martes 9 de junio de 2026, 23:59 (Colombia)** — plantilla [`reflection-week-1-template.docx`](/assets/documents/26-udenar-big-data/reflection-week-1-template.docx).

**Requerimientos del proyecto:** `project_requirements.pdf` en la **semana 2**.

<!-- end NOTEBOOK: -->
