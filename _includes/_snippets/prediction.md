<!-- SLIDES: -->

## Supervised Prediction

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>A label given, not found</b></p>
                <ul>
                    <li>Unsupervised methods find structure in the items</li>
                    <li>Here each item already has a label, given by a rule or by people</li>
                    <li>A model learns the label from the item's attributes</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Classes and numbers</b></p>
                <ul>
                    <li>Here the label is a class, so this is classification</li>
                    <li>Regression is the same weighted sum, with a number as the label</li>
                    <li>A good label is not something the attributes contain by construction, that is leakage</li>
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
                <ul>
                    <li>A model can remember its training rows</li>
                    <li>Only rows it has never seen show how it will do on new items</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Prediction History

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Linear models</b></p>
                <ul>
                    <li><b>1936</b> - Fisher separates iris species from their measurements with a linear discriminant <a href="https://doi.org/10.1111/j.1469-1809.1936.tb02137.x" target="_blank" rel="noopener noreferrer">(Fisher, 1936)</a></li>
                    <li><b>1958</b> - Cox writes regression for a binary outcome, logistic regression <a href="https://doi.org/10.1111/j.2517-6161.1958.tb00292.x" target="_blank" rel="noopener noreferrer">(Cox, 1958)</a></li>
                    <li><b>1958</b> - Rosenblatt's perceptron learns its weights from examples <a href="https://doi.org/10.1037/h0042519" target="_blank" rel="noopener noreferrer">(Rosenblatt, 1958)</a></li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Trees and networks</b></p>
                <ul>
                    <li><b>1984</b> - Classification and regression trees, CART <a href="https://doi.org/10.1201/9781315139470" target="_blank" rel="noopener noreferrer">(Breiman et al., 1984)</a></li>
                    <li><b>1986</b> - Backpropagation trains networks with hidden layers <a href="https://doi.org/10.1038/323533a0" target="_blank" rel="noopener noreferrer">(Rumelhart et al., 1986)</a></li>
                    <li><b>2001</b> - Breiman's random forests <a href="https://doi.org/10.1023/A:1010933404324" target="_blank" rel="noopener noreferrer">(Breiman, 2001)</a></li>
                    <li><b>2001</b> - Breiman's two cultures: model how the data were made, or judge by prediction. Both views are useful <a href="https://doi.org/10.1214/ss/1009213726" target="_blank" rel="noopener noreferrer">(Breiman, 2001)</a></li>
                    <li><b>2015</b> - Deep learning: many layers, much data, fast hardware <a href="https://doi.org/10.1038/nature14539" target="_blank" rel="noopener noreferrer">(LeCun et al., 2015)</a></li>
                </ul>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
