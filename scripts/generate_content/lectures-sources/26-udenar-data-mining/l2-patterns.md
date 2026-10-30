---
course_code: 26-udenar-data-mining
title: Repeating patterns and baselines
description: Lecture 2 introduces repeating patterns. The data are items that carry text. We give a short history of pattern mining, then three methods, each with its own data preparation. The basic method is frequent word pairs, prepared as a set of words per item. The intermediate method is lift, prepared from those pairs plus the count of each word alone, so a pair can be compared with an independence baseline. The advanced method is closeness in a pretrained word embedding, prepared by matching the words to that embedding's vocabulary. Each method is taught with its mathematics, its preparation, and a Python implementation. A pattern is worth keeping when it beats the other patterns and a baseline. One standout item is not a pattern. The lecture closes by stating how a kept pattern will be used in the later decision, and what would change that use.
session: 2
start_time: 07:00 am
end_time: 01:00 pm
hours: 5
author: Christian Cabrera Jojoa
email: chc79@cam.ac.uk
position: Assistant Research Professor
department: Department of Computer Science and Technology
institution: University of Cambridge
layout: lecture
lecture_code: l2-patterns
lecture_date: 07/11/2026
permalink: /teaching/26-udenar-data-mining/l2-patterns/
visible: false
group_notebook: week-1-group
notebook_language: es
notebook_title: Patrones que se repiten y líneas base
notebook_description: Práctica individual de la Lección 2. Encontrar patrones que se repiten en la colección de artículos y comparar cada uno con los otros patrones y con una línea base.
---

<!-- SLIDES: -->

# Last Time

<!-- end SLIDES: -->

{% include _snippets/26-udenar-data-mining/l2-patterns/last-time.md %}

<!-- SLIDES: -->

# Repeating Patterns

<!-- end SLIDES: -->

{% include _snippets/pattern-mining.md %}

<!-- SLIDES: -->

# Text Preparation

<!-- end SLIDES: -->

{% include _snippets/text-preparation.md %}

<!-- SLIDES: -->

# Frequent Word Pairs

<!-- end SLIDES: -->

{% include _snippets/frequent-itemsets.md %}

<!-- SLIDES: -->

# Lift

<!-- end SLIDES: -->

{% include _snippets/lift.md %}

<!-- SLIDES: -->

# Word Embeddings

<!-- end SLIDES: -->

{% include _snippets/word-embeddings.md %}

<!-- SLIDES: -->

# Baselines

<!-- end SLIDES: -->

{% include _snippets/permutation-baseline.md %}

{% include _snippets/multiple-testing.md %}

{% include _snippets/swap-randomization.md %}

{% include _snippets/random-pair-baseline.md %}

<!-- SLIDES: -->

# Comparing the Methods

<!-- end SLIDES: -->

{% include _snippets/pattern-methods-comparison.md %}

{% include _snippets/26-udenar-data-mining/l2-patterns/comparison.md %}

<!-- SLIDES: -->

# Using a Pattern

<!-- end SLIDES: -->

{% include _snippets/pattern-to-decision.md %}

{% include _snippets/26-udenar-data-mining/l2-patterns/decision-use.md %}

<!-- SLIDES: -->

# Conclusions

<!-- end SLIDES: -->

{% include _snippets/26-udenar-data-mining/l2-patterns/conclusions.md %}

{% include _snippets/26-udenar-data-mining/l2-patterns/practical-slides.md %}

{% include _snippets/26-udenar-data-mining/l2-patterns/week1-deliverables.md %}

{% include _snippets/26-udenar-data-mining/l2-patterns/resources.md %}
{% include _snippets/26-udenar-data-mining/l2-patterns/practical.md %}
