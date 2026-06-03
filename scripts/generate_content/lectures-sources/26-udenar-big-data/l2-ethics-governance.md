---
course_code: 26-udenar-big-data
title: Ethics, privacy, and foundations of data governance
description: Lecture 2 (ethics-first framing) — Vs of harm, consent, fairness, Zuboff anchor reading, accountable practice; deepens the L1 project requirements doc before any technical lecture. Async ~2 h video (V1 theory + V2 case-study walkthrough) + ~3 h Saturday sync inside the shared 07:00–13:00 CO block.
session: 2
start_time: 07:00 am
end_time: 01:00 pm
hours: 5
author: Christian Cabrera Jojoa
email: chc79@cam.ac.uk
position: Assistant Research Professor
department: Department of Computer Science and Technology
institution: University of Cambridge
layout: lecture
lecture_code: l2-ethics-governance
lecture_date: 06/06/2026
permalink: /teaching/26-udenar-big-data/l2-ethics-governance/
visible: false
group_notebook: week-1-group
notebook_language: es
notebook_title: Ética, privacidad y gobernanza de datos
notebook_description: Práctica de la Lección 2. Auditoría ética sobre GEIH y primer enlace con OpenStreetMap (escuelas). Ejercicios de entrega en el cuaderno grupal week-1-group.
---

<!-- RENDER: -->

### Resources

