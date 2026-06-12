<!-- SLIDES: -->

## Last Time

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>We built a lakehouse</b></p>
                <ul>
                    <li>We harmonised messy monthly tables into one clean table</li>
                    <li>We stored it as <b>partitioned Parquet</b> in a small lakehouse</li>
                    <li>Cheap storage, columnar files, query-ready by year and month</li>
                </ul>
                <p>As an example, our GEIH lakehouse lives under <b>geih-spine</b>, split into <b>year</b> and <b>month</b>.</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/lake-warehouse-lakehouse.svg" alt="Data lake, warehouse, and lakehouse" style="height: 360px">
            </div>
        </div>
    </div>
</div>

## Last Time

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/big-data-pipeline-template.svg" alt="Big data pipeline, process stage" style="height: 380px">
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Storing was never the goal</b></p>
                <ul>
                    <li>We started from a question, not from a tool</li>
                    <li>Access and storage only set the table</li>
                    <li>Today we <b>process</b>: turn stored data into answers</li>
                </ul>
                <p>The stored data is neutral. The question, who is employed by department, is answered now.</p>
            </div>
        </div>
    </div>
</div>

## Last Time

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>One question, many ways to answer it</b></p>
                <ul>
                    <li>The same query runs on many <b>processing engines</b></li>
                    <li>We follow the history that produced them</li>
                    <li>From <b>MapReduce</b> to modern query engines</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>"Big Data consists of extensive datasets ... that require a scalable architecture for efficient storage, manipulation, and analysis." <a href="https://doi.org/10.6028/NIST.SP.1500-1" target="_blank" rel="noopener noreferrer">(NIST, 2015)</a></p>
                <p>We already did storage. <b>Manipulation and analysis</b> are today.</p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
