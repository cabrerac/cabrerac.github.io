<!-- SLIDES: -->

## The Task

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>A label given, not found</b></p>
                <p>Can the attributes of an item predict a label that someone gave?</p>
                <ul>
                    <li>Each record is an item with attributes and a label, given by a rule or by people</li>
                    <li>A model learns the label from the items whose label is known, then predicts it for new items</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/decision-tree.jpg" alt="Decision tree" style="height: 400px">
                <div class="footnote">Decision Tree - Gilgoldm, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## The Task

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Classes and numbers</b></p>
                <p>Here the label is a class, so this is classification.</p>
                <ul>
                    <li>Regression is the same weighted sum, with a number as the label</li>
                    <li>A good label is not something the attributes contain by construction</li>
                    <li>A prediction is judged on items kept apart, against a majority baseline</li>
                </ul>
                <br>
                <p><b>Supervised prediction</b> learns a given label from the attributes of items whose label is known, and then predicts it for new items.</p>
            </div>
        </div>
    </div>
</div>

# The Data

## The Data

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 55%">
                <p><b>A table with a given label</b></p>
                <p>The data is one row per item, the same attributes for every item, and a label.</p>
                <ul>
                    <li><b>Item:</b> one row, such as a loan, a patient, or an article</li>
                    <li><b>Attribute:</b> a number or a category, possibly missing</li>
                    <li><b>Label:</b> the answer given for each item, by a rule or by people</li>
                </ul>
                <p>Only items with a label train or judge a model.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 45%">
                <p><b>Examples</b></p>
                <table class="table">
                    <thead>
                        <tr><th>Data</th><th>One item</th><th>Label</th></tr>
                    </thead>
                    <tbody>
                        <tr><td>Loans</td><td>one loan</td><td>repaid or not</td></tr>
                        <tr><td>Patients</td><td>one visit</td><td>diagnosis</td></tr>
                        <tr><td>Articles</td><td>one article</td><td>category</td></tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>

## The Data

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Target leakage <a href="https://doi.org/10.1145/2382577.2382579" target="_blank" rel="noopener noreferrer">(Kaufman et al., 2012)</a></b></p>
                <p>An attribute filled in after the label is known, or computed from it.</p>
                <ul>
                    <li>Example: predicting whether a loan is repaid, with a column for late fees</li>
                    <li>Late fees exist only because the loan was not repaid on time</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>How to check</b></p>
                <ul>
                    <li>For each attribute, ask how and when it was made</li>
                    <li>Train the same model with and without the suspect attribute</li>
                    <li>A large drop without it means it was carrying the label</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## The Data

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Train and test</b></p>
                <ul>
                    <li>Split the labelled items before anything is learned</li>
                    <li><b>fit</b> on the training rows only</li>
                    <li><b>predict</b> on the rows kept apart</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Why kept apart</b></p>
                <p>A model can remember its training rows. Only rows it has never seen show how it will do on new items.</p>
            </div>
        </div>
    </div>
</div>

# Modeling

## Methods

<div class="rows" style="height: 100%">
    <div class="row" style="height: 70%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img class="external-svg" src="{{ site.url }}/assets/media/diagrams/prediction-task-taxonomy.svg" alt="Taxonomy of prediction methods" style="width: 100%; height: 100%">
            </div>
        </div>
    </div>
    <div class="row" style="height: 30%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Linear models:</b> a weighted sum of the attributes, turned into a class or a number.</p>
                <p><b>Trees:</b> questions about one attribute at a time, alone or as many trees that vote.</p>
                <p><b>Neural networks:</b> layers that learn their own attributes from the inputs.</p>
                <p><b>Other methods:</b> the label of the nearest items, or a boundary with the widest margin.</p>
            </div>
        </div>
    </div>
</div>

## Methods

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <ul>
                    <li><b>Logistic regression:</b> one weight per attribute, from Lecture 4</li>
                    <li><b>Random forest:</b> many trees that vote</li>
                    <li><b>One hidden layer:</b> a network that learns its own attributes</li>
                </ul>
                <p>These apply to different data sources (e.g., loans, patients, articles, etc).</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/decision-tree.jpg" alt="Decision tree" style="height: 400px">
                <div class="footnote">Decision Tree - Gilgoldm, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
