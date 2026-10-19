<!-- NOTEBOOK: -->

Este cuaderno entrena las arquitecturas de la sesión. Cada bloque describe los datos utilizados, cuál es la tarea que se quiere solucionar y por qué esa arquitectura encaja.

Ejecute las celdas de arriba hacia abajo. En cada **Comprobar**, confirme el mensaje `OK` antes de seguir.

---

## Importaciones

En el siguiente bloque importamos las librerías y conjuntos de datos que usaremos a lo largo del cuaderno.

```python
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
from sklearn.datasets import load_digits, make_moons
from sklearn.linear_model import LogisticRegression, Perceptron
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from torch import nn
```

---

## Dos lunas

Quinientos puntos en el plano forman dos medias lunas entrelazadas, con un poco de ruido. La tarea es decir a qué luna pertenece un punto nuevo. Una recta no puede separar las lunas. El perceptrón y la logística de la sesión 2 son rectas, así que se quedan cortos.

Un perceptrón multicapa añade una capa oculta. Cada unidad oculta es una curva sobre las dos coordenadas. La capa de salida combina esas curvas y puede rodear una luna.

### Los datos

`noise=0.20` desplaza cada punto un poco al azar. Las dos lunas se tocan, y una recta deja puntos de las dos clases del mismo lado. El color del punto es la luna verdadera.

```python
X_lunas, y_lunas = make_moons(n_samples=500, noise=0.20, random_state=42)

plt.figure(figsize=(5, 4))
plt.scatter(X_lunas[:, 0], X_lunas[:, 1], c=y_lunas, cmap="coolwarm", edgecolor="k", s=18)
plt.xlabel("x1")
plt.ylabel("x2")
plt.title("Dos lunas")
plt.show()
```

Partimos 70/30 y escalamos con la media y la desviación de train. Una partición estratificada deja cada luna con la misma proporción en train y en test que en el conjunto completo. Escalar resta la media de train y divide por su desviación. Las dos coordenadas quedan en la misma escala. La media y la desviación se calculan solo con train, así que los puntos de test no entran en el escalado.

```python
X_train, X_test, y_train, y_test = train_test_split(
    X_lunas, y_lunas, test_size=0.30, random_state=42, stratify=y_lunas
)
escalador_lunas = StandardScaler().fit(X_train)
X_train_esc = escalador_lunas.transform(X_train)
X_test_esc = escalador_lunas.transform(X_test)
print("train:", len(y_train), "| test:", len(y_test))
```

### Líneas base

La clase mayoritaria es el baseline. `y_test.mean()` es la fracción de lunas de la clase 1, y la exactitud de decir siempre la clase más común es la mayor entre esa fracción y `1 - y_test.mean()`. Si un modelo acierta menos que eso, no usó el plano. La logística y el perceptrón son las rectas de la sesión 2. La diferencia con el MLP es lo que aporta la capa oculta.

```python
def lineas_base_lunas(X_train, y_train, X_test, y_test):
    """Ajusta la logística y el perceptrón y mide su exactitud en test.

    También mide la exactitud de predecir siempre la clase mayoritaria.

    Args:
        X_train: Matriz de train ya escalada.
        y_train: Etiquetas de train, 0 o 1.
        X_test: Matriz de test ya escalada.
        y_test: Etiquetas de test.

    Returns:
        Un diccionario con la exactitud de cada línea base.
    """
    piso = float(max(y_test.mean(), 1.0 - y_test.mean()))
    logistica = LogisticRegression().fit(X_train, y_train)
    perceptron = Perceptron(random_state=42).fit(X_train, y_train)
    return {
        "piso (mayoría)": piso,
        "logística": float(logistica.score(X_test, y_test)),
        "perceptrón": float(perceptron.score(X_test, y_test)),
    }
```

El diccionario trae tres exactitudes en test. El baseline es acertar siempre la luna más común. Las otras dos son las rectas de la sesión 2.

```python
bases_lunas = lineas_base_lunas(X_train_esc, y_train, X_test_esc, y_test)
print({nombre: round(valor, 3) for nombre, valor in bases_lunas.items()})
```

### El perceptrón multicapa

El modelo que implementamos a continuación usa una capa oculta de 8 unidaes (i.e., `hidden_layer_sizes=(8,)`). Cada unidad dibuja una curva sobre las dos coordenadas. Por defecto la activación es ReLU y el optimizador es Adam. `alpha=1e-4` es la penalización $L_2$ también conocida como mínimos cuadrados o distancia euclidiana . `max_iter=2000` es el tope de pasadas por train. `fit` recibe las lunas sin escalar, porque el `StandardScaler` del pipeline escala por dentro.

```python
mlp_lunas = make_pipeline(
    StandardScaler(),
    MLPClassifier(
        hidden_layer_sizes=(8,),
        alpha=1e-4,
        max_iter=2000,
        random_state=42,
    ),
)
mlp_lunas.fit(X_train, y_train)
exactitud_mlp = float(mlp_lunas.score(X_test, y_test))
print("exactitud MLP en test:", round(exactitud_mlp, 3))
```

El color de fondo es la clase que el modelo asigna a cada punto del plano. Para pintarlo armamos una grilla de 250 por 250 puntos, con medio unidad de margen para no cortar las lunas del borde. `meshgrid` forma las parejas `(x, y)`, `ravel` las aplana y `c_` las junta en dos columnas, que es lo que recibe el modelo. `reshape` devuelve esas clases a la forma de la grilla. El punto de encima conserva el color de su luna verdadera. Si el fondo y el punto coinciden, el modelo acertó. La logística corta el plano con una recta. El MLP cierra una región alrededor de cada luna. La logística se entrenó con datos escalados, así que la grilla de ese panel también se escala antes de predecir.

