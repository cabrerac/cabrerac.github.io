<!-- SLIDES: -->

## Multivariate Linear Regression

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p>Multivariate regression extends the simple linear model to handle <b>multiple input features</b>. The model learns a function that maps multiple input variables to a continuous output.</p>
            </div>
        </div>
    </div>
</div>

## Multivariate Linear Regression

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <br>
                <p>In these problems, each example is a <b>n-element vector</b>. The hypotheses space <em><b>H</b></em> now includes linear functions of multiple continuous-valued inputs and a single continuous output.</p>
                <br>
$$
y = w_0 + w_1x_1 + w_2x_2 + ... + w_nx_n \; ; \; \mathbf{w} = \langle w_0, w_1, w_2, ..., w_n \rangle
$$
</div>
        </div>
    </div>
</div>

## Multivariate Linear Regression

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <br>
                <p>In these problems, each example is a <b>n-element vector</b>. The hypotheses space <em><b>H</b></em> now includes linear functions of multiple continuous-valued inputs and a single continuous output.</p>
                <br>
$$
y = w_0 + w_1x_1 + w_2x_2 + ... + w_nx_n \; ; \; \mathbf{w} = \langle w_0, w_1, w_2, ..., w_n \rangle
$$
<br>We want to find the $h$ that best fits the data.
<br>
$$
h_w = w_0 + w_1x_1 + w_2x_2 + ... + w_nx_n
$$
</div>
        </div>
    </div>
</div>

## Multivariate Linear Regression

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <br>
                <p>In these problems, each example is a <b>n-element vector</b>. The hypotheses space <em><b>H</b></em> now includes linear functions of multiple continuous-valued inputs and a single continuous output.</p>
                <br>
$$
y = w_0 + w_1x_1 + w_2x_2 + ... + w_nx_n \; ; \; \mathbf{w} = \langle w_0, w_1, w_2, ..., w_n \rangle
$$
<br>We want to find the $h$ that best fits the data.
<br>
$$
h_w = w_0 + w_1x_1 + w_2x_2 + ... + w_nx_n
$$
<br>
<p>In vector notation:</p>
$$
y = \mathbf{w}^T\mathbf{x} + w_0
$$
<br>Where $\mathbf{x}$ is the feature vector, $\mathbf{w}$ is the parameters vector, and $w_0$ is a bias term.
</div>
        </div>
    </div>
</div>

## Multivariate Linear Regression

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <br>
                <p>The loss function for multivariate regression is:</p>
                <br>
$$
\text{Loss}(h_\mathbf{w}) = \sum_{i=1}^N (y_i - (h_\mathbf{w}))^2
$$
$$
\text{Loss}(h_\mathbf{w}) = \sum_{i=1}^N (y_i - (\mathbf{w}^T\mathbf{x}_i + w_0))^2
$$
</div>
        </div>
    </div>
</div>

## Multivariate Linear Regression

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <br>
                <p>The loss function for multivariate regression is:</p>
                <br>
$$
\text{Loss}(h_\mathbf{w}) = \sum_{i=1}^N (y_i - (h_\mathbf{w}))^2
$$
$$
\text{Loss}(h_\mathbf{w}) = \sum_{i=1}^N (y_i - (\mathbf{w}^T\mathbf{x}_i + w_0))^2
$$
<br>
<p>In matrix notation:</p>
$$
\text{Loss}(h_\mathbf{w}) = ||\mathbf{y} - \mathbf{X}\mathbf{w}||^2
$$
<br><br>Where $\mathbf{y}$ is the target vector, $\mathbf{X}$ is the feature matrix, and $\mathbf{w}$ is the weight vector.
</div>
        </div>
    </div>
</div>

## Multivariate Linear Regression

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <br>
                <p>Given the Loss function:</p>
$$
\text{Loss}(h_\mathbf{w}) = ||\mathbf{y} - \mathbf{X}\mathbf{w}||^2
$$
</div>
        </div>
    </div>
</div>

## Multivariate Linear Regression

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <br>
                <p>Given the Loss function:</p>
