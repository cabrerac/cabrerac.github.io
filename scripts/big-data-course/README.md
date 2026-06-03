# Big Data course — reusable code (26-udenar-big-data)

Python tools used in **Colabs** and on student laptops for the Udenar Big Data course.

| Package | Role |
|---------|------|
| [`geih_build/`](geih_build/) | **Access:** download GEIH months from DANE, extract CSVs, log timings; harmonise to Parquet (L3+, stub) |
| [`check_submission.py`](check_submission.py) | **Marking aid:** PDF → markdown (`scripts/pdf_to_markdown`) → mechanical pre-check for L1 `project_requirements` and `reflection_l1` |

**Planning:** `work-space/teaching/big-data/planning/spine-spec.md`, `project-requirements-template.md`

**Colabs:** `l1-introduction` (individual practice), `l1-introduction-group` (group homework 2022–2025; notebook only).

**L1 Word templates:** `pip install -r requirements.txt` (includes `python-docx`), then `python scripts/big-data-course/build_l1_docx_templates.py` → `assets/documents/26-udenar-big-data/*.docx`

**Usage in notebooks:** students **implement** the same logic in the L1 Colab (no package import). **`geih_build`** is instructor reference / batch verification under `scripts/big-data-course/geih_build/`.
