<!-- SLIDES: -->

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p>With no answer key, a place is <b>judged</b> against an outside measure, across seeds, and against random pairs.</p>
            </div>
        </div>
    </div>
</div>

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>No answer key</b></p>
                <ul>
                    <li><b>Against an outside measure:</b> does the place agree with a count made outside this set</li>
                    <li><b>Across seeds:</b> does node2vec give the same neighbours on a rerun</li>
                    <li><b>Against random pairs:</b> do neighbours share more than chance</li>
                    <li><b>Coverage:</b> how many items have no place, isolated or with no vector</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/social-network-analysis.jpg" alt="A network of links among people" style="height: 360px">
                <div class="footnote">Social Network Analysis Visualization - Martin Grandjean, CC BY-SA 3.0 <https://creativecommons.org/licenses/by-sa/3.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Against an outside measure <a href="https://doi.org/10.2307/1412159" target="_blank" rel="noopener noreferrer">(Spearman, 1904)</a></b></p>
                <p>$$\rho = 1 - \frac{6 \sum_i d_i^2}{n\,(n^2 - 1)}$$</p>
                <p>$d_i$ is the difference between the two ranks of item $i$, and $n$ the number of items. The denominator is the largest the sum can get, scaled so that $\rho$ lies between -1 and 1.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>Ranks 1, 2, 3, 4 by the graph and 1, 3, 2, 4 outside give $\sum d^2 = 2$, so $\rho = 1 - 12/60 = 0.8$.</p>
                <br>
                <p>An outside count such as citations covers the whole literature, while a graph score covers only this set. A low agreement is a finding, not an error.</p>
            </div>
        </div>
    </div>
</div>

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 35%">
                <p><b>Python: rank agreement</b></p>
                <ul>
                    <li>The graph score and the outside count, for the same items</li>
                    <li>Spearman ranks both, so the scale does not matter</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 65%">

```python
from scipy.stats import spearmanr

def rank_agreement(score, outside, items):
    a = [score[v] for v in items]
    b = [outside[v] for v in items]
    rho, _ = spearmanr(a, b)
    return rho

rho = rank_agreement(rank, citations, connected)
```

            </div>
        </div>
    </div>
</div>

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Across seeds</b></p>
                <p>$$\text{overlap}(v) = \frac{|N_k^{(1)}(v) \cap N_k^{(2)}(v)|}{k}$$</p>
                <p>$N_k^{(1)}(v)$ is the set of the $k$ nearest neighbours of $v$ with the first seed, and $N_k^{(2)}(v)$ with the second. The numerator counts the neighbours both runs share.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>With $k = 5$ and 4 shared neighbours, the overlap is $4/5 = 0.8$. We report the mean over all items with a vector.</p>
                <br>
                <p>A low overlap says the neighbours are mostly chance of the walks.</p>
            </div>
        </div>
    </div>
</div>

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 35%">
                <p><b>Python: seed overlap</b></p>
                <ul>
                    <li>One run per seed, with the same settings</li>
                    <li>Only items with a vector in every run</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 65%">

```python
def top_neighbours(vectors, k):
    return {v: {u for u, _ in vectors.most_similar(v, topn=k)}
            for v in vectors.index_to_key}

def seed_overlap(runs, k):
    tops = [top_neighbours(r, k) for r in runs]
    nodes = set.intersection(*(set(t) for t in tops))
    shares = [len(set.intersection(*(t[v] for t in tops))) / k
              for v in nodes]
    return sum(shares) / len(shares)

overlap = seed_overlap(runs, k=5)
```

            </div>
        </div>
    </div>
</div>

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 35%">
                <p><b>Python: random pairs</b></p>
                <ul>
                    <li>The baseline for neighbours</li>
                    <li>1,000 random pairs of items with a vector</li>
                    <li>Neighbours are closer than chance when they share more than random pairs</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 65%">

```python
import random

def shared_share(pairs, labels):
    hits = sum(bool(labels[a] & labels[b]) for a, b in pairs)
    return hits / len(pairs)

rng = random.Random(0)
nodes = sorted(vectors.index_to_key)
random_pairs = [tuple(rng.sample(nodes, 2))
                for _ in range(1000)]
neighbour_pairs = [(v, u) for v in nodes
                   for u, _ in vectors.most_similar(v, topn=5)]
print(shared_share(neighbour_pairs, topics),
      shared_share(random_pairs, topics))
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
                <p><b>What each method sees</b></p>
                <table class="table">
                    <thead>
                        <tr><th>Method</th><th>Sees</th><th>Misses</th></tr>
                    </thead>
                    <tbody>
                        <tr><td>Degree</td><td>How many links an item has</td><td>Who makes them, and links outside the set</td></tr>
                        <tr><td>PageRank</td><td>Links from well placed items</td><td>Items that only link out</td></tr>
                        <tr><td>node2vec</td><td>Items that share a neighbourhood</td><td>Items with no vector, and why they are close</td></tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>How to compare them</b></p>
                <ul>
                    <li>Run every method on the same graph</li>
                    <li>Look at the top items of each method side by side</li>
                    <li>Read the items where the methods disagree, such as low degree and high PageRank</li>
                    <li>An item that several methods place high is a stronger candidate</li>
                    <li>Disagreement is not a winner. Each method sees something the others miss</li>
                </ul>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
