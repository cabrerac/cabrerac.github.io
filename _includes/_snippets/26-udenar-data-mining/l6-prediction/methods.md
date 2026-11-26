<!-- SLIDES: -->

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
                    <li><p><b>Random forest:</b> many trees that vote, a short refresher</p></li>
                    <li><p><b>Logistic regression:</b> one weight per attribute, as in Lecture 4</p></li>
                    <li><p><b>One hidden layer:</b> a network that learns its own attributes, with a logistic regression on top</p></li>
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
