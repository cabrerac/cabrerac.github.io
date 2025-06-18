<!-- SLIDES: -->

## Linear Classifiers

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p>Linear classifiers are models that separate data into classes using a <b>linear decision boundary</b>.</p>
            </div>
        </div>
    </div>
</div>

## Linear Classifiers

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <br>            
                <p>A decision boundary is a line (or a surface in higher dimensions) that separate data in classes. The hypothesis is the result of passing a linear function through a threshold function:</p>
                <br>
                <img src="{{ site.url }}/assets/media/diagrams/threshold-step.svg" alt="Regression Fit" style="max-width: 90%; height: auto;">
                <div class="footnote">Threshold Function.</div>
                <br>
$$
h_w(x) = Threshold(w . x)
$$
<br>Where $\mathbf{x}$ is the feature vector, $\mathbf{w}$ is the weight vector, and $w_0$ is the bias term.
            </div>
        </div>
    </div>
</div>

## Linear Classifiers

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <br>
                <p>The decision boundary is defined by the set of points where:</p>
                <br>
$$
\mathbf{w}^T\mathbf{x} + w_0 = 0
$$
<br>
<p>This boundary separates the input space into two regions, each corresponding to a class.</p>
            </div>
        </div>
    </div>
</div>

## Linear Classifiers

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <br>
                <p>The loss function for a linear classifier (using the perceptron criterion) is:</p>
                <br>
$$
\text{Loss}(\mathbf{w}) = -\sum_{i \in \mathcal{M}} y_i (\mathbf{w}^T\mathbf{x}_i + w_0)
$$
<br>
<p>Where $\mathcal{M}$ is the set of misclassified examples, $y_i$ is the true label ($+1$ or $-1$), and $\mathbf{x}_i$ is the feature vector for example $i$.</p>
            </div>
        </div>
    </div>
</div>

## Linear Classifiers

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <br>
                <p>The gradient of the perceptron loss with respect to the weights is:</p>
                <br>
$$
\nabla_{\mathbf{w}}\text{Loss}(\mathbf{w}) = -\sum_{i \in \mathcal{M}} y_i \mathbf{x}_i
$$
<br>
<p>For the bias term:</p>
<br>
$$
\frac{\partial \text{Loss}}{\partial w_0} = -\sum_{i \in \mathcal{M}} y_i
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
                <p>We use the gradient to update the weights:</p>
                <br>
$$
\mathbf{w} \leftarrow \mathbf{w} - \alpha \nabla_{\mathbf{w}}\text{Loss}(\mathbf{w})
$$
<br>
<p>Substituting the gradient:</p>
$$
\mathbf{w} \leftarrow \mathbf{w} + \alpha \sum_{i \in \mathcal{M}} y_i \mathbf{x}_i
$$
<br>
<p>And for the bias:</p>
$$
w_0 \leftarrow w_0 + \alpha \sum_{i \in \mathcal{M}} y_i
$$
<br>Where $\alpha$ is the learning rate.
            </div>
        </div>
    </div>
</div>

## Linear Classifiers

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <br>
                <p>An alternative to the discrete perceptron loss is the <b>sigmoid (logistic) loss function</b>, which is smooth and differentiable. The sigmoid loss (logistic loss) for binary classification is:</p>
                <br>
$$
\text{Loss}(\mathbf{w}) = \sum_{i=1}^N \log\left(1 + \exp(-y_i (\mathbf{w}^T\mathbf{x}_i + w_0))\right)
$$
<br>Where $y_i \in \{-1, +1\}$ is the true label, $\mathbf{x}_i$ is the feature vector, $\mathbf{w}$ is the weight vector, and $w_0$ is the bias term.
<br>
<p><b>Advantages:</b></p>
<ul>
  <li>Smooth and differentiable, enabling gradient-based optimization</li>
  <li>Provides a probabilistic interpretation of the output via the sigmoid function</li>
  <li>Commonly used in logistic regression</li>
</ul>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: --> 