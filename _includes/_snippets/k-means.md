<!-- SLIDES: -->

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
            <div class="column vertical-middle text-left" style="width: 45%">
                <p><b>The idea</b></p>
                <ul>
                    <li><p>Choose $k$, the number of groups</p></li>
                    <li><p>Each group has a centre</p></li>
                    <li><p>Each item goes to its closest centre</p></li>
                    <li><p>Move the centres, and repeat</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 55%">
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
                <p>$\mathbf{x}$ is the vector of one item, one number per attribute. $\lVert \mathbf{x} \rVert$ is its length, the square root of the sum of its squared values. After the division, every item has length 1.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>A long text has big counts and a short one small counts. After scaling, only the mix of attributes matters.</p>
                <br>
                <p>$$\cos(\mathbf{x}, \mathbf{y}) = \frac{\mathbf{x} \cdot \mathbf{y}}{\lVert \mathbf{x} \rVert \, \lVert \mathbf{y} \rVert}$$</p>
                <p>The numerator adds the products of matching attributes. The denominator is the product of the two lengths. For scaled items, $\lVert \hat{\mathbf{x}} - \hat{\mathbf{y}} \rVert^2 = 2\,(1 - \cos)$, so plain distance follows cosine.</p>
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
                <br>
                <p>The outer sum runs over the $k$ groups. The inner sum runs over the items of one group. $C_j$ is the set of items in group $j$. $\boldsymbol{\mu}_j$ is the mean of those items, the centre. Each term is the squared distance from an item to its centre.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Lloyd steps <a href="https://doi.org/10.1109/TIT.1982.1056489" target="_blank" rel="noopener noreferrer">(Lloyd, 1982)</a></b></p>
                <ol>
                    <li><p>Place $k$ centres</p></li>
                    <li>Assign each item to the closest centre</li>
                    <li>Move each centre to the mean of its items</li>
                    <li>Repeat 2 and 3 until nothing changes</li>
                </ol>
                <p><b>k-means++</b> picks each next starting centre far from those already picked <a href="https://dl.acm.org/doi/10.5555/1283383.1283494" target="_blank" rel="noopener noreferrer">(Arthur &amp; Vassilvitskii, 2007)</a>.</p>
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
                    <li>Five items on one attribute</li>
                    <li>A = 1, B = 2, C = 3, D = 8, E = 9</li>
                    <li><p>$k = 2$, starting centres at 1 and 9</p></li>
                </ul>
                <br>
                <p>A, B and C are closer to 1. D and E are closer to 9. The centres move to the means, 2 and 8.5. Assigning again changes nothing, so the steps stop.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>$$J = (1-2)^2 + 0^2 + (3-2)^2 + (8-8.5)^2 + (9-8.5)^2 = 2.5$$</p>
                <br>
                <p>Each term is the squared distance of one item to its centre. The first three terms are the group around 2, the last two the group around 8.5. Any other split of these five items into two groups gives a larger $J$.</p>
            </div>
        </div>
    </div>
</div>

## k-means

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 55%">
                <p><b>Choosing k</b></p>
                <ul>
                    <li><p>A short range of $k$, set before the results</p></li>
                    <li><p>One run of k-means for each $k$</p></li>
                    <li><p>$J$ always falls as $k$ grows, so $J$ alone cannot choose</p></li>
                    <li><p>Evaluation compares the values of $k$ with the silhouette. When none stands out, $k$ is chosen for the use, and we say so</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 45%">
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
                <p><b>Limits</b></p>
                <ul>
                    <li>Groups come out round and of similar spread</li>
                    <li>Every item is forced into a group</li>
                    <li>Another start can give other groups</li>
                    <li>The number of groups is ours, not the data's</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/k-means-versus-k-medoids.png" alt="k-means on groups that are not round" style="height: 360px">
                <div class="footnote">K-means versus k-medoids - Agor153, CC BY-SA 3.0 <https://creativecommons.org/licenses/by-sa/3.0>, via Wikimedia Commons</div>
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
for each k in the range set before the results
    place k centres with k-means++
    repeat
        assign each item to its closest centre
        move each centre to the mean of its items
    until nothing changes
    keep the run of this k for Evaluation
```

            </div>
            <div class="column vertical-middle text-left" style="width: 5%">
            </div>
            <div class="column vertical-middle text-left" style="width: 47.5%">

```python
from sklearn.cluster import KMeans
from sklearn.preprocessing import normalize

def kmeans_range(X, ks, seed):
    X = normalize(X)
    return {k: KMeans(n_clusters=k, n_init=10,
                      random_state=seed).fit(X)
            for k in ks}

models = kmeans_range(X, range(2, 9), seed=0)
```

            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
