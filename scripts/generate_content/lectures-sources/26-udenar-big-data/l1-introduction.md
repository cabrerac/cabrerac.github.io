---
course_code: 26-udenar-big-data
title: Introduction to Big Data, methodology, and ecosystems
description: Esta lección presenta el curso y cómo trabajaremos. Introduce el concepto de Big Data, su contexto y ecosistemas. Presentamos la metodología de ciencia de datos y exploramos su primera etapa — poner los datos a disposición (Access).
session: 1
start_time: 07:00 am
end_time: 01:00 pm
hours: 5
author: Christian Cabrera Jojoa
email: chc79@cam.ac.uk
position: Assistant Research Professor
department: Department of Computer Science and Technology
institution: University of Cambridge
layout: lecture
lecture_code: l1-introduction
lecture_date: 06/06/2026
permalink: /teaching/26-udenar-big-data/l1-introduction/
visible: false
---

<!-- NOTEBOOK: -->

## Instrucciones

**Propósito.** Este cuaderno es su **práctica de la Lección 1**. Va a **poner a disposición datos de la encuesta del DANE "Gran Encuesta Integrada de Hogares (GEIH)"**. Esa es la primera etapa de nuestra metodología: **Access** (tener los datos disponibles antes de evaluarlos o analizarlos).

En producción, los microdatos nacionales de empleo abarcan **muchos años a escala de gigabytes o terabytes**. En este laboratorio aprende en dos pasos sobre el **año de encuesta 2024**:

1. **Parte 1 — un mes** (enero): raspar la página, descargar un ZIP, extraer, previsualizar, registrar el resultado.
2. **Parte 2 — el año completo**: reutilizar el mismo código en un bucle para los 12 archivos mensuales del catálogo **819**.

El **mismo patrón** lo usará su grupo después al descargar **2022–2025** en el cuaderno grupal: id de catálogo → raspar lista de archivos → descargar → extraer → manifiesto.

**Qué hacer (en orden).**

1. Lea **Cómo construir la URL de descarga** más abajo — explica lo que automatizamos en código.
2. Abra este cuaderno en **Google Colab** o ejecútelo en local con Python 3.10+.
3. Ejecute las celdas **de arriba hacia abajo** salvo que una celda indique otra cosa.
4. En celdas **Su turno**, escriba su propio texto o código.
5. En celdas **Comprobar**, ejecute las pruebas y corrija celdas anteriores si algo falla.
6. Lleve al sábado las preguntas del **diario de lectura**.

**Estructura de carpetas** (la celda de configuración crea estas rutas):

| Ruta | Función |
|------|---------|
| `data/raw/2024/` | ZIP de 2024 y carpetas con CSV extraídos |
| `outputs/` | Diagramas y exportaciones para la tarea |
| `manifest.json` | Registro de acceso (una fila por archivo descargado) |

---

## Cómo construir la URL de descarga

