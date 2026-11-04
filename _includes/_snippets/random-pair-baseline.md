<!-- SLIDES: -->

## Baselines

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 35%">
                <p><b>Python: random pairs</b></p>
                <ul>
                    <li>The baseline for closeness</li>
                    <li>Cosine of 1,000 random word pairs</li>
                    <li>Pairs of words with the same vector are skipped. The column shared_vector marks them</li>
                    <li>A pair is closer than chance when its cosine is strictly above their 95th percentile, read the same way as the swap baseline</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 65%">


```python
import random

rng_cosine = random.Random(SEED)
words_with_vector = sorted(VECTORS)
random_cosines = []
for _ in range(1000):
    a, b = rng_cosine.sample(words_with_vector, 2)
    if not (a in group_of and group_of.get(a) == group_of.get(b)):
        random_cosines.append(pair_cosine(a, b))
RANDOM_COSINE_P95 = p95(random_cosines)

table["cosine"] = [pair_cosine(a, b) for a, b in zip(table["word_a"], table["word_b"])]

table["beats_cosine"] = (table["cosine"] > RANDOM_COSINE_P95) & ~table["shared_vector"]
```

            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
