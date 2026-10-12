<!-- SLIDES: -->

## Supervised Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 50%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/5/55/Underfitted_Model.png" alt="Underfitted Model" style="height: 100%">
                <div class="footnote">Underfitted Model - AAStein, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons</div>
            </div>    
        </div>
    </div>
    <div class="row" style="height: 50%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
<p>Underfitting occurs when our hypothesis space $\mathcal{H}$ is too simple to capture the true function $f$</p>
<br>
<p>Even the best hypothesis $h^*$ in $\mathcal{H}$ will have high error because:</p>
<br>
$$
\forall h \in \mathcal{H}, \exists x: |h(x) - f(x)| > \epsilon
$$
<br>
<p>where $\epsilon$ is some small positive number.</p>
            </div>
        </div>
    </div>
</div>

## Supervised Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 50%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/9/96/Pyplot_overfitting.png" alt="Overfitting" style="height: 300px">
                <div class="footnote">Overfitting - ThirdOrderLogic, CC BY 4.0 <https://creativecommons.org/licenses/by/4.0>, via Wikimedia Commons</div>
            </div>    
        </div>
    </div>
    <div class="row" style="height: 50%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
<p>Overfitting occurs when our hypothesis space $\mathcal{H}$ is too complex, leading to:</p>
<br>
<p>Low empirical loss but high generalisation loss:</p>
<br>
$$
\text{EmpLoss}_{L,E}(h^*) \ll \text{GenLoss}_{L}(h^*)
$$
<br>
<p>The hypothesis $h^*$ memorizes the training examples instead of learning the true function $f$.</p>
            </div>
        </div>
    </div>
</div>

## Supervised Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 50%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/9/96/Pyplot_overfitting.png" alt="Overfitting" style="height: 300px">
                <div class="footnote">Overfitting - ThirdOrderLogic, CC BY 4.0 <https://creativecommons.org/licenses/by/4.0>, via Wikimedia Commons</div>
            </div>    
        </div>
    </div>
    <div class="row" style="height: 50%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
<p>Regularisation transforms the loss function into a cost function that penalizes complexity to avoid overfitting</p>
<br>
$$
\text{Cost}_{L,\lambda}(h) = \text{EmpLoss}_{L,E}(h) + \lambda \cdot \text{Complexity}(h)
$$
<vr>
<p>Choosing the complexity function depends on the hypotheses space $\mathcal{H}$. A good example for polynomials will be a function that returns the sum of the squares of coefficients.</p>
            </div>
        </div>
    </div>
</div>

## Supervised Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
<p>Given the new cost function</p>
<br>
$$
\text{Cost}_{L,\lambda}(h) = \text{EmpLoss}_{L,E}(h) + \lambda \cdot \text{Complexity}(h)
$$
<br>
<p>The best hypothesis $h^*$ is the one that minimises the cost:</p>
<br>
$$
h^* = \underset{h \in \mathcal{H}}{\operatorname{argmin}} \text{Cost}_{L,\lambda}(h)
$$
<p>where $\lambda$ is a <b>hyperparameter</b> that controls the trade-off between fitting the data and model complexity and serves as a conversion rate.</p>
<br>
<p>Alternatives to mitigate overfitting are feature selection, hyperparameter tuning, splitting dataset in training, validation, and test data (e.g., cross validation algorithm).</p>
</div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
