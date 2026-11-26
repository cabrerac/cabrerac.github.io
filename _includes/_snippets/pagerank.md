<!-- SLIDES: -->

## PageRank

<div class="rows" style="height: 100%">
    <div class="row" style="height: 65%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%; height: 100%">
                <img class="external-svg" src="{{ site.url }}/assets/media/diagrams/graph-task-taxonomy.svg" alt="Taxonomy of graph methods" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
    <div class="row" style="height: 35%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%; height: 100%">
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
                <p><b>Degree</b> counts the neighbours of a node. Its share compares that count with the most it could have.</p>
                <br>
$$
\deg(v) = |N(v)| \qquad \text{share}(v) = \frac{\deg(v)}{n - 1}
$$
                <br>
                <p><b>$n - 1$</b> is every other node, so the share lies between 0 and 1. In a directed graph, in-degree counts links received and out-degree links made.</p>
                <p>Here $\deg(A) = 3$, so its share is $3/4 = 0.75$. E has degree 0 and is isolated.</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/degree-example-2.svg" alt="The degree of each node" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
</div>

## PageRank

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>A node linked to a large share of the others is a <b>hub</b>. Often it is the subject itself. A hub is a warning, not an automatic pick. One pre-set rule for a hub:</p>
                <br>
$$
\deg(v) \ge \max\left(m,\ \lceil 0.10 \cdot (n - 1) \rceil\right)
$$
                <br>
                <p><b>$m$</b> is a minimum count, so a hub in a small set still needs a few links. With $m = 3$ and $n = 9$, the limit is 3, so $\deg(H) = 8$ flags H as a hub.</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/degree-hub-2.svg" alt="The hub flagged as a warning" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
</div>

## PageRank

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>Degree counts every link the same. PageRank weighs who makes it.</p>
                <ul>
                    <li><p>A random surfer follows links with probability $$d = 0.85$$</p></li>
                    <li><p>Now and then the surfer jumps to any item with probability $$1 - d = 0.15$$</p></li>
                    <li><p>PageRank is the share of time the surfer spends on each item</p></li>
                </ul>
                <p>"a page has high rank if the sum of the ranks of its backlinks is high." (<a href="https://web.archive.org/web/20241231011600/http://ilpubs.stanford.edu:8090/422/" target="_blank" rel="noopener noreferrer">Page et al., 1998</a>, p. 3)</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/pagerank-surfer-1.svg" alt="A surfer on A follows a link" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
</div>

## PageRank

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>Degree counts every link the same. PageRank weighs who makes it.</p>
                <ul>
                    <li><p>A random surfer follows links with probability $$d = 0.85$$</p></li>
                    <li><p>Now and then the surfer jumps to any item with probability $$1 - d = 0.15$$</p></li>
                    <li><p>PageRank is the share of time the surfer spends on each item</p></li>
                </ul>
                <p>"a page has high rank if the sum of the ranks of its backlinks is high." (<a href="https://web.archive.org/web/20241231011600/http://ilpubs.stanford.edu:8090/422/" target="_blank" rel="noopener noreferrer">Page et al., 1998</a>, p. 3)</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/pagerank-surfer-3.svg" alt="A jump to any node" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
</div>

## PageRank

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>PageRank is the share of time the random surfer spends on an item.</p>
                <br>
$$
PR(v) = \frac{1 - d}{n} + d \sum_{u \to v} \frac{PR(u)}{\text{out}(u)}
$$
                <br>
                <p><b>$(1 - d)/n$</b> is the jump share, which every item gets. <b>$d = 0.85$</b> is the chance to follow a link</p>
                <p><b>$\text{out}(u)$</b> is the links $u$ makes, which split its score. An item with no links out passes its score to every item.</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/pagerank-example.svg" alt="PageRank example with nodes sized by score" style="height: auto; max-width: 100%; max-height: 90%;">
                <div class="footnote">PageRanks Example - 345Kai and Stannered, Public domain, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## PageRank

