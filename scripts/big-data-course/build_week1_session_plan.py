#!/usr/bin/env python3
"""Build Week 1 session plan PDF from course/week-1/week-1-session-plan-es.md.

Outputs (canonical for the site):
  assets/documents/26-udenar-big-data/week-1-session-plan-es.pdf

Mirror:
  work-space/teaching/big-data/course/week-1/week-1-session-plan-es.pdf

Regenerate after editing the markdown source:
  python scripts/big-data-course/build_week1_session_plan.py
"""

from __future__ import annotations

import html
import re
from pathlib import Path

import pymupdf as fitz

REPO = Path(__file__).resolve().parents[2]
COURSE = "26-udenar-big-data"
SOURCE = REPO / "work-space/teaching/big-data/course/week-1/week-1-session-plan-es.md"
ASSETS_PDF = REPO / "assets/documents" / COURSE / "week-1-session-plan-es.pdf"
MIRROR_PDF = SOURCE.with_suffix(".pdf")

CSS = """
body { font-family: Helvetica, Arial, sans-serif; font-size: 10.5pt; line-height: 1.35; }
h1 { font-size: 17pt; margin-bottom: 4pt; }
h2 { font-size: 12.5pt; margin-top: 14pt; margin-bottom: 6pt; color: #1a1a1a; }
p { margin: 0 0 8pt 0; }
ul { margin: 0 0 8pt 0; padding-left: 18pt; }
li { margin-bottom: 4pt; }
table { border-collapse: collapse; width: 100%; margin: 8pt 0 12pt 0; font-size: 10pt; }
th, td { border: 1px solid #bbb; padding: 5pt 6pt; vertical-align: top; }
th { background: #f0f0f0; font-weight: bold; }
.meta { color: #333; margin-bottom: 10pt; }
code { font-family: Consolas, monospace; font-size: 9pt; }
a { color: #1155cc; }
hr { border: none; border-top: 1px solid #ccc; margin: 12pt 0; }
"""


def _inline(text: str) -> str:
    text = html.escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        r'<a href="\2">\1</a>',
        text,
    )
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    return text


def _parse_table(lines: list[str]) -> str:
    rows = [line.strip().strip("|") for line in lines if line.strip()]
    if len(rows) < 2:
        return ""
    header = [c.strip() for c in rows[0].split("|")]
    body_rows = []
    for row in rows[2:]:
        cells = [c.strip() for c in row.split("|")]
        if len(cells) == len(header):
            body_rows.append(cells)
    parts = ["<table><thead><tr>"]
    parts.extend(f"<th>{_inline(h)}</th>" for h in header)
    parts.append("</tr></thead><tbody>")
    for cells in body_rows:
        parts.append("<tr>")
        parts.extend(f"<td>{_inline(c)}</td>" for c in cells)
        parts.append("</tr>")
    parts.append("</tbody></table>")
    return "".join(parts)


def markdown_to_html(md: str) -> str:
    lines = md.splitlines()
    parts: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue
        if stripped == "---":
            parts.append("<hr/>")
            i += 1
            continue
        if stripped.startswith("# "):
            parts.append(f"<h1>{_inline(stripped[2:])}</h1>")
            i += 1
            continue
        if stripped.startswith("## "):
            parts.append(f"<h2>{_inline(stripped[3:])}</h2>")
            i += 1
            continue
        if stripped.startswith("```"):
            block = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                block.append(html.escape(lines[i]))
                i += 1
            if i < len(lines):
                i += 1
            parts.append(f"<p><code>{'<br/>'.join(block)}</code></p>")
            continue
        if stripped.startswith("|"):
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i])
                i += 1
            parts.append(_parse_table(table_lines))
            continue
        if stripped.startswith("- "):
            parts.append("<ul>")
            while i < len(lines) and lines[i].strip().startswith("- "):
                parts.append(f"<li>{_inline(lines[i].strip()[2:])}</li>")
                i += 1
            parts.append("</ul>")
            continue
        if stripped.startswith("*") and stripped.endswith("*") and not stripped.startswith("**"):
            parts.append(f'<p class="meta"><em>{_inline(stripped.strip("*"))}</em></p>')
            i += 1
            continue

        para = [stripped]
        i += 1
        while i < len(lines) and lines[i].strip() and not lines[i].startswith("#"):
            if lines[i].strip().startswith(("- ", "|", "```", "---")):
                break
            para.append(lines[i].strip())
            i += 1
        parts.append(f"<p>{_inline(' '.join(para))}</p>")

    return f"<body>{''.join(parts)}</body>"


def _write_pdf(path: Path, body_html: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    story = fitz.Story(html=body_html, user_css=CSS)
    mediabox = fitz.paper_rect("a4")
    where = mediabox + (45, 45, -45, -45)
    writer = fitz.DocumentWriter(str(path))
    try:
        more = 1
        while more:
            device = writer.begin_page(mediabox)
            more, _filled = story.place(where)
            story.draw(device, None)
            writer.end_page()
    finally:
        writer.close()


def build() -> Path:
    if not SOURCE.is_file():
        raise FileNotFoundError(SOURCE)
    md = SOURCE.read_text(encoding="utf-8")
    # Drop instructor-only "Regenerar este PDF" section from student PDF
    md = md.split("\n## Regenerar este PDF")[0].strip() + "\n"
    body_html = markdown_to_html(md)
    _write_pdf(ASSETS_PDF, body_html)
    MIRROR_PDF.write_bytes(ASSETS_PDF.read_bytes())
    return ASSETS_PDF


if __name__ == "__main__":
    out = build()
    print(f"Wrote {out}")
    print(f"Mirror {MIRROR_PDF}")
