<!-- SLIDES: -->

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
(x_1, y_1), (x_2, y_2), ..., (x_N, y_N)
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
<p>For linear regression, we have:</p>
$$
p(y \, | \, \mathbf{x}, \mathbf{w}) = \mathcal{N}(y \, | \, \mathbf{w}^T\mathbf{x}, \sigma^2) \iff y = \mathbf{w}^T\mathbf{x} + \epsilon
$$
<br>Where $\epsilon \sim \mathcal{N}(0, \sigma^2)$ is Gaussian noise with zero mean and variance $\sigma^2$. We seek the parameters $\mathbf{w}$.
<br>So, given a training set of $N$ i.i.d input-output pairs:
<br>
$$
(x_1, y_1), (x_2, y_2), ..., (x_N, y_N)
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

## Probabilistic Interpretation of Linear Regression

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
<br>
$$
\mathbf{w}^* = \underset{\mathbf{w}}{\arg\max} \; p(\mathcal{Y} \, | \, \mathcal{X}, \mathbf{w})
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
$$
\mathbf{w}^* = \underset{\mathbf{w}}{\arg\max} \; p(\mathcal{Y} \, | \, \mathcal{X}, \mathbf{w})
$$
<br>As before, a closed-form solution exists, which makes gradient descent unnecessary. We apply the log transformation to the likelihood function and minimise the negative log-likelihood.
<br>
$$
-\text{log} \, p(\mathcal{Y} \, | \, \mathcal{X}, \mathbf{w}) = -\text{log} \prod_{i=1}^N p(y_i \, | \, \mathbf{x}_i, \mathbf{w}) = - \sum_{i=1}^N \text{log} \, p(y_i \, | \, \mathbf{x}_i, \mathbf{w})
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
$$
\mathbf{w}^* = \underset{\mathbf{w}}{\arg\max} \; p(\mathcal{Y} \, | \, \mathcal{X}, \mathbf{w})
$$
<br>As before, a closed-form solution exists, which makes gradient descent unnecessary. We apply the log transformation to the likelihood function and minimise the negative log-likelihood.
<br>
$$
-\text{log} \, p(\mathcal{Y} \, | \, \mathcal{X}, \mathbf{w}) = -\text{log} \prod_{i=1}^N p(y_i \, | \, \mathbf{x}_i, \mathbf{w}) = - \sum_{i=1}^N \text{log} \, p(y_i \, | \, \mathbf{x}_i, \mathbf{w})
$$
<br>We have that:
$$
\text{log} \, p(\mathcal{Y} \, | \, \mathcal{X}, \mathbf{w}) = - \frac{1}{2\sigma^2} \sum_{i=1}^N (y_i - \mathbf{w}^T\mathbf{x}_i)^2 -\frac{N}{2} \log(2\pi\sigma^2)
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
<br>Ignoring the constant terms:
<br>
$$
\text{log} \, p(\mathcal{Y} \, | \, \mathcal{X}, \mathbf{w}) = - \frac{1}{2\sigma^2} \sum_{i=1}^N (y_i - \mathbf{w}^T\mathbf{x}_i)^2
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
<br>Ignoring the constant terms:
<br>
$$
\text{log} \, p(\mathcal{Y} \, | \, \mathcal{X}, \mathbf{w}) = - \frac{1}{2\sigma^2} \sum_{i=1}^N (y_i - \mathbf{w}^T\mathbf{x}_i)^2
$$
<br>The loss function is defined as:
<br>
$$
\text{Loss}(w) = - \frac{1}{2\sigma^2} \sum_{i=1}^N (y_i - \mathbf{w}^T\mathbf{x}_i)^2
$$
$$
\text{Loss}(w) = - \frac{1}{2\sigma^2} (\mathbf{y} - \mathbf{X}\mathbf{w})^T (\mathbf{y} - \mathbf{X}\mathbf{w}) = - \frac{1}{2\sigma^2} || \mathbf{y} - \mathbf{X}\mathbf{w} ||^2
$$
<br>Where $\mathbf{X}$ is the <em>design matrix</em> as the collection of training inputs and $\mathbf{y}$ is a vector of all targets.
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
<p>Minimising the Loss function is equivalent to minimising the sum of squared errors (MSE).</p>
<br>
$$
\text{Loss}(w) = - \frac{1}{2\sigma^2} (\mathbf{y} - \mathbf{X}\mathbf{w})^T (\mathbf{y} - \mathbf{X}\mathbf{w}) = - \frac{1}{2\sigma^2} || \mathbf{y} - \mathbf{X}\mathbf{w} ||^2
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
<p>Minimising the Loss function is equivalent to minimising the sum of squared errors (MSE).</p>
<br>
$$
\text{Loss}(w) = - \frac{1}{2\sigma^2} (\mathbf{y} - \mathbf{X}\mathbf{w})^T (\mathbf{y} - \mathbf{X}\mathbf{w}) = - \frac{1}{2\sigma^2} || \mathbf{y} - \mathbf{X}\mathbf{w} ||^2
$$
<br>As we did before, we compute the gradient of the Loss and equate it to zero:
<br>
$$
\frac{\partial \text{Loss}(\mathbf{w})}{\partial \mathbf{w}} = \mathbf{0}^T
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
<p>Minimising the Loss function is equivalent to minimising the sum of squared errors (MSE).</p>
<br>
$$
\text{Loss}(w) = - \frac{1}{2\sigma^2} (\mathbf{y} - \mathbf{X}\mathbf{w})^T (\mathbf{y} - \mathbf{X}\mathbf{w}) = - \frac{1}{2\sigma^2} || \mathbf{y} - \mathbf{X}\mathbf{w} ||^2
$$
<br>As we did before, we compute the gradient of the Loss and equate it to zero:
<br>
$$
\frac{\partial \text{Loss}(\mathbf{w})}{\partial \mathbf{w}} = \mathbf{0}^T
$$
<br>Solving the derivatives as we did before:
<br>
$$
\mathbf{w}^* = (\mathbf{X}^T \mathbf{X})^{-1} \mathbf{y}
$$
</div>
        </div>
    </div>
</div>

## Probabilistic Interpretation of Linear Regression

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
<br>The regression problem is considered as:
<br>
$$
p(y \, | \, \mathbf{x}, \mathbf{w}) = \mathcal{N}(y \, | \, f(\mathbf{w}^T \mathbf{x}, \sigma^2)
$$                
<br>We want to maximise the likelihood function of the training data given the model parameters.
<br>
$$
p(\mathcal{Y} \, | \, \mathcal{X}, \mathbf{w}) = p(y_1, y_2, ..., y_N \, | \, \mathbf{x}_1, \mathbf{x}_2, ..., \mathbf{x}_N, \mathbf{w})
$$
<br>Closed-form solution for linear regression:
<br>
$$
\mathbf{w}^* = (\mathbf{X}^T \mathbf{X})^{-1} \mathbf{y}
$$
<br>Where $\mathbf{X}$ is the <em>design matrix</em> as the collection of training inputs and $\mathbf{y}$ is a vector of all targets.
</div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/linear-probabilistic.png" alt="Probabilistic Interpretation" style="max-width: 80%; height: auto;">
                <div class="footnote">Probabilistic Interpretation - <a href="https://www.microsoft.com/en-us/research/wp-content/uploads/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf">(Bishop, 2006)</a>.</div>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->