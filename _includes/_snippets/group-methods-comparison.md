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
                        <tr><td>k-means</td><td>Round groups of similar size</td><td>Items between groups, and noise</td></tr>
                        <tr><td>Gaussian mixture</td><td>Long or tilted groups, and how sure each item is</td><td>Groups in many dimensions, without reduction</td></tr>
                        <tr><td>HDBSCAN</td><td>Dense regions of any shape, and noise</td><td>Groups thinner than the rest</td></tr>
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
                    <li>Run every method on the same items</li>
                    <li>Look at the groups of each method side by side, with their top attributes</li>
                    <li>Look for items where the methods disagree, and read them</li>
                    <li>An item that all methods group together is a stronger candidate</li>
                    <li>Disagreement is not a winner. Each method sees something the others miss</li>
                </ul>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
