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
    """Convierte PERIODO GEIH (AAAAMMDD) en año y mes.

    Parámetros:
        periodo: entero DANE, p. ej. 20240101 (enero 2024).

    Retorna:
        Tupla (año, mes), p. ej. (2024, 1).
    """
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

### Lakehouse y Parquet: tres niveles

En la lección hablamos de **lakehouse**: almacenamiento barato y accesible, organizado como **tablas analíticas**, con gobernanza. En este cuaderno **no montamos un servidor**, construimos un **lakehouse pequeño** en Drive con tres niveles:

| Nivel | Qué es | En este cuaderno |
|-------|--------|------------------|
| **Lakehouse** | Conjunto de datos procesados listos para analizar (no solo un montón de archivos crudos) | Carpeta `data/processed/geih-spine/` |
| **Tabla particionada** | Organización tipo Hive: carpetas `clave=valor/` que el motor puede omitir al leer | `anio=2024/mes=01/`, `anio=2024/mes=02/`, … |
| **Archivo Parquet** | Formato **columnar** dentro de cada partición (compresión, tipos, lectura rápida) | `part-000.parquet` |

Los CSV del DANE en `data/raw/` son la **entrada cruda** (como en un data lake). La **Parte 2** harmoniza; la **Parte 3** **carga** el resultado en el lakehouse como Parquet particionado.

### Parquet: leer y escribir (formato de archivo)

**Parquet** es el **formato de archivo** del último nivel de la tabla anterior, no el lakehouse completo. Podemos manipular archivos **Parquet** con **pandas** y **pyarrow**:

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

**Propósito.** Este cuaderno es su práctica de la **Lección 3 (Almacenamiento)**. Ya hicimos **Access** en la lección 1 y evaluamos aspectos éticos y de privacidad de datos en la lección 2. Ahora **construimos un lakehouse GEIH**: una tabla harmonizada y particionada bajo `data/processed/geih-spine/`, implementada con archivos **Parquet** en carpetas `anio=…/mes=…/`.

**Qué hace el cuaderno (en orden).**

| Parte | Tema |
|-------|------|
| **0** | **Solución** del deber grupal semana 1 (`week-1-group`): Parte A (Access **2022–2025**) + Parte B (ética + OSM) |
| **1** | Montar **Google Drive** y **copiar** lo descargado (no repetir DANE en cada sesión) |
| **2** | Función **`harmonize_month`** (transformar: unir tablas + nombres legibles + claves de partición) |
| **3** | **Cargar el lakehouse**: harmonizar 12 meses 2024 → Parquet particionado en Drive |
| **4** | **Benchmark**: leer CSV crudo vs leer el lakehouse |
| **5** | **Gobernanza** del lakehouse (retención, linaje) |

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


def read_geih_csv(path: Path, usecols=None) -> pd.DataFrame:
    """Lee un CSV del DANE con pandas.

    Parámetros:
        path: ruta al archivo (.csv o .CSV).
        usecols: columnas a cargar (None = todas).

    Retorna:
        DataFrame parseado (intenta separador ; y luego ,).

    Lanza:
        ValueError si ningún delimitador produce más de una columna.
    """
    for sep in (CSV_SEP, ","):
        try:
            df = pd.read_csv(
                path,
                sep=sep,
                encoding=CSV_ENCODING,
                usecols=usecols,
                low_memory=False,
            )
        except ValueError:
            continue
        if len(df.columns) > 1:
            return df
    raise ValueError(f"No se pudo parsear {path.name} con ; ni ,")


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
    """Descarga un ZIP del catálogo microdatos DANE.

    Parámetros:
        url: enlace HTTP(S) al archivo ZIP.
        dest: ruta local donde guardar el ZIP.
        timeout: segundos máximos de espera por la red.

    Retorna:
        Tupla (segundos_empleados, bytes_descargados).

    Lanza:
        ValueError si el archivo descargado no empieza con PK (no es ZIP).
    """
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
    """Extrae archivos CSV de un ZIP mensual del DANE.

    Parámetros:
        zip_path: ruta al ZIP descargado (p. ej. Ene_2024.zip).
        dest_dir: carpeta destino (p. ej. data/raw/2024/Ene_2024/).

    Retorna:
        Lista de rutas a los .csv/.CSV extraídos (ordenadas).

    Nota:
        Si el ZIP solo trae csv.zip anidado, lo abre y extrae recursivamente.
    """
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
    """Escribe el manifiesto de acceso (descargas) en JSON.

    Parámetros:
        path: ruta del archivo manifest.json.
        entries: lista de dicts con metadatos por archivo descargado.
    """
    path.write_text(json.dumps(entries, indent=2, ensure_ascii=False), encoding="utf-8")


