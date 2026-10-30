<!-- SLIDES: -->

## Repeating Patterns

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>What is a pattern</b></p>
                <ul>
                    <li>Something that repeats across many transactions</li>
                    <li>Products bought together in many baskets</li>
                    <li>Words used together in many texts</li>
                </ul>
                <p>We count transactions, not mentions.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/supermarket-checkout.jpg" alt="Supermarket checkout" style="height: 400px">
                <div class="footnote">Supermarket checkout Tegut Tauberbischofsheim - Triplec85, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Repeating Patterns

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Texts as transactions</b></p>
                <table class="table">
                    <thead>
                        <tr>
                            <th>Transaction</th>
                            <th>Items</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr><td>Basket 1</td><td>bread, milk, eggs</td></tr>
                        <tr><td>Basket 2</td><td>bread, butter</td></tr>
                        <tr><td><b>One paper's title and abstract</b></td><td><b>its distinct words</b></td></tr>
                        <tr><td>Text 1</td><td>diet, obesity, children, school</td></tr>
                        <tr><td>Text 2</td><td>obesity, sugar, tax</td></tr>
                    </tbody>
                </table>
                <p>Each text becomes a transaction: the set of distinct words it contains. Order and repeats inside the text are gone.</p>
            </div>
        </div>
    </div>
</div>

## Repeating Patterns

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>One standout text is not a pattern</b></p>
                <ul>
                    <li>A text that says "sugar tax" twenty times is still one text</li>
                    <li>A pair seen in one or two texts can be luck or one author's style</li>
                    <li>A pattern needs a minimum number of texts</li>
                    <li>And it needs to beat what chance would give</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Repeating Patterns

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 60%">
                <p><b>Market basket analysis</b></p>
                <table class="table">
                    <tr>
                        <td>
                            <p>"We are given a large database of customer transactions. Each transaction consists of items purchased by a customer in a visit."</p>
                            <p><a href="https://doi.org/10.1145/170036.170072" target="_blank" rel="noopener noreferrer">(Agrawal et al., 1993)</a></p>
                        </td>
                    </tr>
                </table>
                <ul>
                    <li>Association rules from IBM Almaden</li>
                    <li>The start of frequent pattern mining</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 40%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/rakesh-agrawal.jpg" alt="Rakesh Agrawal" style="height: 340px">
                <div class="footnote">Rakesh Agrawal - bwatpu, CC BY-SA 3.0 <https://creativecommons.org/licenses/by-sa/3.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Repeating Patterns

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Counting faster, judging better</b></p>
                <ul>
                    <li><b>1994, Apriori</b> - drop rare items early <a href="https://www.vldb.org/conf/1994/P487.PDF" target="_blank" rel="noopener noreferrer">(Agrawal &amp; Srikant, 1994)</a></li>
                    <li><b>1997, interest</b> - compare a pair with chance, later called lift <a href="https://doi.org/10.1145/253262.253325" target="_blank" rel="noopener noreferrer">(Brin et al., 1997)</a></li>
                    <li><b>2000, FP-growth</b> - count without listing every candidate <a href="https://doi.org/10.1145/335191.335372" target="_blank" rel="noopener noreferrer">(Han et al., 2000)</a></li>
                    <li><b>2002, interestingness</b> - many measures, and they disagree <a href="https://doi.org/10.1145/775047.775053" target="_blank" rel="noopener noreferrer">(Tan et al., 2002)</a></li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Repeating Patterns

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Words that share company</b></p>
                <table class="table">
                    <tr>
                        <td>
                            <p>"Difference of meaning correlates with difference of distribution."</p>
                            <p><a href="https://doi.org/10.1080/00437956.1954.11659520" target="_blank" rel="noopener noreferrer">(Harris, 1954, p. 156)</a></p>
                        </td>
                    </tr>
                </table>
                <p>Firth (1957) argued that we learn what a word means from the words around it. (Firth, J. R., 1957, A synopsis of linguistic theory, 1930-1955, Studies in Linguistic Analysis, p. 11)</p>
                <p>Two words that appear in the same contexts tend to mean similar things.</p>
            </div>
        </div>
    </div>
</div>

## Repeating Patterns

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 60%">
                <p><b>From counts to vectors</b></p>
                <ul>
                    <li><b>2013, word2vec</b> - learn a vector per word from its neighbours <a href="https://arxiv.org/abs/1301.3781" target="_blank" rel="noopener noreferrer">(Mikolov et al., 2013)</a></li>
                    <li><b>2014, GloVe</b> - vectors from global co-occurrence counts <a href="https://aclanthology.org/D14-1162/" target="_blank" rel="noopener noreferrer">(Pennington et al., 2014)</a></li>
                    <li><b>2017, fastText</b> - vectors from parts of words <a href="https://doi.org/10.1162/tacl_a_00051" target="_blank" rel="noopener noreferrer">(Bojanowski et al., 2017)</a></li>
                </ul>
                <p>Pretrained vectors bring what other texts say about a word.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 40%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/tomas-mikolov.jpg" alt="Tomas Mikolov" style="height: 340px">
                <div class="footnote">Tomáš Mikolov (2020) - Jindřich Nosek (NoJin), CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
