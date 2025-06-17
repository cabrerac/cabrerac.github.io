<!-- NOTEBOOK: -->

# Practical Introduction

In this practical session, we will continue exploring linear regression and classification models and how we can use them. We will then explore the perceptron concept in practice.

---

## Exercise 1: Multivariate Linear Regression

In this exercise, we will implement multivariate linear regression using the Boston Housing dataset. We'll focus on:
- Data preprocessing and feature scaling
- Model training and evaluation
- Understanding model coefficients
- Visualizing results

We first start importing the relevant libraries.

```python
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns
```

We continue loading the relevant dataset.

```python
# Load the Boston Housing dataset
url = "https://raw.githubusercontent.com/selva86/datasets/master/BostonHousing.csv"
boston_data = pd.read_csv(url)
# Display basic information
print("Dataset Shape:", boston_data.shape)
print("\nFirst few rows:")
print(boston_data.head())
```

And then follow with the data preprocessing.

```python
# Select features and target
X = boston_data.drop('medv', axis=1)
y = boston_data['medv']
# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
# Split data
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
```

We will use a linear model as we have done before. Now, our input data is multi-variable.

```python
# Train model
model = LinearRegression()
model.fit(X_train, y_train)
# Evaluate model
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f"Mean Squared Error: {mse:.2f}")
print(f"R² Score: {r2:.2f}")
# Display coefficients
coefficients = pd.DataFrame({
    'Feature': boston_data.drop('medv', axis=1).columns,
    'Coefficient': model.coef_
})
print("\nFeature Coefficients:")
print(coefficients.sort_values('Coefficient', ascending=False))
```

We then evaluate the resulting outputs and analyse the feature importance.

```python
# Plot actual vs predicted values
plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred, alpha=0.5)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
plt.xlabel('Actual Values')
plt.ylabel('Predicted Values')
plt.title('Actual vs Predicted Values')
plt.show()
# Plot feature importance
plt.figure(figsize=(12, 6))
sns.barplot(x='Coefficient', y='Feature', data=coefficients.sort_values('Coefficient', ascending=False))
plt.title('Feature Importance')
plt.show()
```

---

## Exercise 2: Linear Classifiers

In this exercise, we'll explore different linear classifiers using the Iris dataset. We'll learn how to implement and compare various classification algorithms, visualize their decision boundaries, and understand their performance characteristics.

Let's start by importing the necessary libraries and loading our dataset.

```python
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, classification_report
import numpy as np
import matplotlib.pyplot as plt
# Load Iris dataset
iris = load_iris()
X = iris.data
y = iris.target
# For visualization, we'll use only two features
X_2d = X[:, [0, 1]]  # Sepal length and width
# Split data
X_train, X_test, y_train, y_test = train_test_split(X_2d, y, test_size=0.2, random_state=42)
```

Now, let's implement and compare different linear classifiers. We'll use three popular algorithms: Logistic Regression, Linear SVM, and SGD Classifier.

```python
# Initialize models
models = {
    'Logistic Regression': LogisticRegression(),
    'Linear SVM': LinearSVC(),
    'SGD Classifier': SGDClassifier()
}
# Train and evaluate models
results = {}
for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    results[name] = {
        'model': model,
        'accuracy': accuracy,
        'predictions': y_pred
    }
    print(f"\n{name} Results:")
    print(f"Accuracy: {accuracy:.3f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
```

To better understand how these classifiers work, let's visualize their decision boundaries. This will help us see how each algorithm separates the different classes in our feature space.

```python
def plot_decision_boundary(X, y, model, title):
    h = 0.02  # Step size
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
    
    Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    
    plt.figure(figsize=(8, 6))
    plt.contourf(xx, yy, Z, alpha=0.4)
    plt.scatter(X[:, 0], X[:, 1], c=y, alpha=0.8)
    plt.xlabel('Sepal Length')
    plt.ylabel('Sepal Width')
    plt.title(title)
    plt.show()
```

We end plotting the decision boundaries for each model.

```python
# Plot decision boundaries for each model
for name, result in results.items():
    plot_decision_boundary(X_2d, y, result['model'], f'Decision Boundary - {name}')
```

---

## Exercise 3: The Perceptron

