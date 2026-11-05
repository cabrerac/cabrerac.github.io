<!-- SLIDES: -->

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 35%">
                <p><b>Python: random pairs</b></p>
                <ul>
                    <li>The baseline for closeness</li>
                    <li>Cosine of 1,000 random item pairs</li>
                    <li>Pairs that share one stored vector are skipped</li>
                    <li>A pair is closer than chance when its cosine is strictly above their 95th percentile</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 65%">

```python
import random

def same_row(a, b, vectors):
    return a in vectors and b in vectors and vectors[a].tobytes() == vectors[b].tobytes()

rng_cosine = random.Random(SEED)
items_with_vector = sorted(vectors)
random_cosines = []
for _ in range(1000):
    a, b = rng_cosine.sample(items_with_vector, 2)
    if not same_row(a, b, vectors):
        random_cosines.append(pair_cosine(a, b, vectors))
RANDOM_COSINE_P95 = p95(random_cosines)

table["cosine"] = [
    pair_cosine(a, b, vectors) for a, b in zip(table["item_a"], table["item_b"])
]
table["beats_cosine"] = table["cosine"] > RANDOM_COSINE_P95
```

            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
