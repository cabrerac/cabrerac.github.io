<!-- SLIDES: -->

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p>A <b>confusion matrix</b> counts the right and wrong answers of a prediction on marked items that the model never saw.</p>
            </div>
        </div>
    </div>
</div>

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>Four counts on the items kept apart. We report all four.</p>
                <ul>
                    <li><p><b>TP:</b> said yes, and it was yes</p></li>
                    <li><p><b>FP:</b> said yes, and it was no</p></li>
                    <li><p><b>FN:</b> said no, and it was yes</p></li>
                    <li><p><b>TN:</b> said no, and it was no</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/eval-confusion-2.svg" alt="The four cells of a confusion matrix" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
</div>

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Precision, recall, F1</b></p>
                <br>
$$
\text{precision} = \frac{TP}{TP + FP}, \qquad \text{recall} = \frac{TP}{TP + FN}
$$
$$
F_1 = \frac{2 \cdot \text{precision} \cdot \text{recall}}{\text{precision} + \text{recall}}
$$
                <table class="table" style="font-size: 0.74em">
                    <thead>
                        <tr><th></th><th>Actual yes</th><th>Actual no</th></tr>
                    </thead>
                    <tbody>
                        <tr><td><b>Predicted yes</b></td><td>TP = 8</td><td>FP = 2</td></tr>
                        <tr><td><b>Predicted no</b></td><td>FN = 4</td><td>TN = 26</td></tr>
                    </tbody>
                </table>
                <p>Toy set: precision 0.80, recall 0.67, and F1 0.73.</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/precision-recall.svg" alt="Precision and recall" style="height: auto; max-width: 100%; max-height: 90%;">
                <div class="footnote">Precisionrecall - Walber, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
