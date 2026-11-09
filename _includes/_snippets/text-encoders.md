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
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Dictionaries:</b> a list of words that a person writes, with no training.</p>
                <p><b>Word counts:</b> weighted word columns and a model learned from the marks.</p>
                <p><b>Text encoders:</b> a pretrained model turns each text into one vector.</p>
                <p><b>Generative models:</b> a language model is asked for the answer in words.</p>
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
            <div class="column vertical-middle text-left" style="width: 55%">
                <p>Counts only see this collection.</p>
                <ul>
                    <li>A word never seen in the marked texts gets no weight</li>
                    <li>Two words with the same meaning are two unrelated columns</li>
                    <li>An encoder learned from many other texts places similar meanings close</li>
                </ul>
                <br>
                <p>"BERT is designed to pre-train deep bidirectional representations from unlabeled text by jointly conditioning on both left and right context in all layers." <a href="https://doi.org/10.18653/v1/N19-1423" target="_blank" rel="noopener noreferrer">(Devlin et al., 2019, abstract)</a></p>
            </div>
            <div class="column vertical-middle text-left" style="width: 45%">
                <img src="{{ site.url }}/assets/media/images/transformer-full-architecture.png" alt="Transformer architecture" style="height: 360px">
                <div class="footnote">Transformer, full architecture - dvgodoy, CC BY 4.0 <https://creativecommons.org/licenses/by/4.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Text Encoders

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 55%">
                <p><b>Preparation: tokens and subwords <a href="https://doi.org/10.18653/v1/P16-1162" target="_blank" rel="noopener noreferrer">(Sennrich et al., 2016)</a></b></p>
                <ul>
                    <li>An encoder reads tokens, not words</li>
                    <li>Rare words are split into known pieces</li>
                    <li>One vocabulary can cover many languages</li>
                    <li>Each model reads at most a fixed number of tokens, so longer texts are cut. We count how many</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 45%">
                <img src="{{ site.url }}/assets/media/images/transformer-full-architecture.png" alt="Transformer architecture" style="height: 360px">
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
                <p>Each token gets a vector that depends on the whole text. Mean pooling turns them into one vector per text.</p>
                <br>
                <p>$$\mathbf{v}(t) = \frac{1}{T} \sum_{j=1}^{T} \mathbf{h}_j \qquad \hat{\mathbf{v}} = \frac{\mathbf{v}}{\lVert \mathbf{v} \rVert}$$</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>$\mathbf{h}_j$ is the vector of token $j$ and $T$ the number of tokens read. The sum adds the token vectors and the division by $T$ takes their mean. Dividing by the length $\lVert \mathbf{v} \rVert$ scales the result to length 1, so the dot product of two texts is their cosine.</p>
            </div>
        </div>
    </div>
</div>

## Text Encoders

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <ul>
                    <li>Three tokens in two dimensions</li>
                    <li><p>$\mathbf{h}_1 = (1, 0)$, $\mathbf{h}_2 = (0, 1)$, $\mathbf{h}_3 = (1, 1)$</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>$$\mathbf{v} = \tfrac{1}{3}(2, 2) = (0.67, 0.67) \qquad \hat{\mathbf{v}} = (0.71, 0.71)$$</p>
                <p>The mean adds the first numbers, 1 + 0 + 1 = 2, and the second numbers, 0 + 1 + 1 = 2, then divides by 3. The length of (0.67, 0.67) is 0.94, so each number becomes 0.71. The same logistic regression then learns one weight per dimension.</p>
            </div>
        </div>
    </div>
</div>

## Text Encoders

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Frozen or fine-tuned</b></p>
                <ul>
                    <li><b>Frozen:</b> the encoder is a fixed function, and a small model learns on its vectors</li>
                    <li><b>Fine-tuned:</b> the encoder itself changes, which needs more marked texts and a GPU</li>
                </ul>
                <br>
                <p>"there are major computational benefits to pre-compute an expensive representation of the training data once and then run many experiments with cheaper models on top of this representation." <a href="https://doi.org/10.18653/v1/N19-1423" target="_blank" rel="noopener noreferrer">(Devlin et al., 2019, section 5.3)</a></p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Set before the results</b></p>
                <ul>
                    <li>The model and its token limit</li>
                    <li>The prefix the model card asks for</li>
                </ul>
                <p><b>Limits</b></p>
                <ul>
                    <li>Text past the token limit is never read</li>
                    <li>The vector does not say why a text is a yes</li>
                    <li>The model carries the biases of the texts it learned from</li>
                </ul>
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
    split it into tokens, cut at the limit
    one vector per token, from the whole text
    mean of the token vectors, scaled to length 1
learn logistic regression on the training vectors
predict on the kept apart vectors
```

            </div>
            <div class="column vertical-middle text-left" style="width: 5%">
            </div>
            <div class="column vertical-middle text-left" style="width: 47.5%">

```python
from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression

def encode(texts, model_name):
    encoder = SentenceTransformer(model_name)
    return encoder.encode(list(texts),
                          normalize_embeddings=True)

train_vectors = encode(train_texts, MODEL_NAME)
test_vectors = encode(test_texts, MODEL_NAME)
model = LogisticRegression(class_weight="balanced",
                           max_iter=1000)
model.fit(train_vectors, train_marks)
predictions = model.predict(test_vectors)
```

            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
