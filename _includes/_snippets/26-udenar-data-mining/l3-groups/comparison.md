<!-- SLIDES: -->
<!-- 2 Nov 2026: the visible note "Numbers: box run on rebuilt data." was removed from these slides (critic brief r1, S4). The source notes stay in these comments. -->
<!-- Numbers: from the executed L3 notebook, which runs exactly the slide code, as listed in box-run/week-2/W2-L3-L4-VALUES.md (30 Oct 2026, about 04:35). Source map in week-2-round-2-por-confirmar.txt. Not from box-run/week2_groups.py, RESULTS.md section 3 or the critic's provisional table. The visible footer was removed on 2 Nov 2026. -->

## Comparing the Methods

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 48%">
                <p><b>The nutrition papers</b></p>
                <ul style="font-size: 0.85em">
                    <li>317 papers, 317 x 869 word counts, floor of 10 papers</li>
                    <li>k-means silhouette, k from 3 to 8: 0.061, 0.058, 0.062, 0.065, 0.065, 0.075</li>
                    <li>Here k = 8, the highest silhouette. Stability and agreement use it</li>
                    <li>Shuffled baseline, 95th percentile at k = 8: 0.054</li>
                    <li>Seed ARI, all 10 pairs, worst and mean: 0.32 and 0.45</li>
                    <li>Mixture K by BIC, share unsure: K = 4, 9 papers (2.8%)</li>
                    <li>HDBSCAN groups, largest, noise: 5 groups, largest 87, noise 108 (34%). Without SVD: 2 groups, 40% noise</li>
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
                <p>The floor of 10 is the same as for a pattern in Lecture 2, and it is the smallest HDBSCAN group. HDBSCAN pairs use only the papers it puts in a group. Not a contest.</p>
            </div>
        </div>
    </div>
</div>

## Comparing the Methods

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p><b>Weak structure in every extract</b></p>
                <table class="table" style="font-size: 0.5em">
                    <thead>
                        <tr><th>Extract</th><th>k-means silhouette</th><th>Shuffled p95</th><th>Seed ARI, mean of 10 pairs</th><th>HDBSCAN groups</th><th>Noise</th></tr>
                    </thead>
                    <tbody>
                        <tr><td>Nutrition papers</td><td>0.075 (k = 8)</td><td>0.054</td><td>0.45</td><td>5</td><td>34%</td></tr>
                        <tr><td>Pobreza</td><td>0.123 (k = 8)</td><td>0.094</td><td>0.49</td><td>10</td><td>29%</td></tr>
                        <tr><td>Vivienda</td><td>0.121 (k = 8)</td><td>0.082</td><td>0.57</td><td>7</td><td>35%</td></tr>
                        <tr><td>Medio ambiente</td><td>0.063 (k = 7)</td><td>0.046</td><td>0.38</td><td>6</td><td>52%</td></tr>
                        <tr><td>Agricultura</td><td>0.055 (k = 7)</td><td>0.053</td><td>0.37</td><td>5</td><td>45%</td></tr>
                        <tr><td>Salud mental</td><td>0.087 (k = 8)</td><td>0.070</td><td>0.49</td><td>5</td><td>46%</td></tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>

## Comparing the Methods

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Weak structure in every extract</b></p>
                <ul>
                    <li>Silhouette across the extracts: 0.032 to 0.123 over every k from 3 to 8, and 0.055 to 0.123 at the chosen k</li>
                    <li>Every extract is above its shuffled baseline, by 0.002 to 0.039. Agricultura only just: 0.055 against 0.053</li>
                    <li>Share of items HDBSCAN leaves as noise: 29% to 52% with SVD, 40% to 100% without</li>
                    <li>Weakest extract: agricultura. Its three method pairs agree at ARI 0.22, 0.23 and 0.25</li>
                    <li>Weak structure is a finding. One result alone is weak, so we combine results</li>
                </ul>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
