<!-- NOTEBOOK: -->

# Practical Introduction

In this practical session, we will deepen our understanding of machine learning models and workflows using `TensorFlow` as an alternative framework to `scikit-learn`. But before, let's reinforce a couple of concepts from last time.

---

## Exercise 1: Data Augmentation with Linear Regression (Ames Housing, TensorFlow)

Data augmentation is a powerful technique to increase the diversity and robustness of your dataset, especially in regression tasks. In this exercise, we will use the Ames Housing dataset to generate synthetic data using a linear regression model. We will then validate that the augmented data is statistically similar to the original data.

As usual we start importing the relevant libraries.

```python
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
import tensorflow as tf
import matplotlib.pyplot as plt
from scipy.stats import ks_2samp
```

We start by loading the dataset, handling missing values, encoding categorical variables, and scaling features for modeling.

```python
# Load the Ames Housing dataset
df = pd.read_csv('https://raw.githubusercontent.com/ageron/handson-ml/master/datasets/housing/housing.csv')
# Preprocessing: handle missing values, encode categoricals, scale features
num_features = df.select_dtypes(include=[np.number]).columns.tolist()
cat_features = df.select_dtypes(include=[object]).columns.tolist()
preprocessor = ColumnTransformer([
    ("num", SimpleImputer(strategy="median"), num_features),
    ("cat", OneHotEncoder(handle_unknown="ignore"), cat_features)
])
X = preprocessor.fit_transform(df)
y = df['median_house_value'].values
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
```

We split the data and train a simple linear regression model using TensorFlow.

```python
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
model = tf.keras.Sequential([tf.keras.layers.Dense(1, input_shape=(X_train.shape[1],))])
model.compile(optimizer='adam', loss='mse')
model.fit(X_train, y_train, epochs=20, verbose=0)
```

We augment synthetic samples by adding Gaussian noise to the model's predictions.

```python
y_pred = model.predict(X_train).flatten()
noise = np.random.normal(0, y_pred.std() * 0.1, size=y_pred.shape)
y_augmented = y_pred + noise
```

We use the Kolmogorov-Smirnov test to compare the distributions of the original and augmented target variables.

```python
stat, p_value = ks_2samp(y_train, y_augmented)
print(f"KS test p-value: {p_value}")
```

We visualize the distributions and interpret the results.

```python
plt.hist(y_train, bins=30, alpha=0.5, label='Original')
plt.hist(y_augmented, bins=30, alpha=0.5, label='Augmented')
plt.legend()
plt.title('Original vs Augmented Target Distribution')
plt.show()
```

A high p-value in the KS test suggests that the augmented data is statistically similar to the original. This means our augmentation process has preserved the essential characteristics of the data, making it suitable for training more robust models.

---

## Exercise 2: PCA on High-Dimensional Data (Fashion-MNIST, TensorFlow)

### Introduction
High-dimensional data presents unique challenges in machine learning. Each image in the Fashion-MNIST dataset is 28x28 pixels, resulting in 784 features per sample. This high number of features makes visualization and modeling more complex, as patterns are harder to discern and computational requirements increase. Dimensionality reduction techniques like Principal Component Analysis (PCA) help us project this data into a lower-dimensional space while preserving as much of the original information as possible. In this exercise, we will explore the structure of Fashion-MNIST, visualize some images, and then apply PCA to see how the data can be represented in just two dimensions.

Let's start by loading the Fashion-MNIST dataset and visualizing some sample images to understand what our data looks like in its original high-dimensional form.

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

Now, let's apply PCA to reduce the dimensionality of our data from 784 features down to just 2 principal components. This will allow us to visualize the structure of the dataset in a 2D plot.

```python
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_flat)
```

We can now visualize the dataset in the new 2D PCA space. Each point represents an image, colored by its class label. Notice how some classes form distinct clusters, while others overlap.

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

The explained variance ratio tells us how much of the original data's information is retained in the principal components. With only two components, we capture a small fraction of the total variance, but enough to visualize the main structure of the data.

```python
print("Explained variance ratio:", pca.explained_variance_ratio_)
```

- The original Fashion-MNIST images are high-dimensional (784 features), making direct visualization and modeling challenging.
- PCA allows us to project this data into a lower-dimensional space, revealing structure and clusters that correspond to different classes.
- The reconstructed images from only two principal components are blurry and lack detail, illustrating the trade-off between dimensionality reduction and information loss.
- The explained variance ratio quantifies how much of the original information is preserved in the reduced space.

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

We evaluate the model on the test set to assess its generalization performance.

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

