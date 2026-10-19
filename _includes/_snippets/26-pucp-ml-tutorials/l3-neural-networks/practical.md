<!-- NOTEBOOK: -->

Este cuaderno entrena las arquitecturas de la sesión. Cada bloque describe los datos utilizados, cuál es la tarea que se quiere solucionar y por qué esa arquitectura encaja.

Ejecute las celdas de arriba hacia abajo. En cada **Comprobar**, confirme el mensaje `OK` antes de seguir.

---

## Importaciones

En el siguiente bloque importamos las librerías y conjuntos de datos que usaremos a lo largo del cuaderno.

```python
import matplotlib.pyplot as plt
import numpy as np
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

## Texto

El párrafo de abajo es el conjunto de datos. La tarea es predecir el carácter que sigue a una ventana de 11 caracteres. Una red recurrente encaja porque lee la ventana de a un carácter y guarda lo ya visto en el estado oculto. Los mismos pesos se reutilizan en cada carácter. La predicción sale del último estado oculto.

### El párrafo

El texto cabe en el cuaderno. Es corto a propósito, para que la red pueda aprenderlo en la sesión y continuar la semilla.

```python
texto = (
    "el temblor movió la estación cercana. "
    "la estación registró el movimiento del suelo. "
    "el operador revisó la señal y avisó al centro. "
    "el centro comparó la señal con las estaciones vecinas."
)
print(texto)
print("largo:", len(texto))
```

Cada fila es una ventana de 11 caracteres, y el objetivo es el carácter que sigue. La primera ventana es `el temblor` más el espacio que la separa de `movió`. El objetivo de esa fila es la `m`. La segunda se corre un carácter y el objetivo es la `o`. La tercera empieza con un espacio y el objetivo es la `v`. La última es `nes vecinas` y el objetivo es el punto final. La celda de abajo imprime esas cuatro, no las 174.

En la función, `texto[i - 11:i]` copia esos 11 caracteres. Cada carácter se vuelve un vector de ceros con un 1 en su columna del alfabeto. `np.stack` apila esas ventanas. El objetivo no es el carácter escrito, es su posición en el alfabeto, porque la pérdida compara índices.

```python
def preparar_texto(texto, ventana=11):
    """Arma ventanas de caracteres y el índice del carácter que sigue.

    Args:
        texto: Párrafo del que salen las ventanas.
        ventana: Cuántos caracteres mira el modelo antes de predecir el siguiente.

    Returns:
        Las ventanas en one-hot, el índice de cada objetivo y el alfabeto.
    """
    alfabeto = sorted(set(texto))
    indice = {caracter: i for i, caracter in enumerate(alfabeto)}
    filas = []
    objetivos = []
    for i in range(ventana, len(texto)):
        fila = np.zeros((ventana, len(alfabeto)))
        for t, caracter in enumerate(texto[i - ventana:i]):
            fila[t, indice[caracter]] = 1.0
        filas.append(fila)
        objetivos.append(indice[texto[i]])
    return np.stack(filas), np.array(objetivos), alfabeto
```

Cada ventana es una matriz de 11 filas y 22 columnas. Cada fila es un carácter. Cada columna es una letra del alfabeto. Hay un 1 en la columna de ese carácter y 0 en las demás. La `e` de la primera ventana tiene el 1 en la columna 6. La red no lee las letras. Lee estas matrices, así que esa es la entrada. `X_texto` apila las 174 matrices, una por ventana. En PyTorch ese bloque se llama tensor y su forma se escribe `(174, 11, 22)`. `y_texto` es el índice del carácter objetivo, uno por ventana, y no es parte de esas matrices.

```python
X_texto, y_texto, alfabeto = preparar_texto(texto)
print("ventanas", X_texto.shape, "| alfabeto", len(alfabeto))
for nombre, k in (("primera", 0), ("segunda", 1), ("tercera", 2), ("última", -1)):
    ventana = "".join(alfabeto[i] for i in X_texto[k].argmax(axis=1))
    print(nombre, repr(ventana), "| objetivo:", repr(alfabeto[y_texto[k]]))
```

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
        salida, h_T = self.rnn(x)
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
    lote_y = torch.tensor(y, dtype=torch.long)
    modelo = ModeloTexto(n_caracteres=X.shape[-1], n_ocultas=n_ocultas)
    optimizador = torch.optim.Adam(modelo.parameters(), lr=1e-3)
    perdida_fn = nn.CrossEntropyLoss()
    historial = []
    for epoca in range(epocas):
        optimizador.zero_grad()
        puntajes = modelo(lote_x)
        perdida = perdida_fn(puntajes, lote_y)
        perdida.backward()
        # Después de backward cada peso tiene un gradiente.
        # Si el largo de ese vector pasa de 1, lo encoge hasta dejarlo en 1.
        # El producto de las pendientes en los 11 caracteres puede hacer enorme el paso.
        nn.utils.clip_grad_norm_(modelo.parameters(), max_norm=1.0)
        optimizador.step()
        historial.append(float(perdida))
    return modelo, historial
```

Para escribir, partimos de una semilla de 11 caracteres. La red elige el carácter de mayor puntaje, lo agregamos al final y soltamos el primero. Esa ventana nueva vuelve a entrar, y repetimos.

```python
def generar(modelo, semilla, n, alfabeto):
    """Completa la semilla con n caracteres, eligiendo el de mayor puntaje.

    Args:
        modelo: Red ya entrenada.
        semilla: Cadena inicial, del largo de la ventana.
        n: Cuántos caracteres nuevos escribir.
        alfabeto: Caracteres en el mismo orden que las columnas one-hot.

    Returns:
        La semilla seguida de los caracteres nuevos.
    """
    indice = {caracter: i for i, caracter in enumerate(alfabeto)}
    ventana = semilla
    nuevos = []
    modelo.eval()
    with torch.no_grad():
        for paso in range(n):
            fila = np.zeros((1, len(ventana), len(alfabeto)))
            for t, caracter in enumerate(ventana):
                fila[0, t, indice[caracter]] = 1.0
            puntajes = modelo(torch.tensor(fila, dtype=torch.float32))
            letra = alfabeto[int(puntajes.argmax(dim=1))]
            nuevos.append(letra)
            ventana = ventana[1:] + letra
    return semilla + "".join(nuevos)
```

La semilla es la primera ventana del párrafo. Lo que sigue debería parecerse al texto, porque el párrafo es corto y la red lo vio entero.

```python
rnn_texto, historial_texto = entrenar_texto(X_texto, y_texto)
generado = generar(rnn_texto, texto[:11], n=80, alfabeto=alfabeto)
print("pérdida inicial:", round(historial_texto[0], 3), "| final:", round(historial_texto[-1], 3))
print(generado)
```

**Comprobar:**

```python
assert historial_texto[-1] < historial_texto[0]
assert len(generado) == 11 + 80
print("La red continúa el texto. OK")
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
