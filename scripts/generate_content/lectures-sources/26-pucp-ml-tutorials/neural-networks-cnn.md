---
course_code: 26-pucp-ml-tutorials
title: Neural Networks, Architectures Survey and Intro CNN
description: From the perceptron to multilayer networks — forward pass, loss, back-propagation intuition, train/validation discipline, a survey of MLP vs CNN selection criteria, and an introduction to convolution and kernels by the end of the session.
session: 3
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
lecture_code: neural-networks-cnn
lecture_date: 19/10/2026
permalink: /teaching/26-pucp-ml-tutorials/neural-networks-cnn/
notebook_title: Redes neuronales y introducción a CNN
notebook_description: Práctica de sesión 3 — FFN train/val e introducción a convoluciones (MNIST stand-in).
---

<!-- ALL: content that goes everywhere -->
<!-- SLIDES: content that only goes to slides -->
<!-- RENDER: content that only goes to rendered markdown -->
<!-- NOTEBOOK: content that only goes to notebook -->
<!-- SLIDES+RENDER: content that goes to both rendered markdown and slides -->

<!-- SLIDES: -->

# From Perceptron to Multilayer

<!-- end SLIDES: -->

<!-- SLIDES+RENDER: -->

## Bridge

Stacking non-linear units yields function classes far beyond a single perceptron. We still ask: **does this architecture fit the decision and the data modality?**

<!-- end SLIDES+RENDER: -->

<!-- SLIDES: -->

# Neural Networks

<!-- end SLIDES: -->

{% include _snippets/neural-networks.md %}

<!-- SLIDES: -->

# Deep Learning Sketch

<!-- end SLIDES: -->

{% include _snippets/deep-learning.md %}

<!-- SLIDES: -->

# Architecture Survey

<!-- end SLIDES: -->

<!-- SLIDES+RENDER: -->

## When to pick what (criteria)

| Family | Strengths | Typical data | Caution |
|--------|-----------|--------------|---------|
| MLP / FFN | Tabular, mixed features | Sensors, engineered features | Ignores spatial structure |
| CNN | Local patterns, translation | Images, grids, some signals | Needs enough spatial signal |
| Later (Nov) | Sequence / language interface | Text, long context | Not a default for every civil task |

Selection criteria: modality, locality, data volume, interpretability needs, deployment constraints.

<!-- end SLIDES+RENDER: -->

<!-- SLIDES: -->

# Intro CNN

<!-- end SLIDES: -->

<!-- SLIDES+RENDER: -->

## Kernels and weight sharing

- Convolution = local weighted sum + shared weights across positions.
- Stack: conv → nonlinearity → pooling → dense head (sketch only).
- Host CV block (programme **#4–6**) deepens vision; today is the **intro** handoff.

<!-- end SLIDES+RENDER: -->

<!-- SLIDES: -->

# Field Usefulness

<!-- end SLIDES: -->

<!-- SLIDES+RENDER: -->

## Decision limits

State what a trained net **cannot** decide alone (safety margins, code compliance, missing sensors). Accuracy is not the civil decision.

<!-- end SLIDES+RENDER: -->

<!-- SLIDES: -->

# Lab Launch

<!-- end SLIDES: -->

<!-- NOTEBOOK: -->

# Introducción práctica

Entrenamos un FFN pequeño con disciplina train/val e introducimos una CNN mínima (MNIST como stand-in).

## Objetivos

1. Entrenar un MLP y reportar train vs validación.
2. Esbozar forward / loss / back-prop en palabras.
3. Probar un mini-CNN y escribir una frase de límite de decisión en campo.

```python
import torch
import torch.nn as nn
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

transform = transforms.ToTensor()
# train_ds = datasets.MNIST(root="./data", train=True, download=True, transform=transform)
# loader = DataLoader(train_ds, batch_size=64, shuffle=True)

class TinyMLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(nn.Flatten(), nn.Linear(28*28, 128), nn.ReLU(), nn.Linear(128, 10))
    def forward(self, x):
        return self.net(x)

print("Define TinyCNN (Conv2d -> ReLU -> MaxPool -> Flatten -> Linear) y compara con TinyMLP")
```

### Ticket de salida

Elige MLP o CNN para un caso civil y nombra **un límite** de la decisión que el modelo no resuelve solo.

<!-- end NOTEBOOK: -->

<!-- SLIDES: -->

# Bridge Forward

<!-- end SLIDES: -->

<!-- SLIDES+RENDER: -->

## Programme handoff

Host CV / PINN block (sessions **#4–7**). We return **23 Nov** for transformers (our session **4** / host **#8**).

<!-- end SLIDES+RENDER: -->
