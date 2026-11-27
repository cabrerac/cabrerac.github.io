---
course_code: 26-udenar-data-mining
title: Prediction
description: Lecture 6 is the prediction task. The question is whether the attributes of an item can predict a label that someone gave. Loans, patients, and articles in a table with a given label can feed the task. We start from the majority class. We explore three methods for this task. Logistic regression, a neural network with one hidden layer whose output layer is a logistic regression, and transformers, the architecture inside the text encoder used in Lecture 4. For logistic regression and the network we go through theory, implementation and evaluation. For transformers we explain the mechanism, without training one. We end with why accuracy misleads, a leakage demo, and what deploying a prediction means and its limits.
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
notebook_title: Predicción
notebook_description: Práctica individual de la Lección 6. Predecir una etiqueta dada a partir de los atributos del artículo, sin usar el texto ni un conteo de popularidad, y contar aciertos y errores sobre ejemplos marcados.
---

<!-- SLIDES: -->

# Last Time

<!-- end SLIDES: -->

{% include _snippets/26-udenar-data-mining/l6-prediction/last-time.md %}

<!-- SLIDES: -->

# The Task

<!-- end SLIDES: -->

{% include _snippets/prediction.md %}

{% include _snippets/majority-baseline.md %}

<!-- SLIDES: -->

# Modeling

<!-- end SLIDES: -->

{% include _snippets/26-udenar-data-mining/l6-prediction/methods.md %}

{% include _snippets/logistic-regression.md %}

{% include _snippets/one-hidden-layer-network.md %}

{% include _snippets/transformer-components.md %}

{% include _snippets/transformer-families.md %}

<!-- SLIDES: -->

# Evaluation

<!-- end SLIDES: -->

{% include _snippets/classification-evaluation.md %}

{% include _snippets/classification-uncertainty.md %}

{% include _snippets/five-folds-code.md %}

<!-- SLIDES: -->

# Leakage

<!-- end SLIDES: -->

{% include _snippets/target-leakage-demo.md %}

<!-- SLIDES: -->

# Deployment

<!-- end SLIDES: -->

{% include _snippets/prediction-to-decision.md %}

<!-- SLIDES: -->

# Conclusions

<!-- end SLIDES: -->

{% include _snippets/26-udenar-data-mining/l6-prediction/conclusions.md %}

{% include _snippets/26-udenar-data-mining/l6-prediction/practical-slides.md %}

{% include _snippets/26-udenar-data-mining/l6-prediction/resources.md %}

{% include _snippets/26-udenar-data-mining/l6-prediction/practical.md %}
