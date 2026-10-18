<!-- SLIDES: -->

## Hyperparameters

<div class="rows" style="height: 100%">
    <div class="row" style="height: 30%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img src="https://upload.wikimedia.org/wikipedia/commons/1/15/Neural_Network.svg" alt="Deep Neural Network" style="height: 170px">
                <div class="footnote">Deep Neural Network with multiple hidden layers - QuantuMechaniX8, CC0, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
    <div class="row" style="height: 70%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <p><b>Architecture</b></p>
                <ul>
                    <li><p><b>Number of layers $L$:</b> depth of the network</p></li>
                    <li><p><b>Hidden units $M$:</b> width of each hidden layer</p></li>
                    <li><p><b>Activation $h(\cdot)$:</b> sigmoid, tanh, or ReLU</p></li>
                </ul>
            </div>
            <div class="column vertical-top text-left" style="width: 50%">
                <p><b>Training</b></p>
                <ul>
                    <li><p><b>Learning rate $\alpha$:</b> size of each gradient descent step</p></li>
                    <li><p><b>Epochs and batch size $m$:</b> passes over the data and examples per update</p></li>
                    <li><p><b>Optimiser:</b> SGD or Adam</p></li>
                    <li><p><b>Regularisation strength $\lambda$:</b> weight of the complexity penalty</p></li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Hyperparameters

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <p><b>Sequences and generative models</b></p>
                <ul>
                    <li><p><b>Hidden state size:</b> dimension of $\mathbf{h}_t$ in RNNs, LSTMs, and GRUs</p></li>
                    <li><p><b>Latent dimension:</b> size of $\mathbf{z}$ in autoencoders, VAEs, and GANs</p></li>
                    <li><p><b>Noise steps $T$ and schedule $\bar{\alpha}_t$:</b> diffusion models</p></li>
                </ul>
            </div>
            <div class="column vertical-top text-left" style="width: 50%">
                <p><b>Graphs and convolutions</b></p>
                <ul>
                    <li><p><b>GNN layers $L$ and aggregation $\bigoplus$:</b> hops reached and how messages combine</p></li>
                    <li><p><b>Kernel size $k$, padding $p$, stride $s$:</b> convolutional layers</p></li>
                    <li><p><b>Residual blocks:</b> depth of a ResNet</p></li>
                </ul>
</div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
