<!-- SLIDES: -->

## Relational Databases

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 50%">
                <table class="table">
                    <tr><td>id_hogar</td><td>orden</td><td>edad</td></tr>
                    <tr><td>A-1</td><td>1</td><td>40</td></tr>
                    <tr><td>A-1</td><td>2</td><td>12</td></tr>
                    <tr><td>B-3</td><td>1</td><td>29</td></tr>
                </table>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Rows, tables, and keys</b></p>
                <ul>
                    <li>Data lives in tables of rows and typed columns</li>
                    <li>Tables link through keys, no value is repeated needlessly</li>
                    <li>We query with <b>SQL</b>, a declarative language</li>
                </ul>
                <p>As an example, GEIH is relational in spirit. A household table and a person table share the keys <b>DIRECTORIO</b>, <b>HOGAR</b>, and <b>ORDEN</b>.</p>
            </div>
        </div>
    </div>
</div>

## Relational Databases

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 50%">
                <p><b>Labour table</b></p>
                <table class="table">
                    <tr><td>id_hogar</td><td>orden</td><td>actividad</td></tr>
                    <tr><td>A-1</td><td>1</td><td>1</td></tr>
                    <tr><td>A-1</td><td>2</td><td>2</td></tr>
                </table>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <p><b>Demographics table</b></p>
                <table class="table">
                    <tr><td>id_hogar</td><td>orden</td><td>edad</td></tr>
                    <tr><td>A-1</td><td>1</td><td>40</td></tr>
                    <tr><td>A-1</td><td>2</td><td>12</td></tr>
                </table>
            </div>
        </div>
    </div>
</div>

## Relational Databases

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Why institutions trusted them: ACID</b></p>
                <ul>
                    <li><b>Atomicity:</b> a transaction happens fully or not at all</li>
                    <li><b>Consistency:</b> the data always satisfies its rules</li>
                    <li><b>Isolation:</b> concurrent users do not corrupt each other</li>
                    <li><b>Durability:</b> a committed change survives a crash</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>This is the world of <b>OLTP</b>, online transaction processing. Many small reads and writes that must never lose money or break a rule.</p>
            </div>
        </div>
    </div>
</div>

## Relational Databases

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p>Relational systems are excellent when data is structured and consistency is sacred. The web then produced data that did not fit neat tables, and that broke some of these assumptions.</p>
            </div>
        </div>
    </div>
</div>

## Non-Relational Databases

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>When tables stop fitting</b></p>
                <ul>
                    <li>Social and web data is huge, sparse, and changes shape</li>
                    <li>One global table on one machine cannot keep up</li>
                    <li>NoSQL stores relax the strict relational model to scale out</li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/nosql-families.svg" alt="Non-relational database families" style="height: 420px">
            </div>
        </div>
    </div>
</div>

## Non-Relational Databases

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Four common families</b></p>
                <ul>
                    <li><b>Key-value:</b> a giant dictionary, fast lookups (Redis, DynamoDB)</li>
                    <li><b>Document:</b> nested JSON per record (MongoDB)</li>
                    <li><b>Column-family:</b> wide sparse rows at scale (Cassandra, HBase)</li>
                    <li><b>Graph:</b> nodes and edges for relationships (Neo4j)</li>
                </ul>
                <p>Each family optimises for a shape of data and a pattern of access. None is a universal replacement for the others.</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/nosql-families.svg" alt="Non-relational database families" style="height: 420px">
            </div>
        </div>
    </div>
</div>

## Non-Relational Databases

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/decentralised-deployment.png" alt="Distributed, decentralised storage" style="height: 420px">
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>The CAP trade-off</b></p>
                <p>Once data is spread across many machines, a store cannot fully guarantee all three at once.</p>
                <ul>
                    <li><b>Consistency:</b> every read sees the latest write</li>
                    <li><b>Availability:</b> every request gets an answer</li>
                    <li><b>Partition tolerance:</b> it survives a broken network</li>
                </ul>
                <p>When the network can split, you must choose between consistency and availability. <a href="https://doi.org/10.1145/564585.564601" target="_blank" rel="noopener noreferrer">(Gilbert &amp; Lynch, 2002)</a> Banks lean to consistency; a social feed leans to availability.</p>
            </div>
        </div>
    </div>
</div>

## Non-Relational Databases

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p>Relational or not, every store makes one core bet about <b>read VS write</b>. That bet is what decides the format we use for GEIH.</p>
            </div>
        </div>
    </div>
</div>

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
                <img src="{{ site.url }}/assets/media/diagrams/row-vs-columnar.svg" alt="Row versus columnar storage layout" style="height: 640px">
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
                <p>A <b>gender</b> column of millions of 1s and 2s collapses to almost nothing. Smaller bytes mean faster reads and cheaper storage.</p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
