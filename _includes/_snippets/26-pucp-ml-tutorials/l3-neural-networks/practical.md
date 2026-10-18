<!-- NOTEBOOK: -->

Este cuaderno se organiza en dos secciones:

1. **Parte guiada:** Cinco arquitecturas, cada una sobre un conjunto clásico y frente a una línea base lineal o simple.
   - **A:** un perceptrón multicapa (MLP), desde cero en numpy y con scikit-learn, sobre las **dos lunas** (`make_moons`).
   - **B:** una red recurrente (RNN), desde cero y con una LSTM de PyTorch, sobre las **manchas solares** de 1700 a 2008.
   - **C:** un **autoencoder** y un **VAE** sobre los **dígitos** 8x8 (`load_digits`).
   - **D:** un **modelo de difusión** (DDPM) que genera puntos de las dos lunas.
   - **E:** una **red neuronal de grafos** (GCN) sobre la red de citas **Cora**.
2. **Parte individual:** Los estudiantes eligen una arquitectura y la replican sobre otro conjunto clásico.

Ejecute las celdas de arriba hacia abajo. En cada **Comprobar**, confirme el mensaje `OK` antes de seguir.

---

## Importaciones

```python
import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.api as sm
import torch
from sklearn.datasets import fetch_olivetti_faces, load_digits, make_circles, make_moons
from sklearn.decomposition import PCA
from sklearn.exceptions import ConvergenceWarning
from sklearn.linear_model import LinearRegression, LogisticRegression, Perceptron
from sklearn.metrics import accuracy_score
from sklearn.mixture import GaussianMixture
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from torch import nn
```

---

## Parte guiada A — MLP sobre las dos lunas

### Paso 1 — Datos y líneas base

500 puntos en dos medias lunas entrelazadas, con ruido. Partición 70/30 estratificada, `random_state=42`, y escalado con la media y la desviación de train. Las líneas base son la clase mayoritaria, la logística y el perceptrón de la sesión 2.

```python
def preparar_clasificacion_2d(X, y):
    """Partición 70/30 estratificada, escalado de train y líneas base."""
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=42, stratify=y)
    escalador = StandardScaler().fit(X_train)
    X_train_esc, X_test_esc = escalador.transform(X_train), escalador.transform(X_test)
    bases = {
        "piso (mayoría)": float(max(y_test.mean(), 1 - y_test.mean())),
        "logística": LogisticRegression().fit(X_train_esc, y_train).score(X_test_esc, y_test),
        "perceptrón": Perceptron(random_state=42).fit(X_train_esc, y_train).score(X_test_esc, y_test),
    }
    return X_train_esc, X_test_esc, y_train, y_test, bases


X_lunas, y_lunas = make_moons(n_samples=500, noise=0.25, random_state=42)
X_train_esc, X_test_esc, y_train, y_test, bases_lunas = preparar_clasificacion_2d(X_lunas, y_lunas)
print("train:", len(y_train), "| test:", len(y_test))
print({k: round(v, 3) for k, v in bases_lunas.items()})
```

### La red, en la notación de las diapositivas

$D = 2$ entradas, $M = 8$ unidades ocultas con $h = \tanh$ y una salida sigmoide $\hat{y}$, la probabilidad de la clase 1. $y$ es la etiqueta (0/1). Como hay una sola salida, quitamos el índice $k$.

$$
\begin{aligned}
a_j &= \sum_{i=1}^{D} w_{ji}^{(1)} x_i + w_{j0}^{(1)} \\
z_j &= h(a_j) \\
\hat{y} &= \sigma\Big(\sum_{j=1}^{M} w_{j}^{(2)} z_j + w_{0}^{(2)}\Big)
\end{aligned}
$$

| Símbolo | En el código | Forma |
|---|---|---|
| $w_{ji}^{(1)}$ | `params["W1"]` | $(M, D)$ |
| $w_{j0}^{(1)}$ | `params["b1"]` | $(M,)$ |
| $w_{j}^{(2)}$ | `params["W2"]` | $(M,)$ |
| $w_{0}^{(2)}$ | `params["b2"]` | escalar |

### Paso 2 — Propagación hacia adelante

La inicialización es la misma que usa `MLPClassifier` con $\tanh$ (uniforme de Glorot), para poder comparar después.

```python
def sigmoide(a):
    r"""Sigmoide $\sigma(a) = 1 / (1 + e^{-a})$."""
    return 1.0 / (1.0 + np.exp(-a))


def inicializar_red(n_entradas: int, n_ocultas: int, seed: int = 42) -> dict:
    r"""Pesos y sesgos iniciales uniformes en $[-l, l]$, con $l = \sqrt{6 / (\text{entradas} + \text{salidas})}$."""
    rng = np.random.default_rng(seed)
    l1 = np.sqrt(6.0 / (n_entradas + n_ocultas))
    l2 = np.sqrt(6.0 / (n_ocultas + 1))
    return {
        "W1": rng.uniform(-l1, l1, size=(n_ocultas, n_entradas)),
        "b1": rng.uniform(-l1, l1, size=n_ocultas),
        "W2": rng.uniform(-l2, l2, size=n_ocultas),
        "b2": float(rng.uniform(-l2, l2)),
    }


def propagar_adelante(X: np.ndarray, params: dict):
    r"""Devuelve $a$, $z$ y $\hat{y}$ para todas las filas de X."""
    a = X @ params["W1"].T + params["b1"]           # a_j
    z = np.tanh(a)                                  # z_j = h(a_j)
    y_hat = sigmoide(z @ params["W2"] + params["b2"])   # salida y_hat
    return a, z, y_hat


params_inicio = inicializar_red(X_train_esc.shape[1], n_ocultas=8)
a_ini, z_ini, y_hat_ini = propagar_adelante(X_train_esc, params_inicio)
print("forma de a y z:", a_ini.shape, "| primeras salidas y_hat:", np.round(y_hat_ini[:5], 3))
```

### Paso 3 — Pérdida de entropía cruzada

La pérdida de las diapositivas, promediada sobre las $N$ filas:

$$
E(\mathbf{w}) = - \frac{1}{N} \sum_{n=1}^N \{ y_n \ln \hat{y}_n + (1-y_n) \ln (1-\hat{y}_n) \}
$$

```python
def perdida_entropia_cruzada(y_hat: np.ndarray, y: np.ndarray) -> float:
    r"""Entropía cruzada media entre $\hat{y}$ y las etiquetas $y \in \{0, 1\}$."""
    y_hat = np.clip(y_hat, 1e-12, 1 - 1e-12)
    return float(-np.mean(y * np.log(y_hat) + (1 - y) * np.log(1 - y_hat)))


print("pérdida inicial:", round(perdida_entropia_cruzada(y_hat_ini, y_train), 4))
```

### Paso 4 — Retropropagación

