<!-- SLIDES: -->

## Last Time

<div class="rows" style="height: 100%">
    <div class="row text-center vertical-middle" style="height: 12%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-center" style="width: 100%">
                <b>Your words from the week 2 discussion</b>
            </div>
        </div>
    </div>
    <div class="row" style="height: 88%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/26-udenar-big-data/week2-wordcloud.png" alt="Week 2 discussion word cloud" style="height: 440px">
            </div>
        </div>
    </div>
</div>

## Last Time

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Can we predict everything?</b></p>
                <ul>
                    <li>One of you asked whether, with enough data, a model could predict the world <b>without uncertainty</b></li>
                    <li>That is the old dream of <b>Laplace's demon</b></li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>"An intellect which ... would know all forces that set nature in motion ... for such an intellect nothing would be uncertain and the future just like the past would be present before its eyes." <a href="https://en.wikipedia.org/wiki/Laplace%27s_demon" target="_blank" rel="noopener noreferrer">(Laplace, 1814)</a></p>
            </div>
        </div>
    </div>
</div>

## Last Time

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Why the demon is a myth</b></p>
                <ul>
                    <li>Perfect prediction would need complete <b>laws</b>, complete <b>data</b>, and unlimited <b>compute</b></li>
                    <li>In practice all three are <b>incomplete</b> — so we model <b>uncertainty</b> with probability</li>
                    <li>Even when publishing aggregates, naive numbers leak — we add <b>noise</b> to protect one person</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>"...the curve described by a molecule of air ... is regulated in a manner just as certain as the planetary orbits; the only difference between them is that which comes from our ignorance." <a href="https://inverseprobability.com/2026/01/25/laplaces-gremlin-and-irreducibility" target="_blank" rel="noopener noreferrer">(on Laplace; Lawrence, 2026)</a></p>
            </div>
        </div>
    </div>
</div>

## Last Time

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 42%">
                <p><b>We built a lakehouse</b></p>
                <ul>
                    <li>Raw files landed cheaply, like a <b>lake</b></li>
                    <li>We queried them with warehouse-style structure</li>
                    <li>A <b>lakehouse</b> is both: low-cost storage plus management features</li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 58%">
                <img src="{{ site.url }}/assets/media/diagrams/lake-warehouse-lakehouse.svg" alt="Data lake, warehouse, and lakehouse" style="height: 420px">
            </div>
        </div>
    </div>
</div>

## Last Time

<div class="rows" style="height: 100%">
    <div class="row" style="height: 14%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p><b>We processed at scale with MapReduce</b></p>
            </div>
        </div>
    </div>
    <div class="row" style="height: 86%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/mapreduce-dataflow.svg" alt="MapReduce dataflow: input, map, shuffle, reduce" style="height: 100%">
            </div>
        </div>
    </div>
</div>

## Last Time

<div class="rows" style="height: 100%">
    <div class="row" style="height: 14%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p><b>Storage and processing are stages of one pipeline</b> — today we connect them with <b>ingestion</b></p>
            </div>
        </div>
    </div>
    <div class="row" style="height: 86%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/big-data-pipeline-template.svg" alt="Big data pipeline" style="height: 100%">
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
