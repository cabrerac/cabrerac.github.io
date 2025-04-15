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

<script src="https://cdn.jsdelivr.net/pyodide/v0.24.1/full/pyodide.js"></script>
<script>
    async function main() {
        let pyodide = await loadPyodide({ indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.24.1/full/'});
        await pyodide.loadPackage("numpy");
        await pyodide.loadPackage("matplotlib");
    }
    main();
</script>

<div class="lecture-resources">
  <p>
    <a href="/assets/slides/25-udenar-ml-intro/ml-introduction.pdf" target="_blank">[PDF Slides]</a>
    <a href="/assets/slides/25-udenar-ml-intro/ml-introduction.html" target="_blank">[HTML Slides]</a>
    <a href="https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/25-udenar-ml-intro/ml-introduction.ipynb" target="_blank">[Colab Notebook]</a>
  </p>
</div>

## Course Overview

Welcome to Introduction to Machine Learning! This course will provide you with a comprehensive understanding of machine learning concepts, algorithms, and practical applications.

# What is Machine Learning?

Machine Learning is a field of study that gives computers the ability to learn without being explicitly programmed. It's a subset of Artificial Intelligence that focuses on building systems that can learn from and make decisions based on data.

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

<script src="https://cdn.jsdelivr.net/pyodide/v0.24.1/full/pyodide.js"></script>
<script>
    async function main() {
        let pyodide = await loadPyodide({ indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.24.1/full/'});
        await pyodide.loadPackage("numpy");
        await pyodide.loadPackage("matplotlib");
    }
    main();
</script>

## Key Characteristics
- Data-driven approach
- Pattern recognition
- Statistical methods
- Iterative learning

<video width="100%" controls>
  <source src="/assets/media/videos/ml-intro.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

### Example: Creating a Simple Dataset

<div>
    <h3>Interactive Example</h3>
    <button onclick="runExample()">Run Example</button>
    <pre id="output"></pre>
</div>

<script>
    async function runExample() {
        let pyodide = await loadPyodide();
        await pyodide.loadPackage("numpy");
        await pyodide.loadPackage("matplotlib");
        let code = `
import numpy as np
import matplotlib.pyplot as plt

# Generate sample data
X = np.random.rand(100, 2)
y = np.array([1 if x[0] + x[1] > 1 else 0 for x in X])

# Plot the data
plt.scatter(X[:, 0], X[:, 1], c=y, cmap='viridis')
plt.title("Sample ML Dataset")
plt.xlabel("Feature 1")
plt.ylabel("Feature 2")
plt.show()
        `;
        await pyodide.runPythonAsync(code);
    }
</script>

### Example: Linear Regression

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
