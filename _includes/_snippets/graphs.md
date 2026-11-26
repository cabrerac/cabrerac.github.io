<!-- SLIDES: -->

## The Task

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>Where does each item sit among the others?</p>
                <ul>
                    <li><p>Each record is an item and the items it links to</p></li>
                    <li><p>A place is read from the links, not from what the item says</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/social-network-analysis.jpg" alt="A network of links among people" style="height: auto; max-width: 100%; max-height: 90%;">
                <div class="footnote">Social Network Analysis Visualization - Martin Grandjean, CC BY-SA 3.0 <https://creativecommons.org/licenses/by-sa/3.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## The Task

<div class="rows" style="height: 100%">
    <div class="row" style="height: 58%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%; height: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/graph-links-1.svg" alt="Six items, each alone" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
    <div class="row" style="height: 42%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%; height: 100%">
                <p>Many methods look at each item alone, by its own attributes or words.</p>
                <ul>
                    <li><p>A graph looks at the links among items</p></li>
                </ul>
            </div>
        </div>
    </div>
</div>

## The Task

<div class="rows" style="height: 100%">
    <div class="row" style="height: 58%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%; height: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/graph-links-2.svg" alt="Two items with no direct link share a neighbour" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
    <div class="row" style="height: 42%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%; height: 100%">
                <p>Many methods look at each item alone, by its own attributes or words.</p>
                <ul>
                    <li><p>A graph looks at the links among items</p></li>
                    <li><p>Two items with no direct link can still share a neighbourhood</p></li>
                </ul>
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
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>Items and the links among them, inside one set.</p>
                <ul>
                    <li><p><b>Node:</b> one item</p></li>
                    <li><p><b>Directed edge:</b> $u \to v$, item $u$ links to item $v$</p></li>
                    <li><p><b>Undirected edge:</b> $u - v$, the two items are linked</p></li>
                </ul>
                <p>Papers and citations, people and friendships, or web pages and links.</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/graph-words-1.svg" alt="Nodes and directed edges" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
</div>

## The Data

<div class="rows" style="height: 100%">
    <div class="row" style="height: 60%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%; height: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/graph-words-2.svg" alt="The neighbours of C highlighted" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
    <div class="row" style="height: 40%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%; height: 100%">
                <ul>
                    <li><p><b>Neighbours:</b> $N(v)$, the nodes linked to $v$. Here $N(C) = \{A, B, D, F\}$</p></li>
                </ul>
            </div>
        </div>
    </div>
</div>

## The Data

<div class="rows" style="height: 100%">
    <div class="row" style="height: 60%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%; height: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/graph-words-3.svg" alt="A shortest path from A to E" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
    <div class="row" style="height: 40%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%; height: 100%">
                <ul>
                    <li><p><b>Neighbours:</b> $N(v)$, the nodes linked to $v$. Here $N(C) = \{A, B, D, F\}$</p></li>
                    <li><p><b>Path:</b> a chain of edges from one node to another</p></li>
                    <li><p><b>Shortest path:</b> a path with the fewest edges, here 3 edges from A to E</p></li>
                </ul>
            </div>
        </div>
    </div>
</div>

## The Data

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <ul>
                    <li><p><b>Component:</b> nodes that can all reach each other</p></li>
                    <li><p><b>Largest component:</b> the biggest of them</p></li>
                    <li><p><b>Isolated node:</b> no link to any other item in the set</p></li>
                </ul>
                <p>A link to an item outside the set is dropped. Isolated does not mean unimportant.</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/graph-parts.svg" alt="The largest component, a small component and an isolated node" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
</div>

## The Data

<div class="rows" style="height: 100%">
    <div class="row" style="height: 62%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%; height: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/graph-from-table-2.svg" alt="Duplicate and self links dropped" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
    <div class="row" style="height: 38%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%; height: 100%">
                <p><b>Preparation:</b> from a table to a graph</p>
                <ul>
                    <li><p>Each row is an item, with the items it links to</p></li>
                    <li><p>Drop duplicate links and self links</p></li>
                </ul>
            </div>
        </div>
    </div>
</div>

## The Data

<div class="rows" style="height: 100%">
    <div class="row" style="height: 62%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%; height: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/graph-from-table-3.svg" alt="The links that stay, drawn as a graph" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
    <div class="row" style="height: 38%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%; height: 100%">
                <p><b>Preparation:</b> from a table to a graph</p>
                <ul>
                    <li><p>Each row is an item, with the items it links to</p></li>
                    <li><p>Drop duplicate links and self links</p></li>
                    <li><p>Keep a link only when both ends are in the set</p></li>
                </ul>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->

{% include _snippets/26-udenar-data-mining/l5-graphs/from-table-matrix.md %}

<!-- SLIDES: -->

# Modeling

## Methods

<div class="rows" style="height: 100%">
    <div class="row" style="height: 65%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%; height: 100%">
                <img class="external-svg" src="{{ site.url }}/assets/media/diagrams/graph-task-taxonomy.svg" alt="Taxonomy of graph methods" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
    <div class="row" style="height: 35%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%; height: 100%">
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
                    <li><p><b>PageRank:</b> links weighted by who makes them</p></li>
                    <li><p><b>Betweenness:</b> how often an item lies between the others</p></li>
                    <li><p><b>Louvain:</b> groups with more links inside than outside</p></li>
                </ul>
                <p>These apply to different data sources (e.g., papers, people, web pages, etc).</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/social-network-analysis.jpg" alt="A network of links among people" style="height: auto; max-width: 100%; max-height: 90%;">
                <div class="footnote">Social Network Analysis Visualization - Martin Grandjean, CC BY-SA 3.0 <https://creativecommons.org/licenses/by-sa/3.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
