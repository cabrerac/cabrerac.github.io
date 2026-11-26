<!-- SLIDES: -->

## node2vec

<div class="rows" style="height: 100%">
    <div class="row" style="height: 65%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%; height: 100%">
                <img class="external-svg" src="{{ site.url }}/assets/media/diagrams/graph-task-taxonomy.svg" alt="Taxonomy of graph methods" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
    <div class="row" style="height: 35%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%; height: 100%">
                <p><b>Link counts:</b> how many links an item has, and from whom.</p>
                <p><b>Paths:</b> how an item sits on the shortest paths between others.</p>
                <p><b>Node embeddings:</b> one vector per item, learned from the links.</p>
                <p><b>Communities:</b> groups of items with more links inside than outside.</p>
            </div>
        </div>
    </div>
</div>

## node2vec

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p><b>node2vec</b> gives each item of a graph a vector, so that items that appear on the same random walks get close vectors.</p>
            </div>
        </div>
    </div>
</div>

## node2vec

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Walks as sentences</b> (<a href="https://doi.org/10.1145/2623330.2623732" target="_blank" rel="noopener noreferrer">Perozzi et al., 2014</a>, <a href="https://doi.org/10.1145/2939672.2939754" target="_blank" rel="noopener noreferrer">Grover and Leskovec, 2016</a>)</p>
                <ul>
                    <li><p>Walk from node to node along the edges, at random</p></li>
                    <li><p>Write the walk down as a sentence, one word per node (here A B D E C)</p></li>
                    <li><p>Nodes that appear in the same walks get close vectors</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/node2vec-walks-2.svg" alt="One random walk written as a sentence" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
</div>

## node2vec

<div class="rows" style="height: 100%">
    <div class="row" style="height: 56%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 47.5%; height: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/node2vec-walks-3.svg" alt="Skip-gram pairs from a window over the walk" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
            <div class="column vertical-middle text-left" style="width: 5%"></div>
            <div class="column vertical-middle text-center" style="width: 47.5%; height: 100%">
                <img src="{{ site.url }}/assets/media/images/skip-gram.svg" alt="Skip-gram model" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
    <div class="row" style="height: 44%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%; height: 100%">
                <p><b>Skip-gram on walks</b></p>
                <ul>
                    <li><p>Slide a window over each walk (left: window of 1 around D gives (D, B) and (D, E))</p></li>
                    <li><p>Each node predicts the nodes in its window (right), the same objective as word2vec on sentences</p></li>
                </ul>
            </div>
        </div>
    </div>
</div>
<div class="footnote" style="flex-shrink: 0;">Skip-gram - Zhang, Lipton, Li, and Smola, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons</div>

## node2vec

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Preparation:</b> only the largest component</p>
                <ul>
                    <li><p>A walk never leaves its component</p></li>
                    <li><p>An isolated item has no walk at all</p></li>
                    <li><p>Small components give noisy walks</p></li>
                </ul>
                <p>G, H and I are outside the largest component and get no vector. We count those items and report them.</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/node2vec-component.svg" alt="Nodes outside the largest component get no vector" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
</div>

## node2vec

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <p>Where does the walk go next? After moving from $t$ to $v$, the next node $x$ gets a weight.</p>
$$
\alpha(t, x) = \begin{cases} 1/p & \text{if } x = t \\ 1 & \text{if } x \text{ is a neighbour of } t \\ 1/q & \text{otherwise} \end{cases}
$$
                <p><b>$p$:</b> the return knob, the weight of going back</p>
                <p><b>$q$:</b> the in-out knob, the weight of moving away from $t$</p>
                <p>$p = q = 1$ is the plain random walk of DeepWalk.</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/node2vec-bias-1.svg" alt="We came from t and stand on v" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
</div>

## node2vec

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <ul>
                    <li><p>We came from $t$ and stand on $v$</p></li>
                    <li><p>$x_1$ is next to $t$ and $x_2$ is far from $t$</p></li>
                    <li><p>$p = 2$ and $q = 0.5$</p></li>
                </ul>
                <p>The weights are 0.5 for $t$, 1 for $x_1$, and 2 for $x_2$. They add to 3.5.</p>
                <p>So the walk goes back with probability 0.14, stays close with 0.29, and moves out with 0.57. A $q$ below 1 pushes the walk outwards.</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/node2vec-bias-2.svg" alt="The weights of the next step" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
