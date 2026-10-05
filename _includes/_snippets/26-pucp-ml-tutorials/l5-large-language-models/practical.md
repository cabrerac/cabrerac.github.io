<!-- NOTEBOOK: -->

# Introducción práctica

Practicamos prompting, un RAG mínimo en memoria, y contrastamos con fine-tuning ligero (conceptual si no hay GPU).

## Objetivos

1. Diseñar prompts con criterios de aptitud.
2. Implementar retrieve y generate sobre un corpus pequeño en memoria.
3. Elegir prompt / RAG / FT para una viñeta y nombrar un riesgo y una mitigación.

```python
corpus = {
    "doc1": "La inspeccion visual no sustituye ensayos normados.",
    "doc2": "Los sensores acelerometricos requieren calibracion periodica.",
    "doc3": "Un modelo predictivo no aprueba por si solo un reforzamiento estructural.",
}

def retrieve(query, corpus, k=2):
    q = set(query.lower().split())
    scored = sorted(corpus.items(), key=lambda kv: len(q & set(kv[1].lower().split())), reverse=True)
    return scored[:k]

hits = retrieve("calibracion de sensores", corpus)
print(hits)
# Genera una respuesta condicionada a hits (API o plantilla offline)
```

### Ticket de salida

Viñeta: elige enfoque, un riesgo de mal uso, y una mitigación.

<!-- end NOTEBOOK: -->
