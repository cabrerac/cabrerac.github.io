<!-- SLIDES: -->

## Item Vectors

<div class="rows" style="height: 100%">
    <div class="row" style="height: 52%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img class="external-svg" src="{{ site.url }}/assets/media/diagrams/pattern-task-taxonomy.svg" alt="Taxonomy of pattern methods" style="width: 100%; height: 100%">
            </div>
        </div>
    </div>
    <div class="row" style="height: 48%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <p><b>Frequent itemsets:</b> sets that occur in many transactions, found by counting.</p>
                <p>FP-growth finds them from a compressed tree of the transactions.</p>
                <p>Eclat finds them by intersecting each item's list of transactions.</p>
                <p><b>Interestingness:</b> a score on a pair beyond the raw count.</p>
                <p>Confidence is the share of the first item's transactions that also hold the second.</p>
                <p>Conviction is high when the first item rarely appears without the second, more rarely than chance.</p>
                <p><b>Sequential patterns:</b> patterns that keep the order of the items.</p>
                <p>GSP builds candidate sequences.</p>
                <p>PrefixSpan grows a sequence from its prefix.</p>
                <p>SPADE intersects lists of sequence ids.</p>
                <p><b>Item vectors:</b> one vector per item in a learned space, so items used alike lie close.</p>
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
                <p>The count says the two words share these abstracts.</p>
                <p>Closeness asks whether those two meanings are close.</p>
                <p>The cosine is measured for a pair that is already in the abstracts.</p>
                <p>A high cosine means the abstract brings two related meanings together.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>health + years</b> share 81 abstracts.</p>
                <p>The model does not place them close.</p>
                <br>
                <p><b>diabetes + obesity</b> share 19 abstracts.</p>
                <p>The model places them close.</p>
                <p>That is a reason to read the abstract.</p>
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
                <p>The cut is the 95th percentile of 1,000 random pairs.</p>
                <p>Each pair is drawn from the words the model knows.</p>
                <p>A pair that shares one stored list is left out.</p>
                <p>The cosines are sorted from smallest to largest.</p>
                <p>The cut is the cosine that leaves 95 of every 100 random pairs behind it.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>Only a pair that passed the support floor is compared with the cut.</p>
                <p>Closeness keeps the pair when its cosine is higher than the cut.</p>
                <p>On these abstracts the cut is 0.46.</p>
                <p><b>diabetes + obesity</b> is 0.78, so closeness keeps it.</p>
                <p><b>health + years</b> is 0.31, so closeness leaves it out.</p>
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
                <p>Each item has to be in the vector table.</p>
                <ul>
                    <li>The table has its own list of items</li>
                    <li>An item with no vector has no cosine</li>
                    <li>That item still has a support and a lift</li>
                    <li>The vectors come from another collection</li>
                </ul>
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

## Item Vectors

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p>Each pair that closeness keeps gives one point to every abstract that contains both words.</p>
                <p>The reading list adds that point to the support point and the lift point.</p>
                <p>The abstracts with the highest total are the ones to read first, up to 30.</p>
                <p><b>food + nutrition</b> is above the cut and below the support floor, so it selects no abstract.</p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
