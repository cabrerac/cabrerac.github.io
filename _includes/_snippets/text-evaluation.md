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
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>The majority class</b></p>
                <p>Always give the most common answer.</p>
                <br>
                <p>$$\text{accuracy} = \frac{n_{\text{majority}}}{n}$$</p>
                <br>
                <p>Accuracy equals the share of that answer. A useful method should beat this line. No method is removed. Ask which one beats it, and why.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">

```python
from sklearn.metrics import accuracy_score, confusion_matrix

def counts_of(marks, pred):
    tn, fp, fn, tp = confusion_matrix(
        marks, pred, labels=[0, 1]).ravel()
    return {"TP": tp, "FP": fp, "FN": fn, "TN": tn,
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
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>The same texts</b></p>
                <p>Yes means the method answers yes for that text.</p>
                <table class="table">
                    <thead>
                        <tr><th>Text</th><th>Keyword list</th><th>TF-IDF</th><th>Encoder</th></tr>
                    </thead>
                    <tbody>
                        <tr><td>A, B</td><td>yes</td><td>yes</td><td>yes</td></tr>
                        <tr><td>C</td><td>yes</td><td>no</td><td>no</td></tr>
                        <tr><td>D</td><td>no</td><td>no</td><td>yes</td></tr>
                    </tbody>
                </table>
                <ul>
                    <li><b>All three:</b> A and B are a stronger candidate.</li>
                    <li><b>Keyword list only:</b> C is a yes from the list alone.</li>
                    <li><b>Encoder only:</b> D is a yes from the encoder alone.</li>
                </ul>
                <p>C can be checked against a word. D cannot, so the encoder yes is difficult to explain.</p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
