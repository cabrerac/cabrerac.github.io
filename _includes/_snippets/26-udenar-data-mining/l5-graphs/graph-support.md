<!-- SLIDES: -->

## The Project

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 40%">
                <p><b>High PageRank in the graph</b></p>
                <p>A paper has links, is in the top quarter by PageRank among linked papers, and is not a hub.</p>
                <ul>
                    <li>The list keeps at most 30 of those papers, the highest PageRank first</li>
                    <li>A hub is a warning, not a place on the list</li>
                    <li>An isolated paper gets no graph result</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 60%">

```python
# table: one row per paper, indexed by title
table["graph_support"] = table.index.isin(high_rank)
kept = pd.Series(rank).loc[high_rank].sort_values(ascending=False).head(MAX_PAPERS).index
table["en_lista"] = table.index.isin(kept)
```

</div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
