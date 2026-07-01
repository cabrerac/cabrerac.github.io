# Scripts

Helper scripts for the site and workflows. Each tool lives in its own folder with its inputs and a README.

| Tool | Description |
|------|-------------|
| **[bulk_email](bulk_email/)** | Send personalized bulk emails from a CSV (Outlook or custom SMTP). |
| **[forms_build](forms_build/)** | Build Google Forms from YAML via the Google Forms API. |
| **[generate_content](generate_content/)** | Generate lecture pages, Marp slides, and Jupyter notebooks from Markdown; generate talk slides and update `_data/talks.yml`. |
| **[pdf_to_markdown](pdf_to_markdown/)** | Extract a PDF into Markdown for use as LLM context (e.g. chat with a paper). |
| **[ensure_cursor_gitignored.ps1](ensure_cursor_gitignored.ps1)** | Add `.cursor/` to `.gitignore` and `git rm --cached` tracked Cursor rules across repos. |
| **[push_cursor_gitignore_repos.ps1](push_cursor_gitignore_repos.ps1)** | `pull` → commit `.gitignore` / `.cursor` untrack only → `push` (repos with no other dirty files). |
| **[sync_publication_urls.py](sync_publication_urls.py)** | Fill `paper_url` in `_data/publications.yml` from `assets/bibs/bibfile.bib` (doi, url, arXiv). On push to `gh-pages`, the [sync workflow](../.github/workflows/sync-publication-urls.yml) runs this automatically when the bib changes. |

Run commands from the **repository root**. See each tool’s README for setup and usage.
