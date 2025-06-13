<!-- SLIDES: -->

## Regression

## Regression

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p>The regression problem involves <b>predicting a continuous numerical value.</b> Regression models approximate a function <em><b>f</b></em> that maps input features to a continuous output.</p>
            </div>
        </div>
    </div>
</div>

## Regression

<div class="rows" style="height: 100%">
    <div class="row" style="height: 40%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <p>The hypotheses space <em><b>H</b></em> includes linear functions of continuous-valued inputs</p>            
            </div>
        </div>
    </div>
<div class="row" style="height: 60%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
            </div>
        </div>
    </div>
</div>

## Regression Models

<div class="rows" style="height: 100%">
    <div class="row" style="height: 40%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <p>The hypotheses space <em><b>H</b></em> includes linear functions of continuous-valued inputs</p>
                <br>
                <p>The simplest example is "fitting a straight line". The model learns the coefficients <em><b>W</b></em></p>
                <br>
$$
y = w_{1}x + w_{0} \; ; \; W = \langle w_0, w_1 \rangle
$$
</div>
    </div>
        </div>
<div class="row" style="height: 60%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
</div>
        </div>
    </div>
</div>

## Regression Models

<div class="rows" style="height: 100%">
    <div class="row" style="height: 40%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <p>The hypotheses space <em><b>H</b></em> includes linear functions of continuous-valued inputs</p>
                <br>
                <p>The simplest example is "fitting a straight line". The model learns the coefficients <em><b>W</b></em></p>
                <br>
$$
y = w_{1}x + w_{0} \; ; \; W = \langle w_0, w_1 \rangle
$$
</div>
    </div>
        </div>
<div class="row" style="height: 60%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
<img src="{{ site.url }}/assets/media/diagrams/regression-hypothesis-space.svg" alt="Hypothesis Space for Regression" style="max-width: 100%; height: auto;">
<div class="footnote">Example functions described using a linear model.</div>
</div>
        </div>
    </div>
</div>

## Regression Models

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 33%">
                <img src="{{ site.url }}/assets/media/diagrams/regression-hypothesis-space.svg" alt="Hypothesis Space for Regression" style="max-width: 100%; height: auto;">
                <div class="footnote">Example functions described using a linear model.</div>
            </div>
            <div class="column vertical-middle text-left" style="width: 33%">
                <img src="{{ site.url }}/assets/media/diagrams/regression-data.svg" alt="Training Data Set" style="max-width: 100%; height: auto;">
                <div class="footnote">Training dataset.</div>
            </div>
            <div class="column vertical-middle text-left" style="width: 33%">
                <img src="{{ site.url }}/assets/media/diagrams/regression-fit.svg" alt="Regression Fit" style="max-width: 100%; height: auto;">
                <div class="footnote">Linear regression fit.</div>
            </div>
        </div>
    </div>
</div>

## Regression Models

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
<p>The simplest example is "fitting a straight line". The model learns the coefficients <em><b>W</b></em></p>
<br>
$$
y = w_{1}x + w_{0} \; ; \; W = \langle w_0, w_1 \rangle
$$
<br>
<p>Finding the <em><b>h</b></em> that best fits teh data is called linear regression</p>
<br>
$$
h_w = w_{1}x + w_{0}
$$
</div>
        </div>
    </div>
</div>

## Regression Models

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
<p>The simplest example is "fitting a straight line". The model learns the coefficients <em><b>W</b></em></p>
<br>
$$
y = w_{1}x + w_{0} \; ; \; W = \langle w_0, w_1 \rangle
$$
<br>
<p>Finding the <em><b>h</b></em> that best fits teh data is called linear regression</p>
<br>
$$
h_w = w_{1}x + w_{0}
$$
<br>
<p>Finding the values of the weights <em><b>w<sub>0</sub></b></em> and <em><b>w<sub>1</sub></b></em> that minimise the empirical loss <em><b>L<sub>2</sub></b></em> (Squared Error).</p>
$$
\text{Loss}(h_w) = \sum_{i=1}^n (y_i - h_w(x_i))^2
$$
$$
\text{Loss}(h_w) = \sum_{i=1}^n (y_i - (w_1 x_i + w_0))^2
$$
</div>
        </div>
    </div>
</div>

## Regression Models

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
<p>Given the <em><b>Loss(h<sub>w</sub>)</b></em></p>
$$
\text{Loss}(h_w) = \sum_{i=1}^n (y_i - (w_1 x_i + w_0))^2
$$
<br>
<p>We want to find <em><b>w*</b></em></p>
$$
w^* = \underset{w}{\arg\min} \; \sum_{i=1}^n (y_i - h_w(x_i))^2
$$
</div>
        </div>
    </div>