$$
\begin{aligned}
\delta &= \hat{y} - y \\
\delta_j &= h'(a_j) \, w_j^{(2)} \delta, \quad h'(a_j) = 1 - \tanh^2(a_j) \\
\frac{\partial E_n}{\partial w_{ji}^{(1)}} &= \delta_j x_i, \quad \frac{\partial E_n}{\partial w_j^{(2)}} = \delta z_j
\end{aligned}
$$

```python
def retropropagar(X: np.ndarray, y: np.ndarray, params: dict) -> dict:
    r"""Gradiente medio de $E$ respecto a W1, b1, W2 y b2."""
    a, z, y_hat = propagar_adelante(X, params)
    n = len(X)
    delta = y_hat - y                                                  # (N,)
    delta_j = (1.0 - np.tanh(a) ** 2) * np.outer(delta, params["W2"])  # (N, M)
    return {
        "W1": delta_j.T @ X / n,
        "b1": delta_j.mean(axis=0),
        "W2": z.T @ delta / n,
        "b2": float(delta.mean()),
    }


def gradiente_numerico(X, y, params, nombre, indice, eps=1e-6):
    r"""Aproxima $\partial E / \partial w$ de un solo peso con diferencias centradas."""
    mas = {k: np.array(v, dtype=float) for k, v in params.items()}
    menos = {k: np.array(v, dtype=float) for k, v in params.items()}
    mas[nombre][indice] += eps
    menos[nombre][indice] -= eps
    e_mas = perdida_entropia_cruzada(propagar_adelante(X, mas)[2], y)
    e_menos = perdida_entropia_cruzada(propagar_adelante(X, menos)[2], y)
    return (e_mas - e_menos) / (2 * eps)
```

**Comprobar:**

```python
grad = retropropagar(X_train_esc, y_train, params_inicio)
for nombre, indice in [("W1", (0, 1)), ("W1", (3, 1)), ("b1", (5,)), ("W2", (2,)), ("b2", ())]:
    analitico = float(np.asarray(grad[nombre])[indice])
    numerico = gradiente_numerico(X_train_esc, y_train, params_inicio, nombre, indice)
    print(f"{nombre}{indice}: retropropagación {analitico:+.6f} | numérico {numerico:+.6f}")
    assert abs(analitico - numerico) < 1e-6, "La retropropagación no coincide con el gradiente numérico."
print("Gradientes verificados. OK")
```

### Paso 5 — Descenso de gradiente

Cada época usa todas las filas de train y aplica $w \leftarrow w - \alpha \, \partial E / \partial w$ a cada peso.

```python
def entrenar_red_numpy(X, y, n_ocultas: int = 8, alpha: float = 0.1, n_epochs: int = 2000, seed: int = 42):
    r"""Descenso de gradiente sobre la entropía cruzada. Devuelve los pesos y la pérdida por época.

    La pérdida se guarda antes de cada actualización, igual que ``loss_curve_`` de scikit-learn.
    """
    params = inicializar_red(X.shape[1], n_ocultas, seed=seed)
    historial = []
    for _ in range(n_epochs):
        historial.append(perdida_entropia_cruzada(propagar_adelante(X, params)[2], y))
        gradientes = retropropagar(X, y, params)
        for clave in params:
            params[clave] = params[clave] - alpha * gradientes[clave]
    return params, historial


def predecir_red_numpy(X: np.ndarray, params: dict) -> np.ndarray:
    r"""Predice 1 si $\hat{y} \geq 0.5$."""
    return (propagar_adelante(X, params)[2] >= 0.5).astype(int)


params_red, historial = entrenar_red_numpy(X_train_esc, y_train)
print("pérdida en la época 1:", round(historial[0], 4), "| última:", round(historial[-1], 4))
```

### Paso 6 — La misma red con scikit-learn

Misma arquitectura (8 unidades, $\tanh$), mismo optimizador: descenso de gradiente con todo el lote, sin momento, sin regularización (`alpha=0`), tasa $\alpha = 0.1$ y 2000 épocas. La tasa se eligió con un bloque de validación dentro de train. Solo cambian los pesos iniciales: mismo esquema, otro generador aleatorio.

En `MLPClassifier`, `alpha` es la penalización $L_2$, no la tasa de aprendizaje. La tasa es `learning_rate_init`.

```python
def entrenar_mlp_como_numpy(X, y, n_ocultas: int = 8, alpha: float = 0.1, n_epochs: int = 2000):
    """MLPClassifier configurado para hacer lo mismo que entrenar_red_numpy."""
    modelo = MLPClassifier(
        hidden_layer_sizes=(n_ocultas,), activation="tanh", solver="sgd",
        learning_rate="constant", learning_rate_init=alpha, momentum=0.0,
        batch_size=len(X), alpha=0.0, max_iter=n_epochs, shuffle=False,
        tol=0.0, n_iter_no_change=n_epochs, random_state=42,
    )
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", ConvergenceWarning)  # llega a max_iter a propósito
        modelo.fit(X, y)
    return modelo


def comparar_red_y_mlp(params, historial, modelo, X_train, y_train, X_test, y_test, bases):
    """Tabla de exactitud de las líneas base y de las dos redes."""
    filas = {nombre: [np.nan, valor, np.nan] for nombre, valor in bases.items()}
    filas["red numpy"] = [accuracy_score(y_train, predecir_red_numpy(X_train, params)),
                          accuracy_score(y_test, predecir_red_numpy(X_test, params)), historial[-1]]
    filas["MLPClassifier"] = [modelo.score(X_train, y_train), modelo.score(X_test, y_test), modelo.loss_curve_[-1]]
    return pd.DataFrame(filas, index=["exactitud train", "exactitud test", "pérdida final"]).T.round(3)


mlp = entrenar_mlp_como_numpy(X_train_esc, y_train)
tabla_lunas = comparar_red_y_mlp(params_red, historial, mlp, X_train_esc, y_train, X_test_esc, y_test, bases_lunas)
print(tabla_lunas.to_string())
```

### Paso 7 — Curvas de pérdida y fronteras

```python
def graficar_red_y_mlp(params, historial, modelo, X, y, titulo):
    """Curvas de pérdida superpuestas y fronteras de las dos redes, lado a lado."""
    fig, ejes = plt.subplots(1, 3, figsize=(16, 4.5))
    ejes[0].plot(historial, color="k", label="red numpy")
    ejes[0].plot(modelo.loss_curve_, color="C1", linestyle="--", label="MLPClassifier")
    ejes[0].set_xlabel("época")
    ejes[0].set_ylabel("entropía cruzada (train)")
    ejes[0].set_title(titulo)
    ejes[0].legend()

    x1, x2 = np.meshgrid(np.linspace(X[:, 0].min() - 0.5, X[:, 0].max() + 0.5, 200),
                         np.linspace(X[:, 1].min() - 0.5, X[:, 1].max() + 0.5, 200))
    rejilla = np.column_stack([x1.ravel(), x2.ravel()])
    probabilidades = {
        "red numpy": propagar_adelante(rejilla, params)[2],
        "MLPClassifier": modelo.predict_proba(rejilla)[:, 1],
    }
    for ax, (nombre, y_hat) in zip(ejes[1:], probabilidades.items()):
        ax.contourf(x1, x2, y_hat.reshape(x1.shape), levels=[0, 0.5, 1], colors=["#dde8f5", "#f5dddd"])
        ax.contour(x1, x2, y_hat.reshape(x1.shape), levels=[0.5], colors="k")
        ax.scatter(X[y == 0, 0], X[y == 0, 1], s=12, color="C0", label="clase 0")
        ax.scatter(X[y == 1, 0], X[y == 1, 1], s=12, color="C3", label="clase 1")
        ax.set_xlabel("$x_1$ (escalada)")
        ax.set_ylabel("$x_2$ (escalada)")
        ax.set_title(f"{nombre}: frontera y_hat = 0.5")
        ax.legend()
    plt.tight_layout()
    plt.show()


graficar_red_y_mlp(params_red, historial, mlp, X_train_esc, y_train, "Dos lunas: pérdida de train")
```