```python
def pintar_regiones(ax, predecir, X, y, titulo):
    """Pinta la clase que el modelo asigna a cada punto del plano.

    Los puntos de datos van encima, con el color de su luna verdadera.

    Args:
        ax: Eje de matplotlib.
        predecir: Función que recibe puntos (n, 2) y devuelve una clase por punto.
        X: Coordenadas originales de las lunas.
        y: Etiqueta verdadera de cada punto.
        titulo: Texto del panel.
    """
    x_min, x_max = X[:, 0].min() - 0.5, X[:, 0].max() + 0.5
    y_min, y_max = X[:, 1].min() - 0.5, X[:, 1].max() + 0.5
    xx, yy = np.meshgrid(np.linspace(x_min, x_max, 250), np.linspace(y_min, y_max, 250))
    malla = np.c_[xx.ravel(), yy.ravel()]
    zz = predecir(malla).reshape(xx.shape)
    ax.contourf(xx, yy, zz, alpha=0.35, cmap="coolwarm")
    ax.scatter(X[:, 0], X[:, 1], c=y, cmap="coolwarm", edgecolor="k", s=16)
    ax.set_title(titulo)
    ax.set_xlabel("x1")
    ax.set_ylabel("x2")
```

```python
logistica_lunas = LogisticRegression().fit(X_train_esc, y_train)
fig, ejes = plt.subplots(1, 2, figsize=(9, 4))
pintar_regiones(
    ejes[0],
    lambda puntos: logistica_lunas.predict(escalador_lunas.transform(puntos)),
    X_lunas,
    y_lunas,
    "Logística",
)
pintar_regiones(ejes[1], mlp_lunas.predict, X_lunas, y_lunas, "MLP")
plt.tight_layout()
plt.show()
```

**Comprobar:**

```python
assert exactitud_mlp > bases_lunas["logística"]
assert exactitud_mlp > bases_lunas["perceptrón"]
print("El MLP separa las lunas mejor que una recta. OK")
```

---

## Manchas solares

La serie trae el número anual de manchas solares, de 1700 a 2008. El ciclo de manchas dura unos 11 años, así que el valor del próximo año depende de los anteriores. La tarea es predecir el año que sigue a partir de una ventana de 11 años (i.e., teniendo en cuenta los 11 años anteriores). Una red recurrente guarda el estado oculto de la historia de la ventana. Los mismos pesos se reutilizan en cada año y La predicción sale del último estado oculto.

### La serie

Cada fila es una ventana de 11 años, y el objetivo es el año que sigue. Once años cubren un ciclo, así que la ventana ve una subida y una bajada. Train son las ventanas cuyo año objetivo cae en 1950 o antes. Test son los 58 años de 1951 a 2008. La media y la desviación se calculan solo con los años de train. El escalado no usa el tramo que queremos predecir.

La primera fila, antes de escalar, usa los conteos de 1700 a 1710. El objetivo es el conteo de 1711.

| Papel | Año | Manchas |
| --- | --- | --- |
| Entrada | 1700 | 5 |
| Entrada | 1701 | 11 |
| Entrada | 1702 | 16 |
| Entrada | 1703 | 23 |
| Entrada | 1704 | 36 |
| Entrada | 1705 | 58 |
| Entrada | 1706 | 29 |
| Entrada | 1707 | 20 |
| Entrada | 1708 | 10 |
| Entrada | 1709 | 8 |
| Entrada | 1710 | 3 |
| Objetivo | 1711 | 0 |

La fila siguiente se corre un año. Sus entradas son 1701 a 1711 y su objetivo es 1712, que también vale 0. El escalado ocurre antes de armar el tensor. La red ve estos conteos después de restar la media de train y dividir por su desviación.

En la función, `valores` es esa columna de manchas. `valores[i - 11:i]` copia los 11 conteos anteriores al año `i` (i.e., la primera copia es 1700 a 1710). `np.stack` apila las copias y cada una queda como una fila. `objetivos` guarda el conteo del año `i`, desde 1711. `anio_objetivo` es el año de calendario de esa fila, y `en_train` es verdadero cuando ese año es 1950 o anterior. `entradas[en_train]` se queda con esas filas. `~en_train` invierte la máscara y deja 1951 a 2008. La media y la desviación se calculan en la serie original, solo hasta 1950. Restamos esa media y dividimos por la desviación. Un cero en esa escala es el promedio de train, y `a_original` vuelve de ahí al número de manchas.

```python
import statsmodels.api as sm


def preparar_manchas(ventana=11):
    """Arma ventanas de manchas solares y una partición por año.

    Args:
        ventana: Cuántos años mira el modelo antes de predecir el siguiente.

    Returns:
        Ventanas de train y de test, la serie completa y los años de test.
    """
    tabla = sm.datasets.sunspots.load_pandas().data
    valores = tabla["SUNACTIVITY"].to_numpy(dtype=float)
    anios = tabla["YEAR"].to_numpy()
    entradas = np.stack([valores[i - ventana:i] for i in range(ventana, len(valores))])
    objetivos = valores[ventana:]
    anio_objetivo = anios[ventana:]
    en_train = anio_objetivo <= 1950
    media = valores[anios <= 1950].mean()
    desv = valores[anios <= 1950].std()
    entradas = (entradas - media) / desv
    objetivos_esc = (objetivos - media) / desv

    def a_original(prediccion):
        """Pasa una predicción escalada al número de manchas."""
        return prediccion * desv + media

    return {
        "X_train": entradas[en_train],
        "y_train": objetivos_esc[en_train],
        "X_test": entradas[~en_train],
        "y_test": objetivos[~en_train],
        "a_original": a_original,
        "anios": anios,
        "valores": valores,
        "anio_test": anio_objetivo[~en_train],
    }
```

