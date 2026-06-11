<!-- SLIDES: -->

## The Need to Store

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p><b>Where does the data live after the program ends?</b></p>
            </div>
        </div>
    </div>
</div>

## The Need to Store

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Raw files pile up fast</b></p>
                <ul>
                    <li>One data file per period, hundreds of MB each (for GEIH, one ZIP per month)</li>
                    <li>Several tables to join on every run</li>
                    <li>Related sources to keep side by side</li>
                </ul>
                <p>Reading and joining raw files on every run is slow, fragile, and hard to share with a teammate.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/data-quality.jpg" alt="Data quality and usability" style="height: 400px">
            </div>
        </div>
    </div>
</div>

## The Need to Store

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Storage is its own stage of the pipeline</b></p>
                <ul>
                    <li><b>Durability:</b> data outlives the notebook session</li>
                    <li><b>Shareability:</b> a team reads the same clean dataset</li>
                    <li><b>Scale:</b> read one month without loading the whole year</li>
                    <li><b>Cost:</b> compressed bytes are cheaper to keep and move</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/big-data-pipeline-template.svg" alt="Pipeline template, store stage" style="height: 380px">
            </div>
        </div>
    </div>
</div>

## The Need to Store

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p>How we store data has changed with every era of computing. The right choice depends on <b>who writes, who reads, and what they ask</b>. To understand today's formats, we follow the history that produced them.</p>
            </div>
        </div>
    </div>
</div>

## Systems and the Web Evolve

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/early-information-system.svg" alt="Early information system" style="height: 400px">
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Early information systems</b></p>
                <ul>
                    <li>Banks, governments, and universities recorded transactions</li>
                    <li>Data was structured, repeated, and had to stay consistent</li>
                    <li>One wrong balance or duplicated record was a real problem</li>
                </ul>
                <p>The first need was not scale. It was <b>correctness</b> of structured records that many programs shared.</p>
            </div>
        </div>
    </div>
</div>

## Systems and the Web Evolve

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>The web changes who produces data</b></p>
                <ul>
                    <li><b>Web 1.0:</b> few publishers, many readers, static pages</li>
                    <li><b>Web 2.0:</b> everyone writes, social networks, comments, photos</li>
                    <li><b>Web 3.0:</b> linked and machine-readable data, maps, sensors</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="https://upload.wikimedia.org/wikipedia/commons/d/d1/First_Web_Server.jpg" alt="First web server at CERN" style="height: 360px; border-radius: 5px;">
                <div class="footnote">The NeXT computer used by Tim Berners-Lee as the first web server. Photo by Coolcaesar, CC BY-SA 3.0, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Systems and the Web Evolve

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>From structured to messy</b></p>
                <ul>
                    <li>Tables of transactions still exist and still matter</li>
                    <li>But now we also store text, images, clickstreams, and maps</li>
                    <li>This is the <b>variety</b> dimension of big data from lecture 1</li>
                </ul>
                <p>"Big Data consists of extensive datasets that require a scalable architecture for efficient storage, manipulation, and analysis because of data volume, variety, velocity, and/or variability." <a href="https://doi.org/10.6028/NIST.SP.1500-1" target="_blank" rel="noopener noreferrer">(NIST, 2015)</a></p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">

```json
{
  "type": "node",
  "id": 1234567,
  "lat": 1.2136, "lon": -77.2811,
  "tags": {
    "amenity": "school",
    "name": "School 1"
  }
}
```

<div class="footnote">A semi-structured OpenStreetMap node. No fixed table, just nested keys and values.</div>
            </div>
        </div>
    </div>
</div>

## Systems and the Web Evolve

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p>Different needs produced different databases. Next we look at the two big families that answer them, <b>relational</b> and <b>non-relational</b>.</p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
