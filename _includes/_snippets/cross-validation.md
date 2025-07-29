<!-- SLIDES: -->

## Cross-validation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p>Cross-validation is a technique for <b>assessing model performance</b> and preventing overfitting by evaluating the model on unseen data.</p>
            </div>
        </div>
    </div>
</div>

## Cross-validation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
            </div>                
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/4/4b/KfoldCV.gif" alt="K-Fold" style="max-width: 80%">
                <div class="footnote">K-fold CV - MBanuelos22, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons.</div>
            </div>
        </div>
    </div>
</div>

## Cross-validation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <br>
                <p><b>K-Fold Cross-validation</b> divides the dataset into K equal parts:</p>

```python
for (int k = 1; k <= K; k++) {
    trainOnAllFoldsExcept(k);
    evaluateOnFold(k);
    recordPerformanceMetric(k);
}
calculateAveragePerformance(K);
```
</div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/4/4b/KfoldCV.gif" alt="K-Fold" style="max-width: 80%">
                <div class="footnote">K-fold CV - MBanuelos22, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons.</div>
            </div>
        </div>
    </div>
</div>

## Cross-validation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <br>
                <p><b>K-Fold Cross-validation</b> divides the dataset into K equal parts:</p>

```python
for (int k = 1; k <= K; k++) {
    trainOnAllFoldsExcept(k);
    evaluateOnFold(k);
    recordPerformanceMetric(k);
}
calculateAveragePerformance(K);
```
<p>Mathematically, for K-fold CV:</p>
$$
\text{CV}(\mathbf{w}) = \frac{1}{K}\sum_{k=1}^K \text{Loss}_k(\mathbf{w})
$$
Where $\text{Loss}_k(\mathbf{w})$ is the loss on fold $k$ when training on all other folds.
</div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/4/4b/KfoldCV.gif" alt="K-Fold" style="max-width: 80%">
                <div class="footnote">K-fold CV - MBanuelos22, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons.</div>
            </div>
        </div>
    </div>
</div>

## Cross-validation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <br>
                <p><b>Leave-One-Out Cross-validation (LOOCV)</b> is a special case where K = N:</p>
$$
\text{LOOCV}(\mathbf{w}) = \frac{1}{N}\sum_{i=1}^N (y_i - \mathbf{w}_{-i}^T\mathbf{x}_i)^2
$$
<br>Where $\mathbf{w}_{-i}$ is trained on all data points except $(\mathbf{x}_i, y_i)$.
</div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/c/c7/LOOCV.gif" alt="LOOCV" style="max-width: 80%">
                <div class="footnote">LOOCV - MBanuelos22, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons.</div>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->