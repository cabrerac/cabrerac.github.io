#!/usr/bin/env python3
"""
Semi-automatic pre-check for L1 PDF submissions (project requirements + reflection).

Extracts text with scripts/pdf_to_markdown, then applies section/keyword rules.
Does not grade substance — flags missing structure before instructor marking.

Examples:
  python scripts/big-data-course/check_submission.py project_requirements grupo1.pdf
  python scripts/big-data-course/check_submission.py reflection_l1 maria.pdf -o out.md
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "scripts" / "pdf_to_markdown"))

from pdf_to_markdown import extract_markdown  # noqa: E402


PROJECT_REQUIREMENTS_SECTIONS = [
    "Metadatos del grupo",
    "Interesados",
    "Pregunta de decisión",
    "Subconjunto de datos",
    "Criterios de éxito",
    "Preocupación ética",
    "Roles y plan de contribución",
    "Pipeline del proyecto",
    "URL del Colab",
    "Rotación de escriba",
]

REFLECTION_L1_SECTIONS = [
    "Metadatos",
    "R1 Proceso",
    "R2 Justificación",
    "R3 Enlace",
    "R4 Ética",
    "R5 Uso de IA",
]

ARCHETYPES = (
    "asignación de recursos",
    "resource allocation",
    "riesgo",
    "early warning",
    "monitoreo",
    "monitoring",
)


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower())


def _word_count(text: str) -> int:
    return len(re.findall(r"\w+", text, flags=re.UNICODE))


def _missing_sections(text: str, markers: list[str]) -> list[str]:
    norm = _normalize(text)
    missing = []
    for m in markers:
        if _normalize(m) not in norm:
            missing.append(m)
    return missing


def check_project_requirements(text: str) -> tuple[bool, list[str]]:
    issues: list[str] = []
    missing = _missing_sections(text, PROJECT_REQUIREMENTS_SECTIONS)
    if missing:
        issues.append(f"Missing sections (fuzzy match): {', '.join(missing)}")
    norm = _normalize(text)
    if not any(a in norm for a in ARCHETYPES):
        issues.append("Archetype not detected (asignación / riesgo / monitoreo).")
    if "colab.research.google.com" not in norm and "drive.google.com" not in norm:
        issues.append("No Colab/Drive URL found.")
    if not re.search(r"\bl[1-6]\b", norm):
        issues.append("Scribe rotation (L1–L6) not detected.")
    wc = _word_count(text)
    if wc < 280:
        issues.append(f"Word count low ({wc}); target ~350–600 plus figure caption.")
    if "zuboff" not in norm and "boyd" not in norm:
        issues.append("No reading cited (Zuboff / boyd) in ethical section.")
    return len(issues) == 0, issues


def check_reflection_l1(text: str) -> tuple[bool, list[str]]:
    issues: list[str] = []
    missing = _missing_sections(text, REFLECTION_L1_SECTIONS)
    if missing:
        issues.append(f"Missing sections: {', '.join(missing)}")
    wc = _word_count(text)
    if wc < 450:
        issues.append(f"Word count low ({wc}); target 500–900.")
    if wc > 1200:
        issues.append(f"Word count high ({wc}); target 500–900.")
    norm = _normalize(text)
    if "zuboff" not in norm and "boyd" not in norm:
        issues.append("No reading cited (Zuboff / boyd).")
    if not any(
        k in norm
        for k in ("nube", "cloud", "edge", "borde", "batch", "lote", "interactiv")
    ):
        issues.append("Architecture trade-off (cloud/edge/batch) not detected.")
    return len(issues) == 0, issues


def main() -> None:
    parser = argparse.ArgumentParser(description="Pre-check L1 PDF submissions.")
    parser.add_argument(
        "kind",
        choices=("project_requirements", "reflection_l1"),
        help="Which template rules to apply",
    )
    parser.add_argument("pdf_path", type=Path)
    parser.add_argument("-o", "--output-md", type=Path, help="Save extracted markdown")
    parser.add_argument("--llm", action="store_true", help="Use pymupdf4llm extraction")
    args = parser.parse_args()

    pdf_path = args.pdf_path.resolve()
    if not pdf_path.is_file():
        print(f"Error: not found: {pdf_path}", file=sys.stderr)
        sys.exit(1)

    text = extract_markdown(pdf_path, use_llm=args.llm)
    if args.output_md:
        args.output_md.write_text(text, encoding="utf-8")
        print(f"Wrote extract: {args.output_md}")

    if args.kind == "project_requirements":
        ok, issues = check_project_requirements(text)
        label = "PROJECT_REQUIREMENTS"
    else:
        ok, issues = check_reflection_l1(text)
        label = "REFLECTION_L1"

    if ok:
        print(f"{label}_PRECHECK_OK")
    else:
        print(f"{label}_PRECHECK_FAIL")
        for issue in issues:
            print(f"  - {issue}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