def list_catalog_downloads(catalog_id: int) -> list[dict]:
    """Lista los ZIP mensuales disponibles en un catálogo DANE.

    Parámetros:
        catalog_id: id del catálogo (p. ej. 819 para GEIH 2024).

    Retorna:
        Lista de dicts con file_id, filename y url por mes, ordenada por nombre.
    """
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
    """Descarga y extrae un mes GEIH si aún no está en disco.

    Parámetros:
        item: dict de list_catalog_downloads (filename, url, file_id).
        year_dir: carpeta del año (p. ej. data/raw/2024/).
        survey_year: año de la encuesta (2022–2025).
        catalog_id: id del catálogo DANE.
        skip_if_exists: si True, omite descarga si la carpeta CSV ya existe.

    Retorna:
        Dict con metadatos para manifest (seconds, bytes_downloaded, extract_dir, …).
    """
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
    # Reutiliza download_zip y extract_csvs (definidas arriba en este bloque)
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
    """Cuenta carpetas mensuales con al menos un CSV.

    Parámetros:
        year_dir: ruta al año (p. ej. data/raw/2024/).

    Retorna:
        Número de subcarpetas con algún .csv o .CSV (0 si no existe year_dir).
    """
    if not year_dir.is_dir():
        return 0
    n = 0
    for p in year_dir.iterdir():
        if not p.is_dir():
            continue
        if any(f.is_file() and f.suffix.lower() == ".csv" for f in p.iterdir()):
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
    manifest_raw = json.loads(LOCAL_MANIFEST.read_text(encoding="utf-8"))
    manifest_df = pd.DataFrame(manifest_raw)
    print(f"Filas en manifiesto: {len(manifest_df)}")
    if "survey_year" in manifest_df.columns:
        print(manifest_df[["survey_year", "filename", "bytes_downloaded", "notes"]].head(3))
        assert "survey_year" in manifest_df.columns
    elif "slice_label" in manifest_df.columns:
        # Manifiesto de geih-build u otra herramienta de acceso (sin survey_year)
        print(manifest_df[["slice_label", "bytes_downloaded", "notes"]].head(3))
    else:
        print("Columnas del manifiesto:", list(manifest_df.columns)[:6])
    assert len(manifest_df) >= 40, "Se esperan ~48 filas (12 meses × 4 años) en la solución completa."
