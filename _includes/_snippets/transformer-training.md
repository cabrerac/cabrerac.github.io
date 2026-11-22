<!-- SLIDES: -->

## The Transformer Architecture

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 48%">
                <p><b>Training process:</b> the targets are the same text shifted one token to the left</p>
$$
E = -\frac{1}{T}\sum_{t=1}^{T} \log P(y_{t+1} \mid y_{1:t})
$$
                <ul>
                    <li><p><b>$E$:</b> the cross-entropy loss, the mean over the $T$ positions</p></li>
                    <li><p><b>$P(y_{t+1} \mid y_{1:t})$:</b> the probability the model gives to the true next token</p></li>
                    <li><p><b>One pass:</b> the causal mask gives all $T$ predictions at once</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 52%">
<img src="{{ site.url }}/assets/media/diagrams/transformer-training-shift.svg" alt="Inputs and shifted targets" style="max-height: 330px; max-width: 100%; width: auto;">
<div class="footnote">Tokens from the <a href="https://arxiv.org/abs/2412.15115">Qwen2.5-0.5B-Instruct</a> tokeniser.</div>
            </div>
        </div>
    </div>
</div>

## The Transformer Architecture

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Training process:</b></p>
                <ul>
                    <li><p><b>Backpropagation:</b> the gradient of $E$ for every weight, from $E$ and $W^Q$, $W^K$, $W^V$, $W^O$ to the FFN, the norms and the output layer</p></li>
                    <li><p><b>Optimisation:</b> Adam updates the weights $\mathbf{W} \leftarrow \mathbf{W} - \alpha \frac{\partial E}{\partial \mathbf{W}}$, with a learning rate that warms up and then decays</p></li>
                    <li><p><b>Regularisation:</b> dropout reduces overfitting</p></li>
                    <li><p><b>Iteration:</b> repeat over batches of text until the loss stops improving</p></li>
                </ul>
                <p>These are the choices of the original transformer (<a href="https://proceedings.neurips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf">Vaswani et al., 2017</a>).</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
<img src="https://upload.wikimedia.org/wikipedia/commons/a/a3/Gradient_descent.gif" alt="Gradient Descent Algorithm" style="max-height: 420px; max-width: 100%; width: auto;">
<div class="footnote">Gradient Descent Algorithm - Jacopo Bertolotti, CC0, via Wikimedia Commons.</div>
            </div>
        </div>
    </div>
</div>

## The Transformer Architecture

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Scale:</b> the same loop on more and more text</p>
                <ul>
                    <li><p><b>A paragraph:</b> four sentences fit in a notebook and train in seconds</p></li>
                    <li><p><b>Original transformer:</b> about 4.5 million English and German sentence pairs (<a href="https://proceedings.neurips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf">Vaswani et al., 2017</a>)</p></li>
                    <li><p><b>Qwen2.5:</b> pretrained on 18 trillion tokens (<a href="https://arxiv.org/abs/2412.15115">Qwen Team, 2024</a>)</p></li>
                </ul>
                <p>Training on large text collections with this task is called <b>pretraining</b>.</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
<img src="{{ site.url }}/assets/media/diagrams/transformer-training-pairs-2.svg" alt="Training pairs from a text" style="max-height: 340px; max-width: 100%; width: auto;">
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