**Comprobar:**

```python
assert len(historial) == len(mlp.loss_curve_) == 2000
assert mlp.coefs_[0].shape == params_red["W1"].T.shape, "Las dos redes deben tener la misma arquitectura."
assert abs(historial[-1] - mlp.loss_curve_[-1]) < 0.1, "Las dos pérdidas finales deberían quedar cerca."
for red in ["red numpy", "MLPClassifier"]:
    assert tabla_lunas.loc[red, "exactitud test"] > bases_lunas["logística"] + 0.05
    assert tabla_lunas.loc[red, "exactitud test"] > bases_lunas["perceptrón"] + 0.05
print("Las dos redes superan a la logística y al perceptrón. OK")
```

---

## Parte guiada B — RNN sobre las manchas solares

### Paso 8 — Serie y ventanas

Número anual de manchas solares, 1700 a 2008 (viene con `statsmodels`). El ciclo dura unos 11 años, así que el valor del próximo año depende de los anteriores.

Cada fila es una ventana de 10 años y el objetivo $y$ es el año siguiente. La partición es **temporal**: train hasta 1950, test 1951 a 2008. La ventana y los ajustes de las redes se eligieron con los últimos 30 años de train como validación, no con test. Escalamos con la media y la desviación de train.

Las líneas base son la **persistencia** (el próximo año repite este), la **media** de train y una **regresión lineal** sobre la misma ventana. Medimos con la raíz del error cuadrático medio (RECM).

```python
def preparar_serie(valores, n_train: int, ventana: int = 10, log: bool = False) -> dict:
    """Ventanas, partición temporal en n_train, escala de train y líneas base.

    Con ``log=True`` las redes trabajan sobre ln(valores) y la RECM se mide en la escala original.
    """
    z = np.log(valores) if log else np.asarray(valores, dtype=float)
    X = np.stack([z[i - ventana:i] for i in range(ventana, len(z))])
    y = z[ventana:]
    en_train = np.arange(ventana, len(z)) < n_train
    media, desv = z[:n_train].mean(), z[:n_train].std()
    a_original = np.exp if log else (lambda v: v)
    serie = {
        "X_train": (X[en_train] - media) / desv, "y_train": (y[en_train] - media) / desv,
        "X_test": (X[~en_train] - media) / desv, "y_test": a_original(y[~en_train]),
        "a_original": lambda y_hat: a_original(y_hat * desv + media),
        "indice_test": np.arange(ventana, len(z))[~en_train],
    }
    lineal = LinearRegression().fit(X[en_train], y[en_train])
    serie["bases"] = {
        "persistencia": recm(serie["y_test"], a_original(X[~en_train, -1])),
        "media de train": recm(serie["y_test"], np.full((~en_train).sum(), a_original(y[en_train]).mean())),
        "regresión lineal": recm(serie["y_test"], a_original(lineal.predict(X[~en_train]))),
    }
    return serie


def recm(y, y_hat) -> float:
    """Raíz del error cuadrático medio."""
    return float(np.sqrt(np.mean((np.asarray(y) - np.asarray(y_hat)) ** 2)))


manchas = sm.datasets.sunspots.load_pandas().data
n_train_manchas = int((manchas["YEAR"] <= 1950).sum())
serie_manchas = preparar_serie(manchas["SUNACTIVITY"].to_numpy(), n_train_manchas)

fig, ax = plt.subplots(figsize=(12, 3))
ax.plot(manchas["YEAR"], manchas["SUNACTIVITY"], color="k", linewidth=0.8)
ax.axvline(1950.5, color="gray", linestyle="--")
ax.set_ylabel("manchas solares")
ax.set_title("Manchas solares, 1700-2008 (línea: fin de train)")
plt.show()
print("train:", len(serie_manchas["y_train"]), "| test:", len(serie_manchas["y_test"]))
print({k: round(v, 1) for k, v in serie_manchas["bases"].items()})
```

### Paso 9 — Una RNN desde cero

La notación es la de las diapositivas. En cada paso $t$ de la ventana, el estado oculto $\mathbf{h}_t$ combina la entrada $x_t$ con el estado anterior. La salida sale del último estado, $\mathbf{h}_T$:

$$
\begin{aligned}
\mathbf{h}_t &= \tanh\left(\mathbf{W}_{hh} \mathbf{h}_{t-1} + \mathbf{W}_{xh} x_t + \mathbf{b}_h\right), \quad \mathbf{h}_0 = \mathbf{0} \\
\hat{y} &= \mathbf{W}_{hy} \mathbf{h}_T + b_y \\
E &= \frac{1}{2N} \sum_{n=1}^N (\hat{y}_n - y_n)^2
\end{aligned}
$$

La retropropagación en el tiempo (BPTT) aplica la regla de la cadena hacia atrás, paso por paso. Con $\delta = \hat{y} - y$, el error en el último estado es $\delta \, \mathbf{W}_{hy}$, y cada paso hacia atrás lo multiplica por $1 - \mathbf{h}_t^2$ y por $\mathbf{W}_{hh}$. Ese producto repetido es el de las diapositivas, $\partial \mathbf{h}_t / \partial \mathbf{h}_k$.

