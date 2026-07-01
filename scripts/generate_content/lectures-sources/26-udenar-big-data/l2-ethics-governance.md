---
course_code: 26-udenar-big-data
title: Ethics, privacy, and foundations of data governance
description: Lecture 2 follows the first access to GEIH by asking what responsible use of that data requires. We treat harm, consent, and fairness not as a final checklist but as requirements that shape every technical choice in Big Data projects. The readings and a guided ethics audit on survey and map data prepare the accountable-practice frame for storage, processing, and analytics ahead.
session: 2
start_time: 07:00 am
end_time: 01:00 pm
hours: 5
author: Christian Cabrera Jojoa
email: chc79@cam.ac.uk
position: Assistant Research Professor
department: Department of Computer Science and Technology
institution: University of Cambridge
layout: lecture
lecture_code: l2-ethics-governance
lecture_date: 06/06/2026
permalink: /teaching/26-udenar-big-data/l2-ethics-governance/
visible: true
group_notebook: week-1-group
notebook_language: es
notebook_title: Ética, privacidad y gobernanza de datos
notebook_description: Práctica de la Lección 2. Auditoría ética sobre GEIH y primer enlace con OpenStreetMap (escuelas).
---

<!-- SLIDES: -->

# Last Time

<!-- end SLIDES: -->

{% include _snippets/26-udenar-big-data/l2-ethics-governance/last-time.md %}

<!-- SLIDES: -->

# Big Data Requirements

<!-- end SLIDES: -->

{% include _snippets/26-udenar-big-data/l2-ethics-governance/big-data-requirements.md %}

<!-- SLIDES: -->

# Ethical Requirements

<!-- end SLIDES: -->

{% include _snippets/26-udenar-big-data/l2-ethics-governance/ethical-requirements.md %}

<!-- SLIDES: -->

# Ethics in the Pipeline

<!-- end SLIDES: -->

{% include _snippets/26-udenar-big-data/l2-ethics-governance/pipeline-ethics.md %}

<!-- SLIDES: -->

# Data Assess

<!-- end SLIDES: -->

{% include _snippets/26-udenar-big-data/l2-ethics-governance/data-assess-ethics.md %}

<!-- SLIDES: -->

# Conclusions

<!-- end SLIDES: -->

{% include _snippets/26-udenar-big-data/l2-ethics-governance/conclusions.md %}

{% include _snippets/26-udenar-big-data/l2-ethics-governance/practical-slides.md %}

{% include _snippets/26-udenar-big-data/l2-ethics-governance/week1-homework.md %}

<!-- RENDER: -->

### Week 1 links

- [Week 1 hub](/teaching/26-udenar-big-data/week-1-hub-es/)

### Resources

