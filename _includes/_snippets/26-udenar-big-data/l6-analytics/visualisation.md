<!-- SLIDES: -->

## Visualisation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p>A chart is an <b>argument</b> for a decision. Visualisation turns numbers into something a person can <b>reason about</b>.</p>
            </div>
        </div>
    </div>
</div>

## Visualisation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Choose the chart for the question</b></p>
                <ul>
                    <li><b>Trend over time?</b> a line chart</li>
                    <li><b>Compare categories?</b> a bar chart</li>
                    <li><b>Relationship between two variables?</b> a scatter plot</li>
                    <li><b>Distribution?</b> a histogram or box plot</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <div style="display: flex; justify-content: space-between;">
                    <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/e/e2/Normhist.png" alt="Normal Distribution Histogram" style="height: 300px">
                    <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/1/17/Normprob.png" alt="Normal Probability Distribution" style="height: 300px">
                </div>
                <div class="footnote">Normal Probability Plot - Visnut, CC BY 3.0 <https://creativecommons.org/licenses/by/3.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Visualisation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
               <p><b>Honest charts</b></p>
                <ul>
                    <li>Start axes at a sensible <b>baseline</b>; do not exaggerate</li>
                    <li>Label units, the <b>source</b>, and the date</li>
                    <li>Show <b>uncertainty</b> when it matters</li>
                </ul>
               <p>A misleading chart is a governance failure, not a style choice.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <div style="display: flex; justify-content: space-between;">
                    <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/e/e2/Normhist.png" alt="Normal Distribution Histogram" style="height: 300px">
                    <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/1/17/Normprob.png" alt="Normal Probability Distribution" style="height: 300px">
                </div>
                <div class="footnote">Normal Probability Plot - Visnut, CC BY 3.0 <https://creativecommons.org/licenses/by/3.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Visualisation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p>A <b>dashboard</b> brings several charts together for an audience. <b>What you choose to show</b> and what you hide is a governance decision.</p>
            </div>
        </div>
    </div>
</div>

## Visualisation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Evidence layers</b></p>
                <ul>
                    <li><b>Official layer:</b> the result we stand behind</li>
                    <li><b>Context layer:</b> monitoring and exploration, clearly labelled <b>not official</b></li>
                </ul>
                <p><b>Governance controls</b></p>
                <ul>
                    <li>Different <b>audiences</b> see different panels</li>
                    <li><b>Suppress</b> small groups to protect people</li>
                    <li>State the <b>source</b> and <b>refresh date</b> on every panel</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
               <img class="external-svg" src="{{ site.url }}/assets/media/images/cities-board.png" alt="Cities-Board" style="height: 300px">
               <div class="footnote">Cities-Board: A Framework to Automate the Development of Smart Cities Dashboards. <a href="https://ieeexplore.ieee.org/abstract/document/9119074" target="_blank" rel="noopener noreferrer">(Rojas, 2020)</a></p></div>
            </div>
        </div>
    </div>
</div>

## Visualisation

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
