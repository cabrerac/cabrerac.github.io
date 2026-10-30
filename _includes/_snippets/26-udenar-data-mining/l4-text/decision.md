<!-- SLIDES: -->
<!-- Course piece (round 2, M8). The rule itself is in the shared combining-results.md (L3). The number in view comes from the executed L4 notebook, box-run/week-2/W2-L3-L4-VALUES.md (L4 section): 52 of 317, supports 0/1/2/3 = 209/56/44/8, HDBSCAN groups for the L3 support. -->

## Adding the Text Result

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 55%">
                <p><b>Three results now</b></p>
                <table class="table" style="font-size: 0.75em">
                    <thead>
                        <tr><th>Paper</th><th>Pattern</th><th>Group</th><th>Text</th><th>Supports</th><th>In view</th></tr>
                    </thead>
                    <tbody>
                        <tr><td>A</td><td>yes</td><td>yes</td><td>yes</td><td>3</td><td>yes</td></tr>
                        <tr><td>B</td><td>no</td><td>yes</td><td>yes</td><td>2</td><td>yes</td></tr>
                        <tr><td>C</td><td>yes</td><td>no</td><td>no</td><td>1</td><td>no</td></tr>
                        <tr><td>D</td><td>no</td><td>noise</td><td>yes</td><td>1</td><td>no, but listed for a look</td></tr>
                    </tbody>
                </table>
                <p>In view with at least 2 supports: 52 of 317 papers</p>


```python
SUPPORT_COLUMNS = ["has_pattern", "read_group", "text_says_read"]
```

            </div>
            <div class="column vertical-middle text-left" style="width: 45%">
                <p><b>What would change it</b></p>
                <ul>
                    <li>Another keyword list</li>
                    <li>Another marked set</li>
                    <li>Another target</li>
                    <li>Another threshold than 0.5</li>
                </ul>
                <p>The text result is one support, like the others. It does not decide alone.</p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
