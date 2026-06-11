<!-- SLIDES: -->

## ETL

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Extract, Transform, Load</b></p>
                <ul>
                    <li><b>Extract:</b> get the data from its source</li>
                    <li><b>Transform:</b> clean, join, rename, fix types</li>
                    <li><b>Load:</b> write it where analysts can use it</li>
                </ul>
                <p>ETL is the classic recipe that moves data from messy sources into a clean store. Storing and processing are both part of it.</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/big-data-pipeline-template.svg" alt="Pipeline template" style="height: 360px">
            </div>
        </div>
    </div>
</div>

## ETL

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Our course pipeline is ETL</b></p>
                <ul>
                    <li><b>Extract:</b> we crawled DANE for GEIH in week 1</li>
                    <li><b>Transform:</b> we harmonise the monthly tables today</li>
                    <li><b>Load:</b> we write partitioned Parquet to Drive</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/big-data-pipeline-template.svg" alt="Pipeline template" style="height: 360px">
            </div>
        </div>
    </div>
</div>

## ETL

<div class="rows" style="height: 100%">
    <div class="row" style="height: 72%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/etl-vs-elt.svg" alt="ETL versus ELT" style="height: 340px">
            </div>
        </div>
    </div>
    <div class="row" style="height: 28%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p><b>ETL or ELT?</b> Warehouses transform before load, so data lands clean. Lakehouses load raw and transform at query time, when an engine reads it.</p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
