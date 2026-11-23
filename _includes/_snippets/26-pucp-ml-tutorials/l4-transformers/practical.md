<!-- NOTEBOOK: -->

Este cuaderno usa transformadores ya entrenados, uno de cada familia vista en la sesión: solo codificador, codificador-decodificador y solo decodificador. No programamos ni entrenamos la arquitectura. Descargamos modelos de [Hugging Face](https://huggingface.co/models) con la librería `transformers` y los usamos con textos sobre sismos y daños en edificaciones. Cada bloque describe los datos utilizados, la tarea que se quiere solucionar y por qué esa familia encaja.

Ejecute las celdas de arriba hacia abajo. En cada **Comprobar**, confirme el mensaje `OK` antes de seguir. Cada parte tiene una línea marcada con `# TODO`, donde usted cambia una frase o un parámetro. Ya trae un ejemplo para que el cuaderno corra. Cámbielo, vuelva a ejecutar la celda y anote lo que observa en la celda de texto que sigue.

Todo el cuaderno corre en CPU, no hace falta GPU. La primera vez, cada modelo se descarga desde Hugging Face. Son seis modelos, entre 250 MB y 1 GB cada uno, unos 3 GB en total. En Colab la descarga tarda pocos minutos. Si Colab muestra un aviso sobre `HF_TOKEN`, puede ignorarlo: los modelos de este cuaderno son públicos y no piden cuenta.

---

## Instalación

Colab ya trae `transformers` y `torch`. Esta celda asegura una versión reciente de `transformers` y agrega `sentencepiece` y `sacremoses`, que usa el tokenizador del modelo de traducción.

```python
%pip install -q "transformers>=4.56" sentencepiece sacremoses
```

## Importaciones

En el siguiente bloque importamos las librerías que usaremos a lo largo del cuaderno.

```python
import time  # mide cuánto tarda cada descarga

import matplotlib.pyplot as plt  # dibuja la matriz de parecido y las probabilidades
import torch  # tensores y cálculo sin gradientes
from transformers import AutoModel  # transformador sin capa de salida, para vectores
from transformers import AutoModelForCausalLM  # transformador solo decodificador con su capa de salida
from transformers import AutoModelForSeq2SeqLM  # transformador codificador-decodificador
from transformers import AutoTokenizer  # tokenizador que acompaña a cada modelo
from transformers import pipeline  # atajo que une tokenizador, modelo y lectura de la salida
```

## Cómo se usa un modelo de Hugging Face

[Hugging Face](https://huggingface.co/models) es un repositorio público de modelos. Cada modelo tiene un nombre, por ejemplo `dccuchile/bert-base-spanish-wwm-cased`, y una ficha que explica con qué datos se entrenó y para qué sirve. Los pasos son siempre los mismos:

1. Buscar un modelo en [huggingface.co/models](https://huggingface.co/models). A la izquierda se puede filtrar por tarea, por ejemplo *Fill-Mask* o *Translation*, y por idioma.
2. Copiar su nombre y leer la ficha: la familia, el idioma y la tarea con que se entrenó.
3. Descargar el tokenizador y el modelo con `from_pretrained(nombre)`. La descarga queda guardada, y la segunda vez se carga desde el disco.
4. Pasar el texto por el tokenizador, que lo convierte en números de token.
5. Pasar esos números por el modelo y leer su salida.

`pipeline(tarea, model=nombre)` hace los pasos 3 a 5 de una sola vez para tareas comunes. Lo usamos en las dos primeras tareas. En el resto hacemos los pasos a mano para ver qué entra y qué sale del modelo.

<!-- end NOTEBOOK: -->

{% include _snippets/pretrained-encoder-usage.md %}

{% include _snippets/pretrained-encoder-decoder-usage.md %}

{% include _snippets/pretrained-decoder-next-token.md %}

<!-- NOTEBOOK: -->

---

## Resumen

| Familia | Modelo | Qué ve | Tareas de este cuaderno |
|---|---|---|---|
| Solo codificador | BETO, DistilBERT multilingüe, MiniLM multilingüe | Todos los tokens de la frase | Completar una palabra, clasificar el tono, comparar frases |
| Codificador-decodificador | MarianMT, T5 | El codificador ve toda la entrada y el decodificador los tokens ya escritos | Traducir y resumir |
| Solo decodificador | Qwen2.5-0.5B | Los tokens anteriores, con la máscara causal | Probabilidad del siguiente token |

En la sesión 5 usaremos modelos solo decodificador mucho más grandes, los modelos de lenguaje grandes, para que escriban texto.

<!-- end NOTEBOOK: -->
