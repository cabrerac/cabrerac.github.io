"""DANE microdatos — discover GEIH catalogs and scrape download files."""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path

import requests

CATALOG_SEARCH_URL = "https://microdatos.dane.gov.co/index.php/catalog/"
DEFAULT_SEARCH_QUERY = "GEIH"

# National monthly GEIH (exclude San Andrés, Ciudades Intermedias, etc.).
NATIONAL_GEIH_TITLE_RE = re.compile(
    r"^Gran Encuesta Integrada de Hogares\s*-\s*GEIH(?:\s*-\s*|\s+)(\d{4})\.?\s*$",
    re.IGNORECASE,
)

# Same onclick pattern as DANE get-microdata pages (see L1 notebook).
DOWNLOAD_ONCLICK_RE = re.compile(
    r"mostrarModal\(\s*'([^']+)'\s*,\s*'"
    r"(https://microdatos\.dane\.gov\.co/index\.php/catalog/\d+/download/\d+)\s*'\s*\)",
    re.IGNORECASE,
)

CATALOG_LINK_RE = re.compile(
    r'href="https://microdatos\.dane\.gov\.co/index\.php/catalog/(\d+)" title="([^"]+)"',
    re.IGNORECASE,
)

FILE_ID_RE = re.compile(r"/download/(\d+)")

# Non-CSV microdata bundles listed on older get-microdata pages (from filename only).
_NON_CSV_FILENAME_MARKERS = (".sav", ".dta", "_txt", ".txt.zip")
_SKIP_FILENAME_MARKERS = ("proyeccion", "cnpv", "empalme")


@dataclass(frozen=True)
class CatalogFile:
    """One downloadable ZIP listed on a catalog get-microdata page."""

    catalog_id: int
    file_id: int
    filename: str
    url: str
    survey_year: int | None = None

    @property
    def stem(self) -> str:
        return Path(self.filename).stem

    def year_dir(self) -> str:
        """Survey year from catalog metadata (not hardcoded)."""
        if self.survey_year is not None:
            return str(self.survey_year)
        return "_unknown"

    def storage_key(self) -> str:
        """Unique key for build state: ``{survey_year}/{filename_stem}``."""
        return f"{self.year_dir()}/{self.stem}"

    def zip_path(self, dest: Path) -> Path:
        return dest / self.year_dir() / self.filename

    def extract_dir(self, dest: Path) -> Path:
        return dest / self.year_dir() / self.stem


@dataclass(frozen=True)
class CatalogEntry:
    catalog_id: int
    survey_year: int
    title: str


@dataclass
class CatalogRegistry:
    entries: list[CatalogEntry]

    def year_to_id(self) -> dict[int, int]:
        return {e.survey_year: e.catalog_id for e in self.entries}

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps({"entries": [asdict(e) for e in self.entries]}, indent=2),
            encoding="utf-8",
        )

    @classmethod
    def load(cls, path: Path) -> CatalogRegistry:
        if not path.is_file():
            return cls(entries=[])
        data = json.loads(path.read_text(encoding="utf-8"))
        return cls(entries=[CatalogEntry(**row) for row in data.get("entries", [])])


def file_id_from_url(url: str) -> int:
    m = FILE_ID_RE.search(url)
    if not m:
        raise ValueError(f"No file id in download URL: {url!r}")
    return int(m.group(1))


def discover_national_geih_catalogs(
    query: str = DEFAULT_SEARCH_QUERY,
    *,
    max_pages: int = 25,
) -> CatalogRegistry:
    """
    Search microdatos.dane.gov.co and collect **national** GEIH catalog ids.

    Parses the same catalog list HTML students see when searching "GEIH".
    Keeps titles matching ``Gran Encuesta Integrada de Hogares - GEIH - YYYY``.
    """
    by_year: dict[int, CatalogEntry] = {}
    for page in range(1, max_pages + 1):
        resp = requests.get(
            CATALOG_SEARCH_URL,
            params={
                "page": page,
                "ps": 50,
                "sk": query,
                "sort_by": "title",
                "sort_order": "desc",
            },
            timeout=120,
        )
        resp.raise_for_status()
        pairs = CATALOG_LINK_RE.findall(resp.text)
        if not pairs:
            break
        for cid_str, title in pairs:
            m = NATIONAL_GEIH_TITLE_RE.match(title.strip())
            if not m:
                continue
            year = int(m.group(1))
            entry = CatalogEntry(
                catalog_id=int(cid_str),
                survey_year=year,
                title=title.strip(),
            )
            by_year[year] = entry
        if f"page={page + 1}" not in resp.text:
            break
    if not by_year:
        raise ValueError(
            f"No national GEIH catalogs found for search {query!r}. "
            "Check network access to microdatos.dane.gov.co."
        )
    return CatalogRegistry(entries=sorted(by_year.values(), key=lambda e: e.survey_year))


def refresh_geih_registry(
    path: Path = Path("catalog_registry.json"),
    *,
    query: str = DEFAULT_SEARCH_QUERY,
) -> CatalogRegistry:
    """Discover catalogs from DANE search and write ``catalog_registry.json``."""
    registry = discover_national_geih_catalogs(query=query)
    registry.save(path)
    return registry


