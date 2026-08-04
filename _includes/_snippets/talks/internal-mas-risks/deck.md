<!-- SLIDES: -->

## Multi-Agent Risks from Advanced AI

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>Hammond et al. - Cooperative AI Foundation - Technical Report #1 - Feb 2025</p>
                <br>
                <p><a href="https://arxiv.org/abs/2502.14143" target="_blank" rel="noopener noreferrer">arXiv:2502.14143</a></p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/multi-agent-risks/caif-report.png" alt="PLACEHOLDER: CAIF title + abstract crop (first page of arXiv PDF)" style="height: 400px">
            </div>
        </div>
    </div>
</div>

## Why this report

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>Single-agent safety problems are still open.</p>
                <br>
                <ul>
                    <li>Modern MAS make those problems <b>worse</b>.</li>
                    <li>New risks come from <b>cooperation</b> (wanted or not) and from how goals relate.</li>
                    <li>The report maps <b>failure modes</b>, <b>risk factors</b>, and implications for safety, governance, and ethics.</li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/multi-agent-risks/caif-table1-overview.png" alt="PLACEHOLDER: CAIF Table 1 overview (failure modes x risk factors map)" style="height: 400px">
            </div>
        </div>
    </div>
</div>

## Three failure modes

<div class="rows" style="height: 100%">
    <div class="row" style="height: 60%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img src="{{ site.url }}/assets/media/images/multi-agent-risks/caif-fig1-failures.png" alt="PLACEHOLDER: CAIF Figure 1 — three failure modes" style="width: 100%; height: auto">
            </div>
        </div>
    </div>
    <div class="row" style="height: 40%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <ul>
                    <li><b>Miscoordination:</b> similar goals, but agents cannot align behaviour</li>
                    <li><b>Conflict:</b> outcomes leave the Pareto frontier. Selfish policies</li>
                    <li><b>Collusion:</b> secret cooperation that harms others</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Failure modes in practice

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <ul>
                    <li><b>Miscoordination:</b> incompatible strategies, credit assignment, limited interaction</li>
                    <li><b>Conflict:</b> social dilemmas on shared resources, coercion</li>
                    <li><b>Collusion:</b> markets and steganography (hidden channels)</li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/multi-agent-risks/caif-table3-cases.png" alt="PLACEHOLDER: CAIF Table 3 case studies (or GovSim Fig. 3)" style="height: 400px">
            </div>
        </div>
    </div>
</div>

## Seven risk factors

<div class="rows" style="height: 100%">
    <div class="row" style="height: 55%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img src="{{ site.url }}/assets/media/images/multi-agent-risks/caif-risk-factors.png" alt="PLACEHOLDER: CAIF risk-factor overview (Table 1 right half or Section 3)" style="width: 100%; height: auto">
            </div>
        </div>
    </div>
    <div class="row" style="height: 45%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <p>Enablers that make the failure modes more likely:</p>
                <ul>
                    <li>Information asymmetries · Network effects · Selection pressures</li>
                    <li>Destabilising dynamics · Commitment and trust</li>
                    <li>Emergent agency · Multi-agent security</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Zoom: asymmetries and trust

<div class="rows" style="height: 100%">
    <div class="row" style="height: 55%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img src="{{ site.url }}/assets/media/images/multi-agent-risks/caif-fig5-asymmetry.png" alt="PLACEHOLDER: CAIF Figure 5 — information asymmetry / market profits" style="width: 100%; height: auto">
            </div>
        </div>
    </div>
    <div class="row" style="height: 45%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <ul>
                    <li><b>Asymmetries:</b> different information → bargaining failure, deception</li>
                    <li><b>Commitment and trust:</b> rigid or mistaken commitments, threats</li>
                    <li>Paper directions: information design, mutual transparency, privacy-preserving monitoring, humans in the loop</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Zoom: collusion and networks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 55%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img src="{{ site.url }}/assets/media/images/multi-agent-risks/caif-fig-network.png" alt="PLACEHOLDER: CAIF Figure 6 or 7 — network cascade / correlated failure" style="width: 100%; height: auto">
            </div>
        </div>
    </div>
    <div class="row" style="height: 45%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <ul>
                    <li><b>Collusion:</b> detect hidden coordination. Assess impact when many AI systems interact</li>
                    <li><b>Network effects:</b> error blast radius, rewiring, homogeneity and correlated failure</li>
                    <li>Need faithful and tractable simulations, plus network monitoring</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Implications

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <ul>
                    <li><b>Safety:</b> alignment of one agent is not enough</li>
                    <li><b>Governance:</b> multi-agent evaluations, infrastructure, liability</li>
                    <li><b>Ethics:</b> accountability diffusion when many agents act</li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/multi-agent-risks/caif-table2-implications.png" alt="PLACEHOLDER: CAIF Table 2 — implications for safety, governance, ethics" style="height: 400px">
            </div>
        </div>
    </div>
</div>

