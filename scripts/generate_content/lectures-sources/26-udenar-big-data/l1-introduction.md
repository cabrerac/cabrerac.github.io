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

## Instructions

**Purpose.** This notebook is your **Lecture 1 practice** notebook. You will **make available data from the DANE survey "Gran Encuesta Integrada de Hogares (GEIH)"**. That is the first stage of our methodology: **Access** (making data available before we assess or analyse it).

In production, national labour microdata spans **many years at gigabyte or terabyte scale**. In this lab we download **one month** so everyone can finish on Colab or a laptop. The **pattern** is the same at larger scale: catalog → download URL → ZIP on disk → extract → log.

**What to do (in order).**

1. Read **How to build the download URL** below — it explains what we automate in code.
2. Open this notebook in **Google Colab** or run it locally with Python 3.10+.
3. Run cells **top to bottom** unless a cell tells you otherwise.
4. In cells marked **Your turn**, write your own text or code.
5. In cells marked **Check**, run the tests and fix earlier cells if something fails.
6. Bring questions from the **learning journal** to Saturday’s session.

**Folder layout** (the Setup cell creates these paths):

| Path | Role |
|------|------|
| `data/raw/` | Downloaded ZIP and extracted CSVs |
| `outputs/` | Diagrams and exports for homework |
| `manifest.json` | Access log (seconds, bytes, method) |

---

## How to build the download URL

