<!-- NOTEBOOK: -->

Este cuaderno se organiza en dos secciones:
1. **Parte guiada:** Volvemos al catálogo USGS de **Colombia**, 2024, magnitud 4.5 o más. Construimos una **red con una capa oculta desde cero** en numpy, la comparamos con **`MLPClassifier`** de scikit-learn, miramos el **sobreajuste** y la **regularización**, y terminamos con una etiqueta donde la frontera **no es lineal**.
2. **Parte individual:** Los estudiantes repiten el método sobre el catálogo del **Perú**, 2024, misma magnitud. Comparan pisos, brechas entre train y test, y justifican qué tamaño de modelo usarían.

En la sesión 2 entrenamos una logística y un perceptrón para anticipar ubicaciones débiles. Los dos dibujan **una sola frontera lineal**. Hoy ponemos capas ocultas entre la entrada y la salida y preguntamos dos cosas: si esas capas ayudan con la misma etiqueta, y en qué tipo de problema sí hacen una diferencia.

Ejecute las celdas de arriba hacia abajo. En cada **Comprobar**, confirme el mensaje `OK` antes de seguir.

Si abre este cuaderno en un Colab fresco, las funciones de descarga y las líneas base se definen otra vez aquí. No asuma que las sesiones 1 y 2 siguen en memoria. Solo usamos numpy, pandas, matplotlib y scikit-learn, que ya vienen instalados en Colab.

