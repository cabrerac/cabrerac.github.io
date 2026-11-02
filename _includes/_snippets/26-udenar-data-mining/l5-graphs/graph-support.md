<!-- SLIDES: -->
<!-- 2 Nov 2026: the visible note "Numbers: box run on rebuilt data." was removed from these slides (critic brief r1, S4). The source notes stay in these comments. -->

<!-- Numbers: slide code on rebuilt data, box run (week-3/feasibility/r3/w3decks_n2v_pagerank.json, critic l5_slide_code.json, sorted(adj)). Round 4: the three former box-run markers filled from the notebooks maker's box run (sorted(adj), seeds 7 to 9, workers=1, betweenness rounded to 9 dp). -->

## The Graph Support

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 45%">
                <p><b>A bridge in the graph</b></p>
                <p>A bridge: top quarter by betweenness among connected papers, and not a hub.</p>
                <p>49 bridges among the 196 connected papers, 15% of the 318.</p>
                <p>Four supports: has_pattern, read_group, text_says_read and graph_support.</p>
                <p>Papers in view with at least two: 69.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 55%">


```python
# table: one row per paper, indexed by title
table["graph_support"] = table.index.isin(bridges)   # top quarter, not a hub
SUPPORT_COLUMNS = ["has_pattern", "read_group", "text_says_read", "graph_support"]
table["supports"] = table[SUPPORT_COLUMNS].astype(int).sum(axis=1)
table["in_view"] = table["supports"] >= MIN_SUPPORTS
print(table["graph_support"].sum(), "bridges,", table["in_view"].sum(), "in view")
```

</div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