print("Parte 0, Paso 0.1, Access 2022–2025: OK")
```

---

### Paso 0.2. Bloque compacto: Parte B — cuasi-identificadores + OSM + enlace GEIH

Solución de la **Parte B** del cuaderno grupal: carga enero **2024** y **2023**, tabla de cuasi-identificadores en ambos años, consulta Overpass en **cinco departamentos**, guarda **`outputs/osm_poi_by_dpto.csv`** y enlaza con la muestra GEIH.

Para contar puntos de interés por departamento tomamos dos decisiones que hacen la consulta **robusta**:

1. **Identificar el área por su código ISO 3166-2** (por ejemplo `CO-NAR` para Nariño) en lugar de un id de relación de OSM. El id puede cambiar y es fácil equivocarse de departamento.
2. **Contar `nwr` (nodos, vías y relaciones), no solo nodos.** Muchas escuelas y hospitales se mapean como polígonos (vías), así que contar solo nodos los deja por fuera y da ceros enganosos.

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

# Código DANE del departamento → nombre y código ISO 3166-2 del departamento.
# Identificar el área por su código ISO es más robusto que usar un id de relación
# (que puede cambiar) y evita contar solo nodos sueltos.
DPTO_TO_OSM_RELATION: dict[int, str] = {
    5: "Antioquia",
    8: "Atlántico",
    11: "Bogotá D.C.",
    52: "Nariño",
    76: "Valle del Cauca",
}
DPTO_TO_ISO: dict[int, str] = {
    5: "CO-ANT",
    8: "CO-ATL",
    11: "CO-DC",
    52: "CO-NAR",
    76: "CO-VAC",
}

LOCAL_OUTPUTS = SESSION_ROOT / "outputs"
LOCAL_OUTPUTS.mkdir(parents=True, exist_ok=True)


def overpass_post(query: str, *, timeout: int = 90) -> requests.Response:
    """Envía una consulta Overpass API con reintentos entre espejos.

    Parámetros:
        query: texto Overpass QL (p. ej. contar amenity= en un área ISO).
        timeout: segundos máximos por intento HTTP.

    Retorna:
        Response HTTP con status 200 y cuerpo JSON.

    Lanza:
        requests.HTTPError si todos los espejos fallan.
    """
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


def contar_amenity(iso_code: str, amenity_regex: str, timeout: int = 90) -> int:
    """Cuenta POI OpenStreetMap por tipo de amenity en un departamento.

    Parámetros:
        iso_code: código ISO 3166-2 del departamento (p. ej. CO-N).
        amenity_regex: patrón regex de tags amenity (p. ej. 'school').
        timeout: segundos para overpass_post.

    Retorna:
        Total de nodos, vías y relaciones que coinciden (0 si vacío).
    """
    query = f"""
[out:json][timeout:60];
area["ISO3166-2"="{iso_code}"]->.a;
nwr["amenity"~"^({amenity_regex})$"](area.a);
out count;
"""
    data = overpass_post(query, timeout=timeout).json()
    elements = data.get("elements", [])
    # 'out count' devuelve un único elemento con el total en sus tags
    return int(elements[0]["tags"]["total"]) if elements else 0


def contar_salud(iso_code: str) -> int:
    """Cuenta POI de salud (hospital, clínica, …) en un departamento.

    Parámetros:
        iso_code: código ISO 3166-2 del departamento.

    Retorna:
        Total OSM de amenity de salud (reutiliza contar_amenity).
    """
    # Reutiliza contar_amenity con regex unión de HEALTH_AMENITIES
    return contar_amenity(iso_code, "|".join(HEALTH_AMENITIES))


def find_enero_dir(survey_year: int) -> Path:
    """Localiza la carpeta de enero bajo data/raw/<año>/.

    Parámetros:
        survey_year: año de la encuesta (p. ej. 2024).

    Retorna:
        Path a la primera carpeta cuyo nombre empieza por 'ene'.

    Lanza:
        FileNotFoundError si no hay carpeta de enero.
    """
    year_dir = LOCAL_RAW / str(survey_year)
    for p in sorted(year_dir.iterdir()):
        if p.is_dir() and p.name.lower().startswith("ene"):
            return p
    raise FileNotFoundError(f"No hay carpeta de enero bajo {year_dir}")


def load_mes_con_edad(survey_year: int) -> pd.DataFrame:
    """Carga enero: Fuerza de trabajo + edad (P6040) unidas por PERSON_KEYS.

    Parámetros:
        survey_year: año GEIH (2023, 2024, …).

    Retorna:
        DataFrame con columnas de empleo y P6040 (edad) por persona.
    """
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
    # Reutiliza read_geih_csv (Parte 0.1)
    labour = read_geih_csv(labour_path)
    demog = read_geih_csv(demog_path, usecols=PERSON_KEYS + ["P6040"])
    return labour.merge(demog, on=PERSON_KEYS, how="left", validate="many_to_one")


def tabla_cuasi_identificadores(frame: pd.DataFrame) -> pd.DataFrame:
    """Resume columnas sensibles presentes y su cardinalidad.

    Parámetros:
        frame: DataFrame GEIH (crudo o harmonizado).

    Retorna:
        DataFrame con columnas: columna, tipo, valores_unicos.
    """
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
    iso_code = DPTO_TO_ISO[dpto_code]  # área OSM por código ISO del departamento
    print(f"\nConsultando {nombre} (DPTO {dpto_code}, ISO {iso_code})...")
    schools = contar_amenity(iso_code, "school")  # escuelas (nodos + vías + relaciones)
    time.sleep(PAUSA_SEG)
    health = contar_salud(iso_code)               # salud: hospital, clínica, etc.
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
    WORK_ROOT = Path("/content/drive/MyDrive/udenar/cease/2026/big-data/")
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
| `data/raw/2022/` … `data/raw/2025/` | CSV crudos del DANE (entrada al pipeline; Parte 0, copiados aquí) |
| `data/processed/geih-spine/` | **Lakehouse GEIH** — tabla harmonizada en Parquet particionado (2024 en este cuaderno) |
| `manifest.json` | Registro de acceso, linaje del lakehouse y gobernanza |
| `outputs/` | Exportaciones auxiliares |

Empezamos configurando las rutas para que utilicen las carpetas y archivos en Google Drive.

En Colab, **`/content/data/raw`** se borra al reiniciar. **`DRIVE_RAW`** es la copia persistente bajo `WORK_ROOT`; **`SESSION_RAW`** es donde la Parte 0 escribe (`LOCAL_RAW`). Solo contamos meses si la carpeta mensual trae **CSV**, no carpetas vacías.

```python
SESSION_RAW = LOCAL_RAW  # Parte 0: típicamente /content/data/raw
DRIVE_RAW = WORK_ROOT / "data" / "raw"


def spine_has_full_raw(raw_root: Path) -> bool:
    """True si raw_root tiene ≥12 carpetas mensuales con CSV por cada año del spine.

    Parámetros:
        raw_root: raíz data/raw (sesión o Drive).

    Retorna:
        False si falta el directorio o algún año tiene menos de 12 meses con CSV.
    """
    if not raw_root.is_dir():
        return False
    # Reutiliza count_month_folders (Parte 0.1) — exige .csv dentro de cada mes
    return all(count_month_folders(raw_root / str(y)) >= 12 for y in SPINE_CATALOGS)


def resolve_raw_dir() -> Path:
    """Elige de dónde leer CSV: Drive completo, si no sesión, si no Drive por defecto.

    Retorna:
        Path a data/raw con datos listos, o DRIVE_RAW como destino de escritura.
    """
    if spine_has_full_raw(DRIVE_RAW):
        return DRIVE_RAW
    if spine_has_full_raw(SESSION_RAW):
        return SESSION_RAW
    return DRIVE_RAW


