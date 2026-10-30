<!-- SLIDES: -->

## Keyword Lists

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>A dictionary method</b></p>
                <ul>
                    <li>Write a list of words that point to the answer</li>
                    <li>A text with at least one word from the list is a match</li>
                    <li>No training, every decision can be explained</li>
                    <li>The list is the model</li>
                </ul>
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
                <ul>
                    <li>Write it from the question, before looking at any result</li>
                    <li>Normalise it the same way as the texts, lower case</li>
                    <li>Add the plural and the singular, diet and diets</li>
                    <li>Keep it short and say why each word is there</li>
                </ul>
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
                <ul>
                    <li>A wider list finds more right texts</li>
                    <li>It also catches more wrong ones</li>
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
