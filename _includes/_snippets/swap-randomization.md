<!-- SLIDES: -->

## Baselines

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>What must chance keep?</b></p>
                <ul>
                    <li>The data is a 0/1 table: one row per text, one column per word</li>
                    <li>Row margin: how many words (at the floor) each text has, its length</li>
                    <li>Column margin: in how many texts each word appears (its support)</li>
                    <li>Shuffling words uniformly keeps only the columns. Long texts lose their extra pairs, so chance looks too weak and most pairs pass</li>
                    <li>Swap randomisation keeps both margins <a href="https://doi.org/10.1145/1297332.1297338" target="_blank" rel="noopener noreferrer">(Gionis et al., 2007)</a></li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Baselines

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                                <p><b>One swap</b></p>

                $$
                \begin{array}{c|cc}
                 & w_1 & w_2 \\ \hline
                t_1 & 1 & 0 \\
                t_2 & 0 & 1
                \end{array}
                \quad \Longrightarrow \quad
                \begin{array}{c|cc}
                 & w_1 & w_2 \\ \hline
                t_1 & 0 & 1 \\
                t_2 & 1 & 0
                \end{array}
                $$

                <p>Text 1 keeps its length, text 2 keeps its length.</p>
                <p>Word 1 and word 2 keep their support.</p>
                <p>Many swaps give one random table with the same margins.</p>
            </div>
        </div>
    </div>
</div>

## Baselines

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 35%">
                <p><b>Python: swap null</b></p>
                <p>5 swap attempts per 1 in the table.</p>
                <ul>
                    <li>100 random tables, seed 7. Sorting each text's words makes the seed repeatable.</li>
                    <li>Keep pairs at the floor and strictly above the 95th percentile.</li>
                    <li>pair_counts, swap_null_counts and kept_pairs are defined in the notebook, Part 6, Step 4.</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 65%">

```python
def swap_randomize(transactions, n_swaps, rng):
    rows = [set(t) for t in transactions]
    cells = [(i, w) for i, t in enumerate(rows) for w in sorted(t)]
    for _ in range(n_swaps):
        a, b = rng.randrange(len(cells)), rng.randrange(len(cells))
        (t1, w1), (t2, w2) = cells[a], cells[b]
        if t1 == t2 or w1 == w2 or w2 in rows[t1] or w1 in rows[t2]:
            continue
        rows[t1].remove(w1)
        rows[t1].add(w2)
        rows[t2].remove(w2)
        rows[t2].add(w1)
        cells[a], cells[b] = (t1, w2), (t2, w1)
    return rows

frequent_words = set(vocabulary)
transactions = [s & frequent_words for s in word_sets]
null = swap_null_counts(transactions, candidates)   # N_SAMPLES tables, SWAPS_PER_ONE, SEED
kept = kept_pairs(candidates, null)
```

            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->