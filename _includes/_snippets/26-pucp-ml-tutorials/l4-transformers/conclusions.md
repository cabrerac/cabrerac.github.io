<!-- SLIDES: -->

## Conclusions

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-center" style="width: 33%">
                <p><b>Next-token prediction</b></p>
                <img src="{{ site.url }}/assets/media/diagrams/transformer-next-token-2.svg" alt="Next-token prediction" style="max-height: 210px; max-width: 100%; width: auto;">
$$
P(x \mid y_{1:n}), \, x \in V
$$
                <p>The text gives its own targets</p>
            </div>
            <div class="column vertical-top text-center" style="width: 33%">
                <p><b>Tokens and positions</b></p>
                <img src="{{ site.url }}/assets/media/diagrams/transformer-embedding.svg" alt="Embedding lookup" style="max-height: 210px; max-width: 100%; width: auto;">
                <div class="footnote">Token ids from the Qwen2.5-0.5B-Instruct tokeniser.</div>
$$
\mathbf{x}_i = E_{t_i} + \mathbf{p}_i
$$
                <p>Subword tokens, ids and vectors</p>
            </div>
            <div class="column vertical-top text-center" style="width: 33%">
                <p><b>Self-attention</b></p>
                <img src="{{ site.url }}/assets/media/diagrams/transformer-attention-3.svg" alt="Self-attention" style="max-height: 210px; max-width: 100%; width: auto;">
$$
\text{head}_i = \sum_{j \leq i} \alpha_{ij}\mathbf{v}_j
$$
                <p>Weights from queries and keys</p>
            </div>
        </div>
    </div>
</div>

## Conclusions

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-center" style="width: 33%">
                <p><b>Multi-head attention</b></p>
                <img src="{{ site.url }}/assets/media/diagrams/transformer-multihead.svg" alt="Multi-head attention" style="max-height: 210px; max-width: 100%; width: auto;">
$$
a_i = \text{concat}(\text{head}^{1}_i, \ldots, \text{head}^{h}_i) W^O
$$
                <p>Heads can learn different relations</p>
            </div>
            <div class="column vertical-top text-center" style="width: 33%">
                <p><b>Causal mask</b></p>
                <img src="{{ site.url }}/assets/media/diagrams/transformer-causal-mask.svg" alt="Causal mask" style="max-height: 210px; max-width: 100%; width: auto;">
$$
M_{ij} = -\infty \,\, \text{for} \,\, j > i
$$
                <p>No look at future tokens</p>
            </div>
            <div class="column vertical-top text-center" style="width: 33%">
                <p><b>Training</b></p>
                <img src="{{ site.url }}/assets/media/diagrams/transformer-training-shift.svg" alt="Shifted targets" style="max-height: 190px; max-width: 100%; width: auto;">
                <div class="footnote">Qwen2.5-0.5B-Instruct tokeniser.</div>
$$
E = -\frac{1}{T}\sum_{t} \log P(y_{t+1} \mid y_{1:t})
$$
                <p>Cross-entropy at every position</p>
            </div>
        </div>
    </div>
</div>

## Conclusions

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 34%">
                <img src="{{ site.url }}/assets/media/diagrams/transformer-map.svg" alt="Decoder-only transformer" style="max-height: 500px; max-width: 100%; width: auto;">
                <div class="footnote">Decoder-only transformer, after Vaswani et al. (2017).</div>
            </div>
            <div class="column vertical-middle text-center" style="width: 66%">
                <img src="{{ site.url }}/assets/media/diagrams/transformer-families-3.svg" alt="Transformer families" style="max-width: 100%; height: auto;">
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
