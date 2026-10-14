<!-- SLIDES: -->

## Network Architectures

<div class="rows" style="height: 100%">
    <div class="row" style="height: 40%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 33%">
                <img src="{{ site.url }}/assets/media/images/neural-network.png" alt="Feedforward Network" style="max-height: 200px; width: auto;">
            </div>
            <div class="column vertical-middle text-center" style="width: 33%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/rnn-unfold.svg" alt="RNN" style="max-width: 100%; height: auto;">
            </div>
            <div class="column vertical-middle text-center" style="width: 33%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/cnn-typical.png" alt="CNN" style="max-width: 100%; height: auto;">
            </div>
        </div>
    </div>
    <div class="row" style="height: 60%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 33%">
                <p><b>Feedforward (MLP)</b></p>
                <ul>
                    <li><b>Data:</b> feature vectors</li>
                    <li><b>Key idea:</b> layers of weighted sums and activations</li>
                    <li><b>Tasks:</b> regression and classification</li>
                </ul>
            </div>
            <div class="column vertical-top text-left" style="width: 33%">
                <p><b>Recurrent (RNN)</b></p>
                <ul>
                    <li><b>Data:</b> sequences</li>
                    <li><b>Key idea:</b> a hidden state shared across time</li>
                    <li><b>Tasks:</b> forecasting, language, speech</li>
                    <li><b>Extension:</b> LSTMs</li>
                </ul>
            </div>
            <div class="column vertical-top text-left" style="width: 33%">
                <p><b>Convolutional (CNN)</b></p>
                <ul>
                    <li><b>Data:</b> images and grids</li>
                    <li><b>Key idea:</b> shared kernels and pooling</li>
                    <li><b>Tasks:</b> classification, detection, segmentation</li>
                    <li><b>Extension:</b> ResNets</li>
                </ul>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
