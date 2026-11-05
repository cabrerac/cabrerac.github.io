<!-- SLIDES: -->

## Text Mining

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 60%">
                <p><b>A short history, counting words</b></p>
                <ul>
                    <li><b>1958, Luhn:</b> frequent words pick the sentences of an automatic abstract <a href="https://doi.org/10.1147/rd.22.0159" target="_blank" rel="noopener noreferrer">(Luhn, 1958)</a></li>
                    <li><b>1972, Sparck Jones:</b> a word in few documents tells more, the idea behind IDF <a href="https://doi.org/10.1108/eb026526" target="_blank" rel="noopener noreferrer">(Sparck Jones, 1972)</a></li>
                    <li><b>1975, Salton:</b> documents as vectors of weighted words <a href="https://doi.org/10.1145/361219.361220" target="_blank" rel="noopener noreferrer">(Salton et al., 1975)</a></li>
                    <li><b>1988, Salton and Buckley:</b> a comparison of word weightings <a href="https://doi.org/10.1016/0306-4573(88)90021-0" target="_blank" rel="noopener noreferrer">(Salton &amp; Buckley, 1988)</a></li>
                    <li><b>1998, Joachims:</b> learning text categories from many word columns <a href="https://doi.org/10.1007/BFb0026683" target="_blank" rel="noopener noreferrer">(Joachims, 1998)</a></li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 40%">
                <img src="{{ site.url }}/assets/media/images/topic-detection-document-word-matrix.gif" alt="Document by word matrix" style="height: 340px">
                <div class="footnote">Topic detection in a document-word matrix - Christoph Carl Kling, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Text Mining

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 60%">
                <p><b>A short history, learned representations</b></p>
                <ul>
                    <li><b>2013, word2vec:</b> a vector per word, learned from context <a href="https://arxiv.org/abs/1301.3781" target="_blank" rel="noopener noreferrer">(Mikolov et al., 2013)</a></li>
                    <li><b>2017, Transformer:</b> attention in place of recurrence <a href="https://arxiv.org/abs/1706.03762" target="_blank" rel="noopener noreferrer">(Vaswani et al., 2017)</a></li>
                    <li><b>2019, BERT:</b> an encoder that reads left and right context <a href="https://doi.org/10.18653/v1/N19-1423" target="_blank" rel="noopener noreferrer">(Devlin et al., 2019)</a></li>
                    <li><b>2019, Sentence-BERT:</b> one vector per sentence, for comparison <a href="https://doi.org/10.18653/v1/D19-1410" target="_blank" rel="noopener noreferrer">(Reimers &amp; Gurevych, 2019)</a></li>
                    <li><b>2024, multilingual E5:</b> one text encoder for many languages <a href="https://arxiv.org/abs/2402.05672" target="_blank" rel="noopener noreferrer">(Wang et al., 2024)</a></li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 40%">
                <img src="{{ site.url }}/assets/media/images/transformer-full-architecture.png" alt="Transformer architecture" style="height: 400px">
                <div class="footnote">Transformer, full architecture - dvgodoy, CC BY 4.0 <https://creativecommons.org/licenses/by/4.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Text Mining

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Extraction from text</b></p>
                <p>Turn each text into a short answer the question needs.</p>
                <ul>
                    <li>Read or skip, on topic or not, mentions a place or not.</li>
                    <li>Many texts, too many to read by hand.</li>
                    <li>A method reads them all, a person checks a sample.</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Text Mining

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Marked examples</b></p>
                <ul>
                    <li>A person marks a sample of texts with the answer</li>
                    <li>The marks are written before any method is run</li>
                    <li>Then no result can bend the marks</li>
                    <li>Some marked texts train a method, others are kept apart to judge it</li>
                    <li>A method is judged by how many marked texts it gets right and how many it gets wrong</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Text Mining

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p><b>Text mining</b> turns many texts, too many to read by hand, into the short answers a question needs.</p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
