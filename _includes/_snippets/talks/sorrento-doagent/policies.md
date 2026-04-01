<!-- SLIDES: -->

## Policies: From Heuristics to LLMs

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <br>

```python
def heuristic_goal_seek(params):
    def decide(request):
        obs = request["inputs"]["observation"]
        action = compute_best_move(obs)
        return {
            "choice": {"status": "act", "action": action}
        }
    return decide
```
</div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Heuristic policies</b></p>
                <ul>
                    <li>Agents have always had policies: rules, heuristics, RL, symbolic planners</li>
                    <li>A policy receives a request and returns a <code>choice</code></li>
                    <li><code>choice.status</code>: "act", "abstain", or "error"</li>
                    <li><code>choice.action</code>: the environment-specific primitive</li>
                </ul>
                <br>
                <p>DOAgent is <b>model-agnostic</b>: the library coordinates decisions, not how they are made.</p>
            </div>
        </div>
    </div>
</div>

## Policies: From Heuristics to LLMs

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <br>

```python
def llm_decide_factory(params):
    def decide(request):
        llm = request["tools"]["llm"]
        prompt = build_prompt(request)
        raw = llm(model="gpt-4o", messages=prompt)
        parsed = json.loads(raw)
        return {
            "choice": {
                "status": "act" if confident else "abstain",
                "action": parsed.get("action"),
            },
            "reasoning": parsed.get("reasoning"),
            "explanation": parsed.get("explanation"),
        }
    return decide
```
</div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>LLM as a policy</b></p>
                <ul>
                    <li><b>Same interface</b>, same records, same analysis</li>
                    <li>The LLM adds: natural-language <code>reasoning</code> and <code>explanation</code></li>
                    <li>The LLM callable is injected as a <b>tool</b> — no framework dependency</li>
                </ul>
                <br>
                <p>What is branded <i>"Agentic AI"</i> is this: <b>an LLM as the policy function</b> in a multi-agent system. LLMs enable policy factorisation using natural language — but the coordination and architecture are established MAS patterns.</p>
            </div>
        </div>
    </div>
</div>

## Policies: From Heuristics to LLMs

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <br>

```json
{
  "kind": "agent_update",
  "actor": "agent_0",
  "payload": {
    "decision": {
      "response": {
        "choice": {"status": "act", "action": 2}
      }
    }
  }
}
```

<p style="text-align: center;"><b>Heuristic agent record</b><br>Simple choice, no reasoning.</p>
</div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <br>

```json
{
  "kind": "agent_update",
  "actor": "agent_0",
  "payload": {
    "decision": {
      "response": {
        "choice": {"status": "act", "action": 2},
        "reasoning": {
          "steps": [{"kind": "tool", "name": "llm", ...}],
          "chain_of_thought": "The goal is north..."
        }
      },
      "explanation": "Moved north toward landmark."
    }
  }
}
```

<p style="text-align: center;"><b>LLM agent record</b><br>Same choice + observable reasoning.</p>
</div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
