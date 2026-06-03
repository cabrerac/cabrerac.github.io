"""Raw GEIH CSV → course Parquet (columns per spine-spec.md). Stub for L3."""

from __future__ import annotations

from pathlib import Path


def harmonise_raw_dir(raw_dir: Path, out_dir: Path) -> None:
    """
    Convert extracted CSVs under ``raw_dir`` to partitioned Parquet under ``out_dir``.

    Column mapping from ``work-space/teaching/big-data/planning/spine-spec.md``.
    Not implemented — groups use raw CSV in L1–L2; L3 introduces Parquet.
    """
    raise NotImplementedError(
        "harmonise_raw_dir is planned for L3. See spine-spec.md and geih_build README."
    )
