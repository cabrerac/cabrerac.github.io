---
course_code: 26-udenar-data-mining
title: Classification, regression, and a given label
description: Lecture 6 introduces classification. The data are a table of item attributes and a given class label. The label is not taken from the text, and it is not a popularity count. The same linear model is regression when the label is a number. This lecture uses a class label. We give a short history of supervised prediction, then three methods, each with its own data preparation. The basic method is logistic regression, prepared as scaled numbers and encoded categories, and scored against a majority-class baseline. The intermediate method is a random forest, prepared on the same table with missing values filled and categories encoded. The advanced method is a neural network with one hidden layer, prepared as a fully numeric scaled table with missing values filled. Each method is taught with its mathematics, its preparation, and a Python implementation. The prediction is judged by how many marked examples it gets right and how many it gets wrong. The lecture closes by adding this result to the earlier ones. Each item shows how many results support it, and we state what would change its place on the list.
session: 6
start_time: 07:00 am
end_time: 01:00 pm
hours: 5
author: Christian Cabrera Jojoa
email: chc79@cam.ac.uk
position: Assistant Research Professor
department: Department of Computer Science and Technology
institution: University of Cambridge
layout: lecture
lecture_code: l6-prediction
lecture_date: 28/11/2026
permalink: /teaching/26-udenar-data-mining/l6-prediction/
visible: false
group_notebook: week-3-group
notebook_language: es
notebook_title: Clasificación, regresión y una etiqueta dada
notebook_description: Práctica individual de la Lección 6. Predecir una etiqueta dada a partir de los atributos del artículo, sin usar el texto ni un conteo de popularidad, y contar aciertos y errores sobre ejemplos marcados.
---

<!-- SLIDES: -->

# Last Time

<!-- end SLIDES: -->

{% include _snippets/26-udenar-data-mining/l6-prediction/last-time.md %}

<!-- SLIDES: -->

# Supervised Prediction

<!-- end SLIDES: -->

{% include _snippets/prediction.md %}

<!-- SLIDES: -->

# Tabular Preparation

<!-- end SLIDES: -->

{% include _snippets/tabular-preparation.md %}

<!-- SLIDES: -->

# Logistic Regression

<!-- end SLIDES: -->

{% include _snippets/logistic-regression.md %}

<!-- SLIDES: -->

# Random Forests

<!-- end SLIDES: -->

{% include _snippets/decision-trees-random-forests.md %}

<!-- SLIDES: -->

# One Hidden Layer

<!-- end SLIDES: -->

{% include _snippets/one-hidden-layer-network.md %}

{% include _snippets/mlp-implementation.md %}

{% include _snippets/26-udenar-data-mining/l6-prediction/network-in-course.md %}

<!-- SLIDES: -->

# Judging Predictions

<!-- end SLIDES: -->

{% include _snippets/classification-evaluation.md %}

<!-- SLIDES: -->

# The Question and the Data

<!-- end SLIDES: -->

{% include _snippets/26-udenar-data-mining/l6-prediction/course-data.md %}

{% include _snippets/26-udenar-data-mining/l6-prediction/comparison.md %}

<!-- SLIDES: -->

# The Project

<!-- end SLIDES: -->

{% include _snippets/combining-results.md %}

{% include _snippets/26-udenar-data-mining/l6-prediction/starter-list.md %}

<!-- SLIDES: -->

# Conclusions

<!-- end SLIDES: -->

{% include _snippets/26-udenar-data-mining/l6-prediction/conclusions.md %}

{% include _snippets/26-udenar-data-mining/l6-prediction/practical-slides.md %}

{% include _snippets/26-udenar-data-mining/l6-prediction/week3-deliverables.md %}

{% include _snippets/26-udenar-data-mining/l6-prediction/resources.md %}
{% include _snippets/26-udenar-data-mining/l6-prediction/practical.md %}
