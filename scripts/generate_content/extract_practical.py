"""Extract inline NOTEBOOK blocks from big-data lecture sources into practical.md snippets."""
from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SOURCES = REPO / "scripts/generate_content/lectures-sources/26-udenar-big-data"
SNIPPETS = REPO / "_includes/_snippets/26-udenar-big-data"

NOTEBOOK_BLOCK = re.compile(
    r"<!-- NOTEBOOK: -->.*?<!-- end NOTEBOOK: -->",
    re.DOTALL,
)


def extract(source: Path) -> bool:
    text = source.read_text(encoding="utf-8")
    match = NOTEBOOK_BLOCK.search(text)
    if not match:
        return False

    stem = source.stem
    dest_dir = SNIPPETS / stem
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / "practical.md"
    dest.write_text(match.group(0).strip() + "\n", encoding="utf-8")

    include_line = f"{{% include _snippets/26-udenar-big-data/{stem}/practical.md %}}\n"
    updated = NOTEBOOK_BLOCK.sub(include_line, text, count=1)
    source.write_text(updated, encoding="utf-8")
    print(f"{source.name} -> {dest.relative_to(REPO)}")
    return True


def main() -> None:
    changed = 0
    for source in sorted(SOURCES.glob("*.md")):
        if source.name == "README.md":
            continue
        if extract(source):
            changed += 1
    print(f"done ({changed} files)")


if __name__ == "__main__":
    main()
