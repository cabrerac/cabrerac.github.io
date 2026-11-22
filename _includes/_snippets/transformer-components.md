<!-- SLIDES: -->

## The Transformer Architecture

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>The transformer is a deep neural network built on the <b>multi-head attention mechanism</b> (<a href="https://proceedings.neurips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf">Vaswani et al., 2017</a>). The original goal was machine translation.</p>
                <ul>
                    <li><p><b>Encoder:</b> reads the whole source sentence</p></li>
                    <li><p><b>Decoder:</b> writes the translation one token at a time</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
<img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/3/34/Transformer%2C_full_architecture.png" alt="Transformer Architecture" style="max-height: 500px; max-width: 100%; width: auto;">
<div class="footnote">Transformer Architecture - dvgodoy, CC BY 4.0 &lt;https://creativecommons.org/licenses/by/4.0&gt;, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## The Transformer Architecture

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 80%">
                <p>Next-token prediction only needs the <b>decoder</b>:</p>
                <ul>
                    <li><p><b>Tokens:</b> cut the text into tokens</p></li>
                    <li><p><b>Embeddings and positions:</b> turn each token into a vector that knows its place</p></li>
                    <li><p><b>Masked multi-head attention:</b> mix in the context from earlier tokens</p></li>
                    <li><p><b>Feed-forward network:</b> transform each vector on its own</p></li>
                    <li><p><b>Residual connections and normalisation:</b> keep training stable</p></li>
                    <li><p><b>Stacking and output:</b> repeat the block $N$ times, then score every token in $V$</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 20%">
<img src="{{ site.url }}/assets/media/diagrams/transformer-map.svg" alt="Decoder-only transformer" style="max-height: 470px; max-width: 100%; width: auto;">
<div class="footnote">After <a href="https://proceedings.neurips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf">Vaswani et al., 2017</a>.</div>
            </div>
        </div>
    </div>
</div>

## The Transformer Architecture

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 80%">
                <p>1. <b>Tokens:</b> a tokeniser cuts the text into tokens from a fixed vocabulary $V$</p>
<img src="{{ site.url }}/assets/media/diagrams/transformer-bpe-2.svg" alt="Words and tokens of a sentence" style="max-height: 240px; max-width: 100%; width: auto;">
                <p>Frequent words stay whole and rare words split into subword pieces. ␣ marks a leading space.</p>
<div class="footnote">Tokens from the <a href="https://arxiv.org/abs/2412.15115">Qwen2.5-0.5B-Instruct</a> tokeniser.</div>
            </div>
            <div class="column vertical-middle text-center" style="width: 20%">
<img src="{{ site.url }}/assets/media/diagrams/transformer-map-tokens.svg" alt="Decoder-only transformer" style="max-height: 470px; max-width: 100%; width: auto;">
<div class="footnote">After <a href="https://proceedings.neurips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf">Vaswani et al., 2017</a>.</div>
            </div>
        </div>
    </div>
</div>

## The Transformer Architecture

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 80%">
                <p>1. <b>Tokens:</b> byte-pair encoding (BPE) (<a href="https://aclanthology.org/P16-1162/">Sennrich et al., 2016</a>)</p>
                <ul>
                    <li><p><b>Start:</b> every character is a token</p></li>
                    <li><p><b>Merge:</b> join the most frequent pair of neighbouring tokens into a new token</p></li>
                    <li><p><b>Repeat:</b> until $V$ reaches the chosen size</p></li>
                </ul>
<img src="{{ site.url }}/assets/media/diagrams/transformer-bpe-examples.svg" alt="Subword pieces of four words" style="max-height: 220px; max-width: 100%; width: auto;">
                <p>No word is out of the vocabulary. A place name like <em>Acarí</em> still splits into known pieces.</p>
<div class="footnote">Tokens from the <a href="https://arxiv.org/abs/2412.15115">Qwen2.5-0.5B-Instruct</a> tokeniser.</div>
            </div>
            <div class="column vertical-middle text-center" style="width: 20%">
