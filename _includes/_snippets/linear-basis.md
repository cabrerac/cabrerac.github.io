<!-- SLIDES: -->

## Linear Basis Function Models

<div class="rows" style="height: 100%">
    <div class="row" style="height: 45%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 33%">
                <img src="{{ site.url }}/assets/media/diagrams/regression-hypothesis-space.svg" alt="Hypothesis Space for Regression" style="max-width: 75%; height: auto;">
                <div class="footnote">Example functions described using a linear model.</div>
            </div>
            <div class="column vertical-middle text-left" style="width: 33%">
                <img src="{{ site.url }}/assets/media/diagrams/regression-data.svg" alt="Training Data Set" style="max-width: 75%; height: auto;">
                <div class="footnote">Training dataset.</div>
            </div>
            <div class="column vertical-middle text-left" style="width: 33%">
                <img src="{{ site.url }}/assets/media/diagrams/regression-fit.svg" alt="Regression Fit" style="max-width: 75%; height: auto;">
                <div class="footnote">Linear regression fit.</div>
            </div>
        </div>
    </div>
    <div class="row" style="height: 55%">
        <img src="{{ site.url }}/assets/media/images/basis-functions.png" alt="Basis Functions" style="max-width: 95%; height: auto;">
        <div class="footnote">Basis Functions - <a href="https://www.microsoft.com/en-us/research/wp-content/uploads/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf">(Bishop, 2006)</a>.</div>
    </div>
</div>

## Linear Basis Function Models

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p>Linear basis function models extend linear regression by applying <b>non-linear transformations</b> to the input features while keeping the model linear in the parameters.</p>
            </div>
        </div>
    </div>
</div>

## Linear Basis Function Models

<div class="rows" style="height: 100%">
    <div class="row" style="height: 50%">
        <br>
        <p>The model becomes:</p>
$$
y = \mathbf{w}^T\boldsymbol{\phi}(\mathbf{x}) + \epsilon
$$
<br>Where $\boldsymbol{\phi}(\mathbf{x}) = [\phi_1(\mathbf{x}), \phi_2(\mathbf{x}), ..., \phi_M(\mathbf{x})]^T$ is a vector of basis functions.
</div>
    <div class="row" style="height: 50%">
        <img src="{{ site.url }}/assets/media/images/basis-functions.png" alt="Basis Functions" style="max-width: 100%; height: auto;">
        <div class="footnote">Basis Functions - <a href="https://www.microsoft.com/en-us/research/wp-content/uploads/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf">(Bishop, 2006)</a>.</div>
    </div>
</div>

## Linear Basis Function Models

<div class="rows" style="height: 100%">
    <div class="row" style="height: 40%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 33%">
                <br>
<p><b>Polynomial basis:</b></p>
$$
\phi_j(x) = x^j
$$
</div>
            <div class="column vertical-top text-left" style="width: 33%">
                <br>
<p><b>Gaussian basis:</b></p>
$$
\phi_j(x) = \exp\left(-\frac{(x - \mu_j)^2}{2\sigma_j^2}\right)
$$
</div>
            <div class="column vertical-top text-left" style="width: 33%">
                <br>
<p><b>Sigmoid basis:</b></p>
$$
\phi_j(x) = \sigma\left(\frac{x - \mu_j}{s_j}\right)
$$
</div>
        </div>
</div>
    <div class="row" style="height: 60%">
        <img src="{{ site.url }}/assets/media/images/basis-functions.png" alt="Basis Functions" style="max-width: 100%; height: auto;">
        <div class="footnote">Basis Functions - <a href="https://www.microsoft.com/en-us/research/wp-content/uploads/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf">(Bishop, 2006)</a>.</div>
    </div>
</div>

## Linear Basis Function Models

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <br>
                <p>If we apply a probabilistic interpretation, we need to maximise the likelihood of:</p>
                <br>
$$
p(\mathcal{Y} \, | \, \mathcal{X}, \mathbf{w}) = \prod_{i=1}^N \mathcal{N} (y_i \, | \, \mathbf{w}^T \boldsymbol{\Phi}(\mathbf{x}), \sigma^2 )
$$
</div>
        </div>
    </div>
</div>

## Linear Basis Function Models

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <br>
                <p>If we apply a probabilistic interpretation, we need to maximise the likelihood of:</p>
                <br>
$$
p(\mathcal{Y} \, | \, \mathcal{X}, \mathbf{w}) = \prod_{i=1}^N \mathcal{N} (y_i \, | \, \mathbf{w}^T \boldsymbol{\Phi}(\mathbf{x}), \sigma^2 )
$$
<br>
<p>After a similar process (See Chapter 3 in <a href="https://www.microsoft.com/en-us/research/wp-content/uploads/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf">Bishop, 2006</a>), the loss function becomes:</p>
<br>
$$
\text{Loss}(\mathbf{w}) = ||\mathbf{y} - \mathbf{w}^T \boldsymbol{\Phi}||^2
$$
</div>
        </div>
    </div>
</div>

## Linear Basis Function Models

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <br>
                <p>If we apply a probabilistic interpretation, we need to maximise the likelihood of:</p>
                <br>
$$
p(\mathcal{Y} \, | \, \mathcal{X}, \mathbf{w}) = \prod_{i=1}^N \mathcal{N} (y_i \, | \, \mathbf{w}^T \boldsymbol{\Phi}(\mathbf{x}), \sigma^2 )
$$
<br>
<p>After a similar process (See Chapter 3 in <a href="https://www.microsoft.com/en-us/research/wp-content/uploads/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf">Bishop, 2006</a>), the loss function becomes:</p>
<br>
$$
\text{Loss}(\mathbf{w}) = ||\mathbf{y} - \mathbf{w}^T \boldsymbol{\Phi}||^2
$$
<br>
<p>And the normal equation solution:</p>
$$
\mathbf{w}^* = (\boldsymbol{\Phi}^T\boldsymbol{\Phi})^{-1}\boldsymbol{\Phi}^T\mathbf{y}
$$
</div>
        </div>
    </div>
</div>

## Linear Basis Function Models

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
            <br>
$$
\mathbf{w}^* = (\boldsymbol{\Phi}^T\boldsymbol{\Phi})^{-1}\boldsymbol{\Phi}^T\mathbf{y}
$$
</div>
        </div>
    </div>
</div>

## Linear Basis Function Models

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
            <br>
$$
\mathbf{w}^* = (\boldsymbol{\Phi}^T\boldsymbol{\Phi})^{-1}\boldsymbol{\Phi}^T\mathbf{y}
$$
<br>The design matrix $\boldsymbol{\Phi}$ is constructed as:
<br>
$$
\boldsymbol{\Phi} = \begin{bmatrix}
\phi_1(\mathbf{x}_1) & \phi_2(\mathbf{x}_1) & \cdots & \phi_M(\mathbf{x}_1) \\
\phi_1(\mathbf{x}_2) & \phi_2(\mathbf{x}_2) & \cdots & \phi_M(\mathbf{x}_2) \\
\vdots & \vdots & \ddots & \vdots \\
\phi_1(\mathbf{x}_N) & \phi_2(\mathbf{x}_N) & \cdots & \phi_M(\mathbf{x}_N)
\end{bmatrix}
$$
<br>By using basis functions $\phi_j(\mathbf{x})$, we can capture complex, non-linear relationships between the input features and the target variable. The design matrix essentially acts as a bridge, allowing us to apply linear techniques to problems that are inherently non-linear in nature. We can design the matrix and evaluate which design works better using cross-validation. This is essentially <b>feature engineering</b>.
</div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->