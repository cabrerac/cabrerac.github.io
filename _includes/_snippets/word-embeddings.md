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
                <p><b>Item vectors:</b> one vector per item, so closeness is a score.</p>
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
                <p>Counts only see this collection.</p>
                <p>Two items that play the same role may rarely share a transaction.</p>
                <ul>
                    <li>Products that substitute for each other</li>
                    <li>Codes that mark the same event</li>
                    <li>Words such as car and automobile</li>
                </ul>
                <p>A vector learned from a larger collection can still place them near each other.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/cosine-similarity.png" alt="Cosine similarity" style="height: 320px">
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
                <p>A word is described by the words around it <a href="https://doi.org/10.1080/00437956.1954.11659520" target="_blank" rel="noopener noreferrer">(Harris, 1954, p. 156)</a>.</p>
                <p>Words with similar neighbours get similar vectors.</p>
                <p>The same training on receipts learns a vector per product, from the products around it.</p>
                <br>
                <p>"Difference of meaning correlates with difference of distribution." <a href="https://doi.org/10.1080/00437956.1954.11659520" target="_blank" rel="noopener noreferrer">(Harris, 1954)</a></p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/word-vector-illustration.jpg" alt="Word vectors" style="height: 380px">
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
                <p>Skip-gram takes a word and predicts its neighbours.</p>
                <p>The weights learned for each word are its vector.</p>
                <br>
                <p>"We propose two novel model architectures for computing continuous vector representations of words from very large data sets." <a href="https://arxiv.org/abs/1301.3781" target="_blank" rel="noopener noreferrer">(Mikolov et al., 2013)</a></p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/skip-gram.svg" alt="Skip-gram model" style="height: 360px">
                <div class="footnote">Skip-gram - Zhang, Lipton, Li, and Smola, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons</div>
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
                    <li><b>Below 0:</b> rare, and usually weak</li>
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
                <img src="{{ site.url }}/assets/media/images/word-vector-illustration.jpg" alt="Word vectors" style="height: 380px">
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
                <p>Some tables store one vector for many items.</p>
                <p>Those items get a cosine of 1. That is not a pattern.</p>
                <p>Read those pairs apart from the rest.</p>
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
                <p>Vectors learn the habits of the collection they were trained on.</p>
                <ul>
                    <li>"Man is to Computer Programmer as Woman is to Homemaker?" <a href="https://arxiv.org/abs/1607.06520" target="_blank" rel="noopener noreferrer">(Bolukbasi et al., 2016)</a></li>
                    <li>Word vectors carry human-like biases <a href="https://doi.org/10.1126/science.aal4230" target="_blank" rel="noopener noreferrer">(Caliskan et al., 2017)</a></li>
                    <li>A close pair can reflect that training collection</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/skip-gram.svg" alt="Skip-gram model" style="height: 360px">
                <div class="footnote">Skip-gram - Zhang, Lipton, Li, and Smola, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons</div>
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
