<!-- SLIDES: -->

## Last Time

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <ul>
                    <li><b>Keyword lists:</b> words taken from the question</li>
                    <li><b>TF-IDF:</b> word weights with logistic regression</li>
                    <li><b>Text encoders:</b> a frozen pretrained model with logistic regression</li>
                    <li><b>Right and wrong counts:</b> marked papers against the majority class</li>
                </ul>
                <p>Each paper now has three results. This lecture reads the links among papers.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/precision-recall.svg" alt="Precision and recall" style="height: 400px">
                <div class="footnote">Precisionrecall - Walber, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons</div>
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
                    <li><b>Data preparation:</b> an edge list inside the set, a directed and an undirected graph, walks on the largest component</li>
                    <li><b>Modeling:</b> degree and PageRank, betweenness, node2vec</li>
                    <li><b>Evaluation:</b> no labels: against citations, across seeds, against random pairs</li>
                    <li><b>Deployment:</b> the graph result as a fourth result for the list</li>
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
