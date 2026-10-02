---
course_code: 26-pucp-ml-tutorials
title: Transformers and Situating LLMs
description: Whiteboard intuition for the transformer architecture (attention, multi-head, encoder/decoder sketch), situating LLMs against the October neural-network block, and a minimal LLM demo with civil-engineering fitness criteria for when not to use an LLM.
session: 4
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
lecture_code: transformers
lecture_date: 23/11/2026
permalink: /teaching/26-pucp-ml-tutorials/transformers/
notebook_title: Transformadores y LLMs
notebook_description: Práctica de sesión 4 — atención mínima y demo LLM con fallback offline (host programa #8).
---

<!-- ALL: content that goes everywhere -->
<!-- SLIDES: content that only goes to slides -->
<!-- RENDER: content that only goes to rendered markdown -->
<!-- NOTEBOOK: content that only goes to notebook -->
<!-- SLIDES+RENDER: content that goes to both rendered markdown and slides -->

<!-- SLIDES: -->

# Where We Left October

<!-- end SLIDES: -->

<!-- SLIDES+RENDER: -->

## Bridge from sessions 1–3

MLP / CNN block emphasised representation learning on structured or grid data. After the host CV / PINN block, we ask what changes for **language-scale** models: representation, scale, and **interface**.

Host programme number for this meeting: **#8** (our continuous session **4**).

<!-- end SLIDES+RENDER: -->

<!-- SLIDES: -->

# The Transformer Architecture

<!-- end SLIDES: -->

{% include _snippets/transformer.md %}

<!-- SLIDES: -->

# Large Language Models

<!-- end SLIDES: -->

{% include _snippets/llms.md %}

<!-- SLIDES: -->

# Civil Fitness

<!-- end SLIDES: -->

<!-- SLIDES+RENDER: -->

## When an LLM might help vs not

- Help: drafting, retrieval-mediated Q&A over **approved** docs, summarising known sources.
- Not enough alone: code-compliance decisions, unverified numerical claims, safety-critical advice without review.
- Prefer tabular NN / classical models when features are structured and labels clear.

<!-- end SLIDES+RENDER: -->

<!-- SLIDES: -->

# Lab Launch

<!-- end SLIDES: -->

<!-- NOTEBOOK: -->

# Introducción práctica

Exploramos atención a escala toy y un demo mínimo de LLM (API si hay clave; si no, fallback offline).

## Objetivos

1. Implementar un producto Q·Kᵀ / softmax toy para ver pesos de atención.
2. Llamar un LLM (o simular) con una pregunta civil.
3. Mapear cuándo preferir tabular NN / modelo clásico vs interfaz LLM.

```python
import numpy as np

def toy_attention(Q, K, V):
    scores = Q @ K.T / np.sqrt(K.shape[-1])
    weights = np.exp(scores - scores.max(axis=-1, keepdims=True))
    weights = weights / weights.sum(axis=-1, keepdims=True)
    return weights @ V, weights

Q = np.random.randn(4, 8)
K = np.random.randn(4, 8)
V = np.random.randn(4, 8)
out, w = toy_attention(Q, K, V)
print(out.shape, w.round(2))
```

### Fallback offline

Si no hay API, describe en markdown la salida esperada y los riesgos de sobreconfianza.

### Ticket de salida

Una pregunta de ingeniería civil → ¿transformer/LLM o modelo tabular/clásico? Justifica en una frase.

<!-- end NOTEBOOK: -->

<!-- SLIDES: -->

# Preview Session 5

<!-- end SLIDES: -->

<!-- SLIDES+RENDER: -->

## Next (host programme #9)

Prompting · minimal RAG · contrast with light fine-tuning · limits and misuse risks.

<!-- end SLIDES+RENDER: -->
