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
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Partitioning:</b> every item goes to one of $k$ groups around centres.</p>
                <p><b>Model-based:</b> each group is a probability distribution, so membership is a probability.</p>
                <p><b>Density-based:</b> groups are dense regions, and items in thin regions are noise.</p>
                <p><b>Hierarchical:</b> a tree of groups inside groups, cut at a chosen level.</p>
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
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Preparation: distances that mean something</b></p>
                <p>Density needs distances that tell near from far.</p>
                <ul>
                    <li>With many attributes, the nearest and the farthest item end up at almost the same distance <a href="https://doi.org/10.1007/3-540-49257-7_15" target="_blank" rel="noopener noreferrer">(Beyer et al., 1999)</a></li>
                    <li>Then almost every item looks alone</li>
                    <li>So HDBSCAN runs on the same few SVD directions as the mixture, with cosine distance</li>
                </ul>
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
                <p>$$\text{core}(a) = \text{distance from } a \text{ to its } m\text{-th nearest item}$$</p>
                <p>$$d_{\text{mreach}}(a, b) = \max\{\text{core}(a),\ \text{core}(b),\ d(a, b)\}$$</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>$m$ is min_samples, set before the results. $d(a, b)$ is the plain distance between two items. The maximum takes the largest of the three numbers.</p>
                <br>
                <p>In a dense region the core distances are small, so this is just $d(a,b)$. In a thin region the core distance is large, so items there are pushed apart.</p>
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
                    <li>A group is stable when it lives across a wide range of cuts. HDBSCAN keeps the most stable groups <a href="https://doi.org/10.21105/joss.00205" target="_blank" rel="noopener noreferrer">(McInnes et al., 2017)</a></li>
                    <li>Items in no kept group get the label -1, noise</li>
                </ol>
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
                    <li><p>$m = 1$ and min_cluster_size = 2</p></li>
                </ul>
                <br>
                <p>Each core distance is 1, except F, whose nearest item is 11 away.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>$d_{\text{mreach}}(E, F) = \max\{1, 11, 11\} = 11$, the longest edge. Cutting it leaves F alone, fewer than 2 items, so F is noise.</p>
                <br>
                <p>$d_{\text{mreach}}(C, D) = \max\{1, 1, 5\} = 5$, the next edge. Cutting it leaves A, B, C and D, E, both with at least 2 items. Two groups and one noise item.</p>
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
                    <li><b>min_cluster_size:</b> the smallest group we would accept as a finding</li>
                    <li><b>min_samples:</b> how many neighbours make an item core</li>
                    <li>A larger min_samples marks more items as noise</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Limits</b></p>
                <ul>
                    <li>Groups thinner than the rest end up as noise</li>
                    <li>A large noise share can hide a real group</li>
                    <li>Noise is a result, a list of items that fit no group</li>
                </ul>
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
use the same few SVD directions
cosine distance between every two items
core distance of each item from min_samples
mutual reachability between every two items
minimum spanning tree, longest edges cut first
keep a split when both parts reach min_cluster_size
keep the most stable groups
label -1 for the items in no kept group
```

            </div>
            <div class="column vertical-middle text-left" style="width: 5%">
            </div>
            <div class="column vertical-middle text-left" style="width: 47.5%">

```python
from sklearn.cluster import HDBSCAN
from sklearn.metrics import pairwise_distances

def density_groups(Z, min_cluster_size, min_samples):
    distances = pairwise_distances(Z, metric="cosine")
    model = HDBSCAN(min_cluster_size=min_cluster_size,
                    min_samples=min_samples,
                    metric="precomputed")
    return model.fit_predict(distances)

labels = density_groups(Z, min_cluster_size=10,
                        min_samples=5)
noise_share = (labels == -1).mean()
```

            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
