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
               <p>From simple linear regression to the perceptron:</p>
               <br>
$$
\hat{y} = w_1 x + w_0
$$
$$
\Downarrow
$$
$$
\hat{y} = w_0 + w_1 x_1 + \dots + w_D x_D
$$
$$
\Downarrow
$$
$$
\hat{y} = \mathbf{w}^\top \mathbf{x}
$$
$$
\Downarrow
$$
$$
\hat{y} = \text{Threshold}(\mathbf{w}^\top \mathbf{x})
$$
$$
\Downarrow
$$
$$
\hat{y} = \sigma(\mathbf{w}^\top \mathbf{x})
$$
</div>
        </div>
    </div>
</div>

## Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/regression-hypothesis-space.svg" alt="Hypothesis Space for Regression" style="max-width: 100%; height: auto;">
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
               <p>From simple linear regression to the perceptron:</p>
               <br>
$$
\hat{y} = w_1 x + w_0
$$
$$
\Downarrow
$$
$$
\hat{y} = w_0 + w_1 x_1 + \dots + w_D x_D
$$
$$
\Downarrow
$$
$$
\hat{y} = \mathbf{w}^\top \mathbf{x}
$$
$$
\Downarrow
$$
$$
\hat{y} = \text{Threshold}(\mathbf{w}^\top \mathbf{x})
$$
$$
\Downarrow
$$
$$
\hat{y} = \sigma(\mathbf{w}^\top \mathbf{x})
$$
</div>
        </div>
    </div>
</div>

## Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/xor_problem.png" alt="XOR Problem" style="max-width: 80%; height: auto;">
                <div class="footnote">XOR Problem - Andreas Maier, CC BY 4.0 <https://creativecommons.org/licenses/by/4.0>, via Wikimedia Commons</div>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>XOR is not linearly separable <a href="https://rodsmith.nz/wp-content/uploads/Minsky-and-Papert-Perceptrons.pdf">(Minsky & Papert, 1969)</a></p>
                <br>
                <p><b>Perceptron with a general activation $g(\cdot)$:</b></p>
$$
\hat{y} = g(\mathbf{w}^\top \mathbf{x})
$$
                <br>
                <p><b>Basis functions $\phi(\mathbf{x})$:</b> a richer hypothesis space</p>
$$
\hat{y} = g\left(\mathbf{w}^\top \phi(\mathbf{x})\right)
$$
</div>
        </div>
    </div>
</div>

## Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 40%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Richer hypothesis spaces:</b></p>
$$
\hat{y} = g(\mathbf{w}^\top \mathbf{x})
$$
$$
\Downarrow
$$
$$
\hat{y} = g\left(\mathbf{w}^\top \phi(\mathbf{x})\right)
$$
</div>
        </div>
    </div>
    <div class="row" style="height: 60%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <img src="{{ site.url }}/assets/media/images/basis-functions.png" alt="Basis Functions" style="max-width: 100%; height: auto;">
                <div class="footnote">Basis Functions - <a href="https://www.microsoft.com/en-us/research/wp-content/uploads/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf">(Bishop, 2006)</a>.</div>
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
            <div class="column vertical-top text-left" style="width: 50%">
                <p><b>Multilayer perceptron (MLP)</b></p>
                <br>
$$
\hat{y} = g\left(\mathbf{w}^\top \phi(\mathbf{x})\right)
$$
                <br>
                <ul>
                    <li>Fix the number of basis functions in advance</li>
                    <li>Basis functions are adaptive and their parameters can be updated during training</li>
                </ul>
               <p><b>Training is costly but inference is cheap</b></p>
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
            <div class="column vertical-top text-left" style="width: 50%">
                <p><b>Multilayer perceptron (MLP)</b></p>
                <br>
$$
\hat{y} = g\left(\mathbf{w}^\top \phi(\mathbf{x})\right)
$$
                <br>
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
            <div class="column vertical-top text-left" style="width: 50%">
               <p><b>Multilayer perceptron (MLP)</b></p>
               <br>
$$
\hat{y} = g\left(\mathbf{w}^\top \phi(\mathbf{x})\right)
$$
                <br>
                <p>The Universal Approximation theorem states that a neural network with one hidden layer can approximate any continuous function on a compact subset of $\mathbb{R}^n$, given sufficient neurons in the hidden layer because neural networks form complex decision boundaries through the combination of linear transformations and non-linear activation functions.</p>
            </div>
        </div>
    </div>
