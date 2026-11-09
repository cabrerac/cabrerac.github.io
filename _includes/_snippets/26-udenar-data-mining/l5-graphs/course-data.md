<!-- SLIDES: -->

## The Question and the Data

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p><b>Our question:</b> where does each nutrition paper sit among the others in the link graph?</p>
            </div>
        </div>
    </div>
</div>

## The Question and the Data

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>From the links column</b></p>
                <ul>
                    <li>318 papers and 453 links inside the set</li>
                    <li>122 papers are isolated (38%)</li>
                    <li>The largest component has 148 papers (47%)</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>What that means</b></p>
                <p>The top paper, a Global Burden of Disease paper, links to 8% of the others, so no hub.</p>
            </div>
        </div>
    </div>
</div>

## The Question and the Data

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>PageRank against degree, the papers</b></p>
                <ul>
                    <li>Top by PageRank: a Global Burden of Disease risk paper</li>
                    <li>Spearman with in-degree 0.97, with total degree 0.75</li>
                    <li>High PageRank, low degree: Obesity in children and young people, degree 6</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## The Question and the Data

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Against citations</b></p>
                <ul>
                    <li>Spearman of PageRank with the citation count, printed by the notebook</li>
                    <li>Citations count the whole literature, PageRank only this set</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## The Question and the Data

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>A rank sink</b></p>
                <p>Two pages that link only to each other keep the score they receive.</p>
                <ul>
                    <li>The random jump lets the surfer out</li>
                    <li>A small closed loop can rank high with few links</li>
                </ul>
                <br>
                <p>"Consider two web pages that point to each other but to no other page." <a href="https://web.archive.org/web/20241231011600/http://ilpubs.stanford.edu:8090/422/" target="_blank" rel="noopener noreferrer">(Page et al., 1998, p. 4)</a></p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/pagerank-example.svg" alt="PageRank example" style="height: 340px">
                <div class="footnote">PageRanks Example - 345Kai and Stannered, Public domain, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## The Question and the Data

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>node2vec on the nutrition papers</b></p>
                <ul>
                    <li><b>No vector:</b> 170 papers (53%), outside the largest component</li>
                    <li><b>Seeds:</b> the top 5 neighbours overlap 0.75 across three seeds</li>
                    <li><b>Topics:</b> neighbours share 0.197, random pairs 0.043</li>
                    <li>The stroke guideline keeps 4 of its 5 nearest neighbours in all three seeds</li>
                </ul>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
