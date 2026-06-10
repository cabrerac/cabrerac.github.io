---
course_code: 26-udenar-big-data
title: Data storage and management
description: Lecture 3 — store GEIH in partitioned Parquet, benchmark layout, and governance at write time. Individual run-only Colab; assessed code lives in week-2-group.
session: 3
start_time: 07:00 am
end_time: 01:00 pm
hours: 5
author: Christian Cabrera Jojoa
email: chc79@cam.ac.uk
position: Senior Research Associate and Affiliated Lecturer
department: Department of Computer Science and Technology
institution: University of Cambridge
layout: lecture
lecture_code: l3-storage
lecture_date: 13/06/2026
permalink: /teaching/26-udenar-big-data/l3-storage/
visible: false
group_notebook: week-2-group
notebook_language: es
notebook_title: Almacenamiento y gestión de datos
notebook_description: Práctica individual de la Lección 3. Harmonizar GEIH 2024 a Parquet particionado, benchmark de lectura y chequeo de gobernanza al almacenar.
---

<!-- SLIDES: -->

# Last Time

<!-- end SLIDES: -->

*Diapositivas L3 — por redactar (apertura: nube de palabras semana 1 + puente ETL).*

<!-- RENDER: -->

### Resources

- [Individual notebook Lecture 3](https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-big-data/l3-storage.ipynb) *(when published)*
- [Group notebook week 2](https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-big-data/week-2-group.ipynb) *(when published)*
- [Week 2 hub](/work-space/teaching/big-data/course/week-2/week-2-hub-es.md) · [Session plan PDF](/assets/documents/26-udenar-big-data/week-2-session-plan-es.pdf)
- [GEIH spine specification](/work-space/teaching/big-data/planning/spine-spec.md) (column names for harmonisation)
- [Reflection template week 2](/assets/documents/26-udenar-big-data/reflection-week-2-template.docx)

### References

- Armbrust, M., et al. (2021). *Lakehouse: A new generation of open platforms*. CIDR.
- Stonebraker, M., & Çetintemel, U. (2010). “One size fits all”: An idea whose time has come and gone. *DEABS*.

<!-- end RENDER: -->

<!-- NOTEBOOK: -->

## Repaso de Python para este cuaderno

Antes del laboratorio repasamos lo que usaremos en las Partes 0 a 5. Lea con calma, no es un curso completo de pandas.

### `Path` y carpetas

**`Path`** une rutas con **`/`**. **`mkdir(parents=True, exist_ok=True)`** crea la jerarquía si falta.

```python
from pathlib import Path

base = Path("data") / "processed" / "geih-spine"
base.mkdir(parents=True, exist_ok=True)
print(base.is_dir())
```

### Funciones reutilizables

Agrupamos pasos que repetimos (p. ej. harmonizar un mes). **`return`** devuelve el resultado.

```python
def mes_desde_periodo(periodo: int) -> tuple[int, int]:
    """PERIODO GEIH (20240101) → (año, mes)."""
    s = str(int(periodo))
    year = int(s[:4])
    mes = int(s[4:6])
    return year, mes

assert mes_desde_periodo(20240101) == (2024, 1)
print("Función mes_desde_periodo: OK")
```

### Unir tablas con `merge`

Igual que en L2: unimos **Fuerza de trabajo** con **Características generales** sobre las mismas claves de persona.

```python
import pandas as pd

PERSON_KEYS = ["DIRECTORIO", "HOGAR", "ORDEN"]
labour = pd.DataFrame(
    {"DIRECTORIO": [1], "HOGAR": [1], "ORDEN": [1], "P6240": [1]}
)
demog = pd.DataFrame(
    {"DIRECTORIO": [1], "HOGAR": [1], "ORDEN": [1], "P6040": [39]}
)
unido = labour.merge(demog, on=PERSON_KEYS, how="left")
assert unido["P6040"].iloc[0] == 39
print("merge: OK")
```

### Apilar meses con `concat`

Después de harmonizar cada mes por separado, a veces apilamos filas con **`concat`**.

