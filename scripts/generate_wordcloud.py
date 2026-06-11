"""Generate a word cloud PNG from a weighted list of terms.

Reusable helper for lecture slides (e.g. the week-1 discussion cloud).
Edit FREQUENCIES below or import build_wordcloud() with your own dict.

Usage:
    python scripts/generate_wordcloud.py <output_png>
"""
import sys
from pathlib import Path

from wordcloud import WordCloud

# Palette taken from the deck SVGs (blue / green / orange / purple).
PALETTE = ["#2f5597", "#548235", "#c55a11", "#7030a0", "#1f6f8b"]

# Week-1 readings plenary (Sat 6 Jun): students' own terms, weighted by how
# often each theme recurred across the five groups (sat-1-retrospective.md).
FREQUENCIES = {
    "más datos ≠ conocimiento": 9.0,
    "representatividad": 8.0,
    "sesgos": 6.5,
    "asimetría del poder": 6.5,
    "contexto": 6.0,
    "problema-first": 6.0,
    "ética": 6.0,
    "OSM": 5.5,
    "DANE": 5.0,
    "fairness": 5.0,
    "accountability": 5.0,
    "validez": 4.5,
    "calidad": 4.5,
    "datos públicos": 4.5,
    "discriminación": 4.0,
    "mitigación": 4.0,
    "desigualdad": 4.0,
    "raw data": 4.0,
    "cooperación": 4.0,
    "colaborativo": 3.5,
    "confiabilidad": 3.5,
    "instituciones": 3.5,
    "conocimiento": 3.5,
    "estadística": 3.5,
    "¿quién se beneficia?": 3.5,
    "responsabilidad": 3.0,
    "los datos no hablan solos": 3.0,
    "dos regímenes de datos": 3.0,
}


def _color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    idx = sum(ord(c) for c in word) % len(PALETTE)
    return PALETTE[idx]


def build_wordcloud(frequencies: dict, out_path: Path) -> Path:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    wc = WordCloud(
        width=1600, height=1000, background_color="white", mode="RGBA",
        prefer_horizontal=0.85, relative_scaling=0.5, margin=6,
        max_font_size=240, min_font_size=14, random_state=7,
        color_func=_color_func,
    )
    wc.generate_from_frequencies(frequencies)
    wc.to_file(str(out_path))
    return out_path


if __name__ == "__main__":
    default = "assets/media/images/26-udenar-big-data/week1-wordcloud.png"
    target = Path(sys.argv[1] if len(sys.argv) > 1 else default)
    saved = build_wordcloud(FREQUENCIES, target)
    print(f"Saved word cloud: {saved}")
