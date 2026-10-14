<!-- SLIDES: -->

## Regularisation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/9/96/Pyplot_overfitting.png" alt="Overfitting" style="height: 300px">
                <div class="footnote">Overfitting - ThirdOrderLogic, CC BY 4.0 <https://creativecommons.org/licenses/by/4.0>, via Wikimedia Commons</div>
            </div>
            <div class="column vertical-top text-left" style="width: 50%">
                <p><b>Last session:</b> underfitting, overfitting, and regularisation</p>
$$
\text{Cost}_{L,\lambda}(h) = \text{EmpLoss}_{L,E}(h) + \lambda \cdot \text{Complexity}(h)
$$
                <p>In neural networks</p>
                <ul>
                    <li><p><b>Weight penalty:</b> $\text{Complexity}(h) = \sum_{l} \|\mathbf{W}^{(l)}\|_F^2$</p></li>
                    <li><p><b>Early stopping:</b> stop training when the validation loss stops improving</p></li>
                    <li><p><b>Dropout:</b> randomly switch off hidden units during training</p></li>
                </ul>
</div>
        </div>
    </div>
</div>

## Regularisation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <p><b>Regularization Techniques:</b></p>
                <br>
                <p><b>Dropout:</b> Randomly deactivate neurons during training</p>
$$
y_i = \begin{cases} \frac{x_i}{1-p} & \text{with probability } 1-p \\ 0 & \text{with probability } p \end{cases}
$$
<br>
<p><b>$L_2$ Regularization:</b> Add penalty to loss function</p>
$$
E_{\text{reg}} = E + \lambda \sum_{l=1}^{L} \|\mathbf{W}^{(l)}\|_F^2
$$
<br>
<p><b>Early Stopping:</b> Stop training when validation loss increases</p>
<br>
<p><b>Data Augmentation:</b> Create additional training examples through transformations</p>
</div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
