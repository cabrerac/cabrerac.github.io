#!/usr/bin/env python3
"""Build instructor-only notebooks from work-space sources (never assets/notebooks/)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
INSTRUCTOR_WS = REPO_ROOT / "work-space" / "teaching" / "big-data" / "instructor"
NOTEBOOK_OUT = INSTRUCTOR_WS / "notebooks"

sys.path.insert(0, str(REPO_ROOT))

from scripts.generate_content.generate_content import ContentGenerator  # noqa: E402


def build_instructor_notebook(stem: str) -> Path:
    source = INSTRUCTOR_WS / f"{stem}.md"
    if not source.is_file():
        raise FileNotFoundError(source)

    gen = ContentGenerator(REPO_ROOT)
    meta = gen.lecture_metadata_from_file(source)
    if not meta.get("instructor_only"):
        raise ValueError(f"{source} must set instructor_only: true in front matter")

    course_code = meta.get("course_code", "26-udenar-big-data")
    course_metadata = gen.get_course_metadata(course_code)
    NOTEBOOK_OUT.mkdir(parents=True, exist_ok=True)
    gen.generate_notebook(source, NOTEBOOK_OUT, course_metadata)
    out = NOTEBOOK_OUT / f"{stem}.ipynb"
    print(f"Wrote instructor notebook: {out}")
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Build instructor-only Colab sources locally.")
    parser.add_argument(
        "notebook",
        nargs="?",
        default="week-2-group-solution",
        help="Notebook stem (default: week-2-group-solution)",
    )
    args = parser.parse_args()
    build_instructor_notebook(args.notebook)


if __name__ == "__main__":
    main()
