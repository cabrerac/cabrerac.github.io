<!-- SLIDES: -->

## Recurrent Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 55%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/rnn-unfold.svg" alt="Unfolded RNN" style="max-width: 100%; height: auto;">
                <div class="footnote">Unfolded recurrent neural network - fdeloche, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons</div>
            </div>
            <div class="column vertical-top text-left" style="width: 45%">
                <p><b>Motivation:</b> sequences have an order and a variable length, and an MLP expects a fixed-size input</p>
                <ul>
                    <li><p><b>Data:</b> time series, text, audio, and sensor signals</p></li>
                    <li><p><b>Tasks:</b> forecasting, sequence classification, language modelling, and speech recognition</p></li>
                    <li><p><b>Key idea:</b> a hidden state carries memory from one time step to the next</p></li>
                </ul>
</div>
        </div>
    </div>
</div>

## Recurrent Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 55%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/rnn-unfold.svg" alt="Unfolded RNN" style="max-width: 100%; height: auto;">
                <div class="footnote">Unfolded recurrent neural network - fdeloche, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons</div>
            </div>
            <div class="column vertical-top text-left" style="width: 45%">
                <p><b>Recurrence:</b> the same weights at every time step $t$</p>
$$
\mathbf{h}_t = \tanh\left(\mathbf{W}_{hh} \mathbf{h}_{t-1} + \mathbf{W}_{xh} \mathbf{x}_t + \mathbf{b}_h\right)
$$
$$
\hat{\mathbf{y}}_t = \mathbf{W}_{hy} \mathbf{h}_t + \mathbf{b}_y
$$
                <p>Weight sharing lets the network process sequences of any length</p>
                <p>Unfolding in time gives a deep feedforward network with shared weights</p>
</div>
        </div>
    </div>
</div>

## Recurrent Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 55%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/rnn-unfold.svg" alt="Unfolded RNN" style="max-width: 100%; height: auto;">
                <div class="footnote">Unfolded recurrent neural network - fdeloche, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons</div>
            </div>
            <div class="column vertical-top text-left" style="width: 45%">
                <p><b>Backpropagation through time:</b> backpropagation on the unfolded network</p>
$$
E = \sum_{t=1}^{T} E_t
$$
$$
\frac{\partial \mathbf{h}_t}{\partial \mathbf{h}_k} = \prod_{i=k+1}^{t} \frac{\partial \mathbf{h}_i}{\partial \mathbf{h}_{i-1}}
$$
                <p>Long products make gradients vanish or explode over long sequences</p>
                <ul>
                    <li><p><b>Gradient clipping:</b> rescale the gradient when its norm is too large</p></li>
                    <li><p><b>Gated units:</b> LSTM and GRU</p></li>
                </ul>
</div>
        </div>
    </div>
</div>

## Recurrent Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 45%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/lstm-cell.svg" alt="LSTM Cell" style="max-width: 100%; height: auto;">
                <div class="footnote">Long short-term memory cell - fdeloche, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons</div>
            </div>
            <div class="column vertical-top text-left" style="width: 55%">
                <p><b>Long short-term memory (LSTM)</b> <a href="https://doi.org/10.1162/neco.1997.9.8.1735" target="_blank" rel="noopener noreferrer">(Hochreiter and Schmidhuber, 1997)</a> adds a cell state $\mathbf{c}_t$ controlled by gates</p>
$$
\mathbf{f}_t, \mathbf{i}_t, \mathbf{o}_t = \sigma\left(\mathbf{W}_{f,i,o} [\mathbf{h}_{t-1}, \mathbf{x}_t] + \mathbf{b}_{f,i,o}\right)
$$
$$
\tilde{\mathbf{c}}_t = \tanh\left(\mathbf{W}_c [\mathbf{h}_{t-1}, \mathbf{x}_t] + \mathbf{b}_c\right)
$$
$$
\mathbf{c}_t = \mathbf{f}_t \odot \mathbf{c}_{t-1} + \mathbf{i}_t \odot \tilde{\mathbf{c}}_t \qquad \mathbf{h}_t = \mathbf{o}_t \odot \tanh(\mathbf{c}_t)
$$
                <p>The additive update of $\mathbf{c}_t$ lets gradients flow over many time steps</p>
</div>
        </div>
    </div>
</div>

## Recurrent Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 30%">
                <p><b>PyTorch</b></p>
                <p>A sequence to one value</p>
                <ul>
                    <li><p><b>Layers:</b> nn.RNN, nn.LSTM, and nn.GRU share one interface</p></li>
                    <li><p><b>Clipping:</b> clip_grad_norm_ before each update</p></li>
                    <li><p><b>Example:</b> a window of ground-motion readings to one prediction</p></li>
                </ul>
            </div>
            <div class="column vertical-top text-left" style="width: 70%">

```python
from torch import nn

class SequenceModel(nn.Module):
    def __init__(self, n_features, n_hidden):
        super().__init__()
        self.lstm = nn.LSTM(n_features, n_hidden, batch_first=True)
        self.head = nn.Linear(n_hidden, 1)

    def forward(self, x):                 # x: (batch, T, n_features)
        out, (h_T, c_T) = self.lstm(x)
        return self.head(h_T[-1])         # last hidden state

# in the training loop
nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
```
</div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
