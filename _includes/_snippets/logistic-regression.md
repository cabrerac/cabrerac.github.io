<!-- SLIDES: -->

## Logistic Regression

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 55%">
                <p><b>From Lecture 4</b></p>
                <p>Logistic regression turns a weighted sum of an item's attributes into the probability of a class.</p>
                <p>$$P(y = 1 \mid \mathbf{x}) = \sigma(\mathbf{w} \cdot \mathbf{x} + b)$$</p>
                <p>Here $\mathbf{x}$ is a row of attributes, not of words. The same log loss, penalty $C$, and balanced class weights apply.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 45%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/logistic-curve.svg" alt="Logistic curve" style="height: 360px">
                <div class="footnote">Logistic-curve - Qef, Public domain, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Logistic Regression

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Preparation: scaling</b></p>
                <p>$$z = \frac{x - \mu}{\sigma}$$</p>
                <p>$x$ is one value of a column. $\mu$ and $\sigma$ are the mean and the standard deviation of that column on the training rows. The numerator centres the value and the denominator puts every column on the same scale, so the penalty treats the weights alike.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Preparation: categories and missing values</b></p>
                <ul>
                    <li><b>One-hot:</b> one column per category, 1 for the item's category and 0 for the others. Never 1, 2, 3, which invents an order</li>
                    <li><b>Missing number:</b> the median of the training rows, plus a flag column that is 1 when the value was missing</li>
                    <li><b>Missing category:</b> the most frequent one, plus the same flag</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Logistic Regression

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <ul>
                    <li>A column with mean 50 and standard deviation 10</li>
                    <li>A value of 65</li>
                    <li>A colour column with red, blue, and green</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>$$z = \frac{65 - 50}{10} = 1.5$$</p>
                <p>65 is one and a half standard deviations above the mean. Red becomes three columns, 1, 0, 0. A missing value of the first column becomes its median, with the flag set to 1. All of it is learned on the training rows, then reused on the rows kept apart.</p>
            </div>
        </div>
    </div>
</div>

## Logistic Regression

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 47.5%">

```text
split the labelled rows, before any fit
on the training rows only
    learn medians, means, scales, and categories
    learn one weight per prepared column
on the rows kept apart
    the same preparation
    yes when the probability is at least 0.5
```

            </div>
            <div class="column vertical-middle text-left" style="width: 5%">
            </div>
            <div class="column vertical-middle text-left" style="width: 47.5%">

```python
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

numbers = make_pipeline(SimpleImputer(strategy="median",
                        add_indicator=True), StandardScaler())
categories = make_pipeline(SimpleImputer(strategy="most_frequent"),
                           OneHotEncoder(handle_unknown="ignore"))
prepare = ColumnTransformer([("num", numbers, NUMBER_COLUMNS),
                             ("cat", categories, CATEGORY_COLUMNS)])
logistic = make_pipeline(prepare, LogisticRegression(
    class_weight="balanced", max_iter=1000))
predictions = logistic.fit(X_train, y_train).predict(X_test)
```

            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
