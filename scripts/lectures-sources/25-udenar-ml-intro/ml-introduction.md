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

Python has become the de facto programming language for machine learning and data science due to its simplicity, readability, and rich ecosystem of libraries. In this notebook, we'll explore the fundamental Python concepts that form the building blocks of machine learning applications. We'll start with basic data structures, move through functions and control flow, and finally apply these concepts to implement basic AI algorithms.

## 1. Data Structures

Data structures are fundamental to organizing and manipulating data in Python. They help us store, access, and modify data efficiently. Let's explore the most commonly used data structures in machine learning.

### Lists and Arrays

Lists are one of Python's most versatile data structures. They can store elements of different types and are mutable, meaning we can modify them after creation.

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

Dictionaries are key-value pairs that allow us to store and retrieve data using unique keys. They're particularly useful for storing structured data and are commonly used in machine learning for feature storage and configuration.

```python
# Dictionaries (key-value pairs)
student = {
    'name': 'Alice',
    'age': 20,
    'courses': ['Math', 'CS', 'ML']
    }
```

```python
# Accessing dictionary elements
print("Name:", student['name'])
print("Courses:", student['courses'])
```

```python
# Dictionary comprehension
squares_dict = {x: x**2 for x in range(5)}
print("Squares dictionary:", squares_dict)
```

### NumPy Arrays

NumPy arrays are the foundation of numerical computing in Python. They provide efficient storage and operations for numerical data, which is crucial for machine learning algorithms.

```python
import numpy as np
```

```python
# Creating arrays
arr = np.array([1, 2, 3, 4, 5])
matrix = np.array([[1, 2, 3], [4, 5, 6]])
```

```python
# Array operations
print("Array shape:", arr.shape)
print("Matrix shape:", matrix.shape)
print("Sum:", arr.sum())
print("Mean:", arr.mean())
```

### Pandas DataFrames

Pandas DataFrames are two-dimensional, size-mutable, and potentially heterogeneous tabular data structures with labeled axes. They're essential for data manipulation and analysis in machine learning.

```python
import pandas as pd
```

```python
# Creating a dictionary
data = {
    'Name': ['Alice', 'Bob', 'Charlie', 'David'],
    'Age': [20, 22, 21, 23],
    'Score': [85, 92, 78, 88]
}
```

```python
# Creating a dataframe from a dictionary
df = pd.DataFrame(data)
```

```python
# Display the DataFrame
print("DataFrame:")
print(df)
```

```python
# Basic DataFrame operations
print("\nBasic statistics:")
print(df.describe())
```

```python
# Selecting data
print("\nFirst two rows:")
print(df.head(2))
```

```python
# Filtering data
print("\nStudents with score > 85:")
print(df[df['Score'] > 85])
```

```python
# Adding a new column
df['Grade'] = ['A', 'A', 'B', 'A']
print("\nDataFrame with grades:")
print(df)
```

```python
# Grouping and aggregation
print("\nAverage score by grade:")
print(df.groupby('Grade')['Score'].mean())
```

## 2. Functions and Control Flow

Functions are reusable blocks of code that perform specific tasks. In machine learning, we use functions to encapsulate algorithms, data preprocessing steps, and evaluation metrics.

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
```

```python
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
```

```python
# While loops
count = 0
while count < 5:
    print(f"Count: {count}")
    count += 1
```

```python
# If-else statements
def classify_number(n):
    if n > 0:
        return "Positive"
    elif n < 0:
        return "Negative"
    else:
        return "Zero"
```

```python
# Example usage
print(classify_number(5))
print(classify_number(-3))
print(classify_number(0))
```

## 3. Applying Concepts to AI Algorithms

Now that we understand the basic building blocks, let's apply these concepts to implement some fundamental AI algorithms.

### Implementing a Greedy Search Algorithm

Greedy search is an AI algorithm that makes locally optimal choices at each step with the hope of finding a global optimum. Let's implement a greedy algorithm to find the shortest path in a graph using a heuristic function.

```python
from collections import defaultdict
import heapq
```

```python
class Graph:
    def __init__(self):
        self.graph = defaultdict(list)
        self.heuristics = {}
    
    def add_edge(self, from_node, to_node, cost):
        self.graph[from_node].append((to_node, cost))
    
    def add_heuristic(self, node, value):
        self.heuristics[node] = value
```

```python
def greedy_search(graph, start, goal):
    """
    Implement greedy search algorithm using a heuristic function.
    
    Parameters:
    graph (Graph): Graph object containing edges and heuristics
    start: Starting node
    goal: Goal node
    
    Returns:
    list: Path from start to goal if found, None otherwise
    """
    # Priority queue to store nodes to explore
    # Format: (heuristic_value, node, path)
    frontier = [(graph.heuristics[start], start, [start])]
    visited = set()
    
    while frontier:
        # Get the node with the lowest heuristic value
        _, current, path = heapq.heappop(frontier)
        
        if current == goal:
            return path
        
        if current in visited:
            continue
            
        visited.add(current)
        
        # Explore neighbors
        for neighbor, _ in graph.graph[current]:
            if neighbor not in visited:
                new_path = path + [neighbor]
                # Use heuristic value for priority
                heapq.heappush(frontier, (graph.heuristics[neighbor], neighbor, new_path))
    
    return None  # No path found
