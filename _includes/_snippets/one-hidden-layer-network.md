<!-- SLIDES: -->

## Neural Network

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p>A <b>neural network with one hidden layer</b> learns its own attributes from the inputs and then runs a logistic regression on them.</p>
            </div>
        </div>
    </div>
</div>

## Neural Network

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>Inputs, one hidden layer of units, and an output.</p>
                <ul>
                    <li><p>Each hidden unit is a weighted sum followed by a bend</p></li>
                    <li><p>The output turns the hidden units into a probability</p></li>
                    <li><p>Every input must be a scaled number, so categories are one-hot encoded and missing values filled</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/colored-neural-network.svg" alt="A network with an input, a hidden and an output layer" style="height: auto; max-width: 100%; max-height: 90%;">
                <div class="footnote">Colored neural network - Glosser.ca, CC BY-SA 3.0 <https://creativecommons.org/licenses/by-sa/3.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Neural Network

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Forward pass</b></p>
                <br>
$$
\hat{y}_k(\mathbf{x}, \mathbf{w}) = \sigma\left( \sum_{j=1}^M w_{kj}^{(2)} \, h\left( \sum_{i=1}^D w_{ji}^{(1)} x_i + w_{j0}^{(1)} \right) + w_{k0}^{(2)} \right)
$$
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/neural-network.png" alt="Two-layer Neural Network" style="height: auto; max-width: 100%;">
                <div class="footnote">Two-layer Neural Network - <a href="https://www.microsoft.com/en-us/research/wp-content/uploads/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf">(Bishop, 2006)</a>.</div>
            </div>
            </div>
        </div>
    </div>
</div>

## Neural Network

<div class="rows" style="height: 100%">
    <div class="row" style="height: 50%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%; height: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/nn-output-lr.svg" alt="Logistic regression next to the output layer of the network" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
    <div class="row" style="height: 50%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%; height: 100%">
                <p><b>The output layer is a logistic regression</b></p>
                <br>
$$
P(y = 1 \mid \mathbf{x}) = \sigma(\mathbf{w}_2 \cdot \mathbf{h} + b_2)
$$
                <ul>
                    <li><p>The same formula as logistic regression, with $\mathbf{h}$ in place of $\mathbf{x}$</p></li>
                    <li><p>The hidden layer learns the columns. The output layer weighs them, as logistic regression weighs attributes</p></li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Neural Network

<div class="rows" style="height: 100%">
    <div class="row" style="height: 50%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%; height: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/nn-backprop-1.svg" alt="The forward pass computes the loss" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
    <div class="row" style="height: 50%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%; height: 100%">
                <p><b>Cross-entropy</b> measures how unlikely the true labels were. With two classes it is the log loss of logistic regression.</p>
                <br>
$$
\mathcal{L} = -\sum_{i} \log P(y_i \mid \mathbf{x}_i) + \frac{\lambda}{2} \lVert \mathbf{W} \rVert^2
$$
                <p><b>$y_i$</b> is the true label of training row $i$, and <b>$\lambda$</b> is the L2 penalty on all weights $\mathbf{W}$.</p>
            </div>
        </div>
    </div>
</div>

## Neural Network

<div class="rows" style="height: 100%">
    <div class="row" style="height: 63%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 50%; height: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/nn-backprop-2.svg" alt="The gradients flow back from the loss" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
            <div class="column vertical-middle text-center" style="width: 50%; height: 100%">
                <img src="https://upload.wikimedia.org/wikipedia/commons/a/a3/Gradient_descent.gif" alt="Gradient Descent Algorithm" style="max-width: 100%; height: auto;">
                <div class="footnote">Gradient Descent Algorithm - Jacopo Bertolotti, CC0, via Wikimedia Commons.</div>
            </div>
        </div>
    </div>
    <div class="row" style="height: 37%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%; height: 100%">
                <p><b>Backpropagation</b></p>
                <ul>
                    <li><p><b>Cross-entropy:</b> the forward pass computes the loss from the true labels</p></li>
                    <li><p><b>Chain rule:</b> gradients flow backward from the loss to every weight</p></li>
                    <li><p><b>Update:</b> each weight moves a small step against its gradient until the loss stops falling</p></li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Neural Network

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Set before the results</b></p>
                <ul>
                    <li><p><b>Units:</b> more units fit more, and overfit more</p></li>
                    <li><p><b>Penalty:</b> $\lambda$, alpha in scikit-learn. Few rows call for a stronger penalty</p></li>
                    <li><p><b>Steps and seed:</b> how many passes, when to stop, and the starting weights</p></li>
                </ul>
                <p><b>Limits</b></p>
                <ul>
                    <li><p>The hidden units have no names, so the reasons are hard to read</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/colored-neural-network.svg" alt="A network with an input, a hidden and an output layer" style="height: auto; max-width: 100%; max-height: 90%;">
                <div class="footnote">Colored neural network - Glosser.ca, CC BY-SA 3.0 <https://creativecommons.org/licenses/by-sa/3.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Neural Network

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 47.5%; font-size: 0.85em">

```text
prepare every column as a scaled number
start the weights at random, fixed seed
repeat
    forward pass: hidden units, output
    loss: cross-entropy plus the penalty
    backward pass: every gradient
    move each weight a small step
until the loss stops falling
predict on the rows kept apart
```
</div>
            <div class="column vertical-middle text-left" style="width: 4%"></div>
            <div class="column vertical-middle text-center" style="width: 47.5%; height: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/nn-backprop-2.svg" alt="The gradients flow back from the loss" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
</div>

## Neural Network

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 38%">
                <p><b>Python usage:</b> scikit-learn</p>
                <p>One hidden layer of 8 units, with the same preparation</p>
                <ul>
                    <li><p><b>hidden_layer_sizes:</b> (8,), one layer of 8 units</p></li>
                    <li><p><b>alpha:</b> the penalty $\lambda = 1.0$</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 4%"></div>
            <div class="column vertical-middle text-left" style="width: 58%; font-size: 0.85em">

```python
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import make_pipeline

model = make_pipeline(prepare, MLPClassifier(
    hidden_layer_sizes=(8,), alpha=1.0,
    max_iter=3000, random_state=7))
model.fit(X_train, y_train)
predictions = model.predict(X_test)
```
</div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
