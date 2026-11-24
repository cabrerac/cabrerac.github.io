<!-- SLIDES: -->

## DOAgent

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/gridworld_demo.gif" alt="Grid-world" style="height: 400px">
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>GridWorld example</b></p>
                <ul>
                    <li>Dependency-free grid-world mapping scenario: agents discover cells and landmarks under partial observations</li>
                    <li>Each round agents publish an agent_update. They read the shared map (from visible records) and choose a move</li>
                    <li>Configurable topology and visibility. Optional energy-based participation (join/leave)</li>
                    <li>Run from config. Session records outcomes, traces, and agent_updates transparently</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## DOAgent

<div class="rows" style="height: 100%">
    <div class="row" style="height: 80%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/provenance_tree.png" alt="Provenance Tree" style="max-width: 100%; height: auto;">
            </div>
        </div>
    </div>
    <div class="row" style="height: 20%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Provenance:</b> the chain of trace, outcome and action records that leads to each outcome. Built from shared records alone.</p>
            </div>
        </div>
    </div>
</div>

## DOAgent

<div class="rows" style="height: 100%">
    <div class="row" style="height: 80%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/causal_attribution.png" alt="Causal attribution results" style="max-width: 100%; height: auto;">
            </div>
        </div>
    </div>
    <div class="row" style="height: 20%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Accountability:</b> which agent caused which state transitions. Left: discovery over rounds. Centre: cells per agent. Right: productive and redundant decisions.</p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
