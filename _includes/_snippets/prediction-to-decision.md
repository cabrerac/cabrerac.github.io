{% include _snippets/deployment.md %}
<!-- SLIDES: -->

## Deployment

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Deploying a prediction</b></p>
                <p>A predicted label for each new item feeds something people do.</p>
                <ul>
                    <li><b>Scoring:</b> new items get a label before anyone gives one</li>
                    <li><b>Queue:</b> items ranked by probability, for a person to check</li>
                    <li><b>Decision:</b> one action per item, such as approve, review, or read</li>
                    <li><b>Report:</b> how many items are predicted yes, with the counts</li>
                </ul>
                <p>We deploy it together with the threshold, the attributes, the kept apart counts with their interval, and the majority baseline.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/decision-tree.jpg" alt="Decision tree" style="height: 400px">
                <div class="footnote">Decision Tree - Gilgoldm, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Deployment

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>What a deployed prediction implies</b></p>
                <ul>
                    <li><b>Prediction, not cause:</b> an attribute that predicts the label does not make it happen</li>
                    <li><b>Tied to the label and the attributes:</b> another label, leakage, or another split gives other counts</li>
                    <li><b>Goes stale:</b> new items drift, so we re-check the counts on newly labelled items</li>
                    <li><b>People:</b> who gave the label, and who carries a false yes or a false no</li>
                </ul>
                <br>
                <p>Items unlike the training rows still get a prediction. A deployed model says nothing reliable about them.</p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
