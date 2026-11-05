<!-- SLIDES: -->

## The Project

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p>The <b>text result</b> marks each paper whose abstract matches the question, and it joins the pattern and group results.</p>
            </div>
        </div>
    </div>
</div>

## The Project

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Three results now</b></p>
                <table class="table" style="font-size: 0.7em">
                                    <thead>
                                        <tr><th>Paper</th><th>Pattern</th><th>Group</th><th>Text</th><th>Results in favour</th><th>In view to start</th></tr>
                                    </thead>
                                    <tbody>
                                        <tr><td>A</td><td>yes</td><td>yes</td><td>yes</td><td>3</td><td>yes</td></tr>
                                        <tr><td>B</td><td>no</td><td>yes</td><td>yes</td><td>2</td><td>yes</td></tr>
                                        <tr><td>C</td><td>yes</td><td>no</td><td>no</td><td>1</td><td>no</td></tr>
                                        <tr><td>D</td><td>no</td><td>noise</td><td>yes</td><td>1</td><td>no, listed for a look</td></tr>
                                    </tbody>
                                </table>
                <p>Papers by number of results: 209 with 0, 56 with 1, 44 with 2, 8 with 3.</p>
                <p>MIN_SUPPORTS starts at 2, which puts 52 of 317 papers in view. Each group sets and justifies this number in its project.</p>
            </div>
        </div>
    </div>
</div>

## The Project

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>The text result</b></p>
                <ul>
                    <li><b>text_says_read:</b> what the text method says for each paper</li>
                    <li><b>marcas.csv:</b> the marks the group writes before any method runs</li>
                    <li>The week 2 group notebook, part 2, does the same on the department file</li>
                </ul>

```python
SUPPORT_COLUMNS = ["has_pattern", "read_group", "text_says_read"]
```

            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>What would change it</b></p>
                <ul>
                    <li>Another keyword list</li>
                    <li>Another marked set</li>
                    <li>Another target</li>
                    <li>Another threshold than 0.5</li>
                </ul>
                <p>The text result is one result, like the others. It does not decide alone.</p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
