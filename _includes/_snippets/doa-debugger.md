<!-- SLIDES: -->

## Data-Oriented Debugger

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 95%">
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="https://upload.wikimedia.org/wikipedia/commons/1/15/Neural_Network.svg" alt="Deep Neural Network" style="max-width: 100%; height: auto;">
                <div class="footnote">Deep Neural Network with multiple hidden layers - QuantuMechaniX8, CC0, via Wikimedia Commons</div>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/context-3.png" alt="AI System" style="height: 400px">
            </div>
        </div>
    </div>
</div>

## Data-Oriented Debugger

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p style="margin: 0 0 0.35em 0;"><b>Related work</b> — taxonomy (paper §Related Work)</p>
                <img class="external-svg" src="{{ site.url }}/assets/media/diagrams/related-work-debugging-taxonomy.svg" alt="Taxonomy of debugging related work: Debugging splits into software debugging with LLM-assisted code (Toggle, RAGFix, Confix, examples truncated) and DNN debugging with visual tools, fault localisation, repair frameworks, and LLM or VLM approaches for neural networks." style="max-width: 100%; height: auto; max-height: 480px;">
                <p style="margin: 0.5em 0 0 0; font-size: 0.85em; text-align: left;">Software branch: conventional code; DNN branch: the four strands used in the paper (fault localisation aggregates traces, learned telemetry, and neuron or cohort analyses). Our work combines instrumentation with LLM-grounded repair.</p>
            </div>
        </div>
    </div>
</div>

## Data-Oriented Debugger

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Positioning of the DOA Debugger</b></p>
                <br>
                <p>The debugger is designed around <b>DOA principles</b>: make the relevant system state and traces explicit, queryable, and reusable for analysis.</p>
                <br>
                <ul>
                    <li><b>Input:</b> structured artefacts from training/inference/runtime logs</li>
                    <li><b>Core:</b> data-first representation + retrieval pipeline to support diagnostic reasoning</li>
                    <li><b>Output:</b> interpretable, context-grounded debugging assistance for ML-based systems</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Data-Oriented Debugger

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 95%">
            <div class="column vertical-middle text-center" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/diagrams/rag-process.svg" alt="RAG Process" style="height: 500px">
                <div class="footnote">RAG Process</div>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/doa-architecture.png" alt="DOA Architecture" style="height: 400px">
            </div>
        </div>
    </div>
</div>

## Data-Oriented Debugger

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 95%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img src="{{ site.url }}/assets/media/images/doa-llm-debugger.png" alt="DOA Debugger" style="height: 500px">
            </div>
        </div>
    </div>
</div>

## Data-Oriented Debugger

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 95%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img src="{{ site.url }}/assets/media/images/doa-log-ml-1.png" alt="DOA Debugger" style="height: 800px">
            </div>
        </div>
    </div>
</div>

## Data-Oriented Debugger

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 95%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img src="{{ site.url }}/assets/media/images/doa-log-ml-2.png" alt="DOA Debugger" style="height: 800px">
            </div>
        </div>
    </div>
</div>

## Data-Oriented Debugger

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 95%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img src="{{ site.url }}/assets/media/images/doa-llm-debugger-ki.png" alt="DOA Debugger" style="height: 500px">
            </div>
        </div>
    </div>
</div>
<!-- end SLIDES: -->
