<!-- SLIDES: -->

## Decision Trees

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Questions in a row</b></p>
                <ul>
                    <li>A tree asks one question about one attribute at each node</li>
                    <li>A leaf predicts the majority class of its training rows</li>
                    <li>The path from the root to a leaf can be read as a rule</li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/decision-tree.jpg" alt="A small decision tree" style="height: 330px">
                <div class="footnote">Decision Tree - Gilgoldm, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Decision Trees

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Gini impurity</b></p>
                <p>$$G(S) = 1 - \sum_{c} p_c^2$$</p>
                <ul>
                    <li><p>$p_c$ is the share of class $c$ among the rows $S$ in a node</p></li>
                    <li><p>$G = 0$ when all rows have one class</p></li>
                    <li><p>$G = 0.5$ for two classes in equal shares</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>A greedy split</b></p>
                <p>$$\frac{|L|}{|S|} G(L) + \frac{|R|}{|S|} G(R)$$</p>
                <ul>
                    <li><p>Keep the split with the lowest weighted impurity of the two sides $L$ and $R$</p></li>
                    <li><p>Repeat in each side until the leaves are pure or too small</p></li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Decision Trees

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 40%">
                <p><b>Python, one split by hand</b></p>
                <ul>
                    <li>The weighted impurity of a threshold</li>
                    <li>The best threshold for one attribute</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 60%">


```python
def gini(labels):
    n = len(labels)
    return 1 - sum((labels.count(c) / n) ** 2 for c in set(labels))

def split_score(x, y, threshold):
    left = [yi for xi, yi in zip(x, y) if xi <= threshold]
    right = [yi for xi, yi in zip(x, y) if xi > threshold]
    n = len(y)
    return len(left) / n * gini(left) + len(right) / n * gini(right)

x = [1, 2, 3, 4, 5, 6]          # one attribute
y = [0, 0, 0, 1, 1, 1]          # the labels
best = min(sorted(set(x))[:-1], key=lambda t: split_score(x, y, t))   # 3
```

</div>
        </div>
    </div>
</div>

## Decision Trees

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>One tree overfits</b></p>
                <ul>
                    <li>A deep tree can give every training row its own leaf</li>
                    <li>It is right on the training rows and unstable on new ones</li>
                    <li>A minimum leaf size limits this</li>
                </ul>
                <p><b>Many trees that vote <a href="https://doi.org/10.1023/A:1010933404324" target="_blank" rel="noopener noreferrer">(Breiman, 2001)</a></b></p>
                <ul>
                    <li>Grow many trees, each a little different, and let them vote</li>
                    <li>Errors of single trees partly cancel out</li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/random-forest-explain.png" alt="A random forest: several trees vote" style="height: 300px">
                <div class="footnote">Random forest explain - TseKiChun, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Random Forests

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Bootstrap, bagging</b></p>
                <ul>
                    <li><p>Each tree is trained on $n$ rows drawn with replacement</p></li>
                    <li><p>About $1 - 1/e \approx 63\%$ of the rows appear in each draw</p></li>
                    <li><p>The rest are <b>out of bag</b> for that tree</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>A random subset of attributes</b></p>
                <ul>
                    <li><p>At each split, only a random subset of the attributes is tried</p></li>
                    <li><p>Often about $\sqrt{d}$ of the $d$ attributes</p></li>
                    <li><p>So the trees do not all pick the same strong attribute first</p></li>
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
                <p><b>Out of bag</b></p>
                <ul>
                    <li>Each row is predicted by the trees that did not see it</li>
                    <li>That gives an error estimate without a separate split</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Attribute importance</b></p>
                <ul>
                    <li>How much each attribute lowers the impurity, over all trees</li>
                    <li>An attribute that dominates is a reason to check for leakage</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Random Forests

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 40%">
                <p><b>Python</b></p>
                <ul>
                    <li>The same table as for the linear model, no scaling needed</li>
                    <li>A fixed number of trees and a minimum leaf size</li>
                    <li>Predict on the rows kept apart</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 60%">


```python
from sklearn.ensemble import RandomForestClassifier

N_TREES = 200

forest = RandomForestClassifier(n_estimators=N_TREES, min_samples_leaf=3,
                                random_state=SEED)
forest.fit(X_train, y_train)   # scaling does not change a split, so the same X_train works
pred_rf = forest.predict(X_test)

importance = pd.Series(forest.feature_importances_, index=feature_names)
print(importance.nlargest(5))
```

</div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