`preparar_manchas` devuelve las matrices ya partidas. `X_train` guarda las filas cuyo objetivo cae en 1950 o antes. `y_train` es el objetivo escalado de cada fila, en un vector aparte. Esa matriz es la que entra en la red recurrente.

```python
serie = preparar_manchas()
print("X_train", serie["X_train"].shape, "| y_train", serie["y_train"].shape)
print("X_test", serie["X_test"].shape, "| y_test", serie["y_test"].shape)

columnas = [f"t-{11 - j}" for j in range(11)]
vista = pd.DataFrame(serie["X_train"][:3], columns=columnas)
vista["y escalado"] = serie["y_train"][:3]
print(vista.round(2).to_string(index=False))
```

`t-11` es el año más viejo de la ventana y `t-1` el más reciente. En la primera fila son 1700 y 1710, ya escalados. `y escalado` es 1711 en la escala de train. `X_test` son las 58 filas de 1951 a 2008. `y_test` guarda esas metas en número de manchas, sin escalar.

La curva es el número de manchas de cada año, de 1700 a 2008. La línea vertical es 1950, el último año cuyo valor entra en train. A la derecha de la línea está el test. El ciclo de unos 11 años se repite a lo largo de toda la serie.

```python
plt.figure(figsize=(8, 3))
plt.plot(serie["anios"], serie["valores"], color="black")
plt.axvline(1950, color="gray", linestyle="--")
plt.xlabel("año")
plt.ylabel("manchas")
plt.title("Manchas solares")
plt.show()
```

### Líneas base

La persistencia dice que el próximo año tendrá las mismas manchas que el último año de la ventana. En una serie que cambia despacio, esa copia ya queda cerca de lo observado. La media ignora la ventana y responde siempre el promedio de train, cerca de la mitad de un ciclo.

El RECM es la raíz del error cuadrático medio, en número de manchas. Un RECM de 20 quiere decir que la predicción se aleja, en promedio, unos 20 manchas del valor observado. Más bajo es una curva más pegada a la serie.

`X_test[:, -1]` es el último año de cada ventana, todavía escalado. `a_original` lo devuelve a número de manchas, y esa copia es la persistencia. Un vector de ceros, pasado por `a_original`, es la media de train. `full_like` repite esa media tantas veces como años hay en el test.

```python
def recm(y_real, y_pred):
    """Raíz del error cuadrático medio, en la escala de las manchas.

    Args:
        y_real: Valores observados.
        y_pred: Valores predichos, en la misma escala.

    Returns:
        Un número. Cero sería una predicción perfecta.
    """
    return float(np.sqrt(np.mean((y_real - y_pred) ** 2)))
```

```python
ultimo_anio = serie["a_original"](serie["X_test"][:, -1])
media_train = float(serie["a_original"](np.zeros(1)))
recm_media = recm(serie["y_test"], np.full_like(serie["y_test"], media_train))
recm_persistencia = recm(serie["y_test"], ultimo_anio)
print("años de test:", len(serie["y_test"]))
print("RECM media:", round(recm_media, 1), "| RECM persistencia:", round(recm_persistencia, 1))
```

### La red recurrente

La red lee los 11 años de uno en uno. `batch_first` ordena el tensor como `(filas, años, 1)`. En cada año actualiza un estado oculto de 32 números, con los mismos pesos. Ese estado es la memoria de la ventana. `salida` guarda el estado de cada año. `h_T[-1]` es solo el estado del último año, porque hay una sola capa, y la cabeza lineal lo convierte en un número: la predicción del año siguiente, todavía en la escala normalizada.

`unsqueeze(-1)` deja el lote con forma `(filas, 11, 1)`.

| Eje | Tamaño | Significado |
| --- | --- | --- |
| Lote | una fila | esta ventana |
| Tiempo | 11 | los años, en orden |
| Características | 1 | el conteo escalado de ese año |

`nn.RNN` tiene tamaño de entrada 1. En el primer paso lee el conteo escalado de 1700 y actualiza el estado oculto. En el segundo paso lee 1701, con los mismos pesos, y así hasta 1710. La cabeza lineal lee solo el estado oculto después de 1710 y devuelve un número, la predicción escalada de 1711.

```python
class ModeloSecuencia(nn.Module):
    """Lee una ventana año por año y predice un solo número.

    El estado oculto se actualiza en cada paso con los mismos pesos.

    Args:
        n_entradas: Cuántos números llegan en cada año. Aquí es 1.
        n_ocultas: Tamaño del estado oculto.
    """

    def __init__(self, n_entradas, n_ocultas):
        super().__init__()
        self.rnn = nn.RNN(n_entradas, n_ocultas, batch_first=True)
        self.cabeza = nn.Linear(n_ocultas, 1)

    def forward(self, x):
        """Predice el año siguiente a cada ventana.

        Args:
            x: Tensor de forma (lote, años, n_entradas).

        Returns:
            Tensor de forma (lote, 1).
        """
        salida, h_T = self.rnn(x)
        return self.cabeza(h_T[-1])
```

