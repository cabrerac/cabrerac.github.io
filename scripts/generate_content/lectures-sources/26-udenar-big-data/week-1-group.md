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

**Entrega Moodle (lunes 9 jun):** ZIP `week-1-<group_id>.zip` con `notebook-week-1-group-<group_id>.ipynb` (renombre este cuaderno al exportar), `manifest.json` y `osm_poi_by_dpto.csv`.

**Catálogos DANE por año:** 2022 → `771`, 2023 → `782`, 2024 → `819`, 2025 → `853`.

**Mapa del cuaderno**

| Bloque | Pasos | Entregable clave |
|--------|-------|------------------|
| **Parte A** (L1) | Config → descarga → exploración (3 pasos) | `manifest.json` + exploración en el cuaderno |
| **Parte B** (L2) | Pasos 1–7 | `outputs/osm_poi_by_dpto.csv` + texto de lecturas y ética |
| **Cierre** | Registro de contribución | Líneas por integrante + escriba semana 1 |

**Tiempo orientativo:** Parte A puede tardar **horas** (descarga ~48 ZIP). Parte B depende de cuántos departamentos incluya en el bucle OSM (empiece con 5–10 DPTO y amplíe si alcanza).

---

# Parte A — Access GEIH 2022–2025 (L1)

**Objetivo.** Replicar el pipeline de acceso de L1 para **cuatro años** y dejar un manifiesto auditable.

## Configuración

Copie del [cuaderno individual L1](https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-big-data/l1-introduction.ipynb) y adapte (referencias L1):

| Qué copiar | Dónde está en L1 |
|------------|------------------|
| `download_zip` | Parte 1, Paso 2 |
| `extract_csvs` | Parte 1, Paso 3 |
| `write_manifest` | Parte 1, Paso 5 |
| `list_catalog_downloads` + bucle `access_file` | Parte 2 (si ya lo tiene) |
| Constantes `CSV_SEP`, `CSV_ENCODING`, `PRIMARY_TABLE_KEYWORD` | Parte 1, Paso 1 |

Añada en esta celda:

- `CATALOG_BY_YEAR = {2022: 771, 2023: 782, 2024: 819, 2025: 853}`
- `DATASET_YEARS = [2022, 2023, 2024, 2025]` y rutas `data/raw/{año}/`
- En `access_file`, **`skip_if_exists=True`** para no re-descargar al re-ejecutar

```python
# SU CÓDIGO — imports, constantes y funciones reutilizadas del cuaderno individual L1

```

---

## Descargar 2022–2025

**En este paso:** por cada año en `DATASET_YEARS`, obtenga la lista de archivos del catálogo DANE, descargue cada mes, extraiga CSV y añada una fila a `manifest_entries`.

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

**Objetivo.** Completar la auditoría ética y el CSV OSM que el cuaderno individual L2 solo **muestra** en un departamento.

Use el mismo mes de muestra que en la exploración L1 (recomendado: **enero 2024**). Reutilice `contar_nodos_amenity` y `OVERPASS_HEADERS` del [cuaderno L2](https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-big-data/l2-ethics-governance.ipynb) (Parte 4).

## Paso 1 — Inventario de cuasi-identificadores

**Pista (L2 Parte 2):** parta de `CANDIDATOS_QI` o liste usted mismo columnas con sensibilidad **baja / media / alta** y uso previsto en salidas del proyecto.

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

Repita la lógica de **L2 Parte 3**: `groupby` **DPTO × banda_edad**, ordene por `filas`, guarde la celda mínima en **`min_filas`** (entero). Imprima si **`min_filas < 5`** (alerta de divulgación).

```python
# SU CÓDIGO — groupby DPTO × banda_edad; asigne min_filas; imprima celda mínima

```

**Comprobar:**

```python
assert min_filas >= 1, "Defina min_filas en la celda anterior"
print(f"L2 — celda mínima: {min_filas} filas")
```

---

## Paso 5 — OSM ampliado por departamento

Parta de **`contar_nodos_amenity`** del cuaderno individual L2.

1. **`amenity=school`** → columna `poi_school_count`
2. Nodos con **`amenity`** en `hospital`, `clinic`, `doctors`, `pharmacy`, `health_centre` → `poi_health_count`
3. **`poi_servicios_basicos_count`** = suma de escuelas + salud

Complete **`DPTO_TO_OSM_RELATION`**: id de **relación** OSM por código DANE. El id de área Overpass es **`3600000000 + relación`**. Nariño (`52`) → relación **`1380130`** → área **`3601380130`** (no **`120027`**, que es Colombia). Busque otras relaciones en [OpenStreetMap](https://www.openstreetmap.org/) (`admin_level=4`). Reutilice **`OVERPASS_HEADERS`** del cuaderno L2. Use **`skip_if_exists`** o cache si re-ejecuta.

Plantilla mínima (complete más códigos DANE; puede empezar con 5–10 departamentos):

```python
# Ejemplo — amplíe el diccionario antes del bucle
DPTO_TO_OSM_RELATION = {
    52: 1380130,   # Nariño — verificar en OSM
    # 11: ...,    # Bogotá D.C. — buscar relación admin_level=4
}
# area_id = 3600000000 + relation_id
# osm_path = Path("outputs/osm_poi_by_dpto.csv")
```

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

Cada integrante añade **una línea** con tarea concreta (descarga, OSM, redacción, gráfico). Indique el **escriba de semana 1** (rota cada semana).

```python
contribution_log = """
- Ana Pérez — bucle descarga 2023 y manifiesto
- Luis Gómez — Paso 5 OSM (10 departamentos)
- ...
Escriba semana 1: Ana Pérez
"""
print(contribution_log)
```

---

## Tarea grupal (Moodle)

ZIP **`week-1-<group_id>.zip`** hasta el **lunes 9 de junio de 2026, 23:59 (Colombia)**:

| Archivo | Descripción |
|---------|-------------|
| `notebook-week-1-group-<group_id>.ipynb` | Este cuaderno ejecutado (plantilla Colab: `week-1-group`) |
| `manifest.json` | Registro DANE (L1) |
| `osm_poi_by_dpto.csv` | POI OSM por departamento (L2) |

**Reflexión individual:** `week-1-reflection-<student>.pdf` el **martes 10 jun** (separado del ZIP).

**Requerimientos del proyecto:** `project_requirements.pdf` en la **semana 2** (use el borrador de práctica responsable de este cuaderno en la clínica del sábado).

<!-- end NOTEBOOK: -->
