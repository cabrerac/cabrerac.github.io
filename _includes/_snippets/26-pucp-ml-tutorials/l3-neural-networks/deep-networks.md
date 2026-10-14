<!-- SLIDES: -->

## Feedforward Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p>Deep learning extends neural networks by using <b>multiple hidden layers</b> to learn hierarchical representations of data, enabling the automatic discovery of complex features.</p>
            </div>
        </div>
    </div>
</div>

## Feedforward Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <img src="https://upload.wikimedia.org/wikipedia/commons/1/15/Neural_Network.svg" alt="Deep Neural Network" style="max-width: 100%; height: auto;">
                <div class="footnote">Deep Neural Network with multiple hidden layers - QuantuMechaniX8, CC0, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Feedforward Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="https://upload.wikimedia.org/wikipedia/commons/1/15/Neural_Network.svg" alt="Deep Neural Network" style="max-width: 100%; height: auto;">
                <div class="footnote">Deep Neural Network with multiple hidden layers - QuantuMechaniX8, CC0, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Feedforward Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <br>
                <p><b>Key Characteristics:</b></p>
                <br>
                <ul>
                    <li><b>Multiple Hidden Layers:</b> 3+ layers for deep architectures</li>
                    <li><b>Hierarchical Features:</b> Each layer learns increasingly abstract representations</li>
                    <li><b>Automatic Feature Learning:</b> No manual feature engineering required</li>
                    <li><b>Representation Learning:</b> Learns useful representations from raw data</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="https://upload.wikimedia.org/wikipedia/commons/1/15/Neural_Network.svg" alt="Deep Neural Network" style="max-width: 100%; height: auto;">
                <div class="footnote">Deep Neural Network with multiple hidden layers - QuantuMechaniX8, CC0, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Feedforward Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <br>
                <p><b>Vanishing and Exploding Gradients:</b> In deep networks, gradients can become very small (vanishing) or very large (exploding) during backpropagation:</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="https://upload.wikimedia.org/wikipedia/commons/1/15/Neural_Network.svg" alt="Deep Neural Network" style="max-width: 100%; height: auto;">
                <div class="footnote">Deep Neural Network with multiple hidden layers - QuantuMechaniX8, CC0, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Feedforward Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <br>
                <p><b>Vanishing and Exploding Gradients:</b> In deep networks, gradients can become very small (vanishing) or very large (exploding) during backpropagation:</p>
                <br>
                <ul>
                    <li><b>Proper Weight Initialization:</b> Xavier/Glorot initialization</li>
                    <li><b>Batch Normalization:</b> Normalize activations during training</li>
                    <li><b>Modern Optimizers:</b> Adam, RMSprop with adaptive learning rates</li>
                    <li><p><b>Regularisation:</b> Dropout, $L_2$, early stopping, and augmentation techniques</p></li>
                    <li><b>Network Architectures:</b> Different architectures for different problems</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="https://upload.wikimedia.org/wikipedia/commons/1/15/Neural_Network.svg" alt="Deep Neural Network" style="max-width: 100%; height: auto;">
                <div class="footnote">Deep Neural Network with multiple hidden layers - QuantuMechaniX8, CC0, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Feedforward Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <p><b>Weight Initialization:</b></p>
                <br>
                <p><b>Xavier/Glorot Initialization:</b></p>
<br>
$$
W_{ij} \sim \mathcal{N}\left(0, \frac{2}{n_{\text{in}} + n_{\text{out}}}\right)
$$
<br>
<p><b>He Initialization (for ReLU):</b></p>
<br>
$$
W_{ij} \sim \mathcal{N}\left(0, \frac{2}{n_{\text{in}}}\right)
$$
<br>Where $n_{\text{in}}$ and $n_{\text{out}}$ are the number of input and output neurons respectively.
</div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="https://upload.wikimedia.org/wikipedia/commons/1/15/Neural_Network.svg" alt="Deep Neural Network" style="max-width: 100%; height: auto;">
                <div class="footnote">Deep Neural Network with multiple hidden layers - QuantuMechaniX8, CC0, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Batch Normalisation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <p><b>Batch normalisation:</b></p>
                <br>
$$
\mu_B = \frac{1}{m} \sum_{i=1}^{m} x_i; \, \, \sigma_B^2 = \frac{1}{m} \sum_{i=1}^{m} (x_i - \mu_B)^2
$$
<br>
$$
\hat{x}_i = \frac{x_i - \mu_B}{\sqrt{\sigma_B^2 + \epsilon}}
$$
<br>
$$
y_i = \gamma \hat{x}_i + \beta
$$
<br>Where $\gamma$ (i.e., scale) and $\beta$ (i.e., shift) are learnable parameters, and $\epsilon$ is a small constant for numerical stability.
</div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="https://upload.wikimedia.org/wikipedia/commons/1/15/Neural_Network.svg" alt="Deep Neural Network" style="max-width: 100%; height: auto;">
                <div class="footnote">Deep Neural Network with multiple hidden layers - QuantuMechaniX8, CC0, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Feedforward Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <p><b>Modern Optimisers:</b></p>
                <br>
                <p>Optimisers train models by efficiently navigating the loss landscape to find optimal parameters. They help in accelerating convergence, avoiding local minima, and improving generalisation.</p>
                <ul>
                    <li><b>Stochastic Gradient Descent (SGD):</b> Updates parameters using a subset of data and reduces computation time.</li>
                    <li><b>Adam:</b> Adaptively adjust the learning rate for each parameter.</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="https://upload.wikimedia.org/wikipedia/commons/a/a3/Gradient_descent.gif" alt="Gradient Descent Algorithm" style="max-width: 100%; height: auto;">
                <div class="footnote">Gradient Descent Algorithm - Jacopo Bertolotti, CC0, via Wikimedia Commons.</div>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
