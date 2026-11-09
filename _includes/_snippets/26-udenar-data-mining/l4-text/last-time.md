<!-- SLIDES: -->

## Last Time

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <ul>
                    <li><b>The task:</b> which items share a group, and which fit no group</li>
                    <li><b>The data:</b> items described by the same attributes</li>
                    <li><b>The methods:</b> k-means, Gaussian mixtures, and HDBSCAN</li>
                    <li><b>Evaluation and deployment:</b> a shuffled baseline, stability, and what using a group would mean</li>
                </ul>
                <p>This lecture is the text extraction task.</p>
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
                    <li><b>The task:</b> what short answer does each text give to a question, judged against marks?</li>
                    <li><b>The data:</b> texts and a sample marked by a person, such as emails, reviews, and abstracts</li>
                    <li><b>Modeling:</b> a keyword list, TF-IDF with logistic regression, and a text encoder</li>
                    <li><b>Evaluation:</b> right and wrong counts against a majority baseline</li>
                    <li><b>Deployment:</b> what using an extraction would mean, and its limits</li>
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
