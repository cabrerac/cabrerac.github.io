<!-- SLIDES: -->

## Logistic Regression

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>Logistic regression turns a weighted sum of an item's attributes into the probability of a class.</p>
                <p>In Lecture 4, $\mathbf{x}$ was a row of TF-IDF weights, one per word. Here it is a row of attributes.</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/logreg-sum-1.svg" alt="A weighted sum of the attributes" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
</div>

## Logistic Regression

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>Logistic regression turns a weighted sum of an item's attributes into the probability of a class.</p>
                <p>In Lecture 4, $\mathbf{x}$ was a row of TF-IDF weights, one per word. Here it is a row of attributes.</p>
                <br>
$$
P(y = 1 \mid \mathbf{x}) = \sigma(\mathbf{w} \cdot \mathbf{x} + b)
$$
                <br>
                <p><b>$\mathbf{w}$</b> is one weight per attribute. <b>$b$</b> is the intercept.</p>
                <p><b>$\sigma$</b> is the logistic function, from any number to a value between 0 and 1.</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/logreg-sum-2.svg" alt="The sum through the logistic function gives a probability" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
</div>

## Logistic Regression

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>From Lecture 4: TF-IDF with logistic regression</b></p>
                <ul>
                    <li><p>The same log loss</p></li>
                    <li><p>The same penalty $C$</p></li>
                    <li><p>Balanced class weights</p></li>
                    <li><p>One weight per column. There a word, here an attribute</p></li>
                </ul>
                <p>Yes when the probability is at least 0.5.</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/logistic-curve.svg" alt="Logistic curve" style="height: auto; max-width: 100%; max-height: 90%;">
                <div class="footnote">Logistic-curve - Qef, Public domain, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Logistic Regression

<div class="rows" style="height: 100%">
    <div class="row" style="height: 46%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%; height: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/logreg-scaling-1.svg" alt="A value of 65 becomes 1.5" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
    <div class="row" style="height: 54%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%; height: 100%">
                <p><b>Preparation:</b> scaling</p>
                <br>
$$
z = \frac{x - \mu}{\sigma}
$$
                <p><b>$x$</b> is one value, and <b>$\mu$</b> and <b>$\sigma$</b> are the mean and standard deviation on the training rows.</p>
                <p>With $\mu = 50$ and $\sigma = 10$, $x = 65$ gives $z = 1.5$. Every column ends on the same scale, so the penalty treats the weights alike.</p>
            </div>
        </div>
    </div>
</div>

## Logistic Regression

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Preparation:</b> categories and missing values</p>
                <ul>
                    <li><p><b>One-hot:</b> one column per category, never 1, 2, 3</p></li>
                    <li><p><b>Missing number:</b> the median of the training rows, plus a flag column</p></li>
                    <li><p><b>Missing category:</b> the most frequent one, plus the same flag</p></li>
                </ul>
                <p>All of it is learned on the training rows, then reused on the rows kept apart.</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/logreg-scaling-2.svg" alt="One-hot columns for a colour" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
</div>

## Logistic Regression

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 47.5%; height: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/logreg-sum-2.svg" alt="The sum through the logistic function gives a probability" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
            <div class="column vertical-middle text-left" style="width: 4%"></div>
            <div class="column vertical-middle text-left" style="width: 47.5%; font-size: 0.85em">

```text
split the labelled rows, before any fit
on the training rows only
    learn medians, means, scales,
        and categories
    learn one weight per prepared column
on the rows kept apart
    the same preparation
    yes when the probability >= 0.5
```
</div>
        </div>
    </div>
</div>

## Logistic Regression

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 58%; font-size: 0.85em">

```python
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler

numbers = make_pipeline(
    SimpleImputer(strategy="median",
                  add_indicator=True),
    StandardScaler())
categories = make_pipeline(
    SimpleImputer(strategy="most_frequent"),
    OneHotEncoder(handle_unknown="ignore"))
prepare = ColumnTransformer([
    ("num", numbers, NUMBER_COLUMNS),
    ("cat", categories, CATEGORY_COLUMNS)])
```
</div>
            <div class="column vertical-middle text-left" style="width: 4%"></div>
            <div class="column vertical-middle text-left" style="width: 38%">
                <p><b>Python usage:</b> scikit-learn</p>
                <p>The preparation, learned from the training rows only</p>
                <ul>
                    <li><p><b>SimpleImputer:</b> fills a missing number with the median, and a missing category with the most frequent one</p></li>
                    <li><p><b>StandardScaler</b> and <b>OneHotEncoder:</b> scaled numbers and one column per category</p></li>
                    <li><p><b>Returns:</b> prepare, one step that turns the table into numbers. The network uses the same preparation</p></li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Logistic Regression

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 38%">
                <p><b>Python usage:</b> scikit-learn</p>
                <p>The preparation and the model in one pipeline</p>
                <ul>
                    <li><p><b>make_pipeline:</b> the preparation is learned again each time the model is fit</p></li>
                    <li><p><b>class_weight:</b> "balanced" gives both classes the same weight</p></li>
                    <li><p><b>Returns:</b> one class per row kept apart. In the Lecture 6 notebook, 0.607 of the 56 rows are right, against 0.518 for the majority class</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 4%"></div>
            <div class="column vertical-middle text-left" style="width: 58%; font-size: 0.85em">

```python
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline

model = make_pipeline(prepare, LogisticRegression(
    class_weight="balanced", max_iter=1000))
model.fit(X_train, y_train)
predictions = model.predict(X_test)
```
</div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
