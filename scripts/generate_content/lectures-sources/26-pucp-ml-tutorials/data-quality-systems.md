---
course_code: 26-pucp-ml-tutorials
title: Data Quality, Systems Framing and AI Narrative
description: We open with a systems view for prioritising civil-engineering decisions before modelling, walk a concise AI history timeline through 2025 Agentic AI and 2026 Multi-Agent Systems, then diagnose data quality as fitness for purpose (garbage-in framing) using a structural-sensor stand-in.
session: 1
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
lecture_code: data-quality-systems
lecture_date: 05/10/2026
permalink: /teaching/26-pucp-ml-tutorials/data-quality-systems/
notebook_title: Diagnóstico de calidad de datos y priorización de problemas
notebook_description: Práctica de sesión 1 — inspeccionar y diagnosticar calidad de datos (stand-in de sensores estructurales).
---

<!-- ALL: content that goes everywhere -->
<!-- SLIDES: content that only goes to slides -->
<!-- RENDER: content that only goes to rendered markdown -->
<!-- NOTEBOOK: content that only goes to notebook -->
<!-- SLIDES+RENDER: content that goes to both rendered markdown and slides -->
<!-- SLIDES+NOTEBOOK: content that goes to both slides and notebook -->
<!-- RENDER+NOTEBOOK: content that goes to both rendered markdown and notebook -->

<!-- SLIDES: -->

# Session Outcomes

<!-- end SLIDES: -->

<!-- SLIDES+RENDER: -->

## What you will be able to do

- Frame a civil / seismic decision with stakeholders, constraints, and success criteria **before** choosing a model.
- Place current tooling on a short history arc through **2025 Agentic AI** and **2026 Multi-Agent Systems** (context, not today's lab).
- Diagnose data quality as **fitness for a purpose** and list concrete risks (missingness, units, leakage, labels).

<!-- end SLIDES+RENDER: -->

<!-- SLIDES: -->

# How We Work

<!-- end SLIDES: -->

<!-- SLIDES+RENDER: -->

## Delivery pattern

- Slides in English; talk and notebooks in Spanish.
- Online; Colab-preferred notebooks; formative checks only.
- This lead owns sessions **1-5** (programme host numbers 1-3 and 8-9).

<!-- end SLIDES+RENDER: -->

<!-- SLIDES: -->

# Systems View First

<!-- end SLIDES: -->

{% include _snippets/problem-first.md %}

{% include _snippets/sys-eng-approach.md %}

<!-- SLIDES: -->

# Prioritise Before Modelling

<!-- end SLIDES: -->

<!-- SLIDES+RENDER: -->

## Civil / seismic vignette (placeholder)

Example decision: prioritise **retrofit screening** versus a new **sensor campaign**. Name the stakeholder, the decision, one hard constraint, and what would count as success — **no model yet**.

<!-- end SLIDES+RENDER: -->

<!-- SLIDES: -->

# AI Narrative Timeline

<!-- end SLIDES: -->

{% include _snippets/early-neural-networks.md %}

{% include _snippets/deep-learning.md %}

<!-- SLIDES: -->

# Recent Arc

<!-- end SLIDES: -->

<!-- SLIDES+RENDER: -->

## Condensed timeline (fitness questions stay)

- Early neural networks → deep learning → transformers / LLMs
- **2025 Agentic AI** — tool-using loops; autonomy claims need evidence
- **2026 Multi-Agent Systems** — roles, coordination, over-trust risks
- Fancy models still fail on **unfit data** (garbage in / garbage out)

<!-- end SLIDES+RENDER: -->

{% include _snippets/agentic-ai.md %}

<!-- SLIDES: -->

# 2026 Multi-Agent Systems

<!-- end SLIDES: -->

<!-- SLIDES+RENDER: -->

## Multi-Agent Systems (context only)

- Multiple agents with roles, shared state, and handoffs.
- Coordination and evaluation become first-class; over-trust and unsafe advice remain risks in engineering settings.
- Host programme session **#10** (co-trainer) covers agents in depth — today this is narrative context only.

<!-- end SLIDES+RENDER: -->

<!-- SLIDES: -->

# Data Quality

<!-- end SLIDES: -->

{% include _snippets/data-quality.md %}

{% include _snippets/data-assess.md %}

<!-- SLIDES: -->

# Checklist

<!-- end SLIDES: -->

<!-- SLIDES+RENDER: -->

## Reusable diagnosis checklist

Schema · units · missingness · duplicates · leakage · temporal coverage · label quality · whether the data can answer the **stated decision**.

<!-- end SLIDES+RENDER: -->

<!-- SLIDES: -->

# Lab Launch

<!-- end SLIDES: -->

<!-- NOTEBOOK: -->

# Introducción práctica

En esta sesión diagnosticamos calidad de datos **antes** de modelar. Usaremos un CSV sintético de sensores estructurales (stand-in). El dataset sísmico real aún está por definir.

## Objetivos

1. Cargar e inspeccionar el stand-in.
2. Medir faltantes, duplicados, rangos y unidades sospechosas.
3. Redactar criterios de éxito y al menos dos riesgos de calidad ligados a una decisión civil.

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Stand-in: replace with course CSV path or upload in Colab
# df = pd.read_csv("sensor-structural-standin.csv")
print("Carga el CSV stand-in y revisa head/info/describe")
```

### Diagnóstico rápido

```python
# Ejemplo de checklist (adapta a tus columnas)
# print(df.isna().mean().sort_values(ascending=False))
# print(df.duplicated().sum())
# df.hist(figsize=(10, 8)); plt.tight_layout()
```

### Ticket de salida

Escribe: (a) criterios de éxito de la decisión; (b) al menos dos riesgos de calidad de datos y por qué importan.

<!-- end NOTEBOOK: -->

<!-- SLIDES: -->

# Preview Session 2

<!-- end SLIDES: -->

<!-- SLIDES+RENDER: -->

## Next

Linear and logistic baselines → the **perceptron** → activation choice.

<!-- end SLIDES+RENDER: -->