Con pocas épocas la red solo copia la forma media del ciclo y se queda por debajo de los picos. Adam ajusta el paso según el tamaño de cada gradiente, y 300 épocas le dan tiempo a seguir la amplitud. El recorte del gradiente limita el producto de pendientes a lo largo de los 11 años. Si ese producto crece, el paso se vuelve enorme y el ajuste se dispara. Antes del bucle, `unsqueeze(-1)` agrega un eje: las ventanas pasan de `(filas, 11)` a `(filas, 11, 1)`, un conteo por año, y el objetivo pasa de `(filas,)` a `(filas, 1)`, que es la forma que compara la pérdida.

```python
def entrenar_rnn(X_train, y_train, n_ocultas=32, epocas=300):
    """Ajusta la red recurrente con error cuadrático y recorta el gradiente.

    Args:
        X_train: Ventanas escaladas, forma (filas, años).
        y_train: Año siguiente escalado, un número por ventana.
        n_ocultas: Tamaño del estado oculto.
        epocas: Pasadas completas por train.

    Returns:
        El modelo entrenado y la pérdida de cada época.
    """
    torch.manual_seed(42)
    X = torch.tensor(X_train, dtype=torch.float32).unsqueeze(-1)
    y = torch.tensor(y_train, dtype=torch.float32).unsqueeze(-1)
    modelo = ModeloSecuencia(n_entradas=1, n_ocultas=n_ocultas)
    optimizador = torch.optim.Adam(modelo.parameters(), lr=1e-3)
    perdida_fn = nn.MSELoss()
    historial = []
    for epoca in range(epocas):
        optimizador.zero_grad()
        prediccion = modelo(X)
        perdida = perdida_fn(prediccion, y)
        perdida.backward()
        nn.utils.clip_grad_norm_(modelo.parameters(), max_norm=1.0)
        optimizador.step()
        historial.append(float(perdida))
    return modelo, historial
```

Esta función apaga el entrenamiento y devuelve la predicción en la escala normalizada. `squeeze(1)` quita el eje de tamaño 1 y deja un número por ventana. En la celda de la figura, `a_original` la pasa de nuevo a número de manchas.

```python
def predecir_rnn(modelo, X):
    """Predice en la escala escalada y devuelve un vector de numpy.

    Args:
        modelo: Un ModeloSecuencia ya entrenado.
        X: Ventanas, forma (filas, años).

    Returns:
        Predicciones, una por ventana.
    """
    modelo.eval()
    with torch.no_grad():
        lote = torch.tensor(X, dtype=torch.float32).unsqueeze(-1)
        return modelo(lote).squeeze(1).numpy()
```

La curva negra es el número observado entre 1951 y 2008. La azul es la predicción de la red a un año. La naranja es la persistencia. El RECM resume la distancia de cada curva a la negra. La comprobación pide que el de la red sea menor que el de la persistencia.

```python
rnn_manchas, historial_rnn = entrenar_rnn(serie["X_train"], serie["y_train"])
pred_test = serie["a_original"](predecir_rnn(rnn_manchas, serie["X_test"]))
recm_rnn = recm(serie["y_test"], pred_test)
print("RECM RNN:", round(recm_rnn, 1), "| pérdida inicial:", round(historial_rnn[0], 3),
      "| pérdida final:", round(historial_rnn[-1], 3))

plt.figure(figsize=(8, 3))
plt.plot(serie["anio_test"], serie["y_test"], color="black", label="observado")
plt.plot(serie["anio_test"], pred_test, label="RNN")
plt.plot(serie["anio_test"], ultimo_anio, label="persistencia", alpha=0.7)
plt.xlabel("año")
plt.ylabel("manchas")
plt.title("Test, 1951 a 2008")
plt.legend()
plt.show()
```

**Comprobar:**

```python
assert len(serie["y_test"]) == 58
assert historial_rnn[-1] < historial_rnn[0]
assert recm_rnn < recm_persistencia
print("La RNN mejora la persistencia. OK")
```

---

## Dígitos escritos a mano

`load_digits` trae 1797 imágenes de 8 por 8 píxeles, sin usar la etiqueta de clase. La tarea es comprimir cada imagen en un código corto y reconstruirla. No hay etiqueta que predecir. El objetivo es la propia imagen.

Un autoencoder encaja porque el codificador produce el código y el decodificador vuelve a los 64 píxeles. El código es más corto que la imagen, así que la red tiene que quedarse con lo que importa.

### Las imágenes

Cada imagen es una grilla de 8 por 8. Un píxel vale de 0 a 16. Dividir por 16 lo deja entre 0 y 1, la escala en la que el error cuadrático trata igual a cada píxel. La partición es 70/30 y es aleatoria. Aquí no hay una clase que equilibrar, porque el objetivo de cada fila es la propia imagen.

```python
def preparar_digitos():
    """Escala los dígitos a [0, 1] y parte 70/30.

    Returns:
        Train y test, una imagen estirada por fila.
    """
    imagenes = load_digits().data / load_digits().data.max()
    return train_test_split(imagenes, test_size=0.30, random_state=42)
```

El ECM es el error cuadrático medio por píxel. Vale 0 si la reconstrucción copia la imagen. Un ECM de 0.02 quiere decir que, en promedio, cada píxel se aleja 0.02 en la escala de 0 a 1.