Documentación del servicio: [USGS FDSN event API](https://earthquake.usgs.gov/fdsnws/event/1/). Documentación del modelo: [`MLPClassifier`](https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html).

---

## Continuidad con las sesiones 1 y 2

Nada cambia en los datos. Usamos el mismo catálogo (USGS, 2024, magnitud 4.5 o más), las mismas ventanas geográficas (Colombia en la parte guiada, Perú en la individual) y la misma etiqueta de la sesión 2: una **ubicación débil** es una fila con `horizontalError > 10` km o `gap > 90` grados.

También repetimos la partición de la sesión 2: 70% para entrenar, 30% para medir, `random_state=42` y estratificada. Así cualquier diferencia con la logística viene del modelo y no de un reparto distinto de filas.

Lo que cambia hoy es lo que hay entre la entrada y la salida. La logística combina `mag`, `depth` y `latitude` en un solo número y lo pasa por una sigmoide. Una red con una capa oculta primero calcula varias combinaciones a la vez, pasa cada una por una activación no lineal, y solo entonces decide. Eso le permite dibujar fronteras curvas.

Dos reglas de la sesión 2 siguen en pie. Toda exactitud se lee **al lado de la línea base mayoritaria**. Y `gap` y `horizontalError` **solo construyen la etiqueta**: nunca entran como características, porque eso sería fuga de etiqueta.

`PARAMETROS_CURSO` (Perú) es el contrato con las sesiones siguientes. **No lo modifique.**

---

## Datos y helpers (reutilización de las sesiones 1 y 2)

No repetimos los recorridos de las sesiones anteriores. En un Colab fresco necesitamos las mismas piezas, y van en **cuatro bloques de código** con docstrings y un **Comprobar**. El material nuevo, la red neuronal, empieza justo después.

### Importaciones

Un solo bloque con lo que usa todo el cuaderno. Respecto a la sesión 2 se suman `StandardScaler`, `make_pipeline` y `MLPClassifier`.

```python
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
```

### Helpers de las sesiones 1 y 2

Este bloque solo define funciones, no descarga nada. `build_usgs_url` y `download_csv` vienen de la sesión 1. `FEATURES_CLASIFICACION`, `preparar_clasificacion` y `exactitud_mayoria` vienen de la sesión 2. Las docstrings son las mismas: documentan el contrato de cada función.

```python
def build_usgs_url(parametros: dict) -> str:
    """Arma la URL del catálogo USGS FDSN a partir de un diccionario de parámetros.

    No toca la red: solo une la base con ``clave=valor`` separados por ``&``.
    Imprima la URL y revísela antes de descargar.
    """
    base = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    consulta = "&".join(f"{clave}={valor}" for clave, valor in parametros.items())
    return f"{base}?{consulta}"


def download_csv(url: str, dest: Path, timeout: int = 120) -> int:
    """Descarga ``url`` a ``dest`` y devuelve el número de bytes escritos.

    Falla temprano si el servidor responde 4xx/5xx o si el cuerpo no empieza
    con ``time,`` (cabecera del CSV del catálogo). Así evitamos guardar una
    página HTML de error con extensión ``.csv``.
    """
    respuesta = requests.get(url, timeout=timeout)
    respuesta.raise_for_status()
    texto = respuesta.text
    if not texto.startswith("time,"):
        raise ValueError(
            "La respuesta no es el CSV del catálogo. "
            "Revise la URL antes de seguir."
        )
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
    if len(y_true) == 0:
        return float("nan")
    n_pos = int(y_true.sum())
    n_neg = len(y_true) - n_pos
    return max(n_pos, n_neg) / len(y_true)
```

### Datos de Colombia

Misma ventana de las sesiones 1 y 2: 2024-01-01 a 2025-01-01, magnitud 4.5 o más, latitud -4.5 a 13.5, longitud -79.5 a -66.5. El bloque arma la URL, descarga el CSV y lo carga en `sismos_colombia`.

```python
# Ventana de Colombia (margen en la frontera). Exactamente la de la sesión 1.
PARAMETROS_COLOMBIA = {
    "format": "csv",
    "starttime": "2024-01-01",
    "endtime": "2025-01-01",
    "minmagnitude": "4.5",
    "minlatitude": "-4.5",
    "maxlatitude": "13.5",
    "minlongitude": "-79.5",
    "maxlongitude": "-66.5",
}
CATALOGO_COLOMBIA = Path("usgs_colombia_2024_m45.csv")

USGS_URL_COLOMBIA = build_usgs_url(PARAMETROS_COLOMBIA)
print(USGS_URL_COLOMBIA)

bytes_colombia = download_csv(USGS_URL_COLOMBIA, CATALOGO_COLOMBIA)
sismos_colombia = pd.read_csv(CATALOGO_COLOMBIA)
print(f"Guardado: {CATALOGO_COLOMBIA} ({bytes_colombia / 1e3:.1f} KB)")
print("Filas, columnas:", sismos_colombia.shape)
sismos_colombia.head()
```

**Comprobar:**

```python
assert USGS_URL_COLOMBIA.startswith("https://earthquake.usgs.gov/fdsnws/event/1/query?")
assert "starttime=2024-01-01" in USGS_URL_COLOMBIA
assert "minmagnitude=4.5" in USGS_URL_COLOMBIA
assert "minlatitude=-4.5" in USGS_URL_COLOMBIA
assert CATALOGO_COLOMBIA.is_file()
assert bytes_colombia > 3_000
columnas_clave = [
    "time", "latitude", "longitude", "depth", "mag", "magType",
    "id", "place", "horizontalError", "gap", "status",
]
faltan = [c for c in columnas_clave if c not in sismos_colombia.columns]
assert not faltan, f"Faltan columnas: {faltan}"
assert len(sismos_colombia) > 20, "El recorte de Colombia vino casi vacío. No cambie los parámetros."
print(f"Helpers + tabla Colombia: {len(sismos_colombia)} sismos. OK")
```

### Líneas base de la sesión 2

Una sola celda reconstruye lo que la red tiene que superar: la tabla de clasificación, la partición train / test, la línea base mayoritaria y la logística de la sesión 2, con los mismos parámetros. Si la red no supera estos dos números, no aporta nada que no tuviéramos ya.

```python
clasif_colombia = preparar_clasificacion(sismos_colombia)
X_co = clasif_colombia[FEATURES_CLASIFICACION].to_numpy()
y_co = clasif_colombia["ubicacion_debil"].to_numpy()

X_train_co, X_test_co, y_train_co, y_test_co = train_test_split(
    X_co,
    y_co,
    test_size=0.30,
    random_state=42,
    stratify=y_co if len(np.unique(y_co)) > 1 else None,
)

baseline_co = exactitud_mayoria(y_test_co)

modelo_logistico_co = LogisticRegression(max_iter=1000, random_state=42)
modelo_logistico_co.fit(X_train_co, y_train_co)
acc_log_co = accuracy_score(y_test_co, modelo_logistico_co.predict(X_test_co))

print("filas usables:", len(clasif_colombia), "| positivos:", int(y_co.sum()))
print("train:", X_train_co.shape[0], "test:", X_test_co.shape[0])
print("línea base mayoritaria (test):", round(baseline_co, 3))
print("exactitud logística (test):", round(acc_log_co, 3))
```

Fíjese en el tamaño del test. Colombia deja unas 19 filas para medir, así que **una sola fila** mal clasificada mueve la exactitud unos 5 puntos. Todos los números de la parte guiada son ruidosos por esa razón. Una diferencia de una o dos filas entre dos modelos no es evidencia de que uno sea mejor.

---

## Parte guiada A — Una red de una capa oculta desde cero (Colombia)

**Propósito.** Construir con numpy la red de las diapositivas, sin bibliotecas de aprendizaje automático: propagación hacia adelante, pérdida de entropía cruzada, retropropagación y descenso de gradiente. La etiqueta es la misma `ubicacion_debil` de la sesión 2 y las entradas son las mismas tres columnas. La pregunta de revisión no cambia: ¿paso esta fila a revisión de distrito, o la marco como sospechosa? Lo único que cambia es la forma de la frontera que separa las dos respuestas.

Escribirla a mano tiene un objetivo concreto. Cuando más adelante usemos `MLPClassifier`, sabremos qué está haciendo por dentro y qué decisiones toma por nosotros. Una red que no entendemos es difícil de defender en un informe técnico.

Una advertencia antes de empezar. Con unas 43 filas de entrenamiento, una red pequeña ya tiene más parámetros de los que conviene. Lo vamos a ver en la curva de pérdida y en la diferencia entre train y test. Ese resultado no es un fallo del código: es la lección de la sección.

### La red, en la notación de las diapositivas

Tenemos $D = 3$ entradas (`mag`, `depth`, `latitude`), $M$ unidades ocultas y una sola salida, porque la etiqueta es binaria. Las diapositivas numeran las salidas con $k = 1, \ldots, K$. Aquí $K = 1$, así que quitamos el índice $k$: los pesos de la salida son $w_j^{(2)}$ y su sesgo es $w_0^{(2)}$. Cada unidad oculta $j$ calcula una combinación lineal $a_j$ de las entradas y la pasa por una activación no lineal $h(\cdot)$. Usamos $h = \tanh$. La salida combina las $M$ unidades ocultas y pasa el resultado por una sigmoide $\sigma$, de modo que $y$ se lee como la probabilidad de ubicación débil:

$$
\begin{aligned}
a_j &= \sum_{i=1}^D w_{ji}^{(1)} x_i + w_{j0}^{(1)} \\
z_j &= h(a_j) \\
y &= \sigma\left( \sum_{j=1}^M w_{j}^{(2)} z_j + w_{0}^{(2)} \right)
\end{aligned}
$$

En el código, cada símbolo tiene un nombre. La etiqueta verdadera, que en las diapositivas es $t$, está en `y_train_co`. La salida de la red, $y$, la llamamos `y` dentro de las funciones.

| Símbolo | Variable | Forma |
|---------|----------|-------|
| $w_{ji}^{(1)}$ | `params["W1"]` | $(M, D)$ |
| $w_{j0}^{(1)}$ | `params["b1"]` | $(M,)$ |
| $w_{j}^{(2)}$ | `params["W2"]` | $(M,)$ |
| $w_{0}^{(2)}$ | `params["b2"]` | escalar |
| $\alpha$ | `alpha` | escalar |

### Paso 1 — Escalar las entradas

`mag` vive entre 4.5 y 6, `depth` puede pasar de 150 km y `latitude` va de -4.5 a 13.5. Si entran así, `depth` domina todas las combinaciones $a_j$ y la $\tanh$ se satura: su derivada queda casi en cero y la red deja de aprender. Por eso restamos la media y dividimos por la desviación estándar. Las dos se calculan **solo con train**. Si usáramos también las filas de test, el modelo vería información de la partición que luego usamos para medirlo.

```python
media_co = X_train_co.mean(axis=0)
desv_co = X_train_co.std(axis=0)

X_train_co_esc = (X_train_co - media_co) / desv_co
X_test_co_esc = (X_test_co - media_co) / desv_co

print("media train (mag, depth, latitude):", np.round(media_co, 2))
print("media train escalada:", np.round(X_train_co_esc.mean(axis=0), 3))
print("desviación train escalada:", np.round(X_train_co_esc.std(axis=0), 3))
```

### Paso 2 — Propagación hacia adelante

Tres funciones. `sigmoide` es la $\sigma$ de la salida. `inicializar_red` crea pesos pequeños y aleatorios con una semilla fija. `propagar_adelante` aplica las tres ecuaciones anteriores a todas las filas a la vez, usando productos de matrices en lugar de bucles.

```python
def sigmoide(a):
    r"""Sigmoide $\sigma(a) = 1 / (1 + e^{-a})$. Comprime cualquier número a $(0, 1)$."""
    return 1.0 / (1.0 + np.exp(-a))


def inicializar_red(n_entradas: int, n_ocultas: int, seed: int = 42) -> dict:
    """Crea los pesos iniciales de una red con una capa oculta y una salida.

    W1 tiene forma $(M, D)$: la fila $j$ guarda los pesos $w_{ji}^{(1)}$ de la unidad oculta $j$.
    W2 tiene forma $(M,)$: un peso $w_j^{(2)}$ por unidad oculta, porque hay una sola salida.
    Los sesgos empiezan en cero y los pesos en valores pequeños y aleatorios.
    """
    rng = np.random.default_rng(seed)
    return {
        "W1": rng.normal(0.0, 1.0 / np.sqrt(n_entradas), size=(n_ocultas, n_entradas)),
        "b1": np.zeros(n_ocultas),
        "W2": rng.normal(0.0, 1.0 / np.sqrt(n_ocultas), size=n_ocultas),
        "b2": 0.0,
    }


def propagar_adelante(X: np.ndarray, params: dict):
    r"""Propagación hacia adelante de la red de una capa oculta.

    Para cada fila de X calcula:
        $a_j = \sum_i w_{ji}^{(1)} x_i + w_{j0}^{(1)}$   (activación de la unidad oculta $j$)
        $z_j = h(a_j)$, con $h = \tanh$   (salida de la unidad oculta $j$)
        $y = \sigma(\sum_j w_j^{(2)} z_j + w_0^{(2)})$   (probabilidad de ubicación débil)

    Returns:
        ``a``, ``z``, ``y``. Devolvemos ``a`` y ``z`` porque la retropropagación los necesita.
    """
    a = X @ params["W1"].T + params["b1"]
    z = np.tanh(a)
    y = sigmoide(z @ params["W2"] + params["b2"])
    return a, z, y


params_inicio = inicializar_red(n_entradas=X_train_co_esc.shape[1], n_ocultas=8)
a_ini, z_ini, y_ini = propagar_adelante(X_train_co_esc, params_inicio)
print("forma de a y z (filas, unidades ocultas):", a_ini.shape, z_ini.shape)
print("primeras 5 salidas y:", np.round(y_ini[:5], 3))
```

### Paso 3 — La pérdida de entropía cruzada

Para una etiqueta binaria, la pérdida de las diapositivas es la entropía cruzada. Castiga mucho a la red cuando asigna una probabilidad baja a la clase correcta. Nosotros la promediamos sobre las $N$ filas, en vez de sumarla, para que su valor no dependa del tamaño de la partición:

$$
E(\mathbf{w}) = - \frac{1}{N} \sum_{n=1}^N \{ t_n \ln y_n + (1-t_n) \ln (1-y_n) \}
$$

```python
def perdida_entropia_cruzada(y: np.ndarray, t: np.ndarray) -> float:
    r"""Entropía cruzada media entre las probabilidades $y$ y las etiquetas $t \in \{0, 1\}$.

    Recorta $y$ lejos de 0 y 1 para que el logaritmo no explote.
    """
    y = np.clip(y, 1e-12, 1 - 1e-12)
    return float(-np.mean(t * np.log(y) + (1 - t) * np.log(1 - y)))


print("pérdida inicial:", round(perdida_entropia_cruzada(y_ini, y_train_co), 4))
print("referencia ln(2):", round(np.log(2), 4))
```

Una red que responde 0.5 para todo tiene una pérdida de $\ln 2 \approx 0.693$. La pérdida inicial queda cerca de ese valor: con pesos pequeños y aleatorios, todas las salidas del paso 2 rondan 0.5. Entrenar quiere decir bajar ese número.

### Paso 4 — Retropropagación

La retropropagación calcula cuánto cambia la pérdida si movemos cada peso un poco. Empieza por el error en la salida, $\delta$. Las diapositivas lo llaman $\delta_k$, uno por cada salida $k$. Con una sola salida basta $\delta$. Con sigmoide y entropía cruzada, ese error es simplemente la diferencia entre lo que la red dijo y la etiqueta. Luego el error viaja hacia atrás: cada unidad oculta $j$ recibe una parte de $\delta$, proporcional al peso $w_j^{(2)}$ que la conecta con la salida y multiplicada por la pendiente de su propia activación. Para $h = \tanh$, esa pendiente es $h'(a_j) = 1 - \tanh^2(a_j)$.

$$
\begin{aligned}
\delta &= y - t \\
\delta_j &= h'(a_j) \, w_j^{(2)} \delta \\
\frac{\partial E_n}{\partial w_{ji}^{(1)}} &= \delta_j x_i \\
\frac{\partial E_n}{\partial w_j^{(2)}} &= \delta z_j
\end{aligned}
$$

La suma $\sum_k w_{kj} \delta_k$ de las diapositivas tiene aquí un solo término, $w_j^{(2)} \delta$. Las dos últimas líneas son la regla general $\partial E_n / \partial w_{ji} = \delta_j z_i$: la derivada respecto a un peso es el error de la unidad a la que llega, por la entrada que trae. En la capa oculta, esa entrada es $x_i$. En la salida, es $z_j$. `retropropagar` hace eso para todas las filas y devuelve el gradiente promedio.

```python
def retropropagar(X: np.ndarray, t: np.ndarray, params: dict) -> dict:
    r"""Gradientes de la entropía cruzada media respecto a cada peso de la red.

    $\delta = y - t$   (error en la única salida)
    $\delta_j = h'(a_j) \, w_j^{(2)} \delta$   (error en la unidad oculta $j$)
    $\partial E / \partial w_{ji}^{(1)} = \delta_j x_i$ y $\partial E / \partial w_j^{(2)} = \delta z_j$

    Returns:
        Un diccionario con las mismas claves que params (W1, b1, W2, b2).
    """
    a, z, y = propagar_adelante(X, params)
    n = len(X)
    delta = y - t                                                    # (N,)
    delta_j = (1.0 - np.tanh(a) ** 2) * np.outer(delta, params["W2"])  # (N, M)
    return {
        "W1": delta_j.T @ X / n,
        "b1": delta_j.mean(axis=0),
        "W2": z.T @ delta / n,
        "b2": float(delta.mean()),
    }
```

Una retropropagación escrita a mano es fácil de equivocar por un signo o un índice, y el error no se nota: la red entrena igual, solo que peor. La forma clásica de verificarla es comparar con una aproximación numérica. Movemos un peso $\pm\epsilon$, medimos cómo cambia la pérdida, y dividimos. Si el código está bien, los dos números coinciden en muchos decimales.

```python
def gradiente_numerico(X, t, params, nombre, indice, eps=1e-6):
    r"""Aproxima $\partial E / \partial w$ para un solo peso con diferencias centradas. Solo para verificar."""
    mas = {k: np.array(v, dtype=float) for k, v in params.items()}
    menos = {k: np.array(v, dtype=float) for k, v in params.items()}
    mas[nombre][indice] += eps
    menos[nombre][indice] -= eps
    e_mas = perdida_entropia_cruzada(propagar_adelante(X, mas)[2], t)
    e_menos = perdida_entropia_cruzada(propagar_adelante(X, menos)[2], t)
    return (e_mas - e_menos) / (2 * eps)


grad_co = retropropagar(X_train_co_esc, y_train_co, params_inicio)
for nombre, indice in [("W1", (0, 1)), ("W1", (3, 2)), ("b1", (5,)), ("W2", (2,)), ("b2", ())]:
    analitico = float(np.asarray(grad_co[nombre])[indice])
    numerico = gradiente_numerico(X_train_co_esc, y_train_co, params_inicio, nombre, indice)
    print(f"{nombre}{indice}: retropropagación {analitico:+.6f} | numérico {numerico:+.6f}")
    assert abs(analitico - numerico) < 1e-6, "La retropropagación no coincide con el gradiente numérico."
print("Gradientes verificados. OK")
```

### Paso 5 — Descenso de gradiente

Con el gradiente, la regla de actualización de las diapositivas mueve cada peso un paso pequeño en la dirección que baja la pérdida. El tamaño del paso es la tasa de aprendizaje $\alpha$. Las diapositivas escriben la regla para una fila $n$. Nosotros usamos el gradiente promedio sobre todas las filas de entrenamiento en cada paso, porque con unas 43 filas no hace falta trabajar por lotes. Cada recorrido completo es una **época**, y guardamos la pérdida de cada época para dibujarla después. La regla se aplica a cada peso $w$ de la red, con las derivadas del paso 4.

$$
w \leftarrow w - \alpha \, \frac{\partial E}{\partial w}
$$

```python
def entrenar_red_numpy(
    X: np.ndarray,
    t: np.ndarray,
    n_ocultas: int = 8,
    alpha: float = 0.1,
    n_epochs: int = 2000,
    seed: int = 42,
):
    r"""Entrena la red de una capa oculta con descenso de gradiente sobre la entropía cruzada.

    $t$ debe ser 0/1. ``alpha`` es la tasa de aprendizaje $\alpha$.

    Returns:
        Los pesos entrenados y la lista de pérdidas de entrenamiento por época.
    """
    params = inicializar_red(X.shape[1], n_ocultas, seed=seed)
    historial = []
    for _ in range(n_epochs):
        gradientes = retropropagar(X, t, params)
        for clave in params:
            params[clave] = params[clave] - alpha * gradientes[clave]
        historial.append(perdida_entropia_cruzada(propagar_adelante(X, params)[2], t))
    return params, historial


def predecir_red_numpy(X: np.ndarray, params: dict, umbral: float = 0.5) -> np.ndarray:
    """Predice 0/1 con la red numpy: 1 si la probabilidad $y$ supera el umbral."""
    return (propagar_adelante(X, params)[2] >= umbral).astype(int)


params_red_co, historial_co = entrenar_red_numpy(X_train_co_esc, y_train_co)
print("pérdida en la época 1:", round(historial_co[0], 4))
print("pérdida en la última época:", round(historial_co[-1], 4))
```

### Paso 6 — La curva de pérdida

La curva muestra la pérdida de entrenamiento época a época. Una curva que baja quiere decir que el descenso de gradiente funciona. No quiere decir que el modelo generalice.

```python
fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(historial_co)
ax.axhline(np.log(2), color="gray", linestyle="--", label="ln 2 (responder 0.5 siempre)")
ax.set_xlabel("época")
ax.set_ylabel("entropía cruzada (train)")
ax.set_title("Colombia 2024: red de una capa oculta (M = 8)")
ax.legend()
plt.show()
```

La pérdida baja rápido al principio y después sigue bajando despacio. Si dejáramos correr más épocas seguiría bajando, porque $M = 8$ unidades ocultas con $D = 3$ entradas suman $MD + M + M + 1 = 41$ parámetros para unas 43 filas. Con esa capacidad, la red puede ir memorizando las filas de entrenamiento una por una. El siguiente paso dice si eso sirve para filas que no vio.

### Paso 7 — Exactitud frente al piso y la logística

Medimos la exactitud en train y en test, y la ponemos al lado de la línea base mayoritaria y de la logística de la sesión 2.

```python
acc_train_red_co = accuracy_score(y_train_co, predecir_red_numpy(X_train_co_esc, params_red_co))
acc_test_red_co = accuracy_score(y_test_co, predecir_red_numpy(X_test_co_esc, params_red_co))

print("línea base mayoritaria (test):", round(baseline_co, 3))
print("logística sesión 2 (test):    ", round(acc_log_co, 3))
print("red numpy (train):            ", round(acc_train_red_co, 3))
print("red numpy (test):             ", round(acc_test_red_co, 3))
print("¿supera la línea base en test?", acc_test_red_co > baseline_co)
```

Lo esperable con estos datos es una exactitud de train bastante más alta que la de test, y una exactitud de test pegada al piso. La red aprendió algo de las 43 filas que vio, pero ese algo no se transfiere a las 19 que no vio. Recuerde además que una fila mueve el test unos 5 puntos. Esto confirma lo que ya sugería la sesión 2: con `mag`, `depth` y `latitude`, la etiqueta de ubicación débil tiene poca señal en Colombia. Una frontera curva no crea señal donde no la hay. Lo que sí puede hacer es acomodarse mejor al ruido de train, y eso es justamente el sobreajuste.

**Comprobar:**

```python
D_co = len(FEATURES_CLASIFICACION)
assert params_red_co["W1"].shape == (8, D_co)
assert params_red_co["b1"].shape == (8,)
assert params_red_co["W2"].shape == (8,)
assert np.isfinite(historial_co).all()
assert historial_co[-1] < historial_co[0], "La pérdida no bajó. Revise alpha o el escalado."
assert 0.0 <= acc_test_red_co <= 1.0
assert acc_train_red_co >= exactitud_mayoria(y_train_co), "En train, la red debería al menos empatar el piso."
print("Red numpy Colombia: OK")
```

---

## Parte guiada B — MLP con scikit-learn y sobreajuste (Colombia)

**Propósito.** Pasar de la red escrita a mano a `MLPClassifier`, variar su tamaño, y medir con cuidado cuándo un modelo más grande deja de ayudar. Misma etiqueta, mismas tres entradas, misma partición. MLP quiere decir *multilayer perceptron*: es la misma red de la parte A, con la posibilidad de poner varias capas ocultas. scikit-learn decide por nosotros varias cosas que antes escribimos a mano. Usa ReLU en lugar de $\tanh$ como activación por defecto, el optimizador Adam en lugar del descenso de gradiente simple, y un criterio de parada propio.

En ingeniería civil, la tentación es clara: si un modelo pequeño no alcanza, probemos uno más grande. La pregunta de esta sección es qué número tiene que cambiar para decir que el modelo grande vale la pena. La respuesta es la exactitud de test frente al piso, no la de train.

### Paso 8 — Un MLP dentro de un pipeline

`make_pipeline(StandardScaler(), MLPClassifier(...))` junta el escalado del paso 1 y la red en un solo objeto. Al llamar `fit`, el escalador aprende media y desviación solo con las filas de train. Al llamar `predict` sobre test, las aplica sin volver a aprenderlas. Es la misma disciplina del paso 1, pero sin poder olvidarla. Empaquetamos la construcción en una función para que la parte individual reutilice exactamente la misma configuración sobre Perú.

```python
def entrenar_mlp(
    X_train: np.ndarray,
    y_train: np.ndarray,
    capas: tuple = (8,),
    alpha: float = 1e-4,
    early_stopping: bool = False,
    seed: int = 42,
):
    r"""Entrena StandardScaler + MLPClassifier y devuelve el pipeline ajustado.

    ``capas`` es ``hidden_layer_sizes``: ``(8,)`` es una capa oculta de 8 unidades,
    ``(32, 16)`` son dos capas ocultas. ``alpha`` es el peso de la penalización $L_2$
    (la $\lambda$ de las diapositivas), no la tasa de aprendizaje $\alpha$ de la parte A.
    Con early_stopping=True se reserva el 20% de train como validación.
    """
    opciones = {}
    if early_stopping:
        opciones = {"early_stopping": True, "validation_fraction": 0.2, "n_iter_no_change": 20}
    modelo = make_pipeline(
        StandardScaler(),
        MLPClassifier(
            hidden_layer_sizes=capas,
            alpha=alpha,
            max_iter=3000,
            random_state=seed,
            **opciones,
        ),
    )
    return modelo.fit(X_train, y_train)


mlp_8_co = entrenar_mlp(X_train_co, y_train_co, capas=(8,))
print("épocas usadas:", mlp_8_co[-1].n_iter_)
print("MLP (8,) train:", round(mlp_8_co.score(X_train_co, y_train_co), 3))
print("MLP (8,) test: ", round(mlp_8_co.score(X_test_co, y_test_co), 3))
print("línea base mayoritaria (test):", round(baseline_co, 3))
```

`score` devuelve la exactitud, igual que `accuracy_score`. Los números no tienen por qué coincidir con la red numpy: cambian la activación, el optimizador y el criterio de parada. Lo que importa es si las dos cuentan la misma historia frente al piso.

### Paso 9 — Tres tamaños, train frente a test

Entrenamos tres arquitecturas: una capa de 8 unidades, una capa de 16, y dos capas de 32 y 16. Para cada una guardamos la exactitud de train, la de test y la **brecha** entre las dos. Una brecha grande es la firma del sobreajuste.

```python
def comparar_tamanos(X_train, y_train, X_test, y_test, tamanos=((8,), (16,), (32, 16)), **opciones):
    """Entrena un MLP por cada tamaño y devuelve una tabla con train, test y brecha.

    opciones se pasa tal cual a entrenar_mlp (por ejemplo alpha o early_stopping).
    """
    filas = []
    for capas in tamanos:
        modelo = entrenar_mlp(X_train, y_train, capas=capas, **opciones)
        acc_train = modelo.score(X_train, y_train)
        acc_test = modelo.score(X_test, y_test)
        filas.append({
            "capas": str(capas),
            "parametros": sum(w.size for w in modelo[-1].coefs_) + sum(b.size for b in modelo[-1].intercepts_),
            "train": round(acc_train, 3),
            "test": round(acc_test, 3),
            "brecha": round(acc_train - acc_test, 3),
        })
    return pd.DataFrame(filas)


tamanos_co = comparar_tamanos(X_train_co, y_train_co, X_test_co, y_test_co)
print("línea base mayoritaria (test):", round(baseline_co, 3), "| logística:", round(acc_log_co, 3))
tamanos_co
```

La columna `parametros` cuenta pesos y sesgos. Compárela con las 43 filas de entrenamiento. Las dos capas de 32 y 16 tienen varias veces más parámetros que filas. Un gráfico ayuda a ver la brecha. Las barras son train y test, y la línea punteada es el piso.

```python
def graficar_train_test(tabla, piso, titulo):
    """Barras de exactitud train y test por arquitectura, con la línea base mayoritaria."""
    posiciones = np.arange(len(tabla))
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(posiciones - 0.2, tabla["train"], width=0.4, label="train")
    ax.bar(posiciones + 0.2, tabla["test"], width=0.4, label="test")
    ax.axhline(piso, color="gray", linestyle="--", label="línea base mayoritaria")
    ax.set_xticks(posiciones)
    ax.set_xticklabels(tabla["capas"])
    ax.set_ylim(0, 1.05)
    ax.set_xlabel("capas ocultas")
    ax.set_ylabel("exactitud")
    ax.set_title(titulo)
    ax.legend(loc="lower right")
    plt.show()


graficar_train_test(tamanos_co, baseline_co, "Colombia 2024: ubicación débil")
```

Cuando preparamos este cuaderno, la exactitud de train subía con el tamaño hasta cerca de 0.98, y la de test se quedaba en el piso (alrededor de 0.68) para los tres tamaños. Es decir, el modelo grande aprendió casi todas las filas de train y no mejoró nada en las de test. Esa es la definición práctica de sobreajuste: la red se ajusta a particularidades de las 43 filas que vio, no a un patrón que se repita en filas nuevas. Si alguien reportara solo la exactitud de train, diría que el modelo es casi perfecto. Por eso la exactitud de train nunca va sola en un informe.

### Paso 10 — Regularización $L_2$ (`alpha`)

Las diapositivas de aprendizaje profundo presentan la regularización $L_2$ como un castigo a los pesos grandes, sumado a la pérdida:

$$
L_{\text{reg}} = L + \lambda \sum_{l} \|\mathbf{W}^{(l)}\|_F^2
$$

Con $\lambda$ grande, la red prefiere pesos pequeños y fronteras más suaves, que se acomodan menos al ruido. En scikit-learn, $\lambda$ se llama `alpha`. Ojo con el nombre: no es la tasa de aprendizaje $\alpha$ de la parte A. En `MLPClassifier`, la tasa de aprendizaje es `learning_rate_init`.

Probamos cuatro valores sobre la red más grande, la que más sobreajustaba.

```python
filas_alpha_co = []
for valor in [1e-4, 1e-2, 1.0, 10.0]:
    modelo = entrenar_mlp(X_train_co, y_train_co, capas=(32, 16), alpha=valor)
    filas_alpha_co.append({
        "alpha": valor,
        "train": round(modelo.score(X_train_co, y_train_co), 3),
        "test": round(modelo.score(X_test_co, y_test_co), 3),
    })
alpha_co = pd.DataFrame(filas_alpha_co)
alpha_co["brecha"] = (alpha_co["train"] - alpha_co["test"]).round(3)
print("línea base mayoritaria (test):", round(baseline_co, 3))
alpha_co
```

Lea la tabla de arriba hacia abajo. Con `alpha` grande, la exactitud de train baja y la brecha se cierra. Eso es lo que la regularización promete. Si entre dos filas el test cambia en una sola fila, no le dé importancia: es el ruido de un test de 19 filas. Lo que no promete es que el test suba. Si en este recorte no hay señal más allá del piso, la regularización solo consigue que la red deje de fingir que la hay. Ese también es un resultado útil.

### Paso 11 — Parada temprana (`early_stopping`)

La otra técnica de las diapositivas es la parada temprana: separar una parte de train como **validación**, vigilar su exactitud durante el entrenamiento, y detenerse cuando deja de mejorar. Así el modelo no llega a la fase en la que solo memoriza.

El costo es concreto. Con `validation_fraction=0.2`, de las 43 filas de train unas 9 se apartan para validar. Esa validación es todavía más pequeña y ruidosa que el test, así que el momento de parar también es ruidoso.

```python
mlp_es_co = entrenar_mlp(X_train_co, y_train_co, capas=(32, 16), early_stopping=True)
acc_train_es_co = mlp_es_co.score(X_train_co, y_train_co)
acc_test_es_co = mlp_es_co.score(X_test_co, y_test_co)
print("épocas antes de parar:", mlp_es_co[-1].n_iter_)
print("MLP (32, 16) con early_stopping, train:", round(acc_train_es_co, 3))
print("MLP (32, 16) con early_stopping, test: ", round(acc_test_es_co, 3))
print("línea base mayoritaria (test):", round(baseline_co, 3))
```

Compare el número de épocas con las del paso 8. La red se detiene mucho antes y la brecha casi desaparece. Si el test sube una fila por encima del piso, no lo lea como una mejora: en 19 filas, una fila es ruido.

Resumen de la parte B para Colombia: con esta etiqueta y estas tres entradas, ningún tamaño de MLP supera de forma clara a la logística ni al piso. Más capas compran exactitud de train, no de test. `alpha` y `early_stopping` cierran la brecha, pero no inventan señal.

**Comprobar:**

```python
assert list(tamanos_co["capas"]) == ["(8,)", "(16,)", "(32, 16)"]
assert tamanos_co[["train", "test"]].apply(lambda c: c.between(0, 1)).all().all()
assert tamanos_co["parametros"].is_monotonic_increasing
grande = tamanos_co.iloc[-1]
assert grande["train"] >= grande["test"] - 0.05, "La red grande debería ir mejor en train que en test."
assert len(alpha_co) == 4
assert alpha_co["train"].iloc[-1] <= alpha_co["train"].iloc[0] + 0.05, "Con alpha alto, train no debería subir."
assert 0 < mlp_es_co[-1].n_iter_ < 3000
print("MLP Colombia (tamaños, alpha, early_stopping): OK")
```

---

## Parte guiada C — Una frontera no lineal (Colombia)

**Propósito.** Ver un caso donde la capa oculta **sí** hace una diferencia. Cambiamos de etiqueta: en lugar de la calidad de localización, preguntamos si un sismo es de **profundidad intermedia**, usando solo dónde ocurrió (latitud y longitud). Las partes A y B mostraron que una red no rescata una etiqueta sin señal. Falta la otra mitad de la historia: cuando la relación entre entradas y etiqueta tiene forma curva, un modelo lineal no la puede dibujar, por mucho que lo entrenemos.

### La etiqueta: profundidad intermedia

Una convención común en sismología separa los sismos **superficiales** (menos de 70 km) de los de **profundidad intermedia** (de 70 a 300 km). Usamos ese corte:
- `profundidad_intermedia = 1` si `depth >= 70` km
- `profundidad_intermedia = 0` en otro caso

En el norte de Sudamérica la diferencia tiene una lectura física. Los sismos superficiales suelen ocurrir en la corteza o cerca de la fosa. Los de profundidad intermedia ocurren dentro de la placa que se hunde bajo el continente. En Colombia, una parte importante de esos eventos intermedios se concentra bajo Santander, en el llamado **nido de Bucaramanga**. Otro grupo aparece en el extremo sur del recorte, cerca de la frontera con Ecuador y Perú. Que los sismos intermedios se agrupen en zonas concretas, con sismos superficiales alrededor, es lo que hace la frontera no lineal.

Sobre las entradas, la regla de no fuga se aplica igual. Como la etiqueta se define con `depth`, `depth` **no** entra como característica. Solo usamos `latitude` y `longitude`. `gap` y `horizontalError` no participan en esta sección.

### Paso 12 — Construir la tabla y la partición

Una función prepara la tabla, igual que `preparar_clasificacion` en la sesión 2. La parte individual la reutiliza sobre Perú. La partición usa los mismos parámetros de siempre.

```python
FEATURES_PROFUNDIDAD = ["latitude", "longitude"]


def preparar_profundidad(tabla: pd.DataFrame) -> pd.DataFrame:
    r"""Construye la etiqueta de profundidad intermedia (``depth`` $\geq 70$ km) y deja filas completas.

    La etiqueta usa depth.
    Las características son solo latitude y longitude. depth NO entra como característica.
    """
    trabajo = tabla[FEATURES_PROFUNDIDAD + ["depth"]].dropna().copy()
    trabajo["profundidad_intermedia"] = (trabajo["depth"] >= 70).astype(int)
    return trabajo


prof_colombia = preparar_profundidad(sismos_colombia)
X_pc = prof_colombia[FEATURES_PROFUNDIDAD].to_numpy()
y_pc = prof_colombia["profundidad_intermedia"].to_numpy()

X_train_pc, X_test_pc, y_train_pc, y_test_pc = train_test_split(
    X_pc,
    y_pc,
    test_size=0.30,
    random_state=42,
    stratify=y_pc if len(np.unique(y_pc)) > 1 else None,
)
baseline_pc = exactitud_mayoria(y_test_pc)

print("filas:", len(prof_colombia), "| profundidad intermedia:", int(y_pc.sum()))
print("train:", len(y_train_pc), "test:", len(y_test_pc))
print("línea base mayoritaria (test):", round(baseline_pc, 3))
```

### Paso 13 — Mapa de epicentros

Antes de entrenar, miramos dónde están los dos tipos de sismo. Cada punto es un epicentro, con la longitud en el eje horizontal y la latitud en el vertical.

```python
def mapa_profundidad(tabla: pd.DataFrame, titulo: str):
    """Dibuja los epicentros en longitud / latitud, coloreados por profundidad intermedia."""
    intermedio = tabla["profundidad_intermedia"] == 1
    fig, ax = plt.subplots(figsize=(5, 6))
    ax.scatter(tabla.loc[~intermedio, "longitude"], tabla.loc[~intermedio, "latitude"],
               alpha=0.6, label="superficial (< 70 km)")
    ax.scatter(tabla.loc[intermedio, "longitude"], tabla.loc[intermedio, "latitude"],
               alpha=0.6, label="intermedio (>= 70 km)")
    ax.set_xlabel("longitud")
    ax.set_ylabel("latitud")
    ax.set_title(titulo)
    ax.set_aspect("equal")
    ax.legend(loc="lower left")
    plt.show()


mapa_profundidad(prof_colombia, "Colombia 2024: epicentros por profundidad")
```

Los sismos intermedios forman dos grupos: uno muy compacto en Santander y otro al sur, cerca de la frontera con Ecuador. Los superficiales quedan a los dos lados. Ninguna recta en este plano deja los dos grupos de un lado y el resto del otro. Para eso hace falta una frontera que se cierre alrededor de ellos, y eso es lo que una capa oculta puede construir combinando varias rectas.

### Paso 14 — Logística frente a MLP

Entrenamos una logística, con el mismo escalado para que la comparación sea justa, y los tres tamaños de MLP con `comparar_tamanos`.

```python
logistica_pc = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000, random_state=42))
logistica_pc.fit(X_train_pc, y_train_pc)
acc_log_pc = logistica_pc.score(X_test_pc, y_test_pc)

tamanos_pc = comparar_tamanos(X_train_pc, y_train_pc, X_test_pc, y_test_pc)
mlp_pc = entrenar_mlp(X_train_pc, y_train_pc, capas=(8,))
acc_mlp_pc = mlp_pc.score(X_test_pc, y_test_pc)

print("línea base mayoritaria (test):", round(baseline_pc, 3))
print("logística (test):             ", round(acc_log_pc, 3))
print("MLP (8,) (test):              ", round(acc_mlp_pc, 3))
tamanos_pc
```

Cuando preparamos este cuaderno, la logística se quedaba en el piso (alrededor de 0.63) y el MLP de una capa con 8 unidades llegaba a cerca de 0.89 en test. Con 19 filas, esa diferencia son unas 5 filas. Sigue siendo una muestra pequeña, pero ahora la diferencia tiene una explicación física que vimos en el mapa, y no es una o dos filas sueltas.

Mire también la tabla de tamaños. Si los tres tamaños dan más o menos lo mismo en test, el modelo más pequeño es suficiente. Agregar capas no ayuda cuando una sola capa ya dibuja la frontera que hace falta.

### Paso 15 — Ver las fronteras

Para ver la diferencia, coloreamos cada punto del mapa según la probabilidad que cada modelo asigna a "profundidad intermedia". La logística solo puede partir el plano con una recta. El MLP puede cerrar una región.

```python
def dibujar_fronteras(modelos: dict, tabla: pd.DataFrame, titulo: str):
    """Colorea el plano longitud / latitud con la probabilidad de cada modelo y superpone los epicentros."""
    lon = np.linspace(tabla["longitude"].min() - 1, tabla["longitude"].max() + 1, 200)
    lat = np.linspace(tabla["latitude"].min() - 1, tabla["latitude"].max() + 1, 200)
    malla_lon, malla_lat = np.meshgrid(lon, lat)
    rejilla = np.column_stack([malla_lat.ravel(), malla_lon.ravel()])  # mismo orden que FEATURES_PROFUNDIDAD
    intermedio = tabla["profundidad_intermedia"] == 1

    fig, ejes = plt.subplots(1, len(modelos), figsize=(5 * len(modelos), 6))
    for ax, (nombre, modelo) in zip(np.atleast_1d(ejes), modelos.items()):
        prob = modelo.predict_proba(rejilla)[:, 1].reshape(malla_lon.shape)
        ax.contourf(malla_lon, malla_lat, prob, levels=np.linspace(0, 1, 11), cmap="RdBu_r", alpha=0.4)
        ax.contour(malla_lon, malla_lat, prob, levels=[0.5], colors="k")
        ax.scatter(tabla.loc[~intermedio, "longitude"], tabla.loc[~intermedio, "latitude"], s=15, label="superficial")
        ax.scatter(tabla.loc[intermedio, "longitude"], tabla.loc[intermedio, "latitude"], s=15, label="intermedio")
        ax.set_title(nombre)
        ax.set_xlabel("longitud")
        ax.set_ylabel("latitud")
        ax.set_aspect("equal")
    np.atleast_1d(ejes)[0].legend(loc="lower left")
    fig.suptitle(titulo)
    plt.show()


dibujar_fronteras({"logística": logistica_pc, "MLP (8,)": mlp_pc}, prof_colombia,
                  "Colombia 2024: frontera de decisión (línea negra = probabilidad 0.5)")
```

La línea negra es donde el modelo pasa de decir "superficial" a decir "intermedio". La de la logística es recta por construcción, y deja sismos superficiales y profundos de los dos lados. La del MLP dibuja una franja que encierra los dos grupos de sismos intermedios. Esa es, en una imagen, la diferencia entre la sesión 2 y la de hoy.

Fíjese también en lo que pasa lejos de los puntos. El MLP asigna probabilidades a zonas donde no hay ningún sismo de entrenamiento. Ahí el color no significa nada: es una extrapolación de la forma de la red, no conocimiento sobre la tectónica de esa zona.

### Lectura civil

Este modelo **clasifica la profundidad a partir de la ubicación**. No estima peligro sísmico, intensidad del movimiento ni daño. Un sismo de profundidad intermedia y uno cortical de la misma magnitud producen movimientos distintos en superficie, pero medir eso requiere otros datos y otros modelos, que no hemos usado aquí. Lo que sí ilustra es una idea útil para la ingeniería: cuando la física produce estructuras localizadas, como el nido de Bucaramanga, un modelo lineal sobre coordenadas no las representa. Un MLP pequeño sí. Y lo hace con 43 filas de entrenamiento porque la estructura es nítida, no porque la red sea grande.

**Comprobar:**

```python
assert set(prof_colombia["profundidad_intermedia"].unique()).issubset({0, 1})
assert "depth" not in FEATURES_PROFUNDIDAD, "depth define la etiqueta. No puede ser característica."
assert len(prof_colombia) > 20
assert 0.5 <= baseline_pc <= 1.0
assert 0.0 <= acc_log_pc <= 1.0 and 0.0 <= acc_mlp_pc <= 1.0
assert acc_mlp_pc >= baseline_pc - 0.10, "El MLP quedó muy por debajo del piso. Revise la tabla."
print("¿El MLP supera a la logística en test?", acc_mlp_pc > acc_log_pc)
print("Frontera no lineal Colombia: OK")
```

---

## Parte individual — Perú 2024

**Propósito.** Repetir las partes B y C sobre Perú, comparar con Colombia, y justificar por escrito qué tamaño de modelo usaría y cuándo un MLP no compensa su complejidad. La parte A sobre Perú es opcional. Las fechas y la magnitud mínima no cambian. Lo único que cambia es la ventana geográfica. Perú tiene unas dos veces más sismos que Colombia en este recorte, así que el test será de unas 40 filas: sigue siendo pequeño, pero una fila ya mueve la exactitud unos 2.5 puntos y no 5.

No escriba funciones nuevas. Reutilice `build_usgs_url`, `download_csv`, `preparar_clasificacion`, `exactitud_mayoria`, `entrenar_mlp`, `comparar_tamanos`, `graficar_train_test`, `preparar_profundidad`, `mapa_profundidad` y `dibujar_fronteras` tal como quedaron. Un método que solo funciona con los datos para los que se escribió no es un método. `PARAMETROS_CURSO` es el contrato con las sesiones siguientes, que vuelven a descargar este mismo recorte. **No lo modifique.**

| Constante | Valor |
|-----------|--------|
| Latitud | -18.5 a 0.2 |
| Longitud | -82 a -68 |

Al final tendrá que comparar:
- El **piso** de cada etiqueta en Perú frente a Colombia.
- La **brecha** entre train y test de cada tamaño de MLP.
- Si el MLP **supera a la logística** en cada etiqueta, y por cuántas filas.
- Una **justificación escrita** del tamaño de modelo que usaría.

### Descargar y cargar Perú

Un solo bloque: parámetros del curso, URL, descarga y lectura.

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

bytes_peru = download_csv(USGS_URL_PERU, CATALOGO_PERU)
sismos_peru = pd.read_csv(CATALOGO_PERU)
print("Filas, columnas:", sismos_peru.shape)
sismos_peru.head()
```

**Comprobar:**

```python
assert "minlatitude=-18.5" in USGS_URL_PERU
assert CATALOGO_PERU.is_file()
assert bytes_peru > 3_000
assert len(sismos_peru) > 50, "El recorte del Perú vino casi vacío. Revise la URL."
print(f"Tabla Perú: {len(sismos_peru)} sismos. OK")
```

### Paso 16 — Líneas base de Perú

La misma celda de líneas base de la sesión 2, ahora con Perú: tabla de clasificación, partición, piso y logística.

```python
clasif_peru = preparar_clasificacion(sismos_peru)
X_pe = clasif_peru[FEATURES_CLASIFICACION].to_numpy()
y_pe = clasif_peru["ubicacion_debil"].to_numpy()

X_train_pe, X_test_pe, y_train_pe, y_test_pe = train_test_split(
    X_pe,
    y_pe,
    test_size=0.30,
    random_state=42,
    stratify=y_pe if len(np.unique(y_pe)) > 1 else None,
)

baseline_pe = exactitud_mayoria(y_test_pe)

modelo_logistico_pe = LogisticRegression(max_iter=1000, random_state=42)
modelo_logistico_pe.fit(X_train_pe, y_train_pe)
acc_log_pe = accuracy_score(y_test_pe, modelo_logistico_pe.predict(X_test_pe))

print("filas usables:", len(clasif_peru), "| positivos:", int(y_pe.sum()))
print("train:", X_train_pe.shape[0], "test:", X_test_pe.shape[0])
print("línea base mayoritaria (test):", round(baseline_pe, 3))
print("exactitud logística (test):", round(acc_log_pe, 3))
```

Note que en Perú la clase mayoritaria es la de ubicación **débil**. Buena parte de la sismicidad ocurre mar adentro, donde las estaciones solo pueden estar de un lado, y eso empuja el `gap` hacia arriba. A diferencia de Colombia, aquí la logística sí supera el piso. Esa es la referencia que el MLP tiene que mejorar.

### Paso 17 — Parte B sobre Perú

Tres tamaños, cuatro valores de `alpha` sobre la red grande, y parada temprana. Todo con las funciones de la parte guiada.

```python
tamanos_pe = comparar_tamanos(X_train_pe, y_train_pe, X_test_pe, y_test_pe)
print("línea base mayoritaria (test):", round(baseline_pe, 3), "| logística:", round(acc_log_pe, 3))
tamanos_pe
```

```python
graficar_train_test(tamanos_pe, baseline_pe, "Perú 2024: ubicación débil")

filas_alpha_pe = []
for valor in [1e-4, 1e-2, 1.0, 10.0]:
    modelo = entrenar_mlp(X_train_pe, y_train_pe, capas=(32, 16), alpha=valor)
    filas_alpha_pe.append({
        "alpha": valor,
        "train": round(modelo.score(X_train_pe, y_train_pe), 3),
        "test": round(modelo.score(X_test_pe, y_test_pe), 3),
    })
alpha_pe = pd.DataFrame(filas_alpha_pe)
alpha_pe["brecha"] = (alpha_pe["train"] - alpha_pe["test"]).round(3)

mlp_es_pe = entrenar_mlp(X_train_pe, y_train_pe, capas=(32, 16), early_stopping=True)
acc_train_es_pe = mlp_es_pe.score(X_train_pe, y_train_pe)
acc_test_es_pe = mlp_es_pe.score(X_test_pe, y_test_pe)
print("early_stopping: épocas", mlp_es_pe[-1].n_iter_,
      "| train", round(acc_train_es_pe, 3), "| test", round(acc_test_es_pe, 3))
alpha_pe
```

Preguntas para leer estos resultados:
1. ¿Algún tamaño de MLP supera a la logística en test por más de una o dos filas (2.5 a 5 puntos)?
2. ¿La red grande vuelve a llegar cerca de 1.0 en train? ¿Cuánto mide su brecha frente a la de Colombia?
3. ¿Qué hace `early_stopping` aquí? Si la exactitud de test cae **por debajo del piso**, la red se detuvo antes de aprender algo útil. Con unas 19 filas de validación, el momento de parar depende de muy pocos ejemplos.

### Paso 18 — Parte C sobre Perú

Misma etiqueta de profundidad intermedia, mismas dos entradas.

```python
prof_peru = preparar_profundidad(sismos_peru)
X_pp = prof_peru[FEATURES_PROFUNDIDAD].to_numpy()
y_pp = prof_peru["profundidad_intermedia"].to_numpy()

X_train_pp, X_test_pp, y_train_pp, y_test_pp = train_test_split(
    X_pp,
    y_pp,
    test_size=0.30,
    random_state=42,
    stratify=y_pp if len(np.unique(y_pp)) > 1 else None,
)
baseline_pp = exactitud_mayoria(y_test_pp)

logistica_pp = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000, random_state=42))
logistica_pp.fit(X_train_pp, y_train_pp)
acc_log_pp = logistica_pp.score(X_test_pp, y_test_pp)

