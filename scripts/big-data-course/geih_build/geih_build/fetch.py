"""Download GEIH files from DANE (HTTP) with optional fallback mirror."""

from __future__ import annotations

import re
import shutil
import zipfile
from pathlib import Path
from typing import Literal

import requests

from geih_build.dane_catalog import CatalogFile
from geih_build.timing import Manifest, timing_context

Method = Literal["http", "fallback"]

CSV_ENCODING = "latin-1"
CSV_SEP = ";"


def normalize_csv_name(name: str) -> str:
    """Collapse non-breaking spaces and repeated whitespace for stable matching."""
    return re.sub(r"\s+", " ", name.replace("\xa0", " ")).strip().lower()


def is_labour_csv_name(name: str) -> bool:
    return "fuerza de trabajo" in normalize_csv_name(name)


def fetch_file(
    file: CatalogFile,
    dest_dir: Path,
    *,
    fallback_csv: Path | None = None,
    method: Method = "http",
    manifest: Manifest | None = None,
) -> Path:
    """
    Download one DANE ZIP and extract CSV files.

    Stores the ZIP as ``{dest}/{survey_year}/{filename}`` and extracts to
    ``{dest}/{survey_year}/{stem}/``.
    """
    dest_dir.mkdir(parents=True, exist_ok=True)
    zip_path = file.zip_path(dest_dir)
    extract_dir = file.extract_dir(dest_dir)
    label = file.storage_key()

    with timing_context(method, label) as entry:
        if method == "fallback":
            if fallback_csv is None or not fallback_csv.is_file():
                raise FileNotFoundError("fallback_csv required when method='fallback'")
            extract_dir.mkdir(parents=True, exist_ok=True)
            out = extract_dir / fallback_csv.name
            shutil.copy2(fallback_csv, out)
            entry.bytes_downloaded = out.stat().st_size
            entry.fallback_used = True
            entry.notes = f"copied from {fallback_csv}"
        else:
            _validate_url_is_download_link(file.url)
            zip_path.parent.mkdir(parents=True, exist_ok=True)
            _download_url(file.url, zip_path)
            entry.bytes_downloaded = zip_path.stat().st_size
            out = _extract_csvs(zip_path, extract_dir)

        if manifest is not None:
            manifest.append(entry)
        return out


def _validate_url_is_download_link(url: str) -> None:
    if "/download/" not in url:
        raise ValueError(
            "That URL looks like a catalog page, not a data file. "
            "Open get-microdata, click Descargar on a file row, "
            "and use the link that contains /download/."
        )


def _download_url(url: str, dest: Path, timeout: int = 600) -> None:
    with requests.get(url.strip(), stream=True, timeout=timeout) as resp:
        resp.raise_for_status()
        with dest.open("wb") as fh:
            for chunk in resp.iter_content(chunk_size=1 << 20):
                if chunk:
                    fh.write(chunk)
    with dest.open("rb") as fh:
        magic = fh.read(4)
    if magic[:2] != b"PK":
        raise zipfile.BadZipFile(
            f"Downloaded file is not a ZIP (got {magic!r}). "
            "You likely used the catalog page URL instead of a Descargar link."
        )


def _extract_csvs(zip_path: Path, dest_dir: Path) -> Path:
    """Extract CSV members; handle flat CSVs and nested ``CSV.zip`` layouts."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "r") as zf:
        names = zf.namelist()
        csv_members = [n for n in names if n.lower().endswith(".csv")]
        nested_csv_zip = next(
            (n for n in names if re.fullmatch(r"csv\s*\d*\.zip", Path(n).name, re.I)),
            None,
        )

        if nested_csv_zip and not csv_members:
            inner_bytes = zf.read(nested_csv_zip)
            inner_path = dest_dir / "_csv_inner.zip"
            inner_path.write_bytes(inner_bytes)
            try:
                return _extract_csvs(inner_path, dest_dir)
            finally:
                inner_path.unlink(missing_ok=True)

        if not csv_members:
            raise ValueError(
                f"No CSV files in {zip_path.name}. Top-level entries: "
                f"{[Path(n).name for n in names[:8]]}"
            )

        labour_path: Path | None = None
        for name in csv_members:
            target = dest_dir / Path(name).name
            with zf.open(name) as src, target.open("wb") as dst:
                shutil.copyfileobj(src, dst)
            if is_labour_csv_name(name):
                labour_path = target
        if labour_path is None:
            raise ValueError(
                "No labour-force CSV (name contains 'fuerza de trabajo') in "
                f"{zip_path.name}. Found: {[Path(n).name for n in csv_members]}"
            )
    return labour_path
