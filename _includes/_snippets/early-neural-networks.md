<!-- SLIDES: -->

## Learning from Examples (1987 - present) - Data-driven Algorithms

<div class="rows" style="height: 100%">
    <div class="row" style="height: 20%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 33%">
                <p><strong>Problem Definition</strong></p>
            </div>
            <div class="column vertical-middle text-center" style="width: 33%">
                <p><strong>Formal Definition</strong></p>
            </div>
            <div class="column vertical-middle text-center" style="width: 33%">
                <p><strong>Computational Representation</strong></p>
            </div>
        </div>
    </div>
    <div class="row" style="height: 80%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 33%">
                <p>
                    Agents cannot be fully pre-programmed. Agent must <b>learn from examples</b> to perform a task.
                </p>
                <img src="{{ site.url }}/assets/media/diagrams/learning-from-data.svg" alt="Learning from data" style="width: 70%; margin-top: 1.0em; background-color: #f6f8fa; padding: 10px; border-radius: 5px;">
                <div class="footnote">Learning from examples: classification problem with decision boundary</div>
            </div>
            <div class="column vertical-middle text-left" style="width: 33%">
                <p>
                    A <b>neural network learning problem</b> is defined by a <em>set of training examples, an architecture of interconnected neurons, an objective function, and a learning algorithm</em>.
                </p>
$$
NN = (D, A, L, \Theta)
$$
$D$: training dataset $\{(x_i, y_i)\}_{i=1}^n$
$A$: network architecture
$L$: loss function
$\Theta$: parameters to learn
            </div>
            <div class="column vertical-middle text-left" style="width: 33%">
                <p>
                    A <b>neural network</b> is a computational graph of interconnected units that transform input features through multiple layers of non-linear transformations.
                </p>
                <p>
                    For each layer $l$:
$$
\begin{align}
z^{(l)} &= W^{(l)}a^{(l-1)} + b^{(l)} \\
a^{(l)} &= \sigma(z^{(l)})
\end{align}
$$
                </p>
                <p>Learns through <b>backpropagation</b>: Computing gradients of error with respect to weights using the chain rule.</p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->