<img src="{{ site.url }}/assets/media/diagrams/transformer-map-tokens.svg" alt="Decoder-only transformer" style="max-height: 470px; max-width: 100%; width: auto;">
<div class="footnote">After <a href="https://proceedings.neurips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf">Vaswani et al., 2017</a>.</div>
            </div>
        </div>
    </div>
</div>

## The Transformer Architecture

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 80%">
                <p>1. <b>Tokens:</b> each token becomes an integer id, its position in $V$</p>
<img src="{{ site.url }}/assets/media/diagrams/transformer-bpe-3.svg" alt="Words, tokens and token ids" style="max-height: 250px; max-width: 100%; width: auto;">
                <p>The Qwen2.5 tokeniser has 151,665 tokens, so every id is a number between 0 and 151,664.</p>
<div class="footnote">Tokens and ids from the <a href="https://arxiv.org/abs/2412.15115">Qwen2.5-0.5B-Instruct</a> tokeniser.</div>
            </div>
            <div class="column vertical-middle text-center" style="width: 20%">
<img src="{{ site.url }}/assets/media/diagrams/transformer-map-tokens.svg" alt="Decoder-only transformer" style="max-height: 470px; max-width: 100%; width: auto;">
<div class="footnote">After <a href="https://proceedings.neurips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf">Vaswani et al., 2017</a>.</div>
            </div>
        </div>
    </div>
</div>

## The Transformer Architecture

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 42%">
                <p>2. <b>Token embedding:</b> each id selects one row of a learnt matrix $E$</p>
$$
\mathbf{e}_i = E_{t_i}
$$
                <ul>
                    <li><p><b>$t_i$:</b> the id of the token at position $i$</p></li>
                    <li><p><b>$E$:</b> $|V|$ rows and $d$ columns, learnt during training ($d = 896$ in Qwen2.5-0.5B)</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 40%">
<img src="{{ site.url }}/assets/media/diagrams/transformer-embedding.svg" alt="Embedding lookup" style="max-height: 420px; max-width: 100%; width: auto;">
            </div>
            <div class="column vertical-middle text-center" style="width: 18%">
<img src="{{ site.url }}/assets/media/diagrams/transformer-map-embed.svg" alt="Decoder-only transformer" style="max-height: 470px; max-width: 100%; width: auto;">
<div class="footnote">After <a href="https://proceedings.neurips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf">Vaswani et al., 2017</a>.</div>
            </div>
        </div>
    </div>
</div>

## The Transformer Architecture

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 42%">
                <p>2. <b>Positional encoding:</b> attention has no sense of order, so each vector gets a position vector</p>
$$
\mathbf{x}_i = \mathbf{e}_i + \mathbf{p}_i
$$
                <p>The original transformer uses sines and cosines of different frequencies, $p_{i,2k} = \sin(i / 10000^{2k/d})$. Many models learn $\mathbf{p}_i$ instead.</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 40%">
<img src="{{ site.url }}/assets/media/diagrams/transformer-positional.svg" alt="Sinusoidal positional encoding" style="max-height: 420px; max-width: 100%; width: auto;">
            </div>
            <div class="column vertical-middle text-center" style="width: 18%">
<img src="{{ site.url }}/assets/media/diagrams/transformer-map-pos.svg" alt="Decoder-only transformer" style="max-height: 470px; max-width: 100%; width: auto;">
<div class="footnote">After <a href="https://proceedings.neurips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf">Vaswani et al., 2017</a>.</div>
            </div>
        </div>
    </div>
</div>

## The Transformer Architecture

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 42%">
                <p>3. <b>Self-attention:</b> each input vector plays three roles</p>
