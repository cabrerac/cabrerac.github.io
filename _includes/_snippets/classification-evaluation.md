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
            <div class="column vertical-top text-left" style="width: 50%">
                <p>Four counts on the items kept apart. We report all four.</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/eval-confusion-1.svg" alt="Actual against predicted" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
</div>

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <p>Four counts on the items kept apart. We report all four.</p>
                <ul>
                    <li><p><b>TP:</b> said yes, and it was yes</p></li>
                    <li><p><b>FP:</b> said yes, and it was no</p></li>
                    <li><p><b>FN:</b> said no, and it was yes</p></li>
                    <li><p><b>TN:</b> said no, and it was no</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/eval-confusion-2.svg" alt="The four cells of a confusion matrix" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
</div>

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Precision, recall, F1</b></p>
$$
\text{precision} = \frac{TP}{TP + FP}, \qquad \text{recall} = \frac{TP}{TP + FN}
$$
$$
F_1 = \frac{2 \cdot \text{precision} \cdot \text{recall}}{\text{precision} + \text{recall}}
$$
                <table class="table" style="font-size: 0.74em">
                    <thead>
                        <tr><th></th><th>Actual yes</th><th>Actual no</th></tr>
                    </thead>
                    <tbody>
                        <tr><td><b>Predicted yes</b></td><td>TP = 8</td><td>FP = 2</td></tr>
                        <tr><td><b>Predicted no</b></td><td>FN = 4</td><td>TN = 26</td></tr>
                    </tbody>
                </table>
                <p>Toy set: precision 0.80, recall 0.67, and F1 0.73.</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/precision-recall.svg" alt="Precision and recall" style="height: auto; max-width: 100%; max-height: 90%;">
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
                <p>A <b>baseline</b> tells us what an answer with no work would give.</p>
                <ul>
                    <li><p><b>The majority class:</b> say no to every item</p></li>
                    <li><p>In the example, 7 right of 10 gives accuracy 0.70 and recall of yes 0</p></li>
                    <li><p>A method must beat it on the counts that matter for the use</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/eval-majority.svg" alt="Saying no to all of 7 no and 3 yes" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
</div>

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
            <div class="column vertical-middle text-left" style="width: 38%">
                <p><b>Python usage:</b> NumPy and scikit-learn</p>
                <p>A 95% bootstrap interval of F1</p>
                <ul>
                    <li><p><b>integers:</b> draws the row numbers with replacement</p></li>
                    <li><p><b>percentile:</b> the 2.5th and 97.5th of the 2,000 values</p></li>
                    <li><p><b>Returns:</b> a low and a high F1, the 2.5th and 97.5th percentiles of the 2,000 values</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 4%"></div>
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
        </div>
    </div>
</div>

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
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
            <div class="column vertical-middle text-left" style="width: 4%"></div>
            <div class="column vertical-middle text-left" style="width: 38%">
                <p><b>Python usage:</b> scikit-learn</p>
                <p>The four counts and the three scores, the same for every method</p>
                <ul>
                    <li><p><b>confusion_matrix:</b> TN, FP, FN and TP, in that order</p></li>
                    <li><p><b>precision_recall_fscore_support:</b> the three scores of the yes class</p></li>
                    <li><p><b>Returns:</b> on a toy set of 40 items with TP 8, FP 2, FN 4 and TN 26, precision 0.80, recall 0.67 and F1 0.73</p></li>
                </ul>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
