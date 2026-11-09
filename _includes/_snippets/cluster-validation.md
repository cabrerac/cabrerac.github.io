<!-- SLIDES: -->

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 55%">
                <p><b>No labels to check against</b></p>
                <ul>
                    <li><b>Silhouette:</b> how well each item sits in its group, against a shuffled baseline</li>
                    <li><b>Stability:</b> the same method with other seeds</li>
                    <li><b>Agreement:</b> do different methods find the same groups</li>
                    <li><b>Noise share:</b> how many items fit no group</li>
                    <li><b>Reading:</b> can someone in the field name each group</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 45%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/cluster-analysis-mouse.svg" alt="Three groups of points" style="height: 360px">
                <div class="footnote">ClusterAnalysis Mouse - Chire, Public domain, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Silhouette <a href="https://doi.org/10.1016/0377-0427(87)90125-7" target="_blank" rel="noopener noreferrer">(Rousseeuw, 1987)</a></b></p>
                <p>$$s(i) = \frac{b(i) - a(i)}{\max\{a(i),\, b(i)\}}$$</p>
                <p>$a(i)$ is the mean distance from item $i$ to the items of its own group. $b(i)$ is the mean distance to the items of the nearest other group. The denominator keeps the score between -1 and 1.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <ul>
                    <li><b>Close to 1:</b> the item sits well inside its group</li>
                    <li><b>Close to 0:</b> the item sits on a border</li>
                    <li><b>Below 0:</b> the item is likely in the wrong group</li>
                </ul>
                <br>
                <p>For item C of the k-means example, $a = (2 + 1)/2 = 1.5$ and $b = (5 + 6)/2 = 5.5$, so $s = 4 / 5.5 = 0.73$. The silhouette of a result is the mean over all items.</p>
            </div>
        </div>
    </div>
</div>

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 35%">
                <p><b>Python: silhouette for each k</b></p>
                <ul>
                    <li>One score per run of k-means</li>
                    <li><p>The highest score suggests a $k$</p></li>
                    <li><p>A flat, low line means there is no natural $k$</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 65%">

```python
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import normalize

X_scaled = normalize(X)
scores = {k: silhouette_score(X_scaled, model.labels_)
          for k, model in models.items()}
best_k = max(scores, key=scores.get)
```

            </div>
        </div>
    </div>
</div>

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>A shuffled table</b></p>
                <p>Chance must keep how often each attribute is used.</p>
                <ul>
                    <li>Each attribute keeps its values, shuffled across the items</li>
                    <li>The links between attributes break, so any structure left is chance</li>
                    <li>Run the same method on many shuffled tables and compute the silhouette</li>
                    <li>The real silhouette is worth a look when it is strictly above the 95th percentile of the shuffled ones</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 35%">
                <p><b>Python: shuffled silhouette</b></p>
                <ul>
                    <li>Each column shuffled on its own</li>
                    <li>The same k and the same seed as the real run</li>
                    <li>100 shuffled tables</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 65%">

```python
import numpy as np

def shuffled_silhouettes(X, k, n_shuffles, seed):
    rng = np.random.default_rng(seed)
    values = []
    for _ in range(n_shuffles):
        shuffled = np.apply_along_axis(rng.permutation, 0, X)
        shuffled = normalize(shuffled)
        model = KMeans(n_clusters=k, n_init=10,
                       random_state=seed).fit(shuffled)
        values.append(silhouette_score(shuffled, model.labels_))
    return values

null = shuffled_silhouettes(X, best_k, 100, seed=0)
beats_chance = scores[best_k] > np.percentile(null, 95)
```

            </div>
        </div>
    </div>
</div>

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Adjusted Rand index <a href="https://doi.org/10.1007/BF01908075" target="_blank" rel="noopener noreferrer">(Hubert &amp; Arabie, 1985)</a></b></p>
                <ul>
                    <li>Takes two labelings of the same items</li>
                    <li>Counts pairs put together, or apart, by both</li>
                    <li>1 means the same groups, 0 means agreement at chance level</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Stability and agreement</b></p>
                <ul>
                    <li><b>Stability:</b> the same method with other seeds</li>
                    <li><b>Agreement:</b> two methods, leaving out the noise items</li>
                </ul>
                <br>
                <p>Labels 1, 1, 2, 2 and 2, 2, 1, 1 give an index of 1. The groups are the same, only their names differ.</p>
            </div>
        </div>
    </div>
</div>

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 35%">
                <p><b>Python: stability and agreement</b></p>
                <ul>
                    <li>Every pair of five seeds</li>
                    <li>Noise left out of the comparison</li>
                    <li>The lowest and the mean index</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 65%">

```python
from itertools import combinations
from sklearn.metrics import adjusted_rand_score

def seed_stability(X, k, seeds):
    runs = [KMeans(n_clusters=k, n_init=10,
                   random_state=s).fit_predict(X)
            for s in seeds]
    return [adjusted_rand_score(a, b)
            for a, b in combinations(runs, 2)]

stability = seed_stability(X, best_k, range(5))
grouped = labels != -1
agreement = adjusted_rand_score(kmeans_labels[grouped],
                                labels[grouped])
```

            </div>
        </div>
    </div>
</div>

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Weak structure is a finding</b></p>
                <p>A silhouette near 0 says many items sit halfway between two groups.</p>
                <ul>
                    <li>That is a fact about the data, not a bug in the code</li>
                    <li>Items on one subject share many attributes, and their subtopics mix</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>How much to trust the groups</b></p>
                <ul>
                    <li><b>Baseline:</b> is the silhouette above the shuffled 95th percentile</li>
                    <li><b>Stability:</b> do the groups survive a new seed</li>
                    <li><b>Noise:</b> how many items have no clear neighbours</li>
                </ul>
                <p>A weak group says: do not decide with one group alone.</p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
