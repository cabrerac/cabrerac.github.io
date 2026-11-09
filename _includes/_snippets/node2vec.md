<!-- SLIDES: -->

## node2vec

<div class="rows" style="height: 100%">
    <div class="row" style="height: 70%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img class="external-svg" src="{{ site.url }}/assets/media/diagrams/graph-task-taxonomy.svg" alt="Taxonomy of graph methods" style="width: 100%; height: 100%">
            </div>
        </div>
    </div>
    <div class="row" style="height: 30%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
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
                <p><b>Walks as sentences <a href="https://doi.org/10.1145/2623330.2623732" target="_blank" rel="noopener noreferrer">(Perozzi et al., 2014)</a> <a href="https://doi.org/10.1145/2939672.2939754" target="_blank" rel="noopener noreferrer">(Grover and Leskovec, 2016)</a></b></p>
                <p>Walk from node to node along the edges, at random.</p>
                <ul>
                    <li>Write the walk down as a sentence, one word per node</li>
                    <li>Train word2vec on the walks, as on sentences</li>
                    <li>Nodes that appear in the same walks get close vectors</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/skip-gram.svg" alt="Skip-gram model" style="height: 360px">
                <div class="footnote">Skip-gram - Zhang, Lipton, Li, and Smola, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## node2vec

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Preparation: only the largest component</b></p>
                <p>A walk never leaves its component.</p>
                <ul>
                    <li>An isolated item has no walk at all</li>
                    <li>Small components give noisy walks</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>No vector</b></p>
                <ul>
                    <li>An item with no vector is never used in a cosine</li>
                    <li>We count those items and report them</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## node2vec

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>After moving from $t$ to $v$, the next node $x$ gets a weight.</p>
                <p>$$\alpha(t, x) = \begin{cases} 1/p & \text{if } x = t \\ 1 & \text{if } x \text{ is a neighbour of } t \\ 1/q & \text{otherwise} \end{cases}$$</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>$t$ is the node we came from and $v$ the node we are on. $x$ is one neighbour of $v$. $p$, the return knob, sets the weight of going back. $q$, the in-out knob, sets the weight of moving away from $t$. Each step picks $x$ with probability proportional to its weight.</p>
                <p>$p = q = 1$ is the plain random walk of DeepWalk.</p>
            </div>
        </div>
    </div>
</div>

## node2vec

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <ul>
                    <li><p>We came from $t$ and stand on $v$</p></li>
                    <li><p>The neighbours of $v$: $t$, $x_1$ next to $t$, and $x_2$ far from $t$</p></li>
                    <li><p>$p = 2$ and $q = 0.5$</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>The weights are $1/2 = 0.5$ for $t$, 1 for $x_1$, and $1/0.5 = 2$ for $x_2$. They add to 3.5.</p>
                <br>
                <p>So the walk goes back with probability 0.14, stays close with 0.29, and moves out with 0.57. A $q$ below 1 pushes the walk outwards.</p>
            </div>
        </div>
    </div>
</div>

## node2vec

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Skip-gram on walks</b></p>
                <p>For each node in a walk, predict the nodes within the window around it. The same objective as word2vec on sentences.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Cosine of node vectors</b></p>
                <p>$$\cos(\mathbf{u}, \mathbf{v}) = \frac{\mathbf{u} \cdot \mathbf{v}}{\lVert \mathbf{u} \rVert \, \lVert \mathbf{v} \rVert}$$</p>
                <p>$\mathbf{u}$ and $\mathbf{v}$ are the vectors of two nodes. The numerator adds the products of matching numbers, and the denominator is the product of their lengths. Nearest neighbours are the nodes with the highest cosine, even with no direct link.</p>
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
                    <li><p>Dimensions of the vector</p></li>
                    <li><p>Walks per node and walk length</p></li>
                    <li><p>$p$, $q$, and the window</p></li>
                    <li><p>The seeds</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Limits</b></p>
                <ul>
                    <li>Another seed gives other walks and other neighbours</li>
                    <li>Items outside the largest component have no vector</li>
                    <li>Close vectors say the neighbourhood is shared, not why</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## node2vec

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 47.5%">

```text
keep the largest component
for each node, several walks
    first step: a random neighbour
    next steps: weight 1/p back, 1 close, 1/q out
write each walk as a sentence of node names
skip-gram on the walks, with a fixed seed
nearest neighbours by cosine
```

            </div>
            <div class="column vertical-middle text-left" style="width: 5%">
            </div>
            <div class="column vertical-middle text-left" style="width: 47.5%">

```python
from gensim.models import Word2Vec

def next_node(neighbours, t, v, p, q, rng):
    options = sorted(neighbours[v])
    weights = [1 / p if x == t else
               1 if x in neighbours[t] else 1 / q
               for x in options]
    return rng.choices(options, weights=weights)[0]

def node_vectors(walks, dimensions, window, seed):
    model = Word2Vec(walks, vector_size=dimensions,
                     window=window, sg=1, min_count=1,
                     workers=1, seed=seed)
    return model.wv
```

            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
