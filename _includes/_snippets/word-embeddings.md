<!-- SLIDES: -->

## Word Embeddings

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p>A <b>word embedding</b> gives each word a vector learned from a large body of text, so that words used in similar contexts get close vectors.</p>
            </div>
        </div>
    </div>
</div>

## Word Embeddings

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Counts only see our texts</b></p>
                <p>Two words with close meanings may rarely share a text.</p>
                <p>Counting cannot tell that car and automobile are close.</p>
                <p>A pretrained embedding learned from far more text can.</p>
                <p>Closeness in an embedding is a third way to judge a pair.</p>
            </div>
        </div>
    </div>
</div>

## Word Embeddings

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>The distributional hypothesis</b> <a href="https://doi.org/10.1080/00437956.1954.11659520" target="_blank" rel="noopener noreferrer">(Harris, 1954, p. 156)</a></p>
                <p>A word is described by the words around it.</p>
                <p>Words with similar neighbours get similar vectors.</p>
                <p>Close vectors mean similar use, not the same meaning.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/word-vector-illustration.jpg" alt="Word vectors" style="height: 380px">
                <div class="footnote">Word vector illustration - Singerep, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Word Embeddings

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Skip-gram</b></p>
                <table class="table">
                    <tr>
                        <td>
                            <p>"We propose two novel model architectures for computing continuous vector representations of words from very large data sets."</p>
                            <p><a href="https://arxiv.org/abs/1301.3781" target="_blank" rel="noopener noreferrer">(Mikolov et al., 2013)</a></p>
                        </td>
                    </tr>
                </table>
                <p>Take a word and predict its neighbours.</p>
                <p>The weights learned for each word are its vector.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/skip-gram.svg" alt="Skip-gram model" style="height: 360px">
                <div class="footnote">Skip-gram - Zhang, Lipton, Li, and Smola, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Word Embeddings

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <p><b>Cosine similarity</b></p>
                <p>$$\cos(\mathbf{u}, \mathbf{v}) = \frac{\mathbf{u} \cdot \mathbf{v}}{\lVert \mathbf{u} \rVert \, \lVert \mathbf{v} \rVert}$$</p>
                <p><b>Close to 1</b> - the words are used in similar ways.</p>
                <p><b>Close to 0</b> - no relation.</p>
                <p><b>Below 0</b> - rare, and usually weak.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/cosine-similarity.png" alt="Cosine similarity" style="height: 300px">
                <div class="footnote">CosineSimilarity - StandingFuture, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Word Embeddings

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Preparation: match the vocabulary</b></p>
                <ul>
                    <li>The model has its own list of words</li>
                    <li>Each of our words must be found in that list</li>
                    <li>Report the words with no vector, such as new terms or acronyms</li>
                    <li>Domain words such as covid and DALYs have no vector in a general English model. They drop out of the embedding view, but not out of support and lift</li>
                    <li>The vectors come from web text, not from our texts</li>
                </ul>
                <p>spaCy English models <a href="https://spacy.io/models/en#en_core_web_lg" target="_blank" rel="noopener noreferrer">(spaCy models)</a></p>
            </div>
        </div>
    </div>
</div>

## Word Embeddings

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Small models share rows</b></p>
                <p>A medium spaCy model keeps 20,000 vectors for about 685,000 words.</p>
                <p>Many words point to the same row.</p>
                <p>Then high and low get a cosine of 1.0, which means nothing.</p>
                <p>The large model has about 343,000 vectors. High and low get 0.76.</p>
                <p>In one collection of health papers, 58 of the 150 most frequent words shared a row in the medium model and none in the large one.</p>
            </div>
        </div>
    </div>
</div>

## Word Embeddings

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 35%">
                <p><b>Python</b></p>
                <ul>
                    <li>Load the large model</li>
                    <li>No closeness when a word has no vector</li>
                    <li>Words with exactly the same vector (a shared or copied row) are read apart</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 65%">


```python
import numpy as np
import spacy

nlp = spacy.load("en_core_web_lg")

def shared_vectors(vocab_words, nlp):
    by_vector = {}
    for w in vocab_words:
        if nlp.vocab.has_vector(w):
            by_vector.setdefault(nlp.vocab.get_vector(w).tobytes(), []).append(w)
    return [group for group in by_vector.values() if len(group) > 1]

group_of = {w: i for i, g in enumerate(shared_vectors(vocabulary, nlp)) for w in g}

def unit_vector(word, nlp):
    v = nlp.vocab.get_vector(word)
    return v / np.linalg.norm(v)

VECTORS = {w: unit_vector(w, nlp) for w in vocabulary if nlp.vocab.has_vector(w)}

def pair_cosine(a, b):
    if a not in VECTORS or b not in VECTORS:
        return float("nan")
    return float(VECTORS[a] @ VECTORS[b])
```

            </div>
        </div>
    </div>
</div>

## Word Embeddings

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Bias</b></p>
                <p>Embeddings learn from human text, with its stereotypes.</p>
                <p>"Man is to Computer Programmer as Woman is to Homemaker?" <a href="https://arxiv.org/abs/1607.06520" target="_blank" rel="noopener noreferrer">(Bolukbasi et al., 2016)</a>.</p>
                <p>Word vectors carry human-like biases, measured like implicit association tests <a href="https://doi.org/10.1126/science.aal4230" target="_blank" rel="noopener noreferrer">(Caliskan et al., 2017)</a>.</p>
                <p>A close pair can reflect the web, not our texts.</p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
