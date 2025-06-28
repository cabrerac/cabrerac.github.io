<!-- NOTEBOOK: -->

# Practical Introduction

In this practical session, we will implement neural networks from scratch and explore deep learning concepts. We'll build multi-layer perceptrons, implement backpropagation, and compare with modern deep learning frameworks.

---

## Exercise 1: Cross Validation for Time Series Data

In this exercise, we'll learn how to properly perform cross-validation for time series data. Unlike standard cross-validation, time series data has a temporal order that must be respected to avoid data leakage from the future into the past. We'll use **TimeSeriesSplit** from scikit-learn to demonstrate this approach.

Let's start by importing the necessary libraries and creating a synthetic time series dataset:

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import TimeSeriesSplit
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_squared_error
```

We'll generate a simple time series dataset:

```python
# Generate a synthetic time series
time = np.arange(100)
# Create a signal with trend and noise
y = 0.5 * time + 10 * np.sin(0.2 * time) + np.random.normal(scale=5, size=len(time))
plt.figure(figsize=(10, 4))
plt.plot(time, y, label='Time Series')
plt.xlabel('Time')
plt.ylabel('Value')
plt.title('Synthetic Time Series Data')
plt.legend()
plt.show()
```

Now, let's prepare the data for supervised learning. We'll use previous values to predict the next value (a simple lagged regression function):

```python
def create_lagged_features(y, lag=3):
    X, y_out = [], []
    for i in range(lag, len(y)):
        X.append(y[i-lag:i])
        y_out.append(y[i])
    return np.array(X), np.array(y_out)
```

Create lagged features (e.g., use previous 3 values to predict the next)

```python
lag = 3
X, y_supervised = create_lagged_features(y, lag=lag)
print(f"Feature shape: {X.shape}, Target shape: {y_supervised.shape}")
```

### Time Series Cross-Validation

**TimeSeriesSplit** is a cross-validation technique specifically designed for time series data. It works by splitting the data into a specified number of consecutive training and test sets, ensuring that the training data always precedes the test data in time. Unlike traditional cross-validation, which randomly shuffles data, **TimeSeriesSplit** maintains the temporal order, preventing data leakage from future to past. Each split uses a growing window of training data and a contiguous block of test data, allowing the model to be trained on past observations and tested on future observations. This method is crucial for evaluating models on time series data, where the chronological order of data points is significant.

We split the data in train, validation, and test sets. We use **TimeSeriesSplit** on the train and validation set:

```python
# 1. Hold out the last 20% as test set
test_size = int(0.2 * len(X))
X_trainval, X_test = X[:-test_size], X[-test_size:]
y_trainval, y_test = y_supervised[:-test_size], y_supervised[-test_size:]
# 2. Use TimeSeriesSplit on the training+validation set
n_splits = 5
tscv = TimeSeriesSplit(n_splits=n_splits)
```

Now, we perform our cross validation using the splitted data.

```python
# Try different values of alpha (the hyperparameter)
alphas = [0.01, 0.1, 1, 10, 100]
best_alpha = None
best_score = float('inf')
for alpha in alphas:
    mse_scores = []
    for train_idx, val_idx in tscv.split(X_trainval):
        X_train, X_val = X_trainval[train_idx], X_trainval[val_idx]
        y_train, y_val = y_trainval[train_idx], y_trainval[val_idx]
        model = Ridge(alpha=alpha)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_val)
        mse = mean_squared_error(y_val, y_pred)
        mse_scores.append(mse)
    avg_mse = np.mean(mse_scores)
    print(f"Alpha: {alpha}, Avg Validation MSE: {avg_mse:.4f}")
    if avg_mse < best_score:
        best_score = avg_mse
        best_alpha = alpha
