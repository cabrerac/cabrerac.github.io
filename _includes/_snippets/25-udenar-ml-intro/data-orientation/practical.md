<!-- NOTEBOOK: -->

# Practical Introduction

In this practical session, we will explore different methods to access datasets for machine learning projects. We'll cover various scenarios where data might not be readily available.

## Exercise 1: Structured Data Access Methods

Let's explore different ways to access data for ML projects, but first let's import the basic libraries.

```python
import pandas as pd
import numpy as np
```

### 1.2 Loading from CSV/Excel Files

We can access local dataset files, which are normally stored as CSV (Comma Separeted Values) files. Let's define a function we can use and reuse.

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
# Example usage with a public API
# Note: Replace with actual API endpoint
# data = fetch_data_from_api('https://api.example.com/data')
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
buildings = get_pois(place, {"amenity": "building"})
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

## Exercise 3: Web Scraping for Data Collection

When data is available on websites but not through APIs, we can use web scraping.

```python
from bs4 import BeautifulSoup
def scrape_web_data(url):
    """
    Scrape data from a webpage
    
    Parameters:
    -----------
    url : str
        URL of the webpage to scrape
        
    Returns:
    --------
    data : list
        List of scraped data
    """
    try:
        # Add headers to mimic a browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Make the request
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # Parse the HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Example: Extract all paragraph text
        # Modify this based on the actual webpage structure
        data = [p.text for p in soup.find_all('p')]
        
        return data
    
    except Exception as e:
        print(f"Error scraping data: {str(e)}")
        return None
# Example usage:
# data = scrape_web_data('https://example.com')
```

Let's use our function to scrape data from the course website. We will extract the course information and lecture details.

```python
# URL of the course website
url = "https://cabrerac.github.io/teaching/25-udenar-ml-intro/"
# Scrape the data
course_data = scrape_web_data(url)
```

We can manipulate the scrapped data now. We should consider the structure of the website when doing so.

```python
if course_data is not None:
    print("Course Information:")
    for item in course_data:
        print(f"- {item}")
    # Extract lecture information
    soup = BeautifulSoup(requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}).text, 'html.parser')
    lectures = soup.find_all('li')
    print("\nLecture Schedule:")
    for lecture in lectures:
        if lecture.text:
            print(f"- {lecture.text}")
```

## Exercise 4: Creating Synthetic Data

When real data is not available, we can create synthetic data that mimics real-world patterns:

```python
def generate_synthetic_data(n_samples=1000, n_features=5, n_classes=3):
    """
    Generate synthetic data for classification problems
    
    Parameters:
    -----------
    n_samples : int
        Number of samples to generate
    n_features : int
        Number of features
    n_classes : int
        Number of classes
        
    Returns:
    --------
    X : array-like
        Feature matrix
    y : array-like
        Target vector
    """
    # Generate random features
    X = np.random.randn(n_samples, n_features)
    
    # Generate target variable based on feature relationships
    y = np.zeros(n_samples)
    for i in range(n_samples):
        # Create some pattern in the data
        if X[i, 0] + X[i, 1] > 0: # y is 0 when the sum of first two features is positive 
            y[i] = 0
        elif X[i, 2] * X[i, 3] > 0: # y is 1 when the product of third and fourht features is positive 
            y[i] = 1
        else: # y is 2 when the above conditions are not satisfied
            y[i] = 2
    
    return X, y
```

We can then generate and visualise the synthetic data.

```python
# Generate and visualize synthetic data
X, y = generate_synthetic_data()
plt.figure(figsize=(10, 6))
plt.scatter(X[:, 0], X[:, 1], c=y, cmap='viridis')
plt.title('Synthetic Data Visualization')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.show()
```

## Homework - Data Access

1. Define a dataset for the problem you want to address using machine learning. The ML Project Canvas from last time can help you to start defining your data needs. If you do not find an available dataset, you are free to create a synthetic one or to change your project according to the data that is available.

<DESCRIBE YOUR DATASET HERE - REFER TO YOUR CANVAS WHERE NEEDED>

```python
# Write the code you need to access/create your dataset here
```

2. [The Humanitarian Data Exchange](https://data.humdata.org/) is a repository where you can find, share, and use humanitarian data. This platform has [datasets related to Colombia](https://data.humdata.org/group/col). For example, this is a [dataset of the health facilities in Colombia](https://data.humdata.org/dataset/colombia-health-facilities-2021). We can access this dataset programatically using the function we created in above.

```python
# URL of the dataset
url = "https://data.humdata.org/dataset/9df9c9a5-cbd1-4d52-a292-8ac392f155a4/resource/7cce7e88-19b3-4e22-890e-884cd8328e70/download/registro_especial_de_prestadores_y_sedes_de_servicios_de_salud_20241120.csv"
# Write your code to access and manipulate the health facilities in Colombia
```

Can you combine the health facilities data with OpenStreetMaps to create a new dataset?

```python
# Write your code to combine the datasets
```

The repository has more datasets for the Colombian context. Explore it and think about the first task of this homework. You can get inspiration for your ML projects based on the available data.


### Submission Guidelines

- Submit your solution as a Jupyter notebook with the following name format: `cease_ml_intro_session_3_<email_username>.ipynb`
- Include clear comments explaining your code
- Provide a written analysis of your results
- Document any challenges faced and how you overcame them
- Due date: [05/06/2025]

## Resources

- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [OpenML Datasets](https://www.openml.org/)
- [Tensorflow Datasets](https://www.tensorflow.org/datasets)
- [Iris Dataset](https://www.geeksforgeeks.org/iris-dataset/)
- [UK Price Paid Dataset](https://www.gov.uk/government/statistical-data-sets/price-paid-data-downloads)
- [Open Postcode Geo Dataset](https://www.getthedata.com/open-postcode-geo)
- [Open Street Maps API](https://wiki.openstreetmap.org/wiki/API)
- [Beautiful Soup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Web Scraping Best Practices](https://www.scrapehero.com/how-to-prevent-getting-blacklisted-while-scraping/)

<!-- end NOTEBOOK: -->

