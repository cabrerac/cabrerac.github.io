<!-- SLIDES: -->

## Linear Classifiers

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p>Linear classifiers are models that separate data into classes using a <b>linear decision boundary</b>. These classifiers are functions that can decide if an input (i.e., vectors of numbers) belong to a specific class or not.</p>
            </div>
        </div>
    </div>
</div>

## Linear Classifiers

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/2/20/Svm_separating_hyperplanes.png" alt="SVM Separating Hyperplanes" style="max-width: 70%; height: auto;">
                <div class="footnote">SVM Separating Hyperplanes - Cyc, Public domain, via Wikimedia Commons.</div>
            </div>
            <div class="column vertical-top text-left" style="width: 50%">
                <p>A decision boundary is a line (or a surface in higher dimensions) that separates data into classes.</p>
            </div>
        </div>
    </div>
</div>

## Linear Classifiers

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/2/20/Svm_separating_hyperplanes.png" alt="SVM Separating Hyperplanes" style="max-width: 70%; height: auto;">
                <div class="footnote">SVM Separating Hyperplanes - Cyc, Public domain, via Wikimedia Commons.</div>
            </div>
            <div class="column vertical-top text-left" style="width: 50%">
                <p>A decision boundary is a line (or a surface in higher dimensions) that separates data into classes.</p>
                <br>
                <p>The hypothesis is the result of passing a linear function through a threshold function:</p>
<br>
$$
h_\mathbf{w}(\mathbf{x}) = \text{Threshold}(\mathbf{w} \cdot \mathbf{x})
$$
</div>
        </div>
    </div>
</div>

## Linear Classifiers

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/2/20/Svm_separating_hyperplanes.png" alt="SVM Separating Hyperplanes" style="max-width: 70%; height: auto;">
                <div class="footnote">SVM Separating Hyperplanes - Cyc, Public domain, via Wikimedia Commons.</div>
            </div>
            <div class="column vertical-top text-left" style="width: 50%">
                <p>A decision boundary is a line (or a surface in higher dimensions) that separates data into classes.</p>
                <br>
                <p>The hypothesis is the result of passing a linear function through a threshold function:</p>
<br>
$$
h_\mathbf{w}(\mathbf{x}) = \text{Threshold}(\mathbf{w} \cdot \mathbf{x})
$$
<img src="{{ site.url }}/assets/media/diagrams/threshold-step.svg" alt="Regression Fit" style="max-width: 100%; height: auto;">
<div class="footnote">Threshold Function.</div>
$$
\text{Threshold}(z) = \begin{cases}
1 & \text{if } z \geq 0 \\
0 & \text{otherwise}
\end{cases}
$$
</div>
        </div>
    </div>
</div>

## Linear Classifiers

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <br>
                <p>The optimal hypothesis is the one that minimises the loss function:</p>
                <br>
$$
h^* = \underset{h \in H}{\arg\min} \; \text{Loss}(h)
$$
<br>Where $H$ is the hypothesis space.
<br>
$$
\mathbf{w}^* = \underset{\mathbf{w}}{\arg\min} \; (y - h_\mathbf{w}(\mathbf{x}))^2
$$
</div>
            <div class="column vertical-middle text-left" style="width: 50%">
$$
h_\mathbf{w}(\mathbf{x}) = \text{Threshold}(\mathbf{w} \cdot \mathbf{x})
$$
<img src="{{ site.url }}/assets/media/diagrams/threshold-step.svg" alt="Regression Fit" style="max-width: 100%; height: 150%;">
<div class="footnote">Threshold Function.</div>
$$
\text{Threshold}(z) = \begin{cases}
1 & \text{if } z \geq 0 \\
0 & \text{otherwise}
\end{cases}
$$
</div>
        </div>
    </div>
</div>

## Linear Classifiers

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <br>
                <p>The optimal hypothesis is the one that minimises the loss function:</p>
                <br>
$$
h^* = \underset{h \in H}{\arg\min} \; \text{Loss}(h)
$$
<br>Where $H$ is the hypothesis space.
<br>
$$
\mathbf{w}^* = \underset{\mathbf{w}}{\arg\min} \; (y - h_\mathbf{w}(\mathbf{x}))^2
$$
<br>
<p>Partial derivatives and gradient methods do not work. Instead, we apply <b>perceptron learning rule.</b></p>
</div>
            <div class="column vertical-middle text-left" style="width: 50%">
$$
h_\mathbf{w}(\mathbf{x}) = \text{Threshold}(\mathbf{w} \cdot \mathbf{x})
$$
<img src="{{ site.url }}/assets/media/diagrams/threshold-step.svg" alt="Regression Fit" style="max-width: 100%; height: 150%;">
<div class="footnote">Threshold Function.</div>
$$
\text{Threshold}(z) = \begin{cases}
1 & \text{if } z \geq 0 \\
0 & \text{otherwise}
\end{cases}
$$
</div>
        </div>
    </div>