</div>

## Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/neural-network.png" alt="Two-layer Neural Network" style="max-width: 100%; height: auto;">
                <div class="footnote">Two-layer Neural Network - <a href="https://www.microsoft.com/en-us/research/wp-content/uploads/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf">(Bishop, 2006)</a>.</div>
            </div>
            <div class="column vertical-top text-left" style="width: 50%">
                <p><b>Feedforward Neural Network:</b></p>
                <ul>
                    <li><p><b>Tasks:</b> regression and classification</p></li>
                    <li><p><b>Data:</b> fixed-length feature vectors such as tabular records and engineered features</p></li>
                    <li><p><b>Key idea:</b> fully connected layers learn the basis functions from data</p></li>
                </ul>
$$
\hat{y} = g\left(\mathbf{w}^\top \phi(\mathbf{x})\right)
$$
               <p><b>Limitation:</b> ignores spatial and temporal structure in the input</p>
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
                <p>First, recall the general form of a linear model with nonlinear basis functions:</p>
$$
\hat{y}(\mathbf{x}, \mathbf{w}) = g\left( \sum_{j=1}^M w_j \phi_j(\mathbf{x}) \right)
$$
<br>
<p>where $g(\cdot)$ is a nonlinear activation function (e.g., identity for regression, sigmoid for classification), $\phi_j(\mathbf{x})$ are basis functions, and $w_j$ are weights.</p>
</div>
            <div class="column vertical-middle text-left" style="width: 50%">
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
                <p>First, recall the general form of a linear model with nonlinear basis functions:</p>
$$
\hat{y}(\mathbf{x}, \mathbf{w}) = g\left( \sum_{j=1}^M w_j \phi_j(\mathbf{x}) \right)
$$
<br>
<p>where $g(\cdot)$ is a nonlinear activation function (e.g., identity for regression, sigmoid for classification), $\phi_j(\mathbf{x})$ are basis functions, and $w_j$ are weights.</p>
<br>
<p>In neural networks, the basis functions themselves are parameterized and learned. The network is constructed as a sequence of transformations.</p>
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
<p>2. Basis function of the inputs or nonlinear activation (hidden layer):</p>
$$
z_j = h(a_j) = \phi_j(\mathbf{x})
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
<p>2. Basis function of the inputs or nonlinear activation (hidden layer):</p>
$$
z_j = h(a_j) = \phi_j(\mathbf{x})
$$
<br>
<p>The designer chooses $h$ (sigmoid, tanh, or ReLU). Every hidden unit uses that same curve.</p>
$$
z_j = h\left(\sum_{i=1}^D w_{ji}^{(1)} x_i + w_{j0}^{(1)}\right)
$$
<p>$w^{(1)}_{ji}$ and $w^{(1)}_{j0}$ set the centre and the width of $z_j$.</p>
<br>
<p>Training learns these weights. The curve $h$ stays the one the designer chose.</p>
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
<p>3. Linear combination of hidden activations (output layer):</p>
$$
a_k = \sum_{j=1}^M w_{kj}^{(2)} z_j + w_{k0}^{(2)}
$$
<p>where $k = 1, \ldots, K$ and $w_{kj}^{(2)}$ are the weights from hidden unit $j$ to output unit $k$, $w_{k0}^{(2)}$ is the bias for output unit $k$. $z_j$ are the learned features. $w^{(2)}$ scales them and does not move the curves.</p>
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
<p>where $k = 1, \ldots, K$ and $w_{kj}^{(2)}$ are the weights from hidden unit $j$ to output unit $k$, $w_{k0}^{(2)}$ is the bias for output unit $k$. $z_j$ are the learned features. $w^{(2)}$ scales them and does not move the curves.</p>
<p>The activations $a_k$ is transformed using an appropriate activation function to produce the final network outputs $\hat{y}_k$. For example, $\hat{y}_k = a_k$ for regression problems or $\hat{y}_k = \sigma(a_k)$ for binary classification problems.</p>
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

## Neural Networks

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

## Neural Networks

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

## Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p>An <b>activation function</b> is a fixed curve applied to one unit's score. On a hidden unit, $h(a_j)$ builds the basis function $z_j$. On an output unit, it turns $a_k$ into the prediction $\hat{y}_k$.</p>
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
                <p><b>Choosing $h$:</b></p>
                <ul>
                    <li><p><b>Nonlinear:</b> a linear $h$ makes the network a linear model</p></li>
                    <li><p><b>Derivative:</b> training follows the slope of $h$. A step is flat almost everywhere</p></li>
                    <li><p><b>Saturation:</b> sigmoid and tanh flatten in the tails. ReLU keeps slope 1 for positive scores, which helps deeper networks</p></li>
                    <li><p><b>Range:</b> tanh is centred at 0. A sigmoid hidden unit is always positive</p></li>
                </ul>
                <p><b>Output activation</b> follows the task. Identity for regression, sigmoid for two classes, softmax for more than two classes.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
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
<p>Given a training set of $N$ example input-output pairs</p>
<br>
$$
(\mathbf{x}_1, \mathbf{y}_1), (\mathbf{x}_2, \mathbf{y}_2), \ldots, (\mathbf{x}_N, \mathbf{y}_N)
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
<p>Given a training set of $N$ example input-output pairs</p>
<br>
$$
(\mathbf{x}_1, \mathbf{y}_1), (\mathbf{x}_2, \mathbf{y}_2), \ldots, (\mathbf{x}_N, \mathbf{y}_N)
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
<p>Given a training set of $N$ example input-output pairs</p>
<br>
$$
(\mathbf{x}_1, \mathbf{y}_1), (\mathbf{x}_2, \mathbf{y}_2), \ldots, (\mathbf{x}_N, \mathbf{y}_N)
$$
<br>Each pair was generated by an unknown function $f$:
<br>
$$
\mathbf{y} = f(\mathbf{x}) + \epsilon
$$
<br>We want to find a hypothesis $\hat{y}$ that minimises the error function:
$$
E(\mathbf{w}) = \frac{1}{2} \sum_{n=1}^N \|\mathbf{y}_n - \hat{\mathbf{y}}(\mathbf{x}_n, \mathbf{w})\|^2
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
p(y \, | \, \mathbf{x}, \mathbf{w}) = \mathcal{N}(y \, | \, \hat{y}(\mathbf{x}, \mathbf{w}), \beta^{-1})
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
p(y \, | \, \mathbf{x}, \mathbf{w}) = \mathcal{N}(y \, | \, \hat{y}(\mathbf{x}, \mathbf{w}), \beta^{-1})
$$
<br>where $\beta$ is the precision (i.e. inverse variance $\sigma^2$).
<br>For an i.i.d. training set, the likelihood function corresponds to:
$$
p(\mathcal{Y} \, | \, \mathcal{X}, \mathbf{w}, \beta) = \prod_{n=1}^N \mathcal{N}(y_n \, | \, \hat{y}(\mathbf{x}_n, \mathbf{w}), \beta^{-1})
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
<br>For an i.i.d. training set, the likelihood function corresponds to:
$$
p(\mathcal{Y} \, | \, \mathcal{X}, \mathbf{w}, \beta) = \prod_{n=1}^N \mathcal{N}(y_n \, | \, \hat{y}(\mathbf{x}_n, \mathbf{w}), \beta^{-1})
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
<br>For an i.i.d. training set, the likelihood function corresponds to:
$$
p(\mathcal{Y} \, | \, \mathcal{X}, \mathbf{w}, \beta) = \prod_{n=1}^N \mathcal{N}(y_n \, | \, \hat{y}(\mathbf{x}_n, \mathbf{w}), \beta^{-1})
$$
<br>Maximising the likelihood function is equivalent to minimising the sum-of-squares error function given by:
$$
E(\mathbf{w}) = \frac{1}{2} \sum_{n=1}^N \left( y_n - \hat{y}(\mathbf{x}_n, \mathbf{w}) \right)^2
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
\hat{y} = \sigma(a) \equiv \frac{1}{1 + \exp(-a)}
$$
We use a single target variable $y$ such that $y=1$ denotes class 1 and $y=0$ denotes class 2.
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
\hat{y} = \sigma(a) \equiv \frac{1}{1 + \exp(-a)}
$$
We use a single target variable $y$ such that $y=1$ denotes class 1 and $y=0$ denotes class 2. We interpret $\hat{y}(\mathbf{x}, \mathbf{w})$ as the conditional probability distribution of targets given inputs:
<br>
$$
p(y|\mathbf{x}, \mathbf{w}) = \hat{y}(\mathbf{x}, \mathbf{w})^y \{1 - \hat{y}(\mathbf{x}, \mathbf{w})\}^{1-y}
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
\hat{y} = \sigma(a) \equiv \frac{1}{1 + \exp(-a)}
$$
We use a single target variable $y$ such that $y=1$ denotes class 1 and $y=0$ denotes class 2. We interpret $\hat{y}(\mathbf{x}, \mathbf{w})$ as the conditional probability distribution of targets given inputs:
<br>
$$
p(y|\mathbf{x}, \mathbf{w}) = \hat{y}(\mathbf{x}, \mathbf{w})^y \{1 - \hat{y}(\mathbf{x}, \mathbf{w})\}^{1-y}
$$
For an i.i.d. training, the error function is the cross-entropy error:
$$
E(\mathbf{w}) = - \sum_{n=1}^N \{ y_n \ln \hat{y}_n + (1-y_n) \ln (1-\hat{y}_n) \}
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
            <div class="column vertical-middle text-left" style="width: 60%">
                <p>We choose any starting point and then compute <b>an estimate of the gradient</b>. We then move a small amount in the steepest downhill direction, repeating until we converge on a point in the weight space with <em>(local)</em> minima loss.</p>
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
<p>The size of the step is given by the parameter $\alpha$, which regulates the behaviour of the gradient descent algorithm. This is a hyperparameter of the regression model we are training, usually called <em>learning rate.</em></p>
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
                <p><b>Error Backpropagation Algorithm:</b></p>