```python
def inicializar_rnn(n_ocultas: int = 8, seed: int = 42) -> dict:
    """Pesos iniciales pequeños de una RNN con una entrada y una salida."""
    rng = np.random.default_rng(seed)
    return {
        "Wxh": rng.normal(0.0, 0.5, size=n_ocultas),
        "Whh": rng.normal(0.0, 0.5 / np.sqrt(n_ocultas), size=(n_ocultas, n_ocultas)),
        "bh": np.zeros(n_ocultas),
        "Why": rng.normal(0.0, 0.5, size=n_ocultas),
        "by": 0.0,
    }


def propagar_rnn(X: np.ndarray, params: dict):
    r"""Recorre la ventana paso a paso. Devuelve los estados $\mathbf{h}_0, \ldots, \mathbf{h}_T$ y $\hat{y}$."""
    h = np.zeros((len(X), len(params["bh"])))
    estados = [h]
    for t in range(X.shape[1]):
        h = np.tanh(h @ params["Whh"].T + np.outer(X[:, t], params["Wxh"]) + params["bh"])
        estados.append(h)
    y_hat = h @ params["Why"] + params["by"]
    return estados, y_hat


def bptt(X: np.ndarray, y: np.ndarray, params: dict) -> dict:
    r"""Gradiente de $E$ respecto a cada peso, por retropropagación en el tiempo."""
    estados, y_hat = propagar_rnn(X, params)
    delta = (y_hat - y) / len(X)                     # delta = y_hat - y, promediado
    grad = {"Why": estados[-1].T @ delta, "by": float(delta.sum()),
            "Wxh": np.zeros_like(params["Wxh"]), "Whh": np.zeros_like(params["Whh"]),
            "bh": np.zeros_like(params["bh"])}
    dh = np.outer(delta, params["Why"])              # dE/dh_T
    for t in range(X.shape[1], 0, -1):
        da = dh * (1.0 - estados[t] ** 2)            # a través de tanh
        grad["Wxh"] += da.T @ X[:, t - 1]
        grad["Whh"] += da.T @ estados[t - 1]
        grad["bh"] += da.sum(axis=0)
        dh = da @ params["Whh"]                      # hacia h_{t-1}
    return grad


def perdida_rnn(X, y, params) -> float:
    r"""$E = \frac{1}{2N} \sum_n (\hat{y}_n - y_n)^2$, en la escala de train."""
    return float(0.5 * np.mean((propagar_rnn(X, params)[1] - y) ** 2))
```

**Comprobar:**

```python
X_chico, y_chico = serie_manchas["X_train"], serie_manchas["y_train"]
params_rnn_inicio = inicializar_rnn()
grad_rnn = bptt(X_chico, y_chico, params_rnn_inicio)
for nombre, indice in [("Wxh", (2,)), ("Whh", (1, 4)), ("bh", (0,)), ("Why", (5,)), ("by", ())]:
    mas = {k: np.array(v, dtype=float) for k, v in params_rnn_inicio.items()}
    menos = {k: np.array(v, dtype=float) for k, v in params_rnn_inicio.items()}
    mas[nombre][indice] += 1e-6
    menos[nombre][indice] -= 1e-6
    numerico = (perdida_rnn(X_chico, y_chico, mas) - perdida_rnn(X_chico, y_chico, menos)) / 2e-6
    analitico = float(np.asarray(grad_rnn[nombre])[indice])
    print(f"{nombre}{indice}: BPTT {analitico:+.6f} | numérico {numerico:+.6f}")
    assert abs(analitico - numerico) < 1e-5, "BPTT no coincide con el gradiente numérico."
print("Gradientes de la RNN verificados. OK")
```

### Paso 10 — Entrenar la RNN numpy y una LSTM de PyTorch

La RNN numpy usa descenso de gradiente con todo el lote ($\alpha = 0.3$, 1000 épocas). La LSTM es la de las diapositivas, con 8 unidades, `Adam` y 300 épocas.

```python
def entrenar_rnn_numpy(X, y, n_ocultas: int = 8, alpha: float = 0.3, n_epochs: int = 1000, seed: int = 42):
    """Descenso de gradiente con BPTT. Devuelve los pesos y la pérdida de train por época."""
    params = inicializar_rnn(n_ocultas, seed)
    historial = []
    for _ in range(n_epochs):
        historial.append(perdida_rnn(X, y, params))
        grad = bptt(X, y, params)
        for clave in params:
            params[clave] = params[clave] - alpha * grad[clave]
    return params, historial


class LSTMSerie(nn.Module):
    """LSTM de 8 unidades que lee la ventana paso a paso -> una salida desde el último estado."""

    def __init__(self, n_features: int = 1, n_hidden: int = 8):
        super().__init__()
        self.lstm = nn.LSTM(n_features, n_hidden, batch_first=True)
        self.head = nn.Linear(n_hidden, 1)

    def forward(self, x):                 # x: (batch, T, n_features)
        out, (h_T, c_T) = self.lstm(x)
        return self.head(h_T[-1]).squeeze(-1)


def entrenar_lstm(X, y, n_epochs: int = 300, tasa: float = 0.01):
    """Entrena con todo el lote y error cuadrático medio. Devuelve el modelo y el ECM de train por época."""
    torch.manual_seed(42)
    modelo = LSTMSerie()
    optimizador = torch.optim.Adam(modelo.parameters(), lr=tasa)
    X_tensor = torch.tensor(X, dtype=torch.float32).unsqueeze(-1)
    y_tensor = torch.tensor(y, dtype=torch.float32)
    historial = []
    for _ in range(n_epochs):
        optimizador.zero_grad()
        perdida = nn.functional.mse_loss(modelo(X_tensor), y_tensor)
        perdida.backward()
        optimizador.step()
        historial.append(perdida.item())
    return modelo, historial


def predecir_lstm(modelo, X) -> np.ndarray:
    """y_hat de la LSTM en la escala de train."""
    with torch.no_grad():
        return modelo(torch.tensor(X, dtype=torch.float32).unsqueeze(-1)).numpy()


params_rnn, historial_rnn = entrenar_rnn_numpy(serie_manchas["X_train"], serie_manchas["y_train"])
lstm, historial_lstm = entrenar_lstm(serie_manchas["X_train"], serie_manchas["y_train"])
print("pérdida final de train, RNN numpy:", round(historial_rnn[-1], 4), "| LSTM (ECM):", round(historial_lstm[-1], 4))
```

### Paso 11 — Comparación en test

```python
def comparar_series(serie, params_rnn, modelo_lstm, eje_x, titulo, unidad):
    """Tabla de RECM en test y gráfico de predicción frente a valor real."""
    y_hat_rnn = serie["a_original"](propagar_rnn(serie["X_test"], params_rnn)[1])
    y_hat_lstm = serie["a_original"](predecir_lstm(modelo_lstm, serie["X_test"]))
    tabla = pd.Series({**serie["bases"],
                       "RNN numpy": recm(serie["y_test"], y_hat_rnn),
                       "LSTM (PyTorch)": recm(serie["y_test"], y_hat_lstm)}, name=f"RECM test ({unidad})")
    fig, ax = plt.subplots(figsize=(12, 3.5))
    ax.plot(eje_x, serie["y_test"], color="gray", linewidth=1.5, label="real")
    ax.plot(eje_x, y_hat_rnn, label="RNN numpy")
    ax.plot(eje_x, y_hat_lstm, label="LSTM (PyTorch)")
    ax.set_ylabel(unidad)
    ax.set_title(titulo)
    ax.legend()
    plt.show()
    return tabla


tabla_manchas = comparar_series(serie_manchas, params_rnn, lstm, manchas["YEAR"].to_numpy()[serie_manchas["indice_test"]],
                                "Manchas solares, test 1951-2008: un año adelante", "manchas solares")
print(tabla_manchas.round(1).to_string())
```

