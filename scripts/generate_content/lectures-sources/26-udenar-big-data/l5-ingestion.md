---
course_code: 26-udenar-big-data
title: Data ingestion and workflow
description: Lecture 5 introduces batch and stream ingestion approaches. Once our data is harmonised on a lakehouse, we need to create data artefacts and views to feed our analytic tasks. These artefacts can be created and processed offline following a schedule (i.e., batch) or in real-time (i.e., streaming) depending on the data nature. This lecture introduces both concepts and the production platforms and tools that support them.
session: 5
start_time: 07:00 am
end_time: 01:00 pm
hours: 5
author: Christian Cabrera Jojoa
email: chc79@cam.ac.uk
position: Assistant Research Professor
department: Department of Computer Science and Technology
institution: University of Cambridge
layout: lecture
lecture_code: l5-ingestion
lecture_date: 20/06/2026
permalink: /teaching/26-udenar-big-data/l5-ingestion/
visible: true
group_notebook: week-3-group
notebook_language: es
notebook_title: Ingesta y flujos de trabajo
notebook_description: Práctica individual de la Lección 5. Pasamos de la ingesta batch sobre el lakehouse GEIH de la semana 2 a una fuente en streaming con Kafka. Registramos auditoría y contrato de esquema.
---

<!-- SLIDES: -->

# Last Time

<!-- end SLIDES: -->

{% include _snippets/26-udenar-big-data/l5-ingestion/last-time.md %}

<!-- SLIDES: -->

# Data Ingestion

<!-- end SLIDES: -->

{% include _snippets/26-udenar-big-data/l5-ingestion/ingestion.md %}

<!-- SLIDES: -->

# Batch and ETL

<!-- end SLIDES: -->

{% include _snippets/26-udenar-big-data/l5-ingestion/batch-etl.md %}

<!-- SLIDES: -->

# Streams

<!-- end SLIDES: -->

{% include _snippets/26-udenar-big-data/l5-ingestion/streams.md %}

<!-- SLIDES: -->

# Conclusions

<!-- end SLIDES: -->

{% include _snippets/26-udenar-big-data/l5-ingestion/conclusions.md %}

{% include _snippets/26-udenar-big-data/l5-ingestion/practical-slides.md %}

<!-- RENDER: -->

### Week 3 links

- [Week 3 hub](/teaching/26-udenar-big-data/week-3-hub-es/)

### Resources

