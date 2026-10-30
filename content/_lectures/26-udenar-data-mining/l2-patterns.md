---
author: Christian Cabrera Jojoa
course_code: 26-udenar-data-mining
department: Department of Computer Science and Technology
description: Lecture 2 introduces repeating patterns. The data are items that carry
  text. We give a short history of pattern mining, then three methods, each with its
  own data preparation. The basic method is frequent word pairs, prepared as a set
  of words per item. The intermediate method is lift, prepared from those pairs plus
  the count of each word alone, so a pair can be compared with an independence baseline.
  The advanced method is closeness in a pretrained word embedding, prepared by matching
  the words to that embedding's vocabulary. Each method is taught with its mathematics,
  its preparation, and a Python implementation. A pattern is worth keeping when it
  beats the other patterns and a baseline. One standout item is not a pattern. The
  lecture closes by stating how a kept pattern will be used in the later decision,
  and what would change that use.
email: chc79@cam.ac.uk
end_time: 01:00 pm
group_notebook: week-1-group
hours: 5
institution: University of Cambridge
layout: lecture
lecture_code: l2-patterns
lecture_date: 07/11/2026
notebook_description: "Pr\xE1ctica individual de la Lecci\xF3n 2. Encontrar patrones\
  \ que se repiten en la colecci\xF3n de art\xEDculos y comparar cada uno con los\
  \ otros patrones y con una l\xEDnea base."
notebook_language: es
notebook_title: "Patrones que se repiten y l\xEDneas base"
permalink: /teaching/26-udenar-data-mining/l2-patterns/
position: Assistant Research Professor
session: 2
start_time: 07:00 am
title: Repeating patterns and baselines
visible: false
---

<link rel="stylesheet" href="/assets/css/slides.css">
<link rel="stylesheet" href="/assets/css/lecture-article.css">
<div class="lecture-resources">
  <p>
    <a href="/assets/slides/26-udenar-data-mining/l2-patterns.html" target="_blank" rel="noopener noreferrer">HTML slides</a> &nbsp;|&nbsp; <a href="https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-data-mining/l2-patterns.ipynb" target="_blank" rel="noopener noreferrer">Notebook - Individual</a> &nbsp;|&nbsp; <a href="https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-data-mining/week-1-group.ipynb" target="_blank" rel="noopener noreferrer">Notebook - Group</a>
  </p>
</div>
### Week 1 links

- [Week 1 hub](/teaching/26-udenar-data-mining/week-1-hub/)

### Resources

- [spaCy English models](https://spacy.io/models/en)
- [spaCy Spanish models](https://spacy.io/models/es)
- [Python `itertools.combinations`](https://docs.python.org/3/library/itertools.html#itertools.combinations)

### References

- Agrawal, R., Imielinski, T., & Swami, A. (1993). [Mining association rules between sets of items in large databases](https://doi.org/10.1145/170036.170072). *ACM SIGMOD Record*, 22(2), 207-216.
- Brin, S., Motwani, R., Ullman, J. D., & Tsur, S. (1997). [Dynamic itemset counting and implication rules for market basket data](https://doi.org/10.1145/253262.253325). *ACM SIGMOD Record*, 26(2), 255-264.
- Gionis, A., Mannila, H., Mielikäinen, T., & Tsaparas, P. (2007). [Assessing data mining results via swap randomization](https://doi.org/10.1145/1297332.1297338). *ACM Transactions on Knowledge Discovery from Data*, 1(3), 14.
- Tan, P.-N., Kumar, V., & Srivastava, J. (2002). [Selecting the right interestingness measure for association patterns](https://doi.org/10.1145/775047.775053). *Proceedings of KDD 2002*, 32-41.
- Mikolov, T., Chen, K., Corrado, G., & Dean, J. (2013). [Efficient estimation of word representations in vector space](https://arxiv.org/abs/1301.3781). *arXiv:1301.3781*.
