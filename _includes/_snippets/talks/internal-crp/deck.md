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
                <img src="{{ site.url }}/assets/media/images/crp/fig0-title-abstract.png" alt="Paper title and abstract" style="height: 400px">
                <div class="footnote">Title and abstract (screenshot from paper)</div>
            </div>
        </div>
    </div>
</div>

## Consistent reasoning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Same problem, different sentences → same correct answer.</b></p>
                <br>
                <ul>
                    <li>(i) Lisa 179 cm, John 178 cm. Who is tallest?</li>
                    <li>(ii) John 178 cm, Lisa 179 cm. Who is tallest?</li>
                    <li>Both describe 178 &lt; 179 → <b>Lisa</b>.</li>
                </ul>
                <br>
                <p><b>Chain for AGI:</b> AGI ⇒ pass Turing Test ⇒ reason consistently on basic arithmetic.</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/crp/fig3-consistent-reasoning.png" alt="Consistent reasoning example" style="height: 400px">
                <div class="footnote">Figure 3: equivalent sentences, same answer</div>
            </div>
        </div>
    </div>
</div>

## The paradox (informal)

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Consistent Reasoning Paradox (CRP)</b></p>
                <br>
                <ul>
                    <li>Human-like intelligence in AI <b>requires</b> consistent reasoning.</li>
                    <li>Any AI that <b>always answers</b> and reasons consistently on many equivalent sentences must <b>hallucinate infinitely often</b> on some basic arithmetic collections.</li>
                    <li>A narrow <b>SpecialBot</b> can be correct on the same problems if it accepts only one sentence per problem.</li>
                    <li><b>Paradox:</b> the less AGI-shaped AI can be more reliable.</li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/crp/fig1-overview.png" alt="CRP overview" style="height: 400px">
                <div class="footnote">Figure 1: CRP overview</div>
            </div>
        </div>
    </div>
</div>

## CRP I — The non-hallucinating AI exists

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Claim.</b> For collection (⋆) (chemotherapy dosage linear program, many equivalent wordings):</p>
                <br>
                <ul>
                    <li>Pick <b>one sentence per problem</b> in a family.</li>
                    <li><b>SpecialBot</b> always answers correctly on that family.</li>
                    <li>It <b>never</b> outputs a wrong answer.</li>
                    <li>It does <b>not</b> reason consistently: other equivalent sentences may get no answer.</li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/crp/fig2-crp-i.png" alt="CRP I" style="height: 400px">
                <div class="footnote">Figure 2 (top): CRP I</div>
            </div>
        </div>
    </div>
</div>

## CRP II — Consistent reasoning yields hallucinations

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Claim.</b> If SpecialBot <b>always answers</b> and accepts <b>any</b> equivalent sentence:</p>
                <br>
                <ul>
                    <li>It <b>hallucinates infinitely often</b>.</li>
                    <li>Holds even with unbounded memory and time.</li>
                    <li>Failure sentences can be written down explicitly (length bounded by program size + small constant).</li>
                    <li>Solving the problem is <b>easier</b> than deciding sentence equivalence.</li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/crp/fig2-crp-ii.png" alt="CRP II" style="height: 400px">
                <div class="footnote">Figure 2 (bottom): CRP II</div>
            </div>
        </div>
    </div>
</div>

## CRP III(a) — Detecting hallucinations is hard

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Claim (deterministic).</b> For the consistent reasoner from CRP II:</p>
                <br>
                <ul>
                    <li>Checking whether it hallucinated is <b>strictly harder</b> than solving the original problem.</li>
                    <li>Even with access to <b>true solutions</b>, you cannot always detect errors.</li>
                    <li><b>Why?</b> Multi-valued problems (e.g. "name a prime"): one witness does not certify all valid answers.</li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/crp/fig1-crp-iii.png" alt="CRP III" style="height: 400px">
                <div class="footnote">Figure 1: CRP III</div>
            </div>
        </div>
    </div>
</div>

## CRP III(b) — Randomness does not help

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Claim (randomised).</b> No checker can be "almost sure":</p>
                <br>
                <ul>
                    <li>Probability of correct detection <b>p &gt; ½</b> on all inputs is impossible.</li>
                    <li>Checker is either <b>100% certain</b> or no better than a <b>coin flip</b>.</li>
                    <li>Relevant to chatbots that use sampling: <b>95% confident</b> is ruled out in this setting.</li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/crp/fig1-crp-iii.png" alt="CRP III" style="height: 400px">
                <div class="footnote">Figure 1: CRP III (same crop as III(a) is fine)</div>
            </div>
        </div>
    </div>
</div>

## CRP IV — Correct answer, no proof

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
                <img src="{{ site.url }}/assets/media/images/crp/fig1-crp-iv.png" alt="CRP IV" style="height: 400px">
                <div class="footnote">Figure 1: CRP IV</div>
            </div>
        </div>
    </div>
</div>

## CRP V — Trustworthy AI with "I don't know"

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
                <img src="{{ site.url }}/assets/media/images/crp/fig1-crp-v.png" alt="CRP V" style="height: 400px">
                <div class="footnote">Figure 1: CRP V</div>
            </div>
        </div>
    </div>
</div>

## The power of "I don't know"

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Takeaways for trustworthy AI</b></p>
                <br>
                <ul>
                    <li>CRP I–IV: always-answer + consistent reasoning ⇒ fallibility (hallucinate, uncheckable, sometimes unexplainable).</li>
                    <li><b>Remedy:</b> implicit <b>"I don't know" function</b> — strongest form of trust CRP allows.</li>
                    <li>AGI cannot be "almost sure"; it knows or it abstains like a coin flip.</li>
                    <li>Modern chatbots lack this abstention mechanism on collections like (⋆).</li>
                </ul>
                <br>
                <p><b>Discussion:</b> Where in our systems would an explicit abstention layer live?</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/crp/fig1-overview.png" alt="CRP overview" style="height: 400px">
                <div class="footnote">Figure 1: CRP overview</div>
            </div>
        </div>
    </div>
</div>

## In practice (optional)

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Figure 4 — ChatGPT-4o and Gemini on (⋆)</b></p>
                <br>
                <ul>
                    <li><b>CRP I:</b> correct on one phrasing.</li>
                    <li><b>CRP II:</b> hallucinate on another equivalent phrasing.</li>
                    <li><b>CRP III:</b> cannot verify another model's answer, even with oracle access.</li>
                </ul>
                <br>
                <p>Skip this slide if time is short.</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/crp/fig4-chatgpt.png" alt="ChatGPT and Gemini experiments" style="height: 400px">
                <div class="footnote">Figure 4: chatbot experiments</div>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
