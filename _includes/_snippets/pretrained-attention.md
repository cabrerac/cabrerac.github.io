<!-- NOTEBOOK: -->

---

## Parte opcional: la atención de un modelo preentrenado

Si le queda tiempo, mire los pesos de atención del mismo modelo sobre la primera frase del párrafo. Es la misma operación de la parte A, aprendida con mucho más texto.

`AutoModel` carga el transformador sin la capa que predice tokens, unos 1 GB de descarga. Con GPU usamos `float16`, que ocupa la mitad de memoria. Sin GPU el mismo código corre en CPU con `float32`, solo más lento. `attn_implementation="eager"` pide la atención escrita paso a paso, la que devuelve los pesos.

```python
dispositivo = "cuda" if torch.cuda.is_available() else "cpu"
tipo = torch.float16 if dispositivo == "cuda" else torch.float32
modelo_hf = AutoModel.from_pretrained(MODELO_HF, dtype=tipo, attn_implementation="eager").to(dispositivo)
modelo_hf.eval()
print("dispositivo:", dispositivo,
      "| capas:", modelo_hf.config.num_hidden_layers,
      "| cabezas por capa:", modelo_hf.config.num_attention_heads)
```

`torch.no_grad()` evita guardar gradientes, porque solo leemos el modelo. `output_attentions=True` devuelve una matriz de pesos por capa y por cabeza. `last_hidden_state` es el vector final de cada token.

```python
frase = texto.split(". ")[0] + "."
entrada = tokenizador(frase, return_tensors="pt").to(dispositivo)
with torch.no_grad():
    salida_hf = modelo_hf(**entrada, output_attentions=True)
print("tokens:", entrada["input_ids"].shape[1],
      "| vectores finales:", tuple(salida_hf.last_hidden_state.shape))
```

Elija una capa y una cabeza. La primera capa es 0. En la capa 9, cabeza 5, las piezas de `movió` miran a las de `temblor`. Pruebe luego la capa 6, cabeza 0, que pone casi todo el peso en el primer token. Muchas cabezas hacen eso.

```python
CAPA, CABEZA = 9, 5
pesos_hf = salida_hf.attentions[CAPA][0, CABEZA].float().cpu()
mapa_atencion(pesos_hf.numpy(), piezas(frase), f"Qwen2.5-0.5B, capa {CAPA}, cabeza {CABEZA}")
```

**Comprobar:**

```python
assert len(salida_hf.attentions) == modelo_hf.config.num_hidden_layers
assert torch.all(pesos_hf[mascara_causal(len(pesos_hf))] == 0)
assert torch.allclose(pesos_hf.sum(dim=-1), torch.ones(len(pesos_hf)), atol=1e-2)
print("El modelo usa la misma máscara causal. OK")
```

<!-- end NOTEBOOK: -->
