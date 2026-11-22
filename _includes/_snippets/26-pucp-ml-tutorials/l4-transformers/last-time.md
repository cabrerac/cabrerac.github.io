<!-- SLIDES: -->

## Last Time

<div class="rows" style="height: 100%">
    <div class="row" style="height: 50%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-center" style="width: 33%">
                <img src="{{ site.url }}/assets/media/images/neural-network.png" alt="Feedforward Network" style="max-height: 60px; max-width: 100%; width: auto;">
                <div class="footnote" style="font-size: 0.5em; padding: 0 12px; box-sizing: border-box;">Two-layer Neural Network - <a href="https://www.microsoft.com/en-us/research/wp-content/uploads/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf">(Bishop, 2006)</a></div>
                <p><b>Feedforward (MLP)</b></p>
                <p><b>Tasks:</b> regression and classification</p>
                <p><b>Data:</b> feature vectors</p>
            </div>
            <div class="column vertical-top text-center" style="width: 33%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/rnn-unfold.svg" alt="RNN" style="max-height: 60px; max-width: 100%; width: auto;">
                <div class="footnote" style="font-size: 0.5em; padding: 0 12px; box-sizing: border-box;">Unfolded RNN - fdeloche, CC BY-SA 4.0, via Wikimedia Commons</div>
                <p><b>Recurrent (RNN, LSTM, GRU)</b></p>
                <p><b>Tasks:</b> forecasting, language, speech</p>
                <p><b>Data:</b> sequences</p>
            </div>
            <div class="column vertical-top text-center" style="width: 33%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/autoencoder-schema.png" alt="Autoencoder" style="max-height: 60px; max-width: 100%; width: auto;">
                <div class="footnote" style="font-size: 0.5em; padding: 0 12px; box-sizing: border-box;">Autoencoder schema - Michela Massi, CC BY-SA 4.0, via Wikimedia Commons</div>
                <p><b>Autoencoders and VAEs</b></p>
                <p><b>Tasks:</b> compression, denoising, generation</p>
                <p><b>Data:</b> unlabelled inputs</p>
            </div>
        </div>
    </div>
    <div class="row" style="height: 50%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-center" style="width: 33%">
                <img src="https://upload.wikimedia.org/wikipedia/commons/8/83/Generative_adversarial_network.svg" alt="GAN" style="max-height: 60px; max-width: 100%; width: auto;">
                <div class="footnote" style="font-size: 0.5em; padding: 0 12px; box-sizing: border-box;">GANs - Zhang, Lipton, Li and Smola, CC BY-SA 4.0, via Wikimedia Commons</div>
                <p><b>GANs and diffusion</b></p>
                <p><b>Tasks:</b> generating images and audio</p>
                <p><b>Data:</b> unlabelled samples</p>
            </div>
            <div class="column vertical-top text-center" style="width: 33%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/message-passing.png" alt="GNN" style="max-height: 60px; max-width: 100%; width: auto;">
                <div class="footnote" style="font-size: 0.5em; padding: 0 12px; box-sizing: border-box;">Message passing neural network - NickDiCicco, CC BY-SA 4.0, via Wikimedia Commons</div>
                <p><b>Graph neural networks</b></p>
                <p><b>Tasks:</b> node, link, and graph prediction</p>
                <p><b>Data:</b> graphs</p>
            </div>
            <div class="column vertical-top text-center" style="width: 33%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/cnn-typical.png" alt="CNN" style="max-height: 60px; max-width: 100%; width: auto;">
                <div class="footnote" style="font-size: 0.5em; padding: 0 12px; box-sizing: border-box;">Typical CNN - Aphex34, CC BY-SA 4.0, via Wikimedia Commons</div>
                <p><b>CNNs and ResNets</b></p>
                <p><b>Tasks:</b> classification, detection, segmentation</p>
                <p><b>Data:</b> images and grids</p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->

{% include _snippets/timelines/ai-history-2001-today.md %}
