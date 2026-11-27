---
course_code: 26-udenar-data-mining
title: Prediction
description: Lecture 6 is the prediction task. The question is whether the attributes of an item can predict a label that someone gave. Loans, patients, and articles in a table with a given label can feed the task. We explore three methods for this task. Logistic regression, a neural network with one hidden layer, and transformers. For logistic regression and the network we go through theory and implementation. For transformers we explain the mechanism, without training one. We then evaluate the trained methods on marked items they never saw. We end with what deploying a prediction means and its limits.
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
notebook_description: Práctica individual de la Lección 6. Predecir desde el resumen si un artículo se debe leer, con la etiqueta de tema de la Lección 4. Comparar la regresión logística y una red con una capa oculta, y contar aciertos y errores sobre artículos apartados.
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

{% include _snippets/prediction-evaluation.md %}

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
