<!-- SLIDES: -->

## One Hidden Layer

<div class="rows" style="height: 100%">
    <div class="row" style="height: 70%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img class="external-svg" src="{{ site.url }}/assets/media/diagrams/prediction-task-taxonomy.svg" alt="Taxonomy of prediction methods" style="width: 100%; height: 100%">
            </div>
        </div>
    </div>
    <div class="row" style="height: 30%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Linear models:</b> a weighted sum of the attributes, turned into a class or a number.</p>
                <p><b>Trees:</b> questions about one attribute at a time, alone or as many trees that vote.</p>
                <p><b>Neural networks:</b> layers that learn their own attributes from the inputs.</p>
                <p><b>Other methods:</b> the label of the nearest items, or a boundary with the widest margin.</p>
            </div>
        </div>
    </div>
</div>

## One Hidden Layer

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p>A <b>neural network with one hidden layer</b> learns its own attributes from the inputs and then runs a logistic regression on them.</p>
            </div>
        </div>
    </div>
</div>

## One Hidden Layer

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>A small neural network</b></p>
                <p>Inputs, one hidden layer of units, and an output.</p>
                <ul>
                    <li>Each hidden unit is a weighted sum followed by a bend</li>
                    <li>The output is logistic regression on the hidden units</li>
                    <li>Every input must be a scaled number, so categories are one-hot encoded and missing values filled</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/colored-neural-network.svg" alt="A network with an input, a hidden and an output layer" style="height: 360px">
                <div class="footnote">Colored neural network - Glosser.ca, CC BY-SA 3.0 <https://creativecommons.org/licenses/by-sa/3.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## One Hidden Layer

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Forward pass</b></p>
                <p>$$\mathbf{h} = \text{ReLU}(\mathbf{W}_1 \mathbf{x} + \mathbf{b}_1)$$</p>
                <p>$$\mathbf{z} = \mathbf{W}_2 \mathbf{h} + \mathbf{b}_2$$</p>
                <p>$\mathbf{x}$ is the row of inputs. $\mathbf{W}_1$ holds one row of weights per hidden unit and $\mathbf{b}_1$ their intercepts. $\text{ReLU}(a) = \max(0, a)$ is the bend. $\mathbf{W}_2$ and $\mathbf{b}_2$ turn the hidden units $\mathbf{h}$ into scores $\mathbf{z}$.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Output</b></p>
                <p>$$P(y = c \mid \mathbf{x}) = \frac{e^{z_c}}{\sum_{k} e^{z_k}}$$</p>
                <p>The numerator is the score of class $c$, made positive. The denominator adds the same over all classes, so the probabilities add to 1. With two classes this is the logistic function.</p>
            </div>
        </div>
    </div>
</div>

## One Hidden Layer

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Cross-entropy</b></p>
                <p>$$\mathcal{L} = -\sum_{i} \log P(y_i \mid \mathbf{x}_i) + \frac{\lambda}{2} \lVert \mathbf{W} \rVert^2$$</p>
                <p>The sum adds, over the training rows, how unlikely the model found the true label $y_i$. $\lambda$ is the L2 penalty on all weights $\mathbf{W}$.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Backpropagation</b></p>
                <p>A forward pass computes the loss.</p>
                <ul>
                    <li>The chain rule gives the gradient of the loss for every weight, from the output back to the inputs</li>
                    <li>Each weight moves a small step against its gradient</li>
                    <li>Repeat over the training rows until the loss stops falling</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## One Hidden Layer

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <ul>
                    <li><p>$\mathbf{x} = (1, 2)$</p></li>
                    <li><p>$\mathbf{W}_1$ rows $(1, -1)$ and $(0, 1)$, $\mathbf{b}_1 = 0$</p></li>
                    <li><p>One output with weights $(0.5, 1)$ and intercept $-1$</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>$\mathbf{W}_1 \mathbf{x} = (1 - 2,\ 2) = (-1, 2)$, and the bend gives $\mathbf{h} = (0, 2)$. The first unit is off.</p>
                <p>$$z = 0.5 \cdot 0 + 1 \cdot 2 - 1 = 1 \qquad \sigma(1) = 0.73$$</p>
                <p>0.73 is at least 0.5, so the item is a yes.</p>
            </div>
        </div>
    </div>
</div>

## One Hidden Layer

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Set before the results</b></p>
                <ul>
                    <li><p><b>Units:</b> more units fit more, and overfit more</p></li>
                    <li><p><b>Penalty:</b> the L2 weight $\lambda$, alpha in scikit-learn. Few rows call for a stronger penalty</p></li>
                    <li><p><b>Steps:</b> how many passes, and when to stop</p></li>
                    <li><p><b>Seed:</b> the starting weights</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Limits</b></p>
                <ul>
                    <li>On a few hundred rows, a network rarely beats a forest</li>
                    <li>Another seed gives other weights</li>
                    <li>The hidden units have no names, so the reasons are hard to read</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## One Hidden Layer

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 47.5%">

```text
prepare every column as a scaled number
start the weights at random, with a fixed seed
repeat
    forward pass: hidden units, then the output
    loss: cross-entropy plus the penalty
    backward pass: the gradient of every weight
    move each weight a small step
until the loss stops falling
predict on the rows kept apart
```

            </div>
            <div class="column vertical-middle text-left" style="width: 5%">
            </div>
            <div class="column vertical-middle text-left" style="width: 47.5%">

```python
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import make_pipeline

network = make_pipeline(prepare, MLPClassifier(
    hidden_layer_sizes=(8,), alpha=1.0,
    max_iter=2000, random_state=0))
predictions = network.fit(X_train, y_train).predict(X_test)
```

            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
