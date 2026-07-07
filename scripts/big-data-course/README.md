# Big Data course — reusable code (26-udenar-big-data)

Python tools used in **Colabs** and on student laptops for the Udenar Big Data course.

| Package | Role |
|---------|------|
| [`geih_build/`](geih_build/) | **Access:** download GEIH months from DANE, extract CSVs, log timings; harmonise to Parquet (L3+, stub) |
| [`check_submission.py`](check_submission.py) | **Marking aid:** PDF → markdown → pre-check for `project_requirements`, `reflection_week_1`–`reflection_week_3`, `reflection_l1` |
| [`grade_book.py`](grade_book.py) | **Grading:** CSV detail files → `grades.xlsx` (Excel formulas) + Moodle `calificaciones.csv` (grades + `Comentarios de retroalimentación`, UTF-8 BOM) |

**Planning:** `work-space/teaching/big-data/planning/spine-spec.md`, `project-requirements-template.md`

**Colabs:** `l1-introduction`, `l2-ethics-governance` (individual); **`week-1-group`** (week-1 group homework).

**Course Word documents:** `pip install -r requirements.txt` (includes `python-docx`), then:

```bash
python scripts/big-data-course/build_course_docx.py --all
```

Targets: `project_requirements`, `data_architecture`, `reflection_week_1`, `reflection_week_2`, `learning_journal_week_1`, `learning_journal_week_2`, `learning_journal_week_3`. Shared helpers live in `docx_build.py`.

Outputs:

- `assets/documents/26-udenar-big-data/project-requirements-template.docx`
- `assets/documents/26-udenar-big-data/reflection-week-1-template.docx`
- `assets/documents/26-udenar-big-data/reflection-week-2-template.docx`
- Mirrors under `work-space/teaching/big-data/course/week-1/` and `week-2/`
- Learning journals: `course/week-1/learning-journal-week-1.docx`, `course/week-2/learning-journal-week-2.docx`

**Project outline (Spanish PDF + DOCX):** `python scripts/big-data-course/build_project_outline.py` → `assets/documents/26-udenar-big-data/project-definition-big-data.pdf`

**Session plans (Spanish PDF):**

```bash
python scripts/big-data-course/build_course_session_plan.py --all
```

Targets: `week_1`, `week_2`. Renderer in `session_plan_build.py`. Outputs:

- `assets/documents/26-udenar-big-data/week-1-session-plan-es.pdf` (+ mirror `course/week-1/`)
- `assets/documents/26-udenar-big-data/week-2-session-plan-es.pdf` (+ mirror `course/week-2/`)

**Usage in notebooks:** students **implement** the same logic in the L1 Colab (no package import). **`geih_build`** is instructor reference / batch verification under `scripts/big-data-course/geih_build/`.
