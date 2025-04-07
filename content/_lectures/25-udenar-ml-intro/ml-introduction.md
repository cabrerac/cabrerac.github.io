---
course_code: 25-udenar-ml-intro
description: This lecture presents the course and a brief context and history of the
  Machine Learning (ML) field.
end_time: TBD
hours: 4
layout: lecture
lecture_code: ml-introduction
lecture_date: 10/05/2025
permalink: /teaching/25-udenar-ml-intro/ml-introduction/
session: 1
start_time: TBD
title: Introduction to Machine Learning
visible: true
---

<div class="lecture-resources">
  <p>
    <a href="/assets/slides/25-udenar-ml-intro/ml-introduction.pdf" target="_blank">[PDF Slides]</a>
    <a href="/assets/slides/25-udenar-ml-intro/ml-introduction.html" target="_blank">[HTML Slides]</a>
    <a href="https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/25-udenar-ml-intro/ml-introduction.ipynb" target="_blank">[Colab Notebook]</a>
  </p>
</div>



## Course Overview

Welcome to Introduction to Machine Learning! This course will provide you with a comprehensive understanding of machine learning concepts, algorithms, and practical applications.

### Course Structure
- 10 sessions of 4 hours each
- Combination of theory and practice
- Hands-on exercises using Python
- Interactive elements (polls, cloud numbers)

### Learning Objectives
By the end of this course, you will:
- Understand fundamental ML concepts
- Be able to implement basic ML algorithms
- Know how to evaluate ML models
- Have practical experience with real-world datasets

# What is Machine Learning?

Machine Learning is a field of study that gives computers the ability to learn without being explicitly programmed. It's a subset of Artificial Intelligence that focuses on building systems that can learn from and make decisions based on data.

![ML Overview](/assets/media/images/ml-overview.png)

## Key Characteristics
- Data-driven approach
- Pattern recognition
- Statistical methods
- Iterative learning

<video width="100%" controls>
  <source src="/assets/media/videos/ml-intro.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

## Interactive Example
Here's a simple example of how ML works:

```python
from sklearn.datasets import make_blobs
import matplotlib.pyplot as plt

# Generate sample data
X, y = make_blobs(n_samples=100, centers=2, random_state=42)

# Plot the data
plt.scatter(X[:, 0], X[:, 1], c=y)
plt.title("Sample ML Dataset")
plt.show()
``` 

# History of AI and ML

## Early Days (1950s-1960s)
- Alan Turing's "Turing Test"
- First neural networks
- Perceptron development

## AI Winter (1970s-1980s)
- Limited computing power
- High expectations vs. reality
- Funding cuts

## Renaissance (1990s-Present)
- Increased computing power
- Big data availability
- Deep learning revolution 

# ML Applications

## Current Applications
1. Computer Vision
   - Image recognition
   - Object detection
   - Medical imaging

2. Natural Language Processing
   - Machine translation
   - Sentiment analysis
   - Chatbots

3. Recommendation Systems
   - Content recommendations
   - Product suggestions
   - Personalized marketing

4. Healthcare
   - Disease diagnosis
   - Drug discovery
   - Patient care optimization 

## Benefits and Risks

### Benefits
- Automation of complex tasks
- Improved decision-making
- Personalization
- Efficiency gains

### Risks and Challenges
- Data privacy concerns
- Algorithmic bias
- Job displacement
- Ethical considerations

## Tools for ML Implementation

### Python Ecosystem
1. Core Libraries
   - NumPy: Numerical computing
   - Pandas: Data manipulation
   - Scikit-learn: ML algorithms
   - TensorFlow/PyTorch: Deep learning

2. Development Tools
   - Jupyter Notebooks
   - Google Colab
   - VS Code with Python extensions

### Practical Session
In this session's practical component, we will:
1. Set up our development environment
2. Explore basic Python libraries for ML
3. Create our first ML pipeline

## Resources

### Recommended Reading
- "Hands-On Machine Learning with Scikit-Learn and TensorFlow" by Aurélien Géron
- "Python for Data Analysis" by Wes McKinney
- Online courses and tutorials

### Additional Materials
- Course GitHub repository
- Discussion forum
- Office hours schedule

## Next Session Preview

In our next session, we will dive deeper into:
- Data preprocessing techniques
- Feature engineering
- Basic ML algorithms
- Model evaluation metrics

