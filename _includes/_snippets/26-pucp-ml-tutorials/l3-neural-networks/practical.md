<!-- NOTEBOOK: -->

Este cuaderno entrena las arquitecturas de la sesión. Cada bloque describe los datos utilizados, cuál es la tarea que se quiere solucionar y por qué esa arquitectura encaja.

Ejecute las celdas de arriba hacia abajo. En cada **Comprobar**, confirme el mensaje `OK` antes de seguir.

---

## Importaciones

```python
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
from sklearn.datasets import load_digits, make_moons
from sklearn.decomposition import PCA
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

Quinientos puntos en el plano forman dos medias lunas entrelazadas, con un poco de ruido. La tarea es decir a qué luna pertenece un punto nuevo.

Una recta no puede separar las lunas. El perceptrón y la logística de la sesión 2 son rectas, así que se quedan cortos.

Un perceptrón multicapa añade una capa oculta. Cada unidad oculta es una curva sobre las dos coordenadas. La capa de salida combina esas curvas y puede rodear una luna.

Implementamos un `MLPClassifier` dentro de un `pipeline`. `hidden_layer_sizes=(8,)` es una capa oculta de 8 unidades. Por defecto la activación es ReLU y el optimizador es Adam. `alpha` es la penalización $L_2$, no la tasa de aprendizaje.

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
    # La clase más frecuente en test. Es el piso si el modelo no aprende nada.
    piso = float(max(y_test.mean(), 1.0 - y_test.mean()))
    logistica = LogisticRegression().fit(X_train, y_train)
    perceptron = Perceptron(random_state=42).fit(X_train, y_train)
    return {
        "piso (mayoría)": piso,
        "logística": float(logistica.score(X_test, y_test)),
        "perceptrón": float(perceptron.score(X_test, y_test)),
    }


# Dos lunas. noise=0.25 las mezcla lo justo para que una recta no baste.
X_lunas, y_lunas = make_moons(n_samples=500, noise=0.25, random_state=42)

# El color es la luna. Una recta no puede dejar cada color de un solo lado.
plt.figure(figsize=(5, 4))
plt.scatter(X_lunas[:, 0], X_lunas[:, 1], c=y_lunas, cmap="coolwarm", edgecolor="k", s=18)
plt.xlabel("x1")
plt.ylabel("x2")
plt.title("Dos lunas")
plt.show()

X_train, X_test, y_train, y_test = train_test_split(
    X_lunas, y_lunas, test_size=0.30, random_state=42, stratify=y_lunas
)

# El escalador aprende la media y la desviación solo con train.
escalador_lunas = StandardScaler().fit(X_train)
X_train_esc = escalador_lunas.transform(X_train)
X_test_esc = escalador_lunas.transform(X_test)
bases_lunas = lineas_base_lunas(X_train_esc, y_train, X_test_esc, y_test)
print("train:", len(y_train), "| test:", len(y_test))
print({nombre: round(valor, 3) for nombre, valor in bases_lunas.items()})
```

```python
# StandardScaler y la red viven en el mismo objeto.
mlp_lunas = make_pipeline(
    StandardScaler(),
    MLPClassifier(
        hidden_layer_sizes=(8,),  # una capa oculta, 8 unidades
        alpha=1e-4,               # penalización L2
        max_iter=2000,
        random_state=42,
    ),
)
# fit recibe las lunas sin escalar. El pipeline escala por dentro.
mlp_lunas.fit(X_train, y_train)
exactitud_mlp = float(mlp_lunas.score(X_test, y_test))
print("exactitud MLP en test:", round(exactitud_mlp, 3))
```

La logística corta el plano con una recta. El MLP cierra una región alrededor de cada luna.

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
    # El color de fondo es la clase predicha. El punto es la clase real.
    zz = predecir(malla).reshape(xx.shape)
    ax.contourf(xx, yy, zz, alpha=0.35, cmap="coolwarm")
    ax.scatter(X[:, 0], X[:, 1], c=y, cmap="coolwarm", edgecolor="k", s=16)
    ax.set_title(titulo)
    ax.set_xlabel("x1")
    ax.set_ylabel("x2")


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

La serie trae el número anual de manchas solares, de 1700 a 2008. El ciclo dura unos 11 años, así que el valor del próximo año depende de los anteriores. La tarea es predecir el año que sigue a partir de una ventana de 11 años.

