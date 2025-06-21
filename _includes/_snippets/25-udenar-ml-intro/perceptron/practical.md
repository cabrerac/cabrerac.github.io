<!-- NOTEBOOK: -->

# Practical Introduction

In this practical session, we will continue exploring linear regression and classification models and how we can use them. We will then explore the perceptron concept in practice.

---

## Exercise 1: Multivariate Linear Regression and Probabilistic Interpretation

In this exercise, we'll explore multivariate linear regression from both a deterministic and probabilistic perspective. We'll implement the model from scratch and compare it with scikit-learn's implementation, then examine the probabilistic interpretation.

Let's start by importing the necessary libraries.

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import seaborn as sns
```

We can now create a synthetic dataset for our analysis:

```python
# Set random seed for reproducibility
np.random.seed(42)
# Generate synthetic data for multivariate regression
n_samples = 1000
n_features = 3
# True parameters
true_weights = np.array([2.5, -1.8, 0.9])
true_bias = 3.2
# Generate features
X = np.random.randn(n_samples, n_features)
# Generate target with noise (probabilistic interpretation)
noise_std = 0.5
y_true = np.dot(X, true_weights) + true_bias
y = y_true + np.random.normal(0, noise_std, n_samples)
```

As always we should explore our data first:

```python
# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"Dataset shape: {X.shape}")
print(f"True weights: {true_weights}")
print(f"True bias: {true_bias}")
print(f"Noise standard deviation: {noise_std}")
```

Now, let's implement multivariate linear regression from scratch using the normal equation approach. This will help us understand the mathematical foundations.

```python
class MultivariateLinearRegression:
    def __init__(self):
        self.weights = None
        self.bias = None       
    def fit(self, X, y):
        # Add bias term to features
        X_b = np.c_[np.ones((X.shape[0], 1)), X]
        # Normal equation: w = (X^T X)^(-1) X^T y
        self.weights = np.linalg.inv(X_b.T.dot(X_b)).dot(X_b.T).dot(y)
        self.bias = self.weights[0]
        self.weights = self.weights[1:]
    def predict(self, X):
        return np.dot(X, self.weights) + self.bias
```

We can train our implementation and compare it with the linear regression model from scikit-learn:

```python
# Train our implementation
our_model = MultivariateLinearRegression()
our_model.fit(X_train, y_train)
# Train scikit-learn's implementation
sk_model = LinearRegression()
sk_model.fit(X_train, y_train)
# Compare results
print("Our Implementation:")
print(f"Weights: {our_model.weights}")
print(f"Bias: {our_model.bias:.4f}")
print("\nScikit-learn Implementation:")
print(f"Weights: {sk_model.coef_}")
print(f"Bias: {sk_model.intercept_:.4f}")
print(f"\nTrue Weights: {true_weights}")
print(f"True Bias: {true_bias}")
```

Let's evaluate the performance of both models and visualize the results.

```python
# Make predictions
our_predictions = our_model.predict(X_test)
sk_predictions = sk_model.predict(X_test)
# Calculate metrics
our_mse = mean_squared_error(y_test, our_predictions)
sk_mse = mean_squared_error(y_test, sk_predictions)
our_r2 = r2_score(y_test, our_predictions)
sk_r2 = r2_score(y_test, sk_predictions)
print("Performance Comparison:")
print(f"Our Model - MSE: {our_mse:.4f}, R²: {our_r2:.4f}")
print(f"Scikit-learn - MSE: {sk_mse:.4f}, R²: {sk_r2:.4f}")
# Visualize predictions vs actual values
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
ax1.scatter(y_test, our_predictions, alpha=0.6)
ax1.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
ax1.set_xlabel('Actual Values')
ax1.set_ylabel('Predicted Values')
ax1.set_title('Our Implementation')
ax2.scatter(y_test, sk_predictions, alpha=0.6)
ax2.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
ax2.set_xlabel('Actual Values')
ax2.set_ylabel('Predicted Values')
ax2.set_title('Scikit-learn Implementation')
plt.tight_layout()
plt.show()
```

Now, let's explore the probabilistic interpretation by examining the likelihood function and maximum likelihood estimation. For that, we will need to define some functions. First, let's define our log likelihood.

```python
def log_likelihood(X, y, weights, bias, sigma):
    """Calculate the log-likelihood for given parameters"""
    predictions = np.dot(X, weights) + bias
    residuals = y - predictions
    n = len(y)  
    # Log-likelihood for Gaussian noise
    log_likelihood = -n/2 * np.log(2 * np.pi * sigma**2) - np.sum(residuals**2) / (2 * sigma**2)
    return log_likelihood
