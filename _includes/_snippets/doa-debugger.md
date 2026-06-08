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
    <div class="row" style="height: 10%">
        <div class="columns" style="width: 100%">
            <p style="text-align: left;">The <b>Monitoring Engine</b> builds a shared data model from forward and backward passes.</p>
        </div>
    </div>
    <div class="row" style="height: 70%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Static artefacts</b> (init / first step)</p>
                <ul>
                    <li><i>model_info.json:</i> optimiser, batch size, epochs, learning rate, loss</li>
                    <li><i>static_attributes.json:</i> per-module input / output shapes and dtypes</li>
                    <li><i>graph.txt</i> / <i>graph.svg:</i> symbolic traced graph of the model</li>
                    <li><i>model_code.py:</i> traced source code</li>
                    <li><i>metrics_metadata.json:</i> step &rarr; {stage, epoch}</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Metrics every k steps</b></p>
                <ul>
                    <li>Parameter L2 distance from initialisation and update size. Total and per-layer</li>
                    <li>Training and evaluation loss and accuracy</li>
                    <li>Per-module input, output, and gradient statistics: <i>min / max / median / mean / std / norm</i></li>
                </ul>
            </div>
        </div>
    </div>
    <div class="row" style="height: 20%">
        <div class="columns" style="width: 100%">
            <p style="text-align: left;"><b>Built on:</b> PyTorch Hooks, <i>torch.fx</i>, and BackPACK. Logs and artefacts are persisted to MLflow.</p>
        </div>
    </div>
</div>

## Data-Oriented Debugger

<div class="rows" style="height: 100%">
    <div class="row" style="height: 14%">
        <div class="columns" style="width: 100%">
            <p style="text-align: left;">The <b>Fault Localisation Engine</b> runs sequential checks over logged MLflow data. The <b>first failure</b> stops the pipeline, triggers <b>graph traversal</b>, then hands off to the repair engine.</p>
        </div>
    </div>
    <div class="row" style="height: 72%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img class="external-svg" src="{{ site.url }}/assets/media/diagrams/doa-fault-localisation-pipeline.svg" alt="Fault localisation pipeline: MLflow monitoring artefacts feed sequential stage checks; first failure triggers graph traversal to a problematic node, then LLM repair with expandable context." style="max-width: 100%; height: auto; max-height: 520px;">
            </div>
        </div>
    </div>
    <div class="row" style="height: 14%">
        <div class="columns" style="width: 100%">
            <p style="text-align: left;"><b>Stages 0–3:</b> execution, loss near zero, loss definition, gradient magnitude. Further checks cover update transformation and gradient/update expectations.</p>
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
    <div class="row" style="height: 16%">
        <div class="columns" style="width: 100%">
            <p style="text-align: left;">The <b>repair engine</b> attaches <b>diagnosis context</b> to the LLM targeted at the problematic node.</p>
        </div>
    </div>
    <div class="row" style="height: 67%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Context per problematic node</b></p>
                <ul>
                    <li>Node <b>name</b> and <b>attributes</b></li>
                    <li><b>Adjacent nodes</b> on the computational graph</li>
                    <li>Per-node issues and globally detected issues</li>
                    <li><b>Traced source code</b> for the node</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Two valid replies</b></p>
                <ul>
                    <li><i>NEED_MORE_CONTEXT</i> with the adjacent nodes the LLM wants to see next.</li>
                    <li><i>ENOUGH_CONTEXT</i> a dictionary of issues, each with <i>recommendation_text</i> and <i>recommendation_code</i>.</li>
                </ul>
            </div>
        </div>
    </div>
    <div class="row" style="height: 17%">
        <div class="columns" style="width: 100%">
            <p style="text-align: left;">The context is targeted, expandable, and grounded in the run's telemetry.</p>
        </div>
    </div>
</div>

## Data-Oriented Debugger

<div class="rows" style="height: 100%">
    <div class="row" style="height: 10%">
        <div class="columns" style="width: 100%">
            <p style="text-align: left;">The <b>repair engine</b> interleaves localisation and LLM repair with context expansion.</p>
        </div>
    </div>
    <div class="row" style="height: 90%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
<pre style="font-size: 0.85em; line-height: 1.45; padding: 0.8em 1em; background: #f4f4f4; border-radius: 6px;">
localise faults across stages
on failure, find the problematic node on the graph
assemble context (node + issues + traced code)

