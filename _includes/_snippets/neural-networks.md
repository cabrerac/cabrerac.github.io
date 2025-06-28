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
                <img src="{{ site.url }}/assets/media/diagrams/perceptron.svg" alt="Perceptron Architecture" style="max-width: 100%; height: auto;">
                <div class="footnote">Perceptron Architecture.</div>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
            </div>
        </div>
    </div>
</div>

## Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/perceptron.svg" alt="Perceptron Architecture" style="max-width: 100%; height: auto;">
                <div class="footnote">Perceptron Architecture.</div>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Previous models:</b></p>
                <br>
                <ul>
                    <li>Useful analytical and computational properties</li>
                    <li>Limited application because of <em>the curse of dimensionality</em></li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/perceptron.svg" alt="Perceptron Architecture" style="max-width: 100%; height: auto;">
                <div class="footnote">Perceptron Architecture.</div>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Large scale problems require we adapt the basis functions to the data.</b></p>
            </div>
        </div>
    </div>
</div>

## Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/4/46/Colored_neural_network.svg" alt="Neural Network" style="max-width: 100%; height: auto;">
                <div class="footnote">Neural Network Architecture.</div>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Large scale problems require we adapt the basis functions to the data.</b></p>
            </div>
        </div>
    </div>
</div>

## Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/4/46/Colored_neural_network.svg" alt="Neural Network" style="max-width: 100%; height: auto;">
                <div class="footnote">Neural Network Architecture.</div>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Neural Networks:</b></p>
                <br>
                <ul>
                    <li>Fix the number of basis functions in advance</li>
                    <li>Basis functions are adaptive and their parameters can be updated during training</li>
                </ul>
                <br>
                <p><b>Training is costly but inference is cheap.</b></p>
            </div>
        </div>
    </div>
</div>

## Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/4/46/Colored_neural_network.svg" alt="Neural Network" style="max-width: 100%; height: auto;">
                <div class="footnote">Neural Network Architecture.</div>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Key Components:</b></p>
                <ul>
                    <li><b>Input Layer:</b> Receives the input features</li>
                    <li><b>Hidden Layers:</b> Process information through weighted connections</li>
                    <li><b>Output Layer:</b> Produces the final prediction</li>
                    <li><b>Activation Functions:</b> Introduce non-linearity</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/4/46/Colored_neural_network.svg" alt="Neural Network" style="max-width: 100%; height: auto;">
                <div class="footnote">Neural Network Architecture.</div>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>The Universal Approximation Theorem</b> states that a neural network with one hidden layer can approximate any continuous function on a compact subset of ℝⁿ, given sufficient neurons in the hidden layer because neural networks form complex decision boundaries through the combination of linear transformations and non-linear activation functions.</p>
            </div>
        </div>
    </div>
</div>

## Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <br>
                <p><b>Feedforward Neural Network:</b></p>
                <p>First, recall the general form of a linear model with nonlinear basis functions:</p>
$$
y(\mathbf{x}, \mathbf{w}) = f\left( \sum_{j=1}^M w_j \phi_j(\mathbf{x}) \right)
$$
<br>where $f(\cdot)$ is a nonlinear activation function (e.g., identity for regression, sigmoid for classification), $\phi_j(\mathbf{x})$ are basis functions, and $w_j$ are weights.
</div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/perceptron.svg" alt="Perceptron Architecture" style="max-width: 100%; height: auto;">
                <div class="footnote">Perceptron Architecture.</div>
            </div>
        </div>
    </div>
</div>

## Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <br>
                <p><b>Feedforward Neural Network:</b></p>
                <p>First, recall the general form of a linear model with nonlinear basis functions:</p>
$$
y(\mathbf{x}, \mathbf{w}) = f\left( \sum_{j=1}^M w_j \phi_j(\mathbf{x}) \right)
$$
<br>where $f(\cdot)$ is a nonlinear activation function (e.g., identity for regression, sigmoid for classification), $\phi_j(\mathbf{x})$ are basis functions, and $w_j$ are weights.
<br>In neural networks, the basis functions themselves are parameterized and learned. The network is constructed as a sequence of transformations.
</div>
            <div class="column vertical-top text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/neural-network.png" alt="Two-layer Neural Network" style="max-width: 100%; height: auto;">
                <div class="footnote">Two-layer Neural Network - <a href="https://www.microsoft.com/en-us/research/wp-content/uploads/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf">(Bishop, 2006)</a>.</div>
            </div>
        </div>
    </div>
