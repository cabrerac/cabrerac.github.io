"""Load and save _data/publications.yml."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
PUB_YML = ROOT / "_data" / "publications.yml"
ORCID_DEFAULT = "0000-0002-6954-6859"


def normalize_doi(doi: str | None) -> str | None:
    if not doi:
        return None
    value = str(doi).strip().lower()
    for prefix in ("https://doi.org/", "http://doi.org/", "doi:"):
        if value.startswith(prefix):
            value = value[len(prefix) :]
    return value or None


def _link_fields_from_url(paper_url: str | None) -> dict[str, str]:
    if not paper_url:
        return {}
    if "arxiv.org/abs/" in paper_url:
        return {"arxiv": paper_url.rsplit("/abs/", 1)[-1].split("?")[0]}
    if "doi.org/" in paper_url:
        return {"doi": paper_url.rsplit("doi.org/", 1)[-1]}
    return {"url": paper_url}


def migrate_flat_list(entries: list[dict[str, Any]]) -> dict[str, Any]:
    publications = []
    for entry in entries:
        pub = dict(entry)
        pub["id"] = pub.pop("bibkey", pub.get("id", ""))
        paper_url = pub.pop("paper_url", None)
        pub.update(_link_fields_from_url(paper_url))
        pub.setdefault("source", "manual")
        pub.setdefault("show", True)
        publications.append(pub)
    return {"orcid": ORCID_DEFAULT, "publications": publications}


def load_publications_data(path: Path = PUB_YML) -> dict[str, Any]:
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    if raw is None:
        return {"orcid": ORCID_DEFAULT, "publications": []}
    if isinstance(raw, list):
        return migrate_flat_list(raw)
    if "publications" not in raw:
        raw["publications"] = []
    if not raw.get("orcid"):
        raw["orcid"] = ORCID_DEFAULT
    return raw


def write_yaml(data: dict[str, Any], path: Path = PUB_YML) -> None:
    path.write_text(
        yaml.dump(data, sort_keys=False, allow_unicode=True, width=1000),
        encoding="utf-8",
    )


def publication_dois(publications: list[dict[str, Any]]) -> set[str]:
    return {d for d in (normalize_doi(p.get("doi")) for p in publications) if d}


def normalize_title(title: str) -> str:
    import re

    text = title.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    return " ".join(text.split())
