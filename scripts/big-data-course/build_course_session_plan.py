#!/usr/bin/env python3
"""Build Saturday session plan PDFs from course markdown sources.

Examples:
  python scripts/big-data-course/build_course_session_plan.py --all
  python scripts/big-data-course/build_course_session_plan.py week_2
"""

from __future__ import annotations

import argparse
from collections.abc import Callable
from pathlib import Path

from session_plan_build import (
    WEEK1_ASSETS,
    WEEK1_SOURCE,
    WEEK2_ASSETS,
    WEEK2_SOURCE,
    WEEK3_ASSETS,
    WEEK3_SOURCE,
    write_session_plan,
)

PLAN_WRITERS: dict[str, Callable[[], list[Path]]] = {
    "week_1": lambda: list(write_session_plan(WEEK1_SOURCE, WEEK1_ASSETS)),
    "week_2": lambda: list(write_session_plan(WEEK2_SOURCE, WEEK2_ASSETS)),
    "week_3": lambda: list(write_session_plan(WEEK3_SOURCE, WEEK3_ASSETS)),
}


def build_all() -> list[Path]:
    paths = []
    for writer in PLAN_WRITERS.values():
        paths.extend(writer())
    return paths


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Big Data course session plan PDFs.")
    parser.add_argument(
        "plan",
        nargs="?",
        choices=tuple(PLAN_WRITERS.keys()),
        help="Session plan to build (omit with --all)",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Build every session plan PDF",
    )
    args = parser.parse_args()

    if args.all:
        paths = build_all()
    elif args.plan:
        paths = PLAN_WRITERS[args.plan]()
    else:
        parser.error("specify a plan name or --all")

    for path in paths:
        print(f"Wrote {path}")


if __name__ == "__main__":
    main()
