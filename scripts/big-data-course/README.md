# Big Data course — reusable code (26-udenar-big-data)

Python tools used in **Colabs** and on student laptops for the Udenar Big Data course.

| Package | Role |
|---------|------|
| [`geih_build/`](geih_build/) | **Access:** download GEIH months from DANE, extract CSVs, log timings; harmonise to Parquet (L3+, stub) |
| [`check_submission.py`](check_submission.py) | **Marking aid:** PDF → markdown → pre-check for `project_requirements`, `reflection_week_1`, `reflection_l1` |

**Planning:** `work-space/teaching/big-data/planning/spine-spec.md`, `project-requirements-template.md`

**Colabs:** `l1-introduction`, `l2-ethics-governance` (individual); **`week-1-group`** (week-1 group homework).

**L1 Word templates:** `pip install -r requirements.txt` (includes `python-docx`), then `python scripts/big-data-course/build_l1_docx_templates.py` → `assets/documents/26-udenar-big-data/*.docx`

**Project outline (Spanish PDF + DOCX):** `python scripts/big-data-course/build_project_outline.py` → `assets/documents/26-udenar-big-data/project-definition-big-data.pdf`

**Usage in notebooks:** students **implement** the same logic in the L1 Colab (no package import). **`geih_build`** is instructor reference / batch verification under `scripts/big-data-course/geih_build/`.
