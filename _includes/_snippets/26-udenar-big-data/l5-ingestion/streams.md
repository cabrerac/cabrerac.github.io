<!-- SLIDES: -->

## Streams

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p>A <b>stream</b> is data that arrives <b>continuously as events over time</b>. It never ends and we cannot wait for a nightly batch.</p>
            </div>
        </div>
    </div>
</div>

## Streams

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Where it comes from</b></p>
                <ul>
                    <li>Web and mobile <b>logs</b>, clickstreams, application events</li>
                    <li><b>Sensors and IoT</b> devices emitting readings</li>
                    <li>Financial <b>ticks</b>, messages, and news feeds</li>
                </ul>
                <p>These systems produce data faster than batch windows can absorb, and decisions need it <b>soon</b> (i.e., real time).</p>
            </div>
        </div>
    </div>
</div>

## Streams

<div class="rows" style="height: 100%">
    <div class="row" style="height: 86%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/stream-processing.svg" alt="Stream processing: unbounded timeline, time windows, stream processor, outputs" style="height: 100%">
            </div>
        </div>
    </div>
    <div class="row" style="height: 14%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p>Process events as they arrive. Results over time windows.</p>
            </div>
        </div>
    </div>
</div>

## Streams

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Batch</b></p>
                <ul>
                    <li>Bounded data, run on a schedule</li>
                    <li>High throughput, latency hours/days</li>
                    <li>Consistent on a snapshot</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Stream</b></p>
                <ul>
                    <li>Unbounded events, processed as they arrive</li>
                    <li>Low latency, results over <b>windows</b> of time</li>
                    <li>Eventual consistency</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Streams

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p>Production systems run <b>both</b>: batch for the heavy, governed history; stream for the fresh signal. The question is how producers and consumers talk.</p>
            </div>
        </div>
    </div>
</div>

## Publish / Subscribe

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p>In <b>publish/subscribe</b>, <b>producers</b> publish events to a named <b>topic</b>, and <b>consumers</b> subscribe to it. Neither side knows the other.</p>
            </div>
        </div>
    </div>
</div>

## Publish / Subscribe

<div class="rows" style="height: 100%">
    <div class="row" style="height: 86%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/pubsub-mechanism.svg" alt="Publish subscribe: producers, append-only topic log, consumers" style="height: 100%">
            </div>
        </div>
    </div>
    <div class="row" style="height: 14%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p>A topic is an append-only log. Consumers track their offset.</p>
            </div>
        </div>
    </div>
</div>

## Publish / Subscribe

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>A topic is an append-only log</b></p>
                <ul>
                    <li>New events are added <b>at the end</b>, never edited</li>
                    <li>Each event has an <b>offset</b>, its position in the log</li>
                    <li>Events are <b>retained</b>, so consumers can replay</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Why decouple?</b></p>
                <ul>
                    <li>Producers and consumers scale and fail <b>independently</b></li>
                    <li>Add a new consumer without touching producers</li>
                    <li>A buffer absorbs bursts of traffic</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Publish / Subscribe

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 38%">
                <p><b>The producer side</b></p>
                <ul>
                    <li>Serialise each event to JSON</li>
                    <li><b>send</b> it to the topic</li>
                    <li>The topic is created on first write</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 62%">

```python
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

for event in events:
    producer.send("events", event)   # publish to the topic
producer.flush()                     # make sure everything left
```

</div>
        </div>
    </div>
</div>

## Publish / Subscribe

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 38%">
                <p><b>The consumer side</b></p>
                <ul>
                    <li>Read from the start of the log</li>
                    <li><b>De-duplicate</b> by a stable id</li>
                    <li>Land events in a store for later</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 62%">

```python
from kafka import KafkaConsumer

consumer = KafkaConsumer(
    "events",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",    # from the start of the log
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
)

seen = set()
for message in consumer:             # events as they arrive
    event = message.value
    if event["id"] not in seen:      # de-duplicate
        seen.add(event["id"])
        store.insert_one(event)      # land in a document store
```

</div>
        </div>
    </div>
</div>

## Publish / Subscribe

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Stream events are semi-structured</b></p>
                <ul>
                    <li>Each event is a JSON document whose fields may vary</li>
                    <li>Their natural home is a <b>document store</b> (e.g. MongoDB), not a rigid table</li>
                </ul>
            </div>
        </div>
    </div>
</div>

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
                <img src="{{ site.url }}/assets/media/diagrams/pubsub-streaming-architecture.svg" alt="Publish subscribe streaming architecture: producers, partitioned topic across brokers, consumer group" style="height: 100%">
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
                    <li>One partition per consumer in the group: <b>horizontal parallelism</b></li>
                    <li>Partitions are <b>replicated</b>: a broker can fail without data loss</li>
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
                    <li>Cluster of brokers + Flink: <b>one local broker</b> in the notebook</li>
                    <li>Managed MongoDB: an <b>in-memory</b> document store</li>
                    <li>Always-on service: an <b>ephemeral</b> session</li>
                </ul>
                <p>Same API and same ideas, no cluster to run.</p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
