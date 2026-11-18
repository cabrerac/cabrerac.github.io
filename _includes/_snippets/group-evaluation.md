<!-- SLIDES: -->

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p><b>Evaluation</b> compares k-means, Gaussian mixtures, and HDBSCAN on the same items.</p>
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
                <p>$a(i)$ is the mean distance from item $i$ to the other items of its own group.</p>
                <p>$b(i)$ is the mean distance to the items of the nearest other group.</p>
                <p>The silhouette of a result is the mean over all items, between -1 and 1. For HDBSCAN it leaves out the noise.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/diagrams/silhouette-item-c.svg" alt="Silhouette of item C" style="height: 380px">
            </div>
        </div>
    </div>
</div>

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 45%">
                <p><b>Choosing k</b></p>
                <p>One run for each $k$ from 3 to 8. The highest silhouette wins, here $k = 8$, the edge of what we tried.</p>
                <p><b>Reading the silhouette <a href="https://doi.org/10.1002/9780470316801" target="_blank" rel="noopener noreferrer">(Kaufman &amp; Rousseeuw, 1990)</a></b></p>
                <ul>
                    <li><b>Above 0.70:</b> strong structure</li>
                    <li><b>0.51 to 0.70:</b> reasonable structure</li>
                    <li><b>0.26 to 0.50:</b> weak, could be artificial</li>
                    <li><b>0.25 or below:</b> no substantial structure</li>
                </ul>
                <p>Below 0.25, the groups are a reading aid, and we say so.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 55%">
                <img src="{{ site.url }}/assets/media/images/group-silhouette-by-k.png" alt="Silhouette for each k on the nutrition abstracts" style="width: 100%; height: auto">
            </div>
        </div>
    </div>
</div>

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 47.5%">

```text
for each k from 3 to 8
    silhouette of its k-means labels, cosine
choose the k with the highest silhouette
keep the labels of that k
```

            </div>
            <div class="column vertical-middle text-left" style="width: 5%">
            </div>
            <div class="column vertical-middle text-left" style="width: 47.5%">

```python
from sklearn.metrics import silhouette_score

silhouettes = {
    k: silhouette_score(X, labels, metric="cosine")
    for k, labels in kmeans_runs.items()}
K_CHOSEN = max(silhouettes, key=silhouettes.get)
kmeans_labels = kmeans_runs[K_CHOSEN]
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
                <p><b>The same items</b></p>
                <p>Read means the item is in a group where at least half the items contain a topic word.</p>
                <table class="table">
                    <thead>
                        <tr><th>Item</th><th>k-means</th><th>Gaussian mixture</th><th>HDBSCAN</th></tr>
                    </thead>
                    <tbody>
                        <tr><td>A, B</td><td>read</td><td>read</td><td>read</td></tr>
                        <tr><td>C, D</td><td>read</td><td>no</td><td>no</td></tr>
                        <tr><td>E</td><td>no</td><td>no</td><td>noise</td></tr>
                    </tbody>
                </table>
                <ul>
                    <li><b>All three:</b> A and B are a stronger candidate.</li>
                    <li><b>k-means only:</b> C and D may be forced into a group.</li>
                    <li><b>Noise:</b> E fits no group and is worth a look.</li>
                </ul>
                <p>An item that all three put in a read group is a stronger candidate.</p>
            </div>
        </div>
    </div>
</div>

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 80%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <img src="{{ site.url }}/assets/media/images/group-methods-panels.png" alt="Groups read, silhouette, and abstracts in read groups for k-means and HDBSCAN" style="width: 100%; height: auto">
            </div>
        </div>
    </div>
    <div class="row" style="height: 20%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p>The individual notebook runs k-means and HDBSCAN on 317 nutrition abstracts. A group is read when at least half of its abstracts contain a topic word. Both silhouettes are below 0.25, no substantial structure, so the groups are a reading aid.</p>
            </div>
        </div>
    </div>
</div>

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 66%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <img src="{{ site.url }}/assets/media/images/group-methods-panels.png" alt="Groups read, silhouette, and abstracts in read groups for k-means and HDBSCAN" style="height: 100%; width: auto; max-width: 100%">
            </div>
        </div>
    </div>
    <div class="row" style="height: 34%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>k-means:</b> 2 of 8 groups read, 56 abstracts, on diabetes care and cardiovascular risk. <b>HDBSCAN:</b> 1 of 5, 10 abstracts on diabetes care standards. <b>Both:</b> 9.<br><b>Not a fair race:</b> HDBSCAN's 0.10 leaves out its 108 noise abstracts (34%), which join no group. k-means' 0.075 counts all 317.</p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
