<!-- NOTEBOOK: -->

# Practical Introduction

In this practical session, we will explore ML model deployment concepts and tools. We'll build a simple model serving system, implement monitoring, and learn about production deployment practices.

---

## Exercise 1: Building a Simple Model Server

In this exercise, we'll create a basic model serving system using Flask to understand the fundamentals of ML model deployment.

Let's start by importing the necessary libraries:

```python
import pickle
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import os
```

Let's create a simple dataset and train a model:

```python
# Create a synthetic dataset
X, y = make_classification(n_samples=1000, n_features=10, n_classes=2, random_state=42)

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a simple model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model accuracy: {accuracy:.4f}")

# Save the model
model_path = "model.pkl"
joblib.dump(model, model_path)
print(f"Model saved to {model_path}")
```

Now let's create a simple Flask application to serve the model:

```python
app = Flask(__name__)

# Load the model
@app.before_first_request
def load_model():
    global model
    model = joblib.load(model_path)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get input data
        data = request.get_json()
        
        if not data or 'features' not in data:
            return jsonify({'error': 'No features provided'}), 400
        
        # Convert to numpy array
        features = np.array(data['features']).reshape(1, -1)
        
        # Make prediction
        prediction = model.predict(features)[0]
        probability = model.predict_proba(features)[0].tolist()
        
        return jsonify({
            'prediction': int(prediction),
            'probability': probability,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

Let's test our model server:

```python
import requests
import json

# Test the model server
def test_prediction(features):
    url = "http://localhost:5000/predict"
    data = {"features": features}
    
    response = requests.post(url, json=data)
    return response.json()

# Test with some sample data
sample_features = X_test[0].tolist()
result = test_prediction(sample_features)
print("Prediction result:")
print(json.dumps(result, indent=2))
```

---

## Exercise 2: Model Versioning and Registry

In this exercise, we'll implement a simple model versioning system to track different model versions and their metadata.

```python
import hashlib
import datetime
import json
from pathlib import Path

class ModelRegistry:
    def __init__(self, registry_path="model_registry"):
        self.registry_path = Path(registry_path)
        self.registry_path.mkdir(exist_ok=True)
        self.metadata_file = self.registry_path / "metadata.json"
        self.load_metadata()
    
    def load_metadata(self):
        if self.metadata_file.exists():
            with open(self.metadata_file, 'r') as f:
                self.metadata = json.load(f)
        else:
            self.metadata = {"models": {}}
    
    def save_metadata(self):
        with open(self.metadata_file, 'w') as f:
            json.dump(self.metadata, f, indent=2)
    
    def register_model(self, model, model_name, version, metrics, features):
        # Create model hash
        model_bytes = pickle.dumps(model)
        model_hash = hashlib.md5(model_bytes).hexdigest()
        
        # Save model file
        model_filename = f"{model_name}_v{version}.pkl"
        model_path = self.registry_path / model_filename
        joblib.dump(model, model_path)
        
        # Update metadata
        model_info = {
            "version": version,
            "hash": model_hash,
            "created_at": datetime.datetime.now().isoformat(),
            "metrics": metrics,
            "features": features,
            "file_path": str(model_path)
        }
        
        if model_name not in self.metadata["models"]:
            self.metadata["models"][model_name] = {}
        
        self.metadata["models"][model_name][version] = model_info
        self.save_metadata()
        
        return model_info
    
    def get_model(self, model_name, version):
        if model_name in self.metadata["models"] and version in self.metadata["models"][model_name]:
            model_info = self.metadata["models"][model_name][version]
            model_path = model_info["file_path"]
            return joblib.load(model_path), model_info
        else:
            raise ValueError(f"Model {model_name} version {version} not found")
    
    def list_models(self):
        return self.metadata["models"]

# Test the model registry
registry = ModelRegistry()

# Register our model
model_metrics = {
    "accuracy": accuracy,
    "n_samples": len(X_train),
    "n_features": X_train.shape[1]
}

