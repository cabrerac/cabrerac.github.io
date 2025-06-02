<!-- NOTEBOOK: -->

# Practical Introduction

In this practical session, we will explore different techniques for ensuring data quality in machine learning projects. We'll cover data cleaning, preprocessing, feature engineering, and validation methods.

## Exercise 1: Data Cleaning

Let's start by importing the necessary libraries and loading a sample dataset that needs cleaning.

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.feature_selection import SelectKBest, f_classif
```

### 1.1 Loading and Exploring Data

First, let's load a dataset with various data quality issues. We'll use the Titanic dataset as it contains several common data quality challenges.

```python
# Load the Titanic dataset
url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
titanic_data = pd.read_csv(url)

# Display basic information about the dataset
print("Dataset Shape:", titanic_data.shape)
print("\nFirst few rows:")
print(titanic_data.head())
print("\nDataset Info:")
print(titanic_data.info())
```

### 1.2 Handling Missing Values

Let's analyze and handle missing values in the dataset.

```python
# Check for missing values
missing_values = titanic_data.isnull().sum()
print("Missing values per column:")
print(missing_values[missing_values > 0])

# Visualize missing values
plt.figure(figsize=(10, 6))
sns.heatmap(titanic_data.isnull(), yticklabels=False, cbar=False, cmap='viridis')
plt.title('Missing Values Heatmap')
plt.show()

# Handle missing values in Age using different strategies
# 1. Mean imputation
mean_imputer = SimpleImputer(strategy='mean')
titanic_data['Age_Mean'] = mean_imputer.fit_transform(titanic_data[['Age']])

# 2. Median imputation
median_imputer = SimpleImputer(strategy='median')
titanic_data['Age_Median'] = median_imputer.fit_transform(titanic_data[['Age']])

# 3. KNN imputation
knn_imputer = KNNImputer(n_neighbors=5)
titanic_data['Age_KNN'] = knn_imputer.fit_transform(titanic_data[['Age']])

