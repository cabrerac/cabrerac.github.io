<!-- NOTEBOOK: -->

# Introducción práctica

Exploramos atención a escala toy y un demo mínimo de LLM (API si hay clave. Si no, fallback offline).

## Objetivos

1. Implementar un producto Q K / softmax toy para ver pesos de atención.
2. Llamar un LLM (o simular) con una pregunta civil.
3. Mapear cuándo preferir tabular NN / modelo clásico vs interfaz LLM.

```python
import numpy as np

def toy_attention(Q, K, V):
    scores = Q @ K.T / np.sqrt(K.shape[-1])
    weights = np.exp(scores - scores.max(axis=-1, keepdims=True))
    weights = weights / weights.sum(axis=-1, keepdims=True)
    return weights @ V, weights

Q = np.random.randn(4, 8)
K = np.random.randn(4, 8)
V = np.random.randn(4, 8)
out, w = toy_attention(Q, K, V)
print(out.shape, w.round(2))
```

### Fallback offline

Si no hay API, describe en markdown la salida esperada y los riesgos de sobreconfianza.

### Ticket de salida

Una pregunta de ingeniería civil. ¿Transformer/LLM o modelo tabular/clásico? Justifica en una frase.

<!-- end NOTEBOOK: -->
