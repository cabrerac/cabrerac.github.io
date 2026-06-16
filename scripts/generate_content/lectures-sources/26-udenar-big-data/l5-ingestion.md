---
course_code: 26-udenar-big-data
title: Data ingestion and workflow
description: Lecture 5 — batch to stream ingestion journey on the GEIH lakehouse plus Kafka news feeds. Audit logging and schema contracts hook back to L2 ethics framing.
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
visible: false
group_notebook: week-3-group
notebook_language: es
notebook_title: Ingesta y flujos de trabajo
notebook_description: Práctica individual de la Lección 5 (run-only). Pasamos de la ingesta batch sobre el lakehouse GEIH de la semana 2 a una fuente en streaming (noticias) con Kafka. Registramos auditoría y contrato de esquema. El código evaluable está en week-3-group Parte A.
---

<!-- SLIDES: -->

# Last Time

<!-- end SLIDES: -->

{% include _snippets/26-udenar-big-data/l5-ingestion/last-time.md %}

<!-- SLIDES: -->

# Vs tour

<!-- end SLIDES: -->

{% include _snippets/26-udenar-big-data/l5-ingestion/vs-tour.md %}

<!-- SLIDES: -->

# Batch vs stream

<!-- end SLIDES: -->

{% include _snippets/26-udenar-big-data/l5-ingestion/batch-stream.md %}

<!-- SLIDES: -->

# Kafka

<!-- end SLIDES: -->

{% include _snippets/26-udenar-big-data/l5-ingestion/kafka-ingest.md %}

<!-- SLIDES: -->

# Conclusions

<!-- end SLIDES: -->

{% include _snippets/26-udenar-big-data/l5-ingestion/conclusions.md %}

{% include _snippets/26-udenar-big-data/l5-ingestion/practical-slides.md %}

<!-- RENDER: -->

### Week 3 links

- [Week 3 hub](/teaching/26-udenar-big-data/week-3-hub-es/) *(when published)*

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

Antes del laboratorio repasamos cuatro ideas que usaremos en las Partes 1 a 7. Si vienen de las lecciones 3 y 4 ya conocen Parquet y agregados; aquí lo nuevo es **registrar lo que hacemos** y **leer datos que llegan poco a poco**.

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

Abrimos el archivo en modo **`"a"`** (de *append*, añadir) para no sobrescribir lo ya escrito:

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
assert len(lineas) == 2  # dos llamadas = dos líneas
print("Bitácora JSONL: OK")
```

Cada línea es independiente: por eso podemos leer el archivo más tarde y reconstruir **todo lo que pasó**, en orden.

### Un *tópico* de Kafka es una lista de mensajes (modelo mental)

En la segunda mitad del cuaderno usamos **Kafka**. Antes de conectarnos a un servidor real, entendamos la idea con Python puro. Un **tópico** es como una **lista a la que solo se agrega al final**:

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

---

## Instrucciones

**De dónde venimos.** En las lecciones 3 y 4 **guardamos** GEIH en un lakehouse (Parquet particionado) y lo **consultamos** con varios motores. Ya tenemos datos confiables, pero **estáticos**: una foto mensual de una encuesta oficial.

**Qué añade esta lección.** La **ingesta** es la capa que *trae* datos al lakehouse y los deja listos para analizar. Veremos dos modos:

- **Batch** (por lotes): procesamos un conjunto **acotado** que ya existe — las particiones GEIH. Lo hacemos de forma **gobernada**: dejamos bitácora y contrato de esquema.
- **Streaming** (flujo): leemos datos que **llegan poco a poco y no terminan** — titulares de noticias — usando **Kafka**.

**Por qué cambiamos de fuente.** GEIH es fuerte en **volumen** y **veracidad** (es oficial), pero **lenta** (mensual) y **estructurada**. Para ver las otras *V* del big data —**velocidad** y **variedad**— necesitamos una fuente distinta. Las noticias llegan a toda hora (velocidad) y son texto libre (variedad), pero **no son estadística oficial** (veracidad baja). Por eso al final del cuaderno trabajamos **sin GEIH**: no para reemplazarla, sino para **sentir** una *V* que la encuesta no ejercita.

**Prerrequisito.** Haber ejecutado **`week-2-group`** y tener `data/processed/geih-spine/` con particiones 2022–2025 en Google Drive. Este cuaderno **no** vuelve a harmonizar CSV.

**Producción vs este laboratorio.** En la industria la ingesta usa herramientas pesadas; aquí usamos versiones ligeras que enseñan la misma idea.

| Capa | En producción | En este curso |
|------|---------------|---------------|
| Orquestación | Airflow / Dagster | **Prefect** (local) |
| Streaming | Cluster de Kafka + Flink | **Un** servidor Kafka compartido |
| Fuente batch | Lakehouse gobernado | Parquet de **`week-2-group`** |
| Fuente stream | Mercados / logs en vivo | **Noticias (RSS)** + reproducción |

**Este cuaderno es individual y solo para ejecutar** (run-only). El código que se evalúa está en **`week-3-group` Parte A**.

**Qué hace el cuaderno (en orden).**

| Parte | Tema |
|-------|------|
| **1** | Montar Drive, rutas e instalar librerías |
| **2** | Puente: leer el lakehouse de la semana 2 |
| **3** | Ingesta **batch gobernada**: capa `curated/` + bitácora + contrato |
| **4** | Orquestar el batch con **Prefect** |
| **5** | Del batch al stream: **productor Kafka** sobre noticias |
| **6** | **Consumidor Kafka**: deduplicar y dejar en `staging/` |
| **7** | **Velocidad a escala**: reproducir muchos eventos (sin GEIH) |

**Entrega de la semana:** el código evaluable va en **`week-3-group`**. Ver **Tareas** al final.

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

# Creamos las carpetas de salida si no existen
for d in (CURATED_DIR, STAGING_DIR):
    d.mkdir(parents=True, exist_ok=True)

print("Lakehouse de entrada:", PROCESSED_DIR)
print("Salidas en:", CURATED_DIR, "y", STAGING_DIR)
```

