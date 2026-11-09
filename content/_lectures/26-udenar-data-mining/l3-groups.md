---
author: Christian Cabrera Jojoa
course_code: 26-udenar-data-mining
department: Department of Computer Science and Technology
description: Lecture 3 is the grouping task. The question is which items are similar
  enough to share a group, and which fit no group. Customers, patients, and texts
  described by the same attributes can feed the task. We explore three methods for
  this task. k-means, Gaussian mixtures, and HDBSCAN. For each method we go through
  its theory, implementation and evaluation. We end with what deploying a group means
  and its limits.
email: chc79@cam.ac.uk
end_time: 01:00 pm
group_notebook: week-2-group
hours: 5
institution: University of Cambridge
layout: lecture
lecture_code: l3-groups
lecture_date: 21/11/2026
notebook_description: "Pr\xE1ctica individual de la Lecci\xF3n 3. Agrupar art\xED\
  culos parecidos, marcar los que no encajan en ning\xFAn grupo y decir qu\xE9 significa\
  \ un grupo para la lectura."
notebook_language: es
notebook_title: "Grupos, at\xEDpicos y qu\xE9 significa un grupo"
permalink: /teaching/26-udenar-data-mining/l3-groups/
position: Assistant Research Professor
session: 3
start_time: 07:00 am
title: Groups, outliers, and what a group means
visible: false
---

<link rel="stylesheet" href="/assets/css/slides.css">
<link rel="stylesheet" href="/assets/css/lecture-article.css">
<div class="lecture-resources">
  <p>
    <a href="/assets/slides/26-udenar-data-mining/l3-groups.html" target="_blank" rel="noopener noreferrer">HTML slides</a> &nbsp;|&nbsp; <a href="https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-data-mining/l3-groups.ipynb" target="_blank" rel="noopener noreferrer">Notebook - Individual</a> &nbsp;|&nbsp; <a href="https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-data-mining/week-2-group.ipynb" target="_blank" rel="noopener noreferrer">Notebook - Group</a>
  </p>
</div>
### Week 2 links

- [Week 2 hub](/teaching/26-udenar-data-mining/week-2-hub/)

### Resources

- [scikit-learn clustering guide](https://scikit-learn.org/stable/modules/clustering.html)
- [scikit-learn `HDBSCAN`](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.HDBSCAN.html)
- [scikit-learn `TruncatedSVD`](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.TruncatedSVD.html)

### References

- Jain, A. K. (2010). [Data clustering: 50 years beyond K-means](https://doi.org/10.1016/j.patrec.2009.09.011). *Pattern Recognition Letters*, 31(8), 651-666.
- Campello, R. J. G. B., Moulavi, D., & Sander, J. (2013). [Density-based clustering based on hierarchical density estimates](https://doi.org/10.1007/978-3-642-37456-2_14). *PAKDD 2013*, 160-172.
- Bishop, C. M., & Bishop, H. (2024). [Deep learning: Foundations and concepts](https://doi.org/10.1007/978-3-031-45468-4). Springer. Chapter 15, Discrete latent variables, pp. 459-493 (k-means, Gaussian mixtures and EM).
