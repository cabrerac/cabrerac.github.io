---
author: Christian Cabrera Jojoa
course_code: 26-udenar-data-mining
department: Department of Computer Science and Technology
description: Lecture 4 is the text extraction task. The question is what short answer
  each text gives to a question. Emails, reviews, and abstracts, with a sample marked
  by a person, can feed the task. We explore three methods for this task. A keyword
  list, TF-IDF with logistic regression, and a text encoder. For each method we go
  through its theory, implementation and evaluation. We end with what deploying an
  extraction means and its limits.
email: chc79@cam.ac.uk
end_time: 01:00 pm
group_notebook: week-2-group
hours: 5
institution: University of Cambridge
layout: lecture
lecture_code: l4-text
lecture_date: 21/11/2026
notebook_description: "Pr\xE1ctica individual de la Lecci\xF3n 4. Extraer de los res\xFA\
  menes lo que la pregunta pide y contar aciertos y errores sobre ejemplos marcados."
notebook_language: es
notebook_title: "Extracci\xF3n de texto y ejemplos marcados"
permalink: /teaching/26-udenar-data-mining/l4-text/
position: Assistant Research Professor
session: 4
start_time: 07:00 am
title: Text extraction and marked examples
visible: false
---

<link rel="stylesheet" href="/assets/css/slides.css">
<link rel="stylesheet" href="/assets/css/lecture-article.css">
<div class="lecture-resources">
  <p>
    <a href="/assets/slides/26-udenar-data-mining/l4-text.html" target="_blank" rel="noopener noreferrer">HTML slides</a> &nbsp;|&nbsp; <a href="https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-data-mining/l4-text.ipynb" target="_blank" rel="noopener noreferrer">Notebook - Individual</a> &nbsp;|&nbsp; <a href="https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-data-mining/week-2-group.ipynb" target="_blank" rel="noopener noreferrer">Notebook - Group</a>
  </p>
</div>
### Week 2 links

- [Week 2 hub](/teaching/26-udenar-data-mining/week-2-hub/)

### Resources

- [scikit-learn `TfidfVectorizer`](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html)
- [scikit-learn `LogisticRegression`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html)
- [`intfloat/multilingual-e5-small` model card](https://huggingface.co/intfloat/multilingual-e5-small)

### References

- Devlin, J., Chang, M.-W., Lee, K., & Toutanova, K. (2019). [BERT: Pre-training of deep bidirectional transformers for language understanding](https://doi.org/10.18653/v1/N19-1423). *Proceedings of NAACL-HLT 2019*, 4171-4186.
- Salton, G., & Buckley, C. (1988). [Term-weighting approaches in automatic text retrieval](https://doi.org/10.1016/0306-4573(88)90021-0). *Information Processing & Management*, 24(5), 513-523.
- Wang, L., Yang, N., Huang, X., Yang, L., Majumder, R., & Wei, F. (2024). [Multilingual E5 text embeddings: A technical report](https://arxiv.org/abs/2402.05672). *arXiv:2402.05672*.