$$
\mathbf{q}_i = W^{Q}\mathbf{x}_i, \quad \mathbf{k}_i = W^{K}\mathbf{x}_i, \quad \mathbf{v}_i = W^{V}\mathbf{x}_i
$$
                <ul>
                    <li><p><b>Query $\mathbf{q}_i$:</b> what the current token is looking for</p></li>
                    <li><p><b>Key $\mathbf{k}_j$:</b> what an earlier token offers to match</p></li>
                    <li><p><b>Value $\mathbf{v}_j$:</b> what an earlier token passes on</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 40%">
<img src="{{ site.url }}/assets/media/diagrams/transformer-attention-1.svg" alt="Queries, keys and values" style="max-height: 420px; max-width: 100%; width: auto;">
            </div>
            <div class="column vertical-middle text-center" style="width: 18%">
<img src="{{ site.url }}/assets/media/diagrams/transformer-map-attn.svg" alt="Decoder-only transformer" style="max-height: 470px; max-width: 100%; width: auto;">
<div class="footnote">After <a href="https://proceedings.neurips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf">Vaswani et al., 2017</a>.</div>
            </div>
        </div>
    </div>
</div>

## The Transformer Architecture

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 42%">
                <p>3. <b>Self-attention:</b> the weight of token $j$ for token $i$</p>
$$
\alpha_{ij} = \text{softmax}_j\left(\frac{\mathbf{q}_i \cdot \mathbf{k}_j}{\sqrt{d_k}}\right) \quad \forall \, j \leq i
$$
                <ul>
                    <li><p><b>$\mathbf{q}_i \cdot \mathbf{k}_j$:</b> how well key $j$ matches query $i$</p></li>
                    <li><p><b>$\sqrt{d_k}$:</b> the square root of the key size keeps the scores in a range where softmax still learns</p></li>
                    <li><p><b>$\alpha_{ij}$:</b> the share of attention that token $i$ gives to token $j$, summing to 1 over $j$</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 40%">
<img src="{{ site.url }}/assets/media/diagrams/transformer-attention-2.svg" alt="Attention weights" style="max-height: 420px; max-width: 100%; width: auto;">
            </div>
            <div class="column vertical-middle text-center" style="width: 18%">
<img src="{{ site.url }}/assets/media/diagrams/transformer-map-attn.svg" alt="Decoder-only transformer" style="max-height: 470px; max-width: 100%; width: auto;">
<div class="footnote">After <a href="https://proceedings.neurips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf">Vaswani et al., 2017</a>.</div>
            </div>
        </div>
    </div>
</div>

## The Transformer Architecture

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 42%">
                <p>3. <b>Self-attention:</b> the output is a weighted sum of the values</p>
$$
\text{head}_i = \sum_{j=1}^{i} \alpha_{ij}\mathbf{v}_j \qquad a_i = \text{head}_i W^O
$$
                <ul>
                    <li><p><b>$\text{head}_i$:</b> the meaning of token $i$, updated with its context</p></li>
                    <li><p><b>$W^O$:</b> reshapes the output of the head</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 40%">
<img src="{{ site.url }}/assets/media/diagrams/transformer-attention-3.svg" alt="Attention output" style="max-height: 420px; max-width: 100%; width: auto;">
            </div>
            <div class="column vertical-middle text-center" style="width: 18%">
<img src="{{ site.url }}/assets/media/diagrams/transformer-map-attn.svg" alt="Decoder-only transformer" style="max-height: 470px; max-width: 100%; width: auto;">
<div class="footnote">After <a href="https://proceedings.neurips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf">Vaswani et al., 2017</a>.</div>
            </div>
        </div>
    </div>
</div>

## The Transformer Architecture

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 42%">
                <p>3. <b>Multi-head attention:</b> $h$ heads in parallel, each with its own $W^Q$, $W^K$ and $W^V$</p>
$$
a_i = \text{concat}(\text{head}^{1}_i, \ldots, \text{head}^{h}_i)\, W^O
$$
                <p>Each head can focus on a different relation, for example adjectives and nouns, or verbs and subjects. These relations are learnt from the data. Qwen2.5-0.5B has 14 heads in each block.</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 40%">
