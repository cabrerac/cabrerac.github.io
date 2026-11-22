<!-- NOTEBOOK: -->

## Parte A: atención desde cero

Usamos el párrafo de la sesión 3 y la misma tarea: leer 11 caracteres y predecir el que sigue. La red recurrente leía la ventana de uno en uno. Una cabeza de atención mira los 11 caracteres a la vez y decide cuánto pesa cada uno.

Construimos la atención en tres pasos: puntajes escalados, máscara causal y softmax. Luego entrenamos una cabeza y la comparamos con la red recurrente.

<!-- end NOTEBOOK: -->

{% include _snippets/char-window-text.md %}

<!-- NOTEBOOK: -->

### Puntajes escalados

Cada carácter produce tres vectores. La consulta $\mathbf{q}$ dice qué busca, la clave $\mathbf{k}$ dice qué ofrece y el valor $\mathbf{v}$ es lo que entrega. El puntaje entre las posiciones $i$ y $j$ es $\mathbf{q}_i \cdot \mathbf{k}_j / \sqrt{d}$. Dividir por $\sqrt{d}$ evita que los puntajes crezcan con el tamaño $d$ del vector.

`K.transpose(-2, -1)` gira las dos últimas dimensiones de `K`. Así `Q @ K.transpose(-2, -1)` calcula todos los productos de una vez, para una ventana o para un lote de ventanas.

```python
def puntajes_escalados(Q, K):
    """Producto de cada consulta con cada clave, dividido por la raíz de d.

    Args:
        Q: Consultas, forma (..., T, d).
        K: Claves, forma (..., T, d).

    Returns:
        Puntajes de forma (..., T, T).
    """
    d = K.shape[-1]
    # TODO: multiplique Q por K transpuesta y divida por la raíz de d
    return Q @ K.transpose(-2, -1) / math.sqrt(d)
```

### Máscara causal

Para predecir lo que sigue, la posición $i$ solo puede mirar las posiciones $0$ a $i$. La máscara marca con `True` todo lo que queda a la derecha de la diagonal. Esos puntajes pasan a $-\infty$ y, después de la softmax, pesan cero.

```python
def mascara_causal(T):
    """Marca las posiciones futuras de una ventana de largo T.

    Args:
        T: Largo de la ventana.

    Returns:
        Tensor booleano (T, T), True arriba de la diagonal.
    """
    # TODO: triangular superior de unos, sin la diagonal
    return torch.triu(torch.ones(T, T, dtype=torch.bool), diagonal=1)
```

### Softmax

La softmax convierte cada fila de puntajes en pesos positivos que suman 1. Restamos el máximo de la fila antes de `exp`. El resultado no cambia y se evitan números enormes. Un $-\infty$ se vuelve $e^{-\infty} = 0$.

```python
def softmax_filas(puntajes):
    """Softmax sobre la última dimensión.

    Args:
        puntajes: Tensor de forma (..., T, T).

    Returns:
        Pesos de la misma forma. Cada fila suma 1.
    """
    # TODO: reste el máximo de cada fila, aplique exp y divida por la suma de la fila
    exponencial = torch.exp(puntajes - puntajes.max(dim=-1, keepdim=True).values)
    return exponencial / exponencial.sum(dim=-1, keepdim=True)
```

### La función completa

`toy_attention` junta los tres pasos. Devuelve la mezcla de valores y los pesos, para poder dibujarlos después.

```python
def toy_attention(Q, K, V, causal=True):
    """Atención de una cabeza: puntajes escalados, máscara causal y softmax.

    Args:
        Q: Consultas, forma (..., T, d).
        K: Claves, forma (..., T, d).
        V: Valores, forma (..., T, d).
        causal: Si es True, cada posición solo mira hacia atrás.

    Returns:
        La mezcla de valores (..., T, d) y los pesos (..., T, T).
    """
    puntajes = puntajes_escalados(Q, K)
    if causal:
        # Las posiciones futuras quedan en menos infinito
        puntajes = puntajes.masked_fill(mascara_causal(Q.shape[-2]), float("-inf"))
    pesos = softmax_filas(puntajes)
    return pesos @ V, pesos
```

Probamos con cuatro posiciones al azar. PyTorch trae su propia atención, `scaled_dot_product_attention`. Si la nuestra está bien, las dos salidas coinciden.

```python
torch.manual_seed(0)
Q, K, V = torch.randn(4, 8), torch.randn(4, 8), torch.randn(4, 8)
salida, pesos = toy_attention(Q, K, V)
referencia = F.scaled_dot_product_attention(Q[None], K[None], V[None], is_causal=True)[0]
print(pesos.round(decimals=2))
```

