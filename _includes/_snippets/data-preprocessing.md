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
                <p>Process of transforming raw data into a format suitable for machine learning while ensuring data quality and consistency.</p>
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
standardized_columns = [col + '_standardized' for col in numerical_features]
titanic_data[standardized_columns] = scaler.fit_transform(titanic_data[numerical_features])
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
minmax_scaler = MinMaxScaler()
minmax_columns = [col + '_minmax' for col in numerical_features]
titanic_data[minmax_columns] = minmax_scaler.fit_transform(titanic_data[numerical_features])
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