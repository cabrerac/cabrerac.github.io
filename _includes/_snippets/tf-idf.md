<!-- SLIDES: -->

## TF-IDF

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p><b>TF-IDF</b> gives a word a high weight in a text when it is frequent in that text and rare in the others.</p>
            </div>
        </div>
    </div>
</div>

## TF-IDF

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <p><b>Term frequency</b></p>
                <p>$$\text{tf}(w, d) = 1 + \log c(w, d)$$</p>
                <p>$c(w, d)$ is how many times word $w$ appears in document $d$, zero stays zero.</p>
                <p>The log stops one repeated word from taking over.</p>
                <p>Ten mentions count more than one, but not ten times more.</p>
                <p><a href="https://doi.org/10.1016/0306-4573(88)90021-0" target="_blank" rel="noopener noreferrer">(Salton &amp; Buckley, 1988)</a></p>
            </div>
        </div>
    </div>
</div>

## TF-IDF

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <p><b>Inverse document frequency</b> <a href="https://doi.org/10.1108/eb026526" target="_blank" rel="noopener noreferrer">(Sparck Jones, 1972)</a></p>
                <p>$$\text{idf}(w) = \log \frac{1 + N}{1 + \text{df}(w)} + 1$$</p>
                <ul>
                    <li><p>$N$ is the number of documents, $\text{df}(w)$ the documents with word $w$</p></li>
                    <li><p>A word in every document gets the lowest weight</p></li>
                    <li><p>A word in few documents gets a high weight</p></li>
                    <li><p>The +1 inside the fraction avoids a division by zero</p></li>
                    <li><p>The +1 outside keeps a word that is in every document from getting weight 0 <a href="https://scikit-learn.org/stable/modules/feature_extraction.html#tfidf-term-weighting" target="_blank" rel="noopener noreferrer">(scikit-learn TF-IDF)</a></p></li>
                </ul>
            </div>
        </div>
    </div>
</div>

## TF-IDF

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <p><b>The document by word matrix</b></p>
                <p>$$x_{dw} = \text{tf}(w, d) \cdot \text{idf}(w)$$</p>
                <p>One row per document, one column per word.</p>
                <p>Each row scaled to length 1, so long texts do not win.</p>
                <p>The weights are learned on the training texts only.</p>
                <p>Texts kept apart are transformed with those same weights.</p>
            </div>
        </div>
    </div>
</div>

## TF-IDF

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 35%">
                <p><b>Python</b></p>
                <ul>
                    <li>The same word function</li>
                    <li>Fitted on training rows only</li>
                    <li>Transform the kept apart rows</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 65%">


```python
from sklearn.feature_extraction.text import TfidfVectorizer

# train_tokens, test_tokens: one word list per text, repeats kept
tfidf = TfidfVectorizer(analyzer=lambda tokens: tokens,
                        sublinear_tf=True)          # tf = 1 + log(count)
X_train = tfidf.fit_transform(train_tokens)     # fitted on the training rows only
X_test = tfidf.transform(test_tokens)           # the marked texts kept apart
feature_names = tfidf.get_feature_names_out()   # one name per column
print(X_train.shape)
```

            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
