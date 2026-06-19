<!-- SLIDES: -->

## Batch Processing

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p><b>Batch</b> collects data into a bounded chunk and processes it <b>on a schedule</b>. For example, every night.</p>
            </div>
        </div>
    </div>
</div>

## Batch Processing

<div class="rows" style="height: 100%">
    <div class="row" style="height: 86%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/batch-processing.svg" alt="Batch processing: bounded input, schedule trigger, ETL run, curated layer" style="height: 100%">
            </div>
        </div>
    </div>
    <div class="row" style="height: 14%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p>Collect a complete snapshot, then process it on a clock.</p>
            </div>
        </div>
    </div>
</div>

## Batch Processing

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Where it comes from</b></p>
                <ul>
                    <li>The oldest model of computing: mainframes ran <b>scheduled jobs</b> overnight</li>
                    <li>Payroll, billing, statements, and reports were produced in bulk</li>
                    <li>Data warehouses kept the same rhythm: load, then report</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/batch-processing.svg" alt="Batch processing: bounded input, schedule trigger, ETL run, curated layer" style="height: 100%">
            </div>
        </div>
    </div>
</div>

## Batch Processing

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Why it still dominates</b></p>
                <ul>
                    <li>High <b>throughput</b>: move a lot of data per run</li>
                    <li>Latency of hours or days is fine for many decisions</li>
                    <li>We do it once and reuse a stable <b>snapshot</b> (i.e., strong consistency)</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/batch-processing.svg" alt="Batch processing: bounded input, schedule trigger, ETL run, curated layer" style="height: 100%">
            </div>
        </div>
    </div>
</div>

## Batch Processing

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Extract, Transform, Load</b></p>
                <ul>
                    <li><b>Extract:</b> read the data from its source</li>
                    <li><b>Transform:</b> clean, join, rename, fix types</li>
                    <li><b>Load:</b> write it where analysts can use it</li>
                </ul>
                <p>ETL is the classic recipe of a batch pipeline. We met it in Lecture 3. Now we <b>automate</b> it.</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/big-data-pipeline-template.svg" alt="Pipeline template" style="height: 340px">
            </div>
        </div>
    </div>
</div>

## Batch Processing

<div class="rows" style="height: 100%">
    <div class="row" style="height: 72%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/etl-vs-elt.svg" alt="ETL versus ELT" style="height: 100%">
            </div>
        </div>
    </div>
    <div class="row" style="height: 28%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p><b>ETL or ELT?</b> Warehouses transform before load, so data lands clean. Lakehouses load raw and transform at query time. Either way we keep <b>staging</b> and <b>curated</b> layers.</p>
            </div>
        </div>
    </div>
</div>

## Batch Processing

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p>A real pipeline has <b>many steps</b> that must run in order. If one fails, we need to know <b>which</b> and recover. <b>Orchestration</b> manages that.</p>
            </div>
        </div>
    </div>
</div>

## Batch Processing

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>What an orchestrator gives us</b></p>
                <ul>
                    <li>Declare steps and the <b>order</b> between them (a workflow)</li>
                    <li><b>Schedule</b> runs (e.g. nightly) without a human</li>
                    <li><b>Retries</b> on failure and <b>observability</b>: logs of every run</li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/orchestrator-workflow.svg" alt="Orchestrated workflow: scheduler, Extract Transform Load Validate, governance sidecar" style="height: 100%">
            </div>
        </div>
    </div>
</div>

## Batch Processing

<div class="rows" style="height: 100%">
    <div class="row" style="height: 86%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/orchestrator-workflow.svg" alt="Orchestrated workflow: scheduler, Extract Transform Load Validate, governance sidecar" style="height: 100%">
            </div>
        </div>
    </div>
    <div class="row" style="height: 14%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p>Declare steps once. Run locally today, on schedule in production.</p>
            </div>
        </div>
    </div>
</div>

## Batch Processing

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>The tools</b></p>
                <ul>
                    <li><b>Apache Airflow</b> — the industry standard, schedules DAGs</li>
                    <li><b>Dagster</b> — asset-oriented, strong on data lineage</li>
                    <li><b>Prefect</b> — Pythonic flows; what we use in the lab</li>
                </ul>
                <p>We express steps as <b>tasks</b> and connect them in a <b>flow</b>. The same code runs locally today and on a schedule in production.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
               <img src="{{ site.url }}/assets/media/diagrams/orchestrator-workflow.svg" alt="Orchestrated workflow: scheduler, Extract Transform Load Validate, governance sidecar" style="height: 100%">
            </div>
        </div>
    </div>
</div>

## Batch Processing

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 38%">
                <p><b>A Prefect flow</b></p>
                <ul>
                    <li>Each <b>@task</b> is one ETL step</li>
                    <li>The <b>@flow</b> chains them in order</li>
                    <li>Prefect logs each run and can retry</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 62%">

```python
from prefect import flow, task

@task
def extract(paths):              # Extract: open partitions (lazy)
    return scan_parquet(paths)

@task
def aggregate(frame, output):    # Transform + Load: write curated layer
    result = (frame.filter(...)
                   .group_by(keys).agg(...).collect())
    result.write_parquet(output)
    return output

@task
def validate(path):              # Validate: the output must have rows
    assert read_parquet(path).height > 0
    return path

@flow(name="batch_ingest")
def batch_flow(paths, output):   # one flow chains the steps
    path = aggregate(extract(paths), output)
    return validate(path)
```

</div>
        </div>
    </div>
</div>

## Batch Processing

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p>Automating a pipeline raises a question from Lecture 2: <b>can we trust and reproduce</b> what it produced? Governance is built <b>into</b> ingestion.</p>
            </div>
        </div>
    </div>
</div>

## Batch Processing

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Mechanisms we add to the flow</b></p>
                <ul>
                    <li><b>Audit log:</b> who ran what, when, from which source</li>
                    <li><b>Schema contract:</b> the columns and types a step promises</li>
                    <li><b>Lineage:</b> trace an output back to its inputs</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">

```python
def append_audit(event):
    """One provenance record per pipeline step."""
    record = {**event, "ts": now_iso()}
    with open(AUDIT_LOG, "a") as f:
        f.write(json.dumps(record) + "\n")

contract = {
    "columns": {"key": "str", "count": "int"},
    "source": "curated/aggregate.parquet",
    "schema_version": 1,
    "retention_days": 365,
}
```

</div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
