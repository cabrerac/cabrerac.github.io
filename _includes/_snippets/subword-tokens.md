<!-- NOTEBOOK: -->

---

## Parte B: tokens

Un transformador real no lee caracteres. Lee tokens, piezas de palabra de un vocabulario fijo. Usamos el tokenizador de `Qwen/Qwen2.5-0.5B-Instruct`, un modelo abierto pequeño que maneja español. De este modelo solo usamos el tokenizador y, en la parte opcional, sus pesos de atención. No generamos texto.

La tarea es contar los tokens de un texto frente a sus caracteres y sus palabras, y ver dónde se cortan las palabras. Importa porque el largo máximo y el costo de un modelo se miden en tokens, no en palabras.

### El tokenizador

`AutoTokenizer` descarga el tokenizador desde [Hugging Face](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct) la primera vez. Son unos pocos megabytes. Su vocabulario se armó con pares de bytes (BPE): las secuencias frecuentes quedan como una sola pieza y las raras se arman con piezas más cortas.

```python
MODELO_HF = "Qwen/Qwen2.5-0.5B-Instruct"
tokenizador = AutoTokenizer.from_pretrained(MODELO_HF)
print("tamaño del vocabulario:", len(tokenizador))
```

`tokenizador(texto).input_ids` da el número de cada token. `piezas` decodifica cada número por separado para ver el texto de cada pieza. Un espacio inicial dentro de una pieza es parte del token.

```python
def piezas(texto):
    """Texto de cada token, en orden.

    Args:
        texto: Cadena a tokenizar.

    Returns:
        Lista con el texto de cada token.
    """
    return [tokenizador.decode([i]) for i in tokenizador(texto).input_ids]
```

### Contar tokens

Escriba `contar`. Las palabras salen de `texto.split()`, que corta en los espacios.

```python
def contar(texto):
    """Cuenta caracteres, palabras y tokens de un texto.

    Args:
        texto: Cadena a contar.

    Returns:
        Un diccionario con las tres cuentas.
    """
    # TODO: use len, texto.split() y el tokenizador
    return {
        "caracteres": len(texto),
        "palabras": len(texto.split()),
        "tokens": len(tokenizador(texto).input_ids),
    }
```

Primero el párrafo de la parte A. La red de la parte A veía caracteres. Qwen ve muchas menos piezas, porque muchas palabras comunes son un solo token.

```python
print(contar(texto))
print(piezas(texto.split(". ")[0] + "."))
```

### Los lugares del catálogo

La columna `place` del catálogo USGS describe dónde fue cada sismo, por ejemplo `45 km SW of Acarí, Peru`. Descargamos el recorte del Perú de la sesión 1, 2024 y magnitud 4.5 o más, y tokenizamos esa columna.

<!-- end NOTEBOOK: -->

{% include _snippets/usgs-download.md %}

<!-- NOTEBOOK: -->

`PARAMETROS_CURSO` es el mismo recorte de las sesiones anteriores. No lo modifique.

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

download_csv(build_usgs_url(PARAMETROS_CURSO), CATALOGO_PERU)
sismos_peru = pd.read_csv(CATALOGO_PERU)
lugares = sismos_peru["place"].dropna()
print("sismos:", len(sismos_peru), "| lugares:", len(lugares))
print(lugares.head().to_list())
```

Contamos cada lugar y calculamos tokens por palabra. Un valor cercano a 1 quiere decir que casi todas las palabras son un solo token.

```python
conteos = pd.DataFrame([contar(lugar) for lugar in lugares], index=lugares.index)
conteos.insert(0, "place", lugares)
conteos["tokens por palabra"] = conteos["tokens"] / conteos["palabras"]
print(conteos[["caracteres", "palabras", "tokens"]].sum())
print(conteos.sort_values("tokens por palabra", ascending=False).head().round(2).to_string())
```

### Dónde se cortan las palabras

Miramos las piezas de un lugar completo y de algunas palabras sueltas. Dentro de la frase, ` km`, ` of` y ` Peru` son un solo token cada uno, con su espacio delante. Son frecuentes en el texto con que se armó el vocabulario. Los nombres de lugares peruanos no.

```python
for palabra in ["45 km SW of Acarí, Peru", "Acarí", "Chinchaypujio", "45", "2024"]:
    print(f"{palabra!r:28} -> {piezas(palabra)}")
```

`Acarí` se parte en tres piezas, y la `í` queda sola. Qwen escribe cada dígito como un token aparte, así que el modelo no ve el número 45. Ve un 4 seguido de un 5. Pruebe con otros lugares de la tabla o con un texto suyo.

**Comprobar:**

```python
assert len(piezas("Acarí")) > 1
assert piezas("2024") == ["2", "0", "2", "4"]
assert (conteos["tokens"] >= conteos["palabras"]).all()
print("Los tokens parten las palabras raras y los números. OK")
```

<!-- end NOTEBOOK: -->