La regresión lineal sobre la misma ventana queda casi a la par: con 241 filas de train, una recta sobre los últimos 10 años ya captura buena parte del ciclo.

**Comprobar:**

```python
assert len(manchas) == 309 and serie_manchas["indice_test"].min() == n_train_manchas
assert historial_rnn[-1] < historial_rnn[0] and historial_lstm[-1] < historial_lstm[0]
for red in ["RNN numpy", "LSTM (PyTorch)"]:
    assert tabla_manchas[red] < tabla_manchas["persistencia"] and tabla_manchas[red] < tabla_manchas["media de train"]
print("RNN numpy y LSTM superan a la persistencia y a la media. OK")
```

---

## Parte guiada C — Autoencoder y VAE sobre dígitos

### Paso 12 — Datos y línea base lineal

`load_digits`: 1797 imágenes de 8x8 píxeles, escaladas a $[0, 1]$. Partición 70/30, `random_state=42`. La línea base lineal es PCA con la misma dimensión latente, $K = 8$.

```python
def preparar_imagenes(X, K: int = 8):
    """Partición 70/30, escala a [0, 1] y reconstrucción PCA con K componentes."""
    X = X / X.max()
    X_train, X_test = train_test_split(X, test_size=0.30, random_state=42)
    pca = PCA(n_components=K).fit(X_train)
    X_hat_pca = pca.inverse_transform(pca.transform(X_test))
    return X_train, X_test, X_hat_pca


digitos = load_digits()
X_train_d, X_test_d, X_hat_pca_d = preparar_imagenes(digitos.data)
print("train:", X_train_d.shape, "| test:", X_test_d.shape)
print("ECM PCA (test):", round(float(np.mean((X_hat_pca_d - X_test_d) ** 2)), 4))
```

### Paso 13 — Autoencoder y VAE

El autoencoder comprime $\mathbf{x}$ en $\mathbf{z}$ con el codificador y lo reconstruye como $\hat{\mathbf{x}}$ con el decodificador. La pérdida es el error de reconstrucción. El VAE codifica una media $\boldsymbol{\mu}$ y una log-varianza $\ln \boldsymbol{\sigma}^2$, muestrea $\mathbf{z} = \boldsymbol{\mu} + \boldsymbol{\sigma} \odot \boldsymbol{\epsilon}$, y suma a la pérdida la divergencia KL con la previa $\mathcal{N}(\mathbf{0}, \mathbf{I})$:

$$
E = \|\mathbf{x} - \hat{\mathbf{x}}\|^2 - \frac{1}{2} \sum_{k=1}^{K} \left(1 + \ln \sigma_k^2 - \mu_k^2 - \sigma_k^2\right)
$$

```python
class Autoencoder(nn.Module):
    """Codificador D -> 64 -> K y decodificador K -> 64 -> D. Con variacional=True es un VAE."""

    def __init__(self, D: int, K: int = 8, variacional: bool = False):
        super().__init__()
        self.variacional = variacional
        self.codificador = nn.Sequential(nn.Linear(D, 64), nn.ReLU(), nn.Linear(64, 2 * K if variacional else K))
        self.decodificador = nn.Sequential(nn.Linear(K, 64), nn.ReLU(), nn.Linear(64, D), nn.Sigmoid())

    def codificar(self, x):
        """Devuelve mu y log-varianza (en el autoencoder, log-varianza es None)."""
        h = self.codificador(x)
        return h.chunk(2, dim=-1) if self.variacional else (h, None)

    def forward(self, x):
        mu, log_var = self.codificar(x)
        z = mu + torch.randn_like(mu) * torch.exp(0.5 * log_var) if self.variacional else mu
        return self.decodificador(z), mu, log_var


def entrenar_autoencoder(X, variacional: bool = False, K: int = 8, n_epochs: int = 500):
    """Adam en lotes de 128. Devuelve el modelo y la pérdida media por época."""
    torch.manual_seed(42)
    modelo = Autoencoder(X.shape[1], K, variacional)
    optimizador = torch.optim.Adam(modelo.parameters(), lr=1e-3)
    x = torch.tensor(X, dtype=torch.float32)
    historial = []
    for _ in range(n_epochs):
        perdidas = []
        for lote in torch.randperm(len(x)).split(128):
            optimizador.zero_grad()
            x_hat, mu, log_var = modelo(x[lote])
            perdida = ((x_hat - x[lote]) ** 2).sum(dim=1).mean()
            if variacional:
                perdida = perdida - 0.5 * (1 + log_var - mu ** 2 - log_var.exp()).sum(dim=1).mean()
            perdida.backward()
            optimizador.step()
            perdidas.append(perdida.item())
        historial.append(np.mean(perdidas))
    return modelo, historial


def reconstruir(modelo, X) -> np.ndarray:
    """Reconstrucción usando la media del código, sin muestrear."""
    with torch.no_grad():
        mu, _ = modelo.codificar(torch.tensor(X, dtype=torch.float32))
        return modelo.decodificador(mu).numpy()


ae_d, historial_ae_d = entrenar_autoencoder(X_train_d)
vae_d, historial_vae_d = entrenar_autoencoder(X_train_d, variacional=True)
tabla_digitos = pd.Series({
    "PCA (K = 8)": float(np.mean((X_hat_pca_d - X_test_d) ** 2)),
    "autoencoder": float(np.mean((reconstruir(ae_d, X_test_d) - X_test_d) ** 2)),
    "VAE": float(np.mean((reconstruir(vae_d, X_test_d) - X_test_d) ** 2)),
}, name="ECM de reconstrucción (test)")
print(tabla_digitos.round(4).to_string())
```

El VAE reconstruye peor que PCA: paga el término KL a cambio de un espacio latente del que se puede muestrear.

### Paso 14 — Reconstrucciones y muestras

```python
def mostrar_imagenes(filas: dict, forma, titulo):
    """Una fila de imágenes por entrada de ``filas``."""
    n = len(next(iter(filas.values())))
    fig, ejes = plt.subplots(len(filas), n, figsize=(1.2 * n, 1.3 * len(filas)))
    for i, (nombre, imagenes) in enumerate(filas.items()):
        for j in range(n):
            ejes[i, j].imshow(imagenes[j].reshape(forma), cmap="gray_r")
            ejes[i, j].axis("off")
        ejes[i, 0].set_title(nombre, fontsize=9, loc="left")
    fig.suptitle(titulo)
    plt.tight_layout()
    plt.show()


def muestras_vae(modelo, n: int = 10, K: int = 8) -> np.ndarray:
    """Decodifica n códigos z de la previa N(0, I)."""
    torch.manual_seed(0)
    with torch.no_grad():
        return modelo.decodificador(torch.randn(n, K)).numpy()


mostrar_imagenes({
    "original": X_test_d[:10],
    "autoencoder": reconstruir(ae_d, X_test_d[:10]),
    "VAE": reconstruir(vae_d, X_test_d[:10]),
    "PCA": X_hat_pca_d[:10],
    "VAE, muestras de la previa": muestras_vae(vae_d),
}, (8, 8), "Dígitos 8x8")
```

