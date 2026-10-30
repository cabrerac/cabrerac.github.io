<!-- SLIDES: -->

## Last Time

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Lecture 4</b></p>
                <ul>
                    <li>Keywords, TF-IDF and a frozen encoder</li>
                    <li>Papers kept apart, right and wrong counts</li>
                    <li>A paper stays in view with at least two supports</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Three results so far</b></p>
                <ul>
                    <li>Has a kept pattern, from Lecture 2</li>
                    <li>Sits in a group the team reads, from Lecture 3</li>
                    <li>Matches the question in its text, from Lecture 4</li>
                    <li>Today a fourth, from the links, not the words</li>
                </ul>
                <p>node2vec reuses word2vec from Lecture 2.</p>
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
                    <li><b>Data preparation</b> - an edge list inside the set, a directed and an undirected graph, walks on the largest component</li>
                    <li><b>Modeling</b> - degree and PageRank, betweenness, node2vec</li>
                    <li><b>Evaluation</b> - no labels: against citations, across seeds, against random pairs</li>
                    <li><b>Deployment</b> - the graph result as a fourth support</li>
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
