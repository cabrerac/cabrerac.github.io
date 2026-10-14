<!-- SLIDES: -->

## The Perceptron

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/xor_problem.png" alt="XOR Problem" style="max-width: 80%; height: auto;">
                <div class="footnote">XOR Problem - Andreas Maier, CC BY 4.0 <https://creativecommons.org/licenses/by/4.0>, via Wikimedia Commons</div>
            </div>
            <div class="column vertical-top text-left" style="width: 50%">
                <br>
                <p><b>XOR Problem:</b></p>
                <br>
                <p>The perceptron cannot learn the XOR function because it's not linearly separable.</p> 
                <p><a href="https://rodsmith.nz/wp-content/uploads/Minsky-and-Papert-Perceptrons.pdf">(Minsky & Papert, 1969)</a></p>
                <br>
                <p><b>Other limitations:</b></p>
                <ul>
                    <li>Only binary classification</li>
                    <li>No probabilistic output</li>
                    <li>The step function is not differentiable</li>
                    <li>May oscillate for non-separable data</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Feedforward Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p>Neural networks extend the perceptron by introducing <b>multiple layers of interconnected neurons</b> (i.e., multi-layer perceptron), enabling the learning of complex, non-linear relationships in data.</p>
            </div>
        </div>
    </div>
</div>

## Feedforward Neural Networks

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

## Feedforward Neural Networks

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

## Feedforward Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/perceptron.svg" alt="Perceptron Architecture" style="max-width: 100%; height: auto;">
                <div class="footnote">Perceptron Architecture.</div>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Large scale problems require that we adapt the basis functions to the data.</b></p>
            </div>
        </div>
    </div>
</div>

## Feedforward Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/4/46/Colored_neural_network.svg" alt="Neural Network" style="max-width: 100%; height: auto;">
                <div class="footnote">Neural Network Architecture.</div>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Large scale problems require that we adapt the basis functions to the data.</b></p>
            </div>
        </div>
    </div>
</div>

## Feedforward Neural Networks

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

## Feedforward Neural Networks

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

## Feedforward Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/4/46/Colored_neural_network.svg" alt="Neural Network" style="max-width: 100%; height: auto;">
                <div class="footnote">Neural Network Architecture.</div>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>The Universal Approximation Theorem</b> states that a neural network with one hidden layer can approximate any continuous function on a compact subset of $\mathbb{R}^n$, given sufficient neurons in the hidden layer because neural networks form complex decision boundaries through the combination of linear transformations and non-linear activation functions.</p>
            </div>
        </div>
    </div>
</div>

## Feedforward Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <br>
                <p><b>Feedforward Neural Network:</b></p>
                <p>First, recall the general form of a linear model with nonlinear basis functions:</p>
$$
\hat{y}(\mathbf{x}, \mathbf{w}) = g\left( \sum_{j=1}^M w_j \phi_j(\mathbf{x}) \right)
$$
<br>where $g(\cdot)$ is a nonlinear activation function (e.g., identity for regression, sigmoid for classification), $\phi_j(\mathbf{x})$ are basis functions, and $w_j$ are weights.
</div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/perceptron.svg" alt="Perceptron Architecture" style="max-width: 100%; height: auto;">
                <div class="footnote">Perceptron Architecture.</div>
            </div>
        </div>
    </div>
</div>

## Feedforward Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <br>
                <p><b>Feedforward Neural Network:</b></p>
                <p>First, recall the general form of a linear model with nonlinear basis functions:</p>
$$
\hat{y}(\mathbf{x}, \mathbf{w}) = g\left( \sum_{j=1}^M w_j \phi_j(\mathbf{x}) \right)
$$
<br>where $g(\cdot)$ is a nonlinear activation function (e.g., identity for regression, sigmoid for classification), $\phi_j(\mathbf{x})$ are basis functions, and $w_j$ are weights.
<br>In neural networks, the basis functions themselves are parameterized and learned. The network is constructed as a sequence of transformations.
</div>
            <div class="column vertical-top text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/neural-network.png" alt="Two-layer Neural Network" style="max-width: 100%; height: auto;">
                <div class="footnote">Two-layer Neural Network - <a href="https://www.microsoft.com/en-us/research/wp-content/uploads/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf">(Bishop, 2006)</a>.</div>
            </div>
        </div>
    </div>
