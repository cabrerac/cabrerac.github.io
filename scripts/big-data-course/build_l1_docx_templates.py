#!/usr/bin/env python3
"""Build L1 student Word templates (Spanish) for download on the lecture website.

Outputs (canonical for the site):
  assets/documents/26-udenar-big-data/plantilla-requerimientos-proyecto.docx
  assets/documents/26-udenar-big-data/plantilla-reflexion-l1.docx

Also mirrors to work-space/teaching/big-data/course/week-1/ for instructor editing.

Regenerate after changing section titles (must match check_submission.py).
"""

from __future__ import annotations

from pathlib import Path

from docx import Document
from docx.enum.text import WD_LINE_SPACING
from docx.shared import Pt

REPO = Path(__file__).resolve().parents[2]
COURSE = "26-udenar-big-data"
ASSETS_DIR = REPO / "assets" / "documents" / COURSE
WEEK1_DIR = REPO / "work-space/teaching/big-data/course/week-1"

REQ_ASSETS = ASSETS_DIR / "plantilla-requerimientos-proyecto.docx"
REF_ASSETS = ASSETS_DIR / "plantilla-reflexion-l1.docx"
REQ_WEEK1 = WEEK1_DIR / "plantilla-requerimientos-proyecto.docx"
REF_WEEK1 = WEEK1_DIR / "plantilla-reflexion-l1.docx"


def _style_body(doc: Document) -> None:
    normal = doc.styles["Normal"]
    normal.font.name = "Calibri"
    normal.font.size = Pt(11)
    pf = normal.paragraph_format
    pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    pf.line_spacing = 1.15
    pf.space_after = Pt(6)


def _heading(doc: Document, text: str, level: int = 1) -> None:
    doc.add_heading(text, level=level)


def _para(doc: Document, text: str) -> None:
    doc.add_paragraph(text)


def _section(doc: Document, title: str, prompt: str) -> None:
    _heading(doc, title, 2)
    _para(doc, prompt)
    doc.add_paragraph()


def build_project_requirements() -> Document:
    doc = Document()
    _style_body(doc)
    _heading(doc, "Requerimientos del proyecto — Lección 1", 0)
    _para(doc, "Maestría en Estadística Aplicada · UDENAR · Electiva Big Data · A-2026")
    _para(
        doc,
        "Complete en Word, inserte su diagrama de pipeline en la sección 8, "
        "y entregue project_requirements.pdf en el ZIP grupal (miércoles). "
        "Mantenga los títulos de sección exactamente como aparecen abajo.",
    )
    doc.add_paragraph()

    sections = [
        (
            "1. Metadatos del grupo",
            "Grupo (G1…), integrantes, arquetipo (asignación de recursos | riesgo / alerta temprana | monitoreo), fecha.",
        ),
        (
            "2. Interesados",
            "¿A quién sirve su equipo de analítica y quién se ve afectado por las decisiones?",
        ),
        (
            "3. Pregunta de decisión",
            "Una pregunta específica, respondible con microdatos GEIH, alineada con el arquetipo.",
        ),
        (
            "4. Subconjunto de datos (GEIH)",
            "Años (p. ej. 2022–2025), regiones/departamentos, segmento de población, variables principales.",
        ),
        (
            "5. Criterios de éxito",
            "Al menos dos criterios comprobables (reproducibilidad, tiempo, incertidumbre, etc.).",
        ),
        (
            "6. Preocupación ética y lectura",
            "Un tema concreto del case shell §6 + cite Zuboff cap. 1 u otra lectura de la semana por nombre.",
        ),
        (
            "7. Roles y plan de contribución",
            "Una viñeta por integrante (marco, datos, análisis, escritura, presentación).",
        ),
        (
            "8. Pipeline del proyecto",
            "Inserte su figura (architecture.svg) y 3–5 oraciones: fuentes → almacenamiento → procesamiento → decisión.",
        ),
        (
            "9. URL del Colab grupal canónico",
            "Enlace al Colab/Drive donde el grupo ejecuta l1-introduction-group y consolida tareas.",
        ),
        (
            "10. Rotación de escriba por lección",
            "L1: … L2: … … L6: … (cada integrante al menos una vez).",
        ),
    ]
    for title, prompt in sections:
        _section(doc, title, prompt)
    return doc


def build_reflection_l1() -> Document:
    doc = Document()
    _style_body(doc)
    _heading(doc, "Reflexión individual — Lección 1", 0)
    _para(doc, "Entregable: l1-reflexion-<nombre-estudiante>.pdf (exportar desde este Word).")
    _para(doc, "Extensión orientativa del cuerpo: 500–900 palabras.")
    doc.add_paragraph()

    _section(
        doc,
        "Metadatos",
        "Lección: 1 | Estudiante: … | Grupo: G… | Lectura citada: … | Conteo de palabras: ~…",
    )
    _section(
        doc,
        "R1 Proceso y metodología",
        "Qué hizo en el cuaderno l1-introduction; qué aprendió sobre Access.",
    )
    _section(
        doc,
        "R2 Justificación técnica",
        "Una decisión técnica (URL, streaming, file_id, carpetas) y por qué.",
    )
    _section(
        doc,
        "R3 Enlace con el dominio y la decisión",
        "Cómo su arquetipo y pregunta de decisión del grupo encajan con GEIH.",
    )
    _section(
        doc,
        "R4 Ética y lecturas",
        "Cite boyd & Crawford o Zuboff cap. 1; enlace con privacidad o gobernanza.",
    )
    _section(
        doc,
        "R5 Uso de IA e integridad",
        "Qué herramientas de IA usó en L1 y qué verificó usted mismo.",
    )
    _para(
        doc,
        "Consigna L1: Si el DANE restringiera mañana las descargas masivas, "
        "¿qué parte de su configuración de Access cambiaría primero — y qué implicaría "
        "eso para la rendición de cuentas pública?",
    )
    return doc


def _save_pair(doc: Document, assets_path: Path, week1_path: Path) -> None:
    assets_path.parent.mkdir(parents=True, exist_ok=True)
    week1_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(assets_path)
    doc.save(week1_path)


def build() -> tuple[Path, Path]:
    req = build_project_requirements()
    ref = build_reflection_l1()
    _save_pair(req, REQ_ASSETS, REQ_WEEK1)
    _save_pair(ref, REF_ASSETS, REF_WEEK1)
    return REQ_ASSETS, REF_ASSETS


if __name__ == "__main__":
    req_path, ref_path = build()
    print(f"Wrote {req_path}")
    print(f"Wrote {ref_path}")
    print(f"Mirror {REQ_WEEK1}")
    print(f"Mirror {REF_WEEK1}")
