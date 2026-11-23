<!-- NOTEBOOK: -->

---

## Parte A: solo codificador

Un transformador solo codificador lee todos los tokens de la frase a la vez, los de antes y los de después de cada palabra. No usa la máscara causal. Se preentrena tapando palabras con `[MASK]` y adivinándolas, como BERT. Por eso encaja cuando hay que completar un hueco en un texto completo.

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

**Comprobar:**

```python
assert len(candidatas) == 5  # el modelo propone cinco palabras
assert candidatas[0]["score"] >= candidatas[-1]["score"]  # vienen de más a menos probable
print("El codificador completa la palabra tapada. OK")
```

<!-- end NOTEBOOK: -->
