<!-- SLIDES: -->

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
                <p>Write the walk down as a sentence, one word per node.</p>
                <p>Train word2vec on the walks, as word2vec does on sentences.</p>
                <p>Nodes that appear in the same walks get close vectors.</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/skip-gram.svg" alt="Skip-gram model" style="height: 300px">
                <div class="footnote">Skip-gram - Zhang, Lipton, Li, and Smola, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## node2vec

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 55%">
                <p><b>A biased walk</b></p>
                <p>After moving from $t$ to $v$, the next node $x$ gets a weight</p>
                <p>$$\alpha(t, x) = \begin{cases} 1/p & \text{if } x = t \\ 1 & \text{if } x \text{ is a neighbour of } t \\ 1/q & \text{otherwise} \end{cases}$$</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 45%">
                <p><b>Two knobs</b></p>
                <p>$p$, return: a large $p$ makes going back rare.</p>
                <p>$q$, in-out: $q < 1$ pushes the walk outwards, $q > 1$ keeps it close.</p>
                <p>$p = q = 1$ is the plain random walk of DeepWalk.</p>
                <p>Each step picks $x$ with probability proportional to $\alpha(t, x)$.</p>
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
                <p>For each node in a walk, predict the nodes within the window around it.</p>
                <p>The same objective as word2vec on sentences.</p>
            </div>
            <div class="column vertical-top text-left" style="width: 50%">
                <p><b>Cosine of node vectors</b></p>
                <p>$$\cos(\mathbf{u}, \mathbf{v}) = \frac{\mathbf{u} \cdot \mathbf{v}}{\lVert \mathbf{u} \rVert \, \lVert \mathbf{v} \rVert}$$</p>
                <p>Nearest neighbours are the nodes with the highest cosine.</p>
                <p>They share a neighbourhood, even with no direct link.</p>
            </div>
        </div>
    </div>
</div>

## node2vec

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Only the largest component</b></p>
                <p>A walk never leaves its component.</p>
                <p>An isolated item has no walk at all.</p>
                <p>Items with no vector are counted and reported.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>No vector</b></p>
                <p>No vector, so never used in a cosine.</p>
                <p>Drawn at the origin in a plot, labelled no vector.</p>
                <p>Small components give noisy walks.</p>
            </div>
        </div>
    </div>
</div>

## node2vec

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 40%">
                <p><b>Python, the walks</b></p>
                <p>Nodes and neighbours sorted, so a seed gives the same walks in any session.</p>
                <p>Back with weight 1/p, close with 1, out with 1/q.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 60%">


```python
import random

def node2vec_walks(adj, walks_per_node, walk_length, p, q, seed):
    rng, nodes, walks = random.Random(seed), sorted(adj), []
    for _ in range(walks_per_node):
        rng.shuffle(nodes)
        for start in nodes:
            walk = [start]
            while len(walk) < walk_length:
                here = walk[-1]
                options = sorted(adj[here])   # never empty in the largest component
                if len(walk) == 1:
                    walk.append(rng.choice(options))
                    continue
                before = walk[-2]
                weights = [1 / p if x == before            # go back
                           else 1.0 if x in adj[before]     # stay close
                           else 1 / q                       # move out
                           for x in options]
                walk.append(rng.choices(options, weights=weights)[0])
            walks.append([str(x) for x in walk])
    return walks
```

</div>
        </div>
    </div>
</div>

## node2vec

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 40%">
                <p><b>Python, the vectors</b></p>
                <p>gensim Word2Vec with skip-gram, sg=1.</p>
                <p>workers=1 and a fixed seed.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 60%">


```python
import networkx as nx
from gensim.models import Word2Vec

NODE_DIMENSIONS = 32
WALKS_PER_NODE = 10
WALK_LENGTH = 20
P_RETURN = 1.0
Q_INOUT = 0.5
WINDOW = 5
N2V_SEEDS = (7, 8, 9)

largest = max(nx.connected_components(graph), key=len)
adj = {v: neighbours[v] & largest for v in largest}
no_vector = [v for v in graph if v not in largest]   # reported, never used in a cosine

walks = node2vec_walks(adj, WALKS_PER_NODE, WALK_LENGTH, P_RETURN, Q_INOUT, N2V_SEEDS[0])
model = Word2Vec(walks, vector_size=NODE_DIMENSIONS, window=WINDOW,
                 min_count=1, sg=1, workers=1, seed=N2V_SEEDS[0])
some_item = top_rank[0]
print(model.wv.most_similar(str(some_item), topn=5))
```

</div>
        </div>
    </div>
</div>

## node2vec

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Parameters</b></p>
                <ul>
                    <li>Dimensions of the vector</li>
                    <li>Walks per node and walk length</li>
                    <li>$p$ and $q$, and the window</li>
                </ul>
                <p>Set before looking at the result, never tuned on it.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Checks, no labels needed</b></p>
                <ul>
                    <li><b>Stability</b> - the top 5 neighbours across three seeds overlap</li>
                    <li><b>Against chance</b> - neighbours share more topics than random pairs</li>
                    <li><b>Coverage</b> - how many items got no vector</li>
                </ul>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
