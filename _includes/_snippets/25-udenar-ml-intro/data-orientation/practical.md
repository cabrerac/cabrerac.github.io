<!-- NOTEBOOK: -->

# Practical Introduction

In this practical session, we will explore different techniques for accessing and creating datasets for machine learning projects. We'll cover various scenarios where data might not be readily available and how to handle them.

## Exercise 1: Data Access Methods

Let's explore different ways to access data for ML projects:

```python
import pandas as pd
import numpy as np
import requests
from sklearn.datasets import fetch_openml
import seaborn as sns
import matplotlib.pyplot as plt
```

### 1.1 Using Built-in Datasets

```python
# Load a built-in dataset from scikit-learn
iris = fetch_openml(name='iris', version=1, as_frame=True)
print("Iris dataset shape:", iris.data.shape)
print("\nFirst few rows:")
print(iris.data.head())
```

### 1.2 Loading from CSV/Excel Files

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

### 1.3 Accessing Data via APIs

```python
def fetch_data_from_api(url, params=None):
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {str(e)}")
        return None

# Example usage with a public API
# Note: Replace with actual API endpoint
# data = fetch_data_from_api('https://api.example.com/data')
```

## Exercise 2: Creating Synthetic Data

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
        if X[i, 0] + X[i, 1] > 0:
            y[i] = 0
        elif X[i, 2] * X[i, 3] > 0:
            y[i] = 1
        else:
            y[i] = 2
    
    return X, y

# Generate and visualize synthetic data
X, y = generate_synthetic_data()
plt.figure(figsize=(10, 6))
plt.scatter(X[:, 0], X[:, 1], c=y, cmap='viridis')
plt.title('Synthetic Data Visualization')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.show()
```

## Exercise 3: Web Scraping for Data Collection

When data is available on websites but not through APIs, we can use web scraping:

```python
from bs4 import BeautifulSoup
import time

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

## Exercise 4: Data Quality Assessment

After accessing or creating data, it's important to assess its quality:

```python
def assess_data_quality(data):
    """
    Assess the quality of a dataset
    
    Parameters:
    -----------
    data : pandas.DataFrame
        Input dataset
        
    Returns:
    --------
    quality_report : dict
        Dictionary containing quality metrics
    """
    quality_report = {
        'missing_values': data.isnull().sum().to_dict(),
        'duplicates': data.duplicated().sum(),
        'data_types': data.dtypes.to_dict(),
        'basic_stats': data.describe().to_dict()
    }
    
    return quality_report

# Example usage with synthetic data
df = pd.DataFrame(X, columns=[f'feature_{i}' for i in range(X.shape[1])])
df['target'] = y
quality_report = assess_data_quality(df)
print("\nData Quality Report:")
print(quality_report)
```

## Tasks

1. **Data Access Exercise**:
   - Choose a public dataset from [Kaggle](https://www.kaggle.com/datasets) or [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/index.php)
   - Load the data using appropriate methods
   - Perform initial data quality assessment
   - Document any challenges encountered

2. **Synthetic Data Creation**:
   - Create a synthetic dataset for a specific problem (e.g., customer churn prediction, sales forecasting)
   - Ensure the synthetic data has realistic patterns and relationships
   - Validate the synthetic data using appropriate metrics

3. **Web Scraping Project**:
   - Identify a website with relevant data for your project
   - Implement a web scraper to collect the data
   - Clean and structure the collected data
   - Document the scraping process and any ethical considerations

## Submission Guidelines

- Submit your solution as a Jupyter notebook with the following name format: `cease_ml_intro_session_3_<email_username>.ipynb`
- Include clear comments explaining your code
- Provide a written analysis of your results
- Document any challenges faced and how you overcame them
- Due date: [05/06/2025]

## Resources

- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Beautiful Soup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Scikit-learn Datasets](https://scikit-learn.org/stable/datasets.html)
- [Web Scraping Best Practices](https://www.scrapehero.com/how-to-prevent-getting-blacklisted-while-scraping/)

<!-- end NOTEBOOK: -->