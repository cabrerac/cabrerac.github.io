<!-- SLIDES: -->

## Random Forests

<div class="rows" style="height: 100%">
    <div class="row" style="height: 70%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img class="external-svg" src="{{ site.url }}/assets/media/diagrams/prediction-task-taxonomy.svg" alt="Taxonomy of prediction methods" style="width: 100%; height: 100%">
            </div>
        </div>
    </div>
    <div class="row" style="height: 30%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
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
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Questions in a row</b></p>
                <p>A decision tree asks one question about one attribute at each node.</p>
                <ul>
                    <li>A leaf predicts the majority class of its training rows</li>
                    <li>The path from the root to a leaf reads as a rule</li>
                    <li>Trees split on order only, so they need no scaling. Missing values are filled and categories one-hot encoded</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/decision-tree.jpg" alt="Decision tree" style="height: 360px">
                <div class="footnote">Decision Tree - Gilgoldm, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Random Forests

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Gini impurity</b></p>
                <p>$$G(S) = 1 - \sum_{c} p_c^2$$</p>
                <p>$S$ is the set of rows in a node and $p_c$ the share of class $c$ among them. The sum adds the squared shares. $G = 0$ when all rows have one class, and $G = 0.5$ for two classes in equal shares.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>A greedy split</b></p>
                <p>$$\frac{|L|}{|S|} G(L) + \frac{|R|}{|S|} G(R)$$</p>
                <p>$L$ and $R$ are the rows on the two sides of a split. Each impurity is weighted by the share of rows on its side. The tree keeps the split with the lowest sum, then repeats in each side.</p>
            </div>
        </div>
    </div>
</div>

## Random Forests

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <ul>
                    <li>A node with 6 rows</li>
                    <li>4 yes and 2 no</li>
                    <li>A split sends 3 yes to the left, and 1 yes and 2 no to the right</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>$$G(S) = 1 - \left(\tfrac{4}{6}\right)^2 - \left(\tfrac{2}{6}\right)^2 = 0.44$$</p>
                <p>The left side is pure, $G(L) = 0$. The right side has $G(R) = 1 - \tfrac{1}{9} - \tfrac{4}{9} = 0.44$.</p>
                <p>$$\tfrac{3}{6} \cdot 0 + \tfrac{3}{6} \cdot 0.44 = 0.22$$</p>
                <p>The split halves the impurity, so it is a good first question.</p>
            </div>
        </div>
    </div>
</div>

## Random Forests

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>One tree overfits</b></p>
                <p>A deep tree can give every training row its own leaf. It is right on the training rows and unstable on new ones.</p>
                <p><b>Many trees that vote <a href="https://doi.org/10.1023/A:1010933404324" target="_blank" rel="noopener noreferrer">(Breiman, 2001)</a></b></p>
                <ul>
                    <li><p>Each tree is trained on $n$ rows drawn with replacement, about 63% of them</p></li>
                    <li><p>At each split, only about $\sqrt{d}$ of the $d$ attributes are tried</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Out of bag</b></p>
                <p>Each row is predicted by the trees that did not see it. That gives an error estimate without a separate split.</p>
                <p><b>Attribute importance</b></p>
                <p>How much each attribute lowers the impurity, over all trees. An attribute that dominates is a reason to check for leakage.</p>
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
                    <li>The number of trees</li>
                    <li>The minimum leaf size</li>
                    <li>The number of attributes tried at each split</li>
                    <li>The seed</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Limits</b></p>
                <ul>
                    <li>The vote is harder to read than one tree</li>
                    <li>A forest cannot predict beyond the values it saw</li>
                    <li>Importance favours attributes with many values</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Random Forests

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 47.5%">

```text
for each of many trees
    draw n rows with replacement
    grow a tree, trying a few attributes per split
    stop at the minimum leaf size
for each row kept apart
    every tree votes for a class
    predict the class with the most votes
```

            </div>
            <div class="column vertical-middle text-left" style="width: 5%">
            </div>
            <div class="column vertical-middle text-left" style="width: 47.5%">

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline

forest = make_pipeline(prepare, RandomForestClassifier(
    n_estimators=200, min_samples_leaf=3,
    class_weight="balanced", random_state=0))
predictions = forest.fit(X_train, y_train).predict(X_test)
importance = forest[-1].feature_importances_
```

            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