```python
def ecm(real, reconstruido):
    """Error cuadrático medio entre una imagen y su reconstrucción.

    Args:
        real: Imágenes observadas, una por fila.
        reconstruido: Imágenes producidas por el modelo.

    Returns:
        El promedio de los cuadrados de las diferencias.
    """
    return float(np.mean((real - reconstruido) ** 2))
```

Cada fila del dibujo es un grupo de imágenes, y el texto a la izquierda dice de dónde sale. Cada imagen llega como 64 números, y `reshape` arma de nuevo la grilla de 8 por 8. `vmin=0` y `vmax=1` fijan el blanco y el negro, así dos reconstrucciones se comparan con la misma escala. Si solo hay una fila de imágenes, `subplots` devuelve un vector. Lo envolvemos para poder indexar con `[fila, columna]`.

```python
def mostrar_imagenes(filas, lado=8):
    """Dibuja varias filas de imágenes de 8 por 8.

    Args:
        filas: Lista de pares (título, array de forma (n, 64)).
        lado: Ancho de cada imagen en píxeles.
    """
    n = filas[0][1].shape[0]
    fig, ejes = plt.subplots(len(filas), n, figsize=(n, len(filas) + 0.6))
    if len(filas) == 1:
        ejes = np.array([ejes])
    for i, (titulo, imagenes) in enumerate(filas):
        for j in range(n):
            ejes[i, j].imshow(imagenes[j].reshape(lado, lado), cmap="gray_r", vmin=0, vmax=1)
            ejes[i, j].set_xticks([])
            ejes[i, j].set_yticks([])
        ejes[i, 0].set_ylabel(titulo, rotation=0, ha="right", va="center")
    plt.tight_layout()
    plt.show()
```

Estas ocho imágenes son de test. Ningún modelo las ha usado para ajustarse. Quedan como referencia para las filas de reconstrucción que vienen después.

```python
X_train_d, X_test_d = preparar_digitos()
print("train:", X_train_d.shape, "| test:", X_test_d.shape)
mostrar_imagenes([("original", X_test_d[:8])])
```

### El autoencoder

El codificador pasa de 64 píxeles a 128 y de ahí a 8 números. El decodificador recorre el camino inverso, de 8 a 128 y de 128 a 64. La capa de 128 combina los píxeles antes de comprimirlos. Ciento cincuenta épocas con Adam le dan tiempo a bajar el error de reconstrucción.

```python
class Autoencoder(nn.Module):
    """Comprime un vector de tamaño D y lo reconstruye.

    Args:
        D: Tamaño de la imagen estirada. Aquí 64.
        M: Tamaño de la capa intermedia.
        codigo: Cuántos números tiene el código latente.
    """

    def __init__(self, D, M, codigo):
        super().__init__()
        self.codificador = nn.Sequential(nn.Linear(D, M), nn.ReLU(), nn.Linear(M, codigo))
        self.decodificador = nn.Sequential(nn.Linear(codigo, M), nn.ReLU(), nn.Linear(M, D))

    def forward(self, x):
        """Reconstruye cada fila de x.

        Args:
            x: Tensor de forma (lote, D).

        Returns:
            Tensor de la misma forma que x.
        """
        codigo = self.codificador(x)
        return self.decodificador(codigo)
```

El bucle usa toda la matriz de train en cada paso. El objetivo de la pérdida es la propia imagen.

```python
def entrenar_autoencoder(X_train, epocas=150):
    """Ajusta el autoencoder para minimizar el error de reconstrucción.

    Args:
        X_train: Imágenes de train, una por fila.
        epocas: Pasadas completas por train.

    Returns:
        El modelo y la pérdida de cada época.
    """
    torch.manual_seed(42)
    X = torch.tensor(X_train, dtype=torch.float32)
    modelo = Autoencoder(D=X.shape[1], M=128, codigo=8)
    optimizador = torch.optim.Adam(modelo.parameters(), lr=1e-3)
    perdida_fn = nn.MSELoss()
    historial = []
    for epoca in range(epocas):
        optimizador.zero_grad()
        reconstruccion = modelo(X)
        perdida = perdida_fn(reconstruccion, X)
        perdida.backward()
        optimizador.step()
        historial.append(float(perdida))
    return modelo, historial
```

Esta función pasa las imágenes por el modelo ya entrenado y devuelve píxeles. Si el modelo es el VAE, se queda con la imagen y deja fuera la media y la varianza.

```python
def reconstruir(modelo, X):
    """Reconstruye un numpy array con el modelo, sin guardar gradiente.

    Args:
        modelo: Autoencoder o VAE entrenado.
        X: Imágenes, una por fila.

    Returns:
        Reconstrucciones en numpy, una por fila.
    """
    modelo.eval()
    with torch.no_grad():
        lote = torch.tensor(X, dtype=torch.float32)
        salida = modelo(lote)
        if isinstance(salida, tuple):
            salida = salida[0]
        return salida.numpy()
```

La fila de arriba es la imagen original. La de abajo es la reconstrucción del autoencoder. El ECM impreso resume todo el test, no solo estas ocho imágenes.

```python
ae_digitos, historial_ae = entrenar_autoencoder(X_train_d)
recon_ae = reconstruir(ae_digitos, X_test_d[:8])
ecm_ae = ecm(X_test_d, reconstruir(ae_digitos, X_test_d))
print("ECM autoencoder:", round(ecm_ae, 4), "| pérdida final:", round(historial_ae[-1], 4))
mostrar_imagenes([
    ("original", X_test_d[:8]),
    ("autoencoder", recon_ae),
])
```

