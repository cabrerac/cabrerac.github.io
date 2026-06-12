<!-- SLIDES: -->

## Data Architecture

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p><b>Data architecture</b> shows how data moves from <b>sources</b> through <b>storage and processing</b> to the <b>people and tasks</b> that use it — assess and address.</p>
            </div>
        </div>
    </div>
</div>

## Data Architecture

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 48%">
                <p><b>Typical layers</b></p>
                <ul>
                    <li><b>Sources:</b> GEIH CSV, OSM, other APIs</li>
                    <li><b>Storage format:</b> Parquet, partitions, lakehouse path</li>
                    <li><b>Processing:</b> harmonise, query engines, MapReduce</li>
                    <li><b>Consumers:</b> quality checks (assess), analytics &amp; reports (address)</li>
                </ul>
                <p>Last week you wrote <b>requirements</b>. This week you sketch <b>architecture</b> — how your group will implement those requirements.</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 52%">
                <img src="{{ site.url }}/assets/media/diagrams/big-data-pipeline-template.svg" alt="Big data pipeline template" style="height: 360px">
            </div>
        </div>
    </div>
</div>

## Data Architecture

<div class="rows" style="height: 100%">
    <div class="row" style="height: 12%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p><b>Reference design</b> (research ICU data platform)</p>
            </div>
        </div>
    </div>
    <div class="row" style="height: 88%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/aicu-acces-architecture.svg" alt="aICU access architecture: sources, harmonisation, query engine, consumers" style="height: 100%">
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