</div>

## node2vec

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Cosine of node vectors</b></p>
$$
\cos(\mathbf{u}, \mathbf{v}) = \frac{\mathbf{u} \cdot \mathbf{v}}{\lVert \mathbf{u} \rVert \, \lVert \mathbf{v} \rVert}
$$
                <p><b>$\mathbf{u}, \mathbf{v}$:</b> the vectors of two nodes</p>
                <p><b>$\mathbf{u} \cdot \mathbf{v}$:</b> the sum of the products of matching numbers</p>
                <p>In the figure, $\mathbf{u}$ and $\mathbf{v}$ point the same way, so their cosine is high even with no direct link.</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/node2vec-cosine.svg" alt="Two vectors that point the same way" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
</div>

## node2vec

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Set before the results</b></p>
                <ul>
                    <li><p>The dimensions of the vector</p></li>
                    <li><p>Walks per node and walk length</p></li>
                    <li><p>$p$, $q$, and the window</p></li>
                    <li><p>The seeds</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/node2vec-walks-2.svg" alt="One random walk written as a sentence" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
</div>

## node2vec

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Limits</b></p>
                <ul>
                    <li><p>Another seed gives other walks and other neighbours</p></li>
                    <li><p>Items outside the largest component have no vector</p></li>
                    <li><p>Close vectors say the neighbourhood is shared, not why</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/node2vec-component.svg" alt="Nodes outside the largest component get no vector" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
</div>

## node2vec

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 47.5%; font-size: 0.85em">

```text
keep the largest component
for each node, several walks
    first step: a random neighbour
    next steps: weight 1/p back,
        1 close, 1/q out
write each walk as a sentence
    of node names
skip-gram on the walks, fixed seed
nearest neighbours by cosine
```
</div>
            <div class="column vertical-middle text-left" style="width: 4%"></div>
            <div class="column vertical-middle text-center" style="width: 47.5%; height: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/node2vec-walks-3.svg" alt="Skip-gram pairs from a window over the walk" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
</div>

## node2vec

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 38%">
                <p><b>Python usage:</b> Python</p>
                <p>Plain random walks, $p = q = 1$, on the small graph</p>
                <ul>
                    <li><p><b>neighbours:</b> the linked nodes of each node</p></li>
                    <li><p><b>rng.choice:</b> the next node, each neighbour with the same probability</p></li>
                    <li><p><b>Returns:</b> 50 walks of 10 nodes. The first is A C A C E C A B D E</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 4%"></div>
            <div class="column vertical-middle text-left" style="width: 58%; font-size: 0.85em">

```python
import random

neighbours = {"A": "BC", "B": "AD", "C": "ADE",
              "D": "BCE", "E": "CD"}
rng = random.Random(7)
walks = []
for _ in range(10):
    for start in sorted(neighbours):
        walk = [start]
        for _ in range(9):
            step = rng.choice(neighbours[walk[-1]])
            walk.append(step)
        walks.append(walk)
```
</div>
        </div>
    </div>
</div>

## node2vec

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 58%; font-size: 0.85em">

```python
from gensim.models import Word2Vec

model = Word2Vec(walks, vector_size=8, window=2,
                 sg=1, min_count=1, workers=1,
                 seed=7, epochs=20)
print(model.wv.most_similar("A", topn=2))
```
</div>
            <div class="column vertical-middle text-left" style="width: 4%"></div>
            <div class="column vertical-middle text-left" style="width: 38%">
                <p><b>Python usage:</b> gensim</p>
                <p>Vectors from the walks, read as sentences</p>
                <ul>
                    <li><p><b>walks:</b> the 50 walks from the slide before</p></li>
                    <li><p><b>Word2Vec:</b> skip-gram, sg=1, with a window of 2 and a fixed seed</p></li>
                    <li><p><b>Returns:</b> the two nodes closest to A, [('E', 0.78), ('C', 0.77)]. E has no direct link to A</p></li>
                </ul>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
