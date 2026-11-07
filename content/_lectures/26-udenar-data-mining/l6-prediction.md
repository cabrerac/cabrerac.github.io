---
author: Christian Cabrera Jojoa
course_code: 26-udenar-data-mining
department: Department of Computer Science and Technology
description: Lecture 6 introduces classification. The data are a table of item attributes
  and a given class label. The label is not taken from the text, and it is not a popularity
  count. The same linear model is regression when the label is a number. This lecture
  uses a class label. We give a short history of supervised prediction, then three
  methods, each with its own data preparation. The basic method is logistic regression,
  prepared as scaled numbers and encoded categories, and scored against a majority-class
  baseline. The intermediate method is a random forest, prepared on the same table
  with missing values filled and categories encoded. The advanced method is a neural
  network with one hidden layer, prepared as a fully numeric scaled table with missing
  values filled. Each method is taught with its mathematics, its preparation, and
  a Python implementation. The prediction is judged by how many marked examples it
  gets right and how many it gets wrong. The lecture closes by adding this result
  to the earlier ones. Each item shows how many results support it, and we state what
  would change its place on the list.
email: chc79@cam.ac.uk
end_time: 01:00 pm
group_notebook: week-3-group
hours: 5
institution: University of Cambridge
layout: lecture
lecture_code: l6-prediction
lecture_date: 28/11/2026
notebook_description: "Pr\xE1ctica individual de la Lecci\xF3n 6. Predecir una etiqueta\
  \ dada a partir de los atributos del art\xEDculo, sin usar el texto ni un conteo\
  \ de popularidad, y contar aciertos y errores sobre ejemplos marcados."
notebook_language: es
notebook_title: "Clasificaci\xF3n, regresi\xF3n y una etiqueta dada"
permalink: /teaching/26-udenar-data-mining/l6-prediction/
position: Assistant Research Professor
session: 6
start_time: 07:00 am
title: Classification, regression, and a given label
visible: false
---

<link rel="stylesheet" href="/assets/css/slides.css">
<link rel="stylesheet" href="/assets/css/lecture-article.css">
<div class="lecture-resources">
  <p>
    <a href="/assets/slides/26-udenar-data-mining/l6-prediction.html" target="_blank" rel="noopener noreferrer">HTML slides</a> &nbsp;|&nbsp; <a href="https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-data-mining/l6-prediction.ipynb" target="_blank" rel="noopener noreferrer">Notebook - Individual</a> &nbsp;|&nbsp; <a href="https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-data-mining/week-3-group.ipynb" target="_blank" rel="noopener noreferrer">Notebook - Group</a>
  </p>
</div>
### Week 3 links

- [Week 3 hub](/teaching/26-udenar-data-mining/week-3-hub/)

### Resources

- [scikit-learn `LogisticRegression`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html)
- [scikit-learn `RandomForestClassifier`](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html)
- [scikit-learn `MLPClassifier`](https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html)
- [scikit-learn `DummyClassifier`](https://scikit-learn.org/stable/modules/generated/sklearn.dummy.DummyClassifier.html)

### References

- LeCun, Y., Bengio, Y., & Hinton, G. (2015). [Deep learning](https://doi.org/10.1038/nature14539). *Nature*, 521, 436-444.
- Breiman, L. (2001). [Random forests](https://doi.org/10.1023/A:1010933404324). *Machine Learning*, 45(1), 5-32.
- Bishop, C. M., & Bishop, H. (2024). [Deep learning: Foundations and concepts](https://doi.org/10.1007/978-3-031-45468-4). Springer. Chapter 5, Single-layer networks: Classification, pp. 131-169, and Chapter 6, Deep neural networks, pp. 171-207.