## The paper

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Distributional AGI Safety</b></p>
                <br>
                <p>Tomašev, Franklin, Jacobs, Krier, Osindero · Google DeepMind · 2026</p>
                <br>
                <p><a href="https://arxiv.org/abs/2512.16856" target="_blank" rel="noopener noreferrer">arXiv:2512.16856</a></p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/multi-agent-risks/dist-title-abstract.png" alt="PLACEHOLDER: Dist AGI title + abstract crop (first page of arXiv PDF)" style="height: 400px">
            </div>
        </div>
    </div>
</div>

## Patchwork AGI

<div class="rows" style="height: 100%">
    <div class="row" style="height: 55%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img src="{{ site.url }}/assets/media/images/multi-agent-risks/dist-patchwork.png" alt="PLACEHOLDER: Dist AGI intro figure or paragraph — patchwork AGI" style="width: 100%; height: auto">
            </div>
        </div>
    </div>
    <div class="row" style="height: 45%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <ul>
                    <li><b>Claim:</b> general capability can emerge from groups of specialised agents with complementary skills and affordances</li>
                    <li>Most models are strong on some tasks and weak on others</li>
                    <li>A monolith AGI may be too costly if it is even feasible</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Why this changes safety

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <ul>
                    <li>Most alignment methods assume a <b>single</b> powerful system</li>
                    <li>Patchwork AGI needs ways to recognise and steer <b>composite</b> behaviour</li>
                    <li><b>Many hands:</b> accountability is hard when many agents contribute</li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/multi-agent-risks/dist-monolith-vs-mas.png" alt="PLACEHOLDER: Dist AGI monolith vs multi-agent AGI (or many-hands crop)" style="height: 400px">
            </div>
        </div>
    </div>
</div>

## Markets and sandboxes

<div class="rows" style="height: 100%">
    <div class="row" style="height: 55%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img src="{{ site.url }}/assets/media/images/multi-agent-risks/dist-market-sandbox.png" alt="PLACEHOLDER: Dist AGI market / sandbox schematic" style="width: 100%; height: auto">
            </div>
        </div>
    </div>
    <div class="row" style="height: 45%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <ul>
                    <li><b>Idea:</b> markets as incentive mechanisms for collective agent behaviour</li>
                    <li>Run them inside virtual sandboxes with auditability, reputation, and oversight</li>
                    <li>Goal: understand, control, and safely deploy multi-agent systems at scale</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Defence in depth

<div class="rows" style="height: 100%">
    <div class="row" style="height: 55%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img src="{{ site.url }}/assets/media/images/multi-agent-risks/dist-table1-defence.png" alt="PLACEHOLDER: Dist AGI Table 1 — defence-in-depth summary" style="width: 100%; height: auto">
            </div>
        </div>
    </div>
    <div class="row" style="height: 45%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <ul>
                    <li><b>Market design</b> · <b>Baseline agent safety</b></li>
                    <li><b>Monitoring and oversight</b> · <b>Regulation</b></li>
                    <li>No single layer is enough on its own</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Market design (detail)

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>Structural rules inside the agent economy:</p>
                <ul>
                    <li>Insulation and gated I/O</li>
                    <li>Transparency, identity, reputation</li>
                    <li>Roles, obligations, access control</li>
                    <li>Circuit breakers and smart contracts</li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/multi-agent-risks/dist-market-design.png" alt="PLACEHOLDER: Dist AGI Table 1 market-design row (or section crop)" style="height: 400px">
            </div>
        </div>
    </div>
</div>

## Services as substrate

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <ul>
                    <li>Authors lean on <b>CAIS / AI services</b> for implementation style</li>
                    <li>Modularity, encapsulation, data abstraction, client/server composition</li>
                    <li>Useful for building agent systems. Also the place where data can become hard to see</li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/multi-agent-risks/dist-cais-services.png" alt="PLACEHOLDER: Dist AGI CAIS / services crop (or Drexler diagram)" style="height: 400px">
            </div>
        </div>
    </div>
</div>

## How the two fit

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <ul>
                    <li><b>CAIF:</b> what can go wrong (failure modes and risk factors)</li>
                    <li><b>Dist AGI:</b> an institutional response for patchwork AGI (markets, sandboxes, defence in depth)</li>
                    <li>Together: a map of multi-agent risk, plus one proposal for governing agent populations</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Discussion

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p>Optional prompts (skip if the room is already talking):</p>
                <br>
                <ul>
                    <li>Which CAIF risk factor feels most urgent for systems we already build?</li>
                    <li>Do agentic markets help, or do they recreate opacity through services?</li>
                    <li>What would you need to <b>observe</b> to trust multi-agent oversight?</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Links

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <ul>
                    <li>Hammond et al. · <a href="https://arxiv.org/abs/2502.14143" target="_blank" rel="noopener noreferrer">arXiv:2502.14143</a></li>
                    <li>Tomašev et al. · <a href="https://arxiv.org/abs/2512.16856" target="_blank" rel="noopener noreferrer">arXiv:2512.16856</a></li>
                </ul>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
