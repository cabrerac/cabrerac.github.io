"""Swap randomisation: a null model for frequent pairs that keeps both margins.

Shared helper for the Data Mining course (26-udenar-data-mining). The L2 notebook,
the week 1 group notebook, its private solution and
work-space/teaching/data-mining/scripts/check_week1_patterns.py all use this rule.
Copy it into a notebook as it is. It needs only the standard library and numpy,
so it runs on free Colab.

The question
    A pair of words appears together in c texts. Is c more than chance would give?

What "chance" must keep
    The data is a 0/1 table. One row per text (a transaction), one column per word
    (an item). Two margins describe it:
      - row margin: how many distinct words each text has (its length),
      - column margin: in how many texts each word appears (its support).
    A shuffle that keeps only the column margin puts every word in random texts with
    equal probability. Long texts then lose their extra pairs, chance gives too few
    co-occurrences, and almost every pair looks significant. In the papers extract
    that uniform shuffle kept 11,966 of 16,271 candidate pairs.

The swap
    Swap randomisation keeps both margins exactly (Gionis, Mannila, Mielikainen and
    Tsaparas, 2007, "Assessing data mining results via swap randomization",
    ACM Transactions on Knowledge Discovery from Data 1(3), article 14,
    https://doi.org/10.1145/1297332.1297338). One swap:
      1. pick two (text, word) cells that hold a 1: (t1, w1) and (t2, w2),
      2. if t1 has no w2 and t2 has no w1, move the words:
         (t1, w1), (t2, w2)  ->  (t1, w2), (t2, w1).
    Every text keeps its length and every word keeps its support. After many swaps
    the table is a random table with the same margins. Counting the pairs again on
    that table gives one value of the null.

Choices made here (check script run, 30 Oct 2026)
    - Only words at or above the support floor enter the table. Rarer words can never
      be in a candidate pair, so they do not change any count we test. A text's length
      is then its number of frequent words.
    - SWAPS_PER_ONE = 5: each random table gets 5 swap attempts per 1 in the table,
      starting from the observed table. Each table is an independent chain from the
      observed data, the usual practice. (A backward-forward scheme, Besag and
      Clifford, 1989, gives exact exchangeability. It is not needed here.)
      Rejected attempts count as staying put, which keeps the chain uniform. Gionis et al. run a number of swaps of the same
      order as the number of 1s. At 5 the p95 thresholds no longer move (see the
      week 1 null changelog).
    - N_SAMPLES = 100 random tables. The 95th percentile of 100 values is stable
      enough to decide a pair. 30 was too coarse for a percentile.
    - A pair is kept when its observed count is strictly above the 95th percentile
      of its null counts, and it already clears the support floor.
    - SEED = 7 everywhere, so slides, notebooks and the check script agree. The start
      list of cells is sorted, so the run does not depend on PYTHONHASHSEED.
    - Run time for the papers: about 16 s on the PC, about 20 to 40 s on free Colab.
      A Wikipedia extract takes 3 to 8 s on the PC, about 7 to 20 s on Colab.
      progress_every prints one line every 20 tables so the cell does not look frozen.

Read "kept" as "worth a look", not as "proven". With thousands of pairs, about 5%
pass a 5% test by luck alone. The notebooks say so.

Example
    >>> transactions = [{"a", "b"}, {"a", "b", "c"}, {"b", "c"}, {"a", "c"}]
    >>> null = swap_null_counts(transactions, [("a", "b")], n_samples=10, seed=7, progress_every=0)
    >>> len(null[("a", "b")])
    10
"""
from __future__ import annotations

import math
import random
from collections.abc import Iterable, Sequence

import numpy as np

SUPPORT_SHARE = 0.03   # share of texts
SUPPORT_MIN = 5        # minimum count of texts
SWAPS_PER_ONE = 5      # swap attempts per 1 in the table, for each random table
N_SAMPLES = 100        # random tables
SEED = 7
PROGRESS_EVERY = 20    # print one progress line every 20 tables (0 = quiet)


