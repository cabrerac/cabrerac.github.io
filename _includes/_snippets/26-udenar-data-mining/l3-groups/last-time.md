<!-- SLIDES: -->

## Last Time

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <ul>
                    <li><b>Frequent word pairs:</b> pairs in at least the support floor of papers</li>
                    <li><b>Lift:</b> a pair against independence</li>
                    <li><b>Word embeddings:</b> closeness learned from other texts</li>
                    <li><b>Baselines:</b> swap randomisation says which pairs beat chance</li>
                </ul>
                <p>Each paper now has or has not a kept pair. This lecture groups whole papers.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/frequent-itemsets-lattice.png" alt="Itemset lattice" style="height: 380px">
                <div class="footnote">FrequentItems - Xodarap00, CC BY-SA 3.0 <https://creativecommons.org/licenses/by-sa/3.0>, via Wikimedia Commons</div>
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
                    <li><b>Data preparation:</b> word counts per paper scaled to length 1, then SVD</li>
                    <li><b>Modeling:</b> k-means, a Gaussian mixture, HDBSCAN</li>
                    <li><b>Evaluation:</b> silhouette against a shuffled baseline, stability, agreement, noise</li>
                    <li><b>Deployment:</b> the group result for each paper, saved in outputs/grupos_l3.csv</li>
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
