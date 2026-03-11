# PDF to Markdown

Extract text from a PDF paper into a Markdown file for use as context with an LLM (e.g. chat with the paper while reading).

## Requirements

- Python 3.10+
- PyMuPDF: `pip install PyMuPDF`

## Usage

```bash
# Output to same name with .md (e.g. paper.pdf → paper.md)
python scripts/pdf_to_markdown/pdf_to_markdown.py path/to/paper.pdf

# Explicit output path
python scripts/pdf_to_markdown/pdf_to_markdown.py paper.pdf output.md

# Using -o
python scripts/pdf_to_markdown/pdf_to_markdown.py paper.pdf -o notes/paper.md
```

## Behaviour

- Text is extracted with basic structure: lines with larger font size are emitted as `##` headings.
- Page breaks are marked with `---` and `*Page N*` so you can refer to pages when chatting with the LLM.
- Output is UTF-8 Markdown; paste or feed it into your LLM as context.

## Optional: `pymupdf4llm`

For markdown tuned for LLMs (tables, lists, structure), you can use [pymupdf4llm](https://github.com/pymupdf/pymupdf4llm) and call it from a small wrapper, or switch this script to use it instead of raw PyMuPDF.
