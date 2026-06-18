<!-- SLIDES: -->

## Streaming at Scale

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p>A single log on one machine is not enough at scale. Streaming platforms <b>distribute</b> the log and process it <b>in parallel</b>.</p>
            </div>
        </div>
    </div>
</div>

## Streaming at Scale

<div class="rows" style="height: 100%">
    <div class="row" style="height: 14%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p><b>Distribution, partitioning, and parallelism</b></p>
            </div>
        </div>
    </div>
    <div class="row" style="height: 86%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/pubsub-streaming-architecture.svg" alt="Publish/subscribe streaming architecture: producers, partitioned topic across brokers, consumer group" style="height: 100%">
            </div>
        </div>
    </div>
</div>

## Streaming at Scale

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>How the architecture scales</b></p>
                <ul>
                    <li>A topic is split into <b>partitions</b> spread across <b>brokers</b></li>
                    <li>One partition per consumer &#8594; <b>horizontal parallelism</b></li>
                    <li>Partitions are <b>replicated</b> &#8594; a broker can fail without data loss</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Streaming at Scale

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>The tools</b></p>
                <ul>
                    <li><b>Apache Kafka</b> — the distributed log and broker</li>
                    <li><b>Apache Flink</b> / <b>Spark Streaming</b> — stream processing engines</li>
                    <li><b>Bytewax</b> — stream processing in pure Python</li>
                </ul>
                <p>"Kafka is a distributed messaging system ... for collecting and delivering high volumes of log data with low latency." <a href="https://www.microsoft.com/en-us/research/wp-content/uploads/2017/09/Kafka.pdf" target="_blank" rel="noopener noreferrer">(Kreps et al., 2011)</a></p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Production vs our lab</b></p>
                <ul>
                    <li>Cluster of brokers + Flink &#8594; <b>one local broker</b> in the notebook</li>
                    <li>Managed MongoDB &#8594; an <b>in-memory</b> document store</li>
                    <li>Always-on service &#8594; an <b>ephemeral</b> session</li>
                </ul>
                <p>Same API and same ideas, no cluster to run.</p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