```python
enero = pd.DataFrame({"mes": [1], "dpto": [52]})
febrero = pd.DataFrame({"mes": [2], "dpto": [11]})
dos_meses = pd.concat([enero, febrero], ignore_index=True)
assert len(dos_meses) == 2
print("concat: OK")
```

### Parquet: leer y escribir

**Parquet** es un formato columnar eficiente. Con **pandas** + **pyarrow**:

```python
ejemplo_dir = Path("outputs")
ejemplo_dir.mkdir(parents=True, exist_ok=True)
ruta = ejemplo_dir / "_ejemplo.parquet"

mini = pd.DataFrame({"dpto": [52, 11], "mes": [1, 1]})
mini.to_parquet(ruta, index=False)
recuperado = pd.read_parquet(ruta)
assert len(recuperado) == 2
print("Parquet lectura/escritura: OK")
ruta.unlink(missing_ok=True)
```

En la **Parte 4** usamos **`%%time`** al inicio de una celda para medir cuánto tarda una lectura grande.

### Comprobar con `assert`

Las celdas **Comprobar** validan resultados. Si fallan, corrija celdas anteriores.

```python
assert 2024 == 2024
print("Repaso Python L3: OK")
```

---

## Instrucciones

**Propósito.** Este cuaderno es su práctica de la **Lección 3 (Almacenamiento)**. Ya hicimos **Access** (L1) y ética sobre CSV (L2). Ahora **guardamos** GEIH en un formato analítico, eficiente y escalable: **Parquet particionado** (`year=…/mes=…/`).

**Qué hace el cuaderno (en orden).**

| Parte | Tema |
|-------|------|
| **0** | Access compacto: funciones L1 → **descargar GEIH 2024** en la sesión → OSM mínimo |
| **1** | Montar **Google Drive** y **copiar** lo descargado (no repetir DANE en cada sesión) |
| **2** | Función **`harmonize_month`** (mapeo al spine del curso) |
| **3** | **Harmonizar 12 meses 2024** → Parquet en Drive |
| **4** | **Benchmark**: leer todo el árbol vs una partición |
| **5** | **Gobernanza** al almacenar (retención, linaje) |

**Flujo en Colab (primera vez):** Parte 0 descarga en **`/content`** → Parte 1 guarda en **Drive** → Partes 2–5 leen desde Drive.

**Sesiones siguientes:** ejecute el **Paso 0.2** con **`SKIP_DOWNLOAD = True`** (solo define rutas; no descarga) → **Parte 1** monta Drive → Partes 2–5 leen desde Drive.

**Entregas semana 2:** ver sección **Tareas** al final (ZIP grupal martes · reflexión miércoles).

---

## Parte 0 — Solución compacta semana 1 (Access + descarga 2024)

En semana 1 su grupo implementó **`week-1-group`** (2022–2025). Aquí hacemos una **versión compacta** para el **proyecto final**: mismas funciones L1, pero descargamos solo **2024 completo** (12 meses), que es lo que harmonizamos en este cuaderno.

**Orden:** primero descargamos en la **carpeta de la sesión** (`/content` en Colab). En la **Parte 1** copiamos a **Google Drive** para no repetir la descarga.

### Paso 0.1 — Funciones Access (desde L1)

Estas funciones encapsulan: descargar ZIP → extraer CSV → registrar en `manifest.json`. Son el mismo diseño modular que vio en [L1](https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-big-data/l1-introduction.ipynb).