$$
\text{Loss}(h_\mathbf{w}) = ||\mathbf{y} - \mathbf{X}\mathbf{w}||^2
$$
<br>We want to find $\mathbf{w}^*$
$$
\mathbf{w}^* = \underset{\mathbf{w}}{\arg\min} ||\mathbf{y} - \mathbf{X}\mathbf{w}||^2
$$
</div>
        </div>
    </div>
</div>

## Multivariate Linear Regression

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <br>
                <p>Given the Loss function:</p>
$$
\text{Loss}(h_\mathbf{w}) = ||\mathbf{y} - \mathbf{X}\mathbf{w}||^2
$$
<br>We want to find $\mathbf{w}^*$
$$
\mathbf{w}^* = \underset{\mathbf{w}}{\arg\min} ||\mathbf{y} - \mathbf{X}\mathbf{w}||^2
$$
<br>Taking the derivative with respect to $\mathbf{w}$ and setting to zero:
$$
\frac{\partial}{\partial \mathbf{w}}||\mathbf{y} - \mathbf{X}\mathbf{w}||^2 = 0
$$
</div>
        </div>
    </div>
</div>

## Multivariate Linear Regression

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <br>
                <p>Given the Loss function:</p>
$$
\text{Loss}(h_\mathbf{w}) = ||\mathbf{y} - \mathbf{X}\mathbf{w}||^2
$$
<br>We want to find $\mathbf{w}^*$
$$
\mathbf{w}^* = \underset{\mathbf{w}}{\arg\min} ||\mathbf{y} - \mathbf{X}\mathbf{w}||^2
$$
<br>Taking the derivative with respect to $\mathbf{w}$ and setting to zero:
$$
\frac{\partial}{\partial \mathbf{w}}||\mathbf{y} - \mathbf{X}\mathbf{w}||^2 = 0
$$
<br>
<p>This leads to the normal equation:</p>
$$
\mathbf{w}^* = (\mathbf{X}^T\mathbf{X})^{-1}\mathbf{X}^T\mathbf{y}
$$
</div>
        </div>
    </div>
</div>

## Multivariate Linear Regression

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 40%">
                <img src="https://upload.wikimedia.org/wikipedia/commons/a/a3/Gradient_descent.gif" alt="Gradient Descent Algorithm" style="max-width: 100%; height: auto;">
                <div class="footnote">Gradient Descent Algorithm - Jacopo Bertolotti, CC0, via Wikimedia Commons.</div>
            </div>
            <div class="column vertical-top text-left" style="width: 60%">
                <br>
                <p><b>Gradient Descent for Multivariate Regression</b></p>
                <p>The gradient of the loss function is:</p>
<br>
$$
\nabla_{\mathbf{w}}\text{Loss}(\mathbf{w}) = -2\mathbf{X}^T(\mathbf{y} - \mathbf{X}\mathbf{w})
$$
</div>
        </div>
    </div>
</div>

## Multivariate Linear Regression

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 40%">
                <img src="https://upload.wikimedia.org/wikipedia/commons/a/a3/Gradient_descent.gif" alt="Gradient Descent Algorithm" style="max-width: 100%; height: auto;">
                <div class="footnote">Gradient Descent Algorithm - Jacopo Bertolotti, CC0, via Wikimedia Commons.</div>
            </div>
            <div class="column vertical-top text-left" style="width: 60%">
                <br>
                <p><b>Gradient Descent for Multivariate Regression</b></p>
                <p>The gradient of the loss function is:</p>
<br>
$$
\nabla_{\mathbf{w}}\text{Loss}(\mathbf{w}) = -2\mathbf{X}^T(\mathbf{y} - \mathbf{X}\mathbf{w})
$$
<br>Update rule for $\mathbf{w}$:
$$
\mathbf{w} \leftarrow \mathbf{w} - \alpha\nabla_{\mathbf{w}}\text{Loss}(\mathbf{w})
$$
<br>
$$
\mathbf{w} \leftarrow \mathbf{w} + \alpha\mathbf{X}^T(\mathbf{y} - \mathbf{X}\mathbf{w})
$$
<br>Where $α$ is the learning rate.
</div>
        </div>
    </div>
</div>

<!-- end SLIDES: --> 