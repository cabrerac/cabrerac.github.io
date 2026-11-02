<!-- SLIDES: -->
<!-- 2 Nov 2026: the visible note "Numbers: box run on rebuilt data." was removed from these slides (critic brief r1, S4). The source notes stay in these comments. -->

<!-- Numbers: slide code on rebuilt data, box run (week-3/feasibility/r3/w3decks_n2v_pagerank.json, critic l5_slide_code.json, sorted(adj)). Round 4: the three former box-run markers filled from the notebooks maker's box run (sorted(adj), seeds 7 to 9, workers=1, betweenness rounded to 9 dp). -->

## The Papers as a Graph

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>From the links column</b></p>
                <ul>
                    <li>320 rows, 2 duplicate titles dropped: 318 papers</li>
                    <li>453 directed links inside the set, 441 undirected edges</li>
                    <li>122 papers are isolated (38%)</li>
                    <li>22 components with more than one paper, the largest has 148 (47%)</li>
                    <li>Mean degree 2.77</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>What that means</b></p>
                <p>The top paper, a Global Burden of Disease paper, links to 8% of the others, so no hub.</p>
                <p>The hub rule never flags fewer than 5 links, the minimum of the Lecture 2 support floor. The 10% share decides it in every set.</p>
            </div>
        </div>
    </div>
</div>

## The Wikipedia Extracts as Graphs

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 66%">
                <table class="table" style="font-size: 0.62em">
                    <thead>
                        <tr><th>Extract</th><th>Nodes</th><th>Edges</th><th>Isolated</th><th>Largest</th><th>Top node, share</th><th>Hubs</th></tr>
                    </thead>
                    <tbody>
                        <tr><td>Pobreza</td><td>298</td><td>515</td><td>23%</td><td>230 (77%)</td><td>Pobreza, 22%</td><td>2</td></tr>
                        <tr><td>Vivienda</td><td>324</td><td>457</td><td>27%</td><td>224 (69%)</td><td>Vivienda, 17%</td><td>1</td></tr>
                        <tr><td>Medio ambiente</td><td>335</td><td>685</td><td>25%</td><td>241 (72%)</td><td>Medio ambiente natural, 14%</td><td>3</td></tr>
                        <tr><td>Agricultura</td><td>315</td><td>547</td><td>25%</td><td>231 (73%)</td><td>Agricultura, 30%</td><td>3</td></tr>
                        <tr><td>Salud mental</td><td>332</td><td>828</td><td>14%</td><td>275 (83%)</td><td>Psiquiatría, 27%</td><td>9</td></tr>
                    </tbody>
                </table>
            </div>
            <div class="column vertical-middle text-left" style="width: 34%">
                <p>Fewer isolated items than the papers, 14% to 27%.</p>
                <p>In every extract the top article links to 14% to 30% of the others.</p>
                <p>Read the other articles with and without the hubs.</p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
