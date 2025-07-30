<!-- NOTEBOOK: -->

# Python Basics for Machine Learning

Python has become the de facto programming language for machine learning and data science due to its simplicity, readability, and rich ecosystem of libraries. In this notebook, we'll explore the fundamental Python concepts that form the building blocks of machine learning applications. We'll start with basic data structures, move through functions and control flow, and finally apply these concepts to implement basic AI algorithms.

## 1. Data Structures

Data structures are fundamental to organising and manipulating data in Python. They help us store, access, and modify data efficiently. Let's explore the most commonly used data structures in machine learning.

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
print("Slice:", numbers[1:4])
```

List comprehensions are a concise and efficient way to create lists in Python. They are particularly useful in machine learning for data transformation and feature engineering. Let's explore different types of list comprehensions:

```python
# Basic list comprehension
numbers = [1, 2, 3, 4, 5]
squares = [x**2 for x in numbers]
print("Basic comprehension:", squares)
```

```python
# List comprehension with condition
even_squares = [x**2 for x in numbers if x % 2 == 0]
print("Even squares only:", even_squares)
```

```python
# Nested list comprehension (useful for matrix operations)
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flattened = [num for row in matrix for num in row]
print("Flattened matrix:", flattened)
```

```python
# List comprehension with multiple conditions
filtered_numbers = [x for x in numbers if x > 2 and x < 5]
print("Filtered numbers:", filtered_numbers)
```

```python
# List comprehension with if-else
categorized = ["Even" if x % 2 == 0 else "Odd" for x in numbers]
print("Number categories:", categorized)
```

List comprehensions are especially valuable in machine learning for:
1. Data preprocessing: Transforming raw data into features
2. Feature engineering: Creating new features from existing ones
3. Data filtering: Selecting subsets of data based on conditions
4. Matrix operations: Manipulating multi-dimensional data

For example, in a machine learning context, you might use list comprehensions to:
- Normalize features: `normalized = [(x - min(data)) / (max(data) - min(data)) for x in data]`
- Create polynomial features: `polynomial = [x**2 for x in features]`
- Filter outliers: `clean_data = [x for x in data if x < threshold]`

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

## 3. Error Handling and Debugging

Error handling is crucial in machine learning applications where data can be unpredictable and operations can fail. Let's explore how to handle errors gracefully.

### Try-Except Blocks

```python
def safe_division(a, b):
    """
    Safely divide two numbers with error handling.
    """
    try:
        result = a / b
        return result
    except ZeroDivisionError:
        print("Error: Cannot divide by zero!")
        return None
    except TypeError:
        print("Error: Both arguments must be numbers!")
        return None
```

```python
# Test the function
print(safe_division(10, 2))  # Should work
print(safe_division(10, 0))  # Should handle error
print(safe_division("10", 2))  # Should handle type error
```

### Working with Data Files

```python
def load_data_safely(filename):
    """
    Safely load data from a file with error handling.
    """
    try:
        with open(filename, 'r') as file:
            data = file.read()
        return data
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found!")
        return None
    except PermissionError:
        print(f"Error: No permission to read '{filename}'!")
        return None
```

```python
# Create a sample file for testing
with open('sample_data.txt', 'w') as f:
    f.write("1,2,3,4,5\n")
    f.write("Alice,Bob,Charlie\n")