model_features = [f"feature_{i}" for i in range(X_train.shape[1])]

model_info = registry.register_model(
    model=model,
    model_name="random_forest_classifier",
    version="1.0.0",
    metrics=model_metrics,
    features=model_features
)

print("Registered model info:")
print(json.dumps(model_info, indent=2))

# List all models
print("\nAll registered models:")
print(json.dumps(registry.list_models(), indent=2))
```

---

## Exercise 3: Model Monitoring and Drift Detection

In this exercise, we'll implement basic model monitoring and data drift detection.

```python
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

class ModelMonitor:
    def __init__(self, reference_data):
        self.reference_data = reference_data
        self.reference_stats = self._compute_statistics(reference_data)
    
    def _compute_statistics(self, data):
        """Compute basic statistics for each feature."""
        stats_dict = {}
        for i in range(data.shape[1]):
            feature_data = data[:, i]
            stats_dict[f"feature_{i}"] = {
                "mean": np.mean(feature_data),
                "std": np.std(feature_data),
                "min": np.min(feature_data),
                "max": np.max(feature_data),
                "percentiles": np.percentile(feature_data, [25, 50, 75])
            }
        return stats_dict
    
    def detect_drift(self, new_data, threshold=0.05):
        """Detect data drift using statistical tests."""
        drift_report = {}
        
        for i in range(new_data.shape[1]):
            feature_name = f"feature_{i}"
            new_feature = new_data[:, i]
            ref_feature = self.reference_data[:, i]
            
            # Perform Kolmogorov-Smirnov test
            ks_stat, p_value = stats.ks_2samp(ref_feature, new_feature)
            
            # Check for significant drift
            is_drifted = p_value < threshold
            
            drift_report[feature_name] = {
                "ks_statistic": ks_stat,
                "p_value": p_value,
                "is_drifted": is_drifted,
                "drift_severity": "high" if p_value < 0.01 else "medium" if p_value < 0.05 else "low"
            }
        
        return drift_report
    
    def plot_drift_analysis(self, new_data):
        """Plot drift analysis for visual inspection."""
        n_features = new_data.shape[1]
        fig, axes = plt.subplots(2, n_features, figsize=(4*n_features, 8))
        
        for i in range(n_features):
            feature_name = f"feature_{i}"
            new_feature = new_data[:, i]
            ref_feature = self.reference_data[:, i]
            
            # Histogram comparison
            axes[0, i].hist(ref_feature, alpha=0.5, label='Reference', bins=20)
            axes[0, i].hist(new_feature, alpha=0.5, label='New Data', bins=20)
            axes[0, i].set_title(f'{feature_name} Distribution')
            axes[0, i].legend()
            
            # Q-Q plot
            stats.probplot(new_feature, dist="norm", plot=axes[1, i])
            axes[1, i].set_title(f'{feature_name} Q-Q Plot')
        
        plt.tight_layout()
        plt.show()

# Create monitor with training data as reference
monitor = ModelMonitor(X_train)

# Simulate new data (with some drift)
np.random.seed(123)
drifted_data = X_test + np.random.normal(0, 0.5, X_test.shape)  # Add noise to simulate drift

# Detect drift
drift_report = monitor.detect_drift(drifted_data)
print("Drift Detection Report:")
print(json.dumps(drift_report, indent=2))

# Plot drift analysis
monitor.plot_drift_analysis(drifted_data)
```

---

## Exercise 4: Model Performance Monitoring

In this exercise, we'll implement a simple performance monitoring system to track model predictions and performance metrics over time.

```python
import sqlite3
from datetime import datetime, timedelta

