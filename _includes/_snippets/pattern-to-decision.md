<!-- SLIDES: -->

## Deployment

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p><b>Deployment</b> is putting an evaluated result to use, by someone, inside a process, with a plan to check it while it is in use.</p>
            </div>
        </div>
    </div>
</div>

## Deployment

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Deployment in CRISP-DM</b></p>
                <ul>
                    <li><b>Who:</b> the people who act on the result, often not the analyst</li>
                    <li><b>Where:</b> a report, a decision process, or a running system</li>
                    <li><b>Monitoring:</b> a plan to re-check the result while it is in use</li>
                </ul>
                <br>
                <p>"Depending on the requirements, the deployment phase can be as simple as generating a report or as complex as implementing a repeatable data mining process across the enterprise." <a href="https://www.kde.cs.uni-kassel.de/wp-content/uploads/lehre/ws2012-13/kdd/files/CRISPWP-0800.pdf" target="_blank" rel="noopener noreferrer">(Chapman et al., 2000)</a></p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/crisp-dm-process-diagram.png" alt="CRISP-DM process diagram" style="height: 400px">
                <div class="footnote">CRISP-DM Process Diagram - Kenneth Jensen, CC BY-SA 3.0 <https://creativecommons.org/licenses/by-sa/3.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Deployment

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Deploying a pattern</b></p>
                <p>A kept set of items feeds something people do.</p>
                <ul>
                    <li><b>Decision:</b> items placed, stocked, or offered together</li>
                    <li><b>Recommendation:</b> transactions with A are shown B</li>
                    <li><b>Report:</b> the top sets with their support and lift, for a person to read</li>
                    <li><b>Filter:</b> transactions that hold a set are flagged for review</li>
                </ul>
                <p>We deploy the set together with its support, lift, floor, and baseline.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/supermarket-checkout.jpg" alt="Supermarket checkout" style="height: 400px">
                <div class="footnote">Supermarket checkout Tegut Tauberbischofsheim - Triplec85, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Deployment

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>What a deployed pattern implies</b></p>
                <ul>
                    <li><b>Co-occurrence, not cause:</b> A and B together does not mean A leads to B</li>
                    <li><b>Tied to the data:</b> other transactions or another floor give other support and lift</li>
                    <li><b>Goes stale:</b> we re-check counts and the baseline on new transactions</li>
                    <li><b>People:</b> who acts on it, who is affected, and who falls below the floor</li>
                    <li><b>Training habits:</b> a close pair can reflect the collection the vectors were trained on <a href="https://arxiv.org/abs/1607.06520" target="_blank" rel="noopener noreferrer">(Bolukbasi et al., 2016)</a> <a href="https://doi.org/10.1126/science.aal4230" target="_blank" rel="noopener noreferrer">(Caliskan et al., 2017)</a></li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/context-people.png" alt="People affected by a data system" style="height: 400px">
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
