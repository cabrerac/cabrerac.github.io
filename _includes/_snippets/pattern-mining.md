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

# The Data

## The Data

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 55%">
                <p><b>A set of transactions</b></p>
                <p>The data is many transactions over one shared pool of items.</p>
                <ul>
                    <li><b>Transaction:</b> one record, the items that occurred together</li>
                    <li><b>Item:</b> a member of that pool, present or absent in a transaction</li>
                    <li><b>Co-occurrence:</b> two items co-occur when one transaction contains both</li>
                </ul>
                <p>A repeated item inside one transaction counts once. A pattern is a set that co-occurs in many transactions.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 45%">
                <p><b>Examples</b></p>
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
            </div>
        </div>
    </div>
</div>

# Modeling

## Methods

<div class="rows" style="height: 100%">
    <div class="row" style="height: 70%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img class="external-svg" src="{{ site.url }}/assets/media/diagrams/pattern-task-taxonomy.svg" alt="Taxonomy of pattern methods" style="width: 100%; height: 100%">
            </div>
        </div>
    </div>
    <div class="row" style="height: 30%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <p><b>Frequent itemsets:</b> support count, FP-growth, and Eclat.</p>
                <p><b>Interestingness:</b> lift, confidence, and conviction.</p>
                <p><b>Sequential patterns:</b> GSP, PrefixSpan, and SPADE.</p>
                <p><b>Item vectors:</b> one vector per item in a learned space, so items used alike lie close.</p>
            </div>
        </div>
    </div>
</div>

## Methods

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>FP-growth</b> finds the sets from a compressed tree of the transactions.</p>
                <p><b>Eclat</b> finds them by intersecting each item's list of transactions.</p>
                <p><b>Confidence</b> is the share of the first item's transactions that also hold the second.</p>
                <p><b>Conviction</b> is high when the first item rarely appears without the second, more rarely than chance.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>GSP</b> builds candidate sequences.</p>
                <p><b>PrefixSpan</b> grows a sequence from its prefix.</p>
                <p><b>SPADE</b> intersects lists of sequence ids.</p>
                <p>These names place the three methods we use today.</p>
            </div>
        </div>
    </div>
</div>

## Methods

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <ul>
                    <li><b>Support:</b> a count inside this collection.</li>
                    <li><b>Lift:</b> that count against what chance would give</li>
                    <li><b>Item-vector closeness:</b> a score learned outside this collection</li>
                </ul>
                <p>These apply to different data sources (e.g., products, codes, words, etc).</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/supermarket-checkout.jpg" alt="Supermarket checkout" style="height: 400px">
                <div class="footnote">Supermarket checkout Tegut Tauberbischofsheim - Triplec85, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
