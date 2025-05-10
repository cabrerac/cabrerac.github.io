<!-- SLIDES: -->

## Early AI Approaches (1943-1969) - Searching Algorithms

<div class="rows" style="height: 100%">
    <div class="row" style="height: 20%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 33%">
                <p><strong>Problem Definition</strong></p>
            </div>
            <div class="column vertical-middle text-center" style="width: 33%">
                <p><strong>Formal Definition</strong></p>
            </div>
            <div class="column vertical-middle text-center" style="width: 33%">
                <p><strong>Computational Representation</strong></p>
            </div>
        </div>
    </div>
    <div class="row" style="height: 80%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 33%">
                <p>
                    <b>An agent</b> must find a way to reach <b>a goal</b> in its <b>environment</b>. But, the next step is not obvious.
                </p>
                <img src="https://upload.wikimedia.org/wikipedia/commons/3/3b/Shortest_path_with_direct_weights.svg" alt="Shortest path problem" style="width: 90%; margin-top: 0.5em;">
                <div class="footnote">Shortest path problem: https://en.wikipedia.org/wiki/Shortest_path_problem</div>
            </div>
            <div class="column vertical-middle text-left" style="width: 33%">
                <p>
                    A <b>search problem</b> is defined by a <em>set of states, an initial state, a set of goal states, and a set of actions or transitions between states</em>.<br><br><br>

$$
P = (S, A, s_0, G)
$$
<br><br>
- $S$: set of states
- $A$: set of actions
- $s_0$: initial state
- $G$: set of goal states
                </p>
            </div>
            <div class="column vertical-middle text-left" style="width: 33%">
                <p>
                    A <b>search problem</b> is typically <em>modelled</em> using data structures such as:
                    • Graphs
                    • Adjacency matrix
                    • Node objects
                    • Queues/stacks
                </p>
                <img src="{{ site.url }}/assets/media/diagrams/adjacency-matrix.svg" alt="Adjacency matrix for shortest path graph" style="width: 90%; margin-top: 0.5em;">
                <div class="footnote">Adjacency matrix: https://en.wikipedia.org/wiki/Adjacency_matrix</div>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->

<!--
## Early Search Algorithms
<div class="columns">
<div class="column" style="width: 50%">
### 1950s: Search Methods
- Breadth-First Search (BFS)
- Depth-First Search (DFS)
- A* Algorithm (1968)
</div>
<div class="column" style="width: 50%">
<img src="{{ site.url }}/assets/media/diagrams/search-algorithms.svg" alt="Search Algorithms Diagram" style="width: 100%; height: auto;">
</div>
</div>

## Problem Solving
<div class="columns">
<div class="column" style="width: 50%">
### 1957: General Problem Solver
- Means-ends analysis
- State-space search
- Problem reduction
</div>
<div class="column" style="width: 50%">
<img src="{{ site.url }}/assets/media/diagrams/gps.svg" alt="GPS Diagram" style="width: 100%; height: auto;">
</div>
</div>

## Expert Systems
<div class="columns">
<div class="column" style="width: 50%">
### 1969: The DENDRAL System
- First expert system
- Chemical analysis
- Rule-based reasoning
</div>
<div class="column" style="width: 50%">
<img src="{{ site.url }}/assets/media/diagrams/dendral.svg" alt="DENDRAL Diagram" style="width: 100%; height: auto;">
</div>
</div>

# Early AI Approaches (1943-1969)

## The Artificial Neuron (1943)

The first mathematical model of a neuron was proposed by McCulloch and Pitts in 1943. This model laid the foundation for artificial neural networks.

```python
class McCullochPittsNeuron:
    def __init__(self, weights, threshold):
        self.weights = weights
        self.threshold = threshold
    
    def activate(self, inputs):
        # Sum weighted inputs
        weighted_sum = sum(w * x for w, x in zip(self.weights, inputs))
        # Apply threshold activation
        return 1 if weighted_sum >= self.threshold else 0

# Example usage
neuron = McCullochPittsNeuron(weights=[1, 1], threshold=1.5)
inputs = [1, 1]
output = neuron.activate(inputs)
print(f"Input: {inputs}, Output: {output}")
```

## Hebbian Learning (1949)

