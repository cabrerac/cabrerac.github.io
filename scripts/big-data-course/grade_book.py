#!/usr/bin/env python3
"""Grade workbook for Udenar Big Data course.

Mark in CSV detail files; this script builds grades.xlsx (Excel formulas from
config.yaml) and updates Moodle calificaciones.csv exports.

Usage:
  python scripts/big-data-course/grade_book.py init
  python scripts/big-data-course/grade_book.py build
  python scripts/big-data-course/grade_book.py moodle
  python scripts/big-data-course/grade_book.py all
"""

from __future__ import annotations

import argparse
import csv
import math
import sys
from pathlib import Path
from typing import Any

import yaml

REPO = Path(__file__).resolve().parents[2]
DEFAULT_GRADING_DIR = REPO / "work-space/teaching/big-data/students-work/grading"
STUDENTS_WORK = REPO / "work-space/teaching/big-data/students-work"
GROUPS_ROSTER = REPO / "work-space/teaching/big-data/administration/groups-roster.yaml"
MOODLE_GRADE_COL = "Calificación"
MOODLE_FEEDBACK_COL = "Comentarios de retroalimentación"
MOODLE_EMAIL_COL = "Dirección de correo"
MOODLE_REFLECTION_W2 = STUDENTS_WORK / "week-2/reflection/calificaciones.csv"

try:
    from openpyxl import Workbook
    from openpyxl.utils import get_column_letter
except ImportError:  # pragma: no cover
    Workbook = None  # type: ignore[misc, assignment]
    get_column_letter = None  # type: ignore[misc, assignment]


def _require_openpyxl() -> None:
    if Workbook is None:
        print(
            "openpyxl is required: pip install openpyxl",
            file=sys.stderr,
        )
        sys.exit(1)


