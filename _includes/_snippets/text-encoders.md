<!-- SLIDES: -->

## Text Encoders

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Tokens and subwords</b> <a href="https://doi.org/10.18653/v1/P16-1162" target="_blank" rel="noopener noreferrer">(Sennrich et al., 2016)</a></p>
                <ul>
                    <li>An encoder reads tokens, not words</li>
                    <li>Rare words are split into known pieces</li>
                    <li>One vocabulary covers many languages</li>
                    <li>Each model reads at most a fixed number of tokens</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Text Encoders

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 55%">
                <p><b>The encoder</b></p>
                <table class="table">
                    <tr>
                        <td>
                            <p>"BERT is designed to pre-train deep bidirectional representations from unlabeled text by jointly conditioning on both left and right context in all layers."</p>
                            <p><a href="https://doi.org/10.18653/v1/N19-1423" target="_blank" rel="noopener noreferrer">(Devlin et al., 2019, abstract)</a></p>
                        </td>
                    </tr>
                </table>
                <ul>
                    <li>Each token gets a vector that depends on the whole text</li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 45%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/transformer-full-architecture.png" alt="Transformer architecture, encoder on the left" style="height: 400px">
                <div class="footnote">Transformer, full architecture - dvgodoy, CC BY 4.0 <https://creativecommons.org/licenses/by/4.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Text Encoders

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p><b>Mean pooling</b></p>
                <p>$$\mathbf{v}(t) = \frac{1}{T} \sum_{j=1}^{T} \mathbf{h}_j \qquad \hat{\mathbf{v}} = \frac{\mathbf{v}}{\lVert \mathbf{v} \rVert}$$</p>
                <ul>
                    <li><p>$\mathbf{h}_j$ is the vector of token $j$, $T$ the tokens read</p></li>
                    <li><p>One vector per text, of fixed size</p></li>
                    <li><p>Scaled to length 1, so the dot product is the cosine</p></li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Text Encoders

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Frozen versus fine-tuned</b></p>
                <table class="table">
                    <tr>
                        <td>
                            <p>"there are major computational benefits to pre-compute an expensive representation of the training data once and then run many experiments with cheaper models on top of this representation."</p>
                            <p><a href="https://doi.org/10.18653/v1/N19-1423" target="_blank" rel="noopener noreferrer">(Devlin et al., 2019, section 5.3)</a></p>
                        </td>
                    </tr>
                </table>
                <ul>
                    <li><b>Frozen</b> - the encoder is a fixed function, a small model learns on its vectors</li>
                    <li><b>Fine-tuned</b> - the encoder itself changes, needs more marked texts and a GPU</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Text Encoders

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>One model for many languages</b></p>
                <table class="table">
                    <tr>
                        <td>
                            <p>"The training procedure adheres to the English E5 model recipe, involving contrastive pre-training on 1 billion multilingual text pairs, followed by fine-tuning on a combination of labeled datasets."</p>
                            <p><a href="https://arxiv.org/abs/2402.05672" target="_blank" rel="noopener noreferrer">(Wang et al., 2024, abstract)</a></p>
                        </td>
                    </tr>
                </table>
                <ul>
                    <li>English and Spanish texts with the same model</li>
                    <li>Each text starts with the prefix "query: " <a href="https://huggingface.co/intfloat/multilingual-e5-small" target="_blank" rel="noopener noreferrer">(multilingual-e5-small model card)</a></li>
                    <li>Texts longer than 512 tokens are cut, count how many</li>
                    <li>Cost on free Colab CPU: about 470 MB to download, then about a minute for a few hundred abstracts (box estimate)</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Text Encoders

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 30%">
                <p><b>Python</b></p>
                <ul>
                    <li>Load the model once</li>
                    <li>Count the texts that will be cut</li>
                    <li>Encode, then the same logistic regression</li>
                    <li>Save the vectors, so a rerun does not encode again</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 70%">


```python
from sentence_transformers import SentenceTransformer

encoder = SentenceTransformer(TEXT_MODEL)
encoder.max_seq_length = MAX_LENGTH

lengths = [len(encoder.tokenizer(PREFIX + t)["input_ids"]) for t in texts]
print(sum(l > MAX_LENGTH for l in lengths), "texts are cut")

V_train = encoder.encode([PREFIX + t for t in train_texts],
                           normalize_embeddings=True, batch_size=16)
V_test = encoder.encode([PREFIX + t for t in test_texts],
                        normalize_embeddings=True, batch_size=16)

lr_enc = LogisticRegression(class_weight="balanced", C=C_REG,
                            max_iter=1000).fit(V_train, y_train)
pred_encoder = lr_enc.predict(V_test)
```

            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