```

```python
# Example usage: Finding the shortest path in a map
def create_city_graph():
    # Create a graph representing cities and distances
    graph = Graph()
    
    # Add edges (roads between cities)
    graph.add_edge('A', 'B', 4)
    graph.add_edge('A', 'C', 2)
    graph.add_edge('B', 'D', 3)
    graph.add_edge('C', 'D', 1)
    graph.add_edge('C', 'E', 5)
    graph.add_edge('D', 'F', 2)
    graph.add_edge('E', 'F', 3)
    
    # Add heuristic values (straight-line distance to goal)
    # These are example values - in a real application, these would be actual distances
    graph.add_heuristic('A', 6)
    graph.add_heuristic('B', 4)
    graph.add_heuristic('C', 4)
    graph.add_heuristic('D', 2)
    graph.add_heuristic('E', 3)
    graph.add_heuristic('F', 0)
    
    return graph
```

```python
# Test the greedy search
graph = create_city_graph()
start_city = 'A'
goal_city = 'F'
```

```python
path = greedy_search(graph, start_city, goal_city)
if path:
    print(f"Path found: {' -> '.join(path)}")
else:
    print("No path found")
```

This implementation demonstrates several important AI concepts:

1. **Heuristic Function**: The algorithm uses a heuristic function (represented by the `heuristics` dictionary) to estimate the distance to the goal. In a real application, this could be the straight-line distance to the destination (i.e., Euclidean distance).

2. **Priority Queue**: We use a priority queue (implemented with `heapq`) to always explore the most promising path first, based on the heuristic value.

3. **Graph Representation**: The graph is represented using an adjacency list, which is efficient for sparse graphs.

4. **Greedy Choice**: At each step, the algorithm makes the locally optimal choice by selecting the node with the lowest heuristic value.

The example creates a simple city navigation problem where we want to find a path from city A to city F. The heuristic values represent estimated distances to the goal city. The algorithm will find a path by always choosing the next city that appears closest to the goal according to the heuristic.

Note that while greedy search is fast and memory-efficient, it doesn't guarantee finding the optimal path. This is because it only considers the heuristic value at each step, not the actual cost of the path taken so far.

## 4. Homework Exercise

### Implementing A* Search Algorithm

In this assignment, you will implement the A* search algorithm, which is an extension of the greedy search we covered in class. A* combines the best of both worlds: it uses a heuristic function like greedy search but also considers the actual cost of the path taken so far.

#### Part 1: Understanding A*
1. Research and explain in your own words:
   - How A* differs from greedy search
   - The meaning of the f(n), g(n), and h(n) functions in A*
   - Why A* is guaranteed to find the optimal path when the heuristic is admissible

#### Part 2: Implementation
Implement the A* algorithm by modifying the greedy search code we developed in class. Your implementation should:

1. Create a new class `AStarGraph` that extends the `Graph` class:
   ```python
   class AStarGraph(Graph):
       def __init__(self):
           super().__init__()
           self.costs = {}  # Store actual costs between nodes
   ```

2. Implement the A* search function:
   ```python
   def astar_search(graph, start, goal):
       """
       Implement A* search algorithm.
       
       Parameters:
       graph (AStarGraph): Graph object containing edges, heuristics, and costs
       start: Starting node
       goal: Goal node
       
       Returns:
       tuple: (path, total_cost) if path found, (None, None) otherwise
       """
       # Your implementation here
   ```

3. Use the same city graph from the class example but add actual costs between cities.

#### Part 3: Testing and Analysis
1. Test your implementation with the following scenarios:
   - Path from A to F (as in class example)
   - Path from B to E
   - Path from C to F
   - A case where no path exists

2. Compare the results with the greedy search algorithm:
   - Create a table comparing path length and number of nodes explored
   - Explain any differences in the paths found
   - Analyze the trade-offs between computation time and path optimality

#### Submission Guidelines
- Submit your solution as a Jupyter notebook with the following name format: cease_ml_intro_session_1_<email_username>.ipynb
- Include clear comments explaining your code
- Provide a written analysis of your results
- Include test cases and their outputs
- Due date: [22/05/2025]

#### Resources
- [A* Pathfinding for Beginners](https://www.redblobgames.com/pathfinding/a-star/introduction.html)
- [A* Search Algorithm - Wikipedia](https://en.wikipedia.org/wiki/A*_search_algorithm)
- [Visualization of A* Algorithm](https://qiao.github.io/PathFinding.js/visual/)

<!-- end NOTEBOOK: -->