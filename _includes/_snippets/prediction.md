<!-- SLIDES: -->

## Supervised Prediction

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>From rules to examples</b></p>
                <p>So far every result came from the data itself. Now someone gives a label.</p>
                <ul>
                    <li>A hand-written rule says yes or no for each item</li>
                    <li>A model learns that rule from labelled examples</li>
                    <li><b>Deep learning:</b> many layers, much data and fast hardware <a href="https://doi.org/10.1038/nature14539" target="_blank" rel="noopener noreferrer">(LeCun et al., 2015)</a></li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/decision-tree.jpg" alt="Decision tree" style="height: 360px">
                <div class="footnote">Decision Tree - Gilgoldm, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Supervised Prediction

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 60%">
                <p><b>Linear models</b></p>
                                <ul>
                                    <li><b>1936:</b> Fisher separates iris species from their measurements with a linear discriminant <a href="https://doi.org/10.1111/j.1469-1809.1936.tb02137.x" target="_blank" rel="noopener noreferrer">(Fisher, 1936)</a></li>
                                    <li><b>1958:</b> Cox writes regression for a binary outcome, logistic regression <a href="https://doi.org/10.1111/j.2517-6161.1958.tb00292.x" target="_blank" rel="noopener noreferrer">(Cox, 1958)</a></li>
                                    <li><b>1958:</b> Rosenblatt's perceptron learns its weights from examples <a href="https://doi.org/10.1037/h0042519" target="_blank" rel="noopener noreferrer">(Rosenblatt, 1958)</a></li>
                                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 40%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/logistic-curve.svg" alt="Logistic curve" style="height: 300px">
                <div class="footnote">Logistic-curve - Qef, Public domain, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Supervised Prediction

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 55%">
                <p><b>Trees and networks</b></p>
                <ul>
                    <li><b>1984:</b> Classification and regression trees, CART <a href="https://doi.org/10.1201/9781315139470" target="_blank" rel="noopener noreferrer">(Breiman et al., 1984)</a></li>
                    <li><b>1986:</b> Backpropagation trains networks with hidden layers <a href="https://doi.org/10.1038/323533a0" target="_blank" rel="noopener noreferrer">(Rumelhart et al., 1986)</a></li>
                    <li><b>2001:</b> Breiman's random forests <a href="https://doi.org/10.1023/A:1010933404324" target="_blank" rel="noopener noreferrer">(Breiman, 2001)</a></li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 45%">
                <img src="{{ site.url }}/assets/media/images/random-forest-explain.png" alt="Random forest" style="height: 340px">
                <div class="footnote">Random forest explain - TseKiChun, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Supervised Prediction

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>A label given, not found</b></p>
                <p>Unsupervised methods find structure in the items.</p>
                <ul>
                    <li>Here each item already has a label, given by a rule or by people.</li>
                    <li>A model learns the label from the item's attributes.</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Supervised Prediction

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Classes and numbers</b></p>
                <p>Here the label is a class, so this is classification.</p>
                <ul>
                    <li>Regression is the same weighted sum, with a number as the label.</li>
                    <li>A good label is not something the attributes contain by construction, that is leakage.</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Supervised Prediction

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Train and test</b></p>
                <ul>
                    <li>Split the labelled items before anything is learned</li>
                    <li><b>fit</b> on the training rows only</li>
                    <li><b>predict</b> on the rows kept apart</li>
                    <li>Count right and wrong answers there, against a baseline</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Why kept apart</b></p>
                <p>A model can remember its training rows.</p>
                <p>Only rows it has never seen show how it will do on new items.</p>
            </div>
        </div>
    </div>
</div>

## Supervised Prediction

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p><b>Supervised prediction</b> learns a given label from the attributes of items whose label is known, and then predicts it for new items.</p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
