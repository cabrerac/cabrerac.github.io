"""Add rel=noopener to lecture resource links and mark Back to course as internal."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "content" / "_lectures"
EXT = ' target="_blank" rel="noopener noreferrer"'


def fix(text: str) -> str:
    text = re.sub(r'target="_blank"(?!\s+rel=)', EXT, text)
    text = re.sub(
        r'(<a href="/teaching/[^"]+/")( class="course-nav__internal")?>Back to course</a>',
        r'\1 class="course-nav__internal">Back to course</a>',
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
