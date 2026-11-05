<!-- SLIDES: -->

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
            <div class="column vertical-middle text-left" style="width: 55%">
                <p><b>Counts only see this collection</b></p>
                <p>Two items that play the same role may rarely share a transaction.</p>
                <ul>
                    <li>Products that substitute for each other</li>
                    <li>Codes that mark the same event</li>
                    <li>Words such as car and automobile</li>
                </ul>
                <p>A vector learned from a larger collection can still place them near each other.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 45%">
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
                <p><b>The word case</b> <a href="https://doi.org/10.1080/00437956.1954.11659520" target="_blank" rel="noopener noreferrer">(Harris, 1954, p. 156)</a></p>
                <p>A word is described by the words around it.</p>
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
                <p><b>Skip-gram, the word case</b></p>
                <p>Take a word and predict its neighbours.</p>
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
                <p><b>Cosine similarity</b></p>
                <p>$$\cos(\mathbf{u}, \mathbf{v}) = \frac{\mathbf{u} \cdot \mathbf{v}}{\lVert \mathbf{u} \rVert \, \lVert \mathbf{v} \rVert}$$</p>
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
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Preparation: match the vector table</b></p>
                <ul>
                    <li>The table has its own list of items</li>
                    <li>Each of our items must be found in that list</li>
                    <li>Items with no vector drop out of this method and stay in support and lift</li>
                    <li>The vectors come from another collection, not from these transactions</li>
                </ul>
                <p>The notebook fills the table from a word model.</p>
            </div>
        </div>
    </div>
</div>

## Item Vectors

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 35%">
                <p><b>Shared rows</b></p>
                <p>Some tables store one vector for many items. Those items get a cosine of 1. That is not a pattern.</p>
                <ul>
                    <li>Read those pairs apart from the rest</li>
                    <li>The notebook checks this for the word model</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 65%">

```python
def shared_rows(vocabulary, vectors):
    by_row = {}
    for item in vocabulary:
        if item in vectors:
            by_row.setdefault(vectors[item].tobytes(), []).append(item)
    return [group for group in by_row.values() if len(group) > 1]
```

            </div>
        </div>
    </div>
</div>

## Item Vectors

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 35%">
                <p><b>Python</b></p>
                <ul>
                    <li>No closeness when an item has no vector</li>
                    <li>Unit vectors turn the cosine into a dot product</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 65%">

```python
import numpy as np

def unit_vector(item, vectors):
    vector = vectors[item]
    return vector / np.linalg.norm(vector)

def pair_cosine(a, b, vectors):
    if a not in vectors or b not in vectors:
        return float("nan")
    return float(unit_vector(a, vectors) @ unit_vector(b, vectors))
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
                <p><b>Bias</b></p>
                <p>Vectors learn the habits of the collection they were trained on.</p>
                <ul>
                    <li>"Man is to Computer Programmer as Woman is to Homemaker?" <a href="https://arxiv.org/abs/1607.06520" target="_blank" rel="noopener noreferrer">(Bolukbasi et al., 2016)</a></li>
                    <li>Word vectors carry human-like biases <a href="https://doi.org/10.1126/science.aal4230" target="_blank" rel="noopener noreferrer">(Caliskan et al., 2017)</a></li>
                    <li>A close pair can reflect that training collection</li>
                </ul>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
