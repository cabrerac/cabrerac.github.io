---
course_code: 26-udenar-big-data
title: Introduction to Big Data, methodology, and ecosystems
description: This lecture introduces the course and how we will work along it. It also introduces the Big Data concept, history, context, applications, and ecosystems. We present the data science methodology that will drive our work and explore its first stage, making data available.
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
group_notebook: l1-introduction-group
notebook_language: es
notebook_title: Introducción a big data, metodología y ecosistemas
notebook_description: Práctica de la Lección 1. Poner a disposición datos de la encuesta GEIH del DANE (Access). Instrucciones de entrega en la sección **Tareas** de este cuaderno. Plantillas Word en la página pública de la lección.
---

<!-- RENDER: -->

## Resources

- [Project requirements template](/assets/documents/26-udenar-big-data/plantilla-requerimientos-proyecto.docx): Group deliverable "project_requirements.pdf" inside the group ZIP. Deadline 10/06/2026.
- [L1 individual reflection template](/assets/documents/26-udenar-big-data/plantilla-reflexion-l1.docx): Individual deliverable "l1-reflexion-<student-name>.pdf". Deadline 11/06/2026.

## References

### Week 1 readings

- boyd, d., & Crawford, K. (2012). [Critical questions for big data](https://doi.org/10.1080/1369118X.2012.678878). *Information, Communication & Society*, 15(5), 662–679.
- Zuboff, S. (2019). *The age of surveillance capitalism* (Chapter 1). PublicAffairs. *(Spanish or English edition — distributed by course email.)*
- Mittelstadt, B. D., et al. (2016). [The ethics of algorithms: Mapping the debate](https://doi.org/10.1177/2053951716679679). *Big Data & Society*, 3(2).

### Data source (GEIH)

- [DANE microdata portal](https://microdatos.dane.gov.co/)
- [GEIH 2024 catalog — methodology and documentation](https://microdatos.dane.gov.co/index.php/catalog/819)

<!-- end RENDER: -->

<!-- NOTEBOOK: -->

## Instrucciones

**Propósito.** Este cuaderno es su **práctica de la Lección 1**. Va a **poner a disposición datos de la encuesta del DANE "Gran Encuesta Integrada de Hogares (GEIH)"**. Esa es la primera etapa de nuestra metodología: **Access** (tener los datos disponibles antes de evaluarlos o analizarlos).

En producción, los microdatos nacionales de empleo abarcan **muchos años a escala de gigabytes**. En este laboratorio trabajamos el **año de encuesta 2024** en dos partes:

1. **Parte 1 — un mes** (enero): con el `catalog_id` y `file_id` que entrega el instructor (como en el navegador), descargar un ZIP, extraer, previsualizar y registrar el resultado en `manifest.json`.
2. **Parte 2 — el año completo**: ver **por qué** hace falta **extraer los `file_id` desde la página** get-microdata, automatizar esa lectura y descargar los otros once meses.
3. **Parte 3 — reflexión (individual)**: clasificar las Vs, mapa de las tres A, boceto de arquitectura y comprobación de Access. El **documento de requerimientos del proyecto** (PDF grupal) y la **reflexión individual** (PDF) usan las **plantillas del curso** — ver **Tareas**.

El **mismo patrón** de descarga lo usa el **[cuaderno grupal `l1-introduction-group`](https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-big-data/l1-introduction-group.ipynb)** (**2022–2025**). Plantillas Word: [página de la lección](https://cabrerac.github.io/teaching/26-udenar-big-data/l1-introduction/) (Resources, en inglés).

**Qué hacer (en orden).**

1. Lea **Cómo construir la URL de descarga** más abajo se explica lo que se automatiza en código.
2. Abra este cuaderno en **Google Colab** o ejecútelo en local con Python 3.10+.
3. Ejecute las celdas **de arriba hacia abajo** salvo que una celda indique otra cosa.
4. En celdas **Su turno**, escriba su propio texto o código.
5. En celdas **Comprobar**, ejecute las pruebas y corrija celdas anteriores si algo falla.

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
3. Pulse **Descargar**.
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

El DANE asigna un `catalog_id` por año: `819` para 2024, `853` para 2025 y `900` para 2026. Los archivos de cada año se dividen por mes. Por ejemplo, la lista de archivos de 2024 está [aquí](https://microdatos.dane.gov.co/index.php/catalog/819/get-microdata). Así podemos descargar un archivo por mes. Estas URLs corresponden a los meses de enero y febrero de 2024:

```text
https://microdatos.dane.gov.co/index.php/catalog/819/download/23313
https://microdatos.dane.gov.co/index.php/catalog/819/download/23362
```

También hay un `file_id` por archivo. Por ejemplo, el `file_id` de enero 2024 es `23313`. De esta exploración sale el patrón:


```text
https://microdatos.dane.gov.co/index.php/catalog/{catalog_id}/download/{file_id}
```

| Variable | Significado | Ejemplo (enero 2024) |
|-------|-------------|----------------------|
| `{catalog_id}` | Id DANE del **año de encuesta** | `819` para 2024 |
| `{file_id}` | Id interno de **un ZIP** | `23313` para enero 2024 |

Las celdas siguientes implementan esto en Python. La **Parte 1** usa el enlace de **enero** que ya conoce. La **Parte 2** automatiza la lectura de la página y descarga **el resto de 2024**.

---

## Parte 1 — Descarga de datos para un mes (enero 2024)

### Paso 1 — Configuración — importaciones, constantes y carpetas

Usamos **`pandas`** y **`requests`**, más la biblioteca estándar de Python. La siguiente celda define las variables que vamos a utilizar y crea las carpetas donde almacenaremos los datos descargados.

```python
import json
import re
import time
import zipfile
from pathlib import Path

import pandas as pd
import requests

# Año de práctica L1 — encuesta 2024, catalog_id 819
CATALOG_ID = 819
YEAR = 2024

# Mes de práctica L1 — enero 2024 (file_id del enlace manual arriba)
FILE_ID = 23313
DANE_FILENAME = "Ene_2024.zip"
EXTRACT_DIR = Path(DANE_FILENAME).stem

# Procesamiento de archivos CSV
CSV_SEP = ";"
CSV_ENCODING = "latin-1"
PRIMARY_TABLE_KEYWORD = "fuerza de trabajo"

# Carpetas para almacenar datos descargados
RAW_DIR = Path("data/raw")
YEAR_DIR = RAW_DIR / str(YEAR)
OUTPUTS_DIR = Path("outputs")
YEAR_DIR.mkdir(parents=True, exist_ok=True)
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

print(f"Año: {YEAR}  |  catalog id: {CATALOG_ID}  |  file id: {FILE_ID}  |  archivo: {DANE_FILENAME}")
```

**Comprobar:**

```python
assert CATALOG_ID == 819
assert FILE_ID == 23313
assert DANE_FILENAME == "Ene_2024.zip"
assert YEAR_DIR.is_dir() and OUTPUTS_DIR.is_dir()
print("Configuración: OK")
```

---

## Paso 2 — Descargar el ZIP mensual

Construimos la URL con el patrón de la sección anterior (`catalog_id` + `file_id`). Una descarga directa devuelve un ZIP (GEIH nacional de ese mes).

La función `download_zip` guarda el archivo en **`data/raw/2024/`** y registra tiempo y tamaño para el manifiesto.

### ¿Por qué `stream=True`?

Con **`stream=True`** y `iter_content(...)`, cada trozo se escribe al disco sin cargar todo el ZIP en RAM. Con `stream=False` y `resp.content`, Python puede usar **casi el doble de memoria** un momento. Para **un mes** en Colab el tiempo suele ser similar, la diferencia importa cuando bajan **muchos archivos grandes** o trabajan en un equipo con poca RAM. Esta consideración es importante cuando se piensa en la dimensión **V de volumen**.

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
```

Ahora creamos la URL de descarga directa para el archivo que deseamos descargar e invocamos a la función `download_zip` con los respectivos parámetros.

```python
download_url = (
    f"https://microdatos.dane.gov.co/index.php/catalog/{CATALOG_ID}/download/{FILE_ID}"
)
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
print("Paso 2 — descarga: OK")
```

---

## Paso 3 — Extraer los archivos CSV

Cada ZIP mensual trae **varias** tablas CSV (fuerza de trabajo, vivienda, educación, etc.). Access significa tener **todas** disponibles, para ello implementaremos la función **`extract_csvs`**. Esta función escribe cada archivo `.csv` en una carpeta con el nombre base del ZIP del DANE, p. ej. `data/raw/2024/Ene_2024/`.

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
```

Nuevamente, invocamos la función con los respectivos parámetros.

```python
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
print("Paso 3 — extracción: OK")
```

---

## Paso 4 — Previsualizar la tabla de fuerza de trabajo

El DANE entrega los CSV GEIH con separador **punto y coma** y codificación **`latin-1`**. Si **`read_csv`** falla, revise esos dos ajustes antes de cambiar otra cosa.

Previsualizamos **`Fuerza de trabajo.CSV`** utilizando la funcion `read_csv` de pandas, la cual retorna un dataframe.

```python
df = pd.read_csv(labour_path, sep=CSV_SEP, encoding=CSV_ENCODING, low_memory=False)
n_rows = len(df)
n_cols = len(df.columns)

print(f"Filas: {n_rows:,}  |  Columnas: {n_cols}")
print(f"Columnas (primeras 12): {list(df.columns[:12])}")
df.head()
```

Podemos inspeccionar la información del dataframe.

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

## Paso 5 — Registrar el primer mes en `manifest.json`

Con el fin de documentar el proceso de descaraga guardamos **un objeto JSON por archivo descargado** en el archivo `manifest.json`. Para esto creamos la función `write_manifest`.

```python
def write_manifest(path: Path, entries: list[dict]) -> None:
    path.write_text(json.dumps(entries, indent=2), encoding="utf-8")
```

Ahora utilizamos la función para registrar los datos de la descarga de enero 2024.

```python
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

## Parte 2 — Automatizar el proceso para todo el año 2024

En la Parte 1 descargamos los datos para el mes de enero porque usamos el **`file_id` conocido** (`23313`). Para descargar los datos de todos los meses de 2024 debemos obtener los `file_id` de todos los archivos. Esta tarea se puede hacer manualmente inspeccionando el HTML de la página del DANE. Sin embargo, esta opción no es escalable:

- Hay **once meses más** en 2024 — no conviene copiar a mano once URLs.
- El **`file_id` no se deduce** del nombre `Feb_2024.zip`, el DANE lo asigna al publicar el archivo.
- Si deseamos crear un dataset que incluya más años necesitamos determinar el `file_id` de decenas de archivos por año.

**Solución:** automatizar el proceso de **extraer desde el HTML** cada par `(filename, file_id, url)` y elegir el archivo por **nombre DANE** (`Ene_2024.zip`, `Feb_2024.zip`, …). Eso es lo que hace el navegador al pulsar **Descargar**, aquí lo automatizamos con `requests` y una expresión regular sobre `mostrarModal(...)` que es el objeto HTML que tiene la información que necesitamos.

---

### Paso 1 — URLs del catálogo en código

La URL de **inicio del catálogo** sirve solo para metadatos. **get-microdata** lista los archivos mensuales.

```python
catalog_home = f"https://microdatos.dane.gov.co/index.php/catalog/{CATALOG_ID}"
microdata_page = f"https://microdatos.dane.gov.co/index.php/catalog/{CATALOG_ID}/get-microdata"
print("Inicio del catálogo (solo metadatos):", catalog_home)
print("Get-microdata (archivos mensuales):", microdata_page)
```

---

### Paso 2 — Extraer la lista de archivos desde get-microdata

En la página get-microdata, el DANE coloca cada enlace de descarga como una llamada JavaScript: `mostrarModal('filename', 'url')`. Para extraer los datos, descargamos el HTML usando **`requests`** y utilizamos dos expresiones regulares:

- La primera expresión regular busca todas las llamadas a `mostrarModal` y extrae el nombre del archivo (`filename`) y la URL de descarga (`url`). Básicamente, encuentra patrones de la forma `mostrarModal('Ene_2024.zip', 'https://...download/23313')` dentro del HTML, y captura ambos elementos entre comillas.
- La segunda expresión regular busca, dentro de la URL extraída, el número identificador del archivo (`file_id`). Es decir, detecta el número que aparece después de `/download/` en la ruta como `/download/23313`.

Estas expresiones permiten crear, para cada archivo, una tripleta de datos: nombre del archivo, ID y URL de descarga, de manera automática siguiendo la estructura del HTML de la página.

```python
DOWNLOAD_ONCLICK_RE = re.compile(
    r"mostrarModal\(\s*'([^']+)'\s*,\s*'"
    r"(https://microdatos\.dane\.gov\.co/index\.php/catalog/\d+/download/\d+)\s*'\s*\)",
    re.IGNORECASE,
)
FILE_ID_RE = re.compile(r"/download/(\d+)")
```

La función `list_catalog_downloads` utiliza estas expresiones regulares para obtener todas las tripletas (nombre de archivo, file_id, url de descarga) desde el HTML de la página get-microdata del DANE, automatizando la identificación y extracción de los enlaces de descarga para todos los archivos disponibles en el catálogo.

```python
def list_catalog_downloads(catalog_id: int) -> list[dict]:
    """Obtiene el HTML de get-microdata y parsea tripletas (file_id, filename, url)."""
    page_url = f"https://microdatos.dane.gov.co/index.php/catalog/{catalog_id}/get-microdata"
    resp = requests.get(page_url, timeout=120)
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
```

Ahora podemos listar los archivos a descargar para el año 2024.

```python
# Extraer desde la página todos los file_id (los mismos que ve en el navegador)
all_files = list_catalog_downloads(CATALOG_ID)
print(f"Archivos en catálogo {CATALOG_ID}: {len(all_files)}")
for row in all_files:
    print(f"  {row['file_id']}  {row['filename']}")

january = next(r for r in all_files if r["filename"] == DANE_FILENAME)
print(f"\nEnero en la página: file_id={january['file_id']} (Parte 1 usó {FILE_ID})")
assert january["file_id"] == FILE_ID
```

**Comprobar:**

```python
assert len(all_files) >= 12, "Se esperan 12 archivos mensuales en el catálogo 819"
assert any(r["filename"] == DANE_FILENAME for r in all_files)
print("Paso 2 — lista desde la página: OK")
```

---

### Paso 3 — Una función: descargar y extraer

**`access_file`** descarga y extrae los archivos para un item en la lista `all_files`. Cada item tiene `url`, `file_id` y `filename`. Esta función reutiliza las funciones definidas en el paso 1 **`download_zip`** y **`extract_csvs`**. Esta es una lección importante de nuestro ejercicio: debemos diseñar nuestro código de forma modular y reutilizar funciones para crear soluciones más complejas.

```python
def access_file(
    item: dict,
    year_dir: Path,
    *,
    skip_if_exists: bool = True,
) -> dict:
    """
    Usar item de all_files → descargar ZIP → extraer CSVs → registro de manifiesto.
    """
    url = item["url"]
    file_id = item["file_id"]
    filename = item["filename"]
    zip_path = year_dir / filename
    out_dir = year_dir / Path(filename).stem

    if skip_if_exists and out_dir.is_dir() and any(out_dir.glob("*.CSV")):
        return {
            "method": "http",
            "survey_year": YEAR,
            "catalog_id": CATALOG_ID,
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
        "catalog_id": CATALOG_ID,
        "file_id": file_id,
        "filename": filename,
        "extract_dir": str(out_dir),
        "seconds": seconds,
        "bytes_downloaded": nbytes,
        "notes": f"extracted {len(files)} CSVs",
        "fallback_used": False,
    }
```

### Paso 4 — Descargar los meses restantes

Aquí usamos la lista `all_files` del Paso 2 y omitimos enero porque ya está en disco desde la Parte 1.

```python
entries = [manifest_entry]
for row in all_files:
    if row["filename"] == DANE_FILENAME:
        continue
    print("Descargando:", row["filename"])
    entries.append(access_file(row, YEAR_DIR))

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

Use los archivos que ya tiene en disco: **todo 2024** si terminó la Parte 2, o **solo enero** si aún no completó el bucle de meses. Las preguntas siguientes aplican en ambos casos (con menos detalle si solo tiene un mes).

### Paso 1 — Clasificar las Vs (Su turno)

Para cada **V** (volumen, velocidad, variedad, veracidad), escriba **una oración** basada en **su descarga** (tamaños en `manifest.json`, tiempos, tablas en disco) — no una definición de libro.

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
print("Parte 3, Paso 1 — tabla Vs: OK")
```

---

### Paso 2 — Mapa de las tres A (Su turno)

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

### Paso 3 — Diagrama de arquitectura (Su turno)

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
print("(La figura irá en la sección Pipeline del PDF de requerimientos del proyecto — cuaderno grupal.)")
```

---

### Paso 4 — Párrafo de despliegue (Su turno)

Imagine su pipeline en producción — no solo en Colab. En **3–5 oraciones**, indique si correría en **nube**, **borde (edge)** o **híbrido**, y si el trabajo es por **lotes (batch)** o **interactivo**. Indique **un supuesto** que esté asumiendo.

```python
deployment_paragraph = """
SU TEXTO AQUÍ
"""
print(deployment_paragraph.strip())
```

---

### Paso 5 — Encaje y límites (Su turno)

Los métodos de big data no siempre son la herramienta correcta. Para **la pregunta de decisión de su proyecto** (la definirán en el PDF de requerimientos), ¿dónde ayudaría un stack distribuido? ¿Dónde sería **exceso** a la escala que accedió hoy?

```python
fit_and_limits = """
SU TEXTO AQUÍ
"""
print(fit_and_limits.strip())
```

---

### Paso 6 — Comprobación de Access completado

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

## Tareas

Esta sección define **qué entregar en Moodle**. Las plantillas Word están en la [página de la lección](https://cabrerac.github.io/teaching/26-udenar-big-data/l1-introduction/) (descargas en inglés); complételas en Word y expórtelas a PDF.

### Práctica individual (no calificada)

Cuaderno **`l1-introduction`** (este Colab) — Partes 1–3: Access 2024 + reflexión en el cuaderno. **No** entregue este `.ipynb` en Moodle.

### Trabajo en grupo (60 % de la formativa L1)

Use el Colab **`l1-introduction-group`**. Entregar un ZIP **`l1-introduction-<nombre-grupo>.zip`** hasta el **miércoles 10 de junio de 2026, 23:59 (Colombia)**:

| Archivo en el ZIP | Descripción |
|-------------------|-------------|
| `l1-introduction-<nombre-grupo>.ipynb` | Cuaderno grupal ejecutado — descarga GEIH **2022–2025** + registro de contribución |
| `manifest.json` | Un registro por cada archivo descargado del DANE |
| `project_requirements.pdf` | Requerimientos del proyecto (desde la plantilla Word del curso) |

### Reflexión individual (40 % de la formativa L1)

Entregar **un PDF por estudiante** hasta el **jueves 11 de junio de 2026, 23:59 (Colombia)** — **no** va dentro del ZIP grupal.

| Entregable | Descripción |
|------------|-------------|
| `l1-reflexion-<nombre-estudiante>.pdf` | Reflexión semana 1 (plantilla Word del curso) |

**Consigna:** *Si el DANE restringiera mañana las descargas masivas, ¿qué parte de su configuración de Access cambiaría primero — y qué implicaría eso para la rendición de cuentas pública?*

<!-- end NOTEBOOK: -->