# Test loading
data = load_data_safely('sample_data.txt')
print("Loaded data:", data)
```

## 4. File I/O and Data Processing

File input/output operations are essential for loading and saving data in machine learning workflows.

### Reading and Writing CSV Files

```python
import csv
# Writing data to CSV
data_to_write = [
    ['Name', 'Age', 'Score'],
    ['Alice', 20, 85],
    ['Bob', 22, 92],
    ['Charlie', 21, 78]
]
with open('students.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data_to_write)
# Reading data from CSV
def read_csv_data(filename):
    data = []
    try:
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                data.append(row)
        return data
    except FileNotFoundError:
        print(f"File {filename} not found!")
        return []
# Test reading
students = read_csv_data('students.csv')
print("CSV data:", students)
```

### JSON Data Handling

```python
import json
# Creating JSON data
ml_config = {
    "model_type": "random_forest",
    "parameters": {
        "n_estimators": 100,
        "max_depth": 10
    },
    "features": ["feature1", "feature2", "feature3"],
    "target": "target_variable"
}
# Writing JSON to file
with open('ml_config.json', 'w') as f:
    json.dump(ml_config, f, indent=2)
# Reading JSON from file
def load_ml_config(filename):
    try:
        with open(filename, 'r') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        print(f"Config file {filename} not found!")
        return {}
    except json.JSONDecodeError:
        print(f"Invalid JSON in {filename}!")
        return {}
# Test loading
config = load_ml_config('ml_config.json')
print("ML Config:", config)
```

## 5. Object-Oriented Programming Basics

Understanding classes and objects is important for organising machine learning code and creating reusable components.

### Creating Simple Classes

```python
class DataProcessor:
    """
    A simple class for data processing operations.
    """
    
    def __init__(self, data):
        self.data = data
        self.processed = False
    
    def normalize(self):
        """Normalize the data to 0-1 range."""
        if not self.data:
            return None
        
        min_val = min(self.data)
        max_val = max(self.data)
        
        if max_val == min_val:
            return [0.5] * len(self.data)
        
        normalized = [(x - min_val) / (max_val - min_val) for x in self.data]
        self.processed = True
        return normalized
    
    def get_statistics(self):
        """Get basic statistics of the data."""
        if not self.data:
            return {}
        
        return {
            'count': len(self.data),
            'mean': sum(self.data) / len(self.data),
            'min': min(self.data),
            'max': max(self.data)
        }
    
    def add_outlier_detection(self, threshold=2):
        """Detect outliers using simple statistical method."""
        if not self.data:
            return []
        
        mean = sum(self.data) / len(self.data)
        std = (sum((x - mean) ** 2 for x in self.data) / len(self.data)) ** 0.5
        
        outliers = [x for x in self.data if abs(x - mean) > threshold * std]
        return outliers
```

```python
# Test the DataProcessor class
data = [1, 2, 3, 4, 5, 100]  # 100 is an outlier
processor = DataProcessor(data)
print("Original data:", processor.data)
print("Normalized data:", processor.normalize())
print("Statistics:", processor.get_statistics())
print("Outliers:", processor.add_outlier_detection())
```

### Creating a Simple ML Model Class

```python
class SimpleLinearModel:
    """
    A simple linear regression model implementation.
    """
    
    def __init__(self):
        self.slope = 0
        self.intercept = 0
        self.trained = False
    
    def fit(self, X, y):
        """
        Fit the model using simple linear regression.
        X: list of input values
        y: list of target values
        """
        if len(X) != len(y):
            raise ValueError("X and y must have the same length")
        
        n = len(X)
        sum_x = sum(X)
        sum_y = sum(y)
        sum_xy = sum(x * y for x, y in zip(X, y))
        sum_x2 = sum(x**2 for x in X)
        
        # Calculate slope and intercept
        self.slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x**2)
        self.intercept = (sum_y - self.slope * sum_x) / n
        
        self.trained = True
    
    def predict(self, X):
        """Make predictions using the fitted model."""
        if not self.trained:
            raise ValueError("Model must be trained before making predictions")
        
        return [self.slope * x + self.intercept for x in X]
    
    def get_parameters(self):
        """Get model parameters."""
        return {
            'slope': self.slope,
            'intercept': self.intercept,
            'trained': self.trained
        }
```

```python
# Test the SimpleLinearModel
# Create some sample data
X = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]  # Perfect linear relationship
# Create and train the model
model = SimpleLinearModel()
model.fit(X, y)
print("Model parameters:", model.get_parameters())
# Make predictions
predictions = model.predict([6, 7, 8])
print("Predictions for [6, 7, 8]:", predictions)
```

<!-- end NOTEBOOK: -->