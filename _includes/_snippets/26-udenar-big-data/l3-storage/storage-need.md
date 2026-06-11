<!-- SLIDES: -->

## The Need to Store

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p><b>Where does the data live after the program ends?</b></p>
            </div>
        </div>
    </div>
</div>

## The Need to Store

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Raw files pile up fast</b></p>
                <ul>
                    <li>One data file per period, hundreds of MB each (for GEIH, one ZIP per month)</li>
                    <li>Several tables to join on every run</li>
                    <li>Related sources to keep side by side</li>
                </ul>
                <p>Reading and joining raw files on every run is slow, fragile, and hard to share with a teammate.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/data-quality.jpg" alt="Data quality and usability" style="height: 400px">
            </div>
        </div>
    </div>
</div>

## The Need to Store

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Storage is its own stage of the pipeline</b></p>
                <ul>
                    <li><b>Durability:</b> data outlives the notebook session</li>
                    <li><b>Shareability:</b> a team reads the same clean dataset</li>
                    <li><b>Scale:</b> read one month without loading the whole year</li>
                    <li><b>Cost:</b> compressed bytes are cheaper to keep and move</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/big-data-pipeline-template.svg" alt="Pipeline template, store stage" style="height: 380px">
            </div>
        </div>
    </div>
</div>

## The Need to Store

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p>How we store data has changed with every era of computing. The right choice depends on <b>who writes, who reads, and what they ask</b>. To understand today's formats, we follow the history that produced them.</p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
