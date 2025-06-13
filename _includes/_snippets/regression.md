<!-- SLIDES: -->

## Regression

## Regression

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p>The regression problem involves <b>predicting a continuous numerical value.</b> Regression models approximmate a function <em><b>f</b></em> that maps input features to a continuous output.</p>
            </div>
        </div>
    </div>
</div>

## Regression

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
<p>The hypotheses space <em><b>H</b></em> includes linear functions of continuous-valued inputs</p>
</div>
    </div>
</div>

## Regression

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
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

## Regression

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
<p>The hypotheses space <em><b>H</b></em> includes linear functions of continuous-valued inputs</p>
<br>
<p>The simplest example is "fitting a straight line". The model learns the coefficients <em><b>W</b></em></p>
<br>
$$
y = w_{1}x + w_{0} \; ; \; W = \langle w_0, w_1 \rangle
$$
<img src="{{ site.url }}/assets/media/diagrams/regression-hypothesis-space.svg" alt="Hypothesis Space for Regression" style="max-width: 100%; height: auto;">
<div class="footnote">Example functions described using a linear model.</div>
</div>
    </div>
</div>

## Regression

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

## Regression

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

## Regression

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

## Regression

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

## Regression

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
<p>We know that the the loss is minimised when its partial derivatives with resect to <em><b>w<sub>0</sub></b></em> and <em><b>w<sub>1</sub></b></em> are zero.</p>
<br>
$$
\frac{\partial \text{Loss}(h_w)}{\partial w_0} = 0 \; ; \; \frac{\partial \text{Loss}(h_w)}{\partial w_1} = 0
$$
</div>
    </div>
</div>

## Regression

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
<p>We know that the the loss is minimised when its partial derivatives with resect to <em><b>w<sub>0</sub></b></em> and <em><b>w<sub>1</sub></b></em> are zero.</p>
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

## Regression

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
<p>We know that the the loss is minimised when its partial derivatives with resect to <em><b>w<sub>0</sub></b></em> and <em><b>w<sub>1</sub></b></em> are zero.</p>
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

## Regression

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 33%">
                <img src="{{ site.url }}/assets/media/diagrams/convex-function.jpeg" alt="Convex Function" style="max-width: 100%; height: auto;">
                <div class="footnote">Weights Space - Convex Loss Function.</div>
            </div>
            <div class="column vertical-middle text-left" style="width: 33%">
                <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/e/e3/Non-Convex_Objective_Function.gif" alt="Non Convex Function" style="max-width: 100%; height: auto;">
                <div class="footnote">Non Convex Function - Zachary kaplan, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons.</div>
            </div>
            <div class="column vertical-middle text-left" style="width: 33%">
                <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/a/a3/Gradient_descent.gif" alt="Gradient Descent Algorithm" style="max-width: 100%; height: auto;">
                <div class="footnote">Gradient Descent Algorithm - Jacopo Bertolotti, CC0, via Wikimedia Commons.</div>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
