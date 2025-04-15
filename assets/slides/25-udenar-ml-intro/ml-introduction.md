---
marp: true
theme: beam
paginate: false
header: "Session 1 - Introduction to Machine Learning"
footer: ""
style: |
  :root {
    --primary-color: #0A192F;    /* Deep navy blue */
    --secondary-color: #112240;  /* Slightly lighter navy */
    --accent-color: #0A192F;     /* Deep navy blue for progress bar */
    --text-color: #0A192F;       /* Deep navy blue for text */
    --background-color: #FFFFFF; /* White background */
    --progress-color: #0A192F;   /* Deep navy blue for progress bar */
  }
  
  section {
    background-color: var(--background-color);
    color: var(--text-color);
    padding: 40px;
    font-size: 28px;
    font-family: 'Helvetica Neue', Arial, sans-serif;
  }
  
  h1 {
    font-size: 48px;
    color: var(--text-color);
    margin-bottom: 20px;
    padding-bottom: 10px;
  }
  
  h2 {
    font-size: 40px;
    color: var(--text-color);
    margin-bottom: 15px;
  }
  
  h3 {
    font-size: 32px;
    color: var(--text-color);
    margin-bottom: 10px;
  }
  
  ul, ol {
    margin-left: 30px;
    margin-top: 15px;
  }
  
  li {
    margin-bottom: 10px;
  }
  
  img {
    max-width: 80%;
    margin: 20px auto;
    display: block;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  }
  
  code {
    font-size: 24px;
    background-color: rgba(10, 25, 47, 0.1);
    color: var(--text-color);
    padding: 4px 8px;
    border-radius: 4px;
    font-family: 'Fira Code', monospace;
  }
  
  pre {
    background-color: rgba(10, 25, 47, 0.1);
    padding: 15px;
    border-radius: 8px;
    overflow-x: auto;
  }
  
  /* Progress bar styling */
  section::after {
    content: '';
    position: fixed;
    bottom: 0;
    left: 0;
    width: calc(var(--progress) * 100%);
    height: 2px;
    background: var(--progress-color);
    transition: width 0.3s ease;
    z-index: 1;
  }
  
  /* Header styling */
  header {
    color: var(--text-color);
    font-size: 20px;
    padding: 10px;
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid var(--accent-color);
  }

---

# Introduction to Machine Learning
## This lecture presents the course and a brief context and history of the Machine Learning (ML) field.

## Course Overview

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

Machine Learning is a field of study that gives computers the ability to learn without being explicitly programmed. It's a subset of Artificial Intelligence that focuses on building systems that can learn from and make decisions based on data.

![ML Overview](/assets/media/images/ml-overview.png)


---

## Interactive Example
Here's a simple example of how ML works:

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

---

### Computer Vision
   - Image recognition
   - Object detection
   - Medical imaging


---

### Natural Language Processing
   - Machine translation
   - Sentiment analysis
   - Chatbots


---

### Recommendation Systems
   - Content recommendations
   - Product suggestions
   - Personalized marketing


---

### Healthcare
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

## Next Session Preview

In our next session, we will dive deeper into:
- Data preprocessing techniques
- Feature engineering
- Basic ML algorithms
- Model evaluation metrics
