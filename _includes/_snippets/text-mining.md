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
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Marked examples</b></p>
                <p>A person marks a sample of texts with the answer.</p>
                <ul>
                    <li>The marks are written before any method runs, so no result can bend them</li>
                    <li>Some marked texts train a method, others are kept apart to judge it</li>
                    <li>A method is judged by how many marked texts it gets right and how many it gets wrong</li>
                </ul>
                <br>
                <p><b>Text mining</b> turns many texts, too many to read by hand, into the short answers a question needs.</p>
            </div>
        </div>
    </div>
</div>

# The Data

## The Data

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 55%">
                <p><b>A set of texts and marks</b></p>
                <p>The data is many texts and a sample marked by a person.</p>
                <ul>
                    <li><b>Text:</b> one document, short or long</li>
                    <li><b>Word:</b> a run of letters, the unit we count</li>
                    <li><b>Mark:</b> the answer a person writes for one text</li>
                </ul>
                <p>Only the marked texts can train or judge a method. The rest get an answer from the method.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 45%">
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
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Dictionaries:</b> a list of words that a person writes, with no training.</p>
                <p><b>Word counts:</b> weighted word columns and a model learned from the marks.</p>
                <p><b>Text encoders:</b> a pretrained model turns each text into one vector.</p>
                <p><b>Generative models:</b> a language model is asked for the answer in words.</p>
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
                    <li><b>Keyword list:</b> words written from the question</li>
                    <li><b>TF-IDF with logistic regression:</b> word weights learned from the marks</li>
                    <li><b>Text encoder:</b> a vector learned outside this collection, then logistic regression</li>
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
