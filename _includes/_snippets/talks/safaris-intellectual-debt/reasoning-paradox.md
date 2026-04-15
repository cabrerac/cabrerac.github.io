<!-- SLIDES: -->

## The Reasoning Paradox

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p>We now return to <b>Turing's imitation game</b> and to the chain we set up at the start: what kind of behaviour counts as human-like in dialogue, and what does that demand of a machine?</p>
            </div>
        </div>
    </div>
</div>

## The Reasoning Paradox

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>A key feature of human intelligence is <b>consistent reasoning</b>: humans can solve equivalent problems stated in different ways and give the same correct answer.</p>
                <br>
                <p>Consistent reasoning underpins scientific discussion and communication. To pass the Turing Test, a machine must also reason consistently.</p>
                <br>
                <p><b>AGI ⇒ Passing the Turing Test ⇒ Consistent Reasoning</b></p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="https://upload.wikimedia.org/wikipedia/commons/5/55/Turing_test_diagram.png" alt="The Turing Test" style="height: 400px">
                <div class="footnote">The Turing Test (Imitation Game)</div>
            </div>
        </div>
    </div>
</div>

## The Reasoning Paradox

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Code Roulette</b>: LLMs generate code even when the prompt is truncated or obfuscated to the point of being unintelligible <a href="https://arxiv.org/abs/2506.10204" target="_blank" rel="noopener noreferrer">(Paleyes, Robinson, Sendyka, Cabrera, Lawrence, 2026)</a>.</p>
                <br>
                <p>Presented at <a href="https://llm4code.github.io/" target="_blank" rel="noopener noreferrer">LLM4Code @ ICSE 2026</a>, Rio de Janeiro, Brazil.</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/PLACEHOLDER-code-roulette.png" alt="Code Roulette results" style="height: 400px">
            </div>
        </div>
    </div>
</div>

## The Reasoning Paradox

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Is it smart or is it silly?</b></p>
                <br>
                <p>What would a human do when presented with an unintelligible prompt?</p>
                <br>
                <p>A human would say: <b>"I don't understand the question."</b></p>
                <br>
                <p>The LLM always produces an answer, even when the input is meaningless. <b>It cannot say "I don't know"</b>.</p>
                <br>
                <p>Does this pass the Turing Test? <b>No.</b> A human interrogator would immediately know: no human responds to unintelligible input with confident, plausible-looking code.</p>
            </div>
        </div>
    </div>
</div>

## The Reasoning Paradox

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>The <b>Consistent Reasoning Paradox (CRP)</b> <a href="https://arxiv.org/abs/2408.02357" target="_blank" rel="noopener noreferrer">(Bastounis et al., 2024)</a>:</p>
                <br>
                <p>Any AI that emulates human intelligence through <b>consistent reasoning</b> and <b>always answers</b> will hallucinate infinitely often and is not trustworthy.</p>
                <br>
                <p>The paradox: there exists a specialised AI that is always correct on those problems, but it does not reason consistently and therefore <b>cannot pass the Turing Test</b>.</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/PLACEHOLDER-crp-diagram.png" alt="The Consistent Reasoning Paradox" style="height: 400px">
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
