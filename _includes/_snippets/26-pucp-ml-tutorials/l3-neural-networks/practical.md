<!-- NOTEBOOK: -->

Este cuaderno entrena las arquitecturas de la sesión, en el mismo orden que las diapositivas.

Cada bloque dice qué datos hay, cuál es la tarea y por qué esa arquitectura encaja.

El código que sigue está comentado para leerlo línea por línea.

Ejecute las celdas de arriba hacia abajo. En cada **Comprobar**, confirme el mensaje `OK` antes de seguir.

---

## Importaciones

```python
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

Quinientos puntos en el plano forman dos medias lunas entrelazadas, con un poco de ruido.

La tarea es decir a qué luna pertenece un punto nuevo.

Una recta no puede separar las lunas.

El perceptrón y la logística de la sesión 2 son rectas, así que se quedan cortos.

Un perceptrón multicapa añade una capa oculta.

Cada unidad oculta es una curva sobre las dos coordenadas.

La capa de salida combina esas curvas y puede rodear una luna.

La implementación es la de las diapositivas: `MLPClassifier` dentro de un `pipeline`.

`hidden_layer_sizes=(8,)` es una capa oculta de 8 unidades.

Por defecto la activación es ReLU y el optimizador es Adam.

`alpha` es la penalización $L_2$, no la tasa de aprendizaje.

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
# StandardScaler y la red viven en el mismo objeto, como en la diapositiva.
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

**Comprobar:**

```python
assert exactitud_mlp > bases_lunas["logística"]
assert exactitud_mlp > bases_lunas["perceptrón"]
print("El MLP separa las lunas mejor que una recta. OK")
```

---

## Manchas solares

La serie trae el número anual de manchas solares, de 1700 a 2008.

El ciclo dura unos 11 años, así que el valor del próximo año depende de los anteriores.

La tarea es predecir el año que sigue a partir de una ventana de 11 años.

Una red recurrente encaja porque el estado oculto guarda lo que ya vio en la ventana.

Los mismos pesos se reutilizan en cada año, así que la ventana podría tener otra longitud.

La predicción sale del último estado oculto, como en la diapositiva.

Las líneas base no tienen memoria aprendida.

La persistencia repite el último año.

La media responde siempre el promedio de train.

La regresión lineal usa la misma ventana, pero suma los años con pesos fijos y sin estado oculto.

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
        Tensores de train y de test, y la función que devuelve la escala original.
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
```

Cambiar `nn.RNN` por `nn.LSTM` o `nn.GRU` en `ModeloSecuencia` es el cambio de una línea de la diapositiva.

LSTM y GRU devuelven el estado de otra forma, así que aquí dejamos la RNN.

**Comprobar:**

```python
assert len(serie["y_test"]) == 58
assert historial_rnn[-1] < historial_rnn[0]
assert recm_rnn < recm_media
print("La RNN mejora el promedio de train. OK")
```

---

## Dígitos escritos a mano

`load_digits` trae 1797 imágenes de 8 por 8 píxeles, sin usar la etiqueta de clase.

La tarea es comprimir cada imagen en un código corto y reconstruirla.

No hay etiqueta que predecir. El objetivo es la propia imagen.

Un autoencoder encaja porque el codificador produce el código y el decodificador vuelve a los 64 píxeles.

El código es más corto que la imagen, así que la red tiene que quedarse con lo que importa.

La línea base lineal es PCA con el mismo tamaño de código, 8 números.

PCA también comprime y reconstruye, pero solo con rectas.

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