**Comprobar:**

```python
assert torch.allclose(pesos.sum(dim=-1), torch.ones(4))
assert torch.all(pesos[mascara_causal(4)] == 0)
assert torch.allclose(salida, referencia, atol=1e-5)
print("La atención coincide con la de PyTorch. OK")
```

### Una cabeza de atención

La entrada es la misma matriz one-hot de 11 por 22. Una capa lineal convierte cada carácter en un vector de 32 números. Un vector aprendido por posición le suma dónde está en la ventana. Sin él, la atención no distingue el orden.

Tres capas lineales sacan $Q$, $K$ y $V$. La atención mezcla los valores, y la suma con la entrada es la conexión residual. Una red pequeña por posición (feed-forward) procesa esa mezcla. La cabeza lineal lee solo la última posición, la única que vio los 11 caracteres, y puntúa el carácter siguiente.

```python
class CabezaAtencion(nn.Module):
    """Una cabeza de atención causal que puntúa el carácter siguiente.

    Args:
        n_caracteres: Tamaño del alfabeto. Es también el tamaño de cada one-hot.
        d: Tamaño del vector de cada carácter.
        ventana: Largo de la ventana.
    """

    def __init__(self, n_caracteres, d=32, ventana=11):
        super().__init__()
        self.entrada = nn.Linear(n_caracteres, d)
        # Un vector aprendido por posición
        self.posicion = nn.Parameter(0.1 * torch.randn(ventana, d))
        self.q = nn.Linear(d, d, bias=False)
        self.k = nn.Linear(d, d, bias=False)
        self.v = nn.Linear(d, d, bias=False)
        self.feed_forward = nn.Sequential(nn.Linear(d, 4 * d), nn.ReLU(), nn.Linear(4 * d, d))
        self.cabeza = nn.Linear(d, n_caracteres)

    def forward(self, x):
        """Puntúa el carácter siguiente a cada ventana.

        Args:
            x: Tensor de forma (lote, caracteres, alfabeto).

        Returns:
            Puntajes (lote, alfabeto), sin softmax, y pesos (lote, caracteres, caracteres).
        """
        h = self.entrada(x) + self.posicion
        mezcla, pesos = toy_attention(self.q(h), self.k(h), self.v(h))
        # Conexión residual: la mezcla se suma a la entrada
        h = h + mezcla
        h = h + self.feed_forward(h)
        # La última posición ya miró toda la ventana
        return self.cabeza(h[:, -1]), pesos
```

El entrenamiento es el de la sesión 3: entropía cruzada, Adam y 400 épocas. La tasa de aprendizaje es más alta porque la red es más pequeña.

```python
def entrenar_atencion(X, y, d=32, epocas=400):
    """Ajusta la cabeza de atención para predecir el índice del carácter siguiente.

    Args:
        X: Ventanas one-hot, forma (filas, caracteres, alfabeto).
        y: Índice del carácter objetivo, uno por ventana.
        d: Tamaño del vector de cada carácter.
        epocas: Pasadas completas por el párrafo.

    Returns:
        El modelo entrenado y la pérdida de cada época.
    """
    torch.manual_seed(42)
    lote_x = torch.tensor(X, dtype=torch.float32)
    lote_y = torch.tensor(y, dtype=torch.long)
    modelo = CabezaAtencion(n_caracteres=X.shape[-1], d=d, ventana=X.shape[1])
    optimizador = torch.optim.Adam(modelo.parameters(), lr=1e-2)
    perdida_fn = nn.CrossEntropyLoss()
    historial = []
    for epoca in range(epocas):
        optimizador.zero_grad()
        puntajes, _ = modelo(lote_x)
        perdida = perdida_fn(puntajes, lote_y)
        perdida.backward()
        optimizador.step()
        historial.append(perdida.item())
    return modelo, historial
```

<!-- end NOTEBOOK: -->

{% include _snippets/char-rnn.md %}

<!-- NOTEBOOK: -->

### Atención frente a la red recurrente

Entrenamos las dos redes con las mismas ventanas y medimos cuatro cosas: parámetros, pérdida final, exactitud sobre el párrafo y segundos de entrenamiento. La exactitud es sobre el mismo texto que vieron, así que mide cuánto lo memorizaron, no cuánto generalizan.

