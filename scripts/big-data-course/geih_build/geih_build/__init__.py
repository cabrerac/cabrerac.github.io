"""GEIH download and harmonisation for the Udenar Big Data course."""

from geih_build.access import (
    DEFAULT_MANIFEST,
    DEFAULT_PLAN,
    DEFAULT_REGISTRY,
    DEFAULT_STATE,
    discover_catalogs,
    ensure_catalogs,
    fetch_one,
    plan_from_years,
    run,
    status,
)
from geih_build.dane_catalog import CatalogFile, find_catalog_file, list_catalog_downloads
from geih_build.fetch import CSV_ENCODING, CSV_SEP, fetch_file, is_labour_csv_name
from geih_build.segment import AccessPlan, SegmentQuery, load_access_plan
from geih_build.slice_spec import (
    subset_from_project_requirements,
    subset_from_project_requirements_text,
    subset_from_requirements_file,
)
from geih_build.timing import AccessTiming, Manifest, timing_context

__all__ = [
    "CSV_ENCODING",
    "CSV_SEP",
    "CatalogFile",
    "subset_from_project_requirements",
    "subset_from_project_requirements_text",
    "subset_from_requirements_file",
    "AccessTiming",
    "Manifest",
    "timing_context",
    "AccessPlan",
    "SegmentQuery",
    "load_access_plan",
    "discover_catalogs",
    "ensure_catalogs",
    "fetch_one",
    "fetch_file",
    "plan_from_years",
    "run",
    "status",
    "list_catalog_downloads",
    "find_catalog_file",
    "is_labour_csv_name",
    "DEFAULT_PLAN",
    "DEFAULT_REGISTRY",
    "DEFAULT_STATE",
    "DEFAULT_MANIFEST",
]
