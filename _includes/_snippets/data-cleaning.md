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

## Data Cleaning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Missing Values</b></p>
                <p>Missing data points in the dataset</p>
                <ul>
                    <li>Data collection errors</li>
                    <li>System failures</li>
                    <li>Information not available</li>
                    <li>Data entry mistakes</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
            </div>
        </div>
    </div>
</div>

## Data Cleaning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Missing Values</b></p>
                <p>Missing data points in the dataset</p>
                <ul>
                    <li>Data collection errors</li>
                    <li>System failures</li>
                    <li>Information not available</li>
                    <li>Data entry mistakes</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/missing_values.png" alt="Missing Values" style="height: 500px">
            </div>
        </div>
    </div>
</div>

## Data Cleaning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Missing Values</b></p>
                <p>Missing data points in the dataset</p>
                <ul>
                    <li>Deletion: Remove rows or columns with missing values</li>
                    <li>Imputation: Fill missing values with estimated values</li>
                    <li>Advanced techniques: Use machine learning models to predict missing values</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/missing_values.png" alt="Missing Values" style="height: 500px">
            </div>
        </div>
    </div>
</div>

## Data Cleaning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">

```python
from sklearn.linear_model import LinearRegression
features_for_age = ['Pclass', 'SibSp', 'Parch', 'Fare']
X_train = titanic_data.dropna(subset=['Age'])[features_for_age]
y_train = titanic_data.dropna(subset=['Age'])['Age']
reg_imputer = LinearRegression()
reg_imputer.fit(X_train, y_train)
X_missing = titanic_data[titanic_data['Age'].isnull()][features_for_age]
predicted_ages = reg_imputer.predict(X_missing)
titanic_data_reg = titanic_data.copy()
titanic_data_reg.loc[titanic_data_reg['Age'].isnull(), 'Age'] = predicted_ages
titanic_data['Age_Regression'] = titanic_data_reg['Age']
```
</div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/missing_values.png" alt="Missing Values" style="height: 500px">
            </div>
        </div>
    </div>
</div>

## Data Cleaning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Outliers</b></p>
                <p>Data points that significantly deviate from the rest of the data</p>
                <ul>
                    <li>Measurement errors</li>
                    <li>Data entry mistakes</li>
                    <li>Rare but valid observations</li>
                    <li>System malfunctions</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Data Cleaning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/outliers.png" alt="Outliers" style="height: 500px">
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Outliers</b></p>
                <p>Data points that significantly deviate from the rest of the data</p>
                <ul>
                    <li>Measurement errors</li>
                    <li>Data entry mistakes</li>
                    <li>Rare but valid observations</li>
                    <li>System malfunctions</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Data Cleaning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/outliers.png" alt="Outliers" style="height: 500px">
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Outliers</b></p>
                <p>Data points that significantly deviate from the rest of the data</p>
                <ul>
                    <li>Capping: Limit values to a range</li>
                    <li>Log Transformation: Reduce the impact of extreme values</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Data Cleaning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/outliers.png" alt="Outliers" style="height: 500px">
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">

```python
def cap_outliers(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    df[column + '_capped'] = df[column].clip(lower=lower_bound, upper=upper_bound)
    return df
```
</div>
        </div>
    </div>
</div>

<!-- end SLIDES: --> 