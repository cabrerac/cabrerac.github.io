<!-- SLIDES: -->

## Text Encoders

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

## Text Encoders

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p>A <b>text encoder</b> is a pretrained model that turns a whole text into one vector of numbers.</p>
            </div>
        </div>
    </div>
</div>

## Text Encoders

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>Counts only see this collection.</p>
                <ul>
                    <li>A word never seen in the marked texts gets no weight</li>
                    <li>Two words with the same meaning are two unrelated columns</li>
                    <li>An encoder learned from many other texts places similar meanings close</li>
                </ul>
                <br>
                <p>"BERT is designed to pre-train deep bidirectional representations from unlabeled text by jointly conditioning on both left and right context in all layers." <a href="https://doi.org/10.18653/v1/N19-1423" target="_blank" rel="noopener noreferrer">(Devlin et al., 2019, abstract)</a></p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/transformer-full-architecture.png" alt="Transformer architecture" style="height: auto">
                <div class="footnote">Transformer, full architecture - dvgodoy, CC BY 4.0 <https://creativecommons.org/licenses/by/4.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Text Encoders

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>An encoder reads tokens, words or pieces of words <a href="https://doi.org/10.18653/v1/P16-1162" target="_blank" rel="noopener noreferrer">(Sennrich et al., 2016)</a>.</p>
                <ul>
                    <li><b>Token limit:</b> at most 512 tokens, so longer texts are cut</li>
                    <li><b>Frozen:</b> the encoder is fixed, and a model learns on its vectors</li>
                    <li><b>Fine-tuned:</b> the encoder itself changes, with more marks and a GPU</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/diagrams/encoder-pipeline.svg" alt="From a text to a yes or a no with a text encoder" style="height: 400px">
            </div>
        </div>
    </div>
</div>

## Text Encoders

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>Each token gets a vector that depends on its context. Mean pooling turns them into one vector per text.</p>
                <br>
                <p>$$\mathbf{v}(t) = \frac{1}{T} \sum_{j=1}^{T} \mathbf{h}_j$$</p>
                <br>
                <p>$\mathbf{h}_j$ is the vector of token $j$, and $T$ the number of tokens read. The sum divided by $T$ is their mean.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
               <img class="external-svg" src="{{ site.url }}/assets/media/diagrams/encoder-pipeline.svg" alt="From a text to a yes or a no with a text encoder" style="height: 400px">
            </div>
        </div>
    </div>
</div>

## Text Encoders

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>Scaling removes the length, so only the direction remains.</p>
                <br>
                <p>$$\hat{\mathbf{v}} = \frac{\mathbf{v}}{\lVert \mathbf{v} \rVert}$$</p>
                <br>
                <p>Dividing by the length $\lVert \mathbf{v} \rVert$ gives length 1.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
               <img class="external-svg" src="{{ site.url }}/assets/media/diagrams/encoder-pipeline.svg" alt="From a text to a yes or a no with a text encoder" style="height: 400px">
            </div>
        </div>
    </div>
</div>

## Text Encoders

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>Three tokens in two dimensions.</p>
                <p>$\mathbf{h}_1 = (1, 0)$, $\mathbf{h}_2 = (0, 1)$, $\mathbf{h}_3 = (1, 1)$.</p>
                <br>
                <p>$$\mathbf{v} = \tfrac{1}{3}(2, 2) = (0.67, 0.67)$$</p>
                <br>
                <p>The first numbers add to 2 and the second numbers add to 2. Dividing by 3 gives the mean. Its length is 0.94, and scaling makes each number 0.71.</p>
                <p>The dimensions of the tokens are defined by the pre-trained model. In this example $m = 2$. For the model, $m = 384$. At the end, we have a matrix of $n \times m$, where $n$ is the number of texts and $m$ is the dimension of the tokens. Scaling makes the magnitude 1 and leaves $m$ unchanged.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/diagrams/encoder-pipeline.svg" alt="From a text to a yes or a no with a text encoder" style="height: 400px">
            </div>
        </div>
    </div>
</div>

## Text Encoders

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>Logistic regression turns the vector into a probability of yes <a href="https://doi.org/10.1111/j.2517-6161.1958.tb00292.x" target="_blank" rel="noopener noreferrer">(Cox, 1958)</a>.</p>
                <br>
                <p>$$P(y = 1 \mid \mathbf{x}) = \sigma(\mathbf{w} \cdot \mathbf{x} + b)$$</p>
                <p>$$\sigma(z) = \frac{1}{1 + e^{-z}}$$</p>
                <br>
                <p>$\mathbf{x}$ is the encoder vector of length 1, $\mathbf{w}$ one weight per number in that vector, and $b$ the intercept. $\sigma$ turns the sum into a probability. Yes starts at 0.5. These weights cannot be read as words. The encoder stays fixed.</p>
                <p>We train logistic regression on the marked texts to learn $\mathbf{w}$ and $b$. We approximate a function that maps $\mathbf{x}$ to yes or no and minimises the prediction loss.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/logistic-curve.svg" alt="Logistic curve" style="height: 320px">
                <div class="footnote">Logistic-curve - Qef, Public domain, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Text Encoders

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 47.5%">

```text
load the pretrained encoder once
for each text
    add the prefix "passage: "
    tokens, cut at 512
    one vector per token
    mean vector, scaled to length 1
logistic regression on the training rows
predict on the marked rows
```

            </div>
            <div class="column vertical-middle text-left" style="width: 5%">
            </div>
            <div class="column vertical-middle text-left" style="width: 47.5%">

```python
from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression

encoder = SentenceTransformer(TEXT_MODEL, device="cpu")
encoder.max_seq_length = MAX_LENGTH
encoder_texts = [PREFIX + t for t in texts]
vectors = encoder.encode(encoder_texts,
                         normalize_embeddings=True,
                         batch_size=16)

encoder_model = LogisticRegression(
    class_weight="balanced", C=C_REG, max_iter=1000
).fit(vectors[train_rows], y_train)
pred_encoder = encoder_model.predict(vectors[marked_rows])
```

            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
