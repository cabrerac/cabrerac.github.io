# Course documents: shared helpers

Helpers used by course scripts to build Word templates and session-plan PDFs.

| Module | Role |
|--------|------|
| [`docx_build.py`](docx_build.py) | python-docx helpers (`style_body`, `heading`, `para`, ...). Module-level paths default to the Big Data course; course scripts may override them. |
| [`session_plan_build.py`](session_plan_build.py) | Markdown session plan to HTML to PDF (PyMuPDF). The `## Regenerar este PDF` section is dropped from the PDF. |

Use from a course script:

```python
import sys
from pathlib import Path

sys.path.insert(0, str(REPO_ROOT / "scripts" / "course_docs"))
from session_plan_build import write_session_plan
```

Needs `python-docx` and `pymupdf`.
