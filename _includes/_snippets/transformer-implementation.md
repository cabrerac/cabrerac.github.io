<!-- SLIDES: -->

## The Transformer Architecture

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 30%">
                <p>Scaled scores, causal mask and softmax</p>
                <ul>
                    <li><p><b>Q, K, V:</b> one row per token</p></li>
                    <li><p><b>mask:</b> True above the diagonal, where $j > i$</p></li>
                    <li><p><b>masked_fill:</b> those scores become $-\infty$, so softmax gives them weight 0</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 70%">

```python
import torch

def toy_attention(Q, K, V, causal=True):
    T, d = Q.shape[-2], Q.shape[-1]
    scores = Q @ K.transpose(-2, -1) / d ** 0.5           # q_i . k_j / sqrt(d)
    if causal:
        mask = torch.triu(torch.ones(T, T, dtype=torch.bool), diagonal=1)
        scores = scores.masked_fill(mask, float("-inf"))  # j > i
    weights = torch.softmax(scores, dim=-1)               # rows sum to 1
    return weights @ V, weights                           # sum_j alpha_ij v_j
```
</div>
        </div>
    </div>
</div>

## The Transformer Architecture

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 30%">
                <p>One attention head that scores the next character of a window</p>
                <ul>
                    <li><p><b>embed, position:</b> $\mathbf{x}_i = \mathbf{e}_i + \mathbf{p}_i$</p></li>
                    <li><p><b>h + mix:</b> residual connections, with no normalisation in this small model</p></li>
                    <li><p><b>Training:</b> nn.CrossEntropyLoss on the scores and the true next character, then Adam</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 70%">

```python
from torch import nn

class AttentionHead(nn.Module):
    def __init__(self, n_chars, d=32, window=11):
        super().__init__()
        self.embed = nn.Linear(n_chars, d)                # one-hot to vector
        self.position = nn.Parameter(0.1 * torch.randn(window, d))  # learnt p_i
        self.q = nn.Linear(d, d, bias=False)              # W^Q
        self.k = nn.Linear(d, d, bias=False)              # W^K
        self.v = nn.Linear(d, d, bias=False)              # W^V
        self.feed_forward = nn.Sequential(nn.Linear(d, 4 * d), nn.ReLU(), nn.Linear(4 * d, d))
        self.head = nn.Linear(d, n_chars)                 # one score per character

    def forward(self, x):                                 # x: (batch, window, n_chars)
        h = self.embed(x) + self.position
        mix, weights = toy_attention(self.q(h), self.k(h), self.v(h))
        h = h + mix                                       # residual connection
        h = h + self.feed_forward(h)
        return self.head(h[:, -1]), weights               # scores for the next character
```
</div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
