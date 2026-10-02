---
author: Christian Cabrera Jojoa
course_code: 26-pucp-ml-tutorials
department: Department of Computer Science and Technology
description: "From the perceptron to multilayer networks \u2014 forward pass, loss,\
  \ back-propagation intuition, train/validation discipline, a survey of MLP vs CNN\
  \ selection criteria, and an introduction to convolution and kernels by the end\
  \ of the session."
email: chc79@cam.ac.uk
end_time: 1:00 pm
hours: 3
institution: University of Cambridge
layout: lecture
lecture_code: neural-networks-cnn
lecture_date: 19/10/2026
notebook_description: "Pr\xE1ctica de sesi\xF3n 3 \u2014 FFN train/val e introducci\xF3\
  n a convoluciones (MNIST stand-in)."
notebook_language: es
notebook_title: "Redes neuronales y introducci\xF3n a CNN"
permalink: /teaching/26-pucp-ml-tutorials/neural-networks-cnn/
position: Assistant Research Professor
session: 3
start_time: 10:00 am
title: Neural Networks, Architectures Survey and Intro CNN
visible: false
---

<link rel="stylesheet" href="/assets/css/slides.css">
<link rel="stylesheet" href="/assets/css/lecture-article.css">
<div class="lecture-resources">
  <p>
    <a href="/assets/slides/26-pucp-ml-tutorials/neural-networks-cnn.html" target="_blank" rel="noopener noreferrer">HTML slides</a> &nbsp;|&nbsp; <a href="https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-pucp-ml-tutorials/neural-networks-cnn.ipynb" target="_blank" rel="noopener noreferrer">Notebook - Individual</a>
  </p>
</div>
## Bridge

Stacking non-linear units yields function classes far beyond a single perceptron. We still ask: **does this architecture fit the decision and the data modality?**

## When to pick what (criteria)

| Family | Strengths | Typical data | Caution |
|--------|-----------|--------------|---------|
| MLP / FFN | Tabular, mixed features | Sensors, engineered features | Ignores spatial structure |
| CNN | Local patterns, translation | Images, grids, some signals | Needs enough spatial signal |
| Later (Nov) | Sequence / language interface | Text, long context | Not a default for every civil task |

Selection criteria: modality, locality, data volume, interpretability needs, deployment constraints.

## Kernels and weight sharing

- Convolution = local weighted sum + shared weights across positions.
- Stack: conv → nonlinearity → pooling → dense head (sketch only).
- Host CV block (programme **#4–6**) deepens vision; today is the **intro** handoff.

## Decision limits

State what a trained net **cannot** decide alone (safety margins, code compliance, missing sensors). Accuracy is not the civil decision.

## Programme handoff

Host CV / PINN block (sessions **#4–7**). We return **23 Nov** for transformers (our session **4** / host **#8**).