```python
import json
import re
import time
import zipfile
from pathlib import Path

import pandas as pd
import requests

CSV_SEP = ";"
CSV_ENCODING = "latin-1"
PRIMARY_TABLE_KEYWORD = "fuerza de trabajo"
DEMOG_TABLE_KEYWORDS = ("caracter", "generales")
PERSON_KEYS = ["DIRECTORIO", "HOGAR", "ORDEN"]

DOWNLOAD_ONCLICK_RE = re.compile(
    r"downloadFile\s*\(\s*['\"]([^'\"]+)['\"]\s*,\s*['\"]([^'\"]+)['\"]\s*\)"
)
FILE_ID_RE = re.compile(r"/download/(\d+)")


def download_zip(url: str, dest: Path, timeout: int = 600) -> tuple[float, int]:
    """Descarga url a dest; devuelve (segundos, bytes)."""
    t0 = time.perf_counter()
    with requests.get(url.strip(), stream=True, timeout=timeout) as resp:
        resp.raise_for_status()
        with dest.open("wb") as fh:
            for chunk in resp.iter_content(chunk_size=1 << 20):
                if chunk:
                    fh.write(chunk)
    elapsed = round(time.perf_counter() - t0, 3)
    if dest.read_bytes()[:2] != b"PK":
        raise ValueError("El archivo no es un ZIP válido.")
    return elapsed, dest.stat().st_size


def extract_csvs(zip_path: Path, dest_dir: Path) -> list[Path]:
    """Extrae CSV del ZIP mensual DANE (incluye csv.zip anidado si aplica)."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "r") as zf:
        names = zf.namelist()
        csv_members = [n for n in names if n.lower().endswith(".csv")]
        nested = next(
            (n for n in names if re.fullmatch(r"csv\s*\d*\.zip", Path(n).name, re.I)),
            None,
        )
        if nested and not csv_members:
            inner = dest_dir / "_csv_inner.zip"
            inner.write_bytes(zf.read(nested))
            try:
                return extract_csvs(inner, dest_dir)
            finally:
                inner.unlink(missing_ok=True)
        if not csv_members:
            raise ValueError(f"No hay CSV en {zip_path.name}")
        for name in csv_members:
            target = dest_dir / Path(name).name
            with zf.open(name) as src, target.open("wb") as dst:
                dst.write(src.read())
    return sorted(dest_dir.glob("*.CSV")) + sorted(dest_dir.glob("*.csv"))


def write_manifest(path: Path, entries: list[dict]) -> None:
    path.write_text(json.dumps(entries, indent=2, ensure_ascii=False), encoding="utf-8")


def list_catalog_downloads(catalog_id: int) -> list[dict]:
    """Lee get-microdata y devuelve file_id, filename, url por mes."""
    page_url = f"https://microdatos.dane.gov.co/index.php/catalog/{catalog_id}/get-microdata"
    resp = requests.get(page_url, timeout=120)
    resp.raise_for_status()
    seen: set[int] = set()
    files: list[dict] = []
    for filename, url in DOWNLOAD_ONCLICK_RE.findall(resp.text):
        m = FILE_ID_RE.search(url.strip())
        if not m:
            continue
        file_id = int(m.group(1))
        if file_id in seen:
            continue
        seen.add(file_id)
        files.append({"file_id": file_id, "filename": filename.strip(), "url": url.strip()})
    return sorted(files, key=lambda row: row["filename"].lower())


def access_file(item: dict, year_dir: Path, survey_year: int, catalog_id: int, *, skip_if_exists: bool = True) -> dict:
    """Descarga un mes si falta; si la carpeta CSV ya existe, omite la descarga."""
    filename = item["filename"]
    zip_path = year_dir / filename
    out_dir = year_dir / Path(filename).stem
    if skip_if_exists and out_dir.is_dir() and (list(out_dir.glob("*.CSV")) or list(out_dir.glob("*.csv"))):
        return {
            "method": "http",
            "survey_year": survey_year,
            "catalog_id": catalog_id,
            "file_id": item["file_id"],
            "filename": filename,
            "extract_dir": str(out_dir),
            "seconds": 0.0,
            "bytes_downloaded": zip_path.stat().st_size if zip_path.is_file() else 0,
            "notes": "omitido (ya extraído)",
        }
    seconds, nbytes = download_zip(item["url"], zip_path)
    n_csv = len(extract_csvs(zip_path, out_dir))
    return {
        "method": "http",
        "survey_year": survey_year,
        "catalog_id": catalog_id,
        "file_id": item["file_id"],
        "filename": filename,
        "extract_dir": str(out_dir),
        "seconds": seconds,
        "bytes_downloaded": nbytes,
        "notes": f"extracted {n_csv} CSVs",
    }


print("Parte 0 — funciones Access (L1): definidas")
```

**Comprobar:**

```python
assert callable(download_zip) and callable(access_file)
print("Parte 0, Paso 0.1 — funciones Access: OK")
```

---

### Paso 0.2 — Descargar GEIH 2024 completo (12 meses)

