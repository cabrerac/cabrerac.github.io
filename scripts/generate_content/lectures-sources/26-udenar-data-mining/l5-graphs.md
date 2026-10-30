---
course_code: 26-udenar-data-mining
title: Graphs and an item's place among the others
description: Lecture 5 introduces the links among items in a graph. The data are items and the links among them. We give a short history of graph methods, then three methods, each with its own data preparation. The basic method is degree, prepared as an edge list of links that stay inside the set. A node that links to a large share of the others is a warning, not an automatic pick. The intermediate method is betweenness, prepared as an undirected graph on that edge list. The advanced method is node2vec, prepared as that graph plus the walks that build the embedding, with a fixed place for a node that has no neighbour. Each method is taught with its mathematics, its preparation, and a Python implementation. We characterise an item by its place among the other items. The lecture closes by adding this result to the earlier ones. An item stays in view only when at least two results support it, and we state what would change that.
session: 5
start_time: 07:00 am
end_time: 01:00 pm
hours: 5
author: Christian Cabrera Jojoa
email: chc79@cam.ac.uk
position: Assistant Research Professor
department: Department of Computer Science and Technology
institution: University of Cambridge
layout: lecture
lecture_code: l5-graphs
lecture_date: 21/11/2026
permalink: /teaching/26-udenar-data-mining/l5-graphs/
visible: false
notebook_language: es
notebook_title: Grafos y el lugar de un ítem entre los demás
notebook_description: Práctica individual de la Lección 5. Describir un artículo por su lugar en las citas, no por cuántas veces se lo nombra.
---

{% include _snippets/26-udenar-data-mining/l5-graphs/resources.md %}
{% include _snippets/26-udenar-data-mining/l5-graphs/practical.md %}
