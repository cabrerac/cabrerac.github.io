"""Build state for pause/resume access downloads."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path

from geih_build.dane_catalog import CatalogFile
from geih_build.fetch import is_labour_csv_name


class FileStatus(str, Enum):
    PENDING = "pending"
    DOWNLOADED = "downloaded"
    EXTRACTED = "extracted"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class FileRecord:
    label: str
    filename: str = ""
    file_id: int | None = None
    catalog_id: int | None = None
    survey_year: int | None = None
    status: FileStatus = FileStatus.PENDING
    zip_path: str | None = None
    extract_dir: str | None = None
    error: str | None = None
    bytes_downloaded: int = 0


@dataclass
class BuildState:
    plan_name: str = ""
    files: dict[str, FileRecord] = field(default_factory=dict)

    @classmethod
    def load(cls, path: Path) -> BuildState:
        if not path.is_file():
            return cls()
        data = json.loads(path.read_text(encoding="utf-8"))
        state = cls(plan_name=data.get("plan_name", ""))
        rows = data.get("files") or data.get("slices") or {}
        for label, row in rows.items():
            status_val = row.get("status", FileStatus.PENDING.value)
            state.files[label] = FileRecord(
                label=label,
                filename=row.get("filename", ""),
                file_id=row.get("file_id"),
                catalog_id=row.get("catalog_id"),
                survey_year=row.get("survey_year"),
                status=FileStatus(status_val),
                zip_path=row.get("zip_path"),
                extract_dir=row.get("extract_dir"),
                error=row.get("error"),
                bytes_downloaded=int(row.get("bytes_downloaded", 0)),
            )
        return state

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "plan_name": self.plan_name,
            "files": {k: asdict(v) for k, v in self.files.items()},
        }
        for row in payload["files"].values():
            row["status"] = row["status"].value if isinstance(row["status"], FileStatus) else row["status"]
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def ensure_file(self, file: CatalogFile) -> FileRecord:
        label = file.storage_key()
        if label not in self.files:
            self.files[label] = FileRecord(
                label=label,
                filename=file.filename,
                file_id=file.file_id,
                catalog_id=file.catalog_id,
                survey_year=file.survey_year,
            )
        return self.files[label]


def file_extract_complete(dest_dir: Path, file: CatalogFile) -> bool:
    """True if extracted CSVs look complete for this DANE file."""
    extract_dir = file.extract_dir(dest_dir)
    if not extract_dir.is_dir():
        return False
    csvs = list(extract_dir.glob("*.CSV")) + list(extract_dir.glob("*.csv"))
    if not csvs:
        return False
    labour = [p for p in csvs if is_labour_csv_name(p.name)]
    return bool(labour)


def file_zip_path(dest_dir: Path, file: CatalogFile) -> Path:
    return file.zip_path(dest_dir)


def file_zip_valid(zip_path: Path) -> bool:
    if not zip_path.is_file() or zip_path.stat().st_size < 1024:
        return False
    with zip_path.open("rb") as fh:
        return fh.read(2) == b"PK"