RAW_DIR = resolve_raw_dir()
# Raíz del lakehouse GEIH del curso (tabla particionada en Parquet)
PROCESSED_DIR = WORK_ROOT / "data" / "processed" / "geih-spine"
OUTPUTS_DIR = WORK_ROOT / "outputs"
MANIFEST_PATH = WORK_ROOT / "manifest.json"

for p in (RAW_DIR, PROCESSED_DIR, OUTPUTS_DIR):
    p.mkdir(parents=True, exist_ok=True)

YEAR_DIR = RAW_DIR / str(YEAR)
YEAR_DIR.mkdir(parents=True, exist_ok=True)

print("RAW activo (Partes 2–5):", RAW_DIR.resolve())
print("  sesión:", SESSION_RAW.resolve(), "→", {y: count_month_folders(SESSION_RAW / str(y)) for y in SPINE_CATALOGS})
print("  Drive: ", DRIVE_RAW.resolve(), "→", {y: count_month_folders(DRIVE_RAW / str(y)) for y in SPINE_CATALOGS})
print("Lakehouse (geih-spine):", PROCESSED_DIR)
print("Manifiesto:", MANIFEST_PATH)
```

### Paso 1.3. Copiar la descarga de la sesión → Drive (una vez)

Si acaba de ejecutar el **Paso 0.1**, los CSV están bajo `LOCAL_RAW` (`/content/data/raw/`). Esta celda **copia cada año** a Drive si allí aún no están los 12 meses de ese año.

En **sesiones futuras**, Drive ya tiene los datos. Esta celda imprime *omitido* y puede poner **`SKIP_DOWNLOAD = True`** en el Paso 0.1.

```python
meses_sesion = {y: count_month_folders(SESSION_RAW / str(y)) for y in SPINE_CATALOGS}
meses_drive = {y: count_month_folders(DRIVE_RAW / str(y)) for y in SPINE_CATALOGS}
print("Meses con CSV — sesión:", meses_sesion)
print("Meses con CSV — Drive: ", meses_drive)

if spine_has_full_raw(DRIVE_RAW):
    print("Drive ya tiene 2022–2025 con CSV; no hace falta copiar.")
elif spine_has_full_raw(SESSION_RAW):
    print(f"Copiando {SESSION_RAW.resolve()} → {DRIVE_RAW.resolve()} (puede tardar)...")
    DRIVE_RAW.mkdir(parents=True, exist_ok=True)
    for survey_year in SPINE_CATALOGS:
        local_y = SESSION_RAW / str(survey_year)
        drive_y = DRIVE_RAW / str(survey_year)
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
        "No hay 12 meses con CSV ni en sesión ni en Drive. "
        "Ejecute el Paso 0.1 (SKIP_DOWNLOAD=False) o copie week-1-group a Drive."
    )

# Tras copiar (o si Drive ya estaba listo), apuntar RAW_DIR al origen con CSV
RAW_DIR = DRIVE_RAW if spine_has_full_raw(DRIVE_RAW) else resolve_raw_dir()
YEAR_DIR = RAW_DIR / str(YEAR)
print("RAW activo tras Paso 1.3:", RAW_DIR.resolve())
print("Meses por año en RAW activo:", {y: count_month_folders(RAW_DIR / str(y)) for y in SPINE_CATALOGS})
```

**Comprobar:**

```python
n_raw_final = count_month_folders(YEAR_DIR)
print(f"Meses 2024 en RAW activo ({RAW_DIR}): {n_raw_final}")
assert n_raw_final >= 12, (
    f"Solo {n_raw_final} meses con CSV en {YEAR_DIR}. "
    "Revise las líneas 'sesión' vs 'Drive' del Paso 1.2/1.3."
)
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

La **Parte 2** es el paso **Transform** del ETL: deja cada mes listo para cargar al lakehouse. Antes de escribir archivos **Parquet** (formato de cada partición) necesitamos un **motor** que pandas use por debajo. **PyArrow** lee y escribe Parquet (columnas, compresión, tipos). En Colab no viene instalada, por eso la instalamos a continuación:

```python
# pyarrow: motor que pandas usa para leer/escribir archivos Parquet
%pip install -q pyarrow
```

### Paso 2.1. Localizar CSV de un mes

Cada carpeta mensual trae **varios** CSV. Necesitamos dos: **Fuerza de trabajo** (empleo) y **Características generales** (edad, sexo). Como el nombre exacto del archivo cambia entre meses, en vez de escribirlo a mano buscamos por **palabra clave** dentro del nombre.

Estos *helpers* buscan en **`.CSV` y `.csv`** (en Linux/Colab la extensión importa). Cada función lleva **docstring** en español (qué hace, parámetros, retorno). Más adelante verá comentarios **`# Reutiliza …`** cuando llamamos una función ya definida.

