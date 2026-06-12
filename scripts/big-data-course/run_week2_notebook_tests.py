#!/usr/bin/env python3
"""Execute L3, L4, and week-2-group-solution notebooks against local GEIH data."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import traceback
from pathlib import Path

import nbformat
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError


REPO_ROOT = Path(__file__).resolve().parents[2]
NOTEBOOKS = REPO_ROOT / "assets" / "notebooks" / "26-udenar-big-data"
INSTRUCTOR_NOTEBOOKS = (
    REPO_ROOT / "work-space" / "teaching" / "big-data" / "instructor" / "notebooks"
)
DEFAULT_DATA_ROOT = REPO_ROOT / "scripts" / "big-data-course" / "geih_build"
BUILD_INSTRUCTOR_SCRIPT = REPO_ROOT / "scripts" / "big-data-course" / "build_instructor_notebook.py"


def ensure_instructor_notebook(stem: str = "week-2-group-solution") -> Path:
    path = INSTRUCTOR_NOTEBOOKS / f"{stem}.ipynb"
    if path.is_file():
        return path
    print(f"Building instructor notebook {stem}...", flush=True)
    subprocess.run(
        [sys.executable, str(BUILD_INSTRUCTOR_SCRIPT), stem],
        check=True,
        cwd=REPO_ROOT,
    )
    if not path.is_file():
        raise FileNotFoundError(path)
    return path


def patch_notebook_source(source: str, notebook_stem: str) -> str:
    """Force local execution flags used in instructor smoke tests."""
    out = source
    if notebook_stem in ("l3-storage", "l4-processing", "week-2-group-solution"):
        out = re.sub(
            r"USE_GOOGLE_DRIVE\s*=\s*True",
            "USE_GOOGLE_DRIVE = False",
            out,
        )
    if notebook_stem == "l3-storage":
        out = re.sub(
            r"SKIP_DOWNLOAD\s*=\s*False",
            "SKIP_DOWNLOAD = True",
            out,
        )
    return out


def patch_notebook(nb: nbformat.NotebookNode, notebook_stem: str) -> None:
    for cell in nb.cells:
        if cell.cell_type == "code":
            cell.source = patch_notebook_source(cell.source, notebook_stem)


def execute_notebook(
    notebook_path: Path,
    work_dir: Path,
    timeout: int,
) -> dict:
    work_dir.mkdir(parents=True, exist_ok=True)
    with notebook_path.open(encoding="utf-8") as fh:
        nb = nbformat.read(fh, as_version=4)

    patch_notebook(nb, notebook_path.stem)

    client = NotebookClient(
        nb,
        timeout=timeout,
        kernel_name="python3",
        resources={"metadata": {"path": str(work_dir)}},
    )
    client.execute()

    out_path = work_dir / f"{notebook_path.stem}-executed.ipynb"
    with out_path.open("w", encoding="utf-8") as fh:
        nbformat.write(nb, fh)

    errors = []
    for i, cell in enumerate(nb.cells):
        if cell.cell_type != "code":
            continue
        for output in cell.get("outputs", []):
            if output.get("output_type") == "error":
                errors.append((i, output.get("ename"), output.get("evalue")))

    return {"notebook": notebook_path.name, "output": str(out_path), "errors": errors}


def validate_group_scaffold(notebook_path: Path) -> dict:
    with notebook_path.open(encoding="utf-8") as fh:
        nb = nbformat.read(fh, as_version=4)

    code_cells = [c for c in nb.cells if c.cell_type == "code"]
    student_stub_cells = sum(
        1 for c in code_cells if "# SU CÓDIGO" in c.source or "# SU CODIGO" in c.source
    )
    assert_cells = sum(1 for c in code_cells if "assert " in c.source)
    return {
        "notebook": notebook_path.name,
        "code_cells": len(code_cells),
        "student_stub_cells": student_stub_cells,
        "assert_cells": assert_cells,
        "executable_end_to_end": student_stub_cells > 0,
    }


def assert_data_layout(data_root: Path) -> None:
    raw = data_root / "data" / "raw"
    if not raw.is_dir():
        raise FileNotFoundError(f"Missing {raw} — run geih-build access or copy week-1 data.")
    years = [2022, 2023, 2024, 2025]
    for year in years:
        year_dir = raw / str(year)
        n_months = sum(
            1
            for p in year_dir.iterdir()
            if p.is_dir() and list(p.glob("*.CSV"))
        )
        if n_months < 12:
            raise FileNotFoundError(f"{year_dir}: expected 12 months with CSV, found {n_months}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--data-root",
        type=Path,
        default=DEFAULT_DATA_ROOT,
        help="Directory containing data/raw/2022..2025 (default: geih_build)",
    )
    parser.add_argument(
        "--work-dir",
        type=Path,
        default=None,
        help="Notebook cwd (default: same as --data-root)",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=3600,
        help="Per-cell timeout in seconds (default 3600)",
    )
    parser.add_argument(
        "--skip-l3",
        action="store_true",
        help="Skip l3-storage (use if lakehouse already built in work-dir)",
    )
    args = parser.parse_args()

    work_dir = args.work_dir or args.data_root
    work_dir = work_dir.resolve()
    data_root = args.data_root.resolve()

    print(f"Data root: {data_root}", flush=True)
    print(f"Work dir:  {work_dir}", flush=True)

    try:
        assert_data_layout(data_root)
    except FileNotFoundError as exc:
        print(f"FAIL data layout: {exc}", flush=True)
        return 2

    if work_dir != data_root:
        print("WARN: work-dir != data-root; notebooks expect data/raw under cwd.", flush=True)

    processed = work_dir / "data" / "processed" / "geih-spine"
    if processed.is_dir() and not args.skip_l3:
        print(f"Cleaning stale lakehouse: {processed}", flush=True)
        shutil.rmtree(processed)

    sequence: list[tuple[str, Path]] = []
    if not args.skip_l3:
        sequence.append(("l3-storage.ipynb", NOTEBOOKS / "l3-storage.ipynb"))
    sequence.append(("l4-processing.ipynb", NOTEBOOKS / "l4-processing.ipynb"))
    solution_path = ensure_instructor_notebook()
    sequence.append((solution_path.name, solution_path))

    results: list[dict] = []
    exit_code = 0

    for name, path in sequence:
        if not path.is_file():
            print(f"FAIL missing notebook: {path}", flush=True)
            return 2
        print(f"\n=== Executing {name} (timeout={args.timeout}s/cell) ===", flush=True)
        try:
            result = execute_notebook(path, work_dir, args.timeout)
            results.append(result)
            if result["errors"]:
                exit_code = 1
                print(f"FAIL {name}: {len(result['errors'])} error output(s)", flush=True)
                for idx, ename, evalue in result["errors"][:8]:
                    print(f"  cell {idx}: {ename}: {evalue}", flush=True)
            else:
                print(f"OK {name} -> {result['output']}", flush=True)
        except CellExecutionError as exc:
            exit_code = 1
            print(f"FAIL {name}: CellExecutionError", flush=True)
            print(exc, flush=True)
            results.append({"notebook": name, "failed": True, "error": str(exc)})
            break
        except Exception:
            exit_code = 1
            print(f"FAIL {name}: unexpected error", flush=True)
            traceback.print_exc()
            results.append({"notebook": name, "failed": True})
            break

    group_path = NOTEBOOKS / "week-2-group.ipynb"
    print(f"\n=== Validating {group_path.name} (student scaffold) ===", flush=True)
    scaffold = validate_group_scaffold(group_path)
    results.append(scaffold)
    print(json.dumps(scaffold, indent=2), flush=True)
    if scaffold["student_stub_cells"] < 5 or scaffold["assert_cells"] < 10:
        exit_code = 1
        print("FAIL week-2-group scaffold check", flush=True)

    log_dir = REPO_ROOT / "tmp-notebook-test"
    log_dir.mkdir(parents=True, exist_ok=True)
    summary_path = log_dir / "week2-notebook-test-summary.json"
    summary_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\nSummary: {summary_path}", flush=True)
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