X_train_d, X_test_d, X_hat_pca = preparar_digitos()
print("train:", X_train_d.shape, "| test:", X_test_d.shape)
print("ECM de PCA:", round(ecm(X_test_d, X_hat_pca), 4))
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
ecm_ae = ecm(X_test_d, reconstruir(ae_digitos, X_test_d))
print("ECM autoencoder:", round(ecm_ae, 4), "| pérdida final:", round(historial_ae[-1], 4))
```

**Comprobar:**

```python
assert historial_ae[-1] < historial_ae[0]
assert ecm_ae < ecm(X_test_d, X_hat_pca)
print("El autoencoder reconstruye mejor que PCA. OK")
```

---

## Los mismos dígitos, con un VAE

Los datos son las mismas imágenes.

La tarea ya no es solo reconstruir un dígito visto.

También queremos dibujar dígitos nuevos.

El autoencoder guarda un punto por imagen.

Nada nos dice qué puntos del código corresponden a dígitos que no vimos.

El VAE guarda una distribución por imagen.

El codificador produce una media y una dispersión.

El código es una muestra de esa distribución, y el decodificador la convierte en píxeles.

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
print("Muestras nuevas, forma:", muestras_vae(vae_digitos).shape)
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

Cora es una red de 2708 artículos.

Cada artículo es una bolsa de 1433 palabras, y una arista lo une con los artículos que cita.

La tarea es predecir el tema del artículo, entre 7 temas.

La partición ya viene dada: 140 artículos de train y 1000 de test.

Una logística mira solo las palabras de cada artículo e ignora las citas.

Eso falla cuando dos artículos del mismo tema se citan pero no comparten las mismas palabras.

Una capa convolucional de grafos mezcla cada artículo con sus vecinos.

El tema puede llegar por una cita, no solo por el texto.

La capa de abajo es la de la diapositiva.

`torch_geometric` solo trae el grafo. No es la capa.

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
```

**Comprobar:**

```python
assert cora.num_nodes == 2708
assert int(cora.train_mask.sum()) == 140
assert historial_gcn[-1] < historial_gcn[0]
assert exactitud_gcn > exactitud_logistica
print("La GCN usa las citas y supera a la logística. OK")
```

---

## Fotografías CIFAR-10

CIFAR-10 son fotografías a color de 32 por 32 píxeles.

Hay 10 clases, entre ellas avión, automóvil y pájaro.

La tarea es nombrar el objeto de una foto nueva.

Un perceptrón multicapa trataría cada píxel como una coordenada suelta y no vería que un borde es el mismo en cualquier parte de la foto.

Una red convolucional recorre la imagen con un mismo núcleo.

Ese núcleo busca un patrón local, por ejemplo un borde, y lo puede encontrar en cualquier posición.

Luego una agrupación reduce la foto y la siguiente capa ve patrones un poco más grandes.

El modelo es el de la diapositiva.

Usamos 8000 fotos de train y 2000 de test para que el ajuste quepa en la sesión.

La descarga de CIFAR-10 ocurre una sola vez.

```python
%pip install -q torchvision
```

```python
from torch.utils.data import DataLoader, Subset
from torchvision import datasets, transforms


def cargar_cifar(n_train=8000, n_test=2000):
    """Descarga CIFAR-10 y devuelve dos cargadores con un subconjunto.

    Args:
        n_train: Cuántas fotos de train usar.
        n_test: Cuántas fotos de test usar.

    Returns:
        El cargador de train y el de test.
    """
    transformacion = transforms.ToTensor()
    train = datasets.CIFAR10(root="datos_cifar", train=True, download=True, transform=transformacion)
    test = datasets.CIFAR10(root="datos_cifar", train=False, download=True, transform=transformacion)
    cargador_train = DataLoader(Subset(train, range(n_train)), batch_size=128, shuffle=True)
    cargador_test = DataLoader(Subset(test, range(n_test)), batch_size=128)
    return cargador_train, cargador_test


def exactitud_cargador(modelo, cargador):
    """Fracción de fotos bien clasificadas.

    Args:
        modelo: Red que devuelve 10 puntajes por foto.
        cargador: Lotes de fotos y etiquetas.

    Returns:
        La exactitud entre 0 y 1.
    """
    modelo.eval()
    aciertos = 0
    total = 0
    with torch.no_grad():
        for fotos, etiquetas in cargador:
            pred = modelo(fotos).argmax(dim=1)
            aciertos += int((pred == etiquetas).sum())
            total += len(etiquetas)
    return aciertos / total


def entrenar_fotos(modelo, cargador_train, epocas=3):
    """Entrena un clasificador de fotos con entropía cruzada.

    Args:
        modelo: CNN o red residual.
        cargador_train: Lotes de CIFAR-10.
        epocas: Pasadas por el subconjunto de train.

    Returns:
        El modelo y la pérdida media de cada época.
    """
    optimizador = torch.optim.Adam(modelo.parameters(), lr=1e-3)
    perdida_fn = nn.CrossEntropyLoss()
    historial = []
    for epoca in range(epocas):
        modelo.train()
        total = 0.0
        lotes = 0
        for fotos, etiquetas in cargador_train:
            optimizador.zero_grad()
            # CrossEntropyLoss aplica el softmax. El modelo devuelve puntajes.
            perdida = perdida_fn(modelo(fotos), etiquetas)
            perdida.backward()
            optimizador.step()
            total += float(perdida)
            lotes += 1
        historial.append(total / lotes)
    return modelo, historial


cargador_train, cargador_test = cargar_cifar()
cnn = nn.Sequential(
    nn.Conv2d(3, 32, kernel_size=3, padding=1),  # 32 mapas, la foto sigue en 32x32
    nn.ReLU(),
    nn.MaxPool2d(2),                              # 32x32 pasa a 16x16
    nn.Conv2d(32, 64, kernel_size=3, padding=1),
    nn.ReLU(),
    nn.MaxPool2d(2),                              # 16x16 pasa a 8x8
    nn.Flatten(),
    nn.Linear(64 * 8 * 8, 10),                    # 10 clases
)
cnn, historial_cnn = entrenar_fotos(cnn, cargador_train)
exactitud_cnn = exactitud_cargador(cnn, cargador_test)
print("exactitud CNN:", round(exactitud_cnn, 3), "| pérdida final:", round(historial_cnn[-1], 3))
```

