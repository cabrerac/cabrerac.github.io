---
course_code: 26-udenar-big-data
title: Data storage and management
description: Lecture 3. Store GEIH in partitioned Parquet, benchmark layout, and governance at write time. Individual run-only Colab. Assessed code lives in week-2-group.
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
notebook_description: Práctica individual de la Lección 3. En esta práctica harmonizamos el dataset GEIH para el año 2024 en formato Parquet particionado para hacer su acceso más eficiente. Comparamos el impacto de dicha harmonización y realizamos un chequeo de gobernanza al almacenar los datos.
---

<!-- SLIDES: -->

# Last Time

<!-- end SLIDES: -->

*Diapositivas Lección 3, por redactar (apertura: nube de palabras semana 1 + puente ETL).*

<!-- RENDER: -->

### Resources

- [Individual notebook Lecture 3](https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-big-data/l3-storage.ipynb) *(when published)*
- [Group notebook week 2](https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-big-data/week-2-group.ipynb) *(when published)*
- [Week 2 hub](/work-space/teaching/big-data/course/week-2/week-2-hub-es.md) · [Session plan PDF](/assets/documents/26-udenar-big-data/week-2-session-plan-es.pdf)
- [Reflection template week 2](/assets/documents/26-udenar-big-data/reflection-week-2-template.docx)

### References

- Armbrust, M., et al. (2021). *Lakehouse: A new generation of open platforms*. CIDR.
- Stonebraker, M., & Çetintemel, U. (2010). “One size fits all”: An idea whose time has come and gone. *DEABS*.

<!-- end RENDER: -->

<!-- NOTEBOOK: -->

## Repaso de Python para este cuaderno

Antes del laboratorio repasamos lo que usaremos en las Partes 0 a 5. Lea con calma, no es un curso completo de pandas.

### `Path` y carpetas

**`Path`** sirve para manejar **rutas de archivos y carpetas** en Python. Permite unir rutas usando **`/`** y facilita operaciones como crear carpetas: **`mkdir(parents=True, exist_ok=True)`** crea toda la jerarquía de carpetas si no existe.

Primero importamos y definimos la ruta:

```python
from pathlib import Path

base = Path("data") / "processed" / "geih-spine"
print("Ruta objetivo:", base)
```

Después de definir la ruta, la creamos en disco y comprobamos que es una carpeta:

```python
base.mkdir(parents=True, exist_ok=True)
print("¿Es carpeta?", base.is_dir())
assert base.is_dir()
print("Path y carpetas: OK")
```

### Funciones reutilizables

Las funciones sirven para agrupar pasos que repetimos (p. ej. harmonizar un mes). LAs funciones retornan una salida utilizando la palabra clave **`return`** devuelve el resultado.

A continuacion definimos una función que convierte el código **`PERIODO`** de GEIH en año y mes.

```python
def mes_desde_periodo(periodo: int) -> tuple[int, int]:
    """PERIODO GEIH (20240101) → (año, mes)."""
    s = str(int(periodo))
    year = int(s[:4])
    mes = int(s[4:6])
    return year, mes
```

Después de definir la función, la llamamos con enero 2024 y mostramos el resultado:

```python
year, mes = mes_desde_periodo(20240101)
print(f"Año: {year}, mes: {mes}")
assert (year, mes) == (2024, 1)
print("Función mes_desde_periodo: OK")
```

### Unir tablas con `merge`

Como miramos en el anterior laboratorio, podemos unir DataFrames utilizando la función **merge**. En este caso unimos **Fuerza de trabajo** con **Características generales** sobre las claves de persona.

Importamos pandas y definimos las claves de unión:

```python
import pandas as pd

PERSON_KEYS = ["DIRECTORIO", "HOGAR", "ORDEN"]
print("Claves de unión:", PERSON_KEYS)
```

Creamos dos tablas de ejemplo a partir de un diccionario de Python. Una de fuerza de trabajo y otra demográfica:

```python
labour = pd.DataFrame(
    {"DIRECTORIO": [1], "HOGAR": [1], "ORDEN": [1], "P6240": [1]}
)
demog = pd.DataFrame(
    {"DIRECTORIO": [1], "HOGAR": [1], "ORDEN": [1], "P6040": [39]}
)
print("Fuerza de trabajo:")
print(labour)
print("\nCaracterísticas generales:")
print(demog)
```

Después unimos con **`merge`**. El argumento `how="left"` indica que queremos una **unión izquierda**: todas las filas de la tabla izquierda (`labour`) se mantienen, y se añaden las columnas de la derecha (`demog`) solo si hay coincidencia en las claves. Así, si una persona está en `labour` pero no en `demog`, su fila igual aparece pero con valores vacíos en esas columnas. Revisamos el resultado:

```python
unido = labour.merge(demog, on=PERSON_KEYS, how="left")
print("Tabla unida:")
print(unido)
assert unido["P6040"].iloc[0] == 39
print("merge: OK")
```

### Apilar meses con `concat`

Después de descargar o manipular cada mes por separado, podemos concatenar filas con la función **`concat`** de `pandas`.

```python
enero = pd.DataFrame({"mes": [1], "dpto": [52]})
febrero = pd.DataFrame({"mes": [2], "dpto": [11]})
print("Enero:\n", enero)
print("Febrero:\n", febrero)
```

Concatenamos las filas y mostramos el resultado:

```python
dos_meses = pd.concat([enero, febrero], ignore_index=True)
print("Dos meses apilados:")
print(dos_meses)
assert len(dos_meses) == 2
print("concat: OK")
```

### Parquet: leer y escribir

**Parquet** es un formato basado en columnas que se utiliza para almacenar datos y hacer su consulta más eficiente. Podemos manipular archivos **Parquet** con **pandas** y **pyarrow**:

Preparamos la carpeta y el DataFrame de ejemplo:

```python
ejemplo_dir = Path("outputs")
ejemplo_dir.mkdir(parents=True, exist_ok=True)
ruta = ejemplo_dir / "_ejemplo.parquet"

mini = pd.DataFrame({"dpto": [52, 11], "mes": [1, 1]})
print("DataFrame a guardar:")
print(mini)
```

Escribimos, leemos de vuelta y comparamos:

```python
mini.to_parquet(ruta, index=False)
recuperado = pd.read_parquet(ruta)
print("Leído desde Parquet:")
print(recuperado)
assert len(recuperado) == 2
print("Parquet lectura/escritura: OK")
ruta.unlink(missing_ok=True)
```

