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
<p>The simplest example is "fitting a straight line"</p>
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
                <img src="{{ site.url }}/assets/media/diagrams/regression-data.svg" alt="Hypothesis Space with Data" style="max-width: 100%; height: auto;">
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
$$
y = w_{1}x + w_{0} \; ; \; W = \langle w_0, w_1 \rangle
$$
<p>Finding the <em><b>h</b></em> that best fits teh data is called linear regression</p>
$$
h_w = w_{1}x + w_{0}
$$
<p>Finding the values of the weights <em><b>w<sub>0</sub></b></em> and <em><b>w<sub>1</sub></b></em> that minimise the empirical loss.</p>
</div>
    </div>
</div>

<!-- end SLIDES: -->
