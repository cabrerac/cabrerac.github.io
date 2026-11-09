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
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Preparation: from a table to a graph</b></p>
                <p>Each row is an item, with the items it links to.</p>
                <ul>
                    <li>Drop duplicate items and self links</li>
                    <li>Keep a link only when both ends are in the set</li>
                    <li>Directed edges for PageRank, undirected edges for the rest</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/social-network-analysis.jpg" alt="A network of links among people" style="height: 400px">
                <div class="footnote">Social Network Analysis Visualization - Martin Grandjean, CC BY-SA 3.0 <https://creativecommons.org/licenses/by-sa/3.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Degree

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>Degree counts the neighbours of a node, and its share compares that count with the most it could have.</p>
                <br>
                <p>$$\deg(v) = |N(v)| \qquad \text{share}(v) = \frac{\deg(v)}{n - 1}$$</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>$N(v)$ is the set of neighbours of $v$ and $|N(v)|$ its size. $n$ is the number of nodes. The denominator $n - 1$ is every other node, the most links $v$ can have, so the share lies between 0 and 1.</p>
                <br>
                <p>In a directed graph, in-degree counts links received and out-degree links made.</p>
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
                    <li>Five items, A to E</li>
                    <li>Edges A to B, A to C, A to D, and B to C</li>
                    <li>E has no edge</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>$\deg(A) = 3$, so its share is $3/4 = 0.75$. B and C have degree 2, D has 1.</p>
                <br>
                <p>E has degree 0. It is isolated, a bar at 0 in a histogram of degree. Most graphs have many items with few links and a few with many, a long tail.</p>
            </div>
        </div>
    </div>
</div>

## Degree

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 55%">
                <p><b>The hub warning</b></p>
                <p>A node linked to a large share of the others is a <b>hub</b>.</p>
                <ul>
                    <li>Often it is the subject itself, the item everything else points to</li>
                    <li>A hub is a warning, not an automatic pick</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 45%">
                <img src="{{ site.url }}/assets/media/images/social-network-analysis.jpg" alt="A network of links among people" style="height: 360px">
                <div class="footnote">Social Network Analysis Visualization - Martin Grandjean, CC BY-SA 3.0 <https://creativecommons.org/licenses/by-sa/3.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Degree

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>One rule for a hub, set before the results</b></p>
                <p>$$\deg(v) \ge \max\left(m,\ \lceil 0.10 \cdot (n - 1) \rceil\right)$$</p>
                <p>$0.10 \cdot (n - 1)$ is 10% of the other nodes, rounded up. $m$ is a minimum count, so a hub in a small set still needs a few links. The rule takes the larger of the two.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>In the five items above, with $m = 3$, the limit is $\max(3, 1) = 3$, so A is the only hub.</p>
                <br>
                <p><b>Limits</b></p>
                <ul>
                    <li>Degree counts every link the same</li>
                    <li>One missing link changes the count</li>
                    <li>We report the hubs, then read the other items with and without them</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Degree

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 47.5%">

```text
for each link from a to b
    keep it when both are in the set and a is not b
    add b to the neighbours of a, and a to those of b
degree of each node = number of neighbours
isolated = nodes with degree 0
limit = max(m, ceil(0.10 * (n - 1)))
hubs = nodes with degree at least the limit
```

            </div>
            <div class="column vertical-middle text-left" style="width: 5%">
            </div>
            <div class="column vertical-middle text-left" style="width: 47.5%">

```python
import math
from collections import defaultdict

def undirected_graph(links, items):
    neighbours = defaultdict(set)
    for a, b in links:
        if a in items and b in items and a != b:
            neighbours[a].add(b)
            neighbours[b].add(a)
    return neighbours

def hubs(degree, n, m, share=0.10):
    limit = max(m, math.ceil(share * (n - 1)))
    return {v for v, d in degree.items() if d >= limit}

neighbours = undirected_graph(links, items)
degree = {v: len(neighbours[v]) for v in items}
hub_set = hubs(degree, len(items), m=3)
```

            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