```

And then our negative log likelihood function:

```python
def negative_log_likelihood(params, X, y):
    """Negative log-likelihood for optimization"""
    weights = params[:-2]
    bias = params[-2]
    sigma = params[-1]
    return -log_likelihood(X, y, weights, bias, sigma)
```

Computing the likelihood for different parameter values and minimising using `scipy`:

```python
# Calculate likelihood for different parameter values
from scipy.optimize import minimize
# Initial guess
initial_params = np.concatenate([our_model.weights, [our_model.bias, noise_std]])
# Optimise using maximum likelihood
result = minimize(negative_log_likelihood, initial_params, args=(X_train, y_train))
ml_weights = result.x[:-2]
ml_bias = result.x[-2]
ml_sigma = result.x[-1]
print("Maximum Likelihood Estimation Results:")
print(f"Estimated weights: {ml_weights}")
print(f"Estimated bias: {ml_bias:.4f}")
print(f"Estimated noise std: {ml_sigma:.4f}")
print(f"True noise std: {noise_std}")
# Compare likelihood values
our_likelihood = log_likelihood(X_test, y_test, our_model.weights, our_model.bias, noise_std)
ml_likelihood = log_likelihood(X_test, y_test, ml_weights, ml_bias, ml_sigma)
print(f"\nLog-likelihood comparison:")
print(f"Our model: {our_likelihood:.4f}")
print(f"Maximum likelihood: {ml_likelihood:.4f}")
```

Let's visualise the probabilistic nature of our predictions by showing the uncertainty in our model.

```python
# Calculate prediction intervals
def prediction_intervals(X, weights, bias, sigma, confidence=0.95):
    """Calculate prediction intervals"""
    predictions = np.dot(X, weights) + bias    
    # For 95% confidence interval, use 1.96 standard deviations
    z_score = 1.96 if confidence == 0.95 else 2.58  # 99% confidence    
    lower_bound = predictions - z_score * sigma
    upper_bound = predictions + z_score * sigma    
    return predictions, lower_bound, upper_bound
```

Utilising our visualisation:

```python
# Calculate intervals for test set
preds, lower, upper = prediction_intervals(X_test, ml_weights, ml_bias, ml_sigma)
# Randomly select 10 data points for better visualization
np.random.seed(42)  # For reproducibility
n_plot = min(10, len(y_test))  # Select 10 points or all if less than 10
indices = np.random.choice(len(y_test), n_plot, replace=False)
# Sort the random indices to plot correctly
sorted_indices = np.sort(indices)
# Visualize predictions with uncertainty (using only selected points)
plt.figure(figsize=(10, 6))
# For scatter plot, order doesn't matter, but using sorted_indices for consistency
plt.scatter(sorted_indices, y_test[sorted_indices], alpha=0.6, label='Actual Values')
# For line plot and fill_between, sorted x-axis is crucial
plt.plot(sorted_indices, preds[sorted_indices], 'r-', label='Predictions')
plt.fill_between(sorted_indices, lower[sorted_indices], upper[sorted_indices], alpha=0.3, label='95% Confidence Interval')
plt.xlabel('Sample Index')
plt.ylabel('Target Value')
plt.title('Predictions with Uncertainty Bands (10 Random Samples)')
plt.legend()
plt.show()
# Check coverage of confidence interval (using all data)
coverage = np.mean((y_test >= lower) & (y_test <= upper))
print(f"Coverage of 95% confidence interval: {coverage:.3f} (should be close to 0.95)")
```

---

## Exercise 2: Linear Basis Function and Cross Validation

In this exercise, we'll explore linear basis function models and cross-validation techniques. We'll implement polynomial and Gaussian basis functions, and use cross-validation to find optimal hyperparameters.

Let's start by creating a dataset that demonstrates the need for non-linear transformations.

```python
# Generate non-linear data
np.random.seed(42)
n_samples = 200
# Generate features
X = np.linspace(-3, 3, n_samples).reshape(-1, 1)
# Generate non-linear target with noise
y_true = 2 * np.sin(X.flatten()) + 0.5 * X.flatten()**2
y = y_true + np.random.normal(0, 0.3, n_samples)
# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
# Visualize the data
plt.figure(figsize=(10, 6))
plt.scatter(X_train, y_train, alpha=0.6, label='Training Data')
plt.scatter(X_test, y_test, alpha=0.6, label='Test Data')
plt.plot(X, y_true, 'r-', linewidth=2, label='True Function')
plt.xlabel('X')
plt.ylabel('y')
plt.title('Non-linear Dataset')
plt.legend()
plt.show()
```

Now, let's implement different basis function transformations.

```python
class BasisFunctionTransformer:
    def __init__(self, basis_type='polynomial', degree=3, n_centers=5):
        self.basis_type = basis_type
        self.degree = degree
        self.n_centers = n_centers
        self.centers = None      
    def fit(self, X):
        if self.basis_type == 'gaussian':
            # Set Gaussian centers evenly across the feature range
            self.centers = np.linspace(X.min(), X.max(), self.n_centers)
        return self   
    def transform(self, X):
        if self.basis_type == 'polynomial':
            return self._polynomial_basis(X)
        elif self.basis_type == 'gaussian':
            return self._gaussian_basis(X)
        else:
            raise ValueError(f"Unknown basis type: {self.basis_type}")
    def _polynomial_basis(self, X):
        """Create polynomial basis functions"""
        features = []
        for i in range(self.degree + 1):
            features.append(X ** i)
        return np.hstack(features)
    def _gaussian_basis(self, X):
        """Create Gaussian basis functions"""
        features = []
        sigma = (self.centers[1] - self.centers[0]) / 2  # Set sigma based on center spacing
        for center in self.centers:
            phi = np.exp(-0.5 * ((X - center) / sigma) ** 2)
            features.append(phi)
        return np.hstack(features)

