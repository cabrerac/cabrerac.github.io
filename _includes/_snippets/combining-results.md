<!-- SLIDES: -->

## Combining Results

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p><b>Combining results</b> shows, for each item, which of the different methods support it.</p>
            </div>
        </div>
    </div>
</div>

## Combining Results

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Each result is a reason</b></p>
                <p>Each method sees the items in its own way, and each one is weak alone.</p>
                <p>The list shows which results support each item. An item can stay with one result or none, if you explain why it is on the list.</p>
                <p>Items left out are not deleted, they wait for another result or a reason.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>What would change it</b></p>
                <p>Another setting of any method.</p>
                <p>Another reading of a result.</p>
                <p>A new result that supports or drops an item.</p>
                <p>We write these down next to the result, before anyone uses it.</p>
            </div>
        </div>
    </div>
</div>

## Combining Results

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 45%">
                <p><b>One column per result</b></p>
                <table class="table" style="font-size: 0.7em">
                    <thead>
                        <tr><th>Item</th><th>Result A</th><th>Result B</th><th>Results in favour</th><th>Starting point</th></tr>
                    </thead>
                    <tbody>
                        <tr><td>1</td><td>yes</td><td>yes</td><td>2</td><td>in</td></tr>
                        <tr><td>2</td><td>yes</td><td>no</td><td>1</td><td>out</td></tr>
                        <tr><td>3</td><td>no</td><td>yes</td><td>1</td><td>out</td></tr>
                        <tr><td>4</td><td>no</td><td>no</td><td>0</td><td>out, not deleted</td></tr>
                    </tbody>
                </table>
                <p>A new result adds a column. The count is only a starting point. You can keep or drop any item if you say why.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 55%">


```python
SUPPORT_COLUMNS = ["result_a", "result_b"]   # one per result

table["supports"] = table[SUPPORT_COLUMNS].astype(int).sum(axis=1)
# a starting point, change it with a reason
table["in_view"] = table["supports"] >= MIN_SUPPORTS
print(table["in_view"].sum(), "items in view")
```

            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
