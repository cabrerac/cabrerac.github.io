"""Remove redundant Back to course links from lecture resource bars."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "content" / "_lectures"

BACK = re.compile(
    r'\s*&nbsp;\|\s*<a href="/teaching/[^"]+/"(?: class="course-nav__internal")?>Back to course</a>',
    re.IGNORECASE,
)
BACK_TRAILING = re.compile(
    r'<a href="/teaching/[^"]+/"(?: class="course-nav__internal")?>Back to course</a>',
    re.IGNORECASE,
)


def fix(text: str) -> str:
    text = BACK.sub("", text)
    text = BACK_TRAILING.sub("", text)
    text = re.sub(r"(?:\s*&nbsp;\|\s*)+\s*(?=</p>)", "", text)
    text = re.sub(
        r'<div class="lecture-resources">\s*<p>\s*</p>\s*</div>\s*',
        "",
        text,
    )
    return text


def main() -> None:
    for path in ROOT.rglob("*.md"):
        original = path.read_text(encoding="utf-8")
        updated = fix(original)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            print(f"updated {path.relative_to(ROOT.parent.parent)}")


if __name__ == "__main__":
    main()
