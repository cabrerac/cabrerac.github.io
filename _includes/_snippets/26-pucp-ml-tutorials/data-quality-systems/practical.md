<!-- NOTEBOOK: -->

## Repaso de Python para este cuaderno

Estas celdas cubren solo lo que usaremos hoy: armar una URL, descargar un CSV y leerlo con pandas. Si ya lo domina, ejecútelas y siga. Si no, léalas antes de la Parte 1.

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

## Instrucciones

**Propósito.** Esta práctica es la sesión 1. El objetivo es **poner a disposición** un catálogo público de sismos y **evaluar** si esos registros sirven para una revisión post-terremoto, antes de entrenar ningún modelo.

La decisión de hoy es esta: después de un sismo en el Perú, ¿qué filas del catálogo están en condiciones de usarse para una revisión (dónde fue, qué tan grande, qué tan segura es la localización)?

Trabajamos con el catálogo del **USGS** (Servicio Geológico de Estados Unidos), no con un archivo de este curso. Usted construye la URL, descarga el CSV y lo revisa.

**Qué hacer (en orden).**

1. Lea cómo se arma la URL.
2. Abra el cuaderno en **Google Colab** o ejecútelo en local con Python 3.10+.
3. Ejecute las celdas **de arriba hacia abajo**.
4. En cada celda **Comprobar**, confirme el mensaje `OK` antes de seguir.
5. Cierre con el diagnóstico escrito. No borre filas todavía.

**La misma descarga en las sesiones siguientes.** Las constantes de abajo (fechas, magnitud mínima y ventana geográfica) no se cambian en octubre ni en noviembre. Así todas las sesiones ven las mismas filas.

| Constante | Valor | Papel |
|-----------|--------|--------|
| Inicio | 2024-01-01 | Primer instante incluido |
| Fin | 2025-01-01 | Límite superior (cubre todo 2024) |
| Magnitud mínima | 4.5 | Sismos que ya importan para una revisión |
| Latitud | -18.5 a 0.2 | Ventana del Perú, con un margen en la frontera |
| Longitud | -82 a -68 | Ventana del Perú, con un margen en la frontera |

