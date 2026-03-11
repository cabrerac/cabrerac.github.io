#!/usr/bin/env python3
"""
PDF to Markdown — extract paper content for LLM use

Reads a PDF and writes a Markdown file with extracted text and structure.
Use --llm to use pymupdf4llm (tables, lists, better structure); otherwise
uses PyMuPDF with simple heading inference.

Example:
  python scripts/pdf_to_markdown/pdf_to_markdown.py paper.pdf output.md
  python scripts/pdf_to_markdown/pdf_to_markdown.py paper.pdf -o notes/paper.md
  python scripts/pdf_to_markdown/pdf_to_markdown.py paper.pdf --llm -o paper.md
"""

import argparse
import sys
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    print(
        "Error: PyMuPDF is required. Install with: pip install PyMuPDF",
        file=sys.stderr,
    )
    sys.exit(1)


def extract_markdown_pymupdf(pdf_path: Path) -> str:
    """Extract text from PDF with simple structure (headings vs body) as Markdown."""
    doc = fitz.open(pdf_path)
    lines_out = []
    # Collect font sizes to infer body vs heading
    sizes_seen: list[float] = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        blocks = page.get_text("dict", flags=fitz.TEXT_PRESERVE_WHITESPACE)["blocks"]

        for block in blocks:
            for line in block.get("lines", []):
                line_text_parts = []
                line_size = None
                for span in line.get("spans", []):
                    text = (span.get("text") or "").strip()
                    if not text:
                        continue
                    line_text_parts.append(text)
                    s = span.get("size")
                    if s is not None:
                        line_size = s if line_size is None else max(line_size, s)
                if not line_text_parts:
                    continue
                text = " ".join(line_text_parts).strip()
                if not text:
                    continue
                if line_size is not None:
                    sizes_seen.append(line_size)

                # Heuristic: short line and larger than typical body → heading
                body_size = (
                    sum(sizes_seen) / len(sizes_seen) if len(sizes_seen) > 5 else 11.0
                )
                is_heading = (
                    line_size is not None
                    and line_size > body_size * 1.15
                    and len(text) < 200
                )
                if is_heading:
                    lines_out.append("")
                    lines_out.append(f"## {text}")
                    lines_out.append("")
                else:
                    lines_out.append(text)

        if page_num < len(doc) - 1:
            lines_out.append("")
            lines_out.append("---")
            lines_out.append("")
            lines_out.append(f"*Page {page_num + 2}*")
            lines_out.append("")
    doc.close()

    # Normalize: single newline between paragraphs, no leading/trailing junk
    combined = "\n".join(lines_out)
    paragraphs = [p.strip() for p in combined.split("\n\n") if p.strip()]
    return "\n\n".join(paragraphs).strip() + "\n"


def extract_markdown_llm(pdf_path: Path) -> str:
    """Extract PDF to Markdown using pymupdf4llm (tables, lists, structure)."""
    try:
        import pymupdf4llm
    except ImportError:
        print(
            "Error: pymupdf4llm is required for --llm. Install with: pip install pymupdf4llm",
            file=sys.stderr,
        )
        sys.exit(1)
    md = pymupdf4llm.to_markdown(str(pdf_path))
    if isinstance(md, bytes):
        return md.decode("utf-8", errors="replace")
    return md


def extract_markdown(pdf_path: Path, use_llm: bool) -> str:
    """Extract PDF to Markdown; use_llm=True for pymupdf4llm, else PyMuPDF."""
    if use_llm:
        return extract_markdown_llm(pdf_path)
    return extract_markdown_pymupdf(pdf_path)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract PDF content to Markdown for LLM use (e.g. chat with the paper)."
    )
    parser.add_argument(
        "pdf_path",
        type=Path,
        help="Path to the PDF file",
    )
    parser.add_argument(
        "output_path",
        type=Path,
        nargs="?",
        default=None,
        help="Path for the output Markdown file (default: same name as PDF with .md)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        dest="output_path_opt",
        help="Path for the output Markdown file (alternative to positional)",
    )
    parser.add_argument(
        "--llm",
        action="store_true",
        help="Use pymupdf4llm for extraction (tables, lists, better structure). Requires: pip install pymupdf4llm",
    )
    args = parser.parse_args()

    pdf_path = args.pdf_path.resolve()
    if not pdf_path.exists():
        print(f"Error: PDF not found: {pdf_path}", file=sys.stderr)
        sys.exit(1)
    if not pdf_path.suffix.lower() == ".pdf":
        print("Warning: file does not have .pdf extension.", file=sys.stderr)

    output_path = args.output_path_opt or args.output_path
    if output_path is None:
        output_path = pdf_path.with_suffix(".md")
    output_path = output_path.resolve()

    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        md_content = extract_markdown(pdf_path, use_llm=args.llm)
    except Exception as e:
        print(f"Error extracting PDF: {e}", file=sys.stderr)
        sys.exit(1)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(md_content)

    print(f"Wrote {len(md_content)} characters to {output_path}")


if __name__ == "__main__":
    main()