**Comprobar:**

```python
assert X_train_d.shape[1] == 64 and 0 <= X_train_d.min() and X_train_d.max() <= 1
assert historial_ae_d[-1] < historial_ae_d[0] and historial_vae_d[-1] < historial_vae_d[0]
assert tabla_digitos["autoencoder"] < tabla_digitos["PCA (K = 8)"], "El autoencoder debería reconstruir mejor que PCA."
print("Autoencoder y VAE entrenados. OK")
```

---

## Parte guiada D — Modelo de difusión sobre las dos lunas

### Paso 15 — Datos y líneas base

2000 puntos de `make_moons` con poco ruido, estandarizados: 1500 para entrenar y 500 reservados para medir. Las líneas base son una sola gaussiana multivariada y una mezcla de 8 gaussianas (`GaussianMixture`), ajustadas a los mismos 1500 puntos.

Medimos con la **distancia de energía** entre 500 muestras generadas y los 500 puntos reservados: $2\,\mathbb{E}\|\mathbf{a} - \mathbf{b}\| - \mathbb{E}\|\mathbf{a} - \mathbf{a}'\| - \mathbb{E}\|\mathbf{b} - \mathbf{b}'\|$. Vale 0 si las dos distribuciones son iguales. Como referencia, medimos también 500 puntos reales de train frente a los reservados.

```python
def distancia_energia(a: np.ndarray, b: np.ndarray) -> float:
    """Distancia de energía entre dos nubes de puntos. Cero si vienen de la misma distribución."""
    media_dist = lambda p, q: np.mean(np.linalg.norm(p[:, None] - q[None], axis=-1))
    return float(2 * media_dist(a, b) - media_dist(a, a) - media_dist(b, b))


def preparar_2d(X):
    """Estandariza y separa 1500 puntos para entrenar y el resto para medir. Ajusta las líneas base."""
    X = (X - X.mean(axis=0)) / X.std(axis=0)
    X_train, X_reserva = X[:1500], X[1500:]
    gaussiana = np.random.default_rng(0).multivariate_normal(X_train.mean(axis=0), np.cov(X_train.T), 500)
    mezcla = GaussianMixture(n_components=8, random_state=42).fit(X_train).sample(500)[0]
    bases = {
        "real (train) frente a reserva": distancia_energia(X_train[:500], X_reserva),
        "una gaussiana": distancia_energia(gaussiana, X_reserva),
        "mezcla de 8 gaussianas": distancia_energia(mezcla, X_reserva),
    }
    return X_train, X_reserva, {"una gaussiana": gaussiana, "mezcla de 8 gaussianas": mezcla}, bases


X_lunas_gen, _ = make_moons(n_samples=2000, noise=0.05, random_state=42)
X_train_g, X_reserva_g, muestras_base_g, bases_g = preparar_2d(X_lunas_gen)
print({k: round(v, 4) for k, v in bases_g.items()})
```

### Paso 16 — Un DDPM pequeño

El proceso hacia adelante agrega ruido gaussiano en $T = 100$ pasos: $\mathbf{x}_t = \sqrt{\bar{\alpha}_t}\, \mathbf{x}_0 + \sqrt{1 - \bar{\alpha}_t}\, \boldsymbol{\epsilon}$. Una MLP aprende a predecir $\boldsymbol{\epsilon}$ a partir de $\mathbf{x}_t$ y $t$, con error cuadrático. Para generar, partimos de ruido puro y quitamos el ruido predicho paso a paso, de $t = T$ a $t = 1$.

```python
T_DIFUSION = 100
betas = torch.linspace(1e-4, 0.02, T_DIFUSION)
alphas = 1 - betas
alphas_bar = torch.cumprod(alphas, dim=0)


class RedRuido(nn.Module):
    """MLP que predice el ruido epsilon a partir de (x_t, t / T)."""

    def __init__(self):
        super().__init__()
        self.red = nn.Sequential(nn.Linear(3, 128), nn.ReLU(), nn.Linear(128, 128), nn.ReLU(), nn.Linear(128, 2))

    def forward(self, x, t):
        return self.red(torch.cat([x, (t.float() / T_DIFUSION).unsqueeze(-1)], dim=-1))


def entrenar_ddpm(X, n_pasos: int = 3000):
    """Adam con lotes de 256 puntos y un t al azar por punto. Devuelve el modelo y la pérdida por paso."""
    torch.manual_seed(42)
    modelo = RedRuido()
    optimizador = torch.optim.Adam(modelo.parameters(), lr=1e-3)
    x0 = torch.tensor(X, dtype=torch.float32)
    historial = []
    for _ in range(n_pasos):
        lote = x0[torch.randint(len(x0), (256,))]
        t = torch.randint(T_DIFUSION, (256,))
        ruido = torch.randn_like(lote)
        x_t = alphas_bar[t].sqrt().unsqueeze(-1) * lote + (1 - alphas_bar[t]).sqrt().unsqueeze(-1) * ruido
        optimizador.zero_grad()
        perdida = ((modelo(x_t, t) - ruido) ** 2).mean()
        perdida.backward()
        optimizador.step()
        historial.append(perdida.item())
    return modelo, historial


def muestrear_ddpm(modelo, n: int = 500) -> np.ndarray:
    """Parte de ruido N(0, I) y quita el ruido predicho paso a paso."""
    torch.manual_seed(0)
    with torch.no_grad():
        x = torch.randn(n, 2)
        for t in reversed(range(T_DIFUSION)):
            ruido = modelo(x, torch.full((n,), t))
            x = (x - betas[t] / (1 - alphas_bar[t]).sqrt() * ruido) / alphas[t].sqrt()
            if t > 0:
                x = x + betas[t].sqrt() * torch.randn_like(x)
    return x.numpy()


def comparar_generadores(X_reserva, muestras: dict, bases: dict, titulo):
    """Tabla de distancia de energía y gráfico de real frente a generado."""
    tabla = pd.Series({**bases, "DDPM": distancia_energia(muestras["DDPM"], X_reserva)}, name="distancia de energía")
    fig, ejes = plt.subplots(1, len(muestras), figsize=(4.5 * len(muestras), 4), sharex=True, sharey=True)
    for ax, (nombre, puntos) in zip(ejes, muestras.items()):
        ax.scatter(X_reserva[:, 0], X_reserva[:, 1], s=4, color="gray", label="real (reserva)")
        ax.scatter(puntos[:, 0], puntos[:, 1], s=4, color="C3", label="generado")
        ax.set_title(nombre)
        ax.legend(loc="lower left")
    fig.suptitle(titulo)
    plt.tight_layout()
    plt.show()
    return tabla


ddpm_g, historial_ddpm_g = entrenar_ddpm(X_train_g)
tabla_gen = comparar_generadores(X_reserva_g, {**muestras_base_g, "DDPM": muestrear_ddpm(ddpm_g)}, bases_g, "Dos lunas")
print(tabla_gen.round(4).to_string())
```

