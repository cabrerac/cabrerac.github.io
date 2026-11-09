<!-- SLIDES: -->

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 30%">
                <p><b>Python: five folds on the training rows</b></p>
                <p>Any preparation learned from data sits inside the model, so each fold learns it again.</p>
                <ul>
                    <li>Every training row is predicted once</li>
                    <li>Shown next to the kept apart counts</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 70%">

```python
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.metrics import accuracy_score, f1_score

folds = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)

# model: the method with its preparation inside it
# train_inputs: the training rows before any learned preparation
# pred_cv = cross_val_predict(model, train_inputs, y_train, cv=folds)
```

            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
