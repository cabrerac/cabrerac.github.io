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
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Related Work</b></p>
                <ul style="margin-top: 0;">
                    <li><b>Debugging software using LLMs:</b> LLMs support different stages like localisation and fixing. Related works apply different strategies to analyse buggy software, prompt LLMs, and apply patches
                        <a href="https://doi.org/10.1145/3660773" target="_blank" rel="noopener noreferrer">(Hossain et al., 2024)</a>,
                        <a href="https://ieeexplore.ieee.org/document/10825785" target="_blank" rel="noopener noreferrer">(Mansur et al., 2024)</a>,
                        <a href="https://www.sciencedirect.com/science/article/pii/S0164121224001614" target="_blank" rel="noopener noreferrer">(Xiao et al., 2024)</a>,
                        <a href="https://arxiv.org/abs/2506.19045" target="_blank" rel="noopener noreferrer">(Yaraghi et al., 2025)</a>,
                        <a href="https://arxiv.org/abs/2411.08172" target="_blank" rel="noopener noreferrer">(Morovati et al., 2024)</a>.
                    </li>
                    <li><b>Visual tools:</b> They turn low-level signals (e.g., losses, gradients, etc) into dashboards or dependency views so training issues are easier to see
                        <a href="https://proceedings.neurips.cc/paper_files/paper/2021/file/ae3539867aaeec609a4260c6feb725f4-Paper.pdf" target="_blank" rel="noopener noreferrer">(Schneider et al., 2021)</a>,
                        <a href="https://arxiv.org/abs/2407.21656" target="_blank" rel="noopener noreferrer">(Dietz et al., 2024)</a>.
                    </li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Data-Oriented Debugger

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Related Work</b></p>
                <ul style="margin-top: 0;">
                    <li><b>Fault localisation using traces and graphs:</b> One line of work records traces from training signals and analyses them with statistics and rules. Another line builds graphs from the training programme and checks them against known bug patterns in configuration
                        <a href="https://ieeexplore.ieee.org/document/9402065" target="_blank" rel="noopener noreferrer">(Wardat et al., 2021)</a>,
                        <a href="https://ieeexplore.ieee.org/document/10589839" target="_blank" rel="noopener noreferrer">(Hong et al., 2024)</a>.
                    </li>
                    <li><b>Fault localisation using ML on metric streams:</b> They treat diagnosis as a learning problem over telemetry. These works turn sequences of training summaries into features and train predictors for fault types.
                        <a href="https://doi.org/10.1145/3510003.3510099" target="_blank" rel="noopener noreferrer">(Cao et al., 2022)</a>,
                        <a href="https://arxiv.org/abs/2411.08172" target="_blank" rel="noopener noreferrer">(Morovati et al., 2024)</a>.
                    </li>
                    <li><b>Fault localisation on neurons and inputs:</b> Some methods compare internal state between good and bad runs. Others cluster failing inputs that share a root cause before retraining, or freeze or isolate neurons to see what drives a bug
                        <a href="https://doi.org/10.1145/3236024.3236082" target="_blank" rel="noopener noreferrer">(Ma et al., 2018)</a>,
                        <a href="https://doi.org/10.1145/3510454.3516858" target="_blank" rel="noopener noreferrer">(Fahmy et al., 2022)</a>,
                        <a href="https://doi.org/10.1145/3650212.3652132" target="_blank" rel="noopener noreferrer">(Chen et al., 2024)</a>.
                    </li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Data-Oriented Debugger

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Related Work</b> (continued)</p>
                <ul style="margin-top: 0;">
                    <li><b>Repair frameworks:</b> After fault localisation, these pipelines propose concrete repairs—often by mapping symptoms to a fixed set of rules, predicting a fault class for a CNN then searching hyper-parameters, or monitoring training and applying one of several predefined recovery steps before restarting. Repairs are tied to chosen catalogs rather than open-ended text generation
                        <a href="https://doi.org/10.1145/3510003.3510071" target="_blank" rel="noopener noreferrer">(Wardat et al., 2022)</a>,
                        <a href="https://ieeexplore.ieee.org/document/10491264" target="_blank" rel="noopener noreferrer">(Wardat et al., 2024)</a>,
                        <a href="https://ieeexplore.ieee.org/document/10654494" target="_blank" rel="noopener noreferrer">(Zhang et al., 2025)</a>.
                    </li>
                    <li><b>LLMs and VLMs for debugging DNNs:</b> Recent work uses vision–language models and heatmaps to relate internal activations to semantics, uses LLMs to tag failures and build error slices, or uses separate prompts for fault localisation and for repair on hyper-parameters. Studies on ChatGPT for deep learning repair show that richer prompt context (intent, code, data) helps compared with code alone
                        <a href="https://doi.ieeecomputersociety.org/10.1109/CAIN66642.2025.00027" target="_blank" rel="noopener noreferrer">(Hu et al., 2025)</a>,
                        <a href="https://arxiv.org/abs/2501.16751" target="_blank" rel="noopener noreferrer">(Chen et al., 2025)</a>,
                        <a href="https://arxiv.org/abs/2506.03396" target="_blank" rel="noopener noreferrer">(Kim et al., 2025)</a>,
                        <a href="https://link.springer.com/article/10.1007/s10515-025-00492-x" target="_blank" rel="noopener noreferrer">(Cao et al., 2025)</a>. Our debugger follows that direction by packaging numerical and structural context from instrumentation for the LLM stage.
                    </li>
                </ul>
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
