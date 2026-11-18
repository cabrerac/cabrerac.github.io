<!-- SLIDES: -->

## k-means

<div class="rows" style="height: 100%">
    <div class="row" style="height: 70%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img class="external-svg" src="{{ site.url }}/assets/media/diagrams/group-task-taxonomy.svg" alt="Taxonomy of grouping methods" style="width: 100%; height: 100%">
            </div>
        </div>
    </div>
    <div class="row" style="height: 30%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <p><b>Partitioning:</b> each item goes to one of $k$ groups around centres.</p>
                <p><b>Model-based:</b> each group is a distribution, so membership is a probability.</p>
                <p><b>Density-based:</b> groups are dense regions, and thin regions are noise.</p>
                <p><b>Hierarchical:</b> a tree of groups inside groups.</p>
            </div>
        </div>
    </div>
</div>

## k-means

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p><b>k-means</b> splits the items into $k$ groups so that each item is close to the centre of its own group.</p>
            </div>
        </div>
    </div>
</div>

## k-means

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>The idea</b></p>
                <ul>
                    <li><p>Choose $k$, the number of groups</p></li>
                    <li><p>Each group has a centre</p></li>
                    <li><p>Each item goes to its closest centre</p></li>
                    <li><p>Move the centres, and repeat</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/k-means-convergence.gif" alt="k-means moving its centres" style="height: 360px">
                <div class="footnote">K-means convergence - Chire, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## k-means

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Preparation: each item scaled to length 1</b></p>
                <p>$$\hat{\mathbf{x}} = \frac{\mathbf{x}}{\lVert \mathbf{x} \rVert}$$</p>
                <p>$\mathbf{x}$ is one item.</p>
                <p>$\lVert \mathbf{x} \rVert$ is its length, the square root of the sum of its squared values.</p>
                <p>A long text has big counts and a short one small counts. After scaling, only the mix of attributes matters.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/diagrams/unit-length-scaling.svg" alt="Three items before and after scaling to length 1" style="height: 380px">
            </div>
        </div>
    </div>
</div>

## k-means

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>k-means looks for the centres that make the items closest to them.</p>
                <br>
                <p>$$J = \sum_{j=1}^{k} \sum_{i \in C_j} \lVert \mathbf{x}_i - \boldsymbol{\mu}_j \rVert^2$$</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>The outer sum runs over the $k$ groups.</p>
                <p>The inner sum runs over the items of group $j$, the set $C_j$.</p>
                <p>$\boldsymbol{\mu}_j$ is the centre, the mean of those items.</p>
                <p>Each term is the squared distance from an item to its centre.</p>
                <p><b>Lloyd steps:</b> assign each item, move each centre, and repeat <a href="https://doi.org/10.1109/TIT.1982.1056489" target="_blank" rel="noopener noreferrer">(Lloyd, 1982)</a>.</p>
                <p><b>k-means++:</b> starting centres far apart <a href="https://dl.acm.org/doi/10.5555/1283383.1283494" target="_blank" rel="noopener noreferrer">(Arthur &amp; Vassilvitskii, 2007)</a>.</p>
            </div>
        </div>
    </div>
</div>

## k-means

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <ul>
                    <li>A = 1, B = 2, C = 3, D = 8, E = 9</li>
                    <li><p>$k = 2$, starting centres at 1 and 9</p></li>
                </ul>
                <p>A, B and C are closer to 1. D and E are closer to 9. The centres move to the means, 2 and 8.5. Then nothing changes.</p>
                <p>$$J = 1^2 + 0^2 + 1^2 + 0.5^2 + 0.5^2 = 2.5$$</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/diagrams/kmeans-five-items.svg" alt="Two k-means steps on five items" style="height: 380px">
            </div>
        </div>
    </div>
</div>

## k-means

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 47.5%">

```text
scale each item to length 1
for each k from 3 to 8
    place k centres with k-means++
    repeat
        assign each item to its closest centre
        move each centre to the mean of its items
    until nothing changes
    keep the labels of this k for Evaluation
```

            </div>
            <div class="column vertical-middle text-left" style="width: 5%">
            </div>
            <div class="column vertical-middle text-left" style="width: 47.5%">

```python
from sklearn.cluster import KMeans
from sklearn.preprocessing import normalize

X = normalize(counts)   # every row has length 1
kmeans_runs = {}
for k in K_CANDIDATES:
    model = KMeans(n_clusters=k, n_init=10,
                   random_state=SEED).fit(X)
    kmeans_runs[k] = model.labels_
```

            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
