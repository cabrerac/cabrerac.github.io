<!-- SLIDES: -->

## Batch Processing

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p><b>Batch</b> collects data into a bounded chunk and processes it <b>on a schedule</b>. For example, every night.</p>
            </div>
        </div>
    </div>
</div>

## Batch Processing

<div class="rows" style="height: 100%">
    <div class="row" style="height: 86%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/batch-processing.svg" alt="Batch processing: bounded input, schedule trigger, ETL run, curated layer" style="height: 100%">
            </div>
        </div>
    </div>
    <div class="row" style="height: 14%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p>Collect a complete snapshot, then process it on a clock.</p>
            </div>
        </div>
    </div>
</div>

## Batch Processing

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Where it comes from</b></p>
                <ul>
                    <li>The oldest model of computing: mainframes ran <b>scheduled jobs</b> overnight</li>
                    <li>Payroll, billing, statements, and reports were produced in bulk</li>
                    <li>Data warehouses kept the same rhythm: load, then report</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Why it still dominates</b></p>
                <ul>
                    <li>High <b>throughput</b>: move a lot of data per run</li>
                    <li>Latency of hours or days is fine for many decisions</li>
                    <li>We do it once and reuse a stable <b>snapshot</b> (i.e., strong consistency)</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## ETL

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Extract, Transform, Load</b></p>
                <ul>
                    <li><b>Extract:</b> read the data from its source</li>
                    <li><b>Transform:</b> clean, join, rename, fix types</li>
                    <li><b>Load:</b> write it where analysts can use it</li>
                </ul>
                <p>ETL is the classic recipe of a batch pipeline. We met it in Lecture 3. Now we <b>automate</b> it.</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/big-data-pipeline-template.svg" alt="Pipeline template" style="height: 340px">
            </div>
        </div>
    </div>
</div>

## ETL

<div class="rows" style="height: 100%">
    <div class="row" style="height: 72%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/etl-vs-elt.svg" alt="ETL versus ELT" style="height: 100%">
            </div>
        </div>
    </div>
    <div class="row" style="height: 28%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p><b>ETL or ELT?</b> Warehouses transform before load, so data lands clean. Lakehouses load raw and transform at query time. Either way we keep <b>staging</b> and <b>curated</b> layers.</p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
