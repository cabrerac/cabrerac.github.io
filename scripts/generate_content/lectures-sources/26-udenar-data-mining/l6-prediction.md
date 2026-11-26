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

## Methods

<div class="rows" style="height: 100%">
    <div class="row" style="height: 65%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%; height: 100%">
                <img class="external-svg" src="{{ site.url }}/assets/media/diagrams/prediction-task-taxonomy.svg" alt="Taxonomy of prediction methods" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
    <div class="row" style="height: 35%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%; height: 100%">
                <p><b>Linear models:</b> a weighted sum of the attributes, turned into a class or a number.</p>
                <p><b>Trees:</b> questions about one attribute at a time, alone or as many trees that vote.</p>
                <p><b>Neural networks:</b> layers that learn their own attributes from the inputs, and transformers.</p>
                <p><b>Other methods:</b> the label of the nearest items, or a boundary with the widest margin.</p>
            </div>
        </div>
    </div>
</div>

## Methods

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <ul>
                    <li><p><b>Logistic regression:</b> one weight per attribute, as in Lecture 4</p></li>
                    <li><p><b>One hidden layer:</b> a network that learns its own attributes, with a logistic regression on top</p></li>
                    <li><p><b>Transformers:</b> the architecture inside the text encoder used in Lecture 4</p></li>
                </ul>
                <p>These apply to different data sources (e.g., loans, patients, articles, etc).</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/colored-neural-network.svg" alt="A network with an input, a hidden and an output layer" style="height: auto; max-width: 100%; max-height: 90%;">
                <div class="footnote">Colored neural network - Glosser.ca, CC BY-SA 3.0 <https://creativecommons.org/licenses/by-sa/3.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->

{% include _snippets/logistic-regression.md %}

{% include _snippets/one-hidden-layer-network.md %}

<!-- SLIDES: -->

## Transformers

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p>Last time, in Lecture 4, the text encoder was a transformer. The BERT description and the architecture figure are in that lecture. Here we look at the mechanism inside it.</p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->

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