for d = 0 ... context_depth:
    ask LLM
    if reply = ENOUGH_CONTEXT:
        return recommendations
    else:
        expand context to adjacent nodes at depth d

return fallback (the diagnosis itself)
</pre>
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
    <div class="row" style="height: 14%">
        <div class="columns" style="width: 100%">
            <p style="text-align: left;"><b>Phase 0 smoke test</b> (not paper evaluation): does the full path <i>train &rarr; log &rarr; stage funnel &rarr; graph node</i> work on a synthetic fault?</p>
        </div>
    </div>
    <div class="row" style="height: 78%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 48%">
                <p><b>What we measure</b></p>
                <ol style="font-size: 0.9em; margin-top: 0.4em;">
                    <li><b>Logging substrate</b> — MLflow run has graph, metrics, and static artefacts (<i>xlm-estimator</i>).</li>
                    <li><b>Stage funnel</b> — sequential checks stop at the first fault (<i>xlm-interface</i>, no LLM).</li>
                    <li><b>Localisation</b> — graph traversal names one problematic node.</li>
                </ol>
                <p style="margin-top: 0.8em;"><b>Next:</b> full matrix on PyTorch test models, then defect4ml evaluation split.</p>
            </div>
            <div class="column vertical-top text-left" style="width: 52%">
                <p><b>Worked example: <code>high_loss</code></b> (insufficient model capacity)</p>
                <ul style="font-size: 0.9em; margin-top: 0.4em;">
                    <li>Train one epoch, <b>dev</b> profile — telemetry <b>complete</b>.</li>
                    <li>Stage funnel stops at <b>Loss near zero</b> (final loss &gt; 1e-3).</li>
                    <li>Graph traversal flags <b>output_layer</b>.</li>
                </ul>
                <p style="margin-top: 0.6em; font-size: 0.85em;"><i>This shows the pipeline runs end-to-end on a known fault. We are not yet reporting resolution rate or baseline comparison.</i></p>
            </div>
        </div>
    </div>
    <div class="row" style="height: 8%">
        <div class="columns" style="width: 100%">
            <p style="text-align: left; font-size: 0.85em;">Paper metrics (fault resolution, relevance, latency) need the evaluation split and baselines on the slide before that.</p>
        </div>
    </div>
</div>

## Data-Oriented Debugger

<div class="rows" style="height: 100%">
    <div class="row" style="height: 10%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-bottom text-left" style="width: 100%">
               <p style="text-align: left;">We plan to compare our approach with one or more baselines:</p>
            </div>
        </div>
    </div>
    <div class="row" style="height: 90%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 60%">
                <p><b>Compared against</b> (datasets we run):</p>
                <ul>
                    <li><b>Fault localisation:</b> DeepLocalize <a href="https://ieeexplore.ieee.org/document/9402065" target="_blank" rel="noopener noreferrer">(Wardat et al., 2021)</a>, DeepFD <a href="https://doi.org/10.1145/3510003.3510099" target="_blank" rel="noopener noreferrer">(Cao et al., 2022)</a>, FL4Deep <a href="https://arxiv.org/abs/2411.08172" target="_blank" rel="noopener noreferrer">(Morovati et al., 2024)</a>, Pysiassist <a href="https://ieeexplore.ieee.org/document/10589839" target="_blank" rel="noopener noreferrer">(Hong et al., 2024)</a>.</li>
                    <li><b>Repair:</b> DeepDiagnosis <a href="https://doi.org/10.1145/3510003.3510071" target="_blank" rel="noopener noreferrer">(Wardat et al., 2022)</a>, DeepCNN <a href="https://ieeexplore.ieee.org/document/10491264" target="_blank" rel="noopener noreferrer">(Wardat et al., 2024)</a>.</li>
                    <li><b>LLM-based:</b> <a href="https://arxiv.org/abs/2506.03396" target="_blank" rel="noopener noreferrer">(Kim et al., 2025)</a>, <a href="https://doi.org/10.1007/s10515-025-00492-x" target="_blank" rel="noopener noreferrer">(Cao et al., 2025)</a>.</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 40%">
                <p><b>Metrics</b></p>
                <ul>
                    <li>Fault resolution rate</li>
                    <li>Solution relevance</li>
                    <li>Latency</li>
                </ul>
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
