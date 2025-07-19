<!-- NOTEBOOK: -->

# Practical Introduction

In this practical session, we will explore ML model deployment concepts and tools using the actual neural network implementations from our students. We'll deploy three different approaches: from-scratch implementations, comprehensive multi-architecture networks, and modern deep learning frameworks.

---

## Exercise 1: Deploying From-Scratch Neural Network

In this exercise, we'll deploy Juan Carlos Mejia's complete neural network implementation from scratch using Flask. This demonstrates how to deploy custom neural network implementations in production.

Let's start by importing the necessary libraries:

```python
import pickle
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify
from sklearn.datasets import make_classification, make_regression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_squared_error
import joblib
import os
import matplotlib.pyplot as plt
```

And now, we should continue with the activation functions of the neural network:

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
```

And the Neural Network implementation:

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
        
        # Initialize weights and biases
        self.weights = []
        self.biases = []
        self.initialize_parameters()
        self.loss_history = []
    
    def initialize_parameters(self):
        """Initialize weights and biases using Xavier/Glorot initialization"""
        for i in range(len(self.layers) - 1):
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

Now let's create datasets and train the models:

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
# Train the neural network for classification
print("Training the Neural Network for Classification...")
X_class_train_nn = X_class_train.T
X_class_test_nn = X_class_test.T
y_class_train_nn = y_class_train.reshape(1, -1)
y_class_test_nn = y_class_test.reshape(1, -1)
classifier = NeuralNetwork('classification', layers=[2, 4, 1], activation='sigmoid', learning_rate=0.1)
classifier.fit(X_class_train_nn, y_class_train_nn, epochs=500, batch_size=32, verbose=True)
# Train the neural network for regression
print("\nTraining the Neural Network for Regression...")
X_reg_train_nn = X_reg_train.T
X_reg_test_nn = X_reg_test.T
y_reg_train_nn = y_reg_train.reshape(1, -1)
y_reg_test_nn = y_reg_test.reshape(1, -1)
regressor = NeuralNetwork('regression', layers=[3, 5, 1], activation='relu', learning_rate=0.01)
regressor.fit(X_reg_train_nn, y_reg_train_nn, epochs=500, batch_size=32, verbose=True)
# Evaluate the models
y_pred_class = classifier.predict(X_class_test_nn)
y_pred_class_binary = (y_pred_class > 0.5).astype(int)
class_accuracy = accuracy_score(y_class_test, y_pred_class_binary.flatten())
y_pred_reg = regressor.predict(X_reg_test_nn)
reg_mse = mean_squared_error(y_reg_test, y_pred_reg.flatten())
print(f"\nModels Performance:")
print(f"Classification Accuracy: {class_accuracy:.4f}")
print(f"Regression MSE: {reg_mse:.4f}")
# Saving the models
models = {
    'classifier': classifier,
    'regressor': regressor
}
joblib.dump(models, 'models.pkl')
print("Models saved to models.pkl")
```

Now let's create a Flask application to serve the models:

```python
app = Flask(__name__)
# Global variables to store models
models = None
@app.before_first_request
def load_models():
    global jc_models
    jc_models = joblib.load('models.pkl')
    print("Models loaded successfully!")
@app.route('/predict/classification', methods=['POST'])
def predict_classification():
    """Endpoint for the neural network classification model"""
    try:
        data = request.get_json()
        if not data or 'features' not in data:
            return jsonify({'error': 'No features provided'}), 400
        features = np.array(data['features']).reshape(1, -1)
        features_nn = features.T
        prediction_proba = models['classifier'].predict(features_nn)[0, 0]
        prediction = 1 if prediction_proba > 0.5 else 0
        return jsonify({
            'prediction': int(prediction),
            'probability': float(prediction_proba),
            'model_type': 'neural_network',
            'architecture': '2-4-1',
            'activation': 'sigmoid',
            'status': 'success'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@app.route('/predict/regression', methods=['POST'])
def predict_regression():
    """Endpoint for neural network regression model"""
    try:
        data = request.get_json()
        if not data or 'features' not in data:
            return jsonify({'error': 'No features provided'}), 400
        features = np.array(data['features']).reshape(1, -1)
        features_nn = features.T
        prediction = models['regressor'].predict(features_nn)[0, 0]
        return jsonify({
            'prediction': float(prediction),
            'model_type': 'neural_network',
            'architecture': '3-5-1',
            'activation': 'relu',
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@app.route('/models', methods=['GET'])
def list_models():
    """List models and their information"""
    model_info = {
        'classifier': {
            'type': 'classification',
            'architecture': '2-4-1',
            'activation': 'sigmoid',
            'task': 'binary classification',
            'implementation': 'from_scratch'
        },
        'regressor': {
            'type': 'regression',
            'architecture': '3-5-1',
            'activation': 'relu',
            'task': 'regression',
            'implementation': 'from_scratch'
        }
    }
    return jsonify(model_info)
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'models_loaded': jc_models is not None})
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

Let's create functions to test the model server:

```python
import requests
import json
def test_classification(features):
    """Test classification endpoint"""
    url = "http://localhost:5000/predict/classification"
    data = {"features": features}
    response = requests.post(url, json=data)
    return response.json()
