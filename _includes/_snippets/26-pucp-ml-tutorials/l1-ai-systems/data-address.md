<!-- SLIDES: -->

## Data Address

<div class="rows" style="height: 100%">
    <div class="row" style="height: 75%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/data-science-process.png" alt="Data Science Process" style="height: 450px">
            </div>
        </div>
    </div>
    <div class="row" style="height: 25%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p>Only now do we reach <b>address</b>: using the data we trust to answer the question we started from.</p>
            </div>
        </div>
    </div>
</div>

## Data Address

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p>After assessing the data (i.e., data assess), we need to <b>use the data to address the problem in question</b>. This process includes implementing a <b>Machine Learning algorithm</b> that creates a <b>Machine Learning model</b>.</p>
            </div>
        </div>
    </div>
</div>

## Data Address

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>A Machine Learning algorithm is a set of instructions</b> that are used to train a machine learning model. It defines how the model learns from data and makes predictions or decisions. Linear regression, decision trees, and neural networks are examples of machine learning algorithms.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/ml-algorithm.svg" alt="ML Algorithm" style="height: 500px">
            </div>
        </div>
    </div>
</div>

## Data Address

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>A Machine Learning model is a program</b> that is trained on a dataset and used to make predictions or decisions. The goal is to create a <em>trained model</em> that can generalise well to new, unseen data.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/ml-model.svg" alt="ML Model" style="height: 500px">
            </div>
        </div>
    </div>
</div>

## Data Address

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>A Machine Learning algorithm uses the <b>training process</b> that goes from a specific set of observations to a general rule (i.e., induction). This process adjusts the model internal parameters to minimise prediction errors. In a linear regression model, the algorithm adjusts the slope and the intercept.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/training-process.svg" alt="Training Process" style="height: 500px">
            </div>
        </div>
    </div>
</div>

## Data Address

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>In <b>classification</b> problems, the prediction is one of a finite set of values (e.g., safe / unsafe). In <b>regression</b> problems, the model's output is a number.</p>
                <p>Prediction errors are quantified by a <b>loss function</b> that tells the algorithm how far the prediction is from the target. Mean Squared Error is the common choice for regression.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/ml-model.svg" alt="ML Model" style="height: 500px">
            </div>
        </div>
    </div>
</div>

## Data Address

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 40%">
                <p><b>Our address step today</b></p>
                <ul>
                    <li>A regression problem: predict the horizontal location error from the station coverage gap</li>
                    <li>One feature, one target, a straight line</li>
                    <li>It is a first fit to practise the step, not an inspection tool</li>
                    <li>The rows the model never saw are part of the result</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 60%">

```python
from sklearn.linear_model import LinearRegression

usable = catalog[["gap", "horizontalError"]].dropna()
X = usable[["gap"]].to_numpy()
y = usable["horizontalError"].to_numpy()
model = LinearRegression().fit(X, y)
```

</div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
