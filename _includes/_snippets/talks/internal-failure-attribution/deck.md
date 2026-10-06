<!-- SLIDES: -->

## The paper

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Which Agent Causes Task Failures and When? On Automated Failure Attribution of LLM Multi-Agent Systems</b></p>
                <br>
                <p>Shaokun Zhang et al.</p>
                <br>
                <p>ICML 2025 (PMLR 267)</p>
                <p><a href="https://arxiv.org/abs/2505.00212" target="_blank" rel="noopener noreferrer">arXiv:2505.00212</a></p>
                <p><a href="https://github.com/mingyin1/Agents_Failure_Attribution" target="_blank" rel="noopener noreferrer">Who&When code and dataset</a></p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/failure-attribution/title-abstract.png" alt="Paper title and abstract" style="height: 400px">
            </div>
        </div>
    </div>
</div>

## Failure attribution

<div class="rows" style="height: 100%">
    <div class="row" style="height: 55%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img src="{{ site.url }}/assets/media/images/failure-attribution/fig1-overview.png" alt="Manual vs automated failure attribution of LLM multi-agent systems" style="height: 280px; width: auto">
            </div>
        </div>
    </div>
    <div class="row" style="height: 45%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <ul>
                    <li><b>Failure attribution</b> finds the agent and the step responsible for a task failure for debugging MAS.</li>
                    <li>Manual attribution evaluates, reads long logs, attributes, and refines. It needs labour and expertise.</li>
                    <li>The paper aims to automate it with LLMs.</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Turn-based multi-agent systems

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p>A system of $N$ agents $\mathcal{N}=\lbrace 1,\ldots,N \rbrace$ acting in turns. Exactly one agent acts at each time step.</p>

$$M = \langle \mathcal{N}, S, A, P, \varphi \rangle$$

                <p><b>States and actions:</b> $S$ is the state set and $A$ the global action set, with $A_i \subseteq A$ for agent $i$.</p>
                <p><b>Turns:</b> $\varphi(t)$ is the agent active at time $t$, and $P(s_{t+1} \mid s_t, a_t, \varphi(t))$ is the state transition.</p>
                <p><b>Trajectory:</b> $\tau = \langle s_0, a_0, s_1, a_1, \ldots, s_T \rangle$, where $T$ is the terminal step.</p>
                <p><b>Outcome:</b> $Z(\tau)=1$ if the system ultimately fails, otherwise $Z(\tau)=0$.</p>
            </div>
        </div>
    </div>
</div>

## Decisive errors

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Mistake:</b> a pair $(i,t)$ where agent $i$ acts at time $t$ and $a_t$ is wrong. Not every mistake causes the failure.</p>
                <p><b>Intervention:</b> $I_{(i,t)}$ replaces $a_t$ with a correct $\tilde{a}_t$, keeps earlier steps, and adjusts later ones, giving $\tau^{(i,t)} = I_{(i,t)}(\tau)$.</p>
                <p><b>Decisive error:</b> fixing agent $i$ at time $t$ turns failure into success.</p>

$$\Delta_{(i,t)}(\tau) = 1 \iff Z(\tau)=1 \text{ and } Z(\tau^{(i,t)})=0$$

                <p><b>Earliest decisive error:</b> the failure-responsible agent $i^{\ast}$ and the decisive error step $t^{\ast}$.</p>

$$C(\tau)=\lbrace (i,t) \mid \Delta_{(i,t)}(\tau)=1 \rbrace, \qquad (i^{\ast},t^{\ast})=\arg\min_{(i,t)\in C(\tau)} t$$

                <p><b>Automated failure attribution:</b> recover $(i^{\ast}, t^{\ast})$ from the failure log, without human inspection.</p>
            </div>
        </div>
    </div>
</div>

## The Who&When dataset

<div class="rows" style="height: 100%">
    <div class="row" style="height: 40%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>127 systems and 184 annotated failures</b> on queries from the GAIA and AssistantBench validation sets.</p>
                <ul>
                    <li><b>Algorithm-generated:</b> one team per query, built by CaptainAgent (AG2 library) on GPT-4o. Only the systems that fail are kept.</li>
                    <li><b>Hand-crafted:</b> Magentic-One, a mature generalist system of five specialised agents (e.g., web browsing, local files).</li>
                </ul>
            </div>
        </div>
    </div>
    <div class="row" style="height: 60%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <table class="table">
                    <thead>
                        <tr>
                            <th>Systems</th>
                            <th>Queries</th>
                            <th>Failure logs</th>
                            <th>Agents</th>
                            <th>Log length (steps)</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><b>Algorithm-generated</b></td>
                            <td>GAIA</td>
                            <td>98</td>
                            <td>1 to 4</td>
                            <td>5 to 10</td>
                        </tr>
                        <tr>
                            <td><b>Algorithm-generated</b></td>
                            <td>AssistantBench</td>
                            <td>28</td>
                            <td>3 to 4</td>
                            <td>6 to 10</td>
                        </tr>
                        <tr>
                            <td><b>Hand-crafted</b></td>
                            <td>GAIA</td>
                            <td>30</td>
                            <td>1 to 5</td>
                            <td>5 to 130</td>
                        </tr>
                        <tr>
                            <td><b>Hand-crafted</b></td>
                            <td>AssistantBench</td>
                            <td>28</td>
                            <td>2 to 4</td>
                            <td>8 to 129</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>

