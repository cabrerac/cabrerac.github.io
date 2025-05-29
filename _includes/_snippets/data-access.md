<!-- SLIDES: -->

## Data Access

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p><b>Does the data even exist?</b></p>
            </div>
        </div>
    </div>
</div>

## Data Access

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>No, it does not exist!</p>
            </div>
        </div>
    </div>
</div>

## Data Access

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Primary Data Collection</b></p>
                <ul>
                    <li>Questionnaires</li>
                    <li>Interviews</li>
                    <li>Focus group interviews</li>
                    <li>Surveys</li>
                    <li>Case studies</li>
                    <li>Process analysis</li>
                    <li>Experimental method</li>
                    <li>Statistical method</li>
                    <li>...</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>No, it does not exist!</p>
            </div>
        </div>
    </div>
</div>

## Data Access

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Primary Data Collection</b></p>
                <ul>
                    <li>Questionnaires</li>
                    <li>Interviews</li>
                    <li>Focus group interviews</li>
                    <li>Surveys</li>
                    <li>Case studies</li>
                    <li>Process analysis</li>
                    <li>Experimental method</li>
                    <li>Statistical method</li>
                    <li>...</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <ul>
                    <li>Expensive data collection processes</li>
                    <li>Particular methodologies</li>
                    <li>None fits all needs</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Data Access

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>Yes, it does exist!</p>
            </div>
        </div>
    </div>
</div>

## Data Access

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Secondary Data Collection</b></p>
                <ul>
                    <li>Published printed sources</li>
                    <li>Books, journals, magazines, newspapers</li>
                    <li>Government records</li>
                    <li>Census data</li>
                    <li>Public sector records</li>
                    <li>Electronic sources (e.g., public datasets, websites, etc.)</li>
                    <li>...</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>Yes, it does exist!</p>
            </div>
        </div>
    </div>
</div>

## Data Access

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Secondary Data Collection</b></p>
                <ul>
                    <li>Published printed sources</li>
                    <li>Books, journals, magazines, newspapers</li>
                    <li>Government records</li>
                    <li>Census data</li>
                    <li>Public sector records</li>
                    <li>Electronic sources (e.g., public datasets, websites, etc.)</li>
                    <li>...</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <ul>
                    <li>Validity and reliability concerns</li>
                    <li>Outdated data</li>
                    <li>Relevancy issue</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Data Access

## Data Access

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 30%">
                <p><b>Using your own files</b></p>
                <p>The most common are comma separated values files (i.e., CSV files).</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 70%">
            </div>
        </div>
    </div>
</div>

## Data Access

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 30%">
                <p><b>Using your own files</b></p>
                <p>The most common are comma separated values files (i.e., CSV files).</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 70%">

```python
import pandas as pd
dataset = pd.read_csv('path/to/your/dataset.csv')
print("Dataset shape:", dataset.shape)
print("\nFirst few rows:")
print(dataset.head())
```
</div>
        </div>
    </div>
</div>

## Data Access

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 30%">
                <p><b>Using built-in datasets</b></p>
                <p>Different repositories are available online. For example, <a href="https://www.openml.org/" target="_blank">OpenML</a> or <a href="https://www.tensorflow.org/datasets" target="_blank">Tensorflow datasets</a></p>
            </div>
            <div class="column vertical-middle text-left" style="width: 70%">
            </div>
        </div>
    </div>
</div>

## Data Access

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 30%">
                <p><b>Using built-in datasets</b></p>
                <p>Different datasets repositories are available online. For example, <a href="https://www.openml.org/" target="_blank">OpenML</a>, an open source platform for sharing datasets and experiments.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 70%">

```python
from sklearn.datasets import fetch_openml
iris = fetch_openml(name='iris', version=1, as_frame=True)
print("Iris dataset shape:", iris.data.shape)
print("\nFirst few rows:")
print(iris.data.head())
```
</div>
        </div>
    </div>
</div>

## Data Access

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 30%">
                <p><b>Using built-in datasets</b></p>
                <ul>
                    <li>The Iris dataset is a built-in dataset in scikit-learn</li>
                    <li>It contains 150 samples of iris flowers, each with 4 features</li>
                    <li>The target variable is the species of the iris flower</li>
                    <li>It is commonly used for classification tasks</li>
                    <li>Look at the dataset documentation, such as the <a href="https://www.geeksforgeeks.org/iris-dataset/" target="_blank">Iris dataset</a> documentation</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 70%">

```python
from sklearn.datasets import fetch_openml
iris = fetch_openml(name='iris', version=1, as_frame=True)
print("Iris dataset shape:", iris.data.shape)
print("\nFirst few rows:")
print(iris.data.head())
```
</div>
        </div>
    </div>
</div>

