<!-- SLIDES: -->

## Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 40%">
                <p><b>Python implementation:</b> scikit-learn</p>
                <ul>
                    <li><p><b>hidden_layer_sizes:</b> number of hidden layers and units per layer</p></li>
                    <li><p><b>alpha:</b> the $L_2$ penalty $\lambda$, not the learning rate</p></li>
                    <li><p><b>Defaults:</b> ReLU activation and the Adam optimiser</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 60%">

```python
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

model = make_pipeline(
    StandardScaler(),
    MLPClassifier(
        hidden_layer_sizes=(8,),   # one hidden layer, 8 units
        alpha=1e-4,                # L2 penalty
        max_iter=3000,
        random_state=42,
    ),
)
model.fit(X_train, y_train)
print(model.score(X_test, y_test))
```
</div>
        </div>
    </div>
</div>

## Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 40%">
                <p><b>Python implementation:</b> PyTorch</p>
                <ul>
                    <li><p><b>Forward pass:</b> model(X)</p></li>
                    <li><p><b>Backpropagation:</b> loss.backward()</p></li>
                    <li><p><b>Update:</b> optimiser.step() applies $\mathbf{W} \leftarrow \mathbf{W} - \alpha \frac{\partial E}{\partial \mathbf{W}}$</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 60%">

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
