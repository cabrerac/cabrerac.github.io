<!-- SLIDES: -->

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 52%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%; height: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/eval-folds-1.svg" alt="One fold predicted, four fitted" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
    <div class="row" style="height: 48%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%; height: 100%">
                <p><b>Five folds on the training rows</b></p>
                <ul>
                    <li><p>Cut the training rows into five folds</p></li>
                    <li><p>Fit on four folds and predict the fifth</p></li>
                    <li><p>Repeat until every training row is predicted once</p></li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 52%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%; height: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/eval-folds-2.svg" alt="Each fold predicted once" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
    <div class="row" style="height: 48%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%; height: 100%">
                <p><b>Five folds on the training rows</b></p>
                <ul>
                    <li><p>Cut the training rows into five folds</p></li>
                    <li><p>Fit on four folds and predict the fifth</p></li>
                    <li><p>Repeat until every training row is predicted once</p></li>
                </ul>
                <p>Any preparation learned from data sits inside the model, so each fold learns it again.</p>
            </div>
        </div>
    </div>
</div>

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 38%">
                <p><b>Python usage:</b> scikit-learn</p>
                <p>Five folds next to the rows kept apart</p>
                <ul>
                    <li><p><b>StratifiedKFold:</b> five folds with the same share of each class</p></li>
                    <li><p><b>cross_val_predict:</b> one prediction per training row, from the fold that left it out</p></li>
                    <li><p><b>Returns:</b> in the Lecture 6 notebook, the forest is right on 0.62 of the training rows, and the majority class on 0.53</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 4%"></div>
            <div class="column vertical-middle text-left" style="width: 58%; font-size: 0.85em">

```python
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import (
    cross_val_predict)

folds = StratifiedKFold(n_splits=5, shuffle=True,
                        random_state=7)
pred_cv = cross_val_predict(model, X_train, y_train,
                            cv=folds)
accuracy = (pred_cv == y_train).mean()
```
</div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
