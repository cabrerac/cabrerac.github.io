<!-- SLIDES: -->

## Big Data Storage History

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>One web, too much data for one machine</b></p>
                <p>By the early 2000s a single server could not hold or serve the web. Google had to store and index the whole internet, so it built its own stack.</p>
            </div>
        </div>
    </div>
</div>

## Big Data Storage History

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Google File System (2003)</b></p>
                <ul>
                    <li>Spread one huge file across many cheap machines</li>
                    <li>Replicate blocks so failure is normal, not fatal</li>
                    <li>Optimised for large streaming reads, not tiny edits</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>"Component failures are the norm rather than the exception." <a href="https://doi.org/10.1145/945445.945450" target="_blank" rel="noopener noreferrer">(Ghemawat et al., 2003)</a></p>
                <p>The open-source version of this idea became <b>Hadoop HDFS</b>.</p>
            </div>
        </div>
    </div>
</div>

## Big Data Storage History

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Bigtable (2006)</b></p>
                <ul>
                    <li>A distributed table for billions of rows</li>
                    <li>Sparse, wide, and sorted by key</li>
                    <li>Inspired Cassandra and HBase</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>"A Bigtable is a sparse, distributed, persistent multidimensional sorted map." <a href="https://dl.acm.org/doi/10.1145/1365815.1365816" target="_blank" rel="noopener noreferrer">(Chang et al., 2008)</a></p>
            </div>
        </div>
    </div>
</div>

## Big Data Storage History

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Dremel (2010) leads to Parquet</b></p>
                <ul>
                    <li>Columnar storage for fast analytics at web scale</li>
                    <li>Scan a few columns over trillions of rows in seconds</li>
                    <li>Its column format inspired <b>Apache Parquet</b>, our format</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>"Dremel is a scalable, interactive ad-hoc query system for analysis of read-only nested data." <a href="https://doi.org/10.14778/1920841.1920886" target="_blank" rel="noopener noreferrer">(Melnik et al., 2010)</a></p>
            </div>
        </div>
    </div>
</div>

## Big Data Storage History

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p>We will store GEIH in <b>Parquet</b>, the open descendant of this lineage. Two more ideas make it fast and clean, <b>partitioning</b> and <b>harmonization</b>.</p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
