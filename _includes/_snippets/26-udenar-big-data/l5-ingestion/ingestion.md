<!-- SLIDES: -->

## Data Ingestion

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p><b>Ingestion</b> is the stage that moves data from its <b>sources</b> into the place where we store and process it.</p>
            </div>
        </div>
    </div>
</div>

## Data Ingestion

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>The data science pipeline</b></p>
                <ul>
                    <li>Sources &#8594; <b>ingestion</b> &#8594; storage &#8594; processing &#8594; analytics &#8594; decision</li>
                    <li>We have built storage and processing</li>
                    <li>Ingestion is the <b>plumbing</b> that keeps them fed</li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/big-data-pipeline-template.svg" alt="Big data pipeline" style="height: 360px">
            </div>
        </div>
    </div>
</div>

## Data Ingestion

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Two questions decide how we ingest any source</b></p>
                <ul>
                    <li><b>How much?</b> the volume we must move and store</li>
                    <li><b>How often / how fresh?</b> the velocity the decision needs</li>
                </ul>
                <p>The answers split ingestion into two families: <b>batch</b> and <b>stream</b>.</p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