def catalog_id_for_year(year: int, registry_path: Path | None = Path("catalog_registry.json")) -> int:
    if registry_path and registry_path.is_file():
        mapping = CatalogRegistry.load(registry_path).year_to_id()
        if year in mapping:
            return mapping[year]
    raise ValueError(
        f"No GEIH catalog for survey year {year}. Run: geih-build access (refreshes catalogs) "
        f"or delete {registry_path} and retry."
    )


def catalog_page_url(catalog_id: int) -> str:
    return f"https://microdatos.dane.gov.co/index.php/catalog/{catalog_id}"


def get_microdata_page_url(catalog_id: int) -> str:
    return f"https://microdatos.dane.gov.co/index.php/catalog/{catalog_id}/get-microdata"


def list_catalog_downloads(
    catalog_id: int,
    *,
    csv_releases_only: bool = True,
) -> list[CatalogFile]:
    """Scrape download links from get-microdata (``mostrarModal`` onclick)."""
    try:
        survey_year = _survey_year_for_catalog(catalog_id)
    except ValueError:
        survey_year = None
    resp = requests.get(get_microdata_page_url(catalog_id), timeout=120)
    resp.raise_for_status()
    seen: set[int] = set()
    files: list[CatalogFile] = []
    for filename, url in DOWNLOAD_ONCLICK_RE.findall(resp.text):
        url = url.strip()
        filename = filename.strip()
        file_id = file_id_from_url(url)
        if file_id in seen:
            continue
        seen.add(file_id)
        files.append(
            CatalogFile(
                catalog_id=catalog_id,
                file_id=file_id,
                filename=filename,
                url=url,
                survey_year=survey_year,
            )
        )
    files = sorted(files, key=lambda f: f.filename.lower())
    if csv_releases_only:
        return filter_csv_releases(files)
    return files


def filter_csv_releases(files: list[CatalogFile]) -> list[CatalogFile]:
    """
    Keep one CSV microdata ZIP per logical release.

    DANE lists SAV, TXT, and CSV variants for the same month on older catalogs.
    Prefer explicit ``*.csv.zip`` / ``*_csv.zip``; otherwise keep the remaining
    ZIP when it is the only non-SAV/TXT option (e.g. ``Enero.zip`` on 2023).
    """
    eligible: list[CatalogFile] = []
    for f in files:
        lower = f.filename.lower()
        if not lower.endswith(".zip"):
            continue
        if any(m in lower for m in _NON_CSV_FILENAME_MARKERS):
            continue
        if any(m in lower for m in _SKIP_FILENAME_MARKERS):
            continue
        eligible.append(f)

    groups: dict[str, list[CatalogFile]] = {}
    for f in eligible:
        groups.setdefault(_release_key(f.filename), []).append(f)

    chosen: list[CatalogFile] = []
    for group in groups.values():
        best = max(group, key=lambda f: _csv_release_priority(f.filename))
        chosen.append(best)
    return sorted(chosen, key=lambda f: f.filename.lower())


def _release_key(filename: str) -> str:
    """Group alternate formats for the same monthly file (``Abril.zip`` / ``Abril.csv.zip``)."""
    stem = Path(filename).stem.lower()
    for suffix in (".csv", "_csv"):
        if stem.endswith(suffix):
            return stem[: -len(suffix)]
    return stem


def _csv_release_priority(filename: str) -> int:
    lower = filename.lower()
    if ".csv.zip" in lower or lower.endswith("_csv.zip"):
        return 3
    if "geih_" in lower or re.search(r"20\d{2}", lower):
        return 3
    return 1


def find_catalog_file_by_filename(catalog_id: int, dane_filename: str) -> CatalogFile:
    for item in list_catalog_downloads(catalog_id):
        if item.filename == dane_filename:
            return item
    raise ValueError(
        f"No {dane_filename!r} on catalog {catalog_id}. "
        f"Open {get_microdata_page_url(catalog_id)}."
    )


def find_catalog_file(catalog_id: int, file_id: int) -> CatalogFile:
    for item in list_catalog_downloads(catalog_id):
        if item.file_id == file_id:
            return item
    raise ValueError(
        f"No file id {file_id} on catalog {catalog_id}. "
        f"Open {get_microdata_page_url(catalog_id)}."
    )


def _survey_year_for_catalog(catalog_id: int) -> int:
    resp = requests.get(catalog_page_url(catalog_id), timeout=120)
    resp.raise_for_status()
    title = _extract_title(resp.text)
    m = NATIONAL_GEIH_TITLE_RE.match(title) or re.search(
        r"GEIH(?:\s*-\s*|\s+)(\d{4})",
        title,
        re.I,
    )
    if not m:
        raise ValueError(f"Could not parse survey year from catalog {catalog_id}: {title!r}")
    return int(m.group(1))


def _extract_title(html: str) -> str:
    m = re.search(r"<title>([^<]+)</title>", html, re.IGNORECASE)
    return m.group(1).strip() if m else ""
