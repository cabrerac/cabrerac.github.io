<!-- NOTEBOOK: -->

Este cuaderno se organiza en dos secciones:

1. **Parte guiada:** Descargamos el catálogo USGS de **Colombia**, 2024, magnitud 4.5 o más. Construimos tres modelos sobre la calidad de localización: una **regresión lineal**, una **regresión logística** y un **perceptrón**. Cada uno se programa dos veces: **desde cero con numpy** y con **scikit-learn**, y comparamos las dos versiones.
2. **Parte individual:** Los estudiantes eligen **uno** de los tres modelos y lo replican sobre el catálogo del **Perú**, 2024, misma magnitud, desde cero y con scikit-learn. Cierran con una interpretación escrita en términos de una decisión de ingeniería civil.

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

## Datos y helpers (reutilización de la sesión 1)

No repetimos el tutorial de acceso de la sesión 1. En un Colab fresco necesitamos las mismas piezas: importaciones, dos helpers de descarga, el recorte de Colombia y la tabla en memoria. Eso va en **dos bloques de código** con docstrings. El material nuevo —lineal, logística, perceptrón— empieza justo después.

### Importaciones

Un solo bloque con lo que usa todo el cuaderno. Si ya lo tiene cargado de otra celda, puede ejecutarlo de nuevo sin problema.

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

### Helpers de descarga y catálogo de Colombia

Este bloque redefine `build_usgs_url` y `download_csv` (las mismas ideas de la sesión 1), fija `PARAMETROS_COLOMBIA` y la ruta local, arma la URL, descarga el CSV y lo carga en `sismos_colombia`. Lea las docstrings: documentan el contrato de cada función. No rehacemos el recorrido paso a paso del Access.

| Parámetro clave | Valor Colombia |
|-----------------|----------------|
| fechas | 2024-01-01 → 2025-01-01 |
| `minmagnitude` | 4.5 |
| latitud | -4.5 → 13.5 |
| longitud | -79.5 → -66.5 |

```python
def build_usgs_url(parametros: dict) -> str:
    """Arma la URL del catálogo USGS FDSN a partir de un diccionario de parámetros.

    No toca la red: solo une la base con ``clave=valor`` separados por ``&``.
    Imprima la URL y revísela antes de descargar.
    """
    base = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    consulta = "&".join(f"{clave}={valor}" for clave, valor in parametros.items())
    return f"{base}?{consulta}"


def download_csv(url: str, dest: Path, timeout: int = 120) -> int:
    """Descarga ``url`` a ``dest`` y devuelve el número de bytes escritos.

    Falla temprano si el servidor responde 4xx/5xx o si el cuerpo no empieza
    con ``time,`` (cabecera del CSV del catálogo). Así evitamos guardar una
    página HTML de error con extensión ``.csv``.
    """
    respuesta = requests.get(url, timeout=timeout)
    respuesta.raise_for_status()
    texto = respuesta.text
    if not texto.startswith("time,"):
        raise ValueError(
            "La respuesta no es el CSV del catálogo. "
            "Revise la URL antes de seguir."
        )
    dest.write_text(texto, encoding="utf-8")
    return dest.stat().st_size


# Ventana de Colombia (margen en la frontera). Exactamente la de la sesión 1.
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
CATALOGO_COLOMBIA = Path("usgs_colombia_2024_m45.csv")

USGS_URL_COLOMBIA = build_usgs_url(PARAMETROS_COLOMBIA)
print(USGS_URL_COLOMBIA)

bytes_colombia = download_csv(USGS_URL_COLOMBIA, CATALOGO_COLOMBIA)
sismos_colombia = pd.read_csv(CATALOGO_COLOMBIA)
print(f"Guardado: {CATALOGO_COLOMBIA} ({bytes_colombia / 1e3:.1f} KB)")
print("Filas, columnas:", sismos_colombia.shape)
sismos_colombia.head()
```