En dos dimensiones, una mezcla de 8 gaussianas ya describe bien las lunas y puede quedar por delante del DDPM. La difusión se luce en datos de muchas dimensiones, donde una mezcla de gaussianas no escala.

**Comprobar:**

```python
assert X_train_g.shape == (1500, 2) and X_reserva_g.shape == (500, 2)
assert np.mean(historial_ddpm_g[-200:]) < np.mean(historial_ddpm_g[:200])
assert tabla_gen["DDPM"] < tabla_gen["una gaussiana"], "El DDPM debería superar a una sola gaussiana."
print("DDPM entrenado. OK")
```

---

## Parte guiada E — Red neuronal de grafos sobre Cora

### Paso 17 — Datos y línea base sin grafo

Cora: 2708 artículos científicos, cada uno descrito por las palabras que contiene (1433 características binarias) y conectado con los artículos que cita. Hay que predecir su tema, entre 7. Usamos la partición estándar: 140 nodos de train y 1000 de test. La línea base es una logística sobre las palabras de cada artículo, sin mirar las citas.

`torch_geometric` no viene en Colab. La celda siguiente lo instala, sin dependencias extra.

```python
%pip install -q torch_geometric
```

```python
from torch_geometric.datasets import Planetoid
from torch_geometric.nn import GCNConv


def cargar_planetoid(nombre: str):
    """Descarga un conjunto Planetoid y ajusta la logística sobre las características, sin grafo."""
    datos = Planetoid(root="datos_planetoid", name=nombre)[0]
    logistica = LogisticRegression(max_iter=2000).fit(datos.x[datos.train_mask], datos.y[datos.train_mask])
    acc_logistica = logistica.score(datos.x[datos.test_mask], datos.y[datos.test_mask])
    return datos, acc_logistica


cora, acc_log_cora = cargar_planetoid("Cora")
print("nodos:", cora.num_nodes, "| aristas:", cora.num_edges, "| características:", cora.num_features)
print("train:", int(cora.train_mask.sum()), "| test:", int(cora.test_mask.sum()))
print("logística sin grafo (test):", round(acc_log_cora, 3))
```

### Paso 18 — Una GCN de dos capas

Cada capa de la GCN promedia las características de un nodo con las de sus vecinos (con la adyacencia normalizada $\tilde{\mathbf{A}}$) y aplica una capa lineal: $\mathbf{H}^{(l+1)} = \mathrm{ReLU}(\tilde{\mathbf{A}} \mathbf{H}^{(l)} \mathbf{W}^{(l)})$. Usamos la configuración estándar: 16 unidades ocultas, dropout 0.5, `Adam` con tasa 0.01 y `weight_decay=5e-4`, 200 épocas.

```python
class GCN(nn.Module):
    """Dos capas GCNConv con ReLU y dropout en medio."""

    def __init__(self, n_entradas: int, n_clases: int, n_ocultas: int = 16):
        super().__init__()
        self.capa1 = GCNConv(n_entradas, n_ocultas)
        self.capa2 = GCNConv(n_ocultas, n_clases)

    def forward(self, x, aristas):
        h = torch.relu(self.capa1(x, aristas))
        h = nn.functional.dropout(h, p=0.5, training=self.training)
        return self.capa2(h, aristas)


def entrenar_gcn(datos, n_epochs: int = 200):
    """Entrena con los nodos de train. Devuelve el modelo, la pérdida por época y la exactitud de test."""
    torch.manual_seed(42)
    modelo = GCN(datos.num_features, int(datos.y.max()) + 1)
    optimizador = torch.optim.Adam(modelo.parameters(), lr=0.01, weight_decay=5e-4)
    historial = []
    for _ in range(n_epochs):
        modelo.train()
        optimizador.zero_grad()
        perdida = nn.functional.cross_entropy(modelo(datos.x, datos.edge_index)[datos.train_mask], datos.y[datos.train_mask])
        perdida.backward()
        optimizador.step()
        historial.append(perdida.item())
    modelo.eval()
    with torch.no_grad():
        y_hat = modelo(datos.x, datos.edge_index).argmax(dim=1)
    acc = (y_hat[datos.test_mask] == datos.y[datos.test_mask]).float().mean().item()
    return modelo, historial, acc


gcn_cora, historial_gcn_cora, acc_gcn_cora = entrenar_gcn(cora)
tabla_cora = pd.Series({"piso (mayoría)": float(np.bincount(cora.y[cora.test_mask]).max() / int(cora.test_mask.sum())),
                        "logística sin grafo": acc_log_cora, "GCN": acc_gcn_cora}, name="exactitud test")
print(tabla_cora.round(3).to_string())
```

**Comprobar:**

```python
assert cora.num_nodes == 2708 and int(cora.train_mask.sum()) == 140 and int(cora.test_mask.sum()) == 1000
assert historial_gcn_cora[-1] < historial_gcn_cora[0]
assert acc_gcn_cora > acc_log_cora + 0.1, "La GCN debería superar con claridad a la logística sin grafo."
print("GCN entrenada. OK")
```

---

## Parte individual

Elija **una** de las cinco opciones y replique el método de la parte guiada sobre otro conjunto clásico.

| Opción | Arquitectura | Conjunto |
|---|---|---|
| `"mlp"` | MLP numpy y `MLPClassifier` | círculos (`make_circles`) |
| `"rnn"` | RNN numpy y LSTM | pasajeros aéreos mensuales, 1949 a 1960 (`seaborn`); $\ln$(pasajeros), ventanas de 12 meses, test 1958 a 1960 |
| `"ae"` | autoencoder y VAE | rostros Olivetti, 400 imágenes de 64x64 |
| `"difusion"` | DDPM | círculos concéntricos (`make_circles`) |
| `"gnn"` | GCN | red de citas CiteSeer |

### Paso 19 — Elegir el modelo

```python
MODELO_ELEGIDO = "mlp"  # TODO: escriba "mlp", "rnn", "ae", "difusion" o "gnn"

assert MODELO_ELEGIDO in {"mlp", "rnn", "ae", "difusion", "gnn"}, "Use exactamente una de las cinco opciones."
print("Modelo elegido:", MODELO_ELEGIDO)
```

### Opción A — MLP sobre los círculos

```python
if MODELO_ELEGIDO == "mlp":
    # TODO 1: datos, partición y líneas base.
    X_circ, y_circ = make_circles(n_samples=500, noise=0.1, factor=0.5, random_state=42)
    X_train_c, X_test_c, y_train_c, y_test_c, bases_circ = preparar_clasificacion_2d(X_circ, y_circ)

    # TODO 2: red numpy y MLPClassifier con la misma configuración. Pruebe otro n_ocultas o alpha.
    params_red_c, historial_c = entrenar_red_numpy(X_train_c, y_train_c, n_ocultas=8, alpha=0.1)
    mlp_c = entrenar_mlp_como_numpy(X_train_c, y_train_c, n_ocultas=8, alpha=0.1)
    tabla_circ = comparar_red_y_mlp(params_red_c, historial_c, mlp_c, X_train_c, y_train_c, X_test_c, y_test_c, bases_circ)
    print(tabla_circ.to_string())

    # TODO 3: curvas de pérdida y fronteras.
    graficar_red_y_mlp(params_red_c, historial_c, mlp_c, X_train_c, y_train_c, "Círculos: pérdida de train")
else:
    print("Opción A no elegida.")
```

