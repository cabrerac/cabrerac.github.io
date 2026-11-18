<!-- SLIDES: -->

## Keyword Lists

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

## Keyword Lists

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p>A <b>keyword list</b> marks a text as a match when it contains at least one word from a list that a person wrote.</p>
            </div>
        </div>
    </div>
</div>

## Keyword Lists

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>A list sees only the words a person wrote.</p>
                <ul>
                    <li>Write the list from the question, before any result</li>
                    <li>Lower case, with the singular and the plural</li>
                    <li>A text that shares a word with the list is a yes</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/diagrams/keyword-list-match.svg" alt="Three texts against a keyword list" style="height: 380px">
            </div>
        </div>
    </div>
</div>

## Keyword Lists

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>A text is a match when its words and the list share at least one word.</p>
                <br>
                <p>$$\hat{y}(t) = \begin{cases} 1 & \text{if } W(t) \cap L \neq \emptyset \\ 0 & \text{otherwise} \end{cases}$$</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>$t$ is one text and $W(t)$ its set of words. $L$ is the list.</p>
                <p>$\hat{y}(t)$ is the answer, 1 for a match.</p>
                <p><b>What a list misses</b></p>
                <ul>
                    <li><b>Other words:</b> the same answer in other words is a no</li>
                    <li><b>Context:</b> a listed word in another sense is a yes</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Keyword Lists

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <ul>
                    <li><p>$L$ = {free, winner, winners}</p></li>
                    <li>A: "Free entry, one winner", marked yes</li>
                    <li>B: "Meeting moved to noon", marked no</li>
                    <li>C: "Winners announced today", marked yes</li>
                    <li>D: "Free parking for staff", marked no</li>
                </ul>
                <p>A, C and D share a word with the list, so they are a yes. D is a wrong yes.</p>
                <p>Three of four answers are right, an accuracy of 0.75.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/diagrams/keyword-list-match.svg" alt="Three texts against a keyword list" style="height: 380px">
            </div>
        </div>
    </div>
</div>

## Keyword Lists

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 47.5%">

```text
write the list before any result
for each text
    lower case, keep runs of letters
    drop short words and stop words
    match = 1 if a word is in the list
```

            </div>
            <div class="column vertical-middle text-left" style="width: 5%">
            </div>
            <div class="column vertical-middle text-left" style="width: 47.5%">

```python
import re
import numpy as np

WORD_RE = re.compile(r"[^\W\d_]+")   # runs of letters

def words(text, stop_words):
    text = (text or "").lower()
    return {w for w in WORD_RE.findall(text)
            if len(w) >= 3 and w not in stop_words}

word_sets = [words(t, STOP_WORDS) for t in texts]
pred_keywords = np.array([int(bool(s & KEYWORDS))
                          for s in word_sets])
```

            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