```python
def _csv_files(month_dir: Path) -> list[Path]:
    """Lista CSV de una carpeta mensual (.CSV y .csv, sin duplicados).

    Parámetros:
        month_dir: carpeta del mes (p. ej. Ene_2024/).

    Retorna:
        Lista ordenada de rutas a archivos CSV.
    """
    return sorted({*month_dir.glob("*.CSV"), *month_dir.glob("*.csv")})


def _norm_csv_name(path: Path) -> str:
    """Normaliza el nombre de archivo para búsqueda por palabra clave.

    Parámetros:
        path: ruta al CSV.

    Retorna:
        Nombre en minúsculas, sin espacios raros del DANE (\\xa0).
    """
    return re.sub(r"\s+", " ", path.name.lower().replace("\xa0", " "))


def _labour_csv(month_dir: Path) -> Path:
    """Devuelve el CSV de Fuerza de trabajo en una carpeta mensual.

    Parámetros:
        month_dir: carpeta del mes extraído del DANE.

    Retorna:
        Path al primer CSV cuyo nombre contiene PRIMARY_TABLE_KEYWORD.

    Lanza:
        FileNotFoundError con lista de archivos si no hay coincidencia.
    """
    for p in _csv_files(month_dir):
        if PRIMARY_TABLE_KEYWORD in _norm_csv_name(p):
            return p
    names = [p.name for p in _csv_files(month_dir)]
    raise FileNotFoundError(
        f"Sin 'fuerza de trabajo' en {month_dir.name}. Archivos: {names or '(vacío)'}"
    )


def _demog_csv(month_dir: Path) -> Path:
    """Devuelve el CSV de Características generales en una carpeta mensual.

    Parámetros:
        month_dir: carpeta del mes extraído del DANE.

    Retorna:
        Path al CSV cuyo nombre contiene todas las DEMOG_TABLE_KEYWORDS.

    Lanza:
        FileNotFoundError con lista de archivos si no hay coincidencia.
    """
    for p in _csv_files(month_dir):
        if all(kw in _norm_csv_name(p) for kw in DEMOG_TABLE_KEYWORDS):
            return p
    names = [p.name for p in _csv_files(month_dir)]
    raise FileNotFoundError(
        f"Sin características generales en {month_dir.name}. Archivos: {names}"
    )


def month_dirs_for_year(year_dir: Path) -> list[Path]:
    """Lista carpetas mensuales listas para harmonize_month.

    Parámetros:
        year_dir: ruta al año (p. ej. data/raw/2024/).

    Retorna:
        Subcarpetas donde existen labour + demog (omite incompletas con aviso).
    """
    dirs = []
    for p in sorted(year_dir.iterdir()):
        if not p.is_dir():
            continue
        try:
            _labour_csv(p)
            _demog_csv(p)
            dirs.append(p)
        except FileNotFoundError as e:
            print(f"Advertencia — omitido {p.name}: {e}")
    return dirs


# Carpetas de meses que ya tienen CSV extraídos (de la Parte 0 / Drive)
month_dirs_demo = month_dirs_for_year(YEAR_DIR)
demo_month = month_dirs_demo[0]  # usamos el primer mes como ejemplo
print("Mes de ejemplo:", demo_month.name)
print("Fuerza de trabajo:", _labour_csv(demo_month).name)
print("Características:", _demog_csv(demo_month).name)
```

### Paso 2.2. Leer cada tabla por separado

Primero leemos **Fuerza de trabajo** (todas las columnas que necesitamos más adelante):

```python
# Reutiliza _labour_csv y read_geih_csv (Parte 2.1 / Parte 0.1)
labour_path = _labour_csv(demo_month)
labour = read_geih_csv(labour_path)
print(f"Filas fuerza de trabajo: {len(labour):,}")
print("Columnas (muestra):", list(labour.columns[:8]), "...")
print(labour[["DIRECTORIO", "HOGAR", "ORDEN", "PERIODO", "DPTO", "P6240"]].head(2))
```

Después leemos **Características generales**, solo las columnas demográficas que uniremos:

```python
# Reutiliza _demog_csv y read_geih_csv
demog_path = _demog_csv(demo_month)
demog = read_geih_csv(demog_path, usecols=PERSON_KEYS + ["P6040", "P3271"])
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

### Paso 2.5. Decidir el tipo de cada columna y renombrar

Harmonizar **no es solo renombrar**. Por **cada columna** decidimos dos cosas: qué **tipo** tendrá y qué hacer con los **valores faltantes o inválidos**. Estas decisiones dependen de **cómo vamos a usar** la columna después.

- `astype(int)` es **estricto**: falla con un solo faltante y lanza `IntCastingNaNError`. Es justo lo que pasa con `AREA` cuando algún mes trae celdas vacías.
- `pd.to_numeric(..., errors="coerce")` convierte lo no numérico en faltante (`NaN`) en vez de fallar.
- El entero **anulable** `Int64` de pandas **sí admite faltantes** (`<NA>`), útil para códigos enteros (`dpto`, `area`, `edad`).

Veamos la diferencia con un ejemplo pequeño:

```python
ejemplo = pd.Series(["52", "11", "", "x"])  # incluye un vacío y un texto no numérico
print("to_numeric + Int64 (no falla, marca lo inválido como <NA>):")
print(pd.to_numeric(ejemplo, errors="coerce").astype("Int64").tolist())
```

Definimos un ayudante para los códigos enteros y lo reutilizamos:

```python
def a_entero(serie: pd.Series) -> pd.Series:
    """Convierte a entero anulable pandas (Int64), tolerando faltantes.

    Parámetros:
        serie: columna con códigos numéricos (dpto, area, edad, …).

    Retorna:
        Serie Int64; valores no numéricos → <NA>.
    """
    return pd.to_numeric(serie, errors="coerce").astype("Int64")
```

Construimos el DataFrame harmonizado: una fila por persona, con **nombres en español** y el **tipo decidido** por columna. Aquí **no interpretamos** `actividad`, solo la guardamos; quién está ocupado se decide en la lección 4:

```python
harmonized_preview = pd.DataFrame(
    {
        "periodo": (anio * 100 + mes).astype(int),                                  # AAAAMM, siempre presente
        "anio": anio,
        "mes": mes,
        "id_hogar": merged["DIRECTORIO"].astype(str) + "-" + merged["HOGAR"].astype(str),  # clave de texto
        "orden_persona": a_entero(merged["ORDEN"]),                                 # código entero anulable
        "dpto": a_entero(merged["DPTO"]),                                           # código de departamento
        "area": a_entero(merged["AREA"]),                                           # antes fallaba con astype(int)
        "edad": a_entero(merged["P6040"]),                                          # edad en años (entero)
        "sexo": a_entero(merged["P3271"]),                                          # código de sexo
        "actividad": pd.to_numeric(merged["P6240"], errors="coerce"),              # float a propósito (ver nota)
        "factor_expansion": pd.to_numeric(merged["FEX_C18"], errors="coerce"),      # peso de la encuesta (decimal)
    }
)
print("Vista previa harmonizada (5 filas):")
print(harmonized_preview.head(5))
```

**Por qué `actividad` queda como decimal y no `Int64`.** En la lección 4 la compararemos con `actividad == 1` para derivar `ocupado`. Con un decimal, un faltante (`NaN`) se trata como "no ocupado" de forma natural. Con `Int64`, el faltante (`<NA>`) propaga y rompe el filtro booleano. **La forma de harmonizar una columna depende de su uso posterior.**

### Paso 2.6. Consolidación: función `harmonize_month`

Reunimos los pasos 2.1 a 2.5 en **una función reutilizable**. Recibe la carpeta de un mes y devuelve la tabla harmonizada:

```python
def harmonize_month(month_dir: Path) -> pd.DataFrame:
    """Harmoniza un mes GEIH: une tablas, renombra columnas y fija tipos.

    Parámetros:
        month_dir: carpeta con CSV del mes (Fuerza de trabajo + Características).

    Retorna:
        DataFrame una fila/persona con columnas en español (dpto, anio, mes, …)
        y esquema fijo para Parquet (int32/float64 donde corresponde).
    """
    # Reutiliza read_geih_csv, _labour_csv, _demog_csv (Parte 2.1)
    labour = read_geih_csv(_labour_csv(month_dir))
    demog = read_geih_csv(
        _demog_csv(month_dir),
        usecols=PERSON_KEYS + ["P6040", "P3271"],
    )
    # Reutiliza merge por PERSON_KEYS (repaso / L2)
    merged = labour.merge(demog, on=PERSON_KEYS, how="left", validate="many_to_one")
    if "PERIODO" not in merged.columns:
        raise KeyError(f"Falta PERIODO en {month_dir.name}")

    # 3) Claves de tiempo para particionar
    periodo = merged["PERIODO"].astype(int)
    anio = (periodo // 10000).astype(int)
    mes = ((periodo // 100) % 100).astype(int)

    # 4) Renombrar a español y fijar el tipo decidido por columna (ver Paso 2.5)
    out = pd.DataFrame(
        {
            "periodo": (anio * 100 + mes).astype(int),
            "anio": anio,
            "mes": mes,
            "id_hogar": merged["DIRECTORIO"].astype(str) + "-" + merged["HOGAR"].astype(str),
            "orden_persona": a_entero(merged["ORDEN"]),                 # Reutiliza a_entero
            "dpto": a_entero(merged["DPTO"]),
            "area": a_entero(merged["AREA"]),                           # admite faltantes (Int64)
            "edad": a_entero(merged["P6040"]),
            "sexo": a_entero(merged["P3271"]),
            "actividad": pd.to_numeric(merged["P6240"], errors="coerce"),  # float: se compara en lección 4
            "factor_expansion": pd.to_numeric(merged["FEX_C18"], errors="coerce"),
        }
    )
    # Esquema fijo en todas las particiones (evita ArrowTypeError al leer el árbol)
    out["periodo"] = out["periodo"].astype("int32")
    out["anio"] = out["anio"].astype("int32")
    out["mes"] = out["mes"].astype("int32")
    out["actividad"] = out["actividad"].astype("float64")
    out["factor_expansion"] = out["factor_expansion"].astype("float64")
    return out


print("harmonize_month(): consolidada")
```

Probamos la función sobre el mes de ejemplo y mostramos las **primeras 5 filas**:

```python
# Reutiliza harmonize_month (Parte 2.6)
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

## Parte 3. Cargar el lakehouse (Parquet particionado)

Ya tenemos cada mes como una tabla limpia y comparable. Ahora hacemos el paso **Load** del ETL: **cargamos el lakehouse** `geih-spine`.

Recuerde la jerarquía:

1. **Lakehouse** → `data/processed/geih-spine/`
2. **Particiones** → carpetas `anio=2024/mes=MM/` (solo se lee el mes que necesitamos)
3. **Archivos Parquet** → `part-000.parquet` dentro de cada partición (formato columnar, comprimido)

Así no es “guardar un Parquet”, sino **publicar una tabla analítica** en almacenamiento barato. El árbol sirve para la lección 4 y para el trabajo grupal.

**Objetivo.** Recorrer cada carpeta mensual en `data/raw/2024/`, harmonizar y escribir **`anio=2024/mes=MM/part-000.parquet`** dentro del lakehouse. Si ya existe la partición en Drive, puede **omitir** la re-escritura (`SKIP_IF_PARQUET_EXISTS`).

**Ejecución a escala.** Con **`harmonize_month`** ya consolidada, aplicamos el mismo flujo a los 12 meses:

```python
SKIP_IF_PARQUET_EXISTS = True  # no reescribir si la partición del lakehouse ya existe en Drive

# Reutiliza month_dirs_for_year y harmonize_month (Partes 2.1 y 2.6)
month_dirs = month_dirs_for_year(YEAR_DIR)
if not month_dirs:
    raise FileNotFoundError(
        f"No hay CSV bajo {YEAR_DIR}. Monte Drive (Parte 1) o complete week-1-group."
    )

print(f"Carpetas mensuales a procesar: {len(month_dirs)}")
partition_stats: list[dict] = []

for month_dir in month_dirs:
    sample = harmonize_month(month_dir)  # Reutiliza harmonize_month
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
        # Cargar partición del lakehouse (archivo Parquet dentro de anio=/mes=)
        sample.to_parquet(part_file, index=False, use_dictionary=False)
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
print("Parte 3, lakehouse 2024 completo: OK")
```

---

## Parte 4. Benchmark: CSV crudo vs lakehouse

**Objetivo.** Comparar **dos formas de cargar los mismos datos de 2024**: la *forma normal* (leer CSV del DANE y unir tablas, como en la Parte 2) frente a leer el **lakehouse** ya cargado en la Parte 3 (`read_parquet_tree` sobre el árbol `anio=2024/`). Medimos **tiempo**, **memoria** y **tamaño en disco**. El lakehouse gana porque los datos ya están harmonizados, en columnas y particionados; por eso en la lección 4 procesamos sobre el lakehouse y no sobre CSV.

Para que la comparación sea **justa**, ambas rutas producen el mismo año completo (12 meses) en un DataFrame.

```python
def read_parquet_tree(root: Path, columns=None) -> pd.DataFrame:
    """Lee y concatena todas las particiones Parquet bajo root.

    Parámetros:
        root: carpeta del lakehouse o subárbol (p. ej. geih-spine/ o anio=2024/).
        columns: lista opcional de columnas (None = todas).

    Retorna:
        DataFrame con todas las filas de los .parquet encontrados (rglob).

    Lanza:
        FileNotFoundError si no hay archivos .parquet bajo root.
    """
    files = sorted(root.rglob("*.parquet"))
    if not files:
        raise FileNotFoundError(f"Sin Parquet bajo {root}")
    parts = [pd.read_parquet(f, columns=columns) for f in files]
    return pd.concat(parts, ignore_index=True)
```

### Paso 4.1. Forma normal: leer CSV y unir (12 meses)

Recorremos las carpetas de 2024 y aplicamos `harmonize_month` (lee dos CSV por mes y los une). Es lo que tendría que hacer **cada vez** si no hubiera lakehouse:

```python
import time

month_dirs = month_dirs_for_year(YEAR_DIR)  # Reutiliza month_dirs_for_year

t0 = time.perf_counter()
# Reutiliza harmonize_month en bucle (forma cruda sin lakehouse)
df_csv = pd.concat([harmonize_month(m) for m in month_dirs], ignore_index=True)
csv_seconds = round(time.perf_counter() - t0, 2)

mem_csv_mb = df_csv.memory_usage(deep=True).sum() / 1e6
print(f"CSV crudo  -> filas: {len(df_csv):,} | tiempo: {csv_seconds} s | memoria: {mem_csv_mb:.1f} MB")
del df_csv
```

### Paso 4.2. Lakehouse: leer el árbol particionado (12 meses)

Ahora cargamos el **mismo** año desde el lakehouse de la Parte 3 (Parquet bajo `anio=2024/`):

```python
t0 = time.perf_counter()
# Reutiliza read_parquet_tree sobre el subárbol anio=2024/
df_parquet = read_parquet_tree(PROCESSED_DIR / "anio=2024")
parquet_seconds = round(time.perf_counter() - t0, 2)

mem_parquet_mb = df_parquet.memory_usage(deep=True).sum() / 1e6
print(f"Lakehouse  -> filas: {len(df_parquet):,} | tiempo: {parquet_seconds} s | memoria: {mem_parquet_mb:.1f} MB")
```

### Paso 4.3. Tamaño en disco

Los archivos Parquet del lakehouse comprimen por columnas, así que ocupan **mucho menos** que los CSV del DANE:

```python
def dir_size_mb(folder: Path, pattern: str) -> float:
    """Suma tamaño en disco (MB) de archivos que coinciden con un glob.

    Parámetros:
        folder: carpeta raíz para rglob.
        pattern: patrón glob (p. ej. '*.CSV', '*.parquet').

    Retorna:
        Megabytes totales (float).
    """
    return sum(f.stat().st_size for f in folder.rglob(pattern)) / 1e6

csv_mb = dir_size_mb(YEAR_DIR, "*.CSV")
parquet_mb = dir_size_mb(PROCESSED_DIR / "anio=2024", "*.parquet")

resumen = pd.DataFrame(
    {
        "formato": ["CSV crudo", "Lakehouse (Parquet)"],
        "tiempo_seg": [csv_seconds, parquet_seconds],
        "memoria_mb": [round(mem_csv_mb, 1), round(mem_parquet_mb, 1)],
        "disco_mb": [round(csv_mb, 1), round(parquet_mb, 1)],
    }
)
print(resumen.to_string(index=False))
```

**Interpretación.** Leer desde CSV obliga a **re-parsear y re-unir** todo cada vez. El lakehouse ya trae la tabla harmonizada, particionada y en Parquet, así que se lee más rápido y ocupa menos disco.

**Comprobar:**

```python
print(f"CSV: {csv_seconds}s / {csv_mb:.0f}MB | Lakehouse: {parquet_seconds}s / {parquet_mb:.0f}MB")
assert len(df_parquet) > 100_000
assert parquet_mb < csv_mb  # archivos Parquet del lakehouse pesan menos en disco
print("Parte 4, benchmark CSV vs lakehouse: OK")
```

---

## Parte 5. Gobernanza del lakehouse

**Objetivo.** Documentar qué **persistimos** en el lakehouse, mostrar cómo **publicar con privacidad diferencial**, fijar una **regla de retención** y dejar linaje y políticas en `manifest.json`.

### Paso 5.1. Cuasi-identificadores en el lakehouse

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
    """Aplica mecanismo de Laplace a un conteo (privacidad diferencial).

    Parámetros:
        valor_real: conteo verdadero antes de publicar.
        epsilon: presupuesto de privacidad (menor → más ruido).
        sensibilidad: cambio máximo del conteo si entra/sale una persona (1).

    Retorna:
        Conteo con ruido Laplace sumado (float; redondear al publicar).
    """
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

El **linaje** dice de dónde salió el lakehouse (catálogo DANE, versión de harmonización, rutas raw/processed). Es metadato **del conjunto**, no repetido en cada fila Parquet. La **retención** fija cuánto tiempo conservamos el lakehouse.

```python
LINEAGE = {
    "lakehouse": "geih-spine",
    "source_catalog": str(SPINE_CATALOGS[YEAR]),  # catálogo DANE del año (2024 -> 819)
    "harmonisation_version": "2026-06-l3-demo",   # versión del mapeo de la Parte 2
    "raw_path": str(YEAR_DIR),
    "lakehouse_path": str(PROCESSED_DIR),
}
RETENTION_RULE = (
    "Conservar el lakehouse GEIH (Parquet particionado) solo durante el curso (retención: 6 meses) "
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
print("Columnas en el lakehouse:", schema_cols[:6], "...")
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
2. Repite el benchmark de la Parte 4 sobre el lakehouse completo (2022–2025).
3. Documenta **elección de partición** y ética de retención.
4. Continúa en Parte B (procesamiento, lección 4).

Entrega Moodle **martes 16 jun 2026**: ZIP con cuaderno ejecutado + `manifest.json` (sin archivos de datos).

---

## Tareas

Plantillas y plazos en el [hub semana 2](/teaching/26-udenar-big-data/week-2-hub/) y en la [Lección 4 (Procesamiento)](/teaching/26-udenar-big-data/l4-processing/).

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
