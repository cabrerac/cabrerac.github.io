<!-- NOTEBOOK: -->

---

## Parte B: codificador-decodificador

Un transformador codificador-decodificador tiene dos partes. El codificador lee todo el texto de entrada, como en la parte A. El decodificador escribe el texto de salida token por token, con la máscara causal, y en cada paso mira los vectores del codificador. Encaja cuando la entrada y la salida son textos distintos: traducir de un idioma a otro o resumir un texto largo. La salida siempre depende del texto de entrada. En la sesión 5 veremos modelos que escriben texto libre.

### Traducir

Los datos son un reporte corto en español sobre un sismo en el sur del Perú. La tarea es traducirlo al inglés, por ejemplo para compartirlo con un equipo internacional o para usarlo con un modelo que solo lee inglés, como el del resumen que sigue. Usamos `Helsinki-NLP/opus-mt-es-en`, un modelo MarianMT entrenado solo para traducir de español a inglés. Son unos 310 MB.

`AutoModelForSeq2SeqLM` descarga un codificador-decodificador con su capa de salida.

```python
MODELO_TRADUCCION = "Helsinki-NLP/opus-mt-es-en"  # nombre del modelo en Hugging Face
tokenizador_traduccion = AutoTokenizer.from_pretrained(MODELO_TRADUCCION)  # descarga el tokenizador
modelo_traduccion = AutoModelForSeq2SeqLM.from_pretrained(MODELO_TRADUCCION)  # descarga el codificador-decodificador
modelo_traduccion.eval()  # modo de uso, sin entrenamiento
print("parámetros:", modelo_traduccion.num_parameters())  # tamaño del modelo
```

`traducir` sigue los pasos a mano. El tokenizador convierte la frase en números. `generate` pasa esos números por el codificador y luego llama al decodificador una vez por token de salida, hasta que escribe el token de fin o llega a `max_length` tokens. `decode` vuelve a convertir los números de salida en texto.

```python
def traducir(frase):
    """Traduce una frase de español a inglés.

    Args:
        frase: Texto en español.

    Returns:
        Texto en inglés.
    """
    entrada = tokenizador_traduccion(frase, return_tensors="pt")  # números de token de la frase
    with torch.no_grad():  # solo leemos el modelo, sin gradientes
        salida = modelo_traduccion.generate(**entrada, max_length=100)  # codifica y decodifica token por token
    return tokenizador_traduccion.decode(salida[0], skip_special_tokens=True)  # números de salida a texto
```

Traducimos el reporte frase por frase y unimos las traducciones en `reporte_en`, que usa el resumen.

```python
reporte = [  # reporte en español, una frase por elemento
    "Un sismo de magnitud 6,1 sacudió la región de Arequipa, en el sur del Perú, el domingo.",
    "El movimiento dañó decenas de viviendas de adobe y agrietó los muros de un colegio.",
    "Los ingenieros inspeccionaron dos puentes y no encontraron daños estructurales.",
    "Las autoridades no reportaron fallecidos y abrieron albergues para las familias cuyas casas no eran seguras.",
]
traducciones = []  # frases traducidas, en orden
for frase in reporte:  # recorre el reporte
    traduccion = traducir(frase)  # traduce esta frase
    traducciones.append(traduccion)  # la guarda
    print(frase)  # frase original
    print("  ->", traduccion)  # su traducción
reporte_en = " ".join(traducciones)  # el reporte completo en inglés
```

### Resumir

Los datos son el reporte traducido. La tarea es resumirlo en pocas palabras, por ejemplo para un titular o una alerta. Usamos `google-t5/t5-small`, el T5 más pequeño, unos 240 MB. T5 se entrenó con muchas tareas de texto a texto, en inglés, y elige la tarea por el comienzo de la entrada: `summarize:` pide un resumen. Por eso resumimos el reporte en inglés.

```python
MODELO_RESUMEN = "google-t5/t5-small"  # nombre del modelo en Hugging Face
tokenizador_resumen = AutoTokenizer.from_pretrained(MODELO_RESUMEN)  # descarga el tokenizador
modelo_resumen = AutoModelForSeq2SeqLM.from_pretrained(MODELO_RESUMEN)  # descarga el codificador-decodificador
modelo_resumen.eval()  # modo de uso, sin entrenamiento
print("parámetros:", modelo_resumen.num_parameters())  # tamaño del modelo
```

`resumir` hace los mismos pasos que `traducir`. `largo_maximo` es el máximo de tokens del resumen. `num_beams=4` sigue cuatro resúmenes posibles a la vez y se queda con el más probable.

```python
def resumir(texto, largo_maximo):
    """Resume un texto en inglés.

    Args:
        texto: Texto en inglés.
        largo_maximo: Máximo de tokens del resumen.

    Returns:
        El resumen.
    """
    entrada = tokenizador_resumen("summarize: " + texto, return_tensors="pt")  # pide la tarea de resumen
    with torch.no_grad():  # solo leemos el modelo, sin gradientes
        salida = modelo_resumen.generate(**entrada, max_length=largo_maximo, num_beams=4)  # escribe el resumen
    return tokenizador_resumen.decode(salida[0], skip_special_tokens=True)  # números de salida a texto
```

Cambie `LARGO_MAXIMO` en la línea `# TODO`. Pruebe 15 y 30 y compare los resúmenes. Guardamos el resumen en `resumen`, que usa el **Comprobar**.

```python
LARGO_MAXIMO = 60  # TODO: pruebe 15 y 30
resumen = resumir(reporte_en, LARGO_MAXIMO)  # resumen del reporte traducido
print("reporte:", len(reporte_en.split()), "palabras")  # largo del reporte
print("resumen:", len(resumen.split()), "palabras")  # largo del resumen
print(resumen)  # el resumen
```

*Anote lo que observa.* Ejemplo: con 60 tokens el resumen copia tres de las cuatro frases del reporte y deja fuera la primera, la del lugar y la fecha. Con 30 y con 15 se corta a media frase. T5-small resume eligiendo y copiando partes del texto de entrada, no escribe ideas nuevas. También pasa todo a minúsculas.

**Comprobar:**

```python
assert len(traducciones) == len(reporte)  # una traducción por frase
assert "earthquake" in reporte_en.lower()  # la palabra sismo aparece traducida
assert len(resumen.split()) < len(reporte_en.split())  # el resumen es más corto que el reporte
print("El codificador-decodificador traduce y resume. OK")
```

<!-- end NOTEBOOK: -->