Usamos las funciones del paso anterior para dejar **todo 2024** bajo `data/raw/2024/` en la **carpeta de trabajo de esta sesión**. Cada mes queda en su subcarpeta con CSV extraídos, igual que en [L1 Parte 2](https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-big-data/l1-introduction.ipynb).

Si ya completó **`week-1-group`** y copió esos archivos a Drive, en la **Parte 1** puede cargar desde Drive y **omitir** este paso (`SKIP_DOWNLOAD = True`).

```python
YEAR = 2024
CATALOG_ID = 819
SKIP_DOWNLOAD = False  # True si ya tiene 12 meses en Drive (después de Parte 1)

SESSION_ROOT = Path(".")
LOCAL_RAW = SESSION_ROOT / "data" / "raw"
LOCAL_YEAR_DIR = LOCAL_RAW / str(YEAR)
LOCAL_MANIFEST = SESSION_ROOT / "manifest.json"
LOCAL_RAW.mkdir(parents=True, exist_ok=True)
LOCAL_YEAR_DIR.mkdir(parents=True, exist_ok=True)


def count_month_folders(year_dir: Path) -> int:
    if not year_dir.is_dir():
        return 0
    n = 0
    for p in year_dir.iterdir():
        if not p.is_dir():
            continue
        if any(f.suffix.upper() == ".CSV" for f in p.iterdir()):
            n += 1
    return n


n_meses_local = count_month_folders(LOCAL_YEAR_DIR)

if SKIP_DOWNLOAD:
    print("SKIP_DOWNLOAD=True — no se descarga en esta sesión.")
elif n_meses_local >= 12:
    print(f"Ya hay {n_meses_local} meses en {LOCAL_YEAR_DIR} — omitiendo descarga DANE.")
else:
    print("Listando archivos del catálogo 819...")
    all_files = list_catalog_downloads(CATALOG_ID)
    print(f"Archivos en catálogo: {len(all_files)}")
    manifest_entries: list[dict] = []
    for item in all_files:
        print("Procesando:", item["filename"])
        manifest_entries.append(
            access_file(item, LOCAL_YEAR_DIR, YEAR, CATALOG_ID, skip_if_exists=True)
        )
    write_manifest(LOCAL_MANIFEST, manifest_entries)
    total_gb = sum(e.get("bytes_downloaded", 0) for e in manifest_entries) / 1e9
    print(f"Manifiesto escrito: {LOCAL_MANIFEST}")
    print(f"Bytes descargados (suma ZIP): {total_gb:.3f} GB")

n_meses_local = count_month_folders(LOCAL_YEAR_DIR)
print(f"Carpetas mensuales 2024 en sesión: {n_meses_local}")
```

**Comprobar:**

```python
assert LOCAL_YEAR_DIR.is_dir()
assert n_meses_local >= 12, (
    f"Se esperan 12 meses 2024; hay {n_meses_local}. "
    "Revise la conexión DANE o use datos ya copiados desde week-1-group."
)
if LOCAL_MANIFEST.is_file():
    manifest_df = pd.DataFrame(json.loads(LOCAL_MANIFEST.read_text(encoding="utf-8")))
    print(manifest_df[["filename", "bytes_downloaded", "notes"]].head(3))
print("Parte 0, Paso 0.2 — descarga 2024: OK")
```

---

### Paso 0.3 — OSM compacto (desde L2 / week-1-group)

Patrón mínimo Overpass: contar POI por departamento. En el proyecto final puede ampliar a más `amenity` y más departamentos (como en **`week-1-group`**, ≥ 5).