- [Individual notebook Lecture 2](https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-big-data/l2-ethics-governance.ipynb)
- [Group notebook week 1](https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-big-data/week-1-group.ipynb): Deadline 10/06/2026
- [Reflection template week 1](/assets/documents/26-udenar-big-data/reflection-week-1-template.docx): Deadline 11/06/2026
- [Project requirements template](/assets/documents/26-udenar-big-data/project-requirements-template.docx): Feedback in group session week 2
- [OpenStreetMap — Colombia](https://www.openstreetmap.org/relation/120027)
- [Overpass API](https://wiki.openstreetmap.org/wiki/Overpass_API)

### References

- Zuboff, S. (2019). *The age of surveillance capitalism* (Chapter 1). PublicAffairs.
- Mittelstadt, B. D., et al. (2016). [The ethics of algorithms](https://doi.org/10.1177/2053951716679679). *Big Data & Society*, 3(2).
- boyd, d., & Crawford, K. (2012). [Critical questions for big data](https://doi.org/10.1080/1369118X.2012.678878). *Information, Communication & Society*, 15(5), 662–679.

<!-- end RENDER: -->

<!-- NOTEBOOK: -->

## Repaso de Python para este cuaderno

Este cuaderno usa **`pandas`** y **`requests`**. Si completó el cuaderno individual L1, ya conoce parte de esto. Aquí solo aparece lo nuevo para las Partes 1 a 5.

### Tablas con pandas

Un **DataFrame** es una tabla. **`read_csv`** abre un CSV. **`value_counts`** cuenta categorías. **`groupby`** agrupa filas.

```python
import pandas as pd

datos = {"dpto": [52, 52, 11], "edad": [25, 40, 30]}
df = pd.DataFrame(datos)
print(df.groupby("dpto")["edad"].mean())
print(df["dpto"].value_counts())
```

### Unir dos tablas con `merge`

**`merge`** combina tablas por una columna común (aquí **`DPTO`**).

```python
geih = pd.DataFrame({"dpto": [52, 11], "personas": [1000, 5000]})
osm = pd.DataFrame({"dpto": [52, 11], "poi_school_count": [120, 800]})
unido = geih.merge(osm, on="dpto", how="left")
print(unido)
```

### Peticiones HTTP con `requests`

**`requests.post`** envía datos a un servicio web. OpenStreetMap expone la **Overpass API** para consultar mapas.

```python
import requests

url = "https://overpass-api.de/api/interpreter"
query = '[out:json]; node["amenity"="school"](area:120027); out count;'
resp = requests.post(url, data={"data": query}, timeout=60)
resp.raise_for_status()
print(resp.json())
```

### Comprobar con `assert`

Las celdas **Comprobar** usan **`assert`** para validar resultados.

```python
assert len(unido) == 2
print("Repaso Python L2: OK")
```

---

## Instrucciones

**Propósito.** Este cuaderno es su práctica de la **Lección 2**. Trabaja sobre los archivos GEIH que ya descargó en L1. El objetivo es ver **ética y gobernanza en datos reales**: cuasi-identificadores, riesgo de divulgación, límites de inferencia y un primer enlace con **OpenStreetMap (OSM)**.

No hay celdas abiertas aquí. Los ejercicios de entrega están en el cuaderno grupal **[`week-1-group`](https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-big-data/week-1-group.ipynb)**.

**Qué hacer (en orden).**

1. Complete al menos la **Parte 1** del cuaderno individual L1 (enero 2024 en disco).
2. Ejecute las celdas **de arriba hacia abajo**.
3. En celdas **Comprobar**, corrija celdas anteriores si algo falla.
4. Lleve lo aprendido al cuaderno grupal y a la reflexión semana 1.

**Carpetas usadas:**

| Ruta | Función |
|------|---------|
| `data/raw/2024/Ene_2024/` | CSV de enero 2024 (L1) |
| `outputs/` | Tablas y gráficos exportados |

---

## Parte 1 — Cargar GEIH desde L1

Usamos **un mes** (enero 2024), igual que la Parte 1 de L1. Buscamos la tabla **Fuerza de trabajo**.

```python
from pathlib import Path

import pandas as pd

CSV_SEP = ";"
CSV_ENCODING = "latin-1"
YEAR_DIR = Path("data/raw/2024")
MONTH_DIR = YEAR_DIR / "Ene_2024"

# Buscar el CSV de fuerza de trabajo (nombre puede variar en mayúsculas)
candidatos = list(MONTH_DIR.glob("*fuerza*trabajo*.CSV")) + list(
    MONTH_DIR.glob("*fuerza*trabajo*.csv")
)
if not candidatos:
    raise FileNotFoundError(
        f"No hay CSV de fuerza de trabajo en {MONTH_DIR}. "
        "Complete la Parte 1 del cuaderno L1 primero."
    )
geih_path = candidatos[0]

df = pd.read_csv(geih_path, sep=CSV_SEP, encoding=CSV_ENCODING, low_memory=False)
n_rows = len(df)
n_cols = len(df.columns)

print(f"Archivo: {geih_path.name}")
print(f"Filas: {n_rows:,}  |  Columnas: {n_cols}")
print(df.head(3))
```

**Comprobar:**

```python
assert n_rows > 10_000, "Se espera un mes nacional de fuerza de trabajo"
assert "DPTO" in df.columns, "Falta columna DPTO"
print("Parte 1 — carga GEIH: OK")
```

---

## Parte 2 — Cuasi-identificadores

La GEIH no trae nombre ni cédula, pero sí **cuasi-identificadores**: combinaciones que pueden acercarse a identificar hogares o personas en celdas pequeñas.

Listamos columnas sensibles frecuentes en fuerza de trabajo.

```python
# Columnas que suelen ser cuasi-identificadores en GEIH
CANDIDATOS_QI = [
    "DPTO",
    "MPIO",
    "AREA",
    "P6040",
    "P6020",
    "SEXO",
    "P6160",
    "P6240",
    "P6090",
    "PER",
]

presentes = [c for c in CANDIDATOS_QI if c in df.columns]
faltantes = [c for c in CANDIDATOS_QI if c not in df.columns]

tabla_qi = pd.DataFrame(
    {
        "columna": presentes,
        "tipo": [str(df[c].dtype) for c in presentes],
        "valores_unicos": [df[c].nunique(dropna=False) for c in presentes],
    }
)
print("Cuasi-identificadores detectados:")
print(tabla_qi.to_string(index=False))
if faltantes:
    print("\nNo encontradas en este mes (puede variar por año):", ", ".join(faltantes))
```

Interpretación breve:

- **DPTO / MPIO / AREA**: geografía.
- **P6040** (o similar): edad.
- **P6020 / SEXO**: sexo.
- **P6160, P6240, P6090**: educación, ocupación, tipo de empleo (según diccionario DANE).

**Comprobar:**

```python
assert len(presentes) >= 3, "Se esperan al menos DPTO y dos cuasi-identificadores más"
assert "DPTO" in presentes
print("Parte 2 — cuasi-identificadores: OK")
```

---

## Parte 3 — Vista previa de divulgación estadística

Contamos filas en la celda más pequeña **departamento × banda de edad**. Si hay muy pocas filas, publicar ese agregado puede acercarse a identificar personas. En L4 verán mitigaciones (k-anon, supresión). Aquí solo **medimos**.

```python
# Columna de edad: P6040 es habitual en GEIH
if "P6040" not in df.columns:
    raise KeyError("No hay P6040 (edad). Revise df.columns y adapte el nombre.")

# Normalizar DPTO como texto sin ceros a la izquierda inconsistentes
work = df[["DPTO", "P6040"]].copy()
work["DPTO"] = work["DPTO"].astype(str).str.strip()
work["P6040"] = pd.to_numeric(work["P6040"], errors="coerce")
work = work.dropna(subset=["P6040"])

# Bandas de edad simples para el ejercicio
work["banda_edad"] = pd.cut(
    work["P6040"],
    bins=[0, 17, 29, 44, 59, 120],
    labels=["0-17", "18-29", "30-44", "45-59", "60+"],
)

celdas = (
    work.groupby(["DPTO", "banda_edad"], observed=True)
    .size()
    .reset_index(name="filas")
    .sort_values("filas")
)

min_fila = celdas.iloc[0]
print("Cinco celdas con menos filas (DPTO × banda de edad):")
print(celdas.head(5).to_string(index=False))
print(
    f"\nCelda mínima: DPTO={min_fila['DPTO']}, "
    f"banda={min_fila['banda_edad']}, filas={min_fila['filas']}"
)

K_MIN = 5
if min_fila["filas"] < K_MIN:
    print(f"ALERTA: celda con menos de {K_MIN} filas — riesgo de divulgación si se publica tal cual.")
else:
    print(f"En este mes nacional la celda mínima tiene al menos {K_MIN} filas (vista previa).")
```

**Comprobar:**

```python
assert len(celdas) > 0
assert min_fila["filas"] >= 1
print("Parte 3 — divulgación (vista previa): OK")
```

---

## Parte 4 — OpenStreetMap: escuelas en un departamento

OSM es un mapa colaborativo. Consultamos **Overpass API** para contar nodos con **`amenity=school`** en **un departamento** (Nariño, código DANE **`52`**).

### Paso 1 — Configuración OSM

Cada departamento tiene un **id de área** en OSM (relación administrativa). Para Nariño usamos **`120027`**. En el cuaderno grupal completarán ids para más departamentos.

```python
import json
import time

import matplotlib.pyplot as plt
import requests

OVERPASS_URL = "https://overpass-api.de/api/interpreter"
OUTPUTS_DIR = Path("outputs")
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

# Nariño — código DANE 52
DPTO_DEMO = 52
DPTO_DEMO_NOMBRE = "Nariño"
OSM_AREA_ID_NARINO = 120027

AMENITY_SCHOOL = "school"
PAUSA_SEG = 1.0  # cortesía con el servidor público Overpass
```

### Paso 2 — Función para contar POI

```python
def contar_nodos_amenity(area_id: int, amenity: str, timeout: int = 90) -> int:
    """Cuenta nodos OSM con amenity dado dentro del area_id."""
    query = f"""
    [out:json][timeout:60];
    area({area_id})->.a;
    node["amenity"="{amenity}"](area.a);
    out;
    """
    resp = requests.post(OVERPASS_URL, data={"data": query}, timeout=timeout)
    resp.raise_for_status()
    data = resp.json()
    return len(data.get("elements", []))


t0 = time.perf_counter()
poi_school_count = contar_nodos_amenity(OSM_AREA_ID_NARINO, AMENITY_SCHOOL)
elapsed = round(time.perf_counter() - t0, 2)
time.sleep(PAUSA_SEG)

print(f"{DPTO_DEMO_NOMBRE} (DPTO {DPTO_DEMO}): amenity=school → {poi_school_count} nodos")
print(f"Consulta Overpass: {elapsed} s")
```

**Comprobar:**

```python
assert poi_school_count >= 0
print("Parte 4, Paso 2 — consulta OSM: OK")
```

### Paso 3 — Agregar GEIH en el mismo departamento

Comparamos **personas en la muestra GEIH** del departamento con **escuelas OSM**. Es un enlace ilustrativo, no una conclusión causal.

```python
work_dpto = df.copy()
work_dpto["DPTO"] = pd.to_numeric(work_dpto["DPTO"], errors="coerce")
geih_dpto = (
    work_dpto.groupby("DPTO")
    .size()
    .reset_index(name="personas_muestra")
)
geih_dpto["DPTO"] = geih_dpto["DPTO"].astype(int)

fila_demo = geih_dpto.loc[geih_dpto["DPTO"] == DPTO_DEMO]
if fila_demo.empty:
    raise ValueError(f"No hay filas GEIH para DPTO {DPTO_DEMO} en este mes.")

personas_demo = int(fila_demo["personas_muestra"].iloc[0])

enlace = pd.DataFrame(
    [
        {
            "dpto": DPTO_DEMO,
            "nombre": DPTO_DEMO_NOMBRE,
            "personas_muestra": personas_demo,
            "poi_school_count": poi_school_count,
        }
    ]
)
print(enlace.to_string(index=False))
enlace.to_csv(OUTPUTS_DIR / "enlace_geih_osm_demo.csv", index=False)
```

**Comprobar:**

```python
assert personas_demo > 0
assert enlace["poi_school_count"].iloc[0] == poi_school_count
print("Parte 4, Paso 3 — agregado GEIH: OK")
```

### Paso 4 — Gráfico simple del enlace

```python
fig, ax = plt.subplots(figsize=(5, 3))
ax.bar(["Personas\n(muestra GEIH)", "Escuelas\n(OSM)"], [personas_demo, poi_school_count], color=["#4472C4", "#ED7D31"])
ax.set_title(f"Nariño (DPTO {DPTO_DEMO}) — enero 2024")
ax.set_ylabel("Conteo")
fig.tight_layout()
fig.savefig(OUTPUTS_DIR / "enlace_geih_osm_demo.png", dpi=120)
plt.show()
print(f"Figura guardada: {OUTPUTS_DIR / 'enlace_geih_osm_demo.png'}")
```

### Paso 5 — Problemas éticos al unir GEIH y OSM

Al unir encuesta y mapa aparecen límites que debe conocer antes del proyecto:

1. **Cobertura desigual de OSM.** No todos los departamentos están mapeados con la misma calidad. Pocos POI no siempre significa pocos servicios reales.
2. **Falacia ecológica.** Un patrón a nivel departamento no prueba nada sobre una persona concreta.
3. **Sin consentimiento cruzado.** Los encuestados no acordaron mezclar sus respuestas con un mapa voluntario.
4. **Sesgo urbano.** Las ciudades suelen tener más nodos OSM que zonas rurales.
5. **Definición del POI.** Aquí contamos solo **`amenity=school`**. Otro tag daría otra historia (lo verán en el cuaderno grupal).

**Comprobar:**

```python
assert (OUTPUTS_DIR / "enlace_geih_osm_demo.csv").is_file()
print("Parte 4 — OSM + enlace GEIH: OK")
```

---

## Parte 5 — Lecturas y el dataset

Relacionamos lo visto en código con las lecturas de la semana.

**boyd y Crawford.** Más datos no responden automáticamente la pregunta del proyecto. GEIH informa mercado laboral oficial. OSM aporta contexto geográfico incompleto. Juntos no sustituyen conocimiento cualitativo ni otras fuentes.

**Zuboff.** GEIH es estadística pública con marco legal. OSM es datos colaborativos con otra lógica de producción. No es "surplus" comercial, pero sí mezcla regímenes de datos distintos que hay que declarar en el pipeline.

**Mittelstadt et al.** Al publicar agregados pueden aparecer daños por **discriminación** (priorizar regiones con más escuelas mapeadas) o **falta de transparencia** (no explicar límites del join). El cuaderno grupal pedirá mapear dos tipos de daño a su arquetipo.

Estos temas alimentan la sección **Preocupaciones éticas** del PDF grupal (semana 2) y la reflexión semana 1.

**Comprobar:**

```python
print("Parte 5 — lecturas: OK (narrativa completada)")
```

---

## Tareas

Esta sección define **qué entregar en Moodle** para la semana 1. Plantillas en la [página de esta lección](https://cabrerac.github.io/teaching/26-udenar-big-data/l2-ethics-governance/).

### Trabajo en grupo (60 % de la formativa semana 1)

Use el Colab plantilla **[`week-1-group`](https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-big-data/week-1-group.ipynb)**. Consolida **L1 + L2**. Entregar ZIP **`week-1-<group_id>.zip`** hasta el **miércoles 10 de junio de 2026, 23:59 (Colombia)**:

| Archivo en el ZIP | Descripción |
|-------------------|-------------|
| `notebook-week-1-group-<group_id>.ipynb` | Cuaderno grupal ejecutado (renombre desde `week-1-group`) |
| `manifest.json` | Registro de acceso DANE |
| `osm_poi_by_dpto.csv` | Conteos OSM por departamento |

Los **requerimientos del proyecto** (`project_requirements.pdf`) se entregan en la **semana 2** (plantilla en la página de esta lección).

### Reflexión individual (40 % de la formativa semana 1)

PDF **`week-1-reflection-<student>.pdf`** hasta el **jueves 11 de junio de 2026, 23:59 (Colombia)**. Cubre L1 y L2 (plantilla semana 1).

### Requerimientos del proyecto

`project_requirements.pdf` se entrega en la **semana 2** (ver definición del proyecto). El cuaderno grupal incluye borrador de práctica responsable para la clínica del sábado.

<!-- end NOTEBOOK: -->