DANE publishes GEIH microdata at **[microdatos.dane.gov.co](https://microdatos.dane.gov.co/)**. To download a data file, you can do it manually by following these instructions:

**Manual path (browser)**:

1. Open `https://microdatos.dane.gov.co/index.php/catalog/819/get-microdata`
2. Find **January 2024** (`Ene_2024`, `GEIH_2024_ENE`, or similar).
3. Click **Descargar** (or inspect the link). The URL must contain **`/download/`**.
4. Example for January 2024:
   `https://microdatos.dane.gov.co/index.php/catalog/819/download/23313`

This manual process works, but it is not practical when we need many files across several years of the survey. We can automate downloads instead. As a first step, we need a **direct download URL**, which we build by exploring the DANE website.

**Host and path pattern**

As an example, the following links correspond to the descriptions of the survey for years 2024, 2025, and 2026.

```text
https://microdatos.dane.gov.co/index.php/catalog/819/
https://microdatos.dane.gov.co/index.php/catalog/853/
https://microdatos.dane.gov.co/index.php/catalog/900/
```

We can see that DANE assigns a `catalog_id` for each year: `819` for 2024, `853` for 2025, and `900` for 2026. DANE splits the data files for each year by month. For example, you can see the list of data files for 2024 [here](https://microdatos.dane.gov.co/index.php/catalog/819/get-microdata). This organisation means we can download one survey file for a given month. The following URLs are the 2024 files for January and February:

```text
https://microdatos.dane.gov.co/index.php/catalog/819/download/23313
https://microdatos.dane.gov.co/index.php/catalog/819/download/23362
```

We can also see that DANE assigns a `file_id` for each data file. For example, the `file_id` for January 2024 is `23313`. From this exploration, we can identify the following pattern:


```text
https://microdatos.dane.gov.co/index.php/catalog/{catalog_id}/download/{file_id}
```

| Piece | Meaning | Example (January 2024) |
|-------|---------|-------------------------|
| `{catalog_id}` | DANE id for that **survey year** | `819` for 2024 |
| `{file_id}` | Internal id for **one uploaded ZIP** | `23313` for January 2024 |

We **cannot** infer `{file_id}` from the month alone — always read it from get-microdata (browser or code). The catalog home page (`…/catalog/819/`) is **not** a download link. If we fetch that URL you get HTML, not a ZIP.

The cells below implement this exploration in Python. **Setup** defines constants; **Step 2** parses the get-microdata page to build the URL automatically.

---

## Setup — imports, constants, and folders

We use **`pandas`** and **`requests`**, plus Python’s standard library. The next cell creates the folder layout from the table above and sets constants for **January 2024** (catalog `819`). Everyone in Lecture 1 uses the same month so we can compare downloads on Saturday.

Run the cell once.

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

## Step 1 — Confirm the catalog pages in code

In the previous section we opened get-microdata in the browser. Here we build the same URLs in Python so the later steps can call them automatically. For Lecture 1 we use **catalog 819** and **January 2024**.

The **catalog home** URL is useful for metadata only. The **get-microdata** URL lists monthly files. The **download** URL (built in Step 2) is the one that returns the ZIP.

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

## Step 2 — Resolve the direct download URL

On the get-microdata page, DANE embeds each download link in a JavaScript call: `mostrarModal('filename', 'url')`. We fetch that page with **`requests`**, parse the HTML, and read the same `{catalog_id}` and `{file_id}` we identified above.

Implement the functions below, then resolve the URL for **January 2024**.

**Hint:** filenames include Spanish month names (`Ene`, `Febrero`, …). Match them inside the ZIP filename.

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

## Step 3 — Download the monthly ZIP

A direct download URL returns one ZIP file (national GEIH for that month). We stream it to `data/raw/` and record elapsed time and file size — you will use both numbers in the **manifest** and in the **Vs** discussion.

Every valid ZIP starts with the bytes **`PK`**. If you see anything else, the URL was wrong — usually the catalog description page instead of a `/download/…` link.

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

## Step 4 — Extract the CSV files

Each monthly ZIP contains **several** CSV tables (labour, housing, education, and others). Access means making **all** of them available on disk, not only the table we analyse first.

Implement **`extract_csvs`** below. It should write every `.csv` member into a month folder such as `data/raw/2024-01/`.

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

DANE ships GEIH CSVs with **semicolon** separators and **`latin-1`** encoding. If **`read_csv`** fails, check those two settings before changing anything else.

We preview **`Fuerza de trabajo.CSV`** (labour force). Most groups start with this table; the other CSVs from Step 4 stay on disk for later weeks.

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

## Step 6 — Write the access log (`manifest.json`)

Group homework asks you to download **every month** in your charter. A small **manifest** records what you fetched: method, seconds, and bytes. We compare manifests across groups on Saturday to discuss Access at scale.

Store **one JSON object per month** in a list so you can append rows when you call **`access_month`** in Step 13.

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

You now have real files on disk. For each **V** (volume, velocity, variety, veracity), write **one sentence** grounded in **this download** — not a generic definition. Your answers feed the **learning journal** (question 8).

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

Our methodology has three stages: **Access → Assess → Address**. In this notebook you complete **Access** (files local and logged). **Assess** and **Address** come in later lectures.

Fill in the table below: what will your group do in Assess and Address?

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

Sketch how data moves from DANE to your group’s decision. Download the course template, relabel it for your **decision archetype** (see the [case shell](https://github.com/cabrerac/cabrerac.github.io/blob/main/work-space/teaching/big-data/planning/case-shell.md)), and save as **`outputs/architecture.svg`**.

Template: [big-data-pipeline-template.svg](https://cabrerac.github.io/assets/media/diagrams/big-data-pipeline-template.svg)

On Colab you can fetch the template with the cell below, then edit in draw.io, Inkscape, or another SVG editor.

```python
template_url = "https://cabrerac.github.io/assets/media/diagrams/big-data-pipeline-template.svg"
template_path = OUTPUTS_DIR / "big-data-pipeline-template.svg"
if not template_path.is_file():
    r = requests.get(template_url, timeout=60)
    r.raise_for_status()
    template_path.write_bytes(r.content)
print("Template saved to:", template_path)
print("Your turn: relabel the diagram and save as outputs/architecture.svg")
```

---

## Step 10 — Deployment paragraph (Your turn)

Imagine your pipeline in production — not only on Colab. In **3–5 sentences**, say whether it would run on **cloud**, **edge**, or **hybrid** infrastructure, and whether work is **batch** or **interactive**. State **one assumption** you are making.

```python
deployment_paragraph = """
YOUR TEXT HERE
"""
print(deployment_paragraph.strip())
```

---

## Step 11 — Fit and limits (Your turn)

Big-data methods are not always the right tool. For **your** charter question, where would a distributed stack help? Where would it be **overkill** at the scale you accessed today?

```python
fit_and_limits = """
YOUR TEXT HERE
"""
print(fit_and_limits.strip())
```

---

## Step 12 — Charter draft (Your turn)

Draft your group’s **`charter.md`** in the cell below. After **Saturday**, merge one version per group using the [charter template](https://github.com/cabrerac/cabrerac.github.io/blob/main/work-space/teaching/big-data/planning/charter-template.md). Headings must match exactly so we can check them automatically.

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

## Step 13 — Wrap Access in one function

After Saturday your group will download **every month** listed in the charter. Refactor Steps 2–6 into **`access_month`**, call it in a loop, and append each result to **`manifest.json`**.

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
print("Implement access_month for L1 group homework — one manifest row per month.")
```

---

## Access completion check

Run this cell after Steps 1–6 (and Step 7 if your Vs table is ready). It prints **`ACCESS_OK`** when the core access path succeeded.

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

## Homework (group — after Saturday)

Submit on Moodle (typically **Wednesday** after L1). Consolidate on your **canonical group Colab** — one notebook the whole group maintains.

| Deliverable | Notes |
|-------------|--------|
| **`charter.md`** | Full template; include **Ethical concern + reading** (cite **Zuboff Ch. 1** by name) |
| **`architecture.svg`** | Relabelled pipeline from Step 9 |
| **`manifest.json`** | One record per month; loop **`access_month`** (Step 13) over charter months |
| **`data/raw/`** | ZIP files and extracted CSVs |

**Example — two months in one manifest:**

```python
# entries = [
#     access_month(2024, 1, CATALOG_BY_YEAR[2024], RAW_DIR),
#     access_month(2024, 2, CATALOG_BY_YEAR[2024], RAW_DIR),
# ]
# write_manifest(Path("manifest.json"), entries)
```

There is no **`L1_output.parquet`** for this lecture. L1 artefacts are the charter, the diagram, and the access log.

---

## Contribution log (group)

Each member adds one line. Name the **L1 scribe** — the person who consolidates the canonical Colab this week.

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

## Reflection (individual — Moodle after homework)

Submit on Moodle. Link **one architecture trade-off** (cloud, edge, or batch) to **privacy, harm, or governance**, citing **boyd & Crawford** or **Zuboff Ch. 1**.

**Prompt:** *If DANE restricted bulk downloads tomorrow, which part of your Access setup would you change first — and what would that mean for public accountability?*

<!-- end NOTEBOOK: -->
