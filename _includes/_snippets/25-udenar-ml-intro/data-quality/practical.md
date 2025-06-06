<!-- NOTEBOOK: -->

# Practical Introduction

In this practical session, we will explore different techniques for ensuring data quality in machine learning projects. We'll cover data cleaning, preprocessing, augmentation, feature engineering, and validation methods.

## Exercise 1: Data Cleaning

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

### 1.1 Loading and Exploring Data

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

### 1.2 Handling Missing Values

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

Median imputation: Replaces missing values with the meadian of the respective feature:
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

### 1.3 Handling Outliers

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

## Exercise 2: Data Preprocessing

Data preprocessing is a crucial step in preparing data for machine learning models. It involves transforming the data into a format that is suitable for analysis and modeling. In this exercise, we'll explore two main preprocessing techniques: feature scaling and categorical feature encoding.

### 2.1 Feature Scaling

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

### 2.2 Categorical Feature Encoding

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

## Exercise 3: Data Augmentation

Data augmentation helps us increase the size and diversity of our datasets. This is particularly important when we have limited data or want to improve model robustness. In this exercise, we'll explore different techniques for augmenting numerical data.

### 3.1 Numerical Data Augmentation

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
- Improve model generalization

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

Finally, let's analyze the statistical properties of the augmented data to understand how each technique affects the data distribution. This analysis helps us ensure that our augmentation techniques maintain the important characteristics of the original data while adding useful variations:

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

## Exercise 4: Feature Engineering

Feature engineering is the process of creating new features from existing data, transforming features, and selecting features to improve models performance. It requires domain knowledge and creativity. In this exercise, we'll explore different feature engineering techniques.

### 4.1 Creating New Features

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

### 4.2 Feature Selection

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

Now, let's apply Principal Component Analysis (PCA) as another feature engineering technique. PCA helps us reduce the dimensionality of our dataset by transforming the original features into a new set of variables (principal components) that capture the most variance in the data. This can make our models simpler, faster, and sometimes even more accurate.

First, we need to select the numerical features and standardize them, since PCA is sensitive to the scale of the data.

```python
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
# Select numerical features and fill NaNs with mean
numerical_features = ['Age', 'Fare', 'SibSp', 'Parch']
X_pca = data[numerical_features].fillna(data[numerical_features].mean())
# Standardize the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_pca)
```

Now, let's apply PCA and examine how much variance each principal component explains.

```python
pca = PCA()
X_pca_transformed = pca.fit_transform(X_scaled)
# Calculate explained variance ratio
explained_variance_ratio = pca.explained_variance_ratio_
cumulative_variance_ratio = np.cumsum(explained_variance_ratio)
```

Let's Plot explained variance ratio

```python
import matplotlib.pyplot as plt
plt.figure(figsize=(10, 6))
plt.plot(range(1, len(explained_variance_ratio) + 1), cumulative_variance_ratio, 'bo-')
plt.axhline(y=0.95, color='r', linestyle='--')
plt.xlabel('Number of Components')
plt.ylabel('Cumulative Explained Variance Ratio')
plt.title('PCA Explained Variance Ratio')
plt.grid(True)
plt.show()
```

Let's also print the explained variance for each component.

```python
print(\"\\nExplained variance ratio by component:\")
for i, ratio in enumerate(explained_variance_ratio):
    print(f\"Component {i+1}: {ratio:.4f}\")
```

Finally, we can visualize the data projected onto the first two principal components.

```python
import pandas as pd
pca_df = pd.DataFrame(
    data=X_pca_transformed,
    columns=[f'PC{i+1}' for i in range(X_pca_transformed.shape[1])]
)
plt.figure(figsize=(10, 8))
plt.scatter(pca_df['PC1'], pca_df['PC2'], alpha=0.5)
plt.xlabel('First Principal Component')
plt.ylabel('Second Principal Component')
plt.title('PCA: First Two Principal Components')
plt.grid(True)
plt.show()
```



### 4.3 Principal Component Analysis (PCA)

PCA (Principal Component Analysis) is a dimensionality reduction technique that is widely used in machine learning and data analysis. It works by transforming the data into a new coordinate system, where the axes are the principal components. These principal components are the directions of maximum variance in the data. The first principal component is the direction in which the data varies the most, the second principal component is the direction in which the data varies the second most, and so on. The number of principal components is equal to the number of original features.

The main idea behind PCA is to reduce the dimensionality of the data while retaining as much of the original variance as possible. This can be useful in several ways. For example, it can make the data easier to visualize, it can make the data easier to work with in machine learning algorithms, and it can help to remove noise from the data.

In practice, PCA is often used as a preprocessing step before applying a machine learning algorithm. The idea is to use PCA to reduce the dimensionality of the data, and then to apply the machine learning algorithm to the reduced data. This can make the machine learning algorithm faster and more accurate.

