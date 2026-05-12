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
    <div class="row" style="height: 16%">
        <div class="columns" style="width: 100%">
            <p style="text-align: left;">The <b>Fault Localisation Engine</b> runs sequential checks of incremental complexity over the logged data. The first failure stops the pipeline and triggers graph traversal to find the problematic node.</p>
        </div>
    </div>
    <div class="row" style="height: 67%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <ul>
                    <li><b>Stage 0 - Model Execution:</b> The run completes without errors and MLflow has the expected logs.</li>
                    <li><b>Stage 1 - Loss near zero:</b> Final training loss approaches zero (threshold &lt; 1e-3). It is a sanity check that the model can fit the data.</li>
                    <li><b>Stage 2 - Loss definition:</b> Loss values are well-defined. It flags <i>NaN</i>, <i>Inf</i>, or undefined values.</li>
                    <li><b>Stage 3 - Gradient magnitude:</b> Gradient norms stay healthy. Vanishing (&lt; 1e-7) or exploding (&gt; 1e3) gradients are flagged.</li>
                </ul>
            </div>
        </div>
    </div>
    <div class="row" style="height: 17%">
        <div class="columns" style="width: 100%">
            <p style="text-align: left;">On a fault, the engine traverses the <b>computational graph</b> to identify the problematic node and hands off to the repair engine.</p>
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