tamanos_pp = comparar_tamanos(X_train_pp, y_train_pp, X_test_pp, y_test_pp)
print("filas:", len(prof_peru), "| profundidad intermedia:", int(y_pp.sum()))
print("línea base mayoritaria (test):", round(baseline_pp, 3))
print("logística (test):", round(acc_log_pp, 3))
tamanos_pp
```

```python
mapa_profundidad(prof_peru, "Perú 2024: epicentros por profundidad")

mlp_pp = entrenar_mlp(X_train_pp, y_train_pp, capas=(32, 16))
acc_mlp_pp = mlp_pp.score(X_test_pp, y_test_pp)
dibujar_fronteras({"logística": logistica_pp, "MLP (32, 16)": mlp_pp}, prof_peru,
                  "Perú 2024: frontera de decisión (línea negra = probabilidad 0.5)")
```

En Perú la geografía es otra. La placa de Nazca se hunde hacia el este bajo los Andes, así que los sismos intermedios tienden a quedar tierra adentro y los superficiales cerca de la costa o mar adentro. Pero hay sismos superficiales tierra adentro mezclados con los intermedios. Mire el mapa antes de leer la tabla. ¿La frontera que necesita se parece más a una recta o a una región cerrada? ¿Qué tamaño de MLP hace falta para mejorar a la logística, y qué le pasa a la brecha con ese tamaño?

Compare también la forma de la frontera del MLP grande con la de Colombia. ¿Sigue una estructura que pueda explicar con la tectónica, o rodea filas sueltas de entrenamiento? La primera es una frontera no lineal. La segunda es sobreajuste dibujado en un mapa.

### (Opcional) Parte A sobre Perú

Si le queda tiempo, entrene la red numpy sobre la etiqueta de ubicación débil de Perú. Recuerde escalar con la media y la desviación de **train de Perú**, no las de Colombia.

```python
media_pe = X_train_pe.mean(axis=0)
desv_pe = X_train_pe.std(axis=0)
X_train_pe_esc = (X_train_pe - media_pe) / desv_pe
X_test_pe_esc = (X_test_pe - media_pe) / desv_pe

