<!-- SLIDES: -->

## Logistic Regression

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p><b>Logistic regression</b> turns a weighted sum of an item's attributes into the probability that the item belongs to a class.</p>
            </div>
        </div>
    </div>
</div>

## Logistic Regression

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 55%">
                <p><b>A probability from a weighted sum</b> <a href="https://doi.org/10.1111/j.2517-6161.1958.tb00292.x" target="_blank" rel="noopener noreferrer">(Cox, 1958)</a></p>
                <p>$$P(y = 1 \mid \mathbf{x}) = \sigma(\mathbf{w} \cdot \mathbf{x} + b)$$</p>
                <p>$$\sigma(z) = \frac{1}{1 + e^{-z}}$$</p>
                <ul>
                    <li><p>One weight per column</p></li>
                    <li><p>Predict 1 when the probability is at least 0.5</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 45%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/logistic-curve.svg" alt="The logistic curve" style="height: 300px">
                <div class="footnote">Logistic-curve - Qef, Public domain, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Logistic Regression

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <p><b>Log loss</b></p>
                <p>$$\mathcal{L}(\mathbf{w}, b) = -\sum_{i=1}^{n} \left[ y_i \log p_i + (1 - y_i) \log (1 - p_i) \right]$$</p>
                <p>$p_i$ is the predicted probability for item $i$.</p>
                <p>A confident wrong answer costs a lot.</p>
                <p>The weights are found by minimising the loss.</p>
            </div>
        </div>
    </div>
</div>

## Logistic Regression

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <p><b>L2 penalty and class weights</b></p>
                <p>$$\min_{\mathbf{w}, b} \ \frac{1}{2} \lVert \mathbf{w} \rVert^2 + C \sum_{i} s_{y_i} \, \ell_i$$</p>
                <p>With many columns, weights can grow to fit noise.</p>
                <p>The penalty keeps them small, a larger $C$ means a weaker penalty.</p>
                <p>$s_y = n / (2\, n_y)$ gives the rare class the same total weight.</p>
                <p>Without it, a model can do well by saying no to everything.</p>
            </div>
        </div>
    </div>
</div>

## Logistic Regression

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 35%">
                <p><b>Python</b></p>
                <ul>
                    <li>Balanced class weights</li>
                    <li>The penalty is a setting, fixed before looking at the test set</li>
                    <li>Predict on the test rows</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 65%">


```python
from sklearn.linear_model import LogisticRegression

lr = LogisticRegression(class_weight="balanced", C=C_REG,
                        max_iter=1000)
lr.fit(X_train, y_train)
pred_lr = lr.predict(X_test)
```

            </div>
        </div>
    </div>
</div>

## Logistic Regression

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 35%">
                <p><b>Reading the weights</b></p>
                <ul>
                    <li>Each column has one weight</li>
                    <li>Positive pushes towards 1</li>
                    <li>Negative pushes towards 0</li>
                    <li>A strange column near the top is worth a look</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 65%">


```python
import pandas as pd

# feature_names: one name per column of X_train
weights = pd.Series(lr.coef_[0], index=feature_names)
print(weights.nlargest(15))    # push towards 1
print(weights.nsmallest(15))   # push towards 0
```

            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
