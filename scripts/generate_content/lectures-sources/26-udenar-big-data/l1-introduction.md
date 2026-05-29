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
---

<!-- NOTEBOOK: -->

## Instructions (read first)

**Purpose.** This notebook is your **Lecture 1 practice** notebook. You will **make available data from the DANE survey named "Gran Encuesta Integrada de Hogares (GEIH)"**. This is the first stage of the big-data process (**Access**).

**Scale disclaimer.** In production, national labour microdata spans **many years in the gigabytes or terabytes scale**. In this lab we access a shorter period of time so everyone can complete Access on Colab or a laptop. The **patterns** (catalog → download → extract → log) stay the same at larger scale.

**What to do (in order).**

1. Open this notebook in **Google Colab** (course website link) or run it locally with Python 3.10+.
2. Run cells **top to bottom** unless a cell tells you otherwise.
3. In cells marked **Your turn**, write your own text or code.
4. In cells marked **Check**, run the tests and fix earlier cells if something fails.
5. Bring questions from the **learning journal** to Saturday’s session.

**Folder layout** (created in the next section):

| Path | Role |
|------|------|
| `data/raw/` | Downloaded ZIP and extracted CSVs |
| `outputs/` | Diagrams and exports for homework |
| `manifest.json` | Access log (seconds, bytes, method) |

---

## How to build the download URL (read before Setup)

