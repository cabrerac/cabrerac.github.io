<!-- SLIDES: -->

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Does the prediction count?</b></p>
                <ul>
                    <li>A prediction counts only when every method beats the majority share on the rows kept apart</li>
                    <li>The same rows kept apart for every method</li>
                    <li>Not a contest. A method that does not beat the majority is reported, not hidden</li>
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
                <p><b>What each method sees</b></p>
                <table class="table">
                    <thead>
                        <tr><th>Method</th><th>Sees</th><th>Misses</th></tr>
                    </thead>
                    <tbody>
                        <tr><td>Logistic regression</td><td>One weight per attribute</td><td>Interactions and bends, unless we add them</td></tr>
                        <tr><td>Random forest</td><td>Splits and interactions, mixed columns</td><td>Values beyond those it saw</td></tr>
                        <tr><td>One hidden layer</td><td>Its own attributes and bends</td><td>Clear reasons, and much on few rows</td></tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>How to compare them</b></p>
                <ul>
                    <li>Run every method on the same rows, with the same split</li>
                    <li>Look at the right and wrong counts of each method side by side</li>
                    <li>Read the items where the methods disagree</li>
                    <li>An item that all methods predict yes is a stronger candidate</li>
                    <li>Disagreement is not a winner. Each method sees something the others miss</li>
                </ul>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