</div>

## Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <p><b>Feedforward Neural Network:</b></p>
<p>1. Linear combination of inputs (first layer):</p>
$$
a_j = \sum_{i=1}^D w_{ji}^{(1)} x_i + w_{j0}^{(1)}
$$
where $j = 1, \ldots, M$ and $w_{ji}^{(1)}$ are the weights from input $i$ to hidden unit $j$, $w_{j0}^{(1)}$ is the bias for hidden unit $j$.
<br>
</div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/perceptron.svg" alt="Perceptron Architecture" style="max-width: 100%; height: auto;">
                <div class="footnote">Perceptron Architecture.</div>
            </div>
        </div>
    </div>
</div>

## Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <p><b>Feedforward Neural Network:</b></p>
<p>1. Linear combination of inputs (first layer):</p>
$$
a_j = \sum_{i=1}^D w_{ji}^{(1)} x_i + w_{j0}^{(1)}
$$
where $j = 1, \ldots, M$ and $w_{ji}^{(1)}$ are the weights from input $i$ to hidden unit $j$, $w_{j0}^{(1)}$ is the bias for hidden unit $j$.
<br>
<p>2. Nonlinear activation (hidden layer):</p>
$$
z_j = h(a_j)
$$
<br>where $h(\cdot)$ is a nonlinear activation function (e.g., sigmoid, tanh, ReLU).
</div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/perceptron.svg" alt="Perceptron Architecture" style="max-width: 100%; height: auto;">
                <div class="footnote">Perceptron Architecture.</div>
            </div>
        </div>
    </div>
</div>

## Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <p><b>Feedforward Neural Network:</b></p>
<p>1. Linear combination of inputs (first layer):</p>
$$
a_j = \sum_{i=1}^D w_{ji}^{(1)} x_i + w_{j0}^{(1)}
$$
where $j = 1, \ldots, M$ and $w_{ji}^{(1)}$ are the weights from input $i$ to hidden unit $j$, $w_{j0}^{(1)}$ is the bias for hidden unit $j$.
<br>
<p>2. Nonlinear activation (hidden layer):</p>
$$
z_j = h(a_j)
$$
<br>where $h(\cdot)$ is a nonlinear activation function (e.g., sigmoid, tanh, ReLU).
</div>
            <div class="column vertical-top text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/neural-network.png" alt="Two-layer Neural Network" style="max-width: 100%; height: auto;">
                <div class="footnote">Two-layer Neural Network - <a href="https://www.microsoft.com/en-us/research/wp-content/uploads/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf">(Bishop, 2006)</a>.</div>
            </div>
        </div>
    </div>
</div>

## Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <p><b>Feedforward Neural Network:</b></p>
<p>3. Linear combination of hidden activations (output layer): </p>
$$
a_k = \sum_{j=1}^M w_{kj}^{(2)} z_j + w_{k0}^{(2)}
$$
where $k = 1, \ldots, K$ and $w_{kj}^{(2)}$ are the weights from hidden unit $j$ to output unit $k$, $w_{k0}^{(2)}$ is the bias for output unit $k$.
</div>
            <div class="column vertical-top text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/neural-network.png" alt="Two-layer Neural Network" style="max-width: 100%; height: auto;">
                <div class="footnote">Two-layer Neural Network - <a href="https://www.microsoft.com/en-us/research/wp-content/uploads/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf">(Bishop, 2006)</a>.</div>
            </div>
        </div>
    </div>
</div>

## Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <p><b>Feedforward Neural Network:</b></p>
<p>3. Linear combination of hidden activations (output layer): </p>
$$
a_k = \sum_{j=1}^M w_{kj}^{(2)} z_j + w_{k0}^{(2)}
$$
where $k = 1, \ldots, K$ and $w_{kj}^{(2)}$ are the weights from hidden unit $j$ to output unit $k$, $w_{k0}^{(2)}$ is the bias for output unit $k$.
<br>Optionally, the output activations $a_k$ can be further transformed using an appropriate activation function to produce the final network outputs $y_k$. For example, $y_k = a_k$ for regression problems or $y_k = \sigma(a_k)$ for binary classification problems.
</div>
            <div class="column vertical-top text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/neural-network.png" alt="Two-layer Neural Network" style="max-width: 100%; height: auto;">
                <div class="footnote">Two-layer Neural Network - <a href="https://www.microsoft.com/en-us/research/wp-content/uploads/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf">(Bishop, 2006)</a>.</div>
            </div>
        </div>
    </div>
