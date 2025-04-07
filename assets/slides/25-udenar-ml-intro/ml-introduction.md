---
marp: true
theme: default
paginate: true
header: "Introduction to Machine Learning"
footer: "Session 1"
style: |
  section {
    background-color: white;
  }
  img {
    max-width: 100%;
    height: auto;
  }
  video {
    max-width: 100%;
  }

# Introduction to Machine Learning
## Session 1: This lecture presents the course and a brief context and history of the Machine Learning (ML) field.


---

## Course Overview

---

Welcome to Introduction to Machine Learning! This course will provide you with a comprehensive understanding of machine learning concepts, algorithms, and practical applications.

---

### Course Structure
- 10 sessions of 4 hours each
- Combination of theory and practice
- Hands-on exercises using Python
- Interactive elements (polls, cloud numbers)

---

### Learning Objectives
By the end of this course, you will:
- Understand fundamental ML concepts
- Be able to implement basic ML algorithms
- Know how to evaluate ML models
- Have practical experience with real-world datasets

---

# What is Machine Learning?

---

Machine Learning is a field of study that gives computers the ability to learn without being explicitly programmed. It's a subset of Artificial Intelligence that focuses on building systems that can learn from and make decisions based on data.

---

![ML Overview](/assets/media/images/ml-overview.png)

---

## Key Characteristics
- Data-driven approach
- Pattern recognition
- Statistical methods
- Iterative learning

---

<video width="100%" controls>
  <source src="/assets/media/videos/ml-intro.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

---

## Interactive Example
Here's a simple example of how ML works:

---

```python
from sklearn.datasets import make_blobs
import matplotlib.pyplot as plt

---

# Generate sample data
X, y = make_blobs(n_samples=100, centers=2, random_state=42)

---

# Plot the data
plt.scatter(X[:, 0], X[:, 1], c=y)
plt.title("Sample ML Dataset")
plt.show()
``` 

---

### Example: Creating a Simple Dataset

---

You can run the following code in your browser using Pyodide:

---

<div>
    <h3>Interactive Example</h3>
    <button onclick="runExample()">Run Example</button>
    <pre id="output"></pre>
</div>

---

<script>
    async function runExample() {
        let pyodide = await loadPyodide();
        await pyodide.loadPackage("numpy");
        await pyodide.loadPackage("matplotlib");
        let code = `
import numpy as np
import matplotlib.pyplot as plt

---

# Generate sample data
X = np.random.rand(100, 2)
y = np.array([1 if x[0] + x[1] > 1 else 0 for x in X])

---

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

---

# History of AI and ML

---

## Early Days (1950s-1960s)
- Alan Turing's "Turing Test"
- First neural networks
- Perceptron development

---

## AI Winter (1970s-1980s)
- Limited computing power
- High expectations vs. reality
- Funding cuts

---

## Renaissance (1990s-Present)
- Increased computing power
- Big data availability
- Deep learning revolution 

---

# ML Applications

---

## Current Applications
1. Computer Vision
   - Image recognition
   - Object detection
   - Medical imaging

---

2. Natural Language Processing
   - Machine translation
   - Sentiment analysis
   - Chatbots

---

3. Recommendation Systems
   - Content recommendations
   - Product suggestions
   - Personalized marketing

---

4. Healthcare
   - Disease diagnosis
   - Drug discovery
   - Patient care optimization 

---

## Benefits and Risks

---

### Benefits
- Automation of complex tasks
- Improved decision-making
- Personalization
- Efficiency gains

---

### Risks and Challenges
- Data privacy concerns
- Algorithmic bias
- Job displacement
- Ethical considerations

---

## Tools for ML Implementation

---

### Python Ecosystem
1. Core Libraries
   - NumPy: Numerical computing
   - Pandas: Data manipulation
   - Scikit-learn: ML algorithms
   - TensorFlow/PyTorch: Deep learning

---

2. Development Tools
   - Jupyter Notebooks
   - Google Colab
   - VS Code with Python extensions

---

### Practical Session
In this session's practical component, we will:
1. Set up our development environment
2. Explore basic Python libraries for ML
3. Create our first ML pipeline

---

## Resources

---

### Recommended Reading
- "Hands-On Machine Learning with Scikit-Learn and TensorFlow" by Aurélien Géron
- "Python for Data Analysis" by Wes McKinney
- Online courses and tutorials

---

### Additional Materials
- Course GitHub repository
- Discussion forum
- Office hours schedule

---

## Next Session Preview

---

In our next session, we will dive deeper into:
- Data preprocessing techniques
- Feature engineering
- Basic ML algorithms
- Model evaluation metrics

---

### Example: Linear Regression

---

You can run the following code in your browser using Pyodide:

---

<div>
    <h3>Interactive Example</h3>
    <button onclick="runLinearRegression()">Run Linear Regression Example</button>
    <pre id="output"></pre>
</div>

---

<script>
    async function runLinearRegression() {
        let pyodide = await loadPyodide();
        let code = `
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

---

# Generate sample data
X = np.random.rand(100, 1) * 10  # Features
y = 2.5 * X + np.random.randn(100, 1) * 2  # Target with noise

---

# Fit linear regression model
model = LinearRegression()
model.fit(X, y)

---

# Predict
X_new = np.array([[0], [10]])
y_predict = model.predict(X_new)

---

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
