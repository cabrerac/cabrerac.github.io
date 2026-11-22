<!-- NOTEBOOK: -->

### La red recurrente

La red lee los 11 caracteres de uno en uno. `batch_first=True` dice que cada matriz de 11 por 22 entra como una ventana, con los 11 caracteres en orden. Es el orden en que `np.stack` apiló las filas. En cada carácter actualiza un estado oculto de 128 números, con los mismos pesos. `salida` guarda el estado de cada carácter. `h_T[-1]` es solo el estado del último carácter, porque hay una sola capa. La cabeza lineal convierte esos 128 números en un puntaje por carácter del alfabeto.

En el primer paso lee la `e` de `el temblor`. En el segundo lee la `l`, con los mismos pesos, y así hasta el espacio. El puntaje más alto después de ese espacio es la predicción de la `m`.

```python
class ModeloTexto(nn.Module):
    """Lee una ventana carácter por carácter y puntúa el carácter siguiente.

    El estado oculto se actualiza en cada paso con los mismos pesos.

    Args:
        n_caracteres: Tamaño del alfabeto. Es también el tamaño de cada one-hot.
        n_ocultas: Tamaño del estado oculto.
    """

    def __init__(self, n_caracteres, n_ocultas):
        super().__init__()
        self.rnn = nn.RNN(n_caracteres, n_ocultas, batch_first=True)
        self.cabeza = nn.Linear(n_ocultas, n_caracteres)

    def forward(self, x):
        """Puntúa el carácter siguiente a cada ventana.

        Args:
            x: Tensor de forma (lote, caracteres, alfabeto).

        Returns:
            Tensor de forma (lote, alfabeto), sin softmax.
        """
        # Guarda el estado de cada carácter y el estado final de la única capa
        salida, h_T = self.rnn(x)
        # Convierte el estado del último carácter en un puntaje por letra
        return self.cabeza(h_T[-1])
```

La pérdida es la entropía cruzada entre esos puntajes y el índice del carácter correcto. Adam ajusta el paso, y 400 épocas le dan tiempo a aprender un párrafo tan corto. El recorte del gradiente limita el producto de pendientes a lo largo de los 11 caracteres.

```python
def entrenar_texto(X, y, n_ocultas=128, epocas=400):
    """Ajusta la red para predecir el índice del carácter siguiente.

    Args:
        X: Ventanas one-hot, forma (filas, caracteres, alfabeto).
        y: Índice del carácter objetivo, uno por ventana.
        n_ocultas: Tamaño del estado oculto.
        epocas: Pasadas completas por el párrafo.

    Returns:
        El modelo entrenado y la pérdida de cada época.
    """
    torch.manual_seed(42)
    lote_x = torch.tensor(X, dtype=torch.float32)
    # El objetivo entra como índice entero
    lote_y = torch.tensor(y, dtype=torch.long)
    # La última dimensión de X es el tamaño del alfabeto
    modelo = ModeloTexto(n_caracteres=X.shape[-1], n_ocultas=n_ocultas)
    optimizador = torch.optim.Adam(modelo.parameters(), lr=1e-3)
    perdida_fn = nn.CrossEntropyLoss()
    historial = []
    for epoca in range(epocas):
        optimizador.zero_grad()
        puntajes = modelo(lote_x)
        # Compara los puntajes con el índice del carácter correcto
        perdida = perdida_fn(puntajes, lote_y)
        perdida.backward()
        # Después de backward cada peso tiene un gradiente.
        # Si el largo de ese vector pasa de 1, lo encoge hasta dejarlo en 1.
        # El producto de las pendientes en los 11 caracteres puede hacer enorme el paso.
        nn.utils.clip_grad_norm_(modelo.parameters(), max_norm=1.0)
        optimizador.step()
        historial.append(perdida.item())
    return modelo, historial
```

<!-- end NOTEBOOK: -->
