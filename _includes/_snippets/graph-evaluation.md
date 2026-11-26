<!-- SLIDES: -->

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p>With no answer key, a place is <b>judged</b> against an outside measure, across seeds, and against random pairs.</p>
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
                    <li><p><b>Across seeds:</b> does node2vec give the same neighbours on a rerun</p></li>
                    <li><p><b>Against random pairs:</b> do neighbours share more than chance</p></li>
                    <li><p><b>Coverage:</b> how many items have no place, isolated or with no vector</p></li>
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
$$
\rho = 1 - \frac{6 \sum_i d_i^2}{n\,(n^2 - 1)}
$$
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
                <p>A low agreement is a finding, not an error.</p>
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
            <div class="column vertical-middle text-left" style="width: 47.5%">
                <p><b>Python usage:</b> SciPy</p>
                <p>Rank agreement of a graph score and an outside count</p>
                <ul>
                    <li><p><b>spearmanr:</b> ranks both lists, so the scale does not matter</p></li>
                    <li><p><b>The same items:</b> both lists in the same order</p></li>
                    <li><p><b>Returns:</b> 0.8. In the Lecture 5 notebook, PageRank against citations gives 0.30</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 5%"></div>
            <div class="column vertical-middle text-left" style="width: 47.5%; font-size: 0.85em">

```python
from scipy.stats import spearmanr

graph_rank = [1, 2, 3, 4]
outside_rank = [1, 3, 2, 4]
rho, _ = spearmanr(graph_rank, outside_rank)
print(round(rho, 2))
```
</div>
        </div>
    </div>
</div>

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Across seeds</b></p>
$$
\text{overlap}(v) = \frac{|N_k^{(1)}(v) \cap N_k^{(2)}(v)|}{k}
$$
                <p><b>$N_k^{(1)}(v)$:</b> the $k$ nearest neighbours of $v$ with the first seed</p>
                <p><b>$N_k^{(2)}(v)$:</b> the same with the second seed</p>
                <p>In the example, 5 neighbours in each run share 4, so the overlap is $4/5 = 0.8$. A low mean overlap says the neighbours are mostly chance.</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/graph-seed-overlap.svg" alt="Two neighbour sets of one node, four shared" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
</div>

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 58%; font-size: 0.85em">

```python
def top_neighbours(vectors, v, k=5):
    """The k nearest neighbours of v, as a set."""
    found = set()
    for u, _ in vectors.most_similar(v, topn=k):
        found.add(u)
    return found

shares = []
for v in nodes:
    first = top_neighbours(runs[0], v)
    for other in runs[1:]:
        shared = first & top_neighbours(other, v)
        shares.append(len(shared) / 5)
overlap = sum(shares) / len(shares)
```
</div>
            <div class="column vertical-middle text-left" style="width: 4%"></div>
            <div class="column vertical-middle text-left" style="width: 38%">
                <p><b>Python usage:</b> gensim</p>
                <p>Neighbours that repeat when node2vec runs again with another seed</p>
                <ul>
                    <li><p><b>most_similar:</b> the 5 nearest neighbours of a node</p></li>
                    <li><p><b>&amp;:</b> keeps the neighbours found by both runs</p></li>
                    <li><p><b>Returns:</b> 0.75 with the three seeds of the Lecture 5 notebook</p></li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 38%">
                <p><b>Python usage:</b> Python</p>
                <p>Do neighbours share more topics than random pairs?</p>
                <ul>
                    <li><p><b>jaccard:</b> shared topics over all topics of two items</p></li>
                    <li><p><b>sample:</b> 1,000 random pairs of items with a vector</p></li>
                    <li><p><b>Returns:</b> 0.197 for neighbours and 0.043 for random pairs in the Lecture 5 notebook, 4.6 times more</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 4%"></div>
            <div class="column vertical-middle text-left" style="width: 58%; font-size: 0.85em">

```python
import random

def jaccard(a, b):
    """Shared elements over all elements."""
    if not a | b:
        return 0.0
    return len(a & b) / len(a | b)

near = []
for v in nodes:
    for u in top_neighbours(runs[0], v):
        near.append(jaccard(topics[v], topics[u]))
rng = random.Random(7)
far = []
for _ in range(1000):
    a, b = rng.sample(nodes, 2)
    far.append(jaccard(topics[a], topics[b]))
```
</div>
        </div>
    </div>
</div>

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 56%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%; height: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/graph-methods-see.svg" alt="What degree, PageRank and node2vec see" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
    <div class="row" style="height: 44%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%; height: 100%">
                <p><b>What each method sees</b></p>
                <ul>
                    <li><p><b>Degree:</b> how many links an item has</p></li>
                    <li><p><b>PageRank:</b> links from well placed items</p></li>
                    <li><p><b>node2vec:</b> items that share a neighbourhood</p></li>
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
                        <tr><td>Degree</td><td>How many links an item has</td><td>Who makes the links</td></tr>
                        <tr><td>PageRank</td><td>Links from well placed items</td><td>Items that only link out</td></tr>
                        <tr><td>node2vec</td><td>Items that share a neighbourhood</td><td>Items outside the largest component, and why they are close</td></tr>
                    </tbody>
                </table>
                <ul>
                    <li><p>Run every method on the same graph, and read items where they disagree</p></li>
                    <li><p>An item placed high by several methods is a stronger candidate. Disagreement is not a winner.</p></li>
                </ul>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
