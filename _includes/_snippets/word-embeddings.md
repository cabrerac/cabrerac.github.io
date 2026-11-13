<!-- SLIDES: -->

## Item Vectors

<div class="rows" style="height: 100%">
    <div class="row" style="height: 70%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img class="external-svg" src="{{ site.url }}/assets/media/diagrams/pattern-task-taxonomy.svg" alt="Taxonomy of pattern methods" style="width: 100%; height: 100%">
            </div>
        </div>
    </div>
    <div class="row" style="height: 30%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <p><b>Frequent itemsets:</b> sets that occur in many transactions, found by counting.</p>
                <p><b>Interestingness:</b> a score that compares a count with chance.</p>
                <p><b>Sequential patterns:</b> patterns that keep the order of the items.</p>
                <p><b>Item vectors:</b> sets that have similar meaning in a learned space.</p>
            </div>
        </div>
    </div>
</div>

## Item Vectors

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p>An <b>item vector</b> places each item in a space learned from a large collection, so that items used in similar situations get close vectors.</p>
            </div>
        </div>
    </div>
</div>

## Item Vectors

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>The count says the two items appear together and closeness asks whether the meaning of these two are close. The cosine similarity tells us how close are the vectorial representation of these items. A high cosine means the items are related.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/word-vector-illustration.jpg" alt="Word vectors" style="height: auto">
                <div class="footnote">Word vector illustration - Singerep, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Item Vectors

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>A word is described by the words around it <a href="https://doi.org/10.1080/00437956.1954.11659520" target="_blank" rel="noopener noreferrer">(Harris, 1954, p. 156)</a>. Words with similar neighbours get similar vectors. The same training on receipts learns a vector per product, from the products around it.</p>
                <br>
                <p>"Difference of meaning correlates with difference of distribution." <a href="https://doi.org/10.1080/00437956.1954.11659520" target="_blank" rel="noopener noreferrer">(Harris, 1954)</a></p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/word-vector-illustration.jpg" alt="Word vectors" style="height: auto">
                <div class="footnote">Word vector illustration - Singerep, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Item Vectors

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>Cosine compares the direction of two item vectors.</p>
                <br>
                <p>$$\cos(\mathbf{u}, \mathbf{v}) = \frac{\mathbf{u} \cdot \mathbf{v}}{\lVert \mathbf{u} \rVert \, \lVert \mathbf{v} \rVert}$$</p>
                <br>
                <p>$\mathbf{u}$ and $\mathbf{v}$ are the two vectors. The numerator is their dot product. The denominator is the product of their lengths. Dividing removes the lengths, so only the angle remains.</p>
                <ul>
                    <li><b>Close to 1:</b> the items are used in similar ways</li>
                    <li><b>Close to 0:</b> no relation</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/cosine-similarity.png" alt="Cosine similarity" style="height: 300px">
                <div class="footnote">CosineSimilarity - StandingFuture, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Item Vectors

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>The cosine similarity of two items must be greater than the 95th percentile of $N$ random pairs.</p>
                <p>Each pair is drawn from the items that have a vector. The cosines are sorted from smallest to largest. The cut is the cosine that leaves 95 of every 100 random pairs behind it.</p>
                <p>Only a pair that passed the support floor is compared with the cut. Closeness keeps the pair when its cosine is higher than the cut.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/cosine-similarity.png" alt="Cosine similarity" style="height: 300px">
                <div class="footnote">CosineSimilarity - StandingFuture, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Item Vectors

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 47.5%">

```text
for each pair kept by support
    if either item has no vector
        cosine is missing
    else if both items share one stored vector
        cosine is missing
    else
        make each vector length 1
        cosine = dot product of the two vectors
```

            </div>
            <div class="column vertical-middle text-left" style="width: 5%">
            </div>
            <div class="column vertical-middle text-left" style="width: 47.5%">

```python
import numpy as np

def unit_vector(item, vectors):
    vector = vectors[item]
    return vector / np.linalg.norm(vector)

def pair_cosine(a, b, vectors):
    if a not in vectors or b not in vectors:
        return float("nan")
    if vectors[a].tobytes() == vectors[b].tobytes():
        return float("nan")
    return float(unit_vector(a, vectors) @ unit_vector(b, vectors))

cosines = {
    pair: pair_cosine(a, b, vectors)
    for (a, b) in candidates
}
```

            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
