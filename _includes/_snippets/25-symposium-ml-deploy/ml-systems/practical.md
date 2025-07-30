<!-- NOTEBOOK: -->

# Python Basics for Machine Learning

Python has become the de facto programming language for machine learning and data science due to its simplicity, readability, and rich ecosystem of libraries. This comprehensive notebook provides a complete introduction to Python programming specifically tailored for machine learning applications.

We'll start with fundamental data structures (lists, dictionaries, NumPy arrays, and Pandas DataFrames), progress through functions, control flow, and error handling, then explore file I/O operations and object-oriented programming. Finally, we'll implement a complete machine learning model from scratch and visualise the results.

This notebook is designed to be self-contained and educational, with detailed explanations of each concept and its relevance to machine learning workflows.

## How to Use This Notebook

This notebook is designed to be self-contained and educational. Each code block builds upon the previous ones, so it's important to run them in order. The explanations will help you understand:

- **What** each piece of code does
- **Why** we use certain approaches in machine learning
- **How** to apply these concepts to real ML problems

Feel free to experiment with the code examples and modify them to better understand the concepts!

## 1. Data Structures

Data structures are fundamental to organising and manipulating data in Python. They help us store, access, and modify data efficiently. Let's explore the most commonly used data structures in machine learning.

### Lists and Arrays

Lists are one of Python's most versatile data structures. They can store elements of different types and are mutable, meaning we can modify them after creation.

**Why are lists important in ML?** In machine learning, we often work with datasets that contain multiple features (like age, height, weight for predicting health outcomes). Lists help us organise this data and perform operations on entire datasets at once.

```python
# Lists in Python
# We create lists using square brackets []
numbers = [1, 2, 3, 4, 5]  # A list of numbers
names = ['Alice', 'Bob', 'Charlie']  # A list of strings
# In ML context: This could be a list of feature values or target values
# For example: ages = [25, 30, 35, 40] for a dataset of people
```

```python
# List operations - accessing elements
# Indexing starts at 0, so the first element is at index 0
print("First element:", numbers[0])  # Gets the first number (1)
print("Last element:", numbers[-1])  # Gets the last number (5)
print("Slice:", numbers[1:4])  # Gets elements from index 1 to 3 (exclusive of 4)
# In ML context: We often need to access specific features or subsets of our data
# For example: first_three_ages = ages[0:3] to get the first three age values
```

List comprehensions are a concise and efficient way to create lists in Python. They are particularly useful in machine learning for data transformation and feature engineering. Let's explore different types of list comprehensions:

**What are list comprehensions?** They're a Pythonic way to create lists by applying an operation to each element in an existing list. Think of them as a compact for-loop that creates a new list.

**Why use them in ML?** In machine learning, we often need to transform our data (like normalising features, creating new features, or filtering data). List comprehensions make these operations clean and readable.

```python
# Basic list comprehension
# Syntax: [expression for item in list]
numbers = [1, 2, 3, 4, 5]
squares = [x**2 for x in numbers]  # Square each number
print("Basic comprehension:", squares)
# This is equivalent to:
# squares = []
# for x in numbers:
#     squares.append(x**2)
```

```python
# List comprehension with condition
# Syntax: [expression for item in list if condition]
even_squares = [x**2 for x in numbers if x % 2 == 0]  # Only square even numbers
print("Even squares only:", even_squares)
# In ML context: This could be filtering outliers or selecting specific features
# For example: normal_ages = [age for age in ages if 18 <= age <= 65]
```

```python
# Nested list comprehension (useful for matrix operations)
# This flattens a 2D matrix into a 1D list
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flattened = [num for row in matrix for num in row]
print("Flattened matrix:", flattened)
# In ML context: This is useful when working with image data or multi-dimensional features
# For example: flattening a 28x28 pixel image into a 784-element feature vector
```

```python
# List comprehension with multiple conditions
# You can combine multiple conditions with 'and' or 'or'
filtered_numbers = [x for x in numbers if x > 2 and x < 5]
print("Filtered numbers:", filtered_numbers)
# In ML context: This could be filtering data based on multiple criteria
# For example: valid_samples = [sample for sample in data if sample['age'] > 18 and sample['score'] > 0.5]
```

```python
# List comprehension with if-else
# Syntax: [expression_if_true if condition else expression_if_false for item in list]
categorized = ["Even" if x % 2 == 0 else "Odd" for x in numbers]
print("Number categories:", categorized)
# In ML context: This could be creating categorical features or labels
# For example: age_groups = ["Young" if age < 30 else "Middle" if age < 60 else "Senior" for age in ages]
```