Una red recurrente encaja porque el estado oculto guarda lo que ya vio en la ventana. Los mismos pesos se reutilizan en cada año, así que la ventana podría tener otra longitud. La predicción sale del último estado oculto.

Las líneas base no tienen memoria aprendida. La persistencia repite el último año. La media responde siempre el promedio de train. La regresión lineal usa la misma ventana, pero suma los años con pesos fijos y sin estado oculto.

```python
import statsmodels.api as sm


def preparar_manchas(ventana=11):
    """Arma ventanas de manchas solares y una partición por año.

    Train llega hasta 1950.
    Test es 1951 a 2008.
    La media y la desviación salen solo de train.

    Args:
        ventana: Cuántos años mira el modelo antes de predecir el siguiente.

    Returns:
        Ventanas de train y de test, la serie completa y los años de test.
    """
    tabla = sm.datasets.sunspots.load_pandas().data
    valores = tabla["SUNACTIVITY"].to_numpy(dtype=float)
    anios = tabla["YEAR"].to_numpy()
    # Cada fila es una ventana. El objetivo es el año que queda justo después.
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


def recm(y_real, y_pred):
    """Raíz del error cuadrático medio, en la escala de las manchas.

    Args:
        y_real: Valores observados.
        y_pred: Valores predichos, en la misma escala.

    Returns:
        Un número. Cero sería una predicción perfecta.
    """
    return float(np.sqrt(np.mean((y_real - y_pred) ** 2)))


serie = preparar_manchas()
# Persistencia: el próximo año será igual al último de la ventana.
ultimo_anio = serie["a_original"](serie["X_test"][:, -1])
media_train = float(serie["a_original"](np.zeros(1)))  # el cero escalado es la media
recm_media = recm(serie["y_test"], np.full_like(serie["y_test"], media_train))
recm_persistencia = recm(serie["y_test"], ultimo_anio)
print("años de test:", len(serie["y_test"]))
print("RECM media:", round(recm_media, 1), "| RECM persistencia:", round(recm_persistencia, 1))

# La línea vertical separa train (hasta 1950) de test.
plt.figure(figsize=(8, 3))
plt.plot(serie["anios"], serie["valores"], color="black")
plt.axvline(1950, color="gray", linestyle="--")
plt.xlabel("año")
plt.ylabel("manchas")
plt.title("Manchas solares")
plt.show()
```

```python
class ModeloSecuencia(nn.Module):
    """Lee una ventana año por año y predice un solo número.

    El estado oculto se actualiza en cada paso con los mismos pesos.
    La cabeza lineal lee solo el último estado.

    Args:
        n_entradas: Cuántos números llegan en cada año. Aquí es 1.
        n_ocultas: Tamaño del estado oculto.
    """

    def __init__(self, n_entradas, n_ocultas):
        super().__init__()
        # batch_first pone el lote delante y el tiempo después.
        self.rnn = nn.RNN(n_entradas, n_ocultas, batch_first=True)
        self.cabeza = nn.Linear(n_ocultas, 1)

    def forward(self, x):
        """Predice el año siguiente a cada ventana.

        Args:
            x: Tensor de forma (lote, años, n_entradas).

        Returns:
            Tensor de forma (lote, 1).
        """
        # h_T tiene un estado por capa. Con una capa, h_T[-1] es el final de la ventana.
        salida, h_T = self.rnn(x)
        return self.cabeza(h_T[-1])


def entrenar_rnn(X_train, y_train, n_ocultas=16, epocas=80):
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
    # La RNN espera (lote, tiempo, características). Hay una característica por año.
    X = torch.tensor(X_train, dtype=torch.float32).unsqueeze(-1)
    y = torch.tensor(y_train, dtype=torch.float32).unsqueeze(-1)
    modelo = ModeloSecuencia(n_entradas=1, n_ocultas=n_ocultas)
    optimizador = torch.optim.SGD(modelo.parameters(), lr=0.05)
    perdida_fn = nn.MSELoss()
    historial = []
    for epoca in range(epocas):
        optimizador.zero_grad()
        prediccion = modelo(X)
        perdida = perdida_fn(prediccion, y)
        perdida.backward()
        # Si el producto a lo largo del tiempo crece, este recorte lo limita.
        nn.utils.clip_grad_norm_(modelo.parameters(), max_norm=1.0)
        optimizador.step()
        historial.append(float(perdida))
    return modelo, historial


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


rnn_manchas, historial_rnn = entrenar_rnn(serie["X_train"], serie["y_train"])
pred_test = serie["a_original"](predecir_rnn(rnn_manchas, serie["X_test"]))
recm_rnn = recm(serie["y_test"], pred_test)
print("RECM RNN:", round(recm_rnn, 1), "| pérdida inicial:", round(historial_rnn[0], 3),
      "| pérdida final:", round(historial_rnn[-1], 3))

# En test se ve si la RNN sigue el ciclo o solo copia el año anterior.
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
assert recm_rnn < recm_media
print("La RNN mejora el promedio de train. OK")
```

