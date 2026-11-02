<!-- SLIDES: -->

<!-- PLACEHOLDER. Depends on the L6 label (week-3-spec.md section 9, open question 1). Filled after Christian decides. -->

## The Prediction Support

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>2 of 3 methods agree</b></p>
                <ul>
                    <li>A paper is predicted positive when at least 2 of logistic regression, the forest and the network say so</li>
                    <li>Training rows: out-of-fold predictions from five folds</li>
                    <li>Rows kept apart: the held-out predictions</li>
                    <li>So no paper is scored by a model that saw its label</li>
                    <li>Rows without a label get no prediction support</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">


```python
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.pipeline import make_pipeline

folds = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)
models = [make_pipeline(prepare, m) for m in (lr, forest, network)]

train_votes = sum(cross_val_predict(m, train, y_train, cv=folds)   # out of fold
                  for m in models)
test_votes = sum(m.fit(train, y_train).predict(test)                # held out
                 for m in models)
voted = pd.concat([train.assign(votes=train_votes),       # indexed by title, like table
                   test.assign(votes=test_votes)])["votes"]
# 2 of 3 agree. Rows without a label get False
table["prediction"] = (voted >= 2).reindex(table.index, fill_value=False)

majority = max(np.mean(y_test), 1 - np.mean(y_test))
l6_counts = all(np.mean(m.predict(test) == y_test) > majority + 0.02
                for m in models)
```

</div>
        </div>
    </div>
</div>

## The Starter List

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 45%">
                <p><b>Five supports, at least two</b></p>
                <ul>
                    <li>has_pattern, read_group, text_says_read, graph_support, prediction</li>
                    <li>The prediction support is <b>prediction & l6_counts</b></li>
                    <li>Under (d), L4 and L6 count as one support, <b>text_or_prediction</b></li>
                    <li>Print how many papers the prediction adds that the text did not have</li>
                    <li>Drop each result once and count who leaves. Also the size at 3 supports</li>
                </ul>
                <p>Sizes for our label: [TBD label, open question 1]</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 55%">


```python
added = table["prediction"] & l6_counts & ~table["text_says_read"]
if one_support:                    # |phi| >= 0.30, or the label repeats L4
    table["text_or_prediction"] = table["text_says_read"] | (table["prediction"] & l6_counts)
    SUPPORT_COLUMNS = ["has_pattern", "read_group", "text_or_prediction", "graph_support"]
else:
    table["prediction"] = table["prediction"] & l6_counts
    SUPPORT_COLUMNS = ["has_pattern", "read_group", "text_says_read", "graph_support", "prediction"]

table["supports"] = table[SUPPORT_COLUMNS].astype(int).sum(axis=1)
table["in_view"] = table["supports"] >= MIN_SUPPORTS
print(table["in_view"].sum(), (table["supports"] >= 3).sum(), added.sum())
```

</div>
        </div>
    </div>
</div>

## The Starter List

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>What fact would remove an article</b></p>
                <p>Every article on the list in outputs/lista_inicial.csv gets a line in the column hecho_que_saca, the fact that would remove it from the starter list.</p>
                <p>The column alerta_centro marks an article that is central only because it links to many others. It is a warning to read the article, never a support.</p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
