# Scripts

Helper scripts for the **public** site and shared workflows. Each tool lives in its own folder with its inputs and a README.

**Not here:** internal or task-specific scripts (grant forms, admin prep, one-offs) belong under **`work-space/<task-id>/`** — that folder is gitignored. See **Characteristic 2** in `.cursor/rules/customised_workspace.mdc`.

| Tool | Description |
|------|-------------|
| **[bulk_email](bulk_email/)** | Send personalized bulk emails from a CSV (Outlook or custom SMTP). |
| **[forms_build](forms_build/)** | Build Google Forms from YAML via the Google Forms API. |
| **[generate_content](generate_content/)** | Generate lecture pages, Marp slides, and Jupyter notebooks from Markdown; generate talk slides and update `_data/talks.yml`. |
| **[pdf_to_markdown](pdf_to_markdown/)** | Extract a PDF into Markdown for use as LLM context (e.g. chat with a paper). |
| **[ensure_cursor_gitignored.ps1](ensure_cursor_gitignored.ps1)** | Add `.cursor/` to `.gitignore` and `git rm --cached` tracked Cursor rules across repos. |
| **[push_cursor_gitignore_repos.ps1](push_cursor_gitignore_repos.ps1)** | `pull` → commit `.gitignore` / `.cursor` untrack only → `push` (repos with no other dirty files). |
| **[publications/](publications/)** | `_data/publications.yml` → `bibfile.bib`; [ORCID sync](publications/sync_orcid.py) + [build](publications/build.py) ([workflow](../.github/workflows/build-publications.yml)). |

Run commands from the **repository root**. See each tool’s README for setup and usage.