In this final exercise, we'll implement a perceptron from scratch and compare it with scikit-learn's implementation. This will help us understand the fundamental concepts behind neural networks and how they learn from data.

First, let's implement our own perceptron class. This implementation will help us understand the learning process and how the perceptron updates its weights.

```python
class Perceptron:
    def __init__(self, learning_rate=0.01, epochs=1000):
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.weights = None
        self.bias = None
        self.errors_ = []
        
    def fit(self, X, y):
        n_samples, n_features = X.shape
        self.weights = np.zeros(n_features)
        self.bias = 0
        
        for _ in range(self.epochs):
            errors = 0
            for idx, x_i in enumerate(X):
                linear_output = np.dot(x_i, self.weights) + self.bias
                y_predicted = np.where(linear_output >= 0, 1, -1)
                
                if y[idx] * y_predicted <= 0:
                    self.weights += self.learning_rate * y[idx] * x_i
                    self.bias += self.learning_rate * y[idx]
                    errors += 1
                    
            self.errors_.append(errors)
            if errors == 0:
                break
                
    def predict(self, X):
        linear_output = np.dot(X, self.weights) + self.bias
        return np.where(linear_output >= 0, 1, -1)
```

Now, let's create a simple dataset to test our implementation. We'll use a binary classification problem to make it easier to visualize the results.

```python
# Create a simple binary classification dataset
X = np.array([[1, 2], [2, 3], [3, 1], [4, 3], [5, 2], [6, 1]])
y = np.array([1, 1, -1, 1, -1, -1])
# Train our perceptron
perceptron = Perceptron(learning_rate=0.01, epochs=1000)
perceptron.fit(X, y)
```

Let's visualize how our perceptron learns over time. This will help us understand the convergence process and how the number of errors changes during training.

```python
# Plot the learning process
plt.figure(figsize=(10, 4))
plt.plot(perceptron.errors_)
plt.xlabel('Epochs')
plt.ylabel('Number of Errors')
plt.title('Perceptron Learning Process')
plt.show()
```

To better understand how our perceptron makes decisions, let's visualize its decision boundary. This will show us how it separates the two classes in our feature space.

```python
def plot_decision_boundary_perceptron(X, y, model):
    h = 0.02
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
    
    Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    
    plt.figure(figsize=(8, 6))
    plt.contourf(xx, yy, Z, alpha=0.4)
    plt.scatter(X[:, 0], X[:, 1], c=y, alpha=0.8)
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.title('Perceptron Decision Boundary')
    plt.show()

plot_decision_boundary_perceptron(X, y, perceptron)
```

Finally, let's compare our implementation with scikit-learn's perceptron to ensure our implementation is working correctly.

```python
from sklearn.linear_model import Perceptron as SklearnPerceptron
# Train scikit-learn's perceptron
sk_perceptron = SklearnPerceptron(max_iter=1000, random_state=42)
sk_perceptron.fit(X, y)
# Compare predictions
our_predictions = perceptron.predict(X)
sk_predictions = sk_perceptron.predict(X)
print("Our Perceptron Accuracy:", np.mean(our_predictions == y))
print("Scikit-learn Perceptron Accuracy:", np.mean(sk_predictions == y))
```

---

## Homework - The Perceptron

The homework assignment will help you applying linear regression algorithms we've learned to a dataset of your choice. You may use a new dataset or continue with the one you defined in previous homeworks. Your task is to use the implementation of the Gradient Descent algorithms in this practical to build a pipeline that applies linear regression in your data and evaluates the results with different hyperparameter values. You are free to explore as much as you wish!

You should provide a clear analysis and narrative of the different steps you used in your implementation, explaining your reasoning and choices throughout the process.

<DESCRIBE YOUR DATASET HERE>

```python
# Write your pipeline here
```

### Submission Guidelines

- Submit your solution as a Jupyter notebook with the following name format: `cease_ml_intro_session_6_<email_username>.ipynb`
- Include clear comments explaining your code
- Provide a written analysis of your results
- Provide a narrative and explanation of the different steps you used in your implementation
- Document any challenges faced and how you overcame them
- Due date: [26/06/2025]

<!-- end NOTEBOOK: -->