---

## Instrucciones

**Propósito.** Este cuaderno es su práctica de la **Lección 3 (Almacenamiento)**. Ya hicimos **Access** en la lección 1 y evaluamos aspectos éticos y de privacidad de datos en la lección 2. Ahora **guardamos** GEIH en un formato eficiente y escalable: **Parquet particionado** (`anio=…/mes=…/`).

**Qué hace el cuaderno (en orden).**

| Parte | Tema |
|-------|------|
| **0** | **Solución** del deber grupal semana 1 (`week-1-group`): Parte A (Access **2022–2025**) + Parte B (ética + OSM) |
| **1** | Montar **Google Drive** y **copiar** lo descargado (no repetir DANE en cada sesión) |
| **2** | Función **`harmonize_month`** (unir tablas + nombres legibles + claves de partición) |
| **3** | **Harmonizar 12 meses 2024** → Parquet en Drive |
| **4** | **Benchmark**: leer todo el árbol vs una partición |
| **5** | **Gobernanza** al almacenar (retención, linaje) |

La Parte 0 puede ser ejecutada con **`SKIP_DOWNLOAD = True`** (solo rutas, sin descarga del dataset de DANE) → Parte 1 monta Drive → Partes 2–5 continúan.

**Entregas semana 2:** ver sección **Tareas** al final (ZIP grupal martes · reflexión miércoles).

---

## Parte 0. Solución del cuaderno grupal de la semana 1

Este bloque es la **solución** para el cuaderno grupal de la semana 1. Sirve para que ustedes comparen sus soluciones y de referencia para el **proyecto final**.

| Paso | Corresponde a | Entregable clave del grupal |
|------|---------------|----------------------------|
| **0.1** | Parte A (lección 1 a escala) | `manifest.json` + CSV **2022–2025** |
| **0.2** | Parte B (lección 2 a escala) | `outputs/osm_poi_by_dpto.csv` + enlace GEIH + gráfico |

Con **`SKIP_DOWNLOAD = True`** en el Paso 0.1, solo se comprueban rutas si los años ya están en disco.

**Orden:** los CSV quedan en **`/content/data/raw/`**. En la **Parte 1** copiamos todo el árbol a **Google Drive** para no repetir la descarga. Las **Partes 2–5** harmonizan y guardan **solo 2024**.

### Paso 0.1. Bloque compacto: Parte A — Access + descarga 2022–2025

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

# El DANE genera el botón de descarga con onclick="mostrarModal('archivo.zip', 'URL')".
# Aceptamos también downloadFile(...) por si cambia el nombre de la función.
DOWNLOAD_ONCLICK_RE = re.compile(
    r"(?:mostrarModal|downloadFile)\s*\(\s*['\"]([^'\"]+)['\"]\s*,\s*['\"]([^'\"]+)['\"]\s*\)"
)
FILE_ID_RE = re.compile(r"/download/(\d+)")

# Catálogos DANE del spine del curso (igual que week-1-group)
SPINE_CATALOGS: dict[int, int] = {
    2022: 771,
    2023: 782,
    2024: 819,
    2025: 853,
}
YEAR = 2024  # año que harmonizamos en este cuaderno (Partes 2–3)

SKIP_DOWNLOAD = False  # True si ya tiene los años en disco

SESSION_ROOT = Path(".")
LOCAL_RAW = SESSION_ROOT / "data" / "raw"
LOCAL_YEAR_DIR = LOCAL_RAW / str(YEAR)
LOCAL_MANIFEST = SESSION_ROOT / "manifest.json"
LOCAL_RAW.mkdir(parents=True, exist_ok=True)


def download_zip(url: str, dest: Path, timeout: int = 600) -> tuple[float, int]:
    """Descarga url a dest. Devuelve (segundos, bytes)."""
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
    """Descarga un mes si falta. Si la carpeta CSV ya existe, omite la descarga."""
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
meses_por_anio = {y: count_month_folders(LOCAL_RAW / str(y)) for y in SPINE_CATALOGS}

if SKIP_DOWNLOAD:
    print("SKIP_DOWNLOAD=True, no se descarga en esta sesión.")
else:
    manifest_entries: list[dict] = []
    for survey_year, catalog_id in SPINE_CATALOGS.items():
        year_dir = LOCAL_RAW / str(survey_year)
        year_dir.mkdir(parents=True, exist_ok=True)
        n_meses_anio = count_month_folders(year_dir)
        if n_meses_anio >= 12:
            print(f"Año {survey_year}: ya hay {n_meses_anio} meses, omitiendo catálogo {catalog_id}.")
            continue
        print(f"Catálogo {catalog_id}, año {survey_year}...")
        all_files = list_catalog_downloads(catalog_id)
        print(f"  Archivos en catálogo: {len(all_files)}")
        for item in all_files:
            print("  Procesando:", item["filename"])
            manifest_entries.append(
                access_file(item, year_dir, survey_year, catalog_id, skip_if_exists=True)
            )
    if manifest_entries:
        write_manifest(LOCAL_MANIFEST, manifest_entries)
        total_gb = sum(e.get("bytes_downloaded", 0) for e in manifest_entries) / 1e9
        print(f"Manifiesto escrito: {LOCAL_MANIFEST}")
        print(f"Bytes descargados en esta ejecución (suma ZIP): {total_gb:.3f} GB")
    else:
        print("Nada nuevo que descargar. Manifiesto existente se conserva si ya estaba en disco.")

n_meses_local = count_month_folders(LOCAL_YEAR_DIR)
meses_por_anio = {y: count_month_folders(LOCAL_RAW / str(y)) for y in SPINE_CATALOGS}
print("Meses por año en sesión:", meses_por_anio)
print("Parte 0, bloque compacto Access 2022–2025: ejecutado")
```

**Comprobar:**

```python
print(f"Meses 2024 en sesión: {n_meses_local}")
print("Meses por año:", meses_por_anio)
assert LOCAL_YEAR_DIR.is_dir()
assert n_meses_local >= 12, (
    f"Se esperan 12 meses 2024. Hay {n_meses_local}. "
    "Ejecute el bloque con SKIP_DOWNLOAD=False o copie datos desde week-1-group / Drive."
)
if LOCAL_MANIFEST.is_file():
    manifest_df = pd.DataFrame(json.loads(LOCAL_MANIFEST.read_text(encoding="utf-8")))
    print(f"Filas en manifiesto: {len(manifest_df)}")
    print(manifest_df[["survey_year", "filename", "bytes_downloaded", "notes"]].head(3))
    assert "survey_year" in manifest_df.columns
    assert len(manifest_df) >= 40, "Se esperan ~48 filas (12 meses × 4 años) en la solución completa."
