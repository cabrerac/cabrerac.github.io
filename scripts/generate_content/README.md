# Generate content (lectures & talks)

Generates site content and assets from Markdown sources: lecture pages, Marp HTML slides, and Jupyter notebooks for courses; slides and optional talk pages for standalone talks.

## Layout

- **`generate_content.py`** — main script (run from repo root).
- **`lectures-sources/`** — one folder per course (e.g. `25-udenar-ml-intro/`), each with `.md` lecture files.
- **`talks-sources/`** — one `.md` file per talk (e.g. `icms-intellectual-debt.md`).

Outputs go to repo-level paths: `content/_lectures/`, `content/_talks/`, `assets/slides/`, `assets/notebooks/`, and `_data/talks.yml` is updated for talks.

## Content tags (in source Markdown)

- `<!-- RENDER: -->` … `<!-- end RENDER: -->` — included in the rendered lecture/talk page.
- `<!-- SLIDES: -->` … `<!-- end SLIDES: -->` — included only in Marp slides.
- `<!-- NOTEBOOK: -->` … `<!-- end NOTEBOOK: -->` — included only in the Jupyter notebook.
- `<!-- ALL: -->` … `<!-- end ALL: -->` — included in all of the above.
- `<!-- PDF -->` inside a slide — mark that slide for PDF export (HTML still gets all slides).

## Requirements

- Python 3 with: `pyyaml`, `nbformat`, `python-magic` (or `python-magic-bin` on Windows), `Pillow`, `requests`.
- **Marp CLI** for slides: `npm install -g @marp-team/marp-cli` (and Node.js on PATH).
- Course metadata: `content/_courses/<course_code>.md` must exist for lecture generation.

## Usage

Run from the **repository root**:

```bash
# One lecture (course_code/lecture_name)
python scripts/generate_content/generate_content.py 25-udenar-ml-intro/ai-systems

# One talk
python scripts/generate_content/generate_content.py --talk icms-intellectual-debt

# All talks
python scripts/generate_content/generate_content.py --talk-all
```

## Talk front matter

In `talks-sources/<talk_id>.md`, set at least `year` (and optionally `output_page: true` to generate a talk page in `content/_talks/`). Other fields (title, venue, etc.) are written to `_data/talks.yml`.
