<!-- SLIDES: -->

## Text Preparation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>From a text to a set of words</b></p>
                <ul>
                    <li><b>Lower case</b> - Obesity and obesity are one word</li>
                    <li><b>Tokens</b> - keep runs of letters, drop numbers and signs</li>
                    <li><b>Short words</b> - drop words under three letters</li>
                    <li><b>Stop words</b> - drop the, of, and, which appear everywhere</li>
                    <li><b>Boilerplate</b> - drop words that come from the format</li>
                    <li><b>Set</b> - keep each word once per text</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Text Preparation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 55%">
                <p><b>Boilerplate</b></p>
                <ul>
                    <li>Words that repeat because of how texts are written, not what they say</li>
                    <li>Section labels such as background, methods, findings</li>
                    <li>Funding lines that name the same funder again and again</li>
                    <li>Web addresses: http, https, www, org</li>
                </ul>
                <p>http and www appear together in many texts, beat every baseline, and mean nothing. A baseline will not catch boilerplate. Preparation must.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 45%">
                <p><b>The words we remove</b></p>
                <table class="table">
                    <tbody>
                        <tr><td>Section labels</td><td>background, methods, findings, interpretation, conclusions, results, objective, objectives, aims</td></tr>
                        <tr><td>Funding lines</td><td>funding, bill, melinda, gates, foundation</td></tr>
                        <tr><td>Web addresses</td><td>http, https, www, org</td></tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>

## Text Preparation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 35%">
                <p><b>Python</b></p>
                <ul>
                    <li>One set of words per text</li>
                    <li>spaCy stop words plus the boilerplate list</li>
                    <li>Drop texts with fewer than five words</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 65%">


```python
import re
from spacy.lang.en.stop_words import STOP_WORDS as STOP_WORDS_EN

WORD_RE = re.compile(r"[^\W\d_]+")
ABSTRACT_LABELS = {
    "background", "methods", "findings", "interpretation", "funding",
    "conclusions", "results", "objective", "objectives", "aims",
    "bill", "melinda", "gates", "foundation",
}
URL_TOKENS = {"http", "https", "www", "org"}
STOP_WORDS = set(STOP_WORDS_EN) | ABSTRACT_LABELS | URL_TOKENS

def words(text, stop_words):
    text = (text or "").lower().replace("[cita requerida]", " ")
    return {w for w in WORD_RE.findall(text) if len(w) >= 3 and w not in stop_words}

word_sets = [words(t, STOP_WORDS) for t in texts]
word_sets = [s for s in word_sets if len(s) >= 5]
```

            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
