<!-- SLIDES: -->

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p><b>Evaluation</b> compares support, lift, and closeness on the same transactions.</p>
            </div>
        </div>
    </div>
</div>

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>The same pairs</b></p>
                <p>Kept means the method places the pair above its own cutoff.</p>
                <table class="table">
                    <thead>
                        <tr><th>Pair</th><th>Support</th><th>Lift</th><th>Closeness</th></tr>
                    </thead>
                    <tbody>
                        <tr><td>A, B</td><td>kept</td><td>kept</td><td>kept</td></tr>
                        <tr><td>C, D</td><td>kept</td><td>kept</td><td>no</td></tr>
                        <tr><td>E, F</td><td>no</td><td>no</td><td>kept</td></tr>
                    </tbody>
                </table>
                <ul>
                    <li><b>All three:</b> A and B are a stronger candidate.</li>
                    <li><b>Counts only:</b> C and D repeat in these transactions.</li>
                    <li><b>Closeness only:</b> E and F are used alike elsewhere.</li>
                </ul>
                <p>A pair that only one method keeps is not a winner.</p>
            </div>
        </div>
    </div>
</div>

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p>The individual notebook runs this comparison on 317 papers abstracts in the nutrition domain. Each abstract is one bag of words.</p>
                <img src="{{ site.url }}/assets/media/images/pattern-methods-panels.png" alt="Three pairs under papers, lift, and cosine" style="width: 100%; height: auto">
                <p>Lift is read only after the support floor. The floor here is 10 papers. A missing lift bar means the pair is below that floor.</p>
            </div>
        </div>
    </div>
</div>

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>The same three readings</b></p>
                <ul>
                    <li><b>All three:</b> diabetes + obesity is a stronger candidate.</li>
                    <li><b>Counts only:</b> health + years repeats in these abstracts.</li>
                    <li><b>Closeness only:</b> food + nutrition are used alike elsewhere. Nine papers are below the floor.</li>
                </ul>
                <p>A pair that only one method keeps is not a winner.</p>
            </div>
        </div>
    </div>
</div>

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 42%">
                <p><b>One pair against the swap</b></p>
                <p>The orange line is the 95th percentile of the swap counts, 80.</p>
                <p>The blue line is the real count, 84.</p>
                <p>The pair stays because the real count is to the right of the cutoff.</p>
                <p>Cosine stays when it is strictly above the random-pair 95th percentile, 0.46.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 58%">
                <img src="{{ site.url }}/assets/media/images/pattern-null-disease-health.png" alt="Swap counts for disease and health" style="width: 100%; height: auto">
            </div>
        </div>
    </div>
</div>

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 42%">
                <p><b>Pairs that pass by luck</b></p>
                <p>814 of the 16,271 pairs at the floor would pass by luck.</p>
                <p>The swap kept 7,311.</p>
                <p>A pass is worth a look.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 58%">
                <img src="{{ site.url }}/assets/media/images/pattern-luck-counts.png" alt="Pairs that would pass by luck against pairs the swap kept" style="width: 100%; height: auto">
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
