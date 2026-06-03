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
notebook_language: es
notebook_title: Introducción a big data, metodología y ecosistemas
notebook_description: Práctica individual de la Lección 1. Poner a disposición datos GEIH (Access). Entregas de la semana 1 en la página de la Lección 2.
---

<!-- RENDER: -->

### Resources

- [Project definition](/assets/documents/26-udenar-big-data/project-definition-big-data.pdf)
- [Individual Notebook](https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-big-data/l1-introduction.ipynb)
- [DANE data website](https://microdatos.dane.gov.co/)
- [GEIH 2024 — documentation](https://microdatos.dane.gov.co/index.php/catalog/819)

**Templates and deliverables for week 1** are in [Lecture 2 webpage](/teaching/26-udenar-big-data/l2-ethics-governance/)

### References

- boyd, d., & Crawford, K. (2012). [Critical questions for big data](https://doi.org/10.1080/1369118X.2012.678878). *Information, Communication & Society*, 15(5), 662–679.
- Zuboff, S. (2019). *The age of surveillance capitalism* (Chapter 1). PublicAffairs. *(Spanish or English edition — distributed by course email.)*
- Mittelstadt, B. D., et al. (2016). [The ethics of algorithms: Mapping the debate](https://doi.org/10.1177/2053951716679679). *Big Data & Society*, 3(2).

<!-- end RENDER: -->

<!-- NOTEBOOK: -->

## Repaso de Python para este cuaderno

Antes de entrar en los detalles del laboratorio, vamos a hacer un repaso de los conceptos de Python que este cuaderno require. Si ya dominó el diagnóstico previo, puede ejecutar estas celdas rápido. Si no, léalas con calma. Aquí solo aparece lo que usaremos en las Partes 1 a 3. No es un curso de pandas completo.

### Variables y cadenas de texto

Una variable guarda un valor. Las cadenas con **`f"..."`** insertan variables dentro del texto.

```python
year = 2024
catalog_id = 819
print(f"Año {year}, catálogo {catalog_id}")
```

### Funciones

Una función agrupa pasos reutilizables. **`return`** devuelve un resultado.

```python
def convert_to_mb(bytes_descargados: int) -> float:
    return bytes_descargados / 1e6

print(convert_to_mb(50000000))
```

### Diccionarios, listas y bucles

Un **diccionario** guarda pares clave valor. Una **lista** ordena varios elementos. Un **`for`** recorre la lista.

```python
# Definimos un diccionario
entrada = {"filename": "Ene_2024.zip", "seconds": 12.5}

# Definimos una lista con un elemento de tipo diccionario
manifest = [entrada]

# Recorremos la lista y accedemos a los datos del diccionario
for fila in manifest:
    print(fila["filename"], fila["seconds"])
```

### Rutas con `Path`

**`Path`** representa carpetas y archivos. El operador **`/`** une rutas. **`mkdir(parents=True, exist_ok=True)`** crea carpetas si faltan. Esta librería se utiliza para crear sistemas de archivos.

```python
from pathlib import Path

carpeta = Path("data/raw") / "2024"
carpeta.mkdir(parents=True, exist_ok=True)
print(carpeta.is_dir())
```

### `json`, `requests` y `zipfile`

- **`json`**: leer y escribir archivos JSON `manifest.json`.
- **`requests`**: se utiliza para consumir servicios disponibles en Internet. En este caso, la utilizaremos para descargar archivos del DANE por HTTP.
- **`zipfile`**: abrir archivos ZIP y extraer su contenido.

Verá estos módulos importados en la celda de configuración de la Parte 1.

### Comprobar con `assert`

**`assert`** detiene la ejecución si una condición es falsa. Las celdas **Comprobar** usan este patrón.

```python
assert catalog_id == 819
print("Repaso Python: OK")
```

---

## Instrucciones

**Propósito.** Este cuaderno es su práctica de la Lección 1. El objetivo es **poner a disposición datos de la encuesta del DANE "Gran Encuesta Integrada de Hogares (GEIH)"**. Esa es la primera etapa de nuestra metodología: **Access** (tener los datos disponibles antes de evaluarlos o analizarlos).

En producción, los microdatos nacionales de empleo abarcan muchos años a escala de gigabytes. En este laboratorio vamos a empezar en una escala más pequeña. Trabajaremos con los datos de la encuesta para el año 2024 en dos partes:

1. **Parte 1 — un mes** (enero): utilizando el respectivo `catalog_id` y `file_id`, descargar un ZIP, extraer, previsualizar y registrar el resultado en `manifest.json`.
2. **Parte 2 — el año completo**: ver por qué hace falta extraer los `file_id` desde la página get-microdata, automatizar esa lectura y descargar los otros once meses.
3. **Parte 3 — exploración inicial**: resumir lo descargado, revisar calidad básica y relacionar números con los conceptos de la lección. La reflexión escrita va en el PDF individual. Ver **Tareas**.

**Qué hacer (en orden).**

1. Lea **Cómo construir la URL de descarga** más abajo se explica lo que se automatiza en código.
2. Abra este cuaderno en **Google Colab** o ejecútelo en local con Python 3.10+.
3. Ejecute las celdas **de arriba hacia abajo** salvo que una celda indique otra cosa.
4. En celdas **Comprobar**, ejecute las pruebas y corrija celdas anteriores si algo falla.
5. Las **entregas** de la semana 1 están en la [página de la Lección 2](https://cabrerac.github.io/teaching/26-udenar-big-data/l2-ethics-governance/) y en el cuaderno **`week-1-group`**.

**Estructura de carpetas** (la celda de configuración crea estas rutas):

| Ruta | Función |
|------|---------|
| `data/raw/2024/` | ZIP de 2024 y carpetas con CSV extraídos |
| `outputs/` | Diagramas y exportaciones para la tarea |
| `manifest.json` | Registro de acceso (una fila por archivo descargado) |

---

### Cómo construir la URL de descarga

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

Las celdas siguientes descargan los datos utilizando la ruta de descarga directa. La **Parte 1** usa el enlace de **enero** que ya conocemos. La **Parte 2** automatiza la lectura de la página y descarga **el resto de 2024**.

---

## Parte 1 — Descarga de datos para un mes (enero 2024)

### Paso 1 — Configuración — importaciones, constantes y carpetas

Usamos **`pandas`** y **`requests`**, más la biblioteca estándar de Python. La siguiente celda define las variables que vamos a utilizar y crea las carpetas donde almacenaremos los datos descargados.

```python
import json          # leer y escribir manifest.json
import re            # expresiones regulares (parsear HTML del DANE)
import time          # medir segundos de descarga
import zipfile       # abrir archivos ZIP
from pathlib import Path

import pandas as pd   # tablas (DataFrame)
import requests      # descargar archivos por HTTP

# Año de práctica L1 — encuesta 2024, catalog_id 819
CATALOG_ID = 819
YEAR = 2024

# Mes de práctica L1 — enero 2024 (file_id del enlace manual arriba)
FILE_ID = 23313
DANE_FILENAME = "Ene_2024.zip"
EXTRACT_DIR = Path(DANE_FILENAME).stem  # "Ene_2024" sin .zip

# Procesamiento de archivos CSV
CSV_SEP = ";"
CSV_ENCODING = "latin-1"
PRIMARY_TABLE_KEYWORD = "fuerza de trabajo"

# Carpetas para almacenar datos descargados
RAW_DIR = Path("data/raw")
YEAR_DIR = RAW_DIR / str(YEAR)
OUTPUTS_DIR = Path("outputs")
YEAR_DIR.mkdir(parents=True, exist_ok=True)   # crea data/raw/2024/ si no existe
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

### Paso 2 — Descargar el ZIP mensual

Construimos la URL con el patrón de la sección anterior (`catalog_id` + `file_id`). Una descarga directa devuelve un ZIP (GEIH nacional de ese mes).

La función `download_zip` guarda el archivo en **`data/raw/2024/`** y registra tiempo y tamaño para el manifiesto.

¿Por qué `stream=True`?

Con **`stream=True`** y `iter_content(...)`, cada trozo se escribe al disco sin cargar todo el ZIP en RAM. Con `stream=False` y `resp.content`, Python puede usar **casi el doble de memoria** un momento. Para **un mes** en Colab el tiempo suele ser similar, la diferencia importa cuando bajan **muchos archivos grandes** o trabajan en un equipo con poca RAM. Esta consideración es importante cuando se piensa en la dimensión **V de volumen**.

```python
def download_zip(url: str, dest: Path, timeout: int = 600) -> tuple[float, int]:
    """Descarga url a dest en streaming; devuelve (segundos, bytes). Falla si no es ZIP."""
    t0 = time.perf_counter()  # marca de tiempo inicial
    with requests.get(url.strip(), stream=True, timeout=timeout) as resp:
        resp.raise_for_status()  # falla si HTTP 4xx/5xx
        with dest.open("wb") as fh:
            for chunk in resp.iter_content(chunk_size=1 << 20):  # trozos de 1 MB
                if chunk:
                    fh.write(chunk)
    elapsed = round(time.perf_counter() - t0, 3)
    magic = dest.read_bytes()[:2]  # un ZIP válido empieza con PK
    if magic != b"PK":
        raise ValueError(
            f"El archivo descargado no es un ZIP (obtuvo {magic!r}). "
            "Use la URL /download/ de get-microdata, no la página inicial del catálogo."
        )
    return elapsed, dest.stat().st_size
```

Ahora creamos la URL de descarga directa para el archivo que deseamos descargar e invocamos a la función `download_zip` con los respectivos parámetros.

```python
# Construir URL directa con catalog_id y file_id
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

### Paso 3 — Extraer los archivos CSV

Cada ZIP mensual trae **varias** tablas CSV (fuerza de trabajo, vivienda, educación, etc.). Access significa tener **todas** disponibles, para ello implementaremos la función **`extract_csvs`**. Esta función escribe cada archivo `.csv` en una carpeta con el nombre base del ZIP del DANE, p. ej. `data/raw/2024/Ene_2024/`.

En algunos meses (p. ej. **abril 2024**) el ZIP exterior no trae `.csv` sueltos sino un **`csv.zip` anidado** (junto con `dta.zip`, `sav.zip`, etc.). La función lo detecta y extrae el ZIP interior.

```python
def extract_csvs(zip_path: Path, dest_dir: Path) -> list[Path]:
    """Extrae cada .csv; si el mes trae csv.zip anidado, lo abre y extrae ahí."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "r") as zf:
        names = zf.namelist()
        csv_members = [n for n in names if n.lower().endswith(".csv")]
        nested_csv_zip = next(
            (n for n in names if re.fullmatch(r"csv\s*\d*\.zip", Path(n).name, re.I)),
            None,
        )
        if nested_csv_zip and not csv_members:
            inner_path = dest_dir / "_csv_inner.zip"
            inner_path.write_bytes(zf.read(nested_csv_zip))
            try:
                return extract_csvs(inner_path, dest_dir)
            finally:
                inner_path.unlink(missing_ok=True)
        if not csv_members:
            raise ValueError(
                f"No hay CSV en {zip_path.name}. Entradas: "
                f"{[Path(n).name for n in names[:8]]}"
            )
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
total_csv_bytes = sum(p.stat().st_size for p in csv_files)  # suma tamaños en bytes

print(f"Extraídos {len(csv_files)} archivo(s) CSV → {extract_dir}/\n")
for p in csv_files:
    print(f"{p.stat().st_size / 1e6:8.2f} MB  {p.name}")
print(f"\nTotal extraído: {total_csv_bytes / 1e6:.2f} MB")
```

**Comprobar:**

```python
assert len(csv_files) >= 1
# next(...) toma el primer archivo cuyo nombre contiene "fuerza de trabajo"
labour_path = next(
    p for p in csv_files if PRIMARY_TABLE_KEYWORD in p.name.lower().replace("\xa0", " ")
)
print("Tabla principal de fuerza de trabajo:", labour_path.name)
print("Paso 3 — extracción: OK")
```

---

### Paso 4 — Previsualizar la tabla de fuerza de trabajo

El DANE entrega los CSV GEIH con separador **punto y coma** y codificación **`latin-1`**. Si **`read_csv`** falla, revise esos dos ajustes antes de cambiar otra cosa.

Previsualizamos **`Fuerza de trabajo.CSV`** utilizando la funcion `read_csv` de pandas, la cual retorna un dataframe.

```python
# read_csv carga el CSV en un DataFrame (tabla en memoria)
df = pd.read_csv(labour_path, sep=CSV_SEP, encoding=CSV_ENCODING, low_memory=False)
n_rows = len(df)       # número de filas
n_cols = len(df.columns)  # número de columnas

print(f"Filas: {n_rows:,}  |  Columnas: {n_cols}")
print(f"Columnas (primeras 12): {list(df.columns[:12])}")
df.head()  # muestra las primeras 5 filas
```

Podemos inspeccionar tipos y valores no nulos por columna.

```python
df.info()  # resumen: tipos, conteo de no nulos por columna
```

**Comprobar:**

```python
assert n_rows > 10_000, "Se espera un mes nacional (decenas de miles de filas)"
assert "DPTO" in df.columns, "Se espera la columna DPTO (código de departamento)"
print("Paso 4 — previsualización: OK")
```

---

### Paso 5 — Registrar el primer mes en `manifest.json`

Con el fin de documentar el proceso de descarga guardamos **un objeto JSON por archivo descargado** en el archivo `manifest.json`. Para esto creamos la función `write_manifest`.

```python
def write_manifest(path: Path, entries: list[dict]) -> None:
    # json.dumps convierte la lista de diccionarios a texto JSON legible
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
        # Ya extraído: no volver a descargar (ahorra tiempo y ancho de banda)
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
entries = [manifest_entry]  # enero ya registrado en Parte 1
for row in all_files:
    if row["filename"] == DANE_FILENAME:
        continue  # enero ya está en disco
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

## Parte 3 — Explorar lo descargado

Esta parte cierra **Access** con una primera mirada a **Assess**. Use lo que ya tiene en disco. Si terminó la Parte 2 trabaja con los doce meses. Si solo completó la Parte 1 basta con enero y una fila en el manifiesto.

Las Vs, las tres A, la arquitectura y la reflexión escrita van en las diapositivas, el PDF grupal y el PDF individual. Aquí solo medimos y observamos.

---

### Paso 1 — Resumen desde `manifest.json`

Cargamos el manifiesto en un dataframe y vemos tamaño y tiempo por archivo.

```python
# Cargar manifiesto y convertirlo en DataFrame para tablas y gráficos
manifest_rows = json.loads(manifest_path.read_text(encoding="utf-8"))
manifest_df = pd.DataFrame(manifest_rows)
manifest_df["mb"] = manifest_df["bytes_downloaded"] / 1e6
manifest_df["mes"] = manifest_df["filename"].str.replace(".zip", "", regex=False)

cols = ["mes", "seconds", "mb", "notes"]
print(manifest_df[cols].to_string(index=False))

total_mb = manifest_df["mb"].sum()
total_seconds = manifest_df["seconds"].sum()
print(f"\nTotal descargado: {total_mb:.1f} MB")
print(f"Tiempo registrado en descargas: {total_seconds:.1f} s")
print(f"Filas en manifiesto: {len(manifest_df)}")
```

**Comprobar:**

```python
assert manifest_path.is_file()
assert len(manifest_df) >= 1
assert manifest_df["bytes_downloaded"].sum() > 0
print("Parte 3, Paso 1 — manifiesto: OK")
```

---

### Paso 2 — Tamaño en disco

Comparamos el peso de los ZIP con el de los CSV extraídos para un mes (enero).

```python
zip_mb = zip_path.stat().st_size / 1e6
csv_mb = sum(p.stat().st_size for p in csv_files) / 1e6

print(f"ZIP enero: {zip_mb:.1f} MB")
print(f"CSV extraídos enero: {csv_mb:.1f} MB")
print(f"Tablas CSV en enero: {len(csv_files)}")
```

Si completó la Parte 2, sume todos los ZIP de 2024.

```python
if len(manifest_df) >= 12:
    all_zips = list(YEAR_DIR.glob("*.zip"))
    all_zip_mb = sum(p.stat().st_size for p in all_zips) / 1e6
    print(f"ZIP 2024 (12 meses): {all_zip_mb:.1f} MB")
else:
    print("Parte 2 pendiente: solo tiene totales de enero por ahora.")
```

**Comprobar:**

```python
assert zip_mb > 1
assert csv_mb > 1
assert len(csv_files) >= 1
print("Parte 3, Paso 2 — tamaño: OK")
```

---

### Paso 3 — Calidad básica en fuerza de trabajo

En la Parte 1 abrió la tabla con `head` e `info`. Aquí revisamos valores faltantes y la distribución de un código categórico. Esto es un primer paso de calidad, no una auditoría completa.

```python
cols_revisar = [c for c in ("PER", "DPTO", "MES") if c in df.columns]
if cols_revisar:
    # isna() detecta celdas vacías; mean() da proporción por columna
    missing = df[cols_revisar].isna().mean().mul(100).round(2)
    print("Porcentaje de valores faltantes:")
    print(missing.to_string())
else:
    print("Columnas PER, DPTO o MES no encontradas. Use df.columns para elegir tres columnas.")
```

Distribución por departamento (siempre disponible en fuerza de trabajo) y, si existe, por sexo.

```python
if "DPTO" in df.columns:
    print("\nFilas por departamento (10 con más registros en este mes):")
    print(df["DPTO"].value_counts(dropna=False).head(10).to_string())

# GEIH suele usar P6020 para sexo; a veces aparece como SEXO
sex_col = next(
    (
        c
        for c in df.columns
        if c.strip().upper() in ("SEXO", "P6020")
        or c.strip().upper().endswith("6020")
    ),
    None,
)
if sex_col:
    print(f"\nConteo en {sex_col} (sexo, códigos DANE):")
    print(df[sex_col].value_counts(dropna=False).head().to_string())
else:
    print("\nNo encontramos columna de sexo (SEXO / P6020).")
    print("Revise el diccionario DANE o pruebe otra columna categórica de df.columns.")
```

**Comprobar:**

```python
assert n_rows > 10_000
assert "DPTO" in df.columns
print("Parte 3, Paso 3 — calidad: OK")
```

---

### Paso 4 — Gráficos de descarga y exploración

Todas las descargas usaron **`stream=True`** (Parte 1). Aún no comparamos `stream=True` frente a `stream=False`. Eso lo veremos en prácticas posteriores.

Visualizamos **todo el manifiesto** (todos los meses registrados). Si solo completó la Parte 1 verá un mes en descarga y un gráfico extra con datos GEIH de enero.

```python
import matplotlib.pyplot as plt

# Orden cronológico de meses DANE (Ene … Dic)
MES_ORDER = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
manifest_plot = manifest_df.copy()
manifest_plot["mes_corto"] = manifest_plot["mes"].str.replace("_2024", "", regex=False)
manifest_plot["mes_ord"] = manifest_plot["mes_corto"].map({m: i for i, m in enumerate(MES_ORDER)})
manifest_plot = manifest_plot.sort_values("mes_ord")

n_meses = len(manifest_plot)
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# Gráfico 1: tamaño descargado por mes (MB) — usa todas las filas del manifiesto
manifest_plot.plot.bar(
    x="mes_corto", y="mb", ax=axes[0], legend=False, color="steelblue"
)
axes[0].set_title(f"Tamaño descargado por mes ({n_meses} mes(es) en manifiesto)")
axes[0].set_xlabel("Mes")
axes[0].set_ylabel("MB")
axes[0].tick_params(axis="x", rotation=45)

# Gráfico 2: segundos por mes (0 = omitido porque ya estaba en disco)
manifest_plot.plot.bar(
    x="mes_corto", y="seconds", ax=axes[1], legend=False, color="darkorange"
)
axes[1].set_title("Segundos de descarga por mes")
axes[1].set_xlabel("Mes")
axes[1].set_ylabel("Segundos")
axes[1].tick_params(axis="x", rotation=45)

plt.tight_layout()
plt.show()

# Si hay al menos 2 meses con tiempo de descarga real, relacionar tamaño y tiempo
timed = manifest_plot[manifest_plot["seconds"] > 0].copy()
if len(timed) >= 2:
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    ax2.scatter(timed["mb"], timed["seconds"], color="steelblue")
    for _, row in timed.iterrows():
        ax2.annotate(row["mes_corto"], (row["mb"], row["seconds"]), fontsize=9)
    ax2.set_title("Tamaño frente a tiempo (meses descargados en esta sesión)")
    ax2.set_xlabel("MB descargados")
    ax2.set_ylabel("Segundos")
    plt.tight_layout()
    plt.show()
    timed["seg_por_mb"] = timed["seconds"] / timed["mb"]
    print("Segundos por MB:")
    print(timed[["mes_corto", "seg_por_mb"]].sort_values("seg_por_mb").to_string(index=False))
elif "DPTO" in df.columns:
    # Un solo mes en manifiesto: explorar variación dentro de enero por departamento
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    df["DPTO"].value_counts().head(12).sort_values().plot.barh(ax=ax2, color="seagreen")
    ax2.set_title("Filas en fuerza de trabajo por departamento (enero, top 12)")
    ax2.set_xlabel("Número de filas")
    plt.tight_layout()
    plt.show()
    print("Parte 2 pendiente: complete el año 2024 para gráficos de descarga multi-mes.")
else:
    print("Ejecute al menos la Parte 1 para ver gráficos.")
```

**Comprobar:**

```python
assert "seconds" in manifest_df.columns
assert "mb" in manifest_df.columns
print("Parte 3, Paso 4 — gráficos: OK")
```

---

### Paso 5 — Comprobación de Access completado

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

Este cuaderno es **práctica individual** (Access). No define entregas en Moodle.

Las entregas de la **semana 1** (L1 + L2) están en la [página de la Lección 2](https://cabrerac.github.io/teaching/26-udenar-big-data/l2-ethics-governance/) y en la sección **Tareas** del cuaderno [L2](https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-big-data/l2-ethics-governance.ipynb) y del cuaderno grupal [week-1-group](https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-big-data/week-1-group.ipynb).

<!-- end NOTEBOOK: -->