**Comprobar (opción A):**

```python
if MODELO_ELEGIDO == "mlp":
    assert historial_c[-1] < historial_c[0]
    assert abs(historial_c[-1] - mlp_c.loss_curve_[-1]) < 0.1
    assert tabla_circ.loc["MLPClassifier", "exactitud test"] > bases_circ["logística"] + 0.05
    print("Opción MLP: OK")
else:
    print("Opción A no elegida.")
```

### Opción B — RNN sobre los pasajeros aéreos

```python
if MODELO_ELEGIDO == "rnn":
    # TODO 1: serie, ventanas de 12 meses y partición temporal.
    vuelos = sns.load_dataset("flights")
    n_train_vuelos = int((vuelos["year"] <= 1957).sum())
    serie_vuelos = preparar_serie(vuelos["passengers"].to_numpy(dtype=float), n_train_vuelos, ventana=12, log=True)

    # TODO 2: RNN numpy y LSTM. Pruebe otro alpha o n_epochs en entrenar_rnn_numpy.
    params_rnn_v, historial_rnn_v = entrenar_rnn_numpy(serie_vuelos["X_train"], serie_vuelos["y_train"])
    lstm_v, historial_lstm_v = entrenar_lstm(serie_vuelos["X_train"], serie_vuelos["y_train"])

    # TODO 3: tabla y gráfico frente a las líneas base.
    meses_test = pd.to_datetime(vuelos["year"].astype(str) + "-" + vuelos["month"].astype(str), format="%Y-%b")
    tabla_vuelos = comparar_series(serie_vuelos, params_rnn_v, lstm_v, meses_test.to_numpy()[serie_vuelos["indice_test"]],
                                   "Pasajeros aéreos, test 1958-1960: un mes adelante", "miles de pasajeros")
    print(tabla_vuelos.round(1).to_string())
else:
    print("Opción B no elegida.")
```

**Comprobar (opción B):**

```python
if MODELO_ELEGIDO == "rnn":
    assert len(vuelos) == 144 and len(serie_vuelos["y_test"]) == 36
    assert historial_rnn_v[-1] < historial_rnn_v[0] and historial_lstm_v[-1] < historial_lstm_v[0]
    assert tabla_vuelos["LSTM (PyTorch)"] < tabla_vuelos["media de train"]
    print("Opción RNN: OK")
else:
    print("Opción B no elegida.")
```

### Opción C — Autoencoder y VAE sobre los rostros Olivetti

```python
if MODELO_ELEGIDO == "ae":
    # TODO 1: rostros (se descargan una vez, unos 4 MB), partición y PCA con K = 8.
    rostros = fetch_olivetti_faces()
    X_train_r, X_test_r, X_hat_pca_r = preparar_imagenes(rostros.data)

    # TODO 2: autoencoder y VAE. Pruebe otro K o n_epochs.
    ae_r, historial_ae_r = entrenar_autoencoder(X_train_r)
    vae_r, historial_vae_r = entrenar_autoencoder(X_train_r, variacional=True)
    tabla_rostros = pd.Series({
        "PCA (K = 8)": float(np.mean((X_hat_pca_r - X_test_r) ** 2)),
        "autoencoder": float(np.mean((reconstruir(ae_r, X_test_r) - X_test_r) ** 2)),
        "VAE": float(np.mean((reconstruir(vae_r, X_test_r) - X_test_r) ** 2)),
    }, name="ECM de reconstrucción (test)")
    print(tabla_rostros.round(4).to_string())

    # TODO 3: reconstrucciones y muestras.
    mostrar_imagenes({
        "original": X_test_r[:8], "autoencoder": reconstruir(ae_r, X_test_r[:8]),
        "VAE": reconstruir(vae_r, X_test_r[:8]), "PCA": X_hat_pca_r[:8],
        "VAE, muestras de la previa": muestras_vae(vae_r, n=8),
    }, (64, 64), "Rostros Olivetti")
else:
    print("Opción C no elegida.")
```

**Comprobar (opción C):**

```python
if MODELO_ELEGIDO == "ae":
    assert X_train_r.shape[1] == 4096
    assert historial_ae_r[-1] < historial_ae_r[0] and historial_vae_r[-1] < historial_vae_r[0]
    print("Opción AE: OK")
else:
    print("Opción C no elegida.")
```

### Opción D — DDPM sobre los círculos

```python
if MODELO_ELEGIDO == "difusion":
    # TODO 1: datos y líneas base.
    X_circ_gen, _ = make_circles(n_samples=2000, noise=0.05, factor=0.5, random_state=42)
    X_train_cg, X_reserva_cg, muestras_base_cg, bases_cg = preparar_2d(X_circ_gen)

    # TODO 2: DDPM. Pruebe otro n_pasos.
    ddpm_cg, historial_ddpm_cg = entrenar_ddpm(X_train_cg)

    # TODO 3: tabla y gráfico.
    tabla_gen_c = comparar_generadores(X_reserva_cg, {**muestras_base_cg, "DDPM": muestrear_ddpm(ddpm_cg)},
                                       bases_cg, "Círculos")
    print(tabla_gen_c.round(4).to_string())
else:
    print("Opción D no elegida.")
```

**Comprobar (opción D):**

```python
if MODELO_ELEGIDO == "difusion":
    assert np.mean(historial_ddpm_cg[-200:]) < np.mean(historial_ddpm_cg[:200])
    assert tabla_gen_c["DDPM"] < tabla_gen_c["una gaussiana"]
    print("Opción difusión: OK")
else:
    print("Opción D no elegida.")
```

### Opción E — GCN sobre CiteSeer

```python
if MODELO_ELEGIDO == "gnn":
    # TODO 1: datos y logística sin grafo.
    citeseer, acc_log_cs = cargar_planetoid("CiteSeer")

    # TODO 2: GCN. Pruebe otro n_epochs.
    gcn_cs, historial_gcn_cs, acc_gcn_cs = entrenar_gcn(citeseer)
    print("logística sin grafo (test):", round(acc_log_cs, 3), "| GCN (test):", round(acc_gcn_cs, 3))
else:
    print("Opción E no elegida.")
```

**Comprobar (opción E):**

```python
if MODELO_ELEGIDO == "gnn":
    assert citeseer.num_nodes == 3327 and int(citeseer.test_mask.sum()) == 1000
    assert acc_gcn_cs > acc_log_cs
    print("Opción GNN: OK")
else:
    print("Opción E no elegida.")
```

<!-- end NOTEBOOK: -->
