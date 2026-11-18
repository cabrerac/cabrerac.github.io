<!-- SLIDES: -->

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p><b>Evaluation</b> compares the keyword list, TF-IDF with logistic regression, and the text encoder on the same marked texts.</p>
            </div>
        </div>
    </div>
</div>

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Confusion matrix</b></p>
                <p>Four counts on marked texts the model never saw.</p>
                <ul>
                    <li><b>TP:</b> said yes, marked yes</li>
                    <li><b>FP:</b> said yes, marked no</li>
                    <li><b>FN:</b> said no, marked yes</li>
                    <li><b>TN:</b> said no, marked no</li>
                </ul>
                <p><b>Accuracy:</b> the right answers over all answers, $(TP + TN) / n$.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/diagrams/confusion-matrix-counts.svg" alt="The four counts of a confusion matrix" style="height: 380px">
            </div>
        </div>
    </div>
</div>

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 55%">
                <p><b>Precision, recall, F1</b></p>
                <p>$$\text{precision} = \frac{TP}{TP + FP} \qquad \text{recall} = \frac{TP}{TP + FN}$$</p>
                <p>$$F_1 = \frac{2 \cdot \text{precision} \cdot \text{recall}}{\text{precision} + \text{recall}}$$</p>
                <p>Precision divides the right yes answers by all yes answers. Recall divides them by all marked yes. F1 is low when either is low.</p>
                <p>With $TP = 8$, $FP = 2$ and $FN = 4$: precision 0.80, recall 0.67, and F1 0.73.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 45%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/precision-recall.svg" alt="Precision and recall" style="height: 360px">
                <div class="footnote">Precisionrecall - Walber, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 38%">
                <p><b>The majority class</b></p>
                <p>Always give the most common answer. Accuracy equals the share of that answer.</p>
                <p><b>A reference line:</b> a useful method should beat it. No method is removed. Ask which one beats it, and why.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 62%">

```python
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.metrics import precision_recall_fscore_support

def counts_of(marks, pred):
    tn, fp, fn, tp = confusion_matrix(
        marks, pred, labels=[0, 1]).ravel()
    p, r, f1, _ = precision_recall_fscore_support(
        marks, pred, average="binary", zero_division=0)
    return {"TP": tp, "FP": fp, "FN": fn, "TN": tn,
            "precision": p, "recall": r, "F1": f1,
            "accuracy": accuracy_score(marks, pred)}

results = pd.DataFrame({name: counts_of(y_test, pred)
    for name, pred in predictions.items()}).T
majority = results.loc["clase mayoritaria", "accuracy"]
results["beats_majority"] = results["accuracy"] > majority
```

            </div>
        </div>
    </div>
</div>

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Five folds</b></p>
                <p>The training marks are split into five parts, each with the same share of yes.</p>
                <ul>
                    <li>Train on four parts and test on the fifth</li>
                    <li>Repeat until each part was the test once</li>
                    <li>Report the lowest and the highest F1 of the five folds</li>
                </ul>
                <p>A wide gap says the marks are too few for one number.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/4/4b/KfoldCV.gif" alt="K-fold cross-validation" style="height: 360px">
                <div class="footnote">K-fold CV - MBanuelos22, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
