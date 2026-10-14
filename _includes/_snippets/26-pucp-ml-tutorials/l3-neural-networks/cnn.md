<!-- SLIDES: -->

## Convolutional Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/cnn-typical.png" alt="Typical CNN" style="max-width: 100%; height: auto;">
                <div class="footnote">Typical CNN - Aphex34, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons</div>
            </div>
            <div class="column vertical-top text-left" style="width: 50%">
                <p><b>Motivation:</b> an MLP on images does not scale and ignores spatial structure</p>
$$
224 \times 224 \times 3 = 150{,}528 \text{ inputs}
$$
                <p>A first hidden layer with 1,000 units already needs about 150 million weights</p>
                <p>Neighbouring pixels are related and the same pattern can appear anywhere in the image</p>
</div>
        </div>
    </div>
</div>

## Convolutional Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/cnn-typical.png" alt="Typical CNN" style="max-width: 100%; height: auto;">
                <div class="footnote">Typical CNN - Aphex34, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons</div>
            </div>
            <div class="column vertical-top text-left" style="width: 50%">
                <ul>
                    <li><p><b>Data:</b> grid-structured inputs such as images, video frames, spectrograms, and maps</p></li>
                    <li><p><b>Tasks:</b> image classification, object detection, and segmentation</p></li>
                    <li><p><b>Key ideas:</b> local connectivity, shared weights, and pooling</p></li>
                </ul>
                <p>LeNet read handwritten digits <a href="https://ieeexplore.ieee.org/document/726791" target="_blank" rel="noopener noreferrer">(LeCun et al., 1998)</a></p>
                <p>AlexNet won the ImageNet challenge <a href="https://papers.nips.cc/paper/4824-imagenet-classification-with-deep-convolutional-neural-networks" target="_blank" rel="noopener noreferrer">(Krizhevsky et al., 2012)</a></p>
</div>
        </div>
    </div>
</div>

## Convolutional Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 45%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/convolution-2d-animation.gif" alt="2D Convolution" style="max-width: 80%; height: auto;">
                <div class="footnote">2D Convolution - Michael Plotke, CC BY-SA 3.0 <https://creativecommons.org/licenses/by-sa/3.0>, via Wikimedia Commons</div>
            </div>
            <div class="column vertical-top text-left" style="width: 55%">
                <p><b>Convolution:</b> a kernel $K$ of size $k \times k$ slides over the input $I$</p>
$$
S(i,j) = (I * K)(i,j) = \sum_{m} \sum_{n} I(i+m, j+n) \, K(m,n)
$$
                <ul>
                    <li><p><b>Local connectivity:</b> each output depends on one $k \times k$ patch</p></li>
                    <li><p><b>Weight sharing:</b> the same kernel is used at every position</p></li>
                </ul>
                <p>Deep learning libraries implement this cross-correlation form and call it convolution</p>
</div>
        </div>
    </div>
</div>

## Convolutional Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 40%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/convolution-padding-strides.gif" alt="Padding and Strides" style="max-width: 70%; height: auto;">
                <div class="footnote">Padding and strides - Vincent Dumoulin, Francesco Visin, MIT <http://opensource.org/licenses/mit-license.php>, via Wikimedia Commons</div>
            </div>
            <div class="column vertical-top text-left" style="width: 60%">
                <p><b>Output size</b> for an $n \times n$ input</p>
$$
o = \left\lfloor \frac{n + 2p - k}{s} \right\rfloor + 1
$$
                <ul>
                    <li><p><b>Kernel size $k$:</b> width of the receptive field</p></li>
                    <li><p><b>Padding $p$:</b> zeros added around the border</p></li>
                    <li><p><b>Stride $s$:</b> step between kernel positions</p></li>
                </ul>
                <p>Example: $n = 5$, $k = 3$, $p = 1$, $s = 2$ gives $o = 3$</p>
</div>
        </div>
    </div>
</div>

## Convolutional Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 45%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/conv-layer.png" alt="Convolutional Layer" style="max-width: 100%; height: auto;">
                <div class="footnote">Convolutional layer - Aphex34, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons</div>
            </div>
            <div class="column vertical-top text-left" style="width: 55%">
                <p><b>Feature maps:</b> each of the $C_{\text{out}}$ kernels produces one map</p>
