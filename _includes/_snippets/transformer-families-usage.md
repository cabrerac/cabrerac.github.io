<!-- SLIDES: -->

## Transformer Families

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 36%">
                <p><b>Python usage:</b> Hugging Face transformers</p>
                <p>Encoder only: fill a masked token</p>
                <ul>
                    <li><p><b>pipeline:</b> downloads the tokeniser and the model, then runs both</p></li>
                    <li><p><b>[MASK]:</b> the model sees the words on both sides</p></li>
                    <li><p><b>Returns:</b> the 5 most likely words, nest 0.758, hole 0.067, house 0.016, ...</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 64%">

```python
from transformers import pipeline

fill = pipeline("fill-mask", model="google-bert/bert-base-uncased")

for guess in fill("The bird built a [MASK] in the tree."):
    print(guess["token_str"], round(guess["score"], 3))
```
</div>
        </div>
    </div>
</div>

## Transformer Families

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 36%">
                <p><b>Python usage:</b> Hugging Face transformers</p>
                <p>Encoder-decoder: translate a sentence</p>
                <ul>
                    <li><p><b>AutoModelForSeq2SeqLM:</b> an encoder-decoder with its output layer</p></li>
                    <li><p><b>generate:</b> the encoder reads the input, the decoder writes the output token by token</p></li>
                    <li><p><b>Returns:</b> El pájaro dejó el nido al amanecer.</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 64%">

```python
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

name = "Helsinki-NLP/opus-mt-en-es"              # English to Spanish
tokenizer = AutoTokenizer.from_pretrained(name)
model = AutoModelForSeq2SeqLM.from_pretrained(name)

inputs = tokenizer("The bird left the nest at dawn.", return_tensors="pt")
output = model.generate(**inputs, max_length=40)  # output token ids
print(tokenizer.decode(output[0], skip_special_tokens=True))
```
</div>
        </div>
    </div>
</div>

## Transformer Families

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 36%">
                <p><b>Python usage:</b> Hugging Face transformers</p>
                <p>Decoder only: probabilities of the next token</p>
                <ul>
                    <li><p><b>AutoModelForCausalLM:</b> a decoder-only transformer with its output layer</p></li>
                    <li><p><b>logits[0, -1]:</b> one score per vocabulary token at the last position</p></li>
                    <li><p><b>Returns:</b> ' tree' 0.167, ' nest' 0.114, ' house' 0.038, ...</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 64%">

```python
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

name = "Qwen/Qwen2.5-0.5B"
tokenizer = AutoTokenizer.from_pretrained(name)
model = AutoModelForCausalLM.from_pretrained(name, dtype=torch.float32)

inputs = tokenizer("The bird left the", return_tensors="pt")
with torch.no_grad():
    scores = model(**inputs).logits[0, -1]        # last position
probs = torch.softmax(scores, dim=-1)             # P(x | y_1:n)
top = torch.topk(probs, 5)
for p, i in zip(top.values, top.indices):
    print(repr(tokenizer.decode([int(i)])), round(float(p), 3))
```
</div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
