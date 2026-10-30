# Scripts

Helper scripts for the **public** site and shared workflows. Each tool lives in its own folder with its inputs and a README.

**Not here:** internal or task-specific scripts (course admin, grading, rosters, form specs, course data builders, notebook test runners) belong under **`work-space/<task-id>/`**. That folder is gitignored. See **Characteristic 2** in `.cursor/rules/customised_workspace.mdc`.

| Tool | Description |
|------|-------------|
| **[generate_content](generate_content/)** | Generate lecture pages, Marp slides, and Jupyter notebooks from Markdown; generate talk slides and update `_data/talks.yml`. |
| **[course_docs](course_docs/)** | Shared helpers for course Word documents (`docx_build.py`) and Markdown-to-PDF session plans (`session_plan_build.py`). |
| **[publications](publications/)** | `_data/publications.yml` to `bibfile.bib`; [ORCID sync](publications/sync_orcid.py) + [build](publications/build.py) ([workflow](../.github/workflows/build-publications.yml)). |
| **[pdf_to_markdown](pdf_to_markdown/)** | Extract a PDF into Markdown for use as LLM context (e.g. chat with a paper). |
| **[forms_build](forms_build/)** | Build Google Forms from YAML via the Google Forms API (`--sources-dir` points at the spec folder). |
| **[bulk_email](bulk_email/)** | Send personalized bulk emails from a CSV (Outlook or custom SMTP). |
| **[generate_wordcloud.py](generate_wordcloud.py)** | Generate a word-cloud PNG from a list of words or free text. |
| **[big-data-course](big-data-course/)** | Builders for the public Big Data data assets (Colombia departments GeoJSON, OSM services CSV). |
| **[data-mining-course](data-mining-course/)** | `swap_randomization.py`, the swap-randomisation null model used in the Data Mining notebooks. |

Run commands from the **repository root**. See each tool's README for setup and usage.
