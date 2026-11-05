<!-- SLIDES: -->

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
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Support favours common items</b></p>
                <p>If A is in half the transactions and B is in half the transactions.</p>
                <ul>
                    <li>They meet in about a quarter of the transactions by chance alone</li>
                    <li>A high support can mean nothing more than two common items</li>
                    <li>Compare a pair with what chance would give</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Lift

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Confidence, and why we skip it</b></p>
                <p>$$\text{conf}(A \Rightarrow B) = \frac{\text{support}(A \cup B)}{\text{support}(A)}$$</p>
                <p>The share of transactions with A that also contain B.</p>
                <p>It ignores how common B is. If most transactions contain B, a rule toward B looks strong even when the items are unrelated <a href="https://doi.org/10.1145/253262.253325" target="_blank" rel="noopener noreferrer">(Brin et al., 1997)</a>.</p>
                <p>Lift divides by what independence predicts.</p>
                <br>
                <p>"It has the flaw that it ignores P(B)." <a href="https://doi.org/10.1145/253262.253325" target="_blank" rel="noopener noreferrer">(Brin et al., 1997)</a></p>
            </div>
        </div>
    </div>
</div>

## Lift

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Lift</b> <a href="https://doi.org/10.1145/253262.253325" target="_blank" rel="noopener noreferrer">(Brin et al., 1997)</a></p>
                <p>$$\text{lift}(A,B) = \frac{P(A,B)}{P(A)\,P(B)} = \frac{n_{AB} \cdot N}{n_A \cdot n_B}$$</p>
                <p>$n_A$ and $n_B$ are the transactions with each item.</p>
                <p>$n_{AB}$ is the support of the pair.</p>
                <p>$N$ is the number of transactions.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Independence</b></p>
                <p>If A and B are independent, $P(A,B) = P(A)\,P(B)$.</p>
                <ul>
                    <li><b>Lift = 1:</b> the pair meets as often as chance</li>
                    <li><b>Lift above 1:</b> the pair meets more often than chance</li>
                    <li><b>Lift below 1:</b> the items avoid each other</li>
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
                <p><b>A worked example</b></p>
                <ul>
                    <li><p>$N = {300}$ transactions</p></li>
                    <li><p>$n_A = {60}$ and $n_B = {30}$</p></li>
                    <li><p>$n_{AB} = {18}$</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>Expected by chance: $\frac{60 \cdot 30}{300} = {6}$</p>
                <p>$$\text{lift} = \frac{18 \cdot 300}{60 \cdot 30} = 3$$</p>
                <p>The pair meets three times more often than chance.</p>
            </div>
        </div>
    </div>
</div>

## Lift

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Rare items inflate lift</b></p>
                <p>Two items in 2 transactions each, together in both, with $N = {300}$:</p>
                <p>$$\text{lift} = \frac{2 \cdot 300}{2 \cdot 2} = 150$$</p>
                <p>A huge lift from two transactions. Lift is computed only on pairs that pass the support floor.</p>
            </div>
        </div>
    </div>
</div>

## Lift

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 35%">
                <p><b>Python</b></p>
                <p>Preparation: the pair counts, each item alone, and the number of transactions.</p>
                <ul>
                    <li>Only for the pairs at the floor</li>
                    <li>Support and lift often rank pairs differently <a href="https://doi.org/10.1145/775047.775053" target="_blank" rel="noopener noreferrer">(Tan et al., 2002)</a></li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 65%">

```python
def compute_lift(pair_support, n_a, n_b, n):
    return pair_support * n / (n_a * n_b)

table["lift"] = [
    compute_lift(count, item_count[a], item_count[b], n)
    for a, b, count in zip(table["item_a"], table["item_b"], table["support"])
]
```

            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