---

## Dígitos escritos a mano

`load_digits` trae 1797 imágenes de 8 por 8 píxeles, sin usar la etiqueta de clase. La tarea es comprimir cada imagen en un código corto y reconstruirla. No hay etiqueta que predecir. El objetivo es la propia imagen.

Un autoencoder encaja porque el codificador produce el código y el decodificador vuelve a los 64 píxeles. El código es más corto que la imagen, así que la red tiene que quedarse con lo que importa.

La línea base lineal es PCA con el mismo tamaño de código, 8 números. PCA también comprime y reconstruye, pero solo con rectas.

```python
def preparar_digitos(K=8):
    """Escala los dígitos a [0, 1], parte 70/30 y reconstruye con PCA.

    Args:
        K: Cuántos números tiene el código. PCA usa los mismos.

    Returns:
        Train, test y la reconstrucción PCA del test.
    """
    imagenes = load_digits().data
    # Los píxeles originales van de 0 a 16. Los pasamos a 0-1.
    imagenes = imagenes / imagenes.max()
    X_train, X_test = train_test_split(imagenes, test_size=0.30, random_state=42)
    pca = PCA(n_components=K).fit(X_train)
    reconstruccion_pca = pca.inverse_transform(pca.transform(X_test))
    return X_train, X_test, reconstruccion_pca


def ecm(real, reconstruido):
    """Error cuadrático medio entre una imagen y su reconstrucción.

    Args:
        real: Imágenes observadas, una por fila.
        reconstruido: Imágenes producidas por el modelo.

    Returns:
        El promedio de los cuadrados de las diferencias.
    """
    return float(np.mean((real - reconstruido) ** 2))


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


X_train_d, X_test_d, X_hat_pca = preparar_digitos()
print("train:", X_train_d.shape, "| test:", X_test_d.shape)
print("ECM de PCA:", round(ecm(X_test_d, X_hat_pca), 4))

# Ocho dígitos de test, antes de comprimirlos.
mostrar_imagenes([("original", X_test_d[:8])])
```

```python
class Autoencoder(nn.Module):
    """Comprime un vector de tamaño D y lo reconstruye.

    El codificador baja de D a M y luego al código.
    El decodificador hace el camino de vuelta.

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


def entrenar_autoencoder(X_train, epocas=25):
    """Ajusta el autoencoder para minimizar el error de reconstrucción.

    Args:
        X_train: Imágenes de train, una por fila.
        epocas: Pasadas completas por train.

    Returns:
        El modelo y la pérdida de cada época.
    """
    torch.manual_seed(42)
    X = torch.tensor(X_train, dtype=torch.float32)
    modelo = Autoencoder(D=X.shape[1], M=32, codigo=8)
    optimizador = torch.optim.Adam(modelo.parameters(), lr=1e-3)
    perdida_fn = nn.MSELoss()
    historial = []
    for epoca in range(epocas):
        optimizador.zero_grad()
        reconstruccion = modelo(X)
        # El objetivo es la entrada. No hay otra etiqueta.
        perdida = perdida_fn(reconstruccion, X)
        perdida.backward()
        optimizador.step()
        historial.append(float(perdida))
    return modelo, historial


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
        # El VAE devuelve también mu y log_var. El autoencoder devuelve solo la imagen.
        if isinstance(salida, tuple):
            salida = salida[0]
        return salida.numpy()


ae_digitos, historial_ae = entrenar_autoencoder(X_train_d)
recon_ae = reconstruir(ae_digitos, X_test_d[:8])
ecm_ae = ecm(X_test_d, reconstruir(ae_digitos, X_test_d))
print("ECM autoencoder:", round(ecm_ae, 4), "| pérdida final:", round(historial_ae[-1], 4))

# El autoencoder conserva el trazo. PCA, con el mismo tamaño de código, lo borra más.
mostrar_imagenes([
    ("original", X_test_d[:8]),
    ("autoencoder", recon_ae),
    ("PCA", X_hat_pca[:8]),
])
```

