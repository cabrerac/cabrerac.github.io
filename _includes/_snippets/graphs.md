<!-- SLIDES: -->

## Graphs

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Euler and the bridges of Königsberg <a href="https://scholarlycommons.pacific.edu/euler-works/53/" target="_blank" rel="noopener noreferrer">(Euler, 1736)</a></b></p>
                <p>Can a walk cross each of the seven bridges exactly once?</p>
                <ul>
                    <li>Euler kept only land masses and bridges, nodes and edges.</li>
                    <li>The answer depends on each land mass's degree.</li>
                    <li>No such walk exists. Graph theory starts here.</li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/konigsberg-bridges.png" alt="The seven bridges of Königsberg" style="height: 300px">
                <div class="footnote">Konigsberg bridges - Bogdan Giuşcă, CC BY-SA 3.0 <https://creativecommons.org/licenses/by-sa/3.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Graphs

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 55%">
                <p><b>Graphs of people</b></p>
                                <ul>
                                    <li><b>1934:</b> Moreno draws sociograms, who chooses whom in a group <a href="https://archive.org/details/whoshallsurvivef0000jlmo" target="_blank" rel="noopener noreferrer">(Moreno, 1934)</a></li>
                                    <li><b>1977:</b> Freeman measures how often a person lies between others, betweenness <a href="https://doi.org/10.2307/3033543" target="_blank" rel="noopener noreferrer">(Freeman, 1977)</a></li>
                                    <li><b>2001:</b> Brandes makes betweenness fast enough for large graphs <a href="https://doi.org/10.1080/0022250X.2001.9990249" target="_blank" rel="noopener noreferrer">(Brandes, 2001)</a></li>
                                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 45%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/graph-betweenness.svg" alt="Graph coloured by betweenness" style="height: 380px">
                <div class="footnote">Graph betweenness - Claudio Rocchini, CC BY 2.5 <https://creativecommons.org/licenses/by/2.5>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Graphs

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 55%">
                <p><b>From citations to links</b></p>
                <p>Papers cite papers and web pages link to web pages.</p>
                <ul>
                    <li>Citation indexes list who cites whom</li>
                                        <li><b>1998:</b> Brin and Page rank web pages by the links they get, PageRank <a href="https://doi.org/10.1016/S0169-7552(98)00110-X" target="_blank" rel="noopener noreferrer">(Brin and Page, 1998)</a> <a href="https://web.archive.org/web/20241231011600/http://ilpubs.stanford.edu:8090/422/" target="_blank" rel="noopener noreferrer">(Page et al., 1998)</a></li>
                    <li><b>2014:</b> DeepWalk turns random walks into sentences for word2vec <a href="https://doi.org/10.1145/2623330.2623732" target="_blank" rel="noopener noreferrer">(Perozzi et al., 2014)</a></li>
                    <li><b>2016:</b> node2vec makes the walks biased, closer or farther <a href="https://doi.org/10.1145/2939672.2939754" target="_blank" rel="noopener noreferrer">(Grover and Leskovec, 2016)</a></li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 45%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/pagerank-example.svg" alt="PageRank example" style="height: 360px">
                <div class="footnote">PageRanks Example - 345Kai and Stannered, Public domain, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Graphs

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Items and the links among them</b></p>
                <p>A graph $G = (V, E)$ has nodes $V$ and edges $E$.</p>
                <ul>
                    <li><p><b>Directed:</b> $u \to v$, item $u$ links to item $v$.</p></li>
                    <li><p><b>Undirected:</b> $u - v$, the two items are linked, whatever the direction.</p></li>
                </ul>
                <p>Not what an item says, but where it sits among the others.</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/social-network-analysis.jpg" alt="A network of links among people" style="height: 380px">
                <div class="footnote">Social Network Analysis Visualization - Martin Grandjean, CC BY-SA 3.0 <https://creativecommons.org/licenses/by-sa/3.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Graphs

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Words for a graph</b></p>
                <ul>
                    <li><p><b>Neighbours:</b> $N(v)$, the nodes linked to $v$.</p></li>
                    <li><p><b>Degree:</b> $\deg(v) = |N(v)|$, how many neighbours.</p></li>
                    <li><b>Path:</b> a chain of edges from one node to another.</li>
                    <li><b>Shortest path:</b> a path with the fewest edges.</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Graphs

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Parts of a graph</b></p>
                <ul>
                    <li><b>Component:</b> nodes that can all reach each other.</li>
                    <li><b>Largest component:</b> the biggest of them.</li>
                    <li><b>Isolated node:</b> degree 0, no link to any other item in the set.</li>
                </ul>
                <p>Isolated means no link inside this set, not unimportant.</p>
            </div>
        </div>
    </div>
</div>

## Graphs

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 45%">
                <p><b>From a table to a graph</b></p>
                <p>Each row is an item, with a column that lists the items it links to.</p>
                </div>
            <div class="column vertical-middle text-left" style="width: 55%">

```python
df = df.drop_duplicates("title")        # each row: an item and the items it links to
titles = list(df["title"])
title_set = set(titles)
links_out = {t: set() for t in titles}          # directed, for PageRank
for title, links in zip(df["title"], df["links"]):
    for target in str(links).split("|"):
        target = target.strip()
        if target in title_set and target != title:
            links_out[title].add(target)        # links inside the set only

neighbours = {t: set() for t in titles}         # undirected, for the rest
for a, targets in links_out.items():
    for b in targets:
        neighbours[a].add(b)
        neighbours[b].add(a)
```

</div>
        </div>
    </div>
</div>

## Graphs

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>What a graph adds</b></p>
                <p>Many methods look at each item alone, by its own attributes or words.</p>
                <p>A graph looks at the links among items.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Three ways to read a place</b></p>
                <ul>
                    <li><b>Degree and PageRank:</b> how many links, and from whom</li>
                    <li><b>Betweenness:</b> how often an item lies between others</li>
                    <li><b>node2vec:</b> which items share a neighbourhood</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Graphs

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p>A <b>graph</b> is a set of items, called nodes, and the links among them, called edges.</p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
