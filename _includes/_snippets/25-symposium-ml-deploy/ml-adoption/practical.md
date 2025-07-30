<!-- NOTEBOOK: -->

# Practical Introduction

In this practical session, we will first explore different methods to <em>access</em> datasets for machine learning projects. We'll cover various scenarios where data might not be readily available. We will then explore different techniques for ensuring data quality in machine learning projects (i.e., <em>data assess</em>). We'll cover data cleaning, preprocessing, augmentation, feature engineering, and validation methods.

## Exercise 1: Structured Data Access Methods

Let's explore different ways to access data for ML projects, but first let's import the basic libraries.

```python
import pandas as pd
import numpy as np
```

### 1.2 Loading from CSV/Excel Files

We can access local dataset files, which are normally stored as CSV (Comma Separated Values) files. Let's define a function we can use and reuse.

```python
# Example of loading data from a CSV file
# Note: Replace 'path_to_file.csv' with your actual file path
def load_csv_data(file_path):
    try:
        data = pd.read_csv(file_path)
        print(f"Successfully loaded data with shape: {data.shape}")
        return data
    except FileNotFoundError:
        print("File not found. Please check the file path.")
        return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None
```

### 1.2 Using Built-in Datasets

We can use platforms like [OpenML](https://www.openml.org/) to access the datasets they offer. In this example, we are accessing [the ***iris*** dataset](https://api.openml.org/d/43839). This dataset contains 150 samples of iris flowers, each with 5 features defining the sepal length, sepal width, petal length, petal width, and specie (target variable).

```python
from sklearn.datasets import fetch_openml
# Load a built-in dataset from scikit-learn
iris = fetch_openml(name='iris', version=1, as_frame=True)
print("Iris dataset shape:", iris.data.shape)
print("\nFirst few rows:")
print(iris.data.head())
```

Another alternative is [Tensorflow Datasets](https://www.tensorflow.org/datasets). In this example, we are accessing [the ***cifar10*** dataset](https://www.tensorflow.org/datasets/catalog/cifar10). This dataset contains 60000 32x32 colour images in 10 classes, with 6000 images per class. There are 50000 training images and 10000 test images.

```python
import tensorflow as tf
# Load a built-in dataset from Tensorflow datasets
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.cifar10.load_data()
print("Training data shape:", x_train.shape)
print("Test data shape:", x_test.shape)
```

We can plot some images of the dataset:

```python
import matplotlib.pyplot as plt
# Plot some images of the dataset
fig, axes = plt.subplots(3, 3, figsize=(10, 10))
for i, ax in enumerate(axes.flat):
    ax.imshow(x_train[i])
    ax.set_title(f"Image {i+1}")
plt.show()
```

### 1.3 Accessing Data via APIs

We can access datasets that are exposed online. We will access the data programatically using the ***requests*** Python module. As this is a repetitive task when handling data, we will create a function we can use and reuse. 

```python
import requests
def fetch_data_from_api(url, params=None):
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {str(e)}")
        return None
```

Now we can use the function to access different datasets. In the following example we are accessing [the UK Price Paid data](https://www.gov.uk/government/statistical-data-sets/price-paid-data-downloads) for houses for the first semester of 2020. The data is then written as a CSV file.

```python
url = 'http://prod.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com/pp-2020-part1.csv'
file_name_part_1='pp-2020-part1.csv'
# Using our function to fetch data from an API
response = fetch_data_from_api(url)
if response.status_code == 200:
  with open("./" + file_name_part_1, "wb") as file:
    file.write(response.content)
```

We can now open the CSV file using the function we defined before.

```python
file_path = './pp-2020-part1.csv'
# Using our function to load data from a CSV file
dataset = load_csv_data(file_path)
print("Dataset shape:", dataset.shape)
print("\nFirst few rows:")
print(dataset.head())
```

As we defined a function to access data via APIs, we can reuse it for different datasets. In this example, we are accessing [the OpenPostcode Geo dataset](https://www.getthedata.com/open-postcode-geo). This time the downloaded file is a zipped file. We need to unzip and the save and open as a CSV file.

```python
import io
import zipfile
url = 'https://www.getthedata.com/downloads/open_postcode_geo.csv.zip'
response = fetch_data_from_api(url)
if response.status_code == 200:
  # Reading and unzipping the downloaded file
  with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
    zip_ref.extractall('open_postcode_geo')
# Using our function to load data from a CSV file
dataset = load_csv_data('open_postcode_geo/open_postcode_geo.csv')
print("Dataset shape:", dataset.shape)
print("\nFirst few rows:")
print(dataset.head())
```

1.4 Joining datasets to create a new one with more information. We first load and explore the price paid data.

```python
price_paid = load_csv_data('pp-2020-part1.csv')
print("Original Price Paid dataset shape:", price_paid.shape)
print("\nFirst few rows:")
print(price_paid.head())
```

Before joining we need to add names to the columns of our dataset.

```python
price_paid_columns = [
    'transaction_unique_identifier',
    'price',
    'date_of_transfer',
    'postcode',
    'property_type',
    'new_build_flag',
    'tenure_type',
    'primary_addressable_object_name',
    'secondary_addressable_object_name',
    'street',
    'locality',
    'town_city',
    'district',
    'county',
    'ppd_category_type',
    'record_status'
]
price_paid.columns = price_paid_columns
print(price_paid.head())
```

We should now load and explore the postcodes data.

```python
postcodes = load_csv_data('open_postcode_geo/open_postcode_geo.csv')
print("Original Postcodes dataset shape:", postcodes.shape)
print("\nFirst few rows:")
print(postcodes.head())
```

Again, we should name the columns of our dataset:

```python
postcodes_columns = [
    'postcode',
    'status',
    'usertype',
    'easting',
    'northing',
    'positional_quality_indicator',
    'country',
    'latitude',
    'longitude',
    'postcode_no_space',
    'postcode_fixed_width_seven',
    'postcode_fixed_width_eight',
    'postcode_area',
    'postcode_district',
    'postcode_sector',
    'outcode',
    'incode'
]
postcodes.columns = postcodes_columns
print(postcodes.head())
```

For joining two datasets, they must share one or more attributes that allow them to match. In this case, both datasets share the `postcode` attribute or column. We use this attribute to merge both datasest.

```python
merged_data = pd.merge(
    price_paid,
    postcodes,
    on='postcode',
    how='inner'
)
```

We can now manipulate and save the enriched dataset.

```python
print("Merged dataset shape:", merged_data.shape)
print("\nSample of merged data:")
print(merged_data.head())
merged_data.to_csv('price_paid_with_coordinates.csv', index=False)
```

## Exercise 2: Unstructured Data Access for Open Street Maps

OpenStreetMap (OSM) provides a rich source of geospatial data that can be accessed through various methods. Let's explore how to work with OSM data:

### 2.1 Using OSMnx for Network Data

OSMnx is a powerful Python package for working with street networks and other spatial data from OpenStreetMap. We need to install the osmnx library first.

```python
%pip install osmnx
```

And the common imports as usual.

```python
import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
```

```python
def get_network_data(place_name, network_type='drive'):
    """
    Retrieve street network data for a specific place
    
    Parameters:
    -----------
    place_name : str
        Name of the place (e.g., 'London, UK')
    network_type : str
        Type of network ('drive', 'walk', 'bike', 'all')
        
    Returns:
    --------
    G : networkx.MultiDiGraph
        Street network graph
    """
    try:
        # Download the street network
        G = ox.graph_from_place(place_name, network_type=network_type)
        print(f"Successfully downloaded network with {len(G.nodes)} nodes and {len(G.edges)} edges")
        return G
    except Exception as e:
        print(f"Error downloading network: {str(e)}")
        return None
```

We can use our function to get the streets data for Pasto.

```python
# Example usage
place = "Pasto, Nariño, Colombia"
G = get_network_data(place)
```

And now we can visualise the data

```python
# Visualize the network
if G is not None:
    fig, ax = ox.plot_graph(G, node_size=0, edge_linewidth=0.5)
    plt.show()
```

### 2.3 Using OSMnx for Points of Interest

We can also extract points of interest (POIs) of a city using OSMnx:

```python
def get_pois(place_name, tags):
    """
    Retrieve points of interest for a specific place and tags
    
    Parameters:
    -----------
    place_name : str
        Name of the place
    tags : dict
        Dictionary of OSM tags to search for
        
    Returns:
    --------
    pois : geopandas.GeoDataFrame
        Points of interest
    """
    try:
        pois = ox.features_from_place(place_name, tags=tags)
        print(f"Found {len(pois)} points of interest")
        return pois
    except Exception as e:
        print(f"Error retrieving POIs: {str(e)}")
        return None
```

We can use our function to find all buildings and schools in Pasto.

```python
# Example: Find all buildings and schools in Pasto
place = "Pasto, Nariño, Colombia"
buildings = get_pois(place, {"building": True})
schools = get_pois(place, {"amenity": "school"})
if schools is not None:
    # Plot the schools
    fig, ax = plt.subplots(figsize=(10, 10))
    schools.plot(ax=ax, markersize=10, color='red')
    if buildings is not None:
        buildings.plot(ax=ax)
    plt.title("Buildings and Schools in Pasto")
    plt.show()
```

### 2.3 Using Overpass API for Custom Queries

The Overpass API allows for more specific queries to extract particular features from OSM. We first must install the overpy module.

```python
%pip install overpy
```

And add the imports as usual.

```python
import overpy
import geopandas as gpd
from shapely.geometry import Point
```

```python
def query_osm_features(query):
    """
    Query specific features from OSM using Overpass API
    
    Parameters:
    -----------
    query : str
        Overpass QL query string
        
    Returns:
    --------
    result : overpy.Result
        Query results
    """
    try:
        api = overpy.Overpass()
        result = api.query(query)
        print(f"Query successful. Found {len(result.nodes)} nodes, {len(result.ways)} ways, and {len(result.relations)} relations")
        return result
    except Exception as e:
        print(f"Error querying OSM: {str(e)}")
        return None
```

We must define a query in the `overpy` language. In our example we want to find all restaurants in Pasto. The query we use has the following parts:

1. `[out:json][timeout:25];`

- out:json specifies that we want the output in JSON format
- timeout:25 sets a timeout of 25 seconds for the query

2. `area[name="Pasto"]->.searchArea;`

- This creates a named area filter called "searchArea"
- It looks for an area with the name "Pasto, Nariño, Colombia"
- The ->.searchArea stores this area for later use in the query

3. The main search block.

- This searches for three types of OSM elements:
-- `node`: Individual points (like a restaurant location)
-- `way`: Lines or areas (like a restaurant building)
-- `relation`: Complex objects made up of multiple elements
- `["amenity"="restaurant"]` is a tag filter that looks for elements tagged as restaurants
- `(area.searchArea)` restricts the search to within the Pasto area we defined

3. The output statements.

- `out body;` outputs the full data for the found elements
- `>;` recursively gets all nodes that are part of the ways and relations
- `out skel qt;` out skel qt outputs the remaining elements in a compact format

Let's execute the function to find all restaurants in Pasto.

```python
# Example: Find all restaurants in a specific area
query = """
[out:json][timeout:25];
area[name="Pasto"]->.searchArea;
(
  node["amenity"="restaurant"](area.searchArea);
  way["amenity"="restaurant"](area.searchArea);
  relation["amenity"="restaurant"](area.searchArea);
);
out body;
>;
out skel qt;
"""
restaurants = query_osm_features(query)
```

We can then manipulate the restaurants data. We convert it to a GeoDataFrame in our example. For that, we create an array of points with the restaurant nodes information.

```python
# Convert results to GeoDataFrame for easier analysis
if restaurants is not None:
    # Create a list to store restaurant points
    points = []
    for node in restaurants.nodes:
        points.append({
            'geometry': Point(float(node.lon), float(node.lat)),
            'name': node.tags.get('name', 'Unknown'),
            'cuisine': node.tags.get('cuisine', 'Unknown')
        })
    # Create GeoDataFrame
    gdf = gpd.GeoDataFrame(points, crs="EPSG:4326")
    print("\nRestaurant data sample:")
    print(gdf.head())
```

We can print more detailed data about restaurants in Pasto.

```python    
# Print more detailed information about the restaurants
print("\nDetailed Restaurant Information:")
print("Total number of restaurants:", len(gdf))
print("\nRestaurant names:")
print(gdf['name'].value_counts().head())
print("\nCuisine types:")
print(gdf['cuisine'].value_counts().head())
```

These methods provide different ways to access and work with OpenStreetMap data, from street networks to points of interest.

## Exercise 3: Data Cleaning

Data cleaning is a fundamental step in any machine learning project. It involves identifying and handling issues in the data that could affect model performance. In this exercise, we'll learn various techniques for cleaning data using the Titanic dataset, which contains several common data quality challenges.

Let's start by importing the necessary libraries. We'll use:
- pandas and numpy for data manipulation
- matplotlib and seaborn for visualisation
- scikit-learn for preprocessing and feature selection

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
```

### 3.1 Loading and Exploring Data

The first step in any data cleaning process is to understand your data. We'll use the [Titanic dataset](https://www.kaggle.com/c/titanic/data), which is perfect for learning data cleaning as it contains various data quality issues like missing values, outliers, and categorical variables. 

Titanic dataset field descriptions

- **PassengerId**: Unique identifier for each passenger.
- **Survived**: 1 if the passenger survived, 0 otherwise.
- **Pclass**: Ticket class (1 = 1st, 2 = 2nd, 3 = 3rd).
- **Name**: Full name of the passenger.
- **Sex**: Gender (male/female).
- **Age**: Age in years.
- **SibSp**: Number of siblings or spouses aboard.
- **Parch**: Number of parents or children aboard.
- **Ticket**: Ticket number.
- **Fare**: Ticket fare.
- **Cabin**: Cabin number.
- **Embarked**: Port of embarkation (C = Cherbourg, Q = Queenstown, S = Southampton).



```python
# Load the Titanic dataset
url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
titanic_data = pd.read_csv(url)
```

Let's examine the dataset to understand its structure and the data it stores:

```python
# Display basic information about the dataset
print("Dataset Shape:", titanic_data.shape)
print("\nFirst few rows:")
print(titanic_data.head())
print("\nDataset Info:")
print(titanic_data.info())
```

### 3.2 Handling Missing Values

Missing values are one of the most common data quality issues. They can occur due to various reasons:
- Data collection errors
- System failures
- Information not available
- Data entry mistakes

It's crucial to handle missing values appropriately as they can significantly impact our analysis and model performance. We'll explore different strategies:
1. Deletion: Remove rows or columns with missing values
2. Imputation: Fill missing values with estimated values
3. Advanced techniques: Use machine learning models to predict missing values

First, let's analyze the extent of missing values in our dataset:

```python
# Check for missing values
missing_values = titanic_data.isnull().sum()
print("Missing values per column:")
print(missing_values[missing_values > 0])
```

Let's visualise the missing values to better understand their distribution:

```python
# Visualise missing values
plt.figure(figsize=(10, 6))
sns.heatmap(titanic_data.isnull(), yticklabels=False, cbar=False, cmap='viridis')
plt.title('Missing Values Heatmap')
plt.show()
```

Deletion strategies for handling missing values.

```python
# Create copies of the data for different deletion strategies
titanic_data_row_drop = titanic_data.copy()
titanic_data_col_drop = titanic_data.copy()
```

Row deletion: Remove rows with any missing values.

```python
rows_before = len(titanic_data_row_drop)
titanic_data_row_drop = titanic_data_row_drop.dropna()
rows_after = len(titanic_data_row_drop)
print(f"\nRow deletion results:")
print(f"Rows before: {rows_before}")
print(f"Rows after: {rows_after}")
print(f"Rows removed: {rows_before - rows_after}")
print(f"Percentage of data lost: {((rows_before - rows_after) / rows_before * 100):.2f}%")
```

Column deletion: Remove columns with missing values.

```python
cols_before = len(titanic_data_col_drop.columns)
titanic_data_col_drop = titanic_data_col_drop.dropna(axis=1)
cols_after = len(titanic_data_col_drop.columns)
print(f"\nColumn deletion results:")
print(f"Columns before: {cols_before}")
print(f"Columns after: {cols_after}")
print(f"Columns removed: {cols_before - cols_after}")
print(f"Percentage of features lost: {((cols_before - cols_after) / cols_before * 100):.2f}%")
```

Selective deletion: Remove rows only if they have missing values in specific columns (We can define the removing criteria).

```python
titanic_data_selective = titanic_data.copy()
rows_before = len(titanic_data_selective)
# Only drop rows with missing values in Age and Embarked
titanic_data_selective = titanic_data_selective.dropna(subset=['Age', 'Embarked'])
rows_after = len(titanic_data_selective)
print(f"\nSelective deletion results (Age and Embarked):")
print(f"Rows before: {rows_before}")
print(f"Rows after: {rows_after}")
print(f"Rows removed: {rows_before - rows_after}")
print(f"Percentage of data lost: {((rows_before - rows_after) / rows_before * 100):.2f}%")
```

Imputation strategies fill missing values based on the values of other records.

```python
from sklearn.impute import SimpleImputer, KNNImputer
```

Mean imputation: Replaces missing values with the mean of the respective feature:
    - Pros: Simple to implement, reduces variance
    - Cons: Can be affected by outliers, doesn't preserve data distribution

```python
mean_imputer = SimpleImputer(strategy='mean')
titanic_data['Age_Mean'] = mean_imputer.fit_transform(titanic_data[['Age']])
```

Median imputation: Replaces missing values with the median of the respective feature:
   - Pros: More robust to outliers than mean
   - Cons: Still reduces variance

```python
median_imputer = SimpleImputer(strategy='median')
titanic_data['Age_Median'] = median_imputer.fit_transform(titanic_data[['Age']])
```

More advanced methods can use ML models to fill the values:

K-Nearest Neighbours (KNN) imputation: This value uses the values of similar data points to the record that is missing data. It selects the `k` most similar data points (i.e., neighbours), and uses ther values to estimate the missing value. 
   - Pros: More sophisticated, considers similar instances
   - Cons: Computationally expensive, requires complete features

```python
knn_imputer = KNNImputer(n_neighbors=5)
titanic_data['Age_KNN'] = knn_imputer.fit_transform(titanic_data[['Age']])
```

Regression imputation: This method uses a regression model to predict missing values based on other features in the dataset. It's particularly useful when there's a strong relationship between the missing feature and other features.

We first prepare the data for training the regression model. We select the features that can have strong relationship with the Age variable.

```python
from sklearn.linear_model import LinearRegression
# Prepare data for regression imputation
# Select features that might help predict Age
features_for_age = ['Pclass', 'SibSp', 'Parch', 'Fare']
X_train = titanic_data.dropna(subset=['Age'])[features_for_age]
y_train = titanic_data.dropna(subset=['Age'])['Age']
```

We then train the model with the selected data features.

```python
# Train the regression model
reg_imputer = LinearRegression()
reg_imputer.fit(X_train, y_train)
```

We now use the trained model to determine the predicted ages and fill the missing values.

```python
# Predict missing Age values
X_missing = titanic_data[titanic_data['Age'].isnull()][features_for_age]
predicted_ages = reg_imputer.predict(X_missing)
# Create a copy of the data for regression imputation
titanic_data_reg = titanic_data.copy()
titanic_data_reg.loc[titanic_data_reg['Age'].isnull(), 'Age'] = predicted_ages
titanic_data['Age_Regression'] = titanic_data_reg['Age']
```

When we are dealing with data and different methods, we must always compare and select the better one according to our needs. This comparison can be based on plots:

```python
# Compare the different imputation strategies
plt.figure(figsize=(15, 5))
plt.subplot(1, 4, 1)
sns.histplot(data=titanic_data, x='Age_Mean', bins=30)
plt.title('Mean Imputation')
plt.grid()
plt.ylim(0, 250)
plt.subplot(1, 4, 2)
sns.histplot(data=titanic_data, x='Age_Median', bins=30)
plt.title('Median Imputation')
plt.grid()
plt.ylim(0, 250)
plt.subplot(1, 4, 3)
sns.histplot(data=titanic_data, x='Age_KNN', bins=30)
plt.title('KNN Imputation')
plt.grid()
plt.ylim(0, 250)
plt.subplot(1, 4, 4)
sns.histplot(data=titanic_data, x='Age_Regression', bins=30)
plt.title('Regression Imputation')
plt.grid()
plt.ylim(0, 250)
plt.tight_layout()
plt.show()
```

Statistical analysis is also helpful to compare te imputation methods:

```python
from scipy import stats
# Compare statistical properties of all imputation methods
print("\nStatistical Properties Comparison:")
print("\nOriginal Data:")
print(f"Mean: {titanic_data['Age'].mean():.3f}")
print(f"Std: {titanic_data['Age'].std():.3f}")
print(f"Skewness: {stats.skew(titanic_data['Age'].dropna()):.3f}")
print("\nMean Imputation:")
print(f"Mean: {titanic_data['Age_Mean'].mean():.3f}")
print(f"Std: {titanic_data['Age_Mean'].std():.3f}")
print(f"Skewness: {stats.skew(titanic_data['Age_Mean']):.3f}")
print("\nMedian Imputation:")
print(f"Mean: {titanic_data['Age_Median'].mean():.3f}")
print(f"Std: {titanic_data['Age_Median'].std():.3f}")
print(f"Skewness: {stats.skew(titanic_data['Age_Median']):.3f}")
print("\nKNN Imputation:")
print(f"Mean: {titanic_data['Age_KNN'].mean():.3f}")
print(f"Std: {titanic_data['Age_KNN'].std():.3f}")
print(f"Skewness: {stats.skew(titanic_data['Age_KNN']):.3f}")
print("\nRegression Imputation:")
print(f"Mean: {titanic_data['Age_Regression'].mean():.3f}")
print(f"Std: {titanic_data['Age_Regression'].std():.3f}")
print(f"Skewness: {stats.skew(titanic_data['Age_Regression']):.3f}")
```

### 3.3 Handling Outliers

Outliers are data points that significantly deviate from the rest of the data. They can be caused by:
- Measurement errors
- Data entry mistakes
- Rare but valid observations
- System malfunctions

Outliers can significantly impact statistical analyses and machine learning models, so it's important to handle them appropriately. The Interquartile Range (IQR) method is a robust statistical approach for outlier detection. It works by first calculating the first quartile (Q1) and the third quartile (Q3) of the data. The IQR is then calculated as the difference between Q3 and Q1. Data points that fall below `Q1 - 1.5*IQR` or above `Q3 + 1.5*IQR` are considered outliers. This method is effective because it is resistant to the influence of outliers themselves, providing a more accurate representation of the data's spread.

```python
# Function to detect outliers using IQR method
def detect_outliers(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return df[(df[column] < lower_bound) | (df[column] > upper_bound)]
```

Let's apply this to the Fare column to detect the outliers:

```python
outliers = detect_outliers(titanic_data, 'Fare')
print(f"Number of outliers in Fare: {len(outliers)}")
```

Now we can visualise the outliers using a boxplot:

```python
plt.figure(figsize=(10, 6))
sns.boxplot(x=titanic_data['Fare'])
plt.title('Fare Distribution with Outliers')
plt.grid()
plt.show()
```

Now, let's implement different strategies to handle outliers:

1. Capping: Limits extreme values to a specified range
   - Pros: Preserves data points while reducing their impact
   - Cons: May lose information about extreme cases

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

Applying capping

```python
titanic_data = cap_outliers(titanic_data, 'Fare')
```

2. Log transformation: Reduces the impact of extreme values
   - Pros: Preserves the order of values while reducing the impact of outliers
   - Cons: Changes the scale of the data

```python
titanic_data['Fare_log'] = np.log1p(titanic_data['Fare'])
```

Let's compare the different strategies to see their impact on the data distribution:

```python
plt.figure(figsize=(15, 5))
plt.subplot(1, 3, 1)
sns.histplot(data=titanic_data, x='Fare', bins=30)
plt.grid()
plt.title('Original Fare')
plt.subplot(1, 3, 2)
sns.histplot(data=titanic_data, x='Fare_capped', bins=30)
plt.grid()
plt.title('Capped Fare')
plt.subplot(1, 3, 3)
sns.histplot(data=titanic_data, x='Fare_log', bins=30)
plt.grid()
plt.title('Log-transformed Fare')
plt.tight_layout()
plt.show()
```

## Exercise 4: Data Preprocessing

Data preprocessing is a crucial step in preparing data for machine learning models. It involves transforming the data into a format that is suitable for analysis and modeling. In this exercise, we'll explore two main preprocessing techniques: feature scaling and categorical feature encoding.

### 4.1 Feature Scaling

Feature scaling is the process of transforming numerical features to a common scale, ensuring that all features contribute equally to the model.

```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler
```

- It ensures all features contribute equally to the model
- It helps algorithms converge faster
- It prevents features with larger scales from dominating the model

We start by selecting the numerica features for scaling.

```python
numerical_features = ['Age', 'Fare', 'SibSp', 'Parch']
```

We'll explore two common scaling techniques:
1. Standardization (Z-score): Centers data around 0 with unit variance
   - Best for: Algorithms that assume normal distribution
   - Formula: z = (x - μ) / σ

```python
scaler = StandardScaler()
standardized_columns = [col + '_standardized' for col in numerical_features]
titanic_data[standardized_columns] = scaler.fit_transform(titanic_data[numerical_features])
```

2. Min-Max scaling: Scales data to a fixed range (usually [0,1])
   - Best for: Algorithms that require bounded input
   - Formula: x_scaled = (x - x_min) / (x_max - x_min)

```python
minmax_scaler = MinMaxScaler()
minmax_columns = [col + '_minmax' for col in numerical_features]
titanic_data[minmax_columns] = minmax_scaler.fit_transform(titanic_data[numerical_features])
```

Let's visualize the impact of different scaling techniques on the Age feature. This will help us understand how each technique affects the data distribution:

```python
plt.figure(figsize=(15, 5))
plt.subplot(1, 3, 1)
sns.histplot(data=titanic_data, x='Age', bins=30)
plt.grid()
plt.title('Original Age')
plt.subplot(1, 3, 2)
sns.histplot(data=titanic_data, x='Age_standardized', bins=30)
plt.grid()
plt.title('Standardized Age')
plt.subplot(1, 3, 3)
sns.histplot(data=titanic_data, x='Age_minmax', bins=30)
plt.grid()
plt.title('Min-Max Scaled Age')
plt.tight_layout()
plt.show()
```

### 4.2 Categorical Feature Encoding

Categorical features need to be converted to numerical format for machine learning algorithms. Different encoding techniques have different advantages and use cases:

Select categorical features.

```python
categorical_features = ['Sex', 'Embarked', 'Pclass']
```

1. One-hot encoding:
   - Creates binary columns for each category
   - Pros: No ordinal relationship, works well with most algorithms
   - Cons: Can lead to high dimensionality (curse of dimensionality)
   - Best for: Nominal categorical variables

```python
titanic_data_encoded = pd.get_dummies(titanic_data, columns=categorical_features, prefix=categorical_features)
```

2. Label encoding:
   - Assigns a unique number to each category
   - Pros: Maintains dimensionality, simple to implement
   - Cons: Can introduce artificial ordinal relationships
   - Best for: Ordinal categorical variables

```python
from sklearn.preprocessing import LabelEncoder
label_encoder = LabelEncoder()
titanic_data['Sex_encoded'] = label_encoder.fit_transform(titanic_data['Sex'])
```

Let's compare the encoding techniques to understand their differences:

```python
print("\nOne-hot encoding example:")
print(titanic_data_encoded[['Sex_female', 'Sex_male']].head())
print("\nLabel encoding example:")
print(titanic_data[['Sex', 'Sex_encoded']].head())
```

## Exercise 5: Data Augmentation

Data augmentation helps us increase the size and diversity of our datasets. This is particularly important when we have limited data or want to improve model robustness. In this exercise, we'll explore different techniques for augmenting numerical data.

### 5.1 Numerical Data Augmentation

We'll implement two main techniques:

1. Gaussian Noise: Adds controlled random noise to the data, which helps the model become more robust to small variations in the input.
2. SMOTE-like: Creates synthetic samples by interpolating between existing data points, which helps balance the dataset and prevent overfitting.

```python
import numpy as np
from scipy import stats
```

First, let's prepare our data by selecting the numerical features we want to augment:

```python
numerical_features = ['Age', 'Fare', 'SibSp', 'Parch']
X_aug = titanic_data[numerical_features].fillna(titanic_data[numerical_features].mean())
```

Let's implement the Gaussian noise augmentation. This technique adds random noise from a normal distribution to our data, which helps the model learn to be invariant to small variations in the input:

```python
def add_gaussian_noise(data, noise_factor=0.05):
    noise = np.random.normal(0, noise_factor, data.shape)
    return data + noise
```

Now, let's implement a SMOTE-like augmentation. This technique creates synthetic samples by interpolating between existing data points and their nearest neighbors. This helps to:
- Increase the size of the dataset
- Create more balanced classes
- Improve model generalisation

```python
def numerical_smote(data, k=5):
    augmented_data = []
    for i in range(len(data)):
        # Get all unique values except the current one
        unique_values = np.unique(data[data != data[i]])
        # Compute distances only to unique values
        distances = np.abs(unique_values - data[i])
        # Get up to k nearest unique neighbors
        k_neighbors = unique_values[np.argsort(distances)[:k]]
        for neighbor in k_neighbors:
            new_sample = data[i] + np.random.random() * (neighbor - data[i])
            augmented_data.append(new_sample)
    return np.array(augmented_data)
```

Let's apply these techniques to the Age feature.

```python
age_data = X_aug['Age'].values
gaussian_augmented = add_gaussian_noise(age_data)
smote_augmented = numerical_smote(age_data)
```

Let's print a few values to see the differences.

```python
print('Original Age Data: ')
print(age_data[:10])
print(f'The original age data has {len(age_data)} elements')
print('\nGaussian Augmented Age Data: ')
print(gaussian_augmented[:10])
print(f'The Gaussian augmented age data has {len(gaussian_augmented)} elements')
print('\nSMOTE Augmented Age Data: ')
print(smote_augmented[:10])
print(f'The SMOTE augmented age data has {len(smote_augmented)} elements')
```

Let's visualise the datasets to understand how each augmentation technique affects the data distribution.

```python
plt.figure(figsize=(15, 5))
plt.subplot(1, 3, 1)
plt.hist(age_data, bins=30)
plt.grid()
plt.title('Original Age')
plt.subplot(1, 3, 2)
plt.hist(gaussian_augmented, bins=30)
plt.grid()
plt.title('Gaussian Noise Augmented')
plt.subplot(1, 3, 3)
plt.hist(smote_augmented, bins=30)
plt.grid()
plt.title('SMOTE Augmented')
plt.tight_layout()
plt.show()
```

Let's analyze the statistical properties of the augmented data to understand how each technique affects the data distribution. This analysis helps us ensure that our augmentation techniques maintain the important characteristics of the original data while adding useful variations:

```python
print("\nStatistical Properties Comparison:")
print("\nOriginal Data:")
print(f"Mean: {np.mean(age_data):.3f}")
print(f"Std: {np.std(age_data):.3f}")
print(f"Skewness: {stats.skew(age_data):.3f}")
print("\nGaussian Noise Augmented:")
print(f"Mean: {np.mean(gaussian_augmented):.3f}")
print(f"Std: {np.std(gaussian_augmented):.3f}")
print(f"Skewness: {stats.skew(gaussian_augmented):.3f}")
print("\nSMOTE Augmented:")
print(f"Mean: {np.mean(smote_augmented):.3f}")
print(f"Std: {np.std(smote_augmented):.3f}")
print(f"Skewness: {stats.skew(smote_augmented):.3f}")
```

We can finally use the ANOVA test to compare the distributions of the original and augmented target variables. The one-way ANOVA tests the null hypothesis that two or more groups have the same population mean. The test is applied to samples from two or more groups, possibly with differing sizes.

H0 - The original and augmented target variables are not statistically significantly different.

H1 - The original and augmented target variables are statistically significantly different.

```python
from scipy.stats import f_oneway
stat, p_value = f_oneway(age_data, smote_augmented)
print(f"ANOVA test p-value: {p_value}")
```

A high p-value in the ANOVA test suggests that the augmented data is statistically similar to the original. This means our augmentation process has preserved the essential characteristics of the data, making it suitable for training more robust models.

We visualize the distributions and interpret the results.

```python
plt.hist(age_data, bins=30, alpha=0.5, label='Original Age')
plt.hist(smote_augmented, bins=30, alpha=0.5, label='Augmented Age')
plt.legend()
plt.title('Original vs Augmented Target Distribution')
plt.show()
```

## Exercise 6: Feature Engineering

Feature engineering is the process of creating new features from existing data, transforming features, and selecting features to improve models performance. It requires domain knowledge and creativity. In this exercise, we'll explore different feature engineering techniques.

### 6.1 Creating New Features

Creating new features can help capture important patterns and relationships in the data. We'll create several new features that might be useful for predicting survival in the Titanic dataset:

1. Family size: Combines SibSp and Parch to create a more meaningful feature
2. Title: Extracts social status information from the Name field
3. Cabin information: Creates a binary feature indicating cabin availability
4. Age groups: Bins age into meaningful categories

```python
titanic_data['FamilySize'] = titanic_data['SibSp'] + titanic_data['Parch'] + 1
titanic_data['Title'] = titanic_data['Name'].str.extract(' ([A-Za-z]+)\.', expand=False)
titanic_data['HasCabin'] = titanic_data['Cabin'].notna().astype(int)
titanic_data['AgeGroup'] = pd.cut(titanic_data['Age'], 
                                 bins=[0, 12, 18, 35, 60, 100],
                                 labels=['Child', 'Teenager', 'Young Adult', 'Adult', 'Senior'])
```

Let's examine our new features to understand their distribution:

```python
# Display the new features
print("\nNew features:")
print(titanic_data[['FamilySize', 'Title', 'HasCabin', 'AgeGroup']].head())
```

### 6.2 Feature Selection

Feature selection helps us identify the most important features for our model. This is important because:
- It reduces dimensionality
- It helps prevent overfitting
- It improves model interpretability
- It can reduce training time

First, let's prepare our data applying previous techniques::

```python
url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
data = pd.read_csv(url)
#Data Cleaning and Data Drop Process
drop_elements = ['Name','Cabin','Ticket']
data = data.drop(drop_elements, axis=1)
data['Fare'] = data['Fare'].fillna(data['Fare'].dropna().median())
data['Age'] = data['Age'].fillna(data['Age'].dropna().median())
# Change to categoric column to numeric
data.loc[data['Sex']=='male','Sex']=0
data.loc[data['Sex']=='female','Sex']=1
# Replacing nan values for embarked
data['Embarked']=data['Embarked'].fillna('S') 
# Change to categoric column to numeric
data.loc[data['Embarked']=='S','Embarked']=0
data.loc[data['Embarked']=='C','Embarked']=1
data.loc[data['Embarked']=='Q','Embarked']=2
```

Let's see the correlation matrix for our processed data.

```python
corr_matrix = data.corr()
plt.figure(figsize=(12, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0)
plt.title('Feature Correlation Matrix')
plt.show()
```

Now, lets apply a Decision Tree Classifier method. 

A decision tree classifier works by recursively splitting the dataset into subsets based on the feature that results in the largest information gain (or reduction in impurity, such as Gini impurity or entropy) at each step. The tree structure is built so that each internal node represents a decision based on a feature, and each leaf node represents a class label. For feature selection, decision trees are useful because they naturally rank features by how important they are for making accurate predictions: features that are used for splits closer to the root of the tree are generally more important. The feature importance scores provided by the tree reflect how much each feature contributed to reducing impurity across all splits in the tree.

We need to start separating the feature and target variables

```python
X = data.drop('Survived', axis=1)
y = data['Survived']
```

We can fit a decision tree classifier now.

```python
from sklearn.tree import DecisionTreeClassifier
tree = DecisionTreeClassifier(random_state=42)
tree.fit(X, y)
```

As a result, we can now print the feature importances.

```python
importances = tree.feature_importances_
feature_names = X.columns
# Print feature importances
for name, importance in zip(feature_names, importances):
    print(f"{name}: {importance:.3f}")
```

And visualise these importances too.

```python
plt.figure(figsize=(10, 6))
sns.barplot(x=importances, y=feature_names)
plt.title('Feature Importances from Decision Tree')
plt.xlabel('Importance')
plt.ylabel('Feature')
plt.show()
```

We can also see the decision tree, which is a bit complex to interpret.

```python
from sklearn.tree import export_graphviz
import graphviz
dot_data = export_graphviz(
    tree, out_file=None, 
    feature_names=X.columns,  
    class_names=['Not Survived', 'Survived'],
    filled=True, rounded=True, special_characters=True
)
graph = graphviz.Source(dot_data)
graph.format = 'png'
graph.render("titanic_tree")
graph
```

### 6.3 PCA on High-Dimensional Data (Fashion-MNIST, TensorFlow)

High-dimensional data presents unique challenges in machine learning. Each image in the Fashion-MNIST dataset is 28x28 pixels, resulting in 784 features per sample. This high number of features makes visualisation and modelling more complex, as patterns are harder to discern and computational requirements increase. Dimensionality reduction techniques like Principal Component Analysis (PCA) help us project this data into a lower-dimensional space while preserving as much of the original information as possible. In this exercise, we will explore the structure of Fashion-MNIST, visualise some images, and then apply PCA to see how the data can be represented in just two dimensions.

Let's start by loading the Fashion-MNIST dataset and visualising some sample images to understand what our data looks like in its original high-dimensional form.

```python
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
(X_train, y_train), (_, _) = tf.keras.datasets.fashion_mnist.load_data()
# Show some sample images
plt.figure(figsize=(10, 2))
for i in range(10):
    plt.subplot(1, 10, i+1)
    plt.imshow(X_train[i], cmap='gray')
    plt.axis('off')
    plt.title(str(y_train[i]))
plt.suptitle('Sample Fashion-MNIST Images (Original 28x28, 784 features)')
plt.show()
# Flatten images for PCA
X_flat = X_train.reshape((X_train.shape[0], -1)) / 255.0
```

Now, let's apply PCA to reduce the dimensionality of our data from 784 features down to just 2 principal components. This will allow us to visualise the structure of the dataset in a 2D plot.

```python
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_flat)
explained_variance = pca.explained_variance_ratio_
cumulative_variance = np.cumsum(explained_variance)
```

Let's Plot explained variance ratio

```python
import matplotlib.pyplot as plt
plt.figure(figsize=(10, 6))
plt.plot(range(1, len(explained_variance) + 1), cumulative_variance, 'bo-')
plt.axhline(y=0.95, color='r', linestyle='--')
plt.xlabel('Number of Components')
plt.ylabel('Cumulative Explained Variance Ratio')
plt.title('PCA Explained Variance Ratio')
plt.grid(True)
plt.show()
```

The explained variance ratio tells us how much of the original data's information is retained in the principal components. With only two components, we capture a small fraction of the total variance, but enough to visualize the main structure of the data.

However, we can still visualise the dataset in the new 2D PCA space. Each point represents an image, coloured by its class label. Notice how some classes form distinct clusters, while others overlap.

```python
plt.figure(figsize=(8,6))
for label in np.unique(y_train):
    idx = y_train == label
    plt.scatter(X_pca[idx, 0], X_pca[idx, 1], label=str(label), alpha=0.5, s=10)
plt.legend()
plt.title('Fashion-MNIST after PCA (2D projection)')
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.show()
```

Although PCA reduces the data to two dimensions, we can also attempt to reconstruct the original images from the reduced representation (using the inverse transform). This helps us see how much information is lost in the dimensionality reduction process.

```python
# Project and reconstruct a few images
X_pca_10 = pca.transform(X_flat[:10])
X_reconstructed = pca.inverse_transform(X_pca_10)
plt.figure(figsize=(10, 4))
for i in range(10):
    # Original
    plt.subplot(2, 10, i+1)
    plt.imshow(X_flat[i].reshape(28, 28), cmap='gray')
    plt.axis('off')
    if i == 0:
        plt.ylabel('Original')
    # Reconstructed
    plt.subplot(2, 10, i+11)
    plt.imshow(X_reconstructed[i].reshape(28, 28), cmap='gray')
    plt.axis('off')
    if i == 0:
        plt.ylabel('PCA (2D)')
plt.suptitle('Original vs. PCA-Reconstructed Images')
plt.show()
```

- The original Fashion-MNIST images are high-dimensional (784 features), making direct visualisation and modelling challenging.
- PCA allows us to project this data into a lower-dimensional space, revealing structure and clusters that correspond to different classes.
- The reconstructed images from only two principal components are blurry and lack detail, illustrating the trade-off between dimensionality reduction and information loss.
- The explained variance ratio quantifies how much of the original information is preserved in the reduced space.


Let's apply PCA with different number of components and see when most of the variance in the data is explained. Let's apply PCA with 10 principal components.

```python
pca = PCA(n_components=10)
X_pca = pca.fit_transform(X_flat)
explained_variance = pca.explained_variance_ratio_
cumulative_variance = np.cumsum(explained_variance)
```

Let's Plot explained variance ratio

```python
import matplotlib.pyplot as plt
plt.figure(figsize=(10, 6))
plt.plot(range(1, len(explained_variance) + 1), cumulative_variance, 'bo-')
plt.axhline(y=0.95, color='r', linestyle='--')
plt.xlabel('Number of Components')
plt.ylabel('Cumulative Explained Variance Ratio')
plt.title('PCA Explained Variance Ratio')
plt.grid(True)
plt.show()
```

Let's apply PCA with 100 principal components.

```python
pca = PCA(n_components=100)
X_pca = pca.fit_transform(X_flat)
explained_variance = pca.explained_variance_ratio_
cumulative_variance = np.cumsum(explained_variance)
```

Let's Plot explained variance ratio

```python
import matplotlib.pyplot as plt
plt.figure(figsize=(10, 6))
plt.plot(range(1, len(explained_variance) + 1), cumulative_variance, 'bo-')
plt.axhline(y=0.95, color='r', linestyle='--')
plt.xlabel('Number of Components')
plt.ylabel('Cumulative Explained Variance Ratio')
plt.title('PCA Explained Variance Ratio')
plt.grid(True)
plt.show()
```

Let's apply PCA with 200 principal components.

```python
pca = PCA(n_components=200)
X_pca = pca.fit_transform(X_flat)
explained_variance = pca.explained_variance_ratio_
cumulative_variance = np.cumsum(explained_variance)
```

Let's Plot explained variance ratio

```python
import matplotlib.pyplot as plt
plt.figure(figsize=(10, 6))
plt.plot(range(1, len(explained_variance) + 1), cumulative_variance, 'bo-')
plt.axhline(y=0.95, color='r', linestyle='--')
plt.xlabel('Number of Components')
plt.ylabel('Cumulative Explained Variance Ratio')
plt.title('PCA Explained Variance Ratio')
plt.grid(True)
plt.show()
```

Let's reconstruct a few images with 200 principal components.

```python
# Project and reconstruct a few images
X_pca_10 = pca.transform(X_flat[:10])
X_reconstructed = pca.inverse_transform(X_pca_10)
plt.figure(figsize=(10, 4))
for i in range(10):
    # Original
    plt.subplot(2, 10, i+1)
    plt.imshow(X_flat[i].reshape(28, 28), cmap='gray')
    plt.axis('off')
    if i == 0:
        plt.ylabel('Original')
    # Reconstructed
    plt.subplot(2, 10, i+11)
    plt.imshow(X_reconstructed[i].reshape(28, 28), cmap='gray')
    plt.axis('off')
    if i == 0:
        plt.ylabel('PCA (2D)')
plt.suptitle('Original vs. PCA-Reconstructed Images')
plt.show()
```

## Exercise 7: Data Validation

Data validation is a crucial step in ensuring the quality and reliability of our processed data. It helps us verify that our data cleaning and preprocessing steps have been successful and that the data is ready for modeling. In this exercise, we'll implement various validation checks and calculate quality metrics.

### 7.1 Data Quality Checks

We'll create a comprehensive validation function that performs various data quality checks:
1. Missing values: Ensures no unexpected missing values remain
2. Duplicates: Identifies any duplicate records
3. Data types: Verifies correct data types for each column
4. Infinite values: Checks for any infinite values that might cause issues

```python
def validate_data(df):
    """
    Perform various data quality checks
    """
    validation_results = {}
    
    # 1. Check for missing values
    missing_values = df.isnull().sum()
    validation_results['missing_values'] = missing_values[missing_values > 0]
    
    # 2. Check for duplicates
    duplicates = df.duplicated().sum()
    validation_results['duplicates'] = duplicates
    
    # 3. Check data types
    validation_results['dtypes'] = df.dtypes
    
    # 4. Check for infinite values
    inf_values = df.isin([np.inf, -np.inf]).sum()
    validation_results['infinite_values'] = inf_values[inf_values > 0]
    
    return validation_results
```

Let's run the validation checks on our processed dataset:

```python
# Perform validation
validation_results = validate_data(titanic_data_encoded)
print("\nValidation Results:")
for check, result in validation_results.items():
    print(f"\n{check}:")
    print(result)
```

### 7.2 Data Quality Metrics

In addition to basic validation checks, we'll calculate various data quality metrics to assess the overall quality of our dataset:

1. Completeness: Measures the proportion of non-missing values
2. Uniqueness: Measures the proportion of unique values
3. Consistency: Checks for logical consistency in the data

```python
def calculate_quality_metrics(df):
    """
    Calculate various data quality metrics
    """
    metrics = {}
    
    # 1. Completeness
    completeness = 1 - (df.isnull().sum() / len(df))
    metrics['completeness'] = completeness
    
    # 2. Uniqueness
    uniqueness = df.nunique() / len(df)
    metrics['uniqueness'] = uniqueness
    
    # 3. Consistency (check for negative values in positive-only columns)
    positive_columns = ['Age', 'Fare', 'SibSp', 'Parch']
    consistency = {}
    for col in positive_columns:
        if col in df.columns:
            consistency[col] = (df[col] >= 0).mean()
    metrics['consistency'] = consistency
    
    return metrics
```

Let's calculate and display the quality metrics:

```python
# Calculate metrics
quality_metrics = calculate_quality_metrics(titanic_data_encoded)
print("\nQuality Metrics:")
for metric, values in quality_metrics.items():
    print(f"\n{metric}:")
    print(values)
```

## Exercise 8: Image Preprocessing

Image preprocessing is a crucial step in preparing image data for machine learning models. In this exercise, we'll explore various techniques for preprocessing images using the MNIST dataset, which contains handwritten digits.

```python
from sklearn.datasets import fetch_openml
import numpy as np
import matplotlib.pyplot as plt
```

### 8.1 Loading and Exploring Image Data

```python
# Load MNIST dataset
X, y = fetch_openml('mnist_784', version=1, return_X_y=True, as_frame=False)
# Display basic information
print("Dataset shape:", X.shape)
print("Number of classes:", len(np.unique(y)))
print("Image dimensions:", int(np.sqrt(X.shape[1])), "x", int(np.sqrt(X.shape[1])))
```

Let's display some sample images

```python
# Display sample images
plt.figure(figsize=(10, 5))
for i in range(5):
    plt.subplot(1, 5, i+1)
    plt.imshow(X[i].reshape(28, 28), cmap='gray')
    plt.title(f'Label: {y[i]}')
    plt.axis('off')
plt.tight_layout()
plt.show()
```

### 8.2 Basic Image Preprocessing

Let's implement some image preprocessing techniques:

```python
from skimage.transform import resize
from sklearn.preprocessing import MinMaxScaler
```

Resize images to a smaller size (e.g., 20x20).

```python
def resize_images(images, target_size=(20, 20)):
    resized_images = np.array([resize(img.reshape(28, 28), target_size).flatten() 
                             for img in images])
    return resized_images
```

Normalize pixel values to [0, 1].

```python
def normalize_images(images):
    scaler = MinMaxScaler()
    return scaler.fit_transform(images)
```

Applying preprocessing.

```python
X_resized = resize_images(X[:1000])  # Process first 1000 images for demonstration
X_normalized = normalize_images(X_resized)
```

And we can visualize the effects of preprocessing.

```python
plt.figure(figsize=(15, 5))
index = np.random.random_integers(0,999)
for i in range(3):
    plt.subplot(1, 3, i+1)
    if i == 0:
        plt.imshow(X[index].reshape(28, 28), cmap='gray')
        plt.title('Original')
    elif i == 1:
        plt.imshow(X_resized[index].reshape(20, 20), cmap='gray')
        plt.title('Resized')
    else:
        plt.imshow(X_normalized[index].reshape(20, 20), cmap='gray')
        plt.title('Normalised')
    plt.axis('off')
plt.tight_layout()
plt.show()
```

### 8.3 Advanced Image Preprocessing

Some more advanced preprocessing techniques:

```python
from skimage.filters import sobel
from scipy.ndimage import gaussian_filter
from skimage.transform import rotate
```

Data augmentation: 

Adding random rotation and noise to make models robust to real-world variations in orientation or pixel values.

```python
def augment_image(image, angle_range=(-15, 15)):
    angle = np.random.uniform(angle_range[0], angle_range[1])
    rotated = rotate(image.reshape(20, 20), angle, mode='edge')
    noise = np.random.normal(0, 0.05, rotated.shape)
    augmented = rotated + (noise * (rotated > 0.1))
    return augmented.flatten()
```

Edge detection using the sobel filter to identify the boundaries of an image. It extracts the most significant features (e.g., shapes, contours, and boundaries).

```python
def detect_edges(image):
    edges = sobel(image.reshape(20, 20))
    return edges.flatten()
```

Noise reduction using Gaussian blur to improve image quality by removing random variations or unwanted artifacts from the images.

```python
def reduce_noise(image):
    blurred = gaussian_filter(image.reshape(20, 20), sigma=1)
    return blurred.flatten()
```

Applying the preprocessing techniques

```python
X_augmented = np.array([augment_image(img) for img in X_normalized[:100]])
X_edges = np.array([detect_edges(img) for img in X_normalized[:100]])
X_denoised = np.array([reduce_noise(img) for img in X_normalized[:100]])
```

Visualising the effects of the preprocessing

```python
plt.figure(figsize=(15, 5))
index = np.random.random_integers(0, 99)
for i in range(3):
    plt.subplot(1, 3, i+1)
    if i == 0:
        plt.imshow(X_augmented[index].reshape(20, 20), cmap='gray')
        plt.title('Augmented')
    elif i == 1:
        plt.imshow(X_edges[index].reshape(20, 20), cmap='gray')
        plt.title('Edge Detection')
    else:
        plt.imshow(X_denoised[index].reshape(20, 20), cmap='gray')
        plt.title('Noise Reduction')
    plt.axis('off')
plt.tight_layout()
plt.show()
```

### 8.4 Image Preprocessing Pipeline

Let's create a complete preprocessing pipeline that combines all the techniques:

```python
class ImagePreprocessor:
    def __init__(self, target_size=(20, 20)):
        self.target_size = target_size
        self.scaler = MinMaxScaler()
    
    def preprocess(self, images, augment=False):
        # 1. Resize
        resized = np.array([resize(img.reshape(28, 28), self.target_size).flatten() 
                          for img in images])
        
        # 2. Normalize
        normalized = self.scaler.fit_transform(resized)
        
        if augment:
            # 3. Augment
            augmented = np.array([augment_image(img) for img in normalized])
            return augmented
        
        return normalized
```

Creating and using the preprocessor

```python
preprocessor = ImagePreprocessor()
X_processed = preprocessor.preprocess(X[:1000], augment=True)
```

Visualising the final processed images

```python
plt.figure(figsize=(12, 5))
for i in range(5):
    # Original image
    plt.subplot(2, 5, i+1)
    plt.imshow(X[i].reshape(28, 28), cmap='gray')
    plt.title(f'Original {i+1}')
    plt.axis('off')
    # Processed image
    plt.subplot(2, 5, i+6)
    plt.imshow(X_processed[i].reshape(20, 20), cmap='gray')
    plt.title(f'Processed {i+1}')
    plt.axis('off')
plt.tight_layout()
plt.show()
```

<!-- end NOTEBOOK: -->

