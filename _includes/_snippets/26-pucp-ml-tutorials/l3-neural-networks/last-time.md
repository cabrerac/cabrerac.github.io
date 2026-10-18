<!-- SLIDES: -->

## Last Time

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-center" style="width: 33%">
                <p><b>Linear regression</b></p>
                <img src="{{ site.url }}/assets/media/diagrams/regression-fit.svg" alt="Regression Fit" style="max-width: 100%; height: auto;">
                <div class="footnote">Linear regression fit.</div>
$$
h_\mathbf{w}(x) = w_{1}x + w_{0}
$$
            </div>
            <div class="column vertical-top text-center" style="width: 33%">
                <p><b>Linear classifiers</b></p>
                <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/2/20/Svm_separating_hyperplanes.png" alt="SVM Separating Hyperplanes" style="max-width: 70%; height: auto;">
                <div class="footnote">SVM Separating Hyperplanes - Cyc, Public domain, via Wikimedia Commons.</div>
$$
h_\mathbf{w}(\mathbf{x}) = \text{Threshold}(\mathbf{w} \cdot \mathbf{x})
$$
            </div>
            <div class="column vertical-top text-center" style="width: 33%">
                <p><b>Hypothesis space and loss</b></p>
                <img src="{{ site.url }}/assets/media/diagrams/regression-hypothesis-space.svg" alt="Hypothesis Space for Regression" style="max-width: 100%; height: auto;">
                <div class="footnote">Example functions described using a linear model.</div>
$$
h^* = \underset{h \in \mathcal{H}}{\arg\min} \; \text{Loss}(h)
$$
            </div>
        </div>
    </div>
</div>

## Last Time

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-center" style="width: 33%">
                <p><b>Gradient descent</b></p>
                <img src="https://upload.wikimedia.org/wikipedia/commons/a/a3/Gradient_descent.gif" alt="Gradient Descent Algorithm" style="max-width: 80%; height: auto;">
                <div class="footnote">Gradient Descent Algorithm - Jacopo Bertolotti, CC0, via Wikimedia Commons.</div>
$$
\mathbf{w} \leftarrow \mathbf{w} - \alpha\nabla_{\mathbf{w}}\text{Loss}(\mathbf{w})
$$
                <p>$\alpha$ is the learning rate</p>
            </div>
            <div class="column vertical-top text-center" style="width: 33%">
                <p><b>Underfitting and overfitting</b></p>
                <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/9/96/Pyplot_overfitting.png" alt="Overfitting" style="max-width: 85%; height: auto;">
                <div class="footnote">Overfitting - ThirdOrderLogic, CC BY 4.0 <https://creativecommons.org/licenses/by/4.0>, via Wikimedia Commons</div>
$$
\text{EmpLoss}_{L,E}(h^*) \ll \text{GenLoss}_{L}(h^*)
$$
                <p>$\mathcal{H}$ too simple or too complex</p>
            </div>
            <div class="column vertical-top text-center" style="width: 33%">
                <p><b>The perceptron</b></p>
                <img src="{{ site.url }}/assets/media/diagrams/perceptron.svg" alt="Perceptron Architecture" style="max-width: 100%; height: auto;">
                <div class="footnote">Perceptron Architecture.</div>
$$
y = f(\mathbf{w}^T\phi(\mathbf{x}))
$$
                <p>A linear classifier</p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
