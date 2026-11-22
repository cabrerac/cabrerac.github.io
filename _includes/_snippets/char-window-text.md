<!-- NOTEBOOK: -->

### El párrafo

El texto cabe en el cuaderno. Es corto a propósito, para que una red pequeña pueda aprenderlo en la sesión.

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

Cada fila es una ventana de 11 caracteres, y el objetivo es el carácter que sigue. La primera ventana es `el temblor` más el espacio que la separa de `movió`. El objetivo de esa fila es la `m`. La segunda se corre un carácter y el objetivo es la `o`. La tercera empieza con un espacio y el objetivo es la `v`. La última es `nes vecinas` y el objetivo es el punto final.

En la función, `texto[i - 11:i]` copia esos 11 caracteres. Cada carácter se vuelve un vector de ceros con un 1 en su columna del alfabeto. `np.stack` apila esas ventanas. Esta transformación permite comparar indices (i.e., posiciones en el alfabeto) en lugar del carácter escrito.

```python
def preparar_texto(texto, ventana=11):
    """Arma ventanas de caracteres y el índice del carácter que sigue.

    Args:
        texto: Párrafo del que salen las ventanas.
        ventana: Cuántos caracteres mira el modelo antes de predecir el siguiente.

    Returns:
        Las ventanas en one-hot, el índice de cada objetivo y el alfabeto.
    """
    # Ordena los caracteres distintos del párrafo
    alfabeto = sorted(set(texto))
    # Crea un diccionario para convertir un caracter en su indice
    indice = {caracter: i for i, caracter in enumerate(alfabeto)}
    filas = []
    objetivos = []
    for i in range(ventana, len(texto)):
        # 11 filas (i.e., caracteres) y una columna por letra del alfabeto
        fila = np.zeros((ventana, len(alfabeto)))
        for t, caracter in enumerate(texto[i - ventana:i]):
            # Pone el 1 en la columna de ese carácter
            fila[t, indice[caracter]] = 1.0
        filas.append(fila)
        # Guarda el índice del carácter que sigue a la ventana
        objetivos.append(indice[texto[i]])
    # Apila las ventanas en un solo bloque
    return np.stack(filas), np.array(objetivos), alfabeto
```

Cada ventana es una matriz de 11 filas y 22 columnas. Cada fila es un carácter. Cada columna es una letra del alfabeto. Hay un 1 en la columna de ese carácter y 0 en las demás. La `e` de la primera ventana tiene el 1 en la columna 6. La red no lee las letras. Lee estas matrices, así que esa es la entrada. `X_texto` apila las 174 matrices, una por ventana. En PyTorch ese bloque se llama tensor y su forma se escribe `(174, 11, 22)`. `y_texto` es el índice del carácter objetivo, uno por ventana, y no es parte de esas matrices.

```python
X_texto, y_texto, alfabeto = preparar_texto(texto)
print("ventanas", X_texto.shape, "| alfabeto", len(alfabeto))
for nombre, k in (("primera", 0), ("segunda", 1), ("tercera", 2), ("última", -1)):
    # Lee la columna del 1 en cada fila y la vuelve a convertir en letra
    ventana = "".join(alfabeto[i] for i in X_texto[k].argmax(axis=1))
    print(nombre, repr(ventana), "| objetivo:", repr(alfabeto[y_texto[k]]))
```

<!-- end NOTEBOOK: -->
