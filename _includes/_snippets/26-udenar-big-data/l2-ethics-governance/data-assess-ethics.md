<!-- SLIDES: -->

## Data Assess

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/data-science-process.png" alt="Data science process" style="height: 480px">
            </div>
        </div>
    </div>
</div>

## Data Assess

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Data quality carries ethical requirements</b></p>
                <ul>
                    <li>Missing, biased, or mis-labelled data can harm groups silently</li>
                    <li>Assess is where we inspect structure, coverage, and risk before analytics</li>
                    <li>Veracity is a Big Data dimension with direct policy consequences</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/data-assess-pipeline.svg" alt="Data assess pipeline" style="height: 420px">
            </div>
        </div>
    </div>
</div>

## Data Assess

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Data cleaning (assess step)</b></p>
                <p>Detect and correct corrupt or inaccurate records before you trust aggregates.</p>
                <ul>
                    <li>Missing values and definition changes across years</li>
                    <li>Outliers that distort small regions</li>
                    <li>Documentation of every transform for accountability</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/b/bb/Data_visualization_icon.svg/280px-Data_visualization_icon.svg.png" alt="Data quality" style="height: 260px">
                <div class="footnote">Data visualization icon, CC BY-SA 4.0, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Data Assess

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 30%">
                <p><b>Quasi-identifiers in GEIH</b></p>
                <ul>
                    <li>Department, age, sex, education, occupation combinations</li>
                    <li>List sensitive columns before any publishable aggregate</li>
                    <li><a href="https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-big-data/l2-ethics-governance.ipynb" target="_blank" rel="noopener noreferrer">Lecture 2 notebook</a>, Part 2</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 70%">

```python
CANDIDATOS_QI = ["DPTO", "MPIO", "AREA", "P6040", "P6240", "P6160"]
presentes = [c for c in CANDIDATOS_QI if c in df.columns]
tabla_qi = pd.DataFrame({
    "columna": presentes,
    "valores_unicos": [df[c].nunique() for c in presentes],
})
```

</div>
        </div>
    </div>
</div>

## Data Assess

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 30%">
                <p><b>Disclosure preview</b></p>
                <ul>
                    <li>Count rows in small department × age cells</li>
                    <li>Alert when a cell has very few respondents</li>
                    <li>Part 3 in the notebook</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 70%">

```python
work = df[["DPTO", "P6040"]].copy()
work["banda_edad"] = pd.cut(work["P6040"], bins=[0, 17, 29, 44, 59, 120])
celdas = work.groupby(["DPTO", "banda_edad"], observed=True).size()
celda_min = celdas.min()
```

</div>
        </div>
    </div>
</div>

## Data Assess

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 30%">
                <p><b>Join survey and map data</b></p>
                <ul>
                    <li>Overpass query for POIs by department</li>
                    <li>Compare with GEIH sample counts</li>
                    <li>State limits: coverage, consent, ecological fallacy</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 70%">

```python
query = """
[out:json][timeout:60];
area(3601380130)->.a;
node["amenity"="school"](area.a);
out;
"""
poi_count = len(overpass_post(query).json()["elements"])
```

</div>
        </div>
    </div>
</div>

## Data Assess

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/data-science-process.png" alt="Data science process" style="height: 420px">
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/big-data-pipeline-template.svg" alt="Big data pipeline" style="height: 420px">
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