List comprehensions are especially valuable in machine learning for:
1. **Data preprocessing**: Transforming raw data into features
2. **Feature engineering**: Creating new features from existing ones
3. **Data filtering**: Selecting subsets of data based on conditions
4. **Matrix operations**: Manipulating multi-dimensional data

For example, in a machine learning context, you might use list comprehensions to:
- **Normalize features**: `normalized = [(x - min(data)) / (max(data) - min(data)) for x in data]`
- **Create polynomial features**: `polynomial = [x**2 for x in features]`
- **Filter outliers**: `clean_data = [x for x in data if x < threshold]`

**Try it yourself!** Experiment with the examples above by changing the numbers list or adding your own conditions. This will help you understand how list comprehensions work in practice.

### Dictionaries

Dictionaries are key-value pairs that allow us to store and retrieve data using unique keys. They're particularly useful for storing structured data and are commonly used in machine learning for feature storage and configuration.

**What are dictionaries?** Think of them as a collection of labeled boxes. Each box (key) contains a value, and you can access the value by knowing the label.

**Why are they important in ML?** In machine learning, we often work with structured data where each sample has multiple features with specific names (like 'age', 'height', 'weight'). Dictionaries help us organise this data clearly and access specific features easily.

```python
# Dictionaries (key-value pairs)
# We create dictionaries using curly braces {} with key: value pairs
student = {
    'name': 'Alice',      # Key: 'name', Value: 'Alice'
    'age': 20,           # Key: 'age', Value: 20
    'courses': ['Math', 'CS', 'ML']  # Key: 'courses', Value: a list
}
# In ML context: This could represent a single data point with multiple features
# For example: patient = {'age': 45, 'blood_pressure': 120, 'cholesterol': 200}
```

```python
# Accessing dictionary elements
# We use square brackets with the key name to access values
print("Name:", student['name'])      # Gets the value associated with 'name'
print("Courses:", student['courses']) # Gets the list of courses
# In ML context: We often need to access specific features of our data
# For example: age = patient['age'] to get a patient's age
```

```python
# Dictionary comprehension
# Similar to list comprehensions, but creates key-value pairs
squares_dict = {x: x**2 for x in range(5)}  # Creates {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}
print("Squares dictionary:", squares_dict)
# In ML context: This could be creating feature mappings or configurations
# For example: feature_scales = {feature: max_value for feature, max_value in zip(features, max_values)}
```

### NumPy Arrays

NumPy arrays are the foundation of numerical computing in Python. They provide efficient storage and operations for numerical data, which is crucial for machine learning algorithms.

**What are NumPy arrays?** They're like super-powered lists that are optimised for numerical operations. They're faster and more memory-efficient than regular Python lists for mathematical operations.

**Why are they essential in ML?** Machine learning involves lots of mathematical operations (matrix multiplications, statistical calculations, etc.). NumPy arrays make these operations fast and efficient, which is crucial when working with large datasets.

```python
import numpy as np
# We import NumPy with the alias 'np' - this is the standard convention
# NumPy provides the foundation for most scientific computing in Python
```

```python
# Creating arrays
# We convert regular Python lists to NumPy arrays
arr = np.array([1, 2, 3, 4, 5])  # 1D array (vector)
matrix = np.array([[1, 2, 3], [4, 5, 6]])  # 2D array (matrix)
# In ML context: 
# - arr could represent a single feature across all samples
# - matrix could represent multiple features for multiple samples
```

```python
# Array operations
# NumPy provides many useful methods for array analysis
print("Array shape:", arr.shape)      # Shows dimensions: (5,) for 1D array
print("Matrix shape:", matrix.shape)  # Shows dimensions: (2, 3) for 2D array
print("Sum:", arr.sum())              # Sum of all elements
print("Mean:", arr.mean())            # Average of all elements
# In ML context: These operations are fundamental for data analysis
# For example: calculating the mean of a feature across all samples
```

### Pandas DataFrames

Pandas DataFrames are two-dimensional, size-mutable, and potentially heterogeneous tabular data structures with labeled axes. They're essential for data manipulation and analysis in machine learning.

**What are DataFrames?** Think of them as Excel spreadsheets in Python - they have rows and columns with labels, and can contain different types of data in different columns.

**Why are they crucial in ML?** Most real-world datasets come in tabular format (CSV files, Excel files, etc.). DataFrames make it easy to load, clean, and analyse this data. They're the bridge between raw data and machine learning algorithms.

