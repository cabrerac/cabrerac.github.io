<!-- NOTEBOOK: -->

Este cuaderno se organiza en dos secciones:

1. **Seccion guiada:** Descargamos el catálogo USGS de **Colombia**, 2024, para sismos de magnitud 4.5 o más. Recorremos las diferentes etapas de la metodología de ciencia de datos **acceso**, **evaluación** y **address**.
2. **Sección individual:** Los estudiantes replicarán el mismo método sobre el catálogo del **Perú**, 2024, misma magnitud. Reutilicen las funciones de la parte guiada.

En esta oportunidad nos interesa determinar después de un sismo, ¿qué filas están en condiciones de usarse para una revisión (dónde fue, qué tan grande, qué tan segura es la localización)?

Ejecute las celdas de arriba hacia abajo. En cada **Comprobar**, confirme el mensaje `OK` antes de seguir.

Las sesiones siguientes vuelven a descargar el recorte del **Perú**. No cambie esos parámetros.

Documentación del servicio: [USGS FDSN event API](https://earthquake.usgs.gov/fdsnws/event/1/).

---

## Repaso de Python para este cuaderno

Estas celdas cubren solo lo que usaremos hoy: armar una URL, descargar un CSV y leerlo con pandas. Si ya lo domina, ejecútelas y siga.

### Una dirección y `requests`

**`requests.get`** pide un archivo por HTTP. **`raise_for_status`** detiene la celda si el servidor responde con error.

```python
import requests

respuesta = requests.get("https://earthquake.usgs.gov/fdsnws/event/1/version", timeout=60)
respuesta.raise_for_status()
print(respuesta.text.strip())
```

### Guardar con `Path` y leer con pandas

**`Path`** es la ruta del archivo en esta sesión de Colab. **`read_csv`** convierte el CSV en una tabla.

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

El USGS publica el catálogo en `https://earthquake.usgs.gov/fdsnws/event/1/query`. `format=csv` pide una tabla. El resto fija el recorte.

Esa URL **es** la decisión de acceso. Una magnitud mínima de 4.5 deja fuera sismos pequeños. La ventana geográfica deja fuera el resto del mundo.

| Constante | Valor | Papel |
|-----------|--------|--------|
| Inicio | 2024-01-01 | Primer instante incluido |
| Fin | 2025-01-01 | Límite superior (cubre todo 2024) |
| Magnitud mínima | 4.5 | Sismos que ya importan para una revisión |
| Latitud | -4.5 a 13.5 | Ventana de Colombia, con un margen en la frontera |
| Longitud | -79.5 a -66.5 | Ventana de Colombia, con un margen en la frontera |

```python
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
```

`build_usgs_url` solo une la base y los parámetros. No descarga nada.

```python
def build_usgs_url(parametros: dict) -> str:
    """Arma la URL del catálogo USGS a partir de un diccionario de parámetros."""
    base = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    consulta = "&".join(f"{clave}={valor}" for clave, valor in parametros.items())
    return f"{base}?{consulta}"


USGS_URL_COLOMBIA = build_usgs_url(PARAMETROS_COLOMBIA)
print(USGS_URL_COLOMBIA)
```

**Comprobar:**

```python
assert USGS_URL_COLOMBIA.startswith("https://earthquake.usgs.gov/fdsnws/event/1/query?")
assert "starttime=2024-01-01" in USGS_URL_COLOMBIA
assert "minmagnitude=4.5" in USGS_URL_COLOMBIA
assert "minlatitude=-4.5" in USGS_URL_COLOMBIA
print("URL de Colombia: OK")
```

`download_csv` guarda la respuesta en disco y rechaza una página de error que no sea una tabla.

```python
def download_csv(url: str, dest: Path, timeout: int = 120) -> int:
    """Descarga url a dest y devuelve el número de bytes.

    Falla si la respuesta no es el CSV del catálogo.
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

Access termina cuando la tabla está en memoria y sabemos qué columnas trajimos.

```python
sismos_colombia = pd.read_csv(CATALOGO_COLOMBIA)
print("Filas, columnas:", sismos_colombia.shape)
print("Columnas:", list(sismos_colombia.columns))
sismos_colombia.head()
```

**Comprobar:**

```python
columnas_clave = ["time", "latitude", "longitude", "depth", "mag", "magType", "id", "place", "horizontalError", "gap", "status"]
faltan = [columna for columna in columnas_clave if columna not in sismos_colombia.columns]
assert not faltan, f"Faltan columnas: {faltan}"
assert len(sismos_colombia) > 20, "El recorte de Colombia vino casi vacío. No cambie los parámetros."
print(f"Tabla Colombia: {len(sismos_colombia)} sismos. OK")
```

Cada fila es un sismo. `mag` es la magnitud. `depth` es la profundidad en kilómetros. `magType` dice qué escala se usó (`mb`, `mww`, `mwr` no son intercambiables sin más). `gap` es el hueco angular entre estaciones, en grados. `horizontalError` es la incertidumbre horizontal en kilómetros.

---

## Parte guiada B — Evaluación (Colombia)

La evaluación responde a la decisión, no a un puntaje genérico. Una fila sirve para la revisión si sabemos dónde fue, con qué magnitud, y con qué incertidumbre.

```python
faltantes = sismos_colombia.isna().sum().sort_values(ascending=False)
print("Valores faltantes por columna:")
print(faltantes[faltantes > 0])
if faltantes.sum() == 0:
    print("Ninguna celda vacía en este recorte.")

duplicados = int(sismos_colombia["id"].duplicated().sum())
print("Ids duplicados:", duplicados)
```

Un catálogo sin celdas vacías no está terminado. El recorte de magnitud 4.5 ya dejó fuera muchos registros peor determinados.

El USGS a veces publica la profundidad como **10 km** cuando no la pudo estimar.

```python
profundidad_fija = sismos_colombia["depth"].round(3).eq(10)
print(f"Profundidad exactamente 10 km: {int(profundidad_fija.sum())} de {len(sismos_colombia)}")
sismos_colombia.loc[profundidad_fija, ["time", "place", "mag", "depth", "depthError"]].head()
```

```python
print(sismos_colombia["magType"].value_counts(dropna=False))
```

No compare un `mb` con un `mww` como si fueran el mismo número.

Un error horizontal de más de 10 km, o un `gap` mayor que 90 grados, debilita la frase "este distrito".

```python
incertidumbre = (sismos_colombia["horizontalError"] > 10) | (sismos_colombia["gap"] > 90)
print(f"Localización débil para un distrito: {int(incertidumbre.sum())} de {len(sismos_colombia)}")
(
    sismos_colombia.loc[incertidumbre, ["place", "mag", "horizontalError", "gap"]]
    .sort_values("horizontalError", ascending=False)
    .head(8)
)
```

`resumen_calidad` junta los conteos. La parte individual vuelve a llamar esta función.

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

Address usa la tabla para un modelo. Aquí predice `horizontalError` a partir de `gap`. Es un primer ajuste para practicar el paso, no una herramienta de inspección.

Solo entran filas que tienen ambas columnas. Las demás quedan fuera del ajuste y el riesgo debe quedar escrito.

```python
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt


def filas_para_modelo(tabla: pd.DataFrame) -> pd.DataFrame:
    """Devuelve las filas que tienen gap y horizontalError."""
    return tabla[["gap", "horizontalError"]].dropna()


def entrenar_error_por_gap(tabla: pd.DataFrame):
    """Ajusta horizontalError como función lineal de gap.

    Returns:
        El modelo entrenado y la tabla usada en el ajuste.
    """
    usable = filas_para_modelo(tabla)
    X = usable[["gap"]].to_numpy()
    y = usable["horizontalError"].to_numpy()
    modelo = LinearRegression().fit(X, y)
    return modelo, usable


modelo_colombia, usable_colombia = entrenar_error_por_gap(sismos_colombia)
print("coeficiente (km por grado):", float(modelo_colombia.coef_[0]))
print("intercepto:", float(modelo_colombia.intercept_))
print(f"filas usadas: {len(usable_colombia)} de {len(sismos_colombia)}")
```

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

**Comprobar:**

```python
assert len(usable_colombia) > 15
assert modelo_colombia.coef_.shape == (1,)
print("Modelo Colombia: OK")
```

Escriba, con los números de `resumen_colombia` y del ajuste, si usaría este catálogo para una revisión y qué riesgo queda después del modelo.

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

Repita **acceso**, **evaluación** y **address** sobre el Perú. Las fechas y la magnitud mínima son las mismas. Cambia la ventana geográfica.

`PARAMETROS_CURSO` es el contrato con las sesiones siguientes. No lo cambie.

| Constante | Valor |
|-----------|--------|
| Latitud | -18.5 a 0.2 |
| Longitud | -82 a -68 |

Reutilice `build_usgs_url`, `download_csv`, `resumen_calidad` y `entrenar_error_por_gap`.

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

**Comprobar:**

```python
assert "minlatitude=-18.5" in USGS_URL_PERU
assert CATALOGO_PERU.is_file()
assert len(sismos_peru) > 50, "El recorte del Perú vino casi vacío. Revise la URL."
print(f"Tabla Perú: {len(sismos_peru)} sismos. OK")
```

Llame de nuevo a `resumen_calidad` y a `entrenar_error_por_gap`. Compare con Colombia.

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
