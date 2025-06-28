<!-- SLIDES: -->

## ML Definition

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <div style="font-size: 2em; margin: 40px 0;">
$$\text{model} + \text{data} \stackrel{\text{compute}}{\rightarrow} \text{prediction}$$
</div>
                <div style="margin-top: 30px;">
                </div>
            </div>
        </div>
    </div>
</div>

## The Data Science Process

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/data-science-process.png" alt="Data Science Process" style="height: 500px">
            </div>
        </div>
    </div>
</div>

## Machine Learning Pipeline

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 95%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/data-assess-pipeline.svg" alt="Data Assess Pipeline" style="height: 500px">
            </div>
        </div>
    </div>
</div>

## Probabilistic Interpretation of Linear Regression

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p>Linear regression can be interpreted from a <b>probabilistic perspective</b>, where we model the uncertainty in our predictions using probability distributions.</p>
            </div>
        </div>
    </div>
</div>

## Probabilistic Interpretation of Linear Regression

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>Linear regression can be interpreted from a <b>probabilistic perspective</b>, where we model the uncertainty in our predictions using probability distributions.</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/linear-probabilistic.png" alt="Probabilistic Interpretation" style="max-width: 80%; height: auto;">
                <div class="footnote">Probabilistic Interpretation - <a href="https://www.microsoft.com/en-us/research/wp-content/uploads/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf">(Bishop, 2006)</a>.</div>
            </div>
        </div>
    </div>
</div>

## Probabilistic Interpretation of Linear Regression

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <br>
                <p>Instead of assuming deterministic relationships, we model the regression problem with the likelihood function:</p>
<br>
$$
p(y \, | \, \mathbf{x}) = \mathcal{N}(y \, | \, f(\mathbf{x}), \sigma^2)
$$                
<br>The functional relationship between $x$ and $y$ is given as:
<br>
$$
y = f(\mathbf{x}) + \epsilon
$$
<br>Where $\epsilon \sim \mathcal{N}(0, \sigma^2)$ is Gaussian noise with zero mean and variance $\sigma^2$.
<br>We want to find $h$ that approximates the unknown function $f$ and generalises well.
</div>
        </div>
    </div>
</div>

## Probabilistic Interpretation of Linear Regression

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <br>
<p>For linear regression, we have:</p>
$$
p(y \, | \, \mathbf{x}, \mathbf{w}) = \mathcal{N}(y \, | \, \mathbf{w}^T\mathbf{x}, \sigma^2) \iff y = \mathbf{w}^T\mathbf{x} + \epsilon
$$
<br>Where $\epsilon \sim \mathcal{N}(0, \sigma^2)$ is Gaussian noise with zero mean and variance $\sigma^2$. We seek the parameters $\mathbf{w}$.
<br>So, given a training set of $N$ i.i.d input-output pairs:
<br>
$$
(\mathbf{x}_1, y_1), (\mathbf{x}_2, y_2), ..., (\mathbf{x}_N, y_N)
$$
<br>The likelihood factorises according to:
<br>
$$
p(\mathcal{Y} \, | \, \mathcal{X}, \mathbf{w}) = p(y_1, y_2, ..., y_N \, | \, \mathbf{x}_1, \mathbf{x}_2, ..., \mathbf{x}_N, \mathbf{w})
$$
</div>
        </div>
    </div>
</div>

## Probabilistic Interpretation of Linear Regression

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
<br>
<p>The likelihood function tells us how likely the observed data is given the specific parameters:</p>
<br>
$$
p(y_1, y_2, ..., y_N \, | \, \mathbf{x}_1, \mathbf{x}_2, ..., \mathbf{x}_N, \mathbf{w}) = \prod_{i=1}^N p(y_i \, | \, \mathbf{x}_i, \mathbf{w})
$$
$$
\prod_{i=1}^N p(y_i \, | \, \mathbf{x}_i, \mathbf{w}) = \prod_{i=1}^N \mathcal{N} (y_i \, | \, \mathbf{w}^T\mathbf{x}, \sigma^2 )
$$
<br>We estimate $\mathbf{w}$ by maximising the likelihood.
<br> 
$$
\mathbf{w}^* = \underset{\mathbf{w}}{\arg\max} \; p(\mathcal{Y} \, | \, \mathcal{X}, \mathbf{w})
 $$
</div>
        </div>
    </div>
</div>

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

## The Perceptron

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p>The perceptron is one of the earliest and simplest <b>artificial neural network models</b> for binary classification.</p>
            </div>
        </div>
    </div>
</div>

## The Perceptron

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/1/1a/330-PSA-80-60_%28USN_710739%29_%2820897323365%29.jpg" alt="Rosenblatt" style="max-width: 75%; height: auto;">
                <div class="footnote">Dr. Frank Rosenblatt and the Mark I - National Museum of the U.S. Navy, Public domain, via Wikimedia Commons.</div>
            </div>
            <div class="column vertical-top text-left" style="width: 50%">
                <p>The perceptron was simulated by <b>Frank Rosenblatt</b> in 1957 on an IBM 704 machine as a model for biological neural networks. The neural network was invented in 1943 by <a href="https://www.cs.cmu.edu/~epxing/Class/10715/reading/McCulloch.and.Pitts.pdf">McCulloch & Pitts</a>.</p>
                <br>
                <p>By 1962 Rosenblatt published the <a href="https://gwern.net/doc/ai/nn/1962-rosenblatt-principlesofneurodynamics.pdf">"Principles of Neurodynamics: Perceptrons and the Theory of Brain Mechanisms"</a>.</p>
                <br>
                <p>The Perceptron machine is named Mark I. It is a special-purpose hardware that implemented the perceptron supervised learning for image recognition.</p>
            </div>
        </div>
    </div>
