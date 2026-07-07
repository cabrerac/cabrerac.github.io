<!-- SLIDES: -->

## The paper

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>On the consistent reasoning paradox of intelligence and optimal trust in AI: The power of 'I don't know'</b></p>
                <br>
                <p>A. Bastounis · P. Campodonico · M. van der Schaar · B. Adcock · A. C. Hansen</p>
                <br>
                <p><a href="https://arxiv.org/abs/2408.02357" target="_blank" rel="noopener noreferrer">arXiv:2408.02357</a></p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/crp/title-abstract.png" alt="Paper title and abstract" style="height: 400px">
            </div>
        </div>
    </div>
</div>

## Consistent reasoning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 85%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img src="{{ site.url }}/assets/media/images/crp/consistent-reasoning.png" alt="Consistent reasoning example" style="width: 100%; height: auto; max-height: 380px">
                <div class="footnote">Equivalent sentences, same answer</div>
            </div>
        </div>
    </div>
    <div class="row" style="height: 15%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <p><b>Same problem, different sentences → same correct answer</b>: For an AGI to pass the Turing Test, it must reason consistently on basic arithmetic problems.</p>
            </div>
        </div>
    </div>
</div>

## The paradox

<div class="rows" style="height: 100%">
    <div class="row" style="height: 58%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img src="{{ site.url }}/assets/media/images/crp/overview.png" alt="CRP overview" style="width: 100%; height: auto; max-height: 380px">
                <div class="footnote">CRP overview</div>
            </div>
        </div>
    </div>
    <div class="row" style="height: 42%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <p><b>Consistent Reasoning Paradox (CRP). Human-like intelligence in AI <b>requires</b> consistent reasoning.</b></p>
                <ul>
                    <li>Any AI that <b>always answers</b> and reasons consistently on many equivalent sentences must <b>hallucinate infinitely often</b> on some basic arithmetic collections.</li>
                    <li>A narrow <b>SpecialBot</b> can be correct on the same problems if it accepts only one sentence per problem.</li>
                    <li><b>Paradox:</b> the less AGI-shaped AI can be more reliable.</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## CRP I: The non-hallucinating AI exists

<div class="rows" style="height: 100%">
    <div class="row" style="height: 58%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img src="{{ site.url }}/assets/media/images/crp/crp-i.png" alt="CRP I" style="width: 100%; height: auto; max-height: 380px">
                <div class="footnote">CRP I</div>
            </div>
        </div>
    </div>
    <div class="row" style="height: 42%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <p><b>Claim.</b> For collection (⋆) (chemotherapy dosage linear program, many equivalent wordings):</p>
                <ul>
                    <li>Pick <b>one sentence per problem</b> in a family.</li>
                    <li><b>SpecialBot</b> always answers correctly on that family.</li>
                    <li>It <b>never</b> outputs a wrong answer.</li>
                    <li>It does <b>not</b> reason consistently: other equivalent sentences may get no answer.</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## CRP II: Consistent reasoning yields hallucinations

<div class="rows" style="height: 100%">
    <div class="row" style="height: 58%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img src="{{ site.url }}/assets/media/images/crp/crp-ii.png" alt="CRP II" style="width: 100%; height: auto; max-height: 380px">
                <div class="footnote">CRP II</div>
            </div>
        </div>
    </div>
    <div class="row" style="height: 42%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <p><b>Claim.</b> If SpecialBot <b>always answers</b> and accepts <b>any</b> equivalent sentence:</p>
                <ul>
                    <li>It <b>hallucinates infinitely often</b>.</li>
                    <li>Holds even with unbounded memory and time.</li>
                    <li>Failure sentences can be written down explicitly (length bounded by program size + small constant).</li>
                    <li>Solving the problem is <b>easier</b> than deciding sentence equivalence.</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## CRP III: Detecting hallucinations is hard