DANE publishes GEIH microdata at **[microdatos.dane.gov.co](https://microdatos.dane.gov.co/)**. To download a file you need a **direct download URL**. The catalog **home** page is not a data file — if you download that by mistake you get HTML instead of the actual data.

**Host and path pattern**

```text
https://microdatos.dane.gov.co/index.php/catalog/{catalog_id}/download/{file_id}
```

| Piece | Meaning | Example (January 2024) |
|-------|---------|-------------------------|
| `{catalog_id}` | DANE id for that **survey year** | `819` for 2024 |
| `{file_id}` | Internal id for **one uploaded ZIP** | `23313` (verify on the portal — it can change if DANE re-uploads) |

**Catalog id by year** (check on the portal when a new year appears):

| Year | Catalog id |
|------|------------|
| 2022–2023 | 782 |
| 2024 | 819 |
| 2025 | 853 |

**Three URLs students confuse — only the third downloads data**

| URL | Role |
|-----|------|
| `…/catalog/819` | Survey **description** (HTML) — do **not** use as download link |
| `…/catalog/819/get-microdata` | **File list** — one row per month, *Descargar* button |
| `…/catalog/819/download/23313` | **Direct ZIP** for one month — use this in code |

**Manual path (browser)** — same information your code will automate later:

1. Open `https://microdatos.dane.gov.co/index.php/catalog/819/get-microdata`
2. Find **January 2024** (`Ene_2024`, `GEIH_2024_ENE`, or similar).
3. Click **Descargar** (or inspect the link). The URL must contain **`/download/`**.
4. Example for January 2024:
   `https://microdatos.dane.gov.co/index.php/catalog/819/download/23313`

You **cannot** infer `{file_id}` from the month alone — always take it from get-microdata (browser or code). In the notebook, **Setup** defines constants; **Step 2** parses the page to build the URL programmatically.

---

## Setup — imports, constants, and folders

We use **`pandas`** and **`requests`** only (plus Python’s standard library). You will **implement** each access step in the cells below.

Run the next cell once.

```python
import json
import re
import time
import zipfile
from pathlib import Path

import pandas as pd
import requests

# L1 canonical month — same GEIH month for every student
YEAR = 2024
MONTH = 1
SLICE_LABEL = f"{YEAR}-{MONTH:02d}"

# DANE catalog id for 2024 GEIH (see microdatos.dane.gov.co)
CATALOG_BY_YEAR = {2022: 782, 2023: 782, 2024: 819, 2025: 853}
CATALOG_ID = CATALOG_BY_YEAR[YEAR]

# GEIH CSV conventions (verify on first open if preview fails)
LABOUR_CSV_SUFFIX = "Fuerza de trabajo.CSV"
CSV_SEP = ";"
CSV_ENCODING = "latin-1"

RAW_DIR = Path("data/raw")
OUTPUTS_DIR = Path("outputs")
RAW_DIR.mkdir(parents=True, exist_ok=True)
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

print(f"Slice: {SLICE_LABEL}  |  catalog id: {CATALOG_ID}")
```

**Check:**

```python
assert SLICE_LABEL == "2024-01"
assert CATALOG_ID == 819
assert RAW_DIR.is_dir() and OUTPUTS_DIR.is_dir()
print("Setup: OK")
```

---

## Step 1 — Open the catalog in your browser

Confirm the URLs from the section above. For Lecture 1 everyone uses **catalog 819**, **January 2024**.

```python
def get_microdata_page_url(catalog_id: int) -> str:
    return f"https://microdatos.dane.gov.co/index.php/catalog/{catalog_id}/get-microdata"

catalog_home = f"https://microdatos.dane.gov.co/index.php/catalog/{CATALOG_ID}"
microdata_page = get_microdata_page_url(CATALOG_ID)
print("Catalog home (metadata only):", catalog_home)
print("Get-microdata (monthly files):", microdata_page)
print("Expected download path shape:", f".../catalog/{CATALOG_ID}/download/{{file_id}}")
```

---

## Step 2 — Resolve the direct download URL (implement)

DANE assigns an internal file id per upload (e.g. `…/download/23313`). The get-microdata page embeds download links in JavaScript `mostrarModal('filename', 'url')` calls. **Your turn:** implement the helpers below, then resolve the URL for January 2024.

**Hint:** month names on the page include `Ene`, `Febrero`, … — match them inside the ZIP filename.

```python
MONTH_PAGE_LABELS = (
    "Ene", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre",
)

DOWNLOAD_ONCLICK_RE = re.compile(
    r"mostrarModal\(\s*'([^']+)'\s*,\s*'"
    r"(https://microdatos\.dane\.gov\.co/index\.php/catalog/\d+/download/\d+)\s*'\s*\)",
    re.IGNORECASE,
)


def year_from_filename(filename: str) -> int | None:
    m = re.search(r"(20\d{2})", filename)
    return int(m.group(1)) if m else None


def month_from_filename(filename: str) -> int | None:
    lower = filename.lower()
    for idx, label in enumerate(MONTH_PAGE_LABELS, start=1):
        if label.lower() in lower or label[:3].lower() in lower:
            return idx
    return None


def list_catalog_downloads(catalog_id: int) -> list[dict]:
    """Fetch get-microdata HTML and parse (filename, download_url) pairs."""
    resp = requests.get(get_microdata_page_url(catalog_id), timeout=120)
    resp.raise_for_status()
    files = []
    for filename, url in DOWNLOAD_ONCLICK_RE.findall(resp.text):
        month = month_from_filename(filename)
        year = year_from_filename(filename)
        if month and year:
            files.append(
                {"year": year, "month": month, "filename": filename, "url": url.strip()}
            )
    return files


def resolve_download_url(catalog_id: int, year: int, month: int) -> str:
    for item in list_catalog_downloads(catalog_id):
        if item["year"] == year and item["month"] == month:
            return item["url"]
    label = MONTH_PAGE_LABELS[month - 1]
    raise ValueError(
        f"No download link for {label} {year} on catalog {catalog_id}. "
        f"Open {get_microdata_page_url(catalog_id)} and use Descargar for that month."
    )


def validate_download_url(url: str) -> None:
    if "/download/" not in url:
        raise ValueError(
            "That URL looks like a catalog page, not a data file. "
            "Use the link from Descargar that contains /download/."
        )
```

```python
download_url = resolve_download_url(CATALOG_ID, YEAR, MONTH)
validate_download_url(download_url)
print("Direct download URL:", download_url)
```

**Check:**

```python
assert "/download/" in download_url, "Need a /download/ link, not the catalog home page"
assert str(CATALOG_ID) in download_url
print("Step 2 — download URL: OK")
```

---

## Step 3 — Download the monthly ZIP and record time (implement)

Stream the file to disk. A valid ZIP starts with the bytes `PK`. If you see HTML instead, the URL was wrong (Step 2).

```python
def download_zip(url: str, dest: Path, timeout: int = 600) -> tuple[float, int]:
    """Stream url to dest; return (seconds, bytes_written). Raise if not a ZIP."""
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
            f"Downloaded file is not a ZIP (got {magic!r}). "
            "Use the /download/ URL from get-microdata, not the catalog home page."
        )
    return elapsed, dest.stat().st_size


zip_path = RAW_DIR / f"{SLICE_LABEL}.zip"
download_seconds, bytes_downloaded = download_zip(download_url, zip_path)

print(f"Saved: {zip_path}")
print(f"Size: {bytes_downloaded / 1e6:.2f} MB")
print(f"Time: {download_seconds} s")
```

**Check:**

```python
assert zip_path.is_file(), "ZIP file missing"
assert zip_path.read_bytes()[:2] == b"PK", "Not a ZIP — fix the download URL"
assert bytes_downloaded > 1_000_000, "ZIP seems too small"
print("Step 3 — download: OK")
```

---

## Step 4 — Extract all CSV files (implement)

Each monthly ZIP contains **several** CSV tables. Access means making **all of them** available locally.

```python
def extract_csvs(zip_path: Path, dest_dir: Path) -> list[Path]:
    """Extract every .csv member; return sorted list of paths."""
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


month_dir = RAW_DIR / SLICE_LABEL
csv_files = extract_csvs(zip_path, month_dir)
total_csv_bytes = sum(p.stat().st_size for p in csv_files)

print(f"Extracted {len(csv_files)} CSV file(s) → {month_dir}/\n")
for p in csv_files:
    print(f"{p.stat().st_size / 1e6:8.2f} MB  {p.name}")
print(f"\nTotal extracted: {total_csv_bytes / 1e6:.2f} MB")
```

**Check:**

```python
assert len(csv_files) >= 1
labour_path = next(p for p in csv_files if LABOUR_CSV_SUFFIX.lower() in p.name.lower())
print("Primary labour table:", labour_path.name)
print("Step 4 — extract: OK")
```

---

## Step 5 — Preview the labour table

GEIH CSVs use **semicolon** separators and **`latin-1`** encoding. We preview **`Fuerza de trabajo.CSV`** (labour force) — the table most groups use first.

```python
df = pd.read_csv(labour_path, sep=CSV_SEP, encoding=CSV_ENCODING, low_memory=False)
n_rows = len(df)
n_cols = len(df.columns)

print(f"Rows: {n_rows:,}  |  Columns: {n_cols}")
print(f"Columns (first 12): {list(df.columns[:12])}")
df.head()
```

```python
df.info()
```

**Check:**

```python
assert n_rows > 10_000, "Expected a national month (tens of thousands of rows)"
assert "DPTO" in df.columns, "Expected DPTO (department code) column"
print("Step 5 — preview: OK")
```

---

## Step 6 — Write `manifest.json` (implement)

Groups submit **`manifest.json`** with homework: method, seconds, bytes per month. Use a **list of records** so you can append more months later.

```python
def write_manifest(path: Path, entries: list[dict]) -> None:
    path.write_text(json.dumps(entries, indent=2), encoding="utf-8")


manifest_entry = {
    "method": "http",
    "slice_label": SLICE_LABEL,
    "seconds": download_seconds,
    "bytes_downloaded": bytes_downloaded,
    "notes": f"extracted {len(csv_files)} CSVs ({total_csv_bytes} bytes)",
    "fallback_used": False,
}
manifest_path = Path("manifest.json")
write_manifest(manifest_path, [manifest_entry])
print(manifest_path.read_text(encoding="utf-8"))
```

**Check:**

```python
assert manifest_path.is_file()
data = json.loads(manifest_path.read_text(encoding="utf-8"))
assert data[0]["method"] == "http"
assert data[0]["bytes_downloaded"] > 0
print("Step 6 — manifest: OK")
```

---

## Step 7 — Classify the Vs (Your turn)

Using the files you now have on disk, fill in one sentence per **V**. This feeds the **learning journal** (question 8).

```python
vs_table = {
    "volume": "",    # e.g. ZIP size, number of CSVs, row count
    "velocity": "",  # e.g. how often DANE publishes; your download time
    "variety": "",   # e.g. multiple CSV tables, codes vs labels
    "veracity": "",  # e.g. official survey, weights, missing codes
}
# YOUR TURN — replace empty strings with one sentence each
vs_table["volume"] = "..."
vs_table["velocity"] = "..."
vs_table["variety"] = "..."
vs_table["veracity"] = "..."

for v, sentence in vs_table.items():
    print(f"{v}: {sentence}")
```

**Check:**

```python
for v, sentence in vs_table.items():
    assert isinstance(sentence, str) and len(sentence.strip()) >= 20, f"Write at least one sentence for {v}"
print("Step 7 — Vs table: OK")
```

---

## Step 8 — Three As map (Your turn)

**Access** ends when raw files are local and logged. **Assess** (L2–L4) and **Address** (L5–L6) come later.

```python
three_as = """
| Stage | L1 status | What happens next (your group) |
|-------|-----------|--------------------------------|
| Access | DONE in this notebook | … |
| Assess | Not yet | … |
| Address | Not yet | … |
"""
# YOUR TURN — replace the … placeholders (2–4 bullets total across Assess and Address)
print(three_as)
```

---

## Step 9 — Architecture diagram (Your turn)

Copy the course pipeline template, relabel it for your **decision archetype** (see case shell), and save as **`outputs/architecture.svg`**.

Template: [big-data-pipeline-template.svg](https://cabrerac.github.io/assets/media/diagrams/big-data-pipeline-template.svg)

On Colab you can download it:

```python
template_url = "https://cabrerac.github.io/assets/media/diagrams/big-data-pipeline-template.svg"
template_path = OUTPUTS_DIR / "big-data-pipeline-template.svg"
if not template_path.is_file():
    r = requests.get(template_url, timeout=60)
    r.raise_for_status()
    template_path.write_bytes(r.content)
print("Template saved to:", template_path)
print("Your turn: open in draw.io / Inkscape / your editor, relabel, save as outputs/architecture.svg")
```

---

## Step 10 — Deployment paragraph (Your turn)

In **3–5 sentences**, state whether your pipeline would run **cloud**, **edge**, **hybrid**, or **batch vs interactive** in production, and one assumption.

```python
deployment_paragraph = """
YOUR TEXT HERE
"""
print(deployment_paragraph.strip())
```

---

## Step 11 — Fit and limits (Your turn)

Where do **big-data methods** help for your charter question, and where would they be **overkill** at this scale?

```python
fit_and_limits = """
YOUR TEXT HERE
"""
print(fit_and_limits.strip())
```

---

## Step 12 — Charter draft (Your turn — individual)

Draft sections below. After **Saturday**, your group merges one **`charter.md`** using the [charter template](https://github.com/cabrerac/cabrerac.github.io/blob/main/work-space/teaching/big-data/planning/charter-template.md) (exact headings required).

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

## Step 13 — Wrap Access in one function (for group homework)

After Saturday, your group will fetch **more months** from the charter. Refactor Steps 2–6 into a single function and loop over `(year, month)` pairs.

```python
def access_month(
    year: int,
    month: int,
    catalog_id: int,
    raw_dir: Path,
) -> dict:
    """
    Resolve URL → download ZIP → extract CSVs → return one manifest record.
    Implement by calling your functions from Steps 2–4 and download_zip.
    """
    label = f"{year}-{month:02d}"
    url = resolve_download_url(catalog_id, year, month)
    validate_download_url(url)
    zip_path = raw_dir / f"{label}.zip"
    seconds, nbytes = download_zip(url, zip_path)
    month_dir = raw_dir / label
    files = extract_csvs(zip_path, month_dir)
    return {
        "method": "http",
        "slice_label": label,
        "seconds": seconds,
        "bytes_downloaded": nbytes,
        "notes": f"extracted {len(files)} CSVs",
        "fallback_used": False,
    }


# Example: append a second month after your charter is fixed
# entries = [manifest_entry]
# entries.append(access_month(2024, 2, CATALOG_BY_YEAR[2024], RAW_DIR))
# write_manifest(manifest_path, entries)
print("Implement access_month for L1 group homework (multiple months).")
```

---

## Access completion check

Run after Steps 1–6 (and your Vs table if ready). Prints **`ACCESS_OK`** when the core access path succeeded.

```python
def _ok(name, fn):
    try:
        ok = bool(fn())
    except Exception:
        ok = False
    print(f"{name}: {'OK' if ok else 'incomplete'}")
    return ok

checks = [
    ("ZIP on disk", lambda: zip_path.is_file() and zip_path.read_bytes()[:2] == b"PK"),
    ("CSVs extracted", lambda: len(csv_files) >= 1),
    ("Labour preview", lambda: n_rows > 10_000),
    ("manifest.json", lambda: manifest_path.is_file()),
    ("Vs table", lambda: all(len(vs_table[k].strip()) >= 20 for k in vs_table)),
]
passed = sum(_ok(name, fn) for name, fn in checks)
print(f"\nACCESS_CHECKS={passed}/{len(checks)}")
if passed >= 4:
    print("ACCESS_OK — you completed the L1 access path.")
```

---

## § Homework (group — after Saturday)

Due per Moodle (typically **Wednesday** after L1). Consolidate on your **canonical group Colab**.

| Deliverable | Notes |
|-------------|--------|
| **`charter.md`** | Full template; include **Ethical concern + reading** (Zuboff Ch. 1 by name) |
| **`architecture.svg`** | Relabelled pipeline from Step 9 |
| **`manifest.json`** | One record per month; use `access_month` (Step 13) in a loop for charter months |
| **`data/raw/`** | ZIP + extracted CSVs |

**Example — two months in the manifest:**

```python
# entries = [
#     access_month(2024, 1, CATALOG_BY_YEAR[2024], RAW_DIR),
#     access_month(2024, 2, CATALOG_BY_YEAR[2024], RAW_DIR),
# ]
# write_manifest(Path("manifest.json"), entries)
```

No **`L1_output.parquet`** — L1 artefacts are the charter, diagram, and access log.

---

## § Contribution log (group)

One line per member; name the **L1 scribe** (owns canonical Colab consolidation this week).

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

## § Reflection (individual — Moodle after homework)

Submit on Moodle. Link **one architecture trade-off** (cloud / edge / batch) to **privacy, harm, or governance**, citing **boyd & Crawford** or **Zuboff Ch. 1**.

Prompt: *Which part of your Access setup would change first if DANE restricted bulk downloads, and what would that imply for public accountability?*

<!-- end NOTEBOOK: -->
