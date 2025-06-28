<!-- SLIDES: -->

## Deep Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p>Deep learning extends neural networks by using <b>multiple hidden layers</b> to learn hierarchical representations of data, enabling the automatic discovery of complex features.</p>
            </div>
        </div>
    </div>
</div>

## Deep Learning

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

## Deep Learning

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

## Deep Learning

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

## Deep Learning

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

## Deep Learning

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
                    <li><b>Regularisation:</b> Dropout, L2, early stopping, and augmentation techniques</li>
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

## Deep Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <p><b>Weight Initialization:</b></p>
                <br>
                <p><b>Xavier/Glorot Initialization:</b></p>
<br>
$$
W_{ij} \sim \mathcal{N}\left(0, \frac{2}{n_{in} + n_{out}}\right)
$$
<br>
<p><b>He Initialization (for ReLU):</b></p>
<br>
$$
W_{ij} \sim \mathcal{N}\left(0, \frac{2}{n_{in}}\right)
$$
<br>Where $n_{in}$ and $n_{out}$ are the number of input and output neurons respectively.
</div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="https://upload.wikimedia.org/wikipedia/commons/1/15/Neural_Network.svg" alt="Deep Neural Network" style="max-width: 100%; height: auto;">
                <div class="footnote">Deep Neural Network with multiple hidden layers - QuantuMechaniX8, CC0, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Deep Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <p><b>Input normalisation:</b></p>
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

## Deep Learning

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
                    <li><b>...</b></li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="https://upload.wikimedia.org/wikipedia/commons/a/a3/Gradient_descent.gif" alt="Gradient Descent Algorithm" style="max-width: 100%; height: auto;">
                <div class="footnote">Gradient Descent Algorithm - Jacopo Bertolotti, CC0, via Wikimedia Commons.</div>
            </div>
        </div>
    </div>
</div>

## Deep Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <p><b>Regularization Techniques:</b></p>
                <br>
                <p><b>Dropout:</b> Randomly deactivate neurons during training</p>
$$
y_i = \begin{cases} \frac{x_i}{1-p} & \text{with probability } 1-p \\ 0 & \text{with probability } p \end{cases}
$$
<br>
<p><b>L2 Regularization:</b> Add penalty to loss function</p>
$$
L_{reg} = L + \lambda \sum_{l=1}^{L} ||\mathbf{W}^{(l)}||_F^2
$$
<br>
<p><b>Early Stopping:</b> Stop training when validation loss increases</p>
<br>
<p><b>Data Augmentation:</b> Create additional training examples through transformations</p>
</div>
        </div>
    </div>
</div>

## Deep Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <p><b>Network Architectures:</b></p>
                <p>The architecture impacts the model's performance. The selection criteria includes: data type, task complexity, computational resources, generalisation needs</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="https://upload.wikimedia.org/wikipedia/commons/1/15/Neural_Network.svg" alt="Deep Neural Network" style="max-width: 100%; height: auto;">
                <div class="footnote">Deep Neural Network with multiple hidden layers - QuantuMechaniX8, CC0, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Deep Learning

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

## Deep Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <p><b>Network Architectures:</b></p>
            <p>The architecture impacts the model's performance. The selection criteria includes: data type, task complexity, computational resources, generalisation needs</p>
            <ul>
                <li><b>Residual Networks (ResNets):</b> Allow gradients to flow through the network.</li>
                <li><b>Convolutional Neural Networks (CNNs):</b> Used in image and video recognition tasks.</li>
            </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="https://upload.wikimedia.org/wikipedia/commons/4/43/Convolution_arithmetic_-_Padding_strides_odd_transposed.gif" alt="Convolutional Network" style="max-width: 100%; height: auto;">
                <div class="footnote">CNNs - Vincent Dumoulin, Francesco Visin, MIT <http://opensource.org/licenses/mit-license.php>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Deep Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <p><b>Network Architectures:</b></p>
            <p>The architecture impacts the model's performance. The selection criteria includes: data type, task complexity, computational resources, generalisation needs</p>
            <ul>
                <li><b>Residual Networks (ResNets):</b> Allow gradients to flow through the network.</li>
                <li><b>Convolutional Neural Networks (CNNs):</b> Used in image and video recognition tasks.</li>
                <li><b>Recurrent Neural Networks (RNNs):</b> Applied in language modeling and sequence prediction tasks.</li>
            </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="https://upload.wikimedia.org/wikipedia/commons/4/44/Hopfield-net-vector.svg" alt="Recurrent Neural Network" style="max-width: 100%; height: auto;">
                <div class="footnote">RNNs - Zawersh, CC BY-SA 3.0 <https://creativecommons.org/licenses/by-sa/3.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Deep Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <p><b>Network Architectures:</b></p>
            <p>The architecture impacts the model's performance. The selection criteria includes: data type, task complexity, computational resources, generalisation needs</p>
            <ul>
                <li><b>Residual Networks (ResNets):</b> Allow gradients to flow through the network.</li>
                <li><b>Convolutional Neural Networks (CNNs):</b> Used in image and video recognition tasks.</li>
                <li><b>Recurrent Neural Networks (RNNs):</b> Applied in language modeling and sequence prediction tasks.</li>
                <li><b>Generative Adversarial Networks (GANs):</b> Used for generating realistic data samples, such as images and audio.</li>
            </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="https://upload.wikimedia.org/wikipedia/commons/8/83/Generative_adversarial_network.svg" alt="Generative Adversarial Network" style="max-width: 200%; height: auto;">
                <div class="footnote">GANs - Zhang, Aston and Lipton, Zachary C. and Li, Mu and Smola, Alexander J., CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: --> 