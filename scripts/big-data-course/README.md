# Big Data course: public data builders (26-udenar-big-data)

These scripts rebuild the small public data files used by the Big Data notebooks. They show where the published data came from.

| Script | Output |
|--------|--------|
| [`build_colombia_geojson.py`](build_colombia_geojson.py) | `assets/data/26-udenar-big-data/colombia_departments.geojson` (DANE MGN department layer, simplified) |
| [`build_osm_services.py`](build_osm_services.py) | `assets/data/26-udenar-big-data/osm_services_by_dpto.csv` (OpenStreetMap counts per department; cache in `.cache/`) |

```bash
python scripts/big-data-course/build_colombia_geojson.py
python scripts/big-data-course/build_osm_services.py
```

Course-specific tools (Word and PDF builders, grading, submission checks, notebook tests, the GEIH download package) are private and live outside the public repo. The shared document helpers are in [`scripts/course_docs/`](../course_docs/).
