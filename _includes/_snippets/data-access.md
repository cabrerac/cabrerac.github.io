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

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 30%">
                <p><b>Using built-in datasets</b></p>
                <p>Different datasets repositories are available online. For example, <a href="https://www.openml.org/" target="_blank">OpenML</a>, an open source platform for sharing datasets and experiments.</p>
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
import pandas as pd
import numpy as np
import requests
from sklearn.datasets import fetch_openml
import seaborn as sns
import matplotlib.pyplot as plt
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
                    <li>Import relevant libraries (e.g., <em>sklearn.datasets</em>)</li>
                    <li>Load a built-in dataset from scikit-learn</li>
                    <li>Initial exploration of the dataset properties</li>
                    <li>Look at the dataset documentation, such as the <a href="https://www.geeksforgeeks.org/iris-dataset/" target="_blank">Iris dataset</a></li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 70%">

```python
import pandas as pd
import numpy as np
import requests
from sklearn.datasets import fetch_openml
import seaborn as sns
import matplotlib.pyplot as plt
iris = fetch_openml(name='iris', version=1, as_frame=True)
print("Iris dataset shape:", iris.data.shape)
print("\nFirst few rows:")
print(iris.data.head())
```
</div>
        </div>
    </div>
</div>
<!-- end SLIDES: -->