Instalamos las librerías que **no** vienen en Colab. Cada una cubre una parte del pipeline:

- **Prefect:** orquesta el batch (encadena pasos en un *flujo*).
- **kafka-python:** cliente para **publicar** y **leer** mensajes de Kafka.
- **feedparser:** descarga y lee **feeds RSS** de noticias.
- **Polars / PyArrow:** leen Parquet y agregan, como en las lecciones 3 y 4.

```python
%pip install -q polars pyarrow prefect kafka-python feedparser requests
```

Importamos todo. Si Kafka no está instalado (o no hay servidor), dejamos las clases en `None` y más adelante el cuaderno cae a un modo **sin servidor** para que igual puedan completarlo.

```python
import json
import os
import time
import uuid
from datetime import datetime, timezone

import feedparser
import polars as pl
import requests

try:
    from kafka import KafkaConsumer, KafkaProducer
except ImportError:
    KafkaProducer = KafkaConsumer = None  # modo sin servidor (fallback)

print("Dependencias: OK")
```

**Comprobar:**

```python
assert WORK_ROOT.is_dir()
assert PROCESSED_DIR.is_dir(), (
    f"No encuentro {PROCESSED_DIR}. Ejecute week-2-group (lakehouse 2022–2025) primero."
)
print("Parte 1, configuración: OK")
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
assert len(partitions) >= 1, "No hay particiones. Monte Drive y complete week-2-group."
print("Parte 2, puente con el lakehouse: OK")
```

---

## Parte 3. Ingesta batch gobernada: capa curated, bitácora y contrato

**Idea.** La ingesta batch toma datos confiables y deja una **capa lista para analizar** (`curated/`), dejando rastro de **qué** hicimos (bitácora) y **prometiendo** qué columnas publicamos (contrato). Esto es *gobernanza*: no basta con que el cálculo sea correcto, debe ser **trazable**.

Para enseñar el patrón usamos **una** partición de ejemplo (no recorremos todo el árbol; eso es trabajo de `week-2-group`).

### Paso 3.1. La función de bitácora

Reutilizamos la idea del Repaso, ahora apuntando a `AUDIT_PATH`. Cada paso del pipeline llamará a `append_audit` para dejar una línea.

