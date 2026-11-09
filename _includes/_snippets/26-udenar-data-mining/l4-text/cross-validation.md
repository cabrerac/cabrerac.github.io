<!-- SLIDES: -->

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p><b>Cross-validation</b> judges a model on rows it did not see, by splitting the labelled rows into folds and letting each fold be the test once.</p>
            </div>
        </div>
    </div>
</div>

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>K folds</b></p>
                <p>The labelled rows are split into K equal parts.</p>
                <ul>
                    <li>Train on all parts but one</li>
                    <li>Test on the part left out</li>
                    <li>Repeat until each part was the test once</li>
                    <li>Report the mean over the K folds</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/4/4b/KfoldCV.gif" alt="K-fold cross-validation" style="height: 360px">
                <div class="footnote">K-fold CV - MBanuelos22, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>The mean over the folds</b></p>
                <p>$$\text{CV}(\mathbf{w}) = \frac{1}{K}\sum_{k=1}^K \text{Loss}_k(\mathbf{w})$$</p>
                <ul>
                    <li><p>$\text{Loss}_k(\mathbf{w})$ is the loss on fold $k$ when the model trains on the other folds</p></li>
                    <li>A fold keeps the share of each class when it is stratified</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/4/4b/KfoldCV.gif" alt="K-fold cross-validation" style="height: 360px">
                <div class="footnote">K-fold CV - MBanuelos22, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Leave one out</b></p>
                <p>K equals the number of rows, so each row is the test once.</p>
                <ul>
                    <li>Uses almost every row to train</li>
                    <li>Needs one model per row</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/c/c7/LOOCV.gif" alt="Leave one out cross-validation" style="height: 360px">
                <div class="footnote">LOOCV - MBanuelos22, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
