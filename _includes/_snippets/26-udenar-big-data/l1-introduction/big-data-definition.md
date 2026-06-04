<!-- SLIDES: -->

## What is Big Data

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p>Industry and research stretched the term as storage, computing, and pipelines changed.</p>
                <table class="table">
                    <tr>
                        <td>
                            <p>"Data storage is growing at a higher rate than ever before, and coupled with rapidly increasing demand for instant access, will cause great stress on both the physical and the human infrastructure of computing."</p>
                            <p><a href="https://www.usenix.org/conference/1999-usenix-annual-technical-conference/big-data-and-next-wave-infrastress-problems" target="_blank" rel="noopener noreferrer">(Mashey, 1999)</a></p>
                        </td>
                        <td>
                            <p>"Big data refers to datasets whose size is beyond the ability of typical database software tools to capture, store, manage, and analyze."</p>
                            <p><a href="https://www.mckinsey.com/~/media/mckinsey/business%20functions/mckinsey%20digital/our%20insights/big%20data%20the%20next%20frontier%20for%20innovation/mgi_big_data_exec_summary.pdf" target="_blank" rel="noopener noreferrer">(Manyika et al., 2011)</a></p>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <p>"Big Data is a cultural, technological, and scholarly phenomenon that rests on the interplay of technology, analysis, and mythology."</p>
                            <p><a href="https://doi.org/10.1080/1369118X.2012.678878" target="_blank" rel="noopener noreferrer">(boyd &amp; Crawford, 2012)</a></p>
                        </td>
                        <td>
                            <p>"Big Data consists of extensive datasets that require a scalable architecture for efficient storage, manipulation, and analysis because of data volume, variety, velocity, and/or variability."</p>
                            <p><a href="https://doi.org/10.6028/NIST.SP.1500-1" target="_blank" rel="noopener noreferrer">(NIST, 2015)</a></p>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
    </div>
</div>

## What is Big Data

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Common dimensions: 3Vs? 4Vs? 5Vs?</b></p>
                <ul>
                    <li><b>Volume</b> - data no longer fits comfortably in memory</li>
                    <li><b>Velocity</b> - data arrives continuously or in bursts</li>
                    <li><b>Variety</b> - tables, files, streams, and maps mixed together</li>
                    <li><b>Veracity</b> - quality, bias, and missing values matter</li>
                    <li><b>Value</b> - data must support a decision or action that matters</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## What is Big Data

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <img src="https://upload.wikimedia.org/wikipedia/commons/8/8b/Moore%27s_Law_Transistor_Count_1971-2018.png" alt="Moore's Law" style="width: 100%; border-radius: 5px;">
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->

{% include _snippets/timelines/ai-history-87-today.md %}

{% include _snippets/timelines/ai-history-2000-2012.md %}

{% include _snippets/timelines/ai-history-2001-today.md %}

<!-- SLIDES: -->

## What is Big Data

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Big data in the 2000s</b></p>
                <p>Large and complex datasets improve models' statistical power.</p>
                <ul>
                    <li>Social networks</li>
                    <li>Mobile computing</li>
                    <li>Internet of Things</li>
                    <li>Public and official statistics at a national scale</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/e/e3/BigData_2267x1146_trasparent.png" alt="Big Data dimensions" style="width: 100%; background-color: #f6f8fa; padding: 10px; border-radius: 5px;">
            </div>
        </div>
    </div>
</div>

## What is Big Data

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Big data developments</b></p>
                <ul>
                    <li><b>Hadoop and HDFS:</b> distributed file systems</li>
                    <li><b>MapReduce:</b> batch jobs split into scalable steps</li>
                    <li><b>Apache Spark:</b> distributed processing</li>
                    <li><b>NoSQL stores:</b> Cassandra, HBase, MongoDB</li>
                    <li><b>Stream processing:</b> Kafka, Flink for live data</li>
                    <li><b>Cloud warehouses:</b> BigQuery, Redshift, Snowflake</li>
                    <li><b>Lakehouse formats:</b> Parquet, Delta Lake, Iceberg</li>
                    <li><b>Orchestration:</b> Airflow, Prefect for data pipelines</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/e/e3/BigData_2267x1146_trasparent.png" alt="Big Data dimensions" style="width: 100%; background-color: #f6f8fa; padding: 10px; border-radius: 5px;">
            </div>
        </div>
    </div>
</div>

## What is Big Data

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>In this course, we explore situations where at least one dimension of big data forces a <b>non-trivial choice</b> across the data management process.</p>
                <ul>
                    <li>Formal labels and Vs are useful, but they are not enough on their own</li>
                    <li>More data is not automatically better understanding <a href="https://doi.org/10.1080/1369118X.2012.678878" target="_blank" rel="noopener noreferrer">(boyd &amp; Crawford, 2012)</a></li>
                    <li>We start from the problem and the decision, not from a platform logo</li>
                    <li>For us, the most important V is <b>value</b></li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/e/e3/BigData_2267x1146_trasparent.png" alt="Big Data dimensions" style="width: 100%; background-color: #f6f8fa; padding: 10px; border-radius: 5px;">
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