print("Parte 0, Paso 0.1, Access 2022–2025: OK")
```

---

### Paso 0.2. Bloque compacto: Parte B — cuasi-identificadores + OSM + enlace GEIH

Solución de la **Parte B** del cuaderno grupal: carga enero **2024** y **2023**, tabla de cuasi-identificadores en ambos años, consulta Overpass en **cinco departamentos**, guarda **`outputs/osm_poi_by_dpto.csv`** y enlaza con la muestra GEIH.

Requiere haber ejecutado el **Paso 0.1** (o tener los CSV en `LOCAL_RAW`).

```python
import matplotlib.pyplot as plt

OVERPASS_HEADERS = {
    "User-Agent": "UDENAR-BigData-2026/1.0 (Universidad de Narino - Big Data elective)",
    "Accept": "application/json",
}
OVERPASS_ENDPOINTS = [
    "https://overpass.kumi.systems/api/interpreter",
    "https://overpass-api.de/api/interpreter",
]
OVERPASS_RETRY_PAUSE = 2.0
PAUSA_SEG = 1.0
HEALTH_AMENITIES = ("hospital", "clinic", "doctors", "pharmacy", "health_centre")

CANDIDATOS_QI = [
    "DPTO",
    "MPIO",
    "AREA",
    "P6040",
    "P6020",
    "SEXO",
    "P6160",
    "P6240",
    "P6090",
    "PER",
]

# Código DANE → relación OSM (admin_level=4). No use 120027 (Colombia entera).
DPTO_TO_OSM_RELATION: dict[int, str] = {
    5: "Antioquia",
    8: "Atlántico",
    11: "Bogotá D.C.",
    52: "Nariño",
    76: "Valle del Cauca",
}
DPTO_TO_OSM_RELATION_IDS: dict[int, int] = {
    5: 119496,
    8: 1387796,
    11: 1387966,
    52: 1380130,
    76: 119827,
}

LOCAL_OUTPUTS = SESSION_ROOT / "outputs"
LOCAL_OUTPUTS.mkdir(parents=True, exist_ok=True)


def overpass_post(query: str, *, timeout: int = 90) -> requests.Response:
    last_resp = None
    for url in OVERPASS_ENDPOINTS:
        for intento in range(2):
            try:
                r = requests.post(
                    url,
                    data={"data": query},
                    headers=OVERPASS_HEADERS,
                    timeout=timeout,
                )
                last_resp = r
                if r.status_code == 200:
                    return r
                if r.status_code in (429, 502, 503, 504):
                    time.sleep(OVERPASS_RETRY_PAUSE + intento)
                    continue
                r.raise_for_status()
            except requests.Timeout:
                time.sleep(OVERPASS_RETRY_PAUSE + intento)
                continue
    if last_resp is not None:
        last_resp.raise_for_status()
    raise requests.HTTPError("Overpass: sin respuesta útil tras reintentos.")


def contar_nodos_amenity(area_id: int, amenity: str, timeout: int = 90) -> int:
    query = f"""
[out:json][timeout:60];
area({area_id})->.a;
node["amenity"="{amenity}"](area.a);
out;
"""
    data = overpass_post(query, timeout=timeout).json()
    return len(data.get("elements", []))


def contar_salud(area_id: int) -> int:
    total = 0
    for tag in HEALTH_AMENITIES:
        total += contar_nodos_amenity(area_id, tag)
        time.sleep(0.5)
    return total


def find_enero_dir(survey_year: int) -> Path:
    year_dir = LOCAL_RAW / str(survey_year)
    for p in sorted(year_dir.iterdir()):
        if p.is_dir() and p.name.lower().startswith("ene"):
            return p
    raise FileNotFoundError(f"No hay carpeta de enero bajo {year_dir}")


def load_mes_con_edad(survey_year: int) -> pd.DataFrame:
    month_dir = find_enero_dir(survey_year)
    csv_files = list(month_dir.glob("*.CSV")) + list(month_dir.glob("*.csv"))
    labour_path = next(
        p for p in csv_files
        if PRIMARY_TABLE_KEYWORD in p.name.lower().replace("\xa0", " ")
    )
    demog_path = next(
        p for p in csv_files
        if all(kw in p.name.lower().replace("\xa0", " ") for kw in DEMOG_TABLE_KEYWORDS)
    )
    labour = pd.read_csv(labour_path, sep=CSV_SEP, encoding=CSV_ENCODING, low_memory=False)
    demog = pd.read_csv(
        demog_path,
        sep=CSV_SEP,
        encoding=CSV_ENCODING,
        usecols=PERSON_KEYS + ["P6040"],
        low_memory=False,
    )
    return labour.merge(demog, on=PERSON_KEYS, how="left", validate="many_to_one")


def tabla_cuasi_identificadores(frame: pd.DataFrame) -> pd.DataFrame:
    presentes = [c for c in CANDIDATOS_QI if c in frame.columns]
    return pd.DataFrame(
        {
            "columna": presentes,
            "tipo": [str(frame[c].dtype) for c in presentes],
            "valores_unicos": [frame[c].nunique(dropna=False) for c in presentes],
        }
    )


# --- enero 2024 + cuasi-identificadores (L2 Parte 2, dos años) ---
df = load_mes_con_edad(2024)
tabla_qi = tabla_cuasi_identificadores(df)
print("Cuasi-identificadores enero 2024:")
print(tabla_qi.to_string(index=False))

df_2023 = load_mes_con_edad(2023)
tabla_qi_2023 = tabla_cuasi_identificadores(df_2023)
print("\nCuasi-identificadores enero 2023:")
print(tabla_qi_2023.to_string(index=False))

qi_2024 = set(tabla_qi["columna"])
qi_2023 = set(tabla_qi_2023["columna"])
print("\nColumnas QI solo en 2024:", sorted(qi_2024 - qi_2023) or "(ninguna)")
print("Columnas QI solo en 2023:", sorted(qi_2023 - qi_2024) or "(ninguna)")

