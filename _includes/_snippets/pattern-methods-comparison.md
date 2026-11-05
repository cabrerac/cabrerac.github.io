<!-- SLIDES: -->

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>What each method sees</b></p>
                <table class="table">
                    <thead>
                        <tr><th>Method</th><th>Sees</th><th>Misses</th></tr>
                    </thead>
                    <tbody>
                        <tr><td>Support</td><td>Pairs in many transactions</td><td>Chance meetings of common items</td></tr>
                        <tr><td>Lift</td><td>Pairs above chance</td><td>Very rare pairs, without a floor</td></tr>
                        <tr><td>Item-vector closeness</td><td>Items used alike elsewhere</td><td>What happens in this collection</td></tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>How to compare them</b></p>
                <ul>
                    <li>Run every method on the same transactions</li>
                    <li>Look at the top pairs of each method side by side</li>
                    <li>Look for pairs where the methods disagree, and read the transactions behind them</li>
                    <li>A pair that all methods keep is a stronger candidate</li>
                    <li>Disagreement is not a winner. Each method sees something the others miss</li>
                </ul>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