</div>

## Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <p><b>Feedforward Neural Network:</b></p>
                <p>The overall network function combines these stages. For sigmoidal output unit activation functions, takes the form:</p>
$$
y_k(\mathbf{x}, \mathbf{w}) = \sigma\left( \sum_{j=1}^M w_{kj}^{(2)} \, h\left( \sum_{i=1}^D w_{ji}^{(1)} x_i + w_{j0}^{(1)} \right) + w_{k0}^{(2)} \right)
$$
</div>
            <div class="column vertical-top text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/neural-network.png" alt="Two-layer Neural Network" style="max-width: 100%; height: auto;">
                <div class="footnote">Two-layer Neural Network - <a href="https://www.microsoft.com/en-us/research/wp-content/uploads/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf">(Bishop, 2006)</a>.</div>
            </div>
        </div>
    </div>
</div>

## Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <p><b>Feedforward Neural Network:</b></p>
                <p>The overall network function combines these stages. For sigmoidal output unit activation functions, takes the form:</p>
$$
y_k(\mathbf{x}, \mathbf{w}) = \sigma\left( \sum_{j=1}^M w_{kj}^{(2)} \, h\left( \sum_{i=1}^D w_{ji}^{(1)} x_i + w_{j0}^{(1)} \right) + w_{k0}^{(2)} \right)
$$
<br>The bias parameters can be absorbed:
$$
y_k(\mathbf{x}, \mathbf{w}) = \sigma\left( \sum_{j=1}^M w_{kj}^{(2)} \, h\left( \sum_{i=1}^D w_{ji}^{(1)} x_i \right) \right)
$$
</div>
            <div class="column vertical-top text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/neural-network.png" alt="Two-layer Neural Network" style="max-width: 100%; height: auto;">
                <div class="footnote">Two-layer Neural Network - <a href="https://www.microsoft.com/en-us/research/wp-content/uploads/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf">(Bishop, 2006)</a>.</div>
            </div>
        </div>
    </div>
</div>

## Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <p><b>Feedforward Neural Network:</b></p>
                <p>The overall network function combines these stages. For sigmoidal output unit activation functions, takes the form:</p>
$$
y_k(\mathbf{x}, \mathbf{w}) = \sigma\left( \sum_{j=1}^M w_{kj}^{(2)} \, h\left( \sum_{i=1}^D w_{ji}^{(1)} x_i + w_{j0}^{(1)} \right) + w_{k0}^{(2)} \right)
$$
<br>The bias parameters can be absorbed:
$$
y_k(\mathbf{x}, \mathbf{w}) = \sigma\left( \sum_{j=1}^M w_{kj}^{(2)} \, h\left( \sum_{i=1}^D w_{ji}^{(1)} x_i \right) \right)
$$
<br>$h(\cdot)$ are continuous functions. The neural network is differentiable with respect to the parameters $\mathbf{w}$.
</div>
            <div class="column vertical-top text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/neural-network.png" alt="Two-layer Neural Network" style="max-width: 100%; height: auto;">
                <div class="footnote">Two-layer Neural Network - <a href="https://www.microsoft.com/en-us/research/wp-content/uploads/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf">(Bishop, 2006)</a>.</div>
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
            </div>
            <div class="column vertical-top text-left" style="width: 33%">
            </div>
            <div class="column vertical-top text-left" style="width: 33%">
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
            </div>
            <div class="column vertical-top text-left" style="width: 33%">
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
            <div class="column vertical-top text-left" style="width: 50%">
                <p><b>Training Process:</b></p>
<br>
<p>Given a training set of <em><b>N</b></em> example input-output pairs</p>
<br>
$$
(\mathbf{x_1}, \mathbf{y_1}), (\mathbf{x_2}, \mathbf{y_2}), ..., (\mathbf{x_n}, \mathbf{y_n})
$$
</div>
            <div class="column vertical-top text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/neural-network.png" alt="Two-layer Neural Network" style="max-width: 100%; height: auto;">
                <div class="footnote">Two-layer Neural Network - <a href="https://www.microsoft.com/en-us/research/wp-content/uploads/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf">(Bishop, 2006)</a>.</div>
            </div>
        </div>
    </div>
</div>

## Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <p><b>Training Process:</b></p>
<br>
<p>Given a training set of <em><b>N</b></em> example input-output pairs</p>
<br>
$$
(\mathbf{x_1}, \mathbf{y_1}), (\mathbf{x_2}, \mathbf{y_2}), ..., (\mathbf{x_n}, \mathbf{y_n})
$$
<br>Each pair was generated by an unknown function $f$:
<br>
$$
\mathbf{y} = f(\mathbf{x}) + \epsilon
$$
</div>
            <div class="column vertical-top text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/neural-network.png" alt="Two-layer Neural Network" style="max-width: 100%; height: auto;">
                <div class="footnote">Two-layer Neural Network - <a href="https://www.microsoft.com/en-us/research/wp-content/uploads/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf">(Bishop, 2006)</a>.</div>
            </div>
        </div>
    </div>
</div>

## Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <p><b>Training Process:</b></p>
<br>
<p>Given a training set of <em><b>N</b></em> example input-output pairs</p>
<br>
$$
(\mathbf{x_1}, \mathbf{y_1}), (\mathbf{x_2}, \mathbf{y_2}), ..., (\mathbf{x_n}, \mathbf{y_n})
$$
<br>Each pair was generated by an unknown function $f$:
<br>
$$
\mathbf{y} = f(\mathbf{x}) + \epsilon
$$
<br>We want to find a hypothesis $f'$ that minimises the error function:
$$
E(\mathbf{w}) = \frac{1}{2} \sum_{n=1}^N \|\mathbf{y}_n - \mathbf{f'}(\mathbf{x}_n, \mathbf{w})\|^2
$$
</div>
            <div class="column vertical-top text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/neural-network.png" alt="Two-layer Neural Network" style="max-width: 100%; height: auto;">
                <div class="footnote">Two-layer Neural Network - <a href="https://www.microsoft.com/en-us/research/wp-content/uploads/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf">(Bishop, 2006)</a>.</div>
            </div>
        </div>
    </div>
</div>

## Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <p><b>Training Process (regression problem):</b></p>
<br>
<p>Giving a probabilistic interpretation to the network outputs:</p>
<br>
$$
p(y \, | \, \mathbf{x}, \mathbf{w}) = \mathcal{N}(y \, | \, f'(\mathbf{x}, \mathbf{w}), \beta^{-1})
$$                
<br>where $\beta$ is the precision (i.e. inverse variance $\sigma^2$).
</div>
            <div class="column vertical-top text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/neural-network.png" alt="Two-layer Neural Network" style="max-width: 100%; height: auto;">
                <div class="footnote">Two-layer Neural Network - <a href="https://www.microsoft.com/en-us/research/wp-content/uploads/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf">(Bishop, 2006)</a>.</div>
            </div>
        </div>
    </div>
</div>

## Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <p><b>Training Process (regression problem):</b></p>
<br>
<p>Giving a probabilistic interpretation to the network outputs:</p>
<br>
$$
p(y \, | \, \mathbf{x}, \mathbf{w}) = \mathcal{N}(y \, | \, f'(\mathbf{x}, \mathbf{w}), \beta^{-1})
$$                
<br>where $\beta$ is the precision (i.e. inverse variance $\sigma^2$).
<br>For a i.i.d. training set, the likelihood function corresponds to:
$$
p(\mathcal{Y} \, | \, \mathcal{X}, \mathbf{w}, \beta) = \prod_{n=1}^N \mathcal{N}(y_n \, | \, f'(\mathbf{x}_n, \mathbf{w}), \beta^{-1})
$$
</div>
            <div class="column vertical-top text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/neural-network.png" alt="Two-layer Neural Network" style="max-width: 100%; height: auto;">
                <div class="footnote">Two-layer Neural Network - <a href="https://www.microsoft.com/en-us/research/wp-content/uploads/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf">(Bishop, 2006)</a>.</div>
            </div>
        </div>
    </div>
</div>

## Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <p><b>Training Process (regression problem):</b></p>
<br>For a i.i.d. training set, the likelihood function corresponds to:
$$
p(\mathcal{Y} \, | \, \mathcal{X}, \mathbf{w}, \beta) = \prod_{n=1}^N \mathcal{N}(y_n \, | \, f'(\mathbf{x}_n, \mathbf{w}), \beta^{-1})
$$
</div>
            <div class="column vertical-top text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/neural-network.png" alt="Two-layer Neural Network" style="max-width: 100%; height: auto;">
                <div class="footnote">Two-layer Neural Network - <a href="https://www.microsoft.com/en-us/research/wp-content/uploads/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf">(Bishop, 2006)</a>.</div>
            </div>
        </div>
    </div>
</div>

## Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <p><b>Training Process (regression problem):</b></p>
<br>For a i.i.d. training set, the likelihood function corresponds to:
$$
p(\mathcal{Y} \, | \, \mathcal{X}, \mathbf{w}, \beta) = \prod_{n=1}^N \mathcal{N}(y_n \, | \, f'(\mathbf{x}_n, \mathbf{w}), \beta^{-1})
$$
<br>As we saw in previous sessions, maximising the likelihood function is equivalent to minimising the sum-of-squares error function given by:
$$
E(\mathbf{w}) = \frac{1}{2} \sum_{n=1}^N \left( y_n - f'(\mathbf{x}_n, \mathbf{w}) \right)^2
$$
</div>
            <div class="column vertical-top text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/neural-network.png" alt="Two-layer Neural Network" style="max-width: 100%; height: auto;">
                <div class="footnote">Two-layer Neural Network - <a href="https://www.microsoft.com/en-us/research/wp-content/uploads/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf">(Bishop, 2006)</a>.</div>
            </div>
        </div>
    </div>
</div>

## Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <p><b>Training Process (binary classification):</b></p>
                <p>The network output is:</p>
$$
f' = \sigma(a) \equiv \frac{1}{1 + \exp(-a)}
$$
We use a single target variable $f'$ such that $f'=1$ denotes class 1 and $f'=0$ denotes class 2.
</div>
            <div class="column vertical-top text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/neural-network.png" alt="Two-layer Neural Network" style="max-width: 100%; height: auto;">
                <div class="footnote">Two-layer Neural Network - <a href="https://www.microsoft.com/en-us/research/wp-content/uploads/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf">(Bishop, 2006)</a>.</div>
            </div>
        </div>
    </div>
</div>

## Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <p><b>Training Process (binary classification):</b></p>
                <p>The network output is:</p>
$$
f' = \sigma(a) \equiv \frac{1}{1 + \exp(-a)}
$$
We use a single target variable $f'$ such that $f'=1$ denotes class 1 and $f'=0$ denotes class 2. We interpret $f'(\mathbf{x}, \mathbf{w})$ as the conditional probability distribution of targets given inputs:
<br>
$$
p(t|\mathbf{x}, \mathbf{w}) = f'(\mathbf{x}, \mathbf{w})^t \{1 - f'(\mathbf{x}, \mathbf{w})\}^{1-t}
$$
</div>
            <div class="column vertical-top text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/neural-network.png" alt="Two-layer Neural Network" style="max-width: 100%; height: auto;">
                <div class="footnote">Two-layer Neural Network - <a href="https://www.microsoft.com/en-us/research/wp-content/uploads/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf">(Bishop, 2006)</a>.</div>
            </div>
        </div>
    </div>
</div>

## Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <p><b>Training Process (binary classification):</b></p>
                <p>The network output is:</p>
$$
f' = \sigma(a) \equiv \frac{1}{1 + \exp(-a)}
$$
We use a single target variable $f'$ such that $f'=1$ denotes class 1 and $f'=0$ denotes class 2. We interpret $f'(\mathbf{x}, \mathbf{w})$ as the conditional probability distribution of targets given inputs:
<br>
$$
p(t|\mathbf{x}, \mathbf{w}) = f'(\mathbf{x}, \mathbf{w})^t \{1 - f'(\mathbf{x}, \mathbf{w})\}^{1-t}
$$
For a i.i.d. training, the error function is the cross-entropy error:
$$
E(\mathbf{w}) = - \sum_{n=1}^N \{ y_n \ln f'_n + (1-y_n) \ln (1-f'_n) \}
$$
</div>
            <div class="column vertical-top text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/neural-network.png" alt="Two-layer Neural Network" style="max-width: 100%; height: auto;">
                <div class="footnote">Two-layer Neural Network - <a href="https://www.microsoft.com/en-us/research/wp-content/uploads/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf">(Bishop, 2006)</a>.</div>
            </div>
        </div>
    </div>
</div>

## Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 40%">
                <img src="https://upload.wikimedia.org/wikipedia/commons/a/a3/Gradient_descent.gif" alt="Gradient Descent Algorithm" style="max-width: 100%; height: auto;">
                <div class="footnote">Gradient Descent Algorithm - Jacopo Bertolotti, CC0, via Wikimedia Commons.</div>
            </div>
            <div class="column vertical-top text-left" style="width: 60%">
            </div>
        </div>
    </div>
</div>

## Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 40%">
                <img src="https://upload.wikimedia.org/wikipedia/commons/a/a3/Gradient_descent.gif" alt="Gradient Descent Algorithm" style="max-width: 100%; height: auto;">
                <div class="footnote">Gradient Descent Algorithm - Jacopo Bertolotti, CC0, via Wikimedia Commons.</div>
            </div>
            <div class="column vertical-top text-left" style="width: 60%">
                <p>We choose any starting point and then compute <b>an estimate of the gradient and move a small amount in the steepest downhill direction</b>, repeating until we converge on a point in the weight space with <em>(local)</em> minima loss.</p>
<br>
<pre><code>Gradient Descent Algorithm:
Initialize w
repeat
    for each w[i] in w
        Compute gradient: g = ∇Loss(w[i])
        Update weight:   w[i] = w[i] - α * g
until convergence
</code></pre>
<br>
<p>The size of the step is given by the parameter α, which regulates the behaviour of the gradient descent algorithm. This is a hyperparameter of the regression model we are training, usually called <em>learning rate.</em></p>
            </div>
        </div>
    </div>
</div>

## Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p>Error backpropagation is an efficient algorithm for computing gradients in neural networks using the <b>chain rule of calculus</b>.</p>
            </div>
        </div>
    </div>
</div>

## Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/neural-network.png" alt="Two-layer Neural Network" style="max-width: 100%; height: auto;">
                <div class="footnote">Two-layer Neural Network - <a href="https://www.microsoft.com/en-us/research/wp-content/uploads/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf">(Bishop, 2006)</a>.</div>
            </div>
            <div class="column vertical-top text-left" style="width: 50%">
            </div>
        </div>
    </div>
</div>

## Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/neural-network.png" alt="Two-layer Neural Network" style="max-width: 100%; height: auto;">
                <div class="footnote">Two-layer Neural Network - <a href="https://www.microsoft.com/en-us/research/wp-content/uploads/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf">(Bishop, 2006)</a>.</div>
            </div>
            <div class="column vertical-top text-left" style="width: 50%">
                <p><b>Error Backpropagation Algorithm:</b></p>
            </div>
        </div>
    </div>
</div>

## Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/neural-network.png" alt="Two-layer Neural Network" style="max-width: 100%; height: auto;">
                <div class="footnote">Two-layer Neural Network - <a href="https://www.microsoft.com/en-us/research/wp-content/uploads/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf">(Bishop, 2006)</a>.</div>
            </div>
            <div class="column vertical-top text-left" style="width: 50%">
                <p><b>Error Backpropagation Algorithm:</b></p>
<p><b>1. Forward Pass:</b> Compute all activations and outputs for an input vector.</p>
            </div>
        </div>
    </div>
</div>

## Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/neural-network.png" alt="Two-layer Neural Network" style="max-width: 100%; height: auto;">
                <div class="footnote">Two-layer Neural Network - <a href="https://www.microsoft.com/en-us/research/wp-content/uploads/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf">(Bishop, 2006)</a>.</div>
            </div>
            <div class="column vertical-top text-left" style="width: 50%">
                <p><b>Error Backpropagation Algorithm:</b></p>
<p><b>1. Forward Pass:</b> Compute all activations and outputs for an input vector.</p>
<p><b>2. Error Evaluation:</b> Evaluate the error for all the outputs using:</p>
$$
\delta_k = y_k - t_k
$$
</div>
        </div>
    </div>
</div>

## Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/neural-network.png" alt="Two-layer Neural Network" style="max-width: 100%; height: auto;">
                <div class="footnote">Two-layer Neural Network - <a href="https://www.microsoft.com/en-us/research/wp-content/uploads/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf">(Bishop, 2006)</a>.</div>
            </div>
            <div class="column vertical-top text-left" style="width: 50%">
                <p><b>Error Backpropagation Algorithm:</b></p>
<p><b>1. Forward Pass:</b> Compute all activations and outputs for an input vector.</p>
<p><b>2. Error Evaluation:</b> Evaluate the error for all the outputs using:</p>
$$
\delta_k = y_k - t_k
$$
<b>3. Backward Pass:</b> Backpropagate errors for each hidden unit in the network using:
$$
\delta_j = h'(a_j) \sum_k w_{kj} \delta_k
$$
</div>
        </div>
    </div>
</div>

## Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/neural-network.png" alt="Two-layer Neural Network" style="max-width: 100%; height: auto;">
                <div class="footnote">Two-layer Neural Network - <a href="https://www.microsoft.com/en-us/research/wp-content/uploads/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf">(Bishop, 2006)</a>.</div>
            </div>
            <div class="column vertical-top text-left" style="width: 50%">
                <p><b>Error Backpropagation Algorithm:</b></p>
<p><b>1. Forward Pass:</b> Compute all activations and outputs for an input vector.</p>
<p><b>2. Error Evaluation:</b> Evaluate the error for all the outputs using:</p>
$$
\delta_k = y_k - t_k
$$
<b>3. Backward Pass:</b> Backpropagate errors for each hidden unit in the network using:
$$
\delta_j = h'(a_j) \sum_k w_{kj} \delta_k
$$
<b>4. Derivatives Evaluation:</b> Evaluate the derivatives for each parameter using:
$$
\frac{\partial E_n}{\partial w_{ji}} = \delta_j z_i
$$
</div>
        </div>
    </div>
</div>

## Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/neural-network.png" alt="Two-layer Neural Network" style="max-width: 100%; height: auto;">
                <div class="footnote">Two-layer Neural Network - <a href="https://www.microsoft.com/en-us/research/wp-content/uploads/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf">(Bishop, 2006)</a>.</div>
            </div>
            <div class="column vertical-top text-left" style="width: 50%">
                <br>
                <p><b>Gradient Descent Update Rule:</b></p>
</div>
        </div>
    </div>
</div>

## Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/neural-network.png" alt="Two-layer Neural Network" style="max-width: 100%; height: auto;">
                <div class="footnote">Two-layer Neural Network - <a href="https://www.microsoft.com/en-us/research/wp-content/uploads/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf">(Bishop, 2006)</a>.</div>
            </div>
            <div class="column vertical-top text-left" style="width: 50%">
                <br>
                <p><b>Gradient Descent Update Rule:</b></p>
$$
\mathbf{W}^{(l)} \leftarrow \mathbf{W}^{(l)} - \alpha \frac{\partial E_n}{\partial \mathbf{W}^{(l)}}
$$
</div>
        </div>
    </div>
</div>

## Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/neural-network.png" alt="Two-layer Neural Network" style="max-width: 100%; height: auto;">
                <div class="footnote">Two-layer Neural Network - <a href="https://www.microsoft.com/en-us/research/wp-content/uploads/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf">(Bishop, 2006)</a>.</div>
            </div>
            <div class="column vertical-top text-left" style="width: 50%">
                <br>
                <p><b>Gradient Descent Update Rule:</b></p>
$$
\mathbf{W}^{(l)} \leftarrow \mathbf{W}^{(l)} - \alpha \frac{\partial E_n}{\partial \mathbf{W}^{(l)}}
$$
<br>
$$
\mathbf{w_{ji}}^{(l)} \leftarrow \mathbf{w_{ji}}^{(l)} - \alpha \frac{\partial E_n}{\partial w_{ji}^l} 
$$
</div>
        </div>
    </div>
</div>

## Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/neural-network.png" alt="Two-layer Neural Network" style="max-width: 100%; height: auto;">
                <div class="footnote">Two-layer Neural Network - <a href="https://www.microsoft.com/en-us/research/wp-content/uploads/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf">(Bishop, 2006)</a>.</div>
            </div>
            <div class="column vertical-top text-left" style="width: 50%">
                <br>
                <p><b>Gradient Descent Update Rule:</b></p>
$$
\mathbf{W}^{(l)} \leftarrow \mathbf{W}^{(l)} - \alpha \frac{\partial E_n}{\partial \mathbf{W}^{(l)}}
$$
<br>
$$
\mathbf{w_{ji}}^{(l)} \leftarrow \mathbf{w_{ji}}^{(l)} - \alpha \frac{\partial E_n}{\partial w_{ji}^l} 
$$
<br>
$$
\mathbf{w_{ji}}^{(l)} \leftarrow \mathbf{w_{ji}}^{(l)} - \alpha \delta_j z_i
$$
<br>Where $\alpha$ is the learning rate.
</div>
        </div>
    </div>
</div>

<!-- end SLIDES: --> 