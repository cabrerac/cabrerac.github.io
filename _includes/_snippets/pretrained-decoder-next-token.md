<!-- NOTEBOOK: -->

---

## Parte C: solo decodificador

Un transformador solo decodificador lee los tokens de izquierda a derecha, con la máscara causal: cada token mira solo los anteriores. Se preentrena con la tarea de la sesión, predecir el siguiente token, como GPT. Encaja cuando queremos saber cómo sigue un texto. Aquí solo miramos las probabilidades del siguiente token. No dejamos que el modelo escriba texto, eso lo veremos en la sesión 5.

Los datos son el comienzo de frases sobre sismos. La tarea es ver qué tokens el modelo considera más probables a continuación. Usamos `Qwen/Qwen2.5-0.5B`, un modelo abierto pequeño que maneja español, unos 1 GB. `AutoModelForCausalLM` descarga el transformador con su capa de salida, la que da un puntaje por cada token del vocabulario. `dtype=torch.float32` pide los pesos con la precisión habitual de la CPU, así los resultados no cambian entre versiones de la librería.

```python
MODELO_SIGUIENTE = "Qwen/Qwen2.5-0.5B"  # nombre del modelo en Hugging Face
tokenizador_siguiente = AutoTokenizer.from_pretrained(MODELO_SIGUIENTE)  # descarga el tokenizador
modelo_siguiente = AutoModelForCausalLM.from_pretrained(MODELO_SIGUIENTE, dtype=torch.float32)  # descarga el decodificador
modelo_siguiente.eval()  # modo de uso, sin entrenamiento
print("parámetros:", modelo_siguiente.num_parameters())  # tamaño del modelo
print("tokens del vocabulario:", len(tokenizador_siguiente))  # cuántos tokens puede proponer
```

`siguientes_tokens` sigue los pasos de la sesión. El modelo da un puntaje por token del vocabulario en cada posición. Tomamos los de la última posición, los pasamos por softmax para tener probabilidades y nos quedamos con las `k` más altas.

```python
def siguientes_tokens(contexto, k):
    """Los k tokens más probables después de un texto.

    Args:
        contexto: Comienzo de una frase.
        k: Cuántos tokens devolver.

    Returns:
        Lista de pares (texto del token, probabilidad), de más a menos probable.
    """
    entrada = tokenizador_siguiente(contexto, return_tensors="pt")  # números de token del contexto
    with torch.no_grad():  # solo leemos el modelo, sin gradientes
        salida = modelo_siguiente(**entrada)  # un puntaje por token del vocabulario en cada posición
    puntajes = salida.logits[0, -1]  # puntajes de la última posición
    probabilidades = torch.softmax(puntajes, dim=-1)  # puntajes a probabilidades que suman 1
    mejores = torch.topk(probabilidades, k)  # las k probabilidades más altas
    pares = []  # resultado
    for probabilidad, numero in zip(mejores.values, mejores.indices):  # recorre los k mejores
        texto_token = tokenizador_siguiente.decode([int(numero)])  # texto del token
        pares.append((texto_token, float(probabilidad)))  # guarda el par
    return pares  # se usa en el gráfico y en el Comprobar
```

`dibujar_siguientes` muestra los pares en un gráfico de barras. Un espacio al comienzo de un token es parte del token.

```python
def dibujar_siguientes(contexto, pares):
    """Gráfico de barras con las probabilidades del siguiente token.

    Args:
        contexto: Comienzo de la frase, para el título.
        pares: Lista de (texto del token, probabilidad).
    """
    textos = []  # texto de cada barra
    valores = []  # alto de cada barra
    for texto_token, probabilidad in pares:  # recorre los pares
        textos.insert(0, repr(texto_token))  # al comienzo, así el más probable queda arriba; repr muestra los espacios
        valores.insert(0, probabilidad)  # probabilidad del token, en el mismo orden
    plt.barh(textos, valores)  # una barra por token
    plt.xlabel("probabilidad")  # nombre del eje
    plt.title(contexto + " ...")  # el contexto como título
    plt.show()  # muestra el gráfico
```

