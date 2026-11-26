<!-- SLIDES: -->

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p>The place is <b>judged</b> against an outside measure, by the modularity of its communities, and against the other methods.</p>
            </div>
        </div>
    </div>
</div>

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <ul>
                    <li><p><b>Against an outside measure:</b> does the place agree with a count made outside this set</p></li>
                    <li><p><b>Modularity:</b> do the communities have more links inside than chance</p></li>
                    <li><p><b>Against the other methods:</b> bridges that are not hubs, and items placed high by several methods</p></li>
                    <li><p><b>Coverage:</b> how many items have no place, isolated or in a tiny component</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/social-network-analysis.jpg" alt="A network of links among people" style="height: auto; max-width: 100%; max-height: 90%;">
                <div class="footnote">Social Network Analysis Visualization - Martin Grandjean, CC BY-SA 3.0 <https://creativecommons.org/licenses/by-sa/3.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Against an outside measure</b> (<a href="https://doi.org/10.2307/1412159" target="_blank" rel="noopener noreferrer">Spearman, 1904</a>)</p>
                <br>
$$
\rho = 1 - \frac{6 \sum_i d_i^2}{n\,(n^2 - 1)}
$$
                <br>
                <table class="table" style="font-size: 0.72em">
                    <thead>
                        <tr><th>Item</th><th>Graph rank</th><th>Outside rank</th><th>Difference d</th></tr>
                    </thead>
                    <tbody>
                        <tr><td>A</td><td>1</td><td>1</td><td>0</td></tr>
                        <tr><td>B</td><td>2</td><td>3</td><td>-1</td></tr>
                        <tr><td>C</td><td>3</td><td>2</td><td>1</td></tr>
                        <tr><td>D</td><td>4</td><td>4</td><td>0</td></tr>
                    </tbody>
                </table>
                <br>
                <p>Here $\sum d_i^2 = 0 + 1 + 1 + 0 = 2$ and $n = 4$, so $\rho = 1 - 12/60 = 0.8$.</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/graph-rank-agreement.svg" alt="Two rankings of four items" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
</div>

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>An outside count such as citations covers the whole literature. A graph score covers only this set.</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/graph-rank-agreement.svg" alt="Two rankings of four items" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
</div>

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 47.5%; font-size: 0.85em">

```python
from scipy.stats import spearmanr

graph_rank = [1, 2, 3, 4]
outside_rank = [1, 3, 2, 4]
rho, _ = spearmanr(graph_rank, outside_rank)
print(round(rho, 2))
```
</div>
            <div class="column vertical-middle text-left" style="width: 5%"></div>
            <div class="column vertical-middle text-left" style="width: 47.5%">
                <p><b>Python usage:</b> SciPy</p>
                <p>Rank agreement of a graph score and an outside count</p>
                <ul>
                    <li><p><b>spearmanr:</b> ranks both lists, so the scale does not matter</p></li>
                    <li><p><b>The same items:</b> both lists in the same order</p></li>
                    <li><p><b>Returns:</b> 0.8. In the Lecture 5 notebook, PageRank against citations gives 0.30</p></li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Modularity of the communities</b> (<a href="https://doi.org/10.1103/PhysRevE.69.026113" target="_blank" rel="noopener noreferrer">Newman and Girvan, 2004</a>)</p>
                <ul>
                    <li><p>Values from about 0.3 to 0.7 are usual for graphs with clear communities</p></li>
                    <li><p>A partition is judged against the same graph, not against another one</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/louvain-2.svg" alt="Two communities in the toy graph" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
</div>

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Bridges that are not hubs</b></p>
                <ul>
                    <li><p>Betweenness against degree: a bridge has few links and a high betweenness</p></li>
                    <li><p>Read the items where the two disagree first</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/betweenness-1.svg" alt="Betweenness of each node" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
</div>

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 65%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%; height: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/graph-three-methods.svg" alt="What PageRank, betweenness and Louvain see" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
    <div class="row" style="height: 35%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%; height: 100%">
                <p><b>What each method sees</b></p>
                <ul>
                    <li><p><b>PageRank:</b> links from well placed items</p></li>
                    <li><p><b>Betweenness:</b> the items that join groups</p></li>
                    <li><p><b>Louvain:</b> groups with more links inside than outside</p></li>
                </ul>
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
                <table class="table">
                    <thead>
                        <tr><th>Method</th><th>What it sees</th><th>What it misses</th></tr>
                    </thead>
                    <tbody>
                        <tr><td>PageRank</td><td>Links from well placed items</td><td>Items that only link out, and bridges with few links</td></tr>
                        <tr><td>Betweenness</td><td>Items that join groups</td><td>Importance inside one group</td></tr>
                        <tr><td>Louvain</td><td>Groups with more links inside than outside</td><td>Why the items are linked, and very small groups</td></tr>
                    </tbody>
                </table>
                <ul>
                    <li><p>Run every method on the same graph, and read items where they disagree</p></li>
                    <li><p>An item placed high by several methods is a stronger candidate.</p></li>
                </ul>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
