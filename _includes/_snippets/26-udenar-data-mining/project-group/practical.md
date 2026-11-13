<!-- NOTEBOOK: -->

## Instrucciones

**Propósito.** Cuaderno del proyecto. Su grupo sigue como equipo interno de una alcaldía, con los artículos de su secretaría. Este cuaderno junta lo que ya hicieron en las semanas 1, 2 y 3 y escribe la **lista de inicio**.

**Este cuaderno.** Leen los archivos de las tres semanas. No vuelven a calcular pares, grupos, el filtro de texto, el grafo ni la predicción. El texto cuenta el camino, desde la pregunta de la semana 1 hasta la lista. El código escribe `outputs/lista_inicial.csv`.

**Antes de empezar.** Tengan a mano los ZIP de las tres semanas. La primera versión de la lista tiene que existir antes de las diapositivas del viernes 4 de diciembre, porque la charla del sábado 5 de diciembre presenta esa lista. El ZIP calificado es el del martes 8 dic, ya con la corrección después de la charla.

**Datos de entrada.** `outputs/patrones.csv` de la semana 1. `outputs/en_vista.csv` de la semana 2. `outputs/grafo.csv` y `outputs/prediccion.csv` de la semana 3. El documento de requerimientos ya tiene la pregunta y el problema. Aquí los vuelven a escribir, porque un disco de Colab no guarda el cuaderno anterior.

**Materiales.** [Semana 1](https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-data-mining/week-1-group.ipynb), [Semana 2](https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-data-mining/week-2-group.ipynb), [Semana 3](https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-data-mining/week-3-group.ipynb) y [L6 Predicción](https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-data-mining/l6-prediction.ipynb), Parte 6, para el armado de la lista.

**Pregunta del grupo.** ¿Qué artículos entran en la lista de inicio de su secretaría, qué resultados de las tres semanas apoyan a cada uno y qué hecho lo sacaría?

**Mapa del cuaderno**

| Ejercicio | Tema | Entregable clave |
|-----------|------|------------------|
| **0** | Configuración | Los cuatro archivos y el largo de la lista |
| **1** | Semana 1 | La pregunta, el problema y los pares que conservaron |
| **2** | Semana 2 | Qué artículos siguen en vista |
| **3** | Semana 3 | El lugar en la red y si la predicción cuenta |
| **4** | La lista | `outputs/lista_inicial.csv` |
| **5** | La charla | Título y resumen |

**Cómo leer cada paso.** Cada paso empieza con **En este paso**. Si el paso tiene código, termina con una celda **Comprobar**. Una Comprobar revisa que exista lo pedido, con su forma. No revisa el texto. Si falla, corrijan la celda anterior y vuelvan a ejecutar desde ahí.

---

## Ejercicio 0. Configuración

### Paso 0.1. Archivos y largo de la lista

En este paso suben los cuatro archivos y fijan el largo de la lista.
La lista tiene entre 10 y 30 artículos.

```python
from pathlib import Path

import pandas as pd

MIN_ARTICLES = 10
MAX_ARTICLES = 30
MIN_SUPPORTS = 2   # empiece en 2. 0 o 1 valen si el grupo lo explica

patterns = pd.read_csv("outputs/patrones.csv")
week2 = pd.read_csv("outputs/en_vista.csv")
graph = pd.read_csv("outputs/grafo.csv")
prediction = pd.read_csv("outputs/prediccion.csv")
```

**Listo cuando:**
- Los cuatro archivos están en `outputs/`.
- `MIN_SUPPORTS` es el número de resultados a favor que piden para que un artículo se lea. Lo justifican en el Paso 4.2.

**Comprobar:**

En este paso comprobamos que los cuatro archivos traen las columnas que el resto del cuaderno usa.

```python
assert {"pair", "kept"} <= set(patterns.columns)
assert {"title", "has_pattern", "read_group", "text_says_read", "prob_texto"} <= set(week2.columns)
assert {"title", "graph_support", "alerta_centro"} <= set(graph.columns)
assert {"title", "prediction"} <= set(prediction.columns)
assert MIN_ARTICLES < MAX_ARTICLES
print("Paso 0.1: OK")
```

---

## Ejercicio 1. Semana 1

### Paso 1.1. La pregunta, el problema y los pares

En este paso escriben la pregunta y el problema, los mismos del documento de requerimientos, y dicen qué pares conservaron.
Un par que conservan los tres métodos es un candidato más fuerte.
Un par que conserva un solo método no es el ganador.
La pregunta dice qué preguntaría una persona nueva, quién necesita la lista y qué puede y qué no puede decidir.
El problema nombra la secretaría, el archivo y que la lista es un inicio de lectura.

**ESCRIBA SU TEXTO AQUÍ**

**Listo cuando:**
- El texto tiene la pregunta, el problema y los pares que conservaron.
- Dice si los tres métodos coinciden o no.

---

## Ejercicio 2. Semana 2

