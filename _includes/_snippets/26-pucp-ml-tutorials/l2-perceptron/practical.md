<!-- NOTEBOOK: -->

# Introducción práctica

Construimos baselines y un perceptrón sencillo. Justifica la activación frente al baseline.

## Objetivos

1. Entrenar regresión lineal / logística como referencia.
2. Implementar o usar un perceptrón y observar separabilidad lineal.
3. Comparar activaciones en un ejemplo pequeño y justificar la elección.

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression, Perceptron
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

X, y = make_classification(n_samples=400, n_features=2, n_redundant=0,
                           n_informative=2, n_clusters_per_class=1, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

logit = LogisticRegression().fit(X_train, y_train)
perc = Perceptron().fit(X_train, y_train)
print("logit", accuracy_score(y_test, logit.predict(X_test)))
print("perceptron", accuracy_score(y_test, perc.predict(X_test)))
```

### Ticket de salida

¿Por qué elegiste una activación frente al baseline lineal/logístico para tu tarea?

<!-- end NOTEBOOK: -->
