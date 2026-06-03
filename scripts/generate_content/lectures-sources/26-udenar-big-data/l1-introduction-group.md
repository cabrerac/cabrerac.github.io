---
course_code: 26-udenar-big-data
title: L1 — Acceso grupal GEIH 2022–2025
description: Group Colab — GEIH spine 2022–2025 download, manifest, contribution log (notebook only; linked from l1-introduction lecture page).
session: 1
start_time: async
end_time: async
hours: 2
author: Christian Cabrera Jojoa
email: chc79@cam.ac.uk
position: Assistant Research Professor
department: Department of Computer Science and Technology
institution: University of Cambridge
layout: lecture
lecture_code: l1-introduction-group
lecture_date: 06/06/2026
visible: false
skip_slides: true
skip_lecture_page: true
notebook_language: es
notebook_title: Acceso grupal GEIH 2022–2025
notebook_description: Cuaderno canónico del grupo para la Lección 1 — descarga del spine GEIH 2022–2025, manifiesto y registro de contribución. Entrega en la sección **Tarea grupal**; plantillas Word en la página pública de la lección.
---

<!-- NOTEBOOK: -->

## Instrucciones

**Propósito.** Este cuaderno es el **Colab canónico del grupo** para la Lección 1. Descargan el **spine GEIH 2022–2025** con el mismo patrón que practicaron en el cuaderno individual (`l1-introduction`): extraer archivos desde get-microdata → descargar → extraer CSV → `manifest.json`.

**No es el cuaderno de práctica individual** — cada estudiante completa `l1-introduction` por su cuenta; aquí consolidan el trabajo del grupo.

**Plantillas Word:** descargue desde la [página de la Lección 1](https://cabrerac.github.io/teaching/26-udenar-big-data/l1-introduction/) (sección *Materials*). **Plazos y ZIP:** en **Tarea grupal** más abajo.

**Entrega Moodle (miércoles):** ZIP `l1-introduction-<nombre-grupo>.zip` con este `.ipynb`, `manifest.json` y `project_requirements.pdf`.

---

## Configuración

Reutilice las funciones del cuaderno individual (`download_zip`, `extract_csvs`) o cópielas aquí. Defina los **catalog_id** por año (los entrega el instructor).

```python
import json
import re
import time
import zipfile
from pathlib import Path

import requests

# catalog_id por año de encuesta (instructor)
CATALOG_BY_YEAR = {2022: 771, 2023: 782, 2024: 819, 2025: 853}
SPINE_YEARS = [2022, 2023, 2024, 2025]

RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)

DOWNLOAD_ONCLICK_RE = re.compile(
    r"mostrarModal\(\s*'([^']+)'\s*,\s*'"
    r"(https://microdatos\.dane\.gov\.co/index\.php/catalog/\d+/download/\d+)\s*'\s*\)",
    re.IGNORECASE,
)
FILE_ID_RE = re.compile(r"/download/(\d+)")


def download_zip(url: str, dest: Path, timeout: int = 600) -> tuple[float, int]:
    t0 = time.perf_counter()
    with requests.get(url.strip(), stream=True, timeout=timeout) as resp:
        resp.raise_for_status()
        with dest.open("wb") as fh:
            for chunk in resp.iter_content(chunk_size=1 << 20):
                if chunk:
                    fh.write(chunk)
    elapsed = round(time.perf_counter() - t0, 3)
    if dest.read_bytes()[:2] != b"PK":
        raise ValueError(f"No es ZIP: {dest}")
    return elapsed, dest.stat().st_size


def extract_csvs(zip_path: Path, dest_dir: Path) -> list[Path]:
    dest_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "r") as zf:
        csv_members = [n for n in zf.namelist() if n.lower().endswith(".csv")]
        for name in csv_members:
            target = dest_dir / Path(name).name
            with zf.open(name) as src, target.open("wb") as dst:
                dst.write(src.read())
    return sorted(dest_dir.glob("*.CSV")) + sorted(dest_dir.glob("*.csv"))


def list_catalog_downloads(catalog_id: int) -> list[dict]:
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
    return sorted(files, key=lambda r: r["filename"].lower())


def access_file(item: dict, year_dir: Path, survey_year: int, catalog_id: int, *, skip_if_exists: bool = True) -> dict:
    url, file_id, filename = item["url"], item["file_id"], item["filename"]
    zip_path = year_dir / filename
    out_dir = year_dir / Path(filename).stem
    if skip_if_exists and out_dir.is_dir() and any(out_dir.glob("*.CSV")):
        return {
            "method": "http",
            "survey_year": survey_year,
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
    n_csv = len(extract_csvs(zip_path, out_dir))
    return {
        "method": "http",
        "survey_year": survey_year,
        "catalog_id": catalog_id,
        "file_id": file_id,
        "filename": filename,
        "extract_dir": str(out_dir),
        "seconds": seconds,
        "bytes_downloaded": nbytes,
        "notes": f"extracted {n_csv} CSVs",
        "fallback_used": False,
    }


print("Años del spine:", SPINE_YEARS)
print("Catalog ids:", CATALOG_BY_YEAR)
```

---

## Descargar 2022–2025

Una petición get-microdata por año; bucle sobre todos los archivos mensuales. Puede tardar **varias horas** y **varios GB** — planifique red y disco.

```python
manifest_entries: list[dict] = []

for year in SPINE_YEARS:
    catalog_id = CATALOG_BY_YEAR[year]
    year_dir = RAW_DIR / str(year)
    year_dir.mkdir(parents=True, exist_ok=True)
    files = list_catalog_downloads(catalog_id)
    print(f"\n=== {year} (catalog {catalog_id}): {len(files)} archivos ===")
    for row in files:
        print("  ", row["file_id"], row["filename"])
        manifest_entries.append(access_file(row, year_dir, year, catalog_id))

manifest_path = Path("manifest.json")
manifest_path.write_text(json.dumps(manifest_entries, indent=2), encoding="utf-8")
total_gb = sum(e["bytes_downloaded"] for e in manifest_entries) / 1e9
print(f"\nManifest: {len(manifest_entries)} filas | ~{total_gb:.2f} GB descargados")
```

**Comprobar:**

```python
assert manifest_path.is_file()
assert len(manifest_entries) >= 40, "Se esperan ~48 archivos (12×4 años); revise si faltan meses"
print("Spine 2022–2025: OK")
```

---

## Registro de contribución (grupo)

Cada integrante añade una línea. Indique el **escriba de L1** — quien consolida este Colab y la entrega en Moodle.

```python
contribution_log = """
- Nombre 1 — ...
- Nombre 2 — ...
- Nombre 3 — ...
- Nombre 4 — ...
Escriba L1: ...
"""
print(contribution_log)
```

---

## Tarea grupal (Moodle)

ZIP **`l1-introduction-<nombre-grupo>.zip`** hasta el **miércoles 10 de junio de 2026**:

| Archivo | Descripción |
|---------|-------------|
| `l1-introduction-<nombre-grupo>.ipynb` | Este cuaderno ejecutado (o exportado desde el Colab canónico) |
| `manifest.json` | Un registro por archivo DANE descargado |
| `project_requirements.pdf` | Requerimientos del proyecto (plantilla Word del curso) |

La **reflexión individual** (`l1-reflexion-<nombre>.pdf`) se entrega **por separado** — no va en este ZIP.

<!-- end NOTEBOOK: -->
