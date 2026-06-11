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
                <p>We will store GEIH in <b>Parquet</b>, the open descendant of this lineage. Getting messy sources into that format is an <b>ETL</b> job — extract, transform, load.</p>
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
                <img src="{{ site.url }}/assets/media/diagrams/etl-vs-elt.svg" alt="ETL versus ELT" style="height: 100%">
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

## Partitioning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/partition-tree.svg" alt="Partition tree by key" style="height: 420px">
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Split the dataset by a key</b></p>
                <ul>
                    <li>Store each slice in its own folder named key=value</li>
                    <li>For GEIH we split by <b>year</b> and <b>month</b></li>
                    <li>The folder name is data, not just a label</li>
                </ul>
                <p>A query for one month reads only that folder and skips the rest. This is called <b>partition pruning</b>.</p>
            </div>
        </div>
    </div>
</div>

## Partitioning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/partition-tree.svg" alt="Hive-style partition tree" style="height: 460px">
            </div>
        </div>
    </div>
</div>

## Partitioning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 40%">
                <p><b>In the notebook</b></p>
                <ul>
                    <li>One file per month under year and month</li>
                    <li>Written once, read many times</li>
                    <li><a href="https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-big-data/l3-storage.ipynb" target="_blank" rel="noopener noreferrer">Lecture 3 notebook</a></li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 60%">

```python
part_dir = PROCESSED_DIR / f"year={y}" / f"month={m:02d}"
part_file = part_dir / "part-000.parquet"

part_dir.mkdir(parents=True, exist_ok=True)
sample.to_parquet(part_file, index=False)
```

</div>
        </div>
    </div>
</div>

## Harmonisation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 50%">
                <table class="table">
                    <tr><td><b>raw code</b></td><td><b>readable</b></td></tr>
                    <tr><td>P6040</td><td>age</td></tr>
                    <tr><td>P3271</td><td>gender</td></tr>
                    <tr><td>P6240</td><td>activity</td></tr>
                    <tr><td>FEX_C18</td><td>factor_expansion</td></tr>
                </table>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Make the data comparable and readable</b></p>
                <ul>
                    <li>Join the labour and demographics tables per person</li>
                    <li>Rename source codes to readable names</li>
                    <li>Fix types, text to numbers where needed</li>
                    <li>Derive the partition keys, year and month</li>
                </ul>
                <p>The goal is a clean table that any teammate can read without the source codebook open.</p>
            </div>
        </div>
    </div>
</div>

## Harmonisation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 50%">
                <p><b>DANE code</b></p>
                <table class="table">
                    <tr><td>P6040</td><td>age</td></tr>
                    <tr><td>P3271</td><td>gender</td></tr>
                    <tr><td>P6240</td><td>activity</td></tr>
                    <tr><td>FEX_C18</td><td>factor_expansion</td></tr>
                </table>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Readable name</b></p>
                <p>The same value, now with a name a person understands. We keep <b>actividad</b> as the raw code and interpret it later, during processing.</p>
            </div>
        </div>
    </div>
</div>

## Lakehouse

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/lake-warehouse-lakehouse.svg" alt="Data lake, warehouse, and lakehouse" style="height: 100%">
            </div>
        </div>
    </div>
</div>

## Lakehouse

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p>"A lakehouse is a data management system based on low-cost and directly accessible storage that also provides traditional analytical DBMS management features." <a href="https://www.cidrdb.org/cidr2021/papers/cidr2021_paper17.pdf" target="_blank" rel="noopener noreferrer">(Armbrust et al., 2021)</a></p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
