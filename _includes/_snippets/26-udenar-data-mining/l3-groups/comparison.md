<!-- SLIDES: -->

## The Question and the Data

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p><b>Our question:</b> which groups of nutrition papers would a new colleague read?</p>
            </div>
        </div>
    </div>
</div>

## The Question and the Data

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 48%">
                <p><b>The nutrition papers</b></p>
                <ul>
                    <li>317 papers and a floor of 10 papers</li>
                    <li>k-means at k = 8: silhouette 0.075, shuffled baseline 0.054</li>
                    <li>HDBSCAN: 5 groups and 108 noise papers (34%)</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 52%">
                <p><b>Agreement between methods (ARI)</b></p>
                <table class="table" style="font-size: 0.8em">
                    <thead>
                        <tr><th>Pair of methods</th><th>ARI</th></tr>
                    </thead>
                    <tbody>
                        <tr><td>k-means and mixture</td><td>0.29</td></tr>
                        <tr><td>k-means and HDBSCAN</td><td>0.49</td></tr>
                        <tr><td>Mixture and HDBSCAN</td><td>0.70</td></tr>
                    </tbody>
                </table>
                <p>Every extract is weakly structured. Weak structure is a finding.</p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