PCA is a linear transformation, which means that it can only capture linear relationships in the data. If the data has non-linear relationships, PCA may not work well. In this case, other dimensionality reduction techniques, such as t-SNE or UMAP, may be more appropriate.

PCA is a powerful dimensionality reduction technique that:
- Reduces the number of features while preserving important information
- Helps identify patterns in the data
- Can improve model performance by removing noise
- Makes visualization of high-dimensional data possible

The PCA process involves:
1. Standardizing the data
2. Finding the principal components (directions of maximum variance)
3. Projecting the data onto these components

Let's implement PCA:

```python
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
```

We start preparing the data for PCA.

```python
numerical_features = ['Age', 'Fare', 'SibSp', 'Parch', 'FamilySize']
X_pca = titanic_data[numerical_features].fillna(titanic_data[numerical_features].mean())
```

We then standarise the features and apply PCA.

```python
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_pca)
# Apply PCA
pca = PCA()
X_pca_transformed = pca.fit_transform(X_scaled)
```

We then analyse the results.

```python
# Calculate explained variance ratio
explained_variance_ratio = pca.explained_variance_ratio_
cumulative_variance_ratio = np.cumsum(explained_variance_ratio)
# Plot explained variance ratio
plt.figure(figsize=(10, 6))
plt.plot(range(1, len(explained_variance_ratio) + 1), 
         cumulative_variance_ratio, 'bo-')
plt.axhline(y=0.95, color='r', linestyle='--')
plt.xlabel('Number of Components')
plt.ylabel('Cumulative Explained Variance Ratio')
plt.title('PCA Explained Variance Ratio')
plt.grid(True)
plt.show()
```

We can analyse the variance for each component.

```python
# Print explained variance for each component
print("\nExplained variance ratio by component:")
for i, ratio in enumerate(explained_variance_ratio):
    print(f"Component {i+1}: {ratio:.4f}")
```

And continue our analysis of the principal components.

```python
# Create a DataFrame with PCA components
pca_df = pd.DataFrame(
    data=X_pca_transformed,
    columns=[f'PC{i+1}' for i in range(X_pca_transformed.shape[1])]
)
# Visualize the first two principal components
plt.figure(figsize=(10, 8))
plt.scatter(pca_df['PC1'], pca_df['PC2'], alpha=0.5)
plt.xlabel('First Principal Component')
plt.ylabel('Second Principal Component')
plt.title('PCA: First Two Principal Components')
plt.grid(True)
plt.show()
```

We can also examine the feature contributions to principal components.

```python
feature_contributions = pd.DataFrame(
    pca.components_.T,
    columns=[f'PC{i+1}' for i in range(pca.components_.shape[0])],
    index=numerical_features
)
print("\nFeature contributions to principal components:")
print(feature_contributions)
```

## Exercise 5: Data Validation

Data validation is a crucial step in ensuring the quality and reliability of our processed data. It helps us verify that our data cleaning and preprocessing steps have been successful and that the data is ready for modeling. In this exercise, we'll implement various validation checks and calculate quality metrics.

### 5.1 Data Quality Checks

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

### 5.2 Data Quality Metrics

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

## Exercise 6: Image Preprocessing

Image preprocessing is a crucial step in preparing image data for machine learning models. In this exercise, we'll explore various techniques for preprocessing images using the MNIST dataset, which contains handwritten digits.

```python
from sklearn.datasets import fetch_openml
import numpy as np
import matplotlib.pyplot as plt
```

### 6.1 Loading and Exploring Image Data

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

### 6.2 Basic Image Preprocessing

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

### 6.3 Advanced Image Preprocessing

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

### 6.4 Image Preprocessing Pipeline

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

## Homework - Data Quality

The homework assignment will help you apply the data quality techniques we've learned to real-world datasets. You'll need to:
1. Choose and analyze a dataset
2. Apply various data quality techniques
3. Compare different approaches
4. Document your findings

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

- [Dataset Transformations](https://scikit-learn.org/stable/data_transforms.html)


- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Scikit-learn Documentation](https://scikit-learn.org/stable/)
- [Data Cleaning Best Practices](https://towardsdatascience.com/data-cleaning-in-python-the-ultimate-guide-2020-c63b88bf0a0d)
- [Feature Engineering Guide](https://www.kaggle.com/code/ryanholbrook/feature-engineering)
- [Data Validation Techniques](https://towardsdatascience.com/data-validation-techniques-every-data-scientist-should-know-95c5d2c1e4f4)
- [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets.php)
- [Kaggle Datasets](https://www.kaggle.com/datasets)

<!-- end NOTEBOOK: --> 