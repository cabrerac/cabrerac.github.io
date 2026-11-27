<!-- SLIDES: -->

## The Task

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Supervised prediction</b> learns a given label from the attributes of items whose label is known, and then predicts it for new items.</p>
                <ul>
                    <li><p>A class as the label is classification</p></li>
                    <li><p>A number as the label is regression</p></li>
                    <li><p>A good label is not something the attributes contain by construction</p></li>
                </ul>
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
            <div class="column vertical-middle text-left" style="width: 50%">
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

<!-- end SLIDES: -->
