<!-- SLIDES: -->

## Lift

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p><b>Lift</b> compares how often two words appear together with how often they would meet by chance alone.</p>
            </div>
        </div>
    </div>
</div>

## Lift

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Support favours common words</b></p>
                <p>If A is in half the texts and B is in half the texts.</p>
                <p>They meet in about a quarter of the texts by chance alone.</p>
                <p>A high support can mean nothing more than two common words.</p>
                <p>We need to compare a pair with what chance would give.</p>
            </div>
        </div>
    </div>
</div>

## Lift

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <p><b>Confidence, and why we skip it</b></p>
                <p>$$\text{conf}(A \Rightarrow B) = \frac{\text{support}(A \cup B)}{\text{support}(A)}$$</p>
                <p>The share of texts with A that also contain B.</p>
                <p>It ignores how common B is. If 80% of shoppers buy milk, smoked salmon to milk has 80% confidence even when the two are unrelated <a href="https://doi.org/10.1145/253262.253325" target="_blank" rel="noopener noreferrer">(Brin et al., 1997)</a>.</p>
                <p>Lift fixes this by dividing by what independence predicts.</p>
                <table class="table">
                    <tr>
                        <td>
                            <p>"It has the flaw that it ignores P(B)."</p>
                            <p><a href="https://doi.org/10.1145/253262.253325" target="_blank" rel="noopener noreferrer">(Brin et al., 1997)</a></p>
                        </td>
                    </tr>
                </table>
                <p>This course uses support and lift.</p>
            </div>
        </div>
    </div>
</div>

## Lift

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <p><b>Lift</b> <a href="https://doi.org/10.1145/253262.253325" target="_blank" rel="noopener noreferrer">(Brin et al., 1997)</a></p>
                <p>$$\text{lift}(A,B) = \frac{P(A,B)}{P(A)\,P(B)} = \frac{n_{AB} \cdot N}{n_A \cdot n_B}$$</p>
                <p>$n_A$ and $n_B$ are the texts with each word.</p>
                <p>$n_{AB}$ is the support of the pair.</p>
                <p>$N$ is the number of texts.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Independence</b></p>
                <p>If A and B are independent, $P(A,B) = P(A)\,P(B)$.</p>
                <p><b>Lift = 1</b> - the pair meets as often as chance.</p>
                <p><b>Lift above 1</b> - the pair meets more often than chance.</p>
                <p><b>Lift below 1</b> - the words avoid each other.</p>
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
                    <li><p>$N = {300}$ texts</p></li>
                    <li><p>$n_A = {60}$ and $n_B = {30}$</p></li>
                    <li><p>$n_{AB} = {18}$</p></li>
                </ul>
            </div>
            <div class="column vertical-top text-left" style="width: 50%">
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
            <div class="column vertical-top text-left" style="width: 100%">
                <p><b>Rare words inflate lift</b></p>
                <p>Two words in 2 texts each, together in both, with $N = {300}$:</p>
                <p>$$\text{lift} = \frac{2 \cdot 300}{2 \cdot 2} = 150$$</p>
                <p>A huge lift from two texts. This is why lift is computed only on pairs that pass the support floor.</p>
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
                <p>Preparation: the pair counts, each word alone, and the number of texts.</p>
                <p>Only for the pairs at the floor.</p>
                <p>Support and lift often rank pairs very differently. Neither is right on its own <a href="https://doi.org/10.1145/775047.775053" target="_blank" rel="noopener noreferrer">(Tan et al., 2002)</a>.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 65%">


```python
def compute_lift(pair_support, n_a, n_b, n):
    return pair_support * n / (n_a * n_b)

lift = {(a, b): compute_lift(c, word_count[a], word_count[b], N)
        for (a, b), c in candidates.items()}
top = sorted(lift, key=lift.get, reverse=True)[:10]
```

            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
