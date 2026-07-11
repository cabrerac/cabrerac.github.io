---
author: Christian Cabrera Jojoa
course_code: 26-udenar-big-data
description: In this lecture, students present their big-data final projects.
email: chc79@cam.ac.uk
end_time: 10:00 am
hours: 3
layout: lecture
lecture_code: l8-final-project
lecture_date: 27/06/2026
permalink: /teaching/26-udenar-big-data/l8-final-project/
position: Assistant Research Professor
session: 8
skip_notebook: true
skip_slides: true
start_time: 07:00 am
title: Final Projects
visible: true
---

<div class="lecture-resources">
</div>

<link rel="stylesheet" href="/assets/css/lecture-article.css">
### Projects Catalog

{% assign catalog = site.data['26-udenar-big-data-projects'] %}
{% if catalog and catalog.projects and catalog.projects.size > 0 %}
{% for p in catalog.projects %}
### {{ p.title }}

{{ p.abstract }}

{% unless forloop.last %}
---
{% endunless %}
{% endfor %}
{% endif %}

---
