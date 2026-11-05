<!-- SLIDES: -->

## The Task

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Repeating sets</b></p>
                <p>Which sets of items repeat together more often than chance?</p>
                <ul>
                    <li>Each record is a transaction, a set of items</li>
                    <li>A pattern is a set found in many transactions</li>
                </ul>
                <br>
                <p>"We are given a large database of customer transactions. Each transaction consists of items purchased by a customer in a visit." <a href="https://doi.org/10.1145/170036.170072" target="_blank" rel="noopener noreferrer">(Agrawal et al., 1993)</a></p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/supermarket-checkout.jpg" alt="Supermarket checkout" style="height: 400px">
                <div class="footnote">Supermarket checkout Tegut Tauberbischofsheim - Triplec85, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## The Task

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>What counts as a pattern</b></p>
                <p>One standout transaction is not a pattern.</p>
                <ul>
                    <li>A pair seen in one or two transactions can be luck</li>
                    <li>A pattern needs a minimum number of transactions, set before the results</li>
                    <li>It also needs to beat what chance would give</li>
                </ul>
                <br>
                <p>A <b>pattern</b> is a set of items that appear together in many transactions, more often than chance would give.</p>
            </div>
        </div>
    </div>
</div>

## Data for this Task

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Transactions that can feed the task</b></p>
                <table class="table">
                    <thead>
                        <tr><th>Data</th><th>One transaction</th><th>Items</th></tr>
                    </thead>
                    <tbody>
                        <tr><td>Receipts</td><td>one basket</td><td>products</td></tr>
                        <tr><td>Events</td><td>one visit or one session</td><td>codes</td></tr>
                        <tr><td>Texts</td><td>one text</td><td>its distinct words</td></tr>
                    </tbody>
                </table>
                <p>A transaction is a set of items. A repeated item counts once.</p>
            </div>
        </div>
    </div>
</div>

## Methods

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img class="external-svg" src="{{ site.url }}/assets/media/diagrams/pattern-task-taxonomy.svg" alt="Taxonomy of pattern methods" style="width: 100%; height: 460px">
            </div>
        </div>
    </div>
</div>

## Methods

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>The three methods</b></p>
                <ul>
                    <li><b>Support:</b> a count inside this collection. You write this count</li>
                    <li><b>Lift:</b> that count against what chance would give</li>
                    <li><b>Item-vector closeness:</b> a score learned outside this collection</li>
                </ul>
                <p>The same three apply to products, to codes, and to words.</p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
