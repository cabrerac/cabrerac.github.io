# geih_build — GEIH Access layer

Automated, modular, resumable downloads from [DANE microdatos](https://microdatos.dane.gov.co/).

Design: `work-space/teaching/big-data/planning/spine-build-pipeline.md`.

## Two commands

```bash
cd scripts/big-data-course/geih_build
pip install -e .

# Full course spine (2022–2025, CSV releases only) — stop and rerun anytime
geih-build access --refresh-catalog

# One survey year (every file on that catalog page)
geih-build access --years 2024

# L1 single file (catalog id + file id from get-microdata)
geih-build access --catalog 819 --file-id 23313

# Inspect progress
geih-build status
```

`access` automatically:

1. **Discovers** national GEIH catalog ids by searching DANE
2. **Scrapes** each get-microdata page for `{filename, file_id, url}` via `mostrarModal(...)`
3. **Downloads** ZIPs using **DANE filenames** (e.g. `Ene_2024.zip`)
4. **Extracts** CSVs to `data/raw/{filename_stem}/` (flat `.csv` or nested `csv.zip` inside the month bundle)
5. **Resumes** — skips files already on disk (`build_state.json`)

Only **CSV microdata ZIPs** are downloaded (SAV/TXT variants on older catalogs are skipped automatically). Survey year folders come from the catalog page metadata.

Use `--fresh` to re-download. Use `--plan path/to/plan.json` for custom year lists.

## Storage layout

| Path | Contents |
|------|----------|
| `data/raw/2024/Ene_2024.zip` | Downloaded ZIP (DANE filename under survey year) |
| `data/raw/2024/Ene_2024/` | Extracted CSVs |
| `catalog_registry.json` | Survey year → catalog id |
| `build_state.json` | Per-file extract status |

## Python API (Fynesse / notebooks)

```python
from geih_build.access import discover_catalogs, fetch_one, run, plan_from_years
from geih_build.dane_catalog import list_catalog_downloads

discover_catalogs()
for f in list_catalog_downloads(819):
    print(f.file_id, f.filename)

fetch_one(819, 23313)  # L1 file
run(plan_from_years([2024]))
```

L1 ids: `configs/l1_download.json` (catalog id + filename; file id from scrape).