$$
\frac{\partial E_n}{\partial w_{ji}} = \frac{\partial E_n}{\partial a_j}\frac{\partial a_j}{\partial w_{ji}}
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
$$
\frac{\partial E_n}{\partial w_{ji}} = \frac{\partial E_n}{\partial a_j}\frac{\partial a_j}{\partial w_{ji}}
$$
<p><b>1. Forward Pass </b> to compute all activations and outputs for an input vector.</p>
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
$$
\frac{\partial E_n}{\partial w_{ji}} = \frac{\partial E_n}{\partial a_j}\frac{\partial a_j}{\partial w_{ji}}
$$
<p><b>1. Forward Pass </b> to compute all activations and outputs for an input vector.</p>
<p><b>2. Error Evaluation </b> for all outputs using:</p>
$$
\delta_k = \hat{y}_k - y_k
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
$$
\frac{\partial E_n}{\partial w_{ji}} = \frac{\partial E_n}{\partial a_j}\frac{\partial a_j}{\partial w_{ji}}
$$
<p><b>1. Forward Pass </b> to compute all activations and outputs for an input vector.</p>
<p><b>2. Error Evaluation </b> for all outputs using:</p>
$$
\delta_k = \hat{y}_k - y_k
$$
<b>3. Backward Pass:</b> for each hidden unit in the network using:
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
$$
\frac{\partial E_n}{\partial w_{ji}} = \frac{\partial E_n}{\partial a_j}\frac{\partial a_j}{\partial w_{ji}}
$$
<p><b>1. Forward Pass </b> to compute all activations and outputs for an input vector.</p>
<p><b>2. Error Evaluation </b> for all outputs using:</p>
$$
\delta_k = \hat{y}_k - y_k
$$
<b>3. Backward Pass:</b> for each hidden unit in the network using:
$$
\delta_j = h'(a_j) \sum_k w_{kj} \delta_k
$$
<b>4. Derivatives Evaluation </b> for each parameter using:
$$
\frac{\partial E_n}{\partial w_{ji}} = \frac{\partial E_n}{\partial a_j}\frac{\partial a_j}{\partial w_{ji}} = \delta_j z_i
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
w_{ji}^{(l)} \leftarrow w_{ji}^{(l)} - \alpha \frac{\partial E_n}{\partial w_{ji}^{(l)}}
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
w_{ji}^{(l)} \leftarrow w_{ji}^{(l)} - \alpha \frac{\partial E_n}{\partial w_{ji}^{(l)}}
$$
<br>
$$
w_{ji}^{(l)} \leftarrow w_{ji}^{(l)} - \alpha \delta_j z_i
$$
<br>Where $\alpha$ is the learning rate.
</div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
