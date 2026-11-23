<!-- NOTEBOOK: -->

---

## Parte A: solo codificador

Un transformador solo codificador lee todos los tokens de la frase a la vez, los de antes y los de después de cada palabra. No usa la máscara causal. Se preentrena tapando palabras con `[MASK]` y adivinándolas, como BERT. Por eso encaja en tareas donde hay que entender un texto completo: completar un hueco, clasificar un texto o comparar dos textos.

### Completar una palabra

Los datos son una frase sobre un sismo con una palabra tapada con `[MASK]`. La tarea es la misma con que se preentrenó el modelo: proponer la palabra que falta. Usamos `dccuchile/bert-base-spanish-wwm-cased` (BETO), un BERT entrenado con texto en español. Son unos 440 MB.

```python
MODELO_MASCARA = "dccuchile/bert-base-spanish-wwm-cased"  # nombre del modelo en Hugging Face
inicio = time.time()  # hora antes de la descarga
completar = pipeline("fill-mask", model=MODELO_MASCARA)  # descarga tokenizador y modelo, y los une
print("modelo listo en", round(time.time() - inicio, 1), "segundos")  # tiempo de descarga y carga
```

`completar(frase)` devuelve una lista con las cinco palabras más probables. Cada elemento trae la palabra (`token_str`) y su probabilidad (`score`). La función `mostrar_candidatas` las imprime en orden y las devuelve para el **Comprobar**.

```python
def mostrar_candidatas(frase):
    """Imprime las palabras que el modelo propone para [MASK].

    Args:
        frase: Texto con una sola marca [MASK].

    Returns:
        Lista de diccionarios con la palabra y su probabilidad.
    """
    candidatas = completar(frase)  # cinco propuestas, de más a menos probable
    print(frase)  # la frase de entrada
    for candidata in candidatas:  # recorre las propuestas en orden
        palabra = candidata["token_str"]  # texto de la palabra propuesta
        probabilidad = candidata["score"]  # probabilidad que le da el modelo
        print(f"   {palabra:15} {probabilidad:.3f}")  # una línea por propuesta
    return candidatas  # se usa en el Comprobar
```

Cambie la frase de la línea `# TODO`. Pruebe a mover `[MASK]` a otra palabra, por ejemplo al material de la vivienda o al lugar del sismo. Use una sola marca `[MASK]` por frase.

```python
frase_con_mascara = "El sismo de magnitud 7 dañó varios [MASK] en Arequipa."  # TODO: cambie la frase o mueva [MASK]
candidatas = mostrar_candidatas(frase_con_mascara)  # propuestas del modelo para esta frase
candidatas_material = mostrar_candidatas("Muchas casas construidas con [MASK] colapsaron durante el terremoto.")  # el material de la vivienda
```

*Anote lo que observa.* Ejemplo: en la primera frase el modelo propone edificios, puentes y hospitales, cosas que un sismo puede dañar. En la segunda propone materiales: madera, ladrillos, cemento, piedra y tierra. Usa las palabras de los dos lados de `[MASK]`, porque un codificador ve toda la frase. Las probabilidades son más bajas cuando muchas palabras encajan.

### Clasificar el tono de una noticia

Los datos son titulares cortos sobre sismos. La tarea es clasificar cada titular como positivo, neutral o negativo, por ejemplo para revisar primero las noticias de daños. Usamos `lxyuan/distilbert-base-multilingual-cased-sentiments-student`, un codificador pequeño de la familia BERT, ya ajustado para esta clasificación en varios idiomas. Son unos 540 MB. El modelo responde con las etiquetas en inglés: `positive`, `neutral` y `negative`.

```python
MODELO_TONO = "lxyuan/distilbert-base-multilingual-cased-sentiments-student"  # nombre del modelo en Hugging Face
clasificar = pipeline("text-classification", model=MODELO_TONO)  # descarga tokenizador y modelo, y los une
```

`clasificar(titular)` devuelve una lista con un diccionario: la etiqueta más probable (`label`) y su probabilidad (`score`). Guardamos las etiquetas en `tonos`, que usa el **Comprobar**.

```python
titulares = [  # titulares de ejemplo
    "El puente resistió el sismo sin daños.",  # una buena noticia
    "El sismo derrumbó cientos de viviendas de adobe.",  # una mala noticia
    "Un sismo de magnitud 4,5 se registró frente a la costa de Ica.",  # un dato sin juicio
]
tonos = {}  # etiqueta de cada titular
for titular in titulares:  # recorre los titulares
    resultado = clasificar(titular)[0]  # la etiqueta más probable de este titular
    tonos[titular] = resultado["label"]  # guarda la etiqueta
    print(f"{resultado['label']:9} {resultado['score']:.2f}  {titular}")  # una línea por titular
```

*Observe.* El titular del derrumbe sale `negative` y el del puente `positive`. El titular que solo da un dato sale `negative` con una probabilidad cercana a 0.5: el modelo no está seguro. Un modelo ajustado con titulares de sismos clasificaría mejor ese caso.

### Comparar frases