**Comprobar:**

```python
assert historial_ae[-1] < historial_ae[0]
assert recon_ae.shape == (8, 64)
print("El autoencoder reconstruye los dígitos de test. OK")
```

---

## Los mismos dígitos, con un VAE

Los datos son las mismas imágenes. La tarea ya no es solo reconstruir un dígito visto. También queremos dibujar dígitos nuevos. El autoencoder guarda un punto por imagen.

Nada nos dice qué puntos del código corresponden a dígitos que no vimos. El VAE guarda una distribución por imagen. El codificador produce una media y una dispersión. El código es una muestra de esa distribución, y el decodificador la convierte en píxeles.

### El modelo

El codificador no devuelve el código directo. Devuelve una media `mu` y `log_var`, el logaritmo de la varianza de una gaussiana. Guardar el logaritmo mantiene la varianza positiva. Para reconstruir, se saca un código al azar de esa gaussiana. El ruido es una normal estándar, y la media y la varianza lo desplazan y lo estiran. El gradiente pasa por ese desplazamiento, así que el codificador aprende dónde colocar la gaussiana.

```python
class VAE(nn.Module):
    """Codifica cada imagen como una gaussiana y decodifica una muestra.

    Args:
        D: Tamaño de la imagen estirada.
        M: Tamaño de la capa intermedia.
        codigo: Dimensión de la gaussiana latente.
    """

    def __init__(self, D, M, codigo):
        super().__init__()
        self.codificador = nn.Sequential(nn.Linear(D, M), nn.ReLU())
        self.mu = nn.Linear(M, codigo)
        self.log_var = nn.Linear(M, codigo)
        self.decodificador = nn.Sequential(nn.Linear(codigo, M), nn.ReLU(), nn.Linear(M, D))

    def forward(self, x):
        """Reconstruye x y devuelve los parámetros de la gaussiana.

        Args:
            x: Tensor de forma (lote, D).

        Returns:
            La reconstrucción, la media y el logaritmo de la varianza.
        """
        h = self.codificador(x)
        mu = self.mu(h)
        log_var = self.log_var(h)
        epsilon = torch.randn_like(mu)
        z = mu + torch.exp(0.5 * log_var) * epsilon
        return self.decodificador(z), mu, log_var
```

La pérdida tiene dos partes. La primera es el error de reconstrucción, la suma de los cuadrados entre cada píxel y la imagen que devuelve el decodificador. La segunda es la divergencia KL. `log_var.exp()` es la varianza, y esa línea mide cuánto se aleja la gaussiana de una normal estándar, de media 0 y varianza 1. Acercarlas a esa normal llena el espacio del código. Un código nuevo, sacado de esa misma normal, cae en una zona que el decodificador ya recorrió al entrenar.

```python
def perdida_vae(reconstruccion, x, mu, log_var):
    """Suma el error de reconstrucción y la divergencia KL.

    Args:
        reconstruccion: Imagen producida por el decodificador.
        x: Imagen original.
        mu: Media del código.
        log_var: Logaritmo de la varianza del código.

    Returns:
        Un escalar con las dos partes de la pérdida.
    """
    reconstruccion_ecm = ((x - reconstruccion) ** 2).sum()
    kl = -0.5 * (1 + log_var - mu ** 2 - log_var.exp()).sum()
    return reconstruccion_ecm + kl
```

El bucle es el del autoencoder. Cambia la pérdida, que ahora suma la reconstrucción y la KL.

```python
def entrenar_vae(X_train, epocas=80):
    """Ajusta el VAE con reconstrucción más KL.

    Args:
        X_train: Imágenes de train, una por fila.
        epocas: Pasadas completas por train.

    Returns:
        El modelo y la pérdida de cada época.
    """
    torch.manual_seed(42)
    X = torch.tensor(X_train, dtype=torch.float32)
    modelo = VAE(D=X.shape[1], M=128, codigo=8)
    optimizador = torch.optim.Adam(modelo.parameters(), lr=1e-3)
    historial = []
    for epoca in range(epocas):
        optimizador.zero_grad()
        reconstruccion, mu, log_var = modelo(X)
        perdida = perdida_vae(reconstruccion, X, mu, log_var)
        perdida.backward()
        optimizador.step()
        historial.append(float(perdida))
    return modelo, historial
```

Un código nuevo es un vector de 8 números sacado de la normal estándar. `mu.out_features` es ese largo, 8. El decodificador convierte cada vector en 64 píxeles. Esa imagen no copia un dígito del conjunto.

```python
def muestras_vae(modelo, n=8):
    """Decodifica n códigos sacados de la normal estándar.

    Args:
        modelo: Un VAE entrenado.
        n: Cuántas imágenes nuevas dibujar.

    Returns:
        Un array de forma (n, D).
    """
    modelo.eval()
    with torch.no_grad():
        z = torch.randn(n, modelo.mu.out_features)
        return modelo.decodificador(z).numpy()
```

La fila de arriba es el dígito original. La del medio es la reconstrucción del VAE para esa misma imagen. La de abajo no parte de una foto. Parte de 8 códigos nuevos, sacados de la normal estándar, y el decodificador los dibuja. El ECM del VAE suele quedar por encima del autoencoder, porque parte del ajuste se gasta en la KL.

