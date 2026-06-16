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
notebook_description: Práctica individual de la Lección 5 (run-only). Recorrido batch → stream sobre el lakehouse GEIH del week-2-group, más productor/consumidor Kafka sobre noticias. El código evaluable está en week-3-group Parte A.
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

Repasamos lo que usaremos en las Partes 1 a 7. Asumimos que ya ejecutó **`week-2-group`** y tiene Parquet 2022–2025 en Drive.

### Registrar eventos en JSONL (`audit.jsonl`)

Un **log de auditoría** append-only: cada línea es un JSON con quién/qué/cuándo. Abrimos en modo **`"a"`** para no borrar entradas previas.

```python
import json
from datetime import datetime, timezone
from pathlib import Path

audit_path = Path("data/audit.jsonl")
audit_path.parent.mkdir(parents=True, exist_ok=True)

def append_audit_demo(event: dict) -> None:
    event = {**event, "ts_utc": datetime.now(timezone.utc).isoformat()}
    with audit_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")

append_audit_demo({"stage": "demo", "rows": 3})
lines = audit_path.read_text(encoding="utf-8").strip().splitlines()
print("Líneas en audit:", len(lines))
assert len(lines) >= 1
print("JSONL audit: OK")
```

### Listar particiones Parquet con `Path.glob`

El lakehouse de semana 2 usa carpetas `anio=2024/mes=01/part-000.parquet`. **`glob("anio=*/mes=*/part-*.parquet")`** encuentra todas las particiones bajo una raíz.

```python
demo_root = Path("data/processed/geih-spine")
if demo_root.is_dir():
    parts = sorted(demo_root.glob("anio=*/mes=*/part-*.parquet"))
    print("Particiones encontradas:", len(parts))
else:
    print("Demo: carpeta aún no creada — la creará week-2-group.")
print("Path.glob particiones: OK")
```

---

## Instrucciones

**Propósito.** En semanas 2–4 construimos y consultamos el **lakehouse GEIH**. En esta **Lección 5** añadimos la **capa de ingesta**: batch gobernado sobre Parquet existente y un **extremo stream** (noticias vía Kafka) para contrastar **Vs** (volumen, velocidad, variedad, veracidad).

**Prerrequisito.** Ejecute **`week-2-group`** hasta tener `data/processed/geih-spine/` con particiones 2022–2025 en Google Drive. Este cuaderno **no** re-harmoniza CSV.

**Producción vs laboratorio.**

| Capa | En producción | En este curso |
|------|---------------|---------------|
| Orquestación | Airflow / Dagster | **Prefect** local |
| Streaming | Cluster Kafka + Flink | **Un broker** compartido |
| Batch | Lakehouse gobernado | **`week-2-group`** Parquet |
| Stream | Firehose / logs | **RSS** + replay JSONL |

**Recorrido de Vs:** etapas batch (Partes 2–4) = **GEIH**; etapas stream (Partes 5–7) = **sin GEIH** (noticias). En markdown debe quedar claro qué capa responde a qué pregunta de decisión.

**Cuaderno individual:** solo **ejecutar** (run-only). Código evaluable: **`week-3-group` Parte A**.

**Qué hace el cuaderno (en orden).**

| Parte | Tema |
|-------|------|
| **1** | Montar Drive y rutas al lakehouse de semana 2 |
| **2** | Puente: `manifest.json` y listado de particiones |
| **3** | Ingesta batch → `curated/` + `audit.jsonl` + `schema_contract.json` |
| **4** | Orquestación batch con **Prefect** |
| **5** | **Kafka productor:** poll RSS acotado |
| **6** | **Kafka consumidor:** dedupe → `staging/news_labor.parquet` |
| **7** | **Replay** de alta tasa — demo velocidad/volumen **sin GEIH** |

**Entrega semana 3:** código evaluable en **`week-3-group`**. Ver **Tareas** al final.

---

## Parte 1. Configuración: Drive y rutas

Montamos la misma raíz que en las lecciones 3–4. Si trabaja **en local** con el mismo layout, ponga `USE_GOOGLE_DRIVE = False`.

