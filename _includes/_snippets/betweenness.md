<!-- SLIDES: -->

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
                <p><b>An item between others <a href="https://doi.org/10.2307/3033543" target="_blank" rel="noopener noreferrer">(Freeman, 1977)</a></b></p>
                <p>Take two items and the shortest paths between them.</p>
                <p>Count how often an item lies on those paths.</p>
                <p>An item that joins two groups lies on many of them.</p>
                <p>Few links can still mean a high betweenness.</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/graph-betweenness.svg" alt="Graph coloured by betweenness, from low in blue to high in red" style="height: 360px">
                <div class="footnote">Graph betweenness - Claudio Rocchini, CC BY 2.5 <https://creativecommons.org/licenses/by/2.5>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Betweenness

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 55%">
                <p><b>The formula</b></p>
                <p>$$C_B(v) = \sum_{s < t,\ s \ne v \ne t} \frac{\sigma_{st}(v)}{\sigma_{st}}$$</p>
                <p>The sum runs over unordered pairs $s, t$.</p>
                <p>$\sigma_{st}$ is the number of shortest paths from $s$ to $t$.</p>
                <p>$\sigma_{st}(v)$ is how many of them pass through $v$.</p>
            </div>
            <div class="column vertical-top text-left" style="width: 45%">
                <p><b>Normalised</b></p>
                <p>$$\tilde{C}_B(v) = \frac{2 \, C_B(v)}{(n - 1)(n - 2)}$$</p>
                <p>For an undirected graph, $(n - 1)(n - 2) / 2$ pairs can pass through $v$.</p>
                <p>So the score lies between 0 and 1.</p>
            </div>
        </div>
    </div>
</div>

## Betweenness

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 40%">
                <p><b>Shortest paths by breadth-first search</b></p>
                <p>Start at one node, visit its neighbours, then theirs.</p>
                <p>The first visit to a node is along a shortest path.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 60%">


```python
from collections import deque

def distances_from(source, neighbours):
    """Breadth-first search: steps from source to every reachable node."""
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
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Brandes' algorithm <a href="https://doi.org/10.1080/0022250X.2001.9990249" target="_blank" rel="noopener noreferrer">(Brandes, 2001)</a></b></p>
                <p>One breadth-first search from every node, counting shortest paths on the way.</p>
                <p>Then walk back from the farthest nodes and pass each node's share to the nodes before it.</p>
                <p>Time grows with nodes times edges, fine for a few hundred items.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Directed or undirected</b></p>
                <p>Here betweenness uses the undirected graph.</p>
                <p>A link either way puts two items side by side.</p>
                <p>networkx.betweenness_centrality uses Brandes' algorithm.</p>
            </div>
        </div>
    </div>
</div>

## Betweenness

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 40%">
                <p><b>Python</b></p>
                <p>Normalised betweenness for every node.</p>
                <p>The top quarter among connected nodes.</p>
                <p>A bridge is in that quarter and is not a hub.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 60%">


```python
import networkx as nx

graph = nx.Graph()
graph.add_nodes_from(neighbours)
graph.add_edges_from((u, v) for u, vs in neighbours.items() for v in vs)

between = nx.betweenness_centrality(graph, normalized=True)
between = {v: round(b, 9) for v, b in between.items()}   # equal scores stay equal

connected = [v for v in graph if degree[v] > 0]
cut = sorted(between[v] for v in connected)[int(0.75 * len(connected))]
bridges = [v for v in connected if between[v] >= cut and v not in hubs]
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
                <p><b>A bridge between groups</b></p>
                <p>A bridge joins parts of the graph that would be far apart without it.</p>
                <p>A hub lies on many paths only because it touches everything.</p>
                <p>So look first at the bridges that are not hubs, and read them.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Limits</b></p>
                <p>One missing link can move a score a lot.</p>
                <p>Isolated items and small components score 0 or close to it.</p>
                <p>An item can be low on degree and high on betweenness. That disagreement is worth a look.</p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
