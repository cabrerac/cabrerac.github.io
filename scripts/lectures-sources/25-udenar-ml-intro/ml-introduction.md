---
course_code: 25-udenar-ml-intro
title: Artificial Intelligence and Machine Learning
description: This lecture presents the Artificial Intelligence and Machine Learning concepts. Their definition, history, implications, and applications.
session: 1
start_time: 8:00 am
end_time: 12:00 am
hours: 4
author: Christian Cabrera Jojoa
email: chc79@cam.ac.uk
position: Senior Research Associate and Affiliated Lecturer
department: Department of Computer Science and Technology
institution: University of Cambridge
layout: lecture
lecture_code: ml-introduction
lecture_date: 17/05/2025
permalink: /teaching/25-udenar-ml-intro/ml-introduction/
visible: true
---

<!-- ALL: content that goes everywhere -->
<!-- SLIDES: content that only goes to slides -->
<!-- RENDER: content that only goes to rendered markdown -->
<!-- NOTEBOOK: content that only goes to notebook -->
<!-- SLIDES+RENDER: content that goes to both rendered markdown and slides -->
<!-- SLIDES+NOTEBOOK: content that goes to both slides and notebook -->
<!-- RENDER+NOTEBOOK: content that goes to both rendered markdown and notebook -->

<!-- RENDER: -->
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
    <a href="/teaching/25-udenar-ml-intro/" style="color: var(--accent-color);">← Back to Course</a>
  </p>
</div>

<!-- end RENDER: -->

<!-- SLIDES: -->

# The ML Context

<!-- end SLIDES: -->

{% include _snippets/ai-concept.md %}

{% include _snippets/ai-foundations.md %}

{% include _snippets/ai-history.md %}

<!-- SLIDES: -->

# ML Today

<!-- end SLIDES: -->

{% include _snippets/ml-applications.md %}

{% include _snippets/ml-perception.md %}

<!-- SLIDES: -->

# ML Definition

<!-- end SLIDES: -->

{% include _snippets/ml-objective.md %}

<!--SLIDES: -->

## Conclusions

## Conclusions

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
            <h3>Overview</h3>
            <ul>
                <li>ML Context</li>
                <li>AI History</li>
                <li>AI Perception</li>
                <li>AI Winters</li>
                <li>ML Today</li>
                <li>ML Applications, Promises, and Risks</li>
                <li>ML Perception</li>
                <li>ML Definition</li>
            </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
            </div>
        </div>
    </div>
</div>

## Conclusions

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
            <h3>Overview</h3>
            <ul>
                <li>ML Context</li>
                <li>AI History</li>
                <li>AI Perception</li>
                <li>AI Winters</li>
                <li>ML Today</li>
                <li>ML Applications, Promises, and Risks</li>
                <li>ML Perception</li>
                <li>ML Definition</li>
            </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
            <h3>Next Time</h3>
            <ul>
                <li>ML Adoption Process</li>
                <li>ML with Purpose</li>
                <li>ML and Socio-technical Systems</li>
                <li>Data-First</li>
                <li>Data Access</li>
            </ul>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->

<!-- RENDER: -->

### Resources

