<!-- SLIDES: -->

## PageRank

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p><b>PageRank</b> scores an item by the links it receives, and a link counts more when it comes from an item that scores high itself.</p>
            </div>
        </div>
    </div>
</div>

## PageRank

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Degree that weighs who links to a page</b></p>
                <p>Degree counts every link the same. PageRank weighs who makes it.</p>
                <ul>
                    <li>A random surfer follows links, and now and then jumps to any item.</li>
                    <li>PageRank is the share of time the surfer spends on each item.</li>
                </ul>
                <br>
                <p>"a page has high rank if the sum of the ranks of its backlinks is high." <a href="https://web.archive.org/web/20241231011600/http://ilpubs.stanford.edu:8090/422/" target="_blank" rel="noopener noreferrer">(Page et al., 1998, p. 3)</a></p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/pagerank-example.svg" alt="PageRank example with nodes sized by score" style="height: 340px">
                <div class="footnote">PageRanks Example - 345Kai and Stannered, Public domain, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## PageRank

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>The formula</b></p>
                <p>$$PR(v) = \frac{1 - d}{n} + d \sum_{u \to v} \frac{PR(u)}{\text{out}(u)}$$</p>
                <ul>
                    <li><p>$d = 0.85$ is the damping, the chance to follow a link</p></li>
                    <li><p>$\text{out}(u)$ is the number of links $u$ makes. Its score is split among them</p></li>
                    <li><p>An item with no links out passes its score to every item</p></li>
                    <li><p>Items that link only among themselves would trap the surfer, a <b>rank sink</b></p></li>
                </ul>
            </div>
        </div>
    </div>
</div>

## PageRank

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Power iteration</b></p>
                <p>Start with $PR(v) = 1/n$ for every item.</p>
                <ul>
                    <li>Apply the formula to all items until the scores stop changing.</li>
                    <li><p>The scores add up to 1, so compare them with $1/n$.</p></li>
                </ul>
            </div>
        </div>
    </div>
</div>

## PageRank

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 45%">
                <p><b>Four items</b></p>
                <p>A links to B and C. B links to C. C links to A. D links to C.</p>
                <table class="table">
                    <thead>
                        <tr><th>Item</th><th>In-degree</th><th>PageRank</th></tr>
                    </thead>
                    <tbody>
                        <tr><td>A</td><td>1</td><td>0.373</td></tr>
                        <tr><td>B</td><td>1</td><td>0.196</td></tr>
                        <tr><td>C</td><td>3</td><td>0.394</td></tr>
                        <tr><td>D</td><td>0</td><td>0.038</td></tr>
                    </tbody>
                </table>
            </div>
            <div class="column vertical-middle text-left" style="width: 55%">
                <p><b>Same in-degree, different PageRank</b></p>
                <p>A's one link comes from C, the best placed item. B's comes from A, which splits its score in two.</p>
                <ul>
                    <li>So A has almost twice the PageRank of B.</li>
                    <li><p>D gets only the random jump, $0.15 / 4 = 0.0375$.</p></li>
                </ul>
            </div>
        </div>
    </div>
</div>

## PageRank

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 40%">
                <p><b>Python, by hand</b></p>
                <p>The directed links as a dict of sets.</p>
                <p>One loop is one step of the surfer for every item.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 60%">

```python
DAMPING = 0.85

def pagerank(links_out, d=DAMPING, steps=100):
    nodes = list(links_out)
    n = len(nodes)
    rank = {v: 1 / n for v in nodes}
    for _ in range(steps):
        new = {v: (1 - d) / n for v in nodes}
        for u in nodes:
            targets = links_out[u] or nodes   # no links: jump anywhere
            for v in targets:
                new[v] += d * rank[u] / len(targets)
        rank = new
    return rank

rank = pagerank(links_out)
```

</div>
        </div>
    </div>
</div>

## PageRank

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 55%">
                <p><b>Python, networkx</b></p>

```python
import networkx as nx

directed = nx.DiGraph()
directed.add_nodes_from(links_out)
directed.add_edges_from((u, v) for u, vs in links_out.items() for v in vs)

rank = nx.pagerank(directed, alpha=DAMPING)
top_rank = sorted(rank, key=rank.get, reverse=True)[:10]
not_by_degree = [v for v in top_rank if v not in top_degree]
```

</div>
            <div class="column vertical-middle text-left" style="width: 45%">
                <p><b>Reading question</b></p>
                <p>When do degree and PageRank disagree?</p>
                <ul>
                    <li>When an item gets few links, but from well placed items.</li>
                    <li>When an item gets many links from items nobody links to.</li>
                    <li>A hub tops both, so the hub warning holds for PageRank too.</li>
                </ul>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