params_red_pe, historial_pe = entrenar_red_numpy(X_train_pe_esc, y_train_pe)
acc_train_red_pe = accuracy_score(y_train_pe, predecir_red_numpy(X_train_pe_esc, params_red_pe))
acc_test_red_pe = accuracy_score(y_test_pe, predecir_red_numpy(X_test_pe_esc, params_red_pe))
print("red numpy Perú, train:", round(acc_train_red_pe, 3), "| test:", round(acc_test_red_pe, 3))
print("línea base mayoritaria (test):", round(baseline_pe, 3), "| logística:", round(acc_log_pe, 3))
```

**Comprobar:**

```python
assert len(clasif_peru) > 50 and len(prof_peru) > 50
assert len(tamanos_pe) == 3 and len(tamanos_pp) == 3
assert len(alpha_pe) == 4
for tabla in [tamanos_pe, tamanos_pp, alpha_pe]:
    assert tabla[["train", "test"]].apply(lambda c: c.between(0, 1)).all().all()
assert 0.5 <= baseline_pe <= 1.0 and 0.5 <= baseline_pp <= 1.0
assert 0.0 <= acc_log_pe <= 1.0 and 0.0 <= acc_log_pp <= 1.0
assert 0.0 <= acc_mlp_pp <= 1.0
print("Partes B y C sobre Perú: OK")
print("URL del curso (guárdela):", USGS_URL_PERU)
```

### Paso 19 — Colombia frente a Perú

Una tabla con los números que necesita para justificar su elección. Cada fila es una etiqueta en un país.

```python
def fila_resumen(pais, etiqueta, y_test, piso, acc_log, tamanos):
    """Resume una etiqueta en un país: tamaño del test, piso, logística y los MLP (8,) y (32, 16).

    La diferencia con la logística se expresa también en filas de test.
    """
    chico = tamanos.set_index("capas").loc["(8,)"]
    grande = tamanos.set_index("capas").loc["(32, 16)"]
    return {
        "país": pais,
        "etiqueta": etiqueta,
        "filas test": len(y_test),
        "piso": round(piso, 3),
        "logística": round(acc_log, 3),
        "MLP (8,) test": chico["test"],
        "MLP (32, 16) train": grande["train"],
        "MLP (32, 16) test": grande["test"],
        "filas (8,) - logística": int(round((chico["test"] - acc_log) * len(y_test))),
        "filas (32, 16) - logística": int(round((grande["test"] - acc_log) * len(y_test))),
    }


