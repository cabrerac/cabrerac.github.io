<!-- SLIDES: -->

## Frequent Word Pairs

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p>A <b>frequent word pair</b> is a pair of words that appear together in at least a minimum number of texts, the support floor.</p>
            </div>
        </div>
    </div>
</div>

## Frequent Word Pairs

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Preparation</b></p>
                <p>One set of words per text.</p>
                <ul>
                    <li>All pairs of words inside each set.</li>
                    <li>A count of texts for each pair.</li>
                    <li>{diet, obesity, risk} gives three pairs: diet + obesity, diet + risk, obesity + risk.</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Frequent Word Pairs

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Support</b></p>
                <p>The support of a pair is the number of texts that hold both words.</p>
                <p>$$\text{support}(A,B) = \left|\{\, i : A \in T_i \text{ and } B \in T_i \,\}\right|$$</p>
                <p>$T_i$ is the set of distinct words in text $i$, and $N$ is the number of texts.</p>
                <p>As a share of the $N$ texts, $P(A,B) = \text{support}(A,B) / N$.</p>
                <p>Papers report support as a share. We count, so 10 texts out of 300 is a share of 3.3%.</p>
            </div>
        </div>
    </div>
</div>

## Frequent Word Pairs

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>A small example</b></p>
                <table class="table">
                    <thead>
                        <tr><th>Text</th><th>Words</th></tr>
                    </thead>
                    <tbody>
                        <tr><td>1</td><td>{diet, obesity, risk}</td></tr>
                        <tr><td>2</td><td>{diet, risk}</td></tr>
                        <tr><td>3</td><td>{obesity, risk}</td></tr>
                        <tr><td>4</td><td>{diet, obesity, risk}</td></tr>
                    </tbody>
                </table>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Support</b></p>
                <ul>
                    <li><b>diet + risk:</b> 3 texts</li>
                    <li><b>obesity + risk:</b> 3 texts</li>
                    <li><b>diet + obesity:</b> 2 texts</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Frequent Word Pairs

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>The support floor</b></p>
                <p>A pair needs at least $k$ texts, a share of the collection with a minimum count.</p>
                <p>$$k = \max\left(5,\ \lceil 0.03 \cdot N \rceil\right)$$</p>
                <p>With 100 texts, k is 5.</p>
                <p>With 300 texts, k is 9.</p>
                <p>With 1,000 texts, k is 30.</p>
                <br>
                <p>"This is used to make sure that the items this rule applies to actually occur frequently enough for someone to care." <a href="https://doi.org/10.1145/253262.253325" target="_blank" rel="noopener noreferrer">(Brin et al., 1997)</a></p>
            </div>
        </div>
    </div>
</div>

## Frequent Word Pairs

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Why a floor</b></p>
                <p>One standout text cannot make a pattern alone.</p>
                <ul>
                    <li>Rare pairs look strong by luck.</li>
                    <li>The list stays small enough to read.</li>
                    <li>1,000 words give 499,500 possible pairs.</li>
                </ul>
                <p>$$\binom{V}{2} = \frac{V(V-1)}{2}$$</p>
            </div>
        </div>
    </div>
</div>

## Frequent Word Pairs

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>The Apriori property</b> <a href="https://www.vldb.org/conf/1994/P487.PDF" target="_blank" rel="noopener noreferrer">(Agrawal &amp; Srikant, 1994)</a></p>
                <p>A pair cannot be in more texts than either of its words.</p>
                <p>If a word is below the floor, every pair with it is below the floor.</p>
                <p>So we drop rare words first, then count pairs.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/frequent-itemsets-lattice.png" alt="Itemset lattice" style="height: 360px">
                <div class="footnote">FrequentItems - Xodarap00, CC BY-SA 3.0 <https://creativecommons.org/licenses/by-sa/3.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Frequent Word Pairs

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 35%">
                <p><b>Python: the floor</b></p>
                <p>The floor from the number of texts.</p>
                <ul>
                    <li>Count each word once per text.</li>
                    <li>Keep the words at the floor.</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 65%">

```python
import math
from collections import Counter

SUPPORT_SHARE = 0.03
SUPPORT_MIN = 5
SEED = 7   # one seed for every random step

def support_floor(n_texts):
    return max(SUPPORT_MIN, math.ceil(SUPPORT_SHARE * n_texts))

N = len(word_sets)
FLOOR = support_floor(N)
word_count = Counter(w for s in word_sets for w in s)
vocabulary = sorted(w for w, c in word_count.items() if c >= FLOOR)
```

            </div>
        </div>
    </div>
</div>

## Frequent Word Pairs

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 35%">
                <p><b>Python: the pairs</b></p>
                <p>Pairs from the kept words only.</p>
                <ul>
                    <li>combinations gives each pair once.</li>
                    <li>Keep the pairs at the floor.</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 65%">

```python
from itertools import combinations
import pandas as pd

def count_pairs(word_sets, word_count, floor):
    pairs = Counter()
    for s in word_sets:
        frequent = sorted(w for w in s if word_count[w] >= floor)
        pairs.update(combinations(frequent, 2))
    return {pair: c for pair, c in pairs.items() if c >= floor}

candidates = count_pairs(word_sets, word_count, FLOOR)
table = pd.DataFrame(
    [(a, b, c) for (a, b), c in candidates.items()],
    columns=["word_a", "word_b", "support"],
)
table["pair"] = table["word_a"] + " + " + table["word_b"]
```

            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
