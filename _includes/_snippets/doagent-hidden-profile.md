<!-- SLIDES: -->

## DOAgent

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>We also want to analyse how information flows in multi-agent systems and ask interpretability questions from three dimensions: explainability, traceability, and accountability.</p>
                <p><b>Hidden profile game:</b> three agents choose one of three routes.</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/doagent-hidden-profile/hidden-profile-game.png" alt="Hidden profile game: facts are dealt, agents send messages in rounds, report chances and vote" style="width: 460px">
            </div>
        </div>
    </div>
</div>

## DOAgent

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Two implementations</b> of the same game, with the same rules and the same scripted agents.</p>
                <ul>
                    <li><b>DOAgent:</b> one shared session, read at logging level 0, 1 or 2</li>
                    <li><b>MARBLE</b>, the framework behind MultiAgentBench: each component keeps its own log. We read one agent's log, three agent logs, all component logs, or a structured trace</li>
                </ul>
                <p>We played every possible deal (i.e., 18) and then asked interpretability questions.</p>
                <p><b>Record questions</b> are answered from one entry. <b>Link questions</b> need a stated connection between entries.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/doagent-hidden-profile/hidden-profile-readings.png" alt="One game read through a DOAgent session at three levels and through MARBLE logs in four ways" style="width: 540px">
            </div>
        </div>
    </div>
</div>

## DOAgent

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <p class="text-left"><b>Accountability:</b></p>
                <img src="{{ site.url }}/assets/media/images/doagent-hidden-profile/questions-accountability.png" alt="Accountability questions answered by each view, out of 18 deals" style="width: 1182px; max-width: 100%">
            </div>
        </div>
    </div>
</div>

## DOAgent

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <p class="text-left"><b>Traceability:</b></p>
                <img src="{{ site.url }}/assets/media/images/doagent-hidden-profile/questions-traceability.png" alt="Traceability questions answered by each view, out of 18 deals" style="width: 1182px; max-width: 100%">
            </div>
        </div>
    </div>
</div>

## DOAgent

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <p class="text-left"><b>Explainability:</b></p>
                <img src="{{ site.url }}/assets/media/images/doagent-hidden-profile/questions-explainability.png" alt="Explainability questions answered by each view, out of 18 deals" style="width: 1182px; max-width: 100%">
            </div>
        </div>
    </div>
</div>

## DOAgent

<div class="rows" style="height: 100%">
    <div class="row" style="height: 10%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <p class="text-left"><b>Uncertainty left after each step (bits):</b> only session levels 1 and 2 reach zero, like the rules.</p>
            </div>
        </div>
    </div>
    <div class="row" style="height: 90%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <img src="{{ site.url }}/assets/media/images/doagent-hidden-profile/recovery-curves.png" alt="Bits of uncertainty left after each step, for each view and dimension" style="width: 1190px; max-width: 100%">
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
