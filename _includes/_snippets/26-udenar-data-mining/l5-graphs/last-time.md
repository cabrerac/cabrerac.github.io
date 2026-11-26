<!-- SLIDES: -->

## Last Time

<div class="rows" style="height: 100%">
    <div class="row" style="height: 50%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 33%; height: 100%">
                <img src="{{ site.url }}/assets/media/images/critical-thinking.png" alt="Critical Thinking" style="height: auto; max-width: 100%; max-height: 42%;">
                <p><b>Business understanding</b></p>
                <p>Short answers from many texts</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 33%; height: 100%">
                <table class="table" style="font-size: 0.6em">
                    <tbody>
                        <tr><td>Emails</td><td>spam</td></tr>
                        <tr><td>Reviews</td><td>complaint</td></tr>
                        <tr><td>Abstracts</td><td>on topic</td></tr>
                    </tbody>
                </table>
                <p><b>Data understanding</b></p>
                <p>Texts and their marks</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 33%; height: 100%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/topic-detection-document-word-matrix.gif" alt="Blocks of words appear in a document word matrix" style="height: auto; max-width: 100%; max-height: 42%;">
                <p><b>Data preparation</b></p>
                <p>Word sets, TF-IDF rows, and tokens</p>
            </div>
        </div>
    </div>
    <div class="row" style="height: 50%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 33%; height: 100%">
                <img src="{{ site.url }}/assets/media/images/transformer-full-architecture.png" alt="Transformer architecture" style="height: auto; max-width: 100%; max-height: 42%;">
                <p><b>Modeling</b></p>
                <p>A list, word weights, and an encoder</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 33%; height: 100%">
                <img class="external-svg" src="{{ site.url }}/assets/media/diagrams/confusion-matrix-counts.svg" alt="The four counts of a confusion matrix" style="height: auto; max-width: 100%; max-height: 42%;">
                <p><b>Evaluation</b></p>
                <p>Accuracy, the confusion matrix, and where the three agree</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 33%; height: 100%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/crisp-dm-process-diagram.png" alt="CRISP-DM process diagram" style="height: auto; max-width: 100%; max-height: 42%;">
                <p><b>Deployment</b></p>
                <p>What using an extraction would mean</p>
            </div>
        </div>
    </div>
</div>
<div class="footnote" style="flex-shrink: 0;">Topic detection in a document-word matrix - Christoph Carl Kling, CC BY-SA 4.0. Transformer, full architecture - dvgodoy, CC BY 4.0. CRISP-DM Process Diagram - Kenneth Jensen, CC BY-SA 3.0. All via Wikimedia Commons. Critical Thinking (Designed by freepik.com)</div>

## CRISP-DM

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <ul>
                    <li><p><b>The task:</b> where does each item sit among the others?</p></li>
                    <li><p><b>The data:</b> items and the links among them</p></li>
                    <li><p><b>Modeling:</b> degree, PageRank, and node2vec</p></li>
                    <li><p><b>Evaluation:</b> an outside measure, seeds, and random pairs</p></li>
                    <li><p><b>Deployment:</b> what using an item's place would mean</p></li>
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
