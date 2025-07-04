<!-- SLIDES: -->

## ML Definition

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <div style="font-size: 2em; margin: 40px 0;">
$$\text{model} + \text{data} \stackrel{\text{compute}}{\rightarrow} \text{prediction}$$
</div>
                <div style="margin-top: 30px;">
                </div>
            </div>
        </div>
    </div>
</div>

## The Data Science Process

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/data-science-process.png" alt="Data Science Process" style="height: 500px">
            </div>
        </div>
    </div>
</div>

## Machine Learning Pipeline

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 95%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/data-assess-pipeline.svg" alt="Data Assess Pipeline" style="height: 500px">
            </div>
        </div>
    </div>
</div>

## The Perceptron

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <img src="{{ site.url }}/assets/media/images/perceptron-overview.png" alt="Perceptron Overview" style="max-width: 100%; height: auto;">
                <div class="footnote">Perceptron Overview - Andreas Maier, CC BY 4.0 <https://creativecommons.org/licenses/by/4.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

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

## Deep Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <img src="https://upload.wikimedia.org/wikipedia/commons/1/15/Neural_Network.svg" alt="Deep Neural Network" style="max-width: 100%; height: auto;">
                <div class="footnote">Deep Neural Network with multiple hidden layers - QuantuMechaniX8, CC0, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: --> 



