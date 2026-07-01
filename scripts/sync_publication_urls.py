#!/usr/bin/env python3
"""Sync paper_url in _data/publications.yml from assets/bibs/bibfile.bib.

Workflow when you publish a new paper:
  1. Add a @entry to assets/bibs/bibfile.bib (doi, url, or arXiv eprint).
  2. Add a matching row to _data/publications.yml (same bibkey; paper_url optional).
  3. Push — the GitHub Action runs this script and commits URL updates.

Run locally: python scripts/sync_publication_urls.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
BIB = ROOT / "assets" / "bibs" / "bibfile.bib"
PUB = ROOT / "_data" / "publications.yml"

# Entries without doi/url/eprint in bib, or where bib is not the best link.
MANUAL_URLS: dict[str, str] = {
    "palade2018middleware": "https://doi.org/10.1007/s40860-018-0055-4",
    "white2019augmented": "https://doi.org/10.1007/978-3-030-17642-6_13",
    "cabrera2018services": "https://doi.org/10.1007/978-3-030-03596-9_21",
    "palade2018stigmergic": "https://doi.org/10.1007/978-3-030-03596-9_45",
    "cabrera2020udiscovery": "https://www.tara.tcd.ie/handle/2262/91854",
    "cabrera2014sedea": "http://www.scielo.org.co/scielo.php?pid=S0124-71072014000200008&script=sci_arttext",
}


def parse_bib(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    urls: dict[str, str] = {}
    for block in re.split(r"\n@", text):
        block = block.strip()
        if not block:
            continue
        if not block.startswith("@"):
            block = "@" + block
        key_match = re.search(r"@\w+\{([^,]+),", block)
        if not key_match:
            continue
        key = key_match.group(1).strip()
        doi = re.search(r"doi\s*=\s*\{([^}]+)\}", block)
        url = re.search(r"url\s*=\s*\{([^}]+)\}", block)
        eprint = re.search(r"eprint\s*=\s*\{([^}]+)\}", block)
        if doi:
            urls[key] = f"https://doi.org/{doi.group(1).strip()}"
        elif url:
            urls[key] = url.group(1).strip()
        elif eprint:
            urls[key] = f"https://arxiv.org/abs/{eprint.group(1).strip()}"
    return urls


def main() -> int:
    bib_urls = parse_bib(BIB)
    publications = yaml.safe_load(PUB.read_text(encoding="utf-8"))
    updated = 0
    missing: list[str] = []

    for entry in publications:
        bibkey = entry.get("bibkey")
        if not bibkey:
            continue
        new_url = MANUAL_URLS.get(bibkey) or bib_urls.get(bibkey)
        if new_url and entry.get("paper_url") != new_url:
            entry["paper_url"] = new_url
            updated += 1
        elif not new_url and not entry.get("paper_url"):
            missing.append(bibkey)

    if updated == 0:
        print("No paper_url changes.")
        if missing:
            print("Still missing links:", ", ".join(missing))
        return 0

    PUB.write_text(
        yaml.dump(publications, sort_keys=False, allow_unicode=True, width=1000),
        encoding="utf-8",
    )
    print(f"Updated {updated} paper_url entries in {PUB.relative_to(ROOT)}")
    if missing:
        print("Still missing links:", ", ".join(missing))
    return 0


if __name__ == "__main__":
    sys.exit(main())
