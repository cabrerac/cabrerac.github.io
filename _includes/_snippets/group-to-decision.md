{% include _snippets/deployment.md %}
<!-- SLIDES: -->

## Deployment

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Deploying a group</b></p>
                <p>A group of similar items feeds something people do.</p>
                <ul>
                    <li><b>Report:</b> each group with its size and top attributes, for a person to read</li>
                    <li><b>Decision:</b> one plan, offer, or reading list per group</li>
                    <li><b>Routing:</b> a new item goes to the nearest group</li>
                    <li><b>Review:</b> the items that fit no group go to a person</li>
                </ul>
                <p>We deploy the groups together with $k$ or min_cluster_size, the silhouette against its baseline, and stability.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/clusters-with-noise.svg" alt="Groups with noise points" style="height: 400px">
                <div class="footnote">Cluster-2 - hellisp and Wgabrie, Public domain, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Deployment

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>What a deployed group implies</b></p>
                <ul>
                    <li><b>A group is a reading, not a fact:</b> a person names it, and another person may name it otherwise</li>
                    <li><p><b>Tied to the data and the settings:</b> another $k$, seed, or number of directions gives other groups</p></li>
                    <li><b>Goes stale:</b> new items move the centres, so we re-run and re-check stability</li>
                    <li><b>People:</b> who is labelled by a group, and who sits in noise</li>
                </ul>
                <br>
                <p>Items in noise fit no group. A deployed group says nothing about them.</p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
