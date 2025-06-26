<!-- SLIDES: -->

## Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p>Neural networks extend the perceptron by introducing <b>multiple layers of interconnected neurons</b> (i.e., multi-layer perceptron), enabling the learning of complex, non-linear relationships in data.</p>
            </div>
        </div>
    </div>
</div>

## Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/ml-model.svg" alt="Neural Network Architecture" style="max-width: 100%; height: auto;">
                <div class="footnote">Feedforward Neural Network Architecture.</div>
            </div>
            <div class="column vertical-top text-left" style="width: 50%">
                <br>
                <p><b>Key Components:</b></p>
                <br>
                <p>• <b>Input Layer:</b> Receives the input features</p>
                <p>• <b>Hidden Layers:</b> Process information through weighted connections</p>
                <p>• <b>Output Layer:</b> Produces the final prediction</p>
                <p>• <b>Activation Functions:</b> Introduce non-linearity</p>
                <br>
                <p><b>Universal Approximation:</b> A neural network with one hidden layer can approximate any continuous function.</p>
            </div>
        </div>
    </div>
</div>

## Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <br>
                <p><b>Feedforward Neural Network:</b></p>
                <br>
                <p>For a neural network with multiple layers, the output of one layer is:</p>
                <br>
$$
\mathbf{a}^{(l)} = f^{(l)}(\mathbf{z}^{(l)})
$$
<br>Where the pre-activation $\mathbf{z}^{(l)}$ is:
<br>
$$
\mathbf{z}^{(l)} = \mathbf{W}^{(l)}\mathbf{a}^{(l-1)} + \mathbf{b}^{(l)}
$$
<br>Here, $\mathbf{W}^{(l)}$ is the weight matrix, $\mathbf{b}^{(l)}$ is the bias vector, and $f^{(l)}$ is the activation function for layer $l$.
</div>
        </div>
    </div>
</div>

## Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <br>
                <p><b>Forward Propagation:</b></p>
                <br>
$$
\mathbf{a}^{(0)} = \mathbf{x}
$$
<br>
$$
\mathbf{z}^{(l)} = \mathbf{W}^{(l)}\mathbf{a}^{(l-1)} + \mathbf{b}^{(l)} \quad \text{for } l = 1, 2, ..., L
$$
<br>
$$
\mathbf{a}^{(l)} = f^{(l)}(\mathbf{z}^{(l)}) \quad \text{for } l = 1, 2, ..., L-1
$$
<br>
$$
\mathbf{y} = \mathbf{a}^{(L)} = f^{(L)}(\mathbf{z}^{(L)})
$$
<br>Where $x$ is the network input and $y$ is the network output.
</div>
        </div>
    </div>
</div>

## Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p><b>Activation functions</b> introduce non-linearity into the network, enabling it to learn complex patterns and relationships.</p>
            </div>
        </div>
    </div>
</div>

## Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 33%">
                <p><b>Sigmoid Function:</b></p>
$$
\sigma(z) = \frac{1}{1 + e^{-z}}
$$
<br>Range: $(0, 1)$
<br>Derivative: $\sigma'(z) = \sigma(z)(1 - \sigma(z))$
<br>
<img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/8/88/Logistic-curve.svg" alt="Logistic Curve" style="max-width: 65%; height: auto;">
<div class="footnote">Logistic Curve - Qef, Public domain, via Wikimedia Commons.</div>
            </div>
            <div class="column vertical-top text-left" style="width: 33%">
                <p><b>Hyperbolic Tangent:</b></p>
$$
\tanh(z) = \frac{e^z - e^{-z}}{e^z + e^{-z}}
$$
<br>Range: $(-1, 1)$
<br>Derivative: $\tanh'(z) = 1 - \tanh^2(z)$
<br>
<img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/8/87/Hyperbolic_Tangent.svg" alt="Hyperbolic Tangent" style="max-width: 75%; height: auto;">
<div class="footnote">Hyperbolic Tangent - Geek3, CC BY-SA 3.0 <https://creativecommons.org/licenses/by-sa/3.0>, via Wikimedia Commons.</div>
            </div>
            <div class="column vertical-top text-left" style="width: 33%">
                <p><b>ReLU (Rectified Linear Unit):</b></p>
$$
\text{ReLU}(z) = \max(0, z)
$$
<br>Range: $[0, \infty)$
<br>Derivative: $\text{ReLU}'(z) = \begin{cases} 1 & \text{if } z > 0 \\ 0 & \text{if } z \leq 0 \end{cases}$
<br>
<img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/c/c9/Ramp_function.svg" alt="Ramp Function" style="max-width: 75%; height: auto;">
<div class="footnote">Ramp Function - Qef, Public domain, via Wikimedia Commons.</div>
            </div>
        </div>
    </div>
