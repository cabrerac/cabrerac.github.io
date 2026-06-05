#!/usr/bin/env python3
"""Execute week-1 individual notebooks end-to-end; validate group notebook structure."""

from __future__ import annotations

import argparse
import json
import sys
import traceback
from pathlib import Path

import nbformat
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError


REPO_ROOT = Path(__file__).resolve().parents[2]
NOTEBOOKS = REPO_ROOT / "assets" / "notebooks" / "26-udenar-big-data"


def execute_notebook(notebook_path: Path, work_dir: Path, timeout: int) -> dict:
    work_dir.mkdir(parents=True, exist_ok=True)
    with notebook_path.open(encoding="utf-8") as fh:
        nb = nbformat.read(fh, as_version=4)

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


def validate_group_notebook(notebook_path: Path) -> dict:
    with notebook_path.open(encoding="utf-8") as fh:
        nb = nbformat.read(fh, as_version=4)

    code_cells = [c for c in nb.cells if c.cell_type == "code"]
    student_stub_cells = sum(
        1 for c in code_cells if c.source.strip() in {"# SU CÓDIGO", "# SU CODIGO"}
    )
    assert_cells = sum(1 for c in code_cells if "assert " in c.source)
    markdown_hits = sum(
        1
        for c in nb.cells
        if c.cell_type == "markdown"
        and any(k in c.source for k in ("Parte A", "Parte B", "manifest.json", "osm_poi"))
    )

    return {
        "notebook": notebook_path.name,
        "code_cells": len(code_cells),
        "student_stub_cells": student_stub_cells,
        "assert_cells": assert_cells,
        "markdown_section_hits": markdown_hits,
        "executable_end_to_end": student_stub_cells > 0,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--work-dir",
        type=Path,
        default=REPO_ROOT / "tmp-notebook-test",
        help="Directory for downloads, outputs, and executed notebooks",
    )
    parser.add_argument("--timeout", type=int, default=900, help="Per-cell timeout (seconds)")
    args = parser.parse_args()

    results: list[dict] = []
    exit_code = 0

    for name in ("l1-introduction.ipynb", "l2-ethics-governance.ipynb"):
        path = NOTEBOOKS / name
        print(f"\n=== Executing {name} ===", flush=True)
        try:
            result = execute_notebook(path, args.work_dir, args.timeout)
            results.append(result)
            if result["errors"]:
                exit_code = 1
                print(f"FAIL {name}: {len(result['errors'])} error output(s)", flush=True)
                for idx, ename, evalue in result["errors"][:5]:
                    print(f"  cell {idx}: {ename}: {evalue}", flush=True)
            else:
                print(f"OK {name} -> {result['output']}", flush=True)
        except CellExecutionError as exc:
            exit_code = 1
            print(f"FAIL {name}: CellExecutionError", flush=True)
            print(exc, flush=True)
            results.append({"notebook": name, "failed": True, "error": str(exc)})
        except Exception:
            exit_code = 1
            print(f"FAIL {name}: unexpected error", flush=True)
            traceback.print_exc()
            results.append({"notebook": name, "failed": True})

    group_path = NOTEBOOKS / "week-1-group.ipynb"
    print(f"\n=== Validating {group_path.name} (student template) ===", flush=True)
    group_result = validate_group_notebook(group_path)
    results.append(group_result)
    print(json.dumps(group_result, indent=2), flush=True)
    if group_result["student_stub_cells"] < 1 or group_result["assert_cells"] < 3:
        exit_code = 1
        print("FAIL week-1-group structure check", flush=True)

    summary_path = args.work_dir / "smoke-test-summary.json"
    summary_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\nSummary written to {summary_path}", flush=True)
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