```python
ACTIVIDAD_OCUPADO = 1  # en GEIH, actividad == 1 significa "ocupado" (igual que en L4)


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

Calculamos un agregado por **departamento y mes**: cuántos ocupados hay (`conteo`) y la suma de sus factores de expansión (`ponderado`, la estimación poblacional, como en L4). Usamos **Polars perezoso** (`scan_parquet`): arma el plan y solo lee al hacer `collect()`.

```python
sample_part = partitions[0]  # una partición = un mes de ejemplo

# scan_parquet NO lee aún: define un plan de consulta perezoso
lf = pl.scan_parquet(str(sample_part))

agg = (
    lf
    .filter(pl.col("actividad") == ACTIVIDAD_OCUPADO)  # quedarnos con ocupados
    .group_by(["dpto", "anio", "mes"])                 # una fila por dpto/mes
    .agg(
        pl.len().alias("conteo"),                      # número de ocupados
        pl.col("factor_expansion").sum().alias("ponderado"),  # estimación poblacional
    )
    .collect()                                          # AQUÍ se ejecuta y se lee el Parquet
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

Un **contrato de esquema** es una promesa: "esta tabla tiene estas columnas, con estos tipos, viene de esta fuente y se usa así". Sirve para que quien consuma los datos sepa qué esperar, y para detectar si algo cambió sin avisar.

```python
schema_contract = {
    "name": "geih_dept_month_curated",
    "source": "geih-spine",
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

## Parte 4. Orquestar el batch con Prefect

**Idea.** Un pipeline real tiene **varios pasos** que deben correr en orden y, si algo falla, queremos saber **dónde**. Un **orquestador** como **Prefect** nos deja declarar pasos (`@task`) y encadenarlos en un **flujo** (`@flow`). Prefect registra cada ejecución, reintenta si pedimos, y muestra qué paso falló.

Aquí envolvemos lo de la Parte 3 en un flujo mínimo: un paso entrega la ruta del curated y otro lo **valida**.

```python
from prefect import flow, task


@task
def task_curated_snapshot() -> str:
    """Paso 1: devuelve la ruta del curated que escribimos en la Parte 3."""
    return str(curated_path)


@task
def task_validate(path_str: str) -> int:
    """Paso 2: valida que el curated tenga filas y devuelve cuántas."""
    df = pl.read_parquet(path_str)
    assert df.height > 0, "El curated no debería estar vacío"
    return df.height


@flow(name="geih_batch_ingest")
def batch_flow() -> int:
    """Flujo: encadena los dos pasos y deja rastro en la bitácora."""
    ruta = task_curated_snapshot()   # Prefect ejecuta el paso 1
    n = task_validate(ruta)          # … y luego el paso 2 (depende del 1)
    append_audit({"stage": "prefect_flow", "rows": n})
    return n


rows = batch_flow()
print("El flujo Prefect validó filas:", rows)
```

En producción este mismo patrón corre **programado** (p. ej. cada noche) y puede traer también series macro (la TRM del Banco de la República vía SDMX). Lo omitimos aquí para no depender de la red, pero la idea es la misma: **un paso más en el flujo**.

**Comprobar:**

```python
assert rows > 0, "El flujo debería haber validado al menos una fila"
print("Parte 4, orquestación con Prefect: OK")
```

---

## Parte 5. Del batch al stream: productor de noticias con Kafka

**Idea.** Hasta aquí los datos ya existían. Ahora pasamos al **streaming**: una fuente que **llega poco a poco**. Tomamos **titulares de noticias** sobre empleo. El patrón Kafka tiene dos lados; en esta parte hacemos el **productor** (quien escribe al tópico).

Recuerden del Repaso: un **tópico** es una lista a la que solo se agrega. El productor empuja mensajes; el consumidor (Parte 6) los lee.

### Paso 5.1. Conectar al servidor (o trabajar sin él)

El servidor Kafka es **externo** (no vive dentro de Colab). Sus credenciales se ponen en **Secrets** de Colab (o variables de entorno locales): `KAFKA_BOOTSTRAP_SERVERS`, `KAFKA_SASL_USERNAME`, `KAFKA_SASL_PASSWORD`. Si no hay credenciales, seguimos en **modo sin servidor** guardando los eventos en un archivo local: así el cuaderno se completa igual.

```python
KAFKA_BOOTSTRAP = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "")
KAFKA_USER = os.environ.get("KAFKA_SASL_USERNAME", "")
KAFKA_PASS = os.environ.get("KAFKA_SASL_PASSWORD", "")

