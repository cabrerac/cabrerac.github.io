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
                <p>Here the key is <b>dpto</b> and the value is the survey weight.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 58%">

```python
def map_partition(path):
    df = read(path, ["dpto", "actividad", "peso"])
    emp = df[df.actividad == 1]          # derive: employed
    return zip(emp.dpto, emp.peso)       # emit (key, value)

def reduce(key, values):                 # one group at a time
    return {"conteo": len(values),
            "suma": sum(values)}
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
                <p>MapReduce is the <b>mental model</b>, but writing it by hand is verbose. Modern <b>query engines</b> run the same map, group, and reduce for us, and optimise it. We meet three: <b>pandas</b>, <b>DuckDB</b>, and <b>Polars</b>.</p>
            </div>
        </div>
    </div>
</div>

## Query Engines

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 42%">
                <p><b>pandas: the familiar one</b></p>
                <ul>
                    <li>Loads the data into memory as a DataFrame</li>
                    <li><b>filter</b> then <b>groupby(...).agg(...)</b></li>
                    <li>Great up to a few million rows on one machine</li>
                </ul>
                <p>Same map, group, reduce, now in one expression.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 58%">

```python
df = pd.read_parquet(PARQUET_2024)
df["ocupado"] = df["actividad"] == 1     # derive
(df[df["ocupado"]]                       # filter
   .groupby("dpto")                      # group by key
   .agg(conteo=("ocupado", "count"),
        suma=("factor_expansion", "sum")))
```

</div>
        </div>
    </div>
</div>

## Query Engines

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 42%">
                <p><b>DuckDB: SQL on files</b></p>
                <ul>
                    <li>An analytical database <b>inside the notebook</b>, no server</li>
                    <li>Reads Parquet directly and queries with <b>SQL</b></li>
                    <li><b>WHERE</b> filters, <b>GROUP BY</b> is the reduce</li>
                </ul>
                <p>SQL is the lingua franca of data, the same idea as relational databases in lecture 3.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 58%">

```sql
SELECT
    dpto,
    COUNT(*)              AS conteo,
    SUM(factor_expansion) AS suma
FROM read_parquet('geih-spine/**/*.parquet')
WHERE actividad = 1          -- filter: employed
GROUP BY dpto                -- the reduce
ORDER BY dpto;
```

</div>
        </div>
    </div>
</div>

## Query Engines

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 42%">
                <p><b>Polars: lazy and parallel</b></p>
                <ul>
                    <li>Built for speed, runs on all CPU cores</li>
                    <li><b>Lazy:</b> it builds a plan and waits</li>
                    <li>Nothing runs until <b>collect()</b></li>
                </ul>
                <p>Lazy evaluation lets the engine optimise the whole query before reading a single row.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 58%">

```python
(pl.scan_parquet("geih-spine/**/*.parquet")  # lazy, reads nothing yet
   .filter(pl.col("actividad") == 1)          # filter
   .group_by("dpto")                          # group by key
   .agg(pl.len().alias("conteo"),
        pl.col("factor_expansion").sum())
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
                <p><b>One question, four engines, one answer.</b> MapReduce shows the pattern; pandas, DuckDB, and Polars implement it for us. Which is fastest depends on the data and the machine, so we <b>measure</b> it in the notebook, not on a slide.</p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