# --- OSM por departamento (L2 Parte 4, ≥ 5 DPTO) ---
osm_rows: list[dict] = []
for dpto_code, nombre in DPTO_TO_OSM_RELATION.items():
    rel_id = DPTO_TO_OSM_RELATION_IDS[dpto_code]
    area_id = 3600000000 + rel_id
    print(f"\nConsultando {nombre} (DPTO {dpto_code}, relación {rel_id})...")
    schools = contar_nodos_amenity(area_id, "school")
    health = contar_salud(area_id)
    osm_rows.append(
        {
            "dpto": dpto_code,
            "nombre": nombre,
            "poi_school_count": schools,
            "poi_health_count": health,
            "poi_servicios_basicos_count": schools + health,
        }
    )
    time.sleep(PAUSA_SEG)

osm_df = pd.DataFrame(osm_rows)
osm_path = LOCAL_OUTPUTS / "osm_poi_by_dpto.csv"
osm_df.to_csv(osm_path, index=False)
print(f"\nGuardado: {osm_path}")
print(osm_df.to_string(index=False))

# --- enlace GEIH + OSM (L2 Parte 4, todos los DPTO del CSV) ---
work_dpto = df.copy()
work_dpto["DPTO"] = pd.to_numeric(work_dpto["DPTO"], errors="coerce")
geih_dpto = (
    work_dpto.groupby("DPTO")
    .size()
    .reset_index(name="personas_muestra")
)
geih_dpto["DPTO"] = geih_dpto["DPTO"].astype(int)

enlace_df = geih_dpto.merge(osm_df, left_on="DPTO", right_on="dpto", how="inner")
print("\nEnlace GEIH + OSM (enero 2024):")
print(enlace_df[["DPTO", "nombre", "personas_muestra", "poi_servicios_basicos_count"]].to_string(index=False))

fig, ax = plt.subplots(figsize=(6, 4))
ax.scatter(
    enlace_df["personas_muestra"],
    enlace_df["poi_servicios_basicos_count"],
    s=60,
)
for _, row in enlace_df.iterrows():
    ax.annotate(str(int(row["DPTO"])), (row["personas_muestra"], row["poi_servicios_basicos_count"]), fontsize=8)
ax.set_xlabel("Personas en muestra GEIH (enero 2024)")
ax.set_ylabel("POI servicios básicos (OSM)")
ax.set_title("Enlace ilustrativo GEIH + OSM (5 departamentos)")
fig.tight_layout()
fig.savefig(LOCAL_OUTPUTS / "enlace_geih_osm_grupo.png", dpi=120)
plt.show()
print("Parte 0, Paso 0.2, Parte B week-1-group: ejecutado")
```

**Comprobar:**

```python
assert "DPTO" in df.columns and "P6040" in df.columns
assert {"columna", "tipo", "valores_unicos"}.issubset(tabla_qi.columns)
assert len(tabla_qi) >= 5
assert "DPTO" in tabla_qi["columna"].values
assert len(tabla_qi_2023) >= 1
assert osm_path.is_file()
assert len(osm_df) >= 5
assert {"dpto", "poi_school_count", "poi_health_count", "poi_servicios_basicos_count"}.issubset(
    osm_df.columns
)
assert len(enlace_df) >= 5
assert "personas_muestra" in enlace_df.columns
print("Parte 0, Paso 0.2, Parte B week-1-group: OK")
```

---

## Parte 1. Google Drive: persistir lo descargado

En Colab, **`/content`** se borra al cerrar la sesión. Por eso, **después de la Parte 0**, copiamos **`data/raw/`** (2022–2025) y **`manifest.json`** a **Google Drive**.

### Paso 1.1. Montar Drive (solo Colab)

Si trabaja en **local**, deje `USE_GOOGLE_DRIVE = False`: `WORK_ROOT` será la carpeta del proyecto (donde ya tiene los CSV tras la Parte 0).

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
    # Puede cambiar por la ruta en donde usted quiere guardar los datos
    WORK_ROOT = Path("/content/drive/MyDrive/udenar/cease/2026/big-data/data/")
    print(f"Raíz persistente en Drive: {WORK_ROOT}")
else:
    WORK_ROOT = SESSION_ROOT
    print(f"Raíz local (misma sesión): {WORK_ROOT.resolve()}")

WORK_ROOT.mkdir(parents=True, exist_ok=True)
```

### Paso 1.2. Rutas de trabajo en Drive (o local)

A partir de aquí, **Partes 2–5** leen y escriben bajo `WORK_ROOT`:

| Ruta | Contenido |
|------|-----------|
| `data/raw/2022/` … `data/raw/2025/` | CSV descargados (Parte 0, copiados aquí) |
| `data/processed/geih-spine/` | Parquet harmonizado (2024 en este cuaderno) |
| `manifest.json` | Registro de acceso DANE |
| `outputs/` | Exportaciones auxiliares |

Empezamos configurando las rutas para que utilicen las carpetas y archivos en Google Drive.

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

### Paso 1.3. Copiar la descarga de la sesión → Drive (una vez)

Si acaba de ejecutar el **Paso 0.1**, los CSV están bajo `LOCAL_RAW` (`/content/data/raw/`). Esta celda **copia cada año** a Drive si allí aún no están los 12 meses de ese año.

En **sesiones futuras**, Drive ya tiene los datos. Esta celda imprime *omitido* y puede poner **`SKIP_DOWNLOAD = True`** en el Paso 0.1.

```python
def spine_ready_on_drive(raw_dir: Path) -> bool:
    return all(count_month_folders(raw_dir / str(y)) >= 12 for y in SPINE_CATALOGS)


if spine_ready_on_drive(RAW_DIR):
    print("Drive ya tiene 2022–2025 completos, no hace falta copiar.")
elif spine_ready_on_drive(LOCAL_RAW):
    print("Copiando data/raw/2022–2025 de la sesión → Drive (puede tardar)...")
    for survey_year in SPINE_CATALOGS:
        local_y = LOCAL_RAW / str(survey_year)
        drive_y = RAW_DIR / str(survey_year)
        if count_month_folders(local_y) >= 12:
            drive_y.mkdir(parents=True, exist_ok=True)
            for item in local_y.iterdir():
                dest = drive_y / item.name
                if item.is_dir():
                    shutil.copytree(item, dest, dirs_exist_ok=True)
                elif item.is_file():
                    shutil.copy2(item, dest)
    if LOCAL_MANIFEST.is_file() and not MANIFEST_PATH.is_file():
        shutil.copy2(LOCAL_MANIFEST, MANIFEST_PATH)
    print("Copia a Drive terminada.")
else:
    raise FileNotFoundError(
        "Faltan años en local y en Drive. Ejecute el Paso 0.1 (bloque compacto) primero."
    )

print("Meses por año en Drive:", {y: count_month_folders(RAW_DIR / str(y)) for y in SPINE_CATALOGS})
```

