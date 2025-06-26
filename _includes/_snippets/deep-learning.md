<!-- SLIDES: -->

## Deep Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p>Deep learning extends neural networks by using <b>multiple hidden layers</b> to learn hierarchical representations of data, enabling the automatic discovery of complex features.</p>
            </div>
        </div>
    </div>
</div>

## Deep Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/ml-model.svg" alt="Deep Neural Network" style="max-width: 100%; height: auto;">
                <div class="footnote">Deep Neural Network with multiple hidden layers.</div>
            </div>
            <div class="column vertical-top text-left" style="width: 50%">
                <br>
                <p><b>Key Characteristics:</b></p>
                <br>
                <p>• <b>Multiple Hidden Layers:</b> 3+ layers for deep architectures</p>
                <p>• <b>Hierarchical Features:</b> Each layer learns increasingly abstract representations</p>
                <p>• <b>Automatic Feature Learning:</b> No manual feature engineering required</p>
                <p>• <b>Representation Learning:</b> Learns useful representations from raw data</p>
            </div>
        </div>
    </div>
</div>

## Deep Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <br>
                <p><b>Mathematical Formulation:</b></p>
                <p>For a deep neural network the forward propagation is:</p>
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
<br>Where each layer $l$ has its own weight matrix $\mathbf{W}^{(l)}$, bias vector $\mathbf{b}^{(l)}$, and activation function $f^{(l)}$.
</div>
        </div>
    </div>
</div>

## Deep Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p><b>Modern Activation Functions</b> for deep networks address the vanishing gradient problem.</p>
            </div>
        </div>
    </div>
</div>

## Deep Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 33%">
                <p><b>ReLU (Rectified Linear Unit):</b></p>
$$
\text{ReLU}(z) = \max(0, z)
$$
<br>Range: $[0, \infty)$
<br>Derivative: $\text{ReLU}'(z) = \begin{cases} 1 & \text{if } z > 0 \\ 0 & \text{if } z \leq 0 \end{cases}$
<br>
<img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/c/c9/Ramp_function.svg" alt="ReLU Function" style="max-width: 75%; height: auto;">
<div class="footnote">ReLU Function - Qef, Public domain, via Wikimedia Commons.</div>
            </div>
            <div class="column vertical-top text-left" style="width: 33%">
                <p><b>Leaky ReLU:</b></p>
$$
\text{LeakyReLU}(z) = \begin{cases} z & \text{if } z > 0 \\ \alpha z & \text{if } z \leq 0 \end{cases}
$$
<br>Range: $(-\infty, \infty)$
<br>Derivative: $\text{LeakyReLU}'(z) = \begin{cases} 1 & \text{if } z > 0 \\ \alpha & \text{if } z \leq 0 \end{cases}$
<br>
<img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/8/88/Leaky_ReLU.svg" alt="Leaky ReLU" style="max-width: 75%; height: auto;">
<div class="footnote">Leaky ReLU - Geek3, CC BY-SA 3.0, via Wikimedia Commons.</div>
            </div>
            <div class="column vertical-top text-left" style="width: 33%">
                <p><b>ELU (Exponential Linear Unit):</b></p>
$$
\text{ELU}(z) = \begin{cases} z & \text{if } z > 0 \\ \alpha(e^z - 1) & \text{if } z \leq 0 \end{cases}
$$
<br>Range: $[-\alpha, \infty)$
<br>Derivative: $\text{ELU}'(z) = \begin{cases} 1 & \text{if } z > 0 \\ \text{ELU}(z) + \alpha & \text{if } z \leq 0 \end{cases}$
<br>
<img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/f/f9/ELU_function.svg" alt="ELU Function" style="max-width: 75%; height: auto;">
<div class="footnote">ELU Function - Geek3, CC BY-SA 3.0, via Wikimedia Commons.</div>
            </div>
        </div>
    </div>
</div>

## Deep Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <br>
                <p><b>Vanishing and Exploding Gradients:</b></p>
                <p>In deep networks, gradients can become very small (vanishing) or very large (exploding) during backpropagation:</p>
                <br>