```python
vae_digitos, historial_vae = entrenar_vae(X_train_d)
ecm_vae = ecm(X_test_d, reconstruir(vae_digitos, X_test_d))
print("ECM VAE:", round(ecm_vae, 4), "| pérdida final:", round(historial_vae[-1], 1))
mostrar_imagenes([
    ("original", X_test_d[:8]),
    ("VAE", reconstruir(vae_digitos, X_test_d[:8])),
    ("muestras", muestras_vae(vae_digitos)),
])
```

**Comprobar:**

```python
assert historial_vae[-1] < historial_vae[0]
assert muestras_vae(vae_digitos).shape == (8, 64)
print("El VAE reconstruye y puede muestrear. OK")
```

---

## Artículos y citas de Cora

Cora es una red de 2708 artículos. Cada artículo es una bolsa de 1433 palabras, y una arista lo une con los artículos que cita. La tarea es predecir el tema del artículo, entre 7 temas. La partición ya viene dada: 140 artículos de train y 1000 de test.

Una logística mira solo las palabras de cada artículo e ignora las citas. Eso falla cuando dos artículos del mismo tema se citan pero no comparten las mismas palabras.

Una capa convolucional de grafos mezcla cada artículo con sus vecinos. El tema puede llegar por una cita, no solo por el texto.

### El grafo

`torch_geometric` descarga el grafo de Cora y las máscaras de train y de test. La capa que mezcla vecinos la escribimos debajo, para ver la multiplicación por la matriz de citas.

```python
%pip install -q torch_geometric
```

La matriz `A` tiene un 1 donde un artículo cita a otro. `Planetoid(...)[0]` se queda con el único grafo de la lista. Al crear `A` está llena de ceros, una fila y una columna por artículo. `edge_index` trae cada cita como un par de origen y destino, y `A[origen, destino] = 1` escribe ese 1.

```python
from torch_geometric.datasets import Planetoid


def cargar_cora():
    """Descarga Cora y arma la matriz de adyacencia.

    Returns:
        El grafo de Planetoid y una matriz A con 1 en cada cita.
    """
    grafo = Planetoid(root="datos_cora", name="Cora")[0]
    n = grafo.num_nodes
    A = torch.zeros(n, n)
    origen, destino = grafo.edge_index
    A[origen, destino] = 1.0
    return grafo, A
```

`cora.x` es la matriz de palabras. Una fila es un artículo y una columna es una palabra, con 0 o 1. `train_mask` es un vector de verdadero o falso, uno por fila. No es una columna de la matriz. `cora.x[train_mask]` se queda con las filas marcadas verdadero, igual que `entradas[en_train]`.

```python
cora, A_cora = cargar_cora()
print("cora.x", tuple(cora.x.shape), "| A", tuple(A_cora.shape))
print("train", int(cora.train_mask.sum()), "| test", int(cora.test_mask.sum()))
print("primeras banderas de train_mask:", cora.train_mask[:8].numpy())
print("filas de train", tuple(cora.x[cora.train_mask].shape))
```

Las primeras banderas dicen qué artículos del inicio entran en train. La logística ve solo esas 140 filas, cada una con 1433 palabras. La red sobre el grafo recibe las 2708 filas, y la máscara solo elige cuáles entran en la pérdida.

La barra de la izquierda cuenta cuántos artículos hay en cada uno de los 7 temas. El histograma de la derecha cuenta las citas de cada artículo. La suma de cada fila de `A` es cuántas citas salen de ese artículo. La mayoría tiene pocas, y unos pocos están muy conectados. Esa diferencia importa al mezclar vecinos. Un artículo con muchas citas arrastraría la suma si cada fila no se escala.

```python
print("nodos:", cora.num_nodes, "| características:", cora.num_features)

temas, cuentas = np.unique(cora.y.numpy(), return_counts=True)
fig, ejes = plt.subplots(1, 2, figsize=(9, 3))
ejes[0].bar(temas, cuentas, color="steelblue")
ejes[0].set_xlabel("tema")
ejes[0].set_ylabel("artículos")
ejes[0].set_title("Artículos por tema")
ejes[1].hist(A_cora.sum(dim=1).numpy(), bins=30, color="steelblue")
ejes[1].set_xlabel("citas")
ejes[1].set_ylabel("artículos")
ejes[1].set_title("Cuántas citas tiene cada artículo")
plt.tight_layout()
plt.show()
```

### Línea base sin grafo

La logística ve solo la bolsa de 1433 palabras. No ve qué artículos se citan. `cora.x[train_mask]` deja las 140 filas de train, y `test_mask` deja las 1000 de test. Se ajusta con esas 140 y se mide en las 1000. Es el piso de un modelo que ignora el grafo. La GCN tiene que superar este número usando las mismas palabras más las citas.

```python
logistica_cora = LogisticRegression(max_iter=2000)
X_train_cora = cora.x[cora.train_mask].numpy()
y_train_cora = cora.y[cora.train_mask].numpy()
X_test_cora = cora.x[cora.test_mask].numpy()
y_test_cora = cora.y[cora.test_mask].numpy()
logistica_cora.fit(X_train_cora, y_train_cora)
exactitud_logistica = float(logistica_cora.score(X_test_cora, y_test_cora))
print("exactitud logística sin grafo:", round(exactitud_logistica, 3))
```

### La capa

