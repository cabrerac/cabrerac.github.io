<!-- NOTEBOOK: -->

`build_usgs_url` y `download_csv` son las funciones de la sesión 1. La primera arma la URL del catálogo USGS a partir de un diccionario. La segunda descarga el CSV y falla temprano si la respuesta no es el catálogo.

```python
def build_usgs_url(parametros: dict) -> str:
    """Arma la URL del catálogo USGS a partir de un diccionario de parámetros."""
    base = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    consulta = "&".join(f"{clave}={valor}" for clave, valor in parametros.items())
    return f"{base}?{consulta}"


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
```

<!-- end NOTEBOOK: -->
