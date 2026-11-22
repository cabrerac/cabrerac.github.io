<!-- SLIDES: -->

## Next-Token Prediction

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 45%">
                <p><b>Task:</b> predict the next token of a text written in natural language</p>
                <p>Given the tokens read so far, which token comes next?</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 55%">
<img src="{{ site.url }}/assets/media/diagrams/transformer-next-token-1.svg" alt="Next-token prediction" style="max-height: 300px; max-width: 100%; width: auto;">
            </div>
        </div>
    </div>
</div>

## Next-Token Prediction

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 45%">
                <p><b>Task:</b> predict the next token of a text written in natural language</p>
$$
P(x \mid y_{1:n}), \qquad x \in V
$$
                <ul>
                    <li><p><b>$y_{1:n}$:</b> the $n$ tokens read so far, the context</p></li>
                    <li><p><b>$x$:</b> a candidate for the next token</p></li>
                    <li><p><b>$V$:</b> the vocabulary, every token the model knows</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 55%">
<img src="{{ site.url }}/assets/media/diagrams/transformer-next-token-2.svg" alt="Next-token prediction with a model" style="max-height: 420px; max-width: 100%; width: auto;">
            </div>
        </div>
    </div>
</div>

## Next-Token Prediction

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Data:</b> text in natural language</p>
                <ul>
                    <li><p><b>Order:</b> the same words in another order mean something else</p></li>
                    <li><p><b>Length:</b> each text has its own length</p></li>
                    <li><p><b>Context:</b> <em>la estación</em> in the second sentence is the station of the first one</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
<div style="font-size: 0.8em; padding: 12px 18px; border-left: 4px solid var(--secondary-color);"><p><em>"el temblor movió la estación cercana. la estación registró el movimiento del suelo. el operador revisó la señal y avisó al centro. el centro comparó la señal con las estaciones vecinas."</em></p></div>
                <p><span style="font-size: 0.8em">A short paragraph about an earthquake and a seismic station.</span></p>
            </div>
        </div>
    </div>
</div>

## Next-Token Prediction

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <p><b>Examples:</b> every position of the text gives one example</p>
                <ul>
                    <li><p><b>Input:</b> the text up to that position</p></li>
                    <li><p><b>Target:</b> the token that follows</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
<img src="{{ site.url }}/assets/media/diagrams/transformer-training-pairs-1.svg" alt="Training pairs from a text" style="max-height: 380px; max-width: 100%; width: auto;">
            </div>
        </div>
    </div>
</div>

## Next-Token Prediction

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <p><b>Examples:</b> every position of the text gives one example</p>
                <ul>
                    <li><p><b>Input:</b> the text up to that position</p></li>
                    <li><p><b>Target:</b> the token that follows</p></li>
                </ul>
                <p><b>Self-supervised learning:</b> the text gives its own targets, so any text can be training data</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
<img src="{{ site.url }}/assets/media/diagrams/transformer-training-pairs-2.svg" alt="Training pairs from a text" style="max-height: 380px; max-width: 100%; width: auto;">
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
