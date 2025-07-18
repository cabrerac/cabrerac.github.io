<!-- SLIDES: -->

## MLOps

## MLOps

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 95%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/data-assess-pipeline.svg" alt="Data Assess Pipeline" style="height: 500px">
            </div>
        </div>
    </div>
</div>

## MLOps

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 95%">
            <div class="column vertical-middle text-center" style="width: 50%">
                <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/1/1b/ML_Ops_Venn_Diagram.svg" alt="MLOps" style="height: 500px">
                <div class="footnote">MLOps - Cmbreuel, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons.</div>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>MLOps</b> is a set of practices and tools that support deploying and maintaining ML models in production reliably and efficiently. The goal is to <b>automate and streamline the ML pipeline</b>. These practices and tools include all the pipeline stages from data collection, model training, and deployment to monitoring and governance. We aim to ensure that ML models are robust, scalable, and continuously delivering value.</p>
            </div>
        </div>
    </div>
</div>

## MLOps

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 95%">
            <div class="column vertical-middle text-center" style="width: 50%">
                <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/1/1b/ML_Ops_Venn_Diagram.svg" alt="MLOps" style="height: 500px">
                <div class="footnote">MLOps - Cmbreuel, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons.</div>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <ul>
                    <li>Automated data collection</li>
                    <li>Automated model training and validation</li>
                    <li>Continuous integration and continuous deployment</li>
                    <li>Monitoring and logging</li>
                    <li>Governance and compliance</li>
                    <li>Scalability and reliability</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## MLOps

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 95%">
            <div class="column vertical-middle text-center" style="width: 50%">
                <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/1/1b/ML_Ops_Venn_Diagram.svg" alt="MLOps" style="height: 500px">
                <div class="footnote">MLOps - Cmbreuel, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons.</div>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">

```python
import mlflow
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelMonitor:
    def __init__(self, model_name):
        self.model_name = model_name
        mlflow.set_tracking_uri("http://localhost:5000")
    def log_prediction(self, input_data, prediction, 
                      actual=None, model_version="1.0"):
        """Log model predictions for monitoring"""
        with mlflow.start_run():
            mlflow.log_params({
                "input_size": len(input_data),
                "model_version": model_version,
                "timestamp": datetime.now().isoformat()
            })
        
            mlflow.log_metric("prediction", prediction)
        
            if actual is not None:
                mlflow.log_metric("actual", actual)
                mlflow.log_metric("error", abs(prediction - actual))
                
            logger.info(f"Prediction logged: {prediction}")
            
    def monitor_drift(self, current_stats, baseline_stats):
        """Monitor for data drift"""
        drift_score = self.calculate_drift(current_stats, baseline_stats)
        mlflow.log_metric("drift_score", drift_score)
        if drift_score > 0.1:  # Threshold
            logger.warning(f"Data drift detected: {drift_score}")
```
</div>
        </div>
    </div>
</div>

## MLOps

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 95%">
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="https://upload.wikimedia.org/wikipedia/commons/1/15/Neural_Network.svg" alt="Deep Neural Network" style="max-width: 100%; height: auto;">
                <div class="footnote">Deep Neural Network with multiple hidden layers - QuantuMechaniX8, CC0, via Wikimedia Commons</div>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">

```python
import mlflow
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelMonitor:
    def __init__(self, model_name):
        self.model_name = model_name
        mlflow.set_tracking_uri("http://localhost:5000")
    def log_prediction(self, input_data, prediction, 
                      actual=None, model_version="1.0"):
        """Log model predictions for monitoring"""
        with mlflow.start_run():
            mlflow.log_params({
                "input_size": len(input_data),
                "model_version": model_version,
                "timestamp": datetime.now().isoformat()
            })
        
            mlflow.log_metric("prediction", prediction)
        
            if actual is not None:
                mlflow.log_metric("actual", actual)
                mlflow.log_metric("error", abs(prediction - actual))
                
            logger.info(f"Prediction logged: {prediction}")
            
    def monitor_drift(self, current_stats, baseline_stats):
        """Monitor for data drift"""
        drift_score = self.calculate_drift(current_stats, baseline_stats)
        mlflow.log_metric("drift_score", drift_score)
        if drift_score > 0.1:  # Threshold
            logger.warning(f"Data drift detected: {drift_score}")
```
</div>
        </div>
    </div>
</div>

## MLOps

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 95%">
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="https://upload.wikimedia.org/wikipedia/commons/1/15/Neural_Network.svg" alt="Deep Neural Network" style="max-width: 100%; height: auto;">
                <div class="footnote">Deep Neural Network with multiple hidden layers - QuantuMechaniX8, CC0, via Wikimedia Commons</div>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="https://cabrerac.github.io/assets/media/images/doa-architecture.png" alt="DOA Architecture" style="height: 400px">
            </div>
        </div>
    </div>
</div>

## MLOps

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 95%">
            <div class="column vertical-middle text-center" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/diagrams/rag-process.svg" alt="RAG Process" style="height: 500px">
                <div class="footnote">RAG Process</div>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/doa-architecture.png" alt="DOA Architecture" style="height: 400px">
            </div>
        </div>
    </div>
</div>

## MLOps

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 95%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img src="{{ site.url }}/assets/media/images/doa-log-ml.png" alt="DOA Debugger" style="height: 400px">
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->