Sumar la identidad pone un 1 en la diagonal. Cada artículo conserva sus propias palabras además de las de sus vecinos. El grado es el número de citas más uno, por ese bucle. Dividir por la raíz del grado deja en la misma escala a un artículo muy citado y a uno casi aislado. En el código, `A + eye` arma esa diagonal, el grado elevado a `-1/2` queda en otra diagonal, y multiplicar por la izquierda y por la derecha escala filas y columnas. Después la capa lineal cambia el tamaño del vector y `A_hat` mezcla cada artículo con sus vecinos. Los pesos de esa capa son los mismos para todos los artículos. La última capa deja la activación apagada. ReLU pondría a cero los puntajes negativos, y un tema con puntaje negativo dejaría de competir.

```python
class CapaGCN(nn.Module):
    """Una capa que mezcla el vector de cada nodo con el de sus vecinos.

    Args:
        n_entrada: Tamaño del vector que llega.
        n_salida: Tamaño del vector que sale.
        activar: Si es False, no aplica ReLU. La última capa deja los puntajes libres.
    """

    def __init__(self, n_entrada, n_salida, activar=True):
        super().__init__()
        self.lineal = nn.Linear(n_entrada, n_salida)
        self.activar = activar

    def forward(self, H, A):
        """Aplica la convolución del grafo.

        Args:
            H: Vectores de los nodos, forma (nodos, n_entrada).
            A: Adyacencia, forma (nodos, nodos).

        Returns:
            Vectores nuevos, forma (nodos, n_salida).
        """
        A_tilde = A + torch.eye(A.shape[0])
        D_inv_sqrt = torch.diag(A_tilde.sum(dim=1).pow(-0.5))
        A_hat = D_inv_sqrt @ A_tilde @ D_inv_sqrt
        mezclado = A_hat @ self.lineal(H)
        if self.activar:
            return torch.relu(mezclado)
        return mezclado
```

La primera capa mezcla a cada artículo con los que cita directamente. La segunda repite la mezcla, así que el tema puede llegar desde un artículo a dos citas de distancia. Dieciséis es el tamaño del vector intermedio.

```python
class RedGCN(nn.Module):
    """Dos capas de convolución sobre el grafo.

    Args:
        n_entrada: Número de palabras, 1433 en Cora.
        n_oculta: Tamaño del vector intermedio.
        n_clases: Número de temas.
    """

    def __init__(self, n_entrada, n_oculta, n_clases):
        super().__init__()
        self.capa1 = CapaGCN(n_entrada, n_oculta)
        self.capa2 = CapaGCN(n_oculta, n_clases, activar=False)

    def forward(self, H, A):
        """Devuelve un puntaje por tema para cada artículo.

        Args:
            H: Bolsas de palabras.
            A: Adyacencia de citas.

        Returns:
            Tensor de forma (nodos, n_clases), sin softmax.
        """
        return self.capa2(self.capa1(H, A), A)
```

`train_mask` marca los 140 artículos cuya etiqueta entra en la pérdida. Cada paso ve el grafo entero, porque un vecino de test puede estar citado por uno de train. El error solo se calcula en esos 140. Los 1000 de test se reservan para medir la exactitud. Los temas van de 0 a 6. `y.max()` vale 6, y sumarle 1 da las 7 clases. `argmax` elige el tema con el puntaje más alto.

```python
def entrenar_gcn(grafo, A, epocas=200):
    """Ajusta la GCN solo con los artículos marcados como train.

    Args:
        grafo: Objeto de Cora, con x, y y las máscaras.
        A: Matriz de adyacencia.
        epocas: Pasos de gradiente. Cada paso ve el grafo entero.

    Returns:
        El modelo, la pérdida de cada época y la exactitud en test.
    """
    torch.manual_seed(42)
    modelo = RedGCN(grafo.num_features, n_oculta=16, n_clases=int(grafo.y.max()) + 1)
    optimizador = torch.optim.Adam(modelo.parameters(), lr=0.01)
    historial = []
    for epoca in range(epocas):
        optimizador.zero_grad()
        puntajes = modelo(grafo.x, A)
        perdida = nn.functional.cross_entropy(puntajes[grafo.train_mask], grafo.y[grafo.train_mask])
        perdida.backward()
        optimizador.step()
        historial.append(float(perdida))
    modelo.eval()
    with torch.no_grad():
        pred = modelo(grafo.x, A).argmax(dim=1)[grafo.test_mask].numpy()
        exactitud = accuracy_score(grafo.y[grafo.test_mask].numpy(), pred)
    return modelo, historial, float(exactitud)
```

La barra compara la exactitud de la logística y la de la GCN en los mismos 1000 artículos. La altura es la fracción de temas acertados. La logística usa solo las palabras. La GCN usa las palabras y las citas.

```python
gcn_cora, historial_gcn, exactitud_gcn = entrenar_gcn(cora, A_cora)
print("exactitud GCN:", round(exactitud_gcn, 3), "| pérdida final:", round(historial_gcn[-1], 3))

plt.figure(figsize=(4, 3))
plt.bar(["logística", "GCN"], [exactitud_logistica, exactitud_gcn], color=["gray", "steelblue"])
plt.ylabel("exactitud en test")
plt.ylim(0, 1)
plt.title("Palabras solas frente a palabras y citas")
plt.show()
```

**Comprobar:**

```python
assert cora.num_nodes == 2708
assert int(cora.train_mask.sum()) == 140
assert historial_gcn[-1] < historial_gcn[0]
assert exactitud_gcn > exactitud_logistica
print("La GCN usa las citas y supera a la logística. OK")
```

<!-- end NOTEBOOK: -->