## Data Access

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 30%">
                <p><b>Using built-in datasets</b></p>
                <ul>
                    <li>Another popular dataset: CIFAR-10 from <a href="https://www.tensorflow.org/datasets" target="_blank">Tensorflow datasets</a></li>
                    <li>Contains 60,000 32x32 color images</li>
                    <li>10 different classes</li>
                    <li>Commonly used for image classification</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 70%">

```python
import tensorflow as tf
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.cifar10.load_data()
print("Training data shape:", x_train.shape)
print("Test data shape:", x_test.shape)
```
</div>
        </div>
    </div>
</div>

## Data Access

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 30%">
                <p><b>Accessing data via APIs</b></p>
                <ul>
                    <li>APIs are interfaces that allow different systems to communicate with each other</li>
                    <li>Servers expose these interfaces</li>
                    <li>Clients consume these interfaces (i.e., client-server architecture)</li>
                    <li>They communicate through the internet</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 70%">

```python
import requests
url = '<url_of_the_dataset>'
response = requests.get(url)
if response.status_code == 200:
  with open("." + file_name_part_1, "wb") as file:
    file.write(response.content)
```
</div>
        </div>
    </div>
</div>

## Data Access

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 30%">
                <p><b>Accessing data via APIs</b></p>
                <ul>
                    <li>The UK Price Paid data for housing in dates back to 1995 and contains millions of transactions</li>
                    <li>This database is available at <a href="https://www.gov.uk/government/statistical-data-sets/price-paid-data-downloads">gov.uk</a></li>
                    <li>The total data is over 4 gigabytes in size and it is available in a single file or in multiple files splitted by years and semester</li>
                    <li>The example downloads the data for the first semester of 2020</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 70%">

```python
import requests
url = 'http://prod.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com/pp-2020-part1.csv'
response = requests.get(url)
if response.status_code == 200:
  with open("." + file_name_part_1, "wb") as file:
    file.write(response.content)
```
</div>
        </div>
    </div>
</div>

## Data Access

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 30%">
                <p><b>Accessing data via APIs</b></p>
                <ul>
                    <li>The UK Price Paid data for housing in dates back to 1995 and contains millions of transactions</li>
                    <li>This database is available at <a href="https://www.gov.uk/government/statistical-data-sets/price-paid-data-downloads">gov.uk</a></li>
                    <li>The total data is over 4 gigabytes in size and it is available in a single file or in multiple files splitted by years and semester</li>
                    <li>The example downloads the data for the first semester of 2020</li>
                    <li>This can be read as a CSV file</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 70%">

```python
import requests
import pandas as pd
url = 'http://prod.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com/pp-2020-part1.csv'
response = requests.get(url)
if response.status_code == 200:
  with open("." + file_name_part_1, "wb") as file:
    file.write(response.content)
dataset = pd.read_csv('pp-2020-part1.csv')
print("Dataset shape:", dataset.shape)
print("\nFirst few rows:")
print(dataset.head())
```
</div>
        </div>
    </div>
</div>

## Data Access

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 30%">
                <p><b>Accessing data via APIs</b></p>
                <ul>
                    <li>OpenStreetMaps (OSM) is a collaborative project to create a free editable map of the world <a href="https://www.openstreetmap.org/#map=14/1.21711/-77.26727">Explore OSM</a>.</li>
                    <li>OSM enables the creation of custom maps, geospatial analysis, and location-based services</li>
                    <li>It is open sources and anyone can access it</li>
                    <li>The data lacks the structure we are used to</li>
                    <li>We need to install the Python module first</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 70%">

```python
pip install osmnx
```
</div>
        </div>
    </div>
</div>

## Data Access

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 30%">
                <p><b>Accessing data via APIs</b></p>
                <ul>
                    <li>This example shows how to download the points of interest (POIs) of Pasto, Nariño, Colombia, using Python and storing these in a CSV file</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 70%">

```python
import osmnx as ox
import pandas as pd
place = "Pasto, Nariño, Colombia"
pois = ox.features_from_place(place, tags={'amenity': True})
pois_df = pd.DataFrame(pois)
print(f"Number of POIs found: {len(pois_df)}")
print("\nSample of POIs:")
print(pois_df[['amenity', 'name']].head())
pois_df.to_csv('pasto_pois.csv', index=False)
```
</div>
        </div>
    </div>
</div>

## Data Access

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 30%">
                <p><b>Accessing data via APIs</b></p>
                <ul>
                    <li>We can also plot the city buildings</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 70%">

```python
import osmnx as ox
import pandas as pd
place = "Pasto, Nariño, Colombia"
buildings = ox.features_from_place(place, tags={'building': True})
buildings.plot()
```
</div>
        </div>
    </div>
</div>

## Data Access

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 30%">
                <p><b>Accessing data via APIs</b></p>
                <ul>
                    <li>We can also plot the city buildings</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 70%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/pasto-buildings.png" alt="Pasto Buildings" style="height: 500px">
            </div>
        </div>
    </div>
</div>


<!-- end SLIDES: -->