<img src="{{ site.url }}/assets/media/diagrams/transformer-multihead.svg" alt="Multi-head attention" style="max-height: 420px; max-width: 100%; width: auto;">
            </div>
            <div class="column vertical-middle text-center" style="width: 18%">
<img src="{{ site.url }}/assets/media/diagrams/transformer-map-attn.svg" alt="Decoder-only transformer" style="max-height: 470px; max-width: 100%; width: auto;">
<div class="footnote">After <a href="https://proceedings.neurips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf">Vaswani et al., 2017</a>.</div>
            </div>
        </div>
    </div>
</div>

## The Transformer Architecture

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 42%">
                <p>4. <b>Feed-forward network:</b> a two-layer network applied to each position on its own</p>
$$
\text{FFN}(\mathbf{x}_i) = \text{ReLU}(\mathbf{x}_i \mathbf{W}_1 + \mathbf{b}_1)\mathbf{W}_2 + \mathbf{b}_2
$$
                <p>Attention mixes tokens and the FFN transforms each mixed vector. The original transformer goes from 512 to 2048 numbers and back (<a href="https://proceedings.neurips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf">Vaswani et al., 2017</a>).</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 40%">
<img src="{{ site.url }}/assets/media/diagrams/transformer-ffn.svg" alt="Position-wise feed-forward network" style="max-height: 420px; max-width: 100%; width: auto;">
            </div>
            <div class="column vertical-middle text-center" style="width: 18%">
<img src="{{ site.url }}/assets/media/diagrams/transformer-map-ffn.svg" alt="Decoder-only transformer" style="max-height: 470px; max-width: 100%; width: auto;">
<div class="footnote">After <a href="https://proceedings.neurips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf">Vaswani et al., 2017</a>.</div>
            </div>
        </div>
    </div>
</div>

## The Transformer Architecture

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 42%">
                <p>5. <b>Residual connections and layer normalisation:</b></p>
                <ul>
                    <li><p><b>Residual:</b> keeps what the token originally meant while adding the context</p></li>
                    <li><p><b>Normalisation:</b> keeps the values in a range that helps gradient descent</p></li>
                </ul>
$$
\text{LayerNorm}(\mathbf{x}) = \frac{\mathbf{x} - \mu}{\sigma + \epsilon} \cdot \gamma + \beta
$$
                <p>$\mu$ and $\sigma$ are the mean and standard deviation of $\mathbf{x}$, $\epsilon$ avoids a division by zero, and $\gamma$ and $\beta$ are learnt.</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 40%">
<img src="{{ site.url }}/assets/media/diagrams/transformer-residual-norm.svg" alt="Residual connection and layer normalisation" style="max-height: 420px; max-width: 100%; width: auto;">
            </div>
            <div class="column vertical-middle text-center" style="width: 18%">
<img src="{{ site.url }}/assets/media/diagrams/transformer-map-norm.svg" alt="Decoder-only transformer" style="max-height: 470px; max-width: 100%; width: auto;">
<div class="footnote">After <a href="https://proceedings.neurips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf">Vaswani et al., 2017</a>.</div>
            </div>
        </div>
    </div>
</div>

## The Transformer Architecture

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 42%">
                <p>6. <b>Causal mask:</b> a token never sees the tokens it has to predict</p>
$$
\alpha_{ij} = \text{softmax}_j\left(\frac{\mathbf{q}_i \cdot \mathbf{k}_j}{\sqrt{d_k}} + M_{ij}\right), \quad M_{ij} = \begin{cases} 0 & j \leq i \\ -\infty & j > i \end{cases}
$$
                <p>With the mask, one pass over a text trains every position at the same time.</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 40%">
<img src="{{ site.url }}/assets/media/diagrams/transformer-causal-mask.svg" alt="Causal mask" style="max-height: 420px; max-width: 100%; width: auto;">
            </div>
            <div class="column vertical-middle text-center" style="width: 18%">
