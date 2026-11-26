<!-- SLIDES: -->

## Last Time

<div class="rows" style="height: 100%">
    <div class="row" style="height: 50%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 33%; height: 100%">
                <img src="{{ site.url }}/assets/media/images/social-network-analysis.jpg" alt="A network of links among people" style="height: auto; max-width: 100%; max-height: 42%;">
                <p><b>Business understanding</b></p>
                <p>An item's place among the others</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 33%; height: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/graph-words-1.svg" alt="Nodes and directed edges" style="height: auto; max-width: 100%; max-height: 42%;">
                <p><b>Data understanding</b></p>
                <p>Items and their links</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 33%; height: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/graph-from-table-3.svg" alt="From a table to a graph" style="height: auto; max-width: 100%; max-height: 42%;">
                <p><b>Data preparation</b></p>
                <p>Links inside the set, two graphs</p>
            </div>
        </div>
    </div>
    <div class="row" style="height: 50%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 33%; height: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/pagerank-iteration-3.svg" alt="Four items sized by PageRank" style="height: auto; max-width: 100%; max-height: 42%;">
                <p><b>Modeling</b></p>
                <p>Degree, PageRank, and node2vec</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 33%; height: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/graph-seed-overlap.svg" alt="Two neighbour sets of one node" style="height: auto; max-width: 100%; max-height: 42%;">
                <p><b>Evaluation</b></p>
                <p>An outside measure, seeds, random pairs</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 33%; height: 100%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/crisp-dm-process-diagram.png" alt="CRISP-DM process diagram" style="height: auto; max-width: 100%; max-height: 42%;">
                <p><b>Deployment</b></p>
                <p>What using a place would mean</p>
            </div>
        </div>
    </div>
</div>
<div class="footnote" style="flex-shrink: 0;">Social Network Analysis Visualization - Martin Grandjean, CC BY-SA 3.0. CRISP-DM Process Diagram - Kenneth Jensen, CC BY-SA 3.0. Both via Wikimedia Commons</div>

## CRISP-DM

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <ul>
                    <li><p><b>The task:</b> can the attributes of an item predict a label that someone gave?</p></li>
                    <li><p><b>The data:</b> a table of attributes with a given label</p></li>
                    <li><p><b>Modeling:</b> logistic regression, a random forest, and one hidden layer</p></li>
                    <li><p><b>Evaluation:</b> right and wrong counts on items kept apart, against the majority class</p></li>
                    <li><p><b>Deployment:</b> what using a prediction would mean</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/crisp-dm-process-diagram.png" alt="CRISP-DM process diagram" style="height: auto; max-width: 100%; max-height: 90%;">
                <div class="footnote">CRISP-DM Process Diagram - Kenneth Jensen, CC BY-SA 3.0 <https://creativecommons.org/licenses/by-sa/3.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