```python
from pathlib import Path

USE_GOOGLE_DRIVE = True

try:
    import google.colab  # noqa: F401
    IN_COLAB = True
except ImportError:
    IN_COLAB = False

if USE_GOOGLE_DRIVE and IN_COLAB:
    from google.colab import drive

    drive.mount("/content/drive")
    WORK_ROOT = Path("/content/drive/MyDrive/udenar/cease/2026/big-data/")
    print(f"Raíz en Drive: {WORK_ROOT}")
else:
    WORK_ROOT = Path(".")
    print(f"Raíz local: {WORK_ROOT.resolve()}")

PROCESSED_DIR = WORK_ROOT / "data" / "processed" / "geih-spine"
CURATED_DIR = WORK_ROOT / "data" / "curated"
STAGING_DIR = WORK_ROOT / "data" / "staging"
AUDIT_PATH = WORK_ROOT / "data" / "audit.jsonl"
SCHEMA_PATH = WORK_ROOT / "data" / "schema_contract.json"
MANIFEST_PATH = WORK_ROOT / "manifest.json"
TOPIC_RAW = "udenar.news.raw"  # demo instructor; en grupo use su group_id

for d in (CURATED_DIR, STAGING_DIR):
    d.mkdir(parents=True, exist_ok=True)

print("Lakehouse:", PROCESSED_DIR)
```

Este cuaderno usa librerías que no vienen instaladas en Colab:

- **Prefect:** orquestación de flujos batch (etapas encadenadas con `@flow`).
- **kafka-python:** cliente Kafka para publicar y leer eventos JSON.
- **feedparser:** leer feeds RSS de noticias.
- **Polars / PyArrow:** leer Parquet y agregar (como en L3–L4).

```python
%pip install -q polars pyarrow prefect kafka-python feedparser requests
```

Importamos dependencias:

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
    KafkaProducer = KafkaConsumer = None

print("Dependencias: OK")
```

**Comprobar:**

```python
assert WORK_ROOT.is_dir()
assert PROCESSED_DIR.is_dir(), (
    f"No encuentro {PROCESSED_DIR}. Complete week-2-group primero."
)
print("Parte 1, configuración: OK")
```

---

## Parte 2. Puente desde week-2-group

Reutilizamos el **lakehouse harmonizado** (`anio=/mes=/`). **No** re-harmonizamos CSV.

```python
if MANIFEST_PATH.is_file():
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    print("manifest.json (claves):", list(manifest.keys())[:8])
else:
    manifest = {}
    print("manifest.json no encontrado — use el de su week-2-group")

partitions = sorted(PROCESSED_DIR.glob("anio=*/mes=*/part-*.parquet"))
print("Particiones Parquet:", len(partitions))
print("Ejemplo:", partitions[0].relative_to(WORK_ROOT) if partitions else "—")
```

**Comprobar:**

```python
assert len(partitions) >= 1, "Monte Drive y complete week-2-group primero."
print("Parte 2, puente week-2: OK")
```

---

## Parte 3. Ingesta batch: curated, audit y contrato de esquema

Agregado mensual por departamento desde **una partición de ejemplo** (mismo espíritu que L4, sin recorrer todo el árbol).

Definimos `append_audit` y la regla de ocupado:

```python
ACTIVIDAD_OCUPADO = 1

def append_audit(event: dict) -> None:
    event = {**event, "ts_utc": datetime.now(timezone.utc).isoformat()}
    with AUDIT_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")