</div>

## Linear Classifiers

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <br>
                <p>Perceptron update rule:</p>
                <br>
$$
w_i \leftarrow w_i + \alpha (y - h_\mathbf{w}(\mathbf{x})) x_i
$$
<br>
<p>The rule is applied one example at a time, choosing examples at random (as in stochastic gradient descent).</p>
</div>
            <div class="column vertical-middle text-left" style="width: 50%">
$$
h_\mathbf{w}(\mathbf{x}) = \text{Threshold}(\mathbf{w} \cdot \mathbf{x})
$$
<img src="{{ site.url }}/assets/media/diagrams/threshold-step.svg" alt="Regression Fit" style="max-width: 100%; height: 150%;">
<div class="footnote">Threshold Function.</div>
$$
\text{Threshold}(z) = \begin{cases}
1 & \text{if } z \geq 0 \\
0 & \text{otherwise}
\end{cases}
$$
</div>
        </div>
    </div>
</div>

## Linear Classifiers

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <br>
                <p>An alternative to the discrete threshold function is the <b>logistic function</b>, which is smooth and differentiable.</p> 
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
<img src="{{ site.url }}/assets/media/diagrams/threshold-step.svg" alt="Regression Fit" style="max-width: 100%; height: auto;">
<div class="footnote">Threshold Function.</div>
<img src="https://upload.wikimedia.org/wikipedia/commons/8/88/Logistic-curve.svg" alt="Logistic Curve" style="max-width: 60%; height: auto;">
<div class="footnote">Logistic Curve - Qef, Public domain, via Wikimedia Commons.</div>
</div>
        </div>
    </div>
</div>

## Linear Classifiers

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <br>
                <p>An alternative to the discrete threshold function is the <b>logistic function</b>, which is smooth and differentiable.</p> 
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
$$
h_\mathbf{w}(\mathbf{x}) = \sigma(\mathbf{w} \cdot \mathbf{x})
$$
<img src="https://upload.wikimedia.org/wikipedia/commons/8/88/Logistic-curve.svg" alt="Logistic Curve" style="max-width: 70%; height: auto;">
<div class="footnote">Logistic Curve - Qef, Public domain, via Wikimedia Commons.</div>
$$
\sigma(z) = \frac{1}{1 + e^{-z}}
$$
</div>
        </div>
    </div>
</div>

## Linear Classifiers

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <br>
                <p>An alternative to the discrete threshold function is the <b>logistic function</b>, which is smooth and differentiable. The process of finding the optimal hypothesis is called <b>logistic regression.</b></p>
<br>
$$
h^* = \underset{h \in H}{\arg\min} \; \text{Loss}(y - h_\mathbf{w}(\mathbf{x}))
$$
<br>
$$
h^* = \underset{h \in H}{\arg\min} \; \text{Loss}(y - \sigma(\mathbf{w} \cdot \mathbf{x}))
$$
<br>Where $H$ is the hypothesis space.
</div>
            <div class="column vertical-middle text-left" style="width: 50%">
$$
h_\mathbf{w}(\mathbf{x}) = \sigma(\mathbf{w} \cdot \mathbf{x})
$$
<img src="https://upload.wikimedia.org/wikipedia/commons/8/88/Logistic-curve.svg" alt="Logistic Curve" style="max-width: 70%; height: auto;">
<div class="footnote">Logistic Curve - Qef, Public domain, via Wikimedia Commons.</div>
$$
\sigma(z) = \frac{1}{1 + e^{-z}}
$$
</div>
        </div>
    </div>
</div>

## Linear Classifiers

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <br>
                <p>An alternative to the discrete threshold function is the <b>logistic function</b>, which is smooth and differentiable. The process of finding the optimal hypothesis is called <b>logistic regression.</b></p>
<br>
$$
h^* = \underset{h \in H}{\arg\min} \; \text{Loss}(y - h_\mathbf{w}(\mathbf{x}))
$$
<br>
$$
h^* = \underset{h \in H}{\arg\min} \; \text{Loss}(y - \sigma(\mathbf{w} \cdot \mathbf{x}))
$$
<br>Where $H$ is the hypothesis space.
<br>
$$
\mathbf{w}^* = \underset{\mathbf{w}}{\arg\min} \; (y - \sigma(\mathbf{w} \cdot \mathbf{x}))^2
$$
</div>
            <div class="column vertical-middle text-left" style="width: 50%">
$$
h_\mathbf{w}(\mathbf{x}) = \sigma(\mathbf{w} \cdot \mathbf{x})
$$
<img src="https://upload.wikimedia.org/wikipedia/commons/8/88/Logistic-curve.svg" alt="Logistic Curve" style="max-width: 70%; height: auto;">
<div class="footnote">Logistic Curve - Qef, Public domain, via Wikimedia Commons.</div>
$$
\sigma(z) = \frac{1}{1 + e^{-z}}
$$
</div>
        </div>
    </div>
