---
course_code: 26-pucp-ml-tutorials
title: Linear Models to the Perceptron
description: From linear and logistic baselines to the perceptron as a building block for neural networks. We cover loss intuition, linear separability limits, and activation choice (linear, sigmoid, tanh, ReLU) for civil-engineering decision contexts.
session: 2
start_time: 10:00 am
end_time: 1:00 pm
hours: 3
author: Christian Cabrera Jojoa
email: chc79@cam.ac.uk
position: Assistant Research Professor
department: Department of Computer Science and Technology
institution: University of Cambridge
layout: lecture
notebook_language: es
visible: false
lecture_code: linear-perceptron
lecture_date: 12/10/2026
permalink: /teaching/26-pucp-ml-tutorials/linear-perceptron/
notebook_title: Modelos lineales y perceptrón
notebook_description: Práctica de sesión 2 — baselines lineal/logístico y perceptrón con justificación de activación.
---

<!-- ALL: content that goes everywhere -->
<!-- SLIDES: content that only goes to slides -->
<!-- RENDER: content that only goes to rendered markdown -->
<!-- NOTEBOOK: content that only goes to notebook -->
<!-- SLIDES+RENDER: content that goes to both rendered markdown and slides -->

<!-- SLIDES: -->

# Recap Session 1

<!-- end SLIDES: -->

<!-- SLIDES+RENDER: -->

## Fitness before the model

Session 1 locked success criteria and data-quality risks. Today we add **baselines** and the **perceptron** — still evaluating fitness for the decision, not accuracy alone.

<!-- end SLIDES+RENDER: -->

<!-- SLIDES: -->

# Session Outcomes

<!-- end SLIDES: -->

<!-- SLIDES+RENDER: -->

## Outcomes (O3)

- Fit a linear / logistic baseline and interpret what it assumes.
- Explain the perceptron update and **linear separability** limits.
- Justify an **activation** choice for a simple task.

<!-- end SLIDES+RENDER: -->

<!-- SLIDES: -->

# Linear Baselines

<!-- end SLIDES: -->

{% include _snippets/regression.md %}

{% include _snippets/multivariate-regression.md %}

<!-- SLIDES: -->

# Logistic Baseline

<!-- end SLIDES: -->

{% include _snippets/linear-classifiers.md %}

<!-- SLIDES: -->

# The Perceptron

<!-- end SLIDES: -->

{% include _snippets/perceptron.md %}

<!-- SLIDES: -->

# Activations

<!-- end SLIDES: -->

<!-- SLIDES+RENDER: -->

## Activation choice (intuition)

| Activation | Typical use | Watch-outs |
|------------|-------------|------------|
| Linear | Regression heads | No non-linearity |
| Sigmoid | Binary probs (classic) | Saturation / vanishing gradients |
| Tanh | Zero-centred classic | Still saturates |
| ReLU | Hidden layers (default start) | Dying ReLU; not a probability |

Match activation to the **decision surface** and training stability — not fashion.

<!-- end SLIDES+RENDER: -->

<!-- SLIDES: -->

# Lab Launch

<!-- end SLIDES: -->

<!-- NOTEBOOK: -->

# Introducción práctica

Construimos baselines y un perceptrón sencillo. Justifica la activación frente al baseline.

## Objetivos

1. Entrenar regresión lineal / logística como referencia.
2. Implementar o usar un perceptrón y observar separabilidad lineal.
3. Comparar activaciones en un ejemplo pequeño y justificar la elección.

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression, Perceptron
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

X, y = make_classification(n_samples=400, n_features=2, n_redundant=0,
                           n_informative=2, n_clusters_per_class=1, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

logit = LogisticRegression().fit(X_train, y_train)
perc = Perceptron().fit(X_train, y_train)
print("logit", accuracy_score(y_test, logit.predict(X_test)))
print("perceptron", accuracy_score(y_test, perc.predict(X_test)))
```

### Ticket de salida

¿Por qué elegiste una activación frente al baseline lineal/logístico para tu tarea?

<!-- end NOTEBOOK: -->

<!-- SLIDES: -->

# Preview Session 3

<!-- end SLIDES: -->

<!-- SLIDES+RENDER: -->

## Next

Feed-forward nets, loss / back-prop intuition, architecture survey, **intro CNN**.

<!-- end SLIDES+RENDER: -->
