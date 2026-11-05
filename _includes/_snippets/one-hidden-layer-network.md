<!-- SLIDES: -->

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
                    <li>Each hidden unit is a weighted sum followed by a bend.</li>
                    <li>The output is logistic regression on the hidden units.</li>
                    <li>So the network learns its own attributes from the inputs.</li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/colored-neural-network.svg" alt="A network with an input, a hidden and an output layer" style="height: 330px">
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
                <p>$\text{ReLU}(a) = \max(0, a)$, applied to each unit.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Output</b></p>
                <p>$$P(y = c \mid \mathbf{x}) = \frac{e^{z_c}}{\sum_{k} e^{z_k}}$$</p>
                <p>Softmax turns the scores $\mathbf{z}$ into probabilities.</p>
                <p>With two classes it is the logistic function.</p>
                <p>Predict the class with the highest probability.</p>
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
                <p>$\lambda$ is the L2 penalty on the weights.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Backpropagation in one slide</b></p>
                <p>Compute the loss with a forward pass.</p>
                <ul>
                    <li>The chain rule gives the gradient of the loss for every weight, from the output back to the inputs.</li>
                    <li>Move each weight a small step against its gradient.</li>
                    <li>Repeat over the training rows until the loss stops falling.</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## One Hidden Layer

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Hyperparameters</b></p>
                <ul>
                    <li><b>Units:</b> how many hidden units. More units fit more, and overfit more</li>
                    <li><p><b>Penalty:</b> the L2 weight $\lambda$ (alpha in scikit-learn). Few rows call for a stronger penalty</p></li>
                    <li><b>Steps:</b> how many passes over the data, and when to stop</li>
                    <li>Scale every column first. Large inputs stall learning</li>
                    <li>Set once before looking at the kept apart rows</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## One Hidden Layer

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Against the other two</b></p>
                <p>A forest needs no scaling and handles mixed columns well.</p>
                <p>On a few hundred rows, a network rarely wins.</p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
