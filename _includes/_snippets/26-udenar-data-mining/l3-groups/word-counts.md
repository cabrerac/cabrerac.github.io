<!-- SLIDES: -->
<!-- Course piece (round 2, S10 and S11): the papers preparation, moved out of the shared clustering.md. word_list is the L2 word function with repeats kept, as in the L3 notebook. 317 x 869 is the shape with the L2 STOP_WORDS (URL words dropped), checkpoint B review M2. -->

## Groups of Similar Items

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 30%">
                <p><b>Word counts for the papers</b></p>
                <p>The word function of Lecture 2, with repeats kept.</p>
                <p>Texts with at least 5 distinct words, as in Lecture 2.</p>
                <p>Words in at least the floor of papers and at most half of them.</p>
                <p>Each row scaled to length 1.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 70%">


```python
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import normalize

def word_list(text, stop_words):
    """Like words from Lecture 2, but keeps the repeats."""
    text = (text or "").lower().replace("[cita requerida]", " ")
    return [w for w in WORD_RE.findall(text) if len(w) >= 3 and w not in stop_words]

token_lists = [word_list(t, STOP_WORDS) for t in texts]
token_lists = [t for t in token_lists if len(set(t)) >= 5]   # 317 papers
FLOOR = support_floor(len(token_lists))

vectorizer = CountVectorizer(analyzer=lambda tokens: tokens,
                             min_df=FLOOR, max_df=MAX_WORD_SHARE)
counts = vectorizer.fit_transform(token_lists)
X = normalize(counts)   # each row scaled to length 1
print(X.shape)          # (317, 869)
```

            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
