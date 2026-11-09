<!-- SLIDES: -->

## Last Time

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <ul>
                    <li><b>The task:</b> where each item sits among the others</li>
                    <li><b>The data:</b> items and the links among them, inside one set</li>
                    <li><b>The methods:</b> degree, PageRank, and node2vec</li>
                    <li><b>Evaluation and deployment:</b> an outside measure, seeds, random pairs, and what using a place would mean</li>
                </ul>
                <p>Every result so far came from the data itself. This lecture is the prediction task, with a given label.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/crisp-dm-process-diagram.png" alt="CRISP-DM process diagram" style="height: 400px">
                <div class="footnote">CRISP-DM Process Diagram - Kenneth Jensen, CC BY-SA 3.0 <https://creativecommons.org/licenses/by-sa/3.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## This Lecture in CRISP-DM

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <ul>
                    <li><b>The task:</b> can the attributes of an item predict a label that someone gave?</li>
                    <li><b>The data:</b> a table of attributes with a given label, such as loans, patients, and articles</li>
                    <li><b>Modeling:</b> logistic regression, a random forest, and one hidden layer</li>
                    <li><b>Evaluation:</b> right and wrong counts on items kept apart, against the majority</li>
                    <li><b>Deployment:</b> what using a prediction would mean, and its limits</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/crisp-dm-process-diagram.png" alt="CRISP-DM process diagram" style="height: 400px">
                <div class="footnote">CRISP-DM Process Diagram - Kenneth Jensen, CC BY-SA 3.0 <https://creativecommons.org/licenses/by-sa/3.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
