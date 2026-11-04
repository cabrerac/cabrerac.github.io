<!-- SLIDES: -->

<!-- PLACEHOLDER. Depends on the L6 label (week-3-spec.md section 9, open question 1). Filled after Christian decides. -->

## The Prediction Support

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
                    <li>Rows without a label get no prediction</li>
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

## The Starter List

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 40%">
                <p><b>Five results</b></p>
                <ul>
                    <li>The prediction counts only when the three methods beat the majority class</li>
                    <li>In the group notebooks the label repeats the text, so both share text_or_prediction</li>
                    <li>Print how many papers the prediction adds</li>
                    <li>MIN_SUPPORTS gives a first list. Any article can stay if the group says why</li>
                </ul>
                <p>Sizes for our label: [TBD label, open question 1]</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 60%">


```python
added = table["prediction"] & ~table["text_says_read"]
SUPPORT_COLUMNS = ["has_pattern", "read_group", "text_says_read",
                   "graph_support", "prediction"]

table["supports"] = table[SUPPORT_COLUMNS].astype(int).sum(axis=1)
table["in_view"] = table["supports"] >= MIN_SUPPORTS
print(table["in_view"].sum(), "in view,", added.sum(), "added")
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
