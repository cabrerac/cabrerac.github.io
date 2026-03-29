<!-- SLIDES: -->

## Policy Factorisation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Factorisation</b>: separating the <b>reasoning</b> (Z) from the <b>action</b> (A) in a decision.</p>
                <br>
                <p>In the POMDP framework, a policy maps beliefs to actions: <b>&pi;(b) &rarr; a</b>. With factorisation we observe the intermediate reasoning: <b>&pi;(b) &rarr; (z, a)</b>.</p>
                <br>
                <ul>
                    <li><b>Z</b> (reasoning): chain-of-thought, tool-use traces, confidence scores</li>
                    <li><b>A</b> (action): the environment-specific primitive</li>
                </ul>
                <br>
                <p>Both live in the same <code>agent_update</code> record. Observable, queryable, analysable.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>DOAgent captures reasoning from two sources transparently:</b></p>
                <br>
                <p><b>1. Tool traces (automatic)</b></p>
                <p>When agents have <code>tools</code>, the library wraps each callable and captures inputs, output, timing.</p>
                <br>
                <p><b>2. Policy-provided reasoning</b></p>
                <p>The policy may return its own <code>reasoning</code> (e.g. LLM chain-of-thought, native reasoning tokens).</p>
                <br>
                <p>The library <b>merges</b> both sources into a single <code>reasoning</code> field. No extra work from the user.</p>
            </div>
        </div>
    </div>
</div>

## The "I Don't Know" Function

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
        "choice": {
          "status": "abstain",
          "action": null
        },
        "reasoning": {
          "chain_of_thought": "Observation is ambiguous.
           Two landmarks are equidistant.
           Confidence: 0.15.",
          "steps": [{"kind": "tool", "name": "llm", ...}]
        }
      },
      "explanation": "Abstained: low confidence (0.15)."
    }
  }
}
```
</div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>"I don't know"</b> is not a special feature. It is a <b>natural product of reasoning</b>.</p>
                <br>
                <ul>
                    <li>The LLM reasons, concludes low confidence &rarr; <code>status: "abstain"</code></li>
                    <li>The reasoning trace explains <b>why</b> the agent abstained</li>
                    <li>The record is inspectable via <code>session.inspect("agent_update")</code></li>
                </ul>
                <br>
                <p>Inspired by the <b>Consistent Reasoning Paradox</b> <a href="https://arxiv.org/abs/2310.13684" target="_blank" rel="noopener noreferrer">(CRP, 2023)</a>: trustworthy behaviour includes the ability to say "I don't know."</p>
                <br>
                <p><b>Factorisation makes abstention observable.</b> Without it, a null action is indistinguishable from a bug.</p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