class PerformanceMonitor:
    def __init__(self, db_path="model_performance.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create predictions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                model_version TEXT,
                features TEXT,
                prediction INTEGER,
                probability REAL,
                actual_label INTEGER,
                response_time REAL
            )
        ''')
        
        # Create performance metrics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS performance_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                model_version TEXT,
                accuracy REAL,
                precision REAL,
                recall REAL,
                f1_score REAL,
                n_predictions INTEGER
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def log_prediction(self, model_version, features, prediction, probability, actual_label=None, response_time=None):
        """Log a prediction to the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO predictions (model_version, features, prediction, probability, actual_label, response_time)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (model_version, json.dumps(features), prediction, probability, actual_label, response_time))
        
        conn.commit()
        conn.close()
    
    def get_recent_predictions(self, hours=24):
        """Get predictions from the last N hours."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        time_threshold = datetime.now() - timedelta(hours=hours)
        
        cursor.execute('''
            SELECT * FROM predictions 
            WHERE timestamp > ?
            ORDER BY timestamp DESC
        ''', (time_threshold,))
        
        predictions = cursor.fetchall()
        conn.close()
        
        return predictions
    
    def calculate_performance_metrics(self, model_version, hours=24):
        """Calculate performance metrics for recent predictions."""
        predictions = self.get_recent_predictions(hours)
        
        if not predictions:
            return None
        
        # Filter predictions with actual labels
        labeled_predictions = [p for p in predictions if p[6] is not None]  # actual_label column
        
        if not labeled_predictions:
            return None
        
        predictions_list = [p[4] for p in labeled_predictions]  # prediction column
        actuals_list = [p[6] for p in labeled_predictions]      # actual_label column
        
        # Calculate metrics
        accuracy = sum(p == a for p, a in zip(predictions_list, actuals_list)) / len(predictions_list)
        
        # Calculate precision, recall, F1 (simplified for binary classification)
        tp = sum(1 for p, a in zip(predictions_list, actuals_list) if p == 1 and a == 1)
        fp = sum(1 for p, a in zip(predictions_list, actuals_list) if p == 1 and a == 0)
        fn = sum(1 for p, a in zip(predictions_list, actuals_list) if p == 0 and a == 1)
        
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        metrics = {
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1_score": f1_score,
            "n_predictions": len(labeled_predictions)
        }
        
        # Store metrics
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO performance_metrics (model_version, accuracy, precision, recall, f1_score, n_predictions)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (model_version, accuracy, precision, recall, f1_score, len(labeled_predictions)))
        
        conn.commit()
        conn.close()
        
        return metrics

# Test the performance monitor
monitor = PerformanceMonitor()

# Simulate some predictions
model_version = "1.0.0"
for i in range(10):
    features = X_test[i].tolist()
    prediction = model.predict([X_test[i]])[0]
    probability = model.predict_proba([X_test[i]])[0].max()
    actual_label = y_test[i]
    
    monitor.log_prediction(
        model_version=model_version,
        features=features,
        prediction=int(prediction),
        probability=float(probability),
        actual_label=int(actual_label),
        response_time=0.1
    )

# Calculate performance metrics
metrics = monitor.calculate_performance_metrics(model_version)
print("Performance Metrics:")
print(json.dumps(metrics, indent=2))

# Get recent predictions
recent_predictions = monitor.get_recent_predictions()
print(f"\nRecent predictions count: {len(recent_predictions)}")
```

---

## Exercise 5: Containerization with Docker

In this exercise, we'll create a Docker container for our model serving application.

```python
# Create requirements.txt
requirements = """
flask==2.0.1
scikit-learn==1.0.2
numpy==1.21.0
pandas==1.3.0
joblib==1.1.0
requests==2.26.0
scipy==1.7.0
matplotlib==3.4.0
seaborn==0.11.0
"""

with open("requirements.txt", "w") as f:
    f.write(requirements)

# Create Dockerfile
dockerfile_content = """
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
"""

with open("Dockerfile", "w") as f:
    f.write(dockerfile_content)

print("Created requirements.txt and Dockerfile")
print("\nTo build and run the Docker container:")
print("docker build -t ml-model-server .")
print("docker run -p 5000:5000 ml-model-server")
```

This practical session covers the essential aspects of ML model deployment, from building simple model servers to implementing monitoring and containerization.

<!-- end NOTEBOOK: --> 