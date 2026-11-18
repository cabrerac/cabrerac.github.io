<!-- SLIDES: -->

## HDBSCAN

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

## HDBSCAN

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p><b>HDBSCAN</b> finds groups as dense regions of items and leaves the items in thin regions out as noise.</p>
            </div>
        </div>
    </div>
</div>

## HDBSCAN

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Groups as dense regions</b></p>
                <ul>
                    <li><p>A group is a place where items are packed together</p></li>
                    <li><p>Items in thin regions are noise</p></li>
                    <li><p>There is no $k$ to choose</p></li>
                    <li><p>Groups can have any shape <a href="https://dl.acm.org/doi/10.5555/3001460.3001507" target="_blank" rel="noopener noreferrer">(Ester et al., 1996)</a></p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/dbscan-illustration.svg" alt="Core points, border points and noise" style="height: 360px">
                <div class="footnote">DBSCAN-Illustration - Chire, CC BY-SA 3.0 <https://creativecommons.org/licenses/by-sa/3.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## HDBSCAN

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Core distance and mutual reachability <a href="https://doi.org/10.1007/978-3-642-37456-2_14" target="_blank" rel="noopener noreferrer">(Campello et al., 2013)</a></b></p>
                <p>$$\text{core}(a) = d(a, a_m)$$</p>
                <p>$$d_{\text{mreach}}(a, b) =$$</p>
                <p>$$\max\{\text{core}(a),\ \text{core}(b),\ d(a, b)\}$$</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>$a_m$ is the $m$-th nearest item to $a$, and $m$ is min_samples. $d$ is the plain distance.</p>
                <p>In a dense region the core distances are small, so this is just $d(a, b)$.</p>
                <p>In a thin region it is large, so items there are pushed apart.</p>
                <p><b>Preparation:</b> cosine distance on 10 SVD directions.</p>
            </div>
        </div>
    </div>
</div>

## HDBSCAN

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <ul>
                    <li>Six items on one attribute</li>
                    <li>A = 1, B = 2, C = 3, D = 8, E = 9, F = 20</li>
                    <li>min_samples = 2, the item and its nearest neighbour</li>
                    <li>min_cluster_size = 2</li>
                </ul>
                <p>Each core distance is 1, except F, which is 11 away from E.</p>
                <p>The longest edge, 11, is cut first and leaves F alone, so F is noise. The next, 5, leaves A, B, C and D, E. Two groups and one noise item.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/diagrams/hdbscan-six-items.svg" alt="Edges, cuts and result of HDBSCAN on six items" style="height: 380px">
            </div>
        </div>
    </div>
</div>

## HDBSCAN

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Two parameters, set before the results</b></p>
                <ul>
                    <li><b>min_cluster_size:</b> FLOOR, the smallest group we accept, the support floor of Lecture 2</li>
                    <li><b>min_samples:</b> MIN_SAMPLES = 5, how many neighbours make an item core</li>
                </ul>
                <p><b>Limits</b></p>
                <ul>
                    <li><b>Thin groups:</b> a group thinner than the rest ends up as noise</li>
                    <li><b>Noise:</b> a list of items that fit no group, for a look, not deleted</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/dbscan-illustration.svg" alt="Core points, border points and noise" style="height: 360px">
                <div class="footnote">DBSCAN-Illustration - Chire, CC BY-SA 3.0 <https://creativecommons.org/licenses/by-sa/3.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## HDBSCAN

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 47.5%">

```text
use the 10 SVD directions
cosine distance between every two items
core distance of each item from min_samples
mutual reachability between every two items
tree of the items, longest edges cut first
keep a split when both parts reach min_cluster_size
keep the groups that last over the most cuts
label -1 for the items in no kept group
```

            </div>
            <div class="column vertical-middle text-left" style="width: 5%">
            </div>
            <div class="column vertical-middle text-left" style="width: 47.5%">

```python
from sklearn.cluster import HDBSCAN
from sklearn.metrics import pairwise_distances

distances = pairwise_distances(Z, metric="cosine")
hdbscan_labels = HDBSCAN(
    min_cluster_size=FLOOR, min_samples=MIN_SAMPLES,
    metric="precomputed", copy=True,
).fit(distances).labels_
```

            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
