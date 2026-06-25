---
author: Christian Cabrera Jojoa
course_code: 26-udenar-big-data
description: "Sat 27 Jun 2026 \u2014 final group presentations (L8), then research\
  \ talk L7. Public project catalog (English title + abstract, opt-in). Final ZIP\
  \ Tue 30 Jun; reflection Wed 1 Jul."
email: chc79@cam.ac.uk
end_time: 01:00 pm
hours: 6
layout: lecture
lecture_code: l8-final-project
lecture_date: 27/06/2026
permalink: /teaching/26-udenar-big-data/l8-final-project/
position: Assistant Research Professor
session: 8
skip_notebook: true
skip_slides: true
start_time: 07:00 am
title: Proyectos finales y cierre del curso
visible: false
---

<link rel="stylesheet" href="/assets/css/slides.css">
<link rel="stylesheet" href="/assets/css/lecture-article.css">
<div class="lecture-resources">
  <p>
    <a href="/teaching/26-udenar-big-data/">Back to course</a>
  </p>
</div>

**Saturday 27 Jun 2026** · Final group presentations, then research talk

Each group: **~20 min** (6 slides + **live demo** of pipeline / dashboard) + **~10 min** Q&A. Template: [project-presentation-template.pptx](/assets/documents/26-udenar-big-data/project-presentation-template.pptx).

After all presentations: [L7 — Research lines and masters projects](/teaching/26-udenar-big-data/l7-research/) (~1 h).

---

### Entregas finales (Moodle)

| Entrega | Plazo (Colombia) |
|---------|------------------|
| ZIP `project-<group_id>.zip` (informe PDF + código + manifiesto + linaje) | **Martes 30 jun 2026, 23:59** |
| Reflexión `project-reflection-<student>.pdf` | **Miércoles 1 jul 2026, 23:59** |

Plantillas: [informe](/assets/documents/26-udenar-big-data/project-report-template.docx) · [diapositivas](/assets/documents/26-udenar-big-data/project-presentation-template.pptx) · [reflexión](/assets/documents/26-udenar-big-data/project-reflection-template.docx)

Detalle de la entrega: sección **Entregables del proyecto** en [L6](/teaching/26-udenar-big-data/l6-analytics/).

---

### Catálogo de proyectos

{% assign catalog = site.data['26-udenar-big-data-projects'] %}
{% if catalog and catalog.projects and catalog.projects.size > 0 %}
<h3>Proyectos publicados (opt-in)</h3>
{% for p in catalog.projects %}
<h4>{{ p.title }} <span style="font-weight: normal; font-size: 0.9em;">({{ p.group_id }})</span></h4>
<p>{{ p.abstract }}</p>
{% unless forloop.last %}
<hr>
{% endunless %}
{% endfor %}
{% else %}
<p><em>Los resúmenes en inglés de los grupos que opten por publicación aparecerán aquí después del 30 de junio de 2026.</em></p>
{% endif %}

---
