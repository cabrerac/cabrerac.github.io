<!-- NOTEBOOK: -->

Este cuaderno construye la atención de la sesión desde cero y luego mira cómo un modelo real corta el texto en tokens. Cada bloque describe los datos utilizados, la tarea que se quiere solucionar y por qué el método encaja.

Ejecute las celdas de arriba hacia abajo. En cada **Comprobar**, confirme el mensaje `OK` antes de seguir. Las líneas marcadas con `# TODO` son las que usted escribe. Ya traen una solución para que el cuaderno corra. Bórrela, escriba la suya y vuelva a ejecutar el **Comprobar**.

La parte A corre bien en CPU. Para la parte opcional conviene una GPU: en Colab, Entorno de ejecución, Cambiar tipo de entorno, T4 GPU.

---

## Instalación

Colab ya trae casi todo. Esta celda solo asegura una versión de `transformers` que conoce el modelo de la parte B.

```python
%pip install -q "transformers>=4.56" requests pandas matplotlib
```

## Importaciones

En el siguiente bloque importamos las librerías que usaremos a lo largo del cuaderno.

```python
import math
import time
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
import torch
import torch.nn.functional as F
from torch import nn
from transformers import AutoModel, AutoTokenizer
```

---

<!-- end NOTEBOOK: -->

{% include _snippets/attention-from-scratch.md %}

{% include _snippets/subword-tokens.md %}

{% include _snippets/pretrained-attention.md %}
