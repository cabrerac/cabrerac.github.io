<!-- SLIDES: -->

## The aICU Project

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>Deploying ML in the <b>Intensive Care Unit</b> to support practitioners in collaboration with clinicians at the <b>Karolinska Institute</b>.</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
               <img src="{{ site.url }}/assets/media/diagrams/aicu-acces-architecture.svg" alt="aICU access architecture" style="height: 520px">
            </div>
        </div>
    </div>
</div>

## The aICU Project

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/big-data-pipeline-template.svg" alt="Big data pipeline, analytics stage" style="height: 380px">
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
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/aicu-acces-architecture.svg" alt="aICU access architecture" style="height: 520px">
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Uniform access</b> to harmonised ICU data across heterogeneous sources (aICU, MIMIC, eICU, HiRID, …).</p>
                <ul>
                    <li><b>Federated deployment:</b> same library locally and on hospital servers.</li>
                    <li><b>Harmonisation layer:</b> clinical concepts mapped to per-source extraction rules.</li>
                    <li><b>Query engine:</b> DuckDB with delta_scan on versioned Delta Lake tables.</li>
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
                <div class="column vertical-middle text-center" style="width: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/aicu-acces-architecture.svg" alt="aICU access architecture" style="height: 520px">
            </div>
</div>
            <div class="column vertical-middle text-left" style="width: 50%">

```python
from aicu_access import load_concept
df = load_concept("hr", source="miiv")
```
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
