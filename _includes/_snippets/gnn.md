<!-- SLIDES: -->

## Graph Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/message-passing.png" alt="Message Passing" style="max-width: 62%; height: auto;">
                <div class="footnote">Message passing neural network - NickDiCicco, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons</div>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <ul>
                    <li><p><b>Tasks:</b> node classification, link prediction, and graph classification</p></li>
                    <li><p><b>Data:</b> graphs such as social networks, molecules, and road or sensor networks</p></li>
                    <li><p><b>Key idea:</b> each node updates its representation with messages from its neighbours</p></li>
                </ul>
</div>
        </div>
    </div>
</div>

## Graph Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/message-passing.png" alt="Message Passing" style="max-width: 62%; height: auto;">
                <div class="footnote">Message passing neural network - NickDiCicco, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons</div>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Example:</b> a sensor network, such as seismic stations</p>
                <ul>
                    <li><p><b>Nodes:</b> sensors</p></li>
                    <li><p><b>Edges:</b> nearby sensors are connected</p></li>
                    <li><p><b>Node features:</b> recent readings</p></li>
                    <li><p><b>Task:</b> node regression, such as the shaking at each station</p></li>
                </ul>
</div>
        </div>
    </div>
</div>

## Graph Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 40%">
                <p><b>Python implementation:</b> PyTorch</p>
                <p>A GCN layer in plain PyTorch</p>
                <ul>
                    <li><p><b>PyTorch Geometric:</b> GCNConv implements this layer</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 60%">

```python
import torch
from torch import nn

class GCNLayer(nn.Module):
    def __init__(self, n_in, n_out):
        super().__init__()
        self.linear = nn.Linear(n_in, n_out)          # W(l)

    def forward(self, H, A):                          # H: (N, n_in), A: (N, N)
        A_tilde = A + torch.eye(A.shape[0])           # self-loops
        D_inv_sqrt = torch.diag(A_tilde.sum(dim=1).pow(-0.5))
        A_hat = D_inv_sqrt @ A_tilde @ D_inv_sqrt     # degree normalisation
        return torch.relu(A_hat @ self.linear(H))
```
</div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->

## Graph Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 45%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/message-passing.png" alt="Message Passing" style="max-width: 62%; height: auto;">
                <div class="footnote">Message passing neural network - NickDiCicco, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons</div>
            </div>
            <div class="column vertical-middle text-left" style="width: 55%">
                <p><b>Theory:</b> message passing on a graph with nodes $v$ and neighbours $\mathcal{N}(v)$</p>
$$
\mathbf{h}_v^{(l+1)} = \phi\left(\mathbf{h}_v^{(l)}, \bigoplus_{u \in \mathcal{N}(v)} \psi\left(\mathbf{h}_v^{(l)}, \mathbf{h}_u^{(l)}\right)\right)
$$
                <ul>
                    <li><p><b>Message $\psi$:</b> computed for each neighbour $u$</p></li>
                    <li><p><b>Aggregation $\bigoplus$:</b> sum, mean, or max</p></li>
                    <li><p><b>Update $\phi$:</b> combines the node and its messages</p></li>
                    <li><p><b>Weight sharing:</b> the same $\psi$ and $\phi$ at every node</p></li>
                    <li><p><b>Depth:</b> $L$ layers reach nodes $L$ hops away</p></li>
                </ul>
</div>
        </div>
    </div>
</div>

## Graph Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 45%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/message-passing.png" alt="Message Passing" style="max-width: 62%; height: auto;">
                <div class="footnote">Message passing neural network - NickDiCicco, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons</div>
            </div>
            <div class="column vertical-middle text-left" style="width: 55%">
                <p><b>Graph convolutional network (GCN)</b> <a href="https://arxiv.org/abs/1609.02907" target="_blank" rel="noopener noreferrer">(Kipf and Welling, 2017)</a></p>
$$
\mathbf{H}^{(l+1)} = h\left(\tilde{\mathbf{D}}^{-\frac{1}{2}} \tilde{\mathbf{A}} \tilde{\mathbf{D}}^{-\frac{1}{2}} \mathbf{H}^{(l)} \mathbf{W}^{(l)}\right)
$$
$$
\tilde{\mathbf{A}} = \mathbf{A} + \mathbf{I} \qquad \tilde{D}_{ii} = \sum_{j} \tilde{A}_{ij}
$$
                <ul>
                    <li><p><b>Adjacency matrix $\mathbf{A}$:</b> which nodes are connected</p></li>
                    <li><p><b>Self-loops $\mathbf{I}$:</b> keep each node's own features</p></li>
                    <li><p><b>Degree normalisation:</b> a mean over neighbours</p></li>
                    <li><p><b>Weights $\mathbf{W}^{(l)}$:</b> shared by all nodes</p></li>
                </ul>
</div>
        </div>
    </div>
</div>
