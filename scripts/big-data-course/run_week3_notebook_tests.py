#!/usr/bin/env python3
"""Execute L5 and L6 individual notebooks; validate week-3-group scaffold."""

from __future__ import annotations

import argparse
import json
import re
import sys
import traceback
from pathlib import Path

import nbformat
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError

REPO_ROOT = Path(__file__).resolve().parents[2]
NOTEBOOKS = REPO_ROOT / "assets" / "notebooks" / "26-udenar-big-data"
DEFAULT_DATA_ROOT = REPO_ROOT / "scripts" / "big-data-course" / "geih_build"


def patch_notebook_source(source: str, notebook_stem: str) -> str:
    """Force local execution flags for instructor smoke tests."""
    out = source
    if notebook_stem in ("l5-ingestion", "l6-analytics"):
        out = re.sub(
            r"USE_GOOGLE_DRIVE\s*=\s*True",
            "USE_GOOGLE_DRIVE = False",
            out,
        )
    if notebook_stem == "l5-ingestion" and "kafka-storage.sh" in out:
        out = (
            "# Smoke test: skip Kafka broker download/start on local runs\n"
            "KAFKA_ENABLED = False\n"
            'print("Smoke test: Kafka broker skipped; memory RSS path used.")\n'
        )
    return out


def patch_notebook(nb: nbformat.NotebookNode, notebook_stem: str) -> None:
    if notebook_stem in ("l5-ingestion", "l6-analytics"):
        nb.cells.insert(
            0,
            nbformat.v4.new_code_cell(
                "import asyncio\n"
                "try:\n"
                "    import nest_asyncio\n"
                "    nest_asyncio.apply()\n"
                "except ImportError:\n"
                "    pass\n"
                "if __import__('sys').platform == 'win32':\n"
                "    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())\n"
            ),
        )
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
    markdown_hits = sum(
        1
        for c in nb.cells
        if c.cell_type == "markdown"
        and any(k in c.source for k in ("Ejercicio 1", "Ejercicio 2", "manifest.json", "Prefect"))
    )
    return {
        "notebook": notebook_path.name,
        "code_cells": len(code_cells),
        "student_stub_cells": student_stub_cells,
        "assert_cells": assert_cells,
        "markdown_section_hits": markdown_hits,
        "executable_end_to_end": student_stub_cells > 0,
    }


def assert_data_layout(data_root: Path) -> None:
    processed = data_root / "data" / "processed" / "geih-spine"
    if not processed.is_dir():
        raise FileNotFoundError(
            f"Missing {processed} — run week-2 pipeline first (run_week2_notebook_tests.py)."
        )
    n_parts = len(list(processed.rglob("part-*.parquet")))
    if n_parts < 12:
        raise FileNotFoundError(f"{processed}: expected ≥12 partitions, found {n_parts}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--data-root",
        type=Path,
        default=DEFAULT_DATA_ROOT,
        help="Directory containing data/processed/geih-spine (default: geih_build)",
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
        "--skip-l5",
        action="store_true",
        help="Skip l5-ingestion (use if curated/ already exists)",
    )
    parser.add_argument(
        "--skip-l6",
        action="store_true",
        help="Skip l6-analytics",
    )
    args = parser.parse_args()

    work_dir = (args.work_dir or args.data_root).resolve()
    data_root = args.data_root.resolve()

    print(f"Data root: {data_root}", flush=True)
    print(f"Work dir:  {work_dir}", flush=True)

    try:
        assert_data_layout(data_root)
    except FileNotFoundError as exc:
        print(f"FAIL data layout: {exc}", flush=True)
        return 2

    sequence: list[tuple[str, Path]] = []
    if not args.skip_l5:
        sequence.append(("l5-ingestion.ipynb", NOTEBOOKS / "l5-ingestion.ipynb"))
    if not args.skip_l6:
        sequence.append(("l6-analytics.ipynb", NOTEBOOKS / "l6-analytics.ipynb"))

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

    group_path = NOTEBOOKS / "week-3-group.ipynb"
    print(f"\n=== Validating {group_path.name} (student scaffold) ===", flush=True)
    scaffold = validate_group_scaffold(group_path)
    results.append(scaffold)
    print(json.dumps(scaffold, indent=2), flush=True)
    if scaffold["student_stub_cells"] < 8 or scaffold["assert_cells"] < 12:
        exit_code = 1
        print("FAIL week-3-group scaffold check", flush=True)

    log_dir = REPO_ROOT / "tmp-notebook-test"
    log_dir.mkdir(parents=True, exist_ok=True)
    summary_path = log_dir / "week3-notebook-test-summary.json"
    summary_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\nSummary: {summary_path}", flush=True)
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