Hoy nos importan sobre todo `gap`, `horizontalError`, `mag`, `depth` y `latitude`. Si aparece alguna columna que no reconoce, búsquela en el [glosario del USGS](https://earthquake.usgs.gov/data/comcat/).

**Comprobar:**

```python
assert USGS_URL_COLOMBIA.startswith("https://earthquake.usgs.gov/fdsnws/event/1/query?")
assert "starttime=2024-01-01" in USGS_URL_COLOMBIA
assert "minmagnitude=4.5" in USGS_URL_COLOMBIA
assert "minlatitude=-4.5" in USGS_URL_COLOMBIA
assert CATALOGO_COLOMBIA.is_file()
assert bytes_colombia > 3_000
columnas_clave = [
    "time", "latitude", "longitude", "depth", "mag", "magType",
    "id", "place", "horizontalError", "gap", "status",
]
faltan = [c for c in columnas_clave if c not in sismos_colombia.columns]
assert not faltan, f"Faltan columnas: {faltan}"
assert len(sismos_colombia) > 20, "El recorte de Colombia vino casi vacío. No cambie los parámetros."
print(f"Helpers + tabla Colombia: {len(sismos_colombia)} sismos. OK")
```

---

## Parte guiada B — Regresión lineal (Colombia)

**Propósito.** Entrenar un primer modelo sobre los datos que acabamos de descargar, y ser explícitos sobre lo que ese modelo no cubre. La pregunta es la misma que cerró la sesión 1 en address: **dado el `gap` de un sismo, ¿cuánto error horizontal cabe esperar?**

Es un problema de **regresión**, porque la respuesta es un número y no una categoría. El modelo más simple que puede responderla es una **recta**: una pendiente y un intercepto, dos parámetros que el algoritmo ajusta para que la recta pase lo más cerca posible de los puntos observados.

En ingeniería civil, ese número se lee así: si el hueco angular de estaciones crece, ¿cuántos kilómetros adicionales de incertidumbre horizontal cabe esperar en este recorte? Una pendiente positiva confirma la intuición física (peor cobertura → mayor error). Una pendiente cercana a cero diría que, en este recorte concreto, el `gap` no explica casi nada del error. Ambas lecturas son útiles. Ninguna reemplaza el cálculo de incertidumbre del USGS, que ya está hecho con mucha más información que la que tenemos aquí.

Dos advertencias antes de entrenar, y las dos son parte del resultado:

**Esto no es una herramienta de inspección.** Estamos ajustando una recta para practicar el paso de modelado, no para sustituir el informe operativo del USGS.

**El modelo solo ve las filas completas.** `dropna()` descarta los sismos a los que les falta `gap` o `horizontalError`. Esas filas no desaparecen del problema, solo desaparecen del ajuste. Y no faltan al azar: son típicamente los eventos peor determinados, justo los que más nos preocupaban en la evaluación de la sesión 1. El modelo se entrena, entonces, sobre la parte más fácil del catálogo. Hay que decirlo cuando se presenten los resultados.

### Paso 1 — Elegir las filas

Empaquetamos el filtro en una función. La parte individual reutilizará exactamente la misma regla sobre Perú. Si cada país se filtrara con criterios distintos, cualquier diferencia en la pendiente podría venir del método en vez de los datos.

```python
def filas_para_regresion(tabla: pd.DataFrame) -> pd.DataFrame:
    """Devuelve las filas que tienen gap y horizontalError."""
    return tabla[["gap", "horizontalError"]].dropna()
```

### Paso 2 — Entrenar la recta

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

### Paso 3 — Mirar el ajuste

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

### Paso 4 — La misma recta desde cero (numpy)

`LinearRegression` nos dio la pendiente y el intercepto en una línea. Ahora hacemos el mismo trabajo a mano, para ver qué hay dentro de ese `fit`. Es la misma estructura de los ejercicios de regresión del curso de introducción: implementar, comparar coeficientes con la biblioteca, comparar métricas y dibujar.

El modelo es $y = w x + b$, con $x$ el `gap` y $t$ el `horizontalError` observado. Entrenar es buscar los $w$ y $b$ que minimizan el **error cuadrático medio**:

$$
E(w, b) = \frac{1}{N} \sum_{n=1}^{N} \left( w x_n + b - t_n \right)^2
$$

Hay dos caminos. El primero es el **descenso de gradiente**: empezar en $w = b = 0$ y moverse, paso a paso, en la dirección que más baja el error. El tamaño del paso es la tasa de aprendizaje $\alpha$:

$$
w \leftarrow w - \alpha \frac{\partial E}{\partial w}, \qquad b \leftarrow b - \alpha \frac{\partial E}{\partial b}
$$

El segundo es la **ecuación normal**, que para la recta tiene solución cerrada, $[b, w]^\top = (X^\top X)^{-1} X^\top t$, donde $X$ lleva una columna de unos para el intercepto. Con una sola variable y unas 60 filas, las dos llegan al mismo sitio. Usamos la segunda solo como control.

Un detalle práctico. El `gap` va de unos 20 a más de 200 grados. Con números así, un mismo $\alpha$ es demasiado grande para $w$ y demasiado pequeño para $b$, y el descenso oscila o no avanza. Por eso la función estandariza $x$ por dentro (media 0, desviación 1) y, al final, devuelve $w$ y $b$ en las unidades originales: km por grado y km.

```python
def entrenar_lineal_numpy(x, t, alpha: float = 0.1, n_epochs: int = 500):
    """Ajusta t = w x + b con descenso de gradiente sobre el error cuadrático medio.

    x se estandariza por dentro para que un mismo alpha sirva para w y para b.
    w y b se devuelven en las unidades originales (km por grado y km).

    Returns:
        w, b y la lista del error cuadrático medio por época.
    """
    x = np.asarray(x, dtype=float)
    t = np.asarray(t, dtype=float)
    media, desv = x.mean(), x.std()
    xs = (x - media) / desv
    w, b = 0.0, 0.0
    historial = []
    for _ in range(n_epochs):
        error = w * xs + b - t
        historial.append(float(np.mean(error ** 2)))
        w = w - alpha * 2 * np.mean(error * xs)
        b = b - alpha * 2 * np.mean(error)
    return w / desv, b - w * media / desv, historial


def ecuacion_normal(x, t):
    """Solución cerrada de mínimos cuadrados con una columna de unos para el intercepto.

    Returns:
        w y b en las unidades originales.
    """
    X_b = np.c_[np.ones(len(x)), np.asarray(x, dtype=float)]
    b, w = np.linalg.inv(X_b.T @ X_b) @ X_b.T @ np.asarray(t, dtype=float)
    return float(w), float(b)


def comparar_lineal_con_sklearn(usable: pd.DataFrame, modelo_sk):
    """Entrena la recta numpy sobre las filas usadas y la compara con un LinearRegression ya ajustado.

    Returns:
        Una tabla con pendiente, intercepto, MSE y R² de cada versión, y el resultado numpy (w, b, historial).
    """
    x = usable["gap"].to_numpy(dtype=float)
    t = usable["horizontalError"].to_numpy(dtype=float)
    w_gd, b_gd, historial = entrenar_lineal_numpy(x, t)
    w_ne, b_ne = ecuacion_normal(x, t)
    versiones = {
        "numpy (descenso de gradiente)": (w_gd, b_gd),
        "numpy (ecuación normal)": (w_ne, b_ne),
        "scikit-learn": (float(modelo_sk.coef_[0]), float(modelo_sk.intercept_)),
    }
    filas = []
    for nombre, (w, b) in versiones.items():
        pred = w * x + b
        mse = float(np.mean((t - pred) ** 2))
        r2 = 1 - np.sum((t - pred) ** 2) / np.sum((t - t.mean()) ** 2)
        filas.append({"versión": nombre, "pendiente (km/grado)": w, "intercepto (km)": b,
                      "MSE (km²)": mse, "R²": r2})
    return pd.DataFrame(filas).set_index("versión").round(5), (w_gd, b_gd, historial)


comparacion_lineal_co, (w_gd_co, b_gd_co, historial_lineal_co) = comparar_lineal_con_sklearn(
    usable_lineal_co, modelo_lineal_co
)
comparacion_lineal_co
```

Lea la tabla por columnas. Las tres versiones deberían coincidir en pendiente e intercepto hasta varios decimales, y por tanto también en MSE y $R^2$. Si coinciden, ya sabe qué hace `LinearRegression().fit`: minimiza el mismo error que acabamos de escribir. El $R^2$ dice qué fracción de la variación del error horizontal explica el `gap`. Un valor bajo no es un fallo del código: es lo que la sesión 1 ya sugería, que el `gap` explica solo una parte del error.

### Paso 5 — Comparar las dos rectas y la curva de pérdida

A la izquierda, las dos rectas sobre los mismos puntos. Si el código numpy está bien, la línea punteada queda encima de la continua. A la derecha, el error cuadrático medio en cada época del descenso de gradiente, con el error final de scikit-learn como referencia.

```python
def graficar_lineal(usable: pd.DataFrame, w_gd: float, b_gd: float, modelo_sk, historial, titulo: str):
    """Dibuja la recta numpy frente a la de scikit-learn y la curva de pérdida del descenso de gradiente."""
    x = usable["gap"].to_numpy(dtype=float)
    t = usable["horizontalError"].to_numpy(dtype=float)
    linea_x = np.array([x.min(), x.max()])
    mse_sk = float(np.mean((t - modelo_sk.predict(x.reshape(-1, 1))) ** 2))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))
    ax1.scatter(x, t, alpha=0.4, label="filas usadas")
    ax1.plot(linea_x, modelo_sk.predict(linea_x.reshape(-1, 1)), color="C1", label="scikit-learn")
    ax1.plot(linea_x, w_gd * linea_x + b_gd, color="k", linestyle="--", label="numpy (gradiente)")
    ax1.set_xlabel("gap (grados)")
    ax1.set_ylabel("horizontalError (km)")
    ax1.set_title(titulo)
    ax1.legend()
    ax2.plot(historial, label="numpy (gradiente)")
    ax2.axhline(mse_sk, color="C1", linestyle="--", label="MSE de scikit-learn")
    ax2.set_xlabel("época")
    ax2.set_ylabel("MSE (km²)")
    ax2.set_yscale("log")
    ax2.set_title("Curva de pérdida")
    ax2.legend()
    plt.tight_layout()
    plt.show()


graficar_lineal(usable_lineal_co, w_gd_co, b_gd_co, modelo_lineal_co, historial_lineal_co,
                "Colombia 2024: numpy frente a scikit-learn")
```

La curva baja rápido en las primeras épocas y luego se aplana sobre la línea de scikit-learn. Ese aplanamiento es la señal de que el descenso llegó al mínimo: más épocas ya no mejoran nada. Si la curva subiera o saltara, $\alpha$ sería demasiado grande. Pruebe `alpha=1.2` en `entrenar_lineal_numpy` para verlo, y vuelva a 0.1.

**Comprobar:**

```python
w_sk_co = float(modelo_lineal_co.coef_[0])
b_sk_co = float(modelo_lineal_co.intercept_)
w_ne_co, b_ne_co = ecuacion_normal(usable_lineal_co["gap"], usable_lineal_co["horizontalError"])
assert abs(w_ne_co - w_sk_co) < 1e-8 and abs(b_ne_co - b_sk_co) < 1e-6
assert abs(w_gd_co - w_sk_co) < 1e-3 * max(1.0, abs(w_sk_co)), "La pendiente numpy no coincide con scikit-learn."
assert abs(b_gd_co - b_sk_co) < 1e-2 * max(1.0, abs(b_sk_co)), "El intercepto numpy no coincide con scikit-learn."
assert historial_lineal_co[-1] < historial_lineal_co[0]
print("Recta numpy = recta scikit-learn (Colombia): OK")
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

### Paso 6 — Construir la tabla de clasificación

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

### Paso 7 — Partición train / test

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

### Paso 8 — Entrenar la logística

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

### Paso 9 — La logística desde cero (numpy)

Igual que con la recta, programamos la logística a mano y la comparamos con scikit-learn. El modelo combina las tres características en un número y lo pasa por la sigmoide:

$$
y_n = \sigma\left( \mathbf{w}^\top \mathbf{x}_n + b \right), \qquad \sigma(a) = \frac{1}{1 + e^{-a}}
$$

$y_n$ se lee como la probabilidad de que la fila $n$ sea una ubicación débil. La pérdida ya no es el error cuadrático, sino la **entropía cruzada**, que castiga mucho una probabilidad baja asignada a la clase correcta:

$$
E(\mathbf{w}, b) = -\frac{1}{N} \sum_{n=1}^{N} \left\{ t_n \ln y_n + (1 - t_n) \ln (1 - y_n) \right\}
$$

Su gradiente tiene una forma muy simple, el error de cada fila multiplicado por sus entradas:

$$
\frac{\partial E}{\partial \mathbf{w}} = \frac{1}{N} \sum_{n=1}^{N} (y_n - t_n)\, \mathbf{x}_n, \qquad \frac{\partial E}{\partial b} = \frac{1}{N} \sum_{n=1}^{N} (y_n - t_n)
$$

y el descenso de gradiente usa la misma regla de la recta, con tasa de aprendizaje $\alpha$.

Dos decisiones para que la comparación sea justa:

1. **Escalado.** `mag`, `depth` y `latitude` están en escalas muy distintas. Estandarizamos con la media y la desviación **de train**, y entrenamos las dos versiones sobre las mismas entradas escaladas. Así los coeficientes se pueden comparar uno a uno.
2. **Regularización de scikit-learn.** `LogisticRegression` añade por defecto una penalización $L_2$ a los pesos, controlada por `C` (por defecto `C=1`, y un `C` pequeño quiere decir penalización fuerte). Nuestra versión numpy no penaliza nada. Para comparar el mismo problema, el modelo de referencia usa `C=1e6`, que deja la penalización en la práctica en cero. El modelo del paso 8 sigue siendo la línea base de la sesión: sin escalar y con `C=1`, así que sus coeficientes no se comparan con estos.

```python
def sigmoide(a):
    """Sigmoide: comprime cualquier número real al intervalo (0, 1)."""
    return 1.0 / (1.0 + np.exp(-a))


def entrenar_logistica_numpy(X: np.ndarray, t: np.ndarray, alpha: float = 0.5, n_epochs: int = 5000):
    """Entrena una regresión logística con descenso de gradiente sobre la entropía cruzada.

    X debe venir escalada. t debe ser 0/1. Sin regularización.

    Returns:
        Pesos w, sesgo b y la lista de la entropía cruzada por época.
    """
    w = np.zeros(X.shape[1])
    b = 0.0
    historial = []
    for _ in range(n_epochs):
        y = sigmoide(X @ w + b)
        y_rec = np.clip(y, 1e-12, 1 - 1e-12)
        historial.append(float(-np.mean(t * np.log(y_rec) + (1 - t) * np.log(1 - y_rec))))
        w = w - alpha * X.T @ (y - t) / len(X)
        b = b - alpha * float(np.mean(y - t))
    return w, b, historial


def predecir_logistica_numpy(X: np.ndarray, w: np.ndarray, b: float) -> np.ndarray:
    """Predice 0/1: 1 si la probabilidad de ubicación débil es al menos 0.5."""
    return (sigmoide(X @ w + b) >= 0.5).astype(int)


def comparar_logistica_con_sklearn(X_train, y_train, X_test, y_test):
    """Escala con train, entrena la logística numpy y una LogisticRegression con C=1e6, y las compara.

    Returns:
        Un diccionario con el escalado, los pesos de las dos versiones, la curva de pérdida,
        las exactitudes de test y una tabla de coeficientes.
    """
    media, desv = X_train.mean(axis=0), X_train.std(axis=0)
    A_train, A_test = (X_train - media) / desv, (X_test - media) / desv
    w, b, historial = entrenar_logistica_numpy(A_train, y_train)
    referencia = LogisticRegression(C=1e6, max_iter=10_000).fit(A_train, y_train)
    tabla = pd.DataFrame(
        {"numpy": list(w) + [b],
         "scikit-learn (C=1e6)": list(referencia.coef_[0]) + [float(referencia.intercept_[0])]},
        index=FEATURES_CLASIFICACION + ["sesgo"],
    )
    tabla["diferencia"] = tabla["numpy"] - tabla["scikit-learn (C=1e6)"]
    return {
        "media": media, "desv": desv, "w": w, "b": b, "historial": historial, "referencia": referencia,
        "acc_numpy": accuracy_score(y_test, predecir_logistica_numpy(A_test, w, b)),
        "acc_sklearn": accuracy_score(y_test, referencia.predict(A_test)),
        "tabla": tabla.round(4),
    }


logistica_numpy_co = comparar_logistica_con_sklearn(X_train_co, y_train_co, X_test_co, y_test_co)
print("línea base mayoritaria (test):        ", round(baseline_co, 3))
print("logística numpy (test):               ", round(logistica_numpy_co["acc_numpy"], 3))
print("logística scikit-learn C=1e6 (test):  ", round(logistica_numpy_co["acc_sklearn"], 3))
print("logística del paso 8, C=1 (test):     ", round(acc_log_co, 3))
logistica_numpy_co["tabla"]
```

La columna `diferencia` debería quedar en el tercer o cuarto decimal. Eso confirma que `LogisticRegression` resuelve el mismo problema que nuestras veinte líneas, solo que con un optimizador más rápido. Ahora los coeficientes sí se leen en una misma escala: cada uno dice cuánto cambia el logit de la ubicación débil cuando la variable sube una desviación estándar. Las exactitudes de test van, como siempre, al lado del piso.

### Paso 10 — Frontera de decisión y curva de pérdida

Tres características no caben en un plano. Para dibujar la frontera fijamos `latitude` en su media de train y miramos el plano `mag`–`depth`. La línea es donde la probabilidad vale 0.5: de un lado el modelo dice "ubicación firme", del otro "ubicación débil". Es el mismo recurso de rejilla y contorno que usamos para la frontera del perceptrón en el curso de introducción.

```python
def graficar_logistica(res: dict, tabla: pd.DataFrame, titulo: str):
    """Curva de pérdida numpy y fronteras de decisión (probabilidad 0.5) numpy y scikit-learn en el plano mag-depth.

    latitude queda fija en su media de train.
    """
    mag = np.linspace(tabla["mag"].min() - 0.1, tabla["mag"].max() + 0.1, 200)
    prof = np.linspace(0, tabla["depth"].max() + 10, 200)
    malla_mag, malla_prof = np.meshgrid(mag, prof)
    rejilla = np.column_stack([malla_mag.ravel(), malla_prof.ravel(), np.full(malla_mag.size, res["media"][2])])
    rejilla_esc = (rejilla - res["media"]) / res["desv"]
    prob_np = sigmoide(rejilla_esc @ res["w"] + res["b"]).reshape(malla_mag.shape)
    prob_sk = res["referencia"].predict_proba(rejilla_esc)[:, 1].reshape(malla_mag.shape)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))
    ax1.plot(res["historial"], label="numpy (gradiente)")
    ax1.set_xlabel("época")
    ax1.set_ylabel("entropía cruzada (train)")
    ax1.set_title("Curva de pérdida")
    ax1.legend()
    debil = tabla["ubicacion_debil"] == 1
    ax2.scatter(tabla.loc[~debil, "mag"], tabla.loc[~debil, "depth"], alpha=0.5, label="ubicación firme")
    ax2.scatter(tabla.loc[debil, "mag"], tabla.loc[debil, "depth"], alpha=0.5, label="ubicación débil")
    ax2.contour(malla_mag, malla_prof, prob_sk, levels=[0.5], colors="C1")
    ax2.contour(malla_mag, malla_prof, prob_np, levels=[0.5], colors="k", linestyles="--")
    ax2.plot([], [], color="C1", label="frontera scikit-learn")
    ax2.plot([], [], color="k", linestyle="--", label="frontera numpy")
    ax2.set_xlabel("mag")
    ax2.set_ylabel("depth (km)")
    ax2.set_title(titulo)
    ax2.legend(fontsize=8)
    plt.tight_layout()
    plt.show()


