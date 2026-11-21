<!-- SLIDES: -->

## The Project

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 40%">
                <p><b>2 of 3 methods agree</b></p>
                <ul>
                    <li>A paper is predicted positive when at least 2 of logistic regression, the forest and the network say so</li>
                    <li>Training rows: out-of-fold predictions from five folds</li>
                    <li>Rows kept apart: the held-out predictions</li>
                    <li>So no paper is scored by a model that saw its label</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 60%">

```python
import pandas as pd
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.pipeline import make_pipeline

folds = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)
models = [make_pipeline(prepare, m) for m in (lr, forest, network)]

train_votes = sum(cross_val_predict(m, train, y_train, cv=folds)
                  for m in models)
test_votes = sum(m.fit(train, y_train).predict(test)
                 for m in models)
voted = pd.concat([train.assign(votes=train_votes),
                   test.assign(votes=test_votes)])["votes"]
# 2 of 3 agree. Rows without a label get False
table["prediction"] = (voted >= 2).reindex(table.index, fill_value=False)
```

</div>
        </div>
    </div>
</div>

## The Project

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 40%">
                <p><b>The reading list</b></p>
                <ul>
                    <li>A paper is on the list when at least 2 of the 3 methods say yes, and the three beat the majority class</li>
                    <li>The list keeps at most 30, the ones with more votes first</li>
                    <li>A positive prediction is not, by itself, a reason to read</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 60%">

```python
if l6_counts:
    chosen = table.index[table["prediction"]]
else:
    chosen = []
reading = table.loc[chosen].reset_index()
reading["votos"] = voted.reindex(reading["title"]).to_numpy()
reading_list = reading.sort_values(
    ["votos", "title"], ascending=[False, True]).head(MAX_PAPERS)
```

</div>
        </div>
    </div>
</div>

## The Project

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>What the list is</b></p>
                <p>The list is the papers this lecture predicts as international, at most 30.</p>
                <p>Predicting international is not a reason to read the paper.</p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
