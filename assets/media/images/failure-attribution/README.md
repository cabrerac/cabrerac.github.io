# Failure attribution reading-group talk figures

PNG crops from Zhang et al., [arXiv:2505.00212](https://arxiv.org/abs/2505.00212), for `internal-mas-failure-attribution` slides.

| File | Paper source | Slide |
|------|--------------|-------|
| `title-abstract.png` | Title + abstract | The paper |
| `fig1-overview.png` | Figure 1 | Failure attribution |
| `fig9-example.png` | Figure 9 | A failure instance |
| `fig2-annotation.png` | Figure 2 | Annotation is hard |
| `table1-results.png` | Table 1 | Who vs when |
| `fig4-context-length.png` | Figure 4 | Context length |
| `fig6-histogram.png` | Figure 6 | A statistical view |

Regenerate slides:

```bash
python scripts/generate_content/generate_content.py --talk internal-mas-failure-attribution
```