graficar_logistica(logistica_numpy_co, clasif_colombia, "Colombia 2024: frontera con latitude en su media")
```

Si las dos fronteras se superponen, el código numpy está bien. Fíjese en que la frontera es una **recta** en este plano: la logística es un modelo lineal con una sigmoide al final, y por eso solo puede separar las clases con una línea (un plano, en tres dimensiones). Si en este corte los dos colores están mezclados a ambos lados de la línea, ninguna recta los separa bien, y eso explica por qué la exactitud apenas se aleja del piso. Si la línea no aparece dentro del gráfico, el modelo predice la misma clase en todo este corte: también es un resultado.

**Comprobar:**

```python
res = logistica_numpy_co
diferencia_max = float(np.max(np.abs(res["tabla"]["diferencia"])))
assert diferencia_max < 0.01, f"Los coeficientes numpy se alejan de scikit-learn ({diferencia_max:.4f})."
assert abs(res["acc_numpy"] - res["acc_sklearn"]) <= 1 / len(y_test_co) + 1e-9, "Las exactitudes difieren en más de una fila."
assert res["historial"][-1] < res["historial"][0]
assert 0.0 <= res["acc_numpy"] <= 1.0
print("Logística numpy = logística scikit-learn (Colombia): OK")
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

En símbolos, con la etiqueta $t_n \in \{-1, +1\}$ y la tasa de aprendizaje $\alpha$ (`learning_rate` en el código), cada error mueve los pesos así:

$$
\mathbf{w} \leftarrow \mathbf{w} + \alpha \, t_n \mathbf{x}_n
$$

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
| **Lineal** | Deja pasar la combinación tal cual | Es el modelo de regresión del paso 2. Útil para predecir un error en km |
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

**Propósito.** Elegir **uno** de los tres modelos de la parte guiada, replicarlo sobre Perú desde cero y con scikit-learn, y explicar el resultado en términos de una decisión de ingeniería civil.

Las fechas y la magnitud mínima no cambian. Lo único que cambia es la ventana geográfica. No escriba funciones nuevas de descarga ni de entrenamiento: todo lo que necesita ya está definido arriba. Un método que solo funciona con los datos para los que se escribió no es un método.

`PARAMETROS_CURSO` es el contrato con las sesiones siguientes, que vuelven a descargar este mismo recorte. **No lo modifique.**

| Constante | Valor |
|-----------|--------|
| Latitud | -18.5 a 0.2 |
| Longitud | -82 a -68 |

El recorrido tiene cuatro pasos:

1. Descargar y preparar Perú (común a los tres modelos).
2. Elegir el modelo en `MODELO_ELEGIDO`.
3. Ejecutar la opción elegida: versión numpy frente a scikit-learn, más un gráfico. Las celdas de las otras dos opciones no hacen nada.
4. Escribir la interpretación.

