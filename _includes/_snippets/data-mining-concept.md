<!-- SLIDES: -->

## The Data Mining Concept

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p>How we store data has changed with every era of computing. The right choice depends on <b>who writes, who reads, and what they ask</b>.</p>
            </div>
        </div>
    </div>
</div>

## The Data Mining Concept

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
                <p>The first need was not scale. It was <b>correctness</b> of structured records that many programs shared (i.e., relational databases).</p>
            </div>
        </div>
    </div>
</div>

## The Data Mining Concept

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

## The Data Mining Concept

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>From structured to messy</b></p>
                <ul>
                    <li>Tables of transactions still exist and still matter</li>
                    <li>But now we also store text, images, clickstreams, and maps</li>
                    <li>This is the <b>variety</b> of big data</li>
                </ul>
                <p>A relation is a fixed table. A non-relational store is not.</p>
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

## The Data Mining Concept

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p>Different needs produced different databases. Relational or not, every store makes one core bet about <b>read and write</b>.</p>
            </div>
        </div>
    </div>
</div>

## The Data Mining Concept

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Two opposite jobs</b></p>
                <ul>
                    <li><b>OLTP:</b> many small writes, read whole records, one at a time</li>
                    <li><b>OLAP:</b> few big reads, scan one column over millions of rows</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## The Data Mining Concept

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p><b>Stored data answers nothing on its own. What do we want to know?</b></p>
            </div>
        </div>
    </div>
</div>

## The Data Mining Concept

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Processing is its own stage</b></p>
                <ul>
                    <li><b>Filter:</b> keep only the rows that matter</li>
                    <li><b>Aggregate:</b> count, sum, and average over groups</li>
                    <li><b>Derive:</b> compute new facts the raw data did not state</li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/warehouse-olap.svg" alt="Operational systems to data warehouse to analytics" style="height: 360px">
            </div>
        </div>
    </div>
</div>

## The Data Mining Concept

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/warehouse-olap.svg" alt="Operational systems to data warehouse to analytics" style="height: 360px">
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Early processing: from records to reports</b></p>
                <ul>
                    <li>First systems just recorded transactions, one at a time</li>
                    <li>Managers wanted summaries, not single records</li>
                    <li>So data was copied into a separate place to analyse</li>
                </ul>
                <p>Reading for analysis is a different job from writing transactions. That split is what created processing as a stage.</p>
            </div>
        </div>
    </div>
</div>

## The Data Mining Concept

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/warehouse-olap.svg" alt="Operational systems to data warehouse to analytics" style="height: 360px">
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Data warehouses and history</b></p>
                <ul>
                    <li>A <b>warehouse</b> integrates clean data from many systems</li>
                    <li>It keeps <b>years of history</b>, organised by time</li>
                    <li>This is <b>OLAP</b>: few big reads that scan and group</li>
                </ul>
                <p>Keeping history is what made analysis possible. You cannot study a trend you did not store.</p>
            </div>
        </div>
    </div>
</div>

## The Data Mining Concept

<div class="rows" style="height: 100%">
    <div class="row" style="height: 18%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>What this group wrote</b></p>
                <p>Ten answers to what data mining is, in their own words.</p>
            </div>
        </div>
    </div>
    <div class="row" style="height: 82%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img src="{{ site.url }}/assets/media/images/intake-data-mining-words.png" alt="Word cloud of the group's definitions of data mining" style="width: 100%; height: auto">
            </div>
        </div>
    </div>
</div>

## The Data Mining Concept

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>A definition from the 1990s</b></p>
                <ul>
                    <li>A process, not one algorithm</li>
                    <li>Patterns that are valid, new, useful, and understandable</li>
                </ul>
                <br>
                <p>"The nontrivial process of identifying valid, novel, potentially useful, and ultimately understandable patterns in data." <a href="https://ojs.aaai.org/aimagazine/index.php/aimagazine/article/view/1230" target="_blank" rel="noopener noreferrer">(Fayyad et al., 1996)</a></p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/data-mining-archival-images-of-ai.jpg" alt="Data mining, archival images of AI" style="height: 400px">
                <div class="footnote">Data Mining 3 - Hanna Barakat &amp; Archival Images of AI + AIxDESIGN, CC BY 4.0 <https://creativecommons.org/licenses/by/4.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## The Data Mining Concept

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p><b>Data mining</b> is the search for valid, new and useful patterns in large collections of data, as one step of a longer process of knowledge discovery.</p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
