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
            <div class="column vertical-top text-left" style="width: 100%">
                <p><b>A dictionary method</b></p>
                <p>Write a list of words that point to the answer.</p>
                <p>A text with at least one word from the list is a match.</p>
                <p>No training, every decision can be explained.</p>
                <p>The list is the model.</p>
                <p>$$\hat{y}(t) = \begin{cases} 1 & \text{if } W(t) \cap L \neq \emptyset \\ 0 & \text{otherwise} \end{cases}$$</p>
                <p>$W(t)$ is the set of words of text $t$ and $L$ is the list.</p>
            </div>
        </div>
    </div>
</div>

## Keyword Lists

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Building the list</b></p>
                <p>Write it from the question, before looking at any result.</p>
                <p>Normalise it the same way as the texts, lower case.</p>
                <p>Add the plural and the singular, diet and diets.</p>
                <p>Keep it short and say why each word is there.</p>
            </div>
        </div>
    </div>
</div>

## Keyword Lists

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Wider or narrower</b></p>
                <p>A wider list finds more right texts.</p>
                <p>It also catches more wrong ones.</p>
                <p>A narrow list misses texts that use other words.</p>
                <p>Changing the list after seeing the marks is fitting the list to the test.</p>
            </div>
        </div>
    </div>
</div>

## Keyword Lists

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 35%">
                <p><b>Python</b></p>
                <ul>
                    <li>The list written from the question</li>
                    <li>The same word function as before</li>
                    <li>Match or no match</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 65%">


```python
KEYWORDS = {"obesity", "obese", "diet", "diets", "dietary",
            "diabetes", "diabetic", "hypertension", "cholesterol"}

def keyword_match(text):
    """1 if the text has any word of the list, 0 if not."""
    return int(bool(words(text, STOP_WORDS) & KEYWORDS))

pred_keywords = [keyword_match(t) for t in test_texts]   # the marked texts kept apart
```

            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