**Comprobar:**

```python
assert historial_ae[-1] < historial_ae[0]
assert ecm_ae < ecm(X_test_d, X_hat_pca)
print("El autoencoder reconstruye mejor que PCA. OK")
```

---

## Los mismos dígitos, con un VAE

Los datos son las mismas imágenes. La tarea ya no es solo reconstruir un dígito visto. También queremos dibujar dígitos nuevos. El autoencoder guarda un punto por imagen.

Nada nos dice qué puntos del código corresponden a dígitos que no vimos. El VAE guarda una distribución por imagen. El codificador produce una media y una dispersión. El código es una muestra de esa distribución, y el decodificador la convierte en píxeles.

Para dibujar un dígito nuevo se muestra de la distribución estándar y se decodifica.

```python
class VAE(nn.Module):
    """Codifica cada imagen como una gaussiana y decodifica una muestra.

    log_var es el logaritmo de la varianza, más estable que guardar sigma.

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
        # Reparametrización. epsilon es ruido estándar, y el gradiente pasa por mu y sigma.
        epsilon = torch.randn_like(mu)
        z = mu + torch.exp(0.5 * log_var) * epsilon
        return self.decodificador(z), mu, log_var


def perdida_vae(reconstruccion, x, mu, log_var):
    """Suma el error de reconstrucción y la divergencia KL.

    La KL acerca la gaussiana de cada imagen a la normal estándar.
    Así un código nuevo, sacado de esa normal, sigue siendo decodificable.

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


def entrenar_vae(X_train, epocas=40):
    """Ajusta el VAE con reconstrucción más KL.

    Args:
        X_train: Imágenes de train, una por fila.
        epocas: Pasadas completas por train.

    Returns:
        El modelo y la pérdida de cada época.
    """
    torch.manual_seed(42)
    X = torch.tensor(X_train, dtype=torch.float32)
    modelo = VAE(D=X.shape[1], M=32, codigo=8)
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
        # El código no viene de una imagen. Viene de la distribución previa.
        z = torch.randn(n, modelo.mu.out_features)
        return modelo.decodificador(z).numpy()


vae_digitos, historial_vae = entrenar_vae(X_train_d)
ecm_vae = ecm(X_test_d, reconstruir(vae_digitos, X_test_d))
print("ECM VAE:", round(ecm_vae, 4), "| pérdida final:", round(historial_vae[-1], 1))

# La fila de abajo no reconstruye una foto. Sale de un código nuevo.
mostrar_imagenes([
    ("original", X_test_d[:8]),
    ("VAE", reconstruir(vae_digitos, X_test_d[:8])),
    ("muestras", muestras_vae(vae_digitos)),
])
```

El VAE suele reconstruir un poco peor que el autoencoder.

Paga la KL a cambio de poder muestrear dígitos nuevos.

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

```python
%pip install -q torch_geometric
```

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
    # edge_index tiene dos filas: origen y destino de cada cita.
    origen, destino = grafo.edge_index
    A[origen, destino] = 1.0
    return grafo, A


