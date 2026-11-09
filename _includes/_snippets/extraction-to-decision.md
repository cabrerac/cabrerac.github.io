{% include _snippets/deployment.md %}
<!-- SLIDES: -->

## Deployment

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Deploying an extraction</b></p>
                <p>A short answer for each text feeds something people do.</p>
                <ul>
                    <li><b>Filter:</b> texts marked yes go to a person to read</li>
                    <li><b>Routing:</b> each text goes to the team its answer names</li>
                    <li><b>Report:</b> how many texts say yes, with the right and wrong counts</li>
                    <li><b>Decision:</b> one action per text, such as reply, read, or skip</li>
                </ul>
                <p>We deploy it together with the list or the threshold, the marks, the right and wrong counts with their interval, and the majority baseline.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/precision-recall.svg" alt="Precision and recall" style="height: 360px">
                <div class="footnote">Precisionrecall - Walber, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Deployment

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>What a deployed extraction implies</b></p>
                <ul>
                    <li><b>Errors have a cost:</b> a false yes is read for nothing, and a false no is never seen</li>
                    <li><b>Tied to the marks and the target:</b> another marked set, target, or threshold gives other counts</li>
                    <li><b>Goes stale:</b> wording changes, so we mark a fresh sample and count again</li>
                    <li><b>People:</b> who marks the texts, and whose language or long texts the method reads worse</li>
                </ul>
                <br>
                <p>Texts that use other words are never flagged. A deployed list says nothing about them.</p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