#### Books
- Russell, S. and Norvig, P. (2010). Artificial Intelligence: A Modern Approach 3rd ed. Prentice Hall
- [Deisenroth M. P. et. al. (2020). Mathematics for Machine Learning](https://mml-book.github.io/)


#### Papers and Reports
- [Turing A. M. (1950). Computing Machinery and Intelligence](https://courses.cs.umbc.edu/471/papers/turing.pdf)
- [Lighthill J. (1972). Artificial Intelligence: A General Survey](https://www.chilton-computing.org.uk/inf/literature/reports/lighthill_report/p001.htm)
- [Feigenbaum E. A. (1980). Expert Systems in the 1980s](https://stacks.stanford.edu/file/druid:vf069sz9374/vf069sz9374.pdf)
- [Vol. 117, No. 1, Winter, 1988, Artificial Intelligence](https://www.jstor.org/stable/i20025133)
- [Hart P. (2021). An Artificial Intelligence Odyssey: From the Research Lab to the Real World](https://ieeexplore.ieee.org/abstract/document/9423541)
- [Shumailov I. et. al. (2024). AI models collapse when trained on recursively generated data](https://www.nature.com/articles/s41586-024-07566-y)


#### Talks
- [Geoffrey Hinton Lecture at Cambridge (2023)](https://www.youtube.com/watch?v=rGgGOccMEiY)
- [Demmis Hassabis Lecture at Cambridge (2025)](https://www.youtube.com/watch?v=hHooQmmzG4k)

<!-- end RENDER: -->

<!-- NOTEBOOK: -->

# Python Basics for Machine Learning

This notebook introduces fundamental Python concepts that are essential for machine learning projects. We'll cover data structures, functions, control flow, and then apply these concepts to implement basic search algorithms and expert systems.

## 1. Data Structures

### Lists and Arrays

```python
# Lists in Python
numbers = [1, 2, 3, 4, 5]
names = ['Alice', 'Bob', 'Charlie']
```

```python
# List operations
print("First element:", numbers[0])
print("Last element:", numbers[-1])
print("Slice:", numbers[1:3])
```

```python
# List comprehension (very useful in ML)
squares = [x**2 for x in numbers]
print("Squares:", squares)
```

### Dictionaries

```python
# Dictionaries (key-value pairs)
student = {
    'name': 'Alice',
    'age': 20,
    'courses': ['Math', 'CS', 'ML']
}

# Accessing dictionary elements
print("Name:", student['name'])
print("Courses:", student['courses'])

# Dictionary comprehension
squares_dict = {x: x**2 for x in range(5)}
print("Squares dictionary:", squares_dict)
```

### NumPy Arrays

```python
import numpy as np

# Creating arrays
arr = np.array([1, 2, 3, 4, 5])
matrix = np.array([[1, 2, 3], [4, 5, 6]])

# Array operations
print("Array shape:", arr.shape)
print("Matrix shape:", matrix.shape)
print("Sum:", arr.sum())
print("Mean:", arr.mean())
```

## 2. Functions and Control Flow

### Functions

```python
def calculate_statistics(data):
    """
    Calculate basic statistics for a dataset.
    
    Parameters:
    data (list): List of numbers
    
    Returns:
    tuple: (mean, variance)
    """
    mean = sum(data) / len(data)
    variance = sum((x - mean) ** 2 for x in data) / len(data)
    return mean, variance

# Example usage
data = [1, 2, 3, 4, 5]
mean, var = calculate_statistics(data)
print(f"Mean: {mean}, Variance: {var}")
```

### Loops and Control Statements

```python
# For loops
for i in range(5):
    print(f"Number: {i}")

# While loops
count = 0
while count < 5:
    print(f"Count: {count}")
    count += 1

# If-else statements
def classify_number(n):
    if n > 0:
        return "Positive"
    elif n < 0:
        return "Negative"
    else:
        return "Zero"

# Example usage
print(classify_number(5))
print(classify_number(-3))
print(classify_number(0))
```

## 3. Applying Concepts to ML Algorithms

### Implementing a Simple Search Algorithm

```python
def linear_search(arr, target):
    """
    Implement linear search algorithm.
    
    Parameters:
    arr (list): List to search in
    target: Element to find
    
    Returns:
    int: Index of target if found, -1 otherwise
    """
    for i, element in enumerate(arr):
        if element == target:
            return i
    return -1

# Example usage
numbers = [4, 2, 7, 1, 9, 3]
target = 7
result = linear_search(numbers, target)
print(f"Target {target} found at index: {result}")
```

### Implementing a Simple Expert System

```python
class SimpleExpertSystem:
    def __init__(self):
        self.knowledge_base = {
            'fever': ['flu', 'cold', 'covid'],
            'cough': ['flu', 'cold', 'covid'],
            'fatigue': ['flu', 'covid'],
            'sore_throat': ['cold', 'flu']
        }
    
    def diagnose(self, symptoms):
        """
        Diagnose based on symptoms.
        
        Parameters:
        symptoms (list): List of symptoms
        
        Returns:
        dict: Possible conditions and their likelihood
        """
        conditions = {}
        for symptom in symptoms:
            if symptom in self.knowledge_base:
                for condition in self.knowledge_base[symptom]:
                    conditions[condition] = conditions.get(condition, 0) + 1
        
        # Calculate likelihood
        total_symptoms = len(symptoms)
        return {k: v/total_symptoms for k, v in conditions.items()}

# Example usage
expert = SimpleExpertSystem()
symptoms = ['fever', 'cough', 'fatigue']
diagnosis = expert.diagnose(symptoms)
print("Diagnosis:", diagnosis)
```

## 4. Homework Exercise

### Part 1: Python Basics
1. Create a function that takes a list of numbers and returns:
   - The mean
   - The median
   - The mode
   - A dictionary with the frequency of each number

2. Implement a function that checks if a string is a palindrome using:
   - A for loop
   - A while loop
   - List comprehension

### Part 2: ML Concepts
1. Implement a simple binary classifier that:
   - Takes a list of features
   - Uses a threshold to classify items
   - Returns the accuracy of the classification

2. Create a simple recommendation system that:
   - Takes a user's preferences (as a dictionary)
   - Takes a list of items with their features
   - Returns the top 3 most similar items

### Submission Guidelines
- Submit your solutions as a Jupyter notebook
- Include comments explaining your code
- Test your code with different inputs
- Due date: [Add due date]

<!-- end NOTEBOOK: -->