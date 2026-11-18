<!-- SLIDES: -->

## TF-IDF with Logistic Regression

<div class="rows" style="height: 100%">
    <div class="row" style="height: 70%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img class="external-svg" src="{{ site.url }}/assets/media/diagrams/text-task-taxonomy.svg" alt="Taxonomy of text extraction methods" style="width: 100%; height: 100%">
            </div>
        </div>
    </div>
    <div class="row" style="height: 30%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <p><b>Dictionaries:</b> a list of words a person writes, with no training.</p>
                <p><b>Word counts:</b> weighted words and a model learned from the marks.</p>
                <p><b>Text encoders:</b> a pretrained model turns a text into one vector.</p>
                <p><b>Generative models:</b> a language model answers in words.</p>
            </div>
        </div>
    </div>
</div>

## TF-IDF with Logistic Regression

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p><b>TF-IDF with logistic regression</b> weights each word by how much it says about one text, then learns from marked texts how each weighted word pushes a text towards yes.</p>
            </div>
        </div>
    </div>
</div>

## TF-IDF with Logistic Regression

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>A list only sees the words a person wrote.</p>
                <ul>
                    <li>Other words can point to the answer too</li>
                    <li>The marked texts show which words go with yes and which with no</li>
                    <li>So each word gets a weight in each text, and a model learns one weight per word</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/topic-detection-document-word-matrix.gif" alt="Blocks of words appear in a document word matrix" style="height: 360px">
                <div class="footnote">Topic detection in a document-word matrix - Christoph Carl Kling, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## TF-IDF with Logistic Regression

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>$$\text{tf}(w, d) = 1 + \ln c(w, d)$$</p>
                <p>$c(w, d)$ counts word $w$ in text $d$. The log stops one repeated word from taking over <a href="https://doi.org/10.1016/0306-4573(88)90021-0" target="_blank" rel="noopener noreferrer">(Salton &amp; Buckley, 1988)</a>.</p>
                <p>$$\text{idf}(w) = \ln \frac{1 + N}{1 + \text{df}(w)} + 1$$</p>
                <p>$N$ is the number of texts and $\text{df}(w)$ the texts with word $w$. A rare word gets a large weight <a href="https://doi.org/10.1108/eb026526" target="_blank" rel="noopener noreferrer">(Sparck Jones, 1972)</a>.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>$$x_{dw} = \text{tf}(w, d) \cdot \text{idf}(w)$$</p>
                <p>Each text becomes a row with one weight per word, scaled to length 1.</p>
                <p>The IDF is learned on the training texts only, and reused on the texts kept apart.</p>
            </div>
        </div>
    </div>
</div>

## TF-IDF with Logistic Regression

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <ul>
                    <li><p>Three short texts, $N = 3$</p></li>
                    <li>"free" is in 1 text, twice in text A</li>
                    <li>"prize" and "noon" are in 2 texts each</li>
                </ul>
                <p>$$\text{tf} = 1 + \ln 2 = 1.69 \qquad \text{idf} = \ln \tfrac{4}{2} + 1 = 1.69$$</p>
                <p>So free gets about 2.87 in text A. A word in all three texts gets an IDF of 1.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/diagrams/tfidf-three-texts.svg" alt="Word counts of three texts and the TF-IDF of free" style="height: 380px">
            </div>
        </div>
    </div>
</div>

## TF-IDF with Logistic Regression

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Logistic regression <a href="https://doi.org/10.1111/j.2517-6161.1958.tb00292.x" target="_blank" rel="noopener noreferrer">(Cox, 1958)</a></b></p>
                <p>$$P(y = 1 \mid \mathbf{x}) = \sigma(\mathbf{w} \cdot \mathbf{x} + b), \quad \sigma(z) = \frac{1}{1 + e^{-z}}$$</p>
                <p>$\mathbf{x}$ is the TF-IDF row of a text, $\mathbf{w}$ one weight per word, and $b$ the intercept.</p>
                <p>$\sigma$ turns the sum into a probability, yes from 0.5. $\sigma(2) = 0.88$ is a yes.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/logistic-curve.svg" alt="Logistic curve" style="height: 320px">
                <div class="footnote">Logistic-curve - Qef, Public domain, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## TF-IDF with Logistic Regression

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 47.5%">

```text
split the rows, before any fit
on the training rows
    learn the IDF of each word
    one TF-IDF row of length 1 per text
    one weight per word, balanced classes
on the marked rows
    yes when the probability is at least 0.5
```

            </div>
            <div class="column vertical-middle text-left" style="width: 5%">
            </div>
            <div class="column vertical-middle text-left" style="width: 47.5%">

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

token_lists = [word_list(t, STOP_WORDS) for t in texts]
train_tokens = [token_lists[i] for i in train_rows]
tfidf = TfidfVectorizer(analyzer=lambda tokens: tokens,
                        sublinear_tf=True)
X_train = tfidf.fit_transform(train_tokens)
X_marked = tfidf.transform(
    [token_lists[i] for i in marked_rows])

tfidf_model = LogisticRegression(
    class_weight="balanced", C=C_REG, max_iter=1000
).fit(X_train, y_train)
pred_tfidf = tfidf_model.predict(X_marked)
```

            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