Cambie el contexto en la línea `# TODO`. Pruebe a agregar o quitar palabras, por ejemplo el lugar o el material, y vea cómo cambian las probabilidades. Cambie también `K`. Guardamos los pares en `pares`, que usa el **Comprobar**.

```python
contexto = "Después del sismo, los ingenieros revisaron los daños en el"  # TODO: cambie el contexto
K = 5  # cuántos tokens mostrar
pares = siguientes_tokens(contexto, K)  # los K tokens más probables
for texto_token, probabilidad in pares:  # recorre los pares
    print(f"{texto_token!r:15} {probabilidad:.3f}")  # una línea por token
dibujar_siguientes(contexto, pares)  # gráfico de barras
```

*Anote lo que observa.* Ejemplo: el token más probable es ` ed`, el comienzo de ` edificio`. El modelo propone tokens, piezas de palabra, no palabras completas. Las cinco probabilidades suman menos de 0.2, porque el resto se reparte entre los más de 150 mil tokens del vocabulario. Pruebe también un contexto que termine a mitad de palabra, por ejemplo `El sismo de magn`.

### Cada posición predice la siguiente

En el entrenamiento, cada posición de una frase predice su siguiente token, todas a la vez. Lo vemos con una frase completa: para cada posición mostramos el token que sigue en la frase, la probabilidad que el modelo le daba y el token que el modelo creía más probable. Es la misma lectura de probabilidades de arriba, sin escribir nada nuevo.

```python
frase = "El sismo de magnitud 7 dañó varias viviendas de adobe en Arequipa."  # frase completa
entrada = tokenizador_siguiente(frase, return_tensors="pt")  # números de token de la frase
with torch.no_grad():  # solo leemos el modelo, sin gradientes
    salida = modelo_siguiente(**entrada)  # puntajes en todas las posiciones a la vez
probabilidades = torch.softmax(salida.logits[0], dim=-1)  # probabilidades en cada posición
numeros = entrada["input_ids"][0]  # números de token de la frase
aciertos = 0  # posiciones donde el token real era el más probable
for posicion in range(len(numeros) - 1):  # cada posición menos la última
    real = int(numeros[posicion + 1])  # el token que sigue en la frase
    probable = int(torch.argmax(probabilidades[posicion]))  # el token que el modelo creía más probable
    if real == probable:  # el modelo acertó
        aciertos = aciertos + 1  # cuenta el acierto
    texto_actual = tokenizador_siguiente.decode([int(numeros[posicion])])  # token de esta posición
    texto_real = tokenizador_siguiente.decode([real])  # texto del siguiente token real
    texto_probable = tokenizador_siguiente.decode([probable])  # texto del token más probable
    probabilidad_real = float(probabilidades[posicion, real])  # probabilidad del token real
    print(f"{texto_actual!r:12} -> real {texto_real!r:12} {probabilidad_real:.3f} | más probable {texto_probable!r}")  # una línea por posición
print("aciertos:", aciertos, "de", len(numeros) - 1)  # cuántas posiciones acertó
```

Donde la probabilidad del token real es baja, el error de entropía cruzada del entrenamiento es alto. El material (` ad`, de adobe) y el lugar (` Are`, de Arequipa) son difíciles de adivinar. Las piezas que terminan una palabra ya empezada, como `itud` o `quip`, son fáciles.

**Comprobar:**

```python
assert len(pares) == K  # el modelo devolvió K tokens
assert pares[0][1] >= pares[-1][1]  # vienen de más a menos probable
total = 0.0  # suma de las K probabilidades
for texto_token, probabilidad in pares:  # recorre los pares
    total = total + probabilidad  # suma esta probabilidad
assert 0 < total <= 1.0001  # son parte de una distribución que suma 1
print("El decodificador da la probabilidad del siguiente token. OK")
```

<!-- end NOTEBOOK: -->
