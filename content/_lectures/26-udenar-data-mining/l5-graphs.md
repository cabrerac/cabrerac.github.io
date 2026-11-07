---
author: Christian Cabrera Jojoa
course_code: 26-udenar-data-mining
department: Department of Computer Science and Technology
description: Lecture 5 introduces the links among items in a graph. The data are items
  and the links among them. We give a short history of graph methods, then three methods,
  each with its own data preparation. The basic method is degree, prepared as an edge
  list of links that stay inside the set. A node that links to a large share of the
  others is a warning, not an automatic pick. The intermediate method is betweenness,
  prepared as an undirected graph on that edge list. The advanced method is node2vec,
  prepared as that graph plus the walks that build the embedding, with a fixed place
  for a node that has no neighbour. Each method is taught with its mathematics, its
  preparation, and a Python implementation. We characterise an item by its place among
  the other items. The lecture closes by adding this result to the earlier ones. Each
  item shows how many results support it, and we state what would change its place
  on the list.
email: chc79@cam.ac.uk
end_time: 01:00 pm
group_notebook: week-3-group
hours: 5
institution: University of Cambridge
layout: lecture
lecture_code: l5-graphs
lecture_date: 28/11/2026
notebook_description: "Pr\xE1ctica individual de la Lecci\xF3n 5. Describir un art\xED\
  culo por su lugar en las citas, no por cu\xE1ntas veces se lo nombra."
notebook_language: es
notebook_title: "Grafos y el lugar de un \xEDtem entre los dem\xE1s"
permalink: /teaching/26-udenar-data-mining/l5-graphs/
position: Assistant Research Professor
session: 5
start_time: 07:00 am
title: Graphs and an item's place among the others
visible: false
---

<link rel="stylesheet" href="/assets/css/slides.css">
<link rel="stylesheet" href="/assets/css/lecture-article.css">
<div class="lecture-resources">
  <p>
    <a href="/assets/slides/26-udenar-data-mining/l5-graphs.html" target="_blank" rel="noopener noreferrer">HTML slides</a> &nbsp;|&nbsp; <a href="https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-data-mining/l5-graphs.ipynb" target="_blank" rel="noopener noreferrer">Notebook - Individual</a> &nbsp;|&nbsp; <a href="https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-data-mining/week-3-group.ipynb" target="_blank" rel="noopener noreferrer">Notebook - Group</a>
  </p>
</div>
### Week 3 links

- [Week 3 hub](/teaching/26-udenar-data-mining/week-3-hub/)

### Resources

- [NetworkX `pagerank`](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.link_analysis.pagerank_alg.pagerank.html)
- [NetworkX `betweenness_centrality`](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.centrality.betweenness_centrality.html)
- [gensim `Word2Vec`](https://radimrehurek.com/gensim/models/word2vec.html)

### References

- Page, L., Brin, S., Motwani, R., & Winograd, T. (1998). [The PageRank citation ranking: Bringing order to the web](https://web.archive.org/web/20241231011600/http://ilpubs.stanford.edu:8090/422/). Stanford InfoLab technical report 1999-66.
- Freeman, L. C. (1977). [A set of measures of centrality based on betweenness](https://doi.org/10.2307/3033543). *Sociometry*, 40(1), 35-41.
- Brandes, U. (2001). [A faster algorithm for betweenness centrality](https://doi.org/10.1080/0022250X.2001.9990249). *Journal of Mathematical Sociology*, 25(2), 163-177.
- Grover, A., & Leskovec, J. (2016). [node2vec: Scalable feature learning for networks](https://doi.org/10.1145/2939672.2939754). *Proceedings of KDD 2016*, 855-864.