```python
import pandas as pd
# We import pandas with the alias 'pd' - this is the standard convention
# Pandas is built on top of NumPy and provides high-level data manipulation tools
```

```python
# Creating a dictionary
# We'll use a dictionary to create our DataFrame
# Each key becomes a column name, each value becomes the column data
data = {
    'Name': ['Alice', 'Bob', 'Charlie', 'David'],  # Column of names
    'Age': [20, 22, 21, 23],                       # Column of ages
    'Score': [85, 92, 78, 88]                      # Column of scores
}
# In ML context: This could be a dataset with features (Age, Score) and identifiers (Name)
```

```python
# Creating a dataframe from a dictionary
df = pd.DataFrame(data)
# This converts our dictionary into a structured DataFrame
# Each row represents a student, each column represents a feature
```

```python
# Display the DataFrame
print("DataFrame:")
print(df)
# Notice how the data is displayed in a neat table format
# The index (row numbers) is automatically created
```

```python
# Basic DataFrame operations
print("\nBasic statistics:")
print(df.describe())
# describe() gives us summary statistics for numerical columns
# This is very useful for understanding our data distribution
```

```python
# Selecting data
print("\nFirst two rows:")
print(df.head(2))
# head(n) shows the first n rows of the DataFrame
# This is useful for quickly inspecting large datasets
```

```python
# Filtering data
print("\nStudents with score > 85:")
print(df[df['Score'] > 85])
# We can filter rows based on conditions
# This is essential for data cleaning and subset selection in ML
```

```python
# Adding a new column
df['Grade'] = ['A', 'A', 'B', 'A']
print("\nDataFrame with grades:")
print(df)
# We can easily add new features to our dataset
# This is common in feature engineering for ML
```

```python
# Grouping and aggregation
print("\nAverage score by grade:")
print(df.groupby('Grade')['Score'].mean())
# groupby() allows us to group data and calculate statistics
# This is useful for understanding relationships between features
```

## 2. Functions and Control Flow

Functions are reusable blocks of code that perform specific tasks. In machine learning, we use functions to encapsulate algorithms, data preprocessing steps, and evaluation metrics.

**What are functions?** Functions are like recipes - they take ingredients (inputs), follow steps (the code inside), and produce a result (output). They help us organise code and avoid repeating the same operations.

**Why are they essential in ML?** In machine learning, we often need to perform the same operations on different datasets (like normalising data, calculating metrics, or training models). Functions let us write the code once and reuse it many times.

```python
def calculate_statistics(data):
    """
    Calculate basic statistics for a dataset.
    
    Parameters:
    data (list): List of numbers
    
    Returns:
    tuple: (mean, variance)
    """
    # Calculate the mean (average)
    mean = sum(data) / len(data)
    
    # Calculate the variance (how spread out the data is)
    variance = sum((x - mean) ** 2 for x in data) / len(data)
    
    # Return both values as a tuple
    return mean, variance
# In ML context: This function could be used to understand the distribution of features
# For example: calculating the mean and variance of house prices in a dataset
```

```python
# Example usage
data = [1, 2, 3, 4, 5]
mean, var = calculate_statistics(data)
print(f"Mean: {mean}, Variance: {var}")
# The function returns two values, which we can assign to two variables
# This is called "unpacking" a tuple
```

### Loops and Control Statements

Loops and control statements help us make decisions and repeat operations in our code. They're fundamental to programming and very useful in machine learning.

**What are loops?** Loops let us repeat the same operation multiple times without writing the same code over and over.

**What are control statements?** They let our code make decisions based on conditions (like "if this is true, do that").

```python
# For loops
# For loops iterate over a sequence (like a list or range)
for i in range(5):  # range(5) creates [0, 1, 2, 3, 4]
    print(f"Number: {i}")
# In ML context: This could be iterating through data samples or features
# For example: for sample in dataset: process_sample(sample)
```

```python
# While loops
# While loops continue as long as a condition is True
count = 0
while count < 5:  # Keep going while count is less than 5
    print(f"Count: {count}")
    count += 1  # Increase count by 1 each time
# In ML context: This could be training a model until convergence
# For example: while error > threshold: train_one_more_step()
```

```python
# If-else statements
# These let us make decisions based on conditions
def classify_number(n):
    if n > 0:           # If n is greater than 0
        return "Positive"
    elif n < 0:         # Else if n is less than 0
        return "Negative"
    else:               # Otherwise (n equals 0)
        return "Zero"
# In ML context: This could be a simple classification model
# For example: classifying emails as spam/not spam based on certain criteria
```

