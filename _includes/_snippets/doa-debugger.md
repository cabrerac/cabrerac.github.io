<!-- SLIDES: -->

## Data-Oriented Debugger

<div class="rows" style="height: 100%">
   <div class="row" style="height: 20%">
        <div class="columns" style="width: 100%">
            <p style="text-align: left;">Interpreting DNNs behaviour is hard. ML engineers struggle to identify the root of errors in buggy models when networks fail silently. <b>The DOA principles can support practitioners when debugging DNNs.</b></p>
        </div>
    </div>
    <div class="row" style="height: 80%">
        <div class="columns" style="width: 100%">
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
    <div class="row" style="height: 75%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p style="margin: 0 0 0.35em 0;"><b>Related work taxonomy</b></p>
                <img class="external-svg" src="{{ site.url }}/assets/media/diagrams/related-work-debugging-taxonomy.svg" alt="Taxonomy of debugging related work: Debugging splits into software debugging with LLM-assisted code (Toggle, RAGFix, Confix, examples truncated) and DNN debugging with visual tools, fault localisation, repair frameworks, and LLM or VLM approaches for neural networks." style="max-width: 100%; height: auto; max-height: 480px;">
            </div>
        </div>
    </div>
    <div class="row" style="height: 25%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p style="text-align: left;">DNN branch: fault localisation aggregates traces, learned telemetry, and neuron or cohort analyses. Repair frameworks rely on pre-defined rules and solutions, and hyperparameter optimisation. Recent LLM-based approaches use prompt-engineering (e.g., semantic heatmaps, errors context, etc.) to identify the causes of errors and assign hyperparameters' values. <b>Our work combines monitoring, DOA, and LLM-based repair.</b></p>
            </div>
        </div>
    </div>
</div>

## Data-Oriented Debugger

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p>The debugger is designed around the <b>data-first systems</b> principle. It makes the relevant system state and traces explicit, queryable, and reusable for analysis. Such a data substrate is used for fault localisation and repair. LLMs operate as interfaces to interpret the recorded data.</p>
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
    <div class="row" style="height: 20%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
               We are generating logging data at the moment. Next step is to use the logs for testing and evaluating fault localisation and repair.
            </div>
         </div>
    </div>
    <div class="row" style="height: 80%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Data captured per run</b></p>
                <ul>
                    <li><b>Model</b>, <b>layer</b> and <b>parameter</b> metrics over training</li>
                    <li>Computational graph (<i>graph.json</i> / <i>graph.svg</i>), model code and static attributes</li>
                    <li>Per-orchestration: manifest, run mappings, timing summary, failure summary</li>
                    <li>Execution profiles for trade-offs: <b>dev</b>, <b>stability</b>, <b>paper</b></li>
                </ul>
                <p style="text-align: left;">Two entry points: PyTorch test models and a curated set of <b>real-world and silent DNN bugs</b>.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Bug dataset:</b> <a href="http://defect4aitesting.soccerlab.polymtl.ca/" target="_blank" rel="noopener noreferrer">defect4ml</a> (TensorFlow &amp; Keras)</p>
                <ul>
                    <li><b>100</b> real-world DNN bugs</li>
                    <li>Bug type: <b>silent (59)</b> vs. not silent (41)</li>
                    <li>Data dependency: <i>0</i> code-inspectable &middot; <i>1</i> not data-specific (testing helps) &middot; <i>2</i> data-specific</li>
                    <li>Silent groups for evaluation: <b>not data-specific (42)</b> + <b>data-specific (16)</b></li>
                    <li>Splits: <b>debug 8</b> and <b>evaluation 50</b>. 1 excluded</li>
                </ul>
                <p style="text-align: left;">Running all of them at the moment with different logging levels to measure the impact of DOA. <b>Trade-off between execution time and bugs resolution.</b></p>
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