```

Construimos el agregado y lo escribimos en `curated/`:

```python
sample_part = partitions[0]
lf = pl.scan_parquet(str(sample_part))
agg = (
    lf.filter(pl.col("actividad") == ACTIVIDAD_OCUPADO)
    .group_by(["dpto", "anio", "mes"])
    .agg(
        pl.len().alias("conteo"),
        pl.col("factor_expansion").sum().alias("ponderado"),
    )
    .collect()
)
curated_path = CURATED_DIR / "geih_dept_month_sample.parquet"
agg.write_parquet(curated_path)
append_audit(
    {
        "stage": "batch_curated",
        "source": "geih-spine",
        "path": str(curated_path),
        "rows": agg.height,
    }
)
print(agg.head())
print("Curated:", curated_path)
```

Escribimos **`schema_contract.json`** (columnas, dtypes, fuente, retención):

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
    "retention_note": "Agregados para analítica — no publicar microdatos.",
}
SCHEMA_PATH.write_text(json.dumps(schema_contract, indent=2), encoding="utf-8")
append_audit({"stage": "schema_contract", "path": str(SCHEMA_PATH)})
print("schema_contract.json escrito")
```

**Comprobar:**

```python
assert curated_path.is_file()
assert SCHEMA_PATH.is_file()
assert agg.height > 0
print("Parte 3, ingesta batch: OK")
```

---

## Parte 4. Orquestación batch (Prefect)

Envolvemos la validación del curated en un flujo Prefect (stage 2 del recorrido).

```python
from prefect import flow, task

@task
def task_curated_snapshot() -> str:
    return str(curated_path)

@task
def task_validate(path_str: str) -> int:
    df = pl.read_parquet(path_str)
    assert df.height > 0
    return df.height

@flow(name="geih_batch_ingest_demo")
def batch_flow() -> int:
    p = task_curated_snapshot()
    n = task_validate(p)
    append_audit({"stage": "prefect_flow", "rows": n})
    return n

rows = batch_flow()
print("Prefect flow filas:", rows)
```

*(Opcional macro Banrep TRM: `requests` a SDMX — ver planificación L5 etapa 2; omitido aquí si no hay red.)*

**Comprobar:**

```python
assert rows > 0
print("Parte 4, Prefect: OK")
```

---

## Parte 5. Kafka: productor RSS

Configure en Colab **Secrets** (o `.env` local): `KAFKA_BOOTSTRAP_SERVERS`, `KAFKA_SASL_USERNAME`, `KAFKA_SASL_PASSWORD` (p. ej. Upstash).

```python
KAFKA_BOOTSTRAP = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "")
KAFKA_USER = os.environ.get("KAFKA_SASL_USERNAME", "")
KAFKA_PASS = os.environ.get("KAFKA_SASL_PASSWORD", "")
KAFKA_ENABLED = bool(KAFKA_BOOTSTRAP and KafkaProducer)

RSS_FEEDS = [
    "https://www.portafolio.co/rss/economia.xml",
    "https://www.eltiempo.com/rss/economia.xml",
]
KEYWORDS = ("empleo", "desempleo", "mercado laboral", "trabajo", "geih")

def keyword_hit(text: str) -> bool:
    t = (text or "").lower()
    return any(k in t for k in KEYWORDS)

def poll_rss_events(max_items: int = 20) -> list[dict]:
    events = []
    for url in RSS_FEEDS:
        feed = feedparser.parse(url)
        for entry in feed.entries[: max_items // len(RSS_FEEDS)]:
            title = entry.get("title", "")
            summary = entry.get("summary", "")
            if keyword_hit(title + " " + summary):
                events.append(
                    {
                        "id": str(uuid.uuid4()),
                        "url": entry.get("link", ""),
                        "title": title,
                        "published": entry.get("published", ""),
                        "feed": url,
                        "layer": "news_discourse",
                        "geih": False,
                    }
                )
    return events

print("Kafka habilitado:", KAFKA_ENABLED)
```

Publicamos eventos al tópico (o guardamos fallback JSONL si no hay broker):

```python
if KAFKA_ENABLED:
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
        producer.send(TOPIC_RAW, ev)
    producer.flush()
    append_audit({"stage": "kafka_produce", "topic": TOPIC_RAW, "count": len(rss_events)})
    print("Eventos publicados:", len(rss_events))
else:
    rss_events = poll_rss_events()
    replay_path = STAGING_DIR / "rss_poll_fallback.jsonl"
    with replay_path.open("w", encoding="utf-8") as f:
        for ev in rss_events:
            f.write(json.dumps(ev, ensure_ascii=False) + "\n")
    print("Sin Kafka — fallback:", replay_path, "| eventos:", len(rss_events))
```

