<!-- SLIDES: -->

## The Reasoning Paradox

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>Turing proposed the <b>Imitation Game</b> (now called the <b>Turing Test</b>): a machine wins if the interrogator cannot tell it apart from a human.</p>
                <br>
                <p><em>"It will be assumed that the best strategy [for the machine] is to try to provide answers that would naturally be given by a man." </em><a href="https://doi.org/10.1093/mind/LIX.236.433" target="_blank" rel="noopener noreferrer">(Turing, 1950)</a></p>
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
            <div class="column vertical-middle text-left" style="width: 100%">
                <p>A key feature of human intelligence is <b>consistent reasoning</b>: humans can solve equivalent problems stated in different ways and tend to treat them with the same underlying logic.</p>
                <br>
                <p>Consistent reasoning is at the core of scientific discussions, communication, and reasoning. To pass the Turing Test, a machine must also reason consistently.</p>
                <br>
                <p style="text-align: center;"><b>AGI ⇒ Passing the Turing Test ⇒ Consistent Reasoning</b></p>
                <br>
                <p>For <b>trustworthy</b> dialogue, a system also needs a genuine way to abstain. For example to say <b>"I don't know"</b> when the input does not support an answer <a href="https://arxiv.org/abs/2408.02357" target="_blank" rel="noopener noreferrer">(Bastounis et al., 2024)</a>.</p>
            </div>
        </div>
    </div>
</div>

## The Reasoning Paradox

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Code Roulette</b>: we studied how sensitive LLM <b>code generation</b> is to prompt wording and formatting <a href="https://arxiv.org/abs/2506.10204" target="_blank" rel="noopener noreferrer">(Paleyes, Robinson, Sendyka, Cabrera, Lawrence, 2026)</a>.</p>
                <br>
                <p>We found that LLMs can solve the task even when the prompt is truncated or obfuscated to the point of being unintelligible <a href="https://arxiv.org/abs/2505.23598" target="_blank" rel="noopener noreferrer">(Sendyka et al., 2025)</a>.</p>
                </p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/obfuscated-tasks-llms.png" alt="Obfuscated Tasks LLMs" style="height: 400px">
                <div class="footnote">Obfuscated and unintelligible coding tasks solved by LLMs</div>
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
                <p>Does this pass the Turing Test? A human interrogator would immediately know: no human responds to unintelligible input with confident, plausible-looking code.</p>
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
                <p>Any AI that emulates human intelligence through <b>consistent reasoning</b> and <b>always answers</b> will hallucinate infinitely often.</p>
                <br>
                <p>The paradox: there exists a specialised AI that is always correct on those problems, but it does not reason consistently and therefore <b>cannot pass the Turing Test</b>.</p>
                <br>
                <p>Today's most advanced models do not, in practice, learn a reliable <b>"I don't know"</b> behaviour. That makes them <b>difficult to trust</b> in the strong sense discussed above.</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="https://upload.wikimedia.org/wikipedia/commons/5/55/Turing_test_diagram.png" alt="The Turing Test" style="height: 400px">
                <div class="footnote">The Turing Test (Imitation Game)</div>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
