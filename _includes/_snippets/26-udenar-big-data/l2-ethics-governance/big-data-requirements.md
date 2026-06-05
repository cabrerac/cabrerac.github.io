<!-- SLIDES: -->

## Big Data Requirements

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <ul>
                    <li>Scalability: Elastic compute and storage at scale</li>
                    <li>Availability: Fault tolerance and replication</li>
                    <li>Latency: Network bandwidth and distributed execution</li>
                    <li>Security: identity, and access control</li>
                    <li>Interoperability: Service interfaces (APIs) for clients and pipelines</li>
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
                <img class="external-svg" src="https://miro.medium.com/v2/resize:fit:1100/format:webp/0*_aRaKVpgmI1hwiY7.png" alt="Apache Spark" style="height: 400px">
                <div class="footnote">
                    Big Data tools — via
                    <a href="https://informationit27.medium.com/big-data-open-source-tools-150d6a68214a" target="_blank" rel="noopener noreferrer">Medium</a>
                </div>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <ul>
                    <li>Distributed file systems and batch engines (Hadoop era)</li>
                    <li>In-memory and stream processing (Spark, Flink, Kafka)</li>
                    <li>Cloud object storage, warehouses, and lakehouse platforms</li>
                    <li>Orchestration, catalogues, and observability tools</li>
                </ul>
                <p>Most investment targets scale and speed...</p>
            </div>
        </div>
    </div>
</div>

## Big Data Requirements

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Data governance</b> is the formulation of policy to optimize, secure, and leverage information as an enterprise asset by aligning the objectives of multiple functions. <a href="https://doi.org/10.1145/1795194.1795237" target="_blank" rel="noopener noreferrer">(Khatri &amp; Brown, 2010)</a></p>
                <br>
                <p>Existing efforts: GDPR-style regulation, public-sector frameworks such as the <a href="https://www.gov.uk/government/publications/data-ethics-framework/data-and-ai-ethics-framework" target="_blank" rel="noopener noreferrer">UK Data and AI Ethics Framework</a> (transparency, accountability, fairness, privacy, trade-offs), catalogues, lineage, IAM. Still less mature than the technical stack, often reactive after harm.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/2/2e/Data-flow-diagram-example.svg" alt="Data governance flows" style="height: 380px">
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
                <img class="external-svg" src="https://i.guim.co.uk/img/media/b930887f181ada1747127defc2a50b0a8a14af8b/43_223_5393_3224/master/5393.jpg?width=620&dpr=2&s=none&crop=none" alt="Mark Zuckerberg stands and faces the audience as he testifies during the Senate hearing on online child sexual exploitation at the US Capitol in Washington DC. Photograph: Evelyn Hockstein/Reuters" style="height: 400px">
               <div class="footnote">Mark Zuckerberg stands and faces the audience as he testifies during the Senate hearing on online child sexual exploitation at the US Capitol in Washington DC. Photograph: Evelyn Hockstein/Reuters</div>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Governance after consequences</b></p>
                <ul>
                    <li>Public hearings follow harm, leaks, and election controversies</li>
                    <li>Policy and platform changes arrive late in the pipeline</li>
                    <li>Reactive fixes differ from designing requirements in from the start</li>
                    <li>Frameworks such as the <a href="https://www.gov.uk/government/publications/data-ethics-framework/data-and-ai-ethics-framework" target="_blank" rel="noopener noreferrer">UK Data and AI Ethics Framework</a> aim to bridge principles and practice earlier</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Big Data Requirements

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p>"<b>Surveillance capitalism</b> unilaterally claims human experience as free raw material for translation into behavioral data." <a href="https://doi.org/10.7551/mitpress/10858.001.0001" target="_blank" rel="noopener noreferrer">(Zuboff, 2019)</a></p>
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
                <img class="external-svg" src="https://imgs.xkcd.com/comics/machine_learning.png" alt="ML System?" style="height: 500px">
               <div class="footnote">https://xkcd.com/1838/, CC BY-NC 2.5 <https://creativecommons.org/licenses/by-nc/2.5/>, via XKCD</div>
            </div>
        </div>
    </div>
</div>

## Big Data Requirements

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/big-data-pipeline-template.svg" alt="Pipeline template" style="height: 380px">
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
