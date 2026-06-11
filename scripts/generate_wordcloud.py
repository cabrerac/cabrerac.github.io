"""Generate a word cloud PNG from any set of words.

Reusable across lectures: pass your own terms via --input, or free text via
--text. With no input it falls back to the built-in example set.

Input file formats (auto-detected by extension, comments with '#' allowed):
  * .json            -> {"term": weight, ...}
  * .txt / .md / .csv-> one entry per line, "term ; weight" (also ',' ':' '\\t');
                        weight optional (defaults to 1.0)
  * with --text      -> the file is treated as free prose; word frequencies
                        (and 2-word collocations) are counted automatically

Examples:
  python scripts/generate_wordcloud.py -o out.png -i words.txt
  python scripts/generate_wordcloud.py -o out.png -i notes.md --text
  python scripts/generate_wordcloud.py            # built-in example -> default path
"""
import argparse
import json
import re
from pathlib import Path

from wordcloud import WordCloud

# Palette taken from the deck SVGs (blue / green / orange / purple / teal).
DEFAULT_PALETTE = ["#2f5597", "#548235", "#c55a11", "#7030a0", "#1f6f8b"]

DEFAULT_OUTPUT = "assets/media/images/26-udenar-big-data/week1-wordcloud.png"

# Built-in fallback only. Real word sets should come from --input.
EXAMPLE_FREQUENCIES = {
    "más datos ≠ conocimiento": 9.0, "representatividad": 8.0, "sesgos": 6.5,
    "asimetría del poder": 6.5, "contexto": 6.0, "problema-first": 6.0,
    "ética": 6.0, "OSM": 5.5, "DANE": 5.0, "fairness": 5.0, "accountability": 5.0,
    "validez": 4.5, "calidad": 4.5, "datos públicos": 4.5, "discriminación": 4.0,
    "mitigación": 4.0, "desigualdad": 4.0, "raw data": 4.0, "cooperación": 4.0,
    "colaborativo": 3.5, "confiabilidad": 3.5, "instituciones": 3.5,
    "conocimiento": 3.5, "estadística": 3.5, "¿quién se beneficia?": 3.5,
    "responsabilidad": 3.0, "los datos no hablan solos": 3.0,
    "dos regímenes de datos": 3.0,
}

# A line is "term" or "term <delim> weight"; only a trailing number is a weight.
_WEIGHTED_LINE = re.compile(r"^(?P<term>.+?)\s*[;,:\t]\s*(?P<weight>\d+(?:\.\d+)?)\s*$")


def _palette_color_func(palette):
    def _color(word, **kwargs):
        return palette[sum(ord(c) for c in word) % len(palette)]
    return _color


def parse_frequencies(path: Path) -> dict:
    """Parse a term/weight file (.json or delimited lines)."""
    if path.suffix.lower() == ".json":
        return {str(k): float(v) for k, v in json.loads(path.read_text(encoding="utf-8")).items()}

    freqs = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        m = _WEIGHTED_LINE.match(line)
        if m:
            freqs[m.group("term")] = float(m.group("weight"))
        else:
            freqs[line] = 1.0
    return freqs


def build_wordcloud(frequencies=None, *, text=None, out_path: Path,
                    width=1600, height=1000, palette=None,
                    background="white", max_font_size=240) -> Path:
    palette = palette or DEFAULT_PALETTE
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    wc = WordCloud(
        width=width, height=height, background_color=background, mode="RGBA",
        prefer_horizontal=0.85, relative_scaling=0.5, margin=6,
        max_font_size=max_font_size, min_font_size=14, random_state=7,
        collocations=bool(text), color_func=_palette_color_func(palette),
    )
    if text is not None:
        wc.generate(text)
    else:
        wc.generate_from_frequencies(frequencies)
    wc.to_file(str(out_path))
    return out_path


def main():
    ap = argparse.ArgumentParser(description="Generate a word cloud PNG from any set of words.")
    ap.add_argument("-o", "--output", default=DEFAULT_OUTPUT, help="output PNG path")
    ap.add_argument("-i", "--input", help="term/weight file (.json or delimited lines)")
    ap.add_argument("--text", action="store_true", help="treat --input as free prose")
    ap.add_argument("--width", type=int, default=1600)
    ap.add_argument("--height", type=int, default=1000)
    ap.add_argument("--background", default="white", help="background colour or 'transparent'")
    ap.add_argument("--palette", help="comma-separated hex colours, overrides default")
    args = ap.parse_args()

    palette = args.palette.split(",") if args.palette else None
    background = None if args.background == "transparent" else args.background

    text = freqs = None
    if args.input:
        content = Path(args.input)
        if args.text:
            text = content.read_text(encoding="utf-8")
        else:
            freqs = parse_frequencies(content)
    else:
        freqs = EXAMPLE_FREQUENCIES
        print("[INFO] No --input given; using built-in example word set.")

    saved = build_wordcloud(
        frequencies=freqs, text=text, out_path=args.output,
        width=args.width, height=args.height, palette=palette, background=background,
    )
    print(f"Saved word cloud: {saved}")


if __name__ == "__main__":
    main()
