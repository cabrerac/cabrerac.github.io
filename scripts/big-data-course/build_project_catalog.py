#!/usr/bin/env python3
"""Sync project catalog YAML from work-space to _data/ for L8 listing page.

Source (edit after opt-in ZIPs are approved):
  work-space/teaching/big-data/course/project/project-catalog.yaml

Output:
  _data/26-udenar-big-data-projects.yml

Then regenerate L8:
  python scripts/generate_content/generate_content.py 26-udenar-big-data/l8-final-project
"""

from __future__ import annotations

import argparse
from pathlib import Path

import yaml

from docx_build import REPO

SOURCE = REPO / "work-space/teaching/big-data/course/project/project-catalog.yaml"
DEST = REPO / "_data/26-udenar-big-data-projects.yml"


def load_catalog(path: Path) -> dict:
    if not path.exists():
        return {"projects": []}
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not data:
        return {"projects": []}
    if "projects" not in data:
        raise ValueError(f"{path}: expected top-level 'projects' list")
    return data


def write_catalog(data: dict, dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(
        yaml.dump(data, allow_unicode=True, sort_keys=False, default_flow_style=False),
        encoding="utf-8",
    )
    return dest


def main() -> None:
    parser = argparse.ArgumentParser(description="Build L8 project catalog data file")
    parser.add_argument(
        "--source",
        type=Path,
        default=SOURCE,
        help="YAML catalog source",
    )
    parser.add_argument(
        "--dest",
        type=Path,
        default=DEST,
        help="Jekyll data output",
    )
    args = parser.parse_args()
    data = load_catalog(args.source)
    out = write_catalog(data, args.dest)
    n = len(data.get("projects", []))
    print(f"Wrote {out} ({n} project(s))")


if __name__ == "__main__":
    main()