### Descargar y cargar Perú

Un solo bloque: parámetros del curso, URL, descarga y lectura. Sin rehacer el tutorial de Access.

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

### Paso 14 — Preparar Perú (común a las tres opciones)

Esta celda arma las dos tablas que usan los modelos: las filas con `gap` y `horizontalError` para la recta, y la tabla de clasificación con la partición de siempre (`test_size=0.30`, `random_state=42`, estratificada) para la logística y el perceptrón. También calcula el piso de la clase mayoritaria.

```python
usable_lineal_pe = filas_para_regresion(sismos_peru)

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

print(f"filas para la recta: {len(usable_lineal_pe)} de {len(sismos_peru)}")
print("filas para clasificar:", len(clasif_peru), "| positivos:", int(y_pe.sum()))
print("train:", len(y_train_pe), "test:", len(y_test_pe))
print("línea base mayoritaria (test):", round(baseline_pe, 3))
```

Note que en Perú la clase mayoritaria es la de ubicación **débil**. Buena parte de la sismicidad ocurre mar adentro, donde las estaciones solo pueden estar de un lado, y eso empuja el `gap` hacia arriba. El test tiene unas 40 filas, así que una fila mueve la exactitud unos 2.5 puntos.

### Paso 15 — Elegir el modelo

Escriba en la celda siguiente `"lineal"`, `"logistica"` o `"perceptron"`. Si no está seguro, piense en la decisión que quiere apoyar:

- **Lineal:** cuántos kilómetros de error horizontal cabe esperar dado el `gap`. Sirve para dimensionar un margen de incertidumbre.
- **Logística:** el riesgo de que una fila sea una ubicación débil. Sirve para ordenar filas por sospecha en un informe.
- **Perceptrón:** una decisión dura, pasa o no pasa. Sirve como filtro rápido antes de la revisión de distrito.

```python
MODELO_ELEGIDO = "logistica"  # TODO: escriba "lineal", "logistica" o "perceptron"

assert MODELO_ELEGIDO in {"lineal", "logistica", "perceptron"}, "Use exactamente una de las tres opciones."
print("Modelo elegido:", MODELO_ELEGIDO)
```

### Opción A — Regresión lineal sobre Perú

Ajuste `horizontalError ~ gap` con scikit-learn y con numpy, compare la tabla y dibuje las dos rectas con la curva de pérdida. Las funciones son las de los pasos 2, 4 y 5. Al leer el resultado, mire la pendiente frente a la de Colombia, el rango de `gap` de cada país y las filas usadas frente al total.

```python
if MODELO_ELEGIDO == "lineal":
    # TODO 1: recta de scikit-learn sobre Perú (misma función de la parte guiada).
    modelo_lineal_pe, usable_lineal_pe = entrenar_error_por_gap(sismos_peru)
    # TODO 2: recta numpy y comparación. Pruebe también otro alpha en entrenar_lineal_numpy.
    comparacion_lineal_pe, (w_gd_pe, b_gd_pe, historial_lineal_pe) = comparar_lineal_con_sklearn(
        usable_lineal_pe, modelo_lineal_pe
    )
    print(comparacion_lineal_pe.to_string())
    print("pendiente Colombia (scikit-learn):", round(float(modelo_lineal_co.coef_[0]), 5))
    # TODO 3: gráfico de las dos rectas y la curva de pérdida.
    graficar_lineal(usable_lineal_pe, w_gd_pe, b_gd_pe, modelo_lineal_pe, historial_lineal_pe,
                    "Perú 2024: numpy frente a scikit-learn")
else:
    print("Opción A no elegida.")
```

