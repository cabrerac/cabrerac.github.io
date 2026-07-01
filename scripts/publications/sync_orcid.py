#!/usr/bin/env python3
"""Propose new publications in _data/publications.yml from ORCID + Crossref.

Does not change topic, show, venue, or other fields on existing rows.
New ORCID works are appended with show: false for your review.

  python scripts/publications/sync_orcid.py
  python scripts/publications/sync_orcid.py --dry-run
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from typing import Any

from store import (
    PUB_YML,
    load_publications_data,
    normalize_doi,
    normalize_title,
    publication_dois,
    write_yaml,
)

ORCID_HEADERS = {"Accept": "application/vnd.orcid+json"}
CROSSREF_HEADERS = {"Accept": "application/json", "User-Agent": "cabrerac.github.io (publications-sync)"}


def fetch_json(url: str, headers: dict[str, str]) -> dict[str, Any]:
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode())


def fetch_orcid_works(orcid: str) -> list[dict[str, Any]]:
    url = f"https://pub.orcid.org/v3.0/{orcid}/works"
    payload = fetch_json(url, ORCID_HEADERS)
    works: list[dict[str, Any]] = []
    for group in payload.get("group", []):
        summary = group.get("work-summary", [{}])[0]
        title = (
            summary.get("title", {})
            .get("title", {})
            .get("value", "")
            .strip()
        )
        doi = None
        for external in summary.get("external-ids", {}).get("external-id", []) or []:
            if str(external.get("external-id-type", "")).lower() == "doi":
                doi = normalize_doi(external.get("external-id-value"))
                break
        works.append(
            {
                "title": title,
                "doi": doi,
                "orcid_type": summary.get("type", ""),
            }
        )
    return works


def fetch_crossref_metadata(doi: str) -> dict[str, Any] | None:
    try:
        payload = fetch_json(f"https://api.crossref.org/works/{doi}", CROSSREF_HEADERS)
    except urllib.error.HTTPError:
        return None
    return payload.get("message")


def _year_from_crossref(message: dict[str, Any]) -> int | None:
    for key in ("published-print", "published-online", "created", "issued"):
        parts = message.get(key, {}).get("date-parts", [[]])
        if parts and parts[0]:
            return int(parts[0][0])
    return None


def _authors_from_crossref(message: dict[str, Any]) -> str:
    names: list[str] = []
    for author in message.get("author", []):
        given = author.get("given", "").strip()
        family = author.get("family", "").strip()
        if family and given:
            names.append(f"{given} {family}")
        elif family:
            names.append(family)
    return ", ".join(names)


def _venue_from_crossref(message: dict[str, Any]) -> str:
    for key in ("container-title", "publisher"):
        values = message.get(key) or []
        if values and values[0]:
            return str(values[0])
    event = message.get("event", {}) or {}
    if event.get("name"):
        return str(event["name"])
    return "Unknown venue"


def infer_pub_type(crossref_type: str, orcid_type: str) -> str:
    crossref_type = (crossref_type or "").lower()
    orcid_type = (orcid_type or "").lower()
    if crossref_type in {"journal-article"} or orcid_type in {"journal-article"}:
        return "journal"
    if crossref_type in {"proceedings-article", "book-chapter"} or orcid_type in {
        "conference-paper",
        "book-chapter",
    }:
        return "conf"
    if crossref_type in {"dissertation"} or orcid_type in {"dissertation"}:
        return "thesis"
    if crossref_type in {"posted-content", "report"} or "preprint" in orcid_type:
        return "preprint"
    return "conf"


def make_id(authors: str, year: int, title: str, existing_ids: set[str]) -> str:
    family = authors.split(",")[0].strip().split()[-1].lower()
    family = re.sub(r"[^a-z]", "", family) or "work"
    word = re.sub(r"[^a-z0-9]", "", title.split()[0].lower())[:10] or "paper"
    base = f"{family}{year}{word}"
    candidate = base
    suffix = 2
    while candidate in existing_ids:
        candidate = f"{base}{suffix}"
        suffix += 1
    return candidate


def entry_from_crossref(
    doi: str,
    orcid_type: str,
    existing_ids: set[str],
) -> dict[str, Any] | None:
    message = fetch_crossref_metadata(doi)
    if not message:
        return None
    title = (message.get("title") or [""])[0].strip()
    year = _year_from_crossref(message)
    authors = _authors_from_crossref(message)
    if not title or not year or not authors:
        return None
    pub_id = make_id(authors, year, title, existing_ids)
    return {
        "id": pub_id,
        "title": title,
        "authors": authors,
        "journal": _venue_from_crossref(message),
        "year": year,
        "type": infer_pub_type(message.get("type", ""), orcid_type),
        "topic": "other",
        "doi": doi,
        "source": "orcid",
        "show": False,
    }


def existing_titles(publications: list[dict[str, Any]]) -> set[str]:
    return {normalize_title(p.get("title", "")) for p in publications if p.get("title")}


def sync_from_orcid(data: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    orcid = data.get("orcid", "")
    publications = list(data.get("publications", []))
    known_dois = publication_dois(publications)
    known_titles = existing_titles(publications)
    existing_ids = {str(p["id"]) for p in publications if p.get("id")}
    messages: list[str] = []
    added = 0

    for work in fetch_orcid_works(orcid):
        title_key = normalize_title(work.get("title", ""))
        if title_key and title_key in known_titles:
            continue

        doi = work.get("doi")
        if not doi:
            messages.append(f"Skipped (no DOI on ORCID): {work.get('title', '?')}")
            continue
        if doi in known_dois:
            continue

        entry = entry_from_crossref(doi, work.get("orcid_type", ""), existing_ids)
        if not entry:
            messages.append(f"Skipped (Crossref lookup failed): {doi}")
            continue

        publications.append(entry)
        known_dois.add(doi)
        known_titles.add(normalize_title(entry["title"]))
        existing_ids.add(entry["id"])
        added += 1
        messages.append(f"Added (show: false): {entry['title'][:70]}")

    data["publications"] = publications
    if added:
        messages.insert(0, f"Added {added} publication(s) from ORCID.")
    else:
        messages.insert(0, "No new ORCID publications to add.")
    return data, messages


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync publications from ORCID.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print changes without writing publications.yml",
    )
    args = parser.parse_args()

    data = load_publications_data(PUB_YML)
    updated, messages = sync_from_orcid(data)
    for line in messages:
        print(line)

    if args.dry_run or messages[0].startswith("No new"):
        return 0

    write_yaml(updated, PUB_YML)
    print(f"Wrote {PUB_YML}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
