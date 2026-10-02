---
author: Christian Cabrera Jojoa
course_code: 26-pucp-ml-tutorials
department: Department of Computer Science and Technology
description: Practical prompting patterns, a minimal RAG loop (retrieve, ground, generate),
  contrast of prompt-only vs RAG vs light fine-tuning, and explicit limits and misuse
  risks (hallucination, over-trust, leakage, unsafe advice) in engineering contexts.
email: chc79@cam.ac.uk
end_time: 1:00 pm
hours: 3
institution: University of Cambridge
layout: lecture
lecture_code: prompting-rag-ft
lecture_date: 30/11/2026
notebook_description: "Pr\xE1ctica de sesi\xF3n 5 \u2014 prompting, RAG en memoria\
  \ y contraste con FT (host programa"
notebook_language: es
notebook_title: Prompting, RAG y fine-tuning ligero
permalink: /teaching/26-pucp-ml-tutorials/prompting-rag-ft/
position: Assistant Research Professor
session: 5
start_time: 10:00 am
title: Prompting, RAG and Fine-Tuning
visible: false
---

<link rel="stylesheet" href="/assets/css/slides.css">
<link rel="stylesheet" href="/assets/css/lecture-article.css">
<div class="lecture-resources">
  <p>
    <a href="/assets/slides/26-pucp-ml-tutorials/prompting-rag-ft.html" target="_blank" rel="noopener noreferrer">HTML slides</a> &nbsp;|&nbsp; <a href="https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-pucp-ml-tutorials/prompting-rag-ft.ipynb" target="_blank" rel="noopener noreferrer">Notebook - Individual</a>
  </p>
</div>
## Session framing

Host programme **#9** / our session **5**. Transformers give an interface; today we choose **how** to specialise behaviour: prompt, retrieve, or fine-tune — with risks visible.

## Patterns that improve fitness

- Role + task + constraints + output format.
- Few-shot exemplars when the schema matters.
- Ask for uncertainty / abstention when evidence is thin.
- Limits of prompt-only: no fresh private knowledge; brittle on long or conflicting context.

## Retrieve → ground → generate

1. Index approved documents (chunk + embed or keyword).
2. Retrieve top-k for the query.
3. Generate **conditioned** on retrieved text; cite or quote spans.
4. Failure modes: wrong chunk, outdated corpus, citation washing, still possible hallucination.

## When FT is warranted

- Stable task format, enough clean examples, need consistent style/schema.
- Costly vs prompt/RAG; risk of overfitting and data leakage from training corpus.
- Prefer smallest change that meets the decision requirement.

## Prompt / RAG / FT

| Approach | Adds | Best when | Main risk |
|----------|------|-----------|-----------|
| Prompt-only | Instructions | Public knowledge + clear format | Brittleness, no private docs |
| RAG | External evidence | Answers must cite corpus | Bad retrieval, over-trust |
| Light FT | Weight updates | Stable specialised behaviour | Leakage, cost, drift |

## Engineering-relevant risks

- Hallucination · over-trust · data leakage · unsafe advice.
- Mitigations: human review, abstain policy, logging, data boundaries, never skip code/standards checks.

## Handoff

Host programme **#10** (AI Agents, co-trainer). Our five sessions close here with risks and choice criteria explicit.
