<!-- SLIDES: -->

## Random Forests

<div class="rows" style="height: 100%">
    <div class="row" style="height: 65%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%; height: 100%">
                <img class="external-svg" src="{{ site.url }}/assets/media/diagrams/prediction-task-taxonomy.svg" alt="Taxonomy of prediction methods" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
    <div class="row" style="height: 35%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%; height: 100%">
                <p><b>Linear models:</b> a weighted sum of the attributes, turned into a class or a number.</p>
                <p><b>Trees:</b> questions about one attribute at a time, alone or as many trees that vote.</p>
                <p><b>Neural networks:</b> layers that learn their own attributes from the inputs.</p>
                <p><b>Other methods:</b> the label of the nearest items, or a boundary with the widest margin.</p>
            </div>
        </div>
    </div>
</div>

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
            <div class="column vertical-top text-left" style="width: 50%">
                <p>A decision tree asks one question about one attribute at each node.</p>
                <ul>
                    <li><p>A leaf predicts the majority class of its training rows</p></li>
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
            <div class="column vertical-top text-left" style="width: 50%">
                <p>A decision tree asks one question about one attribute at each node.</p>
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
    <div class="row" style="height: 44%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 47.5%; height: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/forest-gini-1.svg" alt="A node with 4 yes and 2 no" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
            <div class="column vertical-middle text-left" style="width: 5%"></div>
            <div class="column vertical-middle text-center" style="width: 47.5%; height: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/forest-gini-2.svg" alt="A split into a pure side and a mixed side" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
    <div class="row" style="height: 56%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%; height: 100%">
                <p><b>Gini impurity and a greedy split</b></p>
$$
G(S) = 1 - \sum_{c} p_c^2 \qquad\qquad \text{split} = \frac{|L|}{|S|} G(L) + \frac{|R|}{|S|} G(R)
$$
                <ul>
                    <li><p><b>Left:</b> 4 yes and 2 no give $G = 0.44$. Pure nodes have $G = 0$</p></li>
                    <li><p><b>Right:</b> 3 yes left ($G = 0$) and 1 yes, 2 no right ($G = 0.44$) give $3/6 \cdot 0 + 3/6 \cdot 0.44 = 0.22$</p></li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Random Forests

<div class="rows" style="height: 100%">
    <div class="row" style="height: 48%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%; height: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/forest-vote-1.svg" alt="Rows drawn with replacement for each tree" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
    <div class="row" style="height: 52%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%; height: 100%">
                <p>A deep tree can give every training row its own leaf. It is right on those rows and unstable on new ones.</p>
                <p><b>Many trees that vote</b> (<a href="https://doi.org/10.1023/A:1010933404324" target="_blank" rel="noopener noreferrer">Breiman, 2001</a>)</p>
                <ul>
                    <li><p>Each tree gets $n$ rows drawn with replacement, about 63% of them</p></li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Random Forests

<div class="rows" style="height: 100%">
    <div class="row" style="height: 48%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%; height: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/forest-vote-3.svg" alt="The trees vote for the majority class" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
    <div class="row" style="height: 52%">
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
    <div class="row" style="height: 56%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%; height: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/random-forest-oob-1.svg" alt="Trees that did not draw row 3" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
    <div class="row" style="height: 44%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%; height: 100%">
                <ul>
                    <li><p><b>Out of bag:</b> each row is predicted only by the trees that did not draw it (here trees 1 and 2 for row 3)</p></li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Random Forests

<div class="rows" style="height: 100%">
    <div class="row" style="height: 56%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%; height: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/random-forest-oob-2.svg" alt="Out-of-bag trees vote on row 3" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
    <div class="row" style="height: 44%">
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
                    <li><p>The number of trees</p></li>
                    <li><p>The minimum leaf size</p></li>
                    <li><p>The number of attributes tried at each split</p></li>
                    <li><p>The seed</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/forest-vote-3.svg" alt="The trees vote for the majority class" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
</div>

## Random Forests

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
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
            <div class="column vertical-middle text-left" style="width: 38%">
                <p><b>Python usage:</b> scikit-learn</p>
                <p>A forest with the same preparation as logistic regression</p>
                <ul>
                    <li><p><b>n_estimators:</b> 200 trees</p></li>
                    <li><p><b>min_samples_leaf:</b> at least 3 rows per leaf</p></li>
                    <li><p><b>Returns:</b> in the Lecture 6 notebook, 0.714 of the 56 rows kept apart are right. The top importances are n_authors 0.513 and year 0.368</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 4%"></div>
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
        </div>
    </div>
</div>

<!-- end SLIDES: -->
