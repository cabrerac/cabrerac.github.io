<!-- SLIDES: -->

## Access in This Course

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Household survey microdata</b></p>
                <ul>
                    <li>National integrated household survey from the statistics office</li>
                    <li>Monthly files with labour, demographics, housing, and income modules</li>
                    <li>Official basis for labour market statistics in Colombia</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Portal</b></p>
                <p><a href="https://microdatos.dane.gov.co/">microdatos.dane.gov.co</a></p>
            </div>
        </div>
    </div>
</div>

## Access in This Course

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>What the notebook automates</b></p>
                <ul>
                    <li>Build a direct download link from catalog and file ids</li>
                    <li>Download one month, then the rest of a survey year</li>
                    <li>Extract comma-separated files from each monthly archive</li>
                    <li>Write a manifest with time and size for each file</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">

```python
url = (
    "https://microdatos.dane.gov.co/index.php/"
    f"catalog/{catalog_id}/download/{file_id}"
)
```

</div>
        </div>
    </div>
</div>

## Access in This Course

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Several tables per month</b></p>
                <ul>
                    <li>Labour, general characteristics, housing, and other modules ship as separate files</li>
                    <li>Column names follow survey question codes documented on the portal</li>
                    <li>Lecture 2 joins tables when a variable lives outside the labour file</li>
                </ul>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