print(f"Best alpha: {best_alpha}")
```

We can now retrain on all training and validation dataset and evaluate on the test set, using the best hyperparameter value.

```python
print(f"Best alpha: {best_alpha}")
# Retrain final model with best alpha
final_model = Ridge(alpha=best_alpha)
final_model.fit(X_trainval, y_trainval)
y_test_pred = final_model.predict(X_test)
test_mse = mean_squared_error(y_test, y_test_pred)
print(f"Test MSE: {test_mse:.4f}")
# Plot test predictions
plt.figure(figsize=(10, 4))
plt.plot(range(len(y)), y, label='True Time Series')
plt.plot(range(len(y)-test_size, len(y)), y_test_pred, '--', label='Test Prediction')
plt.xlabel('Time')
plt.ylabel('Value')
plt.title('Final Model Test Set Prediction')
plt.legend()
plt.show()
```

---

## Exercise 2: Implementing Neural Networks from Scratch

In this exercise, we'll implement a multi-layer neural network from scratch, including forward propagation, backpropagation, and training. This will help us understand the fundamental concepts behind neural networks.

Let's start by importing the necessary libraries.

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification, make_regression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_squared_error
import seaborn as sns
```

We'll create a synthetic dataset for our neural network experiments:

```python
# Set random seed for reproducibility
np.random.seed(42)
# Create classification dataset
X_class, y_class = make_classification(
    n_samples=1000, 
    n_features=2, 
    n_classes=2, 
    n_clusters_per_class=1, 
    n_redundant=0, 
    random_state=42
)
# Create linear regression dataset
X_reg, y_reg = make_regression(
    n_samples=1000, 
    n_features=3, 
    n_targets=1, 
    noise=0.1, 
    random_state=42
)
# Create non-linear regression dataset
np.random.seed(42)
n_samples = 1000
X_reg_non = np.random.uniform(-3, 3, (n_samples, 3))
# Non-linear target: combination of sin, cos, and polynomial terms
y_reg_non = (
    10 * np.sin(X_reg_non[:, 0])
    + 5 * np.cos(X_reg_non[:, 1])
    + 0.5 * (X_reg_non[:, 2] ** 3)
    + np.random.normal(scale=2, size=n_samples)
)
# Split the data
X_class_train, X_class_test, y_class_train, y_class_test = train_test_split(
    X_class, y_class, test_size=0.2, random_state=42
)
X_reg_train, X_reg_test, y_reg_train, y_reg_test = train_test_split(
    X_reg, y_reg, test_size=0.2, random_state=42
)
X_reg_non_train, X_reg_non_test, y_reg_non_train, y_reg_non_test = train_test_split(
    X_reg_non, y_reg_non, test_size=0.2, random_state=42
)
print(f"Classification dataset shape: {X_class.shape}")
print(f"Linear Regression dataset shape: {X_reg.shape}")
print(f"Non-linear Regression dataset shape: {X_reg_non.shape}")
```

Let's plot the generated datasets to identify how they behave.

```python
# Plot the three datasets
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
# Classification dataset (first two features, colored by class)
axes[0].scatter(X_class[:, 0], X_class[:, 1], c=y_class, cmap='viridis', alpha=0.7)
axes[0].set_title('Classification Dataset')
axes[0].set_xlabel('Feature 1')
axes[0].set_ylabel('Feature 2')
# Linear regression dataset (first feature vs target)
axes[1].scatter(X_reg[:, 0], y_reg, alpha=0.7)
axes[1].set_title('Linear Regression Dataset')
axes[1].set_xlabel('Feature 1')
axes[1].set_ylabel('Target')
# Non-linear regression dataset (first feature vs target)
axes[2].scatter(X_reg_non[:, 0], y_reg_non, alpha=0.7)
axes[2].set_title('Non-linear Regression Dataset')
axes[2].set_xlabel('Feature 1')
axes[2].set_ylabel('Target')
plt.tight_layout()
plt.show()
```

Now, let's implement activation functions and their derivatives:

```python
def sigmoid(x):
    """Sigmoid activation function"""
    return 1 / (1 + np.exp(-np.clip(x, -500, 500)))
def sigmoid_derivative(x):
    """Derivative of sigmoid function"""
    s = sigmoid(x)
    return s * (1 - s)
def relu(x):
    """ReLU activation function"""
    return np.maximum(0, x)
def relu_derivative(x):
    """Derivative of ReLU function"""
    return np.where(x > 0, 1, 0)
def tanh(x):
    """Hyperbolic tangent activation function"""
    return np.tanh(x)
def tanh_derivative(x):
    """Derivative of tanh function"""
    return 1 - np.tanh(x)**2
```

Let's visualize these activation functions:

```python
# Plot activation functions
x = np.linspace(-5, 5, 1000)
fig, axes = plt.subplots(2, 3, figsize=(15, 10))
# Sigmoid
axes[0, 0].plot(x, sigmoid(x))
axes[0, 0].set_title('Sigmoid Function')
axes[0, 0].grid(True)
axes[1, 0].plot(x, sigmoid_derivative(x))
axes[1, 0].set_title('Sigmoid Derivative')
axes[1, 0].grid(True)
# ReLU
axes[0, 1].plot(x, relu(x))
axes[0, 1].set_title('ReLU Function')
axes[0, 1].grid(True)
axes[1, 1].plot(x, relu_derivative(x))
axes[1, 1].set_title('ReLU Derivative')
axes[1, 1].grid(True)
# Tanh
axes[0, 2].plot(x, tanh(x))
axes[0, 2].set_title('Tanh Function')
axes[0, 2].grid(True)
axes[1, 2].plot(x, tanh_derivative(x))
axes[1, 2].set_title('Tanh Derivative')
axes[1, 2].grid(True)
plt.tight_layout()
plt.show()
```

Now, let's implement our neural network class from scratch:

```python
class NeuralNetwork:
    def __init__(self, task, layers, activation='sigmoid', learning_rate=0.1):
        """
        Initialize neural network
        layers: list of integers representing the number of neurons in each layer
        activation: activation function ('sigmoid', 'relu', 'tanh')
        learning_rate: learning rate for gradient descent
        """
        self.task = task
        self.layers = layers
        self.learning_rate = learning_rate
        self.activation = activation
        # Set activation function
        if activation == 'sigmoid':
            self.activation_func = sigmoid
            self.activation_derivative = sigmoid_derivative
        elif activation == 'relu':
            self.activation_func = relu
            self.activation_derivative = relu_derivative
        elif activation == 'tanh':
            self.activation_func = tanh
            self.activation_derivative = tanh_derivative    
        # Initialize weights and biases
        self.weights = []
        self.biases = []
        self.initialize_parameters()
        # Training history
        self.loss_history = []
    def initialize_parameters(self):
        """Initialize weights and biases using Xavier/Glorot initialization"""
        for i in range(len(self.layers) - 1):
            # Xavier/Glorot initialization
            std = np.sqrt(2.0 / (self.layers[i] + self.layers[i + 1]))
            w = np.random.normal(0, std, (self.layers[i + 1], self.layers[i]))
            b = np.zeros((self.layers[i + 1], 1))
            self.weights.append(w)
            self.biases.append(b)
    def forward_propagation(self, X):
        """Forward propagation through the network"""
        self.activations = [X]
        self.z_values = []
        for i in range(len(self.weights)):
            z = np.dot(self.weights[i], self.activations[-1]) + self.biases[i]
            self.z_values.append(z)
            if i == len(self.weights) - 1:
                # Output layer
                if self.task == 'classification':
                    a = sigmoid(z)
                else:  # regression
                    a = z  # linear activation
            else:
                a = self.activation_func(z)
            self.activations.append(a)
        return self.activations[-1]
    def backward_propagation(self, X, y):
        """Backward propagation to compute gradients"""
        m = X.shape[1]
        # Initialize gradients
        dW = [np.zeros_like(w) for w in self.weights]
        db = [np.zeros_like(b) for b in self.biases]
        # Compute error at output layer
        delta = self.activations[-1] - y
        # Backpropagate through layers
        for i in range(len(self.weights) - 1, -1, -1):
            # Compute gradients for current layer
            dW[i] = np.dot(delta, self.activations[i].T) / m
            db[i] = np.sum(delta, axis=1, keepdims=True) / m
            # Compute error for previous layer (if not input layer)
            if i > 0:
                delta = np.dot(self.weights[i].T, delta) * self.activation_derivative(self.z_values[i - 1])
        return dW, db
    def update_parameters(self, dW, db):
        """Update weights and biases using gradient descent"""
        for i in range(len(self.weights)):
            self.weights[i] -= self.learning_rate * dW[i]
            self.biases[i] -= self.learning_rate * db[i]
    def compute_loss(self, y_true, y_pred, loss_type='binary_crossentropy'):
        """Compute loss function"""
        if loss_type == 'binary_crossentropy':
            # Add small epsilon to avoid log(0)
            epsilon = 1e-15
            y_pred = np.clip(y_pred, epsilon, 1 - epsilon)
            loss = -np.mean(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred))
        elif loss_type == 'mse':
            loss = np.mean((y_true - y_pred) ** 2)
        return loss
    def fit(self, X, y, epochs=1000, batch_size=32, verbose=True):
        """Train the neural network"""
        n_samples = X.shape[1]
        loss_type = 'mse' if self.task == 'regression' else 'binary_crossentropy'
        for epoch in range(epochs):
            # Shuffle data
            indices = np.random.permutation(n_samples)
            X_shuffled = X[:, indices]
            y_shuffled = y[:, indices]
            epoch_loss = 0
            # Mini-batch training
            for i in range(0, n_samples, batch_size):
                batch_end = min(i + batch_size, n_samples)
                X_batch = X_shuffled[:, i:batch_end]
                y_batch = y_shuffled[:, i:batch_end]
                # Forward pass
                y_pred = self.forward_propagation(X_batch)
                # Compute loss
                batch_loss = self.compute_loss(y_batch, y_pred, loss_type)
                epoch_loss += batch_loss
                # Backward pass
                dW, db = self.backward_propagation(X_batch, y_batch)
                # Update parameters
                self.update_parameters(dW, db)
            # Record average loss for the epoch
            avg_loss = epoch_loss / (n_samples // batch_size + 1)
            self.loss_history.append(avg_loss)
            if verbose and epoch % 100 == 0:
                print(f"Epoch {epoch}, Loss: {avg_loss:.4f}")
    def predict(self, X):
        """Make predictions"""
        return self.forward_propagation(X)
```

Let's test our neural network on the classification problem:

```python
# Prepare data for neural network (transpose for our implementation)
X_class_train_nn = X_class_train.T
X_class_test_nn = X_class_test.T
y_class_train_nn = y_class_train.reshape(1, -1)
y_class_test_nn = y_class_test.reshape(1, -1)
# Create and train neural network
nn_classifier = NeuralNetwork('classification', layers=[2, 4, 1], activation='sigmoid', learning_rate=0.1)
nn_classifier.fit(X_class_train_nn, y_class_train_nn, epochs=1000, batch_size=32)
# Plot training loss
plt.figure(figsize=(10, 6))
plt.plot(nn_classifier.loss_history)
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('Training Loss Over Time')
plt.grid(True)
plt.show()
# Make predictions
y_pred_proba = nn_classifier.predict(X_class_test_nn)
y_pred_class = (y_pred_proba > 0.5).astype(int)
# Evaluate performance
accuracy = accuracy_score(y_class_test, y_pred_class.flatten())
print(f"Classification Accuracy: {accuracy:.4f}")
```

Let's visualize the decision boundary:

```python
def plot_decision_boundary(X, y, model, title):
    """Plot decision boundary for 2D classification"""
    h = 0.02
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
    # Make predictions
    Z = model.predict(np.c_[xx.ravel(), yy.ravel()].T)
    Z = Z.reshape(xx.shape)
    plt.figure(figsize=(10, 8))
    plt.contourf(xx, yy, Z, alpha=0.4)
    plt.scatter(X[:, 0], X[:, 1], c=y, alpha=0.8)
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.title(title)
    plt.show()
plot_decision_boundary(X_class_test, y_class_test, nn_classifier, 'Neural Network Decision Boundary')
```

