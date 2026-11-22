<!-- SLIDES: -->

## Recurrent network

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 48%">
                <img src="{{ site.url }}/assets/media/diagrams/attention-vs-recurrence-rnn.svg" alt="Recurrent network over five tokens" style="max-height: 420px; max-width: 100%; width: auto;">
            </div>
            <div class="column vertical-middle text-left" style="width: 52%">
                <p><b>Recurrent network:</b> reads one token at a time and keeps a hidden state</p>
                <br>
$$
P(\text{next} \mid \text{prefix}) = \operatorname{softmax}(\mathbf{W}_{hy} \mathbf{h}_t + \mathbf{b}_y)
$$
$$
\mathbf{h}_t = \tanh\left(\mathbf{W}_{hh} \mathbf{h}_{t-1} + \mathbf{W}_{xh} \mathbf{x}_t + \mathbf{b}_h\right)
$$
                <br>
                <p><b>Computes:</b> one new hidden state at each step</p>
                <p><b>Long paths:</b> "the" reaches "nest" only through every hidden state in between</p>
                <p><b>Sequential:</b> step $t$ starts only after $\mathbf{h}_{t-1}$ is ready</p>
            </div>
        </div>
    </div>
</div>

## Convolutional network

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 48%">
                <img src="{{ site.url }}/assets/media/diagrams/attention-vs-recurrence-cnn.svg" alt="Convolutional network over five tokens" style="max-height: 420px; max-width: 100%; width: auto;">
            </div>
            <div class="column vertical-middle text-left" style="width: 52%">
                <p><b>Convolutional network:</b> each unit sees a window of $k$ neighbouring tokens</p>
                <br>
$$
P(\text{next} \mid \text{prefix}) = \operatorname{softmax}(\mathbf{W}_{zy} \mathbf{z}_t + \mathbf{b}_y)
$$
$$
\mathbf{z}_t = \tanh\left(\mathbf{W}[\mathbf{x}_{t-k+1}; \ldots; \mathbf{x}_t] + \mathbf{b}\right)
$$
                <br>
                <p><b>Computes:</b> one output for each window of $k$ neighbouring tokens</p>
                <p><b>Local:</b> two far tokens meet only after several layers</p>
                <p><b>Parallel:</b> every window is computed at the same time</p>
            </div>
        </div>
    </div>
</div>

## Attention

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 48%">
                <img src="{{ site.url }}/assets/media/diagrams/attention-vs-recurrence-attention.svg" alt="Attention over five tokens" style="max-height: 420px; max-width: 100%; width: auto;">
            </div>
            <div class="column vertical-middle text-left" style="width: 52%">
                <p><b>Attention:</b> every token is compared with every earlier token in one step</p>
                <br>
$$
P(\text{next} \mid \text{prefix}) = \operatorname{softmax}(\mathbf{W}_{uy} \mathbf{u}_i + \mathbf{b}_y)
$$
$$
\mathbf{u}_i = \sum_{j \leq i} \alpha_{ij} \mathbf{v}_j
$$
$$
\alpha_{ij} = \text{softmax}_j\left(\frac{\mathbf{q}_i \cdot \mathbf{k}_j}{\sqrt{d_k}}\right) \quad j \leq i
$$
                <br>
                <p><b>Computes:</b> a weight from each token to earlier tokens</p>
                <p><b>Short paths:</b> "the" and "nest" are one step apart</p>
                <p><b>Parallel:</b> all positions are computed at once, which suits GPUs (<a href="https://proceedings.neurips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf">Vaswani et al., 2017</a>)</p>
            </div>
        </div>
    </div>
</div>

## What each architecture computes

<div class="rows" style="height: 100%">
    <div class="row" style="height: 68%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/attention-vs-recurrence-3.svg" alt="Recurrent network, convolutional network and attention" style="max-height: 380px; max-width: 100%; width: auto;">
            </div>
        </div>
    </div>
    <div class="row" style="height: 32%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <p>A recurrent network computes one hidden state per step. A convolutional network computes one output per window of neighbouring tokens. Attention computes a weight from each token to every earlier token.</p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