</div>

## The Perceptron

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/1/13/Mark_I_Perceptron%2C_Figure_2_of_operator%27s_manual.png" alt="Mark I" style="max-width: 100%; height: auto;">
                <div class="footnote">Mark I Perceptron - John C. Hay, Albert E. Murray, Public domain, via Wikimedia Commons</div>
            </div>
            <div class="column vertical-top text-left" style="width: 50%">
                <p>The Perceptron machine is named Mark I. It is a special-purpose hardware that implemented the perceptron supervised learning for image recognition.</p>
                <br>
                <ul>
                    <li><b>Input layer</b>: An array of 400 photocells (20x20 grid) named "sensory units" or "input retina".</li>
                    <li><b>Hidden Layer</b>: 512 perceptrons named "association units" or "A-units".</li>
                    <li><b>Output Layer</b>: 8 perceptrons named "response units" or "R-units".</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## The Perceptron

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/perceptron.svg" alt="Perceptron Architecture" style="max-width: 100%; height: auto;">
                <div class="footnote">Perceptron Architecture.</div>
            </div>
            <div class="column vertical-top text-left" style="width: 50%">
                <p>The perceptron is a linear classifier model (i.e., linear discriminant), with hypothesis space defined by all the functions of the form:</p>
$$
y = f(\mathbf{w}^T\phi(\mathbf{x}))
$$
<br>The function $f(\cdot)$ is similar to the $\text{Threshold}$ function previously defined. $f(\cdot)$ is given by a step function of the form:
$$
f(z) = \begin{cases}
+1 & \text{if } z \geq 0 \\
-1 & \text{otherwise}
\end{cases}
$$
<br>We want to find $\mathbf{w}^*$:
$$
\mathbf{w}^* = \underset{\mathbf{w}}{\arg\min}Loss(y - h_\mathbf{w}(\phi(\mathbf{x})))
$$
</div>
        </div>
    </div>
</div>

## The Perceptron

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/perceptron-step.svg" alt="Perceptron Step Function" style="max-width: 100%; height: auto;">
                <div class="footnote">Perceptron Step Function.</div>
            </div>
            <div class="column vertical-top text-left" style="width: 50%">
<br>The perceptron step function is not differentiable and the gradient is zero almost everywhere:
$$
f(z) = \begin{cases}
+1 & \text{if } z \geq 0 \\
-1 & \text{otherwise}
\end{cases}
$$
<br>We need to derive the <b>perceptron criterion</b>. We know we are seeking parameters vector $\mathbf{w}$ such that features in $\mathbf{x_i}$ in class $C_1$:
$$
\mathbf{w}^T \phi(\mathbf{x_i}) > 0
$$
<br>And for features in $\mathbf{x_i}$ in class $C_2$:
$$
\mathbf{w}^T \phi(\mathbf{x_i}) < 0
$$
</div>
        </div>
    </div>
</div>

## The Perceptron

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/perceptron-loss.svg" alt="Perceptron Loss Function" style="max-width: 100%; height: auto;">
                <div class="footnote">Perceptron Loss Function.</div>
            </div>
            <div class="column vertical-top text-left" style="width: 50%">
<br>The perceptron step function is not differentiable and the gradient is zero almost everywhere:
$$
f(z) = \begin{cases}
+1 & \text{if } z \geq 0 \\
-1 & \text{otherwise}
\end{cases}
$$
<br>Using $y\in{-1, +1}$, all features will satisfy:
$$
\mathbf{w}^T \phi(\mathbf{x_i})y_i  > 0
$$
<br>The loss function is:
$$
Loss(\mathbf{w}) = max(0, -\mathbf{w}^T \phi(\mathbf{x_i})y_i)
$$
</div>
        </div>
    </div>
</div>

## The Perceptron

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <br>
                <img src="{{ site.url }}/assets/media/diagrams/perceptron-loss.svg" alt="Perceptron Loss Function" style="max-width: 100%; height: auto;">
                <br>The loss function is:
$$
Loss(\mathbf{w}) = max(0, -\mathbf{w}^T \phi(\mathbf{x_i})y_i)
$$
<br>
<p>The update rule for a missclassified input is:</p>
<br>
$$
\mathbf{w}_i = \mathbf{w}_i + \alpha\phi(\mathbf{x_i})y_i
$$
</div>
        </div>
    </div>
</div>

## The Perceptron

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 40%">
                <br>
                <p>The perceptron learning algorithm is similar to the stochastic gradient descent.</p>
                <br>
            </div>
            <div class="column vertical-middle text-left" style="width: 60%">
<pre><code>
Initialise weights w randomly
repeat
    for each training example (x, y)
        Compute prediction: y_pred = f(w·Φ(x))
        if y_pred ≠ y then
            Update weights: w = w + αΦ(x)y
until no misclassifications or max iterations
</code></pre>
            </div>
        </div>
    </div>
</div>

## The Perceptron

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <img src="{{ site.url }}/assets/media/images/perceptron-overview.png" alt="Perceptron Overview" style="max-width: 100%; height: auto;">
                <div class="footnote">Perceptron Overview - Andreas Maier, CC BY 4.0 <https://creativecommons.org/licenses/by/4.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: --> 