$$
\frac{\partial L}{\partial \mathbf{W}^{(l)}} = \frac{\partial L}{\partial \mathbf{z}^{(L)}} \prod_{k=l+1}^{L} \mathbf{W}^{(k)} \prod_{k=l+1}^{L-1} f'(\mathbf{z}^{(k)})
$$
<br>
<p><b>Solutions:</b></p>
<br>
<p>• <b>Proper Weight Initialization:</b> Xavier/Glorot initialization</p>
<p>• <b>Batch Normalization:</b> Normalize activations during training</p>
<p>• <b>Residual Connections:</b> Skip connections to bypass layers</p>
<p>• <b>Modern Optimizers:</b> Adam, RMSprop with adaptive learning rates</p>
</div>
        </div>
    </div>
</div>

## Deep Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <br>
                <p><b>Weight Initialization:</b></p>
                <br>
                <p><b>Xavier/Glorot Initialization:</b></p>
<br>
$$
W_{ij} \sim \mathcal{N}\left(0, \frac{2}{n_{in} + n_{out}}\right)
$$
<br>
<p><b>He Initialization (for ReLU):</b></p>
<br>
$$
W_{ij} \sim \mathcal{N}\left(0, \frac{2}{n_{in}}\right)
$$
<br>Where $n_{in}$ and $n_{out}$ are the number of input and output neurons respectively.
</div>
        </div>
    </div>
</div>

## Deep Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <p>Normalize the inputs to each layer to stabilize training:</p>
$$
\mu_B = \frac{1}{m} \sum_{i=1}^{m} x_i
$$
<br>
$$
\sigma_B^2 = \frac{1}{m} \sum_{i=1}^{m} (x_i - \mu_B)^2
$$
<br>
$$
\hat{x}_i = \frac{x_i - \mu_B}{\sqrt{\sigma_B^2 + \epsilon}}
$$
<br>
$$
y_i = \gamma \hat{x}_i + \beta
$$
<br>Where $\gamma$ and $\beta$ are learnable parameters, and $\epsilon$ is a small constant for numerical stability.
</div>
        </div>
    </div>
</div>

## Deep Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <p><b>Adam Optimizer:</b></p>
$$
m_t = \beta_1 m_{t-1} + (1 - \beta_1) g_t
$$
<br>
$$
v_t = \beta_2 v_{t-1} + (1 - \beta_2) g_t^2
$$
<br>
$$
\hat{m}_t = \frac{m_t}{1 - \beta_1^t}
$$
<br>
$$
\hat{v}_t = \frac{v_t}{1 - \beta_2^t}
$$
<br>
$$
\theta_t = \theta_{t-1} - \frac{\alpha}{\sqrt{\hat{v}_t} + \epsilon} \hat{m}_t
$$
<br>Where $g_t$ is the gradient at time $t$, and $\beta_1, \beta_2$ are momentum parameters.
</div>
        </div>
    </div>
</div>

## Deep Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <p><b>Regularization Techniques:</b></p>
                <br>
                <p><b>Dropout:</b> Randomly deactivate neurons during training</p>
$$
y_i = \begin{cases} \frac{x_i}{1-p} & \text{with probability } 1-p \\ 0 & \text{with probability } p \end{cases}
$$
<br>
<p><b>L2 Regularization:</b> Add penalty to loss function</p>
$$
L_{reg} = L + \lambda \sum_{l=1}^{L} ||\mathbf{W}^{(l)}||_F^2
$$
<br>
<p><b>Early Stopping:</b> Stop training when validation loss increases</p>
<br>
<p><b>Data Augmentation:</b> Create additional training examples through transformations</p>
</div>
        </div>
    </div>
</div>

## Deep Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <br>
                <p><b>Residual Networks (ResNets):</b></p>
                <br>
                <p>Skip connections allow gradients to flow directly through the network:</p>
                <br>
$$
\mathbf{a}^{(l+1)} = f^{(l+1)}(\mathbf{W}^{(l+1)}\mathbf{a}^{(l)} + \mathbf{b}^{(l+1)}) + \mathbf{a}^{(l)}
$$
<br>
<p>This helps with:</p>
<br>
<p>• <b>Vanishing Gradients:</b> Direct path for gradient flow</p>
<p>• <b>Training Deep Networks:</b> Easier optimization</p>
<p>• <b>Identity Mapping:</b> Network can learn residual functions</p>
</div>
        </div>
    </div>
