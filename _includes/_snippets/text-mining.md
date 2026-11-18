<!-- SLIDES: -->

## The Task

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Short answers from texts</b></p>
                <p>What short answer does each text give to a question?</p>
                <ul>
                    <li>Each record is a text</li>
                    <li>The answer is short: read or skip, on topic or not, mentions a place or not</li>
                    <li>There are too many texts to read by hand</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/topic-detection-document-word-matrix.gif" alt="Blocks of words appear in a document word matrix" style="height: 360px">
                <div class="footnote">Topic detection in a document-word matrix - Christoph Carl Kling, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## The Task

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Marked examples</b></p>
                <p>A person marks a sample of texts with the answer.</p>
                <ul>
                    <li>The marks are written before any method runs</li>
                    <li>Some marked texts train a method, others are kept apart to judge it</li>
                </ul>
                <br>
                <p><b>Text mining</b> turns many texts into the short answers a question needs.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/diagrams/text-marked-sample.svg" alt="Texts with a marked sample" style="height: 380px">
            </div>
        </div>
    </div>
</div>

# The Data

## The Data

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 48%">
                <p><b>Texts and a marked sample</b></p>
                <p>The data is many texts and a sample marked by a person.</p>
                <ul>
                    <li><b>Text:</b> one document, short or long</li>
                    <li><b>Word:</b> a run of letters, the unit we count</li>
                    <li><b>Mark:</b> the answer a person writes for one text</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 52%">
                <p><b>Examples</b></p>
                <table class="table">
                    <thead>
                        <tr><th>Data</th><th>One text</th><th>Mark</th></tr>
                    </thead>
                    <tbody>
                        <tr><td>Emails</td><td>one email</td><td>spam or not</td></tr>
                        <tr><td>Reviews</td><td>one review</td><td>complaint or not</td></tr>
                        <tr><td>Abstracts</td><td>one abstract</td><td>on topic or not</td></tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>

# Modeling

## Methods

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
                <p><b>Dictionaries:</b> keyword lists and weighted lexicons.</p>
                <p><b>Word counts:</b> TF-IDF with logistic regression, and Naive Bayes.</p>
                <p><b>Text encoders:</b> frozen or fine-tuned.</p>
                <p><b>Generative models:</b> a prompted language model.</p>
            </div>
        </div>
    </div>
</div>

## Methods

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>A <b>weighted lexicon</b> adds a score per listed word.</p>
                <p><b>Naive Bayes</b> multiplies word probabilities under yes and no.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>A <b>fine-tuned encoder</b> keeps learning on the marks.</p>
                <p>A <b>prompted language model</b> is asked for the answer in words.</p>
                <p>These names place the three methods we use today.</p>
            </div>
        </div>
    </div>
</div>

## Methods

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <ul>
                    <li><b>Keyword list:</b> words from the question</li>
                    <li><b>TF-IDF with logistic regression:</b> word weights learned from the marks</li>
                    <li><b>Text encoder:</b> a vector learned elsewhere</li>
                </ul>
                <p>These apply to different data sources (e.g., emails, reviews, abstracts, etc).</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/topic-detection-document-word-matrix.gif" alt="Blocks of words appear in a document word matrix" style="height: 360px">
                <div class="footnote">Topic detection in a document-word matrix - Christoph Carl Kling, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
