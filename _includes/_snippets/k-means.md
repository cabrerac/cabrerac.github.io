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
                    <li>Each group has a centre</li>
                    <li>Each item goes to its closest centre</li>
                    <li>Move the centres, repeat</li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 55%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/k-means-convergence.gif" alt="k-means moving its centres" style="height: 400px">
                <div class="footnote">K-means convergence - Chire, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## k-means

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <p><b>What k-means minimises</b></p>
                <p>$$J = \sum_{j=1}^{k} \sum_{i \in C_j} \lVert \mathbf{x}_i - \boldsymbol{\mu}_j \rVert^2$$</p>
                <p>$C_j$ is the set of items in group $j$.</p>
                <p>$\boldsymbol{\mu}_j$ is the mean of those items.</p>
                <p>Small $J$ means items sit near their centre.</p>
            </div>
        </div>
    </div>
</div>

## k-means

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <p><b>Lloyd steps</b> <a href="https://doi.org/10.1109/TIT.1982.1056489" target="_blank" rel="noopener noreferrer">(Lloyd, 1982)</a></p>
                <ol>
                    <li><p>Place $k$ centres</p></li>
                    <li>Assign each item to the closest centre</li>
                    <li>Move each centre to the mean of its items</li>
                    <li>Repeat 2 and 3 until nothing changes</li>
                </ol>
                <p><b>k-means++</b> <a href="https://dl.acm.org/doi/10.5555/1283383.1283494" target="_blank" rel="noopener noreferrer">(Arthur &amp; Vassilvitskii, 2007)</a></p>
                <p>Pick the first centre at random.</p>
                <p>Pick each next one far from those already picked.</p>
                <p>Run several starts and keep the lowest $J$.</p>
            </div>
        </div>
    </div>
</div>

## k-means

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <p><b>Silhouette</b> <a href="https://doi.org/10.1016/0377-0427(87)90125-7" target="_blank" rel="noopener noreferrer">(Rousseeuw, 1987)</a></p>
                <p>$$s(i) = \frac{b(i) - a(i)}{\max\{a(i),\, b(i)\}}$$</p>
                <ul>
                    <li><p>$a(i)$ is the mean distance to items in its own group</p></li>
                    <li><p>$b(i)$ is the mean distance to items in the nearest other group</p></li>
                    <li><p>Close to 1, well placed. Close to 0, on a border. Below 0, likely in the wrong group</p></li>
                    <li><p>The score of a result is the mean over all items</p></li>
                </ul>
            </div>
        </div>
    </div>
</div>

## k-means

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Choosing k</b></p>
                <ul>
                    <li><p>Run k-means for a short range of $k$</p></li>
                    <li>Compute the silhouette for each one</li>
                    <li><p>A clear peak suggests a natural $k$</p></li>
                    <li><p>A flat, low line means there is no natural $k$</p></li>
                    <li><p>Then $k$ is chosen for the use, and we say so</p></li>
                </ul>
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
                <p>Groups come out round and of similar spread.</p>
                <p>Every item is forced into a group.</p>
                <p>A different start can give different groups.</p>
                <p>The number of groups is ours, not the data's.</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/k-means-versus-k-medoids.png" alt="k-means on groups that are not round" style="height: 380px">
                <div class="footnote">K-means versus k-medoids - Agor153, CC BY-SA 3.0 <https://creativecommons.org/licenses/by-sa/3.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## k-means

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 35%">
                <p><b>Python</b></p>
                <ul>
                    <li><p>One run per $k$ in the range</p></li>
                    <li>Silhouette with cosine</li>
                    <li>Fixed seed so the run repeats</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 65%">


```python
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

silhouettes = {}
for k in K_CANDIDATES:
    km = KMeans(n_clusters=k, n_init=10, random_state=SEED).fit(X)
    silhouettes[k] = silhouette_score(X, km.labels_, metric="cosine")
print({k: round(s, 3) for k, s in silhouettes.items()})
K_CHOSEN = max(silhouettes, key=silhouettes.get)   # or a k chosen for the use
```

            </div>
        </div>
    </div>
</div>

## k-means

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 35%">
                <p><b>Reading a group</b></p>
                <p>The centre weights each word.</p>
                <p>Its top words name the group.</p>
                <p>Size next to the words.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 65%">


```python
vocabulary = vectorizer.get_feature_names_out()
kmeans = KMeans(n_clusters=K_CHOSEN, n_init=10, random_state=SEED).fit(X)
kmeans_labels = kmeans.labels_
for g, centre in enumerate(kmeans.cluster_centers_):
    top = centre.argsort()[::-1][:8]
    print(g, (kmeans_labels == g).sum(), list(vocabulary[top]))
```

            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