Donald Hebb proposed a learning rule that became fundamental to neural networks. The rule states that neurons that fire together, wire together.

```python
class HebbianLearning:
    def __init__(self, input_size):
        self.weights = [0] * input_size
    
    def update(self, inputs, output):
        # Hebbian learning rule: Δw = η * x * y
        learning_rate = 0.1
        for i in range(len(self.weights)):
            self.weights[i] += learning_rate * inputs[i] * output
    
    def predict(self, inputs):
        return 1 if sum(w * x for w, x in zip(self.weights, inputs)) > 0 else 0

# Example usage
hebb = HebbianLearning(input_size=2)
training_data = [([1, 1], 1), ([1, -1], -1), ([-1, 1], -1), ([-1, -1], 1)]
for inputs, target in training_data:
    hebb.update(inputs, target)
```

## The Perceptron (1957)

Frank Rosenblatt's Perceptron was the first artificial neural network that could learn from examples.

```python
class Perceptron:
    def __init__(self, input_size, learning_rate=0.1):
        self.weights = [0] * input_size
        self.learning_rate = learning_rate
    
    def predict(self, inputs):
        # Calculate weighted sum
        weighted_sum = sum(w * x for w, x in zip(self.weights, inputs))
        # Apply step activation
        return 1 if weighted_sum > 0 else 0
    
    def train(self, inputs, target):
        # Make prediction
        prediction = self.predict(inputs)
        # Calculate error
        error = target - prediction
        # Update weights
        for i in range(len(self.weights)):
            self.weights[i] += self.learning_rate * error * inputs[i]

# Example: Training a perceptron to learn AND gate
perceptron = Perceptron(input_size=2)
training_data = [
    ([1, 1], 1),
    ([1, 0], 0),
    ([0, 1], 0),
    ([0, 0], 0)
]

# Train for 10 epochs
for _ in range(10):
    for inputs, target in training_data:
        perceptron.train(inputs, target)
```

## Early Search Algorithms

Search algorithms were fundamental to early AI development. Here are implementations of key algorithms:

```python
from collections import deque
import heapq

class SearchAlgorithms:
    @staticmethod
    def bfs(graph, start, goal):
        queue = deque([(start, [start])])
        visited = set()
        
        while queue:
            (vertex, path) = queue.popleft()
            if vertex not in visited:
                if vertex == goal:
                    return path
                visited.add(vertex)
                for next_vertex in graph[vertex]:
                    if next_vertex not in visited:
                        queue.append((next_vertex, path + [next_vertex]))
        return None

    @staticmethod
    def dfs(graph, start, goal):
        stack = [(start, [start])]
        visited = set()
        
        while stack:
            (vertex, path) = stack.pop()
            if vertex not in visited:
                if vertex == goal:
                    return path
                visited.add(vertex)
                for next_vertex in graph[vertex]:
                    if next_vertex not in visited:
                        stack.append((next_vertex, path + [next_vertex]))
        return None

    @staticmethod
    def a_star(graph, start, goal, heuristic):
        frontier = []
        heapq.heappush(frontier, (0, start, [start]))
        visited = set()
        
        while frontier:
            _, vertex, path = heapq.heappop(frontier)
            if vertex not in visited:
                if vertex == goal:
                    return path
                visited.add(vertex)
                for next_vertex in graph[vertex]:
                    if next_vertex not in visited:
                        new_path = path + [next_vertex]
                        priority = len(new_path) + heuristic(next_vertex, goal)
                        heapq.heappush(frontier, (priority, next_vertex, new_path))
        return None

# Example usage
graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': ['G'],
    'E': ['G'],
    'F': ['G'],
    'G': []
}

def manhattan_distance(a, b):
    return abs(ord(a) - ord(b))

# Test BFS
bfs_path = SearchAlgorithms.bfs(graph, 'A', 'G')
print(f"BFS path: {bfs_path}")

# Test DFS
dfs_path = SearchAlgorithms.dfs(graph, 'A', 'G')
print(f"DFS path: {dfs_path}")

# Test A*
a_star_path = SearchAlgorithms.a_star(graph, 'A', 'G', manhattan_distance)
print(f"A* path: {a_star_path}")
```

