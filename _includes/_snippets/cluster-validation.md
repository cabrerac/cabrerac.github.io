<!-- SLIDES: -->

## Judging Groups

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p>Groups found without labels are <b>judged</b> against chance, against other runs and against people who know the field, because there is no answer key.</p>
            </div>
        </div>
    </div>
</div>

## Judging Groups

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>No labels to check against</b></p>
                <ul>
                    <li><b>Silhouette</b> - compare it with a shuffled baseline</li>
                    <li><b>Stability</b> - rerun with other seeds</li>
                    <li><b>Agreement</b> - do different methods find the same groups</li>
                    <li><b>Noise share</b> - how many items fit no group</li>
                    <li><b>Top words</b> - can someone in the field name each group</li>
                </ul>
                <p>Weak structure is a finding, not something to hide.</p>
            </div>
        </div>
    </div>
</div>

## Judging Groups

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Weak structure is a finding</b></p>
                <p>A silhouette near 1 says each item is much closer to its group than to any other.</p>
                <p>A silhouette near 0 says many items sit halfway between two groups.</p>
                <p>That is not a bug in the code. It is a fact about the data.</p>
                <p>Texts on one topic share many words, and their subtopics mix.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>How much to trust the groups</b></p>
                <ul>
                    <li><b>Baseline</b> - is the silhouette above the 95th percentile of shuffled data, and by how much</li>
                    <li><b>Stability</b> - do the groups survive a new seed</li>
                    <li><b>Noise</b> - how many items have no clear neighbours</li>
                    <li>A weak group is not useless. It says: do not decide with one group alone</li>
                </ul>
                <p>What would change it: another k, another floor, another preparation such as TF-IDF, or a question that asks for broader groups.</p>
            </div>
        </div>
    </div>
</div>

## Judging Groups

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 36%">
                <p><b>Shuffled baseline</b></p>
                <p>Each word keeps its number of items.</p>
                <p>Its items are drawn at random.</p>
                <p>Real silhouette against the 95th percentile of the shuffled silhouettes, read as in Lecture 2.</p>
                <p>Unlike a swap null, item length is not kept. Rows have length 1, so the mix of words is compared.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 64%">


```python
import numpy as np

rng = np.random.default_rng(SEED)
dense = counts.toarray()
shuffled_silhouettes = []
for _ in range(N_SHUFFLES):
    # each word stays in the same number of items, at random
    X_shuffled = normalize(np.apply_along_axis(rng.permutation, 0, dense))
    km_shuffled = KMeans(n_clusters=K_CHOSEN, n_init=10,
                         random_state=SEED).fit(X_shuffled)
    shuffled_silhouettes.append(silhouette_score(X_shuffled, km_shuffled.labels_, metric="cosine"))
print(round(silhouettes[K_CHOSEN], 3), round(p95(shuffled_silhouettes), 3))
```

            </div>
        </div>
    </div>
</div>

## Judging Groups

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Adjusted Rand index</b> <a href="https://doi.org/10.1007/BF01908075" target="_blank" rel="noopener noreferrer">(Hubert &amp; Arabie, 1985)</a></p>
                <ul>
                    <li>Takes two labelings of the same items</li>
                    <li>Counts pairs put together, or apart, by both</li>
                    <li>1 means the same groups, 0 means agreement at chance level</li>
                    <li>Same method, other seeds, gives stability</li>
                    <li>Two methods give agreement, leaving out the noise items</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Judging Groups

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 35%">
                <p><b>Python</b></p>
                <ul>
                    <li>Five seeds for k-means, all 10 pairs</li>
                    <li>Three pairs of methods</li>
                    <li>Noise left out of the comparison</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 65%">


```python
from itertools import combinations
from sklearn.metrics import adjusted_rand_score

seed_labels = [KMeans(n_clusters=K_CHOSEN, n_init=10, random_state=s).fit(X).labels_
               for s in range(5)]
seed_ari = [adjusted_rand_score(a, b) for a, b in combinations(seed_labels, 2)]

in_group = hdbscan_labels != -1
agreement = {
    "k-means, mixture": adjusted_rand_score(kmeans_labels, mixture_labels),
    "k-means, HDBSCAN": adjusted_rand_score(kmeans_labels[in_group], hdbscan_labels[in_group]),
    "mixture, HDBSCAN": adjusted_rand_score(mixture_labels[in_group], hdbscan_labels[in_group]),
}
print(round(min(seed_ari), 2), round(np.mean(seed_ari), 2))
print({pair: round(ari, 2) for pair, ari in agreement.items()})
```

            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
