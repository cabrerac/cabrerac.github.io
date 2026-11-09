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
                    <li>Then decides what the group is for</li>
                </ul>
                <br>
                <p>"In reality, a cluster is a subjective entity that is in the eye of the beholder and whose significance and interpretation requires domain knowledge." <a href="https://doi.org/10.1016/j.patrec.2009.09.011" target="_blank" rel="noopener noreferrer">(Jain, 2010)</a></p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/critical-thinking.png" alt="Critical Thinking" style="height: 400px">
                <div class="footnote">Critical Thinking (Designed by freepik.com)</div>
            </div>
        </div>
    </div>
</div>

## The Task

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>What counts as a group</b></p>
                <p>A few items that happen to sit close are not a group.</p>
                <ul>
                    <li>A group needs a minimum size, set before the results</li>
                    <li>It also needs to beat what a shuffled table would give</li>
                    <li>An item far from every group is worth a look. It can be an error, a rare case, or something new</li>
                </ul>
                <br>
                <p><b>Clustering</b> puts similar items in the same group and different items in different groups, without being told what the groups are.</p>
            </div>
        </div>
    </div>
</div>

# The Data

## The Data

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 55%">
                <p><b>A set of items</b></p>
                <p>The data is many items, each described by the same attributes.</p>
                <ul>
                    <li><b>Item:</b> one record, such as a customer, a patient, or a text</li>
                    <li><b>Attribute:</b> one value per item, such as a count or a measurement</li>
                    <li><b>Distance:</b> how far apart two items are, computed from their attributes</li>
                </ul>
                <p>Attributes on very different scales are scaled first, so no attribute decides alone. A group is a set of items at a small distance.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 45%">
                <p><b>Examples</b></p>
                <table class="table">
                    <thead>
                        <tr><th>Data</th><th>One item</th><th>Attributes</th></tr>
                    </thead>
                    <tbody>
                        <tr><td>Customers</td><td>one customer</td><td>purchase counts</td></tr>
                        <tr><td>Patients</td><td>one visit</td><td>measurements</td></tr>
                        <tr><td>Texts</td><td>one text</td><td>word counts</td></tr>
                    </tbody>
                </table>
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
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Partitioning:</b> every item goes to one of $k$ groups around centres.</p>
                <p><b>Model-based:</b> each group is a probability distribution, so membership is a probability.</p>
                <p><b>Density-based:</b> groups are dense regions, and items in thin regions are noise.</p>
                <p><b>Hierarchical:</b> a tree of groups inside groups, cut at a chosen level.</p>
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
                    <li><b>HDBSCAN:</b> dense regions, and the items that fit no group</li>
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
