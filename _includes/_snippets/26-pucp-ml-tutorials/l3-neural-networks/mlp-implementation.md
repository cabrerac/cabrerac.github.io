<!-- SLIDES: -->

## Feedforward Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/neural-network.png" alt="Two-layer Neural Network" style="max-width: 100%; height: auto;">
                <div class="footnote">Two-layer Neural Network - <a href="https://www.microsoft.com/en-us/research/wp-content/uploads/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf">(Bishop, 2006)</a>.</div>
            </div>
            <div class="column vertical-top text-left" style="width: 50%">
                <p><b>Multilayer perceptron (MLP)</b></p>
                <ul>
                    <li><p><b>Motivation:</b> learn the basis functions from data instead of fixing them by hand</p></li>
                    <li><p><b>Data:</b> fixed-length feature vectors such as tabular records and engineered features</p></li>
                    <li><p><b>Tasks:</b> regression and classification</p></li>
                    <li><p><b>Limitation:</b> ignores spatial and temporal structure in the input</p></li>
                </ul>
</div>
        </div>
    </div>
</div>

## Feedforward Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 30%">
                <p><b>Forward pass in NumPy</b></p>
                <p>From the practical</p>
$$
a_j = \sum_{i} w_{ji}^{(1)} x_i + w_{j0}^{(1)}
$$
$$
z_j = \tanh(a_j)
$$
$$
\hat{y} = \sigma\left(\sum_{j} w_{j}^{(2)} z_j + w_{0}^{(2)}\right)
$$
            </div>
            <div class="column vertical-top text-left" style="width: 70%">

```python
import numpy as np

def sigmoide(a):
    return 1.0 / (1.0 + np.exp(-a))

def propagar_adelante(X, params):
    a = X @ params["W1"].T + params["b1"]           # a_j
    z = np.tanh(a)                                  # z_j = h(a_j)
    y_hat = sigmoide(z @ params["W2"] + params["b2"])   # output y_hat
    return a, z, y_hat
```
</div>
        </div>
    </div>
</div>

## Feedforward Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 30%">
                <p><b>scikit-learn</b></p>
                <p>From the practical</p>
                <ul>
                    <li><p><b>hidden_layer_sizes:</b> number of hidden layers and units per layer</p></li>
                    <li><p><b>alpha:</b> the $L_2$ penalty $\lambda$, not the learning rate</p></li>
                    <li><p><b>Defaults:</b> ReLU activation and the Adam optimiser</p></li>
                </ul>
            </div>
            <div class="column vertical-top text-left" style="width: 70%">

```python
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

modelo = make_pipeline(
    StandardScaler(),
    MLPClassifier(
        hidden_layer_sizes=(8,),   # one hidden layer, 8 units
        alpha=1e-4,                # L2 penalty
        max_iter=3000,
        random_state=42,
    ),
)
modelo.fit(X_train, y_train)
print(modelo.score(X_test, y_test))
```
</div>
        </div>
    </div>
</div>

## Feedforward Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 30%">
                <p><b>PyTorch</b></p>
                <ul>
                    <li><p><b>Forward pass:</b> model(X)</p></li>
                    <li><p><b>Backpropagation:</b> loss.backward()</p></li>
                    <li><p><b>Update:</b> optimiser.step() applies $\mathbf{W} \leftarrow \mathbf{W} - \alpha \frac{\partial E}{\partial \mathbf{W}}$</p></li>
                </ul>
            </div>
            <div class="column vertical-top text-left" style="width: 70%">

```python
import torch
from torch import nn

model = nn.Sequential(
    nn.Linear(D, 8),   # W(1), b(1)
    nn.Tanh(),         # h(.)
    nn.Linear(8, 1),   # W(2), b(2)
)
loss_fn = nn.BCEWithLogitsLoss()   # sigmoid + cross-entropy
optimiser = torch.optim.SGD(model.parameters(), lr=0.1)

for epoch in range(100):
    optimiser.zero_grad()
    loss = loss_fn(model(X).squeeze(1), y)
    loss.backward()
    optimiser.step()
```
</div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
