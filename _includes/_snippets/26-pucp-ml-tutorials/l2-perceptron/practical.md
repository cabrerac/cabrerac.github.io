<!-- NOTEBOOK: -->

Este cuaderno se organiza en dos secciones:

1. **Parte guiada:** Descargamos el catálogo USGS de **Colombia**, 2024, magnitud 4.5 o más. Construimos tres modelos sobre la calidad de localización: una **regresión lineal**, una **regresión logística** y un **perceptrón**.
2. **Parte individual:** Los estudiantes replican el método sobre el catálogo del **Perú**, 2024, misma magnitud. Comparan activaciones y justifican la elección frente a las líneas base.

En la sesión 1 preguntamos, después de un sismo, qué filas están en condiciones de usarse para una revisión. Hoy damos el siguiente paso: **modelar** esa calidad de localización. La etiqueta que usaremos es la misma idea del umbral de la sesión 1. Una ubicación débil es aquella con `horizontalError > 10` km o `gap > 90` grados.

Ejecute las celdas de arriba hacia abajo. En cada **Comprobar**, confirme el mensaje `OK` antes de seguir.

Si abre este cuaderno en un Colab fresco, las funciones de descarga se definen otra vez aquí. No asuma que la sesión 1 sigue en memoria.

Documentación del servicio: [USGS FDSN event API](https://earthquake.usgs.gov/fdsnws/event/1/).

---

## Continuidad con la sesión 1

Volvemos al mismo catálogo y a las mismas dos columnas que decidían la revisión a escala de distrito. No rehacemos el recorrido Access → Assess → Address: eso ya quedó en la sesión 1. Aquí solo fijamos las decisiones que hoy se convierten en modelos.

**`gap`** se mide en grados (0 a 360). Es el mayor sector del círculo, visto desde el epicentro, sin ninguna estación. Un `gap` pequeño indica cobertura alrededor del sismo. Un `gap` grande indica que casi todas las estaciones estaban del mismo lado.

**`horizontalError`** es el radio, en kilómetros, dentro del cual el epicentro verdadero probablemente se encuentra. Un error de 2 km todavía permite decir "este distrito". Un error de 25 km ya no.

En la sesión 1 usamos esos umbrales para **filtrar** filas. Hoy los usamos para **entrenar** modelos:

- La **recta** responde: dado el `gap`, ¿cuánto error horizontal cabe esperar?
- La **logística** responde: ¿cuál es el riesgo de que esta fila sea una ubicación débil?
- El **perceptrón** responde: ¿de qué lado de una frontera lineal dura cae esta fila?

Los tres modelos hablan el lenguaje de una decisión de ingeniería civil. No reemplazan el cálculo de incertidumbre del USGS. Son líneas base para practicar, con datos reales, la diferencia entre predecir un número, predecir una probabilidad y aprender una frontera de decisión.

La parte guiada usa **Colombia**. La parte individual usa **Perú**. El método es el mismo. Solo cambia la ventana geográfica. `PARAMETROS_CURSO` (Perú) es el contrato con las sesiones siguientes. **No lo modifique.**

---

## Repaso de Python para este cuaderno

Estas celdas cubren lo que usaremos hoy: armar una URL, descargar un CSV, leerlo con pandas y ajustar modelos con scikit-learn y numpy. Si ya lo domina, ejecútelas y siga.

### Importaciones

```python
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
from sklearn.linear_model import LinearRegression, LogisticRegression, Perceptron
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
```

### Una dirección y `requests`

**`requests.get`** pide un archivo por HTTP, igual que lo haría un navegador, pero desde Python. **`raise_for_status`** detiene la celda si el servidor responde con un error (por ejemplo, 404 o 500). Sin esa línea, un fallo del servidor pasaría desapercibido y seguiríamos trabajando con una respuesta vacía.

La celda siguiente pregunta al USGS por la versión de su servicio. Es la consulta más barata posible y sirve para confirmar que hay conexión.

```python
respuesta = requests.get("https://earthquake.usgs.gov/fdsnws/event/1/version", timeout=60)
respuesta.raise_for_status()
print(respuesta.text.strip())
```

### Guardar con `Path` y leer con pandas

**`Path`** representa la ruta de un archivo en esta sesión de Colab. **`read_csv`** convierte un archivo CSV en un `DataFrame`.

Guardamos el CSV en disco antes de leerlo, en vez de pasar el texto directo a pandas. Es un paso extra, pero deja una copia de **exactamente** lo que respondió el servidor. Si mañana el catálogo cambia, esa copia es la única prueba de con qué datos trabajamos hoy.

```python
ejemplo = Path("ejemplo_l2.csv")
ejemplo.write_text("id,valor\nA,1\nB,2\n", encoding="utf-8")
tabla = pd.read_csv(ejemplo)
print(tabla)
assert list(tabla.columns) == ["id", "valor"]
print("Repaso: OK")
```

---

## Parte guiada A — Acceso (Colombia)

**Propósito.** Conseguir el catálogo de Colombia de 2024 y dejarlo en memoria como una tabla, sabiendo qué pedimos y qué dejamos fuera. Este bloque redefine los helpers para un Colab fresco: no depende de que la sesión 1 siga cargada.

### Cómo se construye la URL de descarga

El USGS ofrece dos caminos para obtener los mismos datos.

**Ruta manual (navegador).** Puede abrir el [buscador de sismos](https://earthquake.usgs.gov/earthquakes/search/), llenar el formulario con las fechas, la magnitud mínima y el rectángulo geográfico, y pulsar descargar. Funciona, y es la forma correcta de explorar la primera vez.

El problema aparece cuando necesitamos repetir la consulta: en otra región, en otro año, o dentro de un proceso automático. Un formulario no se puede versionar ni compartir con precisión. Una URL, sí.

**Ruta programática (API).** El mismo servicio acepta la consulta como una dirección web. La base es siempre la misma y los parámetros se agregan después del signo `?`, separados por `&`:

```text
https://earthquake.usgs.gov/fdsnws/event/1/query?format=csv&starttime=2024-01-01&...
```

| Parámetro | Significado | Valor para Colombia |
|-----------|-------------|---------------------|
| `format` | Formato de la respuesta | `csv` |
| `starttime` | Primer instante incluido | `2024-01-01` |
| `endtime` | Límite superior, no incluido | `2025-01-01` |
| `minmagnitude` | Magnitud mínima | `4.5` |
| `minlatitude`, `maxlatitude` | Borde sur y norte del rectángulo | `-4.5`, `13.5` |
| `minlongitude`, `maxlongitude` | Borde oeste y este del rectángulo | `-79.5`, `-66.5` |

Vale la pena detenerse un momento aquí, porque **esa URL es la decisión de acceso**, y es una decisión con consecuencias:

- `minmagnitude=4.5` deja fuera los sismos pequeños. Para una revisión de daños es razonable. Para un estudio de microsismicidad sería un error grave.
- El rectángulo deja fuera el resto del mundo, incluyendo sismos cercanos a la frontera que sí se sintieron en Colombia. Por eso usamos un margen un poco más amplio que el país.
- `endtime=2025-01-01` no incluye ese día. El rango cubre 2024 completo y nada más.

Nadie puede reconstruir nuestro análisis sin esta URL. Guárdela junto con los resultados.

### Paso 1 — Fijar los parámetros del recorte

Escribimos los parámetros como un diccionario y no como una cadena de texto. Así quedan legibles, se pueden revisar uno por uno, y la parte individual podrá reutilizar el mismo mecanismo cambiando solo cuatro valores.

```python
# Ventana de Colombia, con un margen en la frontera.
PARAMETROS_COLOMBIA = {
    "format": "csv",
    "starttime": "2024-01-01",
    "endtime": "2025-01-01",
    "minmagnitude": "4.5",
    "minlatitude": "-4.5",
    "maxlatitude": "13.5",
    "minlongitude": "-79.5",
    "maxlongitude": "-66.5",
}

# Dónde guardaremos la copia local de la respuesta.
CATALOGO_COLOMBIA = Path("usgs_colombia_2024_m45.csv")
```

### Paso 2 — Armar la URL

`build_usgs_url` solo une la base con los parámetros. No descarga nada y no toca la red. Separar el armado de la descarga nos deja imprimir la URL y revisarla **antes** de usarla, que es cuando todavía es barato corregir un error.

```python
def build_usgs_url(parametros: dict) -> str:
    """Arma la URL del catálogo USGS a partir de un diccionario de parámetros."""
    base = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    consulta = "&".join(f"{clave}={valor}" for clave, valor in parametros.items())
    return f"{base}?{consulta}"


USGS_URL_COLOMBIA = build_usgs_url(PARAMETROS_COLOMBIA)
print(USGS_URL_COLOMBIA)
```

Lea la URL que acaba de imprimirse. Debería poder señalar en ella cada decisión de la tabla anterior.

**Comprobar:**

```python
assert USGS_URL_COLOMBIA.startswith("https://earthquake.usgs.gov/fdsnws/event/1/query?")
assert "starttime=2024-01-01" in USGS_URL_COLOMBIA
assert "minmagnitude=4.5" in USGS_URL_COLOMBIA
assert "minlatitude=-4.5" in USGS_URL_COLOMBIA
print("URL de Colombia: OK")
```

### Paso 3 — Descargar el CSV

`download_csv` pide la URL, guarda la respuesta en disco y devuelve su tamaño.

Note la verificación del medio: antes de escribir el archivo comprobamos que el texto empiece con `time,`, que es la primera columna del catálogo. Esto parece exagerado, pero cubre un caso real y silencioso. Cuando una API rechaza una consulta, muchas veces responde con una página de error en HTML **y un código de estado normal**. Sin esa comprobación guardaríamos esa página con extensión `.csv`, pandas fallaría varias celdas más abajo con un mensaje incomprensible, y buscaríamos el problema en el lugar equivocado.

La regla general: **falle temprano y con un mensaje que diga qué revisar.**

```python
def download_csv(url: str, dest: Path, timeout: int = 120) -> int:
    """Descarga url a dest y devuelve el número de bytes.

    Falla si la respuesta no es el CSV del catálogo.
    """
    respuesta = requests.get(url, timeout=timeout)
    respuesta.raise_for_status()  # falla si el servidor respondió 4xx o 5xx
    texto = respuesta.text
    if not texto.startswith("time,"):  # el CSV del catálogo siempre empieza así
        raise ValueError(
            "La respuesta no es el CSV del catálogo. "
            "Revise la URL antes de seguir."
        )
    dest.write_text(texto, encoding="utf-8")
    return dest.stat().st_size


bytes_colombia = download_csv(USGS_URL_COLOMBIA, CATALOGO_COLOMBIA)
print(f"Guardado: {CATALOGO_COLOMBIA}")
print(f"Tamaño: {bytes_colombia / 1e3:.1f} KB")
```

**Comprobar:**

```python
assert CATALOGO_COLOMBIA.is_file()
assert bytes_colombia > 3_000
print("Descarga Colombia: OK")
```

### Paso 4 — Leer la tabla

El acceso termina cuando la tabla está en memoria y sabemos qué columnas trajimos. No cuando el archivo está en disco: un archivo que no hemos abierto todavía no es un dato con el que se pueda trabajar.

```python
sismos_colombia = pd.read_csv(CATALOGO_COLOMBIA)
print("Filas, columnas:", sismos_colombia.shape)
print("Columnas:", list(sismos_colombia.columns))
sismos_colombia.head()
```

Compare la lista de columnas con lo que recuerda de la sesión 1. Hoy nos importan sobre todo `gap`, `horizontalError`, `mag`, `depth` y `latitude`. Si aparece alguna columna que no reconoce, búsquela en el [glosario del USGS](https://earthquake.usgs.gov/data/comcat/) antes de seguir.

**Comprobar:**

```python
columnas_clave = [
    "time", "latitude", "longitude", "depth", "mag", "magType",
    "id", "place", "horizontalError", "gap", "status",
]
faltan = [columna for columna in columnas_clave if columna not in sismos_colombia.columns]
assert not faltan, f"Faltan columnas: {faltan}"
assert len(sismos_colombia) > 20, "El recorte de Colombia vino casi vacío. No cambie los parámetros."
print(f"Tabla Colombia: {len(sismos_colombia)} sismos. OK")
```

---

## Parte guiada B — Regresión lineal (Colombia)

**Propósito.** Entrenar un primer modelo sobre los datos que acabamos de descargar, y ser explícitos sobre lo que ese modelo no cubre. La pregunta es la misma que cerró la sesión 1 en address: **dado el `gap` de un sismo, ¿cuánto error horizontal cabe esperar?**

Es un problema de **regresión**, porque la respuesta es un número y no una categoría. El modelo más simple que puede responderla es una **recta**: una pendiente y un intercepto, dos parámetros que el algoritmo ajusta para que la recta pase lo más cerca posible de los puntos observados.

En ingeniería civil, ese número se lee así: si el hueco angular de estaciones crece, ¿cuántos kilómetros adicionales de incertidumbre horizontal cabe esperar en este recorte? Una pendiente positiva confirma la intuición física (peor cobertura → mayor error). Una pendiente cercana a cero diría que, en este recorte concreto, el `gap` no explica casi nada del error. Ambas lecturas son útiles. Ninguna reemplaza el cálculo de incertidumbre del USGS, que ya está hecho con mucha más información que la que tenemos aquí.

Dos advertencias antes de entrenar, y las dos son parte del resultado:

**Esto no es una herramienta de inspección.** Estamos ajustando una recta para practicar el paso de modelado, no para sustituir el informe operativo del USGS.

**El modelo solo ve las filas completas.** `dropna()` descarta los sismos a los que les falta `gap` o `horizontalError`. Esas filas no desaparecen del problema, solo desaparecen del ajuste. Y no faltan al azar: son típicamente los eventos peor determinados, justo los que más nos preocupaban en la evaluación de la sesión 1. El modelo se entrena, entonces, sobre la parte más fácil del catálogo. Hay que decirlo cuando se presenten los resultados.

### Paso 5 — Elegir las filas

Empaquetamos el filtro en una función. La parte individual reutilizará exactamente la misma regla sobre Perú. Si cada país se filtrara con criterios distintos, cualquier diferencia en la pendiente podría venir del método en vez de los datos.

```python
def filas_para_regresion(tabla: pd.DataFrame) -> pd.DataFrame:
    """Devuelve las filas que tienen gap y horizontalError."""
    return tabla[["gap", "horizontalError"]].dropna()
```

### Paso 6 — Entrenar la recta

`LinearRegression().fit(X, y)` es el **entrenamiento**: el algoritmo recorre los datos y ajusta la pendiente y el intercepto para minimizar el error cuadrático medio, es decir, la suma de las distancias verticales al cuadrado entre cada punto y la recta.

Sobre la forma de los datos: `X` es una matriz de dos dimensiones aunque solo tengamos una variable de entrada, porque scikit-learn siempre espera una fila por observación y una columna por característica. Por eso `usable[["gap"]]` con doble corchete, que devuelve una tabla, en lugar de `usable["gap"]`, que devolvería una sola serie. `y` sí es un vector simple.

```python
def entrenar_error_por_gap(tabla: pd.DataFrame):
    """Ajusta horizontalError como función lineal de gap.

    Returns:
        El modelo entrenado y la tabla usada en el ajuste.
    """
    usable = filas_para_regresion(tabla)
    X = usable[["gap"]].to_numpy()            # una fila por sismo, una columna por variable
    y = usable["horizontalError"].to_numpy()  # el valor que queremos predecir
    modelo = LinearRegression().fit(X, y)
    return modelo, usable


modelo_lineal_co, usable_lineal_co = entrenar_error_por_gap(sismos_colombia)
print("coeficiente (km por grado):", float(modelo_lineal_co.coef_[0]))
print("intercepto:", float(modelo_lineal_co.intercept_))
print(f"filas usadas: {len(usable_lineal_co)} de {len(sismos_colombia)}")
```

Los dos números tienen una lectura concreta:

- El **coeficiente** dice cuántos kilómetros de error adicional corresponden a cada grado más de `gap`. Si es positivo, confirma la intuición física de la sesión 1.
- El **intercepto** es el error que el modelo predice cuando `gap` vale cero, es decir, con cobertura perfecta. Es una extrapolación: probablemente no haya ningún sismo con `gap` cercano a cero en la tabla, así que ese número está fuera del rango de los datos observados.

Fíjese también en cuántas filas se usaron frente al total. Esa diferencia es la que mencionamos en la advertencia anterior: el modelo no vio las filas incompletas.

### Paso 7 — Mirar el ajuste

Nunca acepte un modelo solo por sus coeficientes. Dibújelo.

El gráfico muestra cada sismo como un punto y la recta ajustada encima. Lo que buscamos no es que los puntos caigan exactamente sobre la recta, sino entender **cómo se desvían**: si la dispersión crece con el `gap`, si hay un grupo de puntos muy alejados, o si la relación parece curva en lugar de recta.

```python
fig, ax = plt.subplots(figsize=(6, 4))
ax.scatter(
    usable_lineal_co["gap"],
    usable_lineal_co["horizontalError"],
    alpha=0.4,
    label="filas usadas",
)
linea_x = [usable_lineal_co["gap"].min(), usable_lineal_co["gap"].max()]
linea_y = modelo_lineal_co.predict([[linea_x[0]], [linea_x[1]]])
ax.plot(linea_x, linea_y, color="C1", label="ajuste lineal")
ax.set_xlabel("gap (grados)")
ax.set_ylabel("horizontalError (km)")
ax.set_title("Colombia 2024: error horizontal frente a gap")
ax.legend()
plt.show()
```

Pregúntese, mirando el gráfico: ¿la recta describe bien lo que ve, o hay estructura que se le escapa? Si la respuesta es la segunda, el problema no es el código: es que una recta no es el modelo adecuado. Esa es una conclusión válida y vale la pena escribirla. En este cuaderno la recta sigue siendo nuestra **línea base continua**: el piso contra el que, más adelante, pediremos justificar una activación distinta.

**Comprobar:**

```python
assert len(usable_lineal_co) > 15
assert modelo_lineal_co.coef_.shape == (1,)
print("Regresión lineal Colombia: OK")
```

---

## Parte guiada C — Regresión logística (Colombia)

**Propósito.** Pasar de predecir un **número** (error en km) a predecir un **riesgo**: ¿esta fila es una ubicación demasiado débil para afirmar el distrito?

La regresión lineal del paso anterior responde "cuánto error cabe esperar". En un flujo de revisión post-sismo, muchas veces la pregunta operativa es otra: **¿paso esta fila a revisión de distrito, o la marco como sospechosa?** Esa es una decisión binaria. La regresión logística estima la **probabilidad** de que la fila sea una ubicación débil. Por dentro usa una función sigmoide: comprime una combinación lineal de las entradas a un valor entre 0 y 1.

En el contexto de la revisión, ese número se lee como un **riesgo**: ¿conviene tratar esta fila como sospechosa antes de afirmar el distrito? No es lo mismo que el error en kilómetros. Es una lectura distinta del mismo fenómeno físico (calidad de localización), pensada para una decisión de filtrado.

### La etiqueta: ubicación débil

Usamos exactamente los umbrales de la sesión 1:

- `horizontalError > 10` km
- `gap > 90` grados

La etiqueta es 1 si se cumple **cualquiera** de los dos. Es una decisión nuestra, no una propiedad del catálogo. Si otro equipo usa 15 km y 120 grados obtendrá otro conjunto de positivos. Por eso los umbrales van escritos en el informe, no escondidos en el código.

### Qué entra como características (y qué no)

Aquí hay una trampa fácil de caer, y es la más importante de esta sección.

La etiqueta **se define** con `gap` y `horizontalError`. Si esas mismas columnas entraran también como características, el modelo no estaría prediciendo: estaría **leyendo la respuesta**. Un umbral sobre `gap` o sobre `horizontalError` ya basta para reconstruir la etiqueta. El aprendizaje sería trivial, la exactitud se vería alta sin mérito, y no mediría nada útil sobre el catálogo. En aprendizaje automático eso se llama **fuga de etiqueta** (*label leakage*): la entrada contiene, directa o indirectamente, la definición de la salida.

Por eso `gap` y `horizontalError` quedan **fuera** de las entradas. Solo construyen la etiqueta. Las características son otras columnas que pueden anticipar una localización débil **sin ser** la definición del umbral:

| Característica | Por qué puede importar |
|----------------|------------------------|
| `mag` | Eventos más grandes suelen activar más estaciones, pero no siempre |
| `depth` | La profundidad fija en 10 km y los sismos profundos cambian la geometría aparente |
| `latitude` | En este recorte, la latitud resume en parte la posición relativa a la red |

La línea base de hoy usa solo esas tres. Como ejercicio opcional más adelante puede probar añadir `longitude` y comparar. No es parte del recorrido obligatorio. Tampoco usamos `status` ni `reviewed` en esta sesión: dejar el encoding categórico para más adelante mantiene el modelo pequeño y legible.

### Paso 8 — Construir la tabla de clasificación

Construimos la etiqueta, dejamos solo las filas con las tres características y con `gap` / `horizontalError` completos (sin ellos no hay etiqueta), y miramos el balance de clases antes de entrenar.

```python
FEATURES_CLASIFICACION = ["mag", "depth", "latitude"]


def preparar_clasificacion(tabla: pd.DataFrame) -> pd.DataFrame:
    """Construye la etiqueta de ubicación débil y deja solo filas completas.

    La etiqueta usa gap y horizontalError.
    Las características NO incluyen gap ni horizontalError.
    """
    trabajo = tabla.copy()
    trabajo["ubicacion_debil"] = (
        (trabajo["horizontalError"] > 10) | (trabajo["gap"] > 90)
    ).astype(int)
    columnas = FEATURES_CLASIFICACION + ["ubicacion_debil", "gap", "horizontalError"]
    return trabajo[columnas].dropna()


clasif_colombia = preparar_clasificacion(sismos_colombia)
print("Filas usables:", len(clasif_colombia))
print("Positivos (ubicación débil):", int(clasif_colombia["ubicacion_debil"].sum()))
print("Negativos:", int((clasif_colombia["ubicacion_debil"] == 0).sum()))
clasif_colombia.head()
```

Mire el balance de clases con atención. Si casi todas las filas son del mismo lado, la exactitud de un modelo trivial (siempre predecir la clase mayoritaria) ya es alta. Ese número es la **línea base mayoritaria**. Más abajo lo imprimimos junto a cada exactitud de test.

Un modelo solo aporta algo si **supera** esa línea base. Si apenas la empata, la exactitud alta engaña: el modelo no aprendió nada que no sepa un contador de clases. En ingeniería civil esto es especialmente peligroso, porque un informe que diga "92% de exactitud" suena sólido hasta que alguien pregunta cuál era el piso trivial.

### Paso 9 — Partición train / test

Separar entrenamiento y evaluación es la forma más simple de no autoengañarnos. Entrenamos con una parte de las filas y medimos con otra que el modelo no vio. Fijamos `random_state=42` para que el reparto sea reproducible. Usamos 70% para entrenar y 30% para medir. `stratify` intenta conservar la proporción de positivos y negativos en ambos lados, siempre que haya al menos dos clases.

```python
X_co = clasif_colombia[FEATURES_CLASIFICACION].to_numpy()
y_co = clasif_colombia["ubicacion_debil"].to_numpy()

X_train_co, X_test_co, y_train_co, y_test_co = train_test_split(
    X_co,
    y_co,
    test_size=0.30,
    random_state=42,
    stratify=y_co if len(np.unique(y_co)) > 1 else None,
)

print("train:", X_train_co.shape[0], "test:", X_test_co.shape[0])
print("positivos en train:", int(y_train_co.sum()), "en test:", int(y_test_co.sum()))


def exactitud_mayoria(y_true) -> float:
    """Exactitud de siempre predecir la clase mayoritaria en el conjunto de evaluación."""
    y_true = np.asarray(y_true)
    if len(y_true) == 0:
        return float("nan")
    n_pos = int(y_true.sum())
    n_neg = len(y_true) - n_pos
    return max(n_pos, n_neg) / len(y_true)


baseline_co = exactitud_mayoria(y_test_co)
print("línea base mayoritaria (test):", round(baseline_co, 3))
print("Un modelo útil debe superar ese número. Empatarlo no cuenta como acierto real.")
```

### Paso 10 — Entrenar la logística

`LogisticRegression().fit` ajusta los coeficientes de la combinación lineal que entra a la sigmoide. El resultado no es una recta sobre el error en kilómetros: es una frontera en el espacio de `mag`, `depth` y `latitude` que convierte cada fila en una probabilidad de ubicación débil.

Cuando lea los coeficientes, no los interprete como "kilómetros por unidad". Un coeficiente positivo en `depth`, por ejemplo, dice que (en este ajuste, con las otras variables fijas) mayor profundidad empuja la probabilidad de ubicación débil hacia arriba. La magnitud del coeficiente depende de la escala de cada variable: `mag` y `depth` no están en las mismas unidades, así que no compare coeficientes entre sí como si fueran el mismo tipo de efecto.

```python
modelo_logistico_co = LogisticRegression(max_iter=1000, random_state=42)
modelo_logistico_co.fit(X_train_co, y_train_co)

y_pred_log_co = modelo_logistico_co.predict(X_test_co)
acc_log_co = accuracy_score(y_test_co, y_pred_log_co)
print("línea base mayoritaria (test):", round(baseline_co, 3))
print("exactitud logística (test):", round(acc_log_co, 3))
print("¿supera la línea base?", acc_log_co > baseline_co)
print("coeficientes (mag, depth, latitude):", modelo_logistico_co.coef_[0])
print("intercepto:", float(modelo_logistico_co.intercept_[0]))
```

Compare la exactitud de la logística con la línea base mayoritaria **antes** de celebrar el número. Si la logística apenas empata el piso, el modelo no está aportando una señal útil para filtrar. Si lo supera, todavía conviene preguntarse cuánto: un punto porcentual sobre un piso del 90% no es el mismo logro que cinco puntos sobre un piso del 55%.

**Comprobar:**

```python
assert len(clasif_colombia) > 15
assert set(np.unique(y_co)).issubset({0, 1})
assert 0.0 <= acc_log_co <= 1.0
assert modelo_logistico_co.coef_.shape == (1, len(FEATURES_CLASIFICACION))
print("Regresión logística Colombia: OK")
```

---

## Parte guiada D — Perceptrón (Colombia)

**Propósito.** Aprender la misma etiqueta binaria con un **perceptrón**: el bloque más simple de una red neuronal. A diferencia de la logística, el perceptrón produce una **decisión dura** (0 o 1) a partir de una frontera lineal. No entrega una probabilidad calibrada.

Piénselo así, en el lenguaje de una revisión post-sismo:

- La **logística** responde: "¿qué tan riesgosa es esta fila?" (un número entre 0 y 1).
- El **perceptrón** responde: "¿la paso o la rechazo?" (una decisión binaria).

En un flujo operativo de filtrado rápido, a veces solo se necesita la segunda pregunta. En un informe que debe justificar umbrales ante un revisor, suele hacer falta la primera. Las dos conviven: el perceptrón es el antepasado directo del bloque neuronal; la logística es la versión probabilística de una frontera lineal parecida.

Vamos a implementarlo de dos formas: **desde cero con numpy** (para ver la regla de actualización online) y con **`sklearn.linear_model.Perceptron`** (para contrastar con una implementación de biblioteca). Las exactitudes no tienen por qué coincidir al decimal: no optimizan exactamente la misma función de pérdida ni con el mismo criterio de parada. Lo importante es que **ambos entrenan**, que las asserts confirman el contrato del código, y que ninguna exactitud se lea sin el piso de la clase mayoritaria.

### Paso 11 — Perceptrón desde cero (numpy)

La idea del perceptrón clásico es **online**: mira un ejemplo a la vez y solo actualiza los pesos cuando se equivoca.

1. Calcular la predicción con una combinación lineal y un umbral (signo).
2. Si acierta, no cambia los pesos.
3. Si falla, mueve los pesos hacia el ejemplo mal clasificado.

Esa regla es deliberadamente simple. No minimiza una pérdida suave como la logística. Empuja la frontera hasta que el ejemplo actual queda del lado correcto, y pasa al siguiente. Si los datos no son linealmente separables, el perceptrón puede oscilar: por eso limitamos el número de épocas y no esperamos convergencia perfecta.

Usamos la convención de etiquetas `{0, 1}` convertida a `{-1, +1}` solo dentro del bucle, que es la forma habitual del perceptrón original. Añadimos una columna de unos para el sesgo (bias), de modo que el umbral también se aprende.

```python
def entrenar_perceptron_numpy(
    X: np.ndarray,
    y: np.ndarray,
    n_epochs: int = 20,
    learning_rate: float = 0.1,
    seed: int = 42,
) -> np.ndarray:
    """Entrena un perceptrón online y devuelve el vector de pesos (incluye bias).

    y debe ser 0/1. Internamente se mapea a -1/+1.
    """
    rng = np.random.default_rng(seed)
    # Columna de sesgo: w[0] * 1 + w[1]*x1 + ...
    Xb = np.column_stack([np.ones(len(X)), X])
    pesos = rng.normal(0.0, 0.01, size=Xb.shape[1])
    y_pm = np.where(y == 1, 1, -1)

    for _ in range(n_epochs):
        orden = rng.permutation(len(Xb))
        for i in orden:
            score = float(pesos @ Xb[i])
            pred = 1 if score >= 0.0 else -1
            if pred != y_pm[i]:
                pesos = pesos + learning_rate * y_pm[i] * Xb[i]
    return pesos


def predecir_perceptron_numpy(X: np.ndarray, pesos: np.ndarray) -> np.ndarray:
    """Predice 0/1 con los pesos del perceptrón numpy."""
    Xb = np.column_stack([np.ones(len(X)), X])
    scores = Xb @ pesos
    return (scores >= 0.0).astype(int)


pesos_numpy_co = entrenar_perceptron_numpy(X_train_co, y_train_co)
y_pred_numpy_co = predecir_perceptron_numpy(X_test_co, pesos_numpy_co)
acc_numpy_co = accuracy_score(y_test_co, y_pred_numpy_co)
print("pesos numpy (bias, mag, depth, latitude):", pesos_numpy_co)
print("línea base mayoritaria (test):", round(baseline_co, 3))
print("exactitud perceptrón numpy (test):", round(acc_numpy_co, 3))
print("¿supera la línea base?", acc_numpy_co > baseline_co)
```

Lea los pesos con la misma cautela que los coeficientes de la logística: están en la escala de las variables de entrada, y el sesgo no es un "error en kilómetros". Lo que importa para la decisión operativa es si la exactitud de test supera la línea base mayoritaria, y cómo se compara con la logística del paso anterior.

### Paso 12 — Perceptrón con scikit-learn

`sklearn.linear_model.Perceptron` implementa la misma familia de modelos. Fijamos `random_state` y un número moderado de iteraciones. Por debajo, la biblioteca maneja el sesgo, el criterio de tolerancia y el orden de los ejemplos. Nosotros nos quedamos con la interfaz familiar: `fit` y `predict`.

```python
modelo_perceptron_co = Perceptron(max_iter=1000, random_state=42, tol=1e-3)
modelo_perceptron_co.fit(X_train_co, y_train_co)

y_pred_sk_co = modelo_perceptron_co.predict(X_test_co)
acc_sk_co = accuracy_score(y_test_co, y_pred_sk_co)
print("línea base mayoritaria (test):", round(baseline_co, 3))
print("exactitud perceptrón sklearn (test):", round(acc_sk_co, 3))
print("¿supera la línea base?", acc_sk_co > baseline_co)
print("coeficientes sklearn:", modelo_perceptron_co.coef_[0])
print("intercepto sklearn:", float(modelo_perceptron_co.intercept_[0]))
```

Compare las dos exactitudes del perceptrón con la de la logística y con la línea base mayoritaria. Tres lecturas posibles, todas válidas:

1. **Las tres superan la base.** Hay señal en `mag`, `depth` y `latitude` más allá del contador de clases.
2. **La logística supera a los perceptrones.** La probabilidad suave puede generalizar mejor que la decisión dura en un recorte pequeño o desbalanceado.
3. **Nadie supera la base de forma clara.** Entonces el problema no es "elegir mejor algoritmo": es que estas tres características, en este recorte, no anticipan bien la etiqueta. Esa conclusión también es un resultado.

### Paso 13 — Un vistazo a la decisión

Para visualizar, proyectamos solo dos ejes (`mag` y `depth`) y coloreamos según la etiqueta verdadera. No dibujamos la frontera completa en 3D. El gráfico sirve para recordar que estamos clasificando puntos reales del catálogo, no datos sintéticos generados en el vacío.

```python
fig, ax = plt.subplots(figsize=(6, 4))
debil = clasif_colombia["ubicacion_debil"] == 1
firme = ~debil
ax.scatter(
    clasif_colombia.loc[firme, "mag"],
    clasif_colombia.loc[firme, "depth"],
    alpha=0.5,
    label="ubicación firme",
)
ax.scatter(
    clasif_colombia.loc[debil, "mag"],
    clasif_colombia.loc[debil, "depth"],
    alpha=0.5,
    label="ubicación débil",
)
ax.set_xlabel("mag")
ax.set_ylabel("depth (km)")
ax.set_title("Colombia 2024: etiqueta de ubicación débil")
ax.legend()
plt.show()
```

Si los dos colores se mezclan sin un patrón evidente en este plano, no se sorprenda: la frontera real vive en tres dimensiones (`mag`, `depth`, `latitude`), y además la etiqueta se definió con columnas que **no** están en estos ejes. El gráfico no es una prueba de que el modelo funcione. Es un recordatorio de que el fenómeno es físico y desordenado.

**Comprobar:**

```python
assert pesos_numpy_co.shape == (1 + len(FEATURES_CLASIFICACION),)
assert 0.0 <= acc_numpy_co <= 1.0
assert 0.0 <= acc_sk_co <= 1.0
assert modelo_perceptron_co.coef_.shape == (1, len(FEATURES_CLASIFICACION))
print("Perceptrón Colombia (numpy + sklearn): OK")
```

### Tres modelos, tres lecturas

Antes de pasar a las activaciones y a Perú, fije estas tres frases:

1. **Lineal:** error horizontal esperado dado el `gap` (número continuo).
2. **Logística:** riesgo de ubicación débil (probabilidad entre 0 y 1).
3. **Perceptrón:** frontera lineal dura que acepta o rechaza la fila (decisión 0/1).

Las tres son útiles. Ninguna reemplaza el informe del USGS. Las tres se rompen si las características filtran la etiqueta o si evaluamos sobre el mismo conjunto con el que entrenamos sin decirlo.

---

## Activaciones: de la frontera lineal al bloque neuronal

El perceptrón clásico usa una activación de **umbral** (signo): por encima de cero, 1; por debajo, 0. Las redes modernas cambian esa función. Cuatro nombres que debe reconocer, en el lenguaje de una decisión de sensores y de revisión:

| Activación | Qué hace | Lectura en este contexto |
|------------|----------|--------------------------|
| **Lineal** | Deja pasar la combinación tal cual | Es el modelo de regresión del paso 6. Útil para predecir un error en km |
| **Sigmoide** | Comprime a (0, 1) | Es el corazón de la logística. Útil cuando necesita un riesgo |
| **tanh** | Comprime a (-1, 1), centrada en cero | Similar a la sigmoide, pero simétrica. A veces estabiliza el entrenamiento |
| **ReLU** | `max(0, z)` | Apaga señales negativas. Es la activación por defecto en redes profundas modernas |

Hoy no entrenamos una red profunda. Sí necesitamos que sepa **por qué** elegiría una activación frente a otra cuando el bloque siguiente deje de ser un solo perceptrón. La justificación escrita pesada queda para la parte individual. Aquí solo dejamos un puente corto y una demostración numérica mínima.

```python
z = np.linspace(-4, 4, 9)
print("z      :", np.round(z, 2))
print("lineal :", np.round(z, 2))
print("sigmoide:", np.round(1 / (1 + np.exp(-z)), 3))
print("tanh   :", np.round(np.tanh(z), 3))
print("ReLU   :", np.round(np.maximum(0, z), 2))
```

Observe cómo la sigmoide satura cerca de 0 y 1, cómo `tanh` queda centrada en cero, y cómo ReLU corta todo lo negativo. Esas formas no son decorativas: condicionan qué tipo de señal puede aprender el bloque siguiente.

---

## Parte individual — Perú 2024

**Propósito.** Repetir el método completo por su cuenta, comparar logística frente a perceptrón, y justificar la activación que usaría en un flujo de revisión.

Esta sección es el mismo recorrido de la parte guiada, aplicado a Perú. Las fechas y la magnitud mínima no cambian. Lo único que cambia es la ventana geográfica.

No escriba funciones nuevas de descarga ni de entrenamiento. Reutilice `build_usgs_url`, `download_csv`, `entrenar_error_por_gap`, `preparar_clasificacion`, `entrenar_perceptron_numpy`, `predecir_perceptron_numpy` y `exactitud_mayoria` tal como quedaron. Ese es el punto del ejercicio: un método que solo funciona con los datos para los que se escribió no es un método.

`PARAMETROS_CURSO` es el contrato con las sesiones siguientes, que vuelven a descargar este mismo recorte. **No lo modifique.**

| Constante | Valor |
|-----------|--------|
| Latitud | -18.5 a 0.2 |
| Longitud | -82 a -68 |

Antes de tocar el teclado, recuerde qué espera comparar al final:

- La **pendiente** de la recta `horizontalError ~ gap` frente a la de Colombia.
- El **balance de clases** de la etiqueta de ubicación débil (y por tanto el piso de la línea base mayoritaria).
- Las **exactitudes** de logística y de ambos perceptrones, siempre al lado de ese piso.
- Una **justificación escrita** de activación (sigmoide, tanh, ReLU o lineal) frente a las líneas base de esta sesión.

### Paso 14 — Acceso

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

USGS_URL_PERU = build_usgs_url(PARAMETROS_CURSO)
print(USGS_URL_PERU)
```

```python
bytes_peru = download_csv(USGS_URL_PERU, CATALOGO_PERU)
sismos_peru = pd.read_csv(CATALOGO_PERU)
print("Filas, columnas:", sismos_peru.shape)
sismos_peru.head()
```

Antes de seguir, compare el número de filas con el de Colombia. La diferencia será grande, y no es un error: Perú está sobre el borde de subducción entre la placa de Nazca y la placa Sudamericana, que es una de las zonas sísmicamente más activas del planeta. Buena parte de esa sismicidad ocurre mar adentro, donde las estaciones solo pueden estar de un lado. Eso suele empujar el `gap` hacia arriba y, con él, la proporción de localizaciones débiles.

**Comprobar:**

```python
assert "minlatitude=-18.5" in USGS_URL_PERU
assert CATALOGO_PERU.is_file()
assert len(sismos_peru) > 50, "El recorte del Perú vino casi vacío. Revise la URL."
print(f"Tabla Perú: {len(sismos_peru)} sismos. OK")
```

### Paso 15 — Línea base lineal

Ajuste la misma recta `horizontalError ~ gap` sobre Perú. Imprima el coeficiente al lado del de Colombia y dibuje el ajuste. Las pistas de lectura son las mismas que en la sesión 1:

- **La pendiente.** Si difiere de la de Colombia, pregúntese si se debe a la red de estaciones, a la geografía, o simplemente a que hay muchos más eventos.
- **El rango de `gap`.** Dos rectas ajustadas sobre rangos distintos no son directamente comparables.
- **Las filas usadas frente al total.** El `dropna` vuelve a entrenar sobre la parte más fácil del catálogo.

```python
modelo_lineal_pe, usable_lineal_pe = entrenar_error_por_gap(sismos_peru)
print("coeficiente Perú (km por grado):", float(modelo_lineal_pe.coef_[0]))
print("intercepto Perú:", float(modelo_lineal_pe.intercept_))
print("coeficiente Colombia:", float(modelo_lineal_co.coef_[0]))
print(f"filas usadas Perú: {len(usable_lineal_pe)} de {len(sismos_peru)}")
```

```python
fig, ax = plt.subplots(figsize=(6, 4))
ax.scatter(
    usable_lineal_pe["gap"],
    usable_lineal_pe["horizontalError"],
    alpha=0.4,
    label="filas usadas",
)
linea_x = [usable_lineal_pe["gap"].min(), usable_lineal_pe["gap"].max()]
linea_y = modelo_lineal_pe.predict([[linea_x[0]], [linea_x[1]]])
ax.plot(linea_x, linea_y, color="C1", label="ajuste lineal")
ax.set_xlabel("gap (grados)")
ax.set_ylabel("horizontalError (km)")
ax.set_title("Perú 2024: error horizontal frente a gap")
ax.legend()
plt.show()
```

### Paso 16 — Logística y perceptrón sobre Perú

Use las mismas características (`mag`, `depth`, `latitude`) y la misma etiqueta de ubicación débil. Particione con `random_state=42`. Entrene logística, perceptrón numpy y perceptrón sklearn. Imprima las tres exactitudes de test **junto a la línea base mayoritaria** del conjunto de test. Un modelo útil debe superar ese piso.

No cambie `FEATURES_CLASIFICACION`. Si añade `gap` o `horizontalError` a las entradas, el ejercicio deja de medir lo que pretende: estaría reintroduciendo la fuga de etiqueta que evitamos en la parte guiada.

```python
clasif_peru = preparar_clasificacion(sismos_peru)
X_pe = clasif_peru[FEATURES_CLASIFICACION].to_numpy()
y_pe = clasif_peru["ubicacion_debil"].to_numpy()

X_train_pe, X_test_pe, y_train_pe, y_test_pe = train_test_split(
    X_pe,
    y_pe,
    test_size=0.30,
    random_state=42,
    stratify=y_pe if len(np.unique(y_pe)) > 1 else None,
)

baseline_pe = exactitud_mayoria(y_test_pe)

modelo_logistico_pe = LogisticRegression(max_iter=1000, random_state=42)
modelo_logistico_pe.fit(X_train_pe, y_train_pe)
acc_log_pe = accuracy_score(y_test_pe, modelo_logistico_pe.predict(X_test_pe))

pesos_numpy_pe = entrenar_perceptron_numpy(X_train_pe, y_train_pe)
acc_numpy_pe = accuracy_score(y_test_pe, predecir_perceptron_numpy(X_test_pe, pesos_numpy_pe))

modelo_perceptron_pe = Perceptron(max_iter=1000, random_state=42, tol=1e-3)
modelo_perceptron_pe.fit(X_train_pe, y_train_pe)
acc_sk_pe = accuracy_score(y_test_pe, modelo_perceptron_pe.predict(X_test_pe))

print("Perú — positivos:", int(y_pe.sum()), "de", len(y_pe))
print("Perú — línea base mayoritaria (test):", round(baseline_pe, 3))
print("Perú — exactitud logística:", round(acc_log_pe, 3), "| ¿supera base?", acc_log_pe > baseline_pe)
print("Perú — exactitud perceptrón numpy:", round(acc_numpy_pe, 3), "| ¿supera base?", acc_numpy_pe > baseline_pe)
print("Perú — exactitud perceptrón sklearn:", round(acc_sk_pe, 3), "| ¿supera base?", acc_sk_pe > baseline_pe)
print(
    "Colombia (para comparar) — base:", round(baseline_co, 3),
    "logística:", round(acc_log_co, 3),
    "numpy:", round(acc_numpy_co, 3),
    "sklearn:", round(acc_sk_co, 3),
)
print("coeficientes logística Perú (mag, depth, latitude):", modelo_logistico_pe.coef_[0])
```

Al leer estos números, compare tres cosas, no solo la exactitud más alta:

1. **El piso.** Si en Perú la línea base mayoritaria es mucho más alta o más baja que en Colombia, el "mismo" 85% de exactitud no significa lo mismo.
2. **Quién supera el piso.** Un perceptrón que empata la base no filtra mejor que "siempre predecir la clase mayoritaria".
3. **La diferencia logística vs perceptrón.** Si necesita un riesgo para el informe, la logística habla ese lenguaje. Si necesita un filtro duro y rápido, el perceptrón habla el otro.

**Comprobar:**

```python
assert len(usable_lineal_pe) > 20
assert len(clasif_peru) > 20
assert 0.0 <= acc_log_pe <= 1.0
assert 0.0 <= acc_numpy_pe <= 1.0
assert 0.0 <= acc_sk_pe <= 1.0
print("Replay Perú (lineal + logística + perceptrón): OK")
print("URL del curso (guárdela):", USGS_URL_PERU)
```

### Paso 17 — Comparar y justificar

Complete en sus palabras. No basta con pegar los números: diga qué cambió al pasar de Colombia a Perú, qué modelo preferiría para filtrar ubicaciones débiles en este recorte, y qué activación usaría en el bloque siguiente frente a las líneas base lineal y logística de esta sesión.

```python
diagnostico_activacion = """
Que cambio al pasar de Colombia a Peru (balance de clases, pendiente lineal, exactitudes):
Que modelo prefiero para filtrar ubicaciones debiles en Peru (logistica o perceptron) y por que:
Que activacion usaria en el bloque siguiente y frente a que linea base (lineal o logistica):
"""
print(diagnostico_activacion)
```

---

## Ticket de salida

Escriba **exactamente dos oraciones**. En la primera, diga qué activación elegiría para un flujo de revisión post-sismo. En la segunda, diga por qué esa elección es mejor (o peor) que quedarse solo con la línea base lineal o logística de esta sesión.

```python
ticket_de_salida = """
Oracion 1:
Oracion 2:
"""
print(ticket_de_salida)
```

<!-- end NOTEBOOK: -->
