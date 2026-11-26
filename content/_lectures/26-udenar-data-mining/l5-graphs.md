---
author: Christian Cabrera Jojoa
course_code: 26-udenar-data-mining
department: Department of Computer Science and Technology
description: Lecture 5 is the graph task. The question is where each item sits among
  the others. Papers and their citations, people and their friendships, and web pages
  and their links can feed the task. We explore three methods for this task. PageRank
  (with degree taught inside it), betweenness, and Louvain communities. For each method
  we go through its theory, implementation and evaluation. We end with what deploying
  an item's place means and its limits.
email: chc79@cam.ac.uk
end_time: 01:00 pm
group_notebook: week-3-group
hours: 5
institution: University of Cambridge
layout: lecture
lecture_code: l5-graphs
lecture_date: 28/11/2026
notebook_description: "Pr\xE1ctica individual de la Lecci\xF3n 5. Describir un art\xED\
  culo por su lugar en las citas con PageRank, intermediaci\xF3n y comunidades de\
  \ Louvain."
notebook_language: es
notebook_title: "Grafos y el lugar de un \xEDtem entre los dem\xE1s"
permalink: /teaching/26-udenar-data-mining/l5-graphs/
position: Assistant Research Professor
session: 5
start_time: 07:00 am
title: Graphs
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

### Papers and Reports

- Page, L., Brin, S., Motwani, R., & Winograd, T. (1998). [The PageRank citation ranking: Bringing order to the web](https://web.archive.org/web/20241231011600/http://ilpubs.stanford.edu:8090/422/). Stanford InfoLab technical report 1999-66.
- Freeman, L. C. (1977). [A set of measures of centrality based on betweenness](https://doi.org/10.2307/3033543). *Sociometry*, 40(1), 35-41.
- Brandes, U. (2001). [A faster algorithm for betweenness centrality](https://doi.org/10.1080/0022250X.2001.9990249). *Journal of Mathematical Sociology*, 25(2), 163-177.
- Newman, M. E. J., & Girvan, M. (2004). [Finding and evaluating community structure in networks](https://doi.org/10.1103/PhysRevE.69.026113). *Physical Review E*, 69(2), 026113.
- Blondel, V. D., Guillaume, J.-L., Lambiotte, R., & Lefebvre, E. (2008). [Fast unfolding of communities in large networks](https://doi.org/10.1088/1742-5468/2008/10/P10008). *Journal of Statistical Mechanics: Theory and Experiment*, 2008(10), P10008.

### Web

- [NetworkX `pagerank`](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.link_analysis.pagerank_alg.pagerank.html)
- [NetworkX `betweenness_centrality`](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.centrality.betweenness_centrality.html)
- [NetworkX `louvain_communities`](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.community.louvain.louvain_communities.html)
