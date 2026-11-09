<!-- SLIDES: -->

## Support

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p>A <b>frequent pair</b> is a pair of items that appear together in at least a minimum number of transactions, the support floor.</p>
            </div>
        </div>
    </div>
</div>

## Support

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>One set of items per transaction.</p>
                <ul>
                    <li>All pairs of items inside each set</li>
                    <li>A count of transactions for each pair</li>
                    <li>{A, B, C} gives three pairs: A + B, A + C, B + C</li>
                </ul>
                <p>The items may be products in a receipt, codes in a visit, or distinct words in a text.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/frequent-itemsets-lattice.png" alt="Itemset lattice" style="height: 360px">
                <div class="footnote">FrequentItems - Xodarap00, CC BY-SA 3.0 <https://creativecommons.org/licenses/by-sa/3.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Support

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>The support of a pair is the number of transactions that hold both items.</p>
                <br>
                <p>$$\text{support}(A,B) = \left|\{\, i : A \in T_i \text{ and } B \in T_i \,\}\right|$$</p>
                <br>
                <p>$T_i$ is the set of distinct items in transaction $i$, and $N$ is the number of transactions.</p>
                <br>
                <p>For $N$ transactions</p>
                <br>
                <p>$$P(A,B) = \text{support}(A,B) / N$$</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/frequent-itemsets-lattice.png" alt="Itemset lattice" style="height: 360px">
                <div class="footnote">FrequentItems - Xodarap00, CC BY-SA 3.0 <https://creativecommons.org/licenses/by-sa/3.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Support

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>The support of a pair is the number of transactions that hold both items.</p>
                <br>
                <p>$$\text{support}(A,B) = \left|\{\, i : A \in T_i \text{ and } B \in T_i \,\}\right|$$</p>
                <br>
                <p>$T_i$ is the set of distinct items in transaction $i$, and $N$ is the number of transactions.</p>
                <br>
                <p>For $N$ transactions</p>
                <br>
                <p>$$P(A,B) = \text{support}(A,B) / N$$</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <table class="table">
                    <thead>
                        <tr><th>Transaction</th><th>Items</th></tr>
                    </thead>
                    <tbody>
                        <tr><td>1</td><td>{A, B, C}</td></tr>
                        <tr><td>2</td><td>{A, C}</td></tr>
                        <tr><td>3</td><td>{B, C}</td></tr>
                        <tr><td>4</td><td>{A, B, C}</td></tr>
                    </tbody>
                </table>
                <p><b>Support</b></p>
                <ul>
                  <li><b>A + C:</b> 3 transactions</li>
                  <li><b>B + C:</b> 3 transactions</li>
                  <li><b>A + B:</b> 2 transactions</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Support

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>A pair needs at least $k$ transactions. The support floor is chosen before the results.</p>
                <br>
                <p>$$k = \max\left(k_{\min},\ \lceil s \cdot N \rceil\right)$$</p>
                <br>
                <p>$s$ is a small share of the collection. $k_{\min}$ is a minimum count.</p>
                <br>
                <p>"This is used to make sure that the items this rule applies to actually occur frequently enough for someone to care." <a href="https://doi.org/10.1145/253262.253325" target="_blank" rel="noopener noreferrer">(Brin et al., 1997)</a></p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/frequent-itemsets-lattice.png" alt="Itemset lattice" style="height: 360px">
                <div class="footnote">FrequentItems - Xodarap00, CC BY-SA 3.0 <https://creativecommons.org/licenses/by-sa/3.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Support

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>We need a support floor because one standout transaction cannot make a pattern alone.</p>
                <ul>
                    <li>Rare pairs look strong by luck</li>
                    <li>The list stays small enough to read</li>
                    <li>1,000 items give 499,500 possible pairs</li>
                </ul>
                <br>
                <p>$$\binom{V}{2} = \frac{V(V-1)}{2}$$</p>
                <br>
                <p>$V$ is the number of distinct items. The binomial count is every unordered pair those items can form. The fraction lists each ordered pair, then divides by 2, so A with B is the same pair as B with A.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/frequent-itemsets-lattice.png" alt="Itemset lattice" style="height: 360px">
                <div class="footnote">FrequentItems - Xodarap00, CC BY-SA 3.0 <https://creativecommons.org/licenses/by-sa/3.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Support

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>A pair cannot be in more transactions than either of its items. If an item is below the floor, every pair with it is below the floor. <b>The Apriori property</b> <a href="https://www.vldb.org/conf/1994/P487.PDF" target="_blank" rel="noopener noreferrer">(Agrawal &amp; Srikant, 1994)</a></p>
                <p>Drop rare items, then count pairs.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/frequent-itemsets-lattice.png" alt="Itemset lattice" style="height: 360px">
                <div class="footnote">FrequentItems - Xodarap00, CC BY-SA 3.0 <https://creativecommons.org/licenses/by-sa/3.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Support

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 47.5%">

```text
N = number of transactions
floor = max(minimum, ceil(share * N))

item_count = transactions that contain each item
frequent items = items with item_count at least floor

pair_count starts at 0
for each transaction
    items = frequent items in this transaction
    for each pair of those items
        add 1 to pair_count for that pair

keep pairs with pair_count at least floor
```

            </div>
            <div class="column vertical-middle text-left" style="width: 5%">
            </div>
            <div class="column vertical-middle text-left" style="width: 47.5%">

```python
import math
from collections import Counter
from itertools import combinations

def support_floor(n_transactions, minimum, share):
    return max(minimum, math.ceil(share * n_transactions))

def count_pairs(transactions, minimum, share):
    floor = support_floor(len(transactions), minimum, share)
    item_count = Counter(
        item for basket in transactions for item in basket
    )
    pairs = Counter()
    for basket in transactions:
        # Apriori
        frequent = sorted(
            item for item in basket if item_count[item] >= floor
        )
        pairs.update(combinations(frequent, 2))
    return {
        pair: count
        for pair, count in pairs.items()
        if count >= floor
    }

candidates = count_pairs(transactions, minimum, share)
```

            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
