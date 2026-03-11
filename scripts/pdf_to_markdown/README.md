# PDF to Markdown

Extract text from a PDF paper into a Markdown file for use as context with an LLM (e.g. chat with the paper while reading).

## Requirements

- Python 3.10+
- **PyMuPDF** (default backend): `pip install PyMuPDF`
- **pymupdf4llm** (optional, for `--llm`): `pip install pymupdf4llm` — better tables, lists, and structure

## Usage

```bash
# Default: PyMuPDF extraction (headings from font size, page markers)
python scripts/pdf_to_markdown/pdf_to_markdown.py path/to/paper.pdf

# Use pymupdf4llm for richer markdown (tables, lists, structure)
python scripts/pdf_to_markdown/pdf_to_markdown.py paper.pdf --llm -o paper.md

# Explicit output path (with or without --llm)
python scripts/pdf_to_markdown/pdf_to_markdown.py paper.pdf output.md
python scripts/pdf_to_markdown/pdf_to_markdown.py paper.pdf -o notes/paper.md
```

## Options

| Option | Description |
|-------|-------------|
| `-o`, `--output` | Output Markdown path (alternative to positional). |
| `--llm` | Use **pymupdf4llm** for extraction (requires `pip install pymupdf4llm`). Produces markdown with tables, lists, and improved structure. |

## Behaviour

- **Without `--llm`**: PyMuPDF extracts text; lines with larger font size become `##` headings; page breaks are marked with `---` and `*Page N*`.
- **With `--llm`**: pymupdf4llm extracts with layout awareness: headers, bold/italic, lists, tables, multi-column order. No page markers (pymupdf4llm returns a single flow).
- Output is UTF-8 Markdown; paste or feed it into your LLM as context.
