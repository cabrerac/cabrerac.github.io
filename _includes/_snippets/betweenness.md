<!-- SLIDES: -->

## Betweenness

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>An item between others <a href="https://doi.org/10.2307/3033543" target="_blank" rel="noopener noreferrer">(Freeman, 1977)</a></b></p>
                <ul>
                    <li>Take two items and the shortest paths between them</li>
                    <li>Count how often an item lies on those paths</li>
                    <li>An item that joins two groups lies on many of them</li>
                    <li>Few links can still mean a high betweenness</li>
                </ul>
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
            <div class="column vertical-middle text-left" style="width: 55%">
                <p><b>The formula</b></p>
                <p>$$C_B(v) = \sum_{s < t,\ s \ne v \ne t} \frac{\sigma_{st}(v)}{\sigma_{st}}$$</p>
                <ul>
                    <li><p>The sum runs over unordered pairs $s, t$</p></li>
                    <li><p>$\sigma_{st}$ is the number of shortest paths from $s$ to $t$</p></li>
                    <li><p>$\sigma_{st}(v)$ is how many of them pass through $v$</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 45%">
                <p><b>Normalised</b></p>
                <p>$$\tilde{C}_B(v) = \frac{2 \, C_B(v)}{(n - 1)(n - 2)}$$</p>
                <ul>
                    <li><p>For an undirected graph, $(n - 1)(n - 2) / 2$ pairs can pass through $v$</p></li>
                    <li><p>So the score lies between 0 and 1</p></li>
                </ul>
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
                <ul>
                    <li>Start at one node, visit its neighbours, then theirs</li>
                    <li>The first visit to a node is along a shortest path</li>
                </ul>
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
                <ul>
                    <li>One breadth-first search from every node, counting shortest paths on the way</li>
                    <li>Then walk back from the farthest nodes and pass each node's share to the nodes before it</li>
                    <li>Time grows with nodes times edges, fine for a few hundred items</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Directed or undirected</b></p>
                <ul>
                    <li>Here betweenness uses the undirected graph</li>
                    <li>A link either way puts two items side by side</li>
                    <li>networkx.betweenness_centrality uses Brandes' algorithm</li>
                </ul>
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
                <ul>
                    <li>Normalised betweenness for every node</li>
                    <li>The top quarter among connected nodes</li>
                    <li>A bridge is in that quarter and is not a hub</li>
                </ul>
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
                <ul>
                    <li>A bridge joins parts of the graph that would be far apart without it</li>
                    <li>A hub lies on many paths only because it touches everything</li>
                    <li>So look first at the bridges that are not hubs, and read them</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Limits</b></p>
                <ul>
                    <li>One missing link can move a score a lot</li>
                    <li>Isolated items and small components score 0 or close to it</li>
                    <li>An item can be low on degree and high on betweenness. That disagreement is worth a look</li>
                </ul>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