The shape of the boundary (curved, not straight) shows that the neural network has learned a non-linear separation between the classes, which is something simple linear models (like logistic regression) cannot do. The fit: If most points of each color are on the correct side of the boundary, your model is performing well. Misclassifications: Any points on the wrong side of the boundary are errors.

Now let's test on the regression problem:

```python
# Prepare regression data
X_reg_train_nn = X_reg_train.T
X_reg_test_nn = X_reg_test.T
y_reg_train_nn = y_reg_train.reshape(1, -1)
y_reg_test_nn = y_reg_test.reshape(1, -1)
# Create and train neural network for regression
nn_regressor = NeuralNetwork('regression', layers=[3, 5, 1], activation='relu', learning_rate=0.01)
nn_regressor.fit(X_reg_train_nn, y_reg_train_nn, epochs=1000, batch_size=32)
# Plot training loss
plt.figure(figsize=(10, 6))
plt.plot(nn_regressor.loss_history)
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('Training Loss Over Time (Regression)')
plt.grid(True)
plt.show()
# Make predictions
y_pred_reg = nn_regressor.predict(X_reg_test_nn)
# Evaluate performance
mse = mean_squared_error(y_reg_test, y_pred_reg.flatten())
print(f"Regression MSE: {mse:.4f}")
# Plot predictions vs actual
plt.figure(figsize=(10, 6))
plt.scatter(y_reg_test, y_pred_reg.flatten(), alpha=0.6)
plt.plot([y_reg_test.min(), y_reg_test.max()], [y_reg_test.min(), y_reg_test.max()], 'r--', lw=2)
plt.xlabel('Actual Values')
plt.ylabel('Predicted Values')
plt.title('Neural Network Regression: Predictions vs Actual')
plt.grid(True)
plt.show()
```

Let's plot how the original dataset compares to the model predictions.

```python
# Plot: Feature 1 vs Actual and Predicted (Linear Regression)
plt.figure(figsize=(10, 6))
plt.scatter(X_reg_test[:, 0], y_reg_test, label='Actual', alpha=0.6)
plt.scatter(X_reg_test[:, 0], y_pred_reg.flatten(), label='Predicted', alpha=0.6)
plt.xlabel('Feature 1')
plt.ylabel('Target')
plt.title('Linear Regression: Actual vs Predicted (Feature 1)')
plt.legend()
plt.grid(True)
plt.show()
```

Let's test with our non-linear regression problem.

```python
# Prepare non regression data
X_reg_train_nn = X_reg_non_train.T
X_reg_test_nn = X_reg_non_test.T
y_reg_train_nn = y_reg_non_train.reshape(1, -1)
y_reg_test_nn = y_reg_non_test.reshape(1, -1)
# Create and train neural network for regression
nn_regressor = NeuralNetwork('regression', layers=[3, 5, 1], activation='relu', learning_rate=0.01)
nn_regressor.fit(X_reg_train_nn, y_reg_train_nn, epochs=1000, batch_size=32)
# Plot training loss
plt.figure(figsize=(10, 6))
plt.plot(nn_regressor.loss_history)
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('Training Loss Over Time (Regression)')
plt.grid(True)
plt.show()
# Make predictions
y_pred_reg = nn_regressor.predict(X_reg_test_nn)
# Evaluate performance
mse = mean_squared_error(y_reg_non_test, y_pred_reg.flatten())
print(f"Regression MSE: {mse:.4f}")
# Plot predictions vs actual
plt.figure(figsize=(10, 6))
plt.scatter(y_reg_non_test, y_pred_reg.flatten(), alpha=0.6)
plt.plot([y_reg_non_test.min(), y_reg_non_test.max()], [y_reg_non_test.min(), y_reg_non_test.max()], 'r--', lw=2)
plt.xlabel('Actual Values')
plt.ylabel('Predicted Values')
plt.title('Neural Network Regression: Predictions vs Actual')
plt.grid(True)
plt.show()
```

