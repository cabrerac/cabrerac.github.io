---
author: Christian Cabrera Jojoa
course_code: 26-pucp-ml-tutorials
department: Department of Computer Science and Technology
description: Whiteboard intuition for the transformer architecture (attention, multi-head,
  encoder/decoder sketch), situating LLMs against the October neural-network block,
  and a minimal LLM demo with civil-engineering fitness criteria for when not to use
  an LLM.
email: chc79@cam.ac.uk
end_time: 1:00 pm
hours: 3
institution: University of Cambridge
layout: lecture
lecture_code: transformers
lecture_date: 23/11/2026
notebook_description: "Pr\xE1ctica de sesi\xF3n 4 \u2014 atenci\xF3n m\xEDnima y demo\
  \ LLM con fallback offline (host programa"
notebook_language: es
notebook_title: Transformadores y LLMs
permalink: /teaching/26-pucp-ml-tutorials/transformers/
position: Assistant Research Professor
session: 4
start_time: 10:00 am
title: Transformers and Situating LLMs
visible: false
---

<link rel="stylesheet" href="/assets/css/slides.css">
<link rel="stylesheet" href="/assets/css/lecture-article.css">
<div class="lecture-resources">
  <p>
    <a href="/assets/slides/26-pucp-ml-tutorials/transformers.html" target="_blank" rel="noopener noreferrer">HTML slides</a> &nbsp;|&nbsp; <a href="https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-pucp-ml-tutorials/transformers.ipynb" target="_blank" rel="noopener noreferrer">Notebook - Individual</a>
  </p>
</div>
## Bridge from sessions 1–3

MLP / CNN block emphasised representation learning on structured or grid data. After the host CV / PINN block, we ask what changes for **language-scale** models: representation, scale, and **interface**.

Host programme number for this meeting: **#8** (our continuous session **4**).

## When an LLM might help vs not

- Help: drafting, retrieval-mediated Q&A over **approved** docs, summarising known sources.
- Not enough alone: code-compliance decisions, unverified numerical claims, safety-critical advice without review.
- Prefer tabular NN / classical models when features are structured and labels clear.

## Next (host programme #9)

Prompting · minimal RAG · contrast with light fine-tuning · limits and misuse risks.
