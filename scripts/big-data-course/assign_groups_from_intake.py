#!/usr/bin/env python3
"""Summarise intake CSV for group stratification (instructor aid).

Does not auto-assign — prints tiers and English anchors for manual grouping.
Output YAML template: work-space/teaching/big-data/administration/groups-roster.yaml

Usage:
  python scripts/big-data-course/assign_groups_from_intake.py \\
    "work-space/teaching/big-data/planning/Udenar Big Data 2026 — Intake (Responses) - Form responses 1.csv"
"""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
DEFAULT_CSV = (
    REPO
    / "work-space/teaching/big-data/planning/Udenar Big Data 2026 — Intake (Responses) - Form responses 1.csv"
)


def _score_digit(text: str) -> int | None:
    if not text:
        return None
    m = re.search(r"(\d)", text.replace("=", " "))
    return int(m.group(1)) if m else None


def _eng_level(text: str) -> int:
    m = re.match(r"(\d)", (text or "").strip())
    return int(m.group(1)) if m else 0


def _tier(score: int | None) -> str:
    if score is None:
        return "unknown"
    if score <= 1:
        return "novice"
    if score <= 3:
        return "developing"
    if score <= 5:
        return "comfortable"
    return "strong"


def load_rows(path: Path) -> list[dict[str, str]]:
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def summarise(rows: list[dict[str, str]]) -> None:
    print(f"Responses: {len(rows)}\n")
    print(f"{'Name':32} {'Email':36} {'Diag':>4} {'Tier':12} {'Eng R/L':7} {'Python':22} Background")
    print("-" * 120)
    anchors: list[str] = []
    for r in rows:
        name = r["Nombre completo"].strip()
        email = r["Correo electrónico"].strip().replace(",com", ".com")
        diag_raw = (r.get("Score obtenido en el notebook diagnóstico.") or "").strip()
        diag = _score_digit(diag_raw)
        er = _eng_level(r["Inglés — lectura (textos técnicos)"])
        el = _eng_level(r["Inglés — comprensión auditiva (videos técnicos)"])
        if er >= 3 and el >= 3:
            anchors.append(name)
        print(
            f"{name[:32]:32} {email[:36]:36} {str(diag or '?'):>4} "
            f"{_tier(diag):12} {er}/{el:<5} {r['Experiencia programando en Python'][:22]:22} "
            f"{r['Título universitario más alto y área'][:28]}"
        )
    print(f"\nEnglish anchors (reading≥3 and listening≥3): {len(anchors)}")
    for a in anchors:
        print(f"  - {a}")
    print("\nTarget: 5 groups, 4+4+4+4+3 for 19 students (intake-form-spec.md).")
    print("Edit administration/groups-roster.yaml after stratifying.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarise intake CSV for grouping.")
    parser.add_argument("csv", nargs="?", type=Path, default=DEFAULT_CSV)
    args = parser.parse_args()
    if not args.csv.exists():
        raise SystemExit(f"CSV not found: {args.csv}")
    summarise(load_rows(args.csv))


if __name__ == "__main__":
    main()