</div>

## Regression Models

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
<p>Given the <em><b>Loss(h<sub>w</sub>)</b></em></p>
$$
\text{Loss}(h_w) = \sum_{i=1}^n (y_i - (w_1 x_i + w_0))^2
$$
<br>
<p>We want to find <em><b>w*</b></em></p>
$$
w^* = \underset{w}{\arg\min} \; \sum_{i=1}^n (y_i - h_w(x_i))^2
$$
<br>
<p>We know that the the loss is minimised when its partial derivatives with respect to <em><b>w<sub>0</sub></b></em> and <em><b>w<sub>1</sub></b></em> are zero.</p>
<br>
$$
\frac{\partial \text{Loss}(h_w)}{\partial w_0} = 0 \; ; \; \frac{\partial \text{Loss}(h_w)}{\partial w_1} = 0
$$
</div>
        </div>
    </div>
</div>

## Regression Models

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
<p>We know that the the loss is minimised when its partial derivatives with respect to <em><b>w<sub>0</sub></b></em> and <em><b>w<sub>1</sub></b></em> are zero.</p>
<br>
$$
\frac{\partial \text{Loss}(h_w)}{\partial w_0} = 0 \; ; \; \frac{\partial \text{Loss}(h_w)}{\partial w_1} = 0
$$
<br>
$$
\frac{\partial}{\partial w_0} \left[ \sum_{i=1}^n (y_i - (w_1 x_i + w_0))^2 \right] = 0 \; ; \; \frac{\partial}{\partial w_1} \left[ \sum_{i=1}^n (y_i - (w_1 x_i + w_0))^2 \right] = 0
$$
<br>
</div>
        </div>
    </div>
</div>

## Regression Models

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
<p>We know that the the loss is minimised when its partial derivatives with respect to <em><b>w<sub>0</sub></b></em> and <em><b>w<sub>1</sub></b></em> are zero.</p>
<br>
$$
\frac{\partial \text{Loss}(h_w)}{\partial w_0} = 0 \; ; \; \frac{\partial \text{Loss}(h_w)}{\partial w_1} = 0
$$
<br>
$$
\frac{\partial}{\partial w_0} \left[ \sum_{i=1}^n (y_i - (w_1 x_i + w_0))^2 \right] = 0 \; ; \; \frac{\partial}{\partial w_1} \left[ \sum_{i=1}^n (y_i - (w_1 x_i + w_0))^2 \right] = 0
$$
<br>
<p>Solving the partial derivatives</p>
<br>
$$
w_0 = \frac{1}{n}(\sum_{i=1}^n y_i - w_1 \sum_{i=1}^n x_i) \; ; \;
w_1 = \frac{n\sum_{i=1}^n x_i y_i - \sum_{i=1}^n x_i \sum_{i=1}^n y_i}{n\sum_{i=1}^n x_i^2 - \left(\sum_{i=1}^n x_i\right)^2} 
$$
</div>
        </div>
    </div>
</div>

## Regression Models

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 33%">
                <img src="{{ site.url }}/assets/media/images/convex-function.jpeg" alt="Convex Function" style="max-width: 90%; height: auto;">
                <div class="footnote">Weights Space - Convex Loss Function.</div>
            </div>
        </div>
    </div>
</div>

## Regression Models

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 33%">
                <img src="{{ site.url }}/assets/media/images/convex-function.jpeg" alt="Convex Function" style="max-width: 90%; height: auto;">
                <div class="footnote">Weights Space - Convex Loss Function.</div>
            </div>
            <div class="column vertical-middle text-left" style="width: 33%">
                <img src="https://upload.wikimedia.org/wikipedia/commons/e/e3/Non-Convex_Objective_Function.gif" alt="Non Convex Function" style="max-width: 100%; height: auto;">
                <div class="footnote">Non Convex Function - Zachary kaplan, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons.</div>
            </div>
        </div>
    </div>
</div>

## Regression Models

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 33%">
                <img src="{{ site.url }}/assets/media/images/convex-function.jpeg" alt="Convex Function" style="max-width: 90%; height: auto;">
                <div class="footnote">Weights Space - Convex Loss Function.</div>
            </div>
            <div class="column vertical-middle text-left" style="width: 33%">
                <img src="https://upload.wikimedia.org/wikipedia/commons/e/e3/Non-Convex_Objective_Function.gif" alt="Non Convex Function" style="max-width: 100%; height: auto;">
                <div class="footnote">Non Convex Function - Zachary kaplan, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons.</div>
            </div>
            <div class="column vertical-middle text-left" style="width: 33%">
                <img src="https://upload.wikimedia.org/wikipedia/commons/a/a3/Gradient_descent.gif" alt="Gradient Descent Algorithm" style="max-width: 100%; height: auto;">
                <div class="footnote">Gradient Descent Algorithm - Jacopo Bertolotti, CC0, via Wikimedia Commons.</div>
            </div>
        </div>
    </div>
