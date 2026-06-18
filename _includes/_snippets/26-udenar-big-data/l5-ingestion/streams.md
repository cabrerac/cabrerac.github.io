<!-- SLIDES: -->

## Streams

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p>A <b>stream</b> is data that arrives <b>continuously as events over time</b> — it never ends and we cannot wait for a nightly batch.</p>
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
                <p>These systems produce data faster than batch windows can absorb, and decisions need it <b>soon</b>.</p>
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
                <p>Production systems run <b>both</b>: batch for the heavy, governed history; stream for the fresh signal. The question is how producers and consumers talk — the <b>publish / subscribe</b> pattern.</p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
