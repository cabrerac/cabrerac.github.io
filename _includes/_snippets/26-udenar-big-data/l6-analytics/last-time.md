<!-- SLIDES: -->

## Last Time

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Batch ingestion</b></p>
                <ul>
                    <li>Bounded data, processed on a <b>schedule</b></li>
                    <li><b>ETL</b> steps wired into an orchestrated flow</li>
                    <li>Governance travels with it: audit log, schema contract</li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/etl-vs-elt.svg" alt="ETL versus ELT" style="height: 360px">
            </div>
        </div>
    </div>
</div>

## Last Time

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 42%">
                <p><b>Stream ingestion</b></p>
                <ul>
                    <li>Unbounded <b>events</b>, processed as they arrive</li>
                    <li><b>Publish / subscribe</b> decouples producers and consumers</li>
                    <li>A partitioned log gives parallelism and replay</li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 58%">
                <img src="{{ site.url }}/assets/media/diagrams/pubsub-streaming-architecture.svg" alt="Publish/subscribe streaming architecture" style="height: 380px">
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