Los datos son frases cortas de reportes de inspección. La tarea es medir qué tan parecido es el significado de dos frases, aunque usen palabras distintas. Sirve, por ejemplo, para buscar en un archivo de reportes los que hablan de un mismo daño. Usamos `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`, un codificador pequeño entrenado para dar vectores parecidos a frases con el mismo significado. Son unos 470 MB.

Aquí hacemos los pasos a mano. `AutoTokenizer` y `AutoModel` descargan el tokenizador y el modelo. `AutoModel` trae el transformador sin capa de salida: devuelve un vector por token.

```python
MODELO_FRASES = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"  # nombre del modelo en Hugging Face
tokenizador_frases = AutoTokenizer.from_pretrained(MODELO_FRASES)  # descarga el tokenizador
modelo_frases = AutoModel.from_pretrained(MODELO_FRASES)  # descarga el codificador
modelo_frases.eval()  # modo de uso, sin entrenamiento
print("parámetros:", modelo_frases.num_parameters())  # tamaño del modelo
```

`vector_de_frase` convierte una frase en un solo vector. El codificador da un vector por token, y promediamos esos vectores. Luego lo dividimos por su largo, así el producto de dos vectores queda entre -1 y 1. Ese número es el parecido: cerca de 1 si las frases dicen lo mismo y cerca de 0 si no tienen relación.

```python
def vector_de_frase(frase):
    """Vector de una frase, promedio de los vectores de sus tokens.

    Args:
        frase: Texto a convertir.

    Returns:
        Tensor de una dimensión con largo 1.
    """
    entrada = tokenizador_frases(frase, return_tensors="pt")  # números de token de la frase
    with torch.no_grad():  # solo leemos el modelo, sin gradientes
        salida = modelo_frases(**entrada)  # pasa los tokens por el codificador
    vectores = salida.last_hidden_state[0]  # un vector por token
    promedio = vectores.mean(dim=0)  # promedio de los vectores de los tokens
    return promedio / promedio.norm()  # vector de largo 1


def parecido(frase_a, frase_b):
    """Parecido entre el significado de dos frases.

    Args:
        frase_a: Primera frase.
        frase_b: Segunda frase.

    Returns:
        Número entre -1 y 1.
    """
    vector_a = vector_de_frase(frase_a)  # vector de la primera frase
    vector_b = vector_de_frase(frase_b)  # vector de la segunda frase
    return float(vector_a @ vector_b)  # producto de dos vectores de largo 1
```

Comparamos cada frase con todas las demás y guardamos los valores en `matriz`, que dibujamos y usa el **Comprobar**. Agregue una frase suya en la línea `# TODO` y vea con cuál se parece más.

```python
frases = [  # frases de reportes de inspección
    "El sismo derrumbó viviendas de adobe en Arequipa.",  # daño en viviendas
    "Varias casas de adobe colapsaron por el terremoto.",  # el mismo daño, con otras palabras
    "El puente resistió el sismo sin daños.",  # otra estructura, sin daño
    "El precio del cobre subió esta semana.",  # otro tema
    "La columna del colegio presenta grietas diagonales.",  # TODO: cambie esta frase por una suya
]
matriz = []  # una fila de parecidos por frase
for frase_fila in frases:  # recorre las filas
    fila = []  # parecidos de esta frase con todas
    for frase_columna in frases:  # recorre las columnas
        fila.append(parecido(frase_fila, frase_columna))  # parecido de este par
    matriz.append(fila)  # guarda la fila

etiquetas = []  # nombre corto de cada frase para los ejes
for numero in range(len(frases)):  # recorre las frases
    etiquetas.append(f"frase {numero + 1}")  # frase 1, frase 2, ...
plt.imshow(matriz, cmap="Blues", vmin=0, vmax=1)  # cada celda es el parecido de un par
plt.xticks(range(len(frases)), etiquetas, rotation=45)  # nombres de las columnas
plt.yticks(range(len(frases)), etiquetas)  # nombres de las filas
for fila_numero in range(len(frases)):  # recorre las filas
    for columna_numero in range(len(frases)):  # recorre las columnas
        valor = matriz[fila_numero][columna_numero]  # parecido de este par
        plt.text(columna_numero, fila_numero, f"{valor:.2f}", ha="center", va="center")  # escribe el valor
plt.colorbar(label="parecido")  # escala de colores
plt.title("Parecido entre frases")  # título del gráfico
plt.show()  # muestra el gráfico
```

*Anote lo que observa.* Ejemplo: las frases 1 y 2 tienen un parecido de 0.86 aunque solo comparten «adobe», porque dicen lo mismo. La frase del cobre tiene un parecido cercano a 0 con todas. La frase de las grietas se parece más a las frases de viviendas dañadas, alrededor de 0.2, que a la del cobre.

**Comprobar:**

```python
assert len(candidatas) == 5  # el modelo propone cinco palabras
assert candidatas[0]["score"] >= candidatas[-1]["score"]  # vienen de más a menos probable
assert tonos["El sismo derrumbó cientos de viviendas de adobe."] == "negative"  # el derrumbe es una mala noticia
assert matriz[0][1] > matriz[0][3]  # las dos frases de adobe se parecen más que adobe y cobre
print("Los tres usos del codificador funcionan. OK")
```

<!-- end NOTEBOOK: -->
