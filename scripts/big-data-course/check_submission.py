#!/usr/bin/env python3
"""
Semi-automatic pre-check for L1 PDF submissions (project requirements + reflection).

Extracts text with scripts/pdf_to_markdown, then applies section/keyword rules.
Does not grade substance — flags missing structure before instructor marking.

Examples:
  python scripts/big-data-course/check_submission.py project_requirements grupo1.pdf
  python scripts/big-data-course/check_submission.py reflection_l1 maria.pdf -o out.md
  python scripts/big-data-course/check_submission.py reflection_week_3 entrega.pdf -o out.md --show-r6
  python scripts/big-data-course/check_submission.py reflection_week_3 entrega.md --show-r6
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
    "Requerimientos del proyecto",
    "Objetivos",
    "Subconjunto de datos",
    "Preocupación ética",
    "Mecanismos de ética",
    "Roles y plan de contribución",
    "Pipeline del proyecto",
    "Rotación de liderazgo",
    "Modelo canvas del proyecto",
]

REFLECTION_WEEK_1_SECTIONS = [
    "Metadatos",
    "R1 Proceso",
    "R2 Justificación",
    "R3 Enlace",
    "R4 Ética",
    "R5 Uso de IA",
    "R6 Retroalimentación",
]

REFLECTION_WEEK_2_SECTIONS = REFLECTION_WEEK_1_SECTIONS
REFLECTION_WEEK_3_SECTIONS = REFLECTION_WEEK_1_SECTIONS
REFLECTION_SEMANA_1_SECTIONS = REFLECTION_WEEK_1_SECTIONS
REFLECTION_L1_SECTIONS = REFLECTION_WEEK_1_SECTIONS

# Heuristic phrases common in generic / LLM-assisted Spanish prose (not proof of misconduct).
AI_STYLE_PHRASES = (
    "cabe destacar",
    "es importante mencionar",
    "en este sentido",
    "de manera significativa",
    "sin lugar a dudas",
    "resulta fundamental",
    "juega un papel",
    "desempeña un papel",
    "en el contexto de",
    "es crucial",
    "es esencial",
    "es fundamental",
    "facilitar la comprensión",
    "facilitar la toma de decisiones",
    "herramienta de apoyo",
    "de manera crítica y autónoma",
    "se puede observar",
    "contribuyen a una mayor",
    "mayor transparencia",
    "visión más clara",
    "uno de los aspectos más valiosos",
    "la integración entre",
    "permite interpretar",
    "basada en datos",
    "ciclo completo",
    "garantizar la calidad",
    "garantizar consistencia",
)

AI_STYLE_REGEXES: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "Generic reading glue (\"la relación entre … se entiende\")",
        re.compile(
            r"la relaci[oó]n entre .{10,140} se entiende",
            flags=re.IGNORECASE | re.DOTALL,
        ),
    ),
    (
        "Template bridge (\"esto se refleja en la necesidad de\")",
        re.compile(r"esto se refleja en la necesidad de", flags=re.IGNORECASE),
    ),
    (
        "Passive-only process narration (>=5 \"se <verbo>\" without yo/nosotros)",
        re.compile(
            r"\bse (?:implement|desarroll|realiz|consolid|aplic|obtuv|gener)\w+\b",
            flags=re.IGNORECASE,
        ),
    ),
)

REFLECTION_SECTION_HEADINGS = (
    ("R1", re.compile(r"R1\s+Proceso", re.IGNORECASE)),
    ("R2", re.compile(r"R2\s+Justificaci", re.IGNORECASE)),
    ("R3", re.compile(r"R3\s+Enlace", re.IGNORECASE)),
    ("R4", re.compile(r"R4\s+[ÉE]tica", re.IGNORECASE)),
    ("R5", re.compile(r"R5\s+Uso", re.IGNORECASE)),
    ("R6", re.compile(r"R6\s+Retroalimentaci", re.IGNORECASE)),
)

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


def split_reflection_sections(text: str) -> dict[str, str]:
    """Split reflection body into R1–R6 chunks (best-effort on PDF extracts)."""
    hits: list[tuple[int, str]] = []
    for key, pattern in REFLECTION_SECTION_HEADINGS:
        match = pattern.search(text)
        if match:
            hits.append((match.start(), key))
    if not hits:
        return {}
    hits.sort(key=lambda item: item[0])
    sections: dict[str, str] = {}
    for idx, (start, key) in enumerate(hits):
        end = hits[idx + 1][0] if idx + 1 < len(hits) else len(text)
        chunk = text[start:end].strip()
        # Drop the heading line / prompt echo when possible.
        chunk = re.sub(r"^R[1-6][^\n]*\n?", "", chunk, count=1, flags=re.IGNORECASE)
        chunk = re.sub(r"^¿[^\n]+\?\s*", "", chunk, count=1)
        chunk = re.sub(
            r"^No se califica[^\n]*\n?",
            "",
            chunk,
            count=1,
            flags=re.IGNORECASE,
        )
        sections[key] = chunk.strip()
    return sections


def reflection_body_r1_r5(text: str) -> str:
    sections = split_reflection_sections(text)
    if sections:
        return "\n\n".join(sections.get(k, "") for k in ("R1", "R2", "R3", "R4", "R5")).strip()
    return text


def extract_r6_feedback(text: str) -> str:
    return split_reflection_sections(text).get("R6", "").strip()


def check_ai_generated_style(text: str, *, scope_r1_r5_only: bool = True) -> list[str]:
    """
    Heuristic red flags for generic or LLM-polished prose.
    Informational only — instructor still judges substance and R5 declarations.
    """
    body = reflection_body_r1_r5(text) if scope_r1_r5_only else text
    if not body.strip():
        return ["Could not isolate R1–R5 body for AI-style scan."]

    flags: list[str] = []
    norm = _normalize(body)
    phrase_hits = [p for p in AI_STYLE_PHRASES if p in norm]
    if len(phrase_hits) >= 4:
        sample = ", ".join(f'"{p}"' for p in phrase_hits[:5])
        extra = f" (+{len(phrase_hits) - 5} more)" if len(phrase_hits) > 5 else ""
        flags.append(
            f"Generic phrase cluster ({len(phrase_hits)} hits): {sample}{extra}."
        )
    elif len(phrase_hits) >= 2:
        flags.append(
            "Some generic phrases: "
            + ", ".join(f'"{p}"' for p in phrase_hits)
            + "."
        )

    for label, pattern in AI_STYLE_REGEXES:
        matches = pattern.findall(body)
        if label.startswith("Passive-only"):
            first_person = len(
                re.findall(
                    r"\b(?:yo|mi|mis|mí|nosotros|nuestro|nuestra)\b",
                    body,
                    flags=re.IGNORECASE,
                )
            )
            if len(matches) >= 5 and first_person < 4:
                flags.append(
                    f"{label}: {len(matches)} passive constructions; "
                    f"only {first_person} first-person markers."
                )
        elif matches:
            flags.append(f"{label} detected.")

    wc = _word_count(body)
    first_person = len(
        re.findall(
            r"\b(?:yo|mi|mis|mí|nosotros|nuestro|nuestra)\b",
            body,
            flags=re.IGNORECASE,
        )
    )
    if wc >= 500 and first_person < 6:
        flags.append(
            f"Low first-person voice in R1–R5 ({first_person} markers / {wc} words); "
            "expect concrete 'yo' + notebook specifics."
        )

    r2 = split_reflection_sections(text).get("R2", "")
    if r2:
        has_metric_numbers = bool(
            re.search(
                r"(?:r\s*[²2]|mae|coeficiente).{0,40}\d|\d.{0,40}(?:r\s*[²2]|mae)",
                r2,
                flags=re.IGNORECASE,
            )
        )
        if not has_metric_numbers and _word_count(r2) >= 80:
            flags.append(
                "R2 mentions metrics but no numeric R² / MAE / coefficient values from the notebook."
            )

    r5 = split_reflection_sections(text).get("R5", "")
    if r5:
        tool_named = bool(
            re.search(
                r"\b(?:chatgpt|copilot|gemini|claude|gpt|notebooklm|deepseek)\b",
                r5,
                flags=re.IGNORECASE,
            )
        )
        if not tool_named and _word_count(r5) >= 40:
            if re.search(
                r"herramientas de inteligencia artificial|herramientas de ia",
                r5,
                flags=re.IGNORECASE,
            ):
                flags.append(
                    "R5 cites AI use generically but names no specific tool (ChatGPT, Copilot, …)."
                )

    return flags


def check_project_requirements(text: str) -> tuple[bool, list[str]]:
    issues: list[str] = []
    missing = _missing_sections(text, PROJECT_REQUIREMENTS_SECTIONS)
    if missing:
        issues.append(f"Missing sections (fuzzy match): {', '.join(missing)}")
    norm = _normalize(text)
    if not any(a in norm for a in ARCHETYPES):
        issues.append("Archetype not detected (asignación / riesgo / monitoreo).")
    if not re.search(r"\bs[1-4]\b", norm):
        issues.append("Weekly leadership rotation (S1–S4) not detected.")
    wc = _word_count(text)
    if wc < 280:
        issues.append(f"Word count low ({wc}); target ~350–600 plus figure caption.")
    mech = re.search(
        r"mecanismos de (?:ética|etica) y gobernanza",
        norm,
    )
    if not mech:
        issues.append("Section 7 (Mecanismos de ética y gobernanza) not detected.")
    elif _word_count(text[mech.start() : min(mech.start() + 900, len(text))]) < 25:
        issues.append("Section 7: list concrete mitigation mechanisms (too short).")
    return len(issues) == 0, issues


def check_reflection_week_1(text: str) -> tuple[bool, list[str]]:
    issues: list[str] = []
    missing = _missing_sections(text, REFLECTION_WEEK_1_SECTIONS)
    if missing:
        issues.append(f"Missing sections: {', '.join(missing)}")
    wc = _word_count(text)
    if wc < 600:
        issues.append(f"Word count low ({wc}); target 700–1,000 (semana 1 = L1 + L2).")
    if wc > 1400:
        issues.append(f"Word count high ({wc}); target 700–1,000.")
    norm = _normalize(text)
    if not any(r in norm for r in ("zuboff", "boyd", "mittelstadt", "crawford")):
        issues.append("No assigned reading cited in R4 (boyd, Zuboff, Mittelstadt).")
    if not any(
        k in norm
        for k in (
            "nube",
            "cloud",
            "edge",
            "borde",
            "batch",
            "lote",
            "access",
            "acceso",
            "overpass",
            "osm",
        )
    ):
        issues.append("No technical anchor (Access / architecture / OSM) detected.")
    return len(issues) == 0, issues


def check_reflection_week_2(text: str) -> tuple[bool, list[str]]:
    issues: list[str] = []
    missing = _missing_sections(text, REFLECTION_WEEK_2_SECTIONS)
    if missing:
        issues.append(f"Missing sections: {', '.join(missing)}")
    wc = _word_count(text)
    if wc < 600:
        issues.append(f"Word count low ({wc}); target 700–1,000 (R1–R5).")
    if wc > 1500:
        issues.append(f"Word count high ({wc}); target 700–1,000 (R1–R5).")
    norm = _normalize(text)
    if not any(r in norm for r in ("dwork", "zuboff", "armbrust")):
        issues.append("No assigned reading cited in R4 (Dwork / Zuboff / Armbrust).")
    if not any(
        k in norm
        for k in (
            "parquet",
            "particion",
            "partition",
            "mapreduce",
            "duckdb",
            "polars",
            "lakehouse",
            "harmon",
            "motor",
            "engine",
            "almacen",
            "storage",
            "proces",
        )
    ):
        issues.append("No L3/L4 technical anchor (storage / processing / engine) detected.")
    return len(issues) == 0, issues


def check_reflection_week_3(text: str) -> tuple[bool, list[str]]:
    issues: list[str] = []
    missing = _missing_sections(text, REFLECTION_WEEK_3_SECTIONS)
    if missing:
        issues.append(f"Missing sections: {', '.join(missing)}")
    wc = _word_count(reflection_body_r1_r5(text) or text)
    if wc < 600:
        issues.append(f"Word count low ({wc}); target 700–1,000 (R1–R5).")
    if wc > 1500:
        issues.append(f"Word count high ({wc}); target 700–1,000 (R1–R5).")
    norm = _normalize(text)
    if not any(r in norm for r in ("zaharia", "jarrahi")):
        issues.append("No assigned reading cited in R4 (Zaharia / Jarrahi).")
    if not any(
        k in norm
        for k in (
            "prefect",
            "regres",
            "regression",
            "r²",
            "r2",
            "mae",
            "extract",
            "aggregate",
            "validate",
            "validaci",
            "stream",
            "batch",
            "lote",
            "curated",
            "ingest",
            "tablero",
            "dashboard",
            "bitacora",
            "bitácora",
            "contrato",
            "audit",
        )
    ):
        issues.append(
            "No L5/L6 technical anchor (Prefect / regression / streaming / audit / dashboard) detected."
        )
    issues.extend(f"[AI-style] {flag}" for flag in check_ai_generated_style(text))
    return len([i for i in issues if not i.startswith("[AI-style]")]) == 0, issues


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


def _load_submission_text(path: Path, *, use_llm: bool) -> str:
    if path.suffix.lower() == ".md":
        return path.read_text(encoding="utf-8")
    return extract_markdown(path, use_llm=use_llm)


def _print_precheck(label: str, ok: bool, issues: list[str]) -> None:
    if ok:
        print(f"{label}_PRECHECK_OK")
    else:
        print(f"{label}_PRECHECK_FAIL")
    if not issues:
        return
    structural = [i for i in issues if not i.startswith("[AI-style]")]
    ai_flags = [i[len("[AI-style] "):] for i in issues if i.startswith("[AI-style]")]

    for issue in structural:
        print(f"  - {issue}")
    if ai_flags:
        print("Red flags (AI-style / generic prose):")
        for flag in ai_flags:
            print(f"  - {flag}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Pre-check L1 PDF submissions.")
    parser.add_argument(
        "kind",
        choices=(
            "project_requirements",
            "reflection_l1",
            "reflection_week_1",
            "reflection_week_2",
            "reflection_week_3",
            "reflection_semana_1",
        ),
        help="Which template rules to apply",
    )
    parser.add_argument(
        "pdf_path",
        type=Path,
        help="PDF to extract, or existing .md extract",
    )
    parser.add_argument("-o", "--output-md", type=Path, help="Save extracted markdown")
    parser.add_argument("--llm", action="store_true", help="Use pymupdf4llm extraction")
    parser.add_argument(
        "--show-r6",
        action="store_true",
        help="Print R6 student feedback (ungraded) after pre-check",
    )
    args = parser.parse_args()

    src_path = args.pdf_path.resolve()
    if not src_path.is_file():
        print(f"Error: not found: {src_path}", file=sys.stderr)
        sys.exit(1)

    if src_path.suffix.lower() == ".md":
        text = _load_submission_text(src_path, use_llm=args.llm)
    else:
        text = extract_markdown(src_path, use_llm=args.llm)
        if args.output_md:
            args.output_md.write_text(text, encoding="utf-8")
            print(f"Wrote extract: {args.output_md}")

    if args.kind == "project_requirements":
        ok, issues = check_project_requirements(text)
        label = "PROJECT_REQUIREMENTS"
    elif args.kind in ("reflection_week_1", "reflection_semana_1"):
        ok, issues = check_reflection_week_1(text)
        label = "REFLECTION_WEEK_1"
    elif args.kind == "reflection_week_2":
        ok, issues = check_reflection_week_2(text)
        label = "REFLECTION_WEEK_2"
    elif args.kind == "reflection_week_3":
        ok, issues = check_reflection_week_3(text)
        label = "REFLECTION_WEEK_3"
    else:
        ok, issues = check_reflection_l1(text)
        label = "REFLECTION_L1"

    _print_precheck(label, ok, issues)

    if args.show_r6 and args.kind.startswith("reflection"):
        r6 = extract_r6_feedback(text)
        print("")
        print("R6 (sin nota — retroalimentación del estudiante):")
        if r6:
            print(r6)
        else:
            print("  (no R6 section detected)")

    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
