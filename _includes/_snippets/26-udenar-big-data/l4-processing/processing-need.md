<!-- SLIDES: -->

## The Need to Process

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p><b>Stored data answers nothing on its own. What do we want to know?</b></p>
            </div>
        </div>
    </div>
</div>

## The Need to Process

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Processing is its own stage</b></p>
                <ul>
                    <li><b>Filter:</b> keep only the rows that matter</li>
                    <li><b>Aggregate:</b> count, sum, and average over groups</li>
                    <li><b>Derive:</b> compute new facts the raw data did not state</li>
                </ul>
                <p>As an example, the lakehouse stores <b>actividad</b> as a raw code. Deciding who counts as <b>employed</b> happens here, when we process.</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/big-data-pipeline-template.svg" alt="Pipeline template, process stage" style="height: 380px">
            </div>
        </div>
    </div>
</div>

## The Need to Process

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/warehouse-olap.svg" alt="Operational systems to data warehouse to analytics" style="height: 360px">
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Early processing: from records to reports</b></p>
                <ul>
                    <li>First systems just recorded transactions, one at a time</li>
                    <li>Managers wanted summaries, not single records</li>
                    <li>So data was copied into a separate place to analyse</li>
                </ul>
                <p>Reading for analysis is a different job from writing transactions. That split is what created processing as a stage.</p>
            </div>
        </div>
    </div>
</div>

## The Need to Process

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/warehouse-olap.svg" alt="Operational systems to data warehouse to analytics" style="height: 360px">
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Data warehouses and history</b></p>
                <ul>
                    <li>A <b>warehouse</b> integrates clean data from many systems</li>
                    <li>It keeps <b>years of history</b>, organised by time</li>
                    <li>This is <b>OLAP</b>: few big reads that scan and group</li>
                </ul>
                <p>Keeping history is what made analysis possible. You cannot study a trend you did not store.</p>
            </div>
        </div>
    </div>
</div>

## The Need to Process

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>The web breaks the single machine</b></p>
                <ul>
                    <li>Web 2.0 and 3.0 produced endless, messy <b>streams</b></li>
                    <li>Clicks, text, maps, and sensors, not neat tables</li>
                    <li>Too much data to process on one computer</li>
                </ul>
                <p>The same variety that changed storage now changes <b>compute</b>. One machine can no longer scan it all.</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/decentralised-deployment.png" alt="Distributed, decentralised compute" style="height: 400px">
            </div>
        </div>
    </div>
</div>

## The Need to Process

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p>The answer was to <b>spread the work across many machines</b>. The first widely used recipe for that gave big data its mental model, <b>MapReduce</b>.</p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
