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

<!-- end SLIDES: -->
