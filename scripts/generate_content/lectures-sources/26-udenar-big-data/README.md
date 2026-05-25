# Lecture sources — 26-udenar-big-data

One source file per **lecture** → lecture page + slides + Colab notebook via `scripts/generate_content/generate_content.py`.

| Source file | Session | Date (CO) | Notes |
|-------------|---------|-----------|-------|
| `diagnostic` | 0 — Saturday 0 | Fri 29 May 2026 | Intake baseline (not one of the 8 lectures) |
| `l1-introduction` | 1 AM | Sat 6 Jun 2026 | Stub |
| `l2-storage` | 2 PM | Sat 6 Jun 2026 | Stub |
| `l3-processing` | 3 AM | Sat 13 Jun 2026 | Stub |
| `l4-ingestion` | 4 PM | Sat 13 Jun 2026 | Stub |
| `l5-analytics` | 5 AM | Sat 20 Jun 2026 | Stub |
| `l6-governance` | 6 PM | Sat 20 Jun 2026 | Stub |
| `l7-integration` | 7 AM | Sat 27 Jun 2026 | Stub |
| `l8-final-project` | 8 PM | Sat 27 Jun 2026 | Stub |

Generate one lecture (from repo root):

```bash
python scripts/generate_content/generate_content.py 26-udenar-big-data/l1-introduction
```

Set `visible: true` in each source front matter when ready to publish.

**Website is the canonical materials hub.** Moodle and email are support channels for announcements and submissions.

**Naming:** `lecture_code` matches the source filename stem (e.g. `l2-storage`). Homework artefacts use `L{n}_output` (see planning docs).