</div>

## Feedforward Neural Networks

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

## Feedforward Neural Networks

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

## Feedforward Neural Networks

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

## Feedforward Neural Networks

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

## Feedforward Neural Networks

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
<br>Optionally, the output activations $a_k$ can be further transformed using an appropriate activation function to produce the final network outputs $\hat{y}_k$. For example, $\hat{y}_k = a_k$ for regression problems or $\hat{y}_k = \sigma(a_k)$ for binary classification problems.
</div>
            <div class="column vertical-top text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/neural-network.png" alt="Two-layer Neural Network" style="max-width: 100%; height: auto;">
                <div class="footnote">Two-layer Neural Network - <a href="https://www.microsoft.com/en-us/research/wp-content/uploads/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf">(Bishop, 2006)</a>.</div>
            </div>
        </div>
    </div>
</div>

## Feedforward Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <p><b>Feedforward Neural Network:</b></p>
                <p>The overall network function combines these stages. For sigmoidal output unit activation functions, takes the form:</p>
$$
\hat{y}_k(\mathbf{x}, \mathbf{w}) = \sigma\left( \sum_{j=1}^M w_{kj}^{(2)} \, h\left( \sum_{i=1}^D w_{ji}^{(1)} x_i + w_{j0}^{(1)} \right) + w_{k0}^{(2)} \right)
$$
</div>
            <div class="column vertical-top text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/neural-network.png" alt="Two-layer Neural Network" style="max-width: 100%; height: auto;">
                <div class="footnote">Two-layer Neural Network - <a href="https://www.microsoft.com/en-us/research/wp-content/uploads/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf">(Bishop, 2006)</a>.</div>
            </div>
        </div>
    </div>
</div>

## Feedforward Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <p><b>Feedforward Neural Network:</b></p>
                <p>The overall network function combines these stages. For sigmoidal output unit activation functions, takes the form:</p>
$$
\hat{y}_k(\mathbf{x}, \mathbf{w}) = \sigma\left( \sum_{j=1}^M w_{kj}^{(2)} \, h\left( \sum_{i=1}^D w_{ji}^{(1)} x_i + w_{j0}^{(1)} \right) + w_{k0}^{(2)} \right)
$$
<br>The bias parameters can be absorbed:
$$
\hat{y}_k(\mathbf{x}, \mathbf{w}) = \sigma\left( \sum_{j=1}^M w_{kj}^{(2)} \, h\left( \sum_{i=1}^D w_{ji}^{(1)} x_i \right) \right)
$$
</div>
            <div class="column vertical-top text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/neural-network.png" alt="Two-layer Neural Network" style="max-width: 100%; height: auto;">
                <div class="footnote">Two-layer Neural Network - <a href="https://www.microsoft.com/en-us/research/wp-content/uploads/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf">(Bishop, 2006)</a>.</div>
            </div>
        </div>
    </div>
</div>

## Feedforward Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <p><b>Feedforward Neural Network:</b></p>
                <p>The overall network function combines these stages. For sigmoidal output unit activation functions, takes the form:</p>
$$
\hat{y}_k(\mathbf{x}, \mathbf{w}) = \sigma\left( \sum_{j=1}^M w_{kj}^{(2)} \, h\left( \sum_{i=1}^D w_{ji}^{(1)} x_i + w_{j0}^{(1)} \right) + w_{k0}^{(2)} \right)
$$
<br>The bias parameters can be absorbed:
$$
\hat{y}_k(\mathbf{x}, \mathbf{w}) = \sigma\left( \sum_{j=1}^M w_{kj}^{(2)} \, h\left( \sum_{i=1}^D w_{ji}^{(1)} x_i \right) \right)
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

<!-- end SLIDES: -->
