<!-- SLIDES: -->

## Last Time

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <ul>
                    <li><b>Degree:</b> how many links, and a hub is a warning</li>
                    <li><b>PageRank:</b> a link from a well placed paper counts more</li>
                    <li><b>Betweenness:</b> bridges between parts of the graph</li>
                    <li><b>node2vec:</b> papers that share a neighbourhood</li>
                </ul>
                <p>Every result so far came from the data itself. This lecture starts from a given label.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/pagerank-example.svg" alt="PageRank example" style="height: 380px">
                <div class="footnote">PageRanks Example - 345Kai and Stannered, Public domain, via Wikimedia Commons</div>
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
                    <li><b>Data preparation:</b> one table of attributes, scaled, encoded, missing values flagged</li>
                    <li><b>Modeling:</b> logistic regression, a random forest, one hidden layer</li>
                    <li><b>Evaluation:</b> right and wrong counts on rows kept apart, against the majority</li>
                    <li><b>Deployment:</b> the fifth result and the starter list</li>
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
