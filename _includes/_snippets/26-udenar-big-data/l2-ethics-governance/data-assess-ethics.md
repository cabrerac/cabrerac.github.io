<!-- SLIDES: -->

## Data Assess

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p>After collecting the data (i.e., data access), we need to perform <b>a data assessment process to understand the data</b>, identify and mitigate data quality issues, uncover patterns, and gain insights.</p>
            </div>
        </div>
    </div>
</div>

## Data Assess

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 95%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/data-assess-pipeline.svg" alt="Data Assess Pipeline" style="height: 500px">
            </div>
        </div>
    </div>
</div>

## Data Cleaning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p>Process of <b>detecting and correcting (or removing)</b> corrupt or inaccurate records.</p>
            </div>
        </div>
    </div>
</div>

## Data Preprocessing

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p>Process of <b>transforming raw data into a format suitable for machine learning</b> while ensuring data quality and consistency.</p>
            </div>
        </div>
    </div>
</div>

## Data Augmentation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p>Process of <b>increasing the size and diversity</b> of our datasets.</p>
            </div>
        </div>
    </div>
</div>

## Feature Engineering

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p>Process of <b>creating, transforming, and selecting features in our data</b>, combining domain knowledge and creativity.</p>
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
                <p><b>Quasi-identifiers in GEIH</b></p>
                <ul>
                    <li>Department, age, sex, education, occupation combinations</li>
                    <li>List sensitive columns before any publishable aggregate</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">

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
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Disclosure preview</b></p>
                <ul>
                    <li>Count rows in small department × age cells</li>
                    <li>Alert when a cell has very few respondents</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">

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
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Join survey and map data</b></p>
                <ul>
                    <li>Overpass query for POIs by department</li>
                    <li>Compare with GEIH sample counts</li>
                    <li>State limits: coverage, consent, ecological fallacy</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">

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
            <div class="column vertical-middle text-left" style="width: 100%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/data-science-process.png" alt="Data science process" style="height: 420px">
            </div>
        </div>
    </div>
</div>

## Data Assess

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/big-data-pipeline-template.svg" alt="Big data pipeline" style="height: 420px">
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