```python
OVERPASS_URL = "https://overpass-api.de/api/interpreter"
OVERPASS_HEADERS = {"User-Agent": "UDENAR-BigData-course/2026 (contact: chc79@cam.ac.uk)"}


def overpass_post(query: str, timeout: int = 90) -> requests.Response:
    resp = requests.post(OVERPASS_URL, data={"data": query}, headers=OVERPASS_HEADERS, timeout=timeout)
    resp.raise_for_status()
    return resp


def contar_nodos_amenity(area_id: int, amenity: str, timeout: int = 90) -> int:
    query = f"""
[out:json][timeout:60];
area({area_id})->.a;
node["amenity"="{amenity}"](area.a);
out;
"""
    data = overpass_post(query, timeout=timeout).json()
    return len(data.get("elements", []))


# Ejemplo: Nariño (DANE 52) — relación OSM 1380130 → area 3601380130
DPTO_DEMO = 52
OSM_AREA_NARINO = 3600000000 + 1380130
PAUSA_SEG = 1.0

poi_escuelas = contar_nodos_amenity(OSM_AREA_NARINO, "school")
time.sleep(PAUSA_SEG)
print(f"DPTO {DPTO_DEMO}: amenity=school → {poi_escuelas} nodos")
```

**Comprobar:**

```python
assert poi_escuelas >= 0
print("Parte 0, Paso 0.3 — OSM compacto: OK")
```

Guarde este bloque (funciones Access + descarga + OSM) para el **proyecto final** — es la base del pipeline en `project_requirements.pdf` §9.

---

## Parte 1 — Google Drive: persistir lo descargado

En Colab, **`/content`** se borra al cerrar la sesión. Por eso, **después de descargar en la Parte 0**, copiamos `data/raw/2024/` y `manifest.json` a **Google Drive**. En la próxima sesión montamos Drive y continuamos sin volver a pedir los ZIP al DANE.

### Paso 1.1 — Montar Drive (solo Colab)

Si trabaja en **local**, deje `USE_GOOGLE_DRIVE = False`: `WORK_ROOT` será la carpeta del proyecto (donde ya descargó en el Paso 0.2).

```python
import shutil

USE_GOOGLE_DRIVE = True

try:
    import google.colab  # noqa: F401
    IN_COLAB = True
except ImportError:
    IN_COLAB = False

if USE_GOOGLE_DRIVE and IN_COLAB:
    from google.colab import drive

    drive.mount("/content/drive")
    WORK_ROOT = Path("/content/drive/MyDrive/UDENAR-BigData")
    print(f"Raíz persistente en Drive: {WORK_ROOT}")
else:
    WORK_ROOT = SESSION_ROOT
    print(f"Raíz local (misma sesión): {WORK_ROOT.resolve()}")

WORK_ROOT.mkdir(parents=True, exist_ok=True)
```

### Paso 1.2 — Rutas de trabajo en Drive (o local)

A partir de aquí, **Partes 2–5** leen y escriben bajo `WORK_ROOT`:

| Ruta | Contenido |
|------|-----------|
| `data/raw/2024/` | CSV descargados (Parte 0 → copiados aquí) |
| `data/processed/geih-spine/` | Parquet harmonizado |
| `manifest.json` | Registro de acceso DANE |
| `outputs/` | Exportaciones auxiliares |

```python
RAW_DIR = WORK_ROOT / "data" / "raw"
PROCESSED_DIR = WORK_ROOT / "data" / "processed" / "geih-spine"
OUTPUTS_DIR = WORK_ROOT / "outputs"
MANIFEST_PATH = WORK_ROOT / "manifest.json"

for p in (RAW_DIR, PROCESSED_DIR, OUTPUTS_DIR):
    p.mkdir(parents=True, exist_ok=True)

YEAR_DIR = RAW_DIR / str(YEAR)
YEAR_DIR.mkdir(parents=True, exist_ok=True)

print("RAW:", YEAR_DIR)
print("Parquet:", PROCESSED_DIR)
print("Manifiesto:", MANIFEST_PATH)
```

### Paso 1.3 — Copiar la descarga de la sesión → Drive (una vez)

Si acaba de ejecutar el **Paso 0.2**, los CSV están en `LOCAL_YEAR_DIR` (`/content/data/raw/2024`). Esta celda los **copia a Drive** si allí aún no están los 12 meses.

En **sesiones futuras**, Drive ya tiene los datos: esta celda imprime *omitido* y usted puede poner **`SKIP_DOWNLOAD = True`** en el Paso 0.2.

