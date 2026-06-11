<!-- SLIDES: -->

## Non-Relational Databases

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>When tables stop fitting</b></p>
                <ul>
                    <li>Social and web data is huge, sparse, and changes shape</li>
                    <li>One global table on one machine cannot keep up</li>
                    <li>NoSQL stores relax the strict relational model to scale out</li>
                </ul>
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
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>Each family optimises for a shape of data and a pattern of access. None is a universal replacement for the others.</p>
            </div>
        </div>
    </div>
</div>

## Non-Relational Databases

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>The CAP trade-off</b></p>
                <p>A distributed store cannot fully guarantee all three at once.</p>
                <ul>
                    <li><b>Consistency:</b> every read sees the latest write</li>
                    <li><b>Availability:</b> every request gets an answer</li>
                    <li><b>Partition tolerance:</b> it survives a broken network</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>When the network can split, you must choose between consistency and availability. <a href="https://doi.org/10.1145/564585.564601" target="_blank" rel="noopener noreferrer">(Gilbert &amp; Lynch, 2002)</a></p>
                <p>Banks lean to consistency. A social feed leans to availability.</p>
            </div>
        </div>
    </div>
</div>

## Non-Relational Databases

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p>Relational or not, every store makes one core bet about <b>reading versus writing</b>. That bet is what decides the format we use for GEIH.</p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