resumen = pd.DataFrame([
    fila_resumen("Colombia", "ubicación débil", y_test_co, baseline_co, acc_log_co, tamanos_co),
    fila_resumen("Perú", "ubicación débil", y_test_pe, baseline_pe, acc_log_pe, tamanos_pe),
    fila_resumen("Colombia", "profundidad intermedia", y_test_pc, baseline_pc, acc_log_pc, tamanos_pc),
    fila_resumen("Perú", "profundidad intermedia", y_test_pp, baseline_pp, acc_log_pp, tamanos_pp),
])
resumen
```

Las dos últimas columnas traducen la diferencia a filas, que es la unidad honesta con muestras tan pequeñas. "El MLP acierta 4 filas más de 40" se discute distinto que "el MLP mejora 10 puntos". No elegimos el mejor tamaño mirando el test: eso sería usar la partición de evaluación para entrenar una decisión. Si la ventaja solo aparece con la red grande y su train está cerca de 1.0, pregúntese cuánto de esa ventaja sobreviviría con otra partición.

### Paso 20 — Justificar el tamaño del modelo

Complete en sus palabras. No basta con pegar los números. Diga qué modelo usaría para cada etiqueta en Perú, por qué ese tamaño y no uno más grande, y en qué caso el MLP no compensa su complejidad frente a la logística. Piense en lo que cuesta un modelo más grande: más parámetros que explicar, más sensibilidad a la partición, y una brecha que hay que vigilar.

```python
justificacion_modelo = """
Que cambio al pasar de Colombia a Peru (pisos, brechas, ventaja del MLP sobre la logistica):
Que modelo y que tamano usaria para la ubicacion debil en Peru, y por que:
Que modelo y que tamano usaria para la profundidad intermedia en Peru, y por que:
En que caso el MLP no compensa su complejidad frente a la logistica:
"""
print(justificacion_modelo)
```

---

## Ticket de salida

Escriba **exactamente dos oraciones**. En la primera, elija un modelo (logística, MLP pequeño o MLP grande) para **una** decisión civil concreta, por ejemplo marcar filas sospechosas antes de una revisión de distrito. En la segunda, nombre **un límite** de esa decisión que el modelo no puede resolver solo.

```python
ticket_de_salida = """
Oracion 1:
Oracion 2:
"""
print(ticket_de_salida)
```

<!-- end NOTEBOOK: -->
