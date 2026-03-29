<!-- SLIDES: -->

## DOAgent Library

<div class="rows" style="height: 100%">
   <div class="row" style="height: 100%">
        <div class="columns" style="width: 95%">
            <div class="column vertical-middle text-center" style="width: 50%">
               <img src="https://upload.wikimedia.org/wikipedia/commons/d/da/Magent-graph-2.gif" alt="Multi-agent" style="max-width: 100%; height: auto;">
               <div class="footnote">Two rival teams of agents - Jordan K. Terry, CC BY-SA 4.0, via Wikimedia Commons</div>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/context-3.png" alt="AI System" style="height: 400px">
            </div>
        </div>
    </div>
</div>

## DOAgent Library

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <br>

```python
from doagent import Session

session = Session.from_config({
    "shared_data": {"type": "file"},
    "scenario_name": "push",
    "output_base": "./output",
    "run_config": {"logging_level": 2},
    "policies": {
        "goal_seek": heuristic_goal_seek,
        "push_block": heuristic_push_block,
    },
})
```
</div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Data-first Principle</b></p>
                <p>Agents communicate through a shared data substrate.</p>
                <ul>
                    <li>Config-driven Session API: one entry point for env, agents, and policies</li>
                    <li>Shared data adapters: InMemory, File (JSONL), MongoDB</li>
                    <li>Logging levels control what is recorded (traces, provenance, reasoning)</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## DOAgent Library

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <br>

```json
{
  "id": "au-abc123",
  "timestamp": "2026-03-28T10:00:00Z",
  "actor": "agent_0",
  "kind": "agent_update",
  "payload": {
    "decision": {
      "request": {"inputs": {"observation": {...}}},
      "response": {
        "choice": {"status": "act", "action": 2},
        "reasoning": {"steps": [...]}
      },
      "explanation": "Moved toward landmark."
    }
  },
  "provenance": {"agent": "agent_0", "sources": [...]},
  "accountability": {"owner": "team-a", "policy_id": "pol-1"}
}
```
</div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Data Model</b></p>
                <ul>
                    <li><b>agent_update</b>: decision envelope with request, response (choice + reasoning), and explanation</li>
                    <li><b>outcome</b>: environment state after each step</li>
                    <li><b>trace</b>: cause-effect links between outcomes via agent_updates</li>
                </ul>
                <br>
                <p><b>Logging levels:</b></p>
                <ul>
                    <li>Level 0: agent_update + outcome</li>
                    <li>Level 1: + trace + provenance + accountability</li>
                    <li>Level 2: + explanation + reasoning</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## DOAgent Library

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <br>

```python
from doagent import Session

session = Session.from_config({
    ...
    "topology": {
        "mode": "peer_to_peer",
        "visibility": {
            "agent_0": ["agent_1"],
            "agent_1": ["agent_2"],
        }
    },
})
# Each agent sees only listed peers' records
records = session.visible_records("agent_0",
    kind="agent_update")
```
</div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Decentralisation Principle</b></p>
                <p>Support for heterogeneous communication schemas.</p>
                <ul>
                    <li>Topology: centralised, federated, peer-to-peer</li>
                    <li>Visibility filters which records each agent sees</li>
                    <li>Same agent code runs under any topology — configuration, not code change</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## DOAgent Library

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <br>

```python
# Participation registry: agents join and leave
session.register_participant("agent_0",
    capabilities=["map_discovery"])

# Energy model: deregister when depleted
if energy <= 0:
    session.deregister_participant("agent_0")

# Query who is present
participants = session.participation_registry
```
</div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Openness Principle</b></p>
                <p>Agents can join and leave at any time.</p>
                <ul>
                    <li>ParticipationRegistry: register and query which agents are present</li>
                    <li>Capabilities and resources per agent</li>
                    <li>Session-level API for join/leave</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## DOAgent Library

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 75%">
               <!-- TODO: Update architecture diagram with choice/reasoning/factorisation -->
               <img class="external-svg" src="{{ site.url }}/assets/media/diagrams/doagent-architecture.svg" alt="DOAgent Architecture" style="height: 1000px">
            </div>
            <div class="column vertical-middle text-left" style="width: 25%">
               <img class="external-svg" src="{{ site.url }}/assets/media/images/doagent-qr.png" alt="DOAgent QR Code" style="height: 400px">
            </div>
        </div>
    </div>
</div>

