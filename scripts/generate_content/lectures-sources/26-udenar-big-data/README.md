# Lecture sources — 26-udenar-big-data

One source file per **lecture** → lecture page + slides + Colab notebook via `scripts/generate_content/generate_content.py`.

**Lecture order = AA-rec (ethics-first):** L1 intro → **L2 ethics + governance foundations** → L3 storage → L4 processing → L5 ingestion → L6 analytics + viz (with governance-in-practice synthesis). Operational governance lives as hooks in L3–L6 plus project rubric P3.

**Delivery rhythm (Saturdays 1–3):** one shared **07:00–13:00 Colombia / 13:00–19:00 UK** block per Saturday covering both lectures of the day, after each lecture's **~2 h async video** (V1 theory ~1 h + V2 lab demo ~1 h) released earlier in the week. See `work-space/teaching/big-data/planning/session-plan.md`.

| Source file | Session | Date (CO) | Notes |
|-------------|---------|-----------|-------|
| `diagnostic` | 0 — Saturday 0 | Fri 29 May 2026 | Intake baseline (not one of the 8 lectures); async; not OCARA contact |
| `l1-introduction` | 1 — Sat 1 morning of day | Sat 6 Jun 2026 | Stub |
| `l2-ethics-governance` | 2 — Sat 1 afternoon of day | Sat 6 Jun 2026 | **New ethics-first lecture (AA-rec)** |
| `l3-storage` | 3 — Sat 2 morning of day | Sat 13 Jun 2026 | Was `l2-storage`; ethics hook to L2 |
| `l4-processing` | 4 — Sat 2 afternoon of day | Sat 13 Jun 2026 | Was `l3-processing`; ethics hook to L2 |
| `l5-ingestion` | 5 — Sat 3 morning of day | Sat 20 Jun 2026 | Was `l4-ingestion`; ethics hook to L2 |
| `l6-analytics` | 6 — Sat 3 afternoon of day | Sat 20 Jun 2026 | Was `l5-analytics`; closes governance synthesis |
| `l7-integration` | 7 — async only | week of 22 Jun 2026 | Short integration video; no Saturday sync; project week 22–26 Jun |
| `l8-final-project` | 8 — Sat 4 (single 6 h block) | Sat 27 Jun 2026 | Live presentations only (07:00–13:00 CO) |

Generate one lecture (from repo root):

```bash
python scripts/generate_content/generate_content.py 26-udenar-big-data/l2-ethics-governance
```

Set `visible: true` in each source front matter when ready to publish.

**Website is the canonical materials hub.** Moodle and email are support channels for announcements and submissions.

**Notebook language:** Student practice notebooks (L1–L8, diagnostic) are authored in **Spanish** in the markdown sources; regenerate `.ipynb` after edits.

**Naming:** `lecture_code` matches the source filename stem (e.g. `l3-storage`). Homework artefacts use `L{n}_output` (see planning docs).
