{% include _snippets/deployment.md %}
<!-- SLIDES: -->

## Deployment

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Deploying a place</b></p>
                <p>An item's place among the others feeds something people do.</p>
                <ul>
                    <li><b>Report:</b> the central items and their neighbours, for a person to read</li>
                    <li><b>Decision:</b> whom to brief, connect, or check first</li>
                    <li><b>Recommendation:</b> the nearest neighbours of an item</li>
                    <li><b>Watch list:</b> the hubs, read with care</li>
                </ul>
                <p>We deploy it together with the graph boundary, the hub rule, the seeds, and the random-pair baseline.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/diagrams/pagerank-abc.svg" alt="Three nodes sized by PageRank. A cites B, and B and C cite each other" style="height: 340px">
                <div class="footnote">PageRank on a small graph, A cites B, and B and C cite each other</div>
            </div>
        </div>
    </div>
</div>

## Deployment

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>What a deployed place implies</b></p>
                <ul>
                    <li><b>Place, not quality:</b> a central item is well linked, not better</li>
                    <li><b>Tied to the links inside the set:</b> a missing link moves a score, and isolated is not unimportant</li>
                    <li><b>Goes stale:</b> new links change places, so we rebuild the graph and check again</li>
                    <li><b>People:</b> in a graph of people, a score ranks people, so a hub is a warning, never an automatic pick</li>
                </ul>
                <br>
                <p>Isolated items have no place. A deployed graph result says nothing about them.</p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