Azar puro acertaría cerca de 0.10, porque hay 10 clases.

Con pocas épocas el número no es el de un modelo grande.

Sí debe quedar por encima del azar.

**Comprobar:**

```python
assert historial_cnn[-1] < historial_cnn[0]
assert exactitud_cnn > 0.20
print("La CNN supera el azar en CIFAR-10. OK")
```

---

## Las mismas fotografías, con un bloque residual

Los datos y la tarea son los de CIFAR-10.

La red de arriba ya usa convoluciones.

Si la hacemos mucho más honda, el gradiente tiene que cruzar muchas capas y el entrenamiento se estanca.

Un bloque residual pide a las capas una corrección, y suma la entrada al final.

El gradiente tiene un camino directo por esa suma.

El bloque es el de la diapositiva.

Lo metemos en una red pequeña, con las mismas fotos, para ver el atajo en el código.

```python
class BloqueResidual(nn.Module):
    """Dos convoluciones que aprenden una corrección, más la entrada.

    Args:
        canales: Mapas de entrada y de salida. Tienen que coincidir para poder sumar.
    """

    def __init__(self, canales):
        super().__init__()
        self.conv1 = nn.Conv2d(canales, canales, 3, padding=1)
        self.conv2 = nn.Conv2d(canales, canales, 3, padding=1)
        self.relu = nn.ReLU()

    def forward(self, x):
        """Devuelve la corrección sumada a la entrada, y luego ReLU.

        Args:
            x: Mapas de forma (lote, canales, alto, ancho).

        Returns:
            Mapas de la misma forma.
        """
        # F(x). padding=1 mantiene el alto y el ancho, así la suma es válida.
        correccion = self.conv2(self.relu(self.conv1(x)))
        return self.relu(correccion + x)


class RedResidual(nn.Module):
    """Una convolución de entrada, un bloque residual y la capa de 10 clases.

    La primera convolución pasa de 3 canales de color a 32 mapas.
    El bloque trabaja sobre esos 32 mapas.
    """

    def __init__(self):
        super().__init__()
        self.entrada = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.ReLU(),
        )
        self.bloque = BloqueResidual(32)
        self.pool = nn.AdaptiveAvgPool2d(1)
        self.cabeza = nn.Linear(32, 10)

    def forward(self, x):
        """Clasifica un lote de fotos.

        Args:
            x: Fotos de forma (lote, 3, 32, 32).

        Returns:
            Diez puntajes por foto.
        """
        mapas = self.bloque(self.entrada(x))
        # Un número por mapa, y de ahí a las 10 clases.
        return self.cabeza(self.pool(mapas).flatten(1))


resnet, historial_resnet = entrenar_fotos(RedResidual(), cargador_train)
exactitud_resnet = exactitud_cargador(resnet, cargador_test)
print("exactitud residual:", round(exactitud_resnet, 3), "| pérdida final:", round(historial_resnet[-1], 3))
```

**Comprobar:**

```python
assert historial_resnet[-1] < historial_resnet[0]
assert exactitud_resnet > 0.20
print("El bloque residual entrena sobre las mismas fotos. OK")
```

<!-- end NOTEBOOK: -->
