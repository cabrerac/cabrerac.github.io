"""Build a cached OSM services-by-department CSV asset for the Big Data course.

For each Colombian department we count OpenStreetMap features (nodes + ways +
relations, ``nwr``) in three service categories, querying the Overpass API by the
department's ISO 3166-2 area code (more robust than relation ids):

    - ``health``:    amenity = hospital / clinic / doctors / pharmacy / health_centre
    - ``education``: amenity = school / college / university / kindergarten
    - ``commerce``:  any shop=* (broad retail/commerce proxy)

Output CSV columns: ``dpto, dpto_nombre, health, education, commerce, total``
(``total`` = sum of the three; the notebook derives shares from it).

Because Overpass is rate-limited and occasionally times out, every department/category
result is cached to ``.cache/osm_services_cache.json`` so re-runs resume instead of
restarting. The notebook ships this CSV as a fallback and only does a tiny live query
for one or two departments to demonstrate the technique.

Run once (offline) to (re)generate the asset:

    python scripts/big-data-course/build_osm_services.py
"""

from __future__ import annotations

import csv
import json
import time
from pathlib import Path

import requests

OVERPASS_HEADERS = {
    "User-Agent": "UDENAR-BigData-2026/1.0 (Universidad de Narino - Big Data elective)",
    "Accept": "application/json",
}
OVERPASS_ENDPOINTS = [
    "https://overpass-api.de/api/interpreter",
    "https://maps.mail.ru/osm/tools/overpass/api/interpreter",
]
OVERPASS_RETRY_PAUSE = 3.0
PAUSE_BETWEEN = 1.5

OUT_PATH = (
    Path(__file__).resolve().parents[2]
    / "assets"
    / "data"
    / "26-udenar-big-data"
    / "osm_services_by_dpto.csv"
)
CACHE_PATH = Path(__file__).resolve().parent / ".cache" / "osm_services_cache.json"

# DANE department code -> (clean name, ISO 3166-2 code).
DPTO_INFO: dict[int, tuple[str, str]] = {
    5: ("Antioquia", "CO-ANT"),
    8: ("Atlántico", "CO-ATL"),
    11: ("Bogotá, D.C.", "CO-DC"),
    13: ("Bolívar", "CO-BOL"),
    15: ("Boyacá", "CO-BOY"),
    17: ("Caldas", "CO-CAL"),
    18: ("Caquetá", "CO-CAQ"),
    19: ("Cauca", "CO-CAU"),
    20: ("Cesar", "CO-CES"),
    23: ("Córdoba", "CO-COR"),
    25: ("Cundinamarca", "CO-CUN"),
    27: ("Chocó", "CO-CHO"),
    41: ("Huila", "CO-HUI"),
    44: ("La Guajira", "CO-LAG"),
    47: ("Magdalena", "CO-MAG"),
    50: ("Meta", "CO-MET"),
    52: ("Nariño", "CO-NAR"),
    54: ("Norte de Santander", "CO-NSA"),
    63: ("Quindío", "CO-QUI"),
    66: ("Risaralda", "CO-RIS"),
    68: ("Santander", "CO-SAN"),
    70: ("Sucre", "CO-SUC"),
    73: ("Tolima", "CO-TOL"),
    76: ("Valle del Cauca", "CO-VAC"),
    81: ("Arauca", "CO-ARA"),
    85: ("Casanare", "CO-CAS"),
    86: ("Putumayo", "CO-PUT"),
    88: ("Archipiélago de San Andrés, Providencia y Santa Catalina", "CO-SAP"),
    91: ("Amazonas", "CO-AMA"),
    94: ("Guainía", "CO-GUA"),
    95: ("Guaviare", "CO-GUV"),
    97: ("Vaupés", "CO-VAU"),
    99: ("Vichada", "CO-VID"),
}

# category -> Overpass tag filter clause applied to nwr(...)
CATEGORY_FILTERS: dict[str, str] = {
    "health": '["amenity"~"^(hospital|clinic|doctors|pharmacy|health_centre)$"]',
    "education": '["amenity"~"^(school|college|university|kindergarten)$"]',
    "commerce": '["shop"]',
}


def overpass_post(query: str, *, timeout: int = 90) -> requests.Response:
    """POST an Overpass QL query, retrying across mirrors on rate-limit/timeout."""
    last_resp = None
    for url in OVERPASS_ENDPOINTS:
        for attempt in range(2):
            try:
                r = requests.post(
                    url, data={"data": query}, headers=OVERPASS_HEADERS, timeout=timeout
                )
                last_resp = r
                if r.status_code == 200:
                    return r
                if r.status_code in (429, 502, 503, 504):
                    time.sleep(OVERPASS_RETRY_PAUSE * (attempt + 1))
                    continue
                r.raise_for_status()
            except requests.RequestException:
                time.sleep(OVERPASS_RETRY_PAUSE * (attempt + 1))
                continue
    if last_resp is not None:
        last_resp.raise_for_status()
    raise requests.HTTPError("Overpass: no useful response after retries.")


def count_category(iso_code: str, filter_clause: str) -> int:
    """Count nwr features matching ``filter_clause`` inside an ISO-3166-2 area."""
    query = f"""
[out:json][timeout:90];
area["ISO3166-2"="{iso_code}"]->.a;
nwr{filter_clause}(area.a);
out count;
"""
    data = overpass_post(query).json()
    elements = data.get("elements", [])
    return int(elements[0]["tags"]["total"]) if elements else 0


def load_cache() -> dict[str, int]:
    if CACHE_PATH.is_file():
        return json.loads(CACHE_PATH.read_text(encoding="utf-8"))
    return {}


def save_cache(cache: dict[str, int]) -> None:
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CACHE_PATH.write_text(json.dumps(cache, indent=2), encoding="utf-8")


def main() -> None:
    cache = load_cache()
    rows = []
    total_queries = len(DPTO_INFO) * len(CATEGORY_FILTERS)
    done = 0
    for code, (nombre, iso) in DPTO_INFO.items():
        counts: dict[str, int] = {}
        for category, clause in CATEGORY_FILTERS.items():
            key = f"{iso}:{category}"
            if key in cache:
                counts[category] = cache[key]
            else:
                counts[category] = count_category(iso, clause)
                cache[key] = counts[category]
                save_cache(cache)
                time.sleep(PAUSE_BETWEEN)
            done += 1
            print(
                f"[{done:>3}/{total_queries}] {nombre} ({iso}) {category}: "
                f"{counts[category]}"
            )
        rows.append(
            {
                "dpto": code,
                "dpto_nombre": nombre,
                "health": counts["health"],
                "education": counts["education"],
                "commerce": counts["commerce"],
                "total": counts["health"] + counts["education"] + counts["commerce"],
            }
        )

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUT_PATH.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f, fieldnames=["dpto", "dpto_nombre", "health", "education", "commerce", "total"]
        )
        writer.writeheader()
        writer.writerows(rows)
    print(f"\nWrote {OUT_PATH} ({len(rows)} departments)")


if __name__ == "__main__":
    main()