**Comprobar:**

```python
n_drive_final = count_month_folders(YEAR_DIR)
print(f"Meses en Drive: {n_drive_final}")
assert n_drive_final >= 12
assert WORK_ROOT.is_dir()
print("Parte 1, Drive / persistencia: OK")
```

---

## Parte 2. Harmonización de datos

Un mes del DANE no llega como **una** tabla lista para analizar. Llega como **varios CSV** (i.e., Fuerza de trabajo, Características generales, etc) con **nombres de columna en código** (`P6040`, `P6240`, `FEX_C18`) que además pueden cambiar de formato entre años.

**Harmonizar** quiere decir convertir ese mes crudo en **una sola tabla** con:

1. la información que necesitamos **unida** (empleo + edad/sexo en la misma fila),
2. **nombres legibles** en lugar de los códigos del DANE,
3. **tipos** correctos (números como números) y las **claves de partición** (`anio`, `mes`).

Usamos **nombres en español** para que el dataset hable el mismo idioma que la fuente del DANE.

**Qué columna del DANE pasa a qué nombre**

| Columna DANE | Nombre del cuaderno | Significado | Conversión |
|--------------|---------------------|-------------|------------|
| `PERIODO` | `periodo`, `anio`, `mes` | Periodo de la ronda (AAAAMMDD) | Derivar año y mes |
| `DIRECTORIO` + `HOGAR` | `id_hogar` | Hogar en la muestra del mes | Concatenar como texto |
| `ORDEN` | `orden_persona` | Persona dentro del hogar | Entero |
| `DPTO` | `dpto` | Departamento (código DANE) | Entero |
| `AREA` | `area` | Urbano / rural | Entero |
| `P6040` | `edad` | Edad en años | Numérico |
| `P3271` | `sexo` | Sexo | Numérico |
| `P6240` | `actividad` | Actividad principal (estado en la fuerza de trabajo) | Numérico (sin interpretar) |
| `FEX_C18` | `factor_expansion` | Factor de expansión de la encuesta | Numérico |

