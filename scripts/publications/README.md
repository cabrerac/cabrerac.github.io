# Publications

Single source of truth: **`_data/publications.yml`**.

Generated artifact: **`assets/bibs/bibfile.bib`** (for the site bibtex modal — do not edit by hand).

## Add a paper manually

Edit `_data/publications.yml` under `publications:`:

```yaml
  - id: mypaper2026
    title: "..."
    authors: "Christian Cabrera, ..."
    journal: "Venue name for display"
    year: 2026
    type: journal   # journal | conf | preprint | thesis
    topic: ml_systems
    doi: 10.1145/xxxx    # or arxiv: 2506.12345, or url: https://...
    source: manual
    show: true
```

Then run:

```bash
python scripts/publications/build.py
```

## Sync from ORCID

`orcid: 0000-0002-6954-6859` is at the top of the YAML.

```bash
python scripts/publications/sync_orcid.py --dry-run   # preview
python scripts/publications/sync_orcid.py           # append new DOIs
python scripts/publications/build.py
```

**ORCID sync rules**

- Matches existing rows by **DOI** or **title** — never overwrites your fields.
- New works are appended with `source: orcid`, `show: false`, `topic: other`.
- Review new rows: set `topic`, fix `journal` / `type` if needed, then `show: true`.

Metadata for new DOIs comes from [Crossref](https://www.crossref.org/).

## Automation

On push to `gh-pages` (and monthly), [build-publications.yml](../../.github/workflows/build-publications.yml) runs `sync_orcid.py` then `build.py` and commits changes.
