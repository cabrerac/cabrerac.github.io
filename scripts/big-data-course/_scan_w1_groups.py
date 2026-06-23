#!/usr/bin/env python3
"""One-off scan of week-1 group submissions (instructor marking aid)."""
from __future__ import annotations

import csv
import json
from pathlib import Path

import nbformat

BASE = Path(__file__).resolve().parents[2] / (
    "work-space/teaching/big-data/students-work/week-1/group-notebook/_extracted"
)

GROUPS = {
    "G1": BASE / "unzipped_week-1-_group_1_",
    "G2": BASE / "unzipped_week-1-G2",
    "G3": BASE / "unzipped_week-1-G3",
    "G4": BASE / "unzipped_week_1_G4. Zip",
    "G5": BASE / "unzipped_Week-1-G5",
}


def find_ipynb(folder: Path) -> Path:
    paths = [p for p in folder.rglob("*.ipynb") if "__MACOSX" not in str(p)]
    return paths[0]


def scan_nb(path: Path) -> dict:
    nb = nbformat.read(path.open(encoding="utf-8"), as_version=4)
    asserts: list[tuple[str, str]] = []
    for cell in nb.cells:
        if cell.cell_type != "code":
            continue
        for line in cell.source.splitlines():
            if "assert " in line:
                has_err = any(o.get("output_type") == "error" for o in cell.get("outputs", []))
                if has_err:
                    status = "FAIL"
                elif cell.get("outputs"):
                    status = "PASS"
                else:
                    status = "no_output"
                asserts.append((status, line.strip()[:95]))
    text = "\n".join(c.source for c in nb.cells)
    low = text.lower()
    contrib_section = ""
    for cell in nb.cells:
        if cell.cell_type == "markdown" and "registro de contribución" in cell.source.lower():
            idx = nb.cells.index(cell)
            if idx + 1 < len(nb.cells):
                contrib_section = nb.cells[idx + 1].source[:500]
    return {
        "assert_total": len(asserts),
        "assert_pass": sum(1 for s, _ in asserts if s == "PASS"),
        "assert_fail": sum(1 for s, _ in asserts if s == "FAIL"),
        "assert_no_output": sum(1 for s, _ in asserts if s == "no_output"),
        "has_contrib": "contribución" in low or "contribucion" in low,
        "has_enlace": "personas_muestra" in low,
        "has_ethics_table": "cuasi" in low or "quasi" in low,
        "has_readings": "zuboff" in low or "mittelstadt" in low,
        "contrib_preview": contrib_section.replace("\n", " ")[:200],
        "failed_asserts": [a for a in asserts if a[0] != "PASS"],
    }


def check_manifest(p: Path) -> dict:
    data = json.loads(p.read_text(encoding="utf-8"))
    entries = data if isinstance(data, list) else data.get("entries", data.get("files", []))
    if isinstance(data, dict) and not entries:
        entries = data.get("manifest", [])
    n = len(entries) if isinstance(entries, list) else 0
    e0 = entries[0] if entries else {}
    return {
        "n": n,
        "ok_n": n >= 40,
        "bytes_ok": (e0.get("bytes_downloaded") or 0) > 0,
        "year_ok": "survey_year" in e0,
    }


def check_osm(p: Path) -> dict:
    with p.open(encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    cols = set(rows[0].keys()) if rows else set()
    need = {"dpto", "poi_school_count", "poi_health_count", "poi_servicios_basicos_count"}
    return {"n": len(rows), "ok": len(rows) >= 5 and need.issubset(cols), "cols": sorted(cols)}


def main() -> None:
    for gid, folder in GROUPS.items():
        print(f"=== {gid} ===")
        ipynb = find_ipynb(folder)
        manifest = list(folder.rglob("manifest.json"))[0]
        osm = list(folder.rglob("osm_poi_by_dpto.csv"))[0]
        print(f"notebook: {ipynb.relative_to(BASE)}")
        print(f"manifest: {manifest.relative_to(BASE)} -> {check_manifest(manifest)}")
        print(f"osm: {osm.relative_to(BASE)} -> {check_osm(osm)}")
        s = scan_nb(ipynb)
        print(
            f"asserts: {s['assert_pass']}/{s['assert_total']} PASS "
            f"(fail={s['assert_fail']}, no_output={s['assert_no_output']})"
        )
        print(
            f"docs: contrib={s['has_contrib']} enlace={s['has_enlace']} "
            f"ethics_qi={s['has_ethics_table']} readings={s['has_readings']}"
        )
        if s["contrib_preview"]:
            print(f"contrib: {s['contrib_preview']}")
        if s["failed_asserts"]:
            for item in s["failed_asserts"]:
                print(f"  ISSUE: {item}")
        print()


if __name__ == "__main__":
    main()
