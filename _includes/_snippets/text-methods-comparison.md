<!-- SLIDES: -->

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
                        <tr><td>Keyword list</td><td>Texts with the listed words</td><td>Other words for the same answer</td></tr>
                        <tr><td>TF-IDF with logistic regression</td><td>Words that separate the marks</td><td>Word order, and words unseen in training</td></tr>
                        <tr><td>Text encoder</td><td>Meaning across words and languages</td><td>Text past the token limit, and why it decided</td></tr>
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
                    <li>Run every method on the same kept apart texts</li>
                    <li>Look at the right and wrong counts of each method side by side</li>
                    <li>Read the texts where the methods disagree</li>
                    <li>A text that all methods mark yes is a stronger candidate</li>
                    <li>Disagreement is not a winner. Each method sees something the others miss</li>
                </ul>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