<img src="{{ site.url }}/assets/media/diagrams/transformer-map-attn-mask.svg" alt="Decoder-only transformer" style="max-height: 470px; max-width: 100%; width: auto;">
<div class="footnote">After <a href="https://proceedings.neurips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf">Vaswani et al., 2017</a>.</div>
            </div>
        </div>
    </div>
</div>

## The Transformer Architecture

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 42%">
                <p>6. <b>Causal mask:</b> the weights of one head of a pretrained model</p>
                <ul>
                    <li><p><b>Grey cells:</b> masked, weight 0</p></li>
                    <li><p><b>Rows:</b> the weights of each query sum to 1</p></li>
                    <li><p><b>Layer 9, head 5:</b> the pieces of <em>movió</em> put most of their weight on <em>or</em>, the last piece of <em>temblor</em> (0.51 and 0.65)</p></li>
                </ul>
                <p>Other heads look at the previous token, and many put almost all their weight on the first token.</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 58%">
<img src="{{ site.url }}/assets/media/diagrams/transformer-attention-heatmap.svg" alt="Attention weights of one head" style="max-height: 500px; max-width: 100%; width: auto;">
<div class="footnote">Layer 9, head 5 (counting from 0) of <a href="https://arxiv.org/abs/2412.15115">Qwen2.5-0.5B-Instruct</a> on <em>el temblor movió la estación cercana.</em></div>
            </div>
        </div>
    </div>
</div>

## The Transformer Architecture

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 80%">
                <p>7. <b>Stacking:</b> the block repeats $N$ times, and the output of one block is the input of the next</p>
                <ul>
                    <li><p><b>Original transformer:</b> $N = 6$ blocks, 8 heads, $d = 512$ (<a href="https://proceedings.neurips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf">Vaswani et al., 2017</a>)</p></li>
                    <li><p><b>Qwen2.5-0.5B:</b> $N = 24$ blocks, 14 heads, $d = 896$, about 494 million parameters</p></li>
                </ul>
                <p>Each block has its own weights. Every token keeps a vector of size $d$ from the first block to the last.</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 20%">
<img src="{{ site.url }}/assets/media/diagrams/transformer-map-stack.svg" alt="Decoder-only transformer" style="max-height: 470px; max-width: 100%; width: auto;">
<div class="footnote">After <a href="https://proceedings.neurips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf">Vaswani et al., 2017</a>.</div>
            </div>
        </div>
    </div>
</div>

## The Transformer Architecture

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 42%">
                <p>8. <b>Output layer:</b> a linear layer and a softmax turn the last vector into probabilities</p>
$$
P(x = w \mid y_{1:n}) = \frac{e^{z_w}}{\sum_{v \in V} e^{z_v}}
$$
                <ul>
                    <li><p><b>$z_w$:</b> the score (logit) of token $w$ from the linear layer</p></li>
                    <li><p><b>Softmax:</b> values between 0 and 1 that sum to 1 over $V$</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 40%">
<img src="{{ site.url }}/assets/media/diagrams/transformer-output.svg" alt="Output layer" style="max-height: 420px; max-width: 100%; width: auto;">
            </div>
            <div class="column vertical-middle text-center" style="width: 18%">
<img src="{{ site.url }}/assets/media/diagrams/transformer-map-output.svg" alt="Decoder-only transformer" style="max-height: 470px; max-width: 100%; width: auto;">
<div class="footnote">After <a href="https://proceedings.neurips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf">Vaswani et al., 2017</a>.</div>
            </div>
        </div>
    </div>
</div>

## The Transformer Architecture

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
          <div class="column vertical-middle text-center" style="width: 100%">
            <img class="external-svg" src="{{ site.url }}/assets/media/images/transformer-decoder-sequence.png" alt="Transformer Decoder" style="max-height: 500px; max-width: 100%; width: auto;">
            <div class="footnote">Transformer Decoder Architecture - (<a href="https://web.stanford.edu/~jurafsky/slp3/9.pdf">Jurafsky et al., 2025</a>)</div>
          </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
