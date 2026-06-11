<!-- SLIDES: -->

## Read VS Write

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Two opposite jobs</b></p>
                <ul>
                    <li><b>OLTP:</b> many small writes, read whole records, one at a time</li>
                    <li><b>OLAP:</b> few big reads, scan one column over millions of rows</li>
                </ul>
                <p>Our GEIH question is OLAP. We ask for employment by department, not for one person's full record.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>The layout that is fast to write a row is slow to scan a column, and the reverse.</p>
            </div>
        </div>
    </div>
</div>

## Read VS Write

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/row-vs-columnar.svg" alt="Row versus columnar storage layout" style="height: 460px">
            </div>
        </div>
    </div>
</div>

## Read VS Write

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Why columns compress so well</b></p>
                <ul>
                    <li>Values in one column share a type and look alike</li>
                    <li><b>Dictionary encoding:</b> store each distinct value once, then small codes</li>
                    <li><b>Run-length encoding:</b> store a repeated value as value times count</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>A <b>sexo</b> column of millions of 1s and 2s collapses to almost nothing. Smaller bytes mean faster reads and cheaper storage.</p>
            </div>
        </div>
    </div>
</div>

## Read VS Write

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Parquet</b> is the columnar format we will use. Before we store, we still have to turn two messy CSV tables into one clean table. That step has a name, and it is part of a bigger idea.</p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