</div>

## Linear Classifiers

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
<p>Following the gradient descent algorithm, the update rule is:</p>
<br>
$$
w_i \leftarrow w_i - \alpha \frac{\partial \text{Loss}(y - h_\mathbf{w}(\mathbf{x}))}{\partial w_i}
$$
</div>
        </div>
    </div>
</div>

## Linear Classifiers

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
<p>Following the gradient descent algorithm, the update rule is:</p>
<br>
$$
w_i \leftarrow w_i - \alpha \frac{\partial \text{Loss}(y - h_\mathbf{w}(\mathbf{x}))}{\partial w_i}
$$
<br>
<p>The loss function is represented as a composition of functions:</p>
<br>
$$
\text{Loss}(w) = (y - \sigma(\mathbf{w} \cdot \mathbf{x}))^2  \; ; \; f(w)= \mathbf{w} \cdot \mathbf{x} \; ; \; g(f)= \sigma(f) \; ; \; h(g)= (y - g)^2
$$
</div>
        </div>
    </div>
</div>

## Linear Classifiers

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
<p>Following the gradient descent algorithm, the update rule is:</p>
<br>
$$
w_i \leftarrow w_i - \alpha \frac{\partial \text{Loss}(y - h_\mathbf{w}(\mathbf{x}))}{\partial w_i}
$$
<br>
<p>The loss function is represented as a composition of functions:</p>
<br>
$$
\text{Loss}(w) = (y - \sigma(\mathbf{w} \cdot \mathbf{x}))^2  \; ; \; f(w)= \mathbf{w} \cdot \mathbf{x} \; ; \; g(f)= \sigma(f) \; ; \; h(g)= (y - g)^2
$$
<br>
<p>We need to differentiate the loss function using the <b>chain rule</b> to compute the gradients:</p>
<br>
$$
\frac{\partial L}{\partial \mathbf{w}} = \frac{\partial h}{\partial g} \cdot \frac{\partial g}{\partial f} \cdot \frac{\partial f}{\partial \mathbf{w}}
$$
</div>
        </div>
    </div>
</div>

## Linear Classifiers

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
<p>Following the gradient descent algorithm, the update rule is:</p>
<br>
$$
w_i \leftarrow w_i - \alpha \frac{\partial \text{Loss}(y - h_\mathbf{w}(\mathbf{x}))}{\partial w_i}
$$
</div>
        </div>
    </div>
</div>

## Linear Classifiers

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
<p>Following the gradient descent algorithm, the update rule is:</p>
<br>
$$
w_i \leftarrow w_i - \alpha \frac{\partial \text{Loss}(y - h_\mathbf{w}(\mathbf{x}))}{\partial w_i}
$$
<br>
<p>The resulting update rule after solving the partial derivatives:</p>
<br>
$$
w_i \leftarrow w_i + \alpha(y - \sigma(\mathbf{w} \cdot \mathbf{x})) \cdot \sigma(\mathbf{w} \cdot \mathbf{x})(1 - \sigma(\mathbf{w} \cdot \mathbf{x})) \cdot x_i
$$
<br>
<p>The gradient descent algorithm is applied using this update rule.</p>
</div>
        </div>
    </div>
</div>

## Linear Classifiers

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 40%">
                <img src="https://upload.wikimedia.org/wikipedia/commons/a/a3/Gradient_descent.gif" alt="Gradient Descent Algorithm" style="max-width: 100%; height: auto;">
                <div class="footnote">Gradient Descent Algorithm - Jacopo Bertolotti, CC0, via Wikimedia Commons.</div>
            </div>
            <div class="column vertical-top text-left" style="width: 60%">
                <br>
                <p><b>Gradient Descent for Logistic Regression</b></p>
                <p>The gradient of the loss function is:</p>
<br>
$$
\nabla_{\mathbf{w}}\text{Loss}(\mathbf{w}) = 2(y - \sigma(\mathbf{w} \cdot \mathbf{x})) \cdot \sigma(\mathbf{w} \cdot \mathbf{x})(1 - \sigma(\mathbf{w} \cdot \mathbf{x})) \cdot \mathbf{x}
$$
<br>Update rule for $\mathbf{w}$:
$$
\mathbf{w} \leftarrow \mathbf{w} - \alpha\nabla_{\mathbf{w}}\text{Loss}(\mathbf{w})
$$
<br>
$$
\mathbf{w} \leftarrow \mathbf{w} + \alpha(y - \sigma(\mathbf{w} \cdot \mathbf{x})) \cdot \sigma(\mathbf{w} \cdot \mathbf{x})(1 - \sigma(\mathbf{w} \cdot \mathbf{x})) \cdot \mathbf{x}
$$
<br>Where $α$ is the learning rate.
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: --> 