Let's plot how the original dataset compares to the model predictions.

```python
# Plot: Feature 1 vs Actual and Predicted (Non-linear Regression)
plt.figure(figsize=(10, 6))
plt.scatter(X_reg_non_test[:, 0], y_reg_non_test, label='Actual', alpha=0.6)
plt.scatter(X_reg_non_test[:, 0], y_pred_reg.flatten(), label='Predicted', alpha=0.6)
plt.xlabel('Feature 1')
plt.ylabel('Target')
plt.title('Non-linear Regression: Actual vs Predicted (Feature 1)')
plt.legend()
plt.grid(True)
plt.show()
```

---

## Exercise 3: Modern Deep Learning with TensorFlow/Keras

In this exercise, we'll explore modern deep learning techniques using TensorFlow/Keras, including batch normalization, dropout, and modern optimizers.

```python
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.optimizers import Adam, SGD
from tensorflow.keras.callbacks import EarlyStopping
# Set random seeds for reproducibility
tf.random.set_seed(42)
np.random.seed(42)
print(f"TensorFlow version: {tf.__version__}")
```

Let's create a modern deep neural network with advanced techniques:

```python
def create_modern_nn(input_shape, num_classes=1, use_batch_norm=True, use_dropout=True):
    """Create a modern neural network with batch normalization and dropout"""
    model = keras.Sequential()
    # Input layer
    model.add(layers.Dense(64, input_shape=input_shape, activation='relu'))
    if use_batch_norm:
        model.add(layers.BatchNormalization())
    if use_dropout:
        model.add(layers.Dropout(0.3))
    # Hidden layers
    model.add(layers.Dense(128, activation='relu'))
    if use_batch_norm:
        model.add(layers.BatchNormalization())
    if use_dropout:
        model.add(layers.Dropout(0.3))
    model.add(layers.Dense(64, activation='relu'))
    if use_batch_norm:
        model.add(layers.BatchNormalization())
    if use_dropout:
        model.add(layers.Dropout(0.3))
    # Output layer
    if num_classes == 1:
        model.add(layers.Dense(1, activation='sigmoid'))
    else:
        model.add(layers.Dense(num_classes, activation='softmax'))
    return model
```

Now we can create models with different configurations

```python
models_configs = {
    'Basic': create_modern_nn((2,), use_batch_norm=False, use_dropout=False),
    'With BatchNorm': create_modern_nn((2,), use_batch_norm=True, use_dropout=False),
    'With Dropout': create_modern_nn((2,), use_batch_norm=False, use_dropout=True),
    'Modern': create_modern_nn((2,), use_batch_norm=True, use_dropout=True)
}
# Compile and train models
history_dict = {}
for name, model in models_configs.items():
    print(f"\nTraining {name} model...")
    # Compile model
    model.compile(
        optimizer=Adam(learning_rate=0.001),
        loss='binary_crossentropy',
        metrics=['accuracy']
    )
    # Early stopping callback
    early_stopping = EarlyStopping(
        monitor='val_loss',
        patience=50,
        restore_best_weights=True
    )
    # Train model
    history = model.fit(
        X_class_train, y_class_train,
        validation_split=0.2,
        epochs=500,
        batch_size=32,
        callbacks=[early_stopping],
        verbose=0
    )
    history_dict[name] = history.history
    # Evaluate model
    test_loss, test_accuracy = model.evaluate(X_class_test, y_class_test, verbose=0)
    print(f"{name} - Test Accuracy: {test_accuracy:.4f}")
# Plot training history comparison
fig, axes = plt.subplots(2, 2, figsize=(15, 10))
# Training accuracy
axes[0, 0].set_title('Training Accuracy')
for name, history in history_dict.items():
    axes[0, 0].plot(history['accuracy'], label=name)
axes[0, 0].set_ylabel('Accuracy')
axes[0, 0].legend()
axes[0, 0].grid(True)
# Validation accuracy
axes[0, 1].set_title('Validation Accuracy')
for name, history in history_dict.items():
    axes[0, 1].plot(history['val_accuracy'], label=name)
axes[0, 1].set_ylabel('Accuracy')
axes[0, 1].legend()
axes[0, 1].grid(True)
# Training loss
axes[1, 0].set_title('Training Loss')
for name, history in history_dict.items():
    axes[1, 0].plot(history['loss'], label=name)
axes[1, 0].set_ylabel('Loss')
axes[1, 0].set_xlabel('Epoch')
axes[1, 0].legend()
axes[1, 0].grid(True)
# Validation loss
axes[1, 1].set_title('Validation Loss')
for name, history in history_dict.items():
    axes[1, 1].plot(history['val_loss'], label=name)
axes[1, 1].set_ylabel('Loss')
axes[1, 1].set_xlabel('Epoch')
axes[1, 1].legend()
axes[1, 1].grid(True)
plt.tight_layout()
plt.show()
```

