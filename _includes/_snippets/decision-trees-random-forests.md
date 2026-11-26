<!-- SLIDES: -->

## Random Forests

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p>A <b>random forest</b> grows many decision trees, each on a slightly different sample of the rows, and predicts the class most trees vote for.</p>
            </div>
        </div>
    </div>
</div>

## Random Forests

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>A decision tree</b> asks one question about one attribute at each node.</p>
                <ul>
                    <li><p>A leaf predicts the majority class of its training rows</p></li>
                    <li><p>The path from the root to a leaf reads as a rule</p></li>
                    <li><p>Trees split on order only, so they need no scaling</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/decision-tree-2.svg" alt="One root-to-leaf rule path highlighted" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
</div>

## Random Forests

<div class="rows" style="height: 100%">
    <div class="row" style="height: 46%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%; height: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/forest-vote-3.svg" alt="The trees vote for the majority class" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
    <div class="row" style="height: 54%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%; height: 100%">
                <p>A deep tree can give every training row its own leaf. It is right on those rows and unstable on new ones.</p>
                <p><b>Many trees that vote</b> (<a href="https://doi.org/10.1023/A:1010933404324" target="_blank" rel="noopener noreferrer">Breiman, 2001</a>)</p>
                <ul>
                    <li><p>Each tree gets $n$ rows drawn with replacement, about 63% of them</p></li>
                    <li><p>Each split tries only about $\sqrt{d}$ of the $d$ attributes</p></li>
                    <li><p>The forest predicts the class most trees vote for (here two yes and one no give yes)</p></li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Random Forests

<div class="rows" style="height: 100%">
    <div class="row" style="height: 54%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%; height: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/random-forest-oob-2.svg" alt="Out-of-bag trees vote on row 3" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
    <div class="row" style="height: 46%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%; height: 100%">
                <ul>
                    <li><p><b>Out of bag:</b> each row is predicted only by the trees that did not draw it (here trees 1 and 2 for row 3)</p></li>
                    <li><p>Those trees vote on the held-out row, giving an error estimate without a separate split</p></li>
                    <li><p><b>Attribute importance:</b> how much each attribute lowers the impurity, over all trees. A dominant attribute is a reason to check for leakage</p></li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Random Forests

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Set before the results</b></p>
                <ul>
                    <li><p>The number of trees, the minimum leaf size, the attributes tried at each split, and the seed</p></li>
                </ul>
                <p><b>Limits</b></p>
                <ul>
                    <li><p>The vote is harder to read than one tree</p></li>
                    <li><p>A forest cannot predict beyond the values it saw</p></li>
                    <li><p>Importance favours attributes with many values</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/decision-tree-1.svg" alt="A generic decision tree" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
</div>

## Random Forests

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 47.5%; height: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/forest-vote-3.svg" alt="The trees vote for the majority class" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
            <div class="column vertical-middle text-left" style="width: 4%"></div>
            <div class="column vertical-middle text-left" style="width: 47.5%; font-size: 0.85em">

```text
for each of many trees
    draw n rows with replacement
    grow a tree, trying a few
        attributes per split
    stop at the minimum leaf size
for each row kept apart
    every tree votes for a class
    predict the class with most votes
```
</div>
        </div>
    </div>
</div>

## Random Forests

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 58%; font-size: 0.85em">

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline

model = make_pipeline(
    prepare,
    RandomForestClassifier(n_estimators=200,
                           min_samples_leaf=3,
                           random_state=7))
model.fit(X_train, y_train)
predictions = model.predict(X_test)
importance = model[-1].feature_importances_
```
</div>
            <div class="column vertical-middle text-left" style="width: 4%"></div>
            <div class="column vertical-middle text-left" style="width: 38%">
                <p><b>Python usage:</b> scikit-learn</p>
                <p>A forest on the prepared table</p>
                <ul>
                    <li><p><b>prepare:</b> one preparation step for every method, shown in full with logistic regression next</p></li>
                    <li><p><b>n_estimators:</b> 200 trees, at least 3 rows per leaf</p></li>
                    <li><p><b>Returns:</b> in the Lecture 6 notebook, 0.714 of the 56 rows kept apart are right. The top importances are n_authors 0.513 and year 0.368</p></li>
                </ul>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
