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
                <img src="{{ site.url }}/assets/media/images/linear-probabilistic.png" alt="Mark I" style="max-width: 80%; height: auto;">
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
<br>The functional relationship between $x$ and $y$ is give as:
<br>
$$
y = f(\mathbf{x}) + \epsilon
$$
<br>Where $\epsilon \sim \mathcal{N}(0, \sigma^2)$ is Gaussian noise with zero mean and variance $\sigma^2$.
<br>We want to find $h$ that approximates the unkown function $f$ and generalises well.
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
<br>Where $\epsilon \sim \mathcal{N}(0, \sigma^2)$ is Gaussian noise with zero mean and variance $\sigma^2$. We seek for the parameters $\mathbf{w}$.
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
<br>Where $\epsilon \sim \mathcal{N}(0, \sigma^2)$ is Gaussian noise with zero mean and variance $\sigma^2$. We seek for the parameters $\mathbf{w}$.
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
<br>Where $\epsilon \sim \mathcal{N}(0, \sigma^2)$ is Gaussian noise with zero mean and variance $\sigma^2$. We seek for the parameters $\mathbf{w}$.
<br>So, given a training set of $N$ i.i.d input-output pairs:
<br>
$$
(x_1, y_1), (x_2, y_2), ..., (x_N, y_N)
$$
<br>The likelihood factorises according too:
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
<p>The likelihood function tells us how likely is the observed data given the specific parameters:</p>
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
<p>The likelihood function tells us how likely is the observed data given the specific parameters:</p>
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
<br>As before, a closed-form solution exists, which makes gradient descent unnecessary. We apply the log transformation to the likelihood function and minimize the negative log-likelihood.
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
<br>As before, a closed-form solution exists, which makes gradient descent unnecessary. We apply the log transformation to the likelihood function and minimize the negative log-likelihood.
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
<br>The loss functions is defined as:
<br>
$$
\text{Loss}(w) = - \frac{1}{2\sigma^2} \sum_{i=1}^N (y_i - \mathbf{w}^T\mathbf{x}_i)^2
$$
$$
\text{Loss}(w) = - \frac{1}{2\sigma^2} (\mathbf{y} - \mathbf{X}\mathbf{w})^T (\mathbf{y} - \mathbf{X}\mathbf{w}) = - \frac{1}{2\sigma^2} || \mathbf{y} - \mathbf{X}\mathbf{w} ||^2
$$
<br>Where $\mathbf{X}$ is the <em>design matrix</em> as the collection of training inputs and $\mathbf{y}$ is a vector of all training targets.
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
<p>Minimizing the Loss function is equivalent to minimizing the sum of squared errors (MSE).</p>
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
<p>Minimizing the Loss function is equivalent to minimizing the sum of squared errors (MSE).</p>
<br>
$$
\text{Loss}(w) = - \frac{1}{2\sigma^2} (\mathbf{y} - \mathbf{X}\mathbf{w})^T (\mathbf{y} - \mathbf{X}\mathbf{w}) = - \frac{1}{2\sigma^2} || \mathbf{y} - \mathbf{X}\mathbf{w} ||^2
$$
<br>As we did before, we compute the gradient of the Loss and equal it to zero:
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
<p>Minimizing the Loss function is equivalent to minimizing the sum of squared errors (MSE).</p>
<br>
$$
\text{Loss}(w) = - \frac{1}{2\sigma^2} (\mathbf{y} - \mathbf{X}\mathbf{w})^T (\mathbf{y} - \mathbf{X}\mathbf{w}) = - \frac{1}{2\sigma^2} || \mathbf{y} - \mathbf{X}\mathbf{w} ||^2
$$
<br>As we did before, we compute the gradient of the Loss and equal it to zero:
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
            <div class="column vertical-top text-left" style="width: 100%">
                <br>
                <p>This leads to a probabilistic model where the target follows a normal distribution:</p>
                <br>
$$
p(y|\mathbf{x}, \mathbf{w}, \sigma^2) = \mathcal{N}(y|\mathbf{w}^T\mathbf{x}, \sigma^2)
$$
<br>
$$
p(y|\mathbf{x}, \mathbf{w}, \sigma^2) = \frac{1}{\sqrt{2\pi\sigma^2}} \exp\left(-\frac{(y - \mathbf{w}^T\mathbf{x})^2}{2\sigma^2}\right)
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
                <p>For a dataset $\mathcal{D} = \{(\mathbf{x}_1, y_1), ..., (\mathbf{x}_N, y_N)\}$, the likelihood function is:</p>
                <br>
$$
p(\mathcal{D}|\mathbf{w}, \sigma^2) = \prod_{i=1}^N p(y_i|\mathbf{x}_i, \mathbf{w}, \sigma^2)
$$
<br>
$$
p(\mathcal{D}|\mathbf{w}, \sigma^2) = \prod_{i=1}^N \frac{1}{\sqrt{2\pi\sigma^2}} \exp\left(-\frac{(y_i - \mathbf{w}^T\mathbf{x}_i)^2}{2\sigma^2}\right)
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
                <p>Taking the negative log-likelihood (log-likelihood loss):</p>
                <br>
$$
-\log p(\mathcal{D}|\mathbf{w}, \sigma^2) = \frac{N}{2}\log(2\pi\sigma^2) + \frac{1}{2\sigma^2}\sum_{i=1}^N (y_i - \mathbf{w}^T\mathbf{x}_i)^2
$$
<br>
<p>Minimizing this is equivalent to minimizing the sum of squared errors (MSE).</p>
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
                <p>We can also use <b>Bayesian inference</b> by placing a prior on the weights:</p>
                <br>