</div>

## Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <br>
                <p><b>Loss functions</b></p>
                <p>Mean Squared Error (Regression):</p>
                <br>
$$
L(\mathbf{y}, \hat{\mathbf{y}}) = \frac{1}{N} \sum_{i=1}^{N} (y_i - \hat{y}_i)^2
$$
<br>
<p>Cross-Entropy Loss (Classification):</p>
<br>
$$
L(\mathbf{y}, \hat{\mathbf{y}}) = -\sum_{i=1}^{N} y_i \log(\hat{y}_i)
$$
<br>
<p>Binary Cross-Entropy:</p>
<br>
$$
L(y, \hat{y}) = -[y \log(\hat{y}) + (1 - y) \log(1 - \hat{y})]
$$
</div>
        </div>
    </div>
</div>

## Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p>Backpropagation is an efficient algorithm for computing gradients in neural networks using the <b>chain rule of calculus</b>.</p>
            </div>
        </div>
    </div>
</div>

## Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <br>
                <p><b>Backpropagation Algorithm:</b></p>
                <br>
                <p><b>1. Forward Pass:</b> Compute all activations and outputs</p>
                <br>
                <p><b>2. Backward Pass:</b> Compute gradients using chain rule</p>
                <br>
                <p>The gradient of the loss with respect to weights in layer $l$:</p>
                <br>
$$
\frac{\partial L}{\partial \mathbf{W}^{(l)}} = \frac{\partial L}{\partial \mathbf{z}^{(l)}} \frac{\partial \mathbf{z}^{(l)}}{\partial \mathbf{W}^{(l)}} = \boldsymbol{\delta}^{(l)} (\mathbf{a}^{(l-1)})^T
$$
<br>Where $\boldsymbol{\delta}^{(l)} = \frac{\partial L}{\partial \mathbf{z}^{(l)}}$ is the error term for layer $l$.
</div>
        </div>
    </div>
</div>

## Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <br>
                <p><b>Error Propagation:</b></p>
                <br>
                <p>For the output layer:</p>
                <br>
$$
\boldsymbol{\delta}^{(L)} = \frac{\partial L}{\partial \mathbf{z}^{(L)}} = \frac{\partial L}{\partial \mathbf{a}^{(L)}} \odot f'(\mathbf{z}^{(L)})
$$
<br>For hidden layers $l = L-1, L-2, ..., 1$:
<br>
$$
\boldsymbol{\delta}^{(l)} = \frac{\partial L}{\partial \mathbf{z}^{(l)}} = (\mathbf{W}^{(l+1)})^T \boldsymbol{\delta}^{(l+1)} \odot f'(\mathbf{z}^{(l)})
$$
<br>Where $\odot$ denotes element-wise multiplication.
</div>
        </div>
    </div>
</div>

## Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <br>
                <p><b>Backpropagation Algorithm</b></p>
                <br>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">

```python
def backpropagation(X, y, W, b, learning_rate=0.1):
    """
    Backpropagation algorithm for neural network training
    Inputs:
    - X: Input data (n_features, n_samples)
    - y: Target labels (n_outputs, n_samples) 
    - W: List of weight matrices for each layer
    - b: List of bias vectors for each layer
    - learning_rate: Step size for gradient descent
    Outputs:
    - Updated W and b after one training step
    """
    m = X.shape[1]
    a = [X]
    z = []
    for l in range(len(W)):
        z_l = np.dot(W[l], a[l]) + b[l]
        z.append(z_l)
        if l == len(W) - 1:
            a_l_plus_1 = softmax(z_l)
        else:
            a_l_plus_1 = sigmoid(z_l)
        a.append(a_l_plus_1)
    delta = []
    delta_L = (a[-1] - y) * sigmoid_derivative(z[-1])
    delta.append(delta_L)
    for l in range(len(W) - 2, -1, -1):
        delta_l = np.dot(W[l + 1].T, delta[0]) * sigmoid_derivative(z[l])
        delta.insert(0, delta_l)
    for l in range(len(W)):
        dW = np.dot(delta[l], a[l].T) / m
        db = np.sum(delta[l], axis=1, keepdims=True) / m
        W[l] -= learning_rate * dW
        b[l] -= learning_rate * db
    return W, b
```
</div>
        </div>
    </div>
</div>

## Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <br>
                <p><b>Gradient Descent Update Rule:</b></p>
