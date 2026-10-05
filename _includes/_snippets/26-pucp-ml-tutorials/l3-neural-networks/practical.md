<!-- NOTEBOOK: -->

# Introducción práctica

Entrenamos un FFN pequeño con disciplina train/val e introducimos una CNN mínima.

## Objetivos

1. Entrenar un MLP y reportar train vs validación.
2. Esbozar forward / loss / back-prop en palabras.
3. Probar un mini-CNN y escribir una frase de límite de decisión en campo.

```python
import torch
import torch.nn as nn
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

transform = transforms.ToTensor()
# train_ds = datasets.MNIST(root="./data", train=True, download=True, transform=transform)
# loader = DataLoader(train_ds, batch_size=64, shuffle=True)

class TinyMLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(nn.Flatten(), nn.Linear(28*28, 128), nn.ReLU(), nn.Linear(128, 10))
    def forward(self, x):
        return self.net(x)

print("Define TinyCNN (Conv2d -> ReLU -> MaxPool -> Flatten -> Linear) y compara con TinyMLP")
```

### Ticket de salida

Elige MLP o CNN para un caso civil y nombra **un límite** de la decisión que el modelo no resuelve solo.

<!-- end NOTEBOOK: -->
