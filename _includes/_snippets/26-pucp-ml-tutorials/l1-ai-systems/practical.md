<!-- NOTEBOOK: -->

Este cuaderno se organiza en dos secciones:

1. **Seccion guiada:** Descargamos el catálogo USGS de **Colombia**, 2024, para sismos de magnitud 4.5 o más. Recorremos las diferentes etapas de la metodología de ciencia de datos **acceso**, **evaluación** y **address**.
2. **Sección individual:** Los estudiantes replicarán el mismo método sobre el catálogo del **Perú**, 2024, misma magnitud. Reutilicen las funciones de la parte guiada.

En esta oportunidad nos interesa determinar después de un sismo, ¿qué filas están en condiciones de usarse para una revisión (dónde fue, qué tan grande, qué tan segura es la localización)?

Ejecute las celdas de arriba hacia abajo. En cada **Comprobar**, confirme el mensaje `OK` antes de seguir.

Las sesiones siguientes vuelven a descargar el recorte del **Perú**. No cambie esos parámetros.

Documentación del servicio: [USGS FDSN event API](https://earthquake.usgs.gov/fdsnws/event/1/).

---

## El catálogo sísmico del USGS

Antes de escribir una sola línea de código conviene saber qué estamos a punto de descargar. Esta es la diferencia entre usar un archivo y entenderlo, y es justamente el hábito que la etapa de **acceso** quiere instalar.

El **United States Geological Survey (USGS)** mantiene un catálogo mundial de sismos. Cada fila del catálogo no es una medición directa: es el **resultado de un procesamiento**. Una red de estaciones sismológicas registra el movimiento del suelo, un algoritmo identifica el momento en que llegaron las ondas a cada estación, y a partir de esos tiempos de llegada se estima dónde ocurrió el sismo, a qué profundidad y con qué tamaño. Un analista puede revisar esa estimación después y corregirla.

Esto tiene dos consecuencias que vamos a encontrar más adelante en el cuaderno:

- **Cada número viene con una incertidumbre.** La posición no es un punto exacto, es un punto con un radio de error. El catálogo publica ese radio en columnas separadas.
- **La calidad depende de dónde ocurrió el sismo.** Si las estaciones que lo registraron rodean al epicentro, la localización es firme. Si todas las estaciones están del mismo lado (por ejemplo, un sismo mar adentro registrado solo desde el continente), la localización es mucho más débil. El catálogo también publica un indicador de esto.

Un catálogo así es una **fuente secundaria**: nosotros no decidimos qué estaciones instalar, ni qué algoritmo usar, ni qué umbral de detección aplicar. Heredamos todas esas decisiones. Parte del trabajo de evaluación consiste en hacerlas visibles.

Documentación oficial, para ir más allá de este cuaderno:

- [FDSN event API](https://earthquake.usgs.gov/fdsnws/event/1/) — todos los parámetros de consulta disponibles.
- [Buscador de sismos](https://earthquake.usgs.gov/earthquakes/search/) — la misma consulta, pero con un formulario web.
- [Glosario de términos del catálogo](https://earthquake.usgs.gov/data/comcat/) — definición formal de cada columna.

### Qué significa cada columna

El CSV trae más de veinte columnas. Estas son las que usaremos hoy:

| Columna | Significado | Por qué nos importa |
|---------|-------------|---------------------|
| `time` | Fecha y hora del sismo (UTC) | Ubica el evento en el tiempo |
| `latitude`, `longitude` | Epicentro estimado, en grados | Responde "dónde fue" |
| `depth` | Profundidad estimada, en kilómetros | Un sismo superficial sacude más que uno profundo de igual magnitud |
| `mag` | Magnitud estimada | Responde "qué tan grande fue" |
| `magType` | Escala con la que se calculó `mag` | Dos escalas distintas no son el mismo número |
| `gap` | Mayor hueco angular, en grados, entre estaciones vistas desde el epicentro | Mide si las estaciones rodearon al sismo o no |
| `horizontalError` | Incertidumbre horizontal de la localización, en kilómetros | Dice cuánto puede moverse el epicentro |
| `depthError` | Incertidumbre de la profundidad, en kilómetros | Lo mismo, en vertical |
| `id` | Identificador único del evento | Permite detectar filas repetidas |
| `place` | Descripción textual de la ubicación | Útil para leer, no para calcular |
| `status` | `reviewed` si un analista lo revisó, `automatic` si no | Separa lo verificado de lo preliminar |

Dos columnas merecen una explicación más larga porque las vamos a usar para construir el modelo.

**`gap`** se mide en grados y va de 0 a 360. Imagine que se para en el epicentro y mira hacia cada estación que registró el sismo. El `gap` es el mayor sector del círculo en el que **no** hay ninguna estación. Un `gap` de 30 grados significa que las estaciones rodeaban bastante bien al sismo. Un `gap` de 250 grados significa que casi todas estaban del mismo lado, y la localización se apoya en mucha menos información.

**`horizontalError`** es el radio, en kilómetros, dentro del cual el epicentro verdadero probablemente se encuentra. Un error de 2 km todavía permite decir "este distrito". Un error de 25 km ya no.

Cabe esperar que estas dos columnas estén relacionadas: peor cobertura de estaciones debería producir mayor incertidumbre. **Esa relación es exactamente la que vamos a modelar al final de la parte guiada.**

### Por qué Colombia primero y Perú después

Trabajamos con dos recortes del mismo catálogo. La parte guiada usa **Colombia** y la hacemos juntos, paso a paso. La parte individual usa **Perú** y la hace cada estudiante.

No son dos ejercicios distintos: son **el mismo método aplicado dos veces**. Esa es la idea. Cuando el método es el mismo y solo cambia la ventana geográfica, cualquier diferencia en los resultados viene de los datos, no del procedimiento. Y es ahí donde empieza el análisis interesante: Perú tiene una red sismológica distinta, una geología distinta y mucha más actividad mar adentro que Colombia. Si el ajuste cambia, hay una razón física detrás.

El recorte del Perú, además, es el que reutilizaremos en las sesiones 2 a 5. Por eso sus parámetros están fijos.

---

## Repaso de Python para este cuaderno

Estas celdas cubren solo lo que usaremos hoy: armar una URL, descargar un CSV y leerlo con pandas. Si ya lo domina, ejecútelas y siga.

### Una dirección y `requests`

**`requests.get`** pide un archivo por HTTP, igual que lo haría un navegador, pero desde Python. **`raise_for_status`** detiene la celda si el servidor responde con un error (por ejemplo, 404 o 500). Sin esa línea, un fallo del servidor pasaría desapercibido y seguiríamos trabajando con una respuesta vacía.

La celda siguiente pregunta al USGS por la versión de su servicio. Es la consulta más barata posible y sirve para confirmar que hay conexión.

```python
import requests

respuesta = requests.get("https://earthquake.usgs.gov/fdsnws/event/1/version", timeout=60)
respuesta.raise_for_status()
print(respuesta.text.strip())
```

### Guardar con `Path` y leer con pandas

**`Path`** representa la ruta de un archivo en esta sesión de Colab. **`read_csv`** convierte un archivo CSV en un `DataFrame`, que es la tabla con la que trabaja pandas.

Guardamos el CSV en disco antes de leerlo, en vez de pasar el texto directo a pandas. Es un paso extra, pero deja una copia de **exactamente** lo que respondió el servidor. Si mañana el catálogo cambia, esa copia es la única prueba de con qué datos trabajamos hoy.

```python
from pathlib import Path
import pandas as pd

ejemplo = Path("ejemplo.csv")
ejemplo.write_text("id,valor\nA,1\nB,2\n", encoding="utf-8")
tabla = pd.read_csv(ejemplo)
print(tabla)
assert list(tabla.columns) == ["id", "valor"]
print("Repaso: OK")
```

---

## Parte guiada A — Acceso (Colombia)

**Propósito.** Conseguir el catálogo de Colombia de 2024 y dejarlo en memoria como una tabla, sabiendo qué pedimos y qué dejamos fuera.

### Cómo se construye la URL de descarga

El USGS ofrece dos caminos para obtener los mismos datos.

**Ruta manual (navegador).** Puede abrir el [buscador de sismos](https://earthquake.usgs.gov/earthquakes/search/), llenar el formulario con las fechas, la magnitud mínima y el rectángulo geográfico, y pulsar descargar. Funciona, y es la forma correcta de explorar la primera vez.

El problema aparece cuando necesitamos repetir la consulta: en otra región, en otro año, o dentro de un proceso automático que corre cada semana. Un formulario no se puede versionar ni compartir con precisión. Una URL, sí.

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

Compare la lista de columnas con la tabla del diccionario de datos más arriba. Si aparece alguna columna que no reconoce, búsquela en el [glosario del USGS](https://earthquake.usgs.gov/data/comcat/) antes de seguir.

**Comprobar:**

```python
columnas_clave = ["time", "latitude", "longitude", "depth", "mag", "magType", "id", "place", "horizontalError", "gap", "status"]
faltan = [columna for columna in columnas_clave if columna not in sismos_colombia.columns]
assert not faltan, f"Faltan columnas: {faltan}"
assert len(sismos_colombia) > 20, "El recorte de Colombia vino casi vacío. No cambie los parámetros."
print(f"Tabla Colombia: {len(sismos_colombia)} sismos. OK")
```

---

## Parte guiada B — Evaluación (Colombia)

**Propósito.** Decidir si esta tabla sirve para la pregunta que nos hicimos, y dejar escrito qué riesgos quedan.

La evaluación responde a una decisión concreta, no a un puntaje genérico de calidad. Nuestra decisión es: después de un sismo, ¿qué filas están en condiciones de usarse para una revisión? Una fila sirve si sabemos **dónde** fue, **con qué magnitud**, y **con qué incertidumbre**.

Note que este criterio depende del uso. Las mismas filas que descartaremos aquí podrían ser perfectamente válidas para un estudio estadístico regional, donde un error de 30 km no cambia la conclusión. **Fitness for purpose**: la calidad no es una propiedad del dato, es una relación entre el dato y la pregunta.

Vamos a revisar cuatro cosas, en orden.

### Paso 5 — Completitud y unicidad

Empezamos por lo más básico: ¿faltan celdas?, ¿hay eventos repetidos?

```python
faltantes = sismos_colombia.isna().sum().sort_values(ascending=False)
print("Valores faltantes por columna:")
print(faltantes[faltantes > 0])
if faltantes.sum() == 0:
    print("Ninguna celda vacía en este recorte.")

duplicados = int(sismos_colombia["id"].duplicated().sum())
print("Ids duplicados:", duplicados)
```

Es probable que vea pocas celdas vacías y ningún duplicado. **No concluya que el catálogo está limpio.**

Lo que está viendo es consecuencia de nuestra propia decisión de acceso. El filtro de magnitud 4.5 ya dejó fuera los sismos pequeños, que son precisamente los peor determinados: los que menos estaciones registraron y para los que el USGS muchas veces no puede estimar incertidumbres. Nuestro recorte se quedó con los eventos más grandes, que son los mejor caracterizados.

Dicho de otra forma: **filtrar mejora las métricas de calidad sin mejorar los datos.** Es un efecto que conviene reconocer, porque es fácil presentarlo como un logro.

Los problemas que sí tiene esta tabla no se ven contando celdas vacías. Hay que ir a buscarlos.

### Paso 6 — Profundidad fija en 10 km

Cuando el USGS no puede estimar la profundidad de un sismo a partir de los datos disponibles, no deja la celda vacía: **fija el valor en 10 km** y sigue adelante. Es una convención del catálogo, documentada, y razonable desde el punto de vista del procesamiento.

Para nosotros es una trampa. Ese 10 no es una medición, es un marcador de "no sé", pero tiene la misma apariencia que cualquier otro número de la columna. Si calculamos la profundidad promedio sin saber esto, el resultado está contaminado por valores que nunca se midieron.

Este es un ejemplo de **validez**: el valor obedece el formato declarado (es un número de kilómetros) pero no significa lo que el formato promete.

```python
profundidad_fija = sismos_colombia["depth"].round(3).eq(10)
print(f"Profundidad exactamente 10 km: {int(profundidad_fija.sum())} de {len(sismos_colombia)}")
sismos_colombia.loc[profundidad_fija, ["time", "place", "mag", "depth", "depthError"]].head()
```

Mire la columna `depthError` en esas filas. Suele ser alta o estar vacía, que es la pista que confirma la interpretación.

### Paso 7 — Las escalas de magnitud no son intercambiables

La columna `mag` parece una sola variable. No lo es. La columna `magType` dice con qué método se calculó cada valor, y los métodos no son equivalentes.

```python
print(sismos_colombia["magType"].value_counts(dropna=False))
```

Las más comunes en este catálogo:

- **`mww`** — magnitud de momento, calculada con la fase W. Es la más robusta para sismos grandes.
- **`mb`** — magnitud de ondas de cuerpo. Tiende a saturarse: para sismos grandes subestima el tamaño real.
- **`mwr`** — magnitud de momento regional, a partir de estaciones cercanas.
- **`ml`** — magnitud local, la escala original de Richter, pensada para distancias cortas.

Un `mb` de 5.0 y un `mww` de 5.0 **no describen el mismo sismo**. Ordenar la tabla por `mag` mezcla escalas y produce un ranking que no significa lo que parece.

Este es un problema de **consistencia**: los valores están correctos cada uno en su propio marco, pero el marco cambia entre filas y la columna no lo advierte.

### Paso 8 — Qué tan firme es la localización

Llegamos a lo que de verdad decide nuestra pregunta. Queremos poder afirmar "el sismo ocurrió en este distrito". Para eso necesitamos que el error horizontal sea pequeño y que las estaciones hayan rodeado al epicentro.

Usamos dos umbrales:

- **`horizontalError > 10` km.** Por encima de eso, el epicentro puede caer en un distrito vecino y la afirmación deja de sostenerse.
- **`gap > 90` grados.** Un cuarto del círculo sin estaciones ya es una cobertura pobre. Es un criterio de uso frecuente en sismología operativa.

Ambos umbrales son decisiones nuestras, no propiedades del catálogo. Si otro equipo usa 15 km y 120 grados obtendrá otro conjunto de filas válidas. Por eso los umbrales van escritos en el informe, no escondidos en el código.

```python
incertidumbre = (sismos_colombia["horizontalError"] > 10) | (sismos_colombia["gap"] > 90)
print(f"Localización débil para un distrito: {int(incertidumbre.sum())} de {len(sismos_colombia)}")
(
    sismos_colombia.loc[incertidumbre, ["place", "mag", "horizontalError", "gap"]]
    .sort_values("horizontalError", ascending=False)
    .head(8)
)
```

Lea la columna `place` de las filas que salieron. Muchas dirán algo como *"off the coast"*. No es casualidad: un sismo mar adentro solo puede ser registrado desde tierra, así que todas las estaciones quedan del mismo lado y el `gap` se dispara. **El patrón de errores tiene una explicación física**, y encontrarla es parte de la evaluación.

### Paso 9 — Un resumen reutilizable

Hasta aquí revisamos Colombia a mano. La parte individual tiene que hacer lo mismo con Perú, y comparar los dos resultados.

Para que la comparación tenga sentido, las dos tablas deben medirse **con los mismos criterios**. Si Perú se evalúa con umbrales distintos, cualquier diferencia que encontremos podría venir del método en vez de los datos.

Por eso empaquetamos los cuatro chequeos en una función. Es la misma idea de reproducibilidad que vimos con la URL: lo que está escrito como código se puede repetir sin ambigüedad.

```python
def resumen_calidad(tabla: pd.DataFrame) -> dict:
    """Cuenta filas, duplicados, profundidades fijas y localizaciones débiles."""
    return {
        "filas": int(len(tabla)),
        "ids_duplicados": int(tabla["id"].duplicated().sum()),
        "celdas_vacias": int(tabla.isna().sum().sum()),
        "profundidad_10km": int(tabla["depth"].round(3).eq(10).sum()),
        "localizacion_debil": int(((tabla["horizontalError"] > 10) | (tabla["gap"] > 90)).sum()),
        "tipos_magnitud": int(tabla["magType"].nunique()),
    }


resumen_colombia = resumen_calidad(sismos_colombia)
print(resumen_colombia)
```

**Comprobar:**

```python
assert resumen_colombia["filas"] == len(sismos_colombia)
assert resumen_colombia["ids_duplicados"] == 0
assert resumen_colombia["profundidad_10km"] > 0, "Se esperaba al menos una profundidad fija en 10 km."
assert resumen_colombia["tipos_magnitud"] > 1
print("Evaluación Colombia: OK")
```

---

## Parte guiada C — Address (Colombia)

**Propósito.** Entrenar un primer modelo sobre los datos que acabamos de evaluar, y ser explícitos sobre lo que ese modelo no cubre.

### Paso 10 — Elegir la pregunta y las filas

En el paso 8 observamos algo: los sismos con `gap` alto tendían a tener `horizontalError` alto. Tiene sentido físico, porque las dos cosas miden consecuencias de la misma causa, que es la geometría de la red de estaciones.

Convirtamos esa observación en una pregunta que un modelo pueda responder: **dado el `gap` de un sismo, ¿cuánto error horizontal cabe esperar?**

Es un problema de **regresión**, porque la respuesta es un número y no una categoría. Y el modelo más simple que puede responderla es una **recta**: una pendiente y un intercepto, dos parámetros que el algoritmo ajusta para que la recta pase lo más cerca posible de los puntos observados.

Dos advertencias antes de entrenar, y las dos son parte del resultado:

**Esto no es una herramienta de inspección.** Estamos ajustando una recta para practicar el paso de address, no para reemplazar el cálculo de incertidumbre del USGS, que ya está hecho con mucha más información que la que tenemos aquí.

**El modelo solo ve las filas completas.** `dropna()` descarta los sismos a los que les falta `gap` o `horizontalError`. Esas filas no desaparecen del problema, solo desaparecen del ajuste. Y no faltan al azar: son típicamente los eventos peor determinados, justo los que más nos preocupaban en la evaluación. El modelo se entrena, entonces, sobre la parte más fácil del catálogo. Hay que decirlo cuando se presenten los resultados.

```python
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt


def filas_para_modelo(tabla: pd.DataFrame) -> pd.DataFrame:
    """Devuelve las filas que tienen gap y horizontalError."""
    return tabla[["gap", "horizontalError"]].dropna()
```

### Paso 11 — Entrenar el modelo

`LinearRegression().fit(X, y)` es el **entrenamiento**: el algoritmo recorre los datos y ajusta la pendiente y el intercepto para minimizar el error cuadrático medio, es decir, la suma de las distancias verticales al cuadrado entre cada punto y la recta.

Sobre la forma de los datos: `X` es una matriz de dos dimensiones aunque solo tengamos una variable de entrada, porque scikit-learn siempre espera una fila por observación y una columna por característica. Por eso `usable[["gap"]]` con doble corchete, que devuelve una tabla, en lugar de `usable["gap"]`, que devolvería una sola serie. `y` sí es un vector simple.

```python
def entrenar_error_por_gap(tabla: pd.DataFrame):
    """Ajusta horizontalError como función lineal de gap.

    Returns:
        El modelo entrenado y la tabla usada en el ajuste.
    """
    usable = filas_para_modelo(tabla)
    X = usable[["gap"]].to_numpy()          # una fila por sismo, una columna por variable
    y = usable["horizontalError"].to_numpy()  # el valor que queremos predecir
    modelo = LinearRegression().fit(X, y)
    return modelo, usable


modelo_colombia, usable_colombia = entrenar_error_por_gap(sismos_colombia)
print("coeficiente (km por grado):", float(modelo_colombia.coef_[0]))
print("intercepto:", float(modelo_colombia.intercept_))
print(f"filas usadas: {len(usable_colombia)} de {len(sismos_colombia)}")
```

Los dos números tienen una lectura concreta:

- El **coeficiente** dice cuántos kilómetros de error adicional corresponden a cada grado más de `gap`. Si es positivo, confirma la intuición del paso 8.
- El **intercepto** es el error que el modelo predice cuando `gap` vale cero, es decir, con cobertura perfecta. Es una extrapolación: probablemente no haya ningún sismo con `gap` cercano a cero en la tabla, así que ese número está fuera del rango de los datos observados.

Fíjese también en cuántas filas se usaron frente al total. Esa diferencia es la que mencionamos en el paso anterior.

### Paso 12 — Mirar el ajuste

Nunca acepte un modelo solo por sus coeficientes. Dibújelo.

El gráfico muestra cada sismo como un punto y la recta ajustada encima. Lo que buscamos no es que los puntos caigan exactamente sobre la recta, sino entender **cómo se desvían**: si la dispersión crece con el `gap`, si hay un grupo de puntos muy alejados, o si la relación parece curva en lugar de recta.

```python
fig, ax = plt.subplots(figsize=(6, 4))
ax.scatter(usable_colombia["gap"], usable_colombia["horizontalError"], alpha=0.4, label="filas usadas")
linea_x = [usable_colombia["gap"].min(), usable_colombia["gap"].max()]
linea_y = modelo_colombia.predict([[linea_x[0]], [linea_x[1]]])
ax.plot(linea_x, linea_y, color="C1", label="ajuste lineal")
ax.set_xlabel("gap (grados)")
ax.set_ylabel("horizontalError (km)")
ax.set_title("Colombia 2024: error horizontal frente a gap")
ax.legend()
plt.show()
```

Pregúntese, mirando el gráfico: ¿la recta describe bien lo que ve, o hay estructura que se le escapa? Si la respuesta es la segunda, el problema no es el código: es que una recta no es el modelo adecuado. Esa es una conclusión válida y vale la pena escribirla.

**Comprobar:**

```python
assert len(usable_colombia) > 15
assert modelo_colombia.coef_.shape == (1,)
print("Modelo Colombia: OK")
```

### Paso 13 — Escribir el diagnóstico

Un análisis que no se puede explicar en palabras no está terminado. Complete el texto de abajo usando los números de `resumen_colombia` y del ajuste.

Responda, en concreto: ¿usaría este catálogo para una revisión posterior a un sismo? ¿Bajo qué criterios diría que funcionó? ¿Qué dos problemas de calidad encontró? ¿Y qué parte del catálogo quedó fuera del modelo?

```python
diagnostico_colombia = """
Decision:
Criterios de exito:
Dos riesgos de calidad:
Filas que el modelo no vio:
"""
print(diagnostico_colombia)
```

---

## Parte individual — Perú 2024

**Propósito.** Repetir el método completo por su cuenta y comparar los dos países.

Esta sección es el mismo recorrido de la parte guiada, aplicado a Perú. Las fechas y la magnitud mínima no cambian. Lo único que cambia es la ventana geográfica.

No escriba funciones nuevas. Reutilice `build_usgs_url`, `download_csv`, `resumen_calidad` y `entrenar_error_por_gap` tal como quedaron. Ese es el punto del ejercicio: un método que solo funciona con los datos para los que se escribió no es un método.

`PARAMETROS_CURSO` es el contrato con las sesiones 2 a 5, que vuelven a descargar este mismo recorte. **No lo modifique.**

| Constante | Valor |
|-----------|--------|
| Latitud | -18.5 a 0.2 |
| Longitud | -82 a -68 |

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

Antes de seguir, compare el número de filas con el de Colombia. La diferencia será grande, y no es un error: Perú está sobre el borde de subducción entre la placa de Nazca y la placa Sudamericana, que es una de las zonas sísmicamente más activas del planeta.

**Comprobar:**

```python
assert "minlatitude=-18.5" in USGS_URL_PERU
assert CATALOGO_PERU.is_file()
assert len(sismos_peru) > 50, "El recorte del Perú vino casi vacío. Revise la URL."
print(f"Tabla Perú: {len(sismos_peru)} sismos. OK")
```

### Paso 15 — Evaluación y address

Llame a `resumen_calidad` y a `entrenar_error_por_gap` sobre la tabla del Perú, y ponga los resultados al lado de los de Colombia.

```python
resumen_peru = resumen_calidad(sismos_peru)
modelo_peru, usable_peru = entrenar_error_por_gap(sismos_peru)
print("Perú:", resumen_peru)
print("coeficiente Perú:", float(modelo_peru.coef_[0]))
print(f"filas usadas Perú: {len(usable_peru)} de {len(sismos_peru)}")
print("Colombia (para comparar):", resumen_colombia)
print("coeficiente Colombia:", float(modelo_colombia.coef_[0]))
```

```python
fig, ax = plt.subplots(figsize=(6, 4))
ax.scatter(usable_peru["gap"], usable_peru["horizontalError"], alpha=0.4, label="filas usadas")
linea_x = [usable_peru["gap"].min(), usable_peru["gap"].max()]
linea_y = modelo_peru.predict([[linea_x[0]], [linea_x[1]]])
ax.plot(linea_x, linea_y, color="C1", label="ajuste lineal")
ax.set_xlabel("gap (grados)")
ax.set_ylabel("horizontalError (km)")
ax.set_title("Perú 2024: error horizontal frente a gap")
ax.legend()
plt.show()
```

Compare los dos gráficos. Pistas de dónde mirar:

- **La proporción de localizaciones débiles.** Buena parte de la sismicidad peruana ocurre mar adentro, donde las estaciones solo pueden estar de un lado.
- **La pendiente.** Si difiere de la de Colombia, pregúntese si se debe a la red de estaciones, a la geografía, o simplemente a que hay muchos más eventos.
- **El rango de `gap`.** Dos rectas ajustadas sobre rangos distintos no son directamente comparables.

**Comprobar:**

```python
assert resumen_peru["filas"] == len(sismos_peru)
assert len(usable_peru) > 20
print("Replay Perú: OK")
print("URL del curso (guárdela):", USGS_URL_PERU)
```

### Ticket de salida

Complete en sus palabras. No copie el diagnóstico de Colombia.

```python
diagnostico_peru = """
Que cambio al pasar de Colombia a Peru:
Un riesgo de calidad que se repite:
Un riesgo que es distinto:
"""
print(diagnostico_peru)
```

<!-- end NOTEBOOK: -->
