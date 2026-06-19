#!/usr/bin/env python3
"""Build project presentation PowerPoint template (Spanish labels, English optional title slide)."""

from __future__ import annotations

from pathlib import Path

from docx_build import ASSETS_DIR, PROJECT_DIR, REPO

ASSETS_PPTX = ASSETS_DIR / "project-presentation-template.pptx"
PROJECT_PPTX = PROJECT_DIR / "project-presentation-template.pptx"


def build_presentation() -> Path:
    try:
        from pptx import Presentation
        from pptx.util import Inches, Pt
    except ImportError as e:
        raise SystemExit(
            "python-pptx required: pip install python-pptx"
        ) from e

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    layouts = [
        ("Título del proyecto", "Grupo G… · Electiva Big Data · UDENAR 2026"),
        (
            "Modelo canvas",
            "Snapshot del canvas: requerimientos + ética/gobernanza como requisitos.",
        ),
        ("Pipeline de big data", "Fuentes → almacenamiento → procesamiento → ingesta → analítica."),
        (
            "Arquitectura de datos",
            "Harmonización, partición, ingesta gobernada (Prefect, audit, contrato).",
        ),
        (
            "Analítica y resultados",
            "Respuesta a la pregunta de decisión; demo en vivo (tablero, pipeline o celdas clave).",
        ),
        (
            "Conclusiones",
            "Retos del grupo, reflexión breve, recomendación.",
        ),
    ]

    for title, body in layouts:
        slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank
        left, top, width = Inches(0.6), Inches(0.5), Inches(12.0)
        box = slide.shapes.add_textbox(left, top, width, Inches(1.0))
        tf = box.text_frame
        tf.text = title
        tf.paragraphs[0].font.size = Pt(32)
        tf.paragraphs[0].font.bold = True
        body_box = slide.shapes.add_textbox(left, Inches(1.6), width, Inches(5.0))
        bf = body_box.text_frame
        bf.text = body
        bf.paragraphs[0].font.size = Pt(18)

    ASSETS_PPTX.parent.mkdir(parents=True, exist_ok=True)
    PROJECT_PPTX.parent.mkdir(parents=True, exist_ok=True)
    prs.save(ASSETS_PPTX)
    prs.save(PROJECT_PPTX)
    return ASSETS_PPTX


def main() -> None:
    path = build_presentation()
    print(f"Wrote {path}")
    print(f"Wrote {PROJECT_PPTX}")


if __name__ == "__main__":
    main()
