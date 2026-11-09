<!-- SLIDES: -->

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
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Preparation: from a text to a set of words</b></p>
                <ul>
                    <li><b>Lower case:</b> Free and free are one word</li>
                    <li><b>Tokens:</b> keep runs of letters, drop numbers and signs</li>
                    <li><b>Short words:</b> drop words under three letters</li>
                    <li><b>Stop words:</b> drop the, of, and, which appear everywhere</li>
                    <li><b>Boilerplate:</b> drop words that come from the format, such as section labels and web addresses</li>
                    <li><b>Set:</b> keep each word once per text</li>
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
                <p>A text is a match when its words and the list share at least one word.</p>
                <br>
                <p>$$\hat{y}(t) = \begin{cases} 1 & \text{if } W(t) \cap L \neq \emptyset \\ 0 & \text{otherwise} \end{cases}$$</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>$t$ is one text. $W(t)$ is its set of words after preparation. $L$ is the list. $W(t) \cap L$ keeps the words in both, and $\emptyset$ is the empty set. $\hat{y}(t)$ is the answer of the method, 1 for a match.</p>
                <br>
                <p>No training, and every decision can be explained by the word that matched. The list is the model.</p>
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
                    <li><p>$L$ = {free, winner}</p></li>
                    <li>A: "Free entry, one winner"</li>
                    <li>B: "Meeting moved to noon"</li>
                    <li>C: "Winners announced today"</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>A shares free and winner with the list, so A is a match. B shares nothing, so it is not.</p>
                <br>
                <p>C is missed. Its word is winners, not winner. Adding the plural to the list, before looking at any result, fixes it.</p>
            </div>
        </div>
    </div>
</div>

## Keyword Lists

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Building the list, before the results</b></p>
                <ul>
                    <li>Write it from the question</li>
                    <li>Normalise it like the texts, lower case</li>
                    <li>Add the plural and the singular</li>
                    <li>Keep it short and say why each word is there</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Limits</b></p>
                <ul>
                    <li>A wider list finds more right texts, and catches more wrong ones</li>
                    <li>A narrow list misses texts that use other words</li>
                    <li>Changing the list after seeing the marks is fitting the list to the test</li>
                </ul>
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
write the list from the question, before any result
for each text
    lower case, keep runs of letters
    drop short words and stop words
    keep each word once
    match = 1 if any word is in the list, else 0
```

            </div>
            <div class="column vertical-middle text-left" style="width: 5%">
            </div>
            <div class="column vertical-middle text-left" style="width: 47.5%">

```python
import re

def word_set(text, stop_words):
    words = re.findall(r"[a-záéíóúñü]+", text.lower())
    return {w for w in words
            if len(w) >= 3 and w not in stop_words}

def keyword_match(texts, keywords, stop_words):
    return [int(bool(word_set(t, stop_words) & keywords))
            for t in texts]

keywords = {"free", "winner", "winners"}
predictions = keyword_match(texts, keywords, stop_words)
```

            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
