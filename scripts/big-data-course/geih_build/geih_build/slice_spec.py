"""Slice specifications for project requirements / harmonise (L3+) — not used by the access layer."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class SliceSpec:
    """One month of GEIH to download from DANE."""

    year: int
    month: int

    @property
    def period(self) -> int:
        return self.year * 100 + self.month

    def label(self) -> str:
        return f"{self.year}-{self.month:02d}"


# L1 reference ids live in configs/l1_download.json — access uses catalog_id + file_id.


def subset_from_project_requirements_text(text: str) -> list[SliceSpec]:
    """Build month list from project requirements subset section (Spanish or English)."""
    years = _parse_year_range(text)
    if not years:
        years = [2024]
    months = _parse_months(text)
    return [SliceSpec(year=y, month=m) for y in years for m in months]


def subset_from_project_requirements(path: Path) -> list[SliceSpec]:
    """Parse subset from extracted markdown or plain text (e.g. after pdf_to_markdown)."""
    return subset_from_project_requirements_text(path.read_text(encoding="utf-8"))


def subset_from_requirements_file(path: Path) -> list[SliceSpec]:
    """Alias for ``subset_from_project_requirements`` (JSON or markdown text)."""
    return subset_from_project_requirements(path)


def expand_specs(specs: Iterable[SliceSpec]) -> list[SliceSpec]:
    return list(specs)


def _parse_year_range(text: str) -> list[int]:
    import re

    m = re.search(r"(?:Years|Años):\s*(\d{4})\s*[–\-]\s*(\d{4})", text, re.I)
    if m:
        return list(range(int(m.group(1)), int(m.group(2)) + 1))
    m = re.search(r"(?:Years|Años):\s*(\d{4})", text, re.I)
    if m:
        return [int(m.group(1))]
    return []


def _parse_months(text: str) -> list[int]:
    import re

    m = re.search(r"Months:\s*(\d+)\s*[–\-]\s*(\d+)", text, re.I)
    if m:
        return list(range(int(m.group(1)), int(m.group(2)) + 1))
    m = re.search(r"Months:\s*(\d+)", text, re.I)
    if m:
        return [int(m.group(1))]
    return list(range(1, 13))


def load_subset_file(path: Path) -> list[SliceSpec]:
    """JSON list: [{\"year\": 2024, \"month\": 1}, ...]."""
    data = json.loads(path.read_text(encoding="utf-8"))
    return [SliceSpec(year=row["year"], month=row["month"]) for row in data]