# Compare the different imputation strategies
plt.figure(figsize=(15, 5))
plt.subplot(1, 3, 1)
sns.histplot(data=titanic_data, x='Age_Mean', bins=30)
plt.title('Mean Imputation')
plt.subplot(1, 3, 2)
sns.histplot(data=titanic_data, x='Age_Median', bins=30)
plt.title('Median Imputation')
plt.subplot(1, 3, 3)
sns.histplot(data=titanic_data, x='Age_KNN', bins=30)
plt.title('KNN Imputation')
plt.tight_layout()
plt.show()
```

### 1.3 Handling Outliers

Let's identify and handle outliers in the numerical features.

```python
# Function to detect outliers using IQR method
def detect_outliers(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return df[(df[column] < lower_bound) | (df[column] > upper_bound)]

# Detect outliers in Fare
outliers = detect_outliers(titanic_data, 'Fare')
print(f"Number of outliers in Fare: {len(outliers)}")

# Visualize outliers
plt.figure(figsize=(10, 6))
sns.boxplot(x=titanic_data['Fare'])
plt.title('Fare Distribution with Outliers')
plt.show()

# Handle outliers using different strategies
# 1. Capping
def cap_outliers(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    df[column + '_capped'] = df[column].clip(lower=lower_bound, upper=upper_bound)
    return df

# 2. Log transformation
titanic_data['Fare_log'] = np.log1p(titanic_data['Fare'])

# Apply capping
titanic_data = cap_outliers(titanic_data, 'Fare')

# Compare the different strategies
plt.figure(figsize=(15, 5))
plt.subplot(1, 3, 1)
sns.histplot(data=titanic_data, x='Fare', bins=30)
plt.title('Original Fare')
plt.subplot(1, 3, 2)
sns.histplot(data=titanic_data, x='Fare_capped', bins=30)
plt.title('Capped Fare')
plt.subplot(1, 3, 3)
sns.histplot(data=titanic_data, x='Fare_log', bins=30)
plt.title('Log-transformed Fare')
plt.tight_layout()
plt.show()
```

## Exercise 2: Data Preprocessing

### 2.1 Feature Scaling

Let's explore different scaling techniques for numerical features.

```python
# Select numerical features for scaling
numerical_features = ['Age', 'Fare', 'SibSp', 'Parch']

# 1. Standardization (Z-score normalization)
scaler = StandardScaler()
titanic_data[numerical_features + '_standardized'] = scaler.fit_transform(titanic_data[numerical_features])

# 2. Min-Max scaling
minmax_scaler = MinMaxScaler()
titanic_data[numerical_features + '_minmax'] = minmax_scaler.fit_transform(titanic_data[numerical_features])

# Compare the different scaling techniques
plt.figure(figsize=(15, 5))
plt.subplot(1, 3, 1)
sns.histplot(data=titanic_data, x='Age', bins=30)
plt.title('Original Age')
plt.subplot(1, 3, 2)
sns.histplot(data=titanic_data, x='Age_standardized', bins=30)
plt.title('Standardized Age')
plt.subplot(1, 3, 3)
sns.histplot(data=titanic_data, x='Age_minmax', bins=30)
plt.title('Min-Max Scaled Age')
plt.tight_layout()
plt.show()
```

### 2.2 Categorical Feature Encoding

Let's handle categorical features using different encoding techniques.

```python
# Select categorical features
categorical_features = ['Sex', 'Embarked', 'Pclass']

# 1. One-hot encoding
titanic_data_encoded = pd.get_dummies(titanic_data, columns=categorical_features, prefix=categorical_features)

# 2. Label encoding
from sklearn.preprocessing import LabelEncoder
label_encoder = LabelEncoder()
titanic_data['Sex_encoded'] = label_encoder.fit_transform(titanic_data['Sex'])

# Compare the encoding techniques
print("\nOne-hot encoding example:")
print(titanic_data_encoded[['Sex_female', 'Sex_male']].head())
print("\nLabel encoding example:")
print(titanic_data[['Sex', 'Sex_encoded']].head())
```

## Exercise 3: Feature Engineering

### 3.1 Creating New Features

Let's create some new features that might be useful for the Titanic survival prediction.

```python
# 1. Family size
titanic_data['FamilySize'] = titanic_data['SibSp'] + titanic_data['Parch'] + 1

# 2. Title from Name
titanic_data['Title'] = titanic_data['Name'].str.extract(' ([A-Za-z]+)\.', expand=False)

# 3. Cabin information
titanic_data['HasCabin'] = titanic_data['Cabin'].notna().astype(int)

# 4. Age groups
titanic_data['AgeGroup'] = pd.cut(titanic_data['Age'], 
                                 bins=[0, 12, 18, 35, 60, 100],
                                 labels=['Child', 'Teenager', 'Young Adult', 'Adult', 'Senior'])

# Display the new features
print("\nNew features:")
print(titanic_data[['FamilySize', 'Title', 'HasCabin', 'AgeGroup']].head())
```

### 3.2 Feature Selection

Let's use different feature selection techniques to identify the most important features.

```python
# Prepare data for feature selection
X = titanic_data_encoded.select_dtypes(include=[np.number]).dropna()
y = titanic_data['Survived']

# 1. Univariate feature selection
selector = SelectKBest(score_func=f_classif, k=5)
X_selected = selector.fit_transform(X, y)

# Get selected feature names
selected_features = X.columns[selector.get_support()].tolist()
print("\nSelected features using univariate selection:")
print(selected_features)

# 2. Correlation analysis
correlation_matrix = titanic_data_encoded.corr()
plt.figure(figsize=(12, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
plt.title('Feature Correlation Matrix')
plt.show()
```

## Exercise 4: Data Validation

### 4.1 Data Quality Checks

Let's implement some data quality checks to ensure our dataset meets certain criteria.

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

# Perform validation
validation_results = validate_data(titanic_data_encoded)
print("\nValidation Results:")
for check, result in validation_results.items():
    print(f"\n{check}:")
    print(result)
```

### 4.2 Data Quality Metrics

Let's calculate some data quality metrics for our dataset.

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

# Calculate metrics
quality_metrics = calculate_quality_metrics(titanic_data_encoded)
print("\nQuality Metrics:")
for metric, values in quality_metrics.items():
    print(f"\n{metric}:")
    print(values)
```

## Homework - Data Quality

1. Choose a dataset from the [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets.php) or [Kaggle](https://www.kaggle.com/datasets) that interests you. Apply the data quality techniques we've learned to prepare it for machine learning.

<DESCRIBE YOUR DATASET HERE>

```python
# Write the code to load and prepare your dataset here
```

2. For the health facilities dataset we used in the previous practical session, apply the data quality techniques we've learned. Consider the following aspects:
   - Handle missing values appropriately
   - Deal with outliers in numerical features
   - Scale numerical features
   - Encode categorical features
   - Create new features that might be useful
   - Validate the quality of the processed data

```python
# Write your code to improve the quality of the health facilities dataset
```

3. Compare different data quality techniques and their impact on model performance. Use a simple classification or regression model to evaluate how different preprocessing steps affect the results.

```python
# Write your code to compare different data quality techniques
```

### Submission Guidelines

- Submit your solution as a Jupyter notebook with the following name format: `cease_ml_intro_session_4_<email_username>.ipynb`
- Include clear comments explaining your code
- Provide a written analysis of your results
- Document any challenges faced and how you overcame them
- Due date: [12/06/2025]

## Resources

- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Scikit-learn Documentation](https://scikit-learn.org/stable/)
- [Data Cleaning Best Practices](https://towardsdatascience.com/data-cleaning-in-python-the-ultimate-guide-2020-c63b88bf0a0d)
- [Feature Engineering Guide](https://www.kaggle.com/code/ryanholbrook/feature-engineering)
- [Data Validation Techniques](https://towardsdatascience.com/data-validation-techniques-every-data-scientist-should-know-95c5d2c1e4f4)
- [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets.php)
- [Kaggle Datasets](https://www.kaggle.com/datasets)

<!-- end NOTEBOOK: --> 