<!-- SLIDES: -->

## Partitioning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Split the dataset by a key</b></p>
                <ul>
                    <li>Store each slice in its own folder named key=value</li>
                    <li>For GEIH we split by <b>year</b> and <b>month</b></li>
                    <li>The folder name is data, not just a label</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>A query for one month reads only that folder and skips the rest. This is called <b>partition pruning</b>.</p>
            </div>
        </div>
    </div>
</div>

## Partitioning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/partition-tree.svg" alt="Hive-style partition tree" style="height: 460px">
            </div>
        </div>
    </div>
</div>

## Partitioning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 40%">
                <p><b>In the notebook</b></p>
                <ul>
                    <li>One file per month under anio and mes</li>
                    <li>Written once, read many times</li>
                    <li><a href="https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-big-data/l3-storage.ipynb" target="_blank" rel="noopener noreferrer">Lecture 3 notebook</a></li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 60%">

```python
part_dir = PROCESSED_DIR / f"anio={y}" / f"mes={m:02d}"
part_file = part_dir / "part-000.parquet"

part_dir.mkdir(parents=True, exist_ok=True)
sample.to_parquet(part_file, index=False)
```

</div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
