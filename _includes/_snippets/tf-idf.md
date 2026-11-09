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
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Dictionaries:</b> a list of words that a person writes, with no training.</p>
                <p><b>Word counts:</b> weighted word columns and a model learned from the marks.</p>
                <p><b>Text encoders:</b> a pretrained model turns each text into one vector.</p>
                <p><b>Generative models:</b> a language model is asked for the answer in words.</p>
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
                <p><b>Term frequency <a href="https://doi.org/10.1016/0306-4573(88)90021-0" target="_blank" rel="noopener noreferrer">(Salton &amp; Buckley, 1988)</a></b></p>
                <p>$$\text{tf}(w, d) = 1 + \log c(w, d)$$</p>
                <p>$c(w, d)$ is how many times word $w$ appears in text $d$, and zero stays zero. The log stops one repeated word from taking over. Ten mentions count more than one, but not ten times more.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Inverse document frequency <a href="https://doi.org/10.1108/eb026526" target="_blank" rel="noopener noreferrer">(Sparck Jones, 1972)</a></b></p>
                <p>$$\text{idf}(w) = \log \frac{1 + N}{1 + \text{df}(w)} + 1$$</p>
                <p>$N$ is the number of texts and $\text{df}(w)$ the texts with word $w$. The fraction is large for a rare word. The +1 inside avoids a division by zero, and the +1 outside keeps a word in every text above 0.</p>
            </div>
        </div>
    </div>
</div>

## TF-IDF with Logistic Regression

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Preparation: the text by word matrix</b></p>
                <p>$$x_{dw} = \text{tf}(w, d) \cdot \text{idf}(w)$$</p>
                <ul>
                    <li>One row per text, one column per word</li>
                    <li>Each row scaled to length 1, so long texts do not win</li>
                    <li>The IDF is learned on the training texts only, and reused on the texts kept apart</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Logistic regression <a href="https://doi.org/10.1111/j.2517-6161.1958.tb00292.x" target="_blank" rel="noopener noreferrer">(Cox, 1958)</a></b></p>
                <p>$$P(y = 1 \mid \mathbf{x}) = \sigma(\mathbf{w} \cdot \mathbf{x} + b), \quad \sigma(z) = \frac{1}{1 + e^{-z}}$$</p>
                <p>$\mathbf{x}$ is the TF-IDF row of a text and $\mathbf{w}$ one weight per word. $b$ is the intercept. $\sigma$ turns the weighted sum into a probability between 0 and 1. Yes when it is at least 0.5.</p>
            </div>
        </div>
    </div>
</div>

## TF-IDF with Logistic Regression

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Log loss</b></p>
                <p>$$\mathcal{L} = -\sum_{i=1}^{n} \left[ y_i \log p_i + (1 - y_i) \log (1 - p_i) \right]$$</p>
                <p>$y_i$ is the mark of text $i$, 1 or 0. $p_i$ is its predicted probability. Only one of the two terms is on for each text. A confident wrong answer costs a lot, and the weights are found by minimising the sum.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Penalty and class weights</b></p>
                <p>$$\min_{\mathbf{w}, b} \ \frac{1}{2} \lVert \mathbf{w} \rVert^2 + C \sum_{i} s_{y_i} \, \ell_i$$</p>
                <p>$\ell_i$ is the log loss of text $i$. The first term keeps the weights small, and a larger $C$ means a weaker penalty. $s_y = n / (2\, n_y)$ gives the rare class the same total weight, so saying no to everything does not win.</p>
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
                    <li><p>$N = 4$ texts</p></li>
                    <li>"free" is in 1 of them</li>
                    <li>Text A says "free" 3 times</li>
                    <li><p>After the weighted sum, $z = 2$ for text A</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>$$\text{idf} = \log \tfrac{5}{2} + 1 = 1.92 \qquad \text{tf} = 1 + \log 3 = 2.10$$</p>
                <p>So "free" gets 2.10 times 1.92, about 4.0, in text A, before the row is scaled to length 1. A word in all 4 texts would get an IDF of only 1.</p>
                <br>
                <p>$$\sigma(2) = \frac{1}{1 + e^{-2}} = 0.88$$</p>
                <p>0.88 is at least 0.5, so text A is a yes.</p>
            </div>
        </div>
    </div>
</div>

## TF-IDF with Logistic Regression

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Set before the results</b></p>
                <ul>
                    <li><p>$C$, the penalty</p></li>
                    <li>The threshold, 0.5</li>
                    <li>The split into training and kept apart texts</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Limits</b></p>
                <ul>
                    <li>Word order is lost</li>
                    <li>A word never seen in training gets no weight</li>
                    <li>Few marked texts give unstable weights</li>
                    <li>A strange word near the top of the weights is worth a look</li>
                </ul>
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
split the marked texts, before any fit
on the training texts only
    learn the IDF of each word
    turn each text into a TF-IDF row of length 1
    learn one weight per word, balanced classes
on the kept apart texts
    the same IDF, then the weighted sum
    yes when the probability is at least 0.5
```

            </div>
            <div class="column vertical-middle text-left" style="width: 5%">
            </div>
            <div class="column vertical-middle text-left" style="width: 47.5%">

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline

def tfidf_logistic(C):
    return make_pipeline(
        TfidfVectorizer(sublinear_tf=True),
        LogisticRegression(C=C, class_weight="balanced",
                           max_iter=1000),
    )

model = tfidf_logistic(C=1.0).fit(train_texts, train_marks)
predictions = model.predict(test_texts)
```

            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
