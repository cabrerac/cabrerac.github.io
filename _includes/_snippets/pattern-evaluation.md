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
    <div class="row" style="height: 80%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <img src="{{ site.url }}/assets/media/images/pattern-methods-panels.png" alt="Three pairs under papers, lift, and cosine" style="width: 100%; height: auto">
            </div>
        </div>
    </div>
    <div class="row" style="height: 20%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p>The individual notebook runs this comparison on 317 papers abstracts in the nutrition domain. Each abstract is one bag of words.</p>
                <p>Support stays above the 95th percentile of the chance copies, and cosine stays above the 95th percentile of random pairs.</p>
            </div>
        </div>
    </div>
</div>

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 80%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <img src="{{ site.url }}/assets/media/images/pattern-methods-panels.png" alt="Three pairs under papers, lift, and cosine" style="width: 100%; height: auto">
            </div>
        </div>
    </div>
    <div class="row" style="height: 20%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
               <p><b>All three:</b> diabetes + obesity is a stronger candidate.</p>
               <p><b>Counts only:</b> health + years repeats in these abstracts.</p>
               <p><b>Closeness only:</b> food + nutrition are used alike elsewhere.</p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
