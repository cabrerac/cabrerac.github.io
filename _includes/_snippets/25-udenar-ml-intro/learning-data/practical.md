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

### Exercise 3.1: Simple Linear Regression

In this exercise, we will implement a simple linear regression model using scikit-learn. We'll focus on understanding how to:
1. Split data into training, validation, and test sets
2. Build and train a linear regression model
3. Evaluate the model's performance

Let's start by importing the necessary libraries:

```python
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import matplotlib.pyplot as plt
```

We'll use the Boston Housing dataset, which is a classic dataset for regression problems. It contains various features about houses in Boston suburbs and their median values.

```python
# Load the Boston Housing dataset
url = "https://raw.githubusercontent.com/selva86/datasets/master/BostonHousing.csv"
boston_data = pd.read_csv(url)
# Display basic information about the dataset
print("Dataset Shape:", boston_data.shape)
print("\nFirst few rows:")
print(boston_data.head())
```

Let's prepare our data by selecting features and target, and then scale the features:

```python
# Select features and target
X = boston_data.drop('medv', axis=1)  # Features
y = boston_data['medv']  # Target (median house value)
# Scale the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
# Split the data into training (60%), validation (20%), and test (20%) sets
X_train, X_temp, y_train, y_temp = train_test_split(X_scaled, y, test_size=0.4, random_state=42)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)
print(f"Training set size: {X_train.shape[0]}")
print(f"Validation set size: {X_val.shape[0]}")
print(f"Test set size: {X_test.shape[0]}")
```

Now, let's build and train a linear regression model:

```python
# Create and train the model
model = LinearRegression()
model.fit(X_train, y_train)
# Display model coefficients
print("\nModel Coefficients:")
for feature, coef in zip(boston_data.drop('medv', axis=1).columns, model.coef_):
    print(f"{feature}: {coef:.4f}")
print(f"\nIntercept: {model.intercept_:.4f}")
```

Let's evaluate the model on both training and validation sets:

```python
# Function to evaluate model performance
def evaluate_model(X, y, model):
    y_pred = model.predict(X)
    mse = mean_squared_error(y, y_pred)
    mae = mean_absolute_error(y, y_pred)
    r2 = r2_score(y, y_pred)
    return mse, mae, r2
# Evaluate on training set
train_mse, train_mae, train_r2 = evaluate_model(X_train, y_train, model)
print("\nTraining Set Performance:")
print(f"Mean Squared Error: {train_mse:.2f}")
print(f"Mean Absolute Error: {train_mae:.2f}")
print(f"R² Score: {train_r2:.2f}")
# Evaluate on validation set
val_mse, val_mae, val_r2 = evaluate_model(X_val, y_val, model)
print("\nValidation Set Performance:")
print(f"Mean Squared Error: {val_mse:.2f}")
print(f"Mean Absolute Error: {val_mae:.2f}")
print(f"R² Score: {val_r2:.2f}")
```

Finally, let's evaluate the model on the test set and visualise the results:

```python
# Evaluate on test set
test_mse, test_mae, test_r2 = evaluate_model(X_test, y_test, model)
print("\nTest Set Performance:")
print(f"Mean Squared Error: {test_mse:.2f}")
print(f"Mean Absolute Error: {test_mae:.2f}")
print(f"R² Score: {test_r2:.2f}")
# Make predictions on test set
y_pred = model.predict(X_test)
# Plot actual vs predicted values
plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_pred, alpha=0.5)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
plt.xlabel('Actual Values')
plt.ylabel('Predicted Values')
plt.title('Actual vs Predicted Values')
plt.tight_layout()
plt.show()
# Plot residuals
residuals = y_test - y_pred
plt.figure(figsize=(8, 6))
plt.scatter(y_pred, residuals, alpha=0.5)
plt.axhline(y=0, color='r', linestyle='--')
plt.xlabel('Predicted Values')
plt.ylabel('Residuals')
plt.title('Residual Plot')
plt.tight_layout()
plt.show()
```

The validation set helps us monitor the model's performance on unseen data during development, while the test set gives us a final assessment of the model's performance on completely unseen data.

### Exercise 3.2: Comparing Gradient Descent Algorithms

In this exercise, we will implement and compare three different gradient descent algorithms for linear regression:
1. Batch Gradient Descent (BGD)
2. Stochastic Gradient Descent (SGD)
3. Mini-batch Gradient Descent (MBGD)

We'll use a simplified version of the Boston Housing dataset, focusing on just one feature (e.g., 'rm' - average number of rooms) to fit a straight line.

```python
# Select only one feature for simplicity
X = boston_data[['rm']].values  # Average number of rooms
y = boston_data['medv'].values  # Target (median house value)
# Scale the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
# Split the data
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
```

Let's implement the three gradient descent algorithms:

```python
class LinearRegressionGD:
    def __init__(self, learning_rate=0.01, n_iterations=1000):
        self.learning_rate = learning_rate
        self.n_iterations = n_iterations
        self.weights = None
        self.costs = []
        
    def initialize_parameters(self, n_features):
        self.weights = np.zeros(n_features)
        
    def compute_cost(self, X, y):
        predictions = np.dot(X, self.weights)
        return np.mean((predictions - y) ** 2)
    
    def batch_gradient_descent(self, X, y):
        n_samples = X.shape[0]
        self.initialize_parameters(X.shape[1])
        for _ in range(self.n_iterations):
            # Compute predictions
            predictions = np.dot(X, self.weights)
            # Compute gradients
            dw = (1/n_samples) * np.dot(X.T, (predictions - y))
            db = (1/n_samples) * np.sum(predictions - y)
            # Update parameters
            self.weights -= self.learning_rate * dw
            # Store cost
            self.costs.append(self.compute_cost(X, y))
            
    def stochastic_gradient_descent(self, X, y):
        n_samples = X.shape[0]
        self.initialize_parameters(X.shape[1])
        for _ in range(self.n_iterations):
            for i in range(n_samples):
                # Select one random sample
                idx = np.random.randint(0, n_samples)
                X_i = X[idx:idx+1]
                y_i = y[idx:idx+1]
                # Compute prediction
                prediction = np.dot(X_i, self.weights)
                # Compute gradients
                dw = np.dot(X_i.T, (prediction - y_i))
                db = np.sum(prediction - y_i)
                # Update parameters
                self.weights -= self.learning_rate * dw
            # Store cost
            self.costs.append(self.compute_cost(X, y))
            
    def mini_batch_gradient_descent(self, X, y, batch_size=32):
        n_samples = X.shape[0]
        self.initialize_parameters(X.shape[1])
        for _ in range(self.n_iterations):
            # Shuffle the data
            indices = np.random.permutation(n_samples)
            X_shuffled = X[indices]
            y_shuffled = y[indices]
            # Process mini-batches
            for i in range(0, n_samples, batch_size):
                X_batch = X_shuffled[i:i+batch_size]
                y_batch = y_shuffled[i:i+batch_size]
                # Compute predictions
                predictions = np.dot(X_batch, self.weights)
                # Compute gradients
                dw = (1/batch_size) * np.dot(X_batch.T, (predictions - y_batch))
                db = (1/batch_size) * np.sum(predictions - y_batch)
                # Update parameters
                self.weights -= self.learning_rate * dw
            # Store cost
            self.costs.append(self.compute_cost(X, y))
    def predict(self, X):
        return np.dot(X, self.weights)
```

Now, let's train and compare the three algorithms:

```python
# Initialize models
bgd_model = LinearRegressionGD(learning_rate=0.01, n_iterations=100)
sgd_model = LinearRegressionGD(learning_rate=0.01, n_iterations=100)
mbgd_model = LinearRegressionGD(learning_rate=0.01, n_iterations=100)
# Train models
bgd_model.batch_gradient_descent(X_train, y_train)
sgd_model.stochastic_gradient_descent(X_train, y_train)
mbgd_model.mini_batch_gradient_descent(X_train, y_train)
```

Let's plot the cost of each algorithm to compare them.

```python
# Plot cost history
plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.plot(bgd_model.costs, label='Batch GD')
plt.plot(sgd_model.costs, label='Stochastic GD')
plt.plot(mbgd_model.costs, label='Mini-batch GD')
plt.xlabel('Iteration')
plt.ylabel('Cost')
plt.title('Cost History')
plt.legend()
# Plot final results
plt.subplot(1, 2, 2)
plt.scatter(X_test, y_test, alpha=0.5, label='Actual')
x_line = np.linspace(X_test.min(), X_test.max(), 100).reshape(-1, 1)
plt.plot(x_line, bgd_model.predict(x_line), 'r-', label='Batch GD')
plt.plot(x_line, sgd_model.predict(x_line), 'g-', label='Stochastic GD')
plt.plot(x_line, mbgd_model.predict(x_line), 'b-', label='Mini-batch GD')
plt.xlabel('Number of Rooms (scaled)')
plt.ylabel('House Price')
plt.title('Model Predictions')
plt.legend()
plt.tight_layout()
plt.show()
# Print final costs
print("\nFinal Costs:")
print(f"Batch GD: {bgd_model.costs[-1]:.2f}")
print(f"Stochastic GD: {sgd_model.costs[-1]:.2f}")
print(f"Mini-batch GD: {mbgd_model.costs[-1]:.2f}")
```

The visualisation shows how each algorithm's cost function decreases over time and how the final fitted lines compare to each other.

---

## Homework - Regression and Classification

The homework assignment will help you applying linear regression algorithms we've learned to a dataset of your choice. You may use a new dataset or continue with the one you defined in previous homeworks. Your task is to use the implementation of the Gradient Descent algorithms in this practical to build a pipeline that applies linear regression in your data and evaluates the results with different hyperparameter values. You are free to explore as much as you wish!

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

