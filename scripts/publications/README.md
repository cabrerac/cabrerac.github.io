# Publications

Single source of truth: **`_data/publications.yml`**.

Generated artifact: **`assets/bibs/bibfile.bib`** (for the site bibtex modal — do not edit by hand).

## Add a paper

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

On push to `gh-pages`, the [build workflow](../../.github/workflows/build-publications.yml) runs the same script and commits the bib file.

## ORCID

`orcid: 0000-0002-6954-6859` is stored at the top of the YAML. Phase 2 will add `sync_orcid.py` to propose new entries from ORCID.
