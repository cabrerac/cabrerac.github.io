<!-- SLIDES: -->

## Tabular Preparation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Scaling</b></p>
                <p>$$z = \frac{x - \mu}{\sigma}$$</p>
                <ul>
                    <li><p>$\mu$ and $\sigma$ are the mean and standard deviation of the column on the training rows</p></li>
                    <li><p>Needed for logistic regression with a penalty and for a network</p></li>
                    <li><p>Trees split on order only, so they do not need it</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>One-hot categories</b></p>
                <ul>
                    <li>One column per category, 1 for the item's category and 0 for the others</li>
                    <li>Never code categories as 1, 2, 3, that invents an order</li>
                </ul>
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
                <ul>
                    <li>Fill a missing number with the median of the training rows</li>
                    <li>Fill a missing category with the most frequent one</li>
                    <li>Add a flag column: 1 if the value was missing</li>
                    <li>The flag keeps that the value was missing</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>When missing is the information</b></p>
                <ul>
                    <li>If a value is missing for most rows, the filled value is almost constant</li>
                    <li>Then the flag carries what the column says</li>
                </ul>
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
                <ul>
                    <li>Medians, means, scales and categories are learned</li>
                    <li>Learn them on the training rows, then reuse them on the test rows</li>
                </ul>
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
                <ul>
                    <li>A column that is filled in after the label is known, or computed from it</li>
                    <li>Example: predicting whether a loan is repaid, with a column for late fees</li>
                    <li>Late fees exist only because the loan was not repaid on time</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>How to check</b></p>
                <ul>
                    <li>For each input, ask how and when it was made</li>
                    <li>Train the same model with and without the suspect input</li>
                    <li>A large drop without it means it was carrying the label</li>
                </ul>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