Los significados oficiales de cada código están en el [diccionario de datos GEIH del DANE](https://microdatos.dane.gov.co/index.php/catalog/819/data-dictionary).

Harmonizamos **los 12 meses de 2024** en este cuaderno. En **`week-2-group`** su grupo reutiliza la misma función para **2022, 2023 y 2025**.

Antes de escribir Parquet necesitamos un **motor** que sepa leer y escribir ese formato. **PyArrow** es la librería que pandas usa por debajo para Parquet (lectura/escritura en columnas, compresión, tipos). En Colab no viene instalada, por eso la instalamos a continuación:

```python
# pyarrow: motor que pandas usa para leer/escribir archivos Parquet
%pip install -q pyarrow
```

### Paso 2.1. Localizar CSV de un mes

Cada carpeta mensual trae **varios** CSV. Necesitamos dos: **Fuerza de trabajo** (empleo) y **Características generales** (edad, sexo). Como el nombre exacto del archivo cambia entre meses, en vez de escribirlo a mano buscamos por **palabra clave** dentro del nombre.

Estos dos *helpers* recorren los `.CSV` de la carpeta y devuelven el primero cuyo nombre contiene la palabra esperada. El `.replace("\xa0", " ")` arregla un espacio especial que el DANE a veces mete en los nombres:

```python
def _labour_csv(month_dir: Path) -> Path:
    # Devuelve el CSV cuyo nombre contiene "fuerza de trabajo"
    return next(
        p for p in month_dir.glob("*.CSV")
        if PRIMARY_TABLE_KEYWORD in p.name.lower().replace("\xa0", " ")
    )


def _demog_csv(month_dir: Path) -> Path:
    # Devuelve el CSV que contiene las palabras de "características generales"
    return next(
        p for p in month_dir.glob("*.CSV")
        if all(kw in p.name.lower().replace("\xa0", " ") for kw in DEMOG_TABLE_KEYWORDS)
    )


# Carpetas de meses que ya tienen CSV extraídos (de la Parte 0 / Drive)
month_dirs_demo = sorted(
    p for p in YEAR_DIR.iterdir()
    if p.is_dir() and list(p.glob("*.CSV"))
)
demo_month = month_dirs_demo[0]  # usamos el primer mes como ejemplo
print("Mes de ejemplo:", demo_month.name)
print("Fuerza de trabajo:", _labour_csv(demo_month).name)
print("Características:", _demog_csv(demo_month).name)
```

### Paso 2.2. Leer cada tabla por separado

Primero leemos **Fuerza de trabajo** (todas las columnas que necesitamos más adelante):

```python
labour_path = _labour_csv(demo_month)
labour = pd.read_csv(labour_path, sep=CSV_SEP, encoding=CSV_ENCODING, low_memory=False)
print(f"Filas fuerza de trabajo: {len(labour):,}")
print("Columnas (muestra):", list(labour.columns[:8]), "...")
print(labour[["DIRECTORIO", "HOGAR", "ORDEN", "PERIODO", "DPTO", "P6240"]].head(2))
```

Después leemos **Características generales**, solo las columnas demográficas que uniremos:

```python
demog_path = _demog_csv(demo_month)
demog = pd.read_csv(
    demog_path,
    sep=CSV_SEP,
    encoding=CSV_ENCODING,
    usecols=PERSON_KEYS + ["P6040", "P3271"],
    low_memory=False,
)
print(f"Filas características: {len(demog):,}")
print(demog.head(2))
```

### Paso 2.3. Unir tablas con `merge`

Unimos por **`PERSON_KEYS`**, igual que en el repaso y en la lección 2:

```python
merged = labour.merge(demog, on=PERSON_KEYS, how="left", validate="many_to_one")
print(f"Filas después del merge: {len(merged):,}")
print(merged[PERSON_KEYS + ["P6040", "P6240", "DPTO", "PERIODO"]].head(2))
```

### Paso 2.4. Derivar las claves de tiempo desde `PERIODO`

`PERIODO` viene como un número **AAAAMMDD** (por ejemplo `20240101`). De ahí sacamos el **año** y el **mes**, que usaremos para partir el Parquet en carpetas `anio=2024/mes=01/`:

```python
periodo = merged["PERIODO"].astype(int)
anio = (periodo // 10000).astype(int)        # AAAA: primeros 4 dígitos
mes = ((periodo // 100) % 100).astype(int)   # MM: dígitos del mes

print("Periodo de ejemplo:", int(periodo.iloc[0]))
print("Año:", int(anio.iloc[0]), "| Mes:", int(mes.iloc[0]))
```

### Paso 2.5. Renombrar a nombres legibles

Construimos el DataFrame harmonizado: una fila por persona, con los **nombres en español** y los tipos correctos (ver la tabla de mapeo arriba). Aquí **no interpretamos** `actividad`, solo la guardamos tal cual; quién está ocupado se decide en la lección 4:

```python
harmonized_preview = pd.DataFrame(
    {
        "periodo": (anio * 100 + mes).astype(int),                                  # AAAAMM
        "anio": anio,
        "mes": mes,
        "id_hogar": merged["DIRECTORIO"].astype(str) + "-" + merged["HOGAR"].astype(str),  # clave de hogar
        "orden_persona": merged["ORDEN"].astype(int),
        "dpto": merged["DPTO"].astype(int),
        "area": merged["AREA"].astype(int),
        "edad": pd.to_numeric(merged["P6040"], errors="coerce"),                    # texto -> número
        "sexo": pd.to_numeric(merged["P3271"], errors="coerce"),
        "actividad": pd.to_numeric(merged["P6240"], errors="coerce"),               # P6240 sin interpretar
        "factor_expansion": pd.to_numeric(merged["FEX_C18"], errors="coerce"),      # peso de la encuesta
    }
)
print("Vista previa harmonizada (5 filas):")
print(harmonized_preview.head(5))
```

### Paso 2.6. Consolidación: función `harmonize_month`

Reunimos los pasos 2.1 a 2.5 en **una función reutilizable**. Recibe la carpeta de un mes y devuelve la tabla harmonizada:

```python
def harmonize_month(month_dir: Path) -> pd.DataFrame:
    """Lee un mes (Fuerza de trabajo + Características), une por PERSON_KEYS
    y devuelve una tabla con nombres en español y claves de partición."""
    # 1) Leer las dos tablas del mes
    labour = pd.read_csv(
        _labour_csv(month_dir), sep=CSV_SEP, encoding=CSV_ENCODING, low_memory=False
    )
    demog = pd.read_csv(
        _demog_csv(month_dir),
        sep=CSV_SEP,
        encoding=CSV_ENCODING,
        usecols=PERSON_KEYS + ["P6040", "P3271"],  # solo lo que uniremos
        low_memory=False,
    )
    # 2) Unir empleo + demografía por la misma persona
    merged = labour.merge(demog, on=PERSON_KEYS, how="left", validate="many_to_one")
    if "PERIODO" not in merged.columns:
        raise KeyError(f"Falta PERIODO en {month_dir.name}")

    # 3) Claves de tiempo para particionar
    periodo = merged["PERIODO"].astype(int)
    anio = (periodo // 10000).astype(int)
    mes = ((periodo // 100) % 100).astype(int)

    # 4) Renombrar a español y fijar tipos
    return pd.DataFrame(
        {
            "periodo": (anio * 100 + mes).astype(int),
            "anio": anio,
            "mes": mes,
            "id_hogar": merged["DIRECTORIO"].astype(str) + "-" + merged["HOGAR"].astype(str),
            "orden_persona": merged["ORDEN"].astype(int),
            "dpto": merged["DPTO"].astype(int),
            "area": merged["AREA"].astype(int),
            "edad": pd.to_numeric(merged["P6040"], errors="coerce"),
            "sexo": pd.to_numeric(merged["P3271"], errors="coerce"),
            "actividad": pd.to_numeric(merged["P6240"], errors="coerce"),
            "factor_expansion": pd.to_numeric(merged["FEX_C18"], errors="coerce"),
        }
    )


print("harmonize_month(): consolidada")
```

Probamos la función sobre el mes de ejemplo y mostramos las **primeras 5 filas**:

```python
demo_harmonized = harmonize_month(demo_month)
print(f"Filas harmonizadas ({demo_month.name}): {len(demo_harmonized):,}")
print("Columnas:", list(demo_harmonized.columns))
print(demo_harmonized.head(5))
```

**Comprobar:**

```python
print(f"Mes demo: {int(demo_harmonized['mes'].iloc[0])}, filas: {len(demo_harmonized):,}")
assert callable(harmonize_month)
assert len(demo_harmonized) > 1000
assert {"dpto", "actividad", "factor_expansion"}.issubset(demo_harmonized.columns)
print("Parte 2, harmonize_month: OK")
```

---

## Parte 3. Escribir Parquet particionado

Ya tenemos cada mes como una tabla limpia y comparable. Ahora la **guardamos** en **Parquet**, un formato en columnas que se lee rápido, comprime bien y permite **partir** el dataset en carpetas `anio=2024/mes=MM/`. Así se puede leer un solo mes sin cargar el año entero. Esta estructura de árbol sirve para la lección 4 y para el trabajo grupal.

**Objetivo.** Recorrer cada carpeta mensual en `data/raw/2024/`, harmonizar y escribir **`anio=2024/mes=MM/part-000.parquet`**. Si ya existe el árbol en Drive, puede **omitir** la re-escritura (`SKIP_IF_PARQUET_EXISTS`).

**Ejecución a escala.** Con **`harmonize_month`** ya consolidada, aplicamos el mismo flujo a los 12 meses:

```python
SKIP_IF_PARQUET_EXISTS = True  # no reescribir si la partición ya existe en Drive

# Carpetas de meses con CSV listos
month_dirs = sorted(
    p for p in YEAR_DIR.iterdir()
    if p.is_dir() and list(p.glob("*.CSV"))
)
if not month_dirs:
    raise FileNotFoundError(
        f"No hay CSV bajo {YEAR_DIR}. Monte Drive (Parte 1) o complete week-1-group."
    )

print(f"Carpetas mensuales a procesar: {len(month_dirs)}")
partition_stats: list[dict] = []

for month_dir in month_dirs:
    sample = harmonize_month(month_dir)         # transformar el mes
    y = int(sample["anio"].iloc[0])
    m = int(sample["mes"].iloc[0])
    # Una carpeta por año y mes: anio=2024/mes=01/
    part_dir = PROCESSED_DIR / f"anio={y}" / f"mes={m:02d}"
    part_file = part_dir / "part-000.parquet"

    if SKIP_IF_PARQUET_EXISTS and part_file.is_file():
        print(f"Omitido (ya existe): {part_file.relative_to(WORK_ROOT)}")
        # Leyendo solo una columna del Parquet para contar filas
        n_rows = len(pd.read_parquet(part_file, columns=["dpto"]))
    else:
        part_dir.mkdir(parents=True, exist_ok=True)
        # Almacenando el DataFrame como un archivo Parquet
        sample.to_parquet(part_file, index=False)
        n_rows = len(sample)
        print(f"Escrito {part_file.relative_to(WORK_ROOT)} | filas: {n_rows:,}")

    partition_stats.append({"anio": y, "mes": m, "filas": n_rows, "ruta": str(part_file)})

stats_df = pd.DataFrame(partition_stats).sort_values(["anio", "mes"])
print("\nResumen particiones 2024:")
print(stats_df.to_string(index=False))
print(f"Total filas: {stats_df['filas'].sum():,}")
```

**Comprobar:**

```python
print(f"Particiones escritas: {len(stats_df)}")
print(f"Total filas: {stats_df['filas'].sum():,}")
assert len(stats_df) >= 12, f"Se esperan 12 meses 2024. Hay {len(stats_df)}"
assert stats_df["filas"].sum() > 100_000
assert (PROCESSED_DIR / "anio=2024" / "mes=01" / "part-000.parquet").is_file()
print("Parte 3, Parquet 2024 completo: OK")
```

---

## Parte 4. Benchmark: CSV crudo vs Parquet

**Objetivo.** Comparar **las dos formas de cargar los mismos datos de 2024**: la *forma normal* (leer los CSV del DANE y unir tablas, como en la Parte 2) frente a leer el **Parquet** ya harmonizado de la Parte 3. Medimos **tiempo**, **memoria** y **tamaño en disco**. Esto muestra por qué guardamos en Parquet antes de procesar en la lección 4.

Para que la comparación sea **justa**, ambas rutas producen el mismo año completo (12 meses) en un DataFrame.

### Paso 4.1. Forma normal: leer CSV y unir (12 meses)

Recorremos las carpetas de 2024 y aplicamos `harmonize_month` (lee dos CSV por mes y los une). Es lo que tendría que hacer **cada vez** si no guardara Parquet:

```python
import time

month_dirs = sorted(
    p for p in YEAR_DIR.iterdir()
    if p.is_dir() and list(p.glob("*.CSV"))
)

t0 = time.perf_counter()
# Leer + unir los 12 meses desde CSV (forma "cruda")
df_csv = pd.concat([harmonize_month(m) for m in month_dirs], ignore_index=True)
csv_seconds = round(time.perf_counter() - t0, 2)

mem_csv_mb = df_csv.memory_usage(deep=True).sum() / 1e6
print(f"CSV crudo  -> filas: {len(df_csv):,} | tiempo: {csv_seconds} s | memoria: {mem_csv_mb:.1f} MB")
del df_csv
```

### Paso 4.2. Forma Parquet: leer el árbol harmonizado (12 meses)

Ahora cargamos el **mismo** año, pero desde el Parquet de la Parte 3:

```python
t0 = time.perf_counter()
# Leer el árbol completo anio=2024/ (todos los meses)
df_parquet = pd.read_parquet(PROCESSED_DIR / "anio=2024")
parquet_seconds = round(time.perf_counter() - t0, 2)

mem_parquet_mb = df_parquet.memory_usage(deep=True).sum() / 1e6
print(f"Parquet    -> filas: {len(df_parquet):,} | tiempo: {parquet_seconds} s | memoria: {mem_parquet_mb:.1f} MB")
```

### Paso 4.3. Tamaño en disco

Parquet comprime por columnas, así que ocupa **mucho menos** que los CSV del DANE:

```python
def dir_size_mb(folder: Path, pattern: str) -> float:
    # Suma el tamaño (MB) de los archivos que coinciden con el patrón
    return sum(f.stat().st_size for f in folder.rglob(pattern)) / 1e6

csv_mb = dir_size_mb(YEAR_DIR, "*.CSV")
parquet_mb = dir_size_mb(PROCESSED_DIR / "anio=2024", "*.parquet")

resumen = pd.DataFrame(
    {
        "formato": ["CSV crudo", "Parquet"],
        "tiempo_seg": [csv_seconds, parquet_seconds],
        "memoria_mb": [round(mem_csv_mb, 1), round(mem_parquet_mb, 1)],
        "disco_mb": [round(csv_mb, 1), round(parquet_mb, 1)],
    }
)
print(resumen.to_string(index=False))
```

**Interpretación.** Leer desde CSV obliga a **re-parsear y re-unir** todo cada vez; Parquet ya está harmonizado, en columnas y comprimido, así que se lee más rápido y ocupa menos disco. Por eso, en la lección 4, procesamos sobre el Parquet y no sobre los CSV.

**Comprobar:**

```python
print(f"CSV: {csv_seconds}s / {csv_mb:.0f}MB | Parquet: {parquet_seconds}s / {parquet_mb:.0f}MB")
assert len(df_parquet) > 100_000
assert parquet_mb < csv_mb  # Parquet pesa menos en disco
print("Parte 4, benchmark CSV vs Parquet: OK")
```

---

## Parte 5. Gobernanza al almacenar

**Objetivo.** Documentar qué **persistimos** en Parquet, mostrar cómo **publicar con privacidad diferencial**, fijar una **regla de retención** y dejar todo registrado en `manifest.json`.

### Paso 5.1. Cuasi-identificadores en el archivo harmonizado

```python
sample_path = PROCESSED_DIR / "anio=2024" / "mes=01" / "part-000.parquet"
schema_cols = pd.read_parquet(sample_path).columns.tolist()  # columnas guardadas

QI_EN_PARQUET = [
    ("id_hogar", "Clave compuesta de hogar, no publicar en agregados finos"),
    ("dpto", "Geografía departamental"),
    ("area", "Urbano / rural"),
    ("edad", "Edad en años"),
    ("sexo", "Sexo"),
]
tabla_store = pd.DataFrame(QI_EN_PARQUET, columns=["columna", "nota_riesgo"])
print("Columnas sensibles que **guardamos** (microdato interno):")
print(tabla_store.to_string(index=False))
```

### Paso 5.2. Publicar con privacidad diferencial (mecanismo de Laplace)

Ya vimos **cuasi-identificadores** y **k-anonimato** en las lecciones anteriores. Aquí usamos un método distinto: **privacidad diferencial**. En vez de suprimir celdas pequeñas, **añadimos ruido aleatorio calibrado** a cada conteo que publicamos. La idea: el número publicado casi no cambia si una persona está o no en los datos, así nadie puede deducir quién participó.

Dos parámetros mandan:

- **Sensibilidad:** cuánto cambia la consulta si entra o sale **una** persona. Para un **conteo** es **1**.
- **Épsilon (`epsilon`):** el **presupuesto de privacidad**. Más pequeño = más privacidad y más ruido.

El **mecanismo de Laplace** suma ruido `Laplace(0, sensibilidad / epsilon)` al valor real:

```python
import numpy as np

rng = np.random.default_rng(42)  # semilla para reproducir el ejemplo

# Conteo real de personas por departamento (enero 2024)
conteo_real = (
    pd.read_parquet(sample_path, columns=["dpto"])
    .groupby("dpto").size().reset_index(name="personas")
)

DP_SENSIBILIDAD = 1.0   # un conteo cambia en 1 si entra/sale una persona
DP_EPSILON = 1.0        # presupuesto de privacidad (más bajo = más ruido)

def laplace_count(valor_real: int, epsilon: float, sensibilidad: float = 1.0) -> float:
    # Ruido Laplace centrado en 0, escala = sensibilidad / epsilon
    ruido = rng.laplace(loc=0.0, scale=sensibilidad / epsilon)
    return valor_real + ruido

# Publicamos cada conteo con ruido (redondeado, sin negativos)
conteo_real["personas_dp"] = [
    max(0, round(laplace_count(n, DP_EPSILON, DP_SENSIBILIDAD)))
    for n in conteo_real["personas"]
]
print(f"epsilon = {DP_EPSILON}, sensibilidad = {DP_SENSIBILIDAD}")
print(conteo_real.head(5).to_string(index=False))
```

Veamos el efecto del presupuesto: con **`epsilon` pequeño** el ruido es mayor (más privacidad, menos exactitud):

```python
for eps in (0.1, 1.0, 5.0):
    muestra_dp = [round(laplace_count(n, eps)) for n in conteo_real["personas"].head(3)]
    print(f"epsilon={eps:>4}: reales={list(conteo_real['personas'].head(3))} -> con ruido={muestra_dp}")
```

**Interpretación.** El k-anonimato **esconde** a las personas en grupos de al menos `k`. La privacidad diferencial **no esconde filas**: deja publicar conteos, pero con una **garantía matemática** (controlada por `epsilon`) de que el resultado casi no depende de ningún individuo. El costo es **exactitud**: cuanto más privacidad (menor `epsilon`), más ruido. En la **lección 4** complementamos esto con **supresión k = 5** sobre los agregados de empleo.

### Paso 5.3. Linaje y regla de retención

El **linaje** dice de dónde salió el Parquet (catálogo del DANE, versión de harmonización). Es un dato **constante** del dataset, así que lo guardamos **una sola vez** como metadato, no repetido en cada fila. La **retención** fija por cuánto tiempo conservamos los datos.

```python
LINEAGE = {
    "source_catalog": str(SPINE_CATALOGS[YEAR]),  # catálogo DANE del año (2024 -> 819)
    "harmonisation_version": "2026-06-l3-demo",   # versión del mapeo de la Parte 2
    "raw_path": str(YEAR_DIR),
    "processed_path": str(PROCESSED_DIR),
}
RETENTION_RULE = (
    "Conservar el Parquet harmonizado solo durante el curso (retención: 6 meses) "
    "y ELIMINARLO al terminar el curso, a más tardar el 11 de julio de 2026. "
    "No publicar microfilas ni particiones crudas. Agregados externos solo con k >= 5 ocupados."
)
RETENTION_DAYS = 180  # ~6 meses

print("Linaje (metadatos):")
for k, v in LINEAGE.items():
    print(f"  {k}: {v}")
print(f"\nRetención: {RETENTION_DAYS} días, eliminar al finalizar el curso.")
print("Regla:\n ", RETENTION_RULE)
```

### Paso 5.4. Guardar todo en `manifest.json`

El `manifest.json` es el registro auditable que entrega su grupo (sin archivos de datos). Esta vez incluimos **linaje**, **conteos por partición** y el **benchmark** de la Parte 4:

```python
import json

# Conservar el registro de acceso (descarga) de la Parte 0 si existe
acceso_previo = None
if MANIFEST_PATH.is_file():
    try:
        acceso_previo = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        acceso_previo = None

manifest = {
    "linaje": LINEAGE,
    "retencion": {"dias": RETENTION_DAYS, "regla": RETENTION_RULE},
    "particiones": partition_stats,  # anio, mes, filas, ruta (Parte 3)
    "total_filas": int(stats_df["filas"].sum()),
    "benchmark": {
        "csv": {"segundos": csv_seconds, "memoria_mb": round(mem_csv_mb, 1), "disco_mb": round(csv_mb, 1)},
        "parquet": {"segundos": parquet_seconds, "memoria_mb": round(mem_parquet_mb, 1), "disco_mb": round(parquet_mb, 1)},
    },
    "privacidad": {"mecanismo": "laplace", "epsilon": DP_EPSILON, "sensibilidad": DP_SENSIBILIDAD},
}
if acceso_previo is not None:
    manifest["acceso"] = acceso_previo  # descargas registradas en la Parte 0

# Escribir el manifiesto como JSON legible
MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
print("Manifiesto escrito en:", MANIFEST_PATH)
print("Claves:", list(manifest.keys()))
```

**Comprobar:**

```python
guardado = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
print("Columnas en Parquet:", schema_cols[:6], "...")
print("Manifiesto, total filas:", guardado["total_filas"])
assert {"linaje", "particiones", "benchmark"}.issubset(guardado.keys())
assert guardado["linaje"]["source_catalog"] == "819"
assert RETENTION_DAYS > 0
print("Parte 5, gobernanza al almacenar: OK")
```

---

## Puente al cuaderno grupal

En el cuaderno **`week-2-group`** (Parte A) su grupo:

1. Harmoniza **2022–2025** reutilizando **`harmonize_month`** (mismo mapeo).
2. Repite el benchmark de la Parte 4 sobre el árbol completo.
3. Documenta **elección de partición** y ética de retención.
4. Continúa en Parte B (procesamiento, lección 4).

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
