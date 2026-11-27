<!-- SLIDES: -->

## Louvain

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

## Louvain

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p><b>Louvain</b> splits a graph into communities, groups of items with more links inside than outside, by raising modularity one move at a time.</p>
            </div>
        </div>
    </div>
</div>

## Louvain

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Modularity</b> compares the links inside each group with the links a random graph with the same degrees would put there.</p>
                <br>
$$
Q = \sum_{c} \left[ \frac{L_c}{m} - \left( \frac{d_c}{2m} \right)^2 \right]
$$
                <br>
                <p><b>$m$</b> is the number of links. <b>$L_c$</b> are the links inside group $c$. <b>$d_c$</b> is the sum of the degrees in group $c$</p>
                <p>$Q$ near 0 means no more links inside than chance. Higher is a clearer split.</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/louvain-2.svg" alt="Two communities in the toy graph" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
</div>

## Louvain

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Worked example.</b> Two groups, A B C and D E F, joined only through X. $m = 8$.</p>
                <ul>
                    <li><p><b>A B C X:</b> 4 links inside, degrees 2 + 2 + 3 + 2 = 9</p></li>
                    <li><p><b>D E F:</b> 3 links inside, degrees 3 + 2 + 2 = 7</p></li>
                </ul>
$$
Q = \frac{4}{8} - \left(\frac{9}{16}\right)^2 + \frac{3}{8} - \left(\frac{7}{16}\right)^2 = 0.367
$$
                <p>All seven in one group give $Q = 0$.</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/louvain-2.svg" alt="Two communities in the toy graph" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
</div>

## Louvain

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Two steps, repeated</b> (<a href="https://doi.org/10.1088/1742-5468/2008/10/P10008" target="_blank" rel="noopener noreferrer">Blondel et al., 2008</a>)</p>
                <ul>
                    <li><p><b>Start:</b> every node is its own community</p></li>
                    <li><p><b>Move:</b> put each node in the neighbouring community that raises $Q$ most. Stop when no move raises it</p></li>
                    <li><p><b>Aggregate:</b> each community becomes one node, with its inside links as a loop, then move again</p></li>
                    <li><p><b>End:</b> when a pass changes nothing</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/louvain-1.svg" alt="Every node in its own community" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
</div>

## Louvain

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Two steps, repeated</b> (<a href="https://doi.org/10.1088/1742-5468/2008/10/P10008" target="_blank" rel="noopener noreferrer">Blondel et al., 2008</a>)</p>
                <ul>
                    <li><p><b>Start:</b> every node is its own community</p></li>
                    <li><p><b>Move:</b> put each node in the neighbouring community that raises $Q$ most. Stop when no move raises it</p></li>
                    <li><p><b>Aggregate:</b> each community becomes one node, with its inside links as a loop, then move again</p></li>
                    <li><p><b>End:</b> when a pass changes nothing</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/louvain-2.svg" alt="Two communities in the toy graph" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
</div>

## Louvain

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Two steps, repeated</b> (<a href="https://doi.org/10.1088/1742-5468/2008/10/P10008" target="_blank" rel="noopener noreferrer">Blondel et al., 2008</a>)</p>
                <ul>
                    <li><p><b>Start:</b> every node is its own community</p></li>
                    <li><p><b>Move:</b> put each node in the neighbouring community that raises $Q$ most. Stop when no move raises it</p></li>
                    <li><p><b>Aggregate:</b> each community becomes one node, with its inside links as a loop, then move again</p></li>
                    <li><p><b>End:</b> when a pass changes nothing</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/louvain-3.svg" alt="Each community becomes one node" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
</div>

## Louvain

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Set before the results</b></p>
                <ul>
                    <li><p><b>Resolution:</b> above 1 gives more and smaller communities, below 1 fewer and larger ones</p></li>
                    <li><p><b>Seed:</b> the order in which nodes are tried</p></li>
                </ul>
                <p><b>Limits</b></p>
                <ul>
                    <li><p>Another seed can move a few nodes</p></li>
                    <li><p>Very small communities can stay hidden inside larger ones</p></li>
                    <li><p>A community says the items are linked, not why. We read the items to name it</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/louvain-2.svg" alt="Two communities in the toy graph" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
</div>

## Louvain

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 47.5%; font-size: 0.85em">

```text
every node in its own community
repeat
    repeat until no node moves
        for each node, in seed order
            try each neighbouring community
            move to the one that raises Q most
    each community becomes one node
until a pass changes nothing
report the communities and Q
```
</div>
            <div class="column vertical-middle text-left" style="width: 4%"></div>
            <div class="column vertical-middle text-center" style="width: 47.5%; height: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/louvain-3.svg" alt="Each community becomes one node" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
</div>

## Louvain

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 47.5%">
                <p><b>Python usage:</b> networkx</p>
                <p>Communities of the seven items, and their modularity</p>
                <ul>
                    <li><p><b>louvain_communities:</b> a list of sets of nodes, resolution 1 by default</p></li>
                    <li><p><b>modularity:</b> $Q$ of those communities on the same graph</p></li>
                    <li><p><b>Returns:</b> {A, B, C, X} and {D, E, F}, with $Q = 0.367$</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 5%"></div>
            <div class="column vertical-middle text-left" style="width: 47.5%; font-size: 0.85em">

```python
import networkx as nx

graph = nx.Graph()
graph.add_edges_from([("A", "B"), ("A", "C"),
                      ("B", "C"), ("C", "X"),
                      ("X", "D"), ("D", "E"),
                      ("D", "F"), ("E", "F")])
groups = nx.community.louvain_communities(
    graph, seed=7)
q = nx.community.modularity(graph, groups)
print(groups, round(q, 3))
```
</div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
