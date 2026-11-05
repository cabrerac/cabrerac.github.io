<!-- SLIDES: -->

## Last Time

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <ul>
                    <li><b>The concept:</b> data mining searches for valid, new and useful patterns</li>
                    <li><b>The methodologies:</b> KDD, SEMMA and CRISP-DM, the one we follow</li>
                    <li><b>The question:</b> a question, its steps, a standard and a use</li>
                    <li><b>The data and the project:</b> nutrition papers for the labs, a department file for the project</li>
                </ul>
                <p>This lecture starts the modeling phase with patterns that repeat.</p>
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
                    <li><b>Data preparation:</b> one set of words per paper, pair and word counts, a vocabulary match</li>
                    <li><b>Modeling:</b> frequent word pairs, lift, embedding closeness</li>
                    <li><b>Evaluation:</b> a swap randomisation baseline and a random pair baseline</li>
                    <li><b>Deployment:</b> how a kept pattern will be used</li>
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
