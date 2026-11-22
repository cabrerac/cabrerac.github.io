<!-- SLIDES: -->

## Transformer Families

<div class="rows" style="height: 100%">
    <div class="row" style="height: 56%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
<img src="{{ site.url }}/assets/media/diagrams/transformer-families-1.svg" alt="Transformer families" style="max-height: 300px; max-width: 100%; width: auto;">
            </div>
        </div>
    </div>
    <div class="row" style="height: 44%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <ul>
                    <li><p><b>Encoder only:</b> sees every token, pretrained by filling masked tokens, BERT (<a href="https://arxiv.org/abs/1810.04805">Devlin et al., 2018</a>)</p></li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Transformer Families

<div class="rows" style="height: 100%">
    <div class="row" style="height: 56%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
<img src="{{ site.url }}/assets/media/diagrams/transformer-families-2.svg" alt="Transformer families" style="max-height: 300px; max-width: 100%; width: auto;">
            </div>
        </div>
    </div>
    <div class="row" style="height: 44%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <ul>
                    <li><p><b>Encoder only:</b> sees every token, pretrained by filling masked tokens, BERT (<a href="https://arxiv.org/abs/1810.04805">Devlin et al., 2018</a>)</p></li>
                    <li><p><b>Decoder only:</b> sees earlier tokens with the causal mask, pretrained on next-token prediction, GPT (<a href="https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf">Radford et al., 2018</a>)</p></li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Transformer Families

<div class="rows" style="height: 100%">
    <div class="row" style="height: 56%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
<img src="{{ site.url }}/assets/media/diagrams/transformer-families-3.svg" alt="Transformer families" style="max-height: 300px; max-width: 100%; width: auto;">
            </div>
        </div>
    </div>
    <div class="row" style="height: 44%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <ul>
                    <li><p><b>Encoder only:</b> sees every token, pretrained by filling masked tokens, BERT (<a href="https://arxiv.org/abs/1810.04805">Devlin et al., 2018</a>)</p></li>
                    <li><p><b>Decoder only:</b> sees earlier tokens with the causal mask, pretrained on next-token prediction, GPT (<a href="https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf">Radford et al., 2018</a>)</p></li>
                    <li><p><b>Encoder-decoder:</b> an encoder reads the input and a decoder writes the output, T5 (<a href="https://jmlr.org/papers/v21/20-074.html">Raffel et al., 2020</a>)</p></li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Transformer Families

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Pretraining, then adaptation:</b></p>
                <ul>
                    <li><p><b>Pretraining:</b> one of these tasks on a large text collection gives a general model</p></li>
                    <li><p><b>Adaptation:</b> the pretrained model is tailored to a use with instructions, examples, documents, or more training</p></li>
                </ul>
                <p>Large Language Models are decoder-only transformers pretrained at a very large scale. How to use and tailor them is the next step.</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
<img src="{{ site.url }}/assets/media/diagrams/transformer-families-3.svg" alt="Transformer families" style="max-height: 300px; max-width: 100%; width: auto;">
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
