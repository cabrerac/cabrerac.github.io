<!-- SLIDES: -->

## HDBSCAN

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Groups as dense regions</b></p>
                <ul>
                    <li>A group is a place where items are packed together</li>
                    <li>Items in thin regions are noise</li>
                    <li><p>No $k$ to choose</p></li>
                    <li>Groups can have any shape <a href="https://cdn.aaai.org/KDD/1996/KDD96-037.pdf" target="_blank" rel="noopener noreferrer">(Ester et al., 1996)</a></li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/dbscan-illustration.svg" alt="Core points, border points and noise" style="height: 300px">
                <div class="footnote">DBSCAN-Illustration - Chire, CC BY-SA 3.0 <https://creativecommons.org/licenses/by-sa/3.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## HDBSCAN

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p><b>Core distance and mutual reachability</b> <a href="https://doi.org/10.1007/978-3-642-37456-2_14" target="_blank" rel="noopener noreferrer">(Campello et al., 2013)</a></p>
                <p>$$\text{core}(a) = \text{distance from } a \text{ to its } m\text{-th nearest item}$$</p>
                <p>$$d_{\text{mreach}}(a, b) = \max\{\text{core}(a),\ \text{core}(b),\ d(a, b)\}$$</p>
                <ul>
                    <li><p>$m$ is min_samples</p></li>
                    <li><p>In a dense region this is just $d(a,b)$</p></li>
                    <li><p>In a thin region items are pushed apart</p></li>
                </ul>
            </div>
        </div>
    </div>
</div>

## HDBSCAN

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>From distances to a tree</b></p>
                <ol>
                    <li><p>Join all items with a minimum spanning tree on $d_{\text{mreach}}$</p></li>
                    <li>Cut its longest edges one by one</li>
                    <li>Each cut can split a group in two, or drop a few items</li>
                    <li>A split counts only when both parts have at least min_cluster_size items</li>
                    <li>The result is a tree of groups over all densities</li>
                </ol>
            </div>
        </div>
    </div>
</div>

## HDBSCAN

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Stability and noise</b></p>
                <ul>
                    <li>A group is stable when it lives across a wide range of densities</li>
                    <li>HDBSCAN keeps the most stable groups in the tree</li>
                    <li>Items in no kept group get the label -1, noise</li>
                    <li>Noise is a result, a list of items that fit no group</li>
                </ul>
                <p><a href="https://doi.org/10.21105/joss.00205" target="_blank" rel="noopener noreferrer">(McInnes et al., 2017)</a></p>
            </div>
        </div>
    </div>
</div>

## HDBSCAN

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Two parameters</b></p>
                <ul>
                    <li><b>min_cluster_size</b> - the smallest group we accept</li>
                    <li><b>min_samples</b> - how many neighbours make a point core</li>
                    <li>A larger min_samples marks more items as noise</li>
                    <li>A good min_cluster_size is the smallest group you would accept as a finding</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Preparation</b></p>
                <ul>
                    <li>Density needs distances that mean something</li>
                    <li>On all word columns, almost every item looks alone</li>
                    <li>So HDBSCAN runs on a few SVD directions</li>
                    <li>With cosine distance, given as a precomputed matrix</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## HDBSCAN

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 35%">
                <p><b>Python</b></p>
                <ul>
                    <li>Cosine distances on the SVD directions</li>
                    <li>The smallest group we accept</li>
                    <li>Label -1 is noise</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 65%">


```python
from sklearn.cluster import HDBSCAN
from sklearn.metrics import pairwise_distances

distances = pairwise_distances(Z, metric="cosine")
hdb = HDBSCAN(min_cluster_size=FLOOR, min_samples=MIN_SAMPLES,
              metric="precomputed", copy=True).fit(distances)
hdbscan_labels = hdb.labels_    # -1 is noise
n_groups = hdbscan_labels.max() + 1
noise = (hdbscan_labels == -1).mean()
print(n_groups, round(noise, 2))
```

            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
