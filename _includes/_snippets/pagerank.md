<!-- SLIDES: -->

## PageRank

<div class="rows" style="height: 100%">
    <div class="row" style="height: 70%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img class="external-svg" src="{{ site.url }}/assets/media/diagrams/graph-task-taxonomy.svg" alt="Taxonomy of graph methods" style="width: 100%; height: 100%">
            </div>
        </div>
    </div>
    <div class="row" style="height: 30%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Link counts:</b> how many links an item has, and from whom.</p>
                <p><b>Paths:</b> how an item sits on the shortest paths between others.</p>
                <p><b>Node embeddings:</b> one vector per item, learned from the links.</p>
                <p><b>Communities:</b> groups of items with more links inside than outside.</p>
            </div>
        </div>
    </div>
</div>

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
                    <li><p>$PR(v)$ is the score of item $v$, the share of time the surfer spends on it</p></li>
                    <li><p>$n$ is the number of items in the graph</p></li>
                    <li><p>$(1-d)/n$ is the jump share. Every item gets it, whatever links it has</p></li>
                    <li><p>The sum runs over every item $u$ that links to $v$, and each adds a part of its own score</p></li>
                    <li><p>$d = 0.85$ is the damping, the chance to follow a link</p></li>
                    <li><p>$\text{out}(u)$ is the number of links $u$ makes. Its score is split among them</p></li>
                </ul>
                <p>An item with no links out passes its score to every item. Items that link only among themselves would trap the surfer, a <b>rank sink</b>.</p>
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
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>A rank sink</b></p>
                <p>A cites B, and B and C cite each other. Nothing cites A.</p>
                <ul>
                    <li><p><b>Without the jump:</b> A drops to 0 after one step, and B and C keep all the score between them</p></li>
                    <li><p><b>With the jump:</b> every item gets the first term of the formula, so A keeps a small share and the loop cannot hold it all</p></li>
                    <li><p>A small closed loop can still rank high with few links</p></li>
                </ul>
                <br>
                <p>"Consider two web pages that point to each other but to no other page." <a href="https://web.archive.org/web/20241231011600/http://ilpubs.stanford.edu:8090/422/" target="_blank" rel="noopener noreferrer">(Page et al., 1998, p. 4)</a></p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/diagrams/pagerank-abc.svg" alt="Three nodes sized by PageRank. A cites B, and B and C cite each other" style="height: 220px">
                <div class="footnote">PageRank on a small graph, A cites B, and B and C cite each other</div>
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
            <div class="column vertical-middle text-left" style="width: 47.5%">

```text
give every item the score 1 / n
repeat for a fixed number of steps
    give every item the jump share (1 - d) / n
    for each item u
        targets = the items u links to
        if u links to nothing, targets = all items
        give each target d * score of u / size of targets
    the new scores replace the old ones
```

            </div>
            <div class="column vertical-middle text-left" style="width: 5%">
            </div>
            <div class="column vertical-middle text-left" style="width: 47.5%">

```python
DAMPING = 0.85

def pagerank(links_out, d=DAMPING, steps=100):
    nodes = list(links_out)
    n = len(nodes)
    rank = {v: 1 / n for v in nodes}
    for _ in range(steps):
        new = {v: (1 - d) / n for v in nodes}
        for u in nodes:
            targets = links_out[u] or nodes
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

<!-- end SLIDES: -->
