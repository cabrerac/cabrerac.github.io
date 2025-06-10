<!-- SLIDES: -->

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

## Data Preprocessing

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

## Data Preprocessing

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Featuring Scaling</b></p>
                <p>Transforming numerical features to a common scale</p>
                <ul>
                    <li>All features contribute equally to the model</li>
                    <li>Algorithms converge faster</li>
                    <li>Features with larger scales do not dominate the model</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
            </div>
        </div>
    </div>
</div>

## Data Preprocessing

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Featuring Scaling</b></p>
                <p>Standarisation (Z-score): Centers data around 0 with unit variance</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
$$
z = (x - μ) / σ
$$
$x$: data point
$μ$: dataset mean
$σ$: dataset standard deviation
            </div>
        </div>
    </div>
</div>

## Data Preprocessing

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">

```python
scaler = StandardScaler()
cols = [col + '_st' for col in num_feat]
data[cols] = scaler.fit_transform(data[num_feat])
```
</div>
            <div class="column vertical-middle text-left" style="width: 50%">
$$
z = (x - μ) / σ
$$
$x$: data point
$μ$: dataset mean
$σ$: dataset standard deviation
            </div>
        </div>
    </div>
</div>

## Data Preprocessing

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Featuring Scaling</b></p>
                <p>Min-Max scaling: Scales data to a fixed range [0,1]</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
$$
x_{scaled} = (x - x_{min}) / (x_{max} - x_{min})
$$
$x$: data point
$x_{min}$: the minimum value of the feature
$x_{max}$: the maximum value of the feature
            </div>
        </div>
    </div>
</div>

## Data Preprocessing

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">

```python
scaler = MinMaxScaler()
cols = [col + '_minmax' for col in num_feat]
data[cols] = scaler.fit_transform(data[num_feat])
```
</div>
            <div class="column vertical-middle text-left" style="width: 50%">
$$
x_{scaled} = (x - x_{min}) / (x_{max} - x_{min})
$$
$x$: data point
$x_{min}$: the minimum value of the feature
$x_{max}$: the maximum value of the feature
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: --> 