### Opción B — Regresión logística sobre Perú

Entrene la logística numpy y la de scikit-learn con `C=1e6` sobre las mismas entradas escaladas, compare coeficientes y exactitudes, y dibuje la frontera y la curva de pérdida. Las funciones son las de los pasos 9 y 10. Incluya también la logística de la sesión (sin escalar, `C=1`) como referencia.

```python
if MODELO_ELEGIDO == "logistica":
    # TODO 1: logística de referencia de la sesión (sin escalar, C=1).
    modelo_logistico_pe = LogisticRegression(max_iter=1000, random_state=42).fit(X_train_pe, y_train_pe)
    acc_log_pe = accuracy_score(y_test_pe, modelo_logistico_pe.predict(X_test_pe))
    # TODO 2: numpy frente a scikit-learn con C=1e6, mismas entradas escaladas.
    logistica_numpy_pe = comparar_logistica_con_sklearn(X_train_pe, y_train_pe, X_test_pe, y_test_pe)
    print(logistica_numpy_pe["tabla"].to_string())
    print("línea base mayoritaria (test):", round(baseline_pe, 3))
    print("numpy:", round(logistica_numpy_pe["acc_numpy"], 3),
          "| scikit-learn C=1e6:", round(logistica_numpy_pe["acc_sklearn"], 3),
          "| sesión, C=1:", round(acc_log_pe, 3))
    # TODO 3: frontera de decisión y curva de pérdida.
    graficar_logistica(logistica_numpy_pe, clasif_peru, "Perú 2024: frontera con latitude en su media")
else:
    print("Opción B no elegida.")
```

