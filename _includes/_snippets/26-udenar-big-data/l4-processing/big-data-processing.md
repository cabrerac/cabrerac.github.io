<!-- SLIDES: -->

## MapReduce

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>A recipe for many machines (2004)</b></p>
                <ul>
                    <li>Google needed to process the whole web</li>
                    <li>The trick: express work as <b>map</b> then <b>reduce</b></li>
                    <li>The system handles splitting, failures, and machines</li>
                </ul>
                <p>You write two small functions. The framework runs them across a cluster.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>"MapReduce is a programming model and an associated implementation for processing and generating large data sets." <a href="https://doi.org/10.1145/1327452.1327492" target="_blank" rel="noopener noreferrer">(Dean &amp; Ghemawat, 2008)</a></p>
                <p>Its open-source version, <b>Hadoop MapReduce</b>, started the big data tooling era.</p>
            </div>
        </div>
    </div>
</div>

## MapReduce

<div class="rows" style="height: 100%">
    <div class="row" style="height: 14%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p><b>Map, then group by key, then reduce</b></p>
            </div>
        </div>
    </div>
    <div class="row" style="height: 86%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/mapreduce-dataflow.svg" alt="MapReduce dataflow: input, map, shuffle, reduce" style="height: 100%">
            </div>
        </div>
    </div>
</div>

## MapReduce

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 42%">
                <p><b>Three phases</b></p>
                <ul>
                    <li><b>Map:</b> emit a key-value pair per record</li>
                    <li><b>Shuffle:</b> group all values by key</li>
                    <li><b>Reduce:</b> aggregate each group</li>
                </ul>
                <p>Here the key is <b>department</b> and the value is the survey weight.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 58%">

```python
def map_partition(path):
    df = read(path, ["department", "activity", "weight"])
    emp = df[df.activity == 1]            # derive: employed
    return zip(emp.department, emp.weight)  # emit (key, value)

def reduce(key, values):                  # one group at a time
    return {"count": len(values),
            "sum": sum(values)}
```

</div>
        </div>
    </div>
</div>

## MapReduce

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p>MapReduce is the <b>mental model</b>, but writing it by hand is verbose. Modern <b>query engines</b> run the same map, group, and reduce for us, and also handle everyday data operations. We meet three: <b>DuckDB</b>, <b>pandas</b>, and <b>Polars</b>.</p>
            </div>
        </div>
    </div>
</div>

## Query Engines

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>CRUD: the four basic operations</b></p>
                <ul>
                    <li><b>Create:</b> add new rows</li>
                    <li><b>Read:</b> select and filter rows</li>
                    <li><b>Update:</b> change values in place</li>
                    <li><b>Delete:</b> remove rows</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Analysis adds two more</b></p>
                <ul>
                    <li><b>Group by</b> a key, such as department</li>
                    <li><b>Aggregate</b> each group: count, sum, average</li>
                </ul>
                <p>Every engine offers all of these. Only the <b>syntax</b> changes.</p>
            </div>
        </div>
    </div>
</div>

## Query Engines

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 38%">
                <p><b>DuckDB: CRUD in SQL</b></p>
                <ul>
                    <li>An analytical database <b>inside the notebook</b>, no server</li>
                    <li>SQL is the standard language of databases</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 62%">

```sql
INSERT INTO people VALUES (101, 5, 1, 1.2);  -- Create
SELECT * FROM people WHERE department = 5;   -- Read
UPDATE people SET activity = 2 WHERE id = 101;  -- Update
DELETE FROM people WHERE weight IS NULL;     -- Delete
```

</div>
        </div>
    </div>
</div>

## Query Engines

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 38%">
                <p><b>DuckDB: group by and aggregate</b></p>
                <ul>
                    <li><b>WHERE</b> filters rows</li>
                    <li><b>GROUP BY</b> is the reduce</li>
                    <li>Reads Parquet files directly</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 62%">

```sql
SELECT
    department,
    COUNT(*)    AS employed,
    SUM(weight) AS weighted_sum
FROM read_parquet('geih-spine/**/*.parquet')
WHERE activity = 1          -- filter: employed
GROUP BY department         -- the reduce
ORDER BY department;
```

</div>
        </div>
    </div>
</div>

## Query Engines

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 38%">
                <p><b>pandas: CRUD in memory</b></p>
                <ul>
                    <li>The familiar DataFrame, loaded in memory</li>
                    <li>Index and boolean masks select rows</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 62%">

```python
df.loc[len(df)] = {"id": 101, "department": 5,
                   "activity": 1, "weight": 1.2}  # Create
df[df["department"] == 5]                         # Read
df.loc[df["id"] == 101, "activity"] = 2           # Update
df = df[df["weight"].notna()]                     # Delete
```

</div>
        </div>
    </div>
</div>

## Query Engines

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 38%">
                <p><b>pandas: group by and aggregate</b></p>
                <ul>
                    <li><b>filter</b> with a boolean mask</li>
                    <li><b>groupby(...).agg(...)</b> is the reduce</li>
                    <li>Great up to a few million rows</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 62%">

```python
df["employed"] = df["activity"] == 1       # derive
(df[df["employed"]]                        # filter
   .groupby("department")                  # group by key
   .agg(employed=("employed", "count"),
        weighted_sum=("weight", "sum")))
```

</div>
        </div>
    </div>
</div>

## Query Engines

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 38%">
                <p><b>Polars: CRUD, lazy and parallel</b></p>
                <ul>
                    <li>Built for speed, uses all CPU cores</li>
                    <li>Columns are added with <b>with_columns</b></li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 62%">

```python
df = pl.DataFrame({"id": [101], "department": [5],
                   "activity": [1], "weight": [1.2]})  # Create
df.filter(pl.col("department") == 5)                   # Read
df = df.with_columns(employed=pl.col("activity") == 1) # Update
df = df.filter(pl.col("weight").is_not_null())         # Delete
```

</div>
        </div>
    </div>
</div>

## Query Engines

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 38%">
                <p><b>Polars: group by and aggregate</b></p>
                <ul>
                    <li><b>Lazy:</b> it builds a plan and waits</li>
                    <li>Nothing runs until <b>collect()</b></li>
                    <li>The engine optimises the whole query first</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 62%">

```python
(pl.scan_parquet("geih-spine/**/*.parquet")  # lazy, reads nothing yet
   .filter(pl.col("activity") == 1)           # filter
   .group_by("department")                    # group by key
   .agg(pl.len().alias("employed"),
        pl.col("weight").sum().alias("weighted_sum"))
   .collect())                                # run the plan now
```

</div>
        </div>
    </div>
</div>

## Query Engines

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>One question, four engines, one answer.</b> MapReduce shows the pattern. Pandas, DuckDB, and Polars implement it for us. Which is fastest depends on the data and the machine, so we <b>measure</b> it in the notebook, not on a slide.</p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
