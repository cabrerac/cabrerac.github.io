---
course_code: 26-udenar-data-mining
title: Groups, outliers, and what a group means
description: Lecture 3 is the grouping task. The question is which items are similar enough to share a group, and which fit no group. Customers, patients, and texts described by the same attributes can feed the task. We explore three methods for this task. k-means, Gaussian mixtures, and HDBSCAN. For each method we go through its theory, implementation and evaluation. We end with what deploying a group means and its limits.
session: 3
start_time: 07:00 am
end_time: 01:00 pm
hours: 5
author: Christian Cabrera Jojoa
email: chc79@cam.ac.uk
position: Assistant Research Professor
department: Department of Computer Science and Technology
institution: University of Cambridge
layout: lecture
lecture_code: l3-groups
lecture_date: 21/11/2026
permalink: /teaching/26-udenar-data-mining/l3-groups/
visible: false
group_notebook: week-2-group
notebook_language: es
notebook_title: Grupos, atípicos y qué significa un grupo
notebook_description: Práctica individual de la Lección 3. Agrupar artículos parecidos, marcar los que no encajan en ningún grupo y decir qué significa un grupo para la lectura.
---

<!-- SLIDES: -->

# Last Time

<!-- end SLIDES: -->

{% include _snippets/26-udenar-data-mining/l3-groups/last-time.md %}

<!-- SLIDES: -->

# The Task

<!-- end SLIDES: -->

{% include _snippets/clustering.md %}

{% include _snippets/k-means.md %}

{% include _snippets/gaussian-mixtures.md %}

{% include _snippets/hdbscan.md %}

<!-- SLIDES: -->

# Evaluation

<!-- end SLIDES: -->

{% include _snippets/permutation-baseline.md %}

{% include _snippets/cluster-validation.md %}

{% include _snippets/group-methods-comparison.md %}

<!-- SLIDES: -->

# Deployment

<!-- end SLIDES: -->

{% include _snippets/group-to-decision.md %}

{% include _snippets/26-udenar-data-mining/l3-groups/decision-use.md %}

<!-- SLIDES: -->

# Conclusions

<!-- end SLIDES: -->

{% include _snippets/26-udenar-data-mining/l3-groups/conclusions.md %}

{% include _snippets/26-udenar-data-mining/l3-groups/practical-slides.md %}

{% include _snippets/26-udenar-data-mining/l3-groups/resources.md %}
{% include _snippets/26-udenar-data-mining/l3-groups/practical.md %}
