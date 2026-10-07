<!-- SLIDES: -->

## Activations

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p>The activation shapes the <b>decision surface</b> and how training behaves.</p>
            </div>
        </div>
    </div>
</div>

## Activations

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <table>
                    <thead>
                        <tr><th>Activation</th><th>Typical use</th><th>Watch-outs</th></tr>
                    </thead>
                    <tbody>
                        <tr><td>Linear</td><td>Regression heads</td><td>No non-linearity</td></tr>
                        <tr><td>Sigmoid</td><td>Binary probabilities</td><td>Saturation</td></tr>
                        <tr><td>Tanh</td><td>Zero-centred classic</td><td>Still saturates</td></tr>
                        <tr><td>ReLU</td><td>Hidden layers</td><td>Dying ReLU. Not a probability</td></tr>
                    </tbody>
                </table>
                <br>
                <p>Match the activation to the <b>decision</b> and to training stability. Not to fashion.</p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