We can test the different basis functions now:

```python
# Test different basis functions
polynomial_transformer = BasisFunctionTransformer(basis_type='polynomial', degree=3)
gaussian_transformer = BasisFunctionTransformer(basis_type='gaussian', n_centers=5)
polynomial_transformer.fit(X_train)
gaussian_transformer.fit(X_train)
X_poly = polynomial_transformer.transform(X_train)
X_gauss = gaussian_transformer.transform(X_train)
print(f"Original features shape: {X_train.shape}")
print(f"Polynomial basis shape: {X_poly.shape}")
print(f"Gaussian basis shape: {X_gauss.shape}")
```

Let's implement cross-validation to find optimal hyperparameters for our basis function models. First, we import the required libraries.

```python
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline
```

```python
def evaluate_basis_functions(X, y, basis_type='polynomial', param_range=None):
    """Evaluate different basis function configurations using cross-validation"""
    if param_range is None:
        if basis_type == 'polynomial':
            param_range = range(1, 8)  # degrees 1-7
        else:
            param_range = range(3, 12)  # centers 3-11  
    cv_scores = []
    for param in param_range:
        if basis_type == 'polynomial':
            transformer = BasisFunctionTransformer(basis_type='polynomial', degree=param)
        else:
            transformer = BasisFunctionTransformer(basis_type='gaussian', n_centers=param)
        # Create pipeline
        pipeline = Pipeline([
            ('basis', transformer),
            ('regression', LinearRegression())
        ])
        # Perform cross-validation
        scores = cross_val_score(pipeline, X, y, cv=5, scoring='neg_mean_squared_error')
        cv_scores.append(-scores.mean())  # Convert back to positive MSE
    return param_range, cv_scores
```

And the evaluation of the basis functions using cross validation:

```python
# Evaluate polynomial basis functions
poly_params, poly_scores = evaluate_basis_functions(X_train, y_train, 'polynomial')
# Evaluate Gaussian basis functions
gauss_params, gauss_scores = evaluate_basis_functions(X_train, y_train, 'gaussian')
# Visualize cross-validation results
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
ax1.plot(poly_params, poly_scores, 'bo-')
ax1.set_xlabel('Polynomial Degree')
ax1.set_ylabel('Mean Squared Error')
ax1.set_title('Cross-validation: Polynomial Basis')
ax1.grid(True)
ax2.plot(gauss_params, gauss_scores, 'ro-')
ax2.set_xlabel('Number of Gaussian Centers')
ax2.set_ylabel('Mean Squared Error')
ax2.set_title('Cross-validation: Gaussian Basis')
ax2.grid(True)
plt.tight_layout()
plt.show()
# Find optimal parameters
best_poly_degree = poly_params[np.argmin(poly_scores)]
best_gauss_centers = gauss_params[np.argmin(gauss_scores)]
print(f"Optimal polynomial degree: {best_poly_degree}")
print(f"Optimal number of Gaussian centers: {best_gauss_centers}")
```

