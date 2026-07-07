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
                <img src="{{ site.url }}/assets/media/images/crp/consistent-reasoning.png" alt="Consistent reasoning example" style="width: 100%; height: auto">
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
    <div class="row" style="height: 60%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img src="{{ site.url }}/assets/media/images/crp/overview.png" alt="CRP overview" style="width: 100%; height: auto">
            </div>
        </div>
    </div>
    <div class="row" style="height: 40%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <p>Human-like intelligence in AI <b>requires</b> consistent reasoning.</p>
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
                <img src="{{ site.url }}/assets/media/images/crp/crp-i.png" alt="CRP I" style="width: 100%; height: auto">
            </div>
        </div>
    </div>
    <div class="row" style="height: 42%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <p>For collection (⋆):</p>
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
                <img src="{{ site.url }}/assets/media/images/crp/crp-ii.png" alt="CRP II" style="width: 100%; height: auto">
            </div>
        </div>
    </div>
    <div class="row" style="height: 42%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <p>If SpecialBot <b>always answers</b> and accepts <b>any</b> equivalent sentence:</p>
                <ul>
                    <li>It <b>hallucinates infinitely often</b> because it must answer on all equivalent wordings, but equivalence is harder to decide than the problem itself.</li>
                    <li>Holds even with unbounded memory and time.</li>
                    <li>Failure sentences can be written down explicitly.</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## CRP III: Detecting hallucinations is hard

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>After CRP II:</b> a separate checker might still rescue trust. III says it cannot.</p>
                <p><b>III(a).</b> Why an oracle is not enough: for problems like "name a prime", one correct witness does not tell you whether another answer is valid. So even with true solutions on hand, error detection can be harder than solving the problem.</p>
                <p><b>III(b).</b> Randomness does not help chatbots either: a checker cannot be reliably better than guessing. There is no stable "95% confident" middle ground.</p>
            </div>
            <div class="column vertical-middle text-center">
                <img src="{{ site.url }}/assets/media/images/crp/crp-iii-a.png" alt="CRP III(a)" style="width: 100%; height: auto">
                <img src="{{ site.url }}/assets/media/images/crp/crp-iii-b.png" alt="CRP III(b)" style="width: 100%; height: auto">
            </div>
        </div>
    </div>
</div>

## CRP IV: Correct answer, no proof

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>On the same collection:</p>
                <br>
                <ul>
                    <li>There is a family (one sentence per problem) where an AI answers correctly.</li>
                    <li>For at least one sentence, <b>no AI</b> can give a <b>logically correct explanation</b> (a proof in ZFC sense).</li>
                    <li>Correct does not mean explainable. A limit for explainable AI.</li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/crp/crp-iv.png" alt="CRP IV" style="height: 400px">
            </div>
        </div>
    </div>
</div>

## CRP V: Trustworthy AI with "I don't know"

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>There exists a trustworthy, consistent, explainable AI with time budget <b>M</b> minutes:</p>
                <br>
                <ul>
                    <li>Input: any sentence describing the problem.</li>
                    <li>Output: <b>"I know"</b> + correct answer + correct logical explanation, <b>or</b> <b>"I don't know"</b>.</li>
                    <li>Multi-valued problems: always "I don't know".</li>
                    <li>Single-valued problems: "I know" if M is large enough.</li>
                    <li><b>Giving up</b> (parameter M) is necessary, not optional.</li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/crp/crp-v.png" alt="CRP V" style="height: 400px">
            </div>
        </div>
    </div>
</div>

## The power of "I don't know"

<div class="rows" style="height: 100%">
    <div class="row" style="height: 60%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img src="{{ site.url }}/assets/media/images/crp/overview.png" alt="CRP overview" style="width: 100%; height: auto">
            </div>
        </div>
    </div>
    <div class="row" style="height: 40%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <p><b>Takeaways for trustworthy AI</b></p>
                <ul>
                    <li>CRP I–IV: always-answer and consistent reasoning implies fallibility (hallucinate, uncheckable, and sometimes unexplainable).</li>
                    <li><b>Remedy:</b> implicit <b>"I don't know" function</b> as the strongest form of trust CRP allows.</li>
                    <li>Modern chatbots lack this abstention mechanism on collections like (⋆).</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## In practice

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img src="{{ site.url }}/assets/media/images/crp/chatgpt.png" alt="ChatGPT and Gemini experiments" style="width: 100%; height: auto;">
                <div class="footnote">Chatbot experiments</div>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
