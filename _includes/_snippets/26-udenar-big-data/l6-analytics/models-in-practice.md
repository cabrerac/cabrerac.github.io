<!-- SLIDES: -->

## Models in Practice

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p>From theory to a notebook: we fit models on <b>aggregates</b>, never on individuals — the privacy lesson from Lecture 2 still holds.</p>
            </div>
        </div>
    </div>
</div>

## Models in Practice

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 40%">
                <p><b>Train, validate, test</b></p>
                <ul>
                    <li><b>Train:</b> fit the model</li>
                    <li><b>Validation:</b> choose between models</li>
                    <li><b>Test:</b> judge once, at the end</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 60%">

```python
from sklearn.model_selection import train_test_split

# hold out the test set first
X_rest, X_test, y_rest, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42)

# split the rest into train and validation
X_train, X_val, y_train, y_val = train_test_split(
    X_rest, y_rest, test_size=0.25, random_state=42)
```

</div>
        </div>
    </div>
</div>

## Models in Practice

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 40%">
                <p><b>Start simple: a linear model</b></p>
                <ul>
                    <li>Transparent and fast</li>
                    <li>Report <b>R&sup2;</b> and <b>MAE</b> on validation</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 60%">

```python
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error

linear = LinearRegression().fit(X_train, y_train)
pred = linear.predict(X_val)

print("R2 :", r2_score(y_val, pred))
print("MAE:", mean_absolute_error(y_val, pred))
```

</div>
        </div>
    </div>
</div>

## Models in Practice

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 40%">
                <p><b>More flexible: a small neural network</b></p>
                <ul>
                    <li><b>Scale</b> the inputs first (learn scale on train only)</li>
                    <li>An MLP can fit non-linear shapes</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 60%">

```python
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor

scaler = StandardScaler().fit(X_train)
mlp = MLPRegressor(hidden_layer_sizes=(8,),
                   max_iter=500, random_state=42)
mlp.fit(scaler.transform(X_train), y_train)
pred = mlp.predict(scaler.transform(X_val))
```

</div>
        </div>
    </div>
</div>

## Models in Practice

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 40%">
                <p><b>Choose, then judge once</b></p>
                <ul>
                    <li>Pick the model with lower <b>validation</b> error</li>
                    <li>Report <b>test</b> error only at the end</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 60%">

```python
# choose on validation, judge once on test
if mae_linear <= mae_mlp:
    model, name = linear, "linear"
else:
    model, name = mlp, "mlp"

print("chosen:", name)
print("test R2:", r2_score(y_test, model.predict(X_test_ready)))
```

</div>
        </div>
    </div>
</div>

## Models in Practice

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Precision vs explainability</b></p>
                <ul>
                    <li>The neural network may be <b>more accurate</b></li>
                    <li>The linear model is <b>easier to explain</b> to a decision-maker</li>
                    <li>For a public decision, explainability often <b>wins</b></li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>No model removes <b>uncertainty</b> — there is no Laplace demon. We report what the model supports <b>and</b> what it cannot.</p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
