<!-- SLIDES: -->

## The Task

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>Can the attributes of an item predict a label that someone gave?</p>
                <ul>
                    <li><p>Each record is an item with attributes and a label, given by a rule or by people</p></li>
                    <li><p>A model learns the label from items whose label is known</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/decision-tree-1.svg" alt="A generic decision tree" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
</div>

## The Task

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <p><b>Supervised prediction</b> learns a given label from the attributes of items whose label is known, and then predicts it for new items.</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/prediction-label-1.svg" alt="Labelled rows train a model" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
</div>

## The Task

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <p><b>Supervised prediction</b> learns a given label from the attributes of items whose label is known, and then predicts it for new items.</p>
                <ul>
                    <li><p>A class as the label is classification</p></li>
                    <li><p>A number as the label is regression</p></li>
                    <li><p>A good label is not something the attributes contain by construction</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/prediction-label-2.svg" alt="A new row gets a predicted label" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
</div>

# The Data

## The Data

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>One row per item, the same attributes for every item, and a label.</p>
                <ul>
                    <li><p><b>Item:</b> one row, such as a loan, a patient, or an article</p></li>
                    <li><p><b>Attribute:</b> a number or a category, possibly missing</p></li>
                    <li><p><b>Label:</b> the answer given for each item</p></li>
                </ul>
                <p>Only items with a label train or judge a model.</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/prediction-table.svg" alt="A table of items, attributes and a label" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
</div>

## The Data

<div class="rows" style="height: 100%">
    <div class="row" style="height: 54%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%; height: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/prediction-leakage-1.svg" alt="An attribute recorded after the label" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
    <div class="row" style="height: 46%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%; height: 100%">
                <p><b>Target leakage</b> (<a href="https://doi.org/10.1145/2382577.2382579" target="_blank" rel="noopener noreferrer">Kaufman et al., 2012</a>): an attribute filled in after the label is known, or computed from it.</p>
                <ul>
                    <li><p>Predicting whether a loan is repaid, with a column for late fees</p></li>
                    <li><p>Late fees exist only because the loan was not repaid on time</p></li>
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
                <p><b>How to check for leakage</b></p>
                <ul>
                    <li><p>For each attribute, ask how and when it was made</p></li>
                    <li><p>Train the same model with and without the suspect attribute</p></li>
                    <li><p>A large drop without it means it was carrying the label</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/prediction-leakage-2.svg" alt="The same model with and without the suspect attribute" style="height: auto; max-width: 100%; max-height: 100%;">
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
                    <li><p>Split the labelled items before anything is learned</p></li>
                    <li><p><b>fit</b> on the training rows only</p></li>
                    <li><p><b>predict</b> on the rows kept apart</p></li>
                </ul>
                <p>A model can remember its training rows. Only rows it has never seen show how it will do on new items.</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/eval-split.svg" alt="Fit on the training rows, predict the rows kept apart" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
</div>

# Modeling

## Methods

<div class="rows" style="height: 100%">
    <div class="row" style="height: 65%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%; height: 100%">
                <img class="external-svg" src="{{ site.url }}/assets/media/diagrams/prediction-task-taxonomy.svg" alt="Taxonomy of prediction methods" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
    <div class="row" style="height: 35%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%; height: 100%">
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
                    <li><p><b>Logistic regression:</b> one weight per attribute, from Lecture 4</p></li>
                    <li><p><b>Random forest:</b> many trees that vote</p></li>
                    <li><p><b>One hidden layer:</b> a network that learns its own attributes</p></li>
                </ul>
                <p>These apply to different data sources (e.g., loans, patients, articles, etc).</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/decision-tree-1.svg" alt="A generic decision tree" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
