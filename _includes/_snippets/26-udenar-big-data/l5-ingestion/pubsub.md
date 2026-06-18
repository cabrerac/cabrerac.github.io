<!-- SLIDES: -->

## Publish / Subscribe

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p>In <b>publish / subscribe</b>, <b>producers</b> publish events to a named <b>topic</b>, and <b>consumers</b> subscribe to it. Neither side knows the other.</p>
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
                    <li>Once landed, we can still export to Parquet for analytics</li>
                </ul>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