### Paso 2.1. Qué artículos siguen en vista

En este paso dicen qué grupos y qué resultado de texto todavía apoyan a un artículo.
`outputs/en_vista.csv` es la vista de la semana 2. No es la lista de inicio.

```python
# SU CÓDIGO. Paso 2.1: WEEK2_READING

```

**Listo cuando:**
- `WEEK2_READING` nombra un artículo que sigue en vista y dice qué resultado de la semana 2 lo apoya.
- Dice también un artículo que esta semana no deja en vista, o por qué no hay ninguno.

**Comprobar:**

En este paso comprobamos que escribieron la lectura de la semana 2.

```python
assert WEEK2_READING.strip()
print("Paso 2.1: OK")
```

---

## Ejercicio 3. Semana 3

### Paso 3.1. El lugar en la red y la predicción

En este paso describen un artículo por su lugar entre los demás y dicen si la predicción cuenta.
Un artículo en el centro solo porque enlaza con muchos es una alerta, no una razón para dejarlo en la lista.

```python
# SU CÓDIGO. Paso 3.1: WEEK3_READING

```

**Listo cuando:**
- `WEEK3_READING` nombra un artículo, dice su lugar en la red y dice si `prediction` cuenta para ese artículo.
- Si el artículo tiene `alerta_centro`, el texto dice que esa alerta no es un apoyo.

**Comprobar:**

En este paso comprobamos que escribieron la lectura de la semana 3.

```python
assert WEEK3_READING.strip()
print("Paso 3.1: OK")
```

---

## Ejercicio 4. La lista

### Paso 4.1. Los resultados de cada artículo

En este paso juntan, por título, los resultados de las tres semanas.
No vuelvan a entrenar los métodos. Lean las columnas que ya están en los archivos.

| Columna | De dónde sale |
|---------|---------------|
| `has_pattern`, `read_group`, `text_says_read`, `prob_texto` | `week2` |
| `graph_support`, `alerta_centro` | `graph` |
| `prediction` | `prediction` |

```python
# SU CÓDIGO. Paso 4.1: table, una fila por título, con esas columnas

```

**Listo cuando:**
- `table` tiene una fila por título.
- Las columnas de apoyo son verdadero o falso.
- `alerta_centro` está en la tabla y no cuenta como resultado a favor.

**Comprobar:**

En este paso comprobamos que la tabla junta los tres archivos.

```python
assert len(table) == len(week2)
assert table["graph_support"].dtype == table["prediction"].dtype == bool
print("Paso 4.1: OK")
```

### Paso 4.2. Quién se lee

En este paso arman la lista de inicio.
Copien de la Lección 6, Parte 6, Pasos 3 a 5, el conteo de apoyos, el recorte y el orden.
`MIN_SUPPORTS` empieza en 2. Pueden cambiarlo. Muestren cuántos artículos tienen 0, 1, 2 y 3 o más resultados a favor, y expliquen el número que eligieron.
Los artículos que se leen son como mucho `MAX_ARTICLES`. Si quedan menos de `MIN_ARTICLES`, no rellenen. Impriman que el resultado es débil.
Un artículo con `alerta_centro` solo queda por sus otros resultados.

| Qué copiar | Dónde está en L6 |
|------------|------------------|
| `SUPPORT_COLUMNS`, `supports` e `in_view` | Parte 6, Paso 3 |
| `drop_one` | Parte 6, Paso 4 |
| `starter_list`, con `recortado` | Parte 6, Paso 5 |

```python
# SU CÓDIGO. Paso 4.2: SUPPORT_COLUMNS, supports, in_view, drop_one, starter_list y SUPPORT_CHOICE

```

**Listo cuando:**
- `starter_list` trae `alerta_centro`, `supports`, `prob_texto` y `recortado`.
- `SUPPORT_CHOICE` (texto) dice qué valor de `MIN_SUPPORTS` usaron y por qué.

**Comprobar:**

En este paso comprobamos el rango de apoyos y que escribieron la elección.

```python
assert starter_list["supports"].between(0, len(SUPPORT_COLUMNS)).all()
assert starter_list["alerta_centro"].dtype == bool and SUPPORT_CHOICE.strip()
print("Paso 4.2: OK")
```

### Paso 4.3. Qué hecho sacaría cada artículo

En este paso escriben qué hecho sacaría cada artículo que se lee.
Usen `drop_one` de la Lección 6, Parte 6, Paso 4, para ver de qué resultado depende más la lista.

```python
# SU CÓDIGO. Paso 4.3: hecho_que_saca, la columna en starter_list, y WHAT_CHANGES

```

**Listo cuando:**
- `hecho_que_saca` es un diccionario de título a un hecho concreto. Ningún artículo que se lee queda vacío.
- `WHAT_CHANGES` (texto) dice de qué resultado depende más la lista y qué la cambiaría.

**Comprobar:**

En este paso comprobamos la columna y el texto.