Documentación del servicio (léala si una columna no se entiende): [USGS FDSN event API](https://earthquake.usgs.gov/fdsnws/event/1/).

---

### Cómo está armada la URL

El USGS publica el catálogo en `https://earthquake.usgs.gov/fdsnws/event/1/query`. Los parámetros van en la propia dirección. `format=csv` pide una tabla. El resto fija el recorte de este curso.

Esa URL **es** la decisión de acceso. Una magnitud mínima de 4.5 deja fuera sismos pequeños. La ventana geográfica deja fuera el resto del mundo. Lo que no se descarga no se puede evaluar después.

---

## Parte 1 — Acceso

Definimos el recorte una sola vez. `PARAMETROS_CURSO` es el contrato con las sesiones siguientes.

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
CATALOGO_CSV = Path("usgs_peru_2024_m45.csv")
```

`build_usgs_url` solo une la base y los parámetros. No descarga nada.

```python
def build_usgs_url(parametros: dict) -> str:
    """Arma la URL del catálogo USGS a partir de los parámetros del curso."""
    base = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    consulta = "&".join(f"{clave}={valor}" for clave, valor in parametros.items())
    return f"{base}?{consulta}"


USGS_URL = build_usgs_url(PARAMETROS_CURSO)
print(USGS_URL)
```

**Comprobar:**

```python
assert USGS_URL.startswith("https://earthquake.usgs.gov/fdsnws/event/1/query?")
assert "starttime=2024-01-01" in USGS_URL
assert "minmagnitude=4.5" in USGS_URL
print("URL del curso: OK")
```

---

### Paso 2 — Descargar el CSV

`download_csv` guarda la respuesta en disco y rechaza una página de error que no sea una tabla.

```python
def download_csv(url: str, dest: Path, timeout: int = 120) -> int:
    """Descarga url a dest y devuelve el número de bytes. Falla si no llega un CSV."""
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


bytes_descargados = download_csv(USGS_URL, CATALOGO_CSV)
print(f"Guardado: {CATALOGO_CSV}")
print(f"Tamaño: {bytes_descargados / 1e3:.1f} KB")
```

**Comprobar:**

```python
assert CATALOGO_CSV.is_file()
assert bytes_descargados > 5_000
print("Paso 2 — descarga: OK")
```

---

## Parte 2 — Leer la tabla

Access termina cuando la tabla está en memoria y sabemos qué columnas trajimos. Todavía no borramos nada.

```python
sismos = pd.read_csv(CATALOGO_CSV)
print("Filas, columnas:", sismos.shape)
print("Columnas:", list(sismos.columns))
sismos.head()
```

**Comprobar:**

```python
columnas_clave = ["time", "latitude", "longitude", "depth", "mag", "magType", "id", "place", "horizontalError", "gap", "status"]
faltan = [columna for columna in columnas_clave if columna not in sismos.columns]
assert not faltan, f"Faltan columnas: {faltan}"
assert len(sismos) > 50, "El recorte vino casi vacío. No cambie los parámetros."
print(f"Paso 2 — tabla: {len(sismos)} sismos. OK")
```

Cada fila es un sismo. `mag` es la magnitud. `depth` es la profundidad en kilómetros. `magType` dice qué escala se usó (`mb`, `mww`, `mwr` no son intercambiables sin más). `gap` es el hueco angular entre estaciones, en grados: un hueco grande deja la localización mal apoyada. `horizontalError` es la incertidumbre horizontal en kilómetros. `status` dice si el USGS ya revisó el registro.

---

## Parte 3 — Evaluación de calidad

La evaluación responde a la decisión, no a un puntaje genérico. Una fila sirve para la revisión si sabemos dónde fue, con qué magnitud, y con qué incertidumbre.

### Faltantes y duplicados

```python
faltantes = sismos.isna().sum().sort_values(ascending=False)
print("Valores faltantes por columna:")
print(faltantes[faltantes > 0])
if faltantes.sum() == 0:
    print("Ninguna celda vacía en este recorte.")

duplicados = int(sismos["id"].duplicated().sum())
print("Ids duplicados:", duplicados)
```

Un catálogo sin celdas vacías no está terminado. El recorte de magnitud 4.5 ya dejó fuera muchos registros peor determinados. Esa fue una decisión de acceso.

### Profundidad fija en 10 km

El USGS a veces publica la profundidad como **10 km** cuando no la pudo estimar. Esas filas no dicen que el sismo haya ocurrido a 10 km.

```python
profundidad_fija = sismos["depth"].round(3).eq(10)
print(f"Profundidad exactamente 10 km: {int(profundidad_fija.sum())} de {len(sismos)}")
sismos.loc[profundidad_fija, ["time", "place", "mag", "depth", "depthError"]].head()
```

### Escalas de magnitud mezcladas

```python
print(sismos["magType"].value_counts(dropna=False))
```

No compare un `mb` con un `mww` como si fueran el mismo número. Para una revisión basta con saber que la escala está declarada y que la magnitud supera el umbral del curso.

### Localización bastante incierta para elegir un distrito

Un error horizontal de más de 10 km, o un `gap` mayor que 90 grados, debilita la frase "este distrito".

```python
incertidumbre = (sismos["horizontalError"] > 10) | (sismos["gap"] > 90)
print(f"Localización débil para un distrito: {int(incertidumbre.sum())} de {len(sismos)}")
(
    sismos.loc[incertidumbre, ["place", "mag", "horizontalError", "gap"]]
    .sort_values("horizontalError", ascending=False)
    .head(8)
)
```

### Un resumen reutilizable

`resumen_calidad` junta los conteos. Las sesiones siguientes pueden llamar la misma función sobre el mismo CSV.

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


resumen = resumen_calidad(sismos)
print(resumen)
```

**Comprobar:**

```python
assert resumen["filas"] == len(sismos)
assert resumen["ids_duplicados"] == 0
assert resumen["profundidad_10km"] > 0, "Se esperaba al menos una profundidad fija en 10 km."
assert resumen["tipos_magnitud"] > 1
print("Parte 3 — evaluación: OK")
```

---

## Parte 4 — Su diagnóstico

No limpie el CSV. Escriba, con los números de `resumen`, si usaría este catálogo para una revisión post-terremoto y qué riesgo queda.

```python
diagnostico = """
Decision:
Criterios de exito:
Dos riesgos de calidad:
Que fila no usaria, y por que:
"""
print(diagnostico)
```

Guarde esta URL. Las sesiones del 12 de octubre, del 19 de octubre, del 23 de noviembre y del 30 de noviembre vuelven a descargar el mismo recorte.

```python
print(USGS_URL)
```

<!-- end NOTEBOOK: -->
