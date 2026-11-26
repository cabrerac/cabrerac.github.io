{% include _snippets/deployment.md %}

<!-- SLIDES: -->

## Deployment

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>A predicted label for each new item feeds something people do.</p>
                <ul>
                    <li><p><b>Scoring:</b> new items get a label before anyone gives one</p></li>
                    <li><p><b>Queue:</b> items ranked by probability, for a person to check</p></li>
                    <li><p><b>Decision:</b> one action per item, such as approve, review, or read</p></li>
                    <li><p><b>Report:</b> how many items are predicted yes</p></li>
                </ul>
                <p>We deploy it with the threshold, the attributes, the counts and the majority class.</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/decision-tree-1.svg" alt="A generic decision tree" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
</div>

## Deployment

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>What a deployed prediction implies</b></p>
                <ul>
                    <li><p><b>Prediction, not cause:</b> an attribute that predicts the label does not make it happen</p></li>
                    <li><p><b>Tied to the label and the attributes:</b> another label, leakage, or another split gives other counts</p></li>
                    <li><p><b>Goes stale:</b> new items drift, so we check the counts again on newly labelled items</p></li>
                    <li><p><b>People:</b> who gave the label, and who carries a false yes or a false no</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/eval-confusion-2.svg" alt="The four cells of a confusion matrix" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