```python
assert "hecho_que_saca" in starter_list and WHAT_CHANGES.strip()
print("Paso 4.3: OK")
```

### Paso 4.4. Guardar la lista

En este paso guardan `outputs/lista_inicial.csv`.

| Columna | Qué es |
|---------|--------|
| las de `SUPPORT_COLUMNS` | cada resultado, en verdadero o falso |
| `title`, `supports`, `prob_texto`, `recortado`, `alerta_centro`, `hecho_que_saca` | la lista, el recorte, la alerta y el hecho |

```python
# SU CÓDIGO. Paso 4.4: outputs/lista_inicial.csv

```

**Listo cuando:**
- El archivo existe y tiene esas columnas.

**Comprobar:**

En este paso comprobamos que la lista quedó guardada.

```python
saved = pd.read_csv("outputs/lista_inicial.csv")
assert {"title", "supports", "recortado", "alerta_centro", "hecho_que_saca"} <= set(saved.columns)
print("Paso 4.4: OK")
```

---

## Ejercicio 5. La charla

### Paso 5.1. Título y resumen

En este paso escriben el título y el resumen de la charla del sábado 5 de diciembre.
Las diapositivas se entregan el viernes 4 de diciembre. Este texto es la fuente.

| Qué ver | Dónde está |
|---------|------------|
| El formato | [project-title-es.example.txt](https://cabrerac.github.io/assets/documents/26-udenar-data-mining/project-title-es.example.txt) y [project-abstract-es.example.txt](https://cabrerac.github.io/assets/documents/26-udenar-data-mining/project-abstract-es.example.txt). Están escritos sobre el laboratorio de artículos. No sirven para copiar. |

```python
# SU CÓDIGO. Paso 5.1: project_title y project_abstract, guardados con write_text(..., encoding="utf-8")

```

**Listo cuando:**
- `project-title-es.txt` tiene menos de 15 palabras.
- `project-abstract-es.txt` es un párrafo de unas 120 palabras. Nombra la secretaría, la pregunta de la persona nueva, los resultados que apoyan la lista y un hecho que sacaría un artículo.

**Comprobar:**

En este paso comprobamos que el título tiene menos de 15 palabras.

```python
assert 0 < len(Path("project-title-es.txt").read_text(encoding="utf-8").split()) < 15
print("Paso 5.1: OK")
```

## Registro de contribución

En este paso cada integrante anota su tarea concreta y el grupo dice quién consolida el ZIP.

```python
# SU CÓDIGO. Registro: contribution_log, una línea por integrante y quién consolida el ZIP

```

**Listo cuando:**
- `contribution_log` (texto) tiene una línea con una tarea concreta por integrante y dice quién consolidó el ZIP.

## Para la reflexión individual

Use la [plantilla de la reflexión del proyecto](https://cabrerac.github.io/assets/documents/26-udenar-data-mining/project-reflection-template.docx) y mantenga sus títulos. Extensión: entre 800 y 1200 palabras. Por debajo de 500 palabras el texto queda corto. Se entrega el miércoles 9 dic 2026, 23:59 (hora de Colombia). No va dentro del ZIP.

| Título | Qué escribir |
|--------|--------------|
| **Metadatos** | Nombre, grupo, proyecto, conteo aproximado de palabras y la lectura que cita. |
| **Proceso** | Qué hizo el grupo en este cuaderno. Diga cuál fue su contribución. |
| **Decisión** | Elija un artículo de `outputs/lista_inicial.csv` que se lee. Diga qué resultados de las tres semanas lo apoyan y qué hecho lo sacaría. |
| **Métodos** | Explique cómo se comparan los resultados de las tres semanas cuando deciden quién se queda. |
| **Ética** | Nombre una elección técnica del proyecto. Diga a quién ayuda o perjudica, o cómo se podría usar mal la lista. Relacione el punto con una lectura del curso, por autor y año. |

## Entrega

El ZIP se entrega el martes 8 dic 2026, 23:59 (hora de Colombia), con el cuaderno ejecutado y renombrado.
Las diapositivas van en su propia tarea, el viernes 4 de diciembre. No van en este ZIP.
No hay nota de portada.

| Archivo del ZIP `project-<group_id>.zip` | Descripción |
|------------------------------------------|-------------|
| `project-group-<group_id>.ipynb` | Este cuaderno ejecutado |
| `project-requirements-<group_id>.pdf` | El documento de requerimientos, con la devolución del sábado 14 aplicada |
| `outputs/lista_inicial.csv` | La lista de inicio, con los resultados que apoyan cada artículo, `recortado`, `alerta_centro` y `hecho_que_saca` |
| `project-title-es.txt` | El título de la charla, con menos de 15 palabras |
| `project-abstract-es.txt` | El resumen de la charla, un párrafo de unas 120 palabras |

La lista de inicio es el producto del proyecto. Cada artículo que se lee se apoya en los resultados de las tres semanas.

<!-- end NOTEBOOK: -->
