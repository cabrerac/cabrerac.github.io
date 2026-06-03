"""Record how long data access takes — used for Vs comparisons in notebooks."""

from __future__ import annotations

import json
import time
from contextlib import contextmanager
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Iterator


@dataclass
class AccessTiming:
    method: str
    slice_label: str
    seconds: float
    bytes_downloaded: int = 0
    notes: str = ""
    fallback_used: bool = False


@dataclass
class Manifest:
    entries: list[AccessTiming] = field(default_factory=list)

    def append(self, entry: AccessTiming) -> None:
        self.entries.append(entry)

    def write_json(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps([asdict(e) for e in self.entries], indent=2),
            encoding="utf-8",
        )


@contextmanager
def timing_context(method: str, slice_label: str) -> Iterator[AccessTiming]:
    start = time.perf_counter()
    entry = AccessTiming(method=method, slice_label=slice_label, seconds=0.0)
    try:
        yield entry
    finally:
        entry.seconds = round(time.perf_counter() - start, 3)
