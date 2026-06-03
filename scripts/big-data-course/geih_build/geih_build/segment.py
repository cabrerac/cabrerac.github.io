"""Segment queries — expand survey years to DANE file lists."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from geih_build.dane_catalog import CatalogFile, catalog_id_for_year, list_catalog_downloads


@dataclass(frozen=True)
class SegmentQuery:
    """Download all files listed on each survey-year catalog."""

    years: tuple[int, ...]

    def expand_files(
        self,
        *,
        registry_path: Path = Path("catalog_registry.json"),
    ) -> list[CatalogFile]:
        files: list[CatalogFile] = []
        seen: set[int] = set()
        for year in self.years:
            catalog_id = catalog_id_for_year(year, registry_path=registry_path)
            for item in list_catalog_downloads(catalog_id):
                if item.file_id in seen:
                    continue
                seen.add(item.file_id)
                files.append(item)
        return sorted(files, key=lambda f: (f.survey_year or 0, f.filename.lower()))


@dataclass(frozen=True)
class AccessPlan:
    name: str
    segments: tuple[SegmentQuery, ...]
    dest: Path = Path("data/raw")

    def all_files(
        self,
        *,
        registry_path: Path = Path("catalog_registry.json"),
    ) -> list[CatalogFile]:
        out: list[CatalogFile] = []
        seen: set[int] = set()
        for seg in self.segments:
            for item in seg.expand_files(registry_path=registry_path):
                if item.file_id in seen:
                    continue
                seen.add(item.file_id)
                out.append(item)
        return sorted(out, key=lambda f: (f.survey_year or 0, f.filename.lower()))


def load_access_plan(path: Path) -> AccessPlan:
    if path.suffix in {".yaml", ".yml"}:
        raw = _load_yaml(path)
    else:
        raw = json.loads(path.read_text(encoding="utf-8"))
    segments = []
    for row in raw.get("segments", []):
        years = row.get("years")
        if isinstance(years, int):
            years = [years]
        segments.append(SegmentQuery(years=tuple(years)))
    dest = Path(raw.get("dest", "data/raw"))
    return AccessPlan(name=raw.get("name", path.stem), segments=tuple(segments), dest=dest)


def _load_yaml(path: Path) -> dict[str, Any]:
    try:
        import yaml  # type: ignore
    except ImportError as exc:
        raise ImportError(
            "PyYAML required for .yaml plans: pip install pyyaml "
            "or use JSON access plan."
        ) from exc
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def write_plan_json(plan: AccessPlan, path: Path) -> None:
    payload = {
        "name": plan.name,
        "dest": str(plan.dest),
        "segments": [{"years": list(s.years)} for s in plan.segments],
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
