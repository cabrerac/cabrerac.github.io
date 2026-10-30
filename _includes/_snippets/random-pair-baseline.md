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
                    <li>Pairs of words with the same vector are skipped</li>
                    <li>A pair is closer than chance when its cosine is strictly above their 95th percentile, with the same p95() rank rule as the swap null</li>
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
RANDOM_COSINE_P95 = p95(random_cosines)   # same rank rule as the swap null

shared_vector = {p for p in candidates
                 if p[0] in group_of and group_of.get(p[0]) == group_of.get(p[1])}
beats_cosine = {p for p in candidates
                if pair_cosine(*p) > RANDOM_COSINE_P95 and p not in shared_vector}
```

            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
