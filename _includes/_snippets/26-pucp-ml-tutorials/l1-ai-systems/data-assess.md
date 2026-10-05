<!-- SLIDES: -->

## Data Assess

<div class="rows" style="height: 100%">
    <div class="row" style="height: 75%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img src="{{ site.url }}/assets/media/images/data-science-process.png" alt="Data Science Process" style="height: 450px">
            </div>
        </div>
    </div>
    <div class="row" style="height: 25%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p>With the data in hand we move to <b>assess</b>: deciding whether it is fit for the question.</p>
            </div>
        </div>
    </div>
</div>

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
    <div class="row" style="height: 70%">
        <div class="columns" style="width: 95%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/data-assess-pipeline.svg" alt="Data Assess Pipeline" style="height: 380px">
            </div>
        </div>
    </div>
    <div class="row" style="height: 30%">
        <div class="columns" style="width: 95%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p>Four families of methods sit inside this stage: <b>cleaning</b>, <b>preprocessing</b>, <b>augmentation</b>, and <b>feature engineering</b>.</p>
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
                <img src="{{ site.url }}/assets/media/images/missing_values.png" alt="Missing Values" style="height: 450px">
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
                <ul>
                    <li><b>Deletion</b>: remove rows or columns with missing values</li>
                    <li><b>Imputation</b>: fill missing values with estimated values</li>
                    <li><b>Advanced techniques</b>: use machine learning models to predict missing values</li>
                </ul>
                <p>A missing value is not always empty. It can also be a placeholder that looks like data.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">

```python
features = ['Pclass', 'SibSp', 'Parch', 'Fare']
known = titanic.dropna(subset=['Age'])
imputer = LinearRegression()
imputer.fit(known[features], known['Age'])

unknown = titanic['Age'].isnull()
titanic.loc[unknown, 'Age'] = imputer.predict(
    titanic[unknown][features]
)
```

</div>
        </div>
    </div>
</div>

## Data Cleaning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/outliers.png" alt="Outliers" style="height: 450px">
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Outliers</b></p>
                <p>Data points that significantly deviate from the rest of the data: measurement errors, data entry mistakes, system malfunctions, or <b>rare but valid observations</b></p>
                <ul>
                    <li><b>Capping</b>: limit values to a range</li>
                    <li><b>Log transformation</b>: reduce the impact of extreme values</li>
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
                <img src="{{ site.url }}/assets/media/images/outliers.png" alt="Outliers" style="height: 450px">
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">

```python
def cap_outliers(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    df[column + '_capped'] = df[column].clip(
        lower=lower, upper=upper
    )
    return df
```

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

## Data Preprocessing

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Feature Scaling</b></p>
                <p>Transforming numerical features to a common scale</p>
                <ul>
                    <li>All features contribute equally to the model</li>
                    <li>Algorithms converge faster</li>
                    <li>Features with larger scales do not dominate the model</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Standardisation (Z-score)</b> centres data around 0 with unit variance</p>

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
                <p><b>Min-Max scaling</b> maps data to a fixed range [0,1]</p>

$$
x_{scaled} = (x - x_{min}) / (x_{max} - x_{min})
$$

$x_{min}$: the minimum value of the feature
$x_{max}$: the maximum value of the feature
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">

```python
scaler = StandardScaler()
cols = [col + '_st' for col in num_feat]
data[cols] = scaler.fit_transform(data[num_feat])

scaler = MinMaxScaler()
cols = [col + '_minmax' for col in num_feat]
data[cols] = scaler.fit_transform(data[num_feat])
```

</div>
        </div>
    </div>
</div>

## Data Augmentation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>Process of <b>increasing the size and diversity</b> of our datasets.</p>
                <p>More <b>diversity</b> makes models more robust</p>
                <ul>
                    <li>Adding controlled noise</li>
                    <li>Random rotations</li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/augmented.png" alt="Data Augmentation" style="height: 420px">
            </div>
        </div>
    </div>
</div>

## Data Augmentation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>More <b>size</b> improves generalisation</p>
                <ul>
                    <li>Interpolating between existing data points</li>
                    <li>Applying domain-specific transformations</li>
                    <li>Generating synthetic data using GANs</li>
                </ul>
                <p><b>SMOTE</b> interpolates between a point and its k-nearest neighbours</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">

```python
def numerical_smote(data, k=5):
    aug_data = []
    for i in range(len(data)):
        uniq = np.unique(data[data != data[i]])
        dists = np.abs(uniq - data[i])
        k_neigs = uniq[np.argsort(dists)[:k]]
        for neig in k_neigs:
            step = np.random.random() * (neig - data[i])
            aug_data.append(data[i] + step)
    return np.array(aug_data)
```

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

## Feature Engineering

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Creating</b> new features can capture important patterns or relations in the data</p>
                <ul>
                    <li>Extracting information from existing features</li>
                    <li>Combining existing features</li>
                    <li>Adding domain knowledge rules</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">

```python
data['AgeGroup'] = pd.cut(
    data['Age'],
    bins=[0, 12, 18, 35, 60],
    labels=['Child',
            'Teenager',
            'Young Adult',
            'Adult'],
)
```

</div>
        </div>
    </div>
</div>

## Feature Engineering

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/correlation-matrix.png" alt="Correlation Matrix" style="height: 420px">
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Selecting</b> the most important features reduces dimensionality, prevents overfitting, improves interpretability, and reduces training time</p>

```python
corr_matrix = data.corr()
sns.heatmap(corr_matrix, annot=True, center=0)
plt.show()
```

</div>
        </div>
    </div>
</div>

## Feature Engineering

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/features-importance.png" alt="Feature Importance" style="height: 400px">
                <p><b>Decision trees</b> rank features by information gain</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/pca.png" alt="Principal Component Analysis" style="height: 400px">
                <p><b>PCA</b> turns correlated features into uncorrelated components that capture most of the variance</p>
            </div>
        </div>
    </div>
</div>

## Data Quality

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>Every method above answers the same question: is the data <b>fit for a purpose</b>?</p>
                <p>Data quality is multi-dimensional</p>
                <ul>
                    <li><b>Accuracy</b> does the value match the event?</li>
                    <li><b>Completeness</b> are the fields we need present?</li>
                    <li><b>Uniqueness</b> is each event listed once?</li>
                    <li><b>Consistency</b> do units and scales agree?</li>
                    <li><b>Timeliness</b> is the record current enough for the decision?</li>
                    <li><b>Validity</b> does the value obey the declared format?</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/data-quality.jpg" alt="Data Quality" style="height: 400px">
            </div>
        </div>
    </div>
</div>

## Data Quality

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/data-usability.jpg" alt="Data Usability" style="height: 400px">
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Poor data quality can lead to:</b></p>
                <ul>
                    <li>Inaccurate predictions</li>
                    <li>Biased results</li>
                    <li>Over-trust in a table that is not fit</li>
                    <li>Intellectual debt</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Data Quality

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p>For a post-earthquake review, ask of each row:</p>
                <ul>
                    <li>Do we know <b>where</b> it was, and with what uncertainty?</li>
                    <li>Do we know <b>how large</b> it was, and on which scale?</li>
                    <li>What risk remains if we still train a first model?</li>
                </ul>
                <p>The answer depends on the decision, not on the table alone. The same rows can be fit for one question and unfit for another.</p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