class CapaGCN(nn.Module):
    """Una capa que mezcla el vector de cada nodo con el de sus vecinos.

    Args:
        n_entrada: Tamaño del vector que llega.
        n_salida: Tamaño del vector que sale.
        activar: Si es False, no aplica ReLU. La última capa deja los puntajes libres.
    """

    def __init__(self, n_entrada, n_salida, activar=True):
        super().__init__()
        # Los mismos pesos para todos los nodos.
        self.lineal = nn.Linear(n_entrada, n_salida)
        # La última capa predice temas, así que no aplica ReLU a los puntajes.
        self.activar = activar

    def forward(self, H, A):
        """Aplica la convolución del grafo.

        Args:
            H: Vectores de los nodos, forma (nodos, n_entrada).
            A: Adyacencia, forma (nodos, nodos).

        Returns:
            Vectores nuevos, forma (nodos, n_salida).
        """
        # El bucle propio deja pasar el texto del propio artículo.
        A_tilde = A + torch.eye(A.shape[0])
        # Cada fila se escala para que un nodo con muchos vecinos no domine.
        D_inv_sqrt = torch.diag(A_tilde.sum(dim=1).pow(-0.5))
        A_hat = D_inv_sqrt @ A_tilde @ D_inv_sqrt
        mezclado = A_hat @ self.lineal(H)
        if self.activar:
            return torch.relu(mezclado)
        return mezclado


class RedGCN(nn.Module):
    """Dos capas. La segunda alcanza artículos a dos citas de distancia.

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


cora, A_cora = cargar_cora()
# Línea base: las palabras solas, sin el grafo.
logistica_cora = LogisticRegression(max_iter=2000)
X_train_cora = cora.x[cora.train_mask].numpy()
y_train_cora = cora.y[cora.train_mask].numpy()
X_test_cora = cora.x[cora.test_mask].numpy()
y_test_cora = cora.y[cora.test_mask].numpy()
logistica_cora.fit(X_train_cora, y_train_cora)
exactitud_logistica = float(logistica_cora.score(X_test_cora, y_test_cora))
print("nodos:", cora.num_nodes, "| características:", cora.num_features)
print("exactitud logística sin grafo:", round(exactitud_logistica, 3))

temas, cuentas = np.unique(cora.y.numpy(), return_counts=True)
fig, ejes = plt.subplots(1, 2, figsize=(9, 3))
ejes[0].bar(temas, cuentas, color="steelblue")
ejes[0].set_xlabel("tema")
ejes[0].set_ylabel("artículos")
ejes[0].set_title("Artículos por tema")
# El grado es el número de citas de cada artículo.
ejes[1].hist(A_cora.sum(dim=1).numpy(), bins=30, color="steelblue")
ejes[1].set_xlabel("citas")
ejes[1].set_ylabel("artículos")
ejes[1].set_title("Cuántas citas tiene cada artículo")
plt.tight_layout()
plt.show()
```

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
        # La pérdida usa solo los 140 nodos de train. El resto no enseña.
        perdida = nn.functional.cross_entropy(puntajes[grafo.train_mask], grafo.y[grafo.train_mask])
        perdida.backward()
        optimizador.step()
        historial.append(float(perdida))
    modelo.eval()
    with torch.no_grad():
        pred = modelo(grafo.x, A).argmax(dim=1)[grafo.test_mask].numpy()
        exactitud = accuracy_score(grafo.y[grafo.test_mask].numpy(), pred)
    return modelo, historial, float(exactitud)


gcn_cora, historial_gcn, exactitud_gcn = entrenar_gcn(cora, A_cora)
print("exactitud GCN:", round(exactitud_gcn, 3), "| pérdida final:", round(historial_gcn[-1], 3))

plt.figure(figsize=(4, 3))
plt.bar(["logística", "GCN"], [exactitud_logistica, exactitud_gcn], color=["gray", "steelblue"])
plt.ylabel("exactitud en test")
plt.ylim(0, 1)
plt.title("Palabras solas frente a palabras y citas")
plt.show()

# El plano es solo las palabras (dos componentes). El color de la derecha es el tema que dice la GCN.
plano = PCA(n_components=2).fit_transform(cora.x.numpy())
en_test = cora.test_mask.numpy()
with torch.no_grad():
    pred_cora = gcn_cora(cora.x, A_cora).argmax(dim=1).numpy()
fig, ejes = plt.subplots(1, 2, figsize=(9, 4))
ejes[0].scatter(plano[en_test, 0], plano[en_test, 1], c=cora.y.numpy()[en_test], cmap="tab10", s=8)
ejes[0].set_title("Tema real")
ejes[1].scatter(plano[en_test, 0], plano[en_test, 1], c=pred_cora[en_test], cmap="tab10", s=8)
ejes[1].set_title("Tema que predice la GCN")
for eje in ejes:
    eje.set_xlabel("palabra 1")
    eje.set_ylabel("palabra 2")
plt.tight_layout()
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
