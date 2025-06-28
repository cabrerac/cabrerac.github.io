<!-- NOTEBOOK: -->

# Practical Introduction

In this practical session, we will implement neural networks from scratch and explore deep learning concepts. We'll build multi-layer perceptrons, implement backpropagation, and compare with modern deep learning frameworks.

---

## Exercise 1: Implementing Neural Networks from Scratch

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
# Create regression dataset
X_reg, y_reg = make_regression(
    n_samples=1000, 
    n_features=3, 
    n_targets=1, 
    noise=0.1, 
    random_state=42
)
# Split the data
X_class_train, X_class_test, y_class_train, y_class_test = train_test_split(
    X_class, y_class, test_size=0.2, random_state=42
)
X_reg_train, X_reg_test, y_reg_train, y_reg_test = train_test_split(
    X_reg, y_reg, test_size=0.2, random_state=42
)
print(f"Classification dataset shape: {X_class.shape}")
print(f"Regression dataset shape: {X_reg.shape}")
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
                batch_loss = self.compute_loss(y_batch, y_pred)
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

---

## Exercise 2: Vanishing Gradients and Modern Activation Functions

In this exercise, we'll explore the vanishing gradient problem and how modern activation functions help address it. We'll compare different activation functions and their impact on training deep networks.

Let's create a deeper network to demonstrate the vanishing gradient problem:

```python
class DeepNeuralNetwork:
    def __init__(self, layers, activation='sigmoid', learning_rate=0.1):
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
        self.gradient_norms = []
    def initialize_parameters(self):
        """Initialize weights and biases"""
        for i in range(len(self.layers) - 1):
            if self.activation == 'relu':
                # He initialization for ReLU
                std = np.sqrt(2.0 / self.layers[i])
            else:
                # Xavier/Glorot initialization for sigmoid/tanh
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
                a = sigmoid(z)  # Output layer
            else:
                a = self.activation_func(z)
            self.activations.append(a)
        return self.activations[-1]
    def backward_propagation(self, X, y):
        """Backward propagation with gradient tracking"""
        m = X.shape[1]
        dW = [np.zeros_like(w) for w in self.weights]
        db = [np.zeros_like(b) for b in self.biases]
        # Compute error at output layer
        delta = self.activations[-1] - y
        # Track gradient norms
        gradient_norms = []
        # Backpropagate through layers
        for i in range(len(self.weights) - 1, -1, -1):
            # Compute gradients for current layer
            dW[i] = np.dot(delta, self.activations[i].T) / m
            db[i] = np.sum(delta, axis=1, keepdims=True) / m
            # Track gradient norm
            layer_grad_norm = np.linalg.norm(dW[i])
            gradient_norms.append(layer_grad_norm)
            # Compute error for previous layer (if not input layer)
            if i > 0:
                delta = np.dot(self.weights[i].T, delta) * self.activation_derivative(self.z_values[i - 1])
        self.gradient_norms.append(gradient_norms[::-1])  # Reverse to match layer order
        return dW, db
    def update_parameters(self, dW, db):
        """Update weights and biases"""
        for i in range(len(self.weights)):
            self.weights[i] -= self.learning_rate * dW[i]
            self.biases[i] -= self.learning_rate * db[i]
    def compute_loss(self, y_true, y_pred):
        """Compute binary cross-entropy loss"""
        epsilon = 1e-15
        y_pred = np.clip(y_pred, epsilon, 1 - epsilon)
        loss = -np.mean(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred))
        return loss
    def fit(self, X, y, epochs=1000, batch_size=32):
        """Train the deep neural network"""
        n_samples = X.shape[1]
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
                batch_loss = self.compute_loss(y_batch, y_pred)
                epoch_loss += batch_loss
                # Backward pass
                dW, db = self.backward_propagation(X_batch, y_batch)
                # Update parameters
                self.update_parameters(dW, db)
            # Record average loss for the epoch
            avg_loss = epoch_loss / (n_samples // batch_size + 1)
            self.loss_history.append(avg_loss)
            if epoch % 100 == 0:
                print(f"Epoch {epoch}, Loss: {avg_loss:.4f}")
    def predict(self, X):
        """Make predictions"""
        return self.forward_propagation(X)
```

Now let's compare different activation functions on a deep network:

```python
# Create a deeper network architecture
deep_layers = [2, 10, 10, 10, 1]
# Test different activation functions
activations = ['sigmoid', 'tanh', 'relu']
models = {}
for activation in activations:
    print(f"\nTraining network with {activation} activation...")
    model = DeepNeuralNetwork(deep_layers, activation=activation, learning_rate=0.1)
    model.fit(X_class_train_nn, y_class_train_nn, epochs=500, batch_size=32)
    models[activation] = model
# Plot training loss comparison
plt.figure(figsize=(15, 5))
plt.subplot(1, 3, 1)
for activation in activations:
    plt.plot(models[activation].loss_history, label=activation)
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('Training Loss Comparison')
plt.legend()
plt.grid(True)
# Plot gradient norms for the first layer
plt.subplot(1, 3, 2)
for activation in activations:
    first_layer_grads = [grads[0] for grads in models[activation].gradient_norms]
    plt.plot(first_layer_grads, label=activation)
plt.xlabel('Epoch')
plt.ylabel('Gradient Norm (Layer 1)')
plt.title('Gradient Norms Comparison')
plt.legend()
plt.grid(True)
# Plot gradient norms for the last layer
plt.subplot(1, 3, 3)
for activation in activations:
    last_layer_grads = [grads[-1] for grads in models[activation].gradient_norms]
    plt.plot(last_layer_grads, label=activation)
plt.xlabel('Epoch')
plt.ylabel('Gradient Norm (Last Layer)')
plt.title('Gradient Norms Comparison')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
# Compare final performance
print("\nFinal Performance Comparison:")
for activation in activations:
    y_pred = models[activation].predict(X_class_test_nn)
    y_pred_class = (y_pred > 0.5).astype(int)
    accuracy = accuracy_score(y_class_test, y_pred_class.flatten())
    print(f"{activation.capitalize()}: Accuracy = {accuracy:.4f}")
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

# Create models with different configurations
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

## Exercise 4: Transfer Learning and Pre-trained Models

In this exercise, we'll explore transfer learning using pre-trained models. We'll use a pre-trained model and fine-tune it for our classification task.

```python
# For this exercise, we'll simulate transfer learning by creating a "pre-trained" model
# In practice, you would use models like VGG16, ResNet, etc. from keras.applications
def create_pretrained_model(input_shape):
    """Create a model that simulates a pre-trained feature extractor"""
    base_model = keras.Sequential([
        layers.Dense(128, input_shape=input_shape, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.3),
        layers.Dense(64, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.3),
    ])
    return base_model
