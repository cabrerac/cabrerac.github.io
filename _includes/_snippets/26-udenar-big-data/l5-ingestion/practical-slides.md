<!-- SLIDES: -->

## Practical

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Lab demo — the full arc</b></p>
                <ul>
                    <li>Governed <b>batch</b> ETL, orchestrated with a <b>Prefect</b> flow</li>
                    <li>A <b>local Kafka</b> broker: produce and consume events</li>
                    <li>Land the stream in an in-memory <b>document store</b></li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Stack</b></p>
                <ul>
                    <li><code>prefect</code> · <code>kafka-python</code></li>
                    <li><code>feedparser</code> · <code>mongomock</code></li>
                    <li><code>polars</code> · <code>pyarrow</code></li>
                </ul>
                <p>Individual notebook is <b>run-only</b>; you implement the pipeline in the group notebook.</p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
