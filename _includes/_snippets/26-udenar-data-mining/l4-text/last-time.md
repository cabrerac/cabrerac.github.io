<!-- SLIDES: -->

## Last Time

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Lecture 3</b></p>
                <ul>
                    <li>k-means, Gaussian mixtures and HDBSCAN on the papers</li>
                    <li>Low silhouette, no natural k</li>
                    <li>Many papers fit no group, they are listed for a look</li>
                    <li>The list shows which results support each paper</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Two results so far</b></p>
                <ul>
                    <li>Has a kept pattern from Lecture 2</li>
                    <li>Sits in a group the team reads, from Lecture 3</li>
                    <li>Today a third result, read from the text itself</li>
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
                    <li><b>Data preparation</b> - a keyword list, a TF-IDF matrix, the text cut to 512 tokens, marked examples</li>
                    <li><b>Modeling</b> - keyword match, TF-IDF with logistic regression, a frozen encoder with logistic regression</li>
                    <li><b>Evaluation</b> - right and wrong counts on the marked papers</li>
                    <li><b>Deployment</b> - the text result as a third result for the list</li>
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
