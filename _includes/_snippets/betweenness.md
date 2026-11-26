<!-- SLIDES: -->

## Betweenness

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

## Betweenness

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p><b>Betweenness</b> counts how often an item lies on the shortest paths between two other items, so it is high for the items that join groups.</p>
            </div>
        </div>
    </div>
</div>

## Betweenness

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>An item between others</b> (<a href="https://doi.org/10.2307/3033543" target="_blank" rel="noopener noreferrer">Freeman, 1977</a>)</p>
                <p>Take two items and the shortest paths between them.</p>
                <ul>
                    <li><p>Count how often a third item lies on those paths</p></li>
                    <li><p>An item that joins two groups lies on many of them</p></li>
                    <li><p>Few links can still mean a high betweenness</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/graph-betweenness.svg" alt="Graph coloured by betweenness, from low in blue to high in red" style="height: auto; max-width: 100%; max-height: 90%;">
                <div class="footnote">Graph betweenness - Claudio Rocchini, CC BY 2.5 <https://creativecommons.org/licenses/by/2.5>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Betweenness

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
$$
C_B(v) = \sum_{s < t,\ s \ne v \ne t} \frac{\sigma_{st}(v)}{\sigma_{st}}
$$
$$
\tilde{C}_B(v) = \frac{2 \, C_B(v)}{(n - 1)(n - 2)}
$$
                <p><b>$\sigma_{st}$:</b> the number of shortest paths from $s$ to $t$</p>
                <p><b>$\sigma_{st}(v)$:</b> how many of them pass through $v$</p>
                <p><b>$\tilde{C}_B(v)$:</b> the normalised score, between 0 and 1, over the $(n - 1)(n - 2)/2$ pairs without $v$</p>
                <p>The one shortest path from A to E passes through C, X and D.</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/betweenness-2.svg" alt="The shortest path from A to E" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
</div>

## Betweenness

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Worked example.</b> Two groups, A B C and D E F, joined only through X.</p>
                <ul>
                    <li><p>Every path from A, B or C to D, E or F passes through X. That is $3 \cdot 3 = 9$ pairs, so $C_B(X) = 9$</p></li>
                    <li><p>With $n = 7$, $\tilde{C}_B(X) = 2 \cdot 9 / (6 \cdot 5) = 0.6$</p></li>
                    <li><p>C lies on the paths from A and B to X, D, E, F, so $C_B(C) = 8$ and $\tilde{C}_B(C) = 0.53$</p></li>
                    <li><p>A, B, E and F lie on no path between others. Their score is 0</p></li>
                </ul>
                <p>X has degree 2, like A, yet the highest betweenness.</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/betweenness-1.svg" alt="Betweenness of each node" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
</div>

## Betweenness

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 38%">
                <p><b>Python usage:</b> Python</p>
                <p>Shortest paths by breadth-first search</p>
                <ul>
                    <li><p>Start at one node, visit its neighbours, then theirs</p></li>
                    <li><p>The first visit to a node is along a shortest path</p></li>
                    <li><p><b>Returns:</b> from A on the seven items, A 0, B 1, C 1, X 2, D 3, E 4, F 4</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 4%"></div>
            <div class="column vertical-middle text-left" style="width: 58%; font-size: 0.85em">

```python
from collections import deque

def distances_from(source, neighbours):
    """Steps from source to every node it reaches."""
    dist = {source: 0}
    queue = deque([source])
    while queue:
        u = queue.popleft()
        for v in neighbours[u]:
            if v not in dist:
                dist[v] = dist[u] + 1
                queue.append(v)
    return dist
```
</div>
        </div>
    </div>
</div>

## Betweenness

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 47.5%; font-size: 0.85em">

```text
for each node s
    breadth-first search from s
        count the shortest paths
        to every node on the way
    walk back from the farthest nodes
        each node passes its share
        to the nodes just before it
    add the shares to the scores
halve the scores, every pair is seen twice
```
</div>
            <div class="column vertical-middle text-left" style="width: 5%"></div>
            <div class="column vertical-middle text-left" style="width: 47.5%">
                <p><b>Brandes' algorithm</b> (<a href="https://doi.org/10.1080/0022250X.2001.9990249" target="_blank" rel="noopener noreferrer">Brandes, 2001</a>)</p>
                <ul>
                    <li><p>One breadth-first search from every node</p></li>
                    <li><p>Time grows with nodes times edges, fine for a few hundred items</p></li>
                    <li><p><b>networkx</b> uses it in betweenness_centrality</p></li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Betweenness

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 47.5%">
                <p><b>Python usage:</b> networkx</p>
                <p>Betweenness of the seven items, on the undirected graph</p>
                <ul>
                    <li><p><b>nx.Graph:</b> undirected, a link either way puts two items side by side</p></li>
                    <li><p><b>normalized:</b> scores between 0 and 1</p></li>
                    <li><p><b>Returns:</b> X 0.6, C and D 0.533, the other four 0</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 5%"></div>
            <div class="column vertical-middle text-left" style="width: 47.5%; font-size: 0.85em">

```python
import networkx as nx

graph = nx.Graph()
graph.add_edges_from([("A", "B"), ("A", "C"),
                      ("B", "C"), ("C", "X"),
                      ("X", "D"), ("D", "E"),
                      ("D", "F"), ("E", "F")])
between = nx.betweenness_centrality(
    graph, normalized=True)
for v in sorted(between):
    print(v, round(between[v], 3))
```
</div>
        </div>
    </div>
</div>

## Betweenness

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Limits</b></p>
                <ul>
                    <li><p>One missing link can move a score a lot</p></li>
                    <li><p>Isolated items and small components score 0 or close to it</p></li>
                    <li><p>A hub lies on many paths only because it touches everything</p></li>
                    <li><p>An item low on degree and high on betweenness is a bridge worth reading</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/betweenness-1.svg" alt="Betweenness of each node" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
