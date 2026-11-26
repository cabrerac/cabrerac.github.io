<!-- SLIDES: -->

## The Data

<div class="rows" style="height: 100%">
    <div class="row" style="height: 57%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%; height: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/graph-from-table-4.svg" alt="The same graph and its adjacency matrix" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
    <div class="row" style="height: 43%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%; height: 100%">
                <p><b>Preparation:</b> from a table to a graph</p>
                <ul>
                    <li><p>Each row is an item, with the items it links to</p></li>
                    <li><p>Drop duplicate links and self links</p></li>
                    <li><p>Keep a link only when both ends are in the set</p></li>
                    <li><p>Row $i$, column $j$ is 1 when $i$ links to $j$</p></li>
                </ul>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