## A failure instance

<div class="rows" style="height: 100%">
    <div class="row" style="height: 90%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img src="{{ site.url }}/assets/media/images/failure-attribution/fig9-example.png" alt="Who and When failure instance with annotated failure-responsible agents and decisive error steps" style="height: 530px; width: auto">
            </div>
        </div>
    </div>
    <div class="row" style="height: 10%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <p><b>Each instance:</b> query, failure log, system information, and annotation (agent, step, reason).</p>
            </div>
        </div>
    </div>
</div>

## Annotation is hard

<div class="rows" style="height: 100%">
    <div class="row" style="height: 50%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img src="{{ site.url }}/assets/media/images/failure-attribution/fig2-annotation.png" alt="Annotation labour cost, uncertain annotation percentages, and disagreement rates" style="width: 100%; height: auto">
            </div>
        </div>
    </div>
    <div class="row" style="height: 50%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <ul>
                    <li><b>Three experts, three rounds:</b> independent labels with an uncertainty flag, discussion to consensus on uncertain cases, then cross-validation of each other's labels.</li>
                    <li><b>Cost:</b> 30.9, 30.2, and 23.2 human hours.</li>
                    <li><b>Uncertainty:</b> 15% to 30% of each expert's annotations, and disagreement remained before discussion.</li>
                    <li>Annotators parse long logs, follow each agent's logic, and even revisit websites to judge a single step.</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Three attribution methods

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <table class="table">
                    <thead>
                        <tr>
                            <th>Method</th>
                            <th>What the LLM sees</th>
                            <th>How it decides</th>
                            <th>Input tokens</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><b>All-at-once</b></td>
                            <td>Query and the full failure log</td>
                            <td>Names the agent and the step in one call</td>
                            <td>C + n·T<sub>l</sub></td>
                        </tr>
                        <tr>
                            <td><b>Step-by-step</b></td>
                            <td>Query and the log up to the current step</td>
                            <td>Stops at the first step judged wrong</td>
                            <td>i*·C + T<sub>l</sub>·i*(i*+1)/2</td>
                        </tr>
                        <tr>
                            <td><b>Binary search</b></td>
                            <td>Query and one half of the current log segment</td>
                            <td>Keeps the half with the error until one step remains</td>
                            <td>⌈log<sub>2</sub> n⌉ calls on halving segments</td>
                        </tr>
                    </tbody>
                </table>
                <br>
                <p><b>Settings:</b> with and without the ground-truth answer to the query. GPT-4o as the judge unless stated otherwise.</p>
                <div class="footnote">C: query and instruction tokens. n: log entries. T<sub>l</sub>: average tokens per entry. i*: decisive error step.</div>
            </div>
        </div>
    </div>
</div>

## Who vs when

