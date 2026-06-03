---
course_code: 26-udenar-big-data
title: L1 — Acceso grupal GEIH 2022–2025
description: Group Colab — GEIH dataset 2022–2025 download, manifest, contribution log (notebook only; linked from l1-introduction lecture page).
session: 1
start_time: async
end_time: async
hours: 2
author: Christian Cabrera Jojoa
email: chc79@cam.ac.uk
position: Assistant Research Professor
department: Department of Computer Science and Technology
institution: University of Cambridge
layout: lecture
lecture_code: l1-introduction-group
lecture_date: 06/06/2026
visible: false
skip_slides: true
skip_lecture_page: true
notebook_language: es
notebook_title: Acceso grupal GEIH 2022–2025
notebook_description: Cuaderno canónico del grupo para la Lección 1. Descarga del conjunto de datos GEIH 2022–2025, manifiesto y registro de contribución. Entrega en la sección **Tarea grupal**. Plantillas Word en la página pública de la lección.
---

<!-- NOTEBOOK: -->

## Instrucciones

**Propósito.** Este cuaderno es el **Colab canónico del grupo** para la Lección 1. Descargan el conjunto de datos **GEIH 2022–2025** con el mismo patrón que en el [cuaderno individual L1](https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-big-data/l1-introduction.ipynb): get-microdata → descargar ZIP → extraer CSV → `manifest.json`.

**Requisito.** Complete primero el cuaderno individual (al menos Partes 1 y 2). Aquí **adaptan** ese código al dataset 2022–2025. No copie celdas sin entenderlas.

Lea la [definición del proyecto (PDF)](/assets/documents/26-udenar-big-data/definicion-proyecto-big-data.pdf) con su grupo antes de la sesión.

**Materiales:** [página de la Lección 1](https://cabrerac.github.io/teaching/26-udenar-big-data/l1-introduction/) (sección *Resources*).

**Entrega Moodle (miércoles 10 jun):** ZIP `l1-introduction-<nombre-grupo>.zip` con este `.ipynb` y `manifest.json`.

**Catálogos DANE por año:** 2022 → `771`, 2023 → `782`, 2024 → `819`, 2025 → `853`.

---

## Configuración

Copie del cuaderno individual y adapte:

- `download_zip`, `extract_csvs`, `list_catalog_downloads` (y `access_file` si la usó en Parte 2)
- `CATALOG_BY_YEAR = {2022: 771, 2023: 782, 2024: 819, 2025: 853}`
- `DATASET_YEARS = [2022, 2023, 2024, 2025]` y carpetas bajo `data/raw/{año}/`
- En `access_file`, mantenga **`skip_if_exists=True`** si re-ejecuta el cuaderno (evita bajar otra vez meses ya extraídos)

```python
# SU CÓDIGO — imports, constantes y funciones reutilizadas del cuaderno individual

```

---

## Descargar 2022–2025

Una petición get-microdata por año. Bucle sobre los archivos mensuales. Puede tomar un tiempo y ocupar **varios GB**. Planifique red y disco.

Al terminar debe existir:

- `manifest_entries`: lista de diccionarios (una fila por ZIP descargado)
- `manifest_path`: `Path("manifest.json")` escrito con su función `write_manifest`

```python
# SU CÓDIGO — bucle por año y mes; append a manifest_entries; write_manifest al final

```

**Comprobar:**

```python
assert manifest_path.is_file(), "Falta manifest.json"
assert len(manifest_entries) >= 40, "Se esperan ~48 archivos (12 meses × 4 años)"
assert manifest_entries[0].get("bytes_downloaded", 0) > 0
print("Descarga 2022–2025: OK")
```

---

## Exploración inicial del dataset y del proceso de descarga

Replique las ideas de la **Parte 3** del cuaderno individual, adaptadas al dataset grupal. No hace falta analizar los 48 meses en detalle: resuma con el manifiesto y mire **un** CSV de muestra.

### Paso 1 — Resumen desde `manifest.json`

```python
# SU CÓDIGO — cargue manifest.json en un DataFrame (pandas)
# Columnas útiles: survey_year, filename, seconds, bytes_downloaded, notes
# Imprima: total MB, total segundos, filas por año (groupby survey_year)

```

**Comprobar:**

```python
assert len(manifest_df) >= 40
assert manifest_df["bytes_downloaded"].sum() > 0
print("Exploración, Paso 1 — manifiesto: OK")
```

---

### Paso 2 — Vista de un CSV de muestra

Elija **un** mes ya extraído (p. ej. enero 2024 en `data/raw/2024/Ene_2024/`). Abra `Fuerza de trabajo.CSV` con `sep=";"` y `encoding="latin-1"`.

```python
# SU CÓDIGO — read_csv, filas/columnas, value_counts de DPTO (top 10)

```

**Comprobar:**

```python
assert n_rows > 10_000, "Se espera un mes nacional"
assert "DPTO" in df.columns
print("Exploración, Paso 2 — CSV muestra: OK")
```

---

### Paso 3 — Gráfico del proceso de descarga

```python
# SU CÓDIGO — gráfico simple, p. ej. MB total por survey_year (barra)
# Puede adaptar matplotlib de la Parte 3 del cuaderno individual

```

**Comprobar:**

```python
assert "survey_year" in manifest_df.columns
print("Exploración, Paso 3 — gráfico: OK")
```

---

## Registro de contribución (grupo)

Cada integrante añade una línea. Indique el **escriba de L1**, quien consolida este Colab y la entrega en Moodle.

```python
contribution_log = """
- Nombre 1 — ...
- Nombre 2 — ...
- Nombre 3 — ...
- Nombre 4 — ...
Escriba L1: ...
"""
print(contribution_log)
```

---

## Tarea grupal (Moodle)

ZIP **`l1-introduction-<nombre-grupo>.zip`** hasta el **miércoles 10 de junio de 2026**:

| Archivo | Descripción |
|---------|-------------|
| `l1-introduction-<nombre-grupo>.ipynb` | Este cuaderno ejecutado (Colab canónico del grupo) |
| `manifest.json` | Un registro por archivo DANE descargado |

La **reflexión individual** (`l1-reflexion-<nombre>.pdf`) se entrega **por separado** el **jueves 11 jun**.

Los **requerimientos del proyecto** (`project_requirements.pdf`) se discuten en la **semana 2** (ver definición del proyecto en la página de la lección 1).

<!-- end NOTEBOOK: -->