Now, let's train models with the optimal parameters and compare their performance.

```python
# Train models with optimal parameters
best_poly_transformer = BasisFunctionTransformer(basis_type='polynomial', degree=best_poly_degree)
best_gauss_transformer = BasisFunctionTransformer(basis_type='gaussian', n_centers=best_gauss_centers)
best_poly_transformer.fit(X_train)
best_gauss_transformer.fit(X_train)
X_poly_opt = best_poly_transformer.transform(X_train)
X_gauss_opt = best_gauss_transformer.transform(X_train)
# Train regression models
poly_model = LinearRegression()
gauss_model = LinearRegression()
poly_model.fit(X_poly_opt, y_train)
gauss_model.fit(X_gauss_opt, y_train)
# Make predictions
X_poly_test = best_poly_transformer.transform(X_test)
X_gauss_test = best_gauss_transformer.transform(X_test)
poly_pred = poly_model.predict(X_poly_test)
gauss_pred = gauss_model.predict(X_gauss_test)
# Evaluate performance
poly_mse = mean_squared_error(y_test, poly_pred)
gauss_mse = mean_squared_error(y_test, gauss_pred)
poly_r2 = r2_score(y_test, poly_pred)
gauss_r2 = r2_score(y_test, gauss_pred)
print("Performance Comparison:")
print(f"Polynomial Basis - MSE: {poly_mse:.4f}, R²: {poly_r2:.4f}")
print(f"Gaussian Basis - MSE: {gauss_mse:.4f}, R²: {gauss_r2:.4f}")
# Visualize the fitted models
X_plot = np.linspace(-3, 3, 1000).reshape(-1, 1)
X_poly_plot = best_poly_transformer.transform(X_plot)
X_gauss_plot = best_gauss_transformer.transform(X_plot)
poly_plot_pred = poly_model.predict(X_poly_plot)
gauss_plot_pred = gauss_model.predict(X_gauss_plot)
plt.figure(figsize=(12, 8))
plt.subplot(2, 1, 1)
plt.scatter(X_train, y_train, alpha=0.6, label='Training Data')
plt.scatter(X_test, y_test, alpha=0.6, label='Test Data')
plt.plot(X_plot, poly_plot_pred, 'r-', linewidth=2, label=f'Polynomial (degree={best_poly_degree})')
plt.plot(X, y_true, 'g--', linewidth=2, label='True Function')
plt.xlabel('X')
plt.ylabel('y')
plt.title('Polynomial Basis Function Model')
plt.legend()
plt.subplot(2, 1, 2)
plt.scatter(X_train, y_train, alpha=0.6, label='Training Data')
plt.scatter(X_test, y_test, alpha=0.6, label='Test Data')
plt.plot(X_plot, gauss_plot_pred, 'r-', linewidth=2, label=f'Gaussian ({best_gauss_centers} centers)')
plt.plot(X, y_true, 'g--', linewidth=2, label='True Function')
plt.xlabel('X')
plt.ylabel('y')
plt.title('Gaussian Basis Function Model')
plt.legend()
plt.tight_layout()
plt.show()
```

Let's also implement k-fold cross-validation from scratch to better understand the process.

```python
def k_fold_cross_validation(X, y, k=5, model_type='linear'):
    """Implement k-fold cross-validation from scratch"""
    n_samples = len(X)
    fold_size = n_samples // k
    indices = np.random.permutation(n_samples)   
    cv_scores = []
    for i in range(k):
        # Define validation indices
        val_start = i * fold_size
        val_end = val_start + fold_size if i < k - 1 else n_samples
        val_indices = indices[val_start:val_end]
        train_indices = np.concatenate([indices[:val_start], indices[val_end:]])
        # Split data
        X_train_fold = X[train_indices]
        y_train_fold = y[train_indices]
        X_val_fold = X[val_indices]
        y_val_fold = y[val_indices]
        # Train model
        if model_type == 'linear':
            model = LinearRegression()
        else:
            model = LinearRegression()
        model.fit(X_train_fold, y_train_fold)
        # Evaluate
        y_pred_fold = model.predict(X_val_fold)
        mse = mean_squared_error(y_val_fold, y_pred_fold)
        cv_scores.append(mse)
    return np.array(cv_scores)
```

