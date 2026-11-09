<!-- SLIDES: -->

## The Task

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Items and the links among them</b></p>
                <p>Where does each item sit among the others?</p>
                <ul>
                    <li>Each record is an item and the items it links to</li>
                    <li>A place is read from the links, not from what the item says</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/social-network-analysis.jpg" alt="A network of links among people" style="height: 400px">
                <div class="footnote">Social Network Analysis Visualization - Martin Grandjean, CC BY-SA 3.0 <https://creativecommons.org/licenses/by-sa/3.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## The Task

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>What a graph adds</b></p>
                <p>Many methods look at each item alone, by its own attributes or words.</p>
                <ul>
                    <li>A graph looks at the links among items</li>
                    <li>Two items with no direct link can still share a neighbourhood</li>
                    <li>A place needs a rule set before the results, such as the rule for a hub</li>
                </ul>
                <br>
                <p>A <b>graph</b> is a set of items, called nodes, and the links among them, called edges.</p>
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
                <p><b>Items and links in one set</b></p>
                <p>The data is items and the links among them, inside one set.</p>
                <ul>
                    <li><p><b>Node:</b> one item</p></li>
                    <li><p><b>Directed edge:</b> $u \to v$, item $u$ links to item $v$</p></li>
                    <li><p><b>Undirected edge:</b> $u - v$, the two items are linked, whatever the direction</p></li>
                </ul>
                <p>A link to an item outside the set is dropped. An item with no link inside the set is isolated, which does not mean unimportant.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 45%">
                <p><b>Examples</b></p>
                <table class="table">
                    <thead>
                        <tr><th>Data</th><th>One node</th><th>Edges</th></tr>
                    </thead>
                    <tbody>
                        <tr><td>Papers</td><td>one paper</td><td>citations</td></tr>
                        <tr><td>People</td><td>one person</td><td>friendships</td></tr>
                        <tr><td>Web pages</td><td>one page</td><td>links</td></tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>

## The Data

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Words for a graph</b></p>
                <ul>
                    <li><p><b>Neighbours:</b> $N(v)$, the nodes linked to $v$</p></li>
                    <li><p><b>Path:</b> a chain of edges from one node to another</p></li>
                    <li><p><b>Shortest path:</b> a path with the fewest edges</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Parts of a graph</b></p>
                <ul>
                    <li><b>Component:</b> nodes that can all reach each other</li>
                    <li><b>Largest component:</b> the biggest of them</li>
                    <li><b>Isolated node:</b> no link to any other item in the set</li>
                </ul>
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
                <img class="external-svg" src="{{ site.url }}/assets/media/diagrams/graph-task-taxonomy.svg" alt="Taxonomy of graph methods" style="width: 100%; height: 100%">
            </div>
        </div>
    </div>
    <div class="row" style="height: 30%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Link counts:</b> how many links an item has, and from whom.</p>
                <p><b>Paths:</b> how an item sits on the shortest paths between others.</p>
                <p><b>Node embeddings:</b> one vector per item, learned from the links.</p>
                <p><b>Communities:</b> groups of items with more links inside than outside.</p>
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
                    <li><b>Degree:</b> how many links an item has</li>
                    <li><b>PageRank:</b> links weighted by who makes them</li>
                    <li><b>node2vec:</b> which items share a neighbourhood</li>
                </ul>
                <p>These apply to different data sources (e.g., papers, people, web pages, etc).</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/social-network-analysis.jpg" alt="A network of links among people" style="height: 400px">
                <div class="footnote">Social Network Analysis Visualization - Martin Grandjean, CC BY-SA 3.0 <https://creativecommons.org/licenses/by-sa/3.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
