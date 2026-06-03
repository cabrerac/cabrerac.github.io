"""Slice specifications for charter/harmonise (L3+) — not used by the access layer."""

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


def subset_from_charter_json(charter_path: Path) -> list[SliceSpec]:
    """
    Build month list from a group charter ``## Subset`` block (best-effort parse).

    For access downloads, expand survey years to DANE files via ``AccessPlan`` instead.
    """
    text = charter_path.read_text(encoding="utf-8")
    years = _parse_year_range(text)
    if not years:
        years = [2024]
    months = _parse_months(text)
    return [SliceSpec(year=y, month=m) for y in years for m in months]


def expand_specs(specs: Iterable[SliceSpec]) -> list[SliceSpec]:
    return list(specs)


def _parse_year_range(text: str) -> list[int]:
    import re

    m = re.search(r"Years:\s*(\d{4})\s*[–\-]\s*(\d{4})", text, re.I)
    if m:
        return list(range(int(m.group(1)), int(m.group(2)) + 1))
    m = re.search(r"Years:\s*(\d{4})", text, re.I)
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
