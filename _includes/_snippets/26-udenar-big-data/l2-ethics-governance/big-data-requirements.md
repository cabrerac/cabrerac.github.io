<!-- SLIDES: -->

## Big Data Requirements

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Technical requirements (cloud computing)</b></p>
                <ul>
                    <li>Elastic compute and storage at scale</li>
                    <li>Fault tolerance and replication</li>
                    <li>Network bandwidth and distributed execution</li>
                    <li>Security, identity, and access control</li>
                    <li>Service interfaces (APIs) for clients and pipelines</li>
                    <li><b>Ethics</b>, <b>privacy</b>, and <b>fairness</b></li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/soa-cloud.png" alt="Client-server cloud setup" style="height: 400px">
            </div>
        </div>
    </div>
</div>

## Big Data Requirements

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="https://upload.wikimedia.org/wikipedia/commons/c/c2/Apache_Hadoop.svg" alt="Hadoop ecosystem" style="height: 120px">
                <img src="https://upload.wikimedia.org/wikipedia/commons/f/f3/Apache_Spark_logo.svg" alt="Apache Spark" style="height: 80px; margin-left: 20px">
                <img src="https://upload.wikimedia.org/wikipedia/commons/5/51/Cloud_computing_icon.svg" alt="Cloud computing" style="height: 100px; margin-left: 20px">
                <div class="footnote">Apache Hadoop and Spark logos, cloud icon — via Wikimedia Commons</div>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Industry response to technical requirements</b></p>
                <ul>
                    <li>Distributed file systems and batch engines (Hadoop era)</li>
                    <li>In-memory and stream processing (Spark, Flink, Kafka)</li>
                    <li>Cloud object storage, warehouses, and lakehouse platforms</li>
                    <li>Orchestration, catalogues, and observability tools</li>
                    <li>Most investment targets scale and speed, not the bold items above</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Big Data Requirements

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Data governance (scientific view)</b></p>
                <p>«Data governance is the formulation of policy to optimize, secure, and leverage information as an enterprise asset by aligning the objectives of multiple functions.» <a href="https://doi.org/10.1145/1795194.1795237" target="_blank" rel="noopener noreferrer">(Khatri &amp; Brown, 2010)</a></p>
                <p><b>Privacy in context:</b> appropriate flow of information depends on context and role, not secrecy alone. <a href="https://doi.org/10.2139/ssrn.3885612" target="_blank" rel="noopener noreferrer">(Nissenbaum, 2004)</a></p>
                <p>Existing efforts: GDPR-style regulation, catalogues, lineage, IAM. Still less mature than the technical stack, often reactive after harm.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="https://upload.wikimedia.org/wikipedia/commons/4/4f/Data-flow-diagram-example.svg" alt="Data governance flows" style="height: 380px">
                <div class="footnote">Data flow diagram example, CC BY-SA 3.0, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Big Data Requirements

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="https://upload.wikimedia.org/wikipedia/commons/f/f2/Mark_Zuckerberg_testifies_before_the_U.S._Senate_%28cropped%29.jpg" alt="Senate hearing" style="height: 400px">
                <div class="footnote">Mark Zuckerberg testifies before the U.S. Senate, April 2018 — public domain, via Wikimedia Commons</div>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Governance after consequences</b></p>
                <ul>
                    <li>Public hearings follow harm, leaks, and election controversies</li>
                    <li>Policy and platform changes arrive late in the pipeline</li>
                    <li>Reactive fixes differ from designing requirements in from the start</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Big Data Requirements

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>«Surveillance capitalism unilaterally claims human experience as free raw material for translation into behavioral data.»</p>
                <p><a href="https://doi.org/10.7551/mitpress/10858.001.0001" target="_blank" rel="noopener noreferrer">(Zuboff, 2019)</a> — assigned reading, Chapter 1</p>
                <p>Contrast with public statistics (GEIH): a different social contract and duty of care.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/context-3.png" alt="Data-driven system" style="height: 400px">
            </div>
        </div>
    </div>
</div>

## Big Data Requirements

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Problem first, not ethics last</b></p>
                <ul>
                    <li>Ethics is often taught as a final checklist before deployment</li>
                    <li>In this course we place <b>ethics</b>, <b>privacy</b>, and <b>fairness</b> at the start of the pipeline</li>
                    <li>Next: define what these terms mean and where they apply</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/big-data-pipeline-template.svg" alt="Pipeline template" style="height: 380px">
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