</div>

## Regression Models

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 40%">
                <img src="https://upload.wikimedia.org/wikipedia/commons/a/a3/Gradient_descent.gif" alt="Gradient Descent Algorithm" style="max-width: 100%; height: auto;">
                <div class="footnote">Gradient Descent Algorithm - Jacopo Bertolotti, CC0, via Wikimedia Commons.</div>
            </div>
            <div class="column vertical-top text-left" style="width: 60%">
                <p>We choose any starting point and then compute <b>an estimate of the gradient and move a small amount in the steepest downhill direction</b>, repeating until we converge on a point in the weight space with <em>(local)</em> minima loss.</p>
<br>
<pre><code>Gradient Descent Algorithm:
Initialize w randomly
repeat
    for each w[i] in w
        Compute gradient: g = ∇Loss(w[i])
        Update weight:   w[i] = w[i] - α * g
until convergence
</code></pre>
<br>
<p>The size of the step is given by the parameter α, which regulates the behaviour of the gradient descent algorithm. This is a hyperparameter of the regression model we are training, usually called <em>learning rate.</em></p>
            </div>
        </div>
    </div>
</div>

## Regression Models

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
<p>Following with our "straight line" example, the update rule for <em><b>w<sub>0</sub></b></em> and <em><b>w<sub>1</sub></b></em> is</p>
<br>
$$
w_i \leftarrow w_i - \alpha \frac{\partial \text{Loss}(w)}{\partial w_i}
$$
</div>
        </div>
    </div>
</div>

## Regression Models

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
<p>Following with our "straight line" example, the update rule for <em><b>w<sub>0</sub></b></em> and <em><b>w<sub>1</sub></b></em> is</p>
<br>
$$
w_i \leftarrow w_i - \alpha \frac{\partial \text{Loss}(w)}{\partial w_i}
$$
<p>The loss function is a composition of functions</p>
<br>
$$
Loss(w) = (y - h_w(x))^2
$$
</div>
        </div>
    </div>
</div>