<div class="rows" style="height: 100%">
    <div class="row" style="height: 65%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 30%; height: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/pagerank-iteration-1.svg" alt="Step 0, every item at 0.25" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
            <div class="column vertical-middle text-left" style="width: 3%"></div>
            <div class="column vertical-middle text-center" style="width: 30%; height: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/pagerank-iteration-2.svg" alt="Step 1" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
            <div class="column vertical-middle text-left" style="width: 3%"></div>
            <div class="column vertical-middle text-center" style="width: 30%; height: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/pagerank-iteration-3.svg" alt="The converged scores" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
    <div class="row" style="height: 35%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%; height: 100%">
                <p><b>Power iteration</b> on four items (A links to B and C, B to C, C to A, D to C):</p>
                <ul>
                    <li><p><b>Left:</b> step 0 gives every item $PR(v) = 1/n = 0.250$</p></li>
                    <li><p><b>Middle:</b> step 1 applies the formula once</p></li>
                    <li><p><b>Right:</b> repeat until the scores stop changing</p></li>
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
                <p><b>Same in-degree, different PageRank</b></p>
                <p>A and B each get one link.</p>
                <ul>
                    <li><p>A's link comes from C, the best placed item</p></li>
                    <li><p>B's comes from A, which splits its score in two</p></li>
                    <li><p>So A has almost twice the PageRank of B</p></li>
                    <li><p>D gets only the jump share, $0.15 / 4 = 0.0375$</p></li>
                </ul>
                <p>The scores add up to 1, so we compare them with $1/n$.</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/pagerank-iteration-3.svg" alt="The converged scores" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
</div>

## PageRank

<div class="rows" style="height: 100%">
    <div class="row" style="height: 65%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%; height: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/pagerank-sink-1.svg" alt="Without the jump B and C trap the score" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
    <div class="row" style="height: 35%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%; height: 100%">
                <p><b>A rank sink:</b> A links to B, and B and C link to each other. Nothing links to A.</p>
                <p>"Consider two web pages that point to each other but to no other page." (<a href="https://web.archive.org/web/20241231011600/http://ilpubs.stanford.edu:8090/422/" target="_blank" rel="noopener noreferrer">Page et al., 1998</a>, p. 4)</p>
                <ul>
                    <li><p><b>Without the jump ($d = 1$):</b> A drops to 0, and B and C trap all the score between them</p></li>
                </ul>
            </div>
        </div>
    </div>
</div>

## PageRank

<div class="rows" style="height: 100%">
    <div class="row" style="height: 65%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 47.5%; height: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/pagerank-sink-1.svg" alt="Without the jump B and C trap the score" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
            <div class="column vertical-middle text-left" style="width: 5%"></div>
            <div class="column vertical-middle text-center" style="width: 47.5%; height: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/pagerank-sink-2.svg" alt="With the jump all three keep a share" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
    <div class="row" style="height: 35%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%; height: 100%">
                <p><b>A rank sink:</b> A links to B, and B and C link to each other. Nothing links to A.</p>
                <p>"Consider two web pages that point to each other but to no other page." (<a href="https://web.archive.org/web/20241231011600/http://ilpubs.stanford.edu:8090/422/" target="_blank" rel="noopener noreferrer">Page et al., 1998</a>, p. 4)</p>
                <ul>
                    <li><p><b>Without the jump ($d = 1$):</b> A drops to 0, and B and C trap all the score between them</p></li>
                    <li><p><b>With the jump ($d = 0.85$):</b> A keeps 0.050, and B and C share 0.486 and 0.464</p></li>
                </ul>
            </div>
        </div>
    </div>
</div>

## PageRank

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 47.5%; height: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/pagerank-iteration-3.svg" alt="The converged scores" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
            <div class="column vertical-middle text-left" style="width: 4%"></div>
            <div class="column vertical-middle text-left" style="width: 47.5%; font-size: 0.85em">

```text
give every item the score 1 / n
repeat for a fixed number of steps
    give every item (1 - d) / n
    for each item u
        targets = the items u links to
        if u links to nothing
            targets = all items
        give each target
            d * score of u / size of targets
    the new scores replace the old ones
```
</div>
        </div>
    </div>
</div>

## PageRank

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 47.5%; font-size: 0.85em">

```python
import networkx as nx

graph = nx.DiGraph()
graph.add_edges_from([("A", "B"), ("A", "C"),
                      ("B", "C"), ("C", "A"),
                      ("D", "C")])
rank = nx.pagerank(graph, alpha=0.85)
for v in sorted(rank):
    print(v, round(rank[v], 3))
```
</div>
            <div class="column vertical-middle text-left" style="width: 5%"></div>
            <div class="column vertical-middle text-left" style="width: 47.5%">
                <p><b>Python usage:</b> networkx</p>
                <p>PageRank of the four items</p>
                <ul>
                    <li><p><b>nx.DiGraph:</b> a directed graph, one edge per link</p></li>
                    <li><p><b>alpha:</b> the chance to follow a link, $d = 0.85$</p></li>
                    <li><p><b>Returns:</b> A 0.373, B 0.196, C 0.394, D 0.038</p></li>
                </ul>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
