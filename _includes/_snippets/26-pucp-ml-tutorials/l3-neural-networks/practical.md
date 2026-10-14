<!-- NOTEBOOK: -->

Este cuaderno se organiza en dos secciones:

1. **Parte guiada:** Volvemos al catálogo USGS de **Colombia**, ahora 2020 a 2024 con magnitud 4.0 o más, con la etiqueta de ubicación débil de la sesión 2. Programamos una **red con una capa oculta desde cero** en numpy, la comparamos con **`MLPClassifier`** de scikit-learn, miramos el **sobreajuste** y cerramos con una **RNN** y una **CNN** pequeñas sobre una serie diaria de sismos.
2. **Parte individual:** Los estudiantes eligen la red numpy o `MLPClassifier` y la replican sobre el catálogo del **Perú**, 2024, misma magnitud.

Ejecute las celdas de arriba hacia abajo. En cada **Comprobar**, confirme el mensaje `OK` antes de seguir.

Documentación del servicio: [USGS FDSN event API](https://earthquake.usgs.gov/fdsnws/event/1/). Documentación del modelo: [`MLPClassifier`](https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html).

---

## Continuidad con las sesiones 1 y 2

Usamos la misma etiqueta de la sesión 2: una **ubicación débil** es una fila con `horizontalError > 10` km o `gap > 90` grados. Las características siguen siendo `mag`, `depth` y `latitude`. `gap` y `horizontalError` solo construyen la etiqueta. La partición es la misma: `test_size=0.30`, `random_state=42`, estratificada.

La ventana de Colombia de la sesión 2 (2024, magnitud 4.5 o más) deja unas 60 filas y 19 de test. Con esas filas ningún modelo separa la etiqueta mejor que la línea base, ni con validación cruzada. Por eso aquí ampliamos Colombia a 2020-2024 y magnitud 4.0 o más. Perú usa el mismo `PARAMETROS_CURSO` de siempre.

En la sesión 2, la logística y el perceptrón dibujaban una sola frontera lineal. Hoy ponemos una capa oculta entre la entrada y la salida.

---

## Datos y helpers (reutilización de las sesiones 1 y 2)

Repetimos los métodos de acceso de la sesión 1 e importamos las librerías que utilizaremos en esta sesión.

### Importaciones

```python
import warnings
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
from sklearn.exceptions import ConvergenceWarning
from sklearn.linear_model import LinearRegression, LogisticRegression, Perceptron
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
```

### Helpers de descarga y catálogo de Colombia

```python
def build_usgs_url(parametros: dict) -> str:
    """Arma la URL del catálogo USGS FDSN a partir de un diccionario de parámetros."""
    base = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    consulta = "&".join(f"{clave}={valor}" for clave, valor in parametros.items())
    return f"{base}?{consulta}"


def download_csv(url: str, dest: Path, timeout: int = 120) -> int:
    """Descarga ``url`` a ``dest`` y devuelve el número de bytes escritos.

    Falla temprano si el servidor responde 4xx/5xx o si el cuerpo no empieza
    con ``time,`` (cabecera del CSV del catálogo).
    """
    respuesta = requests.get(url, timeout=timeout)
    respuesta.raise_for_status()
    texto = respuesta.text
    if not texto.startswith("time,"):
        raise ValueError("La respuesta no es el CSV del catálogo. Revise la URL antes de seguir.")
    dest.write_text(texto, encoding="utf-8")
    return dest.stat().st_size


# Características de la sesión 2. gap y horizontalError NO están aquí.
FEATURES_CLASIFICACION = ["mag", "depth", "latitude"]


def preparar_clasificacion(tabla: pd.DataFrame) -> pd.DataFrame:
    """Construye la etiqueta de ubicación débil y deja solo filas completas.

    La etiqueta usa gap y horizontalError.
    Las características NO incluyen gap ni horizontalError.
    """
    trabajo = tabla.copy()
    trabajo["ubicacion_debil"] = (
        (trabajo["horizontalError"] > 10) | (trabajo["gap"] > 90)
    ).astype(int)
    columnas = FEATURES_CLASIFICACION + ["ubicacion_debil", "gap", "horizontalError"]
    return trabajo[columnas].dropna()


def exactitud_mayoria(y_true) -> float:
    """Exactitud de siempre predecir la clase mayoritaria en el conjunto de evaluación."""
    y_true = np.asarray(y_true)
    n_pos = int(y_true.sum())
    return max(n_pos, len(y_true) - n_pos) / len(y_true)


PARAMETROS_COLOMBIA = {
    "format": "csv",
    "starttime": "2020-01-01",
    "endtime": "2025-01-01",
    "minmagnitude": "4.0",
    "minlatitude": "-4.5",
    "maxlatitude": "13.5",
    "minlongitude": "-79.5",
    "maxlongitude": "-66.5",
}
CATALOGO_COLOMBIA = Path("usgs_colombia_2020_2024_m40.csv")

USGS_URL_COLOMBIA = build_usgs_url(PARAMETROS_COLOMBIA)
print(USGS_URL_COLOMBIA)
bytes_colombia = download_csv(USGS_URL_COLOMBIA, CATALOGO_COLOMBIA)
sismos_colombia = pd.read_csv(CATALOGO_COLOMBIA)
print("Filas, columnas:", sismos_colombia.shape)
```

| Constante | Valor |
|-----------|--------|
| Fechas | 2020-01-01 a 2025-01-01 |
| Magnitud mínima | 4.0 |
| Latitud | -4.5 a 13.5 |
| Longitud | -79.5 a -66.5 |

### Líneas base de la sesión 2

La tabla de clasificación, la partición, la línea base mayoritaria, la logística y el perceptrón de la sesión 2, con los mismos parámetros.

```python
clasif_colombia = preparar_clasificacion(sismos_colombia)
X_co = clasif_colombia[FEATURES_CLASIFICACION].to_numpy()
y_co = clasif_colombia["ubicacion_debil"].to_numpy()

X_train_co, X_test_co, y_train_co, y_test_co = train_test_split(
    X_co, y_co, test_size=0.30, random_state=42,
    stratify=y_co if len(np.unique(y_co)) > 1 else None,
)
baseline_co = exactitud_mayoria(y_test_co)

modelo_logistico_co = LogisticRegression(max_iter=1000, random_state=42).fit(X_train_co, y_train_co)
acc_log_co = accuracy_score(y_test_co, modelo_logistico_co.predict(X_test_co))
modelo_perceptron_co = Perceptron(max_iter=1000, random_state=42, tol=1e-3).fit(X_train_co, y_train_co)
acc_per_co = accuracy_score(y_test_co, modelo_perceptron_co.predict(X_test_co))

print("filas:", len(clasif_colombia), "| train:", len(y_train_co), "| test:", len(y_test_co))
print("línea base mayoritaria (test):", round(baseline_co, 3))
print("logística (test):", round(acc_log_co, 3), "| perceptrón (test):", round(acc_per_co, 3))
```

**Comprobar:**

```python
assert "minmagnitude=4.0" in USGS_URL_COLOMBIA and CATALOGO_COLOMBIA.is_file()
assert len(clasif_colombia) > 300, "El recorte de Colombia vino casi vacío. No cambie los parámetros."
assert "gap" not in FEATURES_CLASIFICACION and "horizontalError" not in FEATURES_CLASIFICACION
print(f"Colombia: {len(clasif_colombia)} filas, test de {len(y_test_co)}. OK")
```

Con unas 230 filas de test, una fila mueve la exactitud menos de medio punto.

---

## Parte guiada A — Activaciones y red de una capa oculta desde cero (Colombia)

### Paso 1 — Funciones de activación

Las tres activaciones de las diapositivas: sigmoide, $\tanh$ y ReLU.

```python
a_rejilla = np.linspace(-4, 4, 200)
fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(a_rejilla, 1 / (1 + np.exp(-a_rejilla)), label="sigmoide")
ax.plot(a_rejilla, np.tanh(a_rejilla), label="tanh")
ax.plot(a_rejilla, np.maximum(0, a_rejilla), label="ReLU")
ax.axhline(0, color="gray", linewidth=0.5)
ax.set_ylim(-1.2, 2.2)
ax.set_xlabel("a")
ax.set_ylabel("h(a)")
ax.legend()
plt.show()
```

### La red, en la notación de las diapositivas

$D = 3$ entradas, $M$ unidades ocultas con $h = \tanh$ y una salida sigmoide $\hat{y}$, la probabilidad de ubicación débil. $y$ es la etiqueta (0/1). Como hay una sola salida, quitamos el índice $k$.

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

### Paso 2 — Escalar las entradas

`mag`, `depth` y `latitude` están en escalas muy distintas. Escalamos con la media y la desviación de **train**.

```python
escalador_co = StandardScaler().fit(X_train_co)
X_train_co_esc = escalador_co.transform(X_train_co)
X_test_co_esc = escalador_co.transform(X_test_co)
print("medias de train escaladas:", np.round(X_train_co_esc.mean(axis=0), 3))
```

### Paso 3 — Propagación hacia adelante

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


params_inicio = inicializar_red(X_train_co_esc.shape[1], n_ocultas=8)
a_ini, z_ini, y_hat_ini = propagar_adelante(X_train_co_esc, params_inicio)
print("forma de a y z:", a_ini.shape, "| primeras salidas y_hat:", np.round(y_hat_ini[:5], 3))
```

### Paso 4 — Pérdida de entropía cruzada

La pérdida de las diapositivas, promediada sobre las $N$ filas:

$$
E(\mathbf{w}) = - \frac{1}{N} \sum_{n=1}^N \{ y_n \ln \hat{y}_n + (1-y_n) \ln (1-\hat{y}_n) \}
$$

```python
def perdida_entropia_cruzada(y_hat: np.ndarray, y: np.ndarray) -> float:
    r"""Entropía cruzada media entre $\hat{y}$ y las etiquetas $y \in \{0, 1\}$."""
    y_hat = np.clip(y_hat, 1e-12, 1 - 1e-12)
    return float(-np.mean(y * np.log(y_hat) + (1 - y) * np.log(1 - y_hat)))


print("pérdida inicial:", round(perdida_entropia_cruzada(y_hat_ini, y_train_co), 4))
```

### Paso 5 — Retropropagación

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
grad_co = retropropagar(X_train_co_esc, y_train_co, params_inicio)
for nombre, indice in [("W1", (0, 1)), ("W1", (3, 2)), ("b1", (5,)), ("W2", (2,)), ("b2", ())]:
    analitico = float(np.asarray(grad_co[nombre])[indice])
    numerico = gradiente_numerico(X_train_co_esc, y_train_co, params_inicio, nombre, indice)
    print(f"{nombre}{indice}: retropropagación {analitico:+.6f} | numérico {numerico:+.6f}")
    assert abs(analitico - numerico) < 1e-6, "La retropropagación no coincide con el gradiente numérico."
print("Gradientes verificados. OK")
```

### Paso 6 — Descenso de gradiente

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


params_red_co, historial_co = entrenar_red_numpy(X_train_co_esc, y_train_co)
print("pérdida en la época 1:", round(historial_co[0], 4), "| última:", round(historial_co[-1], 4))
```

---

## Parte guiada B — Red numpy frente a `MLPClassifier` (Colombia)

### Paso 7 — La misma red con scikit-learn

Misma arquitectura (8 unidades ocultas, $\tanh$), mismas entradas escaladas, mismo optimizador: descenso de gradiente con todo el lote (`batch_size` igual a las filas de train), sin momento, sin regularización (`alpha=0`), tasa $\alpha = 0.1$ y 2000 épocas. Lo único distinto son los pesos iniciales: mismo esquema, otro generador aleatorio. Para que corra las 2000 épocas desactivamos su criterio de parada.

Atención: en `MLPClassifier`, `alpha` es la penalización $L_2$, no la tasa de aprendizaje. La tasa es `learning_rate_init`.

```python
def entrenar_mlp_como_numpy(X, y, n_ocultas: int = 8, alpha: float = 0.1, n_epochs: int = 2000):
    """MLPClassifier configurado para hacer lo mismo que entrenar_red_numpy."""
    modelo = MLPClassifier(
        hidden_layer_sizes=(n_ocultas,),
        activation="tanh",
        solver="sgd",
        learning_rate="constant",
        learning_rate_init=alpha,
        momentum=0.0,
        batch_size=len(X),
        alpha=0.0,
        max_iter=n_epochs,
        shuffle=False,
        tol=0.0,
        n_iter_no_change=n_epochs,
        random_state=42,
    )
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", ConvergenceWarning)  # llega a max_iter a propósito
        modelo.fit(X, y)
    return modelo


mlp_co = entrenar_mlp_como_numpy(X_train_co_esc, y_train_co)
```

### Paso 8 — Tabla de comparación

```python
def comparar_red_y_mlp(params, historial, modelo, X_train, y_train, X_test, y_test, piso):
    """Tabla de exactitudes y pérdida final de la red numpy y de MLPClassifier."""
    filas = {
        "red numpy": [
            accuracy_score(y_train, predecir_red_numpy(X_train, params)),
            accuracy_score(y_test, predecir_red_numpy(X_test, params)),
            historial[-1],
        ],
        "MLPClassifier": [
            accuracy_score(y_train, modelo.predict(X_train)),
            accuracy_score(y_test, modelo.predict(X_test)),
            modelo.loss_curve_[-1],
        ],
    }
    tabla = pd.DataFrame(filas, index=["exactitud train", "exactitud test", "pérdida final"]).T
    tabla["piso (test)"] = piso
    return tabla.round(3)


tabla_co = comparar_red_y_mlp(params_red_co, historial_co, mlp_co,
                              X_train_co_esc, y_train_co, X_test_co_esc, y_test_co, baseline_co)
print(tabla_co.to_string())
print("logística (test):", round(acc_log_co, 3), "| perceptrón (test):", round(acc_per_co, 3))
```

### Paso 9 — Curvas de pérdida y fronteras

Tres características no caben en un plano. Como en la sesión 2, fijamos `latitude` en su media de train y miramos el plano `mag`–`depth`.

```python
def graficar_red_y_mlp(params, historial, modelo, escalador, X_train, y_train, titulo):
    """Curvas de pérdida superpuestas y fronteras de las dos redes, lado a lado."""
    fig, ejes = plt.subplots(1, 3, figsize=(16, 4.5))
    ejes[0].plot(historial, color="k", label="red numpy")
    ejes[0].plot(modelo.loss_curve_, color="C1", linestyle="--", label="MLPClassifier")
    ejes[0].set_xlabel("época")
    ejes[0].set_ylabel("entropía cruzada (train)")
    ejes[0].set_title(titulo)
    ejes[0].legend()

    mag = np.linspace(X_train[:, 0].min() - 0.2, X_train[:, 0].max() + 0.2, 150)
    depth = np.linspace(X_train[:, 1].min() - 10, X_train[:, 1].max() + 10, 150)
    malla_mag, malla_depth = np.meshgrid(mag, depth)
    rejilla = np.column_stack([malla_mag.ravel(), malla_depth.ravel(),
                               np.full(malla_mag.size, X_train[:, 2].mean())])
    rejilla_esc = escalador.transform(rejilla)
    probabilidades = {
        "red numpy": propagar_adelante(rejilla_esc, params)[2],
        "MLPClassifier": modelo.predict_proba(rejilla_esc)[:, 1],
    }
    for ax, (nombre, prob) in zip(ejes[1:], probabilidades.items()):
        ax.contourf(malla_mag, malla_depth, prob.reshape(malla_mag.shape), levels=[0, 0.5, 1],
                    colors=["#dde8f5", "#f5dddd"])
        ax.contour(malla_mag, malla_depth, prob.reshape(malla_mag.shape), levels=[0.5], colors="k")
        ax.scatter(X_train[y_train == 0, 0], X_train[y_train == 0, 1], color="C0", label="firme")
        ax.scatter(X_train[y_train == 1, 0], X_train[y_train == 1, 1], color="C3", label="débil")
        ax.invert_yaxis()
        ax.set_xlabel("mag")
        ax.set_ylabel("depth (km)")
        ax.set_title(f"{nombre}: frontera y_hat = 0.5")
        ax.legend()
    plt.tight_layout()
    plt.show()


graficar_red_y_mlp(params_red_co, historial_co, mlp_co, escalador_co, X_train_co, y_train_co,
                   "Colombia 2020-2024: pérdida de train")
```

**Comprobar:**

```python
assert len(historial_co) == len(mlp_co.loss_curve_) == 2000
assert mlp_co.coefs_[0].shape == params_red_co["W1"].T.shape, "Las dos redes deben tener la misma arquitectura."
assert historial_co[-1] < historial_co[0] and mlp_co.loss_curve_[-1] < mlp_co.loss_curve_[0]
assert abs(historial_co[-1] - mlp_co.loss_curve_[-1]) < 0.15, "Las dos pérdidas finales deberían quedar cerca."
assert abs(tabla_co.loc["red numpy", "exactitud test"] - tabla_co.loc["MLPClassifier", "exactitud test"]) <= 0.25
print("Red numpy y MLPClassifier comparables. OK")
```

---

## Parte guiada C — Sobreajuste (Colombia)

### Paso 10 — Tres tamaños, train frente a test

Usamos `MLPClassifier` con su optimizador por defecto (`adam`) dentro de un pipeline con `StandardScaler`. Probamos tres tamaños de capa oculta.

```python
def entrenar_mlp(X_train, y_train, ocultas=(8,), **opciones):
    """Pipeline StandardScaler + MLPClassifier con semilla fija."""
    modelo = make_pipeline(
        StandardScaler(),
        MLPClassifier(hidden_layer_sizes=ocultas, max_iter=3000, random_state=42, **opciones),
    )
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", ConvergenceWarning)
        modelo.fit(X_train, y_train)
    return modelo


def comparar_tamanos(X_train, y_train, X_test, y_test, tamanos=((8,), (16,), (32, 16)), **opciones):
    """Exactitud de train y test para cada tamaño de capa oculta."""
    filas = []
    for ocultas in tamanos:
        modelo = entrenar_mlp(X_train, y_train, ocultas, **opciones)
        filas.append({
            "capas ocultas": str(ocultas),
            "train": accuracy_score(y_train, modelo.predict(X_train)),
            "test": accuracy_score(y_test, modelo.predict(X_test)),
        })
    return pd.DataFrame(filas)


def graficar_train_test(tabla, piso, titulo):
    """Barras de exactitud de train y test por tamaño, con el piso."""
    fig, ax = plt.subplots(figsize=(7, 4))
    x = np.arange(len(tabla))
    ax.bar(x - 0.2, tabla["train"], width=0.4, label="train")
    ax.bar(x + 0.2, tabla["test"], width=0.4, label="test")
    ax.axhline(piso, color="gray", linestyle="--", label="línea base mayoritaria")
    ax.set_xticks(x, tabla["capas ocultas"])
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("exactitud")
    ax.set_title(titulo)
    ax.legend()
    plt.show()


tamanos_co = comparar_tamanos(X_train_co, y_train_co, X_test_co, y_test_co)
print(tamanos_co.round(3).to_string(index=False))
graficar_train_test(tamanos_co, baseline_co, "Colombia 2020-2024: ubicación débil")
```

### Paso 11 — Parada temprana

`early_stopping=True` separa el 20% de train como validación y detiene el entrenamiento cuando la pérdida de validación deja de mejorar durante 20 épocas. Para frenar el sobreajuste también está la penalización $L_2$ de la sesión 2: en `MLPClassifier` es `alpha` ($\lambda$ en las diapositivas).

```python
mlp_parada_co = entrenar_mlp(X_train_co, y_train_co, (32, 16),
                             early_stopping=True, validation_fraction=0.2, n_iter_no_change=20)
acc_train_parada_co = accuracy_score(y_train_co, mlp_parada_co.predict(X_train_co))
acc_test_parada_co = accuracy_score(y_test_co, mlp_parada_co.predict(X_test_co))
print("épocas:", mlp_parada_co[-1].n_iter_)
print("train:", round(acc_train_parada_co, 3), "| test:", round(acc_test_parada_co, 3),
      "| piso:", round(baseline_co, 3))
```

**Comprobar:**

```python
assert list(tamanos_co["capas ocultas"]) == ["(8,)", "(16,)", "(32, 16)"]
assert tamanos_co["train"].between(0, 1).all() and tamanos_co["test"].between(0, 1).all()
assert mlp_parada_co[-1].n_iter_ < 3000
print("Tamaños y parada temprana: OK")
```

---

## Parte guiada D — RNN y CNN sobre una serie diaria (Colombia)

Una RNN y una CNN esperan entradas con orden: pasos de tiempo o píxeles vecinos. Una tabla de sismos no lo tiene, pero el conteo diario de sismos sí. Pregunta: con los conteos de los últimos 30 días, ¿cuántos sismos de magnitud 4 o más habrá en la próxima semana?

Esta parte usa **PyTorch**, que ya viene instalado en Colab.

### Paso 12 — Serie diaria de Colombia, 2015 a 2024

```python
PARAMETROS_SERIE = {
    "format": "csv",
    "starttime": "2015-01-01",
    "endtime": "2025-01-01",
    "minmagnitude": "4.0",
    "minlatitude": "-4.5",
    "maxlatitude": "13.5",
    "minlongitude": "-79.5",
    "maxlongitude": "-66.5",
}
CATALOGO_SERIE = Path("usgs_colombia_2015_2024_m40.csv")
download_csv(build_usgs_url(PARAMETROS_SERIE), CATALOGO_SERIE)
sismos_serie = pd.read_csv(CATALOGO_SERIE, parse_dates=["time"])

dias = pd.date_range("2015-01-01", "2024-12-31", freq="D", tz="UTC")
conteo_diario = sismos_serie.groupby(sismos_serie["time"].dt.floor("D")).size().reindex(dias, fill_value=0)

fig, ax = plt.subplots(figsize=(12, 3))
ax.plot(conteo_diario.index, conteo_diario.values, linewidth=0.5, color="k")
ax.set_ylabel("sismos M4+ por día")
ax.set_title("Colombia 2015-2024")
plt.show()
print("días:", len(conteo_diario), "| sismos:", int(conteo_diario.sum()))
```

### Paso 13 — Ventanas y partición temporal

Cada fila es una ventana de 30 días. El objetivo $y$ es el número de sismos de los **7 días siguientes**. La partición es **temporal**: train hasta 2021, test 2022 a 2024. Barajar mezclaría días futuros en train. Dos líneas base: la **persistencia** (los próximos 7 días repiten los últimos 7) y la **media** de train.

```python
VENTANA = 30
HORIZONTE = 7


def ventanas_serie(conteo: pd.Series, ventana: int = VENTANA, horizonte: int = HORIZONTE):
    """X: conteos de los últimos ``ventana`` días. y: suma de los ``horizonte`` días siguientes."""
    valores = conteo.to_numpy(dtype=float)
    inicios = range(ventana, len(valores) - horizonte + 1)
    X = np.stack([valores[i - ventana:i] for i in inicios])
    y = np.array([valores[i:i + horizonte].sum() for i in inicios])
    return X, y, conteo.index[ventana:len(valores) - horizonte + 1]


def ecm(y_real, y_pred) -> float:
    """Error cuadrático medio."""
    return float(np.mean((np.asarray(y_real) - np.asarray(y_pred)) ** 2))


X_serie, y_serie, fechas_serie = ventanas_serie(conteo_diario)
en_train = fechas_serie < pd.Timestamp("2022-01-01", tz="UTC")
X_train_s, y_train_s = X_serie[en_train], y_serie[en_train]
X_test_s, y_test_s = X_serie[~en_train], y_serie[~en_train]

ecm_persistencia = ecm(y_test_s, X_test_s[:, -HORIZONTE:].sum(axis=1))
ecm_media = ecm(y_test_s, np.full(len(y_test_s), y_train_s.mean()))
lineal_s = LinearRegression().fit(X_train_s, y_train_s)
ecm_lineal = ecm(y_test_s, lineal_s.predict(X_test_s))
print("train:", len(y_train_s), "| test:", len(y_test_s))
print("ECM persistencia:", round(ecm_persistencia, 2), "| media:", round(ecm_media, 2),
      "| regresión lineal:", round(ecm_lineal, 2))
```

### Paso 14 — Una RNN y una CNN pequeñas

La RNN (una GRU con 8 unidades) lee los 30 días en orden y decide con su último estado. La CNN pasa 8 filtros de 5 días a lo largo de la ventana y promedia sus respuestas. Las dos se entrenan con todo el lote, `Adam` y error cuadrático medio.

```python
import torch
from torch import nn


class RNNSerie(nn.Module):
    """GRU de 8 unidades que lee la ventana día a día -> una salida desde el último estado."""

    def __init__(self):
        super().__init__()
        self.gru = nn.GRU(input_size=1, hidden_size=8, batch_first=True)
        self.salida = nn.Linear(8, 1)

    def forward(self, x):
        _, estado = self.gru(x.unsqueeze(-1))
        return self.salida(estado[-1]).squeeze(-1)


class CNNSerie(nn.Module):
    """Conv1d (8 filtros de 5 días) -> ReLU -> promedio en el tiempo -> una salida."""

    def __init__(self):
        super().__init__()
        self.conv = nn.Conv1d(in_channels=1, out_channels=8, kernel_size=5)
        self.salida = nn.Linear(8, 1)

    def forward(self, x):
        z = torch.relu(self.conv(x.unsqueeze(1))).mean(dim=-1)
        return self.salida(z).squeeze(-1)


def entrenar_torch(clase_modelo, X_train, y_train, n_epochs: int = 300, tasa: float = 0.01):
    """Entrena con todo el lote y error cuadrático medio. Devuelve el modelo y la pérdida por época."""
    torch.manual_seed(42)
    modelo = clase_modelo()
    optimizador = torch.optim.Adam(modelo.parameters(), lr=tasa)
    X_tensor = torch.tensor(X_train, dtype=torch.float32)
    y_tensor = torch.tensor(y_train, dtype=torch.float32)
    historial = []
    for _ in range(n_epochs):
        optimizador.zero_grad()
        e = nn.functional.mse_loss(modelo(X_tensor), y_tensor)
        e.backward()
        optimizador.step()
        historial.append(e.item())
    return modelo, historial


def predecir_torch(modelo, X):
    """Predicción del conteo de los próximos 7 días."""
    with torch.no_grad():
        return modelo(torch.tensor(X, dtype=torch.float32)).numpy()


rnn_s, historial_rnn = entrenar_torch(RNNSerie, X_train_s, y_train_s)
cnn_s, historial_cnn = entrenar_torch(CNNSerie, X_train_s, y_train_s)
tabla_serie = pd.Series({
    "persistencia": ecm_persistencia,
    "media de train": ecm_media,
    "regresión lineal": ecm_lineal,
    "RNN (GRU)": ecm(y_test_s, predecir_torch(rnn_s, X_test_s)),
    "CNN": ecm(y_test_s, predecir_torch(cnn_s, X_test_s)),
}, name="ECM (test)")
print(tabla_serie.round(2).to_string())

fig, ax = plt.subplots(figsize=(12, 3))
ax.plot(fechas_serie[~en_train], y_test_s, color="gray", linewidth=0.8, label="real")
ax.plot(fechas_serie[~en_train], predecir_torch(rnn_s, X_test_s), label="RNN (GRU)")
ax.plot(fechas_serie[~en_train], predecir_torch(cnn_s, X_test_s), label="CNN")
ax.set_ylabel("sismos M4+ en 7 días")
ax.set_title("Colombia, test 2022-2024")
ax.legend()
plt.show()
```

La GRU y la CNN bajan el error de la persistencia a la mitad, pero quedan al nivel de la media: el conteo de sismos casi no depende de los 30 días anteriores.

**Comprobar:**

```python
assert X_serie.shape[1] == VENTANA
assert fechas_serie[en_train].max() < fechas_serie[~en_train].min(), "La partición debe ser temporal."
assert historial_rnn[-1] < historial_rnn[0] and historial_cnn[-1] < historial_cnn[0]
assert tabla_serie["RNN (GRU)"] < ecm_persistencia and tabla_serie["CNN"] < ecm_persistencia
print("RNN y CNN entrenadas. OK")
```

---

## Parte individual — Perú 2024

Perú está sobre el borde de subducción entre la placa de Nazca y la placa Sudamericana, una de las zonas sísmicamente más activas del planeta. Buena parte de esa sismicidad ocurre mar adentro, frente a la costa donde viven Lima, Callao, Chimbote, Trujillo, Pisco y Arequipa. Ahí las estaciones solo pueden estar de un lado, el `gap` sube y aumentan las ubicaciones débiles. Después de un sismo fuerte, como el de Pisco de 2007 (M8.0), los equipos de evaluación de daños necesitan saber qué epicentros son confiables a escala de distrito antes de priorizar inspecciones de puentes, colegios y hospitales.

Tarea: elegir la red numpy o `MLPClassifier`, entrenarla sobre la etiqueta de ubicación débil del Perú y compararla con la logística, el perceptrón y el piso.

`PARAMETROS_CURSO` es el contrato con las sesiones siguientes. **No lo modifique.**

| Constante | Valor |
|-----------|--------|
| Latitud | -18.5 a 0.2 |
| Longitud | -82 a -68 |

### Descargar y preparar Perú

```python
PARAMETROS_CURSO = {
    "format": "csv",
    "starttime": "2024-01-01",
    "endtime": "2025-01-01",
    "minmagnitude": "4.5",
    "minlatitude": "-18.5",
    "maxlatitude": "0.2",
    "minlongitude": "-82",
    "maxlongitude": "-68",
}
CATALOGO_PERU = Path("usgs_peru_2024_m45.csv")

USGS_URL_PERU = build_usgs_url(PARAMETROS_CURSO)
print(USGS_URL_PERU)
download_csv(USGS_URL_PERU, CATALOGO_PERU)
sismos_peru = pd.read_csv(CATALOGO_PERU)

clasif_peru = preparar_clasificacion(sismos_peru)
X_pe = clasif_peru[FEATURES_CLASIFICACION].to_numpy()
y_pe = clasif_peru["ubicacion_debil"].to_numpy()
X_train_pe, X_test_pe, y_train_pe, y_test_pe = train_test_split(
    X_pe, y_pe, test_size=0.30, random_state=42,
    stratify=y_pe if len(np.unique(y_pe)) > 1 else None,
)
baseline_pe = exactitud_mayoria(y_test_pe)
acc_log_pe = accuracy_score(y_test_pe, LogisticRegression(max_iter=1000, random_state=42)
                            .fit(X_train_pe, y_train_pe).predict(X_test_pe))
acc_per_pe = accuracy_score(y_test_pe, Perceptron(max_iter=1000, random_state=42, tol=1e-3)
                            .fit(X_train_pe, y_train_pe).predict(X_test_pe))

escalador_pe = StandardScaler().fit(X_train_pe)
X_train_pe_esc = escalador_pe.transform(X_train_pe)
X_test_pe_esc = escalador_pe.transform(X_test_pe)

print("filas:", len(clasif_peru), "| train:", len(y_train_pe), "| test:", len(y_test_pe))
print("piso:", round(baseline_pe, 3), "| logística:", round(acc_log_pe, 3), "| perceptrón:", round(acc_per_pe, 3))
```

### Paso 15 — Elegir el modelo

```python
MODELO_ELEGIDO = "mlpclassifier"  # TODO: escriba "numpy" o "mlpclassifier"

assert MODELO_ELEGIDO in {"numpy", "mlpclassifier"}, "Use exactamente una de las dos opciones."
print("Modelo elegido:", MODELO_ELEGIDO)
```

### Opción A — Red numpy sobre Perú

```python
if MODELO_ELEGIDO == "numpy":
    # TODO 1: red numpy sobre Perú. Pruebe otro n_ocultas o alpha.
    params_red_pe, historial_pe = entrenar_red_numpy(X_train_pe_esc, y_train_pe, n_ocultas=8, alpha=0.1)
    # TODO 2: la misma red con MLPClassifier, para comparar.
    mlp_pe = entrenar_mlp_como_numpy(X_train_pe_esc, y_train_pe, n_ocultas=8, alpha=0.1)
    tabla_pe = comparar_red_y_mlp(params_red_pe, historial_pe, mlp_pe,
                                  X_train_pe_esc, y_train_pe, X_test_pe_esc, y_test_pe, baseline_pe)
    print(tabla_pe.to_string())
    # TODO 3: curvas de pérdida y fronteras.
    graficar_red_y_mlp(params_red_pe, historial_pe, mlp_pe, escalador_pe, X_train_pe, y_train_pe,
                       "Perú 2024: pérdida de train")
else:
    print("Opción A no elegida.")
```

### Opción B — `MLPClassifier` sobre Perú

```python
if MODELO_ELEGIDO == "mlpclassifier":
    # TODO 1: tres tamaños, train frente a test.
    tamanos_pe = comparar_tamanos(X_train_pe, y_train_pe, X_test_pe, y_test_pe)
    print(tamanos_pe.round(3).to_string(index=False))
    graficar_train_test(tamanos_pe, baseline_pe, "Perú 2024: ubicación débil")
else:
    print("Opción B no elegida.")
```

**Comprobar:**

```python
assert "minlatitude=-18.5" in USGS_URL_PERU and CATALOGO_PERU.is_file()
assert len(clasif_peru) > 50, "El recorte del Perú vino casi vacío. Revise la URL."
if MODELO_ELEGIDO == "numpy":
    assert historial_pe[-1] < historial_pe[0]
    assert abs(historial_pe[-1] - mlp_pe.loss_curve_[-1]) < 0.15
else:
    assert list(tamanos_pe["capas ocultas"]) == ["(8,)", "(16,)", "(32, 16)"]
print(f"Perú, opción {MODELO_ELEGIDO}: OK")
print("URL del curso (guárdela):", USGS_URL_PERU)
```

<!-- end NOTEBOOK: -->