def support_floor(n_texts: int) -> int:
    """Smallest support a word or a pair needs: max(SUPPORT_MIN, ceil(SUPPORT_SHARE * n))."""
    return max(SUPPORT_MIN, math.ceil(SUPPORT_SHARE * n_texts))


def p95(values: Sequence[float]) -> float:
    """95th percentile by rank (no interpolation), the same rule on slides and in notebooks."""
    values = sorted(values)
    return values[min(len(values) - 1, int(0.95 * len(values)))]


def swap_randomize(transactions: Sequence[set], n_swaps: int, rng: random.Random) -> list[set]:
    """Return a new list of sets with the same text lengths and the same word supports.

    transactions: one set of words per text. It is not changed.
    n_swaps: number of swap attempts. Attempts that would create a duplicate are skipped,
        so the real number of swaps is lower.
    rng: a random.Random, so the run can be repeated.
    """
    rows = [set(t) for t in transactions]
    # sorted(t): a set of strings has no fixed order across processes (PYTHONHASHSEED),
    # so the start list must be sorted for SEED to give the same run everywhere.
    cells = [(i, w) for i, t in enumerate(rows) for w in sorted(t)]
    n_cells = len(cells)
    if n_cells < 2:
        return rows
    for _ in range(n_swaps):
        a = rng.randrange(n_cells)
        b = rng.randrange(n_cells)
        t1, w1 = cells[a]
        t2, w2 = cells[b]
        if t1 == t2 or w1 == w2 or w2 in rows[t1] or w1 in rows[t2]:
            continue
        rows[t1].remove(w1)
        rows[t1].add(w2)
        rows[t2].remove(w2)
        rows[t2].add(w1)
        cells[a] = (t1, w2)
        cells[b] = (t2, w1)
    return rows


def pair_counts(transactions: Sequence[set], pairs: Sequence[tuple], vocab: Sequence[str]) -> np.ndarray:
    """Number of texts that contain both words, for each pair, with one matrix product."""
    index = {w: j for j, w in enumerate(vocab)}
    table = np.zeros((len(transactions), len(vocab)), dtype=np.float32)
    for i, t in enumerate(transactions):
        cols = [index[w] for w in t if w in index]
        table[i, cols] = 1.0
    together = table.T @ table
    left = np.array([index[a] for a, _ in pairs], dtype=np.int64)
    right = np.array([index[b] for _, b in pairs], dtype=np.int64)
    return together[left, right].astype(np.int64)


def swap_null_counts(
    transactions: Sequence[set],
    pairs: Iterable[tuple],
    n_samples: int = N_SAMPLES,
    swaps_per_one: int = SWAPS_PER_ONE,
    seed: int = SEED,
    progress_every: int = PROGRESS_EVERY,
) -> dict[tuple, list[int]]:
    """Null co-occurrence counts for each pair under swap randomisation.

    transactions: one set of words per text, already limited to the words that clear
        the support floor.
    pairs: the candidate pairs (a, b) to test.
    Returns {pair: [count in random table 1, ..., count in random table n_samples]}.
    Each random table starts from the observed table and gets
    swaps_per_one * (number of 1s) swap attempts.
    progress_every: print "random tables: k of n" every that many tables (0 = quiet).
    """
    pairs = list(pairs)
    vocab = sorted({w for p in pairs for w in p} | {w for t in transactions for w in t})
    n_ones = sum(len(t) for t in transactions)
    rng = random.Random(seed)
    samples = np.empty((n_samples, len(pairs)), dtype=np.int64)
    for s in range(n_samples):
        shuffled = swap_randomize(transactions, swaps_per_one * n_ones, rng)
        samples[s] = pair_counts(shuffled, pairs, vocab)
        if progress_every and (s + 1) % progress_every == 0:
            print(f"random tables: {s + 1} of {n_samples}", flush=True)
    return {p: samples[:, j].tolist() for j, p in enumerate(pairs)}


def kept_pairs(observed: dict[tuple, int], null: dict[tuple, list[int]]) -> dict[tuple, int]:
    """Pairs whose observed count is strictly above the 95th percentile of their null counts."""
    return {p: c for p, c in observed.items() if c > p95(null[p])}