```python
def exactitud(modelo, X, y):
    """Fracción de ventanas donde el puntaje más alto es el carácter correcto.

    Args:
        modelo: Red ya entrenada.
        X: Ventanas one-hot.
        y: Índice del carácter objetivo.

    Returns:
        La exactitud entre 0 y 1.
    """
    modelo.eval()
    with torch.no_grad():
        salida = modelo(torch.tensor(X, dtype=torch.float32))
    # La cabeza de atención devuelve también los pesos
    if isinstance(salida, tuple):
        salida = salida[0]
    return float((salida.argmax(dim=1).numpy() == y).mean())


inicio = time.perf_counter()
atencion_texto, historial_atencion = entrenar_atencion(X_texto, y_texto)
segundos_atencion = time.perf_counter() - inicio
inicio = time.perf_counter()
rnn_texto, historial_texto = entrenar_texto(X_texto, y_texto)
segundos_rnn = time.perf_counter() - inicio

comparacion = pd.DataFrame(
    {
        "parámetros": [sum(p.numel() for p in m.parameters()) for m in (atencion_texto, rnn_texto)],
        "pérdida final": [historial_atencion[-1], historial_texto[-1]],
        "exactitud": [exactitud(atencion_texto, X_texto, y_texto), exactitud(rnn_texto, X_texto, y_texto)],
        "segundos": [segundos_atencion, segundos_rnn],
    },
    index=["atención", "recurrente"],
)
print(comparacion.round(3))

plt.figure(figsize=(5, 3.5))
plt.plot(historial_atencion, label="atención")
plt.plot(historial_texto, label="recurrente")
plt.xlabel("época")
plt.ylabel("pérdida")
plt.yscale("log")
plt.legend()
plt.show()
```

Las dos redes aprenden el párrafo. La diferencia está en cómo leen. La recurrente da 11 pasos en orden, y cada paso espera al anterior. La atención calcula las 11 posiciones con unas pocas multiplicaciones de matrices, que es justo lo que una GPU hace rápido. Con 174 ventanas casi no se nota, y en CPU la recurrente puede incluso terminar antes. Con millones de tokens es la razón por la que los transformadores reemplazaron a las redes recurrentes.

**Comprobar:**

```python
assert historial_atencion[-1] < historial_atencion[0]
assert comparacion.loc["atención", "exactitud"] > 0.9
assert comparacion.loc["atención", "parámetros"] < comparacion.loc["recurrente", "parámetros"]
print("La cabeza de atención aprende el párrafo. OK")
```

### El mapa de atención

Cada fila es una posición de la ventana, y cada columna es un carácter que esa posición puede mirar. Arriba de la diagonal todo es cero por la máscara. La última fila es la que usa la cabeza para predecir. Los espacios se dibujan como `␣`.

```python
def mapa_atencion(pesos, etiquetas, titulo):
    """Dibuja una matriz de pesos de atención.

    Args:
        pesos: Matriz (T, T). La fila i son los pesos de la posición i.
        etiquetas: Texto de cada posición.
        titulo: Título del gráfico.
    """
    fig, ax = plt.subplots(figsize=(5.5, 5))
    imagen = ax.imshow(pesos, cmap="viridis", vmin=0, vmax=1)
    ax.set_xticks(range(len(etiquetas)), etiquetas, rotation=90)
    ax.set_yticks(range(len(etiquetas)), etiquetas)
    ax.set_xlabel("posición mirada (clave)")
    ax.set_ylabel("posición que mira (consulta)")
    ax.set_title(titulo)
    fig.colorbar(imagen, ax=ax)
    plt.show()
```

`k = 0` es la primera ventana, `el temblor` y un espacio, con objetivo `m`. Cambie `k` para ver otras ventanas.

```python
k = 0
with torch.no_grad():
    puntajes_k, pesos_k = atencion_texto(torch.tensor(X_texto[k:k + 1], dtype=torch.float32))
caracteres_k = [alfabeto[i].replace(" ", "␣") for i in X_texto[k].argmax(axis=1)]
print("ventana:", repr("".join(alfabeto[i] for i in X_texto[k].argmax(axis=1))),
      "| predicción:", repr(alfabeto[int(puntajes_k.argmax())]),
      "| objetivo:", repr(alfabeto[y_texto[k]]))
mapa_atencion(pesos_k[0].numpy(), caracteres_k, f"Cabeza entrenada, ventana {k}")
```

**Comprobar:**

```python
assert pesos_k.shape == (1, 11, 11)
assert torch.all(pesos_k[0][mascara_causal(11)] == 0)
assert torch.allclose(pesos_k.sum(dim=-1), torch.ones(1, 11))
print("El mapa respeta la máscara causal. OK")
```

<!-- end NOTEBOOK: -->