# Hay Kafka solo si tenemos servidor Y la librería se importó bien
KAFKA_ENABLED = bool(KAFKA_BOOTSTRAP and KafkaProducer)
print("¿Kafka disponible?", KAFKA_ENABLED)
```

### Paso 5.2. Leer noticias por RSS y filtrar por tema

**RSS** es un formato estándar que publican los medios para listar sus titulares. **`feedparser`** lo descarga y nos da una lista de entradas. Como solo nos interesan noticias de **empleo**, filtramos por palabras clave. Esto es *ingesta por sondeo* (*polling*): preguntamos cada cierto tiempo "¿hay algo nuevo?".

```python
RSS_FEEDS = [
    "https://www.portafolio.co/rss/economia.xml",
    "https://www.eltiempo.com/rss/economia.xml",
]
KEYWORDS = ("empleo", "desempleo", "mercado laboral", "trabajo", "geih")


def keyword_hit(text: str) -> bool:
    """True si el texto menciona alguna palabra clave de empleo."""
    t = (text or "").lower()
    return any(k in t for k in KEYWORDS)


def poll_rss_events(max_items: int = 20) -> list[dict]:
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

Con Kafka, **publicar** es enviar cada evento como JSON al tópico. Sin servidor, escribimos los eventos a un archivo `.jsonl` que la Parte 6 podrá leer. En ambos casos dejamos rastro en la bitácora.

```python
if KAFKA_ENABLED:
    # Productor real: serializa cada evento a JSON y lo envía al tópico
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP.split(","),
        security_protocol="SASL_SSL",
        sasl_mechanism="SCRAM-SHA-256",
        sasl_plain_username=KAFKA_USER,
        sasl_plain_password=KAFKA_PASS,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )
    rss_events = poll_rss_events()
    for ev in rss_events:
        producer.send(TOPIC_NEWS, ev)
    producer.flush()  # asegura que todo salió
    append_audit({"stage": "kafka_produce", "topic": TOPIC_NEWS, "count": len(rss_events)})
    print("Eventos publicados al tópico:", len(rss_events))
else:
    # Modo sin servidor: guardamos los eventos en un archivo local
    rss_events = poll_rss_events()
    fallback_path = STAGING_DIR / "rss_poll_fallback.jsonl"
    with fallback_path.open("w", encoding="utf-8") as f:
        for ev in rss_events:
            f.write(json.dumps(ev, ensure_ascii=False) + "\n")
    append_audit({"stage": "rss_poll_local", "path": str(fallback_path), "count": len(rss_events)})
    print("Sin servidor Kafka — eventos guardados en:", fallback_path)

print("Noticias de empleo capturadas:", len(rss_events))
```

**Comprobar:**

```python
# Puede ser 0 si hoy ningún titular menciona empleo — el patrón igual quedó claro
assert isinstance(rss_events, list)
print("Parte 5, productor de noticias: OK")
```

---

## Parte 6. Consumidor: leer el stream, deduplicar y dejar en staging

**Idea.** El otro lado de Kafka es el **consumidor**: lee del tópico y procesa. Dos cuidados típicos del streaming:

- **Deduplicar:** el mismo titular puede llegar varias veces; lo identificamos por su `url`.
- **Dejar en `staging/`:** una capa intermedia, lista para que la analítica (Lección 6) la use.

### Paso 6.1. Leer y deduplicar

