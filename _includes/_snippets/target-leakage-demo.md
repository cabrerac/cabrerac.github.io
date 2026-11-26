<!-- SLIDES: -->

## Leakage

<div class="rows" style="height: 100%">
    <div class="row" style="height: 60%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%; height: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/leakage-demo-1.svg" alt="A toy table where the label is made from one column" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
    <div class="row" style="height: 40%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%; height: 100%">
                <p><b>A label made from an attribute</b></p>
                <ul>
                    <li><p>Here international is yes when an item has 2 or more countries</p></li>
                    <li><p>If countries stays in the table, the model only has to read the rule back</p></li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Leakage

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>A perfect score is a warning</b></p>
                <ul>
                    <li><p>One split on countries is right on all 5 rows</p></li>
                    <li><p>The attribute importance points straight at that column</p></li>
                    <li><p>A perfect score on a hard question is a reason to check, not to celebrate</p></li>
                </ul>
                <p>The fix is to drop every column the label was made from, before any fit.</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/leakage-demo-2.svg" alt="One split on countries is right on every row" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
</div>

## Leakage

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 38%">
                <p><b>Python usage:</b> scikit-learn</p>
                <p>The same logistic regression with and without the suspect column</p>
                <ul>
                    <li><p><b>suspect:</b> the column the label may be made from</p></li>
                    <li><p><b>drop:</b> the same table without it</p></li>
                    <li><p><b>Returns:</b> the accuracy with and without the column</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 4%"></div>
            <div class="column vertical-middle text-left" style="width: 58%; font-size: 0.85em">

```python
from sklearn.base import clone

suspect = "countries"
scores = {}
for name, cols in [("with", columns),
                   ("without", [c for c in columns
                                if c != suspect])]:
    m = clone(model).fit(X_train[cols], y_train)
    scores[name] = m.score(X_test[cols], y_test)
print(scores)
```
</div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
