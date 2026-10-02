---
author: Christian Cabrera Jojoa
course_code: 26-pucp-ml-tutorials
department: Department of Computer Science and Technology
description: From linear and logistic baselines to the perceptron as a building block
  for neural networks. We cover loss intuition, linear separability limits, and activation
  choice (linear, sigmoid, tanh, ReLU) for civil-engineering decision contexts.
email: chc79@cam.ac.uk
end_time: 1:00 pm
hours: 3
institution: University of Cambridge
layout: lecture
lecture_code: linear-perceptron
lecture_date: 12/10/2026
notebook_description: "Pr\xE1ctica de sesi\xF3n 2 \u2014 baselines lineal/log\xED\
  stico y perceptr\xF3n con justificaci\xF3n de activaci\xF3n."
notebook_language: es
notebook_title: "Modelos lineales y perceptr\xF3n"
permalink: /teaching/26-pucp-ml-tutorials/linear-perceptron/
position: Assistant Research Professor
session: 2
start_time: 10:00 am
title: Linear Models to the Perceptron
visible: false
---

<link rel="stylesheet" href="/assets/css/slides.css">
<link rel="stylesheet" href="/assets/css/lecture-article.css">
<div class="lecture-resources">
  <p>
    <a href="/assets/slides/26-pucp-ml-tutorials/linear-perceptron.html" target="_blank" rel="noopener noreferrer">HTML slides</a> &nbsp;|&nbsp; <a href="https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-pucp-ml-tutorials/linear-perceptron.ipynb" target="_blank" rel="noopener noreferrer">Notebook - Individual</a>
  </p>
</div>
## Fitness before the model

Session 1 locked success criteria and data-quality risks. Today we add **baselines** and the **perceptron** — still evaluating fitness for the decision, not accuracy alone.

## Outcomes (O3)

- Fit a linear / logistic baseline and interpret what it assumes.
- Explain the perceptron update and **linear separability** limits.
- Justify an **activation** choice for a simple task.

## Activation choice (intuition)

| Activation | Typical use | Watch-outs |
|------------|-------------|------------|
| Linear | Regression heads | No non-linearity |
| Sigmoid | Binary probs (classic) | Saturation / vanishing gradients |
| Tanh | Zero-centred classic | Still saturates |
| ReLU | Hidden layers (default start) | Dying ReLU; not a probability |

Match activation to the **decision surface** and training stability — not fashion.

## Next

Feed-forward nets, loss / back-prop intuition, architecture survey, **intro CNN**.