```python
news_rows: list[dict] = []
seen_urls: set[str] = set()  # urls ya vistas, para no repetir

if KAFKA_ENABLED:
    # Consumidor real: lee desde el inicio del tópico y se detiene tras 8 s sin mensajes
    consumer = KafkaConsumer(
        TOPIC_NEWS,
        bootstrap_servers=KAFKA_BOOTSTRAP.split(","),
        security_protocol="SASL_SSL",
        sasl_mechanism="SCRAM-SHA-256",
        sasl_plain_username=KAFKA_USER,
        sasl_plain_password=KAFKA_PASS,
        auto_offset_reset="earliest",   # empezar desde el primer mensaje
        consumer_timeout_ms=8000,       # cortar si no llega nada en 8 s
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    )
    for msg in consumer:
        ev = msg.value
        url = ev.get("url", "")
        if url and url not in seen_urls:  # deduplicar por url
            seen_urls.add(url)
            news_rows.append(ev)
    consumer.close()
else:
    # Modo sin servidor: leemos el archivo que dejó la Parte 5
    fallback_path = STAGING_DIR / "rss_poll_fallback.jsonl"
    if fallback_path.is_file():
        for line in fallback_path.read_text(encoding="utf-8").splitlines():
            ev = json.loads(line)
            url = ev.get("url", "")
            if url and url not in seen_urls:
                seen_urls.add(url)
                news_rows.append(ev)

print("Eventos únicos tras deduplicar:", len(news_rows))
```

### Paso 6.2. Escribir la tabla de staging

Convertimos los eventos a un DataFrame de Polars y lo guardamos como Parquet en `staging/`. Esta es la entrada para la Lección 6 (un *monitor* de discurso mediático).

```python
if news_rows:
    news_df = pl.DataFrame(news_rows)
    news_path = STAGING_DIR / "news_labor.parquet"
    news_df.write_parquet(news_path)
    append_audit({"stage": "stream_staging", "path": str(news_path), "rows": news_df.height})
    print(news_df.select(["title", "feed"]).head())
    print("Staging escrito en:", news_path)
else:
    print("Sin noticias de empleo en esta corrida — la tabla de staging queda vacía.")
```

**Comprobar:**

```python
# Si hubo filas, el archivo de staging debe existir
if news_rows:
    assert (STAGING_DIR / "news_labor.parquet").is_file()
print("Parte 6, consumidor y staging: OK")
```

---

## Parte 7. Velocidad a escala: reproducir muchos eventos (sin GEIH)

**Idea.** El streaming brilla cuando los datos llegan **rápido y en gran cantidad**. Para *sentir* esa **velocidad** sin depender del ritmo real de las noticias, **reproducimos** (replay) muchos eventos sintéticos de golpe y medimos cuánto tarda.

Importante: estos datos son **inventados** y **no tienen nada que ver con GEIH**. Aquí no buscamos una cifra de empleo, sino **experimentar la V de velocidad** que la encuesta mensual no tiene.

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
```

### Paso 7.2. Reproducir y medir la velocidad

```python
t0 = time.perf_counter()

if KAFKA_ENABLED:
    # Enviar todos los eventos lo más rápido posible al tópico
    for ev in replay_events:
        producer.send(TOPIC_NEWS, ev)
    producer.flush()
else:
    # Sin servidor, simulamos el tiempo de envío para poder medir
    time.sleep(0.05 * len(replay_events) / 50)

elapsed = time.perf_counter() - t0

append_audit(
    {
        "stage": "replay_throughput",
        "events": len(replay_events),
        "seconds": round(elapsed, 3),
        "geih": False,
    }
)

tasa = len(replay_events) / elapsed if elapsed > 0 else 0
print(f"Reproducidos {len(replay_events)} eventos en {elapsed:.2f} s (~{tasa:,.0f} eventos/s)")
print("Capa NO oficial: esto mide velocidad, no empleo.")
```

**Comprobar:**

```python
assert len(replay_events) >= 1
print("Parte 7, reproducción de eventos: OK")
```

---

## Tareas

Lo que practicaron aquí lo **implementan ustedes** en el cuaderno grupal **`week-3-group` (Parte A)**, sobre **su** lakehouse 2022–2025:

1. Capa **curated** + **bitácora** + **contrato de esquema** (Partes 3).
2. Un **flujo Prefect** que encadene y valide (Parte 4).
3. **Productor y consumidor** de noticias (Partes 5–6), con deduplicado.
4. Un markdown que explique **qué *V* ejercita cada fuente** (GEIH vs noticias) y por qué la fuente debe encajar con la pregunta de decisión.

La reproducción de la Parte 7 es **opcional** (mejora, no obligatoria).

**Entrega grupal:** martes **23 jun 2026** — ZIP con `week-3-group-<group_id>.ipynb` + `manifest.json`.

<!-- end NOTEBOOK: -->
