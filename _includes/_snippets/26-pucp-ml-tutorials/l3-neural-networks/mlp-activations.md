<!-- SLIDES: -->

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
</div>
        </div>
    </div>
</div>

## Feedforward Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p><b>Activation functions</b> introduce non-linearity into the network, enabling it to learn complex patterns and relationships.</p>
            </div>
        </div>
    </div>
</div>

## Feedforward Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 33%">
                <p><b>Sigmoid Function:</b></p>
$$
\sigma(z) = \frac{1}{1 + e^{-z}}
$$
<br>Range: $(0, 1)$
<br>Derivative: $\sigma'(z) = \sigma(z)(1 - \sigma(z))$
<br>
<img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/8/88/Logistic-curve.svg" alt="Logistic Curve" style="max-width: 65%; height: auto;">
<div class="footnote">Logistic Curve - Qef, Public domain, via Wikimedia Commons.</div>
            </div>
            <div class="column vertical-top text-left" style="width: 33%">
            </div>
            <div class="column vertical-top text-left" style="width: 33%">
            </div>
        </div>
    </div>
</div>

## Feedforward Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 33%">
                <p><b>Sigmoid Function:</b></p>
$$
\sigma(z) = \frac{1}{1 + e^{-z}}
$$
<br>Range: $(0, 1)$
<br>Derivative: $\sigma'(z) = \sigma(z)(1 - \sigma(z))$
<br>
<img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/8/88/Logistic-curve.svg" alt="Logistic Curve" style="max-width: 65%; height: auto;">
<div class="footnote">Logistic Curve - Qef, Public domain, via Wikimedia Commons.</div>
            </div>
            <div class="column vertical-top text-left" style="width: 33%">
                <p><b>Hyperbolic Tangent:</b></p>
$$
\tanh(z) = \frac{e^z - e^{-z}}{e^z + e^{-z}}
$$
<br>Range: $(-1, 1)$
<br>Derivative: $\tanh'(z) = 1 - \tanh^2(z)$
<br>
<img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/8/87/Hyperbolic_Tangent.svg" alt="Hyperbolic Tangent" style="max-width: 75%; height: auto;">
<div class="footnote">Hyperbolic Tangent - Geek3, CC BY-SA 3.0 <https://creativecommons.org/licenses/by-sa/3.0>, via Wikimedia Commons.</div>
            </div>
            <div class="column vertical-top text-left" style="width: 33%">
            </div>
        </div>
    </div>
</div>

## Feedforward Neural Networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 33%">
                <p><b>Sigmoid Function:</b></p>
$$
\sigma(z) = \frac{1}{1 + e^{-z}}
$$
<br>Range: $(0, 1)$
<br>Derivative: $\sigma'(z) = \sigma(z)(1 - \sigma(z))$
<br>
<img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/8/88/Logistic-curve.svg" alt="Logistic Curve" style="max-width: 65%; height: auto;">
<div class="footnote">Logistic Curve - Qef, Public domain, via Wikimedia Commons.</div>
            </div>
            <div class="column vertical-top text-left" style="width: 33%">
                <p><b>Hyperbolic Tangent:</b></p>
$$
\tanh(z) = \frac{e^z - e^{-z}}{e^z + e^{-z}}
$$
<br>Range: $(-1, 1)$
<br>Derivative: $\tanh'(z) = 1 - \tanh^2(z)$
<br>
<img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/8/87/Hyperbolic_Tangent.svg" alt="Hyperbolic Tangent" style="max-width: 75%; height: auto;">
<div class="footnote">Hyperbolic Tangent - Geek3, CC BY-SA 3.0 <https://creativecommons.org/licenses/by-sa/3.0>, via Wikimedia Commons.</div>
            </div>
            <div class="column vertical-top text-left" style="width: 33%">
                <p><b>ReLU (Rectified Linear Unit):</b></p>
$$
\text{ReLU}(z) = \max(0, z)
$$
<br>Range: $[0, \infty)$
<br>Derivative: $\text{ReLU}'(z) = \begin{cases} 1 & \text{if } z > 0 \\ 0 & \text{if } z \leq 0 \end{cases}$
<br>
<img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/c/c9/Ramp_function.svg" alt="Ramp Function" style="max-width: 75%; height: auto;">
<div class="footnote">Ramp Function - Qef, Public domain, via Wikimedia Commons.</div>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
