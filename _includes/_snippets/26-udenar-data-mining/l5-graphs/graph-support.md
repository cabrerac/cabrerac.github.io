<!-- SLIDES: -->

## The Project

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 40%">
                <p><b>High PageRank in the graph</b></p>
                <p>A paper has links, is in the top quarter by PageRank among linked papers, and is not a hub.</p>
                <ul>
                    <li>The notebook prints how many linked papers meet the rule</li>
                    <li><b>Four results:</b> has_pattern, read_group, text_says_read and graph_support</li>
                    <li>MIN_SUPPORTS starts at 2 and can change. Each group sets and justifies this number in its project. The notebook prints the 0, 1, 2 and 3 or more counts</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 60%">

```python
# table: one row per paper, indexed by title
table["graph_support"] = table.index.isin(high_rank)
SUPPORT_COLUMNS = ["has_pattern", "read_group",
                   "text_says_read", "graph_support"]
table["supports"] = table[SUPPORT_COLUMNS].astype(int).sum(axis=1)
table["in_view"] = table["supports"] >= MIN_SUPPORTS
```

</div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