def load_config(grading_dir: Path) -> dict[str, Any]:
    path = grading_dir / "config.yaml"
    with open(path, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    cfg["_grading_dir"] = grading_dir.resolve()
    return cfg


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.is_file():
        return [], []
    with open(path, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames or [])
        return fieldnames, list(reader)


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_moodle_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    """Write Moodle grading worksheet — UTF-8 BOM + quote fields with commas (e.g. 5,00)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=fieldnames,
            extrasaction="ignore",
            quoting=csv.QUOTE_MINIMAL,
        )
        writer.writeheader()
        writer.writerows(rows)


def load_groups_roster(path: Path) -> dict[str, str]:
    """Map normalised email → group id (G1–G5)."""
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    email_to_group: dict[str, str] = {}

    def norm(email: str) -> str:
        return email.strip().lower()

    for group_id, group in (data.get("groups") or {}).items():
        for member in group.get("members") or []:
            gid = group.get("group_id") or group_id
            for key in ("email", "form_email"):
                raw = member.get(key)
                if raw:
                    email_to_group[norm(raw)] = gid
    return email_to_group


def load_moodle_roster(path: Path) -> list[dict[str, str]]:
    _, rows = read_csv_rows(path)
    out: list[dict[str, str]] = []
    for row in rows:
        email = (row.get("Dirección de correo") or "").strip()
        if not email:
            continue
        out.append(
            {
                "email": email,
                "nombre": (row.get("Nombre completo") or "").strip(),
            }
        )
    return out


def build_roster(grading_dir: Path) -> list[dict[str, str]]:
    moodle_path = MOODLE_REFLECTION_W2
    if not moodle_path.is_file():
        moodle_path = STUDENTS_WORK / "week-1/reflection/calificaciones.csv"
    students = load_moodle_roster(moodle_path)
    email_to_group = load_groups_roster(GROUPS_ROSTER)
    roster: list[dict[str, str]] = []
    for s in students:
        email = s["email"]
        grupo = email_to_group.get(email.lower(), "")
        roster.append({"email": email, "nombre": s["nombre"], "grupo": grupo})
    roster.sort(key=lambda r: (r["grupo"], r["nombre"]))
    write_csv(grading_dir / "roster.csv", ["email", "nombre", "grupo"], roster)
    return roster


def reflection_headers(prefix: str = "") -> list[str]:
    return [f"{prefix}R{i}" for i in range(1, 6)]


def detail_fieldnames(cfg_entry: dict[str, Any]) -> list[str]:
    base = ["email", "nombre", "grupo"]
    ftype = cfg_entry["type"]
    if ftype == "reflection":
        prefix = cfg_entry.get("criteria_prefix", "")
        base.extend(reflection_headers(prefix))
    elif ftype == "group":
        base.extend(["N1", "N2", "N3"])
    elif ftype == "project":
        base.extend(["P1", "P2", "P3", "P4", "P5", "w3_N1", "w3_N2", "w3_N3"])
    base.append("notas")
    return base


def reflection_criteria_map(prefix: str = "") -> dict[str, str]:
    return {f"R{i}": f"{prefix}R{i}" for i in range(1, 6)}


def init_detail_file(grading_dir: Path, cfg_entry: dict[str, Any], roster: list[dict[str, str]]) -> None:
    path = grading_dir / cfg_entry["file"]
    if path.is_file():
        return
    fields = detail_fieldnames(cfg_entry)
    rows = [{f: "" for f in fields} for _ in roster]
    for i, student in enumerate(roster):
        for key in ("email", "nombre", "grupo"):
            rows[i][key] = student[key]
    write_csv(path, fields, rows)


def load_roster_rows(grading_dir: Path, cfg: dict[str, Any]) -> list[dict[str, str]]:
    roster_path = grading_dir / cfg["paths"]["roster"]
    if roster_path.is_file():
        _, rows = read_csv_rows(roster_path)
        return rows
    return build_roster(grading_dir)


def sync_detail_file(
    grading_dir: Path,
    cfg_entry: dict[str, Any],
    roster: list[dict[str, str]],
) -> tuple[int, int]:
    """Update nombre/grupo from roster. Returns (updated, added)."""
    path = grading_dir / cfg_entry["file"]
    fields = detail_fieldnames(cfg_entry)
    if not path.is_file():
        init_detail_file(grading_dir, cfg_entry, roster)
        return 0, len(roster)

    headers, rows = read_csv_rows(path)
    if not headers:
        init_detail_file(grading_dir, cfg_entry, roster)
        return 0, len(roster)

    roster_by_email = {r["email"].strip().lower(): r for r in roster if r.get("email")}
    existing_by_email: dict[str, dict[str, str]] = {}
    orphans: list[dict[str, str]] = []
    for row in rows:
        email = (row.get("email") or "").strip().lower()
        if email and email in roster_by_email:
            existing_by_email[email] = row
        elif email:
            orphans.append(row)

    updated = 0
    added = 0
    synced: list[dict[str, str]] = []
    for student in roster:
        email_key = student["email"].strip().lower()
        if email_key in existing_by_email:
            row = existing_by_email[email_key]
            changed = False
            for key in ("email", "nombre", "grupo"):
                if row.get(key) != student.get(key, ""):
                    row[key] = student.get(key, "")
                    changed = True
            if changed:
                updated += 1
            synced.append(row)
        else:
            row = {f: "" for f in fields}
            for key in ("email", "nombre", "grupo"):
                row[key] = student.get(key, "")
            synced.append(row)
            added += 1

    synced.extend(orphans)
    write_csv(path, headers, synced)
    return updated, added


def cmd_sync(grading_dir: Path) -> None:
    cfg = load_config(grading_dir)
    roster = load_roster_rows(grading_dir, cfg)
    total_updated = 0
    total_added = 0
    for entry in cfg["detail_files"]:
        updated, added = sync_detail_file(grading_dir, entry, roster)
        total_updated += updated
        total_added += added
        if updated or added:
            print(f"  {entry['file']}: {updated} updated, {added} added")
    print(f"Synced roster -> detail CSVs ({len(roster)} students)")


def cmd_init(grading_dir: Path) -> None:
    grading_dir.mkdir(parents=True, exist_ok=True)
    cfg = load_config(grading_dir)
    roster_path = grading_dir / cfg["paths"]["roster"]
    if roster_path.is_file():
        roster = load_roster_rows(grading_dir, cfg)
        print(f"Using existing roster: {roster_path}")
    else:
        roster = build_roster(grading_dir)
    for entry in cfg["detail_files"]:
        init_detail_file(grading_dir, entry, roster)
        sync_detail_file(grading_dir, entry, roster)
    print(f"Initialized grading dir: {grading_dir}")
    print(f"  roster: {len(roster)} students")
    print("  detail CSV templates created (existing files left unchanged)")


def col_letter(idx: int) -> str:
    return get_column_letter(idx)


def header_index(headers: list[str]) -> dict[str, int]:
    return {h: i + 1 for i, h in enumerate(headers)}


def cell_ref(col_idx: int, row: int) -> str:
    return f"{col_letter(col_idx)}{row}"


def build_weighted_sum(
    criteria: dict[str, float],
    col_map: dict[str, int],
    row: int,
    column_names: dict[str, str] | None = None,
) -> str:
    parts = []
    for name, weight in criteria.items():
        col_name = (column_names or {}).get(name, name)
        parts.append(f"{weight}*{cell_ref(col_map[col_name], row)}")
    return "+".join(parts)


def build_sum(criteria: list[str], col_map: dict[str, int], row: int) -> str:
    refs = [cell_ref(col_map[name], row) for name in criteria]
    return "+".join(refs)


def excel_formula_for_mark(
    formula_key: str,
    formulas_cfg: dict[str, Any],
    col_map: dict[str, int],
    row: int,
    criteria_map: dict[str, str] | None = None,
) -> str:
    spec = formulas_cfg[formula_key]
    template = spec["excel"]

    if "{sum}" in template:
        criteria = spec["criteria"]
        names = list(criteria)
        col_names = [criteria_map.get(n, n) if criteria_map else n for n in names]
        sum_expr = build_sum(col_names, col_map, row)
        return template.replace("{sum}", sum_expr)

    if "{weighted_sum}" in template:
        criteria = spec["criteria"]
        wsum = build_weighted_sum(criteria, col_map, row, criteria_map)
        return template.replace("{weighted_sum}", wsum)

    return template


def sheet_headers(ws) -> list[str]:
    return [ws.cell(1, c).value for c in range(1, ws.max_column + 1)]


def write_sheet_from_csv(ws, headers: list[str], rows: list[dict[str, str]]) -> None:
    ws.append(headers)
    for row in rows:
        ws.append([row.get(h, "") for h in headers])


def add_mark_formulas(
    ws,
    headers: list[str],
    mark_column: str,
    formula_key: str,
    formulas_cfg: dict[str, Any],
    criteria_map: dict[str, str] | None = None,
    data_start_row: int = 2,
) -> None:
    if mark_column not in headers:
        headers = headers + [mark_column]
        ws.cell(row=1, column=len(headers), value=mark_column)
    col_map = header_index(headers)
    mark_col = col_map[mark_column]
    n_rows = ws.max_row
    for row in range(data_start_row, n_rows + 1):
        formula = excel_formula_for_mark(
            formula_key, formulas_cfg, col_map, row, criteria_map
        )
        ws.cell(row=row, column=mark_col, value=formula)


def vlookup_formula(key_col: str, key_row: int, sheet: str, return_col: int, n_rows: int) -> str:
    """VLOOKUP on email column; return_col is 1-based index in target sheet."""
    key_ref = f"{key_col}{key_row}"
    last_col = col_letter(return_col)
    return f'=IFERROR(VLOOKUP({key_ref},\'{sheet}\'!$A:${last_col},{return_col},FALSE),"")'


def consolidado_col_letter(headers: list[str], name: str) -> str:
    return col_letter(headers.index(name) + 1)


def build_consolidado_sheet(
    wb: Workbook,
    cfg: dict[str, Any],
    sheet_mark_cols: dict[str, dict[str, int]],
) -> None:
    cons_cfg = cfg["consolidado"]
    ws_name = cons_cfg["sheet"]
    ws = wb.create_sheet(ws_name)

    roster_path = cfg["_grading_dir"] / cfg["paths"]["roster"]
    _, roster = read_csv_rows(roster_path)
    columns = cons_cfg["columns"]
    headers = [c["header"] for c in columns]
    ws.append(headers)
    col_idx = header_index(headers)

    formulas_cfg = cfg["formulas"]
    n_students = len(roster)
    for i, student in enumerate(roster):
        row_num = i + 2
        row_vals: list[Any] = [""] * len(headers)
        for j, col in enumerate(columns):
            if col.get("source") == "roster":
                row_vals[j] = student.get(col["field"], "")
        ws.append(row_vals)

    for i in range(n_students):
        row_num = i + 2
        for j, col in enumerate(columns):
            header = col["header"]
            if col.get("ref"):
                ref = col["ref"]
                sheet = ref["sheet"]
                column = ref["column"]
                return_col = sheet_mark_cols[sheet][column]
                formula = vlookup_formula("A", row_num, sheet, return_col, n_students)
                ws.cell(row=row_num, column=j + 1, value=formula)
            elif col.get("formula"):
                fkey = col["formula"]
                args = col.get("args", {})
                template = formulas_cfg[fkey]["excel"]
                expr = template
                for arg_name, cons_header in args.items():
                    ref = f"{consolidado_col_letter(headers, cons_header)}{row_num}"
                    expr = expr.replace(f"{{{arg_name}}}", ref)
                ws.cell(row=row_num, column=j + 1, value=expr)


def cmd_build(grading_dir: Path) -> None:
    _require_openpyxl()
    cfg = load_config(grading_dir)
    formulas_cfg = cfg["formulas"]
    wb = Workbook()
    wb.remove(wb.active)

    sheet_mark_cols: dict[str, dict[str, int]] = {}

    # Roster sheet
    roster_path = grading_dir / cfg["paths"]["roster"]
    roster_headers, roster_rows = read_csv_rows(roster_path)
    ws_roster = wb.create_sheet("roster")
    write_sheet_from_csv(ws_roster, roster_headers, roster_rows)

    # Config reference sheet
    ws_cfg = wb.create_sheet("config_ref")
    ws_cfg.append(["key", "value"])
    ws_cfg.append(["course", cfg.get("course", "")])
    for fk, fv in formulas_cfg.items():
        ws_cfg.append([f"formula:{fk}", fv.get("description", "")])
        ws_cfg.append([f"formula:{fk}:excel", fv.get("excel", "")])

    for entry in cfg["detail_files"]:
        sheet_name = entry["sheet"]
        csv_path = grading_dir / entry["file"]
        headers, rows = read_csv_rows(csv_path)
        if not headers:
            print(f"Warning: empty or missing {csv_path}", file=sys.stderr)
            continue

        ws = wb.create_sheet(sheet_name)
        write_sheet_from_csv(ws, headers, rows)

        mark_col = entry["mark_column"]
        crit_map = None
        if entry.get("criteria_prefix") is not None:
            crit_map = reflection_criteria_map(entry.get("criteria_prefix", ""))
        add_mark_formulas(ws, headers, mark_col, entry["formula"], formulas_cfg, crit_map)

        for extra in entry.get("extra_marks") or []:
            extra_mark = extra["mark_column"]
            add_mark_formulas(
                ws,
                sheet_headers(ws),
                extra_mark,
                extra["formula"],
                formulas_cfg,
                criteria_map=extra.get("criteria_map"),
            )

        final_headers = sheet_headers(ws)
        sheet_mark_cols[sheet_name] = header_index(final_headers)

        # Moodle export sheet (copy of moodle csv if present)
        moodle_rel = entry.get("moodle_csv")
        if moodle_rel:
            moodle_path = (grading_dir / moodle_rel).resolve()
            if moodle_path.is_file():
                m_headers, m_rows = read_csv_rows(moodle_path)
                moodle_sheet = f"{sheet_name}_moodle"[:31]
                ws_m = wb.create_sheet(moodle_sheet)
                write_sheet_from_csv(ws_m, m_headers, m_rows)

        for extra in entry.get("extra_marks") or []:
            moodle_rel = extra.get("moodle_csv")
            if moodle_rel:
                moodle_path = (grading_dir / moodle_rel).resolve()
                if moodle_path.is_file():
                    m_headers, m_rows = read_csv_rows(moodle_path)
                    moodle_sheet = f"w3_group_moodle"[:31]
                    if moodle_sheet not in wb.sheetnames:
                        ws_m = wb.create_sheet(moodle_sheet)
                        write_sheet_from_csv(ws_m, m_headers, m_rows)

    build_consolidado_sheet(wb, cfg, sheet_mark_cols)

    out_path = grading_dir / cfg["paths"]["output_xlsx"]
    wb.save(out_path)
    print(f"Wrote {out_path} ({len(wb.sheetnames)} sheets)")


def parse_float(value: str) -> float | None:
    if value is None:
        return None
    s = str(value).strip()
    if not s:
        return None
    s = s.replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return None


def eval_mark_row(
    row: dict[str, str],
    formula_key: str,
    formulas_cfg: dict[str, Any],
    criteria_map: dict[str, str] | None = None,
) -> float | None:
    spec = formulas_cfg[formula_key]
    if formula_key == "reflection_mark":
        vals = []
        for name in spec["criteria"]:
            col = (criteria_map or {}).get(name, name)
            v = parse_float(row.get(col, ""))
            if v is None:
                return None
            vals.append(v)
        return 5.0 * sum(vals) / 15.0

    if formula_key in ("group_mark", "project_group_mark"):
        criteria = spec["criteria"]
        weighted = 0.0
        for name, weight in criteria.items():
            col = criteria_map.get(name, name) if criteria_map else name
            v = parse_float(row.get(col, ""))
            if v is None:
                return None
            weighted += weight * v
        return 5.0 * weighted / 3.0

    return None


def round_activity_mark(value: float, decimals: int = 1) -> float:
    """Round to `decimals` places; .05 in the next digit rounds up (4.75 -> 4.8)."""
    factor = 10**decimals
    return math.floor(value * factor + 0.5) / factor


def format_moodle_grade(value: float) -> str:
    rounded = round_activity_mark(value, decimals=1)
    text = f"{rounded:.2f}".replace(".", ",")
    return text


def collect_marks_and_feedback(
    rows: list[dict[str, str]],
    entry: dict[str, Any],
    formulas_cfg: dict[str, Any],
    crit_map: dict[str, str] | None,
) -> tuple[dict[str, float], dict[str, str]]:
    marks: dict[str, float] = {}
    feedback: dict[str, str] = {}
    for row in rows:
        email = (row.get("email") or "").strip().lower()
        if not email:
            continue
        mark = eval_mark_row(row, entry["formula"], formulas_cfg, crit_map)
        override = parse_float(row.get("mark_override", ""))
        if override is not None:
            marks[email] = override
        elif mark is not None:
            marks[email] = round_activity_mark(mark)
        notas = (row.get("notas") or "").strip()
        if notas:
            feedback[email] = notas
    return marks, feedback


def cmd_moodle(grading_dir: Path) -> None:
    cfg = load_config(grading_dir)
    formulas_cfg = cfg["formulas"]
    grading_dir = cfg["_grading_dir"]

    def update_moodle(
        moodle_rel: str,
        marks_by_email: dict[str, float],
        feedback_by_email: dict[str, str] | None = None,
    ) -> int:
        moodle_path = (grading_dir / moodle_rel).resolve()
        if not moodle_path.is_file():
            print(f"  skip (missing): {moodle_path}")
            return 0
        headers, rows = read_csv_rows(moodle_path)
        if MOODLE_GRADE_COL not in headers:
            print(f"  skip (no {MOODLE_GRADE_COL} column): {moodle_path}")
            return 0
        updated = 0
        for row in rows:
            email = (row.get(MOODLE_EMAIL_COL) or "").strip().lower()
            if email in marks_by_email:
                row[MOODLE_GRADE_COL] = format_moodle_grade(marks_by_email[email])
                updated += 1
            if (
                feedback_by_email
                and email in feedback_by_email
                and MOODLE_FEEDBACK_COL in headers
            ):
                row[MOODLE_FEEDBACK_COL] = feedback_by_email[email]
        write_moodle_csv(moodle_path, headers, rows)
        return updated

    for entry in cfg["detail_files"]:
        csv_path = grading_dir / entry["file"]
        _, rows = read_csv_rows(csv_path)
        crit_map = None
        if entry.get("criteria_prefix") is not None:
            crit_map = reflection_criteria_map(entry.get("criteria_prefix", ""))
        marks, feedback = collect_marks_and_feedback(rows, entry, formulas_cfg, crit_map)

        moodle_rel = entry.get("moodle_csv")
        if moodle_rel and marks:
            n = update_moodle(moodle_rel, marks, feedback)
            fb = len(feedback)
            print(f"{entry['id']}: updated {n} grades, {fb} feedback -> {moodle_rel}")

        for extra in entry.get("extra_marks") or []:
            extra_marks: dict[str, float] = {}
            extra_feedback: dict[str, str] = {}
            for row in rows:
                email = (row.get("email") or "").strip().lower()
                if not email:
                    continue
                mark = eval_mark_row(
                    row,
                    extra["formula"],
                    formulas_cfg,
                    criteria_map=extra.get("criteria_map"),
                )
                if mark is not None:
                    extra_marks[email] = mark
                notas = (row.get("notas") or "").strip()
                if notas:
                    extra_feedback[email] = notas
            moodle_rel = extra.get("moodle_csv")
            if moodle_rel and extra_marks:
                n = update_moodle(moodle_rel, extra_marks, extra_feedback)
                print(f"{extra['id']}: updated {n} rows -> {moodle_rel}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Big Data course grade workbook")
    parser.add_argument(
        "command",
        choices=["init", "sync", "build", "moodle", "all"],
        help="sync: roster → detail CSVs; build: grades.xlsx; moodle: calificaciones.csv",
    )
    parser.add_argument(
        "--grading-dir",
        type=Path,
        default=DEFAULT_GRADING_DIR,
        help="Path to students-work/grading",
    )
    args = parser.parse_args()
    grading_dir = args.grading_dir.resolve()

    if args.command == "init":
        cmd_init(grading_dir)
    elif args.command == "sync":
        cmd_sync(grading_dir)
    elif args.command == "build":
        cmd_build(grading_dir)
    elif args.command == "moodle":
        cmd_moodle(grading_dir)
    elif args.command == "all":
        cmd_sync(grading_dir)
        cmd_build(grading_dir)
        cmd_moodle(grading_dir)


if __name__ == "__main__":
    main()
