---
layout: lecture
lecture_code: ml-introduction
title: "Introduction to Machine Learning"
description: "This lecture presents the course and a brief context and history of the Machine Learning (ML) field."
course_code: 25-udenar-ml-intro
lecture_date: 10/05/2025
start_time: "TBD"
end_time: "TBD"
hours: 4
session: 1
permalink: /teaching/25-udenar-ml-intro/ml-introduction/
visible: true
---

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

{% include _snippets/ml/what-is-ml.md %}

{% include _snippets/ml/history.md %}

{% include _snippets/ml/applications.md %}

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

### Example: Linear Regression

You can run the following code in your browser using Pyodide:

<div>
    <h3>Interactive Example</h3>
    <button onclick="runLinearRegression()">Run Linear Regression Example</button>
    <pre id="output"></pre>
</div>

<script>
    async function runLinearRegression() {
        let pyodide = await loadPyodide();
        let code = `
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Generate sample data
X = np.random.rand(100, 1) * 10  # Features
y = 2.5 * X + np.random.randn(100, 1) * 2  # Target with noise

# Fit linear regression model
model = LinearRegression()
model.fit(X, y)

# Predict
X_new = np.array([[0], [10]])
y_predict = model.predict(X_new)

# Plot the data and the regression line
plt.scatter(X, y, color='blue')
plt.plot(X_new, y_predict, color='red', linewidth=2)
plt.title("Linear Regression Example")
plt.xlabel("Feature")
plt.ylabel("Target")
plt.show()
        `;
        await pyodide.runPythonAsync(code);
    }
</script>