Testing our cross-validation implementation:

```python
# Test our cross-validation implementation
np.random.seed(42)
cv_scores_manual = k_fold_cross_validation(X_train, y_train, k=5)
print("Manual Cross-validation Results:")
print(f"Individual fold MSEs: {cv_scores_manual}")
print(f"Mean MSE: {cv_scores_manual.mean():.4f}")
print(f"Standard deviation: {cv_scores_manual.std():.4f}")
```

Finally, let's demonstrate the importance of cross-validation by showing how different train-test splits can lead to different conclusions.

```python
# Compare different random seeds for train-test split
seeds = [42, 123, 456, 789, 999]
results = []
for seed in seeds:
    X_train_temp, X_test_temp, y_train_temp, y_test_temp = train_test_split(
        X, y, test_size=0.3, random_state=seed
    )  
    # Use optimal polynomial model
    transformer = BasisFunctionTransformer(basis_type='polynomial', degree=best_poly_degree)
    transformer.fit(X_train_temp)
    X_train_transformed = transformer.transform(X_train_temp)
    X_test_transformed = transformer.transform(X_test_temp)
    model = LinearRegression()
    model.fit(X_train_transformed, y_train_temp)
    y_pred_temp = model.predict(X_test_transformed)
    mse_temp = mean_squared_error(y_test_temp, y_pred_temp)
    r2_temp = r2_score(y_test_temp, y_pred_temp)
    results.append({'seed': seed, 'mse': mse_temp, 'r2': r2_temp})
# Visualize the variation
results_df = pd.DataFrame(results)
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.bar(range(len(results)), [r['mse'] for r in results])
plt.xlabel('Random Seed')
plt.ylabel('Mean Squared Error')
plt.title('MSE Variation Across Different Splits')
plt.subplot(1, 2, 2)
plt.bar(range(len(results)), [r['r2'] for r in results])
plt.xlabel('Random Seed')
plt.ylabel('R² Score')
plt.title('R² Variation Across Different Splits')
plt.tight_layout()
plt.show()
print("Results across different random seeds:")
for result in results:
    print(f"Seed {result['seed']}: MSE={result['mse']:.4f}, R²={result['r2']:.4f}")
```

---

## Exercise 3: Linear Classifiers

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

## Exercise 4: The Perceptron

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

## Homework - Linear Basis Functions and Cross-Validation

The homework assignment is focused on exploring the power of Linear Basis Function Models. You will apply the concepts learned in this practical session to a dataset of your choice (you can use a new one or continue with a previous one), preferably one with non-linear relationships.

Your task is to:

1.  **Define a Decision Matrix**: Create a systematic plan to evaluate different linear basis functions. This involves selecting a range of hyperparameters to test. For example:
    *   **Polynomial Basis**: Test various degrees (e.g., from 2 to 10).
    *   **Gaussian Basis**: Test different numbers of centers (e.g., from 5 to 20).
    You should document your choices in a table or matrix format, which will guide your evaluation.

2.  **Evaluate using Cross-Validation**: Use the k-fold cross-validation techniques from this practical (`cross_val_score` or the manual implementation) to evaluate the performance of each configuration defined in your decision matrix. Your goal is to find the optimal hyperparameter for each basis function type based on the cross-validation scores (e.g., Mean Squared Error).

3.  **Analyse and Select**: Visualise the cross-validation results (e.g., plotting MSE vs. hyperparameter value). Based on your analysis, select the best basis function type and its optimal hyperparameter.

4.  **Final Model Evaluation**: Train a final `LinearRegression` model using the best basis function configuration on the entire training set and evaluate its performance on the test set.

5.  **Discussion**: Discuss your findings. Compare the performance of the optimised basis function model with a simple linear regression model. Did the basis functions help capture the non-linearity in the data? Explain your results.

<DESCRIBE YOUR SOLUTION HERE>

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

