<!-- SLIDES: -->

## The aICU Project

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>Deploying ML in the <b>Intensive Care Unit</b> to support practitioners — collaboration with clinicians at the <b>Karolinska Institute</b>.</p>
                <p>Team: doctors, data scientists, ML engineers, and HCI researchers. Problem-first, not model-first.</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/aicu-workshop.jpg" alt="aICU workshop" style="height: 400px">
            </div>
        </div>
    </div>
</div>

## The aICU Project

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>Interdisciplinary work requires:</p>
                <ul>
                    <li>A <b>common vocabulary</b> across clinical and technical roles</li>
                    <li>Openness to unfamiliar domains</li>
                    <li>Clear arguments when methods or ethics matter</li>
                    <li><b>Problem first</b> as the shared anchor</li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/aicu-workshop.jpg" alt="aICU workshop" style="height: 400px">
            </div>
        </div>
    </div>
</div>

## aICU-access

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/aicu-acces-architecture.svg" alt="aICU access architecture" style="height: 520px">
            </div>
        </div>
    </div>
</div>

## aICU-access

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Uniform access</b> to harmonised ICU data across heterogeneous sources (aICU, MIMIC, eICU, HiRID, …).</p>
                <ul>
                    <li><b>Federated deployment:</b> code goes to the data; same library locally and on hospital servers.</li>
                    <li><b>Harmonisation layer:</b> clinical concepts mapped to per-source extraction rules.</li>
                    <li><b>Query engine:</b> DuckDB with <code>delta_scan</code> on versioned Delta Lake tables.</li>
                    <li><b>Privacy by design:</b> least-privilege reads, auditable lineage, no unnecessary export.</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## aICU-access

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>Public API (stable contract for downstream analytics and ML):</p>
                <br>

```python
from aicu_access import load_concept
df = load_concept("hr", source="miiv")
```

</div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>Consumers — data quality, analytics, ML models — see <b>concepts</b>, not storage quirks.</p>
                <p>Adding a dataset = config + ingest script, not re-platforming.</p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
