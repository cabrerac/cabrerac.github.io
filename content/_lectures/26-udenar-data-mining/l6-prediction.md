---
author: Christian Cabrera Jojoa
course_code: 26-udenar-data-mining
department: Department of Computer Science and Technology
description: Lecture 6 is the prediction task. The question is whether the attributes
  of an item can predict a label that someone gave. Loans, patients, and articles
  in a table with a given label can feed the task. We explore three methods for this
  task. Logistic regression, a neural network with one hidden layer, and transformers.
  For logistic regression and the network we go through theory and implementation.
  For transformers we explain the mechanism, without training one. We then evaluate
  the trained methods on marked items they never saw. We end with what deploying a
  prediction means and its limits.
email: chc79@cam.ac.uk
end_time: 01:00 pm
group_notebook: week-3-group
hours: 5
institution: University of Cambridge
layout: lecture
lecture_code: l6-prediction
lecture_date: 28/11/2026
notebook_description: "Pr\xE1ctica individual de la Lecci\xF3n 6. Predecir desde el\
  \ resumen si un art\xEDculo se debe leer, con la etiqueta de tema de la Lecci\xF3\
  n 4. Comparar la regresi\xF3n log\xEDstica y una red con una capa oculta, y contar\
  \ aciertos y errores sobre art\xEDculos apartados."
notebook_language: es
notebook_title: "Predicci\xF3n"
permalink: /teaching/26-udenar-data-mining/l6-prediction/
position: Assistant Research Professor
session: 6
start_time: 07:00 am
title: Prediction
visible: true
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
- [scikit-learn `MLPClassifier`](https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html)
- [scikit-learn `DummyClassifier`](https://scikit-learn.org/stable/modules/generated/sklearn.dummy.DummyClassifier.html)

### References

- Bishop, C. M., & Bishop, H. (2024). [Deep learning: Foundations and concepts](https://doi.org/10.1007/978-3-031-45468-4). Springer. Chapter 5, Single-layer networks: Classification, pp. 131-169, and Chapter 6, Deep neural networks, pp. 171-207.
- LeCun, Y., Bengio, Y., & Hinton, G. (2015). [Deep learning](https://doi.org/10.1038/nature14539). *Nature*, 521, 436-444.
- Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, Ł., & Polosukhin, I. (2017). [Attention is all you need](https://doi.org/10.48550/arXiv.1706.03762). *Advances in Neural Information Processing Systems*, 30.
- Devlin, J., Chang, M.-W., Lee, K., & Toutanova, K. (2019). [BERT: Pre-training of deep bidirectional transformers for language understanding](https://doi.org/10.18653/v1/N19-1423). *Proceedings of NAACL-HLT 2019*, 4171-4186.
