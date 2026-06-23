#!/usr/bin/env python3
"""Scan week-2 group notebook submissions (instructor marking aid)."""
from __future__ import annotations

import json
from pathlib import Path

import nbformat

BASE = Path(__file__).resolve().parents[2] / (
    "work-space/teaching/big-data/students-work/week-2/group-notebook/_extracted"
)

# Submitters mapped to roster groups (from ZIP / Moodle)
GROUPS = {
    "G1": BASE
    / "MIGUEL LEONARDO LEON MENDEZ_552940_assignsubmission_file/unzipped_week-2-group-1",
    "G2": BASE
    / "Christian Martinez Benavides_552941_assignsubmission_file/unzipped_week-2-group-G2",
    "G3": BASE
    / "Mary Anyi Chaves Narvaez_552925_assignsubmission_file/unzipped_week-2-group-_3/week-2-group-_3",
    "G4": BASE
    / "Barbara Pascuaza Dulce_552929_assignsubmission_file/unzipped_week-2-group-G4/week-2-group-G4",
    "G5": BASE
    / "Cristian Santiago Muñoz López_552926_assignsubmission_file/unzipped_week-2-group-G5/week-2-group-G5",
}


def find_ipynb(folder: Path) -> Path:
    paths = [p for p in folder.rglob("*.ipynb") if "__MACOSX" not in str(p)]
    if not paths:
        raise FileNotFoundError(folder)
    return paths[0]


def find_manifest(folder: Path) -> Path | None:
    for name in ("manifest.json", "manifest_week2.json"):
        hits = list(folder.rglob(name))
        if hits:
            return hits[0]
    return None


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
                asserts.append((status, line.strip()[:100]))
    text = "\n".join(c.source for c in nb.cells)
    low = text.lower()
    return {
        "assert_total": len(asserts),
        "assert_pass": sum(1 for s, _ in asserts if s == "PASS"),
        "assert_fail": sum(1 for s, _ in asserts if s == "FAIL"),
        "assert_no_output": sum(1 for s, _ in asserts if s == "no_output"),
        "has_contrib": "contribución" in low or "contribucion" in low,
        "has_partition_note": "particion" in low or "partition" in low,
        "has_engine_note": "duckdb" in low or "polars" in low,
        "has_mr": "mapreduce" in low or "shuffle" in low,
        "has_privacy": "k_suppression" in low or "laplace" in low or "k_min" in low,
        "failed_asserts": [a for a in asserts if a[0] != "PASS"],
    }


def check_manifest(path: Path | None) -> dict:
    if path is None or not path.is_file():
        return {"ok": False, "reason": "missing"}
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return {"ok": len(data) >= 40, "type": "list", "n": len(data)}
    keys = list(data.keys()) if isinstance(data, dict) else []
    partition_stats = data.get("partition_stats") or data.get("partitions") or []
    n_part = len(partition_stats) if isinstance(partition_stats, list) else 0
    return {
        "ok": n_part >= 48 or "partition_stats" in keys or "harmonization" in keys,
        "type": "dict",
        "keys": keys[:12],
        "partition_stats_n": n_part,
        "has_timing": any(k in keys for k in ("timing", "benchmark", "bench")),
    }


def main() -> None:
    for gid, folder in GROUPS.items():
        print(f"=== {gid} ===")
        if not folder.is_dir():
            print("MISSING FOLDER")
            print()
            continue
        ipynb = find_ipynb(folder)
        manifest = find_manifest(folder)
        print(f"notebook: {ipynb.relative_to(BASE)}")
        if manifest:
            print(f"manifest: {manifest.relative_to(BASE)} -> {check_manifest(manifest)}")
        else:
            print("manifest: MISSING")
        s = scan_nb(ipynb)
        print(
            f"asserts: {s['assert_pass']}/{s['assert_total']} PASS "
            f"(fail={s['assert_fail']}, no_output={s['assert_no_output']})"
        )
        print(
            f"docs: contrib={s['has_contrib']} partition={s['has_partition_note']} "
            f"engine={s['has_engine_note']} mr={s['has_mr']} privacy={s['has_privacy']}"
        )
        if s["failed_asserts"]:
            for item in s["failed_asserts"][:8]:
                print(f"  ISSUE: {item}")
        print()


if __name__ == "__main__":
    main()
