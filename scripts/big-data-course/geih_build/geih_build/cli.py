"""GEIH Access — automated, modular DANE downloads for the Big Data course."""

from __future__ import annotations

import argparse
from pathlib import Path

from geih_build import access
from geih_build.segment import load_access_plan


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="geih-build",
        description=(
            "GEIH Access layer: discover DANE catalogs, scrape file ids, "
            "download ZIPs under DANE filenames, extract CSVs. Resumable."
        ),
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_access = sub.add_parser(
        "access",
        help="Download + extract files (default: full course spine plan)",
    )
    p_access.add_argument(
        "--plan",
        type=Path,
        default=None,
        help=f"Access plan YAML/JSON (default: {access.DEFAULT_PLAN.name})",
    )
    p_access.add_argument(
        "--years",
        type=str,
        default=None,
        help="Ad-hoc survey years, e.g. 2024 or 2008-2025 (overrides --plan)",
    )
    p_access.add_argument(
        "--catalog",
        type=int,
        default=None,
        help="Download one file: DANE catalog id (with --file-id)",
    )
    p_access.add_argument(
        "--file-id",
        type=int,
        default=None,
        help="Download one file: DANE file id from get-microdata",
    )
    p_access.add_argument("--dest", type=Path, default=Path("data/raw"))
    p_access.add_argument(
        "--fresh",
        action="store_true",
        help="Do not skip already-extracted files",
    )
    p_access.add_argument(
        "--refresh-catalog",
        action="store_true",
        help="Re-search DANE for GEIH catalog ids before downloading",
    )

    p_status = sub.add_parser("status", help="Catalog registry, build state, disk usage")
    p_status.add_argument("--dest", type=Path, default=Path("data/raw"))

    args = parser.parse_args()

    if args.command == "access":
        if args.catalog is not None or args.file_id is not None:
            if args.catalog is None or args.file_id is None:
                parser.error("--catalog and --file-id must be used together")
            if args.refresh_catalog:
                access.discover_catalogs()
            else:
                access.ensure_catalogs()
            access.fetch_one(
                args.catalog,
                args.file_id,
                dest=args.dest,
                resume=not args.fresh,
            )
        elif args.years:
            plan = access.plan_from_years(
                access.parse_year_range(args.years),
                dest=args.dest,
            )
            access.run(
                plan,
                resume=not args.fresh,
                refresh_catalog=args.refresh_catalog,
            )
        else:
            plan_path = args.plan or access.DEFAULT_PLAN
            loaded = load_access_plan(plan_path)
            from geih_build.segment import AccessPlan

            plan = AccessPlan(name=loaded.name, segments=loaded.segments, dest=args.dest)
            access.run(
                plan,
                resume=not args.fresh,
                refresh_catalog=args.refresh_catalog,
            )

    elif args.command == "status":
        access.status(dest=args.dest)


if __name__ == "__main__":
    main()