$$
p(\mathbf{w}) = \mathcal{N}(\mathbf{w}|\mathbf{0}, \alpha^{-1}\mathbf{I})
$$
<br>
<p>The posterior distribution becomes:</p>
$$
p(\mathbf{w}|\mathcal{D}) \propto p(\mathcal{D}|\mathbf{w})p(\mathbf{w})
$$
</div>
        </div>
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
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <br>
                <p>The model becomes:</p>
                <br>
$$
y = \mathbf{w}^T\boldsymbol{\phi}(\mathbf{x}) + \epsilon
$$
<br>Where $\boldsymbol{\phi}(\mathbf{x}) = [\phi_1(\mathbf{x}), \phi_2(\mathbf{x}), ..., \phi_M(\mathbf{x})]^T$ is a vector of basis functions.
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
                <p>Common basis functions include:</p>
                <br>
<p><b>Polynomial basis:</b></p>
$$
\phi_j(x) = x^j
$$
<br>
<p><b>Gaussian basis:</b></p>
$$
\phi_j(x) = \exp\left(-\frac{(x - \mu_j)^2}{2\sigma_j^2}\right)
$$
<br>
<p><b>Sigmoid basis:</b></p>
$$
\phi_j(x) = \sigma\left(\frac{x - \mu_j}{s_j}\right)
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
                <p>The design matrix $\boldsymbol{\Phi}$ is constructed as:</p>
                <br>
$$
\boldsymbol{\Phi} = \begin{bmatrix}
\phi_1(\mathbf{x}_1) & \phi_2(\mathbf{x}_1) & \cdots & \phi_M(\mathbf{x}_1) \\
\phi_1(\mathbf{x}_2) & \phi_2(\mathbf{x}_2) & \cdots & \phi_M(\mathbf{x}_2) \\
\vdots & \vdots & \ddots & \vdots \\
\phi_1(\mathbf{x}_N) & \phi_2(\mathbf{x}_N) & \cdots & \phi_M(\mathbf{x}_N)
\end{bmatrix}
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
                <p>The loss function becomes:</p>
                <br>
$$
\text{Loss}(\mathbf{w}) = ||\mathbf{y} - \boldsymbol{\Phi}\mathbf{w}||^2
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
                <p>The gradient descent update rule:</p>
                <br>
$$
\mathbf{w} \leftarrow \mathbf{w} + \alpha\boldsymbol{\Phi}^T(\mathbf{y} - \boldsymbol{\Phi}\mathbf{w})
$$
<br>
<p>This allows us to model <b>non-linear relationships</b> while maintaining the computational advantages of linear methods.</p>
</div>
        </div>
    </div>
</div>

## Cross Validation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p>Cross validation is a technique for <b>assessing model performance</b> and preventing overfitting by evaluating the model on unseen data.</p>
            </div>
        </div>
    </div>
</div>

## Cross Validation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <br>
                <p><b>K-Fold Cross Validation</b> divides the dataset into K equal parts:</p>
                <br>
<p>For each fold $k = 1, 2, ..., K$:</p>
<ol>
<li>Train on all folds except fold $k$</li>
<li>Evaluate on fold $k$</li>
<li>Record the performance metric</li>
</ol>
<br>
<p>Final performance = average across all K folds</p>
</div>
        </div>
    </div>
</div>

## Cross Validation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <br>
                <p>Mathematically, for K-fold CV:</p>
                <br>
$$
\text{CV}(\mathbf{w}) = \frac{1}{K}\sum_{k=1}^K \text{Loss}_k(\mathbf{w})
$$
<br>
<p>Where $\text{Loss}_k(\mathbf{w})$ is the loss on fold $k$ when training on all other folds.</p>
</div>
        </div>
    </div>
</div>

## Cross Validation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <br>
                <p><b>Leave-One-Out Cross Validation (LOOCV)</b> is a special case where $K = N$:</p>
                <br>
$$
\text{LOOCV}(\mathbf{w}) = \frac{1}{N}\sum_{i=1}^N (y_i - \mathbf{w}_{-i}^T\mathbf{x}_i)^2
$$
<br>
<p>Where $\mathbf{w}_{-i}$ is trained on all data points except $(\mathbf{x}_i, y_i)$.</p>
</div>
        </div>
    </div>
</div>

## Cross Validation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <br>
                <p>Cross validation helps with:</p>
                <br>
<ul>
<li><b>Model selection:</b> Choosing between different model complexities</li>
<li><b>Hyperparameter tuning:</b> Finding optimal learning rates, regularization parameters</li>
<li><b>Performance estimation:</b> Unbiased estimate of generalization error</li>
<li><b>Overfitting detection:</b> Identifying when model complexity is too high</li>
</ul>
</div>
        </div>
    </div>
</div>

## Cross Validation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <br>
                <p>For ridge regression with regularization parameter $\lambda$:</p>
                <br>
$$
\mathbf{w}^* = \underset{\mathbf{w}}{\arg\min} ||\mathbf{y} - \mathbf{X}\mathbf{w}||^2 + \lambda||\mathbf{w}||^2
$$
<br>
<p>Cross validation helps find the optimal $\lambda$ that balances bias and variance.</p>
</div>
        </div>
    </div>
</div> 

<!-- end SLIDES: --> 