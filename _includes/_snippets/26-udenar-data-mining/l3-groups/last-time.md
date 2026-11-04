<!-- SLIDES: -->

## Last Time

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Lecture 2</b></p>
                <ul>
                    <li>Word pairs in at least the support floor of papers</li>
                    <li>Lift against independence</li>
                    <li>Closeness in a word embedding</li>
                    <li>A swap randomisation baseline for each pair</li>
                    <li>One standout text is not a pattern</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>What we kept</b></p>
                <ul>
                    <li>Pairs at the floor and strictly above the 95th percentile of the swap null, read in lift order</li>
                    <li>Each paper now has or has not a kept pattern</li>
                    <li>That is the first result for the reading list</li>
                    <li>In Lecture 2 a word was an item in a text's basket. From now on, the item is the text we group</li>
                </ul>
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
                    <li><b>Data preparation</b> - word counts per paper scaled to length 1, then SVD</li>
                    <li><b>Modeling</b> - k-means, a Gaussian mixture, HDBSCAN</li>
                    <li><b>Evaluation</b> - silhouette against a shuffled baseline, stability, agreement, noise</li>
                    <li><b>Deployment</b> - the group result for each paper, saved in outputs/grupos_l3.csv</li>
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
