<!-- SLIDES: -->

## The Task

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Similar items</b></p>
                <p>Which items are similar enough to share a group, and which fit no group?</p>
                <ul>
                    <li>Each record is an item, described by its attributes</li>
                    <li>A group is a set of items closer to each other than to the rest</li>
                </ul>
                <br>
                <p>"The aim of clustering is to find structure in data and is therefore exploratory in nature." <a href="https://doi.org/10.1016/j.patrec.2009.09.011" target="_blank" rel="noopener noreferrer">(Jain, 2010)</a></p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/clusters-with-noise.svg" alt="Groups with noise points" style="height: 400px">
                <div class="footnote">Cluster-2 - hellisp and Wgabrie, Public domain, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## The Task

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>A group needs a reader</b></p>
                <p>A method returns labels, not meanings.</p>
                <ul>
                    <li>Someone who knows the field reads each group</li>
                    <li>The smallest group we accept is set before the results</li>
                    <li>An item far from every group is worth a look</li>
                </ul>
                <br>
                <p><b>Clustering</b> puts similar items in the same group, without being told what the groups are.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/critical-thinking.png" alt="Critical Thinking" style="height: 400px">
                <div class="footnote">Critical Thinking (Designed by freepik.com)</div>
            </div>
        </div>
    </div>
</div>

# The Data

## The Data

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Items described by attributes</b></p>
                <p>The data is many items, each described by the same attributes.</p>
                <ul>
                    <li><b>Item:</b> one record, such as a customer, a patient, or a text</li>
                    <li><b>Attribute:</b> one value per item, such as a count</li>
                    <li><b>Distance:</b> how far apart two items are</li>
                </ul>
                <p>A group is a set of items at a small distance.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/diagrams/group-items-attributes.svg" alt="Five items by four attributes" style="height: 380px">
            </div>
        </div>
    </div>
</div>

## The Data

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Attributes that separate groups</b></p>
                <p>An attribute helps only if its value changes from one group to another.</p>
                <ul>
                    <li><b>Common word:</b> in almost every item, such as the name of the department. It describes the whole dataset, so it cannot separate groups.</li>
                    <li><b>Rarer word:</b> in a few items. It can mark one group.</li>
                </ul>
                <p>Lecture 4 weighs this with TF-IDF: a word in many texts gets a low weight.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/diagrams/group-common-word.svg" alt="A word in every item next to words in a few items" style="height: 380px">
            </div>
        </div>
    </div>
</div>

# Modeling

## Methods

<div class="rows" style="height: 100%">
    <div class="row" style="height: 70%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img class="external-svg" src="{{ site.url }}/assets/media/diagrams/group-task-taxonomy.svg" alt="Taxonomy of grouping methods" style="width: 100%; height: 100%">
            </div>
        </div>
    </div>
    <div class="row" style="height: 30%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <p><b>Partitioning:</b> k-means and k-medoids.</p>
                <p><b>Model-based:</b> Gaussian mixtures and latent class models.</p>
                <p><b>Density-based:</b> HDBSCAN, DBSCAN, and OPTICS.</p>
                <p><b>Hierarchical:</b> agglomerative and divisive.</p>
            </div>
        </div>
    </div>
</div>

## Methods

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>k-medoids</b> uses real items as centres.</p>
                <p><b>Latent class models</b> are mixtures for categories.</p>
                <p><b>DBSCAN</b> finds dense regions at one radius.</p>
                <p><b>OPTICS</b> orders the items by density.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Agglomerative</b> merges the two closest groups, step by step.</p>
                <p><b>Divisive</b> splits a group, step by step.</p>
                <p>These names place the three methods we use today.</p>
            </div>
        </div>
    </div>
</div>

## Methods

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <ul>
                    <li><b>k-means:</b> each item goes to its closest centre</li>
                    <li><b>Gaussian mixture:</b> each item gets a probability for each group</li>
                    <li><b>HDBSCAN:</b> dense regions, and noise</li>
                </ul>
                <p>These apply to different data sources (e.g., customers, patients, texts, etc).</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/clusters-with-noise.svg" alt="Groups with noise points" style="height: 400px">
                <div class="footnote">Cluster-2 - hellisp and Wgabrie, Public domain, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
