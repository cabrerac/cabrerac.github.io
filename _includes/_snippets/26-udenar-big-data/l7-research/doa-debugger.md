<!-- SLIDES: -->

## Data-Oriented Debugger

<div class="rows" style="height: 100%">
   <div class="row" style="height: 20%">
        <div class="columns" style="width: 100%">
            <p style="text-align: left;">Interpreting DNN behaviour is hard. ML engineers struggle to find the root cause when networks fail silently. <b>DOA principles can support practitioners when debugging DNNs.</b></p>
        </div>
    </div>
    <div class="row" style="height: 80%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="https://upload.wikimedia.org/wikipedia/commons/1/15/Neural_Network.svg" alt="Deep Neural Network" style="max-width: 100%; height: auto;">
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
                <img class="external-svg" src="{{ site.url }}/assets/media/diagrams/related-work-debugging-taxonomy.svg" alt="Taxonomy of DNN debugging related work" style="max-width: 100%; height: auto; max-height: 480px;">
            </div>
        </div>
    </div>
    <div class="row" style="height: 25%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p style="text-align: left;"><b>Our work combines monitoring, DOA, and LLM-based repair</b> — fault localisation on a queryable telemetry substrate, not post-hoc feature attribution alone.</p>
            </div>
        </div>
    </div>
</div>

## Data-Oriented Debugger

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/doa-debugger.svg" alt="DOA Debugger architecture" style="height: 500px">
            </div>
        </div>
    </div>
</div>

## Data-Oriented Debugger

<div class="rows" style="height: 100%">
    <div class="row" style="height: 10%">
        <div class="columns" style="width: 100%">
            <p style="text-align: left;">The <b>Monitoring Engine</b> builds a shared data model from forward and backward passes (PyTorch hooks, <i>torch.fx</i>, MLflow persistence).</p>
        </div>
    </div>
    <div class="row" style="height: 90%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 33%">
                <img src="{{ site.url }}/assets/media/images/doa-metrics/stable_cnn-model.png" alt="Model-level loss and accuracy vs step" style="width: 100%; height: auto; max-height: 460px;">
                <p style="font-size: 0.8em; margin-top: 0.3em;"><b>Model-level</b></p>
            </div>
            <div class="column vertical-middle text-center" style="width: 33%">
                <img src="{{ site.url }}/assets/media/images/doa-metrics/stable_cnn-parameters.png" alt="Parameter L2 distance vs step" style="width: 100%; height: auto; max-height: 460px;">
                <p style="font-size: 0.8em; margin-top: 0.3em;"><b>Parameters</b></p>
            </div>
            <div class="column vertical-middle text-center" style="width: 34%">
                <img src="{{ site.url }}/assets/media/images/doa-metrics/stable_cnn-layers.png" alt="Per-module gradient norms vs step" style="width: 100%; height: auto; max-height: 460px;">
                <p style="font-size: 0.8em; margin-top: 0.3em;"><b>Per-module</b></p>
            </div>
        </div>
    </div>
</div>

## Data-Oriented Debugger

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%; overflow: hidden;">
        <div class="columns" style="width: 100%; height: 100%;">
            <div class="column vertical-middle text-center" style="width: 100%; height: 100%;">
                <img class="external-svg" src="{{ site.url }}/assets/media/diagrams/doa-fault-localisation-pipeline.svg" alt="Fault localisation pipeline" style="height: 500px;">
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