- [Introductory Python course](https://www.youtube.com/watch?v=nKPbfIU442g) (optional video)
- [Apache Kafka documentation](https://kafka.apache.org/documentation/) (reference)

### References

- Zaharia, M., et al. (2016). [Apache Spark: a unified engine for big data processing](https://doi.org/10.1145/2934664). *CACM*, 59(11), 56–65.
- Jarrahi, M. H., et al. (2023). *The Principles of Data-Centric AI*. *(Course PDF.)*
- Kreps, J., Narkhede, N., & Rao, J. (2011). Kafka: a distributed messaging system for log processing. *(Recommended async.)*

<!-- end RENDER: -->

<!-- NOTEBOOK: -->

## Repaso de Python para este cuaderno

Antes del laboratorio repasamos cuatro ideas que usaremos en las Partes 1 a 7. Si vienen de las lecciones 3 y 4 ya conocen Parquet y agregados. Aquí lo nuevo es **leer y procesar datos que llegan poco a poco** y **registrar lo que hacemos**.

### Diccionarios y desempaquetado con `**`

Cada paso del pipeline produce un **evento**: un diccionario con qué pasó, cuándo y de dónde salieron los datos. El operador **`**`** copia las claves de un diccionario dentro de otro. Lo usamos para **añadir** una marca de tiempo sin tocar el evento original.

Primero creamos un evento de ejemplo:

```python
evento = {"paso": "ingesta", "filas": 1200}
print("Evento original:", evento)
```

Ahora le añadimos una clave nueva copiando las anteriores con `**`:

```python
evento_con_hora = {**evento, "hora": "2026-06-20T07:00"}
print("Evento ampliado:", evento_con_hora)
# El original no cambió: ** crea un diccionario nuevo
assert "hora" not in evento
assert evento_con_hora["filas"] == 1200
print("Desempaquetado con **: OK")
```

### Registrar eventos en un archivo JSONL (`audit.jsonl`)

Un **log de auditoría** (en español, *bitácora*) es un archivo donde **añadimos una línea por cada paso**, sin borrar lo anterior. Usamos el formato **JSONL**: un JSON por línea. Esto nos da **trazabilidad** (de la Lección 2): cualquiera puede revisar qué se hizo con los datos y cuándo.

Para implementar lo descrito anteriormente implementamos la función `registrar` en donde abrimos el archivo bitacora en modo **`"a"`** (de *append*, añadir) para no sobrescribir lo ya escrito. Después podemos invocar la función por cada evento que queramos registrar y leerlo desde donde deseemos:

```python
import json
from datetime import datetime, timezone
from pathlib import Path

audit_demo = Path("audit_demo.jsonl")


def registrar(evento: dict, ruta: Path = audit_demo) -> None:
    """Añade un evento (con marca de tiempo UTC) como una línea JSON.

    Parámetros:
        evento: dict con lo que pasó (paso, filas, fuente, …).
        ruta: archivo JSONL donde se añade la línea.
    """
    # Copiamos el evento y le agregamos la hora actual en UTC
    linea = {**evento, "ts_utc": datetime.now(timezone.utc).isoformat()}
    # Modo "a": cada llamada añade una línea, no borra las previas
    with ruta.open("a", encoding="utf-8") as f:
        f.write(json.dumps(linea, ensure_ascii=False) + "\n")


registrar({"paso": "demo", "filas": 3})
registrar({"paso": "demo", "filas": 7})

lineas = audit_demo.read_text(encoding="utf-8").strip().splitlines()
print("Líneas en la bitácora:", len(lineas))
print("Bitácora JSONL: OK")
```

Cada línea es independiente: por eso podemos leer el archivo más tarde y reconstruir **todo lo que pasó**, en orden.

### Un *tópico* de Kafka es una lista de mensajes (modelo mental)

En la segunda mitad del cuaderno usamos **Kafka**. Antes de conectarnos a un servidor real, entendamos la idea con Python puro. Un **tópico** es como una **lista a la que solo se agrega un elemento al final**:

- el **productor** *escribe* mensajes al final de la lista;
- el **consumidor** *lee* desde una posición (el *offset*) hacia adelante.

Simulamos un tópico con una lista:

```python
topico_demo: list[dict] = []  # un "tópico" = lista de mensajes


def producir(mensaje: dict) -> None:
    """Productor: agrega un mensaje al final del tópico."""
    topico_demo.append(mensaje)


def consumir(desde: int = 0) -> list[dict]:
    """Consumidor: lee los mensajes desde una posición (offset) en adelante."""
    return topico_demo[desde:]


producir({"id": 1, "titular": "Empleo sube en Nariño"})
producir({"id": 2, "titular": "Desempleo nacional estable"})

print("Mensajes en el tópico:", len(topico_demo))
print("Leídos desde offset 0:", consumir(0))
assert len(consumir(0)) == 2
print("Modelo mental de Kafka: OK")
```

Kafka hace esto mismo, pero **distribuido y persistente**: el productor y el consumidor pueden estar en computadores distintos y el tópico sobrevive aunque se apaguen.

### Una base de datos documental con `mongomock`

Los eventos del stream son **semi-estructurados** (JSON con campos que pueden variar). Para almacenarlos no usamos tablas rígidas (como Parquet o SQL), sino una **base de datos documental**: guarda **documentos** tipo JSON, sin esquema fijo. En producción la herramienta típica es **MongoDB**. Aquí usamos **`mongomock`**, que **emula la misma API de MongoDB en memoria**, sin instalar servidor.

Para usar **`mongomock`** primero debemos instalar la librería.

```python
%pip install -q mongomock
```

Después podemos importarlo y utilizarlo como cualquier otra dependencia.

```python
import mongomock
# Servidor real (pip install pymongo): from pymongo import MongoClient
# cliente = MongoClient("mongodb://host:27017/")  # URI del clúster; en producción suele leerse de una variable de entorno

# Un cliente en memoria → una base → una colección de documentos
cliente = mongomock.MongoClient()
coleccion = cliente["demo"]["noticias"]

# insert_many añade varios documentos (no requieren las mismas claves)
coleccion.insert_many(
    [
        {"url": "a", "titular": "Empleo sube en Nariño"},
        {"url": "b", "titular": "Desempleo baja", "fuente": "ejemplo"},
    ]
)

print("Documentos guardados:", coleccion.count_documents({}))
# find consulta documentos; {"_id": 0} oculta el id interno
for doc in coleccion.find({}, {"_id": 0}):
    print(doc)

assert coleccion.count_documents({}) == 2
print("Base documental (mongomock): OK")
```

La misma API (`insert_many`, `find`, `count_documents`) funciona contra un MongoDB real cambiando solo la línea del cliente. Por eso aprendemos el patrón aquí sin montar un servidor.

---

## Instrucciones

En las lecciones 3 y 4 **guardamos** GEIH en un lakehouse (Parquet particionado) y lo **consultamos** con varios motores. Ya tenemos datos confiables, pero **estáticos**: una foto mensual de una encuesta oficial.

La **ingesta** es la capa que *trae* datos al lakehouse y los deja listos para analizar. Veremos dos modos:

- **Batch** (por lotes): procesamos un conjunto **acotado** que ya existe, las particiones GEIH. Lo hacemos de forma **gobernada**: dejamos bitácora y contrato de esquema.
- **Streaming** (flujo): leemos datos que **llegan poco a poco y no terminan** en este caso usando **Kafka**. Por ejemplo, titulares de noticias que se producen todo el tiempo.

GEIH es fuerte en **volumen** y **veracidad** (es oficial), pero **lenta** (mensual) y **estructurada**. Para experimentar las otras *V* del big data (i.e., **velocidad** y **variedad**) necesitamos una fuente distinta. Las noticias llegan a toda hora (velocidad) y son texto libre (variedad), pero **no son estadística oficial** (veracidad baja). Al final del cuaderno trabajamos **sin GEIH** no para reemplazarla, sino para **experimentar** una *V* que la encuesta no permite.

**Prerrequisito.** Tener `data/processed/geih-spine/` con particiones **2022–2025** en Google Drive (entregable del **`week-2-group`**, Ejercicio 1). Si su grupo aún no terminó, la **Parte 0** de este cuaderno incluye una **solución compacta** del mismo ejercicio (solo lakehouse; sin MapReduce ni privacidad).

Las herramientas de ingesta requiren gran cantidad de computo a nivel industrial. Aquí usamos versiones en ambientes ligeros que enseñan la misma idea:

| Capa | En producción | En este curso |
|------|---------------|---------------|
| Orquestación | Airflow / Dagster | **Prefect** (local) |
| Streaming | Cluster de Kafka + Flink | **Un broker Kafka local** (en este runtime) |
| Almacén del stream | MongoDB / Cassandra | **MongoDB en memoria** (`mongomock`) |
| Fuente batch | Lakehouse gobernado | Parquet de **`week-2-group`** |
| Fuente stream | Mercados / logs en vivo | **Noticias (RSS)** + reproducción |

**Qué hace el cuaderno (en orden).**

| Parte | Tema |
|-------|------|
| **1** | Montar Drive, rutas e instalar librerías |
| **0** | **Solución compacta** `week-2-group` Ej. 1 — lakehouse 2022–2025 si falta *(ejecute la Parte 1 antes)* |
| **2** | Puente: leer el lakehouse de la semana 2 |
| **3** | Ingesta **batch gobernada**: capa `curated/` + bitácora + contrato |
| **4** | Orquestar el ETL de **un año completo** con **Prefect** |
| **5** | Levantar un **broker Kafka local** y un **productor** de noticias |
| **6** | **Consumidor Kafka** → deduplicar → guardar en **MongoDB** (documental) |
| **7** | **Velocidad a escala**: reproducir muchos eventos |

**Tareas** al final define los entregables de la semana.

---

## Parte 1. Configuración: Drive, rutas y librerías

Montamos la **misma raíz** que en las lecciones 3 y 4, para reutilizar el lakehouse. Si trabaja **en local** con el mismo layout de carpetas, ponga `USE_GOOGLE_DRIVE = False`.

```python
from pathlib import Path

USE_GOOGLE_DRIVE = True

# Detectamos si estamos en Colab (para montar Drive solo allí)
try:
    import google.colab  # noqa: F401
    IN_COLAB = True
except ImportError:
    IN_COLAB = False

# Si usamos Colab y estamos en Colab
if USE_GOOGLE_DRIVE and IN_COLAB:
    from google.colab import drive

    drive.mount("/content/drive")
    # Misma carpeta que en L3/L4: ahí está el lakehouse de la semana 2
    WORK_ROOT = Path("/content/drive/MyDrive/udenar/cease/2026/big-data/")
    print(f"Raíz en Drive: {WORK_ROOT}")
else:
    WORK_ROOT = Path(".")
    print(f"Raíz local: {WORK_ROOT.resolve()}")
```

Definimos las rutas de trabajo. La capa **`curated/`** guarda agregados listos para analizar; **`staging/`** guarda datos del stream a medio procesar; **`audit.jsonl`** es la bitácora; **`schema_contract.json`** describe qué columnas publicamos.

```python
PROCESSED_DIR = WORK_ROOT / "data" / "processed" / "geih-spine"  # lakehouse de la semana 2
CURATED_DIR = WORK_ROOT / "data" / "curated"                     # agregados gobernados
STAGING_DIR = WORK_ROOT / "data" / "staging"                     # datos del stream
AUDIT_PATH = WORK_ROOT / "data" / "audit.jsonl"                  # bitácora de pasos
SCHEMA_PATH = WORK_ROOT / "data" / "schema_contract.json"        # contrato de esquema
MANIFEST_PATH = WORK_ROOT / "manifest.json"                      # metadatos (de la semana 2)

# Nombre del tópico de noticias. En el cuaderno grupal cada grupo usa su propio id.
TOPIC_NEWS = "udenar.news.raw"
TOPIC_REPLAY = "udenar.news.replay"  # Parte 7: solo eventos sintéticos de velocidad

# Creamos las carpetas de salida si no existen
for d in (CURATED_DIR, STAGING_DIR):
    d.mkdir(parents=True, exist_ok=True)

print("Lakehouse de entrada:", PROCESSED_DIR)
print("Salidas en:", CURATED_DIR, "y", STAGING_DIR)
```

Instalamos las librerías que **no** vienen en Colab. Cada una cubre una parte del pipeline:

- **Prefect:** orquesta el batch (encadena pasos en un *flujo*).
- **kafka-python-ng:** cliente para **publicar** y **leer** mensajes de Kafka (i.e., streams).
- **feedparser:** descarga y lee **feeds RSS** de noticias.
- **mongomock:** una base de datos documental (estilo MongoDB) **en memoria**.
- **Polars / PyArrow:** leen Parquet y agregan, como en las lecciones 3 y 4.

```python
%pip install -q polars pyarrow pandas "prefect>=2.20,<3" kafka-python-ng feedparser mongomock requests nest-asyncio
```

### Si pip muestra ERROR de dependencias (Colab)

Colab **ya trae instaladas** muchas librerías (Google ADK, Hugging Face, W&B, Spark Connect, etc.). Cuando `%pip install` añade las nuestras, el resolvedor compara versiones con **todo** el entorno. A veces imprime en rojo:

`ERROR: pip's dependency resolver does not currently take into account all the packages that are installed.`

**Eso no significa que la instalación falló.** Significa: *algún paquete que Colab trae de fábrica y que **este cuaderno no usa** preferiría otra versión de `websockets`, `click` o `typer`.*

También puede aparecer `Building wheel for sgmllib3k (setup.py) ... done`: pip **compila** una dependencia pequeña de `feedparser`; es **normal**.

| Mensaje típico | Qué significa | ¿Preocuparse? |
|----------------|---------------|---------------|
| `dependency conflicts` + `google-adk`, `langgraph-sdk`, `langsmith` | Colab trae esas herramientas de IA; **no las usamos** en este cuaderno | No |
| `dataproc-spark-connect` + `websockets` | Entorno Spark de Colab; **no lo usamos** aquí | No |
| `wandb` / `huggingface-hub` + `click` o `typer` | Herramientas de experimentos/modelos; **no las usamos** aquí | No |
| `websockets 13.1` incompatible | Desfase con el runtime global de Colab, no con Prefect/Kafka/Polars de esta lección | No |

**Qué hacer:** continúe con la celda de importaciones. Si `import polars`, `from kafka import ...` y el flujo Prefect funcionan, **ignore** esos avisos. Solo investigue si una importación **de este cuaderno** falla de verdad.

Importamos todas las librerías que necesitamos. El cliente de Kafka (`KafkaProducer`/`KafkaConsumer`) lo usaremos contra el broker local que levantamos en la Parte 5.

```python
import json         # manejo de datos en formato JSON
import os           # operaciones con el sistema de archivos y variables de entorno
import time         # funciones relacionadas con el tiempo (pausas, timestamps)
import uuid         # generación de identificadores únicos
from datetime import datetime, timezone  # manejo y conversión de fechas y zonas horarias

import feedparser   # leer y analizar feeds RSS/Atom de noticias
import mongomock    # base de datos documental (MongoDB) en memoria
import polars as pl # procesamiento eficiente de datos tabulares (como pandas, pero más rápido)
import requests     # realizar peticiones HTTP (descargar datos, interactuar con APIs)
from kafka import KafkaConsumer, KafkaProducer  # cliente Kafka (productor/consumidor)

try:
    import nest_asyncio  # permite ejecutar Prefect dentro de Jupyter/Colab
    nest_asyncio.apply()
except ImportError:
    pass

print("Dependencias: OK")
```

**Comprobar:**

```python
assert WORK_ROOT.is_dir()
print("Parte 1, configuración: OK — siga con la Parte 0 si el lakehouse aún no está completo")
```

---

## Parte 0. Solución compacta del lakehouse (`week-2-group`, Ejercicio 1)

Este bloque es la **referencia compacta** del **Ejercicio 1** del cuaderno grupal de la semana 2: harmonizar **2022–2025** y publicar el lakehouse `data/processed/geih-spine/` (Parquet particionado). **No** incluye MapReduce, benchmark de motores ni publicación con k=5/Laplace (Ejercicios 2–3 del grupal): eso sigue siendo trabajo del grupo.

Sirve para **comparar** su entrega grupal y para **desbloquear** esta lección si el lakehouse aún no está en Drive. Las funciones vienen de **`l3-storage`** (Partes 0 y 2).

**Ejecute la Parte 1 antes** (Drive montado y rutas definidas). Con **`SKIP_SPINE_BUILD = True`** (por defecto) solo **comprueba** particiones; con **`False`** construye el árbol (puede tardar en Colab).

| Paso | Qué hace |
|------|----------|
| **0.1** | Comprobar cuántas particiones hay por año |
| **0.2** | Funciones `harmonize_month` (copiadas de L3) |
| **0.3** | Escribir `anio=…/mes=…/part-000.parquet` para 2022–2025 |

### Paso 0.1. Comprobar el lakehouse

```python
SPINE_YEARS = [2022, 2023, 2024, 2025]
SKIP_SPINE_BUILD = True       # False → construye geih-spine aquí (como week-2 Ej. 1)
SKIP_IF_PARQUET_EXISTS = True  # True → no reescribe particiones que ya existen

RAW_DIR = WORK_ROOT / "data" / "raw"


def count_spine_months(spine_dir: Path, year: int) -> int:
    """Cuenta particiones mensuales con Parquet para un año."""
    return len(list(spine_dir.glob(f"anio={year}/mes=*/part-*.parquet")))


def spine_is_complete(spine_dir: Path, years: list[int], min_months: int = 12) -> bool:
    """True si cada año tiene al menos min_months particiones mensuales."""
    if not spine_dir.is_dir():
        return False
    return all(count_spine_months(spine_dir, y) >= min_months for y in years)


def count_month_folders(year_dir: Path) -> int:
    """Cuenta carpetas mensuales con al menos un CSV."""
    if not year_dir.is_dir():
        return 0
    n = 0
    for p in year_dir.iterdir():
        if not p.is_dir():
            continue
        if any(f.is_file() and f.suffix.lower() == ".csv" for f in p.iterdir()):
            n += 1
    return n


def raw_is_complete(raw_root: Path, years: list[int]) -> bool:
    """True si data/raw tiene ≥12 meses con CSV por cada año."""
    return all(count_month_folders(raw_root / str(y)) >= 12 for y in years)


particiones_por_anio = {y: count_spine_months(PROCESSED_DIR, y) for y in SPINE_YEARS}
print("Particiones en geih-spine:", particiones_por_anio)
print("¿Lakehouse completo (≥12 meses/año)?", spine_is_complete(PROCESSED_DIR, SPINE_YEARS))
print("CSV en raw por año:", {y: count_month_folders(RAW_DIR / str(y)) for y in SPINE_YEARS})
```

### Paso 0.2. Harmonización

Reutilizamos la misma **`harmonize_month`** que en L3 y en **`week-2-group`**: une Fuerza de trabajo + Características generales, renombra columnas y fija tipos para Parquet.

```python
import re

import pandas as pd

CSV_SEP = ";"
CSV_ENCODING = "latin-1"
PRIMARY_TABLE_KEYWORD = "fuerza de trabajo"
DEMOG_TABLE_KEYWORDS = ("caracter", "generales")
PERSON_KEYS = ["DIRECTORIO", "HOGAR", "ORDEN"]


def read_geih_csv(path: Path, usecols=None) -> pd.DataFrame:
    """Lee un CSV del DANE (; o ,, encoding latin-1)."""
    for sep in (CSV_SEP, ","):
        try:
            df = pd.read_csv(path, sep=sep, encoding=CSV_ENCODING, usecols=usecols, low_memory=False)
        except ValueError:
            continue
        if len(df.columns) > 1:
            return df
    raise ValueError(f"No se pudo parsear {path.name}")


def _csv_files(month_dir: Path) -> list[Path]:
    """Lista los CSV de una carpeta de mes (acepta extensión .CSV y .csv).

    Parámetros:
        month_dir: carpeta de un mes con los archivos del DANE.

    Retorna:
        Rutas de los CSV, ordenadas y sin duplicados.
    """
    return sorted({*month_dir.glob("*.CSV"), *month_dir.glob("*.csv")})


def _norm_csv_name(path: Path) -> str:
    """Normaliza el nombre de archivo para comparar: minúsculas y espacios simples.

    Reemplaza el espacio especial \xa0 por uno normal y colapsa espacios repetidos,
    para que la búsqueda por palabra clave funcione aunque el nombre venga irregular.

    Parámetros:
        path: ruta del archivo.

    Retorna:
        El nombre del archivo normalizado.
    """
    return re.sub(r"\s+", " ", path.name.lower().replace("\xa0", " "))


def _labour_csv(month_dir: Path) -> Path:
    """Encuentra el CSV de 'fuerza de trabajo' en la carpeta del mes.

    Parámetros:
        month_dir: carpeta de un mes.

    Retorna:
        La ruta del CSV de fuerza de trabajo.

    Lanza:
        FileNotFoundError: si no hay ningún archivo que coincida.
    """
    for p in _csv_files(month_dir):
        if PRIMARY_TABLE_KEYWORD in _norm_csv_name(p):
            return p
    raise FileNotFoundError(f"Sin fuerza de trabajo en {month_dir.name}")


def _demog_csv(month_dir: Path) -> Path:
    """Encuentra el CSV de 'características generales' en la carpeta del mes.

    Parámetros:
        month_dir: carpeta de un mes.

    Retorna:
        La ruta del CSV de características generales.

    Lanza:
        FileNotFoundError: si no hay ningún archivo que coincida.
    """
    for p in _csv_files(month_dir):
        if all(kw in _norm_csv_name(p) for kw in DEMOG_TABLE_KEYWORDS):
            return p
    raise FileNotFoundError(f"Sin características generales en {month_dir.name}")


def month_dirs_for_year(year_dir: Path) -> list[Path]:
    """Lista las carpetas de mes que tienen las DOS tablas necesarias.

    Recorre las subcarpetas de un año y conserva solo las que tienen tanto el CSV
    de fuerza de trabajo como el de características generales; avisa y omite las demás.

    Parámetros:
        year_dir: carpeta de un año (con subcarpetas por mes).

    Retorna:
        Rutas de las carpetas de mes utilizables, ordenadas.
    """
    dirs = []
    for p in sorted(year_dir.iterdir()):
        if not p.is_dir():
            continue
        try:
            _labour_csv(p)   # ¿existe fuerza de trabajo?
            _demog_csv(p)    # ¿existe características generales?
            dirs.append(p)
        except FileNotFoundError as e:
            print(f"Advertencia — omitido {p.name}: {e}")
    return dirs


def a_entero(serie: pd.Series) -> pd.Series:
    """Convierte una columna a entero que admite nulos (Int64 de pandas).

    to_numeric(errors='coerce') vuelve NaN lo que no sea número; Int64 (con I mayúscula)
    es el entero de pandas que permite valores faltantes.

    Parámetros:
        serie: columna a convertir.

    Retorna:
        La columna como Int64.
    """
    return pd.to_numeric(serie, errors="coerce").astype("Int64")


def harmonize_month(month_dir: Path) -> pd.DataFrame:
    """Harmoniza un mes GEIH → una fila/persona, columnas en español."""
    labour = read_geih_csv(_labour_csv(month_dir))
    demog = read_geih_csv(_demog_csv(month_dir), usecols=PERSON_KEYS + ["P6040", "P3271"])
    merged = labour.merge(demog, on=PERSON_KEYS, how="left", validate="many_to_one")
    periodo = merged["PERIODO"].astype(int)
    anio = (periodo // 10000).astype(int)
    mes = ((periodo // 100) % 100).astype(int)
    out = pd.DataFrame(
        {
            "periodo": (anio * 100 + mes).astype(int),
            "anio": anio,
            "mes": mes,
            "id_hogar": merged["DIRECTORIO"].astype(str) + "-" + merged["HOGAR"].astype(str),
            "orden_persona": a_entero(merged["ORDEN"]),
            "dpto": a_entero(merged["DPTO"]),
            "area": a_entero(merged["AREA"]),
            "edad": a_entero(merged["P6040"]),
            "sexo": a_entero(merged["P3271"]),
            "actividad": pd.to_numeric(merged["P6240"], errors="coerce"),
            "factor_expansion": pd.to_numeric(merged["FEX_C18"], errors="coerce"),
        }
    )
    out["periodo"] = out["periodo"].astype("int32")
    out["anio"] = out["anio"].astype("int32")
    out["mes"] = out["mes"].astype("int32")
    out["actividad"] = out["actividad"].astype("float64")
    out["factor_expansion"] = out["factor_expansion"].astype("float64")
    return out


print("harmonize_month: OK")
```

### Paso 0.3. Construir el lakehouse 2022–2025

Recorremos **todos los años** y escribimos una partición Parquet por mes, igual que en **`week-2-group`**, Paso 1.2.

```python
if spine_is_complete(PROCESSED_DIR, SPINE_YEARS):
    print("Lakehouse ya completo — omitimos construcción (compare con su week-2-group).")
elif SKIP_SPINE_BUILD:
    print(
        "AVISO: lakehouse incompleto. Complete week-2-group Ej. 1 "
        "o ponga SKIP_SPINE_BUILD = False y vuelva a ejecutar esta celda."
    )
else:
    if not raw_is_complete(RAW_DIR, SPINE_YEARS):
        raise FileNotFoundError(
            "Faltan CSV 2022–2025 en data/raw/. "
            "Ejecute l3-storage Parte 0 o week-1-group primero."
        )
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    spine_stats: list[dict] = []
    for survey_year in SPINE_YEARS:
        year_dir = RAW_DIR / str(survey_year)
        for month_dir in month_dirs_for_year(year_dir):
            sample = harmonize_month(month_dir)
            y = int(sample["anio"].iloc[0])
            m = int(sample["mes"].iloc[0])
            part_dir = PROCESSED_DIR / f"anio={y}" / f"mes={m:02d}"
            part_file = part_dir / "part-000.parquet"
            if SKIP_IF_PARQUET_EXISTS and part_file.is_file():
                n_rows = len(pd.read_parquet(part_file, columns=["dpto"]))
                print(f"Omitido (ya existe): {part_file.relative_to(WORK_ROOT)}")
            else:
                part_dir.mkdir(parents=True, exist_ok=True)
                sample.to_parquet(part_file, index=False, use_dictionary=False)
                n_rows = len(sample)
                print(f"Escrito {part_file.relative_to(WORK_ROOT)} | filas: {n_rows:,}")
            spine_stats.append({"anio": y, "mes": m, "filas": n_rows})
    resumen = pd.DataFrame(spine_stats).sort_values(["anio", "mes"])
    print("\nResumen construcción lakehouse:")
    print(resumen.groupby("anio")["mes"].count().to_string())
    print("Total filas:", f"{resumen['filas'].sum():,}")
```

**Comprobar:**

```python
particiones_por_anio = {y: count_spine_months(PROCESSED_DIR, y) for y in SPINE_YEARS}
print("Particiones finales:", particiones_por_anio)
assert sum(particiones_por_anio.values()) >= 12, (
    "Faltan particiones en geih-spine. Ejecute week-2-group o Parte 0 con SKIP_SPINE_BUILD = False."
)
print("Parte 0, lakehouse week-2 Ej. 1: OK")
```

---

## Parte 2. Puente: leer el lakehouse de la semana 2

La ingesta batch **no parte de cero**: se apoya en lo que ya existe. Aquí confirmamos que el lakehouse está en su sitio y miramos su `manifest.json` (los metadatos que el grupo escribió en la semana 2).

```python
# Si existe el manifiesto de la semana 2, mostramos algunas de sus claves
if MANIFEST_PATH.is_file():
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    print("manifest.json (primeras claves):", list(manifest.keys())[:8])
else:
    manifest = {}
    print("Sin manifest.json — use el de su week-2-group cuando lo tenga.")
```

Listamos las particiones del lakehouse. Cada archivo `part-*.parquet` es **un mes** de un año (`anio=…/mes=…/`):

```python
# glob recorre el árbol y devuelve todas las particiones mensuales
partitions = sorted(PROCESSED_DIR.glob("anio=*/mes=*/part-*.parquet"))
print("Particiones Parquet encontradas:", len(partitions))
if partitions:
    print("Ejemplo de ruta:", partitions[0].relative_to(WORK_ROOT))
```

**Comprobar:**

```python
assert len(partitions) >= 12, (
    "Esperamos ≥12 particiones mensuales. Complete week-2-group Ej. 1 o la Parte 0 de este cuaderno."
)
print("Parte 2, puente con el lakehouse: OK")
```

---

## Parte 3. Ingesta batch gobernada: capa curated, bitácora y contrato

La ingesta batch toma datos confiables y deja una **capa lista para analizar** (`curated/`), dejando rastro de **qué** hicimos (bitácora) y **prometiendo** qué columnas publicamos (contrato). Esto es parte de la *gobernanza* de nuestros datos. Además de soportar cálculos que sean correcto, estos debe ser **trazables**.

Para enseñar el patrón usamos **una** partición de ejemplo.

### Paso 3.1. La función de bitácora

Reutilizamos la idea del Repaso, ahora apuntando a `AUDIT_PATH`. Cada paso del pipeline llamará a `append_audit` para dejar una línea.

```python
ACTIVIDAD_OCUPADO = 1  # en GEIH, actividad == 1 significa "ocupado"


def append_audit(evento: dict) -> None:
    """Añade un evento a la bitácora del pipeline (data/audit.jsonl).

    Parámetros:
        evento: dict con el paso y sus metadatos (fuente, ruta, filas, …).
    """
    # Añadimos hora UTC y escribimos una línea JSON (modo append)
    linea = {**evento, "ts_utc": datetime.now(timezone.utc).isoformat()}
    with AUDIT_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(linea, ensure_ascii=False) + "\n")


print("append_audit: definida")
```

### Paso 3.2. Construir el agregado curated

Calculamos un agregado por **departamento y mes**: cuántos ocupados hay (`conteo`) y la suma de sus factores de expansión (`ponderado`, la estimación poblacional). Usamos **Polars perezoso** (`scan_parquet`) el cual primero arma el plan y luego lo ejecuta `collect()`.

```python
sample_part = partitions[0]  # una partición = un mes de ejemplo

# scan_parquet no lee aún: define un plan de consulta perezoso
lf = pl.scan_parquet(str(sample_part))

agg = (
    lf
    .filter(pl.col("actividad") == ACTIVIDAD_OCUPADO)  # filtrar los ocupados
    .group_by(["dpto", "anio", "mes"])                 # una fila por dpto/mes
    .agg(                                              # agregaciones
        pl.len().alias("conteo"),                      # número de ocupados
        pl.col("factor_expansion").sum().alias("ponderado"),  # estimación poblacional
    )
    .collect()                                          # Se ejecuta y se lee el Parquet
)

# Guardamos el agregado en la capa curated
curated_path = CURATED_DIR / "geih_dept_month_sample.parquet"
agg.write_parquet(curated_path)

# Dejamos rastro en la bitácora
append_audit(
    {
        "stage": "batch_curated",
        "source": "geih-spine",
        "path": str(curated_path),
        "rows": agg.height,
    }
)

print(agg.head())
print("Curated escrito en:", curated_path)
```

### Paso 3.3. El contrato de esquema

Un **contrato de esquema** define las columnas, tipos y fuente de una tabla además de su forma de uso. Sirve para que quien consuma los datos sepa qué esperar, y para detectar si algo cambió sin avisar. El campo **`artifacts`** lista los archivos Parquet publicados que **comparten** ese esquema (p. ej. la muestra de un mes y, más adelante, el agregado de un año completo).

```python
schema_contract = {
    "name": "geih_dept_month_curated",
    "source": "geih-spine",
    "artifacts": [curated_path.name],  # Parquet(s) gobernados por este contrato
    "columns": [
        {"name": "dpto", "dtype": "Int64"},
        {"name": "anio", "dtype": "Int64"},
        {"name": "mes", "dtype": "Int64"},
        {"name": "conteo", "dtype": "UInt32"},
        {"name": "ponderado", "dtype": "Float64"},
    ],
    # Nota de gobernanza: estos son agregados, no microdatos de personas
    "retention_note": "Agregados para analítica — no publicar microdatos.",
}

SCHEMA_PATH.write_text(json.dumps(schema_contract, indent=2), encoding="utf-8")
append_audit({"stage": "schema_contract", "path": str(SCHEMA_PATH)})
print("schema_contract.json escrito con", len(schema_contract["columns"]), "columnas")
```

**Comprobar:**

```python
assert curated_path.is_file(), "No se escribió la capa curated"
assert SCHEMA_PATH.is_file(), "No se escribió el contrato de esquema"
assert agg.height > 0, "El agregado quedó vacío"
print("Parte 3, ingesta batch gobernada: OK")
```

---

## Parte 4. Orquestar el ETL de un año con Prefect

En la Parte 3 hicimos el ETL **a mano** para **un mes**. Aquí subimos de escala: el mismo patrón, pero **orquestado** para **todas las particiones de un año** (p. ej. los 12 meses de 2022).

Un pipeline real tiene **varios pasos** que deben correr en orden y, si algo falla, queremos saber **dónde**. Un **orquestador** como **Prefect** nos deja declarar pasos (`@task`) y encadenarlos en un **flujo** (`@flow`). Prefect registra cada ejecución, reintenta si pedimos, y muestra qué paso falló.

El flujo **ejecuta el ETL completo** sobre un año: cada tarea hace una operación real. Es el patrón **Extract → Transform → Load → Validate**:

- **`task_extract`** abre todas las particiones del año (Extract),
- **`task_aggregate`** agrega y escribe la capa curated (Transform + Load),
- **`task_validate`** comprueba el resultado (Validate).

Primero elegimos el año y listamos sus particiones:

```python
TARGET_YEAR = 2022  # un año completo, en el grupo extienden a 2022–2025
year_partitions = sorted(PROCESSED_DIR.glob(f"anio={TARGET_YEAR}/mes=*/part-*.parquet"))
print(f"Año {TARGET_YEAR}: {len(year_partitions)} particiones mensuales")
assert len(year_partitions) >= 1, f"No hay particiones para anio={TARGET_YEAR}"
```

Ahora definimos las tareas y el flujo del orquestador de la ETL.

```python
from prefect import flow, task
from prefect.task_runners import SequentialTaskRunner


@task
def task_extract(paths: list[str]) -> pl.LazyFrame:
    """Extract: abre todas las particiones de un año (plan perezoso)."""
    return pl.scan_parquet(paths)


@task
def task_aggregate(lf: pl.LazyFrame, salida: str) -> str:
    """Transform + Load: agrega ocupados por dpto/mes y escribe la capa curated."""
    agg = (
        lf
        .filter(pl.col("actividad") == ACTIVIDAD_OCUPADO)
        .group_by(["dpto", "anio", "mes"])
        .agg(
            pl.len().alias("conteo"),
            pl.col("factor_expansion").sum().alias("ponderado"),
        )
        .collect()
    )
    agg.write_parquet(salida)
    return salida


@task
def task_validate(path_str: str) -> int:
    """Validate: confirma que la salida tenga filas y devuelve cuántas."""
    df = pl.read_parquet(path_str)
    assert df.height > 0, "El curated no debería estar vacío"
    return df.height


@flow(name="geih_batch_ingest_year", task_runner=SequentialTaskRunner())
def batch_flow_year(paths: list[str], salida: str) -> int:
    """Flujo ETL: extrae un año → agrega/escribe → valida, y deja rastro en la bitácora."""
    lf = task_extract(paths)
    ruta = task_aggregate(lf, salida)
    n = task_validate(ruta)
    append_audit({"stage": "prefect_flow", "year": TARGET_YEAR, "rows": n, "path": ruta})
    return n
```

Una vez definidas las tareas y el flujo, podemos ejecutar el flujo Prefect.

```python
flow_out = CURATED_DIR / f"geih_dept_month_{TARGET_YEAR}.parquet"
rows = batch_flow_year([str(p) for p in year_partitions], str(flow_out))
print(f"El flujo Prefect construyó {rows} filas para el año {TARGET_YEAR}")
```

### Paso 4.1. Registrar el Parquet del año en el contrato

El contrato de la Parte 3 ya fijó el **esquema** (columnas y tipos). El flujo Prefect publicó **otro archivo** con el mismo esquema pero más filas (todo el año). Lo añadimos a `artifacts` para que quien consuma los datos sepa que `geih_dept_month_2022.parquet` está gobernado por el mismo contrato.

```python
contract = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
year_artifact = flow_out.name  # p. ej. geih_dept_month_2022.parquet
artifacts = contract.setdefault("artifacts", [])
if year_artifact not in artifacts:
    artifacts.append(year_artifact)
SCHEMA_PATH.write_text(json.dumps(contract, indent=2, ensure_ascii=False), encoding="utf-8")
append_audit({"stage": "schema_contract", "artifact": year_artifact, "path": str(SCHEMA_PATH)})
print("Contrato actualizado — artifacts:", artifacts)
```

A diferencia de la Parte 3 (un mes, a mano), aquí **el orquestador recorre todo el año**. En el cuaderno grupal ustedes **extienden** el mismo flujo a **todos los años** del lakehouse (2022–2025). En producción este patrón se ejecuta **programado** (p. ej. cada noche).

**Comprobar:**

```python
assert rows > 0, "El flujo debería haber construido al menos una fila"
assert flow_out.is_file(), "El flujo debería haber escrito el curated"
contract = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
assert flow_out.name in contract.get("artifacts", []), "El Parquet del año debe estar en schema_contract.json"
flow_df = pl.read_parquet(flow_out)
assert flow_df["anio"].unique().to_list() == [TARGET_YEAR]
print("Parte 4, orquestación de un año con Prefect: OK — meses:", flow_df["mes"].n_unique())
```

---

## Parte 5. Levantar un broker Kafka

Ahora pasamos al **streaming** sobre datos que llegan **a lo largo del tiempo**. En este caso utilizamos **titulares de noticias** sobre empleo como el flujo de información. El patrón Kafka tiene dos lados (i.e., productor y consumidor). En esta parte levantamos un **broker local** y hacemos el **productor** (quien escribe al tópico).

Recuerden del Repaso: un **tópico** es una lista a la que solo se agrega. El productor publica mensajes. El consumidor (Parte 6) los lee.

### Mensajes de log de Kafka que puede ignorar (Colab)

Levantamos un broker **local y efímero** dentro del runtime. Los clientes Python (`kafka-python-ng`) escriben trazas muy verbosas; algunas líneas dicen `ERROR` o `WARNING` aunque el ejercicio **sí funcionó**. Use como prueba los **recuentos finales** (`Eventos publicados…`, `Eventos únicos tras deduplicar…`, `Eventos de reproducción consumidos…`).

| Mensaje en el log | Qué significa | ¿Preocuparse? |
|-------------------|---------------|---------------|
| `group_id is None: disabling auto-commit` | El consumidor no tiene grupo de consumidor; Kafka avisa que no guardará *offsets* automáticamente | No en esta demo (leemos una vez desde `earliest`) |
| `Fetch to node … failed: Cancelled` | El consumidor se cerró por `consumer_timeout_ms` mientras aún había una lectura abierta al broker | No, si ya apareció el recuento de eventos leídos |
| `Topic udenar.news.replay not found in cluster metadata` | El productor envió mensajes **antes** de que el broker registrara el tópico recién creado | No, si al final publicó/consumió los 200 eventos de reproducción |
| `Building wheel…` / otros WARNING de red | Ruido del entorno Colab o del broker recién arrancado | No, salvo que `KAFKA_ENABLED` sea `False` sin explicación |

Si los números cuadran pero el log se ve alarmante, **confíe en el resultado**, no solo en la línea roja de fondo.

### Paso 5.0. Levantar un broker Kafka

En la industria Kafka corre en un **clúster** aparte (i.e., un grupo de servidores distribuidos). Para aprender, levantamos **un broker de un solo nodo dentro de este mismo runtime de Colab**, usando el modo **KRaft**. Cada cuaderno instancia su propio broker **efímero** (desaparece al cerrar la sesión). Estos pasos descargan Kafka, formatean su almacenamiento y arrancan el servidor **en segundo plano**.

```python
import socket
import subprocess
import tarfile
import urllib.request

# Kafka necesita Java. En Colab suele estar, pero verificamos su instalación
subprocess.run("apt-get -qq install -y openjdk-11-jdk-headless", shell=True, check=False)

KAFKA_PKG = "kafka_2.13-3.7.1"
KAFKA_HOME = Path(KAFKA_PKG).resolve()

# 1) Descargar y descomprimir Kafka (si no existe)
if not KAFKA_HOME.is_dir():
    url = f"https://archive.apache.org/dist/kafka/3.7.1/{KAFKA_PKG}.tgz"
    urllib.request.urlretrieve(url, "kafka.tgz")
    with tarfile.open("kafka.tgz") as t:
        t.extractall()
    print("Kafka descargado.")

bin_dir = KAFKA_HOME / "bin"
cfg = KAFKA_HOME / "config" / "kraft" / "server.properties"

# 2) Formatear el almacenamiento KRaft (una vez) con un id de clúster aleatorio
cluster_id = subprocess.check_output([str(bin_dir / "kafka-storage.sh"), "random-uuid"]).decode().strip()
subprocess.run([str(bin_dir / "kafka-storage.sh"), "format", "-t", cluster_id, "-c", str(cfg)], check=False)

# 3) Arrancar el broker en segundo plano (no bloquea el cuaderno)
subprocess.Popen(
    [str(bin_dir / "kafka-server-start.sh"), str(cfg)],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
)


def esperar_puerto(host: str = "localhost", port: int = 9092, timeout: int = 90) -> bool:
    """Espera hasta que el broker acepte conexiones en host:port (o se agote el tiempo)."""
    t0 = time.time()
    while time.time() - t0 < timeout:
        with socket.socket() as s:
            if s.connect_ex((host, port)) == 0:
                return True
        time.sleep(2)
    return False


def broker_responde(bootstrap: str = "localhost:9092", timeout: int = 30) -> bool:
    """Confirma que el broker **responde como Kafka**, no solo que abrió el puerto.

    Abrir el puerto (TCP) es necesario pero **no** suficiente: el broker tarda unos
    segundos más en atender peticiones. Creamos un productor de prueba y le pedimos
    la metadata de un tópico; si responde, el cliente ya puede publicar y leer.
    Fijamos `api_version` para **evitar la auto-negociación**, que es justo lo que
    falla (en silencio) entre `kafka-python` y los brokers Kafka 3.x.

    Parámetros:
        bootstrap: dirección del broker (host:puerto).
        timeout: segundos máximos de espera total.

    Retorna:
        True si el broker contestó; False si se agotó el tiempo.
    """
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            sonda = KafkaProducer(
                bootstrap_servers=bootstrap,
                api_version=(3, 7, 1),
                request_timeout_ms=5000,
            )
            sonda.partitions_for(TOPIC_NEWS)  # fuerza un ida y vuelta real con el broker
            sonda.close()
            return True
        except Exception:
            time.sleep(2)
    return False


# El broker está listo solo si el puerto abrió Y responde como Kafka
KAFKA_ENABLED = esperar_puerto() and broker_responde()
print("¿Broker Kafka local listo?", KAFKA_ENABLED)
```

### Paso 5.1. Apuntar el cliente al broker local

El broker quedó en `localhost:9092` sin autenticación (es local y temporal). Si por algún motivo no arrancó, seguimos en **modo sin broker**: la Parte 6 leerá los eventos directamente de memoria.

```python
KAFKA_BOOTSTRAP = "localhost:9092"
print("Bootstrap:", KAFKA_BOOTSTRAP, "| Kafka activo:", KAFKA_ENABLED)


def esperar_metadata_topico(producer, topic: str, timeout: float = 10) -> None:
    """Tras auto-crear un tópico, el broker tarda un instante en publicar su metadata."""
    t0 = time.time()
    while time.time() - t0 < timeout:
        if producer.partitions_for(topic):
            return
        time.sleep(0.25)


def publicar_eventos(producer, topic: str, eventos: list[dict]) -> None:
    """Publica eventos JSON en un tópico (lo crea si no existe).

    El primer envío auto-crea el tópico; esperamos metadata antes del resto
    para evitar el error 'Topic ... not found in cluster metadata' en Colab.
    """
    if not eventos:
        return
    fut = producer.send(topic, eventos[0])
    fut.get(timeout=10)
    producer.flush()
    esperar_metadata_topico(producer, topic)
    for ev in eventos[1:]:
        producer.send(topic, ev)
    producer.flush()
```

### Paso 5.2. Leer noticias por RSS y filtrar por tema

Diferentes fuentes de información en internet publican actualizaciones en tiempo real utilizando el formato Really Simple Syndication **RSS**. Por ejemplo, los medios de comunicación utilizan este formato para publicar sus titulares. **`feedparser`** es una libreria que descarga y lista entradas **RSS**. Como solo nos interesan noticias de **empleo**, filtramos por palabras clave. Esto es *ingesta por sondeo* (*polling*): preguntamos cada cierto tiempo "¿hay algo nuevo?".

```python
RSS_FEEDS = [
    "https://www.portafolio.co/rss/economia.xml",
    "https://www.eltiempo.com/rss/economia.xml",
]
# Palabras clave de empleo (con sinónimos para que el sondeo en vivo suela traer algo).
KEYWORDS = (
    "empleo", "desempleo", "mercado laboral", "trabajo", "trabajador", "geih",
    "ocupación", "ocupacion", "informalidad", "salario", "nómina", "nomina", "vacante",
)


def keyword_hit(text: str) -> bool:
    """True si el texto menciona alguna palabra clave de empleo."""
    t = (text or "").lower()
    return any(k in t for k in KEYWORDS)


def poll_rss_events(max_items: int = 40) -> list[dict]:
    """Sondea los feeds RSS y devuelve eventos de noticias sobre empleo.

    Parámetros:
        max_items: tope de titulares a revisar (repartido entre feeds).

    Retorna:
        Lista de eventos (dicts) con id, url, título y fuente.
        Cada evento marca geih=False: NO es estadística oficial.
    """
    events: list[dict] = []
    for url in RSS_FEEDS:
        feed = feedparser.parse(url)  # descarga y parsea el RSS
        for entry in feed.entries[: max_items // len(RSS_FEEDS)]:
            title = entry.get("title", "")
            summary = entry.get("summary", "")
            if keyword_hit(title + " " + summary):  # solo noticias de empleo
                events.append(
                    {
                        "id": str(uuid.uuid4()),         # id único del evento
                        "url": entry.get("link", ""),    # para deduplicar luego
                        "title": title,
                        "published": entry.get("published", ""),
                        "feed": url,
                        "geih": False,                   # marca: fuente NO oficial
                    }
                )
    return events


print("Funciones de RSS: definidas")
```

### Paso 5.3. Publicar los eventos al tópico

Con Kafka, **publicar** es enviar cada evento como JSON al tópico. El tópico se crea solo al primer envío. Guardamos también los eventos en memoria (`rss_events`) por si el broker no arrancó.

```python
rss_events = poll_rss_events()  # noticias de empleo capturadas por RSS

if KAFKA_ENABLED:
    # Productor: serializa cada evento a JSON y lo envía al tópico local.
    # api_version fija evita la auto-negociación (causa de envíos que fallan en silencio);
    # acks="all" pide confirmación del broker de que recibió cada mensaje.
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        api_version=(3, 7, 1),
        acks="all",
        retries=3,
        request_timeout_ms=10000,
    )
    # send() devuelve un "futuro"; publicar_eventos confirma el primero y espera metadata
    publicar_eventos(producer, TOPIC_NEWS, rss_events)
    append_audit({"stage": "kafka_produce", "topic": TOPIC_NEWS, "count": len(rss_events)})
    print("Eventos publicados al tópico:", len(rss_events))
else:
    # Sin broker: dejamos los eventos en memoria; la Parte 6 los usará igual
    append_audit({"stage": "rss_poll_memory", "count": len(rss_events)})
    print("Sin broker — eventos quedan en memoria:", len(rss_events))

print("Noticias de empleo capturadas:", len(rss_events))
```

**Comprobar:**

```python
# Puede ser 0 si hoy ningún titular menciona empleo — el patrón igual quedó claro
assert isinstance(rss_events, list)
print("Parte 5, productor de noticias: OK")
```

---

## Parte 6. Consumidor: leer el stream, deduplicar y guardar en MongoDB

El otro lado de Kafka es el **consumidor**. Lee del tópico y procesa. Aquí aplicamos dos cuidados típicos del streaming y guardamos en una **base documental**:

- **Deduplicar:** el mismo titular puede llegar varias veces; lo identificamos por su `url`.
- **Guardar como documentos:** las noticias son semi-estructuradas, así que su sitio natural es **MongoDB** (aquí, `mongomock`), no una tabla rígida.

*(Recuerde la tabla **“Mensajes de log de Kafka que puede ignorar”** al inicio de la Parte 5 si ve `Fetch … Cancelled` u otros ERROR en rojo.)*

### Paso 6.1. Leer del tópico y deduplicar

```python
news_rows: list[dict] = []
seen_urls: set[str] = set()  # urls ya vistas, para no repetir

if KAFKA_ENABLED:
    # Consumidor: lee desde el inicio del tópico y se detiene tras 10 s sin mensajes.
    # group_id fijo + enable_auto_commit=False evita el aviso "group_id is None".
    consumer = KafkaConsumer(
        TOPIC_NEWS,
        bootstrap_servers=KAFKA_BOOTSTRAP,
        auto_offset_reset="earliest",   # empezar desde el primer mensaje
        consumer_timeout_ms=10000,      # cortar si no llega nada en 10 s
        api_version=(3, 7, 1),          # misma versión fija que el productor
        group_id=f"l5-news-{uuid.uuid4().hex[:8]}",  # grupo nuevo → lee desde earliest
        enable_auto_commit=False,       # leemos una vez; no necesitamos commit de offset
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    )
    try:
        for msg in consumer:
            ev = msg.value
            url = ev.get("url", "")
            if url and url not in seen_urls:  # deduplicar por url
                seen_urls.add(url)
                news_rows.append(ev)
    finally:
        consumer.close()  # cierre ordenado (reduce avisos "Fetch ... Cancelled")
else:
    # Sin broker: usamos los eventos en memoria de la Parte 5
    for ev in rss_events:
        url = ev.get("url", "")
        if url and url not in seen_urls:
            seen_urls.add(url)
            news_rows.append(ev)

print("Eventos únicos tras deduplicar:", len(news_rows))
```

### Paso 6.2. Guardar los documentos en MongoDB (mongomock)

Creamos una colección y **insertamos los eventos como documentos**. Luego podemos **consultarla** con la misma API de MongoDB (`find`, `count_documents`).

```python
# Servidor real: mongo = MongoClient("mongodb://host:27017/")  # pymongo — misma API de bases/colecciones
mongo = mongomock.MongoClient()
news_col = mongo["udenar"]["news_raw"]  # base "udenar", colección "news_raw"

if news_rows:
    news_col.insert_many([dict(ev) for ev in news_rows])
    append_audit({"stage": "stream_staging_mongo", "collection": "news_raw", "docs": news_col.count_documents({})})

print("Documentos en MongoDB:", news_col.count_documents({}))
# Ejemplo de consulta: contar por fuente (feed)
for doc in news_col.find({}, {"_id": 0, "title": 1, "feed": 1}).limit(5):
    print(doc)
```

### Paso 6.3. Exportar los documentos para la Lección 6

MongoDB es ideal para **aterrizar** documentos del stream, pero el cuaderno de la Lección 6 corre en **otra sesión**. Exportamos la colección a `staging/news_labor.jsonl` (un JSON por línea): el mismo formato que la bitácora y los mensajes de Kafka. MongoDB almacena documentos (i.e., diccionarios) en collecciones (i.e., listas), los cuales se transforman facilmente a el formato semiestructurado de los archivos `JSON`.

```python
news_path = STAGING_DIR / "news_labor.jsonl"
docs = list(news_col.find({}, {"_id": 0}))

if docs:
    with news_path.open("w", encoding="utf-8") as f:
        for doc in docs:
            f.write(json.dumps(doc, ensure_ascii=False) + "\n")
    append_audit({"stage": "stream_export", "path": str(news_path), "docs": len(docs)})
    print("Exportado a:", news_path, "| documentos:", len(docs))
else:
    print("Sin noticias en esta corrida — no se exporta (la capa es opcional en L6).")
```

**Comprobar:**

```python
# La colección debe existir; si hubo documentos, el export también
assert news_col.count_documents({}) == len(news_rows)
if news_rows:
    assert news_path.is_file()
print("Parte 6, consumidor y MongoDB: OK")
```

---

## Parte 7. Velocidad a escala: reproducir muchos eventos

Las arquitecturas de streaming se destacan cuando los datos llegan **rápido y en gran cantidad**. Para *experimentar* esa **velocidad** sin depender del ritmo real de las noticias, **reproducimos** muchos eventos sintéticos medimos cuánto tarda.

Estos datos son **sintéticos** para **experimentar la V de velocidad**. Cerramos el ciclo **productor → consumidor → MongoDB** como en las Partes 5 y 6. Si durante la publicación o lectura aparecen ERROR de Kafka en el log, consulte la tabla de la **Parte 5**; lo importante es que los **200 eventos** creados en 7.1 coincidan con los consumidos en 7.3.

### Paso 7.1. Preparar el archivo de reproducción

Si no existe, creamos un archivo con muchos eventos de ejemplo:

```python
REPLAY_PATH = STAGING_DIR / "news_events_replay.jsonl"

if not REPLAY_PATH.is_file():
    sample = [
        {
            "id": str(uuid.uuid4()),
            "url": f"https://example.local/item/{i}",
            "title": f"Titular sintético de empleo #{i}",
            "feed": "replay",
            "geih": False,  # datos inventados, NO oficiales
        }
        for i in range(200)
    ]
    with REPLAY_PATH.open("w", encoding="utf-8") as f:
        for ev in sample:
            f.write(json.dumps(ev, ensure_ascii=False) + "\n")
    print("Archivo de reproducción creado con 200 eventos.")

# Cargamos todos los eventos a reproducir
replay_events = [json.loads(ln) for ln in REPLAY_PATH.read_text(encoding="utf-8").splitlines()]
print("Eventos a reproducir:", len(replay_events))
print("Muestra creada (primeros 5 — compare con lo consumido en 7.3):")
for ev in replay_events[:5]:
    print(" -", ev.get("title", "(sin título)"))
```

### Paso 7.2. Publicar la reproducción (productor)

Solo el **productor** envía los eventos al tópico lo más rápido posible. Medimos cuánto tarda el envío.

```python
t0 = time.perf_counter()

if KAFKA_ENABLED:
    publicar_eventos(producer, TOPIC_REPLAY, replay_events)  # tópico aparte: no compite con RSS
else:
    time.sleep(0.05 * len(replay_events) / 50)

produce_elapsed = time.perf_counter() - t0
produce_rate = len(replay_events) / produce_elapsed if produce_elapsed > 0 else 0
print(f"Publicados {len(replay_events)} eventos en {produce_elapsed:.2f} s (~{produce_rate:,.0f} eventos/s)")
```

### Paso 7.3. Consumir la reproducción y ver los titulares

Sin **consumidor**, los mensajes quedan en el tópico pero **no los vemos**. Publicamos la reproducción en un **tópico propio** (`TOPIC_REPLAY`) para no mezclarla con el RSS de las Partes 5–6 ni con *offsets* de ejecuciones anteriores. Cada corrida usa un **grupo de consumidor nuevo** (`uuid`) para leer desde el inicio.

```python
replay_rows: list[dict] = []

if KAFKA_ENABLED:
    # Grupo nuevo en cada corrida → siempre lee el tópico replay desde el principio
    replay_consumer = KafkaConsumer(
        TOPIC_REPLAY,
        bootstrap_servers=KAFKA_BOOTSTRAP,
        auto_offset_reset="earliest",
        consumer_timeout_ms=12000,
        api_version=(3, 7, 1),          # misma versión fija que el productor
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        group_id=f"l5-replay-{uuid.uuid4().hex[:8]}",
        enable_auto_commit=False,
    )
    try:
        for msg in replay_consumer:
            ev = msg.value
            url = ev.get("url", "")
            if url and url not in seen_urls:
                seen_urls.add(url)
                replay_rows.append(ev)
    finally:
        replay_consumer.close()

# Si Kafka no devolvió nada (re-ejecución rara), usamos el lote que acabamos de publicar
if KAFKA_ENABLED and not replay_rows:
    print("Aviso: el consumidor no leyó mensajes — mostramos el lote publicado en 7.2.")
    replay_rows = list(replay_events)
elif not KAFKA_ENABLED:
    replay_rows = list(replay_events)

if replay_rows:
    news_col.insert_many([dict(ev) for ev in replay_rows])
    with news_path.open("a", encoding="utf-8") as f:
        for doc in replay_rows:
            f.write(json.dumps(doc, ensure_ascii=False) + "\n")

append_audit(
    {
        "stage": "replay_throughput",
        "topic": TOPIC_REPLAY,
        "produced": len(replay_events),
        "consumed": len(replay_rows),
        "produce_seconds": round(produce_elapsed, 3),
        "geih": False,
    }
)

print("Eventos de reproducción consumidos:", len(replay_rows))
print("Documentos totales en MongoDB:", news_col.count_documents({}))
print("\nMuestra consumida (primeros 5 — deben coincidir con 7.1):")
for ev in replay_rows[:5]:
    print(" -", ev.get("title", "(sin título)"))
if not replay_rows:
    print(" (ninguno — muestre titulares RSS ya en Mongo:)")
    for doc in news_col.find({}, {"_id": 0, "title": 1}).limit(5):
        print(" -", doc.get("title", "(sin título)"))
print("Capa NO oficial: esto mide velocidad, no empleo.")
```

**Comprobar:**

```python
assert len(replay_events) >= 1
assert len(replay_rows) >= 1, "Deberíamos ver al menos un titular de reproducción"
print("Parte 7, reproducción productor + consumidor: OK")
```

---

## Tareas

Esta lección es **individual y conceptual**: aquí *ven* el camino completo de la ingesta (batch gobernado + stream con Kafka y MongoDB). El **entregable grupal** de la semana, en **`week-3-group`**, se concentra en la parte batch sobre GEIH: construir la capa **curated para todos los años (2022–2025)** con bitácora, contrato y un **flujo Prefect**, y luego (Lección 6) **modelar y visualizar** sobre esos agregados.

Lo que practicaron aquí y reutilizan en el grupo:

1. Capa **curated** + **bitácora** + **contrato de esquema** para **un mes** (Parte 3). El lakehouse de entrada viene de **`week-2-group`** o de la **Parte 0** (solución compacta Ej. 1).
2. Un **flujo Prefect** que orquesta el ETL de **un año completo** (Parte 4).

**Tarea grupal (`week-3-group`, Ejercicio 1):** extiendan el flujo de la Parte 4 para cubrir **todos los años** del lakehouse (2022–2025) en **un solo** `curated/geih_dept_month.parquet`.

La mitad de streaming (Partes 5–7) es para **entender** la *velocidad* y la *variedad* que GEIH no ejercita; **no** va en el ZIP grupal.

**Entrega grupal:** martes **23 jun 2026** — ZIP con `week-3-group-<group_id>.ipynb` + `manifest.json`.

<!-- end NOTEBOOK: -->