### Opción C — Perceptrón sobre Perú

Entrene el perceptrón numpy y el de scikit-learn, compare sus exactitudes con el piso, y dibuje las dos exactitudes junto a la línea base. Las funciones son las de los pasos 11 y 12. Recuerde que las dos versiones no tienen por qué coincidir al decimal: el perceptrón no minimiza una pérdida suave y depende del orden de los ejemplos.

```python
if MODELO_ELEGIDO == "perceptron":
    # TODO 1: perceptrón numpy. Pruebe otro n_epochs o learning_rate y vea si cambia.
    pesos_numpy_pe = entrenar_perceptron_numpy(X_train_pe, y_train_pe)
    acc_numpy_pe = accuracy_score(y_test_pe, predecir_perceptron_numpy(X_test_pe, pesos_numpy_pe))
    # TODO 2: perceptrón de scikit-learn.
    modelo_perceptron_pe = Perceptron(max_iter=1000, random_state=42, tol=1e-3).fit(X_train_pe, y_train_pe)
    acc_sk_pe = accuracy_score(y_test_pe, modelo_perceptron_pe.predict(X_test_pe))
    print("pesos numpy (bias, mag, depth, latitude):", pesos_numpy_pe)
    print("coeficientes scikit-learn:", modelo_perceptron_pe.coef_[0])
    print("piso:", round(baseline_pe, 3), "| numpy:", round(acc_numpy_pe, 3), "| scikit-learn:", round(acc_sk_pe, 3))
    # TODO 3: gráfico de exactitudes frente al piso.
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.bar(["numpy", "scikit-learn"], [acc_numpy_pe, acc_sk_pe], color=["k", "C1"])
    ax.axhline(baseline_pe, color="gray", linestyle="--", label="línea base mayoritaria")
    ax.set_ylim(0, 1)
    ax.set_ylabel("exactitud (test)")
    ax.set_title("Perú 2024: perceptrón")
    ax.legend()
    plt.show()
else:
    print("Opción C no elegida.")
```

**Comprobar:**

```python
assert len(clasif_peru) > 20 and len(usable_lineal_pe) > 20
if MODELO_ELEGIDO == "lineal":
    assert abs(w_gd_pe - float(modelo_lineal_pe.coef_[0])) < 1e-3 * max(1.0, abs(float(modelo_lineal_pe.coef_[0])))
    assert abs(b_gd_pe - float(modelo_lineal_pe.intercept_)) < 1e-2 * max(1.0, abs(float(modelo_lineal_pe.intercept_)))
elif MODELO_ELEGIDO == "logistica":
    assert float(np.max(np.abs(logistica_numpy_pe["tabla"]["diferencia"]))) < 0.01
    assert abs(logistica_numpy_pe["acc_numpy"] - logistica_numpy_pe["acc_sklearn"]) <= 1 / len(y_test_pe) + 1e-9
else:
    assert pesos_numpy_pe.shape == (1 + len(FEATURES_CLASIFICACION),)
    assert 0.0 <= acc_numpy_pe <= 1.0 and 0.0 <= acc_sk_pe <= 1.0
print(f"Perú, opción {MODELO_ELEGIDO}: OK")
print("URL del curso (guárdela):", USGS_URL_PERU)
```

### Paso 16 — Interpretar en términos civiles

Complete en sus palabras. No basta con pegar los números. Diga qué modelo eligió y para qué decisión, si la versión numpy y la de scikit-learn cuentan la misma historia, cómo se compara con la línea base (el piso de la clase mayoritaria si clasifica, o el error de la recta si hace regresión), y qué cambió respecto a Colombia.

```python
interpretacion_peru = """
Modelo elegido y decision civil que apoya:
Numpy frente a scikit-learn (coinciden o no, y por que):
Comparacion con la linea base de Peru:
Que cambio respecto a Colombia:
Que no puede decidir este modelo por si solo:
"""
print(interpretacion_peru)
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
