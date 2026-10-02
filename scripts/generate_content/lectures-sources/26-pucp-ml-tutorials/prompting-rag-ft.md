---
course_code: 26-pucp-ml-tutorials
title: Prompting, RAG and Fine-Tuning
description: Practical prompting patterns, a minimal RAG loop (retrieve, ground, generate), contrast of prompt-only vs RAG vs light fine-tuning, and explicit limits and misuse risks (hallucination, over-trust, leakage, unsafe advice) in engineering contexts.
session: 5
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
lecture_code: prompting-rag-ft
lecture_date: 30/11/2026
permalink: /teaching/26-pucp-ml-tutorials/prompting-rag-ft/
notebook_title: Prompting, RAG y fine-tuning ligero
notebook_description: Práctica de sesión 5 — prompting, RAG en memoria y contraste con FT (host programa #9).
---

<!-- ALL: content that goes everywhere -->
<!-- SLIDES: content that only goes to slides -->
<!-- RENDER: content that only goes to rendered markdown -->
<!-- NOTEBOOK: content that only goes to notebook -->
<!-- SLIDES+RENDER: content that goes to both rendered markdown and slides -->

<!-- SLIDES: -->

# Recap Transformers as Interface

<!-- end SLIDES: -->

<!-- SLIDES+RENDER: -->

## Session framing

Host programme **#9** / our session **5**. Transformers give an interface; today we choose **how** to specialise behaviour: prompt, retrieve, or fine-tune — with risks visible.

<!-- end SLIDES+RENDER: -->

<!-- SLIDES: -->

# Prompting as Specification

<!-- end SLIDES: -->

<!-- SLIDES+RENDER: -->

## Patterns that improve fitness

- Role + task + constraints + output format.
- Few-shot exemplars when the schema matters.
- Ask for uncertainty / abstention when evidence is thin.
- Limits of prompt-only: no fresh private knowledge; brittle on long or conflicting context.

<!-- end SLIDES+RENDER: -->

<!-- SLIDES: -->

# Minimal RAG

<!-- end SLIDES: -->

<!-- SLIDES+RENDER: -->

## Retrieve → ground → generate

1. Index approved documents (chunk + embed or keyword).
2. Retrieve top-k for the query.
3. Generate **conditioned** on retrieved text; cite or quote spans.
4. Failure modes: wrong chunk, outdated corpus, citation washing, still possible hallucination.

<!-- end SLIDES+RENDER: -->

<!-- SLIDES: -->

# Light Fine-Tuning

<!-- end SLIDES: -->

<!-- SLIDES+RENDER: -->

## When FT is warranted

- Stable task format, enough clean examples, need consistent style/schema.
- Costly vs prompt/RAG; risk of overfitting and data leakage from training corpus.
- Prefer smallest change that meets the decision requirement.

<!-- end SLIDES+RENDER: -->

<!-- SLIDES: -->

# Contrast Table

<!-- end SLIDES: -->

<!-- SLIDES+RENDER: -->

## Prompt / RAG / FT

| Approach | Adds | Best when | Main risk |
|----------|------|-----------|-----------|
| Prompt-only | Instructions | Public knowledge + clear format | Brittleness, no private docs |
| RAG | External evidence | Answers must cite corpus | Bad retrieval, over-trust |
| Light FT | Weight updates | Stable specialised behaviour | Leakage, cost, drift |

<!-- end SLIDES+RENDER: -->

<!-- SLIDES: -->

# Risks and Mitigations

<!-- end SLIDES: -->

<!-- SLIDES+RENDER: -->

## Engineering-relevant risks

- Hallucination · over-trust · data leakage · unsafe advice.
- Mitigations: human review, abstain policy, logging, data boundaries, never skip code/standards checks.

<!-- end SLIDES+RENDER: -->

<!-- SLIDES: -->

# Lab Launch

<!-- end SLIDES: -->

<!-- NOTEBOOK: -->

# Introducción práctica

Practicamos prompting, un RAG mínimo en memoria, y contrastamos con fine-tuning ligero (conceptual si no hay GPU).

## Objetivos

1. Diseñar prompts con criterios de aptitud.
2. Implementar retrieve	o generate sobre un corpus pequeño en memoria.
3. Elegir prompt / RAG / FT para una viñeta y nombrar un riesgo + mitigación.

```python
corpus = {
    "doc1": "La inspeccion visual no sustituye ensayos normados.",
    "doc2": "Los sensores acelerometricos requieren calibracion periodica.",
    "doc3": "Un modelo predictivo no aprueba por si solo un reforzamiento estructural.",
}

def retrieve(query, corpus, k=2):
    # ranking toy por solapamiento de tokens
    q = set(query.lower().split())
    scored = sorted(corpus.items(), key=lambda kv: len(q & set(kv[1].lower().split())), reverse=True)
    return scored[:k]

hits = retrieve("calibracion de sensores", corpus)
print(hits)
# Genera una respuesta condicionada a hits (API o plantilla offline)
```

### Ticket de salida

Viñeta: elige enfoque, un riesgo de mal uso, y una mitigación.

<!-- end NOTEBOOK: -->

<!-- SLIDES: -->

# Close

<!-- end SLIDES: -->

<!-- SLIDES+RENDER: -->

## Handoff

Host programme **#10** (AI Agents, co-trainer). Our five sessions close here with risks and choice criteria explicit.

<!-- end SLIDES+RENDER: -->