El DANE publica microdatos GEIH en **[microdatos.dane.gov.co](https://microdatos.dane.gov.co/)**. Para descargar un archivo puede hacerlo manualmente así:

**Ruta manual (navegador)**:

1. Abra `https://microdatos.dane.gov.co/index.php/catalog/819/get-microdata`
2. Busque **enero 2024** (`Ene_2024`, `GEIH_2024_ENE`, o similar).
3. Pulse **Descargar** (o inspeccione el enlace). La URL debe contener **`/download/`**.
4. Ejemplo para enero 2024:
   `https://microdatos.dane.gov.co/index.php/catalog/819/download/23313`

Ese proceso manual sirve, pero no es práctico cuando necesitamos muchos archivos en varios años. Podemos automatizar las descargas. El primer paso es obtener una **URL de descarga directa**, construida al explorar el sitio del DANE.

**Patrón de host y ruta**

Como ejemplo, estos enlaces corresponden a la descripción de la encuesta para 2024, 2025 y 2026.

```text
https://microdatos.dane.gov.co/index.php/catalog/819/
https://microdatos.dane.gov.co/index.php/catalog/853/
https://microdatos.dane.gov.co/index.php/catalog/900/
```

El DANE asigna un `catalog_id` por año: `819` para 2024, `853` para 2025 y `900` para 2026. Los archivos de cada año se dividen por mes. Por ejemplo, la lista de archivos de 2024 está [aquí](https://microdatos.dane.gov.co/index.php/catalog/819/get-microdata). Así podemos descargar un archivo por mes. Estas URLs son enero y febrero de 2024:

```text
https://microdatos.dane.gov.co/index.php/catalog/819/download/23313
https://microdatos.dane.gov.co/index.php/catalog/819/download/23362
```

También hay un `file_id` por archivo. Por ejemplo, el `file_id` de enero 2024 es `23313`. De esta exploración sale el patrón:


```text
https://microdatos.dane.gov.co/index.php/catalog/{catalog_id}/download/{file_id}
```

| Pieza | Significado | Ejemplo (enero 2024) |
|-------|-------------|----------------------|
| `{catalog_id}` | Id DANE del **año de encuesta** | `819` para 2024 |
| `{file_id}` | Id interno de **un ZIP subido** | `23313` para enero 2024 |

**No** puede deducir `{file_id}` solo del nombre del archivo sin raspar get-microdata antes — siempre léalo en la página (navegador o código). La página inicial del catálogo (`…/catalog/819/`) **no** es un enlace de descarga. Si pide esa URL obtiene HTML, no un ZIP.

Las celdas siguientes implementan esto en Python. La **Parte 1** recorre **un mes** paso a paso. La **Parte 2** descarga **el resto de 2024**.

---

## Parte 1 — Un mes (enero 2024)

### Configuración — importaciones, constantes y carpetas

Usamos **`pandas`** y **`requests`**, más la biblioteca estándar de Python. La siguiente celda crea las carpetas. El instructor entrega los valores de **`catalog_id`** (año de encuesta → catálogo). Los **`file_id`** siempre salen de raspar get-microdata en el Paso 2 — nunca van fijos en Configuración.

Ejecute la celda una vez.

```python
import json
import re
import time
import zipfile
from pathlib import Path

import pandas as pd
import requests

# Año de práctica L1 — encuesta 2024, catálogo 819 (lo entrega el instructor)
CATALOG_BY_YEAR = {2022: 771, 2023: 782, 2024: 819, 2025: 853}
YEAR = 2024
CATALOG_ID = CATALOG_BY_YEAR[YEAR]

# Primer mes lo descargamos a mano (Parte 1); file_id sale del raspado en el Paso 2
L1_DANE_FILENAME = "Ene_2024.zip"

CSV_SEP = ";"
CSV_ENCODING = "latin-1"
PRIMARY_TABLE_KEYWORD = "fuerza de trabajo"

RAW_DIR = Path("data/raw")
YEAR_DIR = RAW_DIR / str(YEAR)
OUTPUTS_DIR = Path("outputs")
YEAR_DIR.mkdir(parents=True, exist_ok=True)
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

print(f"Año: {YEAR}  |  catalog id: {CATALOG_ID}  |  primer archivo: {L1_DANE_FILENAME}")
```

**Comprobar:**

```python
assert CATALOG_ID == 819
assert L1_DANE_FILENAME.endswith(".zip")
assert YEAR_DIR.is_dir() and OUTPUTS_DIR.is_dir()
print("Configuración: OK")
```

---

## Paso 1 — Confirmar las páginas del catálogo en código

En la sección anterior abrimos get-microdata en el navegador. Aquí construimos las mismas URLs en Python para que los pasos siguientes las llamen solos. En la Lección 1 usamos el **catálogo 819** y el archivo **`Ene_2024.zip`** — el **`file_id`** se lee de la página raspada en el Paso 2.

La URL de **inicio del catálogo** sirve solo para metadatos. La URL **get-microdata** lista los archivos mensuales. La URL de **descarga** (Paso 2) es la que devuelve el ZIP.

```python
def get_microdata_page_url(catalog_id: int) -> str:
    return f"https://microdatos.dane.gov.co/index.php/catalog/{catalog_id}/get-microdata"

catalog_home = f"https://microdatos.dane.gov.co/index.php/catalog/{CATALOG_ID}"
microdata_page = get_microdata_page_url(CATALOG_ID)
print("Inicio del catálogo (solo metadatos):", catalog_home)
print("Get-microdata (archivos mensuales):", microdata_page)
print("Forma esperada de descarga:", f".../catalog/{CATALOG_ID}/download/{{file_id}}")
```

---

## Paso 2 — Resolver la URL de descarga directa

En get-microdata, el DANE incrusta cada enlace en una llamada JavaScript: `mostrarModal('filename', 'url')`. Pedimos esa página con **`requests`**, parseamos cada fila en **`file_id`**, **`filename`** y **`url`**, y elegimos la fila cuyo **filename** coincide con el archivo de práctica de Configuración.

Implemente las funciones siguientes y resuelva la URL para **`Ene_2024.zip`**.

```python
DOWNLOAD_ONCLICK_RE = re.compile(
    r"mostrarModal\(\s*'([^']+)'\s*,\s*'"
    r"(https://microdatos\.dane\.gov\.co/index\.php/catalog/\d+/download/\d+)\s*'\s*\)",
    re.IGNORECASE,
)
FILE_ID_RE = re.compile(r"/download/(\d+)")


def list_catalog_downloads(catalog_id: int) -> list[dict]:
    """Obtiene el HTML de get-microdata y parsea tripletas (file_id, filename, url)."""
    resp = requests.get(get_microdata_page_url(catalog_id), timeout=120)
    resp.raise_for_status()
    seen: set[int] = set()
    files: list[dict] = []
    for filename, url in DOWNLOAD_ONCLICK_RE.findall(resp.text):
        url = url.strip()
        m = FILE_ID_RE.search(url)
        if not m:
            continue
        file_id = int(m.group(1))
        if file_id in seen:
            continue
        seen.add(file_id)
        files.append(
            {
                "file_id": file_id,
                "filename": filename.strip(),
                "url": url,
            }
        )
    return sorted(files, key=lambda row: row["filename"].lower())


def find_download_by_filename(catalog_id: int, dane_filename: str) -> dict:
    for item in list_catalog_downloads(catalog_id):
        if item["filename"] == dane_filename:
            return item
    raise ValueError(
        f"No hay {dane_filename!r} en el catálogo {catalog_id}. "
        f"Abra {get_microdata_page_url(catalog_id)} y revise la columna de nombres de archivo."
    )


def validate_download_url(url: str) -> None:
    if "/download/" not in url:
        raise ValueError(
            "Esa URL parece una página de catálogo, no un archivo de datos. "
            "Use el enlace de Descargar que contiene /download/."
        )
```

```python
# Raspar todos los file_id de la página (los mismos que vio en el navegador)
for row in list_catalog_downloads(CATALOG_ID):
    print(row["file_id"], row["filename"])

download = find_download_by_filename(CATALOG_ID, L1_DANE_FILENAME)
FILE_ID = download["file_id"]  # descubierto en la página — no fijo en Configuración
download_url = download["url"]
DANE_FILENAME = download["filename"]
EXTRACT_DIR = Path(DANE_FILENAME).stem

validate_download_url(download_url)
print("file_id descubierto:", FILE_ID)
print("Nombre DANE:", DANE_FILENAME)
print("URL de descarga directa:", download_url)
```

**Comprobar:**

```python
assert "/download/" in download_url, "Necesita un enlace /download/, no la página inicial del catálogo"
assert str(CATALOG_ID) in download_url
assert str(FILE_ID) in download_url
assert DANE_FILENAME == L1_DANE_FILENAME
print("Paso 2 — URL de descarga: OK")
```

---

## Paso 3 — Descargar el ZIP mensual

Una URL de descarga directa devuelve un ZIP (GEIH nacional de ese mes). Lo guardamos en streaming en `data/raw/` y registramos tiempo y tamaño — usará ambos números en el **manifiesto** y en la discusión de las **Vs**.

Todo ZIP válido empieza con los bytes **`PK`**. Si ve otra cosa, la URL estaba mal — suele ser la página de descripción del catálogo en lugar de `/download/…`.

```python
def download_zip(url: str, dest: Path, timeout: int = 600) -> tuple[float, int]:
    """Descarga url a dest en streaming; devuelve (segundos, bytes). Falla si no es ZIP."""
    t0 = time.perf_counter()
    with requests.get(url.strip(), stream=True, timeout=timeout) as resp:
        resp.raise_for_status()
        with dest.open("wb") as fh:
            for chunk in resp.iter_content(chunk_size=1 << 20):
                if chunk:
                    fh.write(chunk)
    elapsed = round(time.perf_counter() - t0, 3)
    magic = dest.read_bytes()[:2]
    if magic != b"PK":
        raise ValueError(
            f"El archivo descargado no es un ZIP (obtuvo {magic!r}). "
            "Use la URL /download/ de get-microdata, no la página inicial del catálogo."
        )
    return elapsed, dest.stat().st_size


zip_path = YEAR_DIR / DANE_FILENAME
download_seconds, bytes_downloaded = download_zip(download_url, zip_path)

print(f"Guardado: {zip_path}")
print(f"Tamaño: {bytes_downloaded / 1e6:.2f} MB")
print(f"Tiempo: {download_seconds} s")
```

**Comprobar:**

```python
assert zip_path.is_file(), "Falta el archivo ZIP"
assert zip_path.read_bytes()[:2] == b"PK", "No es ZIP — corrija la URL de descarga"
assert bytes_downloaded > 1_000_000, "El ZIP parece demasiado pequeño"
print("Paso 3 — descarga: OK")
```

---

## Paso 4 — Extraer los archivos CSV

Cada ZIP mensual trae **varias** tablas CSV (fuerza de trabajo, vivienda, educación, etc.). Access significa tener **todas** en disco, no solo la que analizamos primero.

Implemente **`extract_csvs`** abajo. Debe escribir cada miembro `.csv` en una carpeta con el nombre base del ZIP del DANE, p. ej. `data/raw/2024/Ene_2024/`.

```python
def extract_csvs(zip_path: Path, dest_dir: Path) -> list[Path]:
    """Extrae cada miembro .csv; devuelve lista ordenada de rutas."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "r") as zf:
        csv_members = [n for n in zf.namelist() if n.lower().endswith(".csv")]
        if not csv_members:
            raise ValueError(f"No CSV files inside {zip_path.name}")
        for name in csv_members:
            target = dest_dir / Path(name).name
            with zf.open(name) as src, target.open("wb") as dst:
                dst.write(src.read())
    return sorted(dest_dir.glob("*.CSV")) + sorted(dest_dir.glob("*.csv"))


extract_dir = YEAR_DIR / EXTRACT_DIR
csv_files = extract_csvs(zip_path, extract_dir)
total_csv_bytes = sum(p.stat().st_size for p in csv_files)

print(f"Extraídos {len(csv_files)} archivo(s) CSV → {extract_dir}/\n")
for p in csv_files:
    print(f"{p.stat().st_size / 1e6:8.2f} MB  {p.name}")
print(f"\nTotal extraído: {total_csv_bytes / 1e6:.2f} MB")
```

**Comprobar:**

```python
assert len(csv_files) >= 1
labour_path = next(
    p for p in csv_files if PRIMARY_TABLE_KEYWORD in p.name.lower().replace("\xa0", " ")
)
print("Tabla principal de fuerza de trabajo:", labour_path.name)
print("Paso 4 — extracción: OK")
```

---

## Paso 5 — Previsualizar la tabla de fuerza de trabajo

El DANE entrega los CSV GEIH con separador **punto y coma** y codificación **`latin-1`**. Si **`read_csv`** falla, revise esos dos ajustes antes de cambiar otra cosa.

Previsualizamos **`Fuerza de trabajo.CSV`**. La mayoría de grupos empieza por esta tabla; los demás CSV del Paso 4 quedan en disco para semanas posteriores.

```python
df = pd.read_csv(labour_path, sep=CSV_SEP, encoding=CSV_ENCODING, low_memory=False)
n_rows = len(df)
n_cols = len(df.columns)

print(f"Filas: {n_rows:,}  |  Columnas: {n_cols}")
print(f"Columnas (primeras 12): {list(df.columns[:12])}")
df.head()
```

```python
df.info()
```

**Comprobar:**

```python
assert n_rows > 10_000, "Se espera un mes nacional (decenas de miles de filas)"
assert "DPTO" in df.columns, "Se espera la columna DPTO (código de departamento)"
print("Paso 5 — previsualización: OK")
```

---

## Paso 6 — Registrar el primer mes en `manifest.json`

Guardamos **un objeto JSON por archivo descargado**. La Parte 1 añade enero; la Parte 2 agrega los demás meses.

```python
def write_manifest(path: Path, entries: list[dict]) -> None:
    path.write_text(json.dumps(entries, indent=2), encoding="utf-8")


manifest_entry = {
    "method": "http",
    "survey_year": YEAR,
    "catalog_id": CATALOG_ID,
    "file_id": FILE_ID,
    "filename": DANE_FILENAME,
    "extract_dir": str(extract_dir),
    "seconds": download_seconds,
    "bytes_downloaded": bytes_downloaded,
    "notes": f"extracted {len(csv_files)} CSVs ({total_csv_bytes} bytes)",
    "fallback_used": False,
}
manifest_path = Path("manifest.json")
write_manifest(manifest_path, [manifest_entry])
print(manifest_path.read_text(encoding="utf-8"))
```

**Comprobar:**

```python
assert manifest_path.is_file()
data = json.loads(manifest_path.read_text(encoding="utf-8"))
assert data[0]["method"] == "http"
assert data[0]["bytes_downloaded"] > 0
print("Parte 1 completa — un mes en disco.")
```

---

## Parte 2 — Año completo de encuesta 2024

Ya descargó **enero**. Ahora envuelva los Pasos 2–6 en una función y llámela para **cada otro mes** listado en la misma página get-microdata.

### Paso 7 — Una función: raspar, descargar, extraer

```python
def access_file(
    catalog_id: int,
    dane_filename: str,
    year_dir: Path,
    *,
    skip_if_exists: bool = True,
) -> dict:
    """
    Raspar URL → descargar ZIP (nombre DANE) → extraer CSVs → devolver un registro de manifiesto.
    """
    item = find_download_by_filename(catalog_id, dane_filename)
    url = item["url"]
    file_id = item["file_id"]
    filename = item["filename"]
    validate_download_url(url)
    zip_path = year_dir / filename
    out_dir = year_dir / Path(filename).stem

    if skip_if_exists and out_dir.is_dir() and any(out_dir.glob("*.CSV")):
        return {
            "method": "http",
            "survey_year": YEAR,
            "catalog_id": catalog_id,
            "file_id": file_id,
            "filename": filename,
            "extract_dir": str(out_dir),
            "seconds": 0.0,
            "bytes_downloaded": zip_path.stat().st_size if zip_path.is_file() else 0,
            "notes": "omitido (ya extraído)",
            "fallback_used": False,
        }

    seconds, nbytes = download_zip(url, zip_path)
    files = extract_csvs(zip_path, out_dir)
    return {
        "method": "http",
        "survey_year": YEAR,
        "catalog_id": catalog_id,
        "file_id": file_id,
        "filename": filename,
        "extract_dir": str(out_dir),
        "seconds": seconds,
        "bytes_downloaded": nbytes,
        "notes": f"extracted {len(files)} CSVs",
        "fallback_used": False,
    }
```

### Paso 8 — Descargar los meses restantes

Raspe de nuevo la lista de archivos y recorra en bucle. Omita enero — ya lo tiene de la Parte 1.

```python
all_files = list_catalog_downloads(CATALOG_ID)
print(f"Archivos en catálogo {CATALOG_ID}: {len(all_files)}")
for row in all_files:
    print(f"  {row['file_id']}  {row['filename']}")

entries = [manifest_entry]
for row in all_files:
    if row["filename"] == L1_DANE_FILENAME:
        continue
    print("Descargando:", row["filename"])
    entries.append(access_file(CATALOG_ID, row["filename"], YEAR_DIR))

write_manifest(manifest_path, entries)
total_bytes = sum(e["bytes_downloaded"] for e in entries)
print(f"\nFilas del manifiesto: {len(entries)}  |  bytes descargados en total: {total_bytes / 1e9:.3f} GB")
print(manifest_path.read_text(encoding="utf-8"))
```

**Comprobar:**

```python
assert len(entries) == len(all_files), "Se espera una fila de manifiesto por mes"
assert len(list(YEAR_DIR.glob("*.zip"))) == len(all_files)
print("Parte 2 completa — año 2024 completo en disco.")
```

---

## Parte 3 — Reflexionar sobre lo descargado

Use **todo 2024** (o solo enero si la Parte 2 sigue en curso) para las preguntas siguientes.

### Paso 9 — Clasificar las Vs (Su turno)

Ya tiene archivos reales en disco. Para cada **V** (volumen, velocidad, variedad, veracidad), escriba **una oración** basada en **esta descarga** — no una definición genérica. Sus respuestas alimentan el **diario de lectura** (pregunta 8).

```python
vs_table = {
    "volume": "",    # e.g. ZIP size, number of CSVs, row count
    "velocity": "",  # e.g. how often DANE publishes; your download time
    "variety": "",   # e.g. multiple CSV tables, codes vs labels
    "veracity": "",  # e.g. official survey, weights, missing codes
}
# SU TURNO — reemplace las cadenas vacías con una oración cada una
vs_table["volume"] = "..."
vs_table["velocity"] = "..."
vs_table["variety"] = "..."
vs_table["veracity"] = "..."

for v, sentence in vs_table.items():
    print(f"{v}: {sentence}")
```

**Comprobar:**

```python
for v, sentence in vs_table.items():
    assert isinstance(sentence, str) and len(sentence.strip()) >= 20, f"Escriba al menos una oración para {v}"
print("Paso 9 — tabla Vs: OK")
```

---

## Paso 10 — Mapa de las tres A (Su turno)

Nuestra metodología tiene tres etapas: **Access → Assess → Address**. En este cuaderno completa **Access** (archivos locales y registrados). **Assess** y **Address** vienen en lecciones posteriores.

Complete la tabla: ¿qué hará su grupo en Assess y Address?

```python
three_as = """
| Stage | L1 status | What happens next (your group) |
|-------|-----------|--------------------------------|
| Access | HECHO en este cuaderno | … |
| Assess | Aún no | … |
| Address | Aún no | … |
"""
# SU TURNO — reemplace los … (2–4 viñetas en total entre Assess y Address)
print(three_as)
```

---

## Paso 11 — Diagrama de arquitectura (Su turno)

Bosqueje cómo se mueven los datos del DANE a la decisión de su grupo. Descargue la plantilla del curso, reetiquétela para su **arquetipo de decisión** (ver [case shell](https://github.com/cabrerac/cabrerac.github.io/blob/main/work-space/teaching/big-data/planning/case-shell.md)) y guarde como **`outputs/architecture.svg`**.

Plantilla: [big-data-pipeline-template.svg](https://cabrerac.github.io/assets/media/diagrams/big-data-pipeline-template.svg)

En Colab puede obtener la plantilla con la celda siguiente y editarla en draw.io, Inkscape u otro editor SVG.

```python
template_url = "https://cabrerac.github.io/assets/media/diagrams/big-data-pipeline-template.svg"
template_path = OUTPUTS_DIR / "big-data-pipeline-template.svg"
if not template_path.is_file():
    r = requests.get(template_url, timeout=60)
    r.raise_for_status()
    template_path.write_bytes(r.content)
print("Plantilla guardada en:", template_path)
print("Su turno: reetiquete el diagrama y guarde como outputs/architecture.svg")
```

---

## Paso 12 — Párrafo de despliegue (Su turno)

Imagine su pipeline en producción — no solo en Colab. En **3–5 oraciones**, indique si correría en **nube**, **borde (edge)** o **híbrido**, y si el trabajo es por **lotes (batch)** o **interactivo**. Indique **un supuesto** que esté asumiendo.

```python
deployment_paragraph = """
SU TEXTO AQUÍ
"""
print(deployment_paragraph.strip())
```

---

## Paso 13 — Encaje y límites (Su turno)

Los métodos de big data no siempre son la herramienta correcta. Para **su** pregunta del charter, ¿dónde ayudaría un stack distribuido? ¿Dónde sería **exceso** a la escala que accedió hoy?

```python
fit_and_limits = """
SU TEXTO AQUÍ
"""
print(fit_and_limits.strip())
```

---

## Paso 14 — Borrador del charter (Su turno)

Redacte el **`charter.md`** de su grupo en la celda siguiente. Después del **sábado**, fusionen una versión por grupo con la [plantilla de charter](https://github.com/cabrerac/cabrerac.github.io/blob/main/work-space/teaching/big-data/planning/charter-template.md). Los **encabezados** deben coincidir exactamente (en inglés) para la verificación automática.

```python
charter_draft = """
# Group G? — Project charter (DRAFT)

## Metadata
- group: G?
- members: ...
- archetype: resource allocation | risk / early warning | monitoring
- created: YYYY-MM-DD

## Stakeholders
...

## Decision question
...

## Subset
- Years: ...
- Regions / departments: ...
- Population segment: ...
- Variables of primary interest: ...

## Success criteria
...

## Ethical concern + reading
(one case-shell section-6 topic + Zuboff Ch. 1)

## Roles and contribution plan
- Name 1 — ...
"""
print(charter_draft)
```

---

## Comprobación de Access completado

Ejecute esto después de la **Parte 1** (mínimo) o la **Parte 2** (año completo). Imprime **`ACCESS_OK`** cuando la ruta principal de Access funcionó.

```python
def _ok(name, fn):
    try:
        ok = bool(fn())
    except Exception:
        ok = False
    print(f"{name}: {'OK' if ok else 'incompleto'}")
    return ok

manifest_rows = len(json.loads(manifest_path.read_text(encoding="utf-8")))
checks = [
    ("ZIP en disco", lambda: zip_path.is_file() and zip_path.read_bytes()[:2] == b"PK"),
    ("CSV extraídos", lambda: len(csv_files) >= 1),
    ("Previsualización fuerza de trabajo", lambda: n_rows > 10_000),
    ("manifest.json", lambda: manifest_path.is_file()),
    ("Año completo (opcional)", lambda: manifest_rows >= 12),
]
passed = sum(_ok(name, fn) for name, fn in checks)
print(f"\nACCESS_CHECKS={passed}/{len(checks)}")
if passed >= 4:
    print("ACCESS_OK — completó la ruta de Access de L1 (un mes o más).")
```

---

## Tarea (grupo — después del sábado)

Entregar en Moodle (normalmente el **miércoles** después de L1). El **cuaderno grupal** (aparte de esta práctica individual) descargará **2022–2025** con el mismo patrón y los catalog ids que entregamos allí. Cada grupo ejecuta la descarga.

| Entregable | Notas |
|------------|--------|
| **`charter.md`** | Plantilla completa; incluya **Ethical concern + reading** (cite **Zuboff Ch. 1** por nombre) |
| **`architecture.svg`** | Pipeline reetiquetado del Paso 11 |
| **`manifest.json`** | Un registro por archivo DANE en 2022–2025 |
| **`data/raw/`** | ZIP y CSV extraídos bajo carpetas por año |

No hay **`L1_output.parquet`** en esta lección. Los artefactos de L1 son el charter, el diagrama y el registro de acceso.

---

## Registro de contribución (grupo)

Cada integrante añade una línea. Nombre al **escriba de L1** — quien consolida el Colab canónico de la semana.

```python
contribution_log = """
- Name 1 — ...
- Name 2 — ...
- Name 3 — ...
- Name 4 — ...
L1 scribe: ...
"""
print(contribution_log)
```

---

## Reflexión (individual — Moodle después de la tarea)

Entregar en Moodle. Enlace **una decisión de arquitectura** (nube, borde o batch) con **privacidad, daño o gobernanza**, citando **boyd & Crawford** o **Zuboff cap. 1**.

**Consigna:** *Si el DANE restringiera mañana las descargas masivas, ¿qué parte de su configuración de Access cambiaría primero — y qué implicaría eso para la rendición de cuentas pública?*

<!-- end NOTEBOOK: -->
