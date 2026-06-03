---
course_code: 26-udenar-big-data
title: Semana 1 — Acceso GEIH y ética (grupo)
description: Group Colab — GEIH 2022–2025 download, ethics audit, OSM POI by department, contribution log. Consolidates L1 + L2 homework.
session: 1
start_time: async
end_time: async
hours: 4
author: Christian Cabrera Jojoa
email: chc79@cam.ac.uk
position: Assistant Research Professor
department: Department of Computer Science and Technology
institution: University of Cambridge
layout: lecture
lecture_code: week-1-group
lecture_date: 06/06/2026
visible: false
skip_slides: true
skip_lecture_page: true
notebook_language: es
notebook_title: Semana 1 — acceso GEIH y ética (grupo)
notebook_description: Cuaderno canónico del grupo para la semana 1 (L1 + L2). Descarga GEIH 2022–2025, auditoría ética, OSM por departamento y registro de contribución. Entrega en **Tarea grupal**.
---

<!-- NOTEBOOK: -->

## Instrucciones

**Propósito.** Cuaderno **canónico del grupo** para la **semana 1** (Lecciones 1 y 2). Parte A: descargar GEIH **2022–2025** (mismo patrón que el [cuaderno individual L1](https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-big-data/l1-introduction.ipynb)). Parte B: auditoría ética y enlace GEIH + OSM (adaptando el [cuaderno individual L2](https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-big-data/l2-ethics-governance.ipynb)).

**Requisito.** Complete primero los cuadernos individuales L1 (Partes 1 y 2) y L2 (Partes 1 a 4). Aquí **adaptan** ese código. No copie celdas sin entenderlas.

Lea la [definición del proyecto (PDF)](/assets/documents/26-udenar-big-data/project-definition-big-data.pdf) con su grupo (también en la [página L1](/teaching/26-udenar-big-data/l1-introduction/)).

