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
                <br>
                <p>$$\text{accuracy} = \frac{TP + TN}{n}$$</p>
                <br>
                <p>Accuracy is the right answers over all answers. $n$ is the number of marked texts.</p>
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
                <p>Precision is the share of yes answers that were marked yes. Recall is the share of marked yes answers that were found.</p>
                <br>
                <p>$$\text{precision} = \frac{TP}{TP + FP}$$</p>
                <br>
                <p>$$\text{recall} = \frac{TP}{TP + FN}$$</p>
                <br>
                <p>F1 is low when either precision or recall is low.</p>
                <br>
                <p>$$F_1 = \frac{2 \cdot \text{precision} \cdot \text{recall}}{\text{precision} + \text{recall}}$$</p>
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
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>Eight right yes answers, two wrong yes answers, and four missed yes answers.</p>
                <br>
                <p>$$TP = 8,\: FP = 2,\: FN = 4$$</p>
                <br>
                <p>$$\text{precision} = \frac{8}{8 + 2} = 0.80$$</p>
                <br>
                <p>$$\text{recall} = \frac{8}{8 + 4} = 0.67$$</p>
                <br>
                <p>$$F_1 = \frac{2 \cdot 0.80 \cdot 0.67}{0.80 + 0.67} = 0.73$$</p>
                <br>
                <p>Eight of the ten yes answers were marked yes. Eight of the twelve marked yes answers were found.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
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
                <p>Always give the most common answer.</p>
                <br>
                <p>$$\text{accuracy} = \frac{n_{\text{majority}}}{n}$$</p>
                <br>
                <p>Accuracy equals the share of that answer. A useful method should beat this line. No method is removed. Ask which one beats it, and why.</p>
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