```python
# Example usage
print(classify_number(5))   # Should print "Positive"
print(classify_number(-3))  # Should print "Negative"
print(classify_number(0))   # Should print "Zero"
# This demonstrates how our function makes different decisions based on input
```

## 3. Error Handling and Debugging

Error handling is crucial in machine learning applications where data can be unpredictable and operations can fail. Let's explore how to handle errors gracefully.

**What is error handling?** It's a way to prepare for things that might go wrong in our code and handle them gracefully instead of crashing the program.

**Why is it important in ML?** Real-world data is messy! Files might be missing, data might be in the wrong format, or calculations might fail. Good error handling makes our ML systems robust and reliable.

### Try-Except Blocks

```python
def safe_division(a, b):
    """
    Safely divide two numbers with error handling.
    """
    try:
        # Try to do the division
        result = a / b
        return result
    except ZeroDivisionError:
        # If we try to divide by zero, catch this specific error
        print("Error: Cannot divide by zero!")
        return None
    except TypeError:
        # If we try to divide non-numbers, catch this error
        print("Error: Both arguments must be numbers!")
        return None
# In ML context: This could be handling missing data or invalid calculations
# For example: safely calculating averages when some data might be missing
```

```python
# Test the function
print(safe_division(10, 2))   # Should work normally
print(safe_division(10, 0))   # Should handle division by zero gracefully
print(safe_division("10", 2)) # Should handle type error gracefully
# Notice how the function doesn't crash - it handles errors and continues
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

**What is File I/O?** It stands for "Input/Output" - reading data from files and writing data to files. This is how we get data into our programs and save results.

**Why is it crucial in ML?** Machine learning datasets are usually stored in files (CSV, JSON, etc.). We need to read these files to get our data, and often save our models or results back to files.

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

**What is Object-Oriented Programming (OOP)?** It's a way of organising code by grouping related data and functions together into "objects" or "classes". Think of it like organising a kitchen - you have different tools (methods) and ingredients (data) grouped by their purpose.

**Why is it useful in ML?** Machine learning involves complex objects like models, datasets, and preprocessing pipelines. OOP helps us organise these components clearly and reuse them across different projects.

### Creating Simple Classes

```python
class DataProcessor:
    """
    A simple class for data processing operations.
    """
    
    def __init__(self, data):
        # This is the constructor - it runs when we create a new DataProcessor
        self.data = data        # Store the data as an attribute of the object
        self.processed = False  # Track whether we've processed the data
    
    def normalize(self):
        """Normalize the data to 0-1 range."""
        if not self.data:
            return None
        
        # Find the minimum and maximum values in the data
        min_val = min(self.data)
        max_val = max(self.data)
        
        # Handle the case where all values are the same
        if max_val == min_val:
            return [0.5] * len(self.data)
        
        # Normalize each value to the 0-1 range
        normalized = [(x - min_val) / (max_val - min_val) for x in self.data]
        self.processed = True  # Mark that we've processed the data
        return normalized
    
    def get_statistics(self):
        """Get basic statistics of the data."""
        if not self.data:
            return {}
        
        # Calculate and return basic statistics
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
        
        # Calculate mean and standard deviation
        mean = sum(self.data) / len(self.data)
        std = (sum((x - mean) ** 2 for x in self.data) / len(self.data)) ** 0.5
        
        # Find values that are more than 'threshold' standard deviations from the mean
        outliers = [x for x in self.data if abs(x - mean) > threshold * std]
        return outliers