Let's also explore different optimizers:

```python
# Compare different optimizers
optimizers = {
    'SGD': SGD(learning_rate=0.01),
    'Adam': Adam(learning_rate=0.001),
    'Adam (high lr)': Adam(learning_rate=0.01)
}
optimizer_results = {}
for opt_name, optimizer in optimizers.items():
    print(f"\nTraining with {opt_name} optimizer...")
    # Create model
    model = create_modern_nn((2,), use_batch_norm=True, use_dropout=True)
    # Compile model
    model.compile(
        optimizer=optimizer,
        loss='binary_crossentropy',
        metrics=['accuracy']
    )
    # Train model
    history = model.fit(
        X_class_train, y_class_train,
        validation_split=0.2,
        epochs=200,
        batch_size=32,
        verbose=0
    )
    optimizer_results[opt_name] = history.history
    # Evaluate model
    test_loss, test_accuracy = model.evaluate(X_class_test, y_class_test, verbose=0)
    print(f"{opt_name} - Test Accuracy: {test_accuracy:.4f}")
# Plot optimizer comparison
plt.figure(figsize=(15, 5))
plt.subplot(1, 3, 1)
for opt_name, history in optimizer_results.items():
    plt.plot(history['accuracy'], label=opt_name)
plt.title('Training Accuracy')
plt.ylabel('Accuracy')
plt.legend()
plt.grid(True)
plt.subplot(1, 3, 2)
for opt_name, history in optimizer_results.items():
    plt.plot(history['val_accuracy'], label=opt_name)
plt.title('Validation Accuracy')
plt.ylabel('Accuracy')
plt.legend()
plt.grid(True)
plt.subplot(1, 3, 3)
for opt_name, history in optimizer_results.items():
    plt.plot(history['loss'], label=opt_name)
plt.title('Training Loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
```

---

## Homework - Neural Network Architecture Design

The homework assignment focuses on designing and implementing neural network architectures for different types of problems. You will apply the concepts learned in this practical session to create effective neural network solutions. You are free to select the dataset of your preference and develop a full pipeline that will end with a trained neural network model at the end. You can use the implementation of this notebook or the libraries we also show. Your pipeline should include data exploration, preprocessing, and feature engineering. Neural network architecture design, hyperparameter optimisation, and model selection, and a final performance analysis. Please provide a description of each step in your pipeline.

<DESCRIBE YOUR SOLUTION HERE>

```python
# Write your implementation here
```

### Submission Guidelines

- Submit your solution as a Jupyter notebook with the following name format: `neural_networks_session_7_<email_username>.ipynb`
- Include clear comments explaining your code and design decisions
- Provide comprehensive analysis of your results
- Document any challenges faced and how you overcame them
- Include visualizations of your results and model performance
- Due date: 03/07/2025

<!-- end NOTEBOOK: -->