$$
\mathbf{W}^{(l)} \leftarrow \mathbf{W}^{(l)} - \alpha \frac{\partial L}{\partial \mathbf{W}^{(l)}}
$$
<br>
$$
\mathbf{b}^{(l)} \leftarrow \mathbf{b}^{(l)} - \alpha \frac{\partial L}{\partial \mathbf{b}^{(l)}}
$$
<br>Where $\alpha$ is the learning rate.
</div>
<div class="column vertical-middle text-left" style="width: 50%">

```python
def train_neural_network(X_train, y_train, model, num_epochs, batch_size, learning_rate):
    """
    Complete training algorithm for neural network
    Inputs:
    - X_train: Training data (n_features, n_samples)
    - y_train: Training labels (n_outputs, n_samples)
    - model: NeuralNetwork instance with initialized weights and biases
    - num_epochs: Number of training iterations
    - batch_size: Size of mini-batches for SGD
    - learning_rate: Step size for gradient descent
    Outputs:
    - Trained model with optimized weights and biases
    - Training history (loss values per epoch)
    """
    n_samples = X_train.shape[1]
    training_history = []
    for epoch in range(num_epochs):
        indices = np.random.permutation(n_samples)
        X_shuffled = X_train[:, indices]
        y_shuffled = y_train[:, indices]
        epoch_loss = 0
        for i in range(0, n_samples, batch_size):
            batch_end = min(i + batch_size, n_samples)
            X_batch = X_shuffled[:, i:batch_end]
            y_batch = y_shuffled[:, i:batch_end]
            y_pred = model.forward(X_batch)
            batch_loss = compute_loss(y_batch, y_pred)
            epoch_loss += batch_loss
            model.backward(X_batch, y_batch, learning_rate)
        avg_epoch_loss = epoch_loss / (n_samples // batch_size)
        training_history.append(avg_epoch_loss)
        if epoch % 100 == 0:
            print(f"Epoch {epoch}, Loss: {avg_epoch_loss:.4f}")
    return model, training_history
```
</div>
        </div>
    </div>
</div>

## Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                
```python
import numpy as np

class NeuralNetwork:
    def __init__(self, layers):
        self.layers = layers
        self.weights = []
        self.biases = []
        for i in range(len(layers) - 1):
            w = np.random.randn(layers[i+1], layers[i]) * 0.01
            b = np.zeros((layers[i+1], 1))
            self.weights.append(w)
            self.biases.append(b)
    def sigmoid(self, z):
        return 1 / (1 + np.exp(-z))
    def sigmoid_derivative(self, z):
        s = self.sigmoid(z)
        return s * (1 - s)
    def forward(self, X):
        a = X
        for i in range(len(self.weights)):
            z = np.dot(self.weights[i], a) + self.biases[i]
            a = self.sigmoid(z)
        return a
```
</div>
        </div>
    </div>
</div>

## Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">

```python
    def backward(self, X, Y, learning_rate=0.1):
        m = X.shape[1]
        activations = [X]
        z_values = []
        for i in range(len(self.weights)):
            z = np.dot(self.weights[i], activations[-1]) + self.biases[i]
            z_values.append(z)
            a = self.sigmoid(z)
            activations.append(a)
        delta = activations[-1] - Y
        for i in range(len(self.weights) - 1, -1, -1):
            dW = np.dot(delta, activations[i].T) / m
            db = np.sum(delta, axis=1, keepdims=True) / m
            if i > 0:
                delta = np.dot(self.weights[i].T, delta) * self.sigmoid_derivative(z_values[i-1])
            self.weights[i] -= learning_rate * dW
            self.biases[i] -= learning_rate * db
```
</div>
        </div>
    </div>
</div>

## Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <br>
                <p><b>Universal Approximation Theorem:</b></p>
                <br>
$$
F(\mathbf{x}) = \sum_{i=1}^{N} v_i \phi(\mathbf{w}_i^T \mathbf{x} + b_i)
$$
<br>Let $\phi$ be a non-constant, bounded, and monotonically-increasing continuous function. Let $I_m$ denote the $m$-dimensional unit hypercube $[0,1]^m$. The space of continuous functions on $I_m$ is denoted by $C(I_m)$. Then, given any $\epsilon > 0$ and any function $f \in C(I_m)$, there exist vectors $\mathbf{w}_1, \mathbf{w}_2, ..., \mathbf{w}_N$, $\mathbf{b}$, and $\mathbf{v}$.
<br>
$$
|F(\mathbf{x}) - f(\mathbf{x})| < \epsilon \quad \text{for all } \mathbf{x} \in I_m
$$
</div>
        </div>
    </div>
</div>

<!-- end SLIDES: --> 