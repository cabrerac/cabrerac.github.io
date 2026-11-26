{% include _snippets/deployment.md %}

<!-- SLIDES: -->

## Deployment

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>An item's place among the others feeds something people do.</p>
                <ul>
                    <li><p><b>Report:</b> the central items, the bridges and the communities</p></li>
                    <li><p><b>Decision:</b> whom to brief, connect, or check first</p></li>
                    <li><p><b>Recommendation:</b> the other items in the same community</p></li>
                    <li><p><b>Watch list:</b> the hubs, read with care</p></li>
                </ul>
                <p>We deploy it with the graph boundary, the hub rule, and the resolution and seed of the communities.</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/pagerank-iteration-3.svg" alt="Four items sized by PageRank" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
</div>

## Deployment

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>What a deployed place implies</b></p>
                <ul>
                    <li><p><b>Place, not quality:</b> a central item is well linked, not better</p></li>
                    <li><p><b>Tied to the links inside the set:</b> a missing link moves a score or a community</p></li>
                    <li><p><b>Goes stale:</b> new links change places, so we rebuild the graph and check again</p></li>
                    <li><p><b>People:</b> in a graph of people, a hub is a warning, never an automatic pick</p></li>
                </ul>
                <p>Isolated items have no place. A deployed graph result says nothing about them.</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/graph-parts.svg" alt="The largest component, a small component and an isolated node" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