**Comprobar:**

```python
assert len(rss_events) >= 0  # puede ser 0 si RSS no devuelve keywords hoy
print("Parte 5, productor: OK")
```

---

## Parte 6. Kafka: consumidor y staging stream

Leemos el tópico, deduplicamos por URL y escribimos **`staging/news_labor.parquet`**.

```python
news_rows = []

if KAFKA_ENABLED:
    consumer = KafkaConsumer(
        TOPIC_RAW,
        bootstrap_servers=KAFKA_BOOTSTRAP.split(","),
        security_protocol="SASL_SSL",
        sasl_mechanism="SCRAM-SHA-256",
        sasl_plain_username=KAFKA_USER,
        sasl_plain_password=KAFKA_PASS,
        auto_offset_reset="earliest",
        consumer_timeout_ms=8000,
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    )
    seen: set[str] = set()
    for msg in consumer:
        ev = msg.value
        url = ev.get("url", "")
        if url and url not in seen:
            seen.add(url)
            news_rows.append(ev)
    consumer.close()
else:
    fallback = STAGING_DIR / "rss_poll_fallback.jsonl"
    if fallback.is_file():
        for line in fallback.read_text(encoding="utf-8").splitlines():
            news_rows.append(json.loads(line))

if news_rows:
    news_df = pl.DataFrame(news_rows)
    news_path = STAGING_DIR / "news_labor.parquet"
    news_df.write_parquet(news_path)
    append_audit({"stage": "stream_staging", "path": str(news_path), "rows": news_df.height})
    print(news_df.select(["title", "feed"]).head())
else:
    print("Sin filas de noticias en esta corrida.")
```

**Comprobar:**

```python
if news_rows:
    assert (STAGING_DIR / "news_labor.parquet").is_file()
print("Parte 6, consumidor: OK")
```

---

## Parte 7. Fin del viaje: replay de alta tasa (sin GEIH)

Demostración de **velocidad/volumen de eventos** — replay de noticias, **no** microdatos GEIH.

```python
REPLAY_PATH = STAGING_DIR / "news_events_replay.jsonl"
if not REPLAY_PATH.is_file():
    sample = [
        {
            "id": str(uuid.uuid4()),
            "url": f"https://example.local/item/{i}",
            "title": f"Empleo region {i % 5} headline",
            "feed": "replay",
            "layer": "replay_demo",
            "geih": False,
        }
        for i in range(200)
    ]
    with REPLAY_PATH.open("w", encoding="utf-8") as f:
        for ev in sample:
            f.write(json.dumps(ev, ensure_ascii=False) + "\n")
    print("Replay sample creado:", REPLAY_PATH)

replay_events = [json.loads(ln) for ln in REPLAY_PATH.read_text(encoding="utf-8").splitlines()]
t0 = time.perf_counter()
if KAFKA_ENABLED:
    for ev in replay_events:
        producer.send(TOPIC_RAW, ev)
    producer.flush()
else:
    time.sleep(0.05 * len(replay_events) / 50)
elapsed = time.perf_counter() - t0
append_audit(
    {
        "stage": "replay_throughput_demo",
        "events": len(replay_events),
        "seconds": round(elapsed, 3),
        "geih": False,
    }
)
print(f"Replay: {len(replay_events)} eventos en {elapsed:.2f}s — capa NO oficial")
```

**Comprobar:**

```python
assert len(replay_events) >= 1
print("Parte 7, replay: OK")
```

---

## Tareas

En el cuaderno grupal **`week-3-group`** implemente las etapas 1–4 sobre su lakehouse, documente el **recorrido de Vs** (A7) y actualice `manifest.json`. Etapa 5 (replay) = opcional.

**Entrega grupal:** martes **23 jun 2026** — ZIP con `week-3-group-<group_id>.ipynb` + `manifest.json`.

<!-- end NOTEBOOK: -->