<div class="rows" style="height: 100%">
    <div class="row" style="height: 55%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/crp/crp-iii-a.png" alt="CRP III(a)" style="width: 100%; height: auto; max-height: 340px">
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/crp/crp-iii-b.png" alt="CRP III(b)" style="width: 100%; height: auto; max-height: 340px">
            </div>
        </div>
    </div>
    <div class="row" style="height: 45%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <p><b>III(a) deterministic.</b> Checking whether the reasoner hallucinated is <b>strictly harder</b> than solving the original problem. Even with <b>true solutions</b>, you cannot always detect errors (e.g. multi-valued problems: "name a prime").</p>
                <p><b>III(b) randomised.</b> No checker can be "almost sure": probability of correct detection <b>p &gt; ½</b> on all inputs is impossible. The checker is either <b>100% certain</b> or no better than a <b>coin flip</b>. Relevant to sampling chatbots: <b>95% confident</b> is ruled out.</p>
            </div>
        </div>
    </div>
</div>

## CRP IV: Correct answer, no proof

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Claim.</b> On the same collection:</p>
                <br>
                <ul>
                    <li>There is a family (one sentence per problem) where an AI answers correctly.</li>
                    <li>For at least one sentence, <b>no AI</b> can give a <b>logically correct explanation</b> (a proof in ZFC sense).</li>
                    <li>Correct ≠ explainable. Connects to explainable AI limits.</li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/crp/crp-iv.png" alt="CRP IV" style="height: 400px">
                <div class="footnote">CRP IV</div>
            </div>
        </div>
    </div>
</div>

## CRP V: Trustworthy AI with "I don't know"

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Claim.</b> There exists a trustworthy, consistent, explainable AI with time budget <b>M</b> minutes:</p>
                <br>
                <ul>
                    <li>Input: any sentence describing the problem.</li>
                    <li>Output: <b>"I know"</b> + correct answer + correct logical explanation, <b>or</b> <b>"I don't know"</b>.</li>
                    <li>Multi-valued problems → always "I don't know".</li>
                    <li>Single-valued problems → "I know" if M is large enough.</li>
                    <li><b>Giving up</b> (parameter M) is necessary, not optional.</li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/crp/crp-v.png" alt="CRP V" style="height: 400px">
                <div class="footnote">CRP V</div>
            </div>
        </div>
    </div>
</div>

## The power of "I don't know"

<div class="rows" style="height: 100%">
    <div class="row" style="height: 58%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img src="{{ site.url }}/assets/media/images/crp/overview.png" alt="CRP overview" style="width: 100%; height: auto; max-height: 380px">
                <div class="footnote">CRP overview</div>
            </div>
        </div>
    </div>
    <div class="row" style="height: 42%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <p><b>Takeaways for trustworthy AI</b></p>
                <ul>
                    <li>CRP I–IV: always-answer + consistent reasoning ⇒ fallibility (hallucinate, uncheckable, sometimes unexplainable).</li>
                    <li><b>Remedy:</b> implicit <b>"I don't know" function</b> as the strongest form of trust CRP allows.</li>
                    <li>AGI cannot be "almost sure". It knows or it abstains like a coin flip.</li>
                    <li>Modern chatbots lack this abstention mechanism on collections like (⋆).</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## In practice

<div class="rows" style="height: 100%">
    <div class="row" style="height: 58%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img src="{{ site.url }}/assets/media/images/crp/chatgpt.png" alt="ChatGPT and Gemini experiments" style="width: 100%; height: auto; max-height: 380px">
                <div class="footnote">Chatbot experiments</div>
            </div>
        </div>
    </div>
    <div class="row" style="height: 42%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <p><b>ChatGPT-4o and Gemini on (⋆)</b></p>
                <ul>
                    <li><b>CRP I:</b> correct on one phrasing.</li>
                    <li><b>CRP II:</b> hallucinate on another equivalent phrasing.</li>
                    <li><b>CRP III:</b> cannot verify another model's answer, even with oracle access.</li>
                </ul>
                <p>Skip this slide if time is short.</p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
