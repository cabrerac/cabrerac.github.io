<!-- SLIDES: -->

## Lift

<div class="rows" style="height: 100%">
    <div class="row" style="height: 70%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img class="external-svg" src="{{ site.url }}/assets/media/diagrams/pattern-task-taxonomy.svg" alt="Taxonomy of pattern methods" style="width: 100%; height: 100%">
            </div>
        </div>
    </div>
    <div class="row" style="height: 30%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <p><b>Frequent itemsets:</b> sets that occur in many transactions, found by counting.</p>
                <p><b>Interestingness:</b> a score that compares a count with chance.</p>
                <p><b>Sequential patterns:</b> patterns that keep the order of the items.</p>
                <p><b>Item vectors:</b> one vector per item in a learned space, so items used alike lie close.</p>
            </div>
        </div>
    </div>
</div>

## Lift

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p><b>Lift</b> compares how often two items appear together with how often they would meet by chance alone.</p>
            </div>
        </div>
    </div>
</div>

## Lift

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>Support favours common items.</p>
                <p>If A is in half the transactions and B is in half the transactions.</p>
                <ul>
                    <li>They meet in about a quarter of the transactions by chance alone</li>
                    <li>A high support can mean nothing more than two common items</li>
                    <li>Compare a pair with what chance would give</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/diagrams/lift-chance-overlap.svg" alt="Chance overlap of two common items" style="height: 360px">
            </div>
        </div>
    </div>
</div>

## Lift

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>Lift divides the observed co-occurrence by the co-occurrence independence would give <a href="https://doi.org/10.1145/253262.253325" target="_blank" rel="noopener noreferrer">(Brin et al., 1997)</a>.</p>
                <br>
                <p>$$\text{lift}(A,B) = \frac{P(A,B)}{P(A)\,P(B)} = \frac{n_{AB} \cdot N}{n_A \cdot n_B}$$</p>
                <br>
                <p>The joint probability is $n_{AB} / N$. Each marginal is a count over $N$ as well, $n_A / N$ and $n_B / N$.</p>
                <p>Dividing the joint by the product of the marginals leaves $n_{AB} \cdot N$ on top and $n_A \cdot n_B$ below.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>If A and B are independent, $P(A,B) = P(A)\,P(B)$.</p>
                <ul>
                    <li><b>Lift = 1:</b> the pair meets as often as chance</li>
                    <li><b>Lift above 1:</b> the pair meets more often than chance</li>
                    <li><b>Lift below 1:</b> the items avoid each other</li>
                    <li><b>In the lab:</b> the pair is kept when the lift is at least 2</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Lift

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>$N = 300$ transactions</p>
                <p>$n_A = 60$</p>
                <p>$n_B = 30$</p>
                <p>$n_{AB} = 18$</p>
                <br>
                <p>Chance would put them together in $\frac{60 \cdot 30}{300} = 6$ transactions.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>$$\text{lift} = \frac{18 \cdot 300}{60 \cdot 30} = 3$$</p>
                <br>
                <p>18 is three times the 6 transactions chance would give, so the lift is 3.</p>
                <br>
                <p>Two items in 2 transactions each, together in both, with $N = 300$.</p>
                <p>$$\text{lift} = \frac{2 \cdot 300}{2 \cdot 2} = 150$$</p>
                <p>The pair is perfect and the items are rare, so the fraction is huge. Lift is computed only on pairs that pass the support floor.</p>
            </div>
        </div>
    </div>
</div>

## Lift

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 47.5%">

```text
for each pair kept by support
    n_ab = pair_count of that pair
    n_a = item_count of the first item
    n_b = item_count of the second item
    lift = n_ab * N / (n_a * n_b)
```

            </div>
            <div class="column vertical-middle text-left" style="width: 5%">
            </div>
            <div class="column vertical-middle text-left" style="width: 47.5%">

```python
def compute_lift(n_ab, n_a, n_b, n):
    return n_ab * n / (n_a * n_b)

lifts = {}
for (a, b), n_ab in candidates.items():
    lifts[(a, b)] = compute_lift(
        n_ab, item_count[a], item_count[b], n
    )
```

            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