- [OpenStreetMap — Nariño](https://www.openstreetmap.org/relation/1380130)
- [Overpass API](https://wiki.openstreetmap.org/wiki/Overpass_API)
- [Overpass by Example - building queries](https://dev.overpass-api.de/overpass-doc/en/) ([es](https://dev.overpass-api.de/overpass-doc/es/))
- [Overpass QL syntax (reference)](https://wiki.openstreetmap.org/wiki/Overpass_API/Overpass_QL) · [Overpass Turbo](https://wiki.openstreetmap.org/wiki/Overpass_turbo) (try queries in the browser)
- [GEIH 2024 — data dictionary (DANE)](https://microdatos.dane.gov.co/index.php/catalog/819/data-dictionary)
- [UK Data and AI Ethics Framework](https://www.gov.uk/government/publications/data-ethics-framework/data-and-ai-ethics-framework)

### References

- Zuboff, S. (2019). *The age of surveillance capitalism* (Chapter 1). PublicAffairs.
- Mittelstadt, B. D., et al. (2016). [The ethics of algorithms: Mapping the debate](https://doi.org/10.1177/2053951716679679). *Big Data & Society*, 3(2).
- Prabhakaran, V., et al. (2022). [A human rights-based approach to responsible AI](https://arxiv.org/abs/2210.02667). arXiv:2210.02667.
- Afroogh, S., et al. (2024). [Embedded ethics for responsible AI systems in disaster management](https://doi.org/10.1007/s43681-023-00309-1). *AI and Ethics*, 4, 1117–1141.
- UK Government. (2025). [Data and AI Ethics Framework](https://www.gov.uk/government/publications/data-ethics-framework/data-and-ai-ethics-framework).
- Khatri, V., & Brown, C. V. (2010). [Designing data governance](https://doi.org/10.1145/1795194.1795237). *Communications of the ACM*, 53(1), 148–152.
- Nissenbaum, H. (2004). [Privacy as contextual integrity](https://doi.org/10.2139/ssrn.3885612). *Washington Law Review*, 79(1), 119–158.
- boyd, d., & Crawford, K. (2012). [Critical questions for big data](https://doi.org/10.1080/1369118X.2012.678878). *Information, Communication & Society*, 15(5), 662–679.

<!-- end RENDER: -->

<!-- NOTEBOOK: -->

## Repaso de Python para este cuaderno

Este cuaderno usa **`pandas`** y **`requests`**. Si completó el cuaderno individual L1, ya conoce parte de esto. Aquí solo aparece lo nuevo para las Partes 1 a 5.

### Tablas con pandas

Un **DataFrame** es una tabla. **`read_csv`** abre un CSV. **`value_counts`** cuenta categorías. **`groupby`** agrupa filas.

```python
import pandas as pd

# Crear un diccionario de datos
datos = {"dpto": [52, 52, 11], "edad": [25, 40, 30]}
# Crear un DataFrame a partir de un diccionario. Las llaves son los nombres de las columnas
df = pd.DataFrame(datos)
# Agrupar por departamento y calcular la edad media
print(df.groupby("dpto")["edad"].mean())
# Contar cuántas filas hay por departamento
print(df["dpto"].value_counts())
```

### Unir dos tablas con `merge`

**`merge`** combina tablas por una columna común (aquí **`DPTO`**).

```python
# Crear dos datasets
geih = pd.DataFrame({"dpto": [52, 11], "personas": [1000, 5000]})
osm = pd.DataFrame({"dpto": [52, 11], "poi_school_count": [120, 800]})
# Unir los dos datasets a través del código de departamento
unido = geih.merge(osm, on="dpto", how="left")
print(unido)
```

### Peticiones HTTP con `requests`

**`requests.post`** envía solicitudes de datos a un servicio web. OpenStreetMap (OSM) expone la **Overpass API**; las consultas se escriben en **Overpass QL** (texto en el parámetro `data`). Para aprender a armarlas: [**Overpass por ejemplo**](https://dev.overpass-api.de/overpass-doc/es/), [sintaxis QL](https://wiki.openstreetmap.org/wiki/ES:Overpass_API/Overpass_QL), [Overpass Turbo](https://wiki.openstreetmap.org/wiki/ES:Overpass_turbo) (probar en el navegador). El servidor exige **`User-Agent`**.

A veces el servidor responde **`504 Gateway Timeout`** (saturación): reintente o use el espejo alternativo en el código.

```python
import time

import requests

OVERPASS_HEADERS = {
    "User-Agent": "UDENAR-BigData-2026/1.0 (Universidad de Narino - Big Data elective)",
    "Accept": "application/json",
}
# Espejos públicos (orden: primero suele ser más estable en Colab)
OVERPASS_ENDPOINTS = [
    "https://overpass.kumi.systems/api/interpreter",
    "https://overpass-api.de/api/interpreter",
]
OVERPASS_RETRY_PAUSE = 2.0  # segundos entre reintentos


def overpass_post(query: str, *, timeout: int = 90) -> requests.Response:
    """POST a Overpass con espejos y reintentos ante 502/503/504 o timeout."""
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
    raise requests.HTTPError(
        "Overpass: sin respuesta útil tras reintentos (pruebe de nuevo en 1–2 min)."
    )


print("Overpass listo. User-Agent:", OVERPASS_HEADERS["User-Agent"])

_smoke = "[out:json][timeout:5];out count 1;"
try:
    r = overpass_post(_smoke, timeout=25)
    print("Overpass OK — HTTP", r.status_code)
except requests.HTTPError as e:
    print(
        "AVISO: Overpass saturado o lento (504 es habitual). "
        "Espere 1–2 minutos y vuelva a ejecutar esta celda antes de la Parte 4."
    )
    print(e)

```

### Comprobar con `assert`

Las celdas **Comprobar** usan **`assert`** para validar resultados.

```python
assert len(unido) == 2
print("Repaso Python L2: OK")
```

---

## Instrucciones

**Propósito.** Este cuaderno es su práctica de la **Lección 2**. Trabaja sobre microdatos GEIH reales. El objetivo es ver **ética y gobernanza**: cuasi-identificadores, riesgo de divulgación, límites de inferencia y un primer enlace con **OpenStreetMap (OSM)** para enriquecer el dataset creado en el cuaderno de la Lección 1.

Si ya completó la **Parte 1 de L1**, reutilice esos archivos subiendolos a este cuaderno. Si no, la **Parte 1** a continuación descarga **enero 2024** del dataset del DANE.

**Qué hacer (en orden).**

1. Ejecute las celdas **de arriba hacia abajo** (no salte la Parte 1 si ya tiene enero 2024 de L1: el cuaderno reutiliza o vuelve a descargar).
2. En celdas **Comprobar**, corrija celdas anteriores si algo falla.
3. Lleve lo aprendido al **sábado 6 jun**, al cuaderno grupal y a la reflexión semana 1.

**Mapa del cuaderno**

| Parte | Tema | Qué obtiene al final |
|-------|------|----------------------|
| 1 | Access GEIH (enero 2024) | `df` con fuerza de trabajo + edad (`P6040`) |
| 2 | Cuasi-identificadores | Tabla de columnas sensibles presentes |
| 3 | Divulgación (vista previa) | Celda mínima DPTO × banda de edad |
| 4 | OSM + enlace | Conteo escuelas Nariño + CSV/gráfico demo |

**Carpetas usadas:**

| Ruta | Función |
|------|---------|
| `data/raw/2024/` | ZIP y carpeta del mes (enero 2024) |
| `data/raw/2024/Ene_2024/` | CSV extraídos |
| `outputs/` | Tablas y gráficos exportados |

---

## Parte 1 — Access: un mes GEIH (enero 2024)

**Objetivo.** Tener en disco el mismo mes que descargamos en el cuaderno de la Lección 1 y un `DataFrame` listo para hacer una análisis de aspectos éticos del dataset.

Usamos **enero 2024**, igual que la Parte 1 de L1. URL de descarga directa (patrón del DANE):

```text
https://microdatos.dane.gov.co/index.php/catalog/{catalog_id}/download/{file_id}
```

Para enero 2024: `catalog_id=819`, `file_id=23313`. Más detalle en el [cuaderno L1](https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-big-data/l1-introduction.ipynb).

### Paso 1 — Configuración

Las constantes `PERSON_KEYS` (más abajo) son la clave técnica que el DANE usa para enlazar tablas del mismo mes. En **Paso 5** explicamos qué significan con respecto a la privacidad de los datos.

```python
import re
import time
import zipfile
from pathlib import Path

import pandas as pd
import requests

# Identificadores de archivos
CATALOG_ID = 819
YEAR = 2024
FILE_ID = 23313
DANE_FILENAME = "Ene_2024.zip"
EXTRACT_DIR = "Ene_2024"

# Procesamiento de archivos CSV
CSV_SEP = ";"
CSV_ENCODING = "latin-1"
PRIMARY_TABLE_KEYWORD = "fuerza de trabajo"
DEMOG_TABLE_KEYWORDS = ("caracter", "generales")
# Clave de persona en GEIH (tres columnas, ver Paso 5 y diccionario DANE)
PERSON_KEYS = ["DIRECTORIO", "HOGAR", "ORDEN"]

# Carpetas para almacenar datos descargados
RAW_DIR = Path("data/raw")
YEAR_DIR = RAW_DIR / str(YEAR)
MONTH_DIR = YEAR_DIR / EXTRACT_DIR
OUTPUTS_DIR = Path("outputs")
YEAR_DIR.mkdir(parents=True, exist_ok=True)
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

zip_path = YEAR_DIR / DANE_FILENAME
print(f"Año {YEAR} | catalog {CATALOG_ID} | file {FILE_ID} | {DANE_FILENAME}")
```

**Comprobar:**

```python
assert CATALOG_ID == 819 and FILE_ID == 23313
assert YEAR_DIR.is_dir()
print("Parte 1, Paso 1 — configuración: OK")
```

---

### Paso 2 — Descargar el ZIP (si falta)

```python
def download_zip(url: str, dest: Path, timeout: int = 600) -> tuple[float, int]:
    """Descarga url a dest en streaming; devuelve (segundos, bytes)."""
    t0 = time.perf_counter()
    with requests.get(url.strip(), stream=True, timeout=timeout) as resp:
        resp.raise_for_status()
        with dest.open("wb") as fh:
            for chunk in resp.iter_content(chunk_size=1 << 20):
                if chunk:
                    fh.write(chunk)
    elapsed = round(time.perf_counter() - t0, 3)
    if dest.read_bytes()[:2] != b"PK":
        raise ValueError("El archivo descargado no es un ZIP válido.")
    return elapsed, dest.stat().st_size


download_url = (
    f"https://microdatos.dane.gov.co/index.php/catalog/{CATALOG_ID}/download/{FILE_ID}"
)

if zip_path.is_file() and zip_path.read_bytes()[:2] == b"PK":
    bytes_downloaded = zip_path.stat().st_size
    print(f"ZIP ya en disco: {zip_path} ({bytes_downloaded / 1e6:.1f} MB) — omitiendo descarga")
else:
    download_seconds, bytes_downloaded = download_zip(download_url, zip_path)
    print(f"Descargado: {zip_path} ({bytes_downloaded / 1e6:.1f} MB en {download_seconds} s)")
```

**Comprobar:**

```python
assert zip_path.is_file()
assert zip_path.read_bytes()[:2] == b"PK"
assert bytes_downloaded > 1_000_000
print("Parte 1, Paso 2 — descarga: OK")
```

---

### Paso 3 — Extraer CSV

```python
def extract_csvs(zip_path: Path, dest_dir: Path) -> list[Path]:
    """Extrae cada .csv; si hay csv.zip anidado, lo abre y extrae."""
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
            raise ValueError(f"No hay CSV en {zip_path.name}")
        for name in csv_members:
            target = dest_dir / Path(name).name
            with zf.open(name) as src, target.open("wb") as dst:
                dst.write(src.read())
    return sorted(dest_dir.glob("*.CSV")) + sorted(dest_dir.glob("*.csv"))


csv_files = extract_csvs(zip_path, MONTH_DIR)
labour_path = next(
    p for p in csv_files if PRIMARY_TABLE_KEYWORD in p.name.lower().replace("\xa0", " ")
)
print(f"Extraídos {len(csv_files)} CSV en {MONTH_DIR}/")
print(f"Tabla principal: {labour_path.name}")
```

**Comprobar:**

```python
assert len(csv_files) >= 1
assert labour_path.is_file()
print("Parte 1, Paso 3 — extracción: OK")
```

---

### Paso 4 — Cargar fuerza de trabajo

Cada ZIP mensual trae **varias** tablas CSV (no una sola). Los nombres de columna (`P6240`, `P6040`, …) y su significado están en el [diccionario de datos GEIH 2024](https://microdatos.dane.gov.co/index.php/catalog/819/data-dictionary) del DANE — una entrada por tabla (p. ej. [Fuerza de trabajo](https://microdatos.dane.gov.co/index.php/catalog/819/data-dictionary/F65?file_name=Fuerza+de+trabajo), [Características generales](https://microdatos.dane.gov.co/index.php/catalog/819/data-dictionary/F63?file_name=Caracteristicas+generales%2C+seguridad+social+en+salud+y+educacion)).

La tabla **Fuerza de trabajo** contiene variables relacionadas con el empleo (`P6240`, `P6250`, etc.), mientras que la información sobre **edad (`P6040`) y sexo (`P3271`)** se encuentra en la tabla **Características generales**. El código siguiente carga la tabla de Fuerza de trabajo desde el CSV extraído y muestra información básica sobre su contenido (número de filas y columnas, nombres de columnas principales, primeras filas). En el siguiente paso, ambas tablas se unirán para que cada registro de empleo tenga asociada la edad de la persona correspondiente.

```python
# Lee el archivo csv y lo transforma en un DataFrame (i.e., una tabla)
df = pd.read_csv(labour_path, sep=CSV_SEP, encoding=CSV_ENCODING, low_memory=False)
n_rows = len(df)
n_cols = len(df.columns)

print(f"Archivo: {labour_path.name}")
print(f"Filas: {n_rows:,}  |  Columnas: {n_cols}")
print(f"Primeras columnas: {list(df.columns[:12])}")
print(df.head(3))
```

**Comprobar:**

```python
assert n_rows > 10_000, "Se espera un mes nacional de fuerza de trabajo"
assert "DPTO" in df.columns, "Falta columna DPTO"
assert all(k in df.columns for k in PERSON_KEYS), "Faltan claves de persona para unir tablas"
print("Parte 1, Paso 4 — carga fuerza de trabajo: OK")
```

---

### Paso 5 — Unir edad desde Características generales

La tabla **Fuerza de trabajo** no trae edad (`P6040`), esa variable está en **Características generales**. Unimos ambas tablas con **`merge`** sobre las tres columnas `PERSON_KEYS`:

| Columna | Rol |
|---------|-----|
| **`DIRECTORIO`** | Identificador del hogar en la muestra del mes |
| **`HOGAR`** | Número de hogar dentro del directorio |
| **`ORDEN`** | Posición de la persona dentro del hogar |

Juntas identifican **un mismo encuestado** entre tablas del mismo ZIP. Consulte el [diccionario DANE 2024](https://microdatos.dane.gov.co/index.php/catalog/819/data-dictionary) para el texto oficial de cada variable.

Aquí encontramos una lección importante en cuanto a la ética y governanza de los datos. El DANE **no entrega nombre ni cédula** en los microdatos: es una capa de anonimización institucional. Aun así, el archivo sigue siendo microdato: con `DIRECTORIO`, `HOGAR`, `ORDEN` usted puede **reconstruir la ficha de una persona** dentro del mes y **añadir** edad, sexo, empleo, municipio, etc. Eso no “desanonimiza” por sí solo, pero **sí permite inferir** rasgos y, si publica agregados muy pequeños (Parte 3), **acercarse a identificar** a alguien. La institución puso un intermediario (claves internas); **nuestra responsabilidad** es no tratar eso como “ya es anónimo”, documentar límites, y tomar medidas de mitigación en nuestros proyectos.

```python
# Extrayendo el nombre de la tabla con datos demográficos
demog_path = next(
    p
    for p in csv_files
    if all(kw in p.name.lower().replace("\xa0", " ") for kw in DEMOG_TABLE_KEYWORDS)
)
print(f"Tabla demográfica: {demog_path.name}")

# Leyendo la tabla demográfica
demog = pd.read_csv(
    demog_path,
    sep=CSV_SEP,
    encoding=CSV_ENCODING,
    usecols=PERSON_KEYS + ["P6040"],
    low_memory=False,
)

# Uniendo la edad de la tabla demográfica con el DataFrame de fuerza de trabajo utilizando PERSON_KEYS
df = df.merge(demog, on=PERSON_KEYS, how="left", validate="many_to_one")
n_with_age = df["P6040"].notna().sum()
print(f"Filas con P6040 (edad): {n_with_age:,} de {len(df):,}")
```

**Comprobar:**

```python
assert "P6040" in df.columns
assert n_with_age > 10_000
print("Parte 1 — Access, carga y edad: OK")
```

---

## Parte 2 — Cuasi-identificadores

En esta parte del cuaderno vamos a examinar qué columnas del mes actual podrían re-identificar personas si publica agregados finos.

La GEIH no trae nombre ni cédula, pero sí **cuasi-identificadores**: combinaciones (y la propia clave `PERSON_KEYS` en archivos internos) que pueden acercarse a identificar hogares o personas si publica celdas muy pequeñas o cruza fuentes.

Listamos columnas sensibles frecuentes en GEIH. Algunas vienen de **Fuerza de trabajo**, otras (p. ej. **P6040**) de **Características generales** ya unidas en Parte 1.

```python
# Columnas que suelen ser cuasi-identificadores en GEIH (ver diccionario DANE por año)
CANDIDATOS_QI = [
    "DPTO",   # departamento — código geográfico
    "MPIO",   # municipio — código geográfico (más fino que DPTO)
    "AREA",   # área del hogar — urbano / rural (estratificación)
    "P6040",  # edad en años cumplidos — Características generales
    "P6020",  # sexo (código de pregunta; nombre puede variar por año)
    "SEXO",   # sexo (columna alternativa en algunos meses/años)
    "P6160",  # nivel educativo alcanzado — Características generales
    "P6240",  # actividad principal en la semana de referencia — Fuerza de trabajo
    "P6090",  # afiliación / tipo de cotizante en salud — Características generales
    "PER",    # período de la ronda (mes/año de la encuesta; p. ej. 202401)
]

presentes = [c for c in CANDIDATOS_QI if c in df.columns]
faltantes = [c for c in CANDIDATOS_QI if c not in df.columns]

tabla_qi = pd.DataFrame(
    {
        "columna": presentes,
        "tipo": [str(df[c].dtype) for c in presentes],
        "valores_unicos": [df[c].nunique(dropna=False) for c in presentes],
    }
)
print("Cuasi-identificadores detectados:")
print(tabla_qi.to_string(index=False))
if faltantes:
    print("\nNo encontradas en este mes (puede variar por año):", ", ".join(faltantes))
```

Interpretación breve (consulte el [diccionario DANE](https://microdatos.dane.gov.co/index.php/catalog/819/data-dictionary) para el texto exacto de cada pregunta):

- **DPTO / MPIO / AREA**: geografía.
- **P6040**: edad en años cumplidos — tabla *Características generales*.
- **P3271 / P6020 / SEXO**: sexo (nombre varía por año).
- **P6240**: actividad principal la semana pasada — tabla *Fuerza de trabajo*.
- **P6160, P6090**: educación y afiliación en salud — suelen estar en *Características generales*.

La no inclusión del municipio y genero ayudan a mantener anonima la identidad de los encuestados. Lo que debemos determinar es si este patrón se mantiene en todo el conjunto de datos.

**Comprobar:**

```python
assert len(presentes) >= 3, "Se esperan al menos DPTO y dos cuasi-identificadores más"
assert "DPTO" in presentes
print("Parte 2 — cuasi-identificadores: OK")
```

---

## Parte 3 — Vista previa de divulgación estadística

Una prueba sencilla para evaluar la privacidad de nuestro dataset es detectar celdas con muy pocas filas antes de publicar un agregado (regla práctica: alerta si hay menos de 5).

Contamos filas en la celda más pequeña **departamento × banda de edad**. Si hay muy pocas filas, publicar ese agregado puede acercarse a identificar personas.

```python
# P6040 (edad) viene de Características generales — unida en Parte 1, Paso 5
if "P6040" not in df.columns:
    raise KeyError(
        "No hay P6040. Ejecute Parte 1 Paso 5 (merge con Características generales)."
    )

# Normalizar DPTO como texto sin ceros a la izquierda inconsistentes
work = df[["DPTO", "P6040"]].copy()
work["DPTO"] = work["DPTO"].astype(str).str.strip()
work["P6040"] = pd.to_numeric(work["P6040"], errors="coerce")
work = work.dropna(subset=["P6040"])

# Bandas de edad simples para el ejercicio
work["banda_edad"] = pd.cut(
    work["P6040"],
    bins=[0, 17, 29, 44, 59, 120],
    labels=["0-17", "18-29", "30-44", "45-59", "60+"],
)

celdas = (
    work.groupby(["DPTO", "banda_edad"], observed=True)
    .size()
    .reset_index(name="filas")
    .sort_values("filas")
)

min_fila = celdas.iloc[0]
print("Cinco celdas con menos filas (DPTO × banda de edad):")
print(celdas.head(5).to_string(index=False))
print(
    f"\nCelda mínima: DPTO={min_fila['DPTO']}, "
    f"banda={min_fila['banda_edad']}, filas={min_fila['filas']}"
)

K_MIN = 5
if min_fila["filas"] < K_MIN:
    print(f"ALERTA: celda con menos de {K_MIN} filas — riesgo de divulgación si se publica tal cual.")
else:
    print(f"En este mes nacional la celda mínima tiene al menos {K_MIN} filas (vista previa).")
```

Para este mes, el dataset pasa la prueba. Pero como lo vimos anteriormente podemos seguir preguntando si esto se cumple en otras tablas y si el limite `K_MIN` es apropiado.

**Comprobar:**

```python
assert len(celdas) > 0
assert min_fila["filas"] >= 1
print("Parte 3 — divulgación (vista previa): OK")
```

---

## Parte 4 — OpenStreetMap: escuelas en un departamento

Unir fuentes distintas puede mejorar el análisis y la toma de decisiones, pero también introduce desafíos **técnicos**, de **escala** y **éticos** (cobertura desigual, definición del POI, falacia ecológica — Paso 5). Aquí enriquecemos GEIH con un mapa colaborativo.

### OSM — qué es el dataset

**OpenStreetMap (OSM)** es un mapa mundial construido colaborativamente (comunidad, gobiernos, ONG). No es una encuesta: los objetos (nodos, vías, relaciones) llevan **etiquetas** `clave=valor` (p. ej. `amenity=school`). La cobertura y la calidad **varían por territorio**.

Documentación de OSM:

- [**Overpass por ejemplo**](https://dev.overpass-api.de/overpass-doc/es/) — guía paso a paso para **construir consultas** (`area`, `node`, filtros `["amenity"=…]`, `out`, etc.). La función `contar_nodos_amenity` de este cuaderno sigue ese patrón.
- [Sintaxis Overpass QL](https://wiki.openstreetmap.org/wiki/ES:Overpass_API/Overpass_QL) — referencia del lenguaje de consulta.
- [Overpass Turbo](https://wiki.openstreetmap.org/wiki/ES:Overpass_turbo) — editor web para probar una consulta antes de pegarla en Python.
- [Acerca de OpenStreetMap](https://www.openstreetmap.org/about): qué es el proyecto y la licencia de datos ([ODbL](https://www.openstreetmap.org/copyright)).
- [Wiki OSM — etiqueta `amenity`](https://wiki.openstreetmap.org/wiki/Key:amenity) y [`amenity=school`](https://wiki.openstreetmap.org/wiki/Tag:amenity=school): qué cuenta como “escuela” en el mapa.
- [Overpass API](https://wiki.openstreetmap.org/wiki/Overpass_API): uso responsable del servidor público (pausas, `User-Agent`).
- [Relaciones y límites administrativos](https://wiki.openstreetmap.org/wiki/Relation): por qué un departamento es una `relation` con `admin_level=4`.
- [Nariño en OSM (relación 1380130)](https://www.openstreetmap.org/relation/1380130): límite que usamos en código.
- [Taginfo — `amenity=school`](https://taginfo.openstreetmap.org/tags/amenity=school): frecuencia de la etiqueta en el planeta (contexto, no verdad oficial).

En L1 automatizamos la descarga GEIH consultando la página web directamente. En esta oportunidad consultamos OSM con **`requests.post`** al API Overpass (consultas en [**Overpass QL**](https://dev.overpass-api.de/overpass-doc/es/)). Reutilice el **`User-Agent` ASCII** de la celda inicial.

En este ejercicio vamos a contar nodos con **`amenity=school`** en **Nariño** (código DANE **`52`**) y comparar con el tamaño de la muestra GEIH del mismo departamento.

### Paso 1 — Configuración OSM

En la sección de configuración realizamos los import basicos y asignamos las variables y constantes que se utilizarán en el resto del cuaderno.

Cada departamento tiene un **id de relación** en OSM (límite administrativo, `admin_level=4`). Para Nariño la relación es **`1380130`**. En Overpass el **id de área** es **`3600000000 + id_relación`** → **`3601380130`**.

```python
import json
import time

import matplotlib.pyplot as plt

# overpass_post y OVERPASS_HEADERS definidos en el repaso de Python (arriba)
OUTPUTS_DIR = Path("outputs")
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

# Nariño — código DANE 52
DPTO_DEMO = 52
DPTO_DEMO_NOMBRE = "Nariño"
OSM_RELATION_NARINO = 1380130
OSM_AREA_ID_NARINO = 3600000000 + OSM_RELATION_NARINO  # 3601380130

AMENITY_SCHOOL = "school"
PAUSA_SEG = 1.0  # pausa entre consultas (además de los reintentos de overpass_post)
```

### Paso 2 — Función para contar POI

La siguiente función consulta Overpass API para contar nodos con un `amenity` dentro de un **área** (`area({area_id})` en Overpass QL). Si modifica la consulta, revise la estructura en [**Overpass por ejemplo**](https://dev.overpass-api.de/overpass-doc/es/). Argumentos: id de área Overpass, valor de `amenity`, timeout opcional.


```python
def contar_nodos_amenity(area_id: int, amenity: str, timeout: int = 90) -> int:
    """Cuenta nodos OSM con amenity dado dentro del area_id de Overpass."""
    # Solicitud al API para retornar nodos en el area_id con un determinado amenety
    query = f"""
[out:json][timeout:60];
area({area_id})->.a;
node["amenity"="{amenity}"](area.a);
out;
"""
    resp = overpass_post(query, timeout=timeout)
    data = resp.json()
    return len(data.get("elements", []))
```

Una vez la función es definida la podemos invocar con los parámetros deseados.

```python
# Recolectamos datos sobre el tiempo que toma la solicitud al servidor
t0 = time.perf_counter()
poi_school_count = contar_nodos_amenity(OSM_AREA_ID_NARINO, AMENITY_SCHOOL)
elapsed = round(time.perf_counter() - t0, 2)
time.sleep(PAUSA_SEG)

# Imprimir el número de nodos y el tiempo de la solicitud
print(f"{DPTO_DEMO_NOMBRE} (DPTO {DPTO_DEMO}): amenity=school → {poi_school_count} nodos")
print(f"Consulta Overpass: {elapsed} s")
```

**Comprobar:**

```python
assert poi_school_count >= 0
assert poi_school_count < 15_000, (
    "Conteo OSM muy alto: ¿usó la relación del departamento (1380130) "
    "y no la de Colombia (120027)?"
)
print("Parte 4, Paso 2 — consulta OSM: OK")
```

### Paso 3 — Agregar GEIH en el mismo departamento

Comparamos **personas en la muestra GEIH** del departamento con **escuelas OSM**. Es un enlace ilustrativo, no una conclusión causal.

```python
# Creamos una copia del DataFrame y convertimos la columna DPTO a un valor numérico
work_dpto = df.copy()
work_dpto["DPTO"] = pd.to_numeric(work_dpto["DPTO"], errors="coerce")

# Agrupar por DPTO, contar personas en la muestra por departamento y convertir el resultado a int
geih_dpto = (
    work_dpto.groupby("DPTO")
    .size()
    .reset_index(name="personas_muestra")
)
geih_dpto["DPTO"] = geih_dpto["DPTO"].astype(int)

# Filtrar la fila que corresponde a Nariño
fila_demo = geih_dpto.loc[geih_dpto["DPTO"] == DPTO_DEMO]
if fila_demo.empty:
    raise ValueError(f"No hay filas GEIH para DPTO {DPTO_DEMO} en este mes.")

# Extraer el número de nariñenses en la muestra
personas_demo = int(fila_demo["personas_muestra"].iloc[0])

# Unir el número de nariñenses del dataset del DANE con el número de escuelas obtenido desde OSM
enlace = pd.DataFrame(
    [
        {
            "dpto": DPTO_DEMO,
            "nombre": DPTO_DEMO_NOMBRE,
            "personas_muestra": personas_demo,
            "poi_school_count": poi_school_count,
        }
    ]
)
print(enlace.to_string(index=False))
enlace.to_csv(OUTPUTS_DIR / "enlace_geih_osm_demo.csv", index=False)
```

**Comprobar:**

```python
assert personas_demo > 0
assert enlace["poi_school_count"].iloc[0] == poi_school_count
print("Parte 4, Paso 3 — agregado GEIH: OK")
```

### Paso 4 — Gráfico simple del enlace

```python
fig, ax = plt.subplots(figsize=(5, 3))
ax.bar(["Personas\n(muestra GEIH)", "Escuelas\n(OSM)"], [personas_demo, poi_school_count], color=["#4472C4", "#ED7D31"])
ax.set_title(f"Nariño (DPTO {DPTO_DEMO}) - enero 2024")
ax.set_ylabel("Conteo")
fig.tight_layout()
fig.savefig(OUTPUTS_DIR / "enlace_geih_osm_demo.png", dpi=120)
plt.show()
print(f"Figura guardada: {OUTPUTS_DIR / 'enlace_geih_osm_demo.png'}")
```

La unión de diferentes datasets crean oportunidades para mejorar nuestros análisis. Su tarea en este curso es enriquecer el dataset del DANE con datasets como el de OSM. Sin embargo, en el proceso se deben tener en cuenta algunos aspectos éticos y de governanza de datos:

1. **Cobertura desigual de OSM.** No todos los departamentos están mapeados con la misma calidad. Pocos POI no siempre significa pocos servicios reales.
2. **Falacia ecológica.** Un patrón a nivel departamento no prueba nada sobre una persona concreta.
3. **Sesgo urbano.** Las ciudades suelen tener más nodos OSM que zonas rurales.
4. **Definición del POI.** Aquí contamos solo **`amenity=school`**. Otro tag daría otra historia.

**Comprobar:**

```python
assert (OUTPUTS_DIR / "enlace_geih_osm_demo.csv").is_file()
print("Parte 4 — OSM + enlace GEIH: OK")
```

---

## Tareas

Esta sección define **qué entregar en Moodle** para la semana 1. Plantillas en la [página de esta lección](https://cabrerac.github.io/teaching/26-udenar-big-data/l2-ethics-governance/).

### Trabajo en grupo (60 % de la formativa semana 1)

Use el Colab plantilla **[`week-1-group`](https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-big-data/week-1-group.ipynb)**. Consolida **L1 + L2**. Entregar ZIP **`week-1-<group_id>.zip`** hasta el **lunes 8 de junio de 2026**:

| Archivo en el ZIP | Descripción |
|-------------------|-------------|
| `notebook-week-1-group-<group_id>.ipynb` | Cuaderno grupal ejecutado (renombre desde `week-1-group`) |
| `manifest.json` | Registro de acceso DANE |
| `outputs/osm_poi_by_dpto.csv` | Conteos OSM por departamento (cuaderno `week-1-group`) |

### Reflexión individual (40 % de la formativa semana 1)

PDF **`week-1-reflection-<student>.pdf`** hasta el **martes 9 de junio de 2026**. Cubre L1 y L2 (plantilla semana 1).

### Requerimientos del proyecto

`project_requirements.pdf` (plantilla Word en esta lección) se discute en la **semana 2**. En el **sábado 6 jun** avance en la plantilla, ver [plan de sesión semana 1](/assets/documents/26-udenar-big-data/week-1-session-plan-es.pdf).

<!-- end NOTEBOOK: -->
