<!-- SLIDES: -->

## Lakehouse

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Two earlier answers</b></p>
                <ul>
                    <li><b>Data lake:</b> dump raw files cheaply, decide structure later</li>
                    <li><b>Warehouse:</b> model clean tables first, query them fast</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>The lake is flexible but easy to turn into a swamp. The warehouse is reliable but rigid and costly to change.</p>
            </div>
        </div>
    </div>
</div>

## Lakehouse

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/lake-warehouse-lakehouse.svg" alt="Data lake, warehouse, and lakehouse" style="height: 440px">
            </div>
        </div>
    </div>
</div>

## Lakehouse

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>A table format on top of files</b></p>
                <ul>
                    <li>Keep Parquet files in cheap storage</li>
                    <li>Add a layer that gives transactions and versions</li>
                    <li>Delta Lake, Apache Iceberg, and Apache Hudi do this</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>"A lakehouse is a data management system based on low-cost and directly accessible storage that also provides traditional analytical DBMS management features." <a href="https://www.cidrdb.org/cidr2021/papers/cidr2021_paper17.pdf" target="_blank" rel="noopener noreferrer">(Armbrust et al., 2021)</a></p>
            </div>
        </div>
    </div>
</div>

## Lakehouse

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p>Our partitioned Parquet tree is a small lakehouse. In lecture 4 we point engines like <b>DuckDB</b> straight at these files and query them with SQL, no warehouse server required.</p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
