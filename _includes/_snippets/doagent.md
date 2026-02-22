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
from doagent.core import FileSharedData
from doagent.core import StubAgent

shared_data = FileSharedData()
agent = StubAgent("agent-1", shared_data)
agent.write(kind="note", payload={"text": "Hello"})
for r in shared_data.listen("note"):
    print(r.id, r.payload)
```
</div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Data-first Principle</b></p>
                <ul>
                    <li>Shared data adapter with CRUD and listen operations
                    <li>Adapters: For now, InMemory, File (JSONL), and MongoDB</li>
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
  "id": "rec-abc123",
  "timestamp": "2026-02-22T10:00:00Z",
  "actor": "agent_0",
  "kind": "agent_update",
  "payload": { "action": 2, "round": 1 },
  "provenance": { "created_by": "agent_0", "derived_from": ["out-1"] },
  "accountability": { "owner": "team-a", "policy_id": "pol-1" }
}
```
</div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Data-first Principle</b></p>
                <ul>
                    <li>Data Model storing agents updates, environment outcomes, and traces</li>
                    <li>Logging levels controls trace, explanation, provenance, and accountability writes</li>
                    <li>Provenance: created_by, derived_from, used_tools</li>
                    <li>Accountability: owner, policy_id, responsibility_scope</li>
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
from doagent.core import Topology
from doagent.core import TopologyConfig
from doagent.core import select_routing

config = TopologyConfig(mode=Topology.FEDERATED)
decision = select_routing(config)
```
</div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Decentralisation Principle</b></p>
                <ul>
                    <li>Topology: Centralised, federated, p2p</li>
                    <li>TopologyConfig and select_routing: Visibility filters which records each agent sees</li>
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
from doagent.core import InMemoryParticipationRegistry
from doagent.core import ParticipationRecord

registry = InMemoryParticipationRegistry()
registry.register(ParticipationRecord(
    agent_id="agent-1",
    capabilities=["compute"]))
```
</div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Openness Principle</b></p>
                <ul>
                    <li>ParticipationRegistry: Register and query which agents are present to support join/leave and resource exchange</li>
                    <li>ParticipationRecord: agent identifier, capabilities, and resources</li>
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
               <img class="external-svg" src="{{ site.url }}/assets/media/diagrams/doagent-architecture.svg" alt="DOAgent Architecture" style="height: 1000px">
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
                    <li><b>Environments:</b> Use built-in (e.g. PettingZoo) or customised environments. The library wraps it so outcomes and traces are recorded</li>
                    <li><b>Agents:</b> Define which agents take part of the system. The library creates them from config files and connects them to shared data</li>
                    <li><b>Policies:</b> Plug in decision logic via policy adapters (LLM, rules, RL, or custom). The library records decisions and optional explanations</li>
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
env = make_grid_env(width=6, height=6, agent_ids=[...])
registry = PolicyRegistry()
registry.register("pol", pol_fn)
configs = [GridAgentConfig(...)]
session = Session(shared_data, RunConfig(), topology_config=...)
env = session.wrap_env(raw_env, env_actor="env")
agents = session.create_agents(env, configs, registry)
obs = env.reset()
while not done:
    actions = [a.decide(obs) for a in agents]
    obs, rewards, done = env.step(actions)
```
</div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>What users provide</b></p>
                <ul>
                    <li><b>Environments:</b> Use built-in (e.g. PettingZoo) or customised environments. The library wraps it so outcomes and traces are recorded</li>
                    <li><b>Agents:</b> Define which agents take part of the system. The library creates them from config files and connects them to shared data</li>
                    <li><b>Policies:</b> Plug in decision logic via policy adapters (LLM, rules, RL, or custom). The library records decisions and optional explanations</li>
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
                <img class="external-svg" src="{{ site.url }}/assets/media/images/marl-grid.png" alt="Grid-world" style="height: 400px">
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>GridWorld validation example</b></p>
                <ul>
                    <li>Dependency-free grid-world mapping scenario: agents discover cells and landmarks under partial observations</li>
                    <li>Each round agents publish an agent_update. They read the shared map (from visible records) and choose a move according to its policy</li>
                    <li>Configurable topology (centralised, federated, p2p) and visibility. Optional energy-based participation (join/leave)</li>
                    <li>Run from YAML config. Session records outcomes, traces, and agent_updates transparently</li>
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
"actor":"agent_0","payload":{"action":2,"round":1}}
{"id":"tr-1","kind":"trace",
"payload":{"from_id":"out-0","to_id":"out-1"
"enabled_by_id":"au-1","round":1}}
```
</div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Stored records</b></p>
                <ul>
                    <li>Outcome: env state after each step (observations per agent, done flags). One per distinct state when dedup is on</li>
                    <li>Agent_update: per-agent decision and action each round. Links to the outcome it enabled</li>
                    <li>Trace: from_id, to_id, enabled_by_id. Links outcome-to-outcome via the agent_update that caused the transition</li>
                    <li>Collection-per-kind (e.g. outcome.jsonl, agent_update.jsonl, trace.jsonl with FileSharedData)</li>
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
traces = load_jsonl(records_dir / "trace.jsonl")
outcomes = load_jsonl(records_dir / "outcome.jsonl")
agent_updates = load_jsonl(records_dir / "agent_update.jsonl")
attribution = compute_attribution(traces, outcomes, agent_updates)
```
</div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Causal attribution analysis</b></p>
                <ul>
                    <li>Given the trace graph (from_id, to_id, enabled_by_id) and outcome payloads (observations per agent), attribute each state transition to the enabling agent</li>
                    <li>Per agent: cumulative cells discovered over time, total discovery, productive vs redundant moves (decision effectiveness)</li>
                    <li>DOAgent enables it: analysis uses only shared records (trace, outcome, agent_update). No access to policy or env internals. Same script for any run at logging level 2</li>
                </ul>
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
                <p><b>Causal attribution results:</b> Left presents per-agent cumulative discovery over rounds. Centre shows total cells discovered per agent. Right presents decision effectiveness (productive vs redundant transitions per agent). All derived from shared records. No policy or environment internals required.</p>
            </div>
        </div>
    </div>
</div>

## DOAgent Library

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/topology_comparison.png" alt="Topology comparison results" style="max-width: 100%; height: auto;">
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
