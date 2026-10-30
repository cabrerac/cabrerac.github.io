---
course_code: 26-udenar-data-mining
title: Groups, outliers, and what a group means
description: Lecture 3 introduces groups of similar items. The data are items for which similarity can be stated. We give a short history of grouping, then three methods, each with its own data preparation. The basic method is k-means, prepared as scaled vectors. The intermediate method is a Gaussian mixture, prepared as those vectors reduced to a few dimensions. The advanced method is HDBSCAN, prepared as distances on the same vectors. The points it leaves out are the items that fit no group. Each method is taught with its mathematics, its preparation, and a Python implementation. We state what a group means for a decision. The lecture closes by adding this result to the pattern result. An item stays in view only when at least two results support it, and we state what would change that.
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
lecture_date: 14/11/2026
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

# Groups of Similar Items

<!-- end SLIDES: -->

{% include _snippets/clustering.md %}

{% include _snippets/26-udenar-data-mining/l3-groups/word-counts.md %}

<!-- SLIDES: -->

# Reducing the Dimensions

<!-- end SLIDES: -->

{% include _snippets/svd-lsa.md %}

<!-- SLIDES: -->

# k-means

<!-- end SLIDES: -->

{% include _snippets/k-means.md %}

<!-- SLIDES: -->

# Gaussian Mixtures

<!-- end SLIDES: -->

{% include _snippets/gaussian-mixtures.md %}

<!-- SLIDES: -->

# HDBSCAN

<!-- end SLIDES: -->

{% include _snippets/hdbscan.md %}

<!-- SLIDES: -->

# Judging Groups

<!-- end SLIDES: -->

{% include _snippets/permutation-baseline.md %}

{% include _snippets/cluster-validation.md %}

{% include _snippets/26-udenar-data-mining/l3-groups/comparison.md %}

<!-- SLIDES: -->

# Using a Group

<!-- end SLIDES: -->

{% include _snippets/combining-results.md %}

{% include _snippets/26-udenar-data-mining/l3-groups/decision.md %}

<!-- SLIDES: -->

# Conclusions

<!-- end SLIDES: -->

{% include _snippets/26-udenar-data-mining/l3-groups/conclusions.md %}

{% include _snippets/26-udenar-data-mining/l3-groups/practical-slides.md %}

{% include _snippets/26-udenar-data-mining/l3-groups/resources.md %}
{% include _snippets/26-udenar-data-mining/l3-groups/practical.md %}