<div class="rows" style="height: 100%">
    <div class="row" style="height: 10%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Metrics:</b> agent-level accuracy (who), step-level accuracy (when), and step-level accuracy with tolerance.</p>
            </div>
        </div>
    </div>
    <div class="row" style="height: 55%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img src="{{ site.url }}/assets/media/images/failure-attribution/table1-results.png" alt="Table 1: agent-level and step-level accuracy of the three methods with and without ground truth" style="height: 300px; width: auto">
            </div>
        </div>
    </div>
    <div class="row" style="height: 35%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <ul>
                    <li><b>Who:</b> all-at-once is best (53.5% on average). The full log gives the widest view of all agents.</li>
                    <li><b>When:</b> step-by-step is best in 3 of 4 settings (14.2% on average). All-at-once falls below random.</li>
                    <li><b>Same trade-off</b> mostly holds across GPT, Llama, and Qwen models.</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Context length

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 55%">
                <img src="{{ site.url }}/assets/media/images/failure-attribution/fig4-context-length.png" alt="Agent-level and step-level accuracy of the three methods across five log length levels" style="width: 100%; height: auto">
            </div>
            <div class="column vertical-middle text-left" style="width: 45%">
                <p><b>Hand-crafted logs</b> split into five length levels, from 5 to 17 steps (level 1) up to 93 to 130 steps (level 5).</p>
                <br>
                <ul>
                    <li><b>Both metrics drop</b> as logs get longer.</li>
                    <li><b>When is more sensitive:</b> step accuracy falls faster, and all methods reach about 0% on the longest logs.</li>
                    <li><b>More log in the prompt helps who, but long prompts hurt when.</b> LLMs struggle to retrieve one step from a long context.</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Tolerance

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <table class="table">
                    <thead>
                        <tr>
                            <th>Tolerance</th>
                            <th>All-at-once</th>
                            <th>Step-by-step</th>
                            <th>Binary search</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><b>± 1</b></td>
                            <td>12.07</td>
                            <td><b>14.66</b></td>
                            <td>13.79</td>
                        </tr>
                        <tr>
                            <td><b>± 2</b></td>
                            <td><b>19.83</b></td>
                            <td>16.38</td>
                            <td>18.97</td>
                        </tr>
                        <tr>
                            <td><b>± 3</b></td>
                            <td><b>30.17</b></td>
                            <td>18.10</td>
                            <td>22.41</td>
                        </tr>
                        <tr>
                            <td><b>± 4</b></td>
                            <td><b>37.07</b></td>
                            <td>31.90</td>
                            <td>31.89</td>
                        </tr>
                        <tr>
                            <td><b>± 5</b></td>
                            <td><b>43.10</b></td>
                            <td>33.62</td>
                            <td>36.21</td>
                        </tr>
                    </tbody>
                </table>
                <div class="footnote">Step-level accuracy (%) on hand-crafted logs</div>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>In practice, a range of steps is often enough to start debugging.</p>
                <br>
                <ul>
                    <li><b>Exact step:</b> step-by-step leads with no tolerance or ± 1.</li>
                    <li><b>Wider tolerance:</b> all-at-once overtakes and reaches 43.10% at ± 5.</li>
                    <li><b>Hand-crafted logs only:</b> algorithm-generated logs have at most 10 steps, so tolerance would inflate accuracy.</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## A statistical view

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Across all hand-crafted logs</b> (Magentic-One), count how often each agent is blamed.</p>
                <br>
                <ul>
                    <li><b>Agents:</b> 0 Assistant, 1 FileSurfer, 2 Orchestrator, 3 WebSurfer.</li>
                    <li><b>All three methods</b> agree with the ground truth on the agent with the most decisive errors (WebSurfer).</li>
                    <li><b>Top two agents</b> match the ground truth for two of the three methods.</li>
                    <li><b>Takeaway:</b> attribution is more reliable at dataset level than per failure, and that is already useful to refine a system.</li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/failure-attribution/fig6-histogram.png" alt="Histogram of actual and predicted failure-responsible agents for the three methods" style="height: 420px; width: auto">
            </div>
        </div>
    </div>
</div>

## Hybrids and reasoning models

<div class="rows" style="height: 100%">
    <div class="row" style="height: 58%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <table class="table">
                    <thead>
                        <tr>
                            <th>Method</th>
                            <th>Tokens</th>
                            <th>Agent</th>
                            <th>Step</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><b>All-at-once</b></td>
                            <td>17,106</td>
                            <td>57.02</td>
                            <td>4.39</td>
                        </tr>
                        <tr>
                            <td><b>Step-by-step</b></td>
                            <td>87,720</td>
                            <td>35.96</td>
                            <td>7.90</td>
                        </tr>
                        <tr>
                            <td><b>Binary search</b></td>
                            <td>34,659</td>
                            <td>43.97</td>
                            <td>6.90</td>
                        </tr>
                        <tr>
                            <td><b>Hybrid</b></td>
                            <td>149,177</td>
                            <td><b>57.02</b></td>
                            <td><b>12.28</b></td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <table class="table">
                    <thead>
                        <tr>
                            <th>Agent / step</th>
                            <th>All-at-once</th>
                            <th>Step-by-step</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><b>GPT-4o</b></td>
                            <td>54.31 / 4.39</td>
                            <td>33.62 / 7.90</td>
                        </tr>
                        <tr>
                            <td><b>OpenAI o1</b></td>
                            <td>41.38 / 10.34</td>
                            <td>36.21 / 13.79</td>
                        </tr>
                        <tr>
                            <td><b>DeepSeek R1</b></td>
                            <td>56.90 / 3.45</td>
                            <td>32.76 / 6.90</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
    <div class="row" style="height: 42%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <ul>
                    <li><b>Hybrid:</b> all-at-once picks the agent, step-by-step checks only its steps. Best on both metrics, highest token cost.</li>
                    <li><b>Reasoning models</b> (o1, DeepSeek R1) do not consistently beat GPT-4o.</li>
                </ul>
                <div class="footnote">Accuracy (%) on hand-crafted logs.</div>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
