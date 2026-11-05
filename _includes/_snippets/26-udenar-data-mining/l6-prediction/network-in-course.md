<!-- SLIDES: -->

## One Hidden Layer in the Course

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 40%">
                <p><b>In the notebooks</b></p>
                <p>In the course we use the scikit-learn version. The PyTorch version is for after the course.</p>
                <ul>
                    <li>8 hidden units, a penalty of 1.0: few rows, so a stronger penalty.</li>
                    <li>SEED instead of 42, as in every course notebook.</li>
                    <li>The PyTorch slide uses tanh. scikit-learn and the course use ReLU.</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 60%">

```python
from sklearn.neural_network import MLPClassifier

HIDDEN_UNITS = 8
PENALTY = 1.0      # few rows, so a stronger penalty than the default

network = MLPClassifier(hidden_layer_sizes=(HIDDEN_UNITS,), alpha=PENALTY,
                        max_iter=3000, random_state=SEED)
network.fit(X_train, y_train)          # X_train is already scaled by prepare
pred_nn = network.predict(X_test)
```

</div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
