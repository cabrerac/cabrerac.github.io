<!-- SLIDES: -->

## Last Time

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <ul>
                    <li><b>Groups of similar papers:</b> k-means, Gaussian mixtures and HDBSCAN</li>
                    <li><b>Noise:</b> papers that fit no group are listed for a look</li>
                    <li><b>Silhouette:</b> weak structure, judged against a shuffled table</li>
                    <li><b>The project:</b> read_group joins has_pattern as a second result</li>
                </ul>
                <p>Groups ignore what the question means. This lecture reads the text for it.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/clusters-with-noise.svg" alt="Groups with noise points" style="height: 380px">
                <div class="footnote">Cluster-2 - hellisp and Wgabrie, Public domain, via Wikimedia Commons</div>
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
                    <li><b>Data preparation:</b> a keyword list, a TF-IDF matrix, the text cut to 512 tokens, marked examples</li>
                    <li><b>Modeling:</b> keyword match, TF-IDF with logistic regression, a frozen encoder with logistic regression</li>
                    <li><b>Evaluation:</b> right and wrong counts on the marked papers</li>
                    <li><b>Deployment:</b> the text result as a third result for the list</li>
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
