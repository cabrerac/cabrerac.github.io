<!-- SLIDES: -->

## Exploratory Results

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 55%">
                <p><b>Hidden profile game:</b> three agents choose one of three routes. Each agent holds some facts. Shared facts favour a wrong route, and the facts that favour the right route are split across agents.</p>
                <p>We follow one unshared fact, the <b>bridge fact</b>, and ask questions about who held it, who passed it on and how each agent voted. Each answer is checked against the exact answer from the game rules.</p>
                <p><b>A note on words:</b> in metrology, traceability means an unbroken chain of calibrations. Here it means following the links between the records of a run, such as which message carried a fact and in what order things happened.</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 45%">
                <img src="{{ site.url }}/assets/media/images/doagent-hidden-profile/hidden-profile-game.png" alt="Hidden profile game: facts are dealt, agents send messages in rounds, report chances and vote" style="width: 460px">
            </div>
        </div>
    </div>
</div>
<div class="footnote">Exploratory study: 18 deals played by three scripted agents, not model-backed agents.</div>

## Exploratory Results

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Two implementations</b> of the same game, with the same rules and the same scripted agents.</p>
                <ul>
                    <li><b>DOAgent:</b> one shared session, read at logging level 0, 1 or 2</li>
                    <li><b>MARBLE</b>, the framework behind MultiAgentBench: each component keeps its own log. We read one agent's log, three agent logs, all component logs, or a structured trace file</li>
                </ul>
                <p><b>Record questions</b> are answered from one entry. <b>Link questions</b> need a stated connection between entries.</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/doagent-hidden-profile/hidden-profile-readings.png" alt="One game read through a DOAgent session at three levels and through MARBLE logs in four ways" style="width: 540px">
            </div>
        </div>
    </div>
</div>
<div class="footnote">Exploratory study: 18 deals played by three scripted agents, not model-backed agents.</div>

## Exploratory Results

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p class="text-left"><b>Explainability:</b> only session levels 1 and 2 link each vote to the chances behind it.</p>
                <img src="{{ site.url }}/assets/media/images/doagent-hidden-profile/questions-explainability.png" alt="Explainability questions answered by each view, out of 18 deals" style="width: 1182px; max-width: 100%">
            </div>
        </div>
    </div>
</div>
<div class="footnote">Exploratory study: 18 deals played by three scripted agents, not model-backed agents. Each cell counts the deals where the answer matches the game rules.</div>

## Exploratory Results

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p class="text-left"><b>Traceability:</b> the full logs recover order and path. Only levels 1 and 2 link votes to chances.</p>
                <img src="{{ site.url }}/assets/media/images/doagent-hidden-profile/questions-traceability.png" alt="Traceability questions answered by each view, out of 18 deals" style="width: 1182px; max-width: 100%">
            </div>
        </div>
    </div>
</div>
<div class="footnote">Exploratory study: 18 deals, three scripted agents, not model-backed. The game has no step between the votes and the group choice.</div>

## Exploratory Results

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p class="text-left"><b>Accountability:</b> only session levels 1 and 2 link the votes to the group choice.</p>
                <img src="{{ site.url }}/assets/media/images/doagent-hidden-profile/questions-accountability.png" alt="Accountability questions answered by each view, out of 18 deals" style="width: 1182px; max-width: 100%">
            </div>
        </div>
    </div>
</div>
<div class="footnote">Exploratory study: 18 deals played by three scripted agents, not model-backed agents. Each cell counts the deals where the answer matches the game rules.</div>

## Next Steps

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>The same questions with model-backed agents</b>, on two published games:</p>
                <ul>
                    <li><b>HiddenBench:</b> hidden profile tasks for groups of language model agents <a href="https://arxiv.org/abs/2505.11556" target="_blank" rel="noopener noreferrer">(arXiv 2505.11556)</a></li>
                    <li><b>The Traitors:</b> a deception game with a private channel <a href="https://arxiv.org/abs/2505.12923" target="_blank" rel="noopener noreferrer">(arXiv 2505.12923)</a></li>
                </ul>
                <br>
                <p><b>One run, read three ways:</b></p>
                <ul>
                    <li>Each agent's full prompt trace, read by a judge model</li>
                    <li>The session records, read by the same judge</li>
                    <li>The session records, answered by query</li>
                </ul>
                <br>
                <p>A small HiddenBench pilot comes first. The campaign then varies discussion length, group size and visibility.</p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
