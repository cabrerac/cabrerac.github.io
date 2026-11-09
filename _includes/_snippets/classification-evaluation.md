<!-- SLIDES: -->

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p>A <b>confusion matrix</b> counts the right and wrong answers of a prediction on marked items that the model never saw.</p>
            </div>
        </div>
    </div>
</div>

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Confusion matrix</b></p>
                <table class="table">
                    <thead>
                        <tr><th></th><th>Actual yes</th><th>Actual no</th></tr>
                    </thead>
                    <tbody>
                        <tr><td><b>Said yes</b></td><td>TP, right</td><td>FP, wrong</td></tr>
                        <tr><td><b>Said no</b></td><td>FN, wrong</td><td>TN, right</td></tr>
                    </tbody>
                </table>
                <p>Four counts on the items kept apart. We report all four.</p>
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
                <p>Precision divides the right yes answers by all yes answers. Recall divides them by all actual yes items. F1 is their harmonic mean, low when either one is low.</p>
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
            <div class="column vertical-middle text-left" style="width: 55%">
                <p>A <b>baseline</b> tells us what an answer with no work would give.</p>
                <p><b>The majority baseline</b></p>
                <ul>
                    <li>Say no to every item</li>
                    <li>If 70% are actual no, accuracy is 0.70 with no work</li>
                    <li>Its recall and F1 are 0</li>
                    <li>A method must beat it on the counts that matter for the use</li>
                </ul>
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
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>How sure is an F1? <a href="https://doi.org/10.1214/aos/1176344552" target="_blank" rel="noopener noreferrer">(Efron, 1979)</a></b></p>
                <ul>
                    <li><p>The items kept apart are few, so one item more or less moves F1 a lot</p></li>
                    <li><p>Draw the kept apart items again with replacement, the same number, and compute F1. Repeat 2,000 times</p></li>
                    <li><p>The 2.5th and 97.5th percentiles give a 95% interval</p></li>
                    <li><p>For two methods, use the same draws and take the interval of the difference. If it includes 0, the kept apart set cannot tell them apart</p></li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 35%">
                <p><b>Python: the interval</b></p>
                <p>One function for one method or for the difference of two.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 65%">

```python
import numpy as np
from sklearn.metrics import f1_score

N_RESAMPLES = 2000

def f1_interval(y, pred_a, pred_b=None, n_resamples=N_RESAMPLES, seed=SEED):
    """Bootstrap 95% interval of F1(a), or of F1(a) - F1(b) on the same rows."""
    y, a = np.asarray(y), np.asarray(pred_a)
    b = None if pred_b is None else np.asarray(pred_b)
    rng = np.random.default_rng(seed)
    values = []
    for _ in range(n_resamples):
        rows = rng.integers(0, len(y), len(y))
        v = f1_score(y[rows], a[rows], zero_division=0)
        if b is not None:
            v -= f1_score(y[rows], b[rows], zero_division=0)
        values.append(v)
    return np.percentile(values, [2.5, 97.5])

# f1_interval(y_test, pred)            one method
# f1_interval(y_test, pred_b, pred_a)  b minus a, same rows
```

            </div>
        </div>
    </div>
</div>

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 35%">
                <p><b>Python: the counts</b></p>
                <p>The four counts and the three scores.</p>
                <ul>
                    <li>The same function for every method</li>
                    <li>Then read three wrong items per method by hand</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 65%">

```python
from sklearn.metrics import confusion_matrix, precision_recall_fscore_support

def counts_of(y, pred):
    """Right and wrong counts of one method on the test set."""
    tn, fp, fn, tp = confusion_matrix(y, pred, labels=[0, 1]).ravel()
    p, r, f1, _ = precision_recall_fscore_support(
        y, pred, average="binary", zero_division=0)
    return {"TP": tp, "FP": fp, "FN": fn, "TN": tn,
            "precision": p, "recall": r, "F1": f1}

pred_majority = [0] * len(y_test)   # always the larger class
```

            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
