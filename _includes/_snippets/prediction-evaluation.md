<!-- SLIDES: -->

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p><b>Evaluation</b> scores the methods that were trained, on marked items they never saw.</p>
                <p>A method that was not trained is not in the score.</p>
            </div>
        </div>
    </div>
</div>

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Confusion matrix</b></p>
                <p>Four counts on marked items the model never saw.</p>
                <table class="table" style="font-size: 0.74em">
                    <thead>
                        <tr><th></th><th>Actual yes</th><th>Actual no</th></tr>
                    </thead>
                    <tbody>
                        <tr><td><b>Predicted yes</b></td><td>TP = 6</td><td>FP = 1</td></tr>
                        <tr><td><b>Predicted no</b></td><td>FN = 2</td><td>TN = 11</td></tr>
                    </tbody>
                </table>
                <br>
                <p>$$\text{accuracy} = \frac{TP + TN}{n}$$</p>
                <br>
                <p>Accuracy is the right answers over all answers.</p>
                <p>On this toy, $n = 20$ and accuracy is 0.85.</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/diagrams/confusion-matrix-counts.svg" alt="The four counts of a confusion matrix" style="height: 380px">
            </div>
        </div>
    </div>
</div>

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>The majority class</b></p>
                <p>Always give the most common label.</p>
                <br>
                <p>$$\text{accuracy} = \frac{n_{\text{majority}}}{n}$$</p>
                <br>
                <p>On the figure, 7 of 10 are no, so saying no to all is right on 0.70.</p>
                <p>A one-attribute rule is a second line.</p>
                <p>It is one cutoff on a single attribute.</p>
                <p>A useful method beats the majority class.</p>
                <p>If the rule wins, the signal is that attribute.</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/eval-majority.svg" alt="Seven items are no and three are yes, so saying no to all is right on seven" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
</div>

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 58%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%; height: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/eval-folds-2.svg" alt="Each split predicted once" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
    <div class="row" style="height: 42%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%; height: 100%">
                <p><b>More than one split</b></p>
                <ul>
                    <li><p>One held-out set can flatter a method</p></li>
                    <li><p>Repeat the same comparison on other splits</p></li>
                    <li><p>If the winner changes, read the result as weak</p></li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>The same items</b></p>
                <p>Yes means the method answers yes for that item.</p>
                <table class="table">
                    <thead>
                        <tr><th>Item</th><th>Logistic regression</th><th>One hidden layer</th></tr>
                    </thead>
                    <tbody>
                        <tr><td>A, B</td><td>yes</td><td>yes</td></tr>
                        <tr><td>C</td><td>yes</td><td>no</td></tr>
                        <tr><td>D</td><td>no</td><td>yes</td></tr>
                    </tbody>
                </table>
                <ul>
                    <li><p><b>Both:</b> A and B are a stronger candidate.</p></li>
                    <li><p><b>One method only:</b> C and D need a reason.</p></li>
                </ul>
                <p>A method that was not trained has no column.</p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
