"""
GEIH Access layer — discover catalogs, scrape file ids, download, extract.

Files are stored under DANE filenames (ZIP + extract folder = filename stem).
"""

from __future__ import annotations

from pathlib import Path

from geih_build.build_state import (
    BuildState,
    FileStatus,
    file_extract_complete,
    file_zip_path,
    file_zip_valid,
)
from geih_build.dane_catalog import (
    CatalogFile,
    CatalogRegistry,
    catalog_id_for_year,
    discover_national_geih_catalogs,
    find_catalog_file,
    list_catalog_downloads,
)
from geih_build.fetch import fetch_file, is_labour_csv_name
from geih_build.segment import AccessPlan, SegmentQuery, load_access_plan
from geih_build.timing import Manifest

DEFAULT_PLAN = Path(__file__).resolve().parent.parent / "configs" / "spine_access_plan.json"
DEFAULT_REGISTRY = Path("catalog_registry.json")
DEFAULT_STATE = Path("build_state.json")
DEFAULT_MANIFEST = Path("manifest.json")


def discover_catalogs(
    *,
    registry_path: Path = DEFAULT_REGISTRY,
    query: str = "GEIH",
) -> CatalogRegistry:
    """Search DANE for national GEIH catalogs (survey year -> catalog id)."""
    registry = discover_national_geih_catalogs(query=query)
    registry.save(registry_path)
    return registry


def ensure_catalogs(registry_path: Path = DEFAULT_REGISTRY) -> CatalogRegistry:
    if registry_path.is_file():
        return CatalogRegistry.load(registry_path)
    return discover_catalogs(registry_path=registry_path)


def plan_from_years(
    years: list[int],
    *,
    dest: Path = Path("data/raw"),
    name: str = "ad-hoc",
) -> AccessPlan:
    return AccessPlan(
        name=name,
        segments=(SegmentQuery(years=tuple(years)),),
        dest=dest,
    )


def parse_year_range(text: str) -> list[int]:
    text = text.strip()
    if "-" in text:
        start, end = text.split("-", 1)
        return list(range(int(start), int(end) + 1))
    return [int(text)]


def fetch_one(
    catalog_id: int,
    file_id: int,
    dest: Path = Path("data/raw"),
    *,
    registry_path: Path = DEFAULT_REGISTRY,
    resume: bool = True,
) -> Path:
    """Download and extract one DANE file by catalog id + file id (L1 unit)."""
    ensure_catalogs(registry_path)
    file = find_catalog_file(catalog_id, file_id)
    if resume and file_extract_complete(dest, file):
        return next(
            (p for p in file.extract_dir(dest).glob("*.CSV") if is_labour_csv_name(p.name)),
            file.extract_dir(dest),
        )
    return fetch_file(file, dest)


def run(
    plan: AccessPlan,
    *,
    registry_path: Path = DEFAULT_REGISTRY,
    state_path: Path = DEFAULT_STATE,
    manifest_path: Path = DEFAULT_MANIFEST,
    resume: bool = True,
    refresh_catalog: bool = False,
) -> BuildState:
    """
    Run the access plan: discover catalogs (if needed), scrape files, download.

    Idempotent with ``resume=True`` — safe to stop and restart.
    """
    dest = plan.dest
    dest.mkdir(parents=True, exist_ok=True)

    if refresh_catalog or not registry_path.is_file():
        discover_catalogs(registry_path=registry_path)
    else:
        ensure_catalogs(registry_path)

    state = BuildState.load(state_path)
    state.plan_name = plan.name
    manifest = Manifest()
    files = plan.all_files(registry_path=registry_path)

    print(f"Access plan {plan.name!r}: {len(files)} file(s) -> {dest.resolve()}")

    for i, file in enumerate(files, start=1):
        record = state.ensure_file(file)
        label = file.storage_key()
        print(f"[{i}/{len(files)}] {file.year_dir()}/{file.filename}", flush=True)

        if resume and file_extract_complete(dest, file):
            record.status = FileStatus.EXTRACTED
            record.extract_dir = str(file.extract_dir(dest))
            record.zip_path = str(file_zip_path(dest, file))
            print("  skip (already extracted)")
            state.save(state_path)
            continue

        zip_path = file_zip_path(dest, file)
        record.zip_path = str(zip_path)

        try:
            if resume and file_zip_valid(zip_path):
                print("  re-extract from ZIP")
                from geih_build.fetch import _extract_csvs

                _extract_csvs(zip_path, file.extract_dir(dest))
                record.status = FileStatus.EXTRACTED
                record.extract_dir = str(file.extract_dir(dest))
                record.error = None
                state.save(state_path)
                continue

            if zip_path.is_file() and not file_zip_valid(zip_path):
                zip_path.unlink(missing_ok=True)

            labour = fetch_file(file, dest, manifest=manifest)
            record.status = FileStatus.EXTRACTED
            record.extract_dir = str(labour.parent)
            record.error = None
            if manifest.entries:
                record.bytes_downloaded = manifest.entries[-1].bytes_downloaded
            print(f"  ok -> {labour.name}")
        except Exception as exc:  # noqa: BLE001
            record.status = FileStatus.FAILED
            record.error = str(exc)
            print(f"  FAILED: {exc}")

        state.save(state_path)

    manifest.write_json(manifest_path)
    state.save(state_path)
    _print_summary(state, dest)
    return state


def status(
    dest: Path = Path("data/raw"),
    *,
    state_path: Path = DEFAULT_STATE,
    registry_path: Path = DEFAULT_REGISTRY,
) -> None:
    """Print catalog registry, build state, and disk usage."""
    if registry_path.is_file():
        reg = CatalogRegistry.load(registry_path)
        print(f"Catalogs ({len(reg.entries)}):")
        for e in reg.entries:
            print(f"  {e.survey_year} -> {e.catalog_id}")
    else:
        print("No catalog_registry.json — run: geih-build access")

    if state_path.is_file():
        state = BuildState.load(state_path)
        counts: dict[str, int] = {}
        for rec in state.files.values():
            counts[rec.status.value] = counts.get(rec.status.value, 0) + 1
        print(f"Build state ({state.plan_name or 'unnamed'}):")
        for k, v in sorted(counts.items()):
            print(f"  {k}: {v}")
    else:
        print("No build_state.json yet.")

    if dest.is_dir():
        total = sum(p.stat().st_size for p in dest.rglob("*") if p.is_file())
        year_dirs = [p for p in dest.iterdir() if p.is_dir() and p.name.isdigit()]
        n_zips = len(list(dest.rglob("*.zip")))
        n_extract = len([p for p in dest.rglob("*") if p.is_dir() and p.parent.name.isdigit()])
        print(
            f"Data at {dest.resolve()}: {total / 1e9:.3f} GB, "
            f"{len(year_dirs)} year folder(s), {n_zips} ZIP(s)"
        )


def _print_summary(state: BuildState, dest: Path) -> None:
    ok = sum(1 for r in state.files.values() if r.status == FileStatus.EXTRACTED)
    fail = sum(1 for r in state.files.values() if r.status == FileStatus.FAILED)
    total_bytes = sum(p.stat().st_size for p in dest.rglob("*") if p.is_file())
    print(f"Done: {ok} extracted, {fail} failed, {total_bytes / 1e9:.3f} GB on disk")
