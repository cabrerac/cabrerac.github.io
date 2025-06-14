<!-- NOTEBOOK: -->

# Practical Introduction

In this practical session, we will deepen our understanding of machine learning models (i.e., regression) and machine learning algorithms (e.g., batch gradient descent). But, before that we will clarify a couple of concepts from our previous session.

---

## Exercise 1: Data Augmentation and Statistical Testing

In this exercise, we will implement the augmentation technique of our last practical and then apply a statistical test to explore if our data is still valid after augmentation. As usual, we start importing the relevant variables.

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
```

The first step to understand the data. We'll use the [Titanic dataset](https://www.kaggle.com/c/titanic/data), which is perfect for learning data cleaning as it contains various data quality issues like missing values, outliers, and categorical variables. 

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

Now, let's prepare our data by selecting the numerical features we want to augment:

```python
numerical_features = ['Age', 'Fare', 'SibSp', 'Parch']
X_aug = titanic_data[numerical_features].fillna(titanic_data[numerical_features].mean())
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

We use the Kolmogorov-Smirnov test to compare the distributions of the original and augmented target variables.

```python
stat, p_value = ks_2samp(age_data, smote_augmented)
print(f"KS test p-value: {p_value}")
```

A high p-value in the KS test suggests that the augmented data is statistically similar to the original. This means our augmentation process has preserved the essential characteristics of the data, making it suitable for training more robust models.

We visualize the distributions and interpret the results.

```python
plt.hist(age_data, bins=30, alpha=0.5, label='Original Age')
plt.hist(smote_augmented, bins=30, alpha=0.5, label='Augmented Age')
plt.legend()
plt.title('Original vs Augmented Target Distribution')
plt.show()
```

---

## Exercise 2: PCA on High-Dimensional Data (Fashion-MNIST, TensorFlow)

### Introduction
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

---

## Exercise 3: Regression Models

Regression models are used to predict continuous outcomes. In this exercise, we will use the Bike Sharing dataset to build and evaluate a regression model.

We start by loading the dataset, selecting the relevant features and target, and preprocessing the data (including one-hot encoding and scaling).

```python
# Download from UCI: https://archive.ics.uci.edu/ml/datasets/Bike+Sharing+Dataset
url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/00275/Bike-Sharing-Dataset/day.csv'
bike_df = pd.read_csv(url)
# Select features and target
y = bike_df['cnt'].values
X = bike_df.drop(['instant', 'dteday', 'cnt', 'casual', 'registered'], axis=1)
# One-hot encode categorical features
cat_features = ['season', 'yr', 'mnth', 'holiday', 'weekday', 'workingday', 'weathersit']
X = pd.get_dummies(X, columns=cat_features)
# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
```

We split the data into training, validation, and test sets, then build a regression model using TensorFlow.

```python
X_train, X_temp, y_train, y_temp = train_test_split(X_scaled, y, test_size=0.3, random_state=42)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)
model = tf.keras.Sequential([
    tf.keras.layers.Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(1)
])
model.compile(optimizer='adam', loss='mse', metrics=['mae'])
```

We train the model and monitor its performance on the validation set.

```python
history = model.fit(X_train, y_train, epochs=50, validation_data=(X_val, y_val), verbose=0)
```

We evaluate the model on the test set to assess its generalisation performance.

```python
test_loss, test_mae = model.evaluate(X_test, y_test, verbose=0)
print(f"Test MAE: {test_mae:.2f}")
```

A low MAE on the test set indicates good predictive performance. Always compare validation and test results to check for overfitting.

---

## Exercise 4: Classification Models (Wine Quality Dataset, TensorFlow)

Classification models are used to predict categorical outcomes. In this exercise, we will use the Wine Quality dataset to build and evaluate a classification model.

We start by loading the dataset, converting the target to a binary classification problem, and scaling the features.

```python
# Download from UCI: https://archive.ics.uci.edu/ml/datasets/Wine+Quality
url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv'
wine_df = pd.read_csv(url, sep=';')
# Convert quality to binary classification (high quality >= 7)
wine_df['quality_label'] = (wine_df['quality'] >= 7).astype(int)
y = wine_df['quality_label'].values
X = wine_df.drop(['quality', 'quality_label'], axis=1)
# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
```

We split the data into training, validation, and test sets, then build a classification model using TensorFlow.

```python
X_train, X_temp, y_train, y_temp = train_test_split(X_scaled, y, test_size=0.3, random_state=42)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)
model = tf.keras.Sequential([
    tf.keras.layers.Dense(32, activation='relu', input_shape=(X_train.shape[1],)),
    tf.keras.layers.Dense(16, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
```

We train the model and monitor its performance on the validation set.

```python
history = model.fit(X_train, y_train, epochs=50, validation_data=(X_val, y_val), verbose=0)
```

We evaluate the model on the test set to assess its classification performance.

```python
test_loss, test_acc = model.evaluate(X_test, y_test, verbose=0)
print(f"Test Accuracy: {test_acc:.2f}")
```

A high accuracy on the test set indicates good classification performance. For imbalanced datasets, also consider precision, recall, and F1-score for a more complete evaluation.

---

## Homework - Regression and Classification

The homework assignment will help you apply the regression and classification techniques we've learned to a dataset of your choice. You may use a new dataset or continue with the one you defined in previous homeworks. Your task is to build a pipeline to apply a regression or a classification method, or both, depending on your dataset and interests.

You should provide a clear analysis and narrative of the different steps you used in your implementation, explaining your reasoning and choices throughout the process.

<DESCRIBE YOUR DATASET HERE>

```python
# Write your pipeline here
```

### Submission Guidelines

- Submit your solution as a Jupyter notebook with the following name format: `cease_ml_intro_session_5_<email_username>.ipynb`
- Include clear comments explaining your code
- Provide a written analysis of your results
- Provide a narrative and explanation of the different steps you used in your implementation
- Document any challenges faced and how you overcame them
- Due date: [19/06/2025]

<!-- end NOTEBOOK: -->