# Create pre-trained model
pretrained_model = create_pretrained_model((2,))
# Freeze the pre-trained layers
pretrained_model.trainable = False
# Create new model with pre-trained features
transfer_model = keras.Sequential([
    pretrained_model,
    layers.Dense(32, activation='relu'),
    layers.Dropout(0.2),
    layers.Dense(1, activation='sigmoid')
])
# Compile the transfer model
transfer_model.compile(
    optimizer=Adam(learning_rate=0.001),
    loss='binary_crossentropy',
    metrics=['accuracy']
)
print("Transfer model summary:")
transfer_model.summary()
# Train the transfer model
print("\nTraining transfer model...")
transfer_history = transfer_model.fit(
    X_class_train, y_class_train,
    validation_split=0.2,
    epochs=100,
    batch_size=32,
    verbose=0
)
# Fine-tuning: Unfreeze some layers and train with lower learning rate
print("\nFine-tuning the model...")
pretrained_model.trainable = True
# Freeze early layers, keep later layers trainable
for layer in pretrained_model.layers[:-2]:  # Freeze first layers
    layer.trainable = False
# Recompile with lower learning rate
transfer_model.compile(
    optimizer=Adam(learning_rate=0.0001),  # Lower learning rate for fine-tuning
    loss='binary_crossentropy',
    metrics=['accuracy']
)
# Continue training
fine_tune_history = transfer_model.fit(
    X_class_train, y_class_train,
    validation_split=0.2,
    epochs=50,
    batch_size=32,
    verbose=0
)
# Evaluate final model
test_loss, test_accuracy = transfer_model.evaluate(X_class_test, y_class_test, verbose=0)
print(f"Final Transfer Learning Accuracy: {test_accuracy:.4f}")
# Plot transfer learning results
plt.figure(figsize=(15, 5))
plt.subplot(1, 3, 1)
plt.plot(transfer_history.history['accuracy'], label='Transfer Learning')
plt.plot(range(len(transfer_history.history['accuracy']), 
               len(transfer_history.history['accuracy']) + len(fine_tune_history.history['accuracy'])), 
         fine_tune_history.history['accuracy'], label='Fine-tuning')
plt.title('Training Accuracy')
plt.ylabel('Accuracy')
plt.legend()
plt.grid(True)
plt.subplot(1, 3, 2)
plt.plot(transfer_history.history['val_accuracy'], label='Transfer Learning')
plt.plot(range(len(transfer_history.history['val_accuracy']), 
               len(transfer_history.history['val_accuracy']) + len(fine_tune_history.history['val_accuracy'])), 
         fine_tune_history.history['val_accuracy'], label='Fine-tuning')
plt.title('Validation Accuracy')
plt.ylabel('Accuracy')
plt.legend()
plt.grid(True)
plt.subplot(1, 3, 3)
plt.plot(transfer_history.history['loss'], label='Transfer Learning')
plt.plot(range(len(transfer_history.history['loss']), 
               len(transfer_history.history['loss']) + len(fine_tune_history.history['loss'])), 
         fine_tune_history.history['loss'], label='Fine-tuning')
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

The homework assignment focuses on designing and implementing neural network architectures for different types of problems. You will apply the concepts learned in this practical session to create effective neural network solutions.

Your task is to:

1. **Dataset Selection**: Choose a dataset that interests you (classification or regression). You can use:
   - UCI Machine Learning Repository datasets
   - Kaggle datasets
   - Scikit-learn built-in datasets
   - Or create your own synthetic dataset

2. **Architecture Design**: Design and implement multiple neural network architectures:
   - A shallow network (1-2 hidden layers)
   - A deep network (3+ hidden layers)
   - A network with different activation functions
   - A network with modern techniques (batch normalization, dropout)

3. **Hyperparameter Optimization**: Use techniques like:
   - Grid search or random search for hyperparameters
   - Cross-validation for model selection
   - Learning rate scheduling
   - Early stopping

4. **Performance Analysis**: Compare your models using:
   - Training and validation curves
   - Confusion matrices (for classification)
   - Regression metrics (for regression)
   - Model complexity analysis

5. **Discussion**: Analyze your results and discuss:
   - Which architecture performed best and why
   - The impact of different activation functions
   - The effectiveness of regularization techniques
   - Potential improvements and next steps

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