## Regression Models

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
<p>Following with our "straight line" example, the update rule for <em><b>w<sub>0</sub></b></em> and <em><b>w<sub>1</sub></b></em> is</p>
<br>
$$
w_i \leftarrow w_i - \alpha \frac{\partial \text{Loss}(w)}{\partial w_i}
$$
<p>The loss function is a composition of functions</p>
<br>
$$
Loss(w) = (y - h_w(x))^2
$$
<p>We need to differentiate the loss function step by step using the <b>chain rule</b> to compute the gradients</p>
<br>
$$
\frac{\partial \text{g}(f(x))}{\partial x} = \text{g'}(f(x)) \frac{\partial f(x)}{\partial x}
$$
</div>
        </div>
    </div>
</div>

## Regression Models

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
<p>Applying the chain rule to the loss function</p>
$$
\frac{\partial \text{Loss}(w)}{\partial w_i} = \frac{\partial \text{Loss}((y - h_w(x))^2)}{\partial w_i}
$$
<br>
$$
\frac{\partial \text{Loss}((y - h_w(x))^2)}{\partial w_i} = 2(y-h_w(x)) \frac{\partial (y-h_w(x))}{\partial w_i}
$$
<br>
$$
2(y-h_w(x)) \frac{\partial (y-h_w(x))}{\partial w_i} = 2(y-h_w(x)) \frac{\partial (y-(w_1x+w_0))}{\partial w_i}
$$
</div>
        </div>
    </div>
</div>

## Regression Models

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
<p>Applying the chain rule to the loss function</p>
$$
\frac{\partial \text{Loss}(w)}{\partial w_i} = \frac{\partial \text{Loss}((y - h_w(x))^2)}{\partial w_i}
$$
<br>
$$
\frac{\partial \text{Loss}((y - h_w(x))^2)}{\partial w_i} = 2(y-h_w(x)) \frac{\partial (y-h_w(x))}{\partial w_i}
$$
<br>
$$
2(y-h_w(x)) \frac{\partial (y-h_w(x))}{\partial w_i} = 2(y-h_w(x)) \frac{\partial (y-(w_1x+w_0))}{\partial w_i}
$$
<p>Applying this to <em><b>w<sub>0</sub></b></em> and <em><b>w<sub>1</sub></b></em></p>
<br>
$$
\frac{\partial \text{Loss}(w)}{\partial w_0} = -2(y-h_w(x)) \; ; \; \frac{\partial \text{Loss}(w)}{\partial w_1} = -2(y-h_w(x))x
$$
</div>
        </div>
    </div>
</div>

## Regression Models

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
<p>The update rule for each weight in the straight line example is (folding 2 into α)</p>
<br>
$$
w_0 \leftarrow w_ 0 + \alpha (y-h_w(x)) \; ; \; w_1 \leftarrow w_ 1 + \alpha (y-h_w(x))x
$$
<p>For <b><em>N</b></em> training examples</p>
$$
w_0 \leftarrow w_0 + \alpha \sum_{i=1}^N (y_i - h_w(x_i))
\; ; \;
w_1 \leftarrow w_1 + \alpha \sum_{i=1}^N (y_i - h_w(x_i)) x_i
$$
<p>These updates constitute <b>the batch gradient descent</b>. For the straight line, this gradient descent is <em>deterministic</em></p>
<br>
<p>An <b>epoch</b> is defined as one complete pass through the entire dataset during the training process. Multiple epochs are needed for the model to converge to an optimal solution. Not enough epochs could generate underfitting. Too many epochs could generate overfitting. Another hyperparameter for the model.</p>
</div>
        </div>
    </div>
</div>

## Regression

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 40%">
                <p><b>Batch Gradient Descent</b></p>            
                <p>The algorithm updates <b><em>W</em></b> using the entire dataset in each iteration.</p>
            </div>
            <div class="column vertical-top text-left" style="width: 60%">

```python
import numpy as np
def batch_gradient_descent(X, y, alpha=0.01, epochs=1000):
    """
    X: numpy array of shape (n_samples, n_features)
    y: numpy array of shape (n_samples,)
    alpha: learning rate
    epochs: number of passes over the data
    Returns: w (numpy array of shape (n_features,))
    """
    n_samples, n_features = X.shape
    w = np.zeros(n_features)
    for epoch in range(epochs):
        grad = [0] * len(w)
        for i in range(n_samples):
            x_i = X[i]
            y_i = y[i]
            prediction = dot(w, x_i)
            error = prediction - y_i
            for j in range(len(w)):
                grad[j] += error * x_i[j]
        for j in range(len(w)):
            grad[j] /= len(n_samples)
            w[j] -= alpha * grad[j]
    return w
```
</div>
        </div>
    </div>
</div>

## Regression

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 40%">
                <p><b>Stochastic Gradient Descent</b></p>
                <p>The algorithm updates <b><em>W</em></b> after computing the gradient for each training example.</p>
            </div>
            <div class="column vertical-top text-left" style="width: 60%">

```python
import numpy as np
def stochastic_gradient_descent(X, y, alpha=0.01, epochs=1000):
    """
    X: numpy array of shape (n_samples, n_features)
    y: numpy array of shape (n_samples,)
    alpha: learning rate
    epochs: number of passes over the data
    Returns: w (numpy array of shape (n_features,))
    """
    n_samples, n_features = X.shape
    w = np.zeros(n_features)
    for epoch in range(epochs):
        for i in range(n_samples):
            x_i = X[i]
            y_i = y[i]
            prediction = np.dot(w, x_i)
            error = prediction - y_i
            for j in range(n_features):
                w[j] -= alpha * error * x_i[j]
    return w
```
</div>
        </div>
    </div>
</div>

## Regression

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 40%">
                <p><b>Mini-batch Gradient Descent</b></p>
                <p>The algorithm updates <b><em>W</em></b> after computing the gradient for a small batch of training examples (batch size <em>m</em>).</p>
            </div>
            <div class="column vertical-top text-left" style="width: 60%">

```python
import numpy as np
def mini_batch_gradient_descent(X, y, alpha=0.01, epochs=1000, batch_size=32):
    """
    X: numpy array of shape (n_samples, n_features)
    y: numpy array of shape (n_samples,)
    alpha: learning rate
    epochs: number of passes over the data
    batch_size: number of samples per batch
    Returns: w (numpy array of shape (n_features,))
    """
    n_samples, n_features = X.shape
    w = np.zeros(n_features)
    for epoch in range(epochs):
        indices = np.arange(n_samples)
        np.random.shuffle(indices)
        X_shuffled = X[indices]
        y_shuffled = y[indices]
        for start in range(0, n_samples, batch_size):
            end = start + batch_size
            X_batch = X_shuffled[start:end]
            y_batch = y_shuffled[start:end]
            y_pred = X_batch @ w
            error = y_pred - y_batch
            grad = X_batch.T @ error / len(X_batch)
            w -= alpha * grad
    return w
```
</div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->