<!-- SLIDES: -->

## Degree

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p>The <b>degree</b> of an item is the number of links it has to other items in the graph.</p>
            </div>
        </div>
    </div>
</div>

## Degree

<div class="rows" style="height: 100%">
    <div class="row" style="height: 62%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%; height: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/graph-from-table-2.svg" alt="Duplicate and self links dropped" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
    <div class="row" style="height: 38%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%; height: 100%">
                <p><b>Preparation:</b> from a table to a graph</p>
                <ul>
                    <li><p>Each row is an item, with the items it links to</p></li>
                    <li><p>Drop duplicate links and self links</p></li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Degree

<div class="rows" style="height: 100%">
    <div class="row" style="height: 62%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%; height: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/graph-from-table-3.svg" alt="The links that stay, drawn as a graph" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
    <div class="row" style="height: 38%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%; height: 100%">
                <p><b>Preparation:</b> from a table to a graph</p>
                <ul>
                    <li><p>Each row is an item, with the items it links to</p></li>
                    <li><p>Drop duplicate links and self links</p></li>
                    <li><p>Keep a link only when both ends are in the set</p></li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Degree

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>Degree counts the neighbours of a node. Its share compares that count with the most it could have.</p>
$$
\deg(v) = |N(v)|
$$
$$
\text{share}(v) = \frac{\deg(v)}{n - 1}
$$
                <p><b>$N(v)$:</b> the neighbours of $v$, and $|N(v)|$ how many</p>
                <p><b>$n - 1$:</b> every other node, so the share lies between 0 and 1</p>
                <p>In a directed graph, in-degree counts links received and out-degree links made.</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/graph-words-2.svg" alt="The neighbours of C highlighted" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
</div>

## Degree

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <ul>
                    <li><p>Five items, A to E</p></li>
                    <li><p>Edges A to B, A to C, A to D, and B to C</p></li>
                    <li><p>E has no edge</p></li>
                </ul>
                <p>$\deg(A) = 3$, so its share is $3/4 = 0.75$. B and C have degree 2, D has 1.</p>
                <p>E has degree 0. It is isolated.</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/degree-example-2.svg" alt="The degree of each node" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
</div>

## Degree

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>A node linked to a large share of the others is a <b>hub</b>.</p>
                <ul>
                    <li><p>Often it is the subject itself, the item everything else points to</p></li>
                    <li><p>A hub is a warning, not an automatic pick</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/degree-hub-1.svg" alt="A star-like graph" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
</div>

## Degree

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>One rule for a hub, set before the results:</p>
$$
\deg(v) \ge \max\left(m,\ \lceil 0.10 \cdot (n - 1) \rceil\right)
$$
                <p><b>$0.10 \cdot (n - 1)$:</b> 10% of the other nodes, rounded up</p>
                <p><b>$m$:</b> a minimum count, so a hub in a small set still needs a few links</p>
                <p>With $m = 3$ and $n = 9$, the limit is 3, so $\deg(H) = 8$ flags H as a hub.</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/degree-hub-2.svg" alt="The hub flagged as a warning" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
</div>

## Degree

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Limits</b></p>
                <ul>
                    <li><p>Degree counts every link the same</p></li>
                    <li><p>One missing link changes the count</p></li>
                    <li><p>We report the hubs, then read the other items with and without them</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/degree-hub-2.svg" alt="The hub flagged as a warning" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
</div>

## Degree

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 47.5%; font-size: 0.85em">

```text
for each link from a to b
    keep it when both are in the set
        and a is not b
    add b to the neighbours of a
    add a to the neighbours of b
degree = number of neighbours
isolated = nodes with degree 0
limit = max(m, ceil(0.10 * (n - 1)))
hubs = nodes with degree >= limit
```
</div>
            <div class="column vertical-middle text-left" style="width: 4%"></div>
            <div class="column vertical-middle text-center" style="width: 47.5%; height: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/degree-example-2.svg" alt="The degree of each node" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
</div>

## Degree

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 47.5%">
                <p><b>Python usage:</b> networkx</p>
                <p>Degree and the hub rule on the five items</p>
                <ul>
                    <li><p><b>nx.Graph:</b> an undirected graph, nodes first so that E is kept</p></li>
                    <li><p><b>degree:</b> the number of neighbours of each node</p></li>
                    <li><p><b>Returns:</b> {'A': 3, 'B': 2, 'C': 2, 'D': 1, 'E': 0} and the hubs ['A']</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 5%"></div>
            <div class="column vertical-middle text-left" style="width: 47.5%; font-size: 0.85em">

```python
import math
import networkx as nx

graph = nx.Graph()
graph.add_nodes_from(["A", "B", "C", "D", "E"])
graph.add_edges_from([("A", "B"), ("A", "C"),
                      ("A", "D"), ("B", "C")])
degree = dict(graph.degree())
n = graph.number_of_nodes()
limit = max(3, math.ceil(0.10 * (n - 1)))  # m = 3
hubs = []
for v in degree:
    if degree[v] >= limit:
        hubs.append(v)
print(degree, hubs)
```
</div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