def test_regression(features):
    """Test egression endpoint"""
    url = "http://localhost:5000/predict/regression"
    data = {"features": features}
    response = requests.post(url, json=data)
    return response.json()
```

And now we can run the tests:

```python
# Test classification
print("Testing Neural Network Classification:")
sample_class_features = X_class_test[0].tolist()
result_class = test_classification(sample_class_features)
print(json.dumps(result_class, indent=2))
# Test regression
print("\nTesting Neural Network Regression:")
sample_reg_features = X_reg_test[0].tolist()
result_reg = test_jc_regression(sample_reg_features)
print(json.dumps(result_reg, indent=2))
# Test model listing
print("\nAvailable Models:")
response = requests.get("http://localhost:5000/models")
models_info = response.json()
print(json.dumps(models_info, indent=2))
```

---

## Exercise 2: Deploying Multi-Architecture Neural Networks

In this exercise, we'll deploy Anyi Chavez's comprehensive neural network implementation that supports multiple architectures. This demonstrates how to deploy complex neural network systems with different configurations.

Let's implement the multi-architecture neural network with various architectures:

```python
# Multi-Architecture Neural Network Implementation
class MultiArchitectureNeuralNetwork:
    def __init__(self, task, layers, activation='sigmoid', learning_rate=0.1):
        """
        Initialize multi-architecture neural network
        layers: list of integers representing the number of neurons in each layer
        activation: activation function ('sigmoid', 'relu')
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
        
        # Initialize weights and biases
        self.weights = []
        self.biases = []
        self.initialize_parameters()
        self.loss_history = []
    
    def initialize_parameters(self):
        """Initialize weights and biases using Xavier/Glorot initialization"""
        for i in range(len(self.layers) - 1):
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

Now let's train the models with different architectures:

```python
# Train models with different architectures
print("Training Neural Networks with Multiple Architectures...")
# Classification model with complex architecture
input_size = X_class_train.shape[1]
classifier_complex = MultiArchitectureNeuralNetwork(
    'classification', 
    layers=[input_size, 10, 8, 6, 1], 
    activation='sigmoid', 
    learning_rate=0.1
)
classifier_complex.fit(X_class_train.T, y_class_train.reshape(1, -1), epochs=300, verbose=True)
# Simple classification model
classifier_simple = MultiArchitectureNeuralNetwork(
    'classification', 
    layers=[2, 6, 1], 
    activation='sigmoid', 
    learning_rate=0.1
)
classifier_simple.fit(X_class_train.T, y_class_train.reshape(1, -1), epochs=300, verbose=True)
# Regression model with complex architecture
regressor_complex = MultiArchitectureNeuralNetwork(
    'regression', 
    layers=[X_reg_train.shape[1], 16, 8, 1], 
    activation='relu', 
    learning_rate=0.01
)
regressor_complex.fit(X_reg_train.T, y_reg_train.reshape(1, -1), epochs=300, verbose=True)
# Simple regression model
regressor_simple = MultiArchitectureNeuralNetwork(
    'regression', 
    layers=[1, 5, 1], 
    activation='relu', 
    learning_rate=0.01
)
regressor_simple.fit(X_reg_train.T, y_reg_train.reshape(1, -1), epochs=300, verbose=True)
```

We can evaluate the models now:

```python
# Evaluate models
y_pred_class_complex = classifier_complex.predict(X_class_test.T)
y_pred_class_complex_binary = (y_pred_class_complex > 0.5).astype(int)
class_complex_accuracy = accuracy_score(y_class_test, y_pred_class_complex_binary.flatten())
y_pred_class_simple = classifier_simple.predict(X_class_test.T)
y_pred_class_simple_binary = (y_pred_class_simple > 0.5).astype(int)
class_simple_accuracy = accuracy_score(y_class_test, y_pred_class_simple_binary.flatten())
y_pred_reg_complex = regressor_complex.predict(X_reg_test.T)
reg_complex_mse = mean_squared_error(y_reg_test, y_pred_reg_complex.flatten())
y_pred_reg_simple = regressor_simple.predict(X_reg_test.T)
reg_simple_mse = mean_squared_error(y_reg_test, y_pred_reg_simple.flatten())
print(f"\nMulti-Architecture Model Performance:")
print(f"Complex Classifier Accuracy: {class_complex_accuracy:.4f}")
print(f"Simple Classifier Accuracy: {class_simple_accuracy:.4f}")
print(f"Complex Regressor MSE: {reg_complex_mse:.4f}")
print(f"Simple Regressor MSE: {reg_simple_mse:.4f}")
```

Once we are done, we can save the models

```python
# Save models
multi_arch_models = {
    'classifier_complex': classifier_complex,
    'classifier_simple': classifier_simple,
    'regressor_complex': regressor_complex,
    'regressor_simple': regressor_simple
}
joblib.dump(multi_arch_models, 'multi_architecture_models.pkl')
print("Multi-architecture models saved to multi_architecture_models.pkl")
```

Now let's create a Flask application to serve the multi-architecture models with architecture selection:

```python
app2 = Flask(__name__)
# Global variables to store multi-architecture models
multi_arch_models = None
@app2.before_first_request
def load_multi_arch_models():
    global multi_arch_models
    multi_arch_models = joblib.load('multi_architecture_models.pkl')
    print("Multi-architecture models loaded successfully!")
@app2.route('/predict/classification', methods=['POST'])
def predict_multi_arch_classification():
    """Endpoint for multi-architecture neural network classification with architecture selection"""
    try:
        data = request.get_json()
        if not data or 'features' not in data:
            return jsonify({'error': 'No features provided'}), 400
        
        architecture = data.get('architecture', 'complex')  # 'complex' or 'simple'
        features = np.array(data['features']).reshape(1, -1)
        features_nn = features.T
        
        if architecture == 'complex':
            model = multi_arch_models['classifier_complex']
            arch_info = 'input_size-10-8-6-1'
        else:
            model = multi_arch_models['classifier_simple']
            arch_info = '2-6-1'
        
        prediction_proba = model.predict(features_nn)[0, 0]
        prediction = 1 if prediction_proba > 0.5 else 0
        
        return jsonify({
            'prediction': int(prediction),
            'probability': float(prediction_proba),
            'model_type': 'multi_architecture_neural_network',
            'architecture': arch_info,
            'activation': 'sigmoid',
            'complexity': architecture,
            'status': 'success'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@app2.route('/predict/regression', methods=['POST'])
def predict_multi_arch_regression():
    """Endpoint for multi-architecture neural network regression with architecture selection"""
    try:
        data = request.get_json()
        if not data or 'features' not in data:
            return jsonify({'error': 'No features provided'}), 400
        
        architecture = data.get('architecture', 'complex')  # 'complex' or 'simple'
        features = np.array(data['features']).reshape(1, -1)
        features_nn = features.T
        
        if architecture == 'complex':
            model = multi_arch_models['regressor_complex']
            arch_info = 'input_size-16-8-1'
        else:
            model = multi_arch_models['regressor_simple']
            arch_info = '1-5-1'
        
        prediction = model.predict(features_nn)[0, 0]
        
        return jsonify({
            'prediction': float(prediction),
            'model_type': 'multi_architecture_neural_network',
            'architecture': arch_info,
            'activation': 'relu',
            'complexity': architecture,
            'status': 'success'
        })       
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@app2.route('/models', methods=['GET'])
def list_multi_arch_models():
    """List multi-architecture models and their information"""
    model_info = {
        'classifier_complex': {
            'type': 'classification',
            'architecture': 'input_size-10-8-6-1',
            'activation': 'sigmoid',
            'task': 'binary classification',
            'complexity': 'complex'
        },
        'classifier_simple': {
            'type': 'classification',
            'architecture': '2-6-1',
            'activation': 'sigmoid',
            'task': 'binary classification',
            'complexity': 'simple'
        },
        'regressor_complex': {
            'type': 'regression',
            'architecture': 'input_size-16-8-1',
            'activation': 'relu',
            'task': 'regression',
            'complexity': 'complex'
        },
        'regressor_simple': {
            'type': 'regression',
            'architecture': '1-5-1',
            'activation': 'relu',
            'task': 'regression',
            'complexity': 'simple'
        }
    }
    return jsonify(model_info)
@app2.route('/health', methods=['GET'])
def health_check_multi_arch():
    return jsonify({'status': 'healthy', 'models_loaded': multi_arch_models is not None})
if __name__ == '__main__':
    app2.run(debug=True, host='0.0.0.0', port=5001)
```

Let's test the multi-architecture model server creating a couple of functions for that:

```python
def test_multi_arch_classification(features, architecture='complex'):
    """Test multi-architecture classification endpoint"""
    url = "http://localhost:5001/predict/classification"
    data = {"features": features, "architecture": architecture}
    response = requests.post(url, json=data)
    return response.json()
def test_multi_arch_regression(features, architecture='complex'):
    """Test multi-architecture regression endpoint"""
    url = "http://localhost:5001/predict/regression"
    data = {"features": features, "architecture": architecture}
    response = requests.post(url, json=data)
    return response.json()
```

And now we can test the implementation:

```python
# Test complex classification
print("Testing Complex Neural Network Classification:")
result_class_complex = test_multi_arch_classification(sample_class_features, 'complex')
print(json.dumps(result_class_complex, indent=2))
# Test simple classification
print("\nTesting Simple Neural Network Classification:")
result_class_simple = test_multi_arch_classification(sample_class_features, 'simple')
print(json.dumps(result_class_simple, indent=2))
# Test complex regression
print("\nTesting Complex Neural Network Regression:")
result_reg_complex = test_multi_arch_regression(sample_reg_features, 'complex')
print(json.dumps(result_reg_complex, indent=2))
# Test simple regression
print("\nTesting Simple Neural Network Regression:")
result_reg_simple = test_multi_arch_regression(sample_reg_features, 'simple')
print(json.dumps(result_reg_simple, indent=2))
# Test model listing
print("\nAvailable Multi-Architecture Models:")
response = requests.get("http://localhost:5001/models")
models_info = response.json()
print(json.dumps(models_info, indent=2))
```

---

## Exercise 3: Deploying TensorFlow/Keras Computer Vision Model

In this exercise, we'll deploy Jorge Lopez's TensorFlow/Keras implementation for computer vision. This demonstrates how to deploy modern deep learning frameworks in production.

```python
import tensorflow as tf
from tensorflow.keras import models, layers
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import io
import base64
```

Let's implement the computer vision pipeline:

```python
# Computer Vision Model Implementation
class ComputerVisionModel:
    def __init__(self, image_size=256, num_classes=3):
        self.image_size = image_size
        self.num_classes = num_classes
        self.model = None
        self.class_names = ['Potato_Early_blight', 'Potato_healthy', 'Potato_Late_blight']
        self.build_model()
    
    def build_model(self):
        """Build CNN model for plant disease classification"""
        self.model = tf.keras.Sequential([
            # Data preprocessing
            layers.Resizing(self.image_size, self.image_size),
            layers.Rescaling(1.0/255),
            
            # Data augmentation
            layers.RandomFlip("horizontal_and_vertical"),
            layers.RandomRotation(0.2),
            
            # Convolutional layers
            layers.Conv2D(32, 3, padding='same', activation='relu'),
            layers.MaxPooling2D(),
            layers.Conv2D(64, 3, padding='same', activation='relu'),
            layers.MaxPooling2D(),
            layers.Conv2D(64, 3, padding='same', activation='relu'),
            layers.MaxPooling2D(),
            
            # Dense layers
            layers.Flatten(),
            layers.Dense(64, activation='relu'),
            layers.Dropout(0.5),
            layers.Dense(self.num_classes, activation='softmax')
        ])
        
        self.model.compile(
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
    
    def create_synthetic_dataset(self, num_samples=1000):
        """Create synthetic dataset for demonstration"""
        # Generate synthetic images (simulating plant disease images)
        X = np.random.rand(num_samples, self.image_size, self.image_size, 3)
        y = np.random.randint(0, self.num_classes, num_samples)
        
        # Split the data
        split_idx = int(0.8 * num_samples)
        X_train, X_test = X[:split_idx], X[split_idx:]
        y_train, y_test = y[:split_idx], y[split_idx:]
        
        return X_train, X_test, y_train, y_test
    
    def train(self, X_train, y_train, epochs=10, validation_split=0.2):
        """Train the model"""
        history = self.model.fit(
            X_train, y_train,
            epochs=epochs,
            validation_split=validation_split,
            verbose=1
        )
        return history
    
    def predict(self, image):
        """Make prediction on a single image"""
        if isinstance(image, str):
            # Decode base64 image
            image_data = base64.b64decode(image.split(',')[1])
            image = Image.open(io.BytesIO(image_data))
        
        # Preprocess image
        image = image.resize((self.image_size, self.image_size))
        image_array = np.array(image) / 255.0
        image_array = np.expand_dims(image_array, axis=0)
        
        # Make prediction
        predictions = self.model.predict(image_array)
        predicted_class = np.argmax(predictions[0])
        confidence = float(np.max(predictions[0]))
        
        return {
            'class': self.class_names[predicted_class],
            'class_id': int(predicted_class),
            'confidence': confidence,
            'probabilities': predictions[0].tolist()
        }
    
    def evaluate(self, X_test, y_test):
        """Evaluate the model"""
        test_loss, test_accuracy = self.model.evaluate(X_test, y_test, verbose=0)
        return {'loss': test_loss, 'accuracy': test_accuracy}
```

Now we can train our model using the above implementation:

```python
# Create and train the computer vision model
print("Training Computer Vision Model...")
cv_model = ComputerVisionModel()
# Create synthetic dataset
X_train, X_test, y_train, y_test = cv_model.create_synthetic_dataset()
# Train the model
history = cv_model.train(X_train, y_train, epochs=5)
# Evaluate the model
evaluation = cv_model.evaluate(X_test, y_test)
print(f"Computer Vision Model Performance:")
print(f"Test Accuracy: {evaluation['accuracy']:.4f}")
print(f"Test Loss: {evaluation['loss']:.4f}")
# Save the model
cv_model.model.save('computer_vision_model.h5')
print("Computer vision model saved to computer_vision_model.h5")
```

Now let's create a Flask application to serve the computer vision model:

```python
app3 = Flask(__name__)
# Global variable to store the computer vision model
cv_model = None
@app3.before_first_request
def load_cv_model():
    global cv_model
    cv_model = ComputerVisionModel()
    cv_model.model = tf.keras.models.load_model('computer_vision_model.h5')
    print("Computer vision model loaded successfully!")
@app3.route('/predict/image', methods=['POST'])
def predict_image():
    """Endpoint for computer vision model"""
    try:
        # Check if image is provided as base64 or file
        if 'image' in request.files:
            # File upload
            file = request.files['image']
            image = Image.open(file.stream)
        elif 'image_base64' in request.json:
            # Base64 encoded image
            image_data = request.json['image_base64']
            image = Image.open(io.BytesIO(base64.b64decode(image_data.split(',')[1])))
        else:
            return jsonify({'error': 'No image provided'}), 400
        
        # Make prediction
        result = cv_model.predict(image)
        
        return jsonify({
            'prediction': result,
            'model_type': 'computer_vision',
            'framework': 'tensorflow_keras',
            'task': 'plant_disease_classification',
            'classes': cv_model.class_names,
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@app3.route('/predict/batch', methods=['POST'])
def predict_batch():
    """Endpoint for batch prediction with computer vision model"""
    try:
        data = request.get_json()
        if not data or 'images' not in data:
            return jsonify({'error': 'No images provided'}), 400
        
        images_data = data['images']
        results = []
        
        for i, image_data in enumerate(images_data):
            try:
                # Decode base64 image
                image_data_decoded = base64.b64decode(image_data.split(',')[1])
                image = Image.open(io.BytesIO(image_data_decoded))
                
                # Make prediction
                result = cv_model.predict(image)
                result['image_index'] = i
                results.append(result)
                
            except Exception as e:
                results.append({
                    'image_index': i,
                    'error': str(e)
                })
        
        return jsonify({
            'predictions': results,
            'model_type': 'computer_vision',
            'framework': 'tensorflow_keras',
            'task': 'plant_disease_classification',
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@app3.route('/model/info', methods=['GET'])
def get_model_info():
    """Get information about the computer vision model"""
    model_info = {
        'model_type': 'computer_vision',
        'framework': 'tensorflow_keras',
        'task': 'plant_disease_classification',
        'classes': cv_model.class_names if cv_model else [],
        'image_size': 256,
        'architecture': 'CNN with data augmentation',
        'layers': [
            'Conv2D(32) + MaxPooling2D',
            'Conv2D(64) + MaxPooling2D', 
            'Conv2D(64) + MaxPooling2D',
            'Dense(64) + Dropout(0.5)',
            'Dense(3, softmax)'
        ]
    }
    return jsonify(model_info)
@app3.route('/health', methods=['GET'])
def health_check_cv():
    return jsonify({'status': 'healthy', 'model_loaded': cv_model is not None})
if __name__ == '__main__':
    app3.run(debug=True, host='0.0.0.0', port=5002)
```

Let's test the computer vision model server, creating the following functions:

```python
def create_test_image():
    """Create a test image for demonstration"""
    # Create a simple test image
    image = Image.new('RGB', (256, 256), color='green')
    # Convert to base64
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    image_base64 = base64.b64encode(buffer.getvalue()).decode()
    return f"data:image/png;base64,{image_base64}"
def test_cv_image_prediction():
    """Test computer vision image prediction endpoint"""
    url = "http://localhost:5002/predict/image"   
    # Create test image
    test_image = create_test_image()
    data = {"image_base64": test_image}
    response = requests.post(url, json=data)
    return response.json()
def test_cv_batch_prediction():
    """Test computer vision batch prediction endpoint"""
    url = "http://localhost:5002/predict/batch"
    # Create multiple test images
    test_images = [create_test_image() for _ in range(3)]
    data = {"images": test_images}
    response = requests.post(url, json=data)
    return response.json()
```

Now let's test the endpoints:

```python
# Test computer vision image prediction
print("Testing Computer Vision Model:")
result_cv_image = test_cv_image_prediction()
print(json.dumps(result_cv_image, indent=2))
# Test computer vision batch prediction
print("\nTesting Batch Prediction:")
result_cv_batch = test_cv_batch_prediction()
print(json.dumps(result_cv_batch, indent=2))
# Test model info
print("\nComputer Vision Model Information:")
response = requests.get("http://localhost:5002/model/info")
model_info = response.json()
print(json.dumps(model_info, indent=2))
```

---

## Summary

This practical session demonstrates three different approaches to deploying neural network models in production:

1. **From-Scratch Neural Network Implementation** (Port 5000):
   - Complete neural network implementation from scratch
   - Flask deployment with simple API endpoints
   - Demonstrates how to deploy custom implementations

2. **Multi-Architecture Neural Network Implementation** (Port 5001):
   - Comprehensive neural network with multiple architectures
   - Architecture selection via API parameters
   - Shows how to deploy complex model systems

3. **TensorFlow/Keras Computer Vision Implementation** (Port 5002):
   - Modern deep learning framework deployment
   - Computer vision model with image processing
   - Demonstrates production deployment of modern frameworks

Each exercise showcases different deployment strategies and production considerations for machine learning models that you built during the course.

Many thanks!

<!-- end NOTEBOOK: --> 