```python
n_drive = count_month_folders(YEAR_DIR)
n_local = count_month_folders(LOCAL_YEAR_DIR)

if n_drive >= 12:
    print(f"Drive ya tiene {n_drive} meses — no hace falta copiar.")
elif n_local >= 12:
    print(f"Copiando {n_local} meses de la sesión → Drive (puede tardar)...")
    for item in LOCAL_YEAR_DIR.iterdir():
        dest = YEAR_DIR / item.name
        if item.is_dir():
            shutil.copytree(item, dest, dirs_exist_ok=True)
        elif item.is_file():
            shutil.copy2(item, dest)
    if LOCAL_MANIFEST.is_file() and not MANIFEST_PATH.is_file():
        shutil.copy2(LOCAL_MANIFEST, MANIFEST_PATH)
    print("Copia a Drive terminada.")
else:
    raise FileNotFoundError(
        "Faltan meses en local y en Drive. Ejecute el Paso 0.2 (descarga) primero."
    )

print(f"Meses en Drive al final: {count_month_folders(YEAR_DIR)}")
```

**Comprobar:**

```python
assert count_month_folders(YEAR_DIR) >= 12
assert WORK_ROOT.is_dir()
print("Parte 1 — Drive / persistencia: OK")
```

---

## Parte 2 — Función `harmonize_month`

