<!-- SLIDES: -->

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>How sure is an F1?</b> (<a href="https://doi.org/10.1214/aos/1176344552" target="_blank" rel="noopener noreferrer">Efron, 1979</a>)</p>
                <ul>
                    <li><p>The items kept apart are few, so one item more or less moves F1 a lot</p></li>
                    <li><p>Draw the kept apart items again with replacement, the same number, and compute F1. Repeat 2,000 times</p></li>
                    <li><p>The 2.5th and 97.5th percentiles give a 95% interval of F1</p></li>
                    <li><p>For two methods, take the interval of the difference on the same draws</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/eval-bootstrap.svg" alt="F1 on 2,000 draws with replacement" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
</div>

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 58%; font-size: 0.85em">

```python
import numpy as np
from sklearn.metrics import f1_score

def f1_interval(y, pred, n_resamples=2000, seed=0):
    """Bootstrap 95% interval of F1."""
    y = np.asarray(y)
    pred = np.asarray(pred)
    rng = np.random.default_rng(seed)
    values = []
    for _ in range(n_resamples):
        rows = rng.integers(0, len(y), len(y))
        values.append(f1_score(y[rows], pred[rows],
                               zero_division=0))
    return np.percentile(values, [2.5, 97.5])
```
</div>
            <div class="column vertical-middle text-left" style="width: 4%"></div>
            <div class="column vertical-middle text-left" style="width: 38%">
                <p><b>Python usage:</b> NumPy and scikit-learn</p>
                <p>A 95% bootstrap interval of F1</p>
                <ul>
                    <li><p><b>integers:</b> draws the row numbers with replacement</p></li>
                    <li><p><b>percentile:</b> the 2.5th and 97.5th of the 2,000 values</p></li>
                    <li><p><b>Returns:</b> a low and a high F1, the 2.5th and 97.5th percentiles of the 2,000 values</p></li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 38%">
                <p><b>Python usage:</b> scikit-learn</p>
                <p>The four counts and the three scores, the same for every method</p>
                <ul>
                    <li><p><b>confusion_matrix:</b> TN, FP, FN and TP, in that order</p></li>
                    <li><p><b>precision_recall_fscore_support:</b> the three scores of the yes class</p></li>
                    <li><p><b>Returns:</b> on a toy set of 40 items with TP 8, FP 2, FN 4 and TN 26, precision 0.80, recall 0.67 and F1 0.73</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 4%"></div>
            <div class="column vertical-middle text-left" style="width: 58%; font-size: 0.85em">

```python
from sklearn.metrics import confusion_matrix
from sklearn.metrics import (
    precision_recall_fscore_support)

def counts_of(y, pred):
    """Right and wrong counts of one method."""
    tn, fp, fn, tp = confusion_matrix(
        y, pred, labels=[0, 1]).ravel()
    p, r, f1, _ = precision_recall_fscore_support(
        y, pred, average="binary", zero_division=0)
    return {"TP": tp, "FP": fp, "FN": fn, "TN": tn,
            "precision": p, "recall": r, "F1": f1}
```
</div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
