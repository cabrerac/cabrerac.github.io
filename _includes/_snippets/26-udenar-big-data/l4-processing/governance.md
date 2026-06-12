<!-- SLIDES: -->

## Governance at Query Time

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p>Aggregating by department is safe: each cell holds thousands of people. But <b>finer</b> results leak. A table of <b>dpto x edad</b> can leave cells with just a few people, and those few can be re-identified.</p>
            </div>
        </div>
    </div>
</div>

## Governance at Query Time

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>k = 5 suppression</b></p>
                <ul>
                    <li>From lecture 2: hide any cell with fewer than k people</li>
                    <li>Simple, easy to explain to a data owner</li>
                    <li>Cost: small cells disappear, we lose fine detail</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Differential privacy</b></p>
                <ul>
                    <li>From lecture 3: publish every cell, but add calibrated noise</li>
                    <li>A guarantee that no single person changes the result much</li>
                    <li>Cost: every number is slightly wrong, tuned by epsilon</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Governance at Query Time

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Suppression VS noise</b> is a real choice, not a default. Hide the small cells, or keep them all but blur every count. Your group decides which fits the project, and writes down why.</p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