# In ML context: This class could be used to preprocess any dataset
# For example: normalizing features, detecting outliers, or calculating statistics
```

```python
# Test the DataProcessor class
data = [1, 2, 3, 4, 5, 100]  # 100 is an outlier
processor = DataProcessor(data)  # Create a new DataProcessor object
print("Original data:", processor.data)                    # Access the data attribute
print("Normalized data:", processor.normalize())           # Call the normalize method
print("Statistics:", processor.get_statistics())           # Call the statistics method
print("Outliers:", processor.add_outlier_detection())     # Call the outlier detection method
# Notice how we can call different methods on the same object
# This is the power of OOP - related functionality is grouped together
```

### Creating a Simple ML Model Class

Now let's create a simple machine learning model! This is where everything comes together.

**What is linear regression?** It's a method to find the best straight line that fits our data. The line has the form: y = slope × x + intercept

**Why is this important?** Linear regression is one of the most fundamental ML algorithms. Understanding it helps you understand more complex models.

```python
class SimpleLinearModel:
    """
    A simple linear regression model implementation.
    """
    
    def __init__(self):
        # Initialize model parameters
        self.slope = 0        # The slope of our line (how steep it is)
        self.intercept = 0    # Where the line crosses the y-axis
        self.trained = False  # Whether we've trained the model yet
    
    def fit(self, X, y):
        """
        Fit the model using simple linear regression.
        X: list of input values (features)
        y: list of target values (what we want to predict)
        """
        # Check that we have the same number of inputs and outputs
        if len(X) != len(y):
            raise ValueError("X and y must have the same length")
        
        # Calculate the number of data points
        n = len(X)
        
        # Calculate sums needed for the linear regression formula
        sum_x = sum(X)                    # Sum of all X values
        sum_y = sum(y)                    # Sum of all y values
        sum_xy = sum(x * y for x, y in zip(X, y))  # Sum of X*y products
        sum_x2 = sum(x**2 for x in X)    # Sum of X squared values
        
        # Calculate slope using the least squares formula
        self.slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x**2)
        
        # Calculate intercept using the slope
        self.intercept = (sum_y - self.slope * sum_x) / n
        
        # Mark the model as trained
        self.trained = True
    
    def predict(self, X):
        """Make predictions using the fitted model."""
        if not self.trained:
            raise ValueError("Model must be trained before making predictions")
        
        # Use the formula: y = slope * x + intercept
        return [self.slope * x + self.intercept for x in X]
    
    def get_parameters(self):
        """Get model parameters."""
        return {
            'slope': self.slope,
            'intercept': self.intercept,
            'trained': self.trained
        }
# In ML context: This is a complete machine learning model!
# It can learn from data (fit) and make predictions (predict)
```

```python
# Test the SimpleLinearModel
# Create some sample data
X = [1, 2, 3, 4, 5]                    # Input features
y = [2, 4, 6, 8, 10]                   # Target values (perfect linear relationship)
# Create and train the model
model = SimpleLinearModel()              # Create a new model
model.fit(X, y)                         # Train the model on our data
print("Model parameters:", model.get_parameters())
# Make predictions
predictions = model.predict([6, 7, 8])  # Predict for new data points
print("Predictions for [6, 7, 8]:", predictions)
# In this case, since our data has a perfect linear relationship (y = 2x),
# the model should learn slope=2 and intercept=0
# So predictions for [6, 7, 8] should be [12, 14, 16]
```

### Visualising the Results

Now let's create visualisations to better understand our linear regression model and its predictions.

**Why visualise?** Visualisations help us understand what our model is doing. They can show us how well our model fits the data, where it makes mistakes, and how confident we should be in our predictions.

**What will we learn?** We'll see how to create different types of plots that are commonly used in machine learning to evaluate model performance.

```python
import matplotlib.pyplot as plt
import numpy as np
# Create a more comprehensive dataset for visualisation
X_train = [1, 2, 3, 4, 5]
y_train = [2.1, 3.9, 6.2, 7.8, 10.1]  # Slightly noisy data (not perfectly linear)
# Train the model
model = SimpleLinearModel()
model.fit(X_train, y_train)
# Create test data for predictions
X_test = [0, 1, 2, 3, 4, 5, 6, 7, 8]  # Extended range for plotting
y_test = model.predict(X_test)
# Create the plot
plt.figure(figsize=(10, 6))
# Plot training data (the points we used to train the model)
plt.scatter(X_train, y_train, color='blue', s=100, label='Training Data', zorder=5)
# Plot the regression line (the model's prediction line)
plt.plot(X_test, y_test, color='red', linewidth=2, label='Linear Regression')
# Plot predictions for new data points (points we didn't train on)
new_points = [6, 7, 8]
new_predictions = model.predict(new_points)
plt.scatter(new_points, new_predictions, color='green', s=100, marker='s', 
           label='Predictions', zorder=5)
# Add labels and title
plt.xlabel('X Values')
plt.ylabel('Y Values')
plt.title('Simple Linear Regression Model')
plt.legend()
plt.grid(True, alpha=0.3)
# Add model equation to the plot
params = model.get_parameters()
equation = f'y = {params["slope"]:.2f}x + {params["intercept"]:.2f}'
plt.text(0.05, 0.95, f'Model: {equation}', transform=plt.gca().transAxes, 
         bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
plt.tight_layout()
plt.show()
# This plot shows:
# - Blue dots: Our training data (what the model learned from)
# - Red line: The best-fit line the model found
# - Green squares: Predictions for new data points
```

<!-- end NOTEBOOK: -->