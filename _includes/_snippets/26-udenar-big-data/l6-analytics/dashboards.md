<!-- SLIDES: -->

## Dashboards as Governance

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p>A <b>dashboard</b> brings several charts together for an audience. <b>What you choose to show</b> — and what you hide — is a governance decision.</p>
            </div>
        </div>
    </div>
</div>

## Dashboards as Governance

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Evidence layers</b></p>
                <ul>
                    <li><b>Official layer:</b> the result we stand behind</li>
                    <li><b>Context layer:</b> monitoring and exploration, clearly labelled <b>not official</b></li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Governance controls</b></p>
                <ul>
                    <li>Different <b>audiences</b> see different panels</li>
                    <li><b>Suppress</b> small groups to protect people</li>
                    <li>State the <b>source</b> and <b>refresh date</b> on every panel</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Dashboards as Governance

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 38%">
                <p><b>Two layers, one figure</b></p>
                <ul>
                    <li>Each panel <b>names</b> its layer</li>
                    <li>The context panel is marked <b>not official</b></li>
                    <li>The title carries the source</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 62%">

```python
from plotly.subplots import make_subplots
import plotly.graph_objects as go

dash = make_subplots(rows=2, cols=1, subplot_titles=[
    "Official layer: observed vs predicted",
    "Context layer: monitoring (not official)",
])
dash.add_trace(go.Scatter(x=y_val, y=pred, mode="markers"),
               row=1, col=1)
dash.add_trace(go.Bar(x=["events stored"], y=[n_context]),
               row=2, col=1)
dash.update_layout(
    title_text="Evidence dashboard - official + context",
)
```

</div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
