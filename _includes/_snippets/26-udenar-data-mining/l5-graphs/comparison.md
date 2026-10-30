<!-- SLIDES: -->

<!-- Numbers: slide code on rebuilt data, box run (week-3/feasibility/r3/w3decks_n2v_pagerank.json, critic l5_slide_code.json, sorted(adj)). Round 4: the three former box-run markers filled from the notebooks maker's box run (sorted(adj), seeds 7 to 9, workers=1, betweenness rounded to 9 dp). -->

## Comparing the Methods

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>PageRank against degree, the papers</b></p>
                <ul>
                    <li>Top by PageRank: a GBD risk paper (0.033), 10.5 times 1/318</li>
                    <li>Spearman with total degree 0.75, with in-degree 0.97</li>
                    <li>High PageRank, not top 10 by degree: Obesity in children and young people (degree 6), Trends in adult body-mass index (7), Interventions for preventing obesity in children (8)</li>
                    <li>The lowest degree in the top 10 by degree is 14</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Against citations</b></p>
                <ul>
                    <li>Spearman of PageRank with the citation count: 0.30</li>
                    <li>Citations count the whole literature, PageRank only this set</li>
                    <li>Not a contest. Each method reads a different place</li>
                    <li>A paper high in betweenness and low by citations: Guidelines for the Primary Prevention of Stroke, 10th by betweenness and 187th by citations, with degree 10 and 48th by PageRank</li>
                </ul>
                <div class="footnote">Numbers: box run on rebuilt data.</div>
            </div>
        </div>
    </div>
</div>

## Comparing the Methods

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 55%">
                <p><b>High PageRank, low degree, in the Wikipedia extracts</b></p>
                <table class="table" style="font-size: 0.8em">
                    <thead>
                        <tr><th>Extract</th><th>Article</th><th>Degree</th></tr>
                    </thead>
                    <tbody>
                        <tr><td>Salud mental</td><td>Medicina psicosomática</td><td>3</td></tr>
                        <tr><td>Agricultura</td><td>Abono verde</td><td>6</td></tr>
                    </tbody>
                </table>
                <ul>
                    <li>Spearman of PageRank with in-degree 0.96 to 0.98, with total degree 0.61 to 0.74</li>
                    <li>Few links, but from well placed articles</li>
                    <li>The top article by degree also tops PageRank in all five, Psiquiatría in salud mental</li>
                </ul>
                <div class="footnote">Numbers: box run on rebuilt data.</div>
            </div>
            <div class="column vertical-middle text-left" style="width: 45%">
                <p><b>A rank sink: Fannie Mae + Freddie Mac</b></p>
                <ul>
                    <li>In vivienda, Fannie Mae + Freddie Mac link out only to each other</li>
                    <li>That is why they are 7th and 9th by PageRank in vivienda, with degree 4 and 3</li>
                </ul>
                <table class="table">
                    <tr><td><p>"Consider two web pages that point to each other but to no other page. And suppose there is some web page which points to one of them. Then, during iteration, this loop will accumulate rank but never distribute any rank (since there are no outedges). The loop forms a sort of trap which we call a rank sink."</p><p><a href="https://web.archive.org/web/20241231011600/http://ilpubs.stanford.edu:8090/422/" target="_blank" rel="noopener noreferrer">Page et al. (1998), p. 4</a></p></td></tr>
                </table>
            </div>
        </div>
    </div>
</div>

## Comparing the Methods

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 55%">
                <p><b>node2vec on the largest component</b></p>
                <table class="table" style="font-size: 0.66em">
                    <thead>
                        <tr><th>Extract</th><th>No vector</th><th>Top 5 overlap, 3 seeds</th><th>Topic Jaccard, neighbours / random</th></tr>
                    </thead>
                    <tbody>
                        <tr><td>Nutrition papers</td><td>170 (53%)</td><td>0.75</td><td>0.197 / 0.043</td></tr>
                        <tr><td>Pobreza</td><td>68 (23%)</td><td>0.79</td><td>0.162 / 0.030</td></tr>
                        <tr><td>Vivienda</td><td>100 (31%)</td><td>0.81</td><td>0.168 / 0.029</td></tr>
                        <tr><td>Medio ambiente</td><td>94 (28%)</td><td>0.75</td><td>0.129 / 0.031</td></tr>
                        <tr><td>Agricultura</td><td>84 (27%)</td><td>0.73</td><td>0.127 / 0.045</td></tr>
                        <tr><td>Salud mental</td><td>57 (17%)</td><td>0.65</td><td>0.108 / 0.044</td></tr>
                    </tbody>
                </table>
                <div class="footnote">Numbers: box run on rebuilt data.</div>
            </div>
            <div class="column vertical-middle text-left" style="width: 45%">
                <ul>
                    <li>Neighbours share about 2.5 to 6 times more topics or categories than random pairs</li>
                    <li>The overlap across seeds is at least 0.65</li>
                    <li>No vector, the column sin_vector_n2v: more than half of the papers, since only the 148 of the largest component get one</li>
                    <li>Nearest neighbours of the stroke guideline: 4 of the 5 appear in all three seeds. One, Nutrition and physical activity guidelines for cancer survivors, is not directly linked to it</li>
                </ul>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
