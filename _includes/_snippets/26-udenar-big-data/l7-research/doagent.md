<!-- SLIDES: -->

## DOAgent

<div class="rows" style="height: 100%">
   <div class="row" style="height: 100%">
        <div class="columns" style="width: 95%">
            <div class="column vertical-middle text-center" style="width: 50%">
               <img src="https://upload.wikimedia.org/wikipedia/commons/d/da/Magent-graph-2.gif" alt="Multi-agent system" style="max-width: 100%; height: auto;">
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Gap:</b> MAS frameworks orchestrate agents, but rarely treat <b>decisions, outcomes, traces, provenance, and accountability</b> as first-class records under one schema.</p>
                <p>DOAgent contributes a <b>data-oriented substrate</b> where analysis is built in, not bolted on.</p>
            </div>
        </div>
    </div>
</div>

## DOAgent

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <ul>
                    <li><b>Data-first:</b> agents communicate through a shared substrate (InMemory, JSONL, MongoDB).</li>
                    <li><b>Decentralisation:</b> centralised, federated, or peer-to-peer topologies via configuration.</li>
                    <li><b>Openness:</b> agents join and leave; capabilities registered in a participation registry.</li>
                    <li><b>Policy-agnostic:</b> heuristic, RL, or LLM policies under the same record model.</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## DOAgent

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <br>

```json
{
  "id": "au-abc123",
  "kind": "agent_update",
  "actor": "agent_0",
  "payload": {
    "decision": {
      "response": {
        "choice": {"status": "act", "action": 2},
        "reasoning": {"steps": [...]}
      },
      "explanation": "Moved toward landmark."
    }
  },
  "provenance": {"agent": "agent_0"},
  "accountability": {"owner": "team-a"}
}
```
</div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Core record kinds</b></p>
                <ul>
                    <li><b>agent_update</b> — decision envelope (choice + optional reasoning)</li>
                    <li><b>outcome</b> — environment state after each step</li>
                    <li><b>trace</b> — links outcomes via the update that caused the transition</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## DOAgent

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 75%">
               <img class="external-svg" src="{{ site.url }}/assets/media/diagrams/doagent-architecture.svg" alt="DOAgent architecture" style="height: 900px">
            </div>
            <div class="column vertical-middle text-center" style="width: 25%">
               <p><b><a href="https://github.com/cabrerac/doagent" target="_blank" rel="noopener noreferrer">github.com/cabrerac/doagent</a></b></p>
            </div>
        </div>
    </div>
</div>

## DOAgent

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <br>

```python
from doagent.analysis import (
    provenance, traceability,
    accountability, interpretability,
)
traceability.build_trace_graph(run_id, ...)
accountability.causal_attribution(run_id, ...)
```
</div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/trace_graph.png" alt="Trace graph from shared records" style="max-width: 100%; height: auto;">
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
