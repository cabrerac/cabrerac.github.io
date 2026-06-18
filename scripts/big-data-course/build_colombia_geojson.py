"""Build a lightweight Colombia departments GeoJSON asset for the Big Data course.

Source: DANE Marco Geoestadistico Nacional (MGN 2021), department layer, converted
to GeoJSON and published by @macortesgu. We download it, simplify the geometry so the
file is small enough to ship and download in a lab, and keep only two properties:

    - ``dpto``: integer DANE department code (joins to the curated GEIH aggregates).
    - ``dpto_nombre``: department name (our own clean table, avoids encoding issues).

The result feeds the L6 / week-3-group choropleth (employment by department).

Run once (offline) to (re)generate the asset:

    python scripts/big-data-course/build_colombia_geojson.py

Requires ``shapely`` (build-time only; the notebooks just read the resulting GeoJSON).
"""

from __future__ import annotations

import json
import urllib.request
from pathlib import Path

from shapely.geometry import mapping, shape

SOURCE_URL = (
    "https://gist.githubusercontent.com/macortesgu/"
    "87b5aa829ece985e8887f8eac013cee5/raw/MGN2021_DPTO.geo.json"
)
HEADERS = {"User-Agent": "UDENAR-BigData-2026/1.0 (course asset build)"}

OUT_PATH = (
    Path(__file__).resolve().parents[2]
    / "assets"
    / "data"
    / "26-udenar-big-data"
    / "colombia_departments.geojson"
)

# Simplify tolerance in degrees (~0.004 deg = ~450 m) and coordinate rounding.
SIMPLIFY_TOLERANCE = 0.004
COORD_DECIMALS = 4

# DANE department code -> clean Spanish name (our source of truth for labels).
DPTO_NOMBRE: dict[int, str] = {
    5: "Antioquia",
    8: "Atlántico",
    11: "Bogotá, D.C.",
    13: "Bolívar",
    15: "Boyacá",
    17: "Caldas",
    18: "Caquetá",
    19: "Cauca",
    20: "Cesar",
    23: "Córdoba",
    25: "Cundinamarca",
    27: "Chocó",
    41: "Huila",
    44: "La Guajira",
    47: "Magdalena",
    50: "Meta",
    52: "Nariño",
    54: "Norte de Santander",
    63: "Quindío",
    66: "Risaralda",
    68: "Santander",
    70: "Sucre",
    73: "Tolima",
    76: "Valle del Cauca",
    81: "Arauca",
    85: "Casanare",
    86: "Putumayo",
    88: "Archipiélago de San Andrés, Providencia y Santa Catalina",
    91: "Amazonas",
    94: "Guainía",
    95: "Guaviare",
    97: "Vaupés",
    99: "Vichada",
}


def _round_coords(obj):
    """Recursively round coordinate floats to COORD_DECIMALS to shrink the file."""
    if isinstance(obj, float):
        return round(obj, COORD_DECIMALS)
    if isinstance(obj, list):
        return [_round_coords(x) for x in obj]
    if isinstance(obj, tuple):
        return tuple(_round_coords(x) for x in obj)
    return obj


def main() -> None:
    print(f"Downloading source GeoJSON...\n  {SOURCE_URL}")
    req = urllib.request.Request(SOURCE_URL, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=120) as r:
        src = json.loads(r.read().decode("utf-8"))
    print(f"  source features: {len(src.get('features', []))}")

    out_features = []
    seen_codes: set[int] = set()
    for feat in src.get("features", []):
        props = feat.get("properties", {})
        code = int(props["DPTO_CCDGO"])
        seen_codes.add(code)
        geom = shape(feat["geometry"]).simplify(
            SIMPLIFY_TOLERANCE, preserve_topology=True
        )
        out_geom = _round_coords(mapping(geom))
        out_features.append(
            {
                "type": "Feature",
                "properties": {
                    "dpto": code,
                    "dpto_nombre": DPTO_NOMBRE.get(code, props.get("DPTO_CNMBR", "")),
                },
                "geometry": out_geom,
            }
        )

    missing = set(DPTO_NOMBRE) - seen_codes
    extra = seen_codes - set(DPTO_NOMBRE)
    if missing:
        print(f"  WARNING: codes missing from source: {sorted(missing)}")
    if extra:
        print(f"  WARNING: codes not in name table: {sorted(extra)}")

    out = {"type": "FeatureCollection", "features": out_features}
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(
        json.dumps(out, ensure_ascii=False, separators=(",", ":")), encoding="utf-8"
    )
    size_kb = OUT_PATH.stat().st_size / 1024
    print(f"Wrote {OUT_PATH}")
    print(f"  features: {len(out_features)} | size: {size_kb:.0f} KB")


if __name__ == "__main__":
    main()
