import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "content" / "_lectures"
TRAILING = re.compile(r"\s*&nbsp;\|\s*&nbsp;\s*(?=\r?\n)")


def main() -> None:
    for path in ROOT.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        updated = TRAILING.sub("", text)
        updated = re.sub(r'  target="_blank"', ' target="_blank"', updated)
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            print(path.name)


if __name__ == "__main__":
    main()