**Objetivo.** Definir constantes y la función que convierte **un mes** de CSV DANE en filas con nombres del [spine del curso](https://cabrerac.github.io/work-space/teaching/big-data/planning/spine-spec.md). Harmonizamos **los 12 meses de 2024** en este cuaderno; en **`week-2-group`** su grupo añade **2022, 2023 y 2025** con el mismo mapeo.

Instale **PyArrow** (motor Parquet en pandas):

```python
%pip install -q pyarrow
```

```python
HARMONISATION_VERSION = "2026-06-l3-demo"
SOURCE_CATALOG = str(CATALOG_ID)

# Códigos P6240 — ver diccionario DANE; valor 1 = ocupado en muchos meses 2024
EMPLOYED_P6240_VALUES = {1}


def _labour_csv(month_dir: Path) -> Path:
    return next(
        p for p in month_dir.glob("*.CSV")
        if PRIMARY_TABLE_KEYWORD in p.name.lower().replace("\xa0", " ")
    )


def _demog_csv(month_dir: Path) -> Path:
    return next(
        p for p in month_dir.glob("*.CSV")
        if all(kw in p.name.lower().replace("\xa0", " ") for kw in DEMOG_TABLE_KEYWORDS)
    )


def harmonize_month(month_dir: Path) -> pd.DataFrame:
    """
    Lee Fuerza de trabajo + Características de un mes, une por PERSON_KEYS,
    renombra columnas al esquema del curso y añade linaje.
    """
    labour_path = _labour_csv(month_dir)
    demog_path = _demog_csv(month_dir)

    labour = pd.read_csv(labour_path, sep=CSV_SEP, encoding=CSV_ENCODING, low_memory=False)
    demog = pd.read_csv(
        demog_path,
        sep=CSV_SEP,
        encoding=CSV_ENCODING,
        usecols=PERSON_KEYS + ["P6040", "P3271"],
        low_memory=False,
    )
    merged = labour.merge(demog, on=PERSON_KEYS, how="left", validate="many_to_one")

    if "PERIODO" not in merged.columns:
        raise KeyError(f"Falta PERIODO en {labour_path.name}")

    period = merged["PERIODO"].astype(int)
    year = (period // 10000).astype(int)
    mes = ((period // 100) % 100).astype(int)

    out = pd.DataFrame(
        {
            "period": (year * 100 + mes).astype(int),
            "year": year,
            "mes": mes,
            "household_id": merged["DIRECTORIO"].astype(str) + "-" + merged["HOGAR"].astype(str),
            "person_order": merged["ORDEN"].astype(int),
            "dpto": merged["DPTO"].astype(int),
            "area": merged["AREA"].astype(int),
            "age": pd.to_numeric(merged["P6040"], errors="coerce"),
            "sex": pd.to_numeric(merged["P3271"], errors="coerce"),
            "lf_status": pd.to_numeric(merged.get("P6240"), errors="coerce"),
            "expansion_weight": pd.to_numeric(merged["FEX_C18"], errors="coerce"),
            "is_employed": merged["P6240"].isin(EMPLOYED_P6240_VALUES),
            "source_catalog": SOURCE_CATALOG,
            "harmonisation_version": HARMONISATION_VERSION,
        }
    )
    return out


print("harmonize_month() lista")
```

**Comprobar:**

```python
assert callable(harmonize_month)
print("Parte 2 — configuración harmonización: OK")
```

---

## Parte 3 — Escribir Parquet particionado (2024 completo)

**Objetivo.** Recorrer cada carpeta mensual en `data/raw/2024/`, harmonizar y escribir **`year=2024/mes=MM/part-000.parquet`**. Si ya existe el árbol en Drive, puede **omitir** la re-escritura (`SKIP_IF_PARQUET_EXISTS`).

```python
SKIP_IF_PARQUET_EXISTS = True

month_dirs = sorted(
    p for p in YEAR_DIR.iterdir()
    if p.is_dir() and list(p.glob("*.CSV"))
)
if not month_dirs:
    raise FileNotFoundError(
        f"No hay CSV bajo {YEAR_DIR}. Monte Drive (Parte 1) o complete week-1-group."
    )

partition_stats: list[dict] = []

for month_dir in month_dirs:
    sample = harmonize_month(month_dir)
    y = int(sample["year"].iloc[0])
    m = int(sample["mes"].iloc[0])
    part_dir = PROCESSED_DIR / f"year={y}" / f"mes={m:02d}"
    part_file = part_dir / "part-000.parquet"

    if SKIP_IF_PARQUET_EXISTS and part_file.is_file():
        print(f"Omitido (ya existe): {part_file.relative_to(WORK_ROOT)}")
        n_rows = len(pd.read_parquet(part_file, columns=["dpto"]))
    else:
        part_dir.mkdir(parents=True, exist_ok=True)
        sample.to_parquet(part_file, index=False)
        n_rows = len(sample)
        print(f"Escrito {part_file.relative_to(WORK_ROOT)} | filas: {n_rows:,}")

    partition_stats.append({"year": y, "mes": m, "rows": n_rows, "path": str(part_file)})

stats_df = pd.DataFrame(partition_stats).sort_values(["year", "mes"])
print("\nResumen particiones 2024:")
print(stats_df.to_string(index=False))
print(f"Total filas: {stats_df['rows'].sum():,}")
```

**Comprobar:**

```python
assert len(stats_df) >= 12, f"Se esperan 12 meses 2024; hay {len(stats_df)}"
assert stats_df["rows"].sum() > 100_000
assert (PROCESSED_DIR / "year=2024" / "mes=01" / "part-000.parquet").is_file()
print("Parte 3 — Parquet 2024 completo: OK")
```

---

## Parte 4 — Benchmark: todo el árbol vs una partición

**Objetivo.** Medir **tiempo** (y memoria aproximada) al leer **todas** las particiones de 2024 frente a leer **solo enero**. La diferencia ilustra por qué particionamos antes de elegir motor en L4.

### Paso 4.1 — Leer todo `year=2024`

Ejecute la celda siguiente. **`%%time`** reporta el tiempo al final.

```python
%%time
df_full = pd.read_parquet(PROCESSED_DIR / "year=2024")
rows_full = len(df_full)
mem_full_mb = df_full.memory_usage(deep=True).sum() / 1e6
print(f"Filas (árbol completo 2024): {rows_full:,}")
print(f"Memoria aprox. DataFrame: {mem_full_mb:.1f} MB")
del df_full
```

### Paso 4.2 — Leer una sola partición (`mes=01`)

```python
%%time
df_one = pd.read_parquet(PROCESSED_DIR / "year=2024" / "mes=01" / "part-000.parquet")
rows_one = len(df_one)
mem_one_mb = df_one.memory_usage(deep=True).sum() / 1e6
print(f"Filas (solo enero): {rows_one:,}")
print(f"Memoria aprox. DataFrame: {mem_one_mb:.1f} MB")
del df_one
```

**Interpretación.** Si solo necesita enero, leer **`mes=01`** evita cargar los otros once meses. Eso es **podar por partición** (layout en disco), no un algoritmo más rápido. En L4 veremos motores que aprovechan esto automáticamente.

**Comprobar:**

```python
assert rows_full > rows_one
assert rows_one > 10_000
print("Parte 4 — benchmark particiones: OK")
```

---

## Parte 5 — Gobernanza al almacenar

**Objetivo.** Documentar qué **persistimos** en Parquet, qué sigue siendo sensible y qué regla de retención aplicará su grupo (enlace L2 / Dwork / lecturas semana 2).

### Paso 5.1 — Cuasi-identificadores en el archivo harmonizado

```python
sample_path = PROCESSED_DIR / "year=2024" / "mes=01" / "part-000.parquet"
schema_cols = pd.read_parquet(sample_path).columns.tolist()

QI_EN_PARQUET = [
    ("household_id", "Clave compuesta hogar — no publicar en agregados finos"),
    ("dpto", "Geografía departamental"),
    ("area", "Estrato urbano/rural"),
    ("age", "Edad en años"),
    ("sex", "Sexo"),
]
tabla_store = pd.DataFrame(QI_EN_PARQUET, columns=["columna", "nota_riesgo"])
print("Columnas sensibles que **guardamos** (microdato interno):")
print(tabla_store.to_string(index=False))
```

### Paso 5.2 — Regla de retención (plantilla)

Copie y adapte en su Word de requerimientos (§7) y en **`week-2-group`** Parte A4.

```python
RETENTION_RULE = (
    "Conservamos Parquet harmonizado en Drive del grupo solo para el curso y el proyecto; "
    "no publicamos microfilas ni particiones crudas; agregados externos con k≥5 ocupados."
)
LINEAGE = {
    "source_catalog": SOURCE_CATALOG,
    "harmonisation_version": HARMONISATION_VERSION,
    "raw_path": str(YEAR_DIR),
    "processed_path": str(PROCESSED_DIR),
}
print("Regla de retención:\n ", RETENTION_RULE)
print("\nLinaje (metadatos):")
for k, v in LINEAGE.items():
    print(f"  {k}: {v}")
```

**Comprobar:**

```python
assert len(RETENTION_RULE) > 40
assert LINEAGE["source_catalog"] == "819"
print("Parte 5 — gobernanza al almacenar: OK")
```

---

## Puente al cuaderno grupal

En el cuaderno **`week-2-group`** (Parte A) su grupo:

1. Harmoniza **2022–2025** reutilizando **`harmonize_month`** (mismo mapeo).
2. Repite el benchmark de la Parte 4 sobre el árbol completo.
3. Documenta **elección de partición** y ética de retención.
4. Continúa en Parte B (L4) con consultas y privacidad k=5.

Entrega Moodle **martes 16 jun 2026**: ZIP con cuaderno ejecutado + `manifest.json` (sin archivos de datos).

---

## Tareas

Plantillas y plazos en el [hub semana 2](/work-space/teaching/big-data/course/week-2/week-2-hub-es.md) y en la [página L4](/teaching/26-udenar-big-data/l4-processing/) *(cuando esté visible)*.

### Cuaderno individual (este archivo)

Ejecute **Partes 0–5** antes del sábado 13 jun. No hay entrega separada de este cuaderno.

### Trabajo en grupo (semana 2)

Colab **`week-2-group`**. ZIP **`week-2-<group_id>.zip`** hasta el **martes 16 de junio de 2026, 23:59 (Colombia)**:

| Archivo en el ZIP | Descripción |
|-------------------|-------------|
| `week-2-group-<group_id>.ipynb` | Cuaderno grupal ejecutado |
| `manifest.json` | Conteos y metadatos (sin CSV ni Parquet) |

### Reflexión individual

PDF **`week-2-reflection-<student>.pdf`** hasta el **miércoles 17 de junio de 2026**. Plantilla: [reflection-week-2-template.docx](/assets/documents/26-udenar-big-data/reflection-week-2-template.docx).

### Requerimientos del proyecto

Avance en Word durante el **sábado 13 jun** (checkpoint: **§5 subconjunto GEIH definido**). El PDF **`project_requirements.pdf`** se entrega con el **proyecto summativo (27 jun 2026)**.

<!-- end NOTEBOOK: -->