</div>

## Deep Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">

```python
import numpy as np
import tensorflow as tf
class DeepNeuralNetwork:
    def __init__(self, layers, activation='relu'):
        self.layers = layers
        self.activation = activation
        self.weights = []
        self.biases = []
        for i in range(len(layers) - 1):
            std = np.sqrt(2.0 / (layers[i] + layers[i+1]))
            w = np.random.normal(0, std, (layers[i+1], layers[i]))
            b = np.zeros((layers[i+1], 1))
            self.weights.append(w)
            self.biases.append(b)
    def relu(self, z):
        return np.maximum(0, z)
    def relu_derivative(self, z):
        return np.where(z > 0, 1, 0)
    def forward(self, X):
        a = X
        activations = [X]
        for i in range(len(self.weights)):
            z = np.dot(self.weights[i], a) + self.biases[i]
            a = self.relu(z)
            activations.append(a)
        return activations
```
</div>
        </div>
    </div>
</div>

## Deep Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">

```python
def train_deep_network(X_train, y_train, model, epochs=1000, batch_size=32, learning_rate=0.001):
    """
    Training function for deep neural networks with modern techniques
    """
    n_samples = X_train.shape[1]
    optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)
    for epoch in range(epochs):
        indices = np.random.permutation(n_samples)
        X_shuffled = X_train[:, indices]
        y_shuffled = y_train[:, indices]
        epoch_loss = 0
        for i in range(0, n_samples, batch_size):
            batch_end = min(i + batch_size, n_samples)
            X_batch = X_shuffled[:, i:batch_end]
            y_batch = y_shuffled[:, i:batch_end]
            activations = model.forward(X_batch)
            y_pred = activations[-1]
            loss = tf.keras.losses.categorical_crossentropy(y_batch.T, y_pred.T)
            epoch_loss += np.mean(loss)
            with tf.GradientTape() as tape:
                activations = model.forward(X_batch)
                y_pred = activations[-1]
                loss = tf.keras.losses.categorical_crossentropy(y_batch.T, y_pred.T)
            gradients = tape.gradient(loss, model.weights + model.biases)
            optimizer.apply_gradients(zip(gradients, model.weights + model.biases))
        if epoch % 100 == 0:
            print(f"Epoch {epoch}, Loss: {epoch_loss/(n_samples//batch_size):.4f}")
    return model
```
</div>
        </div>
    </div>
</div>

## Deep Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <br>
                <p><b>Convolutional Neural Networks (CNNs):</b></p>
                <br>
                <p>Specialized for processing grid-like data (images):</p>
$$
(\mathbf{I} * \mathbf{K})_{i,j} = \sum_{m} \sum_{n} \mathbf{I}_{i+m,j+n} \mathbf{K}_{m,n}
$$
<br>
<p><b>Key Components:</b></p>
<br>
<p>• <b>Convolutional Layers:</b> Extract local features</p>
<p>• <b>Pooling Layers:</b> Reduce spatial dimensions</p>
<p>• <b>Fully Connected Layers:</b> Final classification</p>
<br>
<p><b>Advantages:</b> Parameter sharing, translation invariance, hierarchical feature learning</p>
</div>
        </div>
    </div>
</div>

## Deep Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <br>
                <p><b>Recurrent Neural Networks (RNNs):</b></p>
                <br>
                <p>Designed for sequential data processing:</p>
                <br>
$$
\mathbf{h}_t = f(\mathbf{W}_h \mathbf{h}_{t-1} + \mathbf{W}_x \mathbf{x}_t + \mathbf{b})
$$
<br>
$$
\mathbf{y}_t = \mathbf{W}_y \mathbf{h}_t + \mathbf{b}_y
$$
<br>
<p><b>Applications:</b> Natural language processing, speech recognition, time series prediction</p>
<br>
<p><b>Challenges:</b> Vanishing gradients in long sequences</p>
<br>
<p><b>Solutions:</b> LSTM, GRU, attention mechanisms</p>
</div>
        </div>
    </div>
</div>

<!-- end SLIDES: --> 