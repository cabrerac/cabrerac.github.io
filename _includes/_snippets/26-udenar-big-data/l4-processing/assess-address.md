<!-- SLIDES: -->

## Data Science Methodology

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p>Running <b>pandas, DuckDB, or Polars</b> is not the end of processing. It is how you <b>reach</b> the data. After that you still <b>assess</b> what you got and <b>address</b> the decision question.</p>
            </div>
        </div>
    </div>
</div>

## Data Science Methodology

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <img src="{{ site.url }}/assets/media/images/data-science-process.png" alt="Data Science Process" style="height: 500px">
            </div>
        </div>
    </div>
</div>

## Data Assess

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Understand and trust the query result</b></p>
                <ul>
                    <li><b>Profile:</b> row counts, missing weights, duplicate keys</li>
                    <li><b>Validate rules:</b> does <code>activity == 1</code> match your employ definition?</li>
                    <li><b>Check coverage:</b> all months / departments present?</li>
                    <li><b>Governance:</b> quasi-identifiers still in stored files?</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Data cleaning</b></p>
                <ul>
                    <li>Drop or impute missing expansion factors with justification</li>
                    <li>Resolve inconsistent codes across years</li>
                    <li>Document every transform in the notebook or manifest</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Data Address

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Use the data to answer the policy question</b></p>
                <ul>
                    <li><b>Aggregates:</b> weighted employment by department</li>
                    <li><b>Artifacts:</b> tables, charts, maps for stakeholders</li>
                    <li><b>Decisions:</b> what we can claim and what we cannot</li>
                </ul>
                <p>Address is <b>not only machine learning</b>. Many big-data projects stop at reliable, governed aggregates and indicators.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Later in the course</b> some groups may add models (L6). The pipeline still flows:</p>
                <p><b>Access</b> (ingest) → <b>Assess</b> (quality) → <b>Address</b> (evidence for a decision).</p>
                <p>Week 2 group notebook: build the lakehouse, query it, <b>assess</b> outputs, <b>address</b> with a publishable aggregate under k-anonymity rules.</p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