## DOAgent Library

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 50%">
               <img src="https://upload.wikimedia.org/wikipedia/commons/d/da/Magent-graph-2.gif" alt="Multi-agent" style="max-width: 100%; height: auto;">
               <div class="footnote">Two rival teams of agents - Jordan K. Terry, CC BY-SA 4.0, via Wikimedia Commons</div>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>What users provide</b></p>
                <ul>
                    <li><b>Environments:</b> Use built-in (e.g. PettingZoo) or custom. The library wraps them so outcomes and traces are recorded</li>
                    <li><b>Agents:</b> Define via config. The library creates them and connects them to shared data</li>
                    <li><b>Policies:</b> Plug in any decision logic (heuristic, RL, LLM, or custom). The library records decisions and optional reasoning</li>
                    <li><b>Tools (optional):</b> Per-agent callables. The library wraps them for transparent tool-use tracing</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## DOAgent Library

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <br>

```python
from doagent import Session, make_env

session = Session.from_config(config)
env = make_env(create_push_env, max_cycles=100)
wrapped = session.wrap_env(env, env_actor="push_env")
agents = session.create_agents(configs,
    goal="push_towards_landmark")

observations = wrapped.reset(seed=42)
for round_id in range(1, 101):
    actions = {
        aid: agents[aid].decide(
            observations[aid], round_id
        )["action"]
        for aid in agents
    }
    step = wrapped.step(actions)
    observations = step["observations"]
```
</div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Run loop</b></p>
                <ul>
                    <li><code>session.wrap_env</code> records outcomes and traces automatically</li>
                    <li><code>session.create_agents</code> binds policies from config</li>
                    <li><code>agent.decide()</code> records the agent_update, wraps tools, merges reasoning</li>
                    <li>User code stays minimal — the library handles recording</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## DOAgent Library

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/gridworld_demo.gif" alt="Grid-world" style="height: 400px">
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>GridWorld validation example</b></p>
                <ul>
                    <li>Dependency-free grid-world mapping scenario: agents discover cells and landmarks under partial observations</li>
                    <li>Each round agents publish an agent_update. They read the shared map (from visible records) and choose a move</li>
                    <li>Configurable topology and visibility. Optional energy-based participation (join/leave)</li>
                    <li>Run from config. Session records outcomes, traces, and agent_updates transparently</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## DOAgent Library

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <br>

```json
{"id":"out-1","kind":"outcome",
"actor":"env","payload":{...}}
{"id":"au-1","kind":"agent_update",
"actor":"agent_0","payload":{
  "decision":{"response":{"choice":{"status":"act","action":2}}}
}}
{"id":"tr-1","kind":"trace",
"payload":{"from_id":"out-0","to_id":"out-1",
"enabled_by_id":"au-1","round":1}}
```
</div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Stored records</b></p>
                <ul>
                    <li><b>outcome</b>: env state after each step (observations per agent, done flags)</li>
                    <li><b>agent_update</b>: per-agent decision envelope with choice, optional reasoning, explanation</li>
                    <li><b>trace</b>: from_id, to_id, enabled_by_id — links outcome-to-outcome via the agent_update that caused the transition</li>
                    <li>Collection-per-kind (e.g. outcome.jsonl, agent_update.jsonl, trace.jsonl)</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## DOAgent Library

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/trace_graph.png" alt="Trace graph" style="max-width: 100%; height: auto;">
            </div>
        </div>
    </div>
</div>

## DOAgent Library

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

provenance.render_chain_tree("last", run_id,
    output_base="output", write_output=True)
traceability.build_trace_graph(run_id,
    output_base="output", write_output=True)
accountability.causal_attribution(run_id,
    output_base="output", write_output=True)
interpretability.build_atomic_explanations(
    "last", run_id, output_base="output",
    write_output=True)
```
</div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Analysis from records alone</b></p>
                <ul>
                    <li><b>Provenance:</b> chain of records leading to an outcome</li>
                    <li><b>Traceability:</b> cause-effect graph across the run</li>
                    <li><b>Accountability:</b> causal attribution — which agent caused which state transitions</li>
                    <li><b>Interpretability:</b> atomic explanation units from traces and decisions</li>
                </ul>
                <br>
                <p>All analysis uses <b>only shared records</b>. No access to policy or env internals. Same tools for any policy type.</p>
            </div>
        </div>
    </div>
</div>

## DOAgent Library

<div class="rows" style="height: 100%">
    <div class="row" style="height: 80%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/causal_attribution.png" alt="Causal attribution results" style="max-width: 100%; height: auto;">
            </div>
        </div>
    </div>
    <div class="row" style="height: 20%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Causal attribution results:</b> Left: per-agent cumulative discovery over rounds. Centre: total cells discovered per agent. Right: decision effectiveness (productive vs redundant transitions). All derived from shared records.</p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
