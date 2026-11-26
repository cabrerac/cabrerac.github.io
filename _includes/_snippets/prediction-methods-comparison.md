<!-- SLIDES: -->

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Does the prediction count?</b></p>
                <ul>
                    <li><p>It counts only when every method beats the majority class by more than 0.02 on the rows kept apart</p></li>
                    <li><p>The same rows kept apart for every method</p></li>
                    <li><p>Not a contest. A method that does not beat the majority class is reported, not hidden</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/eval-counts.svg" alt="Accuracy of three methods against the majority class" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
</div>

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>What each method sees</b> (majority class on the 56 kept-apart rows: 0.518)</p>
                <table class="table">
                    <thead>
                        <tr><th>Method</th><th>What it sees</th><th>What it misses</th><th>L6 test accuracy</th></tr>
                    </thead>
                    <tbody>
                        <tr><td>Logistic regression</td><td>One weight per attribute</td><td>Interactions and bends</td><td>0.607</td></tr>
                        <tr><td>Random forest</td><td>Splits and interactions</td><td>Values beyond those it saw</td><td>0.714</td></tr>
                        <tr><td>One hidden layer</td><td>Its own attributes and bends</td><td>Clear reasons, needs many rows</td><td>0.625</td></tr>
                    </tbody>
                </table>
                <p><b>How to compare them:</b> run every method on the same split, read the disagreements, and treat items predicted yes by all methods as stronger candidates.</p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