$$
\mathbf{Z}^{(l)}_{c} = h\left( \sum_{c'=1}^{C_{\text{in}}} \mathbf{K}^{(l)}_{c,c'} * \mathbf{Z}^{(l-1)}_{c'} + b^{(l)}_{c} \right)
$$
                <p><b>Parameters per layer:</b> $(k \cdot k \cdot C_{\text{in}} + 1) \cdot C_{\text{out}}$</p>
                <p>Example: $3 \times 3$ kernels with $C_{\text{in}} = 3$ and $C_{\text{out}} = 64$ give $1{,}792$ parameters, for any image size</p>
</div>
        </div>
    </div>
</div>

## Convolutional Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/max-pooling.png" alt="Max Pooling" style="max-width: 100%; height: auto;">
                <div class="footnote">Max pooling - Aphex34, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons</div>
            </div>
            <div class="column vertical-top text-left" style="width: 50%">
                <p><b>Pooling</b> summarises each region $\mathcal{R}_{i,j}$ of a feature map</p>
$$
y_{i,j} = \max_{(m,n) \in \mathcal{R}_{i,j}} x_{m,n}
$$
                <ul>
                    <li><p><b>Downsampling:</b> reduces the spatial size</p></li>
                    <li><p><b>Robustness:</b> tolerates small shifts of a pattern</p></li>
                    <li><p><b>No weights:</b> nothing to learn</p></li>
                </ul>
</div>
        </div>
    </div>
</div>

## Convolutional Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/cnn-typical.png" alt="Typical CNN" style="max-width: 100%; height: auto;">
                <div class="footnote">Typical CNN - Aphex34, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons</div>
            </div>
            <div class="column vertical-top text-left" style="width: 50%">
                <p><b>A typical CNN</b></p>
                <ul>
                    <li><p><b>Convolution and ReLU:</b> extract local features</p></li>
                    <li><p><b>Pooling:</b> downsample</p></li>
                    <li><p><b>Flatten and fully connected layers:</b> classify</p></li>
                    <li><p><b>Softmax output:</b> one probability per class</p></li>
                </ul>
$$
\text{softmax}(\mathbf{a})_k = \frac{e^{a_k}}{\sum_{j=1}^{K} e^{a_j}}
$$
                <p>Early layers detect edges, later layers detect parts and objects</p>
</div>
        </div>
    </div>
</div>

## Convolutional Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 35%">
                <img src="https://upload.wikimedia.org/wikipedia/commons/a/a3/Gradient_descent.gif" alt="Gradient Descent Algorithm" style="max-width: 100%; height: auto;">
                <div class="footnote">Gradient Descent Algorithm - Jacopo Bertolotti, CC0, via Wikimedia Commons.</div>
            </div>
            <div class="column vertical-top text-left" style="width: 65%">
                <p><b>Training:</b> backpropagation and gradient descent, as in the MLP</p>
                <p><b>Loss:</b> cross-entropy for $K$ classes</p>
$$
E(\mathbf{w}) = - \sum_{n=1}^{N} \sum_{k=1}^{K} y_{nk} \ln \hat{y}_{k}(\mathbf{x}_n, \mathbf{w})
$$
                <p><b>Shared weights:</b> the kernel gradient adds the contribution of every position</p>
$$
\frac{\partial E}{\partial K(m,n)} = \sum_{i,j} \frac{\partial E}{\partial S(i,j)} \, I(i+m, j+n)
$$
</div>
        </div>
    </div>
</div>

## Convolutional Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 30%">
                <p><b>PyTorch</b></p>
                <p>RGB images of size ${32} \times 32$ and 10 classes</p>
                <ul>
                    <li><p><b>Training loop:</b> the same as for the MLP</p></li>
                    <li><p><b>Loss:</b> CrossEntropyLoss applies the softmax</p></li>
                </ul>
            </div>
            <div class="column vertical-top text-left" style="width: 70%">

```python
from torch import nn

model = nn.Sequential(
    nn.Conv2d(3, 32, kernel_size=3, padding=1),   # 32 feature maps
    nn.ReLU(),
    nn.MaxPool2d(2),                              # 32x32 to 16x16
    nn.Conv2d(32, 64, kernel_size=3, padding=1),
    nn.ReLU(),
    nn.MaxPool2d(2),                              # 16x16 to 8x8
    nn.Flatten(),
    nn.Linear(64 * 8 * 8, 10),                    # 10 classes
)
loss_fn = nn.CrossEntropyLoss()
```
</div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
