<!-- SLIDES: -->

## Tabular Preparation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p><b>Tabular preparation</b> turns a table of mixed attributes into numbers a model can use, by scaling numbers, encoding categories and filling missing values.</p>
            </div>
        </div>
    </div>
</div>

## Tabular Preparation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <p><b>Scaling</b></p>
                <p>$$z = \frac{x - \mu}{\sigma}$$</p>
                <p>$\mu$ and $\sigma$ are the mean and standard deviation of the column on the training rows.</p>
                <p>Needed for logistic regression with a penalty and for a network.</p>
                <p>Trees split on order only, so they do not need it.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>One-hot categories</b></p>
                <p>One column per category, 1 for the item's category and 0 for the others.</p>
                <p>Never code categories as 1, 2, 3, that invents an order.</p>
            </div>
        </div>
    </div>
</div>

## Tabular Preparation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Missing values</b></p>
                <p>Fill a missing number with the median of the training rows.</p>
                <p>Fill a missing category with the most frequent one.</p>
                <p>Add a flag column: 1 if the value was missing.</p>
                <p>The flag keeps that the value was missing.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>When missing is the information</b></p>
                <p>If a value is missing for most rows, the filled value is almost constant.</p>
                <p>Then the flag carries what the column says.</p>
            </div>
        </div>
    </div>
</div>

## Tabular Preparation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 40%">
                <p><b>Fit on the training rows only</b></p>
                <p>Medians, means, scales and categories are learned.</p>
                <p>Learn them on the training rows, then reuse them on the test rows.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 60%">


```python
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

numbers = make_pipeline(SimpleImputer(strategy="median", add_indicator=True),
                        StandardScaler())
categories = make_pipeline(SimpleImputer(strategy="most_frequent"),
                           OneHotEncoder(handle_unknown="ignore"))
prepare = ColumnTransformer([("num", numbers, NUMBER_COLUMNS),
                             ("cat", categories, CATEGORY_COLUMNS)])

X_train = prepare.fit_transform(train)   # learn medians, scales, categories
X_test = prepare.transform(test)         # reuse them, never refit
feature_names = prepare.get_feature_names_out()
```

</div>
        </div>
    </div>
</div>

## Target Leakage

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>An input that already contains the label <a href="https://doi.org/10.1145/2382577.2382579" target="_blank" rel="noopener noreferrer">(Kaufman et al., 2012)</a></b></p>
                <p>A column that is filled in after the label is known, or computed from it.</p>
                <p>Example: predicting whether a loan is repaid, with a column for late fees.</p>
                <p>Late fees exist only because the loan was not repaid on time.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>How to check</b></p>
                <p>For each input, ask how and when it was made.</p>
                <p>Train the same model with and without the suspect input.</p>
                <p>A large drop without it means it was carrying the label.</p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
