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
                <p>The silhouette shows how much closer an item is to its own group than to the nearest other group.</p>
                <br>
                <p><b>Silhouette <a href="https://doi.org/10.1016/0377-0427(87)90125-7" target="_blank" rel="noopener noreferrer">(Rousseeuw, 1987)</a></b></p>
                <br>
                <p>$$s(i) = \frac{b(i) - a(i)}{\max\{a(i),\, b(i)\}}$$</p>
                <br>
                <p>$a(i)$ is the mean distance from item $i$ to the other items of its own group. $b(i)$ is the mean distance to the items of the nearest other group. The silhouette of a result is the mean over all items, between $-1$ and $1$. For HDBSCAN it leaves out the noise.</p>
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
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>Five items on one attribute. C is the item we score. A and B share its group. D and E are the other group.</p>
                <br>
                <p>$$A = 1,\: B = 2,\: C = 3,\: D = 8,\: E = 9$$</p>
                <br>
                <p><b>1. Own group.</b> C is 2 from A and 1 from B, so $a(C) = (2 + 1) / 2 = 1.5$.</p>
                <br>
                <p><b>2. Nearest other group.</b> C is 5 from D and 6 from E, so $b(C) = (5 + 6) / 2 = 5.5$.</p>
                <br>
                <p><b>3. Silhouette.</b> $s(C) = (5.5 - 1.5) / 5.5 = 0.73$. C is closer to its own group.</p>
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
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>$$s = \frac{1}{n} \sum_{i=1}^{n} s(i)$$</p>
                <br>
                <p>$s$ is the mean of items scores for a group. Run k-means, each $k$ is scored by $s$, the mean of its item silhouettes. The highest mean wins, keep that $k$.</p>
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
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>$$s = \frac{1}{n} \sum_{i=1}^{n} s(i)$$</p>
                <br>
                <p>Reading the silhouette <a href="https://doi.org/10.1002/9780470316801" target="_blank" rel="noopener noreferrer">(Kaufman &amp; Rousseeuw, 1990)</a></p>
                <ul>
                    <li><b>Above 0.70:</b> strong structure</li>
                    <li><b>0.51 to 0.70:</b> reasonable structure</li>
                    <li><b>0.26 to 0.50:</b> weak, could be artificial</li>
                    <li><b>0.25 or below:</b> no substantial structure</li>
                </ul>
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
            <div class="column vertical-middle text-left" style="width: 47.5%">

```text
for each k we are willing to try
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
                <p>Read means a person who knows the field keeps that group.</p>
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
                <p><b>1. All three.</b> A and B are read by every method, so they are a stronger candidate.</p>
                <p><b>2. k-means only.</b> C and D are read by k-means alone, so they may be forced into a group.</p>
                <p><b>3. Noise.</b> E fits no group. HDBSCAN marks it as noise, and it is worth a look.</p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
