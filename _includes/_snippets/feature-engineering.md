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

## Feature Engineering

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p>Process of creating, transforming, and selecting features in our data, combining domain knowledge and creativity.</p>
            </div>
        </div>
    </div>
</div>

## Feature Engineering

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>Creating new features in our data can help to capture important patterns or relations in the data</p>
                <ul>
                    <li>Extracting information from existing features</li>
                    <li>Combining existing features</li>
                    <li>Adding domain knowledge rules</li>
                    <li>...</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
            </div>
        </div>
    </div>
</div>

## Feature Engineering

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>Creating new features in our data can help to capture important patterns or relations in the data</p>
                <ul>
                    <li>Extracting information from existing features</li>
                    <li>Combining existing features</li>
                    <li>Adding domain knowledge rules</li>
                    <li>...</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">

```python
data['AgeGroup'] = pd.cut(data['Age'], 
                    bins=[0, 12, 18, 35, 60],
                    labels=['Child', 
                            'Teenager', 
                            'Young Adult', 
                            'Adult'])
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
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>Selecting the most important features in our data reduces dimensionality, prevents overfitting, improves interpretability, and reduces training time</p>
                <ul>
                    <li>Correlation Matrix with Heatmap</li>
                    <li>Decisions Trees</li>
                    <li>Principal Component Analysis (PCA)</li>
                    <li>...</li>
    </div>
</div>

## Feature Engineering

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/correlation-matrix.png" alt="Correlation Matrix" style="height: 500px">
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>Selecting the most important features in our data reduces dimensionality, prevents overfitting, improves interpretability, and reduces training time</p>
                <ul>
                    <li>Correlation Matrix with Heatmap</li>
                    <li>Decisions Trees</li>
                    <li>Principal Component Analysis (PCA)</li>
                    <li>...</li>
    </div>
</div>

## Feature Engineering

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/correlation-matrix.png" alt="Correlation Matrix" style="height: 500px">
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>The matrix helps to visualise the correlation between features</p>
            </div>
    </div>
</div>

## Feature Engineering

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/correlation-matrix.png" alt="Correlation Matrix" style="height: 500px">
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">

```python
corr_matrix = data.corr()
plt.figure(figsize=(12, 8))
sns.heatmap(corr_matrix, annot=True, center=0)
plt.title('Feature Correlation Matrix')
plt.show()
```
</div>
    </div>
</div>

## Feature Engineering

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/features-importance.png" alt="Feature Importance" style="height: 500px">
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>A decision tree helps in identifying the most important features contributing to the prediction. This method splits the dataset into subsets based on the feature that results in the largest information gain. At the end of the process, we get the importance of each feature</p>
            </div>
    </div>
</div>

## Feature Engineering

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/features-importance.png" alt="Feature Importance" style="height: 500px">
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">

```python
from sklearn.tree import DecisionTreeClassifier
tree = DecisionTreeClassifier(random_state=42)
tree.fit(X, y)
```
</div>
    </div>
</div>

## Feature Engineering

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <img src="{{ site.url }}/assets/media/images/titanic-tree.png" alt="Titanic Tree" style="height: 600px">
            </div>
        </div>
    </div>
</div>

## Feature Engineering

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/pca.png" alt="Feature Importance" style="height: 500px">
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>Principal Component Analysis (PCA) is a dimensionality reduction technique that transforms a set of correlated features into a set of linearly uncorrelated features called principal components. These components capture the most variance in the data, allowing for a reduction in the number of features while retaining most of the information.</p>
            </div>
        </div>
    </div>
</div>

## Feature Engineering

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/pca.png" alt="Feature Importance" style="height: 500px">
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">

```python
from sklearn.decomposition import PCA
pca = PCA()
X_pca_transformed = pca.fit_transform(X_scaled)
# Calculate explained variance ratio
explained_variance = pca.explained_variance_ratio_
cumulative_variance = np.cumsum(explained_variance_ratio)
```
</div>
    </div>
</div>

## Feature Engineering

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/pca-individual.png" alt="Feature Importance" style="height: 500px">
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">

```python
from sklearn.decomposition import PCA
pca = PCA()
X_pca_transformed = pca.fit_transform(X_scaled)
# Calculate explained variance ratio
explained_variance = pca.explained_variance_ratio_
cumulative_variance = np.cumsum(explained_variance_ratio)
```
</div>
    </div>
</div>

<!-- end SLIDES: --> 