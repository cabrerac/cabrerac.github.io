#!/usr/bin/env python3
"""Build Week 2 session plan PDF from course/week-2/week-2-session-plan-es.md.

Outputs:
  assets/documents/26-udenar-big-data/week-2-session-plan-es.pdf
  work-space/teaching/big-data/course/week-2/week-2-session-plan-es.pdf
"""

from __future__ import annotations

import html
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
COURSE = "26-udenar-big-data"
SOURCE = REPO / "work-space/teaching/big-data/course/week-2/week-2-session-plan-es.md"
ASSETS_PDF = REPO / "assets/documents" / COURSE / "week-2-session-plan-es.pdf"
MIRROR_PDF = SOURCE.with_suffix(".pdf")

# Reuse renderer from week 1 builder
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_week1_session_plan import CSS, _write_pdf, markdown_to_html  # noqa: E402


def build() -> Path:
    if not SOURCE.is_file():
        raise FileNotFoundError(SOURCE)
    md = SOURCE.read_text(encoding="utf-8")
    md = md.split("\n## Regenerar este PDF")[0].strip() + "\n"
    body_html = markdown_to_html(md)
    _write_pdf(ASSETS_PDF, body_html)
    MIRROR_PDF.write_bytes(ASSETS_PDF.read_bytes())
    return ASSETS_PDF


if __name__ == "__main__":
    out = build()
    print(f"Wrote {out}")
    print(f"Mirror {MIRROR_PDF}")
