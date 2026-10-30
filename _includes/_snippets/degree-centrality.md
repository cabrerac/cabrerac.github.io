<!-- SLIDES: -->

## Degree

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>How many links</b></p>
                <p>$$\deg(v) = |N(v)|$$</p>
                <p>$$\text{share}(v) = \frac{\deg(v)}{n - 1}$$</p>
                <ul>
                    <li><p>$n$ is the number of nodes, so $n - 1$ is the most links a node can have</p></li>
                    <li><p>In a directed graph, in-degree counts links received and out-degree links made</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Reading the degree</b></p>
                <ul>
                    <li>Most items have few links and a few have many</li>
                    <li>A histogram of degree shows this long tail</li>
                    <li>Isolated items sit at degree 0, often a large bar</li>
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
                <p><b>The hub warning</b></p>
                <ul>
                    <li>A node linked to a large share of the others is a <b>hub</b></li>
                    <li>Often it is the topic itself, the article everything else points to</li>
                    <li>A hub is a warning, not an automatic pick</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>One rule for a hub</b></p>
                <ul>
                    <li><p>A node is a hub when it is linked to at least 10% of the others</p></li>
                    <li><p>$\deg(v) \ge \max(m, \lceil 0.10 \cdot (n - 1) \rceil)$</p></li>
                    <li><p>$m$ is a minimum count, so a hub in a small set still needs a few links</p></li>
                    <li><p>Report the hubs, then read the other items with and without them</p></li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Degree

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 40%">
                <p><b>Python</b></p>
                <ul>
                    <li>Degree and its share</li>
                    <li>Isolated nodes and hubs</li>
                    <li>The top 10 by degree, kept for PageRank</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 60%">


```python
import math

HUB_SHARE = 0.10   # linked to at least 10% of the others: a warning
MIN_LINKS = 5      # a hub in a small set still needs a few links

def hub_threshold(n, min_links=MIN_LINKS):
    return max(min_links, math.ceil(HUB_SHARE * (n - 1)))

n = len(neighbours)
degree = {v: len(nbrs) for v, nbrs in neighbours.items()}
degree_share = {v: d / (n - 1) for v, d in degree.items()}
isolated = [v for v, d in degree.items() if d == 0]
hubs = [v for v, d in degree.items() if d >= hub_threshold(n)]

top_degree = sorted(degree, key=degree.get, reverse=True)[:10]
```

</div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