## General Problem Solver (1957)

Newell and Simon's GPS was one of the first AI programs designed to solve general problems.

```python
class GeneralProblemSolver:
    def __init__(self):
        self.operators = []
        self.differences = {}
    
    def add_operator(self, name, preconditions, effects):
        self.operators.append({
            'name': name,
            'preconditions': preconditions,
            'effects': effects
        })
    
    def find_difference(self, current_state, goal_state):
        for key in goal_state:
            if current_state.get(key) != goal_state.get(key):
                return key
        return None
    
    def apply_operator(self, state, operator):
        # Check if preconditions are met
        for precondition in operator['preconditions']:
            if state.get(precondition) != operator['preconditions'][precondition]:
                return None
        
        # Apply effects
        new_state = state.copy()
        for effect in operator['effects']:
            new_state[effect] = operator['effects'][effect]
        return new_state
    
    def solve(self, initial_state, goal_state):
        current_state = initial_state.copy()
        plan = []
        
        while current_state != goal_state:
            difference = self.find_difference(current_state, goal_state)
            if not difference:
                break
                
            # Find applicable operator
            for operator in self.operators:
                if difference in operator['effects']:
                    new_state = self.apply_operator(current_state, operator)
                    if new_state:
                        current_state = new_state
                        plan.append(operator['name'])
                        break
        
        return plan

# Example: Tower of Hanoi problem
gps = GeneralProblemSolver()
gps.add_operator('move_disk', 
                 {'disk': 'small', 'from': 'A', 'to': 'B'},
                 {'disk': 'small', 'from': 'B', 'to': 'C'})

initial_state = {'disk': 'small', 'from': 'A', 'to': 'A'}
goal_state = {'disk': 'small', 'from': 'C', 'to': 'C'}
solution = gps.solve(initial_state, goal_state)
```

## The DENDRAL System (1969)

The DENDRAL system was an early expert system for chemical analysis.

```python
class DendralSystem:
    def __init__(self):
        self.rules = []
        self.mass_spectrum = {}
    
    def add_rule(self, pattern, conclusion):
        self.rules.append({
            'pattern': pattern,
            'conclusion': conclusion
        })
    
    def analyze_spectrum(self, spectrum):
        conclusions = []
        for rule in self.rules:
            if self._match_pattern(spectrum, rule['pattern']):
                conclusions.append(rule['conclusion'])
        return conclusions
    
    def _match_pattern(self, spectrum, pattern):
        # Simplified pattern matching
        for mass, intensity in pattern.items():
            if mass not in spectrum or abs(spectrum[mass] - intensity) > 0.1:
                return False
        return True

# Example usage
dendral = DendralSystem()
# Add rules for chemical fragment identification
dendral.add_rule(
    pattern={15: 1.0, 29: 0.8, 43: 0.6},
    conclusion="Methyl group present"
)
dendral.add_rule(
    pattern={17: 1.0, 31: 0.9},
    conclusion="Hydroxyl group present"
)

# Analyze a mass spectrum
spectrum = {15: 1.0, 29: 0.8, 43: 0.6, 17: 1.0, 31: 0.9}
conclusions = dendral.analyze_spectrum(spectrum)
```
## Key Concepts and Methods

1. **Neural Networks**
   - McCulloch-Pitts Neuron: Binary threshold unit
   - Hebbian Learning: Weight updates based on correlation
   - Perceptron: First learnable neural network

2. **Search Algorithms**
   - Breadth-First Search: Complete but memory-intensive
   - Depth-First Search: Memory-efficient but not complete
   - A* Algorithm: Optimal path finding with heuristics

3. **Symbolic AI**
   - General Problem Solver: Means-ends analysis
   - Rule-based systems: Expert systems like DENDRAL

4. **Learning Methods**
   - Supervised Learning: Perceptron training
   - Unsupervised Learning: Hebbian learning
   - Rule-based Learning: Expert system rules

5. **Problem-Solving Approaches**
   - State-space search
   - Pattern matching
   - Rule-based reasoning

These early approaches laid the foundation for modern AI and machine learning. They demonstrated both the potential and limitations of different AI paradigms, leading to the development of more sophisticated methods in later years.

-->
