---
course_code: 26-udenar-data-mining
title: Text extraction and marked examples
description: Lecture 4 introduces extraction from text. The data are texts. We give a short history of text mining, then three methods, each with its own data preparation. The basic method is a keyword list, prepared as a normalized word list for the stated question. The intermediate method is TF-IDF with logistic regression, prepared as a document-term matrix and a split into marked examples. The advanced method is a frozen multilingual transformer encoder with logistic regression, prepared as the text itself, truncated to the encoder's length. Each method is taught with its mathematics, its preparation, and a Python implementation. The result is judged by how many marked examples it gets right and how many it gets wrong. The lecture closes by adding this result to the earlier ones. Each item shows how many results support it, and we state what would change its place on the list.
session: 4
start_time: 07:00 am
end_time: 01:00 pm
hours: 5
author: Christian Cabrera Jojoa
email: chc79@cam.ac.uk
position: Assistant Research Professor
department: Department of Computer Science and Technology
institution: University of Cambridge
layout: lecture
lecture_code: l4-text
lecture_date: 14/11/2026
permalink: /teaching/26-udenar-data-mining/l4-text/
visible: false
group_notebook: week-2-group
notebook_language: es
notebook_title: Extracción de texto y ejemplos marcados
notebook_description: Práctica individual de la Lección 4. Extraer de los resúmenes lo que la pregunta pide y contar aciertos y errores sobre ejemplos marcados.
---

<!-- SLIDES: -->

# Last Time

<!-- end SLIDES: -->

{% include _snippets/26-udenar-data-mining/l4-text/last-time.md %}

<!-- SLIDES: -->

# Text Mining

<!-- end SLIDES: -->

{% include _snippets/text-mining.md %}

<!-- SLIDES: -->

# Text Preparation

<!-- end SLIDES: -->

{% include _snippets/text-preparation.md %}

<!-- SLIDES: -->

# Keyword Lists

<!-- end SLIDES: -->

{% include _snippets/keyword-lists.md %}

<!-- SLIDES: -->

# TF-IDF

<!-- end SLIDES: -->

{% include _snippets/tf-idf.md %}

<!-- SLIDES: -->

# Logistic Regression

<!-- end SLIDES: -->

{% include _snippets/logistic-regression.md %}

<!-- SLIDES: -->

# Cross-validation

<!-- end SLIDES: -->

{% include _snippets/26-udenar-data-mining/l4-text/cross-validation.md %}

<!-- SLIDES: -->

# Text Encoders

<!-- end SLIDES: -->

{% include _snippets/text-encoders.md %}

<!-- SLIDES: -->

# Judging Text Results

<!-- end SLIDES: -->

{% include _snippets/classification-evaluation.md %}

{% include _snippets/26-udenar-data-mining/l4-text/five-folds.md %}

<!-- SLIDES: -->

# The Question and the Data

<!-- end SLIDES: -->

{% include _snippets/26-udenar-data-mining/l4-text/comparison.md %}

<!-- SLIDES: -->

# The Project

<!-- end SLIDES: -->

{% include _snippets/26-udenar-data-mining/l4-text/decision.md %}

<!-- SLIDES: -->

# Conclusions

<!-- end SLIDES: -->

{% include _snippets/26-udenar-data-mining/l4-text/conclusions.md %}

{% include _snippets/26-udenar-data-mining/l4-text/practical-slides.md %}

{% include _snippets/26-udenar-data-mining/l4-text/week2-deliverables.md %}

{% include _snippets/26-udenar-data-mining/l4-text/resources.md %}
{% include _snippets/26-udenar-data-mining/l4-text/practical.md %}