**Materiales:** páginas de [L1](https://cabrerac.github.io/teaching/26-udenar-big-data/l1-introduction/) y [L2](https://cabrerac.github.io/teaching/26-udenar-big-data/l2-ethics-governance/) (sección *Resources*).

**Entrega Moodle (miércoles 10 jun):** ZIP `week-1-<group_id>.zip` con `notebook-week-1-group-<group_id>.ipynb` (renombre este cuaderno al exportar), `manifest.json` y `osm_poi_by_dpto.csv`.

**Catálogos DANE por año:** 2022 → `771`, 2023 → `782`, 2024 → `819`, 2025 → `853`.

---

# Parte A — Access GEIH 2022–2025 (L1)

## Configuración

Copie del cuaderno individual L1 y adapte:

- `download_zip`, `extract_csvs`, `list_catalog_downloads` (y `access_file` si la usó en Parte 2)
- `CATALOG_BY_YEAR = {2022: 771, 2023: 782, 2024: 819, 2025: 853}`
- `DATASET_YEARS = [2022, 2023, 2024, 2025]` y carpetas bajo `data/raw/{año}/`
- En `access_file`, mantenga **`skip_if_exists=True`** si re-ejecuta el cuaderno

```python
# SU CÓDIGO — imports, constantes y funciones reutilizadas del cuaderno individual L1

```

---

## Descargar 2022–2025

Una petición get-microdata por año. Bucle sobre los archivos mensuales. Puede tomar un tiempo y ocupar **varios GB**.

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

## Exploración inicial (L1)

Replique las ideas de la **Parte 3** del cuaderno individual L1. Resuma con el manifiesto y mire **un** CSV de muestra.

### Paso 1 — Resumen desde `manifest.json`

```python
# SU CÓDIGO — cargue manifest.json en un DataFrame (pandas)
# Imprima: total MB, total segundos, filas por año (groupby survey_year)

```

**Comprobar:**

```python
assert len(manifest_df) >= 40
assert manifest_df["bytes_downloaded"].sum() > 0
print("Exploración L1, Paso 1 — manifiesto: OK")
```

---

### Paso 2 — Vista de un CSV de muestra

Elija **un** mes ya extraído. Abra `Fuerza de trabajo.CSV` con `sep=";"` y `encoding="latin-1"`.

```python
# SU CÓDIGO — read_csv, filas/columnas, value_counts de DPTO (top 10)

```

**Comprobar:**

```python
assert n_rows > 10_000, "Se espera un mes nacional"
assert "DPTO" in df.columns
print("Exploración L1, Paso 2 — CSV muestra: OK")
```

---

### Paso 3 — Gráfico del proceso de descarga

```python
# SU CÓDIGO — gráfico simple, p. ej. MB total por survey_year (barra)

```

**Comprobar:**

```python
assert "survey_year" in manifest_df.columns
print("Exploración L1, Paso 3 — gráfico: OK")
```

---

# Parte B — Ética y OSM (L2)

## Paso 1 — Inventario de cuasi-identificadores

Sobre el **mismo CSV de muestra** (o enero 2024), complete una tabla con al menos **cinco** columnas sensibles para su arquetipo de proyecto.

```python
# SU CÓDIGO — DataFrame con columnas: columna, sensibilidad (baja/media/alta), uso previsto en salidas

```

**Comprobar:**

```python
assert len(tabla_qi) >= 5
assert "DPTO" in tabla_qi["columna"].values
print("L2 — inventario cuasi-identificadores: OK")
```

---

## Paso 2 — Lecturas (respuestas escritas)

En celdas markdown o strings, respondan **con sus palabras** (cite Zuboff y/o Mittelstadt **por nombre** donde aplique):

1. **boyd:** dos limitaciones de inferir la pregunta de su proyecto **solo** con esta tabla GEIH.
2. **Zuboff:** contraste encuesta pública GEIH vs datos de comportamiento comercial (un párrafo corto).
3. **Mittelstadt:** dos tipos de daño algorítmico aplicados a **un** análisis grupal planeado.

```python
respuestas_lecturas = """
1. boyd — ...
2. Zuboff — ...
3. Mittelstadt — ...
"""
print(respuestas_lecturas)
```

**Comprobar:**

```python
assert "boyd" in respuestas_lecturas.lower() or "limit" in respuestas_lecturas.lower()
assert "zuboff" in respuestas_lecturas.lower()
assert "mittelstadt" in respuestas_lecturas.lower()
assert len(respuestas_lecturas.split()) >= 80
print("L2 — lecturas: OK")
```

---

## Paso 3 — Interesados

¿Quién gana y quién pierde si publican un agregado departamental de informalidad o desempleo? (5–8 líneas.)

```python
interesados = """
...
"""
print(interesados)
```

**Comprobar:**

```python
assert len(interesados.split()) >= 40
print("L2 — interesados: OK")
```

---

## Paso 4 — Divulgación en su muestra

Repita la lógica de L2 Parte 3: celda mínima **DPTO × banda de edad**. Indique si la celda tiene menos de 5 filas.

```python
# SU CÓDIGO — groupby DPTO × banda_edad; imprimir celda mínima

```

**Comprobar:**

```python
assert min_filas >= 1
print(f"L2 — celda mínima: {min_filas} filas")
```

---

## Paso 5 — OSM ampliado por departamento

Parta de **`contar_nodos_amenity`** del cuaderno individual L2.

1. **`amenity=school`** → columna `poi_school_count`
2. Nodos con **`amenity`** en `hospital`, `clinic`, `doctors`, `pharmacy`, `health_centre` → `poi_health_count`
3. **`poi_servicios_basicos_count`** = suma de escuelas + salud

Complete **`DPTO_TO_OSM_AREA`**: id de área OSM por código DANE. Nariño (`52`) → `120027`. Busque otros ids en [OpenStreetMap](https://www.openstreetmap.org/) (relaciones administrativas nivel departamento). Use **`skip_if_exists`** o cache en CSV parcial si re-ejecuta.

```python
# SU CÓDIGO — funciones contar escuelas y contar salud; bucle por DPTO; guardar outputs/osm_poi_by_dpto.csv

```

Columnas mínimas del CSV:

| Columna | Descripción |
|---------|-------------|
| `dpto` | Código DANE |
| `poi_school_count` | Nodos `amenity=school` |
| `poi_health_count` | Nodos salud (lista arriba) |
| `poi_servicios_basicos_count` | Suma |

**Comprobar:**

```python
assert osm_path.is_file()
assert len(osm_df) >= 10, "Se esperan al menos 10 departamentos"
assert {"dpto", "poi_school_count", "poi_health_count", "poi_servicios_basicos_count"}.issubset(osm_df.columns)
assert osm_df["poi_servicios_basicos_count"].ge(0).all()
print("L2 — osm_poi_by_dpto.csv: OK")
```

---

## Paso 6 — Enlace GEIH + OSM otra vez

Agregue GEIH por **`DPTO`** (personas en muestra del mes elegido). **`merge`** con `osm_poi_by_dpto.csv`. Gráfico departamental (barras o scatter: personas vs `poi_servicios_basicos_count`).

Escriban **tres riesgos éticos** del join para el proyecto final (cobertura OSM, falacia ecológica, definición del POI, etc.).

```python
# SU CÓDIGO — merge, gráfico, variable riesgos_eticos_join (string multilínea)

```

**Comprobar:**

```python
assert len(enlace_df) >= 10
assert "personas_muestra" in enlace_df.columns
assert len(riesgos_eticos_join.split()) >= 40
print("L2 — enlace GEIH + OSM: OK")
```

---

## Paso 7 — Borrador práctica responsable

Tres a cinco viñetas para la sección **Preocupaciones éticas** del PDF grupal (semana 2). Deben **limitar** decisiones técnicas en L3–L6 (retención, agregación mínima, documentar fuentes OSM, etc.).

```python
practica_responsable = """
- ...
- ...
- ...
"""
print(practica_responsable)
```

**Comprobar:**

```python
assert practica_responsable.count("-") >= 3
assert len(practica_responsable.split()) >= 30
print("L2 — práctica responsable: OK")
```

---

## Registro de contribución (grupo)

Cada integrante añade una línea. Indique el **escriba de semana 1**.

```python
contribution_log = """
- Nombre 1 — ...
- Nombre 2 — ...
- Nombre 3 — ...
- Nombre 4 — ...
Escriba semana 1: ...
"""
print(contribution_log)
```

---

## Tarea grupal (Moodle)

ZIP **`week-1-<group_id>.zip`** hasta el **miércoles 10 de junio de 2026, 23:59 (Colombia)**:

| Archivo | Descripción |
|---------|-------------|
| `notebook-week-1-group-<group_id>.ipynb` | Este cuaderno ejecutado (plantilla Colab: `week-1-group`) |
| `manifest.json` | Registro DANE (L1) |
| `osm_poi_by_dpto.csv` | POI OSM por departamento (L2) |

**Reflexión individual:** `week-1-reflection-<student>.pdf` el **jueves 11 jun** (separado del ZIP).

**Requerimientos del proyecto:** `project_requirements.pdf` en la **semana 2** (use el borrador de práctica responsable de este cuaderno en la clínica del sábado).

<!-- end NOTEBOOK: -->
