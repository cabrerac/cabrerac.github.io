<!-- SLIDES: -->

## Residual Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <p><b>Network Architectures:</b></p>
            <p>The architecture impacts the model's performance. The selection criteria includes: data type, task complexity, computational resources, generalisation needs</p>
            <ul>
                <li><b>Residual Networks (ResNets):</b> Allow gradients to flow through the network.</li>
            </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="https://upload.wikimedia.org/wikipedia/commons/5/59/Resnet.png" alt="ResNet" style="max-width: 100%; height: auto;">
                <div class="footnote">ResNets - Xiaozhu0429, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Residual Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 40%">
                <img src="https://upload.wikimedia.org/wikipedia/commons/5/59/Resnet.png" alt="ResNet" style="max-width: 100%; height: auto;">
                <div class="footnote">ResNets - Xiaozhu0429, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons</div>
            </div>
            <div class="column vertical-top text-left" style="width: 60%">
                <p><b>Motivation:</b> very deep CNNs are hard to train, and training error can grow with depth <a href="https://arxiv.org/abs/1512.03385" target="_blank" rel="noopener noreferrer">(He et al., 2016)</a></p>
                <p><b>Residual block:</b> the layers learn a correction $\mathcal{F}$ to their input</p>
$$
\mathbf{y} = \mathcal{F}(\mathbf{x}, \{\mathbf{W}_i\}) + \mathbf{x}
$$
$$
\frac{\partial \mathbf{y}}{\partial \mathbf{x}} = \frac{\partial \mathcal{F}}{\partial \mathbf{x}} + \mathbf{I}
$$
                <p>The identity term gives the gradient a direct path to early layers</p>
                <p><b>Data and tasks:</b> the same as CNNs, with networks of more than 100 layers</p>
</div>
        </div>
    </div>
</div>

## Residual Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 30%">
                <p><b>PyTorch</b></p>
                <ul>
                    <li><p><b>Skip connection:</b> one addition in forward()</p></li>
                    <li><p><b>Shapes:</b> $\mathcal{F}(\mathbf{x})$ and $\mathbf{x}$ must match</p></li>
                </ul>
            </div>
            <div class="column vertical-top text-left" style="width: 70%">

```python
from torch import nn

class ResidualBlock(nn.Module):
    def __init__(self, channels):
        super().__init__()
        self.conv1 = nn.Conv2d(channels, channels, 3, padding=1)
        self.conv2 = nn.Conv2d(channels, channels, 3, padding=1)
        self.relu = nn.ReLU()

    def forward(self, x):
        f = self.conv2(self.relu(self.conv1(x)))   # F(x)
        return self.relu(f + x)                    # F(x